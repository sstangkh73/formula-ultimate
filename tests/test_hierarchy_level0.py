"""Tests for the goal v2 Level-0 race coupling (Work 159)."""

from __future__ import annotations

import json
import math
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.hierarchy.level0 import (  # noqa: E402
    OUTPUT_FIELDS,
    RACE_KERNEL_ID,
    Level0InputError,
    drag_area_m2,
    evaluate_manifest,
    frontal_extent_m,
    load_config,
    result_bytes,
)

CONFIG_PATH = ROOT / "config" / "hierarchy" / "level0_race_v1.json"
SCRIPT = ROOT / "scripts" / "hierarchy" / "evaluate_level0.py"


def _box_triangles(lo, hi) -> np.ndarray:
    (x0, y0, z0), (x1, y1, z1) = lo, hi
    v = np.array([[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],
                  [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]], dtype=float)
    faces = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4),
             (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
    return v[np.array(faces)]


def _write_stl(path: Path, tris: np.ndarray) -> None:
    out = bytearray(b"\0" * 80) + struct.pack("<I", len(tris))
    for tri in tris:
        out += struct.pack("<3f", 0.0, 0.0, 0.0)
        out += struct.pack("<9f", *tri.reshape(-1).tolist())
        out += struct.pack("<H", 0)
    path.write_bytes(bytes(out))


def _package(directory: Path, root_mass: float) -> Path:
    (directory / "meshes").mkdir(parents=True)
    _write_stl(directory / "meshes" / "a.stl", _box_triangles((0.0, 0.0, 0.0), (2.0, 0.5, 0.4)))
    _write_stl(directory / "meshes" / "b.stl", _box_triangles((1.0, 0.5, 0.0), (3.0, 1.0, 0.6)))
    manifest = {
        "root": "car",
        "nodes": [
            {"id": "car", "kind": "assembly", "children": ["a", "b"], "mass_kg": root_mass},
            {"id": "a", "kind": "part", "mesh": "meshes/a.stl", "mass_kg": root_mass / 2},
            {"id": "b", "kind": "part", "mesh": "meshes/b.stl", "mass_kg": root_mass / 2},
        ],
    }
    path = directory / "manifest.json"
    path.write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")
    return path


class Level0Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = load_config(CONFIG_PATH)
        self._tmp = tempfile.TemporaryDirectory(prefix="fu_level0_unit_")
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_frontal_extent_and_drag_area_are_bounded(self) -> None:
        pts = np.array([[0.0, -0.3, 0.0], [4.0, 0.7, 0.5]])
        self.assertEqual(frontal_extent_m(pts), (1.0, 0.5))
        area = drag_area_m2(pts, self.config)
        self.assertGreater(area, 0.0)
        self.assertLessEqual(area, 1.5 * 1.0 * 0.5)

    def test_bad_drag_coefficient_is_rejected(self) -> None:
        bad = json.loads(json.dumps(self.config))
        bad["drag"]["frontal_box_coefficient"] = 2.0
        with self.assertRaises(Level0InputError):
            drag_area_m2(np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]), bad)

    def test_evaluation_fields_mass_and_finish(self) -> None:
        manifest = _package(self.tmp / "pkg", 400.0)
        result = evaluate_manifest(manifest, self.config, ROOT)
        self.assertEqual(set(result), set(OUTPUT_FIELDS))
        self.assertEqual(result["race_kernel"], RACE_KERNEL_ID)
        self.assertEqual(result["mass_kg"], 400.0)
        self.assertAlmostEqual(result["drag_area_m2"], 1.0 * 1.0 * 0.6)
        self.assertEqual(result["outcome"], "finished")
        self.assertTrue(math.isfinite(result["race_time_s"]) and result["race_time_s"] > 0.0)
        self.assertLessEqual(abs(result["terminal_energy_boundary_residual_j"]), 1.0)

    def test_heavier_vehicle_is_slower(self) -> None:
        light = evaluate_manifest(_package(self.tmp / "light", 400.0), self.config, ROOT)
        heavy = evaluate_manifest(_package(self.tmp / "heavy", 600.0), self.config, ROOT)
        self.assertTrue(heavy["outcome"] != "finished" or heavy["race_time_s"] > light["race_time_s"])

    def test_non_positive_root_mass_is_rejected(self) -> None:
        with self.assertRaises(Level0InputError):
            evaluate_manifest(_package(self.tmp / "zero", 0.0), self.config, ROOT)

    def test_mesh_path_escape_is_rejected(self) -> None:
        manifest = _package(self.tmp / "esc", 400.0)
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["nodes"][1]["mesh"] = "../outside.stl"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(Level0InputError):
            evaluate_manifest(manifest, self.config, ROOT)

    def test_cli_output_is_byte_identical(self) -> None:
        manifest = _package(self.tmp / "cli", 400.0)
        outputs = []
        for name in ("a.json", "b.json"):
            out = self.tmp / name
            done = subprocess.run([sys.executable, str(SCRIPT), "--manifest", str(manifest), "--out", str(out)],
                                  cwd=ROOT, capture_output=True, text=True, timeout=300)
            self.assertEqual(done.returncode, 0, done.stderr)
            outputs.append(out.read_bytes())
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[0], result_bytes(json.loads(outputs[0])))


if __name__ == "__main__":
    unittest.main()
