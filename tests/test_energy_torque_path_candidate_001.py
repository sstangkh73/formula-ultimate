from __future__ import annotations

import json
import math
from pathlib import Path
import unittest


from formula_ultimate.subsystems.energy_torque_path import (
    EnergyTorquePathViolation,
    canonical_sha256,
    evaluate_candidate,
    unique_path_count,
    validate_declaration,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/candidates/energy_torque_path_candidate_001.json"
WORK083_RESULT_SHA256 = "a061d0b2de7b01eb31233cd3ed1ab9945eb5dbc015ca478c26fb9b77fbfaded3"
WORK083_ASSEMBLY_SHA256 = "57dc477bbec58da05a0908d1b9b8de04c57a482f710c2362980fed8c51ccb135"
WORK083_AXLE_SHA256 = "b44add5cc5a31471947d2dbf614ae78c4187384059677e7107dd7151b4e470ef"


def _raw() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def _independent_areas(raw: dict) -> tuple[float, float]:
    """Recompute the frozen surface deltas here so a module formula change cannot pass silently."""
    housing = raw["parts"][1]["geometry"]
    radius = housing["coolant_passage_radius_m"]
    length = housing["box_size_m"][1]
    coolant = len(housing["coolant_passage_x_m"]) * 2.0 * math.pi * radius * (length - radius)
    fins = len(housing["fin_center_y_m"]) * 2.0 * housing["fin_height_m"] * (
        housing["fin_length_m"] + housing["fin_thickness_m"]
    )
    return coolant, fins


def _reseal_manifest(manifest: dict, freecad: dict) -> None:
    body = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    manifest["manifest_sha256"] = canonical_sha256(body)
    freecad["source_manifest_sha256"] = manifest["manifest_sha256"]
    _reseal_freecad(freecad)


def _reseal_freecad(freecad: dict) -> None:
    body = {key: value for key, value in freecad.items() if key != "report_sha256"}
    freecad["report_sha256"] = canonical_sha256(body)


def _fixtures() -> tuple[dict, dict, dict, dict]:
    raw = _raw()
    density = raw["material"]["density_kg_per_m3"]
    part_ids = [part["part_id"] for part in raw["parts"]]
    volumes = {
        "energy_store": 1.918869e-4,
        "converter_housing": 1.870833e-4,
        "converter_rotor": math.pi * 0.024**2 * 0.040,
        "input_shaft": math.pi * 0.010**2 * 0.050,
        "ratio_drum": math.pi * (0.030**2 - 0.006**2) * 0.024,
        "output_shaft": math.pi * 0.0058**2 * 0.067,
        "support_block": 0.082 * 0.018 * 0.0162 - math.pi * 0.0068**2 * 0.018,
    }
    parts = [
        {
            "part_id": part_id,
            "step_file": f"{part_id}.step",
            "step_sha256": format(index + 1, "064x"),
            "valid": True,
            "solid_count": 1,
            "volume_m3": volumes[part_id],
            "mass_kg": volumes[part_id] * density,
        }
        for index, part_id in enumerate(part_ids)
    ]

    contact = {tuple(sorted(pair)) for pair in raw["clearance"]["contact_pairs"]}
    coupling = {tuple(sorted(pair)) for pair in raw["clearance"]["coupling_pairs"]}
    pair_clearance = []
    for index, first in enumerate(part_ids):
        for second in part_ids[index + 1:]:
            key = tuple(sorted((first, second)))
            if key in contact:
                record = {"classification": "contact", "clearance_m": 0.0}
            elif key in coupling:
                record = {"classification": "coupling", "clearance_m": 0.0002}
            else:
                record = {"classification": "forbidden", "clearance_m": 0.001}
            pair_clearance.append({"parts": list(key), "overlap_m3": 0.0, **record})

    coolant_delta, fin_delta = _independent_areas(raw)
    body = {
        "candidate_id": raw["candidate_id"],
        "declaration_sha256": canonical_sha256(raw),
        "hidden_geometry_repair": False,
        "parts": parts,
        "assembly": {
            "step_file": "energy_torque_path_candidate_001.step",
            "step_sha256": "a" * 64,
            "valid": True,
            "solid_count": 7,
            "volume_m3": math.fsum(volumes.values()),
        },
        "derived": {
            "store_cavity_volume_m3": 0.080 * 0.106 * 0.072,
            "housing_coolant_area_delta_m2": coolant_delta,
            "housing_fin_area_delta_m2": fin_delta,
            "output_shaft_interface": {
                "y_m": 0.019,
                "radius_m": 0.0058,
                "axis_x_m": -0.040,
                "axis_z_m": -0.104,
            },
            "drum_ground_clearance_m": 0.005,
        },
        "pair_clearance": pair_clearance,
    }
    manifest = {**body, "manifest_sha256": canonical_sha256(body)}

    freecad_body = {
        "source_manifest_sha256": manifest["manifest_sha256"],
        "freecad_version": "1.1.3",
        "occt_version": "7.8.1",
        "hidden_geometry_repair": False,
        "parts": [
            {"part_id": part["part_id"], "step_sha256": part["step_sha256"], "valid": True, "solid_count": 1}
            for part in parts
        ],
        "assembly": {"valid": True, "solid_count": 7},
    }
    freecad = {**freecad_body, "report_sha256": canonical_sha256(freecad_body)}

    work083 = {
        "status": "passed",
        "candidate_verdict": "not_admitted_synthetic_evidence",
        "design_use_allowed": False,
        "result_sha256": WORK083_RESULT_SHA256,
        "assembly_step_sha256": WORK083_ASSEMBLY_SHA256,
        "part_step_sha256": {"axle": WORK083_AXLE_SHA256},
    }
    return raw, manifest, freecad, work083


class EnergyTorquePathDeclarationTests(unittest.TestCase):
    def test_reference_declaration_has_seven_parts_and_one_dof(self) -> None:
        result = validate_declaration(_raw())
        self.assertEqual(
            result["part_ids"],
            [
                "energy_store", "converter_housing", "converter_rotor", "input_shaft",
                "ratio_drum", "output_shaft", "support_block",
            ],
        )
        self.assertEqual(result["mobility_dof"], 1)
        self.assertEqual(result["torque_ratio"], 3.0)
        self.assertEqual(
            result["paths"],
            {"torque_path_count": 1, "reaction_path_count": 1, "recovery_path_count": 1},
        )

    def test_unknown_declaration_field_fails_closed(self) -> None:
        raw = _raw()
        raw["unregistered"] = True
        with self.assertRaisesRegex(EnergyTorquePathViolation, "fields mismatch"):
            validate_declaration(raw)

    def test_joint_constraint_change_cannot_fake_mobility(self) -> None:
        raw = _raw()
        raw["joints"][3]["constraint_rows"] = 6
        with self.assertRaisesRegex(EnergyTorquePathViolation, "constraint rows"):
            validate_declaration(raw)

    def test_removing_the_coupling_row_changes_calculated_mobility(self) -> None:
        raw = _raw()
        raw["couplings"][0]["constraint_rows"] = 0
        with self.assertRaisesRegex(EnergyTorquePathViolation, "one rolling constraint row"):
            validate_declaration(raw)

    def test_transformation_must_change_torque_magnitude(self) -> None:
        raw = _raw()
        raw["couplings"][0]["driven_radius_m"] = raw["couplings"][0]["drive_radius_m"]
        with self.assertRaisesRegex(EnergyTorquePathViolation, "change the torque magnitude"):
            validate_declaration(raw)

    def test_declared_efficiency_above_maximum_is_rejected(self) -> None:
        raw = _raw()
        raw["drive_case"]["converter_efficiency"] = 1.0
        with self.assertRaisesRegex(EnergyTorquePathViolation, "efficiency exceeds the maximum"):
            validate_declaration(raw)

    def test_external_primary_inflow_must_be_zero(self) -> None:
        raw = _raw()
        raw["energy_store_state"]["external_primary_inflow_j"] = 1.0
        with self.assertRaisesRegex(EnergyTorquePathViolation, "external primary energy inflow"):
            validate_declaration(raw)

    def test_brake_torque_must_oppose_rotation(self) -> None:
        raw = _raw()
        raw["brake_case"]["output_brake_torque_nm"] = 12.0
        with self.assertRaisesRegex(EnergyTorquePathViolation, "oppose positive rotation"):
            validate_declaration(raw)

    def test_severed_torque_edge_is_rejected(self) -> None:
        raw = _raw()
        raw["paths"]["torque_edges"].pop()
        with self.assertRaisesRegex(EnergyTorquePathViolation, "torque path"):
            validate_declaration(raw)

    def test_severed_reaction_edge_is_rejected(self) -> None:
        raw = _raw()
        raw["paths"]["reaction_edges"].pop()
        with self.assertRaisesRegex(EnergyTorquePathViolation, "reaction path"):
            validate_declaration(raw)

    def test_meshed_solver_evidence_cannot_be_claimed(self) -> None:
        raw = _raw()
        raw["structural_analytic"]["meshed_solver_evidence"] = True
        with self.assertRaisesRegex(EnergyTorquePathViolation, "no meshed solver evidence"):
            validate_declaration(raw)

    def test_nonfinite_values_fail_closed(self) -> None:
        raw = _raw()
        raw["drive_case"]["rotor_angular_speed_rad_s"] = float("nan")
        with self.assertRaisesRegex(EnergyTorquePathViolation, "finite domain"):
            validate_declaration(raw)


class EnergyTorquePathEvidenceTests(unittest.TestCase):
    def test_geometry_identity_change_fails_closed(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        manifest["parts"][2]["step_sha256"] = "f" * 64
        with self.assertRaisesRegex(EnergyTorquePathViolation, "manifest identity"):
            evaluate_candidate(raw, manifest, freecad, work083)

    def test_mass_must_be_geometry_derived(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        manifest["parts"][0]["mass_kg"] *= 0.5
        _reseal_manifest(manifest, freecad)
        with self.assertRaisesRegex(EnergyTorquePathViolation, "not geometry-derived"):
            evaluate_candidate(raw, manifest, freecad, work083)

    def test_forbidden_clearance_below_gate_is_rejected(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        for record in manifest["pair_clearance"]:
            if record["classification"] == "forbidden":
                record["clearance_m"] = 0.0001
                break
        _reseal_manifest(manifest, freecad)
        with self.assertRaisesRegex(EnergyTorquePathViolation, "below the frozen clearance gate"):
            evaluate_candidate(raw, manifest, freecad, work083)

    def test_reclassifying_a_forbidden_pair_is_rejected(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        for record in manifest["pair_clearance"]:
            if record["classification"] == "forbidden":
                record["classification"] = "contact"
                break
        _reseal_manifest(manifest, freecad)
        with self.assertRaisesRegex(EnergyTorquePathViolation, "wrong clearance classification"):
            evaluate_candidate(raw, manifest, freecad, work083)

    def test_interference_beyond_the_gate_is_rejected(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        manifest["pair_clearance"][0]["overlap_m3"] = 1e-6
        _reseal_manifest(manifest, freecad)
        with self.assertRaisesRegex(EnergyTorquePathViolation, "interfere beyond the frozen gate"):
            evaluate_candidate(raw, manifest, freecad, work083)

    def test_cooling_area_must_match_the_frozen_geometry(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        manifest["derived"]["housing_fin_area_delta_m2"] *= 1.5
        _reseal_manifest(manifest, freecad)
        with self.assertRaisesRegex(EnergyTorquePathViolation, "fin area disagrees"):
            evaluate_candidate(raw, manifest, freecad, work083)

    def test_output_shaft_must_meet_the_frozen_work083_interface(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        manifest["derived"]["output_shaft_interface"]["y_m"] = 0.025
        _reseal_manifest(manifest, freecad)
        with self.assertRaisesRegex(EnergyTorquePathViolation, "Work 083 axle end plane"):
            evaluate_candidate(raw, manifest, freecad, work083)

    def test_transformation_body_may_not_reach_the_ground_plane(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        manifest["derived"]["drum_ground_clearance_m"] = -0.001
        _reseal_manifest(manifest, freecad)
        with self.assertRaisesRegex(EnergyTorquePathViolation, "reaches the declared ground plane"):
            evaluate_candidate(raw, manifest, freecad, work083)

    def test_freecad_must_retain_separate_solids(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        freecad["assembly"]["solid_count"] = 1
        _reseal_freecad(freecad)
        with self.assertRaisesRegex(EnergyTorquePathViolation, "separate solids"):
            evaluate_candidate(raw, manifest, freecad, work083)

    def test_work083_identity_mismatch_fails_closed(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        work083["part_step_sha256"]["axle"] = "b" * 64
        with self.assertRaisesRegex(EnergyTorquePathViolation, "axle identity mismatch"):
            evaluate_candidate(raw, manifest, freecad, work083)

    def test_work083_synthetic_evidence_cannot_be_relabelled(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        work083["design_use_allowed"] = True
        with self.assertRaisesRegex(EnergyTorquePathViolation, "relabelled"):
            evaluate_candidate(raw, manifest, freecad, work083)


class EnergyTorquePathReferenceTests(unittest.TestCase):
    def test_reference_evaluation_closes_every_declared_ledger(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        result = evaluate_candidate(raw, manifest, freecad, work083)
        physics = result["physics"]
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["candidate_verdict"], "not_admitted_synthetic_evidence")
        self.assertFalse(result["design_use_allowed"])
        self.assertEqual(physics["rejections"], [])
        self.assertEqual(physics["torque_path_count"], 1)
        self.assertEqual(physics["reaction_path_count"], 1)
        self.assertLessEqual(physics["torque_residual_relative"], 1e-5)
        self.assertLessEqual(physics["reaction_residual_relative"], 1e-5)
        self.assertLessEqual(physics["energy_residual_relative"], 1e-4)
        self.assertLessEqual(physics["thermal_residual_relative"], 1e-4)
        self.assertEqual(physics["external_primary_inflow_j"], 0.0)
        self.assertLess(physics["store_final_energy_j"], physics["store_initial_energy_j"])

    def test_reference_transformation_and_statics_are_geometry_consistent(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        physics = evaluate_candidate(raw, manifest, freecad, work083)["physics"]
        self.assertEqual(physics["torque_ratio"], 3.0)
        self.assertAlmostEqual(physics["output_angular_speed_rad_s"], 100.0, places=12)
        self.assertAlmostEqual(physics["ideal_output_torque_nm"], 24.0, places=12)
        self.assertAlmostEqual(physics["delivered_output_torque_nm"], 22.8, places=12)
        self.assertAlmostEqual(physics["traction_force_n"], 800.0, places=9)
        self.assertAlmostEqual(
            physics["support_reaction_n"] + physics["work083_interface_reaction_n"],
            physics["traction_force_n"],
            places=9,
        )

    def test_reference_thermal_states_stay_inside_declared_domains(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        physics = evaluate_candidate(raw, manifest, freecad, work083)["physics"]
        for segment in physics["thermal_segments"].values():
            self.assertLessEqual(
                segment["coolant_temperature_rise_k"], raw["thermal"]["maximum_coolant_temperature_rise_k"]
            )
            self.assertLessEqual(segment["housing_temperature_k"], raw["material"]["maximum_temperature_k"])
        self.assertLessEqual(physics["coolant_velocity_m_s"], raw["thermal"]["maximum_coolant_velocity_m_s"])

    def test_analytic_structural_cases_stay_below_their_limit(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        structural = evaluate_candidate(raw, manifest, freecad, work083)["structural_analytic"]
        self.assertEqual(structural["evidence_class"], "analytic_synthetic_verification")
        self.assertFalse(structural["meshed_solver_evidence"])
        self.assertEqual(tuple(structural["cases"]), tuple(raw["structural_analytic"]["cases"]))
        self.assertLessEqual(structural["maximum_utilization"], raw["structural_analytic"]["maximum_utilization"])

    def test_every_declared_control_produces_its_preregistered_consequence(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        controls = evaluate_candidate(raw, manifest, freecad, work083)["controls"]
        self.assertEqual(set(controls), set(raw["controls"]))
        self.assertTrue(all(control["status"] == "passed" for control in controls.values()))
        self.assertEqual(controls["locked_converter"]["delivered_work_j"], 0.0)
        self.assertEqual(controls["seized_support"]["delivered_work_j"], 0.0)
        self.assertIn("open_torque_path", controls["broken_coupling"]["rejections"])
        self.assertIn("declared_efficiency_exceeds_maximum", controls["zero_loss_exploit"]["rejections"])
        self.assertIn("efficiency_outside_unit_interval", controls["efficiency_over_one"]["rejections"])
        self.assertIn("undeclared_energy_source", controls["reversed_torque"]["rejections"])
        self.assertIn("speed_domain_exceeded", controls["overspeed"]["rejections"])
        self.assertIn(
            "coolant_temperature_rise_exceeded_brake", controls["inadequate_cooling"]["rejections"]
        )
        self.assertIn("open_reaction_path", controls["disconnected_housing_reaction"]["rejections"])
        self.assertTrue(controls["mirror"]["support_reaction_matches_reference"])

    def test_unmet_meshed_structural_gate_is_reported(self) -> None:
        raw, manifest, freecad, work083 = _fixtures()
        result = evaluate_candidate(raw, manifest, freecad, work083)
        self.assertTrue(any("meshed" in item for item in result["unmet_program_gates"]))


class EnergyTorquePathIdentityTests(unittest.TestCase):
    def test_canonical_identity_is_mapping_order_independent(self) -> None:
        self.assertEqual(canonical_sha256({"a": 1, "b": 2}), canonical_sha256({"b": 2, "a": 1}))

    def test_path_counting_detects_severed_and_duplicated_routes(self) -> None:
        self.assertEqual(unique_path_count([["a", "b"], ["b", "c"]], "a", "c"), 1)
        self.assertEqual(unique_path_count([["a", "b"]], "a", "c"), 0)
        self.assertEqual(unique_path_count([["a", "b"], ["b", "c"], ["a", "c"]], "a", "c"), 2)


if __name__ == "__main__":
    unittest.main()
