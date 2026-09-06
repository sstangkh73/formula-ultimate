from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from formula_ultimate.search.executable_morphology import (
    ARCHITECTURE_OPERATORS,
    GEOMETRY_OPERATORS,
    MorphologyViolation,
    OPERATORS,
    digest,
    functional_signature,
    mutate,
    root_genome,
    validate_config,
    validate_genome,
)
from formula_ultimate.search.morphology_archive import EVIDENCE_SCOPE, MorphologyArchive


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/experiments/executable_morphology_qd_v1.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def archive_record(cid: str, *, disposition: str = "feasible", quality: float | None = 1.0,
                   margin: float | None = None, cost: float = 1.0, novelty: float = 1.0) -> dict:
    return {
        "candidate_id": cid,
        "context_sha256": digest(["context", cid]),
        "functional_signature": digest(["function", cid]),
        "descriptors": {"part_count": 2, "interface_cycle_rank": 0, "branch_node_count": 0, "terminal_domain_count": 2},
        "disposition": disposition,
        "quality": quality,
        "margin": margin,
        "cost": cost,
        "novelty": novelty,
        "parents": [],
        "evidence_scope": EVIDENCE_SCOPE,
    }


class ExecutableMorphologyTests(unittest.TestCase):
    def test_config_freezes_multiple_seeds_operators_archive_and_claim_boundary(self) -> None:
        result = validate_config(load_config())
        self.assertEqual("passed", result["status"])
        self.assertGreaterEqual(result["seed_count"], 2)
        self.assertEqual(len(OPERATORS), result["operator_count"])
        self.assertIn("physical_validation", load_config()["claim_boundary"]["prohibited_claims"])

    def test_root_is_valid_and_external_function_is_seed_invariant(self) -> None:
        limits = load_config()["limits"]
        a, b = root_genome(7), root_genome(19)
        self.assertEqual("passed", validate_genome(a, limits)["status"])
        self.assertEqual(functional_signature(a), functional_signature(b))
        self.assertNotEqual(digest(a), digest(b))

    def test_every_registered_operator_is_deterministic_and_valid(self) -> None:
        limits = load_config()["limits"]
        parent = root_genome(7)
        for step, operator in enumerate(OPERATORS, start=1):
            first = mutate(parent, operator, seed=7, step=step, limits=limits)
            second = mutate(parent, operator, seed=7, step=step, limits=limits)
            self.assertEqual(first, second, operator)
            self.assertEqual("passed", validate_genome(first["child"], limits)["status"])
            self.assertEqual(operator in GEOMETRY_OPERATORS, first["trace"]["declared_geometry_change"])
            self.assertEqual(operator in ARCHITECTURE_OPERATORS, first["trace"]["declared_architecture_change"])
            self.assertEqual(digest(first["trace"]), first["lineage_sha256"])
            parent = first["child"]

    def test_split_and_merge_change_decomposition_and_terminal_ancestry_remains_valid(self) -> None:
        limits = load_config()["limits"]
        parent = mutate(root_genome(7), "grow_branch", seed=7, step=1, limits=limits)["child"]
        before = len(parent["parts"])
        split = mutate(parent, "split_part", seed=7, step=2, limits=limits)["child"]
        self.assertEqual(before + 1, len(split["parts"]))
        self.assertGreater(len(split["interfaces"]), len(parent["interfaces"]))
        self.assertNotEqual(functional_signature(parent), functional_signature(split))
        merged = mutate(split, "merge_parts", seed=7, step=3, limits=limits)["child"]
        self.assertEqual(len(split["parts"]) - 1, len(merged["parts"]))
        self.assertEqual("passed", validate_genome(merged, limits)["status"])
        self.assertEqual({"external_source", "external_sink"}, {item for terminal in merged["terminals"] for item in terminal["ancestry"]})

    def test_split_preserves_existing_interface_endpoints_for_every_registered_seed(self) -> None:
        config = load_config()
        for seed in config["seeds"]:
            parent = mutate(root_genome(seed), "perturb_node", seed=seed, step=1, limits=config["limits"])["child"]
            parent = mutate(parent, "grow_branch", seed=seed, step=2, limits=config["limits"])["child"]
            child = mutate(parent, "split_part", seed=seed, step=3, limits=config["limits"])["child"]
            self.assertEqual("passed", validate_genome(child, config["limits"])["status"])

    def test_nonfinite_short_edge_stale_interface_and_missing_ancestry_fail_closed(self) -> None:
        limits = load_config()["limits"]
        bad = root_genome(7)
        bad["parts"][0]["nodes"][0]["radius_m"] = float("nan")
        with self.assertRaisesRegex(MorphologyViolation, "finite"):
            validate_genome(bad, limits)
        bad = root_genome(7)
        bad["parts"][0]["nodes"][1]["point_m"] = list(bad["parts"][0]["nodes"][0]["point_m"])
        with self.assertRaisesRegex(MorphologyViolation, "edge length"):
            validate_genome(bad, limits)
        bad = root_genome(7)
        bad["interfaces"][0]["node_b"] = "missing"
        with self.assertRaisesRegex(MorphologyViolation, "interface node"):
            validate_genome(bad, limits)
        bad = root_genome(7)
        bad["terminals"][0]["ancestry"] = []
        with self.assertRaisesRegex(MorphologyViolation, "ancestry"):
            validate_genome(bad, limits)

    def test_identifier_or_controller_change_does_not_fake_geometry_operator(self) -> None:
        limits = load_config()["limits"]
        parent = root_genome(7)
        child = mutate(parent, "mutate_controller", seed=7, step=1, limits=limits)
        self.assertFalse(child["trace"]["declared_geometry_change"])
        renamed = deepcopy(parent)
        renamed["genome_id"] = "renamed_only"
        self.assertEqual(functional_signature(parent), functional_signature(renamed))


class MorphologyArchiveTests(unittest.TestCase):
    def make_archive(self) -> MorphologyArchive:
        policy = load_config()["archive"]
        return MorphologyArchive(policy["capacity_per_niche"], policy["reproduction_caps"])

    def test_archive_is_bounded_and_uses_deterministic_quality_ties(self) -> None:
        archive = self.make_archive()
        archive.update(archive_record("worse", quality=1.0, cost=2.0))
        archive.update(archive_record("best", quality=3.0, cost=3.0))
        decision = archive.update(archive_record("middle", quality=2.0, cost=1.0))
        self.assertTrue(decision["retained"])
        self.assertEqual(["worse"], decision["evicted"])
        feasible = archive.snapshot()["niches"][0]["feasible"]
        self.assertEqual(["best", "middle"], [item["candidate_id"] for item in feasible])

    def test_failed_and_unresolved_are_separate_and_reproduction_is_capped(self) -> None:
        archive = self.make_archive()
        archive.update(archive_record("ok", disposition="feasible", quality=2.0))
        archive.update(archive_record("bad", disposition="failed", quality=None, margin=-0.2))
        archive.update(archive_record("unknown", disposition="unresolved", quality=None, cost=0.5))
        niche = archive.snapshot()["niches"][0]
        self.assertEqual(["ok"], [item["candidate_id"] for item in niche["feasible"]])
        self.assertEqual(["bad"], [item["candidate_id"] for item in niche["failed"]])
        self.assertEqual(["unknown"], [item["candidate_id"] for item in niche["unresolved"]])
        self.assertEqual({"feasible": ["ok"], "failed": ["bad"], "unresolved": ["unknown"]}, archive.select_reproducers())

    def test_novelty_cannot_erase_failure_or_expand_claim_scope(self) -> None:
        archive = self.make_archive()
        record = archive_record("bad", disposition="failed", quality=None, margin=-0.1, novelty=1e9)
        archive.update(record)
        self.assertEqual([], archive.snapshot()["niches"][0]["feasible"])
        record["candidate_id"] = "forged"
        record["context_sha256"] = digest("forged")
        record["evidence_scope"] = "physical_feasibility"
        with self.assertRaisesRegex(MorphologyViolation, "evidence scope"):
            archive.update(record)

    def test_archive_candidate_cannot_be_overwritten(self) -> None:
        archive = self.make_archive()
        archive.update(archive_record("same"))
        with self.assertRaisesRegex(MorphologyViolation, "overwritten"):
            archive.update(archive_record("same", quality=9.0))


@unittest.skipUnless(importlib.util.find_spec("cadquery"), "CadQuery is available only in the pinned local CAD environment")
class RealCadMorphologyTests(unittest.TestCase):
    def test_geometry_operator_changes_step_hash_and_measured_field(self) -> None:
        from scripts.experiments.run_executable_morphology_qd import execute_genome

        config = load_config()
        root = root_genome(7)
        child = mutate(root, "mutate_radius_field", seed=7, step=1, limits=config["limits"])["child"]
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            a = execute_genome(root, config["limits"], folder / "a.step")
            b = execute_genome(child, config["limits"], folder / "b.step")
        self.assertNotEqual(a["geometry_sha256"], b["geometry_sha256"])
        self.assertNotEqual(a["measurement_sha256"], b["measurement_sha256"])
        self.assertNotEqual(a["measurement"]["volume_m3"], b["measurement"]["volume_m3"])


if __name__ == "__main__":
    unittest.main()
