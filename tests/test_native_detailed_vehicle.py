from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for item in (ROOT, SRC):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from formula_ultimate.assembly.native_detailed_vehicle import (
    FINAL_STATUS,
    NativeDetailedVehicleViolation,
    evaluate_admitted_evidence,
    validate_declaration,
)


CONFIG = ROOT / "config/development/native_detailed_vehicle_v1.json"
HAS_CADQUERY = importlib.util.find_spec("cadquery") is not None


class NativeDetailedVehicleTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.declaration = validate_declaration(self.raw)

    def evidence(self):
        manifest = {
            "status": "passed",
            "candidate_id": self.raw["candidate"]["candidate_id"],
            "declaration_sha256": self.declaration["protocol_sha256"],
            "hidden_geometry_repair": False,
            "definitions": [
                {
                    "definition_id": item["definition_id"],
                    "valid": True,
                    "closed": True,
                    "solid_count": 1,
                    "feature_count": len(item["feature_inventory"]),
                    "semantic_faces": {selector: [{"signature_sha256": "0" * 64}] for selector in item["semantic_face_selectors"]},
                }
                for item in self.raw["definitions"]
            ],
            "instances": [{"instance_id": item["instance_id"]} for item in self.raw["instances"]],
            "material_assembly": {"solid_count": self.declaration["material_instance_count"]},
            "void_assembly": {"solid_count": self.declaration["void_instance_count"]},
            "collision_clearance": {"maximum_noncontact_penetration_m3": 0.0, "boolean_failures": []},
            "motion": {
                "sample_count": 101,
                "collision_count": 0,
                "successive_minimum_clearance_change_m": 0.0,
            },
            "occurrence_coverage_fraction": 1.0,
            "unknown_essential_occurrences": [],
            "physics_boundary_coverage_fraction": 1.0,
        }
        freecad = {
            "status": "passed",
            "hidden_geometry_repair": False,
            "definitions": [
                {"definition_id": item["definition_id"], "valid": True, "solid_count": 1}
                for item in self.raw["definitions"]
            ],
            "instances": [
                {"instance_id": item["instance_id"], "valid": True, "solid_count": 1}
                for item in self.raw["instances"]
            ],
            "material_assembly": {"solid_count": self.declaration["material_instance_count"]},
            "void_assembly": {"solid_count": self.declaration["void_instance_count"]},
            "maximum_residuals": {
                "volume_relative": 0.0,
                "mass_relative": 0.0,
                "center_absolute_m": 0.0,
                "inertia_relative": 0.0,
            },
            "semantic_boundary_survival_rate": 1.0,
            "step_hash_match": True,
            "invalid_or_null_solids": 0,
            "mass_properties": {"mass_kg": 1.0, "center_m": [0.0, 0.0, 0.0], "inertia_kg_m2": [1.0] * 6},
        }
        return manifest, freecad

    def test_frozen_declaration_has_complete_native_inventory(self):
        self.assertEqual(self.declaration["status"], "passed")
        self.assertEqual(self.declaration["definition_count"], 48)
        self.assertEqual(self.declaration["instance_count"], 83)
        self.assertEqual(self.declaration["material_instance_count"], 77)
        self.assertEqual(self.declaration["void_instance_count"], 6)
        self.assertEqual(self.declaration["required_occurrence_count"], 40)
        self.assertNotEqual(self.raw["candidate"]["candidate_id"], "final_126_r1")
        self.assertEqual(self.raw["candidate"]["claim_scope"], "native_geometry_and_assembly_only")

    def test_admission_is_geometry_only_and_never_promotes(self):
        manifest, freecad = self.evidence()
        admitted = evaluate_admitted_evidence(self.raw, manifest, freecad)
        self.assertEqual(admitted["status"], FINAL_STATUS)
        self.assertTrue(admitted["downstream_physics_revalidation_required"])
        self.assertFalse(admitted["promotion_allowed"])

    def test_render_invalid_and_lost_semantic_evidence_fail_closed(self):
        manifest, freecad = self.evidence()
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "native-solid manifest is required"):
            evaluate_admitted_evidence(self.raw, None, None)
        invalid = copy.deepcopy(manifest)
        invalid["definitions"][0]["valid"] = False
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "invalid native part"):
            evaluate_admitted_evidence(self.raw, invalid, freecad)
        lost = copy.deepcopy(freecad)
        lost["semantic_boundary_survival_rate"] = 0.99
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "lost semantic face"):
            evaluate_admitted_evidence(self.raw, manifest, lost)

    def test_missing_occurrences_duplicate_regions_and_floating_parts_fail(self):
        missing = copy.deepcopy(self.raw)
        missing["instances"] = [item for item in missing["instances"] if "bearing" not in item["occurrence_classes"]]
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "missing required physical occurrence"):
            validate_declaration(missing)
        duplicate = copy.deepcopy(self.raw)
        duplicate["instances"][1]["region_id"] = duplicate["instances"][0]["region_id"]
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "duplicate material/void ownership"):
            validate_declaration(duplicate)
        floating = copy.deepcopy(self.raw)
        floating["instances"][1]["attachment"] = None
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "floating component"):
            validate_declaration(floating)

    def test_primitive_proxy_and_structural_void_fail(self):
        primitive = copy.deepcopy(self.raw)
        primitive["definitions"][0]["geometry"]["primitive_replacement"] = True
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "same-envelope primitive substitution"):
            validate_declaration(primitive)
        proxy = copy.deepcopy(self.raw)
        proxy["definitions"][0]["provenance"] = {"kind": "evidence_bound_purchased", "proxy": True}
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "unsupported purchased proxy"):
            validate_declaration(proxy)
        dense_void = copy.deepcopy(self.raw)
        next(item for item in dense_void["materials"] if item["material_id"] == "void")["density_kg_m3"] = 1.0
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "zero structural density"):
            validate_declaration(dense_void)

    def test_axis_worst_case_route_motion_and_cycle_fail(self):
        axes = copy.deepcopy(self.raw)
        contact = next(item for item in axes["instances"] if item.get("attachment") and not item["attachment"]["approved_noncontact"])
        contact["attachment"]["child_axis"] = [1.0, 0.0, 0.0]
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "mating axes mismatch"):
            validate_declaration(axes)
        worst = copy.deepcopy(self.raw)
        contact = next(item for item in worst["instances"] if item.get("attachment") and not item["attachment"]["approved_noncontact"])
        contact["attachment"]["worst_case_status"] = "failed"
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "worst-case tolerance failed"):
            validate_declaration(worst)
        route = copy.deepcopy(self.raw)
        route["routes"][0]["actual_minimum_bend_radius_m"] = 0.0
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "bend-radius failure"):
            validate_declaration(route)
        motion = copy.deepcopy(self.raw)
        motion["motion"]["sample_count"] = 100
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "at least 101 samples"):
            validate_declaration(motion)
        cyclic = copy.deepcopy(self.raw)
        next(item for item in cyclic["instances"] if item["instance_id"] == "rear_beam")["attachment"]["parent_instance_id"] = "rear_carrier_left"
        with self.assertRaisesRegex(NativeDetailedVehicleViolation, "cyclic assembly order"):
            validate_declaration(cyclic)


@unittest.skipUnless(HAS_CADQUERY, "CadQuery kernel tests use the pinned Work 078 environment")
class NativeDetailedVehicleKernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from scripts.cad import build_native_detailed_vehicle  # noqa: PLC0415

        cls.build = build_native_detailed_vehicle

    def setUp(self):
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8"))

    def test_cadquery_closed_flag_regression_uses_valid_single_solid(self):
        box = self.build._box([0.1, 0.1, 0.1])
        self.assertFalse(box.Closed())
        self.assertTrue(box.isValid())
        self.assertEqual(len(box.Solids()), 1)
        self.assertTrue(self.build.is_one_valid_solid(box))

    def test_fan_definition_regression_is_one_fused_solid(self):
        definition = next(item for item in self.raw["definitions"] if item["definition_id"] == "fan")
        fan = self.build.shape_from_definition(definition)
        self.assertTrue(self.build.is_one_valid_solid(fan))
        self.assertEqual(len(fan.Solids()), 1)

    def test_semantic_signature_canonicalizes_signed_zero(self):
        self.assertEqual(self.build._clean_signature_number(-0.0, 7), 0.0)
        self.assertEqual(str(self.build._clean_signature_number(-0.0, 7)), "0.0")


if __name__ == "__main__":
    unittest.main()
