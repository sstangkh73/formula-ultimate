from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.components.engineering_contracts import (
    EngineeringContractViolation,
    evaluate_manufacturing_witness,
    record_sha256,
    validate_engineering_assignment,
    validate_manufacturing_process,
    validate_material_record,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/materials/engineering_material_manufacturing_v1.json"


def load_reference() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def reverse_mappings(value):
    if isinstance(value, dict):
        return {key: reverse_mappings(item) for key, item in reversed(tuple(value.items()))}
    if isinstance(value, list):
        return [reverse_mappings(item) for item in value]
    return value


class EngineeringContractTests(unittest.TestCase):
    def test_reference_binding_passes_but_is_not_design_eligible(self) -> None:
        raw = load_reference()
        result = validate_engineering_assignment(
            raw["assignment"],
            raw["material"],
            raw["manufacturing_process"],
            raw["geometry_witness"],
        )
        self.assertEqual("passed", result["status"])
        self.assertFalse(result["design_use_allowed"])
        self.assertFalse(result["material"]["design_use_allowed"])
        self.assertFalse(result["manufacturing_process"]["production_use_allowed"])
        self.assertEqual("missing", result["material"]["fatigue_evidence_status"])
        self.assertEqual(
            "synthetic",
            result["manufacturing_witness"]["measurement_evidence_status"],
        )
        self.assertLess(result["material"]["elastic_consistency_relative_residual"], 1e-12)
        self.assertTrue(all(value >= 0.0 for value in result["manufacturing_witness"]["margins"].values()))

    def test_mapping_order_replays_record_hashes_exactly(self) -> None:
        raw = load_reference()
        self.assertEqual(
            record_sha256(raw["material"]),
            record_sha256(reverse_mappings(raw["material"])),
        )
        self.assertEqual(
            record_sha256(raw["manufacturing_process"]),
            record_sha256(reverse_mappings(raw["manufacturing_process"])),
        )

    def test_unknown_maximum_force_or_wrong_unit_fails_closed(self) -> None:
        raw = load_reference()
        raw["material"]["properties"]["maximum_force_n"] = 1e12
        with self.assertRaisesRegex(EngineeringContractViolation, "schema_error"):
            validate_material_record(raw["material"])
        raw = load_reference()
        density = raw["material"]["properties"].pop("density_kg_per_m3")
        raw["material"]["properties"]["density_g_per_cm3"] = density / 1000.0
        with self.assertRaisesRegex(EngineeringContractViolation, "schema_error"):
            validate_material_record(raw["material"])

    def test_nonfinite_negative_and_poisson_values_fail_closed(self) -> None:
        cases = [
            ("density_kg_per_m3", math.nan, "invalid_numeric_value"),
            ("fracture_toughness_pa_sqrt_m", -1.0, "invalid_numeric_value"),
            ("poisson_ratio", 0.5, "invalid_poisson_ratio"),
        ]
        for name, value, code in cases:
            raw = load_reference()
            raw["material"]["properties"][name] = value
            with self.subTest(name=name):
                with self.assertRaisesRegex(EngineeringContractViolation, code):
                    validate_material_record(raw["material"])

    def test_inconsistent_elastic_constants_and_strength_order_fail(self) -> None:
        raw = load_reference()
        raw["material"]["properties"]["shear_modulus_pa"] *= 1.1
        with self.assertRaisesRegex(EngineeringContractViolation, "inconsistent_elastic_constants"):
            validate_material_record(raw["material"])
        raw = load_reference()
        raw["material"]["properties"]["yield_strength_pa"] = 400e6
        with self.assertRaisesRegex(EngineeringContractViolation, "invalid_strength_order"):
            validate_material_record(raw["material"])

    def test_missing_property_source_and_unsupported_fatigue_claim_fail(self) -> None:
        raw = load_reference()
        raw["material"]["property_sources"]["density_kg_per_m3"] = "missing_source"
        with self.assertRaisesRegex(EngineeringContractViolation, "missing_property_source"):
            validate_material_record(raw["material"])
        raw = load_reference()
        raw["material"]["fatigue"] = {
            "evidence_status": "available",
            "model": "sn_curve",
            "points": [],
            "source_id": "work079_synthetic_material_fixture",
        }
        with self.assertRaisesRegex(EngineeringContractViolation, "unsupported_fatigue_claim"):
            validate_material_record(raw["material"])

    def test_geometry_and_tool_process_violations_are_causal(self) -> None:
        cases = [
            (lambda witness: witness["wall_thicknesses_m"].__setitem__(0, 0.001), "wall_too_thin"),
            (lambda witness: witness["hole_diameters_m"].__setitem__(0, 0.003), "hole_too_small"),
            (lambda witness: witness["ligaments_m"].__setitem__(0, 0.002), "ligament_too_small"),
            (lambda witness: witness["web_thicknesses_m"].__setitem__(0, 0.001), "web_too_thin"),
            (lambda witness: witness["internal_radii_m"].__setitem__(0, 0.0005), "internal_radius_too_small"),
            (lambda witness: witness["bend_radii_m"].__setitem__(0, 0.002), "bend_radius_too_small"),
            (lambda witness: witness["tool_access_checks"][0].__setitem__("direction", "q"), "tool_direction_blocked"),
            (lambda witness: witness["tool_access_checks"][0].__setitem__("clearance_m", 0.001), "tool_clearance_blocked"),
            (lambda witness: witness["tool_access_checks"][0].__setitem__("depth_m", 0.1), "tool_depth_ratio_exceeded"),
            (lambda witness: witness.__setitem__("requested_tolerance_m", 0.00005), "tolerance_too_tight"),
            (lambda witness: witness["unsupported_features"].append("enclosed_cavity"), "unsupported_feature"),
        ]
        process = load_reference()["manufacturing_process"]
        for mutation, code in cases:
            witness = deepcopy(load_reference()["geometry_witness"])
            mutation(witness)
            with self.subTest(code=code):
                with self.assertRaisesRegex(EngineeringContractViolation, code):
                    evaluate_manufacturing_witness(process, witness)

    def test_missing_process_source_and_stale_assignment_hash_fail(self) -> None:
        raw = load_reference()
        raw["manufacturing_process"]["limit_sources"]["minimum_wall_thickness_m"] = "missing_source"
        with self.assertRaisesRegex(EngineeringContractViolation, "missing_limit_source"):
            validate_manufacturing_process(raw["manufacturing_process"])
        raw = load_reference()
        raw["assignment"]["material_record_sha256"] = "f" * 64
        with self.assertRaisesRegex(EngineeringContractViolation, "assignment_identity_mismatch"):
            validate_engineering_assignment(
                raw["assignment"],
                raw["material"],
                raw["manufacturing_process"],
                raw["geometry_witness"],
            )


if __name__ == "__main__":
    unittest.main()
