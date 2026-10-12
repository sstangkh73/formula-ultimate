"""Tests for the v2 flush-contact joint kinds (Work 156)."""

from __future__ import annotations

import unittest
from pathlib import Path

from formula_ultimate.hierarchy.composition import (
    DEFAULT_MATERIAL_CATALOGUE,
    load_leaf_materials,
    plan_vehicle,
)
from formula_ultimate.hierarchy.decomposition import DEFAULT_CONFIG, decompose
from formula_ultimate.hierarchy.functional import FLUSH_JOINT_KINDS, V2_DECOMPOSITION_CONFIG
from formula_ultimate.hierarchy.part_tree import JOINT_KINDS

ROOT = Path(__file__).resolve().parents[1]


class FlushJointKindTests(unittest.TestCase):
    def test_v2_kinds_are_v1_kinds_without_threaded(self):
        self.assertNotIn("threaded", FLUSH_JOINT_KINDS)
        self.assertEqual(set(FLUSH_JOINT_KINDS), set(JOINT_KINDS) - {"threaded"})
        self.assertEqual(V2_DECOMPOSITION_CONFIG.joint_kinds, FLUSH_JOINT_KINDS)

    def test_v1_default_still_draws_threaded(self):
        self.assertEqual(DEFAULT_CONFIG.joint_kinds, JOINT_KINDS)
        kinds = {a.kind for a in decompose(11, DEFAULT_CONFIG).attachments}
        self.assertIn("threaded", kinds)

    def test_only_joint_kinds_differ_from_v1_config(self):
        v1 = {k: v for k, v in vars(DEFAULT_CONFIG).items() if k != "joint_kinds"}
        v2 = {k: v for k, v in vars(V2_DECOMPOSITION_CONFIG).items() if k != "joint_kinds"}
        self.assertEqual(v1, v2)

    def test_v2_plans_have_no_axis_less_threaded_interface(self):
        catalogue = load_leaf_materials(ROOT / DEFAULT_MATERIAL_CATALOGUE)
        for seed in (0, 1, 2):
            plan = plan_vehicle(seed, catalogue, V2_DECOMPOSITION_CONFIG)
            kinds = [a.kind for a in plan.tree.attachments]
            self.assertTrue(kinds, f"seed {seed}: no attachments")
            self.assertNotIn("threaded", kinds, f"seed {seed}")
            self.assertTrue(set(kinds) <= set(FLUSH_JOINT_KINDS), f"seed {seed}: {sorted(set(kinds))}")


if __name__ == "__main__":
    unittest.main()
