"""Tests for the v2 wheel-and-brake ground-contact corners (Work 161)."""

from __future__ import annotations

import dataclasses
import json
import math
import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np

from formula_ultimate.hierarchy.composition import LeafMaterial
from formula_ultimate.hierarchy.ground_contacts import (
    CORNER_FUNCTIONS,
    DEFAULT_GROUND_CONTACT_CONFIG,
    add_ground_contacts,
    axle_profile,
    bore_profile,
    corner_ids,
    draw_corner_geometry,
    ground_contact_problems,
    y_prism,
)
from formula_ultimate.hierarchy.leaf_geometry import closure_problems, read_binary_stl, volume_and_centroid
from formula_ultimate.hierarchy.mechanisms import (
    DECK_ID,
    ClusterBounds,
    mechanism_problems,
    plan_mechanisms,
    prism_vertices,
)


ROOT = Path(__file__).resolve().parents[1]
CAD_PYTHON = ROOT / ".tools" / "cadquery-mcp" / "Scripts" / "python.exe"
CATALOGUE = (LeafMaterial("test-material-a", 1000.0, "synthetic"),
             LeafMaterial("test-material-b", 2000.0, "synthetic"))
BOUNDS = ClusterBounds(lo=(-0.2, -1.3, -1.4), hi=(2.2, 0.6, 1.2), lowest_leaf="g1.p0",
                       lowest_point=(0.3, -0.2, -1.4))


def _layer(seed: int):
    return add_ground_contacts(plan_mechanisms(seed, BOUNDS, CATALOGUE), seed, CATALOGUE)


class CornerPlanningTests(unittest.TestCase):
    def test_layers_pass_both_rechecks_for_many_seeds(self):
        for seed in range(30):
            layer = _layer(seed)
            self.assertEqual(mechanism_problems(layer, BOUNDS, ["g1.p0"]), [], f"seed {seed}")
            self.assertEqual(ground_contact_problems(layer), [], f"seed {seed}")

    def test_deterministic_and_seed_driven(self):
        self.assertEqual(_layer(11), _layer(11))
        wheel = corner_ids(1)["wheel"]
        programs = [{p.id: p.program for p in _layer(s).parts}[wheel] for s in (11, 23)]
        self.assertNotEqual(programs[0], programs[1])

    def test_structure_motions_and_evidence(self):
        layer = _layer(11)
        corners = [a for a in layer.assemblies if a.functions == CORNER_FUNCTIONS]
        self.assertEqual(len(corners), 4)
        self.assertEqual(layer.root_children[0], "m0-load_structure")
        self.assertEqual(set(layer.root_children[1:]), {a.id for a in corners})
        self.assertEqual(len(layer.motions), 4)
        for motion in layer.motions:
            self.assertEqual(motion["type"], "revolute")
            self.assertEqual(motion["range_rad"], 2 * math.pi)
            self.assertAlmostEqual(float(np.linalg.norm(motion["axis_dir"])), 1.0, places=12)
        evidence = layer.evidence
        self.assertEqual(evidence["load_structure"], {"members": [DECK_ID]})
        self.assertEqual(evidence["ground_propulsion"]["motions"], [m["id"] for m in layer.motions])
        self.assertEqual(evidence["braking"], {"rotor_motion": corner_ids(1)["motion"],
                                               "stator": corner_ids(1)["stator"]})
        kinds = {i["id"]: i["kind"] for i in layer.interfaces}
        self.assertEqual(kinds[corner_ids(1)["wheel"] + ".bearing"], "bearing")
        self.assertEqual(kinds[corner_ids(1)["axle"] + ".seat"], "bonded")

    def test_only_wheels_reach_the_ground_band_and_support_is_symmetric(self):
        layer = _layer(23)
        verts = {p.id: prism_vertices(p.program) for p in layer.parts}
        lowest = min(float(v[:, 2].min()) for v in verts.values())
        owners = {pid for pid, v in verts.items() if (v[:, 2] <= lowest + 1e-3).any()}
        self.assertEqual(owners, {corner_ids(k)["wheel"] for k in range(1, 5)})
        band = np.concatenate([v[v[:, 2] <= lowest + 1e-3] for v in verts.values()])
        b = layer.backbone
        self.assertLess(band[:, 1].min(), b.y0)
        self.assertGreater(band[:, 1].max(), b.y1)
        self.assertLess(band[:, 0].min(), b.core_x0)
        self.assertGreater(band[:, 0].max(), b.core_x1)

    def test_bore_clears_the_axle_in_every_rotation(self):
        g = draw_corner_geometry(11, plan_mechanisms(11, BOUNDS, CATALOGUE))
        c = DEFAULT_GROUND_CONTACT_CONFIG.bearing_clearance_m
        axle = np.asarray(axle_profile(g))
        bore = np.asarray(bore_profile(g, c, DEFAULT_GROUND_CONTACT_CONFIG.bore_sides))
        circum = float(np.linalg.norm(axle, axis=1).max())
        # Every bore edge stays at least r_a + c from the axis.
        for a, e in zip(bore, np.roll(bore, -1, axis=0) - bore):
            self.assertGreaterEqual(abs(a[0] * e[1] - a[1] * e[0]) / np.linalg.norm(e), circum + c * (1 - 1e-9))
        # A bore vertex faces each axle vertex closely, so the contact is sampled.
        gaps = np.linalg.norm(axle[:, None, :] - bore[None, :, :], axis=2).min(axis=1)
        self.assertLessEqual(float(gaps.max()), DEFAULT_GROUND_CONTACT_CONFIG.max_bearing_vertex_gap_m)
        with self.assertRaises(ValueError):
            bore_profile(g, c, 50)

    def test_y_prism_maps_world_profile_on_both_sides(self):
        square = [[-0.1, -0.2], [0.1, -0.2], [0.1, 0.3], [-0.1, 0.3]]
        for side in (1, -1):
            verts = prism_vertices(y_prism("m9-x.part", "test", square, 0.5, 1.0, 2.0, 3.0, side))
            self.assertAlmostEqual(float(verts[:, 0].min()), 0.9, places=12)
            self.assertAlmostEqual(float(verts[:, 2].min()), 1.8, places=12)
            self.assertAlmostEqual(float(verts[:, 2].max()), 2.3, places=12)
            span = sorted([3.0, 3.0 + side * 0.5])
            self.assertAlmostEqual(float(verts[:, 1].min()), span[0], places=12)
            self.assertAlmostEqual(float(verts[:, 1].max()), span[1], places=12)

    def test_problems_detect_broken_corners(self):
        layer = _layer(11)
        stator = corner_ids(1)["stator"]
        moved = [dataclasses.replace(p, program=y_prism(stator, "stator", [[-0.01, 0.0], [0.01, 0.0], [0.0, 0.01]],
                                                        0.01, 0.0, 0.0, 9.0, 1))
                 if p.id == stator else p for p in layer.parts]
        problems = ground_contact_problems(dataclasses.replace(layer, parts=tuple(moved)))
        self.assertTrue(any("stator" in p for p in problems), problems)
        no_motion = dataclasses.replace(layer, motions=layer.motions[1:])
        self.assertTrue(any("motion" in p for p in ground_contact_problems(no_motion)))


CAD_CHECK = r"""
import json, sys
from pathlib import Path
root, spec, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path[:0] = [str(root / "src"), str(root), str(root / "scripts" / "hierarchy")]
from functional_realization import realize_program
programs = json.loads(spec.read_text(encoding="utf-8"))
print(json.dumps({k: realize_program(v, out / (k + ".stl"), 1000.0) for k, v in programs.items()}))
"""


@unittest.skipUnless(CAD_PYTHON.is_file(), "pinned CadQuery runtime is absent")
class CornerRealizationTests(unittest.TestCase):
    def test_wheel_and_axle_meshes_are_closed_and_keep_the_bearing_gap(self):
        layer = _layer(11)
        ids = corner_ids(2)
        programs = {role: {p.id: p.program for p in layer.parts}[ids[role]] for role in ("axle", "wheel")}
        with tempfile.TemporaryDirectory() as tmp:
            spec = Path(tmp) / "corner.json"
            spec.write_text(json.dumps(programs), encoding="utf-8")
            done = subprocess.run([str(CAD_PYTHON), "-c", CAD_CHECK, str(ROOT), str(spec), tmp], cwd=ROOT,
                                  capture_output=True, text=True, timeout=600)
            self.assertEqual(done.returncode, 0, done.stderr)
            meshes = {role: read_binary_stl(Path(tmp) / f"{role}.stl") for role in programs}
        motion = {m["id"]: m for m in layer.motions}[ids["motion"]]
        point = np.asarray(motion["axis_point_m"])
        for role, tris in meshes.items():
            self.assertEqual(closure_problems(tris), [], role)
            self.assertGreater(volume_and_centroid(tris)[0], 0.0)
        # Radial distances in the x-z plane from the axle axis.
        axle_r = np.linalg.norm((meshes["axle"].reshape(-1, 3) - point)[:, [0, 2]], axis=1).max()
        wheel_r = np.linalg.norm((meshes["wheel"].reshape(-1, 3) - point)[:, [0, 2]], axis=1)
        self.assertGreater(float(wheel_r.min()), float(axle_r))
        self.assertLess(float(wheel_r.min()) - float(axle_r), 1e-4)


if __name__ == "__main__":
    unittest.main()
