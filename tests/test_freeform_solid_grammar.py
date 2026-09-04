from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.components.freeform_solid_grammar import (
    OPERATORS,
    REQUIRED_FAMILIES,
    FreeformSolidGrammarError,
    declaration_sha256,
    validate_solid_grammar,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/cad/freeform_brep_solid_grammar_v2.json"
WIRE_CONFIG = ROOT / "config/cad/freeform_wire_grammar_v2.json"
HAS_CADQUERY = importlib.util.find_spec("cadquery") is not None


def load_solid() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def load_wire() -> dict:
    return json.loads(WIRE_CONFIG.read_text(encoding="utf-8"))


def profile_ids() -> set[str]:
    return {item["profile_id"] for item in load_wire()["profiles"]}


def reverse_mappings(value):
    if isinstance(value, dict):
        return {key: reverse_mappings(item) for key, item in reversed(tuple(value.items()))}
    if isinstance(value, list):
        return [reverse_mappings(item) for item in value]
    return value


class FreeformSolidParserTests(unittest.TestCase):
    def test_reference_covers_ten_candidates_required_families_and_all_operators(self) -> None:
        result = validate_solid_grammar(load_solid(), profile_ids())
        self.assertEqual("passed", result["status"])
        self.assertEqual(10, result["candidate_count"])
        self.assertTrue(REQUIRED_FAMILIES.issubset(result["family_coverage"]))
        self.assertEqual(set(OPERATORS), set(result["operator_coverage"]))

    def test_key_order_is_invariant_and_path_mutation_is_causal(self) -> None:
        raw = load_solid()
        self.assertEqual(declaration_sha256(raw), declaration_sha256(reverse_mappings(raw)))
        changed = deepcopy(raw)
        changed["candidates"][0]["features"][1]["parameters"]["points_m"][1][0] += 0.001
        self.assertNotEqual(declaration_sha256(raw), declaration_sha256(changed))

    def test_unknown_field_operator_profile_and_forward_ancestry_fail_closed(self) -> None:
        raw = load_solid(); raw["candidates"][0]["surprise"] = 1
        with self.assertRaisesRegex(FreeformSolidGrammarError, "schema mismatch"):
            validate_solid_grammar(raw, profile_ids())
        raw = load_solid(); raw["candidates"][0]["features"][0]["operator"] = "voxel_magic"
        with self.assertRaisesRegex(FreeformSolidGrammarError, "unsupported solid operator"):
            validate_solid_grammar(raw, profile_ids())
        raw = load_solid(); raw["candidates"][0]["features"][0]["parameters"]["profile_id"] = "missing"
        with self.assertRaisesRegex(FreeformSolidGrammarError, "unknown Work 091 profile"):
            validate_solid_grammar(raw, profile_ids())
        raw = load_solid(); raw["candidates"][0]["features"][2]["inputs"] = ["left_sweep", "root_path"]
        with self.assertRaisesRegex(FreeformSolidGrammarError, "valid earlier ancestry"):
            validate_solid_grammar(raw, profile_ids())

    def test_zero_path_nonfinite_dimension_and_input_type_fail_closed(self) -> None:
        raw = load_solid(); raw["candidates"][0]["features"][1]["parameters"]["points_m"][1] = [0.0, 0.0, 0.0]
        with self.assertRaisesRegex(FreeformSolidGrammarError, "path is zero length"):
            validate_solid_grammar(raw, profile_ids())
        raw = load_solid(); raw["candidates"][2]["features"][4]["parameters"]["radius_m"] = math.inf
        with self.assertRaisesRegex(FreeformSolidGrammarError, "finite"):
            validate_solid_grammar(raw, profile_ids())
        raw = load_solid(); raw["candidates"][0]["features"][2]["inputs"] = ["root_path", "root_section"]
        with self.assertRaisesRegex(FreeformSolidGrammarError, "input types are incompatible"):
            validate_solid_grammar(raw, profile_ids())

    def test_body_count_tolerance_and_required_family_policy_fail_closed(self) -> None:
        raw = load_solid(); raw["candidates"][0]["expected_body_count"] = 0
        with self.assertRaisesRegex(FreeformSolidGrammarError, "body count"):
            validate_solid_grammar(raw, profile_ids())
        raw = load_solid(); raw["limits"]["measurement_relative_tolerance"] = 0.1
        with self.assertRaisesRegex(FreeformSolidGrammarError, "tolerance policy"):
            validate_solid_grammar(raw, profile_ids())
        raw = load_solid(); raw["candidates"][0]["family"] = "removed_required_family"
        with self.assertRaisesRegex(FreeformSolidGrammarError, "family coverage"):
            validate_solid_grammar(raw, profile_ids())


@unittest.skipUnless(HAS_CADQUERY, "CadQuery kernel tests use the pinned Work 092 environment")
class FreeformSolidKernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from scripts.cad.generate_freeform_solid_corpus import execute_candidate  # noqa: PLC0415

        cls.execute_candidate = staticmethod(execute_candidate)
        cls.profiles = {item["profile_id"]: item for item in load_wire()["profiles"]}

    def test_entire_corpus_executes_declared_features_and_exact_body_counts(self) -> None:
        coverage = set()
        for candidate in load_solid()["candidates"]:
            with self.subTest(candidate=candidate["candidate_id"]):
                shape, trace = self.execute_candidate(candidate, self.profiles)
                self.assertTrue(shape.isValid())
                self.assertGreater(shape.Volume(), 0.0)
                self.assertEqual(candidate["expected_body_count"], len(shape.Solids()))
                self.assertEqual(len(candidate["features"]), len(trace))
                coverage.update(item["operator"] for item in trace)
        self.assertEqual(set(OPERATORS), coverage)

    def test_empty_subtraction_disconnected_union_and_shell_self_erasure_fail(self) -> None:
        candidate = deepcopy(load_solid()["candidates"][1])
        candidate["features"][-1]["inputs"] = ["outer", "outer"]
        with self.assertRaisesRegex(RuntimeError, "invalid, empty"):
            self.execute_candidate(candidate, self.profiles)

        candidate = deepcopy(load_solid()["candidates"][0])
        candidate["features"][4]["parameters"]["points_m"] = [[0.5, 0.0, 0.05], [0.52, 0.0, 0.07], [0.54, 0.0, 0.09]]
        candidate["features"][3]["parameters"]["translation_m"] = [0.5, 0.0, 0.05]
        with self.assertRaisesRegex(RuntimeError, "final body policy"):
            self.execute_candidate(candidate, self.profiles)

        candidate = deepcopy(load_solid()["candidates"][5])
        candidate["features"][-1]["parameters"]["thickness_m"] = 0.2
        with self.assertRaises(Exception):
            self.execute_candidate(candidate, self.profiles)


if __name__ == "__main__":
    unittest.main()
