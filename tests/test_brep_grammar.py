from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest

from formula_ultimate.components.brep_grammar import (
    OPERATORS,
    REQUIRED_FAMILIES,
    BrepGrammarViolation,
    brep_declaration_sha256,
    validate_brep_grammar,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/cad/brep_feature_grammar_v1.json"
HAS_CADQUERY = importlib.util.find_spec("cadquery") is not None


def load_reference() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def reverse_mappings(value):
    if isinstance(value, dict):
        return {key: reverse_mappings(item) for key, item in reversed(tuple(value.items()))}
    if isinstance(value, list):
        return [reverse_mappings(item) for item in value]
    return value


class BrepGrammarParserTests(unittest.TestCase):
    def test_reference_covers_required_families_and_operators(self) -> None:
        result = validate_brep_grammar(load_reference())
        self.assertEqual("passed", result["status"])
        self.assertEqual(5, result["candidate_count"])
        self.assertEqual(REQUIRED_FAMILIES, set(result["family_coverage"]))
        self.assertEqual(OPERATORS, set(result["operator_coverage"]))

    def test_mapping_key_order_does_not_change_declaration_identity(self) -> None:
        raw = load_reference()
        reordered = reverse_mappings(raw)
        self.assertEqual(brep_declaration_sha256(raw), brep_declaration_sha256(reordered))
        self.assertEqual(
            validate_brep_grammar(raw)["declaration_sha256"],
            validate_brep_grammar(reordered)["declaration_sha256"],
        )

    def test_unknown_operator_and_field_fail_closed(self) -> None:
        raw = load_reference()
        raw["candidates"][0]["features"][1]["operator"] = "magic_solid"
        with self.assertRaisesRegex(BrepGrammarViolation, "unsupported feature operator"):
            validate_brep_grammar(raw)
        raw = load_reference()
        raw["candidates"][0]["features"][1]["parameters"]["distance_mm"] = 140.0
        with self.assertRaisesRegex(BrepGrammarViolation, "unknown=.*distance_mm"):
            validate_brep_grammar(raw)

    def test_zero_thickness_and_out_of_bounds_fail_closed(self) -> None:
        raw = load_reference()
        raw["candidates"][1]["features"][1]["parameters"]["distance_m"] = 0.0
        with self.assertRaisesRegex(BrepGrammarViolation, "must be > 0"):
            validate_brep_grammar(raw)
        raw = load_reference()
        raw["candidates"][1]["features"][1]["parameters"]["distance_m"] = 5.1
        with self.assertRaisesRegex(BrepGrammarViolation, "<= 5 m"):
            validate_brep_grammar(raw)

    def test_forward_or_unknown_input_fails_closed(self) -> None:
        raw = load_reference()
        raw["candidates"][1]["features"][1]["inputs"] = ["future_feature"]
        with self.assertRaisesRegex(BrepGrammarViolation, "must precede"):
            validate_brep_grammar(raw)

    def test_invalid_annulus_and_counterbore_fail_closed(self) -> None:
        raw = load_reference()
        raw["candidates"][4]["features"][0]["parameters"]["size_b_m"] = 0.05
        with self.assertRaisesRegex(BrepGrammarViolation, "annulus inner radius"):
            validate_brep_grammar(raw)
        raw = load_reference()
        raw["candidates"][2]["features"][3]["parameters"]["counterbore_diameter_m"] = 0.005
        with self.assertRaisesRegex(BrepGrammarViolation, "counterbore diameter"):
            validate_brep_grammar(raw)


@unittest.skipUnless(HAS_CADQUERY, "CadQuery kernel tests use the pinned Work 078 environment")
class BrepKernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from scripts.cad.generate_brep_feature_corpus import (  # noqa: PLC0415
            BrepExecutionError,
            _execute_candidate,
        )

        cls.execution_error = BrepExecutionError
        cls.execute_candidate = staticmethod(_execute_candidate)

    def test_five_canonical_families_end_as_one_valid_solid(self) -> None:
        for candidate in load_reference()["candidates"]:
            with self.subTest(candidate=candidate["candidate_id"]):
                shape, trace = self.execute_candidate(candidate)
                self.assertTrue(shape.isValid())
                self.assertEqual(1, len(shape.Solids()))
                self.assertGreater(shape.Volume(), 0.0)
                self.assertEqual(len(candidate["features"]), len(trace))

    def test_self_erasing_subtract_is_observable(self) -> None:
        candidate = {
            "candidate_id": "negative_subtract",
            "family": "bracket",
            "features": [
                {"feature_id": "profile", "operator": "sketch_profile", "inputs": [], "parameters": {"profile_type": "circle", "center_x_m": 0.0, "center_y_m": 0.0, "size_a_m": 0.02, "size_b_m": 0.0}},
                {"feature_id": "blank", "operator": "extrude", "inputs": ["profile"], "parameters": {"distance_m": 0.02}},
                {"feature_id": "empty", "operator": "boolean_subtract", "inputs": ["blank", "blank"], "parameters": {}},
            ],
            "final_feature_id": "empty",
        }
        with self.assertRaisesRegex(self.execution_error, "empty shape"):
            self.execute_candidate(candidate)

    def test_disconnected_pattern_cannot_be_a_final_part(self) -> None:
        candidate = {
            "candidate_id": "negative_multisolid",
            "family": "bracket",
            "features": [
                {"feature_id": "profile", "operator": "sketch_profile", "inputs": [], "parameters": {"profile_type": "circle", "center_x_m": 0.0, "center_y_m": 0.0, "size_a_m": 0.002, "size_b_m": 0.0}},
                {"feature_id": "seed", "operator": "extrude", "inputs": ["profile"], "parameters": {"distance_m": 0.002}},
                {"feature_id": "separate", "operator": "linear_pattern", "inputs": ["seed"], "parameters": {"count": 2, "spacing_m": 0.02, "direction": "x"}},
            ],
            "final_feature_id": "separate",
        }
        with self.assertRaisesRegex(self.execution_error, "exactly one solid"):
            self.execute_candidate(candidate)


if __name__ == "__main__":
    unittest.main()
