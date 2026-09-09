from __future__ import annotations

import copy
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.components.spatial_material import (
    SpatialMaterialViolation,
    canonical_bytes,
    combine_mass_properties,
    dependent_evidence_identity,
    validate_declaration,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "development" / "spatial_material_v1.json"


class SpatialMaterialDeclarationTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8"))

    def test_registered_declaration_passes_with_required_coverage(self):
        result = validate_declaration(self.raw)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["case_count"], 3)
        self.assertEqual(result["family_coverage"], ["curved", "hollow", "multi_body"])

    def test_duplicate_and_incomplete_body_ownership_fail_closed(self):
        duplicate = copy.deepcopy(self.raw)
        duplicate["cases"][0]["material_regions"].append(
            {"region_id": "duplicate", "material_id": "synthetic_steel", "body_indices": [0]}
        )
        with self.assertRaisesRegex(SpatialMaterialViolation, "duplicate body ownership"):
            validate_declaration(duplicate)

        missing = copy.deepcopy(self.raw)
        missing["cases"][2]["material_regions"] = missing["cases"][2]["material_regions"][:-1]
        with self.assertRaisesRegex(SpatialMaterialViolation, "exactly one owner"):
            validate_declaration(missing)

    def test_unknown_material_and_nonfinite_placement_fail_closed(self):
        unknown = copy.deepcopy(self.raw)
        unknown["cases"][0]["material_regions"][0]["material_id"] = "unknown"
        with self.assertRaisesRegex(SpatialMaterialViolation, "unknown material"):
            validate_declaration(unknown)

        nonfinite = copy.deepcopy(self.raw)
        nonfinite["cases"][0]["placement"]["translation_m"][1] = math.inf
        with self.assertRaisesRegex(SpatialMaterialViolation, "must be finite"):
            validate_declaration(nonfinite)
        with self.assertRaisesRegex(SpatialMaterialViolation, "finite canonical JSON"):
            canonical_bytes({"invalid": math.nan})

    def test_cavity_must_match_explicit_subtraction_schema(self):
        invalid = copy.deepcopy(self.raw)
        invalid["cases"][1]["void_regions"][0]["operation"] = "implicit_complement"
        with self.assertRaisesRegex(SpatialMaterialViolation, "subtractive void"):
            validate_declaration(invalid)

    def test_material_and_placement_mutations_change_evidence_identity(self):
        case = self.raw["cases"][0]
        original = dependent_evidence_identity(
            case["source_step_sha256"], case["material_regions"], case["placement"], case["void_regions"]
        )
        material = copy.deepcopy(case)
        material["material_regions"][0]["material_id"] = "synthetic_steel"
        moved = copy.deepcopy(case)
        moved["placement"]["translation_m"][2] += 0.01
        self.assertNotEqual(
            original,
            dependent_evidence_identity(
                material["source_step_sha256"], material["material_regions"], material["placement"], material["void_regions"]
            ),
        )
        self.assertNotEqual(
            original,
            dependent_evidence_identity(
                moved["source_step_sha256"], moved["material_regions"], moved["placement"], moved["void_regions"]
            ),
        )


class SpatialMaterialMassPropertyTests(unittest.TestCase):
    def test_homogeneous_rectangular_solid_matches_analytic_mass_and_inertia(self):
        size = (0.01, 0.02, 0.03)
        volume = math.prod(size)
        density = 2700.0
        inertia_per_density = [
            [volume * (size[1] ** 2 + size[2] ** 2) / 12.0, 0.0, 0.0],
            [0.0, volume * (size[0] ** 2 + size[2] ** 2) / 12.0, 0.0],
            [0.0, 0.0, volume * (size[0] ** 2 + size[1] ** 2) / 12.0],
        ]
        result = combine_mass_properties(
            [
                {
                    "volume_m3": volume,
                    "density_kg_m3": density,
                    "centre_m": [0.1, -0.2, 0.3],
                    "centroidal_inertia_per_density_m5": inertia_per_density,
                }
            ]
        )
        self.assertAlmostEqual(result["mass_kg"], volume * density, places=15)
        self.assertEqual(result["centre_of_mass_m"], [0.1, -0.2, 0.3])
        for axis in range(3):
            self.assertAlmostEqual(
                result["centroidal_inertia_kg_m2"][axis][axis],
                inertia_per_density[axis][axis] * density,
                places=15,
            )

    def test_parallel_axis_combination_is_symmetric_and_moves_centre(self):
        unit_inertia = [[1e-6, 0.0, 0.0], [0.0, 1e-6, 0.0], [0.0, 0.0, 1e-6]]
        result = combine_mass_properties(
            [
                {
                    "volume_m3": 1e-3,
                    "density_kg_m3": 1000.0,
                    "centre_m": [-1.0, 0.0, 0.0],
                    "centroidal_inertia_per_density_m5": unit_inertia,
                },
                {
                    "volume_m3": 1e-3,
                    "density_kg_m3": 3000.0,
                    "centre_m": [1.0, 0.0, 0.0],
                    "centroidal_inertia_per_density_m5": unit_inertia,
                },
            ]
        )
        self.assertEqual(result["centre_of_mass_m"], [0.5, 0.0, 0.0])
        inertia = result["centroidal_inertia_kg_m2"]
        self.assertAlmostEqual(inertia[0][1], inertia[1][0])
        self.assertGreater(inertia[1][1], inertia[0][0])
        self.assertGreater(inertia[2][2], inertia[0][0])


if __name__ == "__main__":
    unittest.main()
