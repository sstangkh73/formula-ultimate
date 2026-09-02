from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.assembly.joint_kernel import (
    AssemblyKernelViolation,
    assembly_declaration_sha256,
    evaluate_assembly,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/assembly/mechanical_assembly_joint_kernel_v1.json"


def load_reference() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def reverse_mappings(value):
    if isinstance(value, dict):
        return {key: reverse_mappings(item) for key, item in reversed(tuple(value.items()))}
    if isinstance(value, list):
        return [reverse_mappings(item) for item in value]
    return value


class JointKernelTests(unittest.TestCase):
    def assert_code(self, expected: str, declaration: dict) -> None:
        with self.assertRaises(AssemblyKernelViolation) as caught:
            evaluate_assembly(declaration)
        self.assertEqual(expected, caught.exception.code)

    def test_reference_calculates_rank_dof_clearance_and_collision(self) -> None:
        result = evaluate_assembly(load_reference())
        self.assertEqual("passed", result["status"])
        self.assertEqual(19, result["constraint_row_count"])
        self.assertEqual(19, result["constraint_rank"])
        self.assertEqual(0, result["constraint_redundancy_count"])
        self.assertEqual(5, result["realized_dof_count"])
        self.assertEqual(0, result["collision_count"])
        self.assertAlmostEqual(0.14, result["minimum_motion_envelope_gap_m"])
        self.assertFalse(result["hidden_alignment_or_repair"])

    def test_mapping_order_preserves_declaration_and_result_identity(self) -> None:
        raw = load_reference()
        reordered = reverse_mappings(raw)
        self.assertEqual(assembly_declaration_sha256(raw), assembly_declaration_sha256(reordered))
        self.assertEqual(evaluate_assembly(raw)["result_sha256"], evaluate_assembly(reordered)["result_sha256"])

    def test_geometry_hash_change_changes_both_identities(self) -> None:
        raw = load_reference()
        changed = deepcopy(raw)
        changed["components"][0]["geometry_sha256"] = "0" * 64
        self.assertNotEqual(assembly_declaration_sha256(raw), assembly_declaration_sha256(changed))
        self.assertNotEqual(evaluate_assembly(raw)["result_sha256"], evaluate_assembly(changed)["result_sha256"])

    def test_misaligned_axis_and_origin_fail_without_auto_alignment(self) -> None:
        raw = load_reference()
        raw["components"][0]["interfaces"][0]["frame"]["z_axis"] = [0.0, 1.0, 0.0]
        raw["components"][0]["interfaces"][0]["frame"]["y_axis"] = [0.0, 0.0, -1.0]
        self.assert_code("mate_axis_mismatch", raw)

        raw = load_reference()
        raw["components"][0]["interfaces"][0]["frame"]["origin_m"][0] = 0.001
        self.assert_code("mate_position_mismatch", raw)

    def test_redundant_joint_is_detected_from_constraint_rank(self) -> None:
        raw = load_reference()
        duplicate = deepcopy(raw["joints"][0])
        duplicate["joint_id"] = "rotor_joint_redundant"
        raw["joints"].append(duplicate)
        self.assert_code("overconstrained_assembly", raw)

    def test_declared_or_expected_dof_cannot_replace_calculation(self) -> None:
        raw = load_reference()
        raw["joints"][0]["declared_dofs"] = []
        self.assert_code("declared_dof_mismatch", raw)

        raw = load_reference()
        raw["expected"]["realized_dof_count"] = 6
        self.assert_code("realized_dof_mismatch", raw)

        raw = load_reference()
        raw["expected"]["constraint_rank"] = 19.5
        self.assert_code("invalid_numeric_value", raw)

    def test_clearance_limits_and_joint_limits_fail_closed(self) -> None:
        raw = load_reference()
        raw["joints"][1]["clearance"]["radial_m"] = 0.001
        self.assert_code("excessive_clearance", raw)

        raw = load_reference()
        raw["joints"][1]["limits"]["home"] = 0.1
        self.assert_code("invalid_joint_limits", raw)

    def test_continuous_prismatic_envelope_collision_fails(self) -> None:
        raw = load_reference()
        slider_ground = raw["ground_interfaces"][1]["frame"]["origin_m"]
        slider_frame = raw["components"][1]["frame"]["origin_m"]
        slider_ground[0] = 0.12
        slider_frame[0] = 0.12
        raw["joints"][1]["limits"] = {"minimum": -0.12, "home": 0.0, "maximum": 0.12}
        self.assert_code("motion_envelope_collision", raw)

    def test_missing_duplicate_and_incompatible_interfaces_fail_closed(self) -> None:
        raw = load_reference()
        raw["joints"][0]["interface_b"] = "missing"
        self.assert_code("missing_interface", raw)

        raw = load_reference()
        raw["components"][0]["interfaces"].append(deepcopy(raw["components"][0]["interfaces"][0]))
        self.assert_code("duplicate_interface", raw)

        raw = load_reference()
        raw["components"][0]["interfaces"][0]["interface_type"] = "prismatic"
        self.assert_code("incompatible_interface", raw)

    def test_nonfinite_and_left_handed_frames_fail_closed(self) -> None:
        raw = load_reference()
        raw["components"][0]["frame"]["origin_m"][0] = math.nan
        self.assert_code("invalid_numeric_value", raw)

        raw = load_reference()
        raw["components"][0]["frame"]["z_axis"] = [0.0, 0.0, -1.0]
        self.assert_code("invalid_frame", raw)


if __name__ == "__main__":
    unittest.main()
