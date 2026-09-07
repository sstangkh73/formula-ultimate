from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from formula_ultimate.experiments.discovery_registration import digest
from formula_ultimate.experiments.integration_intake import (
    IntegrationIntakeViolation,
    active_path_evidence,
    audit_work100_result,
    validate_config,
)
from formula_ultimate.topology.functional_vehicle import REQUIRED_CAPABILITIES


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/experiments/work101_integration_intake_v1.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def edge(edge_id: str, a: str, b: str, mechanical_flow: float, thermal_flow: float) -> tuple[dict, dict]:
    common = {"edge_id": edge_id, "segment": 0, "a": a, "b": b}
    return ({**common, "flow": mechanical_flow}, {**common, "flow": thermal_flow})


def candidate(candidate_id: str, treatment: str, seed: int, value: float, signature: str, edges: list[tuple[dict, dict]], *, survivor: bool = True) -> dict:
    mechanical = [item[0] for item in edges]
    thermal = [item[1] for item in edges]
    return {
        "candidate_id": candidate_id,
        "treatment": treatment,
        "seed": seed,
        "functional_signature": signature,
        "candidate_survivor": survivor,
        "training": {
            "value": value,
            "error": 0.001,
            "primary": {"levels": [{"mechanical_field": {"segments": mechanical}, "thermal_field": {"segments": thermal}}]},
        },
    }


def chain(prefix: str = "") -> list[tuple[dict, dict]]:
    return [
        edge(f"{prefix}edge_a", f"{prefix}source", f"{prefix}middle", 5000.0, 30.0),
        edge(f"{prefix}edge_b", f"{prefix}middle", f"{prefix}sink", 5000.0, 30.0),
    ]


def sealed_report(config: dict, candidates: list[dict]) -> dict:
    survivors = sorted(item["candidate_id"] for item in candidates if item["candidate_survivor"])
    deterministic = {
        "schema": "fixture",
        "registration_sha256": "a" * 64,
        "candidates": candidates,
        "survivors": survivors,
    }
    deterministic["deterministic_sha256"] = digest(deterministic)
    config["source"].update({
        "work100_registration_sha256": "a" * 64,
        "work100_deterministic_sha256": deterministic["deterministic_sha256"],
        "expected_candidate_count": len(candidates),
        "expected_survivor_count": len(survivors),
    })
    return {
        "deterministic_evidence": deterministic,
        "decision_replay": {"status": "exact"},
        "scientific_admission": {"accounting_admissible": True, "scientific_survivors": len(survivors), "physical_validation": False},
    }


class IntegrationIntakeTests(unittest.TestCase):
    def test_config_uses_existing_technology_neutral_capability_contract(self) -> None:
        config = load_config()
        self.assertEqual("passed", validate_config(config)["status"])
        self.assertEqual(set(REQUIRED_CAPABILITIES), set(config["capabilities"]["required_vehicle"]))
        self.assertEqual(["load_structure"], config["capabilities"]["work100_contribution"])

    def test_zero_flow_declared_branch_is_pruned_not_called_a_mechanism(self) -> None:
        config = load_config()
        fixed = candidate("fixed", "FIXED_TOPOLOGY", 7, 0.5, "fixed_signature", chain())
        branched = chain() + [edge("declared_branch", "middle", "leaf", 1e-12, 1e-14)]
        graph = candidate("graph", "GRAPH_ONLY", 7, 0.5, "different_declared_signature", branched)
        report = sealed_report(config, [fixed, graph])
        result = audit_work100_result(config, report)
        row = next(item for item in result["candidate_causality"] if item["candidate_id"] == "graph")
        self.assertEqual("declared_topology_only_inactive_appendage", row["classification"])
        self.assertFalse(row["active_topology_distinct_from_fixed"])
        self.assertEqual(1, row["path_evidence"]["inactive_edge_count"])
        self.assertEqual(0, result["summary"]["functional_mechanism_candidate_count"])

    def test_active_parallel_path_and_meaningful_response_are_mechanism_candidate(self) -> None:
        config = load_config()
        fixed = candidate("fixed", "FIXED_TOPOLOGY", 7, 0.5, "fixed_signature", chain())
        parallel = [
            edge("p1", "source", "middle", 2500.0, 15.0),
            edge("p2", "middle", "sink", 2500.0, 15.0),
            edge("p3", "source", "other", 2500.0, 15.0),
            edge("p4", "other", "sink", 2500.0, 15.0),
        ]
        graph = candidate("graph", "GRAPH_ONLY", 7, 0.56, "graph_signature", parallel)
        report = sealed_report(config, [fixed, graph])
        result = audit_work100_result(config, report)
        row = next(item for item in result["candidate_causality"] if item["candidate_id"] == "graph")
        self.assertEqual("functional_mechanism_candidate", row["classification"])
        self.assertTrue(row["active_topology_distinct_from_fixed"])
        self.assertTrue(row["response_difference_meaningful"])

    def test_identifier_rename_does_not_change_unlabelled_active_topology(self) -> None:
        config = load_config()
        left = candidate("left", "FIXED_TOPOLOGY", 7, 0.5, "one", chain())
        right = candidate("right", "RANDOM_CONTROL", 7, 0.5, "two", chain("renamed_"))
        left_path = active_path_evidence(left, config["activity"])
        right_path = active_path_evidence(right, config["activity"])
        self.assertEqual(left_path["active_topology_sha256"], right_path["active_topology_sha256"])

    def test_incomplete_capability_and_evidence_coverage_blocks_program_exit(self) -> None:
        config = load_config()
        fixed = candidate("fixed", "FIXED_TOPOLOGY", 7, 0.5, "fixed", chain())
        report = sealed_report(config, [fixed])
        result = audit_work100_result(config, report)
        intake = result["integration_intake"]
        self.assertEqual("blocked_incomplete_capability_and_evidence_coverage", intake["status"])
        self.assertEqual(sorted(set(REQUIRED_CAPABILITIES) - {"load_structure"}), intake["missing_vehicle_capabilities"])
        self.assertFalse(intake["promotion_ready"])
        self.assertFalse(intake["whole_vehicle_candidate_created"])
        self.assertFalse(intake["work101_program_exit"])

    def test_nonsurvivor_cannot_become_a_mechanism_candidate(self) -> None:
        config = load_config()
        fixed = candidate("fixed", "FIXED_TOPOLOGY", 7, 0.5, "fixed", chain())
        parallel = [
            edge("p1", "source", "middle", 2500.0, 15.0),
            edge("p2", "middle", "sink", 2500.0, 15.0),
            edge("p3", "source", "other", 2500.0, 15.0),
            edge("p4", "other", "sink", 2500.0, 15.0),
        ]
        failed = candidate("failed", "GRAPH_ONLY", 7, 0.6, "graph", parallel, survivor=False)
        report = sealed_report(config, [fixed, failed])
        result = audit_work100_result(config, report)
        row = next(item for item in result["candidate_causality"] if item["candidate_id"] == "failed")
        self.assertEqual("not_a_scoped_survivor", row["classification"])
        self.assertEqual(0, result["summary"]["functional_mechanism_candidate_count"])

    def test_result_and_source_identity_tampering_fail_closed(self) -> None:
        config = load_config()
        fixed = candidate("fixed", "FIXED_TOPOLOGY", 7, 0.5, "fixed", chain())
        report = sealed_report(config, [fixed])
        tampered = deepcopy(report)
        tampered["deterministic_evidence"]["candidates"][0]["training"]["value"] = 0.1
        with self.assertRaisesRegex(IntegrationIntakeViolation, "identity mismatch"):
            audit_work100_result(config, tampered)
        tampered = deepcopy(report)
        tampered["deterministic_evidence"]["survivors"] = []
        body = deepcopy(tampered["deterministic_evidence"])
        body.pop("deterministic_sha256")
        tampered["deterministic_evidence"]["deterministic_sha256"] = digest(body)
        config["source"]["work100_deterministic_sha256"] = tampered["deterministic_evidence"]["deterministic_sha256"]
        with self.assertRaisesRegex(IntegrationIntakeViolation, "survivor count|membership"):
            audit_work100_result(config, tampered)

    def test_canonicalization_bound_fails_instead_of_using_identifier_fallback(self) -> None:
        config = load_config()
        oversized = [edge(f"e{i}", f"n{i}", f"n{i+1}", 5000.0, 30.0) for i in range(8)]
        specimen = candidate("large", "FIXED_TOPOLOGY", 7, 0.5, "large", oversized)
        with self.assertRaisesRegex(IntegrationIntakeViolation, "canonicalization bound"):
            active_path_evidence(specimen, config["activity"])

    def test_repeated_audit_is_exact_and_does_not_mutate_source(self) -> None:
        config = load_config()
        fixed = candidate("fixed", "FIXED_TOPOLOGY", 7, 0.5, "fixed", chain())
        report = sealed_report(config, [fixed])
        before = deepcopy(report)
        first = audit_work100_result(config, report)
        second = audit_work100_result(config, report)
        self.assertEqual(first, second)
        self.assertEqual(before, report)
        body = deepcopy(first)
        observed = body.pop("result_sha256")
        self.assertEqual(digest(body), observed)


if __name__ == "__main__":
    unittest.main()
