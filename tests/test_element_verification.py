from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from formula_ultimate.structural import (
    StructuralEvidenceError,
    TensionSpec,
    build_element_column_input,
    parse_element_column_dat,
    parse_element_msh2,
)


MSH2_C3D10 = """$MeshFormat
2.2 0 8
$EndMeshFormat
$Nodes
10
1 0 0 0
2 1 0 0
3 1 1 0
4 1 0 1
5 0.5 0 0
6 1 0.5 0
7 0.5 0.5 0
8 0.5 0 0.5
9 1 0.5 0.5
10 1 0 0.5
$EndNodes
$Elements
2
1 9 0 2 3 4 6 9 10
2 11 0 1 2 3 4 5 6 7 8 9 10
$EndElements
"""


class ElementMeshTests(unittest.TestCase):
    def test_gmsh_c3d10_order_is_converted_for_calculix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mesh.msh"
            path.write_text(MSH2_C3D10, encoding="ascii")
            mesh = parse_element_msh2(path, expected_order=2)
        self.assertEqual((1, 2, 3, 4, 5, 6, 7, 8, 10, 9), mesh.tetrahedra[2])
        self.assertEqual("C3D10", mesh.calculix_element_type)

    def test_quadratic_face_constant_load_uses_only_midsides_and_closes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mesh.msh"
            path.write_text(MSH2_C3D10, encoding="ascii")
            mesh = parse_element_msh2(path, expected_order=2)
        spec = TensionSpec(
            "p", "e", "s", "fixture", 1.0, 1.0, 0.5, "m", 70e9, 0.3, 2700.0, "synthetic", -90.0
        )
        deck, loads, fixed, loaded = build_element_column_input(spec=spec, mesh=mesh, boundary_tolerance_m=1e-12)
        self.assertEqual({6, 9, 10}, set(loads))
        self.assertAlmostEqual(-90.0, sum(loads.values()))
        self.assertEqual((1,), fixed)
        self.assertEqual({2, 3, 4, 6, 9, 10}, set(loaded))
        self.assertIn("*ELEMENT, TYPE=C3D10", deck)
        self.assertIn("2, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9", deck)

    def test_wrong_element_order_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mesh.msh"
            path.write_text(MSH2_C3D10, encoding="ascii")
            with self.assertRaises(StructuralEvidenceError):
                parse_element_msh2(path, expected_order=1)


class ElementDatTests(unittest.TestCase):
    def test_parser_retains_multiple_integration_points(self) -> None:
        text = """
 displacements (vx,vy,vz) for set LOADED
 2 1.0E-3 2.0E-3 3.0E-3
 forces (fx,fy,fz) for set FIXED
 1 9.0E1 0.0E0 0.0E0
 total force (fx,fy,fz) for set FIXED
 9.0E1 0.0E0 0.0E0
 stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set EALL
 2 1 1.0E6 0 0 0 0 0
 2 2 2.0E6 0 0 0 0 0
 strains (elem, integ.pnt.,exx,eyy,ezz,exy,exz,eyz) for set EALL
 2 1 1.0E-5 0 0 0 0 0
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "column.dat"
            path.write_text(text, encoding="ascii")
            parsed = parse_element_column_dat(path)
        self.assertEqual(2, len(parsed["stress_tensors_pa"]))
        self.assertEqual((90.0, 0.0, 0.0), parsed["total_reaction"])


if __name__ == "__main__":
    unittest.main()
