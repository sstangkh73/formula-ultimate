from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from formula_ultimate.search.topology_genome import TopologyGenomeError, declaration_sha256, validate_topology_corpus
from formula_ultimate.search.topology_mutation import (
    OPERATORS,
    TOPOLOGY_OPERATORS,
    TopologyMutationError,
    propose,
    validate_mutation_protocol,
    validate_policy,
)


ROOT = Path(__file__).resolve().parents[1]
GENOMES = ROOT / "config/genomes/typed_morphology_topology_genome_v1.json"
SOLIDS = ROOT / "config/cad/freeform_brep_solid_grammar_v2.json"
PROTOCOL = ROOT / "config/experiments/topology_mutation_v1.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def candidates() -> dict[str, str]:
    return {item["candidate_id"]: item["family"] for item in load(SOLIDS)["candidates"]}


class TopologyMutationTests(unittest.TestCase):
    def test_protocol_has_equal_fixed_slots_and_exact_source(self) -> None:
        corpus, protocol = load(GENOMES), load(PROTOCOL)
        result = validate_mutation_protocol(protocol, declaration_sha256(corpus))
        self.assertEqual("passed", result["status"])
        self.assertEqual(48, result["total_slots"])
        self.assertEqual(list(OPERATORS), protocol["operator_schedule"])

    def test_same_parent_seed_and_slot_replay_exactly(self) -> None:
        corpus, protocol = load(GENOMES), load(PROTOCOL)
        args = dict(parent_genome_id="branch_four_001", operator="grow_branch", seed=5505, slot_index=0)
        first = propose(corpus, protocol, candidates(), **args)
        second = propose(corpus, protocol, candidates(), **args)
        self.assertEqual(first, second)
        changed = propose(corpus, protocol, candidates(), **{**args, "seed": 5506})
        self.assertNotEqual(first["lineage_sha256"], changed["lineage_sha256"])

    def test_at_least_four_topology_operator_families_accept_valid_children(self) -> None:
        corpus, protocol, accepted = load(GENOMES), load(PROTOCOL), set()
        for stratum in protocol["initializer_strata"]:
            for slot_index, operator in enumerate(protocol["operator_schedule"]):
                result = propose(corpus, protocol, candidates(), parent_genome_id=stratum["parent_genome_id"], operator=operator, seed=stratum["seed"], slot_index=slot_index)
                if result["status"] == "accepted" and operator in TOPOLOGY_OPERATORS:
                    accepted.add(operator)
                    self.assertTrue(result["declared_topology_change"])
                    self.assertNotEqual(result["parent_topology_signature"], result["child_topology_signature"])
        self.assertGreaterEqual(len(accepted), 4)

    def test_non_topology_controls_are_not_mislabeled(self) -> None:
        corpus, protocol = load(GENOMES), load(PROTOCOL)
        for index, operator in enumerate(("replace_solid_family", "insert_feature", "mutate_material_process"), start=5):
            result = propose(corpus, protocol, candidates(), parent_genome_id="serial_three_001", operator=operator, seed=2202, slot_index=index)
            self.assertEqual("accepted", result["status"])
            self.assertFalse(result["declared_topology_change"])

    def test_post_observation_mutation_fails_closed(self) -> None:
        with self.assertRaisesRegex(TopologyMutationError, "after result observation"):
            propose(load(GENOMES), load(PROTOCOL), candidates(), parent_genome_id="serial_three_001", operator="grow_branch", seed=1, slot_index=0, observation_available=True)

    def test_incompatible_process_and_impossible_joint_fail_policy(self) -> None:
        corpus, protocol = load(GENOMES), load(PROTOCOL)
        bad = deepcopy(corpus["genomes"][0]); bad["parts"][0]["material_id"] = "material_pending_006"; bad["parts"][0]["process_id"] = "process_pending_001"
        with self.assertRaisesRegex(TopologyMutationError, "incompatible"):
            validate_policy(bad, protocol)
        bad = deepcopy(corpus["genomes"][3]); bad["interfaces"][1]["domains"].append("thermal")
        with self.assertRaisesRegex(TopologyMutationError, "impossible"):
            validate_policy(bad, protocol)

    def test_cycle_and_disconnected_terminal_fail_genome_validation(self) -> None:
        corpus = load(GENOMES); corpus["genomes"][1]["parts"][0]["parent_part_id"] = "converter"; corpus["genomes"][1]["parts"][1]["parent_part_id"] = "input"
        with self.assertRaisesRegex(TopologyGenomeError, "containment cycle"):
            validate_topology_corpus(corpus, candidates())
        corpus = load(GENOMES); corpus["genomes"][1]["paths"][0]["interface_ids"][0] = "converter_to_output"
        with self.assertRaisesRegex(TopologyGenomeError, "disconnected"):
            validate_topology_corpus(corpus, candidates())

    def test_exhausted_retry_budget_is_visible(self) -> None:
        result = propose(load(GENOMES), load(PROTOCOL), candidates(), parent_genome_id="monolithic_crossdomain_001", operator="prune_branch", seed=1101, slot_index=1)
        self.assertEqual("rejected", result["status"])
        self.assertEqual(3, len(result["failures"]))
        self.assertTrue(all(item["message"] for item in result["failures"]))

    def test_protocol_and_replay_mutation_change_identity(self) -> None:
        corpus, protocol = load(GENOMES), load(PROTOCOL)
        with self.assertRaisesRegex(TopologyMutationError, "probability"):
            bad = deepcopy(protocol); bad["operator_probabilities"]["grow_branch"] = 0.5
            validate_mutation_protocol(bad, declaration_sha256(corpus))
        first = propose(corpus, protocol, candidates(), parent_genome_id="asymmetric_hybrid_six_001", operator="add_crosslink", seed=6606, slot_index=3)
        altered = propose(corpus, protocol, candidates(), parent_genome_id="asymmetric_hybrid_six_001", operator="add_crosslink", seed=6606, slot_index=4)
        self.assertNotEqual(first["lineage_sha256"], altered["lineage_sha256"])


if __name__ == "__main__":
    unittest.main()
