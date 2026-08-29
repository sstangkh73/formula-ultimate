from __future__ import annotations

import math
import unittest

from formula_ultimate.structural import (
    MeshData,
    ResponsePoint,
    StructuralEvidenceError,
    cantilever_first_mode,
    imperfect_mesh,
    response_is_strictly_monotonic,
    secant_amplification,
    shaped_imperfect_mesh,
    smooth_cubic_crookedness,
)


class NonlinearImperfectColumnTests(unittest.TestCase):
    def test_cantilever_mode_boundary_and_normalization(self) -> None:
        self.assertEqual(0.0, cantilever_first_mode(0.0, 0.2))
        self.assertAlmostEqual(1.0, cantilever_first_mode(0.2, 0.2))
        self.assertAlmostEqual(1.0 - math.sqrt(0.5), cantilever_first_mode(0.1, 0.2))

    def test_imperfection_preserves_connectivity_and_fixed_face(self) -> None:
        mesh = MeshData(
            nodes={
                1: (0.0, 0.0, 0.0),
                2: (0.2, 0.0, 0.0),
                3: (0.2, 0.01, 0.0),
                4: (0.2, 0.0, 0.01),
            },
            tetrahedra={1: (1, 2, 3, 4)},
            triangles={2: (2, 3, 4)},
        )
        changed = imperfect_mesh(mesh, length_m=0.2, tip_amplitude_m=0.001)
        self.assertEqual((0.0, 0.0, 0.0), changed.nodes[1])
        self.assertAlmostEqual(0.001, changed.nodes[2][2])
        self.assertIs(mesh.tetrahedra, changed.tetrahedra)

    def test_secant_relation_and_domain_fail_closed(self) -> None:
        self.assertEqual(1.0, secant_amplification(0.0, 100.0))
        self.assertEqual(2.0, secant_amplification(50.0, 100.0))
        self.assertAlmostEqual(10.0, secant_amplification(90.0, 100.0))
        for load in (-1.0, 100.0, 101.0):
            with self.assertRaises(StructuralEvidenceError):
                secant_amplification(load, 100.0)

    def test_independent_cubic_shape_and_unknown_shape_rejection(self) -> None:
        self.assertEqual(0.0, smooth_cubic_crookedness(0.0, 0.2))
        self.assertEqual(0.5, smooth_cubic_crookedness(0.1, 0.2))
        self.assertEqual(1.0, smooth_cubic_crookedness(0.2, 0.2))
        mesh = MeshData(
            nodes={1: (0.0, 0.0, 0.0), 2: (0.2, 0.0, 0.0), 3: (0.2, 0.01, 0.0), 4: (0.2, 0.0, 0.01)},
            tetrahedra={1: (1, 2, 3, 4)},
            triangles={2: (2, 3, 4)},
        )
        with self.assertRaises(StructuralEvidenceError):
            shaped_imperfect_mesh(mesh, length_m=0.2, tip_amplitude_m=0.001, shape_id="undeclared")

    def test_monotonicity_rejects_flat_or_reversed_response(self) -> None:
        good = [ResponsePoint(0.25, 1.3, 1.3, 1.333), ResponsePoint(0.5, 2.0, 2.0, 2.0)]
        flat = [ResponsePoint(0.25, 1.3, 1.3, 1.333), ResponsePoint(0.5, 1.3, 1.3, 2.0)]
        self.assertTrue(response_is_strictly_monotonic(good))
        self.assertFalse(response_is_strictly_monotonic(flat))


if __name__ == "__main__":
    unittest.main()
