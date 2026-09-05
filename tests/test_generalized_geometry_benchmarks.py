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
    response_reference,
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
