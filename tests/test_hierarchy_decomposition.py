import dataclasses
import unittest

from formula_ultimate.hierarchy.decomposition import (
    DEFAULT_CONFIG,
    ROOT_ID,
    DecompositionFailure,
    _attempt,
    config_sha256,
    constraint_violations,
    decompose,
    leaves,
    levels,
    subtree_height,
    subtree_leaf_count,
    topology_signature,
)
from formula_ultimate.hierarchy.part_tree import JOINT_KINDS
from formula_ultimate.topology.functional_vehicle import REQUIRED_CAPABILITIES


ACCEPTANCE_SEEDS = (11, 23, 37)
SWEEP_SEEDS = tuple(range(0, 30))


class DecompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trees = {seed: decompose(seed) for seed in set(ACCEPTANCE_SEEDS + SWEEP_SEEDS)}

    def test_same_seed_gives_identical_tree(self):
        self.assertEqual(decompose(11), decompose(11))

    def test_declared_constraints_hold_for_every_seed(self):
        for seed, tree in self.trees.items():
            self.assertEqual(constraint_violations(tree, DEFAULT_CONFIG), [], f"seed {seed}")
            self.assertGreaterEqual(levels(tree), 4)
            self.assertGreaterEqual(len(leaves(tree)), 150)

    def test_every_capability_has_a_deep_named_subtree(self):
        for seed, tree in self.trees.items():
            for capability in REQUIRED_CAPABILITIES:
                deep = [
                    node.id for node in tree.nodes
                    if node.children and capability in node.functions
                    and subtree_height(tree, node.id) >= 2
                    and subtree_leaf_count(tree, node.id) >= 5
                ]
                self.assertTrue(deep, f"seed {seed}: {capability}")

    def test_root_carries_no_capability(self):
        for tree in self.trees.values():
            self.assertEqual(tree.node_map()[ROOT_ID].functions, ())

    def test_tree_is_well_formed(self):
        for seed, tree in self.trees.items():
            node_by_id = tree.node_map()
            self.assertEqual(len(node_by_id), len(tree.nodes))
            parents = {}
            for node in tree.nodes:
                for child in node.children:
                    self.assertNotIn(child, parents, f"seed {seed}: {child} has two parents")
                    parents[child] = node.id
                    self.assertEqual(node_by_id[child].parent, node.id)
                    self.assertEqual(node_by_id[child].depth, node.depth + 1)
                if node.children:
                    self.assertIn(node.anchor_child, node.children)
            self.assertEqual(set(parents), set(node_by_id) - {ROOT_ID})

    def test_attachments_join_leaves_with_known_kinds(self):
        for tree in self.trees.values():
            node_by_id = tree.node_map()
            for item in tree.attachments:
                self.assertIn(item.kind, JOINT_KINDS)
                self.assertFalse(node_by_id[item.source].children)
                self.assertFalse(node_by_id[item.target].children)
                self.assertNotEqual(item.source, item.target)

    def test_acceptance_seeds_give_different_topologies(self):
        signatures = {topology_signature(self.trees[s], ROOT_ID) for s in ACCEPTANCE_SEEDS}
        self.assertEqual(len(signatures), len(ACCEPTANCE_SEEDS))
        for capability in sorted(REQUIRED_CAPABILITIES):
            variants = {
                frozenset(
                    topology_signature(self.trees[s], node.id)
                    for node in self.trees[s].nodes
                    if node.children and capability in node.functions
                )
                for s in ACCEPTANCE_SEEDS
            }
            self.assertGreaterEqual(len(variants), 2, capability)

    def test_sweep_seeds_all_differ(self):
        signatures = {topology_signature(self.trees[s], ROOT_ID) for s in SWEEP_SEEDS}
        self.assertEqual(len(signatures), len(SWEEP_SEEDS))

    def test_leaf_lengths_respect_floor_and_ratio(self):
        for tree in self.trees.values():
            node_by_id = tree.node_map()
            lengths = [node_by_id[n].characteristic_length_m for n in leaves(tree)]
            self.assertGreaterEqual(min(lengths), DEFAULT_CONFIG.min_leaf_length_m)
            self.assertGreaterEqual(max(lengths) / min(lengths), 100.0)

    def test_config_hash_tracks_config(self):
        changed = dataclasses.replace(DEFAULT_CONFIG, root_length_m=3.5)
        self.assertRegex(config_sha256(DEFAULT_CONFIG), r"^[0-9a-f]{64}$")
        self.assertNotEqual(config_sha256(DEFAULT_CONFIG), config_sha256(changed))
        self.assertEqual(decompose(11).config_sha256, config_sha256(DEFAULT_CONFIG))

    def test_rejected_attempts_report_violations(self):
        strict = dataclasses.replace(DEFAULT_CONFIG, min_total_leaves=10_000, max_attempts=3)
        self.assertTrue(constraint_violations(_attempt(11, 0, strict), strict))
        with self.assertRaises(DecompositionFailure):
            decompose(11, strict)

    def test_seed_must_be_int(self):
        with self.assertRaises(TypeError):
            decompose("11")
        with self.assertRaises(TypeError):
            decompose(True)


if __name__ == "__main__":
    unittest.main()
