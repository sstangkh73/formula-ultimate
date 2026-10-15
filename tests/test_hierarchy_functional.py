"""Tests for the goal v2 functional manifest helpers (Work 155)."""

from __future__ import annotations

import math
import unittest

import numpy as np

from formula_ultimate.hierarchy.functional import (
    DESIGN_LANGUAGE_VERSION_V2,
    build_functional_manifest,
    config_sha256_v2,
    mesh_inertia,
)


def box_mesh(size, center=(0.0, 0.0, 0.0), rotation=None) -> np.ndarray:
    """Closed outward-oriented 12-triangle box mesh."""

    hx, hy, hz = (s / 2 for s in size)
    v = np.array([[-hx, -hy, -hz], [hx, -hy, -hz], [hx, hy, -hz], [-hx, hy, -hz],
                  [-hx, -hy, hz], [hx, -hy, hz], [hx, hy, hz], [-hx, hy, hz]])
    faces = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4),
             (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
    if rotation is not None:
        v = v @ np.asarray(rotation).T
    v = v + np.asarray(center)
    return v[np.array(faces)]


def rot_z(angle: float) -> np.ndarray:
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def box_inertia(mass, size) -> np.ndarray:
    a, b, c = size
    return mass / 12.0 * np.diag([b * b + c * c, a * a + c * c, a * a + b * b])


class MeshInertiaTests(unittest.TestCase):
    def test_offset_box_matches_closed_form(self):
        size, density = (0.4, 0.2, 0.1), 2500.0
        mass, com, inertia = mesh_inertia([(box_mesh(size, center=(1.0, -2.0, 0.5)), density)])
        expected_mass = density * 0.4 * 0.2 * 0.1
        self.assertAlmostEqual(mass, expected_mass, places=10)
        np.testing.assert_allclose(com, [1.0, -2.0, 0.5], atol=1e-12)
        np.testing.assert_allclose(inertia, box_inertia(expected_mass, size), rtol=0, atol=1e-12)

    def test_rotated_box_transforms_as_a_tensor(self):
        size, density, angle = (0.4, 0.2, 0.1), 1000.0, 0.3
        r = rot_z(angle)
        mass, _com, inertia = mesh_inertia([(box_mesh(size, center=(0.2, 0.1, 0.0), rotation=r), density)])
        expected = r @ box_inertia(mass, size) @ r.T
        np.testing.assert_allclose(inertia, expected, rtol=0, atol=1e-12)
        self.assertNotAlmostEqual(inertia[0, 1], 0.0, places=6)

    def test_two_bodies_use_the_parallel_axis_theorem(self):
        size = (0.1, 0.1, 0.1)
        mass, com, inertia = mesh_inertia([(box_mesh(size, center=(-0.5, 0.0, 0.0)), 1000.0),
                                           (box_mesh(size, center=(0.5, 0.0, 0.0)), 3000.0)])
        m1, m2 = 1.0, 3.0
        self.assertAlmostEqual(mass, m1 + m2, places=10)
        np.testing.assert_allclose(com, [0.25, 0.0, 0.0], atol=1e-12)
        own = box_inertia(m1, size) + box_inertia(m2, size)
        shift = m1 * 0.75 ** 2 + m2 * 0.25 ** 2
        np.testing.assert_allclose(inertia, own + np.diag([0.0, shift, shift]), rtol=0, atol=1e-12)

    def test_empty_or_inverted_mesh_is_rejected(self):
        inverted = box_mesh((0.1, 0.1, 0.1))[:, ::-1]
        with self.assertRaises(ValueError):
            mesh_inertia([(inverted, 1000.0)])


class FunctionalManifestTests(unittest.TestCase):
    V1 = {"design_language_version": "hier-composition-v1", "seed": 3, "config_sha256": "0" * 64,
          "git_commit": "abc", "length_unit": "m", "mass_unit": "kg", "contact_tolerance_m": 1e-4,
          "root": "vehicle", "nodes": [], "interfaces": []}

    def test_adds_exactly_the_v2_fields(self):
        config = config_sha256_v2(self.V1["config_sha256"])
        manifest = build_functional_manifest(self.V1, [], {}, np.eye(3), config)
        self.assertEqual(set(manifest) - set(self.V1),
                         {"up_axis", "motions", "function_evidence", "vehicle_inertia_kg_m2"})
        self.assertEqual(manifest["up_axis"], "z")
        self.assertEqual(manifest["design_language_version"], DESIGN_LANGUAGE_VERSION_V2)
        self.assertRegex(manifest["config_sha256"], r"^[0-9a-f]{64}$")
        self.assertNotEqual(manifest["config_sha256"], self.V1["config_sha256"])
        self.assertEqual(manifest["vehicle_inertia_kg_m2"], [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        self.assertEqual(self.V1["design_language_version"], "hier-composition-v1")

    def test_rejects_bad_inertia(self):
        with self.assertRaises(ValueError):
            build_functional_manifest(self.V1, [], {}, np.eye(2), "0" * 64)
        with self.assertRaises(ValueError):
            build_functional_manifest(self.V1, [], {}, np.full((3, 3), np.nan), "0" * 64)


if __name__ == "__main__":
    unittest.main()
