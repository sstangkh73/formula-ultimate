from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.components.constructive_validity import ConstructiveValidityError, build_candidate, declaration_sha256, evaluate_candidate, validate_gate_config
from formula_ultimate.search.topology_mutation import protocol_sha256


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/manufacturing/constructive_validity_gate_v1.json"
MUTATION = ROOT / "config/experiments/topology_mutation_v1.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def candidate(scenario_id: str = "baseline") -> tuple[dict, dict]:
    config = load(CONFIG); family = config["representation_families"][1]
    scenario = next(item for item in config["scenarios"] if item["scenario_id"] == scenario_id)
    return config, build_candidate(config, family, scenario)


class ConstructiveValidityTests(unittest.TestCase):
    def test_config_declares_balanced_matched_campaign(self) -> None:
        config = load(CONFIG); result = validate_gate_config(config, mutation_protocol_sha256=protocol_sha256(load(MUTATION)))
        self.assertEqual("passed", result["status"]); self.assertEqual(48, result["total_opportunities"])
        self.assertEqual("synthetic_contract_fixture", config["measurement_evidence"]["status"])

    def test_baseline_accepts_and_exact_replay_matches(self) -> None:
        config, raw = candidate(); first = evaluate_candidate(raw, config); second = evaluate_candidate(raw, config)
        self.assertEqual(first, second); self.assertEqual("accepted", first["status"]); self.assertFalse(first["performance_evidence_used"])

    def test_preregistered_repair_changes_genotype_and_is_traced(self) -> None:
        config, raw = candidate("preregistered_support_repair"); result = evaluate_candidate(raw, config)
        self.assertEqual("repaired", result["status"]); self.assertEqual("add_support", result["repair_trace"][0]["operation"])
        self.assertNotEqual(result["original_genotype_sha256"], result["evaluated_genotype_sha256"])

    def test_required_injected_failures_are_visible_for_every_family(self) -> None:
        config = load(CONFIG)
        expected = {
            "self_intersection": "self_intersection", "sliver": "sliver_feature", "zero_thickness": "zero_thickness",
            "inaccessible_feature": "tool_access_blocked", "unsupported_wall": "wall_below_minimum", "hidden_repair": "hidden_repair",
        }
        for family in config["representation_families"]:
            for scenario_id, code in expected.items():
                scenario = next(item for item in config["scenarios"] if item["scenario_id"] == scenario_id)
                result = evaluate_candidate(build_candidate(config, family, scenario), config)
                self.assertEqual("rejected", result["status"]); self.assertIn(code, result["violations"])
        unsupported = evaluate_candidate(candidate("unsupported_wall")[1], config)
        self.assertIn("unsupported_overhang", unsupported["violations"])

    def test_enclosed_void_tolerance_joining_and_compatibility_reject(self) -> None:
        config, raw = candidate(); raw["evidence"]["enclosed_void_count"] = 1; raw["evidence"]["minimum_escape_hole_m"] = 0.0001
        raw["evidence"]["requested_tolerance_m"] = 0.00001; raw["evidence"]["joining_access_fraction"] = 0.1; raw["material_id"] = "material_pending_006"
        result = evaluate_candidate(raw, config)
        self.assertEqual("rejected", result["status"])
        self.assertTrue({"enclosed_void_not_vented", "tolerance_too_tight", "joining_access_blocked", "material_process_incompatible"}.issubset(result["violations"]))

    def test_post_observation_and_budget_repairs_reject_without_trace(self) -> None:
        config, raw = candidate("preregistered_support_repair"); raw["evaluation_observed"] = True
        result = evaluate_candidate(raw, config); self.assertIn("post_observation_repair_prohibited", result["violations"]); self.assertFalse(result["repair_trace"])
        config, raw = candidate(); raw["proposed_repairs"] = ["add_support", "increase_escape_hole"]
        result = evaluate_candidate(raw, config); self.assertIn("repair_budget_exceeded", result["violations"]); self.assertFalse(result["repair_trace"])

    def test_invalid_brep_solid_count_radius_and_ligament_all_report(self) -> None:
        config, raw = candidate(); raw["evidence"].update({"brep_valid": False, "solid_count": 0, "minimum_radius_m": 0.0, "minimum_ligament_m": 0.0})
        result = evaluate_candidate(raw, config)
        self.assertTrue({"invalid_brep", "invalid_solid_count", "radius_below_minimum", "ligament_below_minimum"}.issubset(result["violations"]))

    def test_unknown_field_nonfinite_and_boolean_alias_fail_schema(self) -> None:
        config, raw = candidate(); raw["legacy_repair"] = True
        with self.assertRaisesRegex(ConstructiveValidityError, "schema mismatch"): evaluate_candidate(raw, config)
        config, raw = candidate(); raw["evidence"]["minimum_wall_m"] = math.nan
        with self.assertRaisesRegex(ConstructiveValidityError, "finite"): evaluate_candidate(raw, config)
        config, raw = candidate(); raw["evidence"]["brep_valid"] = 1
        with self.assertRaisesRegex(ConstructiveValidityError, "Boolean"): evaluate_candidate(raw, config)

    def test_protocol_or_config_mutation_fails_or_changes_identity(self) -> None:
        config = load(CONFIG)
        with self.assertRaisesRegex(ConstructiveValidityError, "identity mismatch"):
            validate_gate_config(config, mutation_protocol_sha256="0" * 64)
        changed = deepcopy(config); changed["process_profiles"][0]["limits"]["minimum_wall_m"] *= 2
        self.assertNotEqual(declaration_sha256(config), declaration_sha256(changed))


if __name__ == "__main__":
    unittest.main()
