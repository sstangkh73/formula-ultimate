from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
import unittest


from formula_ultimate.subsystems.ground_interaction import (
    GroundInteractionViolation,
    canonical_sha256,
    evaluate_candidate,
    validate_declaration,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/candidates/ground_interaction_candidate_001.json"


def _raw() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def _fixtures() -> tuple[dict, dict, dict, dict]:
    raw = _raw()
    hashes = [
        raw["structural_evidence"]["geometry_step_sha256"],
        "1" * 64,
        "2" * 64,
        "3" * 64,
        "4" * 64,
    ]
    parts = [
        {
            "part_id": item["part_id"],
            "step_file": f"{item['part_id']}.step",
            "step_sha256": hashes[index],
            "valid": True,
            "solid_count": 1,
            "volume_m3": 1.0e-5 * (index + 1),
        }
        for index, item in enumerate(raw["parts"])
    ]
    manifest_body = {
        "candidate_id": raw["candidate_id"],
        "declaration_sha256": canonical_sha256(raw),
        "hidden_geometry_repair": False,
        "parts": parts,
        "assembly": {
            "step_file": "ground_interaction_candidate_001.step",
            "step_sha256": "a" * 64,
            "valid": True,
            "solid_count": 5,
            "volume_m3": 1.5e-4,
        },
        "motion_clearance": [
            {
                "state": state,
                "translation_m": translation,
                "minimum_forbidden_clearance_m": 0.008,
                "maximum_overlap_m3": 0.0,
            }
            for state, translation in (("minimum", -0.007), ("reference", 0.0), ("maximum", 0.007))
        ],
    }
    manifest = {**manifest_body, "manifest_sha256": canonical_sha256(manifest_body)}
    freecad_body = {
        "source_manifest_sha256": manifest["manifest_sha256"],
        "freecad_version": "1.1.3",
        "occt_version": "7.8.1",
        "hidden_geometry_repair": False,
        "parts": [
            {
                "part_id": part["part_id"],
                "step_sha256": part["step_sha256"],
                "valid": True,
                "solid_count": 1,
            }
            for part in parts
        ],
        "assembly": {"valid": True, "solid_count": 5},
    }
    freecad = {**freecad_body, "report_sha256": canonical_sha256(freecad_body)}
    structural = {
        "status": "passed",
        "result_sha256": raw["structural_evidence"]["result_sha256"],
        "geometry_step_sha256": raw["structural_evidence"]["geometry_step_sha256"],
        "material_record_sha256": raw["structural_evidence"]["material_record_sha256"],
        "design_use_allowed": False,
        "adjudication": {
            "status": "passed",
            "design_use_allowed": False,
            "evidence_class": "synthetic_verification",
            "structural_state": "elastic",
            "fine_metrics": {
                "maximum_displacement_m": 1.5e-5,
                "p90_von_mises_stress_pa": 3.9e6,
            },
        },
    }
    return raw, manifest, freecad, structural


class GroundInteractionCandidateTests(unittest.TestCase):
    def test_reference_declaration_has_five_parts_and_two_dof(self) -> None:
        result = validate_declaration(_raw())
        self.assertEqual(result["part_ids"], ["structural_mount", "guide_frame", "carrier", "axle", "contact_roller"])
        self.assertEqual(result["mobility_dof"], 2)
        self.assertAlmostEqual(result["travel_m"], 0.014)

    def test_unknown_declaration_field_fails_closed(self) -> None:
        raw = _raw()
        raw["unregistered"] = True
        with self.assertRaisesRegex(GroundInteractionViolation, "fields mismatch"):
            validate_declaration(raw)

    def test_joint_constraint_change_cannot_fake_mobility(self) -> None:
        raw = _raw()
        raw["joints"][2]["constraint_rows"] = 6
        with self.assertRaisesRegex(GroundInteractionViolation, "constraint rows"):
            validate_declaration(raw)

    def test_nonpositive_normal_force_is_rejected(self) -> None:
        raw = _raw()
        raw["ground_interface"]["force_on_candidate_n"][2] = 0.0
        raw["ground_interface"]["force_direction_angle_rad"] = math.atan2(180.0, 320.0)
        with self.assertRaisesRegex(GroundInteractionViolation, "positive normal"):
            validate_declaration(raw)

    def test_disconnected_reference_force_path_is_rejected(self) -> None:
        raw = _raw()
        raw["paths"]["force_edges"].pop()
        with self.assertRaisesRegex(GroundInteractionViolation, "force path"):
            validate_declaration(raw)

    def test_geometry_identity_change_fails_closed(self) -> None:
        raw, manifest, freecad, structural = _fixtures()
        manifest["parts"][1]["step_sha256"] = "f" * 64
        with self.assertRaisesRegex(GroundInteractionViolation, "manifest identity"):
            evaluate_candidate(raw, manifest, freecad, structural)

    def test_motion_clearance_below_gate_is_rejected(self) -> None:
        raw, manifest, freecad, structural = _fixtures()
        manifest["motion_clearance"][2]["minimum_forbidden_clearance_m"] = 0.0
        body = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
        manifest["manifest_sha256"] = canonical_sha256(body)
        freecad["source_manifest_sha256"] = manifest["manifest_sha256"]
        freecad_body = {key: value for key, value in freecad.items() if key != "report_sha256"}
        freecad["report_sha256"] = canonical_sha256(freecad_body)
        with self.assertRaisesRegex(GroundInteractionViolation, "clearance"):
            evaluate_candidate(raw, manifest, freecad, structural)

    def test_freecad_must_retain_separate_solids(self) -> None:
        raw, manifest, freecad, structural = _fixtures()
        freecad["assembly"]["solid_count"] = 1
        body = {key: value for key, value in freecad.items() if key != "report_sha256"}
        freecad["report_sha256"] = canonical_sha256(body)
        with self.assertRaisesRegex(GroundInteractionViolation, "separate solids"):
            evaluate_candidate(raw, manifest, freecad, structural)

    def test_synthetic_structural_evidence_cannot_be_relabelled(self) -> None:
        raw, manifest, freecad, structural = _fixtures()
        structural["design_use_allowed"] = True
        with self.assertRaisesRegex(GroundInteractionViolation, "relabelled"):
            evaluate_candidate(raw, manifest, freecad, structural)

    def test_reference_evaluation_closes_ledgers_and_exercises_controls(self) -> None:
        raw, manifest, freecad, structural = _fixtures()
        result = evaluate_candidate(raw, manifest, freecad, structural)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["candidate_verdict"], "not_admitted_synthetic_evidence")
        self.assertFalse(result["design_use_allowed"])
        self.assertEqual(result["paths"], {"force_path_count": 1, "torque_path_count": 1})
        self.assertLessEqual(result["physics"]["force_residual_relative"], 1e-5)
        self.assertLessEqual(result["physics"]["moment_residual_relative"], 1e-5)
        self.assertLessEqual(result["physics"]["drive_energy_residual_relative"], 1e-4)
        self.assertEqual(result["controls"]["disconnected_mount"]["subsystem_state"], "dnf")
        self.assertEqual(result["controls"]["contact_loss"]["subsystem_state"], "dnf")
        self.assertEqual(result["controls"]["broken_torque_path"]["delivered_torque_nm"], 0.0)

    def test_nonfinite_values_fail_closed(self) -> None:
        raw = _raw()
        raw["torque_case"]["angular_speed_rad_s"] = float("nan")
        with self.assertRaisesRegex(GroundInteractionViolation, "finite domain"):
            validate_declaration(raw)

    def test_canonical_identity_is_mapping_order_independent(self) -> None:
        self.assertEqual(canonical_sha256({"a": 1, "b": 2}), canonical_sha256({"b": 2, "a": 1}))


if __name__ == "__main__":
    unittest.main()
