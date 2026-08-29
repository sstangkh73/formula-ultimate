from __future__ import annotations

import math
from pathlib import Path
import tempfile
import unittest

from formula_ultimate.structural import (
    MeshData,
    StructuralEvidenceError,
    TensionSpec,
    build_calculix_input,
    parse_calculix_dat,
    parse_msh2,
)


def specimen(**overrides: object) -> TensionSpec:
    values: dict[str, object] = {
        "protocol_id": "protocol",
        "experiment_id": "experiment",
        "specimen_id": "specimen",
        "claim_level": "solver route only",
        "length_m": 1.0,
        "width_m": 1.0,
        "height_m": 1.0,
        "material_id": "synthetic",
        "youngs_modulus_pa": 100.0,
        "poisson_ratio": 0.3,
        "density_kg_per_m3": 1.0,
        "material_provenance": "test fixture",
        "resultant_force_n": 10.0,
    }
    values.update(overrides)
    return TensionSpec(**values)  # type: ignore[arg-type]


def cube_mesh() -> MeshData:
    nodes = {
        1: (0.0, 0.0, 0.0),
        2: (0.0, 1.0, 0.0),
        3: (0.0, 0.0, 1.0),
        4: (0.0, 1.0, 1.0),
        5: (1.0, 0.0, 0.0),
        6: (1.0, 1.0, 0.0),
        7: (1.0, 0.0, 1.0),
        8: (1.0, 1.0, 1.0),
    }
    return MeshData(
        nodes=nodes,
        tetrahedra={1: (1, 5, 6, 7), 2: (1, 6, 7, 8)},
        triangles={1: (5, 6, 8), 2: (5, 8, 7)},
    )


class TensionSpecTests(unittest.TestCase):
    def test_analytical_reference_uses_si_equations(self) -> None:
        spec = specimen()
        self.assertEqual(1.0, spec.area_m2)
        self.assertEqual(10.0, spec.analytical_stress_pa)
        self.assertEqual(0.1, spec.analytical_strain)
        self.assertEqual(0.1, spec.analytical_displacement_m)
        self.assertEqual(0.5, spec.analytical_energy_j)

    def test_nonphysical_or_nonfinite_parameters_are_rejected(self) -> None:
        for changes in (
            {"length_m": 0.0},
            {"youngs_modulus_pa": math.nan},
            {"poisson_ratio": 0.5},
            {"resultant_force_n": 0.0},
        ):
            with self.subTest(changes=changes):
                with self.assertRaises(StructuralEvidenceError):
                    specimen(**changes)


class MeshAndDeckTests(unittest.TestCase):
    def test_surface_load_closes_and_is_area_weighted(self) -> None:
        deck, loads, fixed, loaded = build_calculix_input(
            spec=specimen(), mesh=cube_mesh(), boundary_tolerance_m=1.0e-12
        )
        self.assertEqual((1, 2, 3, 4), fixed)
        self.assertEqual((5, 6, 7, 8), loaded)
        self.assertTrue(math.isclose(math.fsum(loads.values()), 10.0))
        self.assertAlmostEqual(10.0 / 3.0, loads[5])
        self.assertAlmostEqual(10.0 / 6.0, loads[6])
        self.assertIn("*ELEMENT, TYPE=C3D4, ELSET=EALL", deck)
        self.assertIn("FIXED, 1, 3, 0.0", deck)

    def test_disconnected_tetrahedra_are_rejected(self) -> None:
        with self.assertRaisesRegex(StructuralEvidenceError, "disconnected"):
            MeshData(
                nodes={
                    1: (0.0, 0.0, 0.0), 2: (1.0, 0.0, 0.0),
                    3: (0.0, 1.0, 0.0), 4: (0.0, 0.0, 1.0),
                    5: (2.0, 0.0, 0.0), 6: (3.0, 0.0, 0.0),
                    7: (2.0, 1.0, 0.0), 8: (2.0, 0.0, 1.0),
                },
                tetrahedra={1: (1, 2, 3, 4), 2: (5, 6, 7, 8)},
                triangles={1: (1, 2, 3)},
            )

    def test_ascii_msh2_subset_is_parsed(self) -> None:
        content = """$MeshFormat
2.2 0 8
$EndMeshFormat
$Nodes
4
1 0 0 0
2 1 0 0
3 0 1 0
4 0 0 1
$EndNodes
$Elements
2
1 2 0 1 2 3
2 4 0 1 2 3 4
$EndElements
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.msh"
            path.write_text(content, encoding="ascii")
            mesh = parse_msh2(path)
        self.assertEqual({2: (1, 2, 3, 4)}, mesh.tetrahedra)
        self.assertEqual({1: (1, 2, 3)}, mesh.triangles)


class CalculixParserTests(unittest.TestCase):
    def test_parser_keeps_stress_and_strain_tables_separate(self) -> None:
        content = """ displacements (vx,vy,vz) for set LOADED and time 1
 5 1.0E-03 0 0
 forces (fx,fy,fz) for set FIXED and time 1
 1 -1.0E+01 0 0
 total force (fx,fy,fz) for set FIXED and time 1
 -1.0E+01 0 0
 stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set EALL and time 1
 10 1 1.0E+07 0 0 0 0 0
 strains (elem, integ.pnt.,exx,eyy,ezz,exy,exz,eyz) for set EALL and time 1
 10 1 1.0E-04 0 0 0 0 0
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.dat"
            path.write_text(content, encoding="ascii")
            parsed = parse_calculix_dat(path)
        self.assertEqual({10: 10_000_000.0}, parsed["axial_stress_by_element_pa"])
        self.assertEqual(
            {10: (10_000_000.0, 0.0, 0.0, 0.0, 0.0, 0.0)},
            parsed["stress_tensor_by_element_pa"],
        )
        self.assertEqual((-10.0, 0.0, 0.0), parsed["reactions"][1])
        self.assertEqual((-10.0, 0.0, 0.0), parsed["total_reaction"])

    def test_missing_evidence_table_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.dat"
            path.write_text("not solver evidence", encoding="ascii")
            with self.assertRaisesRegex(StructuralEvidenceError, "missing"):
                parse_calculix_dat(path)


if __name__ == "__main__":
    unittest.main()
