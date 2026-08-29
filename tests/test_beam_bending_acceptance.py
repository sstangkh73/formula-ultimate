from __future__ import annotations

import math
import unittest

from formula_ultimate.structural import (
    BendingSpec,
    MeshData,
    StructuralEvidenceError,
    build_bending_calculix_input,
)


def specimen(**overrides: object) -> BendingSpec:
    values: dict[str, object] = {
        "protocol_id": "protocol",
        "experiment_id": "experiment",
        "specimen_id": "beam",
        "claim_level": "solver route only",
        "length_m": 10.0,
        "width_m": 1.0,
        "height_m": 1.0,
        "material_id": "synthetic",
        "youngs_modulus_pa": 100.0,
        "poisson_ratio": 0.3,
        "density_kg_per_m3": 1.0,
        "material_provenance": "test fixture",
        "force_magnitude_n": 10.0,
        "gauge_x_min_m": 1.0,
        "gauge_x_max_m": 9.0,
    }
    values.update(overrides)
    return BendingSpec(**values)  # type: ignore[arg-type]


def beam_mesh() -> MeshData:
    nodes = {
        1: (0.0, 0.0, 0.0),
        2: (0.0, 1.0, 0.0),
        3: (0.0, 0.0, 1.0),
        4: (0.0, 1.0, 1.0),
        5: (10.0, 0.0, 0.0),
        6: (10.0, 1.0, 0.0),
        7: (10.0, 0.0, 1.0),
        8: (10.0, 1.0, 1.0),
    }
    return MeshData(
        nodes=nodes,
        tetrahedra={1: (1, 5, 6, 7), 2: (1, 6, 7, 8)},
        triangles={1: (5, 6, 8), 2: (5, 8, 7)},
    )


class BendingSpecTests(unittest.TestCase):
    def test_euler_bernoulli_references_use_si_equations(self) -> None:
        spec = specimen()
        self.assertAlmostEqual(1.0 / 12.0, spec.second_moment_m4)
        self.assertAlmostEqual(400.0, spec.analytical_tip_displacement_m)
        self.assertAlmostEqual(100.0, spec.analytical_root_moment_nm)
        self.assertAlmostEqual(600.0, spec.analytical_root_outer_stress_pa)
        self.assertAlmostEqual(2000.0, spec.analytical_energy_j)
        self.assertAlmostEqual(270.0, spec.analytical_sxx_pa(x_m=1.0, z_m=0.75))

    def test_invalid_domain_and_nonfinite_inputs_are_rejected(self) -> None:
        for changes in (
            {"length_m": 9.0},
            {"gauge_x_min_m": 0.0},
            {"gauge_x_max_m": 10.0},
            {"force_magnitude_n": 0.0},
            {"youngs_modulus_pa": math.nan},
        ):
            with self.subTest(changes=changes):
                with self.assertRaises(StructuralEvidenceError):
                    specimen(**changes)

    def test_reference_point_outside_beam_is_rejected(self) -> None:
        with self.assertRaisesRegex(StructuralEvidenceError, "outside"):
            specimen().analytical_sxx_pa(x_m=11.0, z_m=0.5)


class BendingDeckTests(unittest.TestCase):
    def test_transverse_surface_load_closes_and_uses_dof_three(self) -> None:
        deck, loads, fixed, loaded = build_bending_calculix_input(
            spec=specimen(), mesh=beam_mesh(), boundary_tolerance_m=1.0e-12
        )
        self.assertEqual((1, 2, 3, 4), fixed)
        self.assertEqual((5, 6, 7, 8), loaded)
        self.assertTrue(math.isclose(math.fsum(loads.values()), -10.0))
        self.assertAlmostEqual(-10.0 / 3.0, loads[5])
        self.assertAlmostEqual(-10.0 / 6.0, loads[6])
        self.assertIn("*ELEMENT, TYPE=C3D4, ELSET=EALL", deck)
        self.assertIn("5, 3,", deck)
        self.assertNotIn("5, 1,", deck)

    def test_node_sets_wrap_before_calculix_entry_limit(self) -> None:
        mesh = beam_mesh()
        nodes = dict(mesh.nodes)
        for node_id in range(9, 26):
            nodes[node_id] = (0.0, node_id / 100.0, 0.5)
        expanded = MeshData(
            nodes=nodes,
            tetrahedra=mesh.tetrahedra,
            triangles=mesh.triangles,
        )
        deck, _, fixed, _ = build_bending_calculix_input(
            spec=specimen(), mesh=expanded, boundary_tolerance_m=1.0e-12
        )
        self.assertGreater(len(fixed), 16)
        fixed_block = deck.split("*NSET, NSET=FIXED", 1)[1].split(
            "*NSET, NSET=LOADED", 1
        )[0]
        for line in fixed_block.strip().splitlines():
            self.assertLessEqual(len(line.split(",")), 16)


if __name__ == "__main__":
    unittest.main()
