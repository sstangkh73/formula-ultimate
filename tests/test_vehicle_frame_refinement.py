import unittest

from formula_ultimate.structural.vehicle_frame_refinement import (
    FrameModel,
    VehicleFrameError,
    analytical_cantilever,
    benchmark_model,
    build_calculix_b31_deck,
    parse_calculix_b31_dat,
    parse_calculix_section_forces_frd,
    section_force_extreme_von_mises,
    solve_frame,
)


class VehicleFrameRefinementTests(unittest.TestCase):
    def test_project_frame_matches_cantilever_analytical_reference(self):
        length, side, force, young = 1.0, 0.02, 100.0, 70e9
        reference = analytical_cantilever(length, side, force, young)
        for subdivisions in (1, 2, 4):
            model, loads = benchmark_model(length, side, subdivisions)
            loads = {node: (0.0, -force, 0.0, 0.0, 0.0, 0.0) for node in loads}
            result = solve_frame(model, loads, young, 0.3)
            self.assertAlmostEqual(reference["tip_displacement_m"], result.maximum_displacement_m, places=10)
            self.assertAlmostEqual(reference["maximum_bending_stress_pa"], result.maximum_von_mises_pa, delta=reference["maximum_bending_stress_pa"]*0.01)
            self.assertLess(max(abs(x) for x in result.equilibrium_residual), 1e-7)

    def test_load_reversal_and_refinement_are_deterministic(self):
        model, loads = benchmark_model(1.0, 0.02, 4)
        node = next(iter(loads))
        positive = {node: (0, 100, 0, 0, 0, 0)}
        negative = {node: (0, -100, 0, 0, 0, 0)}
        a = solve_frame(model, positive, 70e9, 0.3)
        b = solve_frame(model, negative, 70e9, 0.3)
        self.assertAlmostEqual(a.maximum_displacement_m, b.maximum_displacement_m)
        self.assertAlmostEqual(a.maximum_von_mises_pa, b.maximum_von_mises_pa)
        self.assertEqual(a.node_displacements[-1][1][1], -b.node_displacements[-1][1][1])

    def test_deck_and_strict_parser(self):
        model, loads = benchmark_model(1.0, 0.02, 1)
        deck = build_calculix_b31_deck(model, loads, 70e9, 0.3)
        self.assertIn("*ELEMENT,TYPE=B31", deck)
        self.assertIn("*BEAM SECTION", deck)
        fixture = """displacements (vx,vy,vz) for set NALL and time 1.0
 1 0 0 0
 2 0 -1.0E-3 0
 stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set E_BEAM and time 1.0
 1 1 1.0E6 0 0 0 0 0
"""
        parsed = parse_calculix_b31_dat(fixture)
        self.assertEqual(1e-3, parsed["maximum_displacement_m"])
        self.assertEqual(1e6, parsed["maximum_von_mises_pa"])
        with self.assertRaisesRegex(VehicleFrameError, "stress"):
            parse_calculix_b31_dat("displacements (vx,vy,vz)\n1 0 0 0\n")

    def test_section_force_frd_parser_and_surface_stress(self):
        fixture = """ -4  STRESS      6    1
 -5  SXX         1    4    1    1
 -1         1 0.00000E+00 1.00000E+02 0.00000E+00 0.00000E+00-5.00000E+01 0.00000E+00
 -1         2 0.00000E+00 1.00000E+02 0.00000E+00 0.00000E+00-5.00000E+01 0.00000E+00
 -3
"""
        rows = parse_calculix_section_forces_frd(fixture)
        self.assertEqual(2, len(rows))
        model, _ = benchmark_model(1.0, 0.02, 1)
        stress = section_force_extreme_von_mises(rows, model.sections[0])
        expected_bending = 6 * 50 / 0.02**3
        expected_shear = 1.5 * 100 / 0.02**2
        self.assertAlmostEqual(
            (expected_bending**2 + 3 * expected_shear**2) ** 0.5,
            stress,
        )
        with self.assertRaisesRegex(VehicleFrameError, "missing"):
            parse_calculix_section_forces_frd("9999\n")

    def test_invalid_stiffness_and_singular_model_fail_closed(self):
        model, loads = benchmark_model(1.0, 0.02, 1)
        with self.assertRaisesRegex(VehicleFrameError, "stiffness"):
            solve_frame(model, loads, 0.0, 0.3)
        disconnected = FrameModel(model.nodes, (), model.sections, model.fixed_node_id, model.component_node_ids)
        with self.assertRaisesRegex(VehicleFrameError, "singular"):
            solve_frame(disconnected, loads, 70e9, 0.3)


if __name__ == "__main__":
    unittest.main()
