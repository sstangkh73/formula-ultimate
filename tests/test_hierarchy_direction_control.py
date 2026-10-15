"""Tests for the v2 steering post and arm (Work 162)."""

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
from formula_ultimate.hierarchy.direction_control import (
    DEFAULT_DIRECTION_CONTROL_CONFIG,
    STEER_FUNCTIONS,
    _z_prism,
    add_direction_control,
    convex_hull,
    direction_control_problems,
    steer_ids,
    steering_bore,
)
from formula_ultimate.hierarchy.ground_contacts import add_ground_contacts, ground_contact_problems
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
STEER_INDEX = 5


def _layer(seed: int, bounds: ClusterBounds = BOUNDS):
    layer = add_ground_contacts(plan_mechanisms(seed, bounds, CATALOGUE), seed, CATALOGUE)
    return add_direction_control(layer, seed, CATALOGUE)


class SteeringPlanningTests(unittest.TestCase):
    def test_layers_pass_every_recheck_for_many_seeds(self):
        narrow = ClusterBounds(lo=(0.0, -0.1, 0.0), hi=(0.3, 0.1, 0.4), lowest_leaf="g1.p0",
                               lowest_point=(0.1, 0.0, 0.0))
        for bounds in (BOUNDS, narrow):
            for seed in range(30):
                layer = _layer(seed, bounds)
                self.assertEqual(mechanism_problems(layer, bounds, ["g1.p0"]), [], f"seed {seed}")
                self.assertEqual(ground_contact_problems(layer), [], f"seed {seed}")
                self.assertEqual(direction_control_problems(layer), [], f"seed {seed}")

    def test_deterministic_and_seed_driven(self):
        self.assertEqual(_layer(11), _layer(11))
        arm = steer_ids(STEER_INDEX)["arm"]
        programs = [{p.id: p.program for p in _layer(s).parts}[arm] for s in (11, 23)]
        self.assertNotEqual(programs[0], programs[1])

    def test_structure_motion_and_evidence(self):
        layer = _layer(11)
        ids = steer_ids(STEER_INDEX)
        assembly = {a.id: a for a in layer.assemblies}[ids["assembly"]]
        self.assertEqual(assembly.functions, STEER_FUNCTIONS)
        self.assertEqual(layer.root_children[-1], ids["assembly"])
        motion = {m["id"]: m for m in layer.motions}[ids["motion"]]
        self.assertEqual(motion["parts"], [ids["arm"]])
        self.assertEqual(motion["axis_dir"], [0.0, 0.0, 1.0])
        self.assertGreaterEqual(motion["range_rad"], 0.2)
        for other in layer.evidence["ground_propulsion"]["motions"]:
            drive = {m["id"]: m for m in layer.motions}[other]["axis_dir"]
            self.assertLessEqual(abs(float(np.dot(motion["axis_dir"], drive))), math.cos(math.radians(30)))
        self.assertEqual(layer.evidence["direction_control"], {"motion": ids["motion"]})
        kinds = {(i["a"], i["b"]): i["kind"] for i in layer.interfaces}
        self.assertEqual(kinds[(ids["boss"], DECK_ID)], "bonded")
        self.assertEqual(kinds[(ids["arm"], ids["post"])], "bearing")

    def test_bore_clears_the_post_and_samples_the_contact(self):
        c = DEFAULT_DIRECTION_CONTROL_CONFIG.bearing_clearance_m
        for post_sides in (6, 8):
            post = np.asarray([[0.02 * math.cos(2 * math.pi * k / post_sides),
                                0.02 * math.sin(2 * math.pi * k / post_sides)] for k in range(post_sides)])
            bore = np.asarray(steering_bore(post_sides, 0.02, c, 96))
            for a, e in zip(bore, np.roll(bore, -1, axis=0) - bore):
                self.assertGreaterEqual(abs(a[0] * e[1] - a[1] * e[0]) / np.linalg.norm(e), 0.02 + c * (1 - 1e-9))
            gaps = np.linalg.norm(post[:, None, :] - bore[None, :, :], axis=2).min(axis=1)
            self.assertLessEqual(float(gaps.max()), DEFAULT_DIRECTION_CONTROL_CONFIG.max_bearing_vertex_gap_m)
        with self.assertRaises(ValueError):
            steering_bore(8, 0.02, c, 100)

    def test_arm_sweep_stays_clear_of_the_other_mechanism_parts(self):
        layer = _layer(37)
        ids = steer_ids(STEER_INDEX)
        motion = {m["id"]: m for m in layer.motions}[ids["motion"]]
        verts = {p.id: prism_vertices(p.program) for p in layer.parts}
        centre = np.asarray(motion["axis_point_m"][:2])
        reach = float(np.linalg.norm(verts[ids["arm"]][:, :2] - centre, axis=1).max())
        arm_z = verts[ids["arm"]][:, 2]
        for pid, v in verts.items():
            if pid in ids.values() or pid == DECK_ID:
                continue
            level = v[(v[:, 2] >= arm_z.min()) & (v[:, 2] <= arm_z.max())]
            if len(level):
                self.assertGreater(float(np.linalg.norm(level[:, :2] - centre, axis=1).min()), reach, pid)
        self.assertGreater(float(arm_z.min()), float(verts[DECK_ID][:, 2].max()))

    def test_convex_hull_is_counter_clockwise(self):
        hull = convex_hull([[0, 0], [1, 0], [1, 1], [0, 1], [0.5, 0.5], [0.5, 0.0]])
        self.assertEqual(hull, [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])

    def test_problems_detect_broken_steering(self):
        layer = _layer(11)
        ids = steer_ids(STEER_INDEX)
        moved = [dataclasses.replace(p, program=_z_prism(ids["post"], "steer_post",
                                                          [[0.0, 0.0], [0.01, 0.0], [0.0, 0.01]],
                                                          0.05, 0.0, 0.0, 9.0))
                 if p.id == ids["post"] else p for p in layer.parts]
        problems = direction_control_problems(dataclasses.replace(layer, parts=tuple(moved)))
        self.assertTrue(any("post" in p for p in problems), problems)
        tilted = [dict(m, axis_dir=[0.0, 1.0, 0.0]) if m["id"] == ids["motion"] else m for m in layer.motions]
        problems = direction_control_problems(dataclasses.replace(layer, motions=tuple(tilted)))
        self.assertTrue(any("axis within" in p for p in problems), problems)


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
class SteeringRealizationTests(unittest.TestCase):
    def test_post_and_arm_meshes_are_closed_and_keep_the_bearing_gap(self):
        layer = _layer(11)
        ids = steer_ids(STEER_INDEX)
        programs = {role: {p.id: p.program for p in layer.parts}[ids[role]] for role in ("post", "arm")}
        with tempfile.TemporaryDirectory() as tmp:
            spec = Path(tmp) / "steer.json"
            spec.write_text(json.dumps(programs), encoding="utf-8")
            done = subprocess.run([str(CAD_PYTHON), "-c", CAD_CHECK, str(ROOT), str(spec), tmp], cwd=ROOT,
                                  capture_output=True, text=True, timeout=600)
            self.assertEqual(done.returncode, 0, done.stderr)
            meshes = {role: read_binary_stl(Path(tmp) / f"{role}.stl") for role in programs}
        motion = {m["id"]: m for m in layer.motions}[ids["motion"]]
        centre = np.asarray(motion["axis_point_m"][:2])
        for role, tris in meshes.items():
            self.assertEqual(closure_problems(tris), [], role)
            self.assertGreater(volume_and_centroid(tris)[0], 0.0)
        post_r = np.linalg.norm(meshes["post"].reshape(-1, 3)[:, :2] - centre, axis=1).max()
        arm_r = np.linalg.norm(meshes["arm"].reshape(-1, 3)[:, :2] - centre, axis=1)
        self.assertGreater(float(arm_r.min()), float(post_r))
        self.assertLess(float(arm_r.min()) - float(post_r), 1e-4)


if __name__ == "__main__":
    unittest.main()
