from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.structural.generalized_geometry_benchmarks import (
    CASE_IDS,
    GeneralizedBenchmarkViolation,
    adjudicate_mesh_evidence,
    discrete_response,
    evaluate_case,
    failure_indicators,
    response_reference,
    scalar_constitutive_evidence,
    severed_edge_control,
    validate_config,
    validate_severed_edge_control,
    validate_source_evidence,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/structural/generalized_geometry_benchmarks_v1.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def witness(case: dict) -> dict:
    sections = [
        {"path_fraction": fraction, "area_m2": area, "equivalent_radius_m": 0.05, "second_moment_proxy_m4": inertia}
        for fraction, area, inertia in ((0.0, 0.012, 1.2e-5), (0.5, 0.010, 1.0e-5), (1.0, 0.008, 0.8e-5))
    ]
    return {
        "candidate_id": case["source_candidate_id"],
        "solid_count": 2 if case["case_id"] == "contact_pair" else 1,
        "section_evolution": {"samples": sections},
        "thickness_field": {"minimum_sampled_span_m": 0.01},
        "regions": [
            {"region_id": "support_region", "region_signature_sha256": "1" * 64},
            {"region_id": "load_region", "region_signature_sha256": "2" * 64},
            {"region_id": "contact_region", "region_signature_sha256": "3" * 64},
        ],
        "path_witness": {"path_length_m": 1.0, "minimum_sampled_bend_radius_m": 0.2},
        "curvature_spectrum": {"curvature_sample_count": 24},
    }


class GeneralizedGeometryBenchmarkTests(unittest.TestCase):
    def test_config_freezes_seven_nonprimitive_sources_and_complete_coverage(self) -> None:
        result = validate_config(load_config())
        self.assertEqual(CASE_IDS, tuple(item["case_id"] for item in load_config()["cases"]))
        self.assertEqual(7, result["case_count"])
        self.assertEqual(["beam", "contact", "shell", "solid"], result["model_coverage"])
        self.assertEqual(["bearing_preload", "bonded", "hertz_frictional", "sliding_friction"], result["contact_law_coverage"])

    def test_all_seven_cross_method_adapters_pass_with_machine_readable_justification(self) -> None:
        config = load_config()
        results = [evaluate_case(config, case, witness(case)) for case in config["cases"]]
        self.assertEqual(set(CASE_IDS), {item["case_id"] for item in results})
        self.assertEqual({"beam", "shell", "solid", "contact"}, {item["model_selection"]["selected_model"] for item in results})
        self.assertTrue(all(item["model_selection"]["justification"] for item in results))
        self.assertTrue(all(item["contact_state"]["valid"] for item in results))
        self.assertTrue(all(item["connection_transition"]["to_state"] == "intact" for item in results))
        self.assertTrue(all(item["design_use_allowed"] is False for item in results))

    def test_primitive_substitution_missing_region_and_model_mismatch_fail_closed(self) -> None:
        config = load_config()
        changed = deepcopy(config); changed["cases"][0]["source_candidate_id"] = "box_primitive_001"
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "non-primitive source"):
            validate_config(changed)
        case = config["cases"][0]; missing = witness(case); missing["regions"].pop()
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "semantic region"):
            evaluate_case(config, case, missing)
        mismatch = deepcopy(case); mismatch["expected_model"] = "solid"
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "frozen expectation"):
            evaluate_case(config, mismatch, witness(case))

    def test_nonrefining_levels_and_contact_law_mutation_fail_config(self) -> None:
        config = load_config(); changed = deepcopy(config); changed["cases"][0]["discrete_levels"] = [8, 16, 16]
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "levels"):
            validate_config(changed)
        changed = deepcopy(config); changed["cases"][6]["contact_law"] = "silent_penalty_fallback"
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "identity, model, or law"):
            validate_config(changed)

    def test_nonfinite_response_excess_residual_and_nonconvergence_fail_adjudication(self) -> None:
        config = load_config(); case = config["cases"][0]; geometry = witness(case)
        reference = response_reference(case, geometry, config["material"])
        levels = [discrete_response(case, geometry, config["material"], level) for level in case["discrete_levels"]]
        bad = deepcopy(levels); bad[-1]["response_m"] = math.nan
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "finite"):
            adjudicate_mesh_evidence(config["tolerances"], reference, bad)
        bad = deepcopy(levels); bad[-1]["force_residual_relative"] = 1e-3
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "force_residual"):
            adjudicate_mesh_evidence(config["tolerances"], reference, bad)
        bad = deepcopy(levels); bad[-1]["solver_converged"] = False
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "did not converge"):
            adjudicate_mesh_evidence(config["tolerances"], reference, bad)

    def test_forced_divergence_stays_invalid_without_fallback(self) -> None:
        config = load_config(); case = config["cases"][0]
        result = evaluate_case(config, case, witness(case), force_divergence=True)
        self.assertEqual("invalid", result["status"])
        self.assertEqual("solver_divergence", result["reason"])
        self.assertFalse(result["fallback_used"])

    def test_field_balance_is_unavailable_instead_of_fabricated_zero(self) -> None:
        config = load_config()
        for case in config["cases"]:
            with self.subTest(case=case["case_id"]):
                result = evaluate_case(config, case, witness(case))
                self.assertFalse(result["full_balance_validated"])
                self.assertEqual("not_evaluated_no_field_solution", result["balance_gate_status"])
                for level in result["mesh_results"]:
                    for key in ("force_residual_relative", "moment_residual_relative", "energy_residual_relative"):
                        self.assertIsNone(level[key])
                    self.assertEqual("scalar_constitutive_only", level["equilibrium_evidence"])

    def test_linear_spring_work_and_perturbed_equilibrium(self) -> None:
        # A 400 N/m spring at 0.02 m holds 8 N and stores 0.08 J.
        balanced = scalar_constitutive_evidence(0.02, 8.0, 400.0)
        self.assertAlmostEqual(0.08, balanced["stored_energy"])
        self.assertTrue(balanced["solver_converged"])
        perturbed = scalar_constitutive_evidence(0.021, 8.0, 400.0)
        self.assertAlmostEqual(0.05, perturbed["generalized_equilibrium_residual_relative"])
        self.assertGreater(perturbed["constitutive_energy_residual_relative"], 0.04)
        self.assertFalse(perturbed["solver_converged"])

    def test_hertz_energy_is_integral_of_force_and_has_correct_derivative(self) -> None:
        # K=1e6 N/m^(3/2), delta=1e-4 m -> F=1 N, U=4e-5 J.
        delta = 1e-4
        value = scalar_constitutive_evidence(delta, 1.0, 1e6, exponent=1.5)
        self.assertAlmostEqual(4e-5, value["stored_energy"], places=15)
        self.assertNotAlmostEqual(5e-5, value["stored_energy"], places=8)
        count = 10000
        width = delta / count
        integrated = math.fsum(1e6 * ((i + 0.5) * width) ** 1.5 for i in range(count)) * width
        self.assertAlmostEqual(integrated / value["stored_energy"], 1.0, places=8)
        h = delta * 1e-5
        up = scalar_constitutive_evidence(delta + h, 1.0, 1e6, exponent=1.5)["stored_energy"]
        down = scalar_constitutive_evidence(delta - h, 1.0, 1e6, exponent=1.5)["stored_energy"]
        self.assertAlmostEqual(1.0, (up - down) / (2 * h), places=9)
        self.assertFalse(scalar_constitutive_evidence(1.1 * delta, 1.0, 1e6, exponent=1.5)["solver_converged"])

    def test_hertz_pressure_indentation_use_same_modulus_and_radius(self) -> None:
        config = load_config(); case = deepcopy(config["cases"][-1]); geometry = witness(case)
        material = deepcopy(config["material"])
        material.update(youngs_modulus_pa=1.5e6, poisson_ratio=0.0)
        case.update(load_n=1.0, temperature_delta_k=0.0)
        geometry["path_witness"]["minimum_sampled_bend_radius_m"] = 1.0
        # Thickness must not silently clamp the supplied effective radius.
        geometry["thickness_field"]["minimum_sampled_span_m"] = 2.0
        response = response_reference(case, geometry, material)["response_m"]
        pressure = failure_indicators(case, geometry, material)["stress_pa"]["contact"]
        self.assertAlmostEqual(1e-4, response, places=14)
        self.assertAlmostEqual(4774.64829275686, pressure, places=8)
        # Different E and nu with the same E* must give the same contact result.
        material.update(youngs_modulus_pa=1.40625e6, poisson_ratio=0.25)
        self.assertAlmostEqual(response, response_reference(case, geometry, material)["response_m"], places=14)
        self.assertAlmostEqual(pressure, failure_indicators(case, geometry, material)["stress_pa"]["contact"], places=8)
        material.update(youngs_modulus_pa=1.5e6, poisson_ratio=0.0)
        # Independently integrate p(r)=p0*sqrt(1-r^2/a^2) over a=0.01 m.
        self.assertAlmostEqual(1.0, 2 * math.pi * pressure * 0.01 ** 2 / 3, places=12)
        case["load_n"] = 8.0
        self.assertAlmostEqual(4 * response, response_reference(case, geometry, material)["response_m"], places=14)
        self.assertAlmostEqual(2 * pressure, failure_indicators(case, geometry, material)["stress_pa"]["contact"], places=8)
        case["load_n"] = 1.0; material["youngs_modulus_pa"] *= 8
        self.assertAlmostEqual(response / 4, response_reference(case, geometry, material)["response_m"], places=14)
        self.assertAlmostEqual(4 * pressure, failure_indicators(case, geometry, material)["stress_pa"]["contact"], places=8)

    def test_pressure_work_has_energy_per_area_units(self) -> None:
        config = load_config(); case = config["cases"][2]
        result = discrete_response(case, witness(case), config["material"], 48)
        self.assertEqual("Pa", result["generalized_load_unit"])
        self.assertEqual("J/m^2", result["energy_unit"])
        self.assertAlmostEqual(0.5 * case["pressure_pa"] * result["response_m"], result["stored_energy"])
        self.assertIsNone(result["energy_residual_relative"])

    def test_actual_newton_budget_exhaustion_is_invalid(self) -> None:
        config = load_config(); case = deepcopy(config["cases"][-1]); geometry = witness(case)
        first = discrete_response(case, geometry, config["material"], 1)
        self.assertFalse(first["solver_converged"])
        self.assertGreater(first["generalized_equilibrium_residual_relative"], 1e-3)
        self.assertEqual(2, len(first["nonlinear_residual_history"]))
        case["discrete_levels"] = [1, 2, 4]
        invalid = evaluate_case(config, case, geometry)
        self.assertEqual("invalid", invalid["status"])
        self.assertFalse(invalid["fallback_used"])
        solved = discrete_response(case, geometry, config["material"], 32)
        self.assertTrue(solved["solver_converged"])
        self.assertLess(solved["effective_elements_or_iterations"], 32)
        self.assertLessEqual(solved["nonlinear_residual_history"][-1], 1e-12)

    def test_invalid_constitutive_domains_are_rejected(self) -> None:
        for response, load, stiffness in [(0, 1, 1), (-1, 1, 1), (1, 0, 1), (1, 1, -1), (math.nan, 1, 1), (1, math.inf, 1)]:
            with self.subTest(values=(response, load, stiffness)):
                with self.assertRaises(GeneralizedBenchmarkViolation):
                    scalar_constitutive_evidence(response, load, stiffness)
        config = load_config(); case = config["cases"][-1]; geometry = witness(case)
        geometry["path_witness"]["minimum_sampled_bend_radius_m"] = 0.0
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "radius"):
            response_reference(case, geometry, config["material"])
        for level in [0, -1, True, 1.5]:
            with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "positive integer"):
                discrete_response(case, witness(case), config["material"], level)

    def test_adjudication_rejects_stale_forged_and_incomplete_evidence(self) -> None:
        config = load_config(); case = config["cases"][0]; geometry = witness(case)
        reference = response_reference(case, geometry, config["material"])
        levels = [discrete_response(case, geometry, config["material"], n) for n in case["discrete_levels"]]
        mutations = [
            ("force_residual_relative", 0.0), ("moment_residual_relative", 0.0),
            ("energy_residual_relative", 0.0), ("full_balance_validated", True),
            ("evaluator_version", "old"), ("stored_energy", 0.0),
            ("reference_relative_error", 0.0), ("level", 16),
            ("response_m", levels[-1]["response_m"] * 1.1),
        ]
        for key, value in mutations:
            with self.subTest(key=key):
                bad = deepcopy(levels); bad[-1][key] = value
                with self.assertRaises(GeneralizedBenchmarkViolation):
                    adjudicate_mesh_evidence(config["tolerances"], reference, bad)
        bad = deepcopy(levels); del bad[-1]["force_residual_relative"]
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "unavailable"):
            adjudicate_mesh_evidence(config["tolerances"], reference, bad)

    def test_severed_edge_propagates_paths_and_nonzero_transmission_is_rejected(self) -> None:
        case = load_config()["cases"][3]; control = severed_edge_control(case)
        validate_severed_edge_control(control)
        self.assertEqual(case["affected_path_ids"], control["affected_path_ids"])
        changed = deepcopy(control); changed["transmitted_force_n"] = 1e-9
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "noncausal"):
            validate_severed_edge_control(changed)

    def test_work096_hash_mutation_and_hidden_repair_fail_closed(self) -> None:
        source = load_config()["source"]
        semantic = {"config_sha256": source["semantic_config_sha256"]}
        report = {"report_sha256": source["freecad_report_sha256"], "hidden_geometry_repair": False}
        comparison = {"comparison_sha256": source["semantic_comparison_sha256"]}
        validate_source_evidence(source, semantic, report, comparison, comparison)
        changed = deepcopy(report); changed["report_sha256"] = "0" * 64
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "identity mismatch"):
            validate_source_evidence(source, semantic, changed, comparison, comparison)
        changed = deepcopy(report); changed["hidden_geometry_repair"] = True
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "repair"):
            validate_source_evidence(source, semantic, changed, comparison, comparison)

    def test_failure_controls_and_design_boundary_are_frozen_before_observation(self) -> None:
        config = load_config()
        self.assertFalse(config["failure_controls"]["post_observation_failure_repair_allowed"])
        self.assertFalse(config["evidence_policy"]["design_use_allowed"])
        changed = deepcopy(config); changed["failure_controls"]["post_observation_failure_repair_allowed"] = True
        with self.assertRaisesRegex(GeneralizedBenchmarkViolation, "failure controls"):
            validate_config(changed)


if __name__ == "__main__":
    unittest.main()
