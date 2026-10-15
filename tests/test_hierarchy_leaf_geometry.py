"""Tests for hierarchy leaf programs, STL round trips and CadQuery realization (Work 151)."""

from __future__ import annotations

import json
import math
import random
import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np

from formula_ultimate.hierarchy.leaf_geometry import (
    LeafProgramError,
    MeshError,
    closure_problems,
    leaf_program,
    measure_mesh,
    placement_transforms,
    program_sha256,
    read_binary_stl,
    stl_bytes,
    transform_points,
    validate_leaf_program,
    with_placement,
)
from formula_ultimate.hierarchy.part_tree import canonical_sha256

ROOT = Path(__file__).resolve().parents[1]
CAD_PYTHON = ROOT / ".tools" / "cadquery-mcp" / "Scripts" / "python.exe"


def _cube(size: float = 1.0) -> np.ndarray:
    v = np.array([[x, y, z] for x in (0, size) for y in (0, size) for z in (0, size)], dtype=float)
    quads = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    tris = []
    for a, b, c, d in quads:
        tris += [(a, b, c), (a, c, d)]
    return v[np.array(tris)]


class ProgramTests(unittest.TestCase):
    def test_program_is_deterministic_and_hashable(self):
        a = leaf_program(random.Random(5), 0.3, leaf_id="x.p0")
        b = leaf_program(random.Random(5), 0.3, leaf_id="x.p0")
        self.assertEqual(a, b)
        self.assertEqual(program_sha256(a), canonical_sha256(a))
        self.assertNotEqual(program_sha256(a), program_sha256(leaf_program(random.Random(6), 0.3, leaf_id="x.p0")))

    def test_programs_cover_both_profile_kinds_and_scale_with_length(self):
        kinds = set()
        for seed in range(40):
            for length in (0.004, 4.0):
                program = leaf_program(random.Random(seed), length)
                validate_leaf_program(program)
                kinds.add(program["profile"]["loops"][0]["segments"][0]["operator"])
                contact = program["contact"]
                self.assertLess(contact["outer_radius_m"], length)
                self.assertLess(contact["height_m"], length)
                self.assertGreater(contact["inscribed_radius_m"], 0.05 * length)
        self.assertEqual(kinds, {"polyline", "bspline"})

    def test_validation_rejects_tampering(self):
        program = leaf_program(random.Random(1), 0.1)
        bad = json.loads(json.dumps(program))
        bad["candidate"]["features"][1]["parameters"]["taper_rad"] = 0.1
        with self.assertRaises(LeafProgramError):
            validate_leaf_program(bad)
        bad = json.loads(json.dumps(program))
        bad["extra"] = 1
        with self.assertRaises(LeafProgramError):
            validate_leaf_program(bad)
        with self.assertRaises(LeafProgramError):
            leaf_program(random.Random(1), 0.0)
        with self.assertRaises(LeafProgramError):
            placement_transforms("w", False, 0.0, [0, 0, 0])

    def test_placement_maps_local_z_to_the_declared_axis(self):
        program = leaf_program(random.Random(2), 0.2)
        for axis, index in (("x", 0), ("y", 1), ("z", 2)):
            for flip in (False, True):
                placed = with_placement(program, placement_transforms(axis, flip, 0.7, [1.0, 2.0, 3.0]))
                origin, tip = transform_points(placed, np.array([[0, 0, 0], [0, 0, 1.0]]))
                np.testing.assert_allclose(origin, [1.0, 2.0, 3.0], atol=1e-12)
                direction = np.zeros(3)
                direction[index] = -1.0 if flip else 1.0
                np.testing.assert_allclose(tip - origin, direction, atol=1e-12)


class MeshTests(unittest.TestCase):
    def test_cube_round_trip_measures_volume_and_centroid(self):
        tris = _cube(0.5) + np.array([1.0, -2.0, 0.25])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "c.stl"
            path.write_bytes(stl_bytes(tris))
            back = read_binary_stl(path)
            self.assertEqual(path.read_bytes(), stl_bytes(back))
        m = measure_mesh(back, 2000.0)
        self.assertAlmostEqual(m["volume_m3"], 0.125, places=12)
        self.assertAlmostEqual(m["mass_kg"], 250.0, places=9)
        np.testing.assert_allclose(m["center_of_mass_m"], [1.25, -1.75, 0.5], atol=1e-12)
        self.assertAlmostEqual(m["box_fill_fraction"], 1.0, places=12)

    def test_open_inverted_and_degenerate_meshes_are_rejected(self):
        cube = _cube()
        self.assertTrue(closure_problems(cube[:-1]))
        with self.assertRaises(MeshError):
            measure_mesh(cube[:, ::-1, :], 1000.0)
        degenerate = cube.copy()
        degenerate[0, 1] = degenerate[0, 0]
        self.assertTrue(closure_problems(degenerate))


CAD_CHECK = r"""
import json, math, random, sys, tempfile
from pathlib import Path
import numpy as np
sys.path.insert(0, sys.argv[1] + "/src"); sys.path.insert(0, sys.argv[1])
from formula_ultimate.hierarchy.leaf_geometry import (
    leaf_program, placement_transforms, read_binary_stl, transform_points, with_placement)
from scripts.hierarchy.leaf_realization import realize_leaf, build_shape, tessellate_m
out = Path(tempfile.mkdtemp())
rows = []
for i, length in enumerate((0.004, 0.03, 0.4, 4.0) * 3):
    rng = random.Random(100 + i)
    local = leaf_program(rng, length, leaf_id=f"t{i}")
    local_tris = tessellate_m(build_shape(local), local)
    pts = local_tris.reshape(-1, 3)
    h = local["contact"]["height_m"]
    caps = pts[(np.abs(pts[:, 2]) < 1e-9 * max(1, h)) | (np.abs(pts[:, 2] - h) < 1e-9 * max(1, h))]
    radii = np.hypot(caps[:, 0], caps[:, 1])
    placed = with_placement(local, placement_transforms("xyz"[i % 3], i % 2 == 1, 0.3 * i, [0.5 * i, -0.2, 1.0]))
    m1 = realize_leaf(placed, out / f"a{i}.stl", 1500.0)
    realize_leaf(placed, out / f"b{i}.stl", 1500.0)
    expected = transform_points(placed, pts)
    got = read_binary_stl(out / f"a{i}.stl").reshape(-1, 3)
    rows.append({
        "length": length, "mass": m1["mass_kg"], "volume": m1["volume_m3"],
        "fill": m1["box_fill_fraction"], "diag": m1["bbox_diagonal_m"],
        "identical": (out / f"a{i}.stl").read_bytes() == (out / f"b{i}.stl").read_bytes(),
        "cap_count": int(len(caps)),
        "cap_r_min": float(radii.min()), "cap_r_max": float(radii.max()),
        "inscribed": local["contact"]["inscribed_radius_m"], "outer": local["contact"]["outer_radius_m"],
        "bbox_err": float(max(np.abs(expected.min(0) - got.min(0)).max(), np.abs(expected.max(0) - got.max(0)).max())),
    })
print(json.dumps(rows))
"""


@unittest.skipUnless(CAD_PYTHON.is_file(), "pinned CadQuery runtime is absent")
class CadRealizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        done = subprocess.run([str(CAD_PYTHON), "-c", CAD_CHECK, str(ROOT)], cwd=ROOT,
                              capture_output=True, text=True, timeout=600)
        if done.returncode != 0:
            raise AssertionError(done.stdout + done.stderr)
        cls.rows = json.loads(done.stdout.strip().splitlines()[-1])

    def test_exports_are_closed_measured_and_replayable(self):
        for row in self.rows:
            self.assertGreater(row["volume"], 0.0)
            self.assertAlmostEqual(row["mass"], row["volume"] * 1500.0, delta=1e-12 * row["mass"])
            self.assertTrue(row["identical"], row)
            self.assertLess(row["fill"], 0.999)
            self.assertTrue(0.3 * row["length"] < row["diag"] < 2.0 * row["length"], row)

    def test_flat_contact_faces_honour_declared_radii(self):
        for row in self.rows:
            self.assertGreater(row["cap_count"], 0)
            self.assertGreaterEqual(row["cap_r_min"], row["inscribed"] * (1 - 1e-9), row)
            self.assertLessEqual(row["cap_r_max"], row["outer"] * (1 + 1e-9), row)

    def test_pure_placement_matches_the_cad_placement(self):
        for row in self.rows:
            # The placed shape is tessellated afresh, so the bounding boxes agree
            # within the declared linear tolerance plus float32 STL rounding.
            self.assertLess(row["bbox_err"], 2e-3 * row["length"] + 1e-6, row)


if __name__ == "__main__":
    unittest.main()
