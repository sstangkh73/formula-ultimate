from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

import numpy as np

from formula_ultimate.structural.geometry_mesh_bridge import build_mesh
from formula_ultimate.structural.vector_solid_fields import (
    VectorSolidViolation,
    elasticity_matrix,
    element_kinematics,
    patch_strain,
    solve,
    validate_protocol,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "development" / "vector_solid_fields_v1.json"


def one_cell_mesh():
    spec = {"minimum": (0.0, 0.0, 0.0), "maximum": (0.01, 0.01, 0.01), "resolution": 0.01, "dimensions": (1, 1, 1)}
    mesh = build_mesh({(0, 0, 0): "fixture"}, spec, maximum_elements=100)
    nodes = np.asarray(mesh["nodes"])
    for triangle in mesh["triangles"]:
        xs = nodes[np.asarray(triangle["nodes"]) - 1, 0]
        if np.allclose(xs, 0.0):
            triangle["set"] = "load_surface"
        elif np.allclose(xs, 0.01):
            triangle["set"] = "contact_surface"
        else:
            triangle["set"] = "external_surface"
    return mesh


class VectorSolidFieldTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.mesh = one_cell_mesh()
        self.material = self.raw["material"]
        self.load = {**self.raw["load"], "resultant_force_n": [-100.0, 20.0, -10.0], "body_acceleration_m_s2": [0.0, 0.0, 0.0]}

    def test_protocol_pins_work110_and_registered_experiment(self):
        result = validate_protocol(self.raw)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(len(result["protocol_sha256"]), 64)
        invalid = copy.deepcopy(self.raw)
        invalid["units"] = "mm_N_MPa"
        with self.assertRaisesRegex(VectorSolidViolation, "units"):
            validate_protocol(invalid)

    def test_isotropic_elasticity_is_symmetric_positive_definite(self):
        matrix = elasticity_matrix(70e9, 0.3)
        np.testing.assert_allclose(matrix, matrix.T)
        self.assertTrue(np.all(np.linalg.eigvalsh(matrix) > 0.0))
        with self.assertRaisesRegex(VectorSolidViolation, "corrupted stiffness"):
            elasticity_matrix(0.0, 0.3)

    def test_tet_patch_and_rigid_modes_have_zero_error(self):
        gradient = np.array([[1e-5, 2e-6, 3e-6], [-4e-6, 5e-6, 6e-6], [7e-6, -8e-6, 9e-6]])
        self.assertLess(patch_strain(self.mesh, gradient), 1e-12)
        rotation = np.array([[0.0, -2e-5, 3e-5], [2e-5, 0.0, -4e-5], [-3e-5, 4e-5, 0.0]])
        self.assertLess(patch_strain(self.mesh, rotation), 1e-12)
        points = np.asarray(self.mesh["nodes"])[np.asarray(self.mesh["tetrahedra"][0]["nodes"]) - 1]
        _, b = element_kinematics(points)
        self.assertLess(np.max(np.abs(b @ np.tile([0.4, -0.2, 0.1], 4))), 1e-12)

    def test_solve_recovers_balance_and_inverse_stiffness_scaling(self):
        result = solve(self.mesh, self.material, self.load)
        self.assertLess(result["force_residual_relative"], 1e-10)
        self.assertLess(result["moment_residual_relative"], 1e-10)
        self.assertLess(result["energy_residual_relative"], 1e-12)
        self.assertEqual(result["node_count"], 8)
        stiff = solve(self.mesh, {**self.material, "youngs_modulus_pa": 2 * self.material["youngs_modulus_pa"]}, self.load)
        self.assertAlmostEqual(stiff["compliance_m_per_n"] / result["compliance_m_per_n"], 0.5, places=12)
        self.assertNotEqual(result["displacement_sha256"], solve(self.mesh, self.material, {**self.load, "resultant_force_n": [-20.0, -100.0, -10.0]})["displacement_sha256"])

    def test_body_force_is_observable_and_negative_cases_fail_closed(self):
        baseline = solve(self.mesh, self.material, self.load)
        gravity = solve(self.mesh, self.material, {**self.load, "body_acceleration_m_s2": [0.0, 0.0, -9.81]})
        self.assertNotEqual(baseline["applied_force_n"], gravity["applied_force_n"])
        unsupported = copy.deepcopy(self.mesh)
        for triangle in unsupported["triangles"]:
            if triangle["set"] == "contact_surface":
                triangle["set"] = "external_surface"
        with self.assertRaisesRegex(VectorSolidViolation, "unsupported rigid modes"):
            solve(unsupported, self.material, self.load)
        with self.assertRaisesRegex(VectorSolidViolation, "corrupted stiffness"):
            solve(self.mesh, {**self.material, "youngs_modulus_pa": 0.0}, self.load)


if __name__ == "__main__":
    unittest.main()
