"""Tests for the goal v2 hex-socket fasteners and threaded joints (Work 158)."""

from __future__ import annotations

import json
import math
import random
import subprocess
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

import numpy as np

from formula_ultimate.hierarchy.composition import (
    DEFAULT_MATERIAL_CATALOGUE,
    build_part_tree,
    load_leaf_materials,
    plan_vehicle,
)
from formula_ultimate.hierarchy.fasteners import (
    DEFAULT_FASTENER_CONFIG,
    SOCKETED_LEAF_GRAMMAR_VERSION,
    add_fasteners,
    fastener_config_record,
    fastener_problems,
    hexagon,
    pin_program,
    socket_axis,
    socket_base_program,
    socket_program,
    validate_v2_program,
)
from formula_ultimate.hierarchy.functional import V2_DECOMPOSITION_CONFIG, config_sha256_v2, with_threaded_axes
from formula_ultimate.hierarchy.leaf_geometry import (
    LEAF_GRAMMAR_VERSION,
    LeafProgramError,
    leaf_program,
    placement_transforms,
    transform_points,
    with_placement,
)
from formula_ultimate.hierarchy.leaf_refinement import refine_layout


ROOT = Path(__file__).resolve().parents[1]
CAD_PYTHON = ROOT / ".tools" / "cadquery-mcp" / "Scripts" / "python.exe"
CLEARANCE = DEFAULT_FASTENER_CONFIG.clearance_m


def _socketed(axis: str = "y", flip: bool = True) -> tuple[dict, dict]:
    placed = with_placement(leaf_program(random.Random(3), 0.2, leaf_id="t"),
                            placement_transforms(axis, flip, 0.4, [0.1, -0.2, 0.3]))
    rho = placed["contact"]["inscribed_radius_m"] - placed["tessellation"]["linear_tolerance_m"]
    return placed, socket_program(placed, 0.2 * rho, 0.3, (0.2 * rho, -0.1 * rho))


class SocketProgramTests(unittest.TestCase):
    def test_socket_round_trips_to_the_placed_program(self):
        placed, holed = _socketed()
        self.assertEqual(holed["leaf_grammar_version"], SOCKETED_LEAF_GRAMMAR_VERSION)
        self.assertEqual([loop["role"] for loop in holed["profile"]["loops"]], ["outer", "hole"])
        validate_v2_program(holed)
        self.assertEqual(socket_base_program(holed), placed)

    def test_hexagon_is_regular_with_the_declared_apothem(self):
        points = np.asarray(hexagon((0.1, -0.2), 0.03, 0.4))
        edges = np.roll(points, -1, axis=0) - points
        np.testing.assert_allclose(np.linalg.norm(edges, axis=1), 0.03 / math.cos(math.pi / 6) * np.ones(6))
        mids = 0.5 * (points + np.roll(points, -1, axis=0)) - np.array([0.1, -0.2])
        np.testing.assert_allclose(np.linalg.norm(mids, axis=1), 0.03 * np.ones(6))
        self.assertGreater(float(edges[0, 0] * edges[1, 1] - edges[0, 1] * edges[1, 0]), 0.0)  # counter-clockwise

    def test_socket_outside_the_inscribed_circle_or_tampered_is_rejected(self):
        placed, holed = _socketed()
        rho = placed["contact"]["inscribed_radius_m"]
        with self.assertRaises(LeafProgramError):
            socket_program(placed, 0.5 * rho, 0.0, (0.5 * rho, 0.0))
        tampered = json.loads(json.dumps(holed))
        tampered["socket"]["apothem_m"] *= 1.01
        with self.assertRaises(LeafProgramError):
            validate_v2_program(tampered)

    def test_pin_faces_sit_at_the_clearance_inside_the_socket(self):
        _placed, holed = _socketed()
        pin = pin_program(holed, CLEARANCE, "t.pin")
        validate_v2_program(pin)
        self.assertEqual(pin["leaf_grammar_version"], LEAF_GRAMMAR_VERSION)
        h = holed["contact"]["height_m"]
        self.assertAlmostEqual(pin["contact"]["height_m"], h - 2 * CLEARANCE)
        # Map the pin's local vertices into the holed leaf's local frame.
        pin_local = np.asarray(pin["profile"]["loops"][0]["segments"][0]["parameters"]["points_m"][:-1])
        prism = np.vstack([np.column_stack([pin_local, np.zeros(6)]),
                           np.column_stack([pin_local, np.full(6, pin["contact"]["height_m"])])])
        world = transform_points(pin, prism)
        socket = np.asarray(holed["profile"]["loops"][1]["segments"][0]["parameters"]["points_m"][:-1])
        expected = np.vstack([np.column_stack([socket, np.zeros(6)]), np.column_stack([socket, np.full(6, h)])])
        expected_world = transform_points(holed, expected)
        centre = np.asarray(holed["socket"]["center_m"])
        # Radial inset of each corner is clearance / cos(30 deg), axial inset is the clearance.
        for k in range(12):
            local_target = expected[k].copy()
            direction = local_target[:2] - centre
            local_target[:2] -= direction / np.linalg.norm(direction) * CLEARANCE / math.cos(math.pi / 6)
            local_target[2] += CLEARANCE if k < 6 else -CLEARANCE
            np.testing.assert_allclose(world[k], transform_points(holed, local_target[None, :])[0], atol=1e-12)
        self.assertEqual(expected_world.shape, (12, 3))

    def test_axis_is_the_socket_axis_at_mid_thickness(self):
        _placed, holed = _socketed("x", False)
        point, direction = socket_axis(holed)
        cx, cy = holed["socket"]["center_m"]
        h = holed["contact"]["height_m"]
        np.testing.assert_allclose(point, transform_points(holed, np.array([[cx, cy, h / 2]]))[0], atol=1e-15)
        self.assertAlmostEqual(float(np.linalg.norm(direction)), 1.0, delta=1e-12)
        np.testing.assert_allclose(np.abs(direction), [1.0, 0.0, 0.0], atol=1e-12)


class AddFastenersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = load_leaf_materials(ROOT / DEFAULT_MATERIAL_CATALOGUE)
        plan = plan_vehicle(5, cls.catalogue, V2_DECOMPOSITION_CONFIG)
        cls.plan = replace(plan, layout=refine_layout(plan.layout))
        cls.result = add_fasteners(cls.plan, cls.catalogue)

    def test_fasteners_are_deterministic_rule_clean_and_numerous(self):
        again = add_fasteners(self.plan, self.catalogue)
        self.assertEqual(again.axes, self.result.axes)
        self.assertEqual([leaf.program for leaf in again.plan.layout.leaves],
                         [leaf.program for leaf in self.result.plan.layout.leaves])
        self.assertEqual(fastener_problems(self.plan, self.result), [])
        self.assertGreaterEqual(len(self.result.axes), 8)

    def test_pins_join_the_holed_leaf_parent_and_the_part_tree_validates(self):
        nodes = self.result.plan.tree.node_map()
        for item in self.result.plan.layout.interfaces:
            if item.kind != "threaded":
                continue
            self.assertEqual(nodes[item.b].parent, nodes[item.a].parent)
            self.assertIn(item.b, nodes[nodes[item.a].parent].children)
        measurements = {leaf.id: {"mass_kg": 1.0, "center_of_mass_m": list(leaf.box_min_m)}
                        for leaf in self.result.plan.layout.leaves}
        tree = build_part_tree(self.result.plan, measurements)  # validates the tree
        self.assertEqual(sum(1 for i in tree.interfaces if i.kind == "threaded"), len(self.result.axes))

    def test_tampered_pin_is_reported(self):
        leaves = list(self.result.plan.layout.leaves)
        index = next(i for i, leaf in enumerate(leaves) if leaf.id.endswith(".pin"))
        tampered = json.loads(json.dumps(leaves[index].program))
        tampered["candidate"]["features"][2]["parameters"]["translation_m"][2] += 1e-3
        leaves[index] = replace(leaves[index], program=tampered)
        layout = replace(self.result.plan.layout, leaves=tuple(leaves))
        broken = replace(self.result, plan=replace(self.result.plan, layout=layout))
        self.assertTrue(any("pin does not match" in p for p in fastener_problems(self.plan, broken)))

    def test_threaded_axes_enter_the_manifest_exactly(self):
        manifest = {"interfaces": [{"id": "x", "a": "a", "b": "b", "kind": "welded"},
                                   {"id": "t", "a": "a", "b": "c", "kind": "threaded"}]}
        out = with_threaded_axes(manifest, {"t": ((1.0, 2.0, 3.0), (0.0, 0.0, 1.0))})
        self.assertEqual(out["interfaces"][1], {"id": "t", "a": "a", "b": "c", "kind": "threaded",
                                                "axis_point_m": [1.0, 2.0, 3.0], "axis_dir": [0.0, 0.0, 1.0]})
        self.assertEqual(out["interfaces"][0], manifest["interfaces"][0])
        with self.assertRaises(ValueError):
            with_threaded_axes(manifest, {})
        self.assertNotEqual(config_sha256_v2("0" * 64), config_sha256_v2("0" * 64, None, fastener_config_record()))


CAD_CHECK = r"""
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts" / "hierarchy"))
from functional_realization import realize_program
from formula_ultimate.hierarchy.leaf_geometry import closure_problems, read_binary_stl
import numpy as np
programs = json.loads(Path(sys.argv[2]).read_text())
out = {}
for name, program in programs.items():
    path = Path(sys.argv[3]) / f"{name}.stl"
    measured = realize_program(program, path, 1000.0)
    tris = read_binary_stl(path)
    verts, index = np.unique(tris.reshape(-1, 3), axis=0, return_inverse=True)
    faces = index.reshape(-1, 3)
    edges = np.unique(np.sort(np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]]), axis=1), axis=0)
    out[name] = {"mass": measured["mass_kg"], "closure": closure_problems(tris),
                 "euler": int(len(verts) - len(edges) + len(faces)), "tris": tris.tolist()}
print(json.dumps(out))
"""


def _line_hits(origin: np.ndarray, direction: np.ndarray, tris: np.ndarray, ray: bool = False) -> int:
    e1, e2 = tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]
    h = np.cross(direction, e2)
    det = np.einsum("ij,ij->i", e1, h)
    ok = np.abs(det) > 1e-18
    inv = np.divide(1.0, det, out=np.zeros_like(det), where=ok)
    s = origin - tris[:, 0]
    u = np.einsum("ij,ij->i", s, h) * inv
    q = np.cross(s, e1)
    v = (q @ direction) * inv
    hit = ok & (u >= 0) & (v >= 0) & (u + v <= 1)
    if ray:
        hit &= np.einsum("ij,ij->i", q, e2) * inv > 0
    return int(hit.sum())


def _point_plane_gaps(points: np.ndarray, tris: np.ndarray) -> np.ndarray:
    normals = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    normals /= np.linalg.norm(normals, axis=1, keepdims=True)
    return np.abs(np.einsum("nij,ij->ni", points[:, None, :] - tris[None, :, 0], normals))


@unittest.skipUnless(CAD_PYTHON.is_file(), "pinned CadQuery runtime is absent")
class FastenerRealizationTests(unittest.TestCase):
    def test_socketed_leaf_has_a_hole_the_pin_axis_crosses_and_the_pin_clears(self):
        plain, holed = _socketed("x", False)
        pin = pin_program(holed, CLEARANCE, "t.pin")
        programs = {"plain": plain, "holed": holed, "pin": pin}
        with tempfile.TemporaryDirectory() as tmp:
            spec = Path(tmp) / "programs.json"
            spec.write_text(json.dumps(programs), encoding="utf-8")
            done = subprocess.run([str(CAD_PYTHON), "-c", CAD_CHECK, str(ROOT), str(spec), tmp], cwd=ROOT,
                                  capture_output=True, text=True, timeout=600)
        self.assertEqual(done.returncode, 0, done.stderr)
        result = json.loads(done.stdout.strip().splitlines()[-1])
        for name in programs:
            self.assertEqual(result[name]["closure"], [], name)
        self.assertEqual(result["holed"]["euler"], 0)  # genus 1
        self.assertEqual(result["pin"]["euler"], 2)
        self.assertLess(result["holed"]["mass"], result["plain"]["mass"])
        h_tris, p_tris = np.asarray(result["holed"]["tris"]), np.asarray(result["pin"]["tris"])
        origin, axis = socket_axis(holed)
        self.assertEqual(_line_hits(origin, axis, h_tris), 0)
        self.assertGreaterEqual(_line_hits(origin, axis, p_tris), 2)
        helper = np.array([0.0, 1.0, 0.0]) if abs(axis[0]) > 0.9 else np.array([1.0, 0.0, 0.0])
        e1 = np.cross(axis, helper); e1 /= np.linalg.norm(e1)
        e2 = np.cross(axis, e1)
        for k in range(8):
            ray = math.cos(k * math.pi / 4 + 0.4027) * e1 + math.sin(k * math.pi / 4 + 0.4027) * e2
            self.assertGreater(_line_hits(origin, ray, h_tris, ray=True), 0)
        # Socket wall triangles: those whose plane passes near the axis region.
        wall = h_tris[np.abs(np.cross(h_tris[:, 1] - h_tris[:, 0], h_tris[:, 2] - h_tris[:, 0]) @ axis) < 1e-12]
        mids = wall.mean(axis=1)
        wall = wall[np.linalg.norm(np.cross(mids - origin, axis), axis=1)
                    < 2 * holed["socket"]["apothem_m"]]
        self.assertEqual(len(wall), 12)  # six flat faces, two triangles each
        gap = _point_plane_gaps(np.unique(p_tris.reshape(-1, 3), axis=0), wall).min()
        self.assertAlmostEqual(float(gap), CLEARANCE, delta=1e-6)


if __name__ == "__main__":
    unittest.main()
