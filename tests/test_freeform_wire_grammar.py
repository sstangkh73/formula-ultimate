from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.components.freeform_wire_grammar import (
    CONSTRAINTS,
    OPERATORS,
    TRANSFORMS,
    FreeformWireGrammarError,
    compare_measurement_witnesses,
    declaration_sha256,
    validate_grammar,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/cad/freeform_wire_grammar_v2.json"
HAS_CADQUERY = importlib.util.find_spec("cadquery") is not None


def load_reference() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def reverse_mappings(value):
    if isinstance(value, dict):
        return {key: reverse_mappings(item) for key, item in reversed(tuple(value.items()))}
    if isinstance(value, list):
        return [reverse_mappings(item) for item in value]
    return value


class FreeformWireGrammarParserTests(unittest.TestCase):
    def test_reference_covers_every_operator_transform_and_constraint(self) -> None:
        result = validate_grammar(load_reference())
        self.assertEqual("passed", result["status"])
        self.assertEqual(12, result["profile_count"])
        self.assertGreaterEqual(result["family_count"], 6)
        self.assertEqual(set(OPERATORS), set(result["operator_coverage"]))
        self.assertEqual(set(TRANSFORMS), set(result["transform_coverage"]))
        self.assertEqual(set(CONSTRAINTS), set(result["constraint_coverage"]))
        self.assertGreaterEqual(result["nonzero_offset_profiles"], 1)
        self.assertGreaterEqual(result["nontrivial_trim_segments"], 1)

    def test_mapping_order_is_identity_invariant_and_control_point_is_causal(self) -> None:
        raw = load_reference()
        self.assertEqual(declaration_sha256(raw), declaration_sha256(reverse_mappings(raw)))
        changed = deepcopy(raw)
        changed["profiles"][10]["loops"][0]["segments"][0]["parameters"]["control_points_m"][1][1] += 0.001
        self.assertNotEqual(declaration_sha256(raw), declaration_sha256(changed))

    def test_unknown_field_and_operator_fail_closed(self) -> None:
        raw = load_reference()
        raw["profiles"][0]["surprise"] = True
        with self.assertRaisesRegex(FreeformWireGrammarError, "schema mismatch"):
            validate_grammar(raw)
        raw = load_reference()
        raw["profiles"][0]["loops"][0]["segments"][0]["operator"] = "magic_curve"
        with self.assertRaisesRegex(FreeformWireGrammarError, "unsupported wire operator"):
            validate_grammar(raw)

    def test_open_and_self_intersecting_polylines_fail_closed(self) -> None:
        raw = load_reference()
        raw["profiles"][0]["loops"][0]["segments"][0]["parameters"]["points_m"][-1] = [0.0, 0.0]
        with self.assertRaisesRegex(FreeformWireGrammarError, "explicitly closed"):
            validate_grammar(raw)
        raw = load_reference()
        raw["profiles"][0]["loops"][0]["segments"][0]["parameters"]["points_m"] = [
            [-0.04, -0.02], [0.04, 0.02], [-0.04, 0.02], [0.04, -0.02], [-0.04, -0.02]
        ]
        with self.assertRaisesRegex(FreeformWireGrammarError, "self-intersection"):
            validate_grammar(raw)

    def test_duplicate_identity_zero_segment_and_nonfinite_value_fail_closed(self) -> None:
        raw = load_reference()
        raw["profiles"][1]["profile_id"] = raw["profiles"][0]["profile_id"]
        with self.assertRaisesRegex(FreeformWireGrammarError, "duplicate profile"):
            validate_grammar(raw)
        raw = load_reference()
        line = raw["profiles"][2]["loops"][0]["segments"][0]
        line["parameters"]["end_m"] = line["parameters"]["start_m"]
        with self.assertRaisesRegex(FreeformWireGrammarError, "zero or sub-tolerance line"):
            validate_grammar(raw)
        raw = load_reference()
        raw["profiles"][7]["loops"][0]["segments"][0]["parameters"]["rotation_rad"] = math.inf
        with self.assertRaisesRegex(FreeformWireGrammarError, "finite"):
            validate_grammar(raw)

    def test_invalid_arcs_bezier_bspline_and_offset_fail_closed(self) -> None:
        raw = load_reference()
        raw["profiles"][3]["loops"][0]["segments"][1]["parameters"]["tangent"] = [0.0, 0.0]
        with self.assertRaisesRegex(FreeformWireGrammarError, "invalid tangent arc"):
            validate_grammar(raw)
        raw = load_reference()
        arc = raw["profiles"][4]["loops"][0]["segments"][0]["parameters"]
        arc["mid_m"] = [(arc["start_m"][0] + arc["end_m"][0]) / 2, (arc["start_m"][1] + arc["end_m"][1]) / 2]
        with self.assertRaisesRegex(FreeformWireGrammarError, "collinear"):
            validate_grammar(raw)
        raw = load_reference()
        raw["profiles"][9]["loops"][0]["segments"][0]["parameters"]["control_points_m"] = [[0.0, 0.0], [0.01, 0.01]]
        with self.assertRaisesRegex(FreeformWireGrammarError, "Bezier requires"):
            validate_grammar(raw)
        raw = load_reference()
        raw["profiles"][11]["loops"][0]["segments"][0]["parameters"]["degree"] = 8
        with self.assertRaisesRegex(FreeformWireGrammarError, "degree is outside"):
            validate_grammar(raw)
        raw = load_reference()
        raw["profiles"][8]["offset"]["distance_m"] = 0.03
        with self.assertRaisesRegex(FreeformWireGrammarError, "offset is outside"):
            validate_grammar(raw)

    def test_measurement_witness_accepts_declared_residual_and_reports_maxima(self) -> None:
        expected = [{"profile_id": "shape", "face_count": 1, "wire_count": 1, "edge_count": 2,
                     "area_m2": 1.0, "perimeter_m": 2.0,
                     "bounding_box_m": {"minimum": [0.0, 0.0, 0.0], "maximum": [1.0, 1.0, 0.0]}}]
        measured = deepcopy(expected)
        measured[0]["perimeter_m"] = 2.002
        measured[0]["bounding_box_m"]["maximum"][0] += 5e-8
        result = compare_measurement_witnesses(
            expected, measured, measurement_relative_tolerance=0.002, bounds_absolute_tolerance_m=1e-7
        )
        self.assertGreater(result["maximum_perimeter_relative_difference"], 0.0)
        self.assertAlmostEqual(5e-8, result["maximum_bounds_absolute_difference_m"], places=14)

    def test_measurement_witness_rejects_topology_metric_and_bounds_mismatch(self) -> None:
        expected = [{"profile_id": "shape", "face_count": 1, "wire_count": 1, "edge_count": 2,
                     "area_m2": 1.0, "perimeter_m": 2.0,
                     "bounding_box_m": {"minimum": [0.0, 0.0, 0.0], "maximum": [1.0, 1.0, 0.0]}}]
        for field, value, message in (("edge_count", 3, "edge_count"), ("perimeter_m", 2.1, "relative tolerance")):
            measured = deepcopy(expected)
            measured[0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(FreeformWireGrammarError, message):
                compare_measurement_witnesses(expected, measured, measurement_relative_tolerance=0.002, bounds_absolute_tolerance_m=1e-7)
        measured = deepcopy(expected)
        measured[0]["bounding_box_m"]["maximum"][0] += 1e-4
        with self.assertRaisesRegex(FreeformWireGrammarError, "bounding-box witness"):
            compare_measurement_witnesses(expected, measured, measurement_relative_tolerance=0.002, bounds_absolute_tolerance_m=1e-7)


@unittest.skipUnless(HAS_CADQUERY, "CadQuery kernel tests use the pinned Work 091 environment")
class FreeformWireKernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        import cadquery as cq  # noqa: PLC0415
        from scripts.cad.generate_freeform_wire_corpus import (  # noqa: PLC0415
            enforce_constraints,
            execute_loop,
            validate_loop_nesting,
        )

        cls.cq = cq
        cls.enforce_constraints = staticmethod(enforce_constraints)
        cls.execute_loop = staticmethod(execute_loop)
        cls.validate_loop_nesting = staticmethod(validate_loop_nesting)

    def test_all_profiles_create_one_valid_positive_area_face(self) -> None:
        for profile in load_reference()["profiles"]:
            with self.subTest(profile=profile["profile_id"]):
                wires = [self.execute_loop(loop, profile) for loop in profile["loops"]]
                face = self.cq.Face.makeFromWires(wires[0], wires[1:])
                self.assertTrue(face.isValid())
                self.assertGreater(face.Area(), 0.0)
                perimeter_m = sum(edge.Length() for edge in face.Edges()) / 1000.0
                self.enforce_constraints(profile, face, perimeter_m)

    def test_invalid_hole_nesting_and_constraint_failure_are_observable(self) -> None:
        profile = deepcopy(load_reference()["profiles"][6])
        profile["loops"][1]["segments"][0]["parameters"]["center_m"] = [0.2, 0.0]
        wires = [self.execute_loop(loop, profile) for loop in profile["loops"]]
        with self.assertRaisesRegex(RuntimeError, "not nested inside"):
            self.validate_loop_nesting(wires, profile["profile_id"], 1e-7)

        profile = deepcopy(load_reference()["profiles"][0])
        profile["constraints"] = [{"kind": "minimum_perimeter", "value": 99.0}]
        wire = self.execute_loop(profile["loops"][0], profile)
        face = self.cq.Face.makeFromWires(wire)
        with self.assertRaisesRegex(RuntimeError, "minimum_perimeter constraint failed"):
            self.enforce_constraints(profile, face, sum(edge.Length() for edge in face.Edges()) / 1000.0)


if __name__ == "__main__":
    unittest.main()
