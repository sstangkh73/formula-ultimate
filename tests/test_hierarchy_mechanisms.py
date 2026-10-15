"""Tests for the v2 mechanism layer framework and structural deck (Work 160)."""

from __future__ import annotations

import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np

from formula_ultimate.hierarchy.composition import LeafMaterial
from formula_ultimate.hierarchy.leaf_geometry import (
    LeafProgramError,
    closure_problems,
    placement_transforms,
    read_binary_stl,
    volume_and_centroid,
)
from formula_ultimate.hierarchy.mechanisms import (
    DECK_ASSEMBLY,
    DECK_ID,
    DECK_SEAT_ID,
    ClusterBounds,
    chamfered_rectangle,
    measure_cluster,
    mechanism_problems,
    merge_mechanism_layer,
    plan_mechanisms,
    prism_program,
    prism_vertices,
    roll_up_manifest_nodes,
    signed_area,
    validate_mechanism_program,
)
from formula_ultimate.hierarchy.part_tree import AssemblyNode, PartNode, PartTree, roll_up


ROOT = Path(__file__).resolve().parents[1]
CAD_PYTHON = ROOT / ".tools" / "cadquery-mcp" / "Scripts" / "python.exe"
CATALOGUE = (LeafMaterial("test-material-a", 1000.0, "synthetic"),
             LeafMaterial("test-material-b", 2000.0, "synthetic"))
BOUNDS = ClusterBounds(lo=(-0.2, -1.3, -1.4), hi=(2.2, 0.6, 1.2), lowest_leaf="g1.p0",
                       lowest_point=(0.3, -0.2, -1.4))


def _box_mesh(lo, hi) -> np.ndarray:
    (x0, y0, z0), (x1, y1, z1) = lo, hi
    v = np.array([[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],
                  [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]], dtype=float)
    faces = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4),
             (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
    return v[np.array(faces)]


class PrismProgramTests(unittest.TestCase):
    def _square(self, side=1.0):
        return [[-side / 2, -side / 2], [side / 2, -side / 2], [side / 2, side / 2], [-side / 2, side / 2]]

    def test_valid_program_with_hole_and_placement(self):
        program = prism_program("m9-x.part", "test", self._square(), 0.2,
                                placement_transforms("y", False, 0.0, [1.0, 2.0, 3.0]),
                                holes=[self._square(0.3)])
        validate_mechanism_program(program)
        verts = prism_vertices(program)
        self.assertEqual(verts.shape, (16, 3))
        # Local +z maps to world +y; the translation is applied last.
        self.assertAlmostEqual(float(verts[:, 1].min()), 2.0, places=12)
        self.assertAlmostEqual(float(verts[:, 1].max()), 2.2, places=12)

    def test_rejects_clockwise_outer_and_escaping_hole(self):
        clockwise = list(reversed(self._square()))
        with self.assertRaises(LeafProgramError):
            prism_program("m9-x.part", "test", clockwise, 0.2, placement_transforms("z", False, 0.0, [0, 0, 0]))
        with self.assertRaises(LeafProgramError):
            prism_program("m9-x.part", "test", self._square(), 0.2, placement_transforms("z", False, 0.0, [0, 0, 0]),
                          holes=[[[0.4, 0.4], [0.7, 0.4], [0.7, 0.7]]])

    def test_rejects_tampered_extrusion(self):
        program = prism_program("m9-x.part", "test", self._square(), 0.2,
                                placement_transforms("z", False, 0.0, [0, 0, 0]))
        bad = copy.deepcopy(program)
        bad["candidate"]["features"][1]["parameters"]["taper_rad"] = 0.1
        with self.assertRaises(LeafProgramError):
            validate_mechanism_program(bad)

    def test_chamfered_rectangle_is_counter_clockwise(self):
        points = chamfered_rectangle(0.0, 3.0, 0.0, 2.0, 0.1)
        self.assertEqual(len(points), 8)
        self.assertAlmostEqual(signed_area(points), 6.0 - 4 * 0.005, places=12)


class PlanningTests(unittest.TestCase):
    def test_measure_cluster_finds_box_and_lowest_leaf(self):
        meshes = {"b": _box_mesh((0, 0, -1.0), (1, 1, 0)), "a": _box_mesh((-2, 0.5, -0.5), (0, 2, 3))}
        bounds = measure_cluster(meshes)
        self.assertEqual(bounds.lo, (-2.0, 0.0, -1.0))
        self.assertEqual(bounds.hi, (1.0, 2.0, 3.0))
        self.assertEqual(bounds.lowest_leaf, "b")
        self.assertEqual(bounds.lowest_point[2], -1.0)

    def test_deck_sits_under_the_cluster_and_is_seed_driven(self):
        layer = plan_mechanisms(11, BOUNDS, CATALOGUE)
        self.assertEqual(mechanism_problems(layer, BOUNDS, ["g1.p0"]), [])
        self.assertEqual(plan_mechanisms(11, BOUNDS, CATALOGUE), layer)
        deck = {p.id: p for p in layer.parts}[DECK_ID]
        verts = prism_vertices(deck.program)
        self.assertAlmostEqual(float(verts[:, 2].max()), BOUNDS.lo[2], places=12)
        self.assertLess(float(verts[:, 0].min()), BOUNDS.lo[0])
        self.assertGreater(float(verts[:, 0].max()), BOUNDS.hi[0] + 0.8)  # the reserved bay
        self.assertEqual(layer.interfaces[0], {"id": DECK_SEAT_ID, "a": DECK_ID, "b": "g1.p0", "kind": "bonded"})
        self.assertEqual(layer.evidence, {"load_structure": {"members": [DECK_ID]}})
        self.assertNotEqual(plan_mechanisms(23, BOUNDS, CATALOGUE).parts[0].program, deck.program)

    def test_problems_detect_a_misplaced_deck(self):
        layer = plan_mechanisms(11, BOUNDS, CATALOGUE)
        lower = ClusterBounds(lo=(BOUNDS.lo[0], BOUNDS.lo[1], BOUNDS.lo[2] - 0.01), hi=BOUNDS.hi,
                              lowest_leaf=BOUNDS.lowest_leaf, lowest_point=BOUNDS.lowest_point)
        self.assertIn("deck top is not at the cluster's lowest height", mechanism_problems(layer, lower, ["g1.p0"]))
        self.assertTrue(mechanism_problems(layer, BOUNDS, [DECK_ID, "g1.p0"]))


class ManifestMergeTests(unittest.TestCase):
    def _manifest(self):
        return {
            "root": "vehicle",
            "nodes": [
                {"id": "vehicle", "kind": "assembly", "children": ["g1"], "functions": [],
                 "mass_kg": 3.0, "center_of_mass_m": [1.0 / 3.0, 0.0, 0.0]},
                {"id": "g1", "kind": "assembly", "children": ["g1.p0", "g1.p1"], "functions": ["energy_storage"],
                 "mass_kg": 3.0, "center_of_mass_m": [1.0 / 3.0, 0.0, 0.0]},
                {"id": "g1.p0", "kind": "part", "mass_kg": 1.0, "center_of_mass_m": [1.0, 0.0, 0.0]},
                {"id": "g1.p1", "kind": "part", "mass_kg": 2.0, "center_of_mass_m": [0.0, 0.0, 0.0]},
            ],
            "interfaces": [{"id": "i0", "a": "g1.p0", "b": "g1.p1", "kind": "bonded"}],
        }

    def test_roll_up_matches_part_tree(self):
        program = {"x": 1}
        parts = [PartNode(id=f"p{i}", mesh=f"m/p{i}.stl", material_id="m", density_kg_m3=1.0, mass_kg=m,
                          center_of_mass_m=c, grammar_version="g", program=program)
                 for i, (m, c) in enumerate([(1.3, (0.1, 0.2, 0.3)), (2.7, (-1.0, 4.0, 0.5)), (0.4, (3.0, 3.0, 3.0))])]
        tree = PartTree(root="r", nodes=(AssemblyNode("r", ("a", "p2"), ()), AssemblyNode("a", ("p0", "p1"), ()),
                                         *parts), interfaces=(), contact_tolerance_m=1e-4)
        expected = roll_up(tree)
        nodes = [{"id": "r", "kind": "assembly", "children": ["a", "p2"], "mass_kg": 0.0, "center_of_mass_m": [0, 0, 0]},
                 {"id": "a", "kind": "assembly", "children": ["p0", "p1"], "mass_kg": 0.0, "center_of_mass_m": [0, 0, 0]}]
        nodes += [{"id": p.id, "kind": "part", "mass_kg": p.mass_kg, "center_of_mass_m": list(p.center_of_mass_m)}
                  for p in parts]
        rolled = {n["id"]: n for n in roll_up_manifest_nodes(nodes, "r")}
        for node_id, (mass, com) in expected.items():
            self.assertEqual(rolled[node_id]["mass_kg"], mass)
            self.assertEqual(tuple(rolled[node_id]["center_of_mass_m"]), com)

    def test_merge_appends_layer_under_root(self):
        bounds = ClusterBounds(lo=(-1.0, -1.0, -0.5), hi=(1.0, 1.0, 0.5), lowest_leaf="g1.p0",
                               lowest_point=(0.0, 0.0, -0.5))
        layer = plan_mechanisms(5, bounds, CATALOGUE)
        measured = {DECK_ID: {"mass_kg": 6.0, "center_of_mass_m": [2.0, 0.0, -0.52]}}
        merged = merge_mechanism_layer(self._manifest(), layer, measured, lambda i: f"meshes/{i}.stl")
        nodes = {n["id"]: n for n in merged["nodes"]}
        self.assertEqual(nodes["vehicle"]["children"], ["g1", DECK_ASSEMBLY])
        self.assertEqual(nodes[DECK_ASSEMBLY]["functions"], ["load_structure"])
        self.assertEqual(nodes["vehicle"]["mass_kg"], 9.0)
        self.assertAlmostEqual(nodes["vehicle"]["center_of_mass_m"][0], (1.0 + 12.0) / 9.0, places=12)
        deck = nodes[DECK_ID]
        self.assertEqual(set(deck), {"id", "kind", "mesh", "material_id", "density_kg_m3", "mass_kg",
                                     "center_of_mass_m", "generator"})
        self.assertEqual(deck["generator"]["program"], layer.parts[0].program)
        self.assertEqual([i["id"] for i in merged["interfaces"]], ["i0", DECK_SEAT_ID])


CAD_CHECK = r"""
import json, sys
from pathlib import Path
root, spec, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path[:0] = [str(root / "src"), str(root), str(root / "scripts" / "hierarchy")]
from functional_realization import realize_program
program = json.loads(spec.read_text(encoding="utf-8"))
print(json.dumps(realize_program(program, out / "deck.stl", 1000.0)))
"""


@unittest.skipUnless(CAD_PYTHON.is_file(), "pinned CadQuery runtime is absent")
class DeckRealizationTests(unittest.TestCase):
    def test_deck_mesh_is_closed_with_its_top_at_the_cluster_bottom(self):
        layer = plan_mechanisms(11, BOUNDS, CATALOGUE)
        deck = layer.parts[0]
        with tempfile.TemporaryDirectory() as tmp:
            spec = Path(tmp) / "deck.json"
            spec.write_text(json.dumps(deck.program), encoding="utf-8")
            done = subprocess.run([str(CAD_PYTHON), "-c", CAD_CHECK, str(ROOT), str(spec), tmp], cwd=ROOT,
                                  capture_output=True, text=True, timeout=600)
            self.assertEqual(done.returncode, 0, done.stderr)
            tris = read_binary_stl(Path(tmp) / "deck.stl")
        self.assertEqual(closure_problems(tris), [])
        pts = tris.reshape(-1, 3)
        self.assertAlmostEqual(float(pts[:, 2].max()), BOUNDS.lo[2], delta=1e-6)
        outline = deck.program["profile"]["loops"][0]["segments"][0]["parameters"]["points_m"][:-1]
        volume, _ = volume_and_centroid(tris)
        self.assertAlmostEqual(volume / (signed_area(outline) * deck.program["height_m"]), 1.0, delta=1e-5)


if __name__ == "__main__":
    unittest.main()
