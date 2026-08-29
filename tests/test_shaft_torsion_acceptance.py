from __future__ import annotations

import math
import unittest

from formula_ultimate.structural import MeshData, StructuralEvidenceError, TorsionSpec, build_torsion_calculix_input


def specimen(**changes: object) -> TorsionSpec:
    values: dict[str, object] = dict(protocol_id="p", experiment_id="e", specimen_id="s", claim_level="local", length_m=10.0, radius_m=1.0, material_id="m", youngs_modulus_pa=100.0, poisson_ratio=0.3, density_kg_per_m3=1.0, material_provenance="fixture", torque_nm=10.0, gauge_x_min_m=2.0, gauge_x_max_m=8.0)
    values.update(changes)
    return TorsionSpec(**values)  # type: ignore[arg-type]


def mesh() -> MeshData:
    nodes = {1:(0.,0.,0.),2:(0.,2.,0.),3:(0.,0.,2.),4:(0.,2.,2.),5:(10.,0.,0.),6:(10.,2.,0.),7:(10.,0.,2.),8:(10.,2.,2.)}
    return MeshData(nodes=nodes, tetrahedra={1:(1,5,6,7),2:(1,6,7,8)}, triangles={1:(5,6,8),2:(5,8,7)})


class TorsionSpecTests(unittest.TestCase):
    def test_references_and_signed_shear(self) -> None:
        spec = specimen()
        self.assertAlmostEqual(100.0 / 2.6, spec.shear_modulus_pa)
        self.assertAlmostEqual(math.pi / 2.0, spec.polar_second_moment_m4)
        self.assertGreater(spec.analytical_twist_rad, 0.0)
        self.assertEqual((-10.0 / spec.polar_second_moment_m4, 0.0), spec.analytical_shear_pa(y_m=1.0, z_m=2.0))
        reverse = specimen(torque_nm=-10.0)
        self.assertAlmostEqual(-spec.analytical_twist_rad, reverse.analytical_twist_rad)
        self.assertAlmostEqual(spec.analytical_energy_j, reverse.analytical_energy_j)

    def test_invalid_contract_is_rejected(self) -> None:
        for change in ({"radius_m":0.0},{"torque_nm":0.0},{"poisson_ratio":0.5},{"gauge_x_min_m":0.0}):
            with self.subTest(change=change), self.assertRaises(StructuralEvidenceError):
                specimen(**change)


class PureTorqueDeckTests(unittest.TestCase):
    def test_consistent_surface_load_is_a_pure_torque(self) -> None:
        spec = specimen()
        deck, loads, weights, fixed, loaded = build_torsion_calculix_input(spec=spec, mesh=mesh(), boundary_tolerance_m=1e-12)
        total = tuple(math.fsum(force[i] for force in loads.values()) for i in range(3))
        torque = math.fsum((mesh().nodes[n][1]-1.0)*f[2]-(mesh().nodes[n][2]-1.0)*f[1] for n,f in loads.items())
        self.assertTrue(all(abs(value) < 1e-12 for value in total))
        self.assertAlmostEqual(10.0, torque)
        self.assertEqual(set(loaded), set(weights))
        self.assertEqual((1,2,3,4), fixed)
        self.assertIn("*CLOAD", deck)
        self.assertLessEqual(max(len(line) for line in deck.splitlines()), 132)

    def test_unrestrained_negative_control_omits_boundary(self) -> None:
        deck, *_ = build_torsion_calculix_input(spec=specimen(), mesh=mesh(), boundary_tolerance_m=1e-12, restrained=False)
        self.assertNotIn("*BOUNDARY", deck)


if __name__ == "__main__":
    unittest.main()
