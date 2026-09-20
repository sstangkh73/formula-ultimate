from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
for item in (ROOT, ROOT / "src"):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from formula_ultimate.structural.element_verification import ElementMeshData  # noqa: E402
from formula_ultimate.structural.geometry_general_evaluator import (  # noqa: E402
    CALCULIX_FIELD_LIMIT,
    FINAL_STATUS,
    STATUSES,
    GeometryEvaluationError,
    build_deck,
    calculix_number,
    classify_candidate,
    consistent_surface_loads,
    euler_bernoulli_tip_displacement,
    mesh_mass_properties,
    parse_static_dat,
    scaled_nodes,
    select_nodes,
    summarize,
    validate_protocol,
    von_mises,
)


CONFIG = ROOT / "config/development/geometry_general_evaluator_v1.json"
GMSH = Path("C:/Program Files/FreeCAD 1.1/bin/gmsh.exe")
CCX = Path("C:/Program Files/FreeCAD 1.1/bin/ccx.exe")
HAS_KERNEL = GMSH.is_file() and CCX.is_file()

MATERIAL = {
    "youngs_modulus_pa": 210000000000.0,
    "poisson_ratio": 0.3,
    "density_kg_m3": 7800.0,
    "allowable_von_mises_pa": 350000000.0,
    "evidence_class": "synthetic_geometry_only",
}


def unit_tetrahedron_mesh() -> tuple[ElementMeshData, dict[int, tuple[float, float, float]]]:
    """One straight-sided C3D10 tetrahedron with its four exterior faces."""

    corners = {1: (0.0, 0.0, 0.0), 2: (1.0, 0.0, 0.0), 3: (0.0, 1.0, 0.0), 4: (0.0, 0.0, 1.0)}
    edges = {
        5: (1, 2), 6: (2, 3), 7: (1, 3), 8: (1, 4), 9: (2, 4), 10: (3, 4),
    }
    nodes = dict(corners)
    for node, (first, second) in edges.items():
        nodes[node] = tuple((corners[first][i] + corners[second][i]) / 2.0 for i in range(3))
    tetrahedra = {1: (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)}
    triangles = {
        1: (1, 2, 3, 5, 6, 7),
        2: (1, 2, 4, 5, 9, 8),
        3: (2, 3, 4, 6, 10, 9),
        4: (1, 3, 4, 7, 10, 8),
    }
    return ElementMeshData(nodes, tetrahedra, triangles, 2), nodes


class DeclarationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8"))

    def test_frozen_declaration_is_valid(self) -> None:
        declaration = validate_protocol(self.raw)
        self.assertEqual(declaration["status"], "passed")
        self.assertGreaterEqual(declaration["level_count"], 3)
        self.assertEqual(declaration["control_count"], 8)

    def test_declaration_fails_closed(self) -> None:
        coarsening = copy.deepcopy(self.raw)
        coarsening["mesh_levels"] = list(reversed(coarsening["mesh_levels"]))
        with self.assertRaisesRegex(GeometryEvaluationError, "coarse to fine"):
            validate_protocol(coarsening)

        two_levels = copy.deepcopy(self.raw)
        two_levels["mesh_levels"] = two_levels["mesh_levels"][:2]
        with self.assertRaisesRegex(GeometryEvaluationError, "three mesh levels"):
            validate_protocol(two_levels)

        unknown_material = copy.deepcopy(self.raw)
        unknown_material["candidates"][0]["material_id"] = "unobtainium"
        with self.assertRaisesRegex(GeometryEvaluationError, "material is not declared"):
            validate_protocol(unknown_material)

        zero_load = copy.deepcopy(self.raw)
        zero_load["candidates"][0]["load_cases"][0]["force_n"] = [0.0, 0.0, 0.0]
        with self.assertRaisesRegex(GeometryEvaluationError, "force must not be zero"):
            validate_protocol(zero_load)

        seven_controls = copy.deepcopy(self.raw)
        seven_controls["controls"] = seven_controls["controls"][:7]
        with self.assertRaisesRegex(GeometryEvaluationError, "eight registered controls"):
            validate_protocol(seven_controls)


class CalculiXFieldTests(unittest.TestCase):
    """CalculiX truncates a free field at 20 characters, silently."""

    def test_numbers_stay_inside_the_parser_limit(self) -> None:
        for value in (0.0048680114672994467, -1000.0, 6.9e10, 1e-18, -2.2621670056434022e-06):
            text = calculix_number(value)
            self.assertLessEqual(len(text), CALCULIX_FIELD_LIMIT)
            self.assertAlmostEqual(float(text), value, delta=abs(value) * 1e-9 + 1e-300)

    def test_non_finite_values_are_refused(self) -> None:
        for value in (float("nan"), float("inf"), "0.1", True):
            with self.assertRaises(GeometryEvaluationError):
                calculix_number(value)

    def test_deck_fields_are_all_representable(self) -> None:
        mesh, nodes = unit_tetrahedron_mesh()
        loads = consistent_surface_loads(mesh, nodes, (2, 3, 4, 6, 9, 10), [0.0, 0.0, -1234.5678901234])
        deck = build_deck(
            mesh=mesh, nodes=nodes, material_id="steel", material=MATERIAL,
            fixed=(1, 5, 7, 8), loads=loads, heading="a heading line longer than twenty characters",
        )
        for index, line in enumerate(deck.splitlines()):
            if line.startswith("*") or index == 1:
                continue
            for field in line.split(","):
                self.assertLessEqual(len(field.strip()), CALCULIX_FIELD_LIMIT, line)
        self.assertIn("*ELEMENT, TYPE=C3D10, ELSET=EALL", deck)

    def test_overlapping_boundary_and_load_is_refused(self) -> None:
        mesh, nodes = unit_tetrahedron_mesh()
        loads = consistent_surface_loads(mesh, nodes, (2, 3, 4, 6, 9, 10), [0.0, 0.0, -100.0])
        with self.assertRaisesRegex(GeometryEvaluationError, "both fixed and loaded"):
            build_deck(
                mesh=mesh, nodes=nodes, material_id="steel", material=MATERIAL,
                fixed=tuple(loads), loads=loads, heading="overlap",
            )


class GeometryMeasurementTests(unittest.TestCase):
    def test_mass_properties_come_from_the_mesh(self) -> None:
        mesh, nodes = unit_tetrahedron_mesh()
        properties = mesh_mass_properties(mesh, nodes, 7800.0)
        self.assertAlmostEqual(properties["volume_m3"], 1.0 / 6.0, places=12)
        self.assertAlmostEqual(properties["mass_kg"], 7800.0 / 6.0, places=9)
        for value in properties["center_m"]:
            self.assertAlmostEqual(value, 0.25, places=12)

    def test_scaling_and_selection_follow_the_declaration(self) -> None:
        mesh, _ = unit_tetrahedron_mesh()
        nodes = scaled_nodes(mesh, 0.001)
        self.assertAlmostEqual(max(xyz[0] for xyz in nodes.values()), 0.001, places=12)
        selected = select_nodes(nodes, {"axis": "x", "side": "maximum", "tolerance_m": 1e-09})
        self.assertEqual(selected, (2,))
        with self.assertRaises(GeometryEvaluationError):
            select_nodes(nodes, {"axis": "w", "side": "maximum", "tolerance_m": 1e-09})

    def test_surface_loads_close_on_the_declared_resultant(self) -> None:
        mesh, nodes = unit_tetrahedron_mesh()
        force = [10.0, -20.0, 30.0]
        loads = consistent_surface_loads(mesh, nodes, (1, 2, 3, 5, 6, 7), force)
        for index, component in enumerate(force):
            self.assertAlmostEqual(sum(load[index] for load in loads.values()), component, places=9)
        # Corner shape functions integrate to zero on a TRI6 face.
        self.assertEqual(sorted(loads), [5, 6, 7])

    def test_incomplete_load_face_is_refused(self) -> None:
        mesh, nodes = unit_tetrahedron_mesh()
        with self.assertRaisesRegex(GeometryEvaluationError, "no complete face triangles"):
            consistent_surface_loads(mesh, nodes, (1, 2), [0.0, 0.0, -1.0])


class ClassificationTests(unittest.TestCase):
    convergence = {"displacement_relative": 0.05, "stress_relative": 0.2}
    residuals = {"reaction_relative": 0.02, "declared_mass_relative": 0.05}

    def levels(self, **overrides):
        base = {
            "status": "solved", "maximum_displacement_m": 1.0e-4, "p90_von_mises_pa": 1.0e6,
            "maximum_von_mises_pa": 2.0e6, "total_reaction_n": [0.0, 0.0, 1000.0], "mass_kg": 10.0,
        }
        base.update(overrides)
        return [
            {**base, "level_id": "coarse", "maximum_displacement_m": base["maximum_displacement_m"] * 1.02},
            {**base, "level_id": "medium", "maximum_displacement_m": base["maximum_displacement_m"] * 1.005},
            {**base, "level_id": "fine"},
        ]

    def classify(self, levels, **overrides):
        arguments = {
            "levels": levels, "convergence": self.convergence, "residuals": self.residuals,
            "allowable_von_mises_pa": 1.0e8, "applied_force_n": [0.0, 0.0, -1000.0], "declared_mass_kg": None,
        }
        arguments.update(overrides)
        return classify_candidate(**arguments)

    def test_converged_within_allowable_passes(self) -> None:
        verdict = self.classify(self.levels())
        self.assertEqual(verdict["status"], "passed")
        self.assertIsNone(verdict["cause"])
        self.assertAlmostEqual(verdict["utilization"], 0.02, places=9)

    def test_tooling_limits_are_never_physical_verdicts(self) -> None:
        for level_status, expected in (
            ("unresolved_mesh", "unresolved_mesh"),
            ("unresolved_solver", "unresolved_solver"),
            ("unsupported_representation", "unsupported_representation"),
        ):
            levels = self.levels()
            levels[1] = {**levels[1], "status": level_status, "cause": "declared by the control"}
            verdict = self.classify(levels)
            self.assertEqual(verdict["status"], expected)
            self.assertNotEqual(verdict["status"], "failed_physics")

    def test_unconverged_refinement_is_unresolved_not_passed(self) -> None:
        levels = self.levels()
        levels[2] = {**levels[2], "maximum_displacement_m": 2.0e-4}
        verdict = self.classify(levels)
        self.assertEqual(verdict["status"], "unresolved_convergence")

    def test_two_solved_levels_cannot_pass(self) -> None:
        verdict = self.classify(self.levels()[:2])
        self.assertEqual(verdict["status"], "unresolved_convergence")

    def test_unbalanced_reaction_is_a_solver_finding(self) -> None:
        verdict = self.classify(self.levels(total_reaction_n=[0.0, 0.0, 10.0]))
        self.assertEqual(verdict["status"], "unresolved_solver")

    def test_overstress_and_contradicted_mass_fail_physics(self) -> None:
        overstressed = self.classify(self.levels(), allowable_von_mises_pa=1.0e5)
        self.assertEqual(overstressed["status"], "failed_physics")
        contradicted = self.classify(self.levels(), declared_mass_kg=1.0)
        self.assertEqual(contradicted["status"], "failed_physics")
        self.assertEqual(contradicted["cause"], "mesh mass contradicts the declared mass")


class EvidenceTests(unittest.TestCase):
    def test_von_mises_matches_uniaxial_stress(self) -> None:
        self.assertAlmostEqual(von_mises((100.0, 0.0, 0.0, 0.0, 0.0, 0.0)), 100.0, places=9)

    def test_static_dat_parsing_keeps_every_integration_point(self) -> None:
        text = "\n".join([
            "displacements (vx,vy,vz) for set NALL",
            "         1  1.000000E-04  0.000000E+00  0.000000E+00",
            "         2  0.000000E+00  0.000000E+00 -2.000000E-04",
            "forces (fx,fy,fz) for set FIXED",
            "         1  0.000000E+00  0.000000E+00  5.000000E+02",
            "total force (fx,fy,fz) for set FIXED",
            "  0.000000E+00  0.000000E+00  1.000000E+03",
            "stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set EALL",
            "     1   1  1.000000E+06  0.0  0.0  0.0  0.0  0.0",
            "     1   2  3.000000E+06  0.0  0.0  0.0  0.0  0.0",
            "strains (elem, integ.pnt.,exx,eyy,ezz,exy,exz,eyz) for set EALL",
            "     1   1  1.000000E-06  0.0  0.0  0.0  0.0  0.0",
        ])
        measured = parse_static_dat(text)
        self.assertAlmostEqual(measured["maximum_displacement_m"], 2.0e-4, places=12)
        self.assertAlmostEqual(measured["maximum_von_mises_pa"], 3.0e6, places=3)
        self.assertEqual(measured["integration_point_count"], 2)
        self.assertEqual(measured["total_reaction_n"], [0.0, 0.0, 1000.0])

    def test_truncated_solver_evidence_is_refused(self) -> None:
        with self.assertRaisesRegex(GeometryEvaluationError, "table is missing"):
            parse_static_dat("displacements (vx,vy,vz) for set NALL\n 1 0.0 0.0 0.0\n")

    def test_summary_accounts_for_every_candidate(self) -> None:
        candidates = [
            {"candidate_id": "a", "status": "passed"},
            {"candidate_id": "b", "status": "unresolved_mesh", "cause": "gmsh refused"},
        ]
        controls = [{"control_id": f"c{index}", "rejected": True} for index in range(8)]
        summary = summarize(candidates, controls)
        self.assertEqual(summary["status"], FINAL_STATUS)
        self.assertEqual(summary["unresolved_count"], 1)
        self.assertEqual(sum(summary["status_counts"].values()), len(candidates))
        self.assertFalse(summary["promotion_allowed"])
        self.assertFalse(summary["physical_validation"])
        self.assertEqual(set(summary["status_counts"]), set(STATUSES))

    def test_summary_fails_when_a_control_survives(self) -> None:
        controls = [{"control_id": f"c{index}", "rejected": index != 0} for index in range(8)]
        summary = summarize([{"candidate_id": "a", "status": "passed"}], controls)
        self.assertEqual(summary["status"], "failed_controls")

    def test_unregistered_status_is_refused(self) -> None:
        with self.assertRaisesRegex(GeometryEvaluationError, "unregistered status"):
            summarize([{"candidate_id": "a", "status": "looks_fine"}], [])

    def test_closed_form_benchmark(self) -> None:
        displacement = euler_bernoulli_tip_displacement(
            force_n=100.0, length_m=0.5, width_m=0.05, height_m=0.02, youngs_modulus_pa=2.1e11
        )
        self.assertAlmostEqual(displacement, 0.0005952380952380952, places=12)


@unittest.skipUnless(HAS_KERNEL, "Gmsh and CalculiX kernel tests use the pinned FreeCAD runtimes")
class KernelTests(unittest.TestCase):
    def test_benchmark_box_meshes_solves_and_matches_the_closed_form(self) -> None:
        import tempfile  # noqa: PLC0415

        from scripts.structural.mesh_step_solid import mesh_solid  # noqa: PLC0415
        from scripts.structural.run_geometry_general_evaluator import solve_deck  # noqa: PLC0415
        from formula_ultimate.structural.element_verification import parse_element_msh2  # noqa: PLC0415

        geometry = {"kind": "benchmark_box", "length_m": 0.5, "width_m": 0.05, "height_m": 0.02}
        with tempfile.TemporaryDirectory() as raw_directory:
            work_dir = Path(raw_directory)
            evidence, mesh_path = mesh_solid(
                gmsh=GMSH, geometry=geometry, size_factor=1.0, work_dir=work_dir, timeout_s=300.0
            )
            self.assertEqual(evidence["exit_code"], 0, evidence["stderr_tail"])
            mesh = parse_element_msh2(mesh_path, expected_order=2)
            nodes = scaled_nodes(mesh, 1.0)
            fixed = select_nodes(nodes, {"axis": "x", "side": "minimum", "tolerance_m": 1e-06})
            loaded = select_nodes(nodes, {"axis": "x", "side": "maximum", "tolerance_m": 1e-06})
            loads = consistent_surface_loads(mesh, nodes, loaded, [0.0, 0.0, -100.0])
            deck = build_deck(
                mesh=mesh, nodes=nodes, material_id="steel", material=MATERIAL,
                fixed=fixed, loads=loads, heading="work138 kernel benchmark",
            )
            solve = solve_deck(CCX, work_dir, deck, timeout_s=600.0)
            self.assertEqual(solve["exit_code"], 0, solve["stdout_tail"])
            measured = parse_static_dat(solve["dat_path"].read_text(encoding="ascii", errors="replace"))
        analytical = euler_bernoulli_tip_displacement(
            force_n=100.0, length_m=0.5, width_m=0.05, height_m=0.02, youngs_modulus_pa=2.1e11
        )
        self.assertLess(abs(measured["maximum_displacement_m"] - analytical) / analytical, 0.1)
        self.assertAlmostEqual(measured["total_reaction_n"][2], 100.0, delta=0.1)


if __name__ == "__main__":
    unittest.main()
