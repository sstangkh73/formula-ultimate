"""Tests for the Work 152 leaf layout planner (pure Python, no CAD)."""

from __future__ import annotations

import copy
import dataclasses
import random
import unittest

import numpy as np

from formula_ultimate.hierarchy.decomposition import decompose
from formula_ultimate.hierarchy.layout import (
    LayoutResult,
    contact_problem,
    layout,
    layout_problems,
    leaf_faces,
)
from formula_ultimate.hierarchy.leaf_geometry import leaf_program, placement_transforms, with_placement
from formula_ultimate.hierarchy.part_tree import canonical_sha256

SEEDS = (11, 23, 37)


def _shifted(result: LayoutResult, leaf_id: str, axis: int, distance: float) -> LayoutResult:
    leaves = []
    for leaf in result.leaves:
        if leaf.id == leaf_id:
            program = copy.deepcopy(leaf.program)
            program["candidate"]["features"][-1]["parameters"]["translation_m"][axis] += distance
            leaf = dataclasses.replace(leaf, program=program)
        leaves.append(leaf)
    return dataclasses.replace(result, leaves=tuple(leaves))


class LayoutSeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trees = {seed: decompose(seed) for seed in SEEDS}
        cls.results = {seed: layout(tree) for seed, tree in cls.trees.items()}

    def test_every_leaf_is_placed_once_with_one_interface_per_attachment(self):
        for seed, result in self.results.items():
            tree = self.trees[seed]
            leaf_ids = sorted(n.id for n in tree.nodes if not n.children)
            self.assertEqual(sorted(leaf.id for leaf in result.leaves), leaf_ids)
            self.assertEqual(len(result.interfaces), len(leaf_ids) - 1)
            self.assertEqual(sorted(i.id for i in result.interfaces), sorted(a.id for a in tree.attachments))
            kinds = {a.id: a.kind for a in tree.attachments}
            for item in result.interfaces:
                self.assertEqual(item.kind, kinds[item.id])
                self.assertIn(item.mode, ("inside", "around"))

    def test_independent_recheck_finds_no_problem(self):
        for seed, result in self.results.items():
            self.assertEqual(layout_problems(result, self.trees[seed]), [], f"seed {seed}")

    def test_layout_is_deterministic(self):
        seed = SEEDS[0]
        again = layout(decompose(seed))
        self.assertEqual([canonical_sha256(l.program) for l in again.leaves],
                         [canonical_sha256(l.program) for l in self.results[seed].leaves])
        self.assertEqual(again.interfaces, self.results[seed].interfaces)

    def test_leaves_use_several_axes_and_side_faces(self):
        for seed, result in self.results.items():
            axes = {leaf.axis for leaf in result.leaves}
            self.assertEqual(axes, {0, 1, 2}, f"seed {seed}")
            self.assertTrue(any(i.b_face.startswith("side") for i in result.interfaces), f"seed {seed}")

    def test_lengths_stay_within_declared_bounds(self):
        for result in self.results.values():
            for leaf in result.leaves:
                self.assertGreaterEqual(leaf.characteristic_length_m, 0.004 * (1 - 1e-12))
                self.assertLessEqual(leaf.characteristic_length_m, 4.0 * leaf.planned_length_m * (1 + 1e-12))

    def test_recheck_detects_overlap_gap_and_disconnection(self):
        seed = SEEDS[0]
        result, tree = self.results[seed], self.trees[seed]
        item = result.interfaces[0]
        source = result.leaf_map()[item.a]
        k = source.axis
        size = source.box_max_m[k] - source.box_min_m[k]
        target_box = result.leaf_map()[item.b]
        toward = 1 if (target_box.box_min_m[k] + target_box.box_max_m[k]) / 2 > (source.box_min_m[k] + source.box_max_m[k]) / 2 else -1
        overlapping = layout_problems(_shifted(result, item.a, k, toward * 0.5 * size), tree)
        self.assertTrue(any("overlap" in p for p in overlapping), overlapping)
        gapped = layout_problems(_shifted(result, item.a, k, -toward * 1e-4), tree)
        self.assertTrue(any(item.id in p and "coplanar" in p for p in gapped), gapped)
        dropped = dataclasses.replace(result, interfaces=result.interfaces[1:])
        self.assertTrue(any("not connected" in p for p in layout_problems(dropped, tree)))


class FaceGeometryTests(unittest.TestCase):
    def _polyline(self, seed: int):
        rng = random.Random(seed)
        while True:
            program = leaf_program(rng, 0.2, leaf_id="f")
            if program["profile"]["family"] == "star_polyline":
                return program

    def test_axis_aligned_hull_edge_gives_a_flush_rectangular_side_face(self):
        program = self._polyline(5)
        points = np.asarray(program["profile"]["loops"][0]["segments"][0]["parameters"]["points_m"][:-1])
        a, b = points[0], points[1]
        normal = np.array([b[1] - a[1], -(b[0] - a[0])])
        hull = bool(np.all(points @ normal <= a @ normal + 1e-12))
        spin = -np.arctan2(normal[1], normal[0])  # rotate edge 0's normal onto local +x
        placed = with_placement(program, placement_transforms("z", False, float(spin), [1.0, 2.0, 3.0]))
        geometry = leaf_faces(placed)
        self.assertEqual(geometry["axis"], 2)
        self.assertTrue(geometry["aligned"])
        self.assertEqual("side0" in geometry["faces"], hull)
        for name, face in geometry["faces"].items():
            if face["kind"] == "rect":
                k = face["axis"]
                self.assertLess(np.ptp(face["corners"][:, k]), 1e-12)
                bound = geometry["hi"][k] if face["sign"] > 0 else geometry["lo"][k]
                self.assertAlmostEqual(face["plane"], bound, delta=1e-12)
        self.assertAlmostEqual(geometry["faces"]["cap0"]["plane"], 3.0, delta=1e-12)
        self.assertAlmostEqual(geometry["faces"]["cap1"]["plane"], 3.0 + program["contact"]["height_m"], delta=1e-12)

    def test_contact_rule_accepts_nested_caps_and_rejects_bad_ones(self):
        big = leaf_faces(with_placement(self._polyline(7), placement_transforms("z", False, 0.0, [0.0, 0.0, 0.0])))
        cap1 = big["faces"]["cap1"]
        small_program = leaf_program(random.Random(3), 0.02, leaf_id="s")
        small = leaf_faces(with_placement(small_program, placement_transforms(
            "z", False, 0.0, [0.0, 0.0, cap1["plane"]])))
        self.assertIsNone(contact_problem(small["faces"]["cap0"], cap1))
        lifted = leaf_faces(with_placement(small_program, placement_transforms(
            "z", False, 0.0, [0.0, 0.0, cap1["plane"] + 1e-6])))
        self.assertEqual(contact_problem(lifted["faces"]["cap0"], cap1), "faces are not coplanar")
        self.assertEqual(contact_problem(small["faces"]["cap1"], cap1), "faces are not opposed on one vehicle axis")
        far = leaf_faces(with_placement(small_program, placement_transforms(
            "z", False, 0.0, [1.0, 0.0, cap1["plane"]])))
        self.assertEqual(contact_problem(far["faces"]["cap0"], cap1), "neither face lies inside the other")


if __name__ == "__main__":
    unittest.main()
