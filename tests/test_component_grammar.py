from __future__ import annotations

from dataclasses import replace
import math
import unittest

from formula_ultimate.components.grammar import (
    GRAMMAR_VERSION,
    GrammarViolation,
    Material,
    MountingPlateSpec,
)


class MountingPlateGrammarTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = MountingPlateSpec(
            length_m=0.200,
            width_m=0.120,
            thickness_m=0.008,
            corner_radius_m=0.010,
            mounting_hole_diameter_m=0.008,
            mounting_spacing_x_m=0.160,
            mounting_spacing_y_m=0.080,
            lightening_radius_m=0.025,
            material=Material("Aluminium assumption", 2700.0),
        )

    def test_valid_spec_has_symmetric_interface_and_positive_properties(self) -> None:
        self.assertEqual(GRAMMAR_VERSION, self.spec.grammar_version)
        self.assertEqual(4, len(self.spec.mounting_hole_centres_m))
        self.assertGreater(self.spec.analytical_volume_m3, 0.0)
        self.assertAlmostEqual(
            self.spec.analytical_mass_kg,
            self.spec.analytical_volume_m3 * 2700.0,
        )

    def test_mapping_round_trip_preserves_spec(self) -> None:
        self.assertEqual(self.spec, MountingPlateSpec.from_mapping(self.spec.to_dict()))

    def test_version_and_schema_mismatch_are_rejected(self) -> None:
        with self.assertRaises(GrammarViolation):
            replace(self.spec, grammar_version="unreviewed_v2")
        mapping = self.spec.to_dict()
        mapping["undeclared_token"] = 1
        with self.assertRaises(GrammarViolation):
            MountingPlateSpec.from_mapping(mapping)

    def test_non_finite_and_dimensional_bounds_are_rejected(self) -> None:
        for change in (
            {"length_m": math.nan},
            {"length_m": 0.119},
            {"width_m": 0.201},
            {"thickness_m": 0.003},
            {"corner_radius_m": 0.031},
            {"mounting_hole_diameter_m": 0.004},
            {"lightening_radius_m": 0.081},
        ):
            with self.subTest(change=change), self.assertRaises(GrammarViolation):
                replace(self.spec, **change)

    def test_material_must_have_name_and_positive_finite_density(self) -> None:
        for name, density in (("", 2700.0), ("Al", 0.0), ("Al", math.inf)):
            with self.subTest(name=name, density=density), self.assertRaises(
                GrammarViolation
            ):
                Material(name, density)

    def test_corner_radius_is_limited_by_plate_width(self) -> None:
        with self.assertRaises(GrammarViolation):
            replace(self.spec, width_m=0.080, corner_radius_m=0.021)

    def test_mounting_interface_edge_ligament_is_enforced(self) -> None:
        with self.assertRaises(GrammarViolation):
            replace(self.spec, mounting_spacing_x_m=0.190)

    def test_mounting_interface_rounded_corner_ligament_is_enforced(self) -> None:
        with self.assertRaisesRegex(GrammarViolation, "rounded-corner ligament"):
            replace(
                self.spec,
                length_m=0.120,
                width_m=0.080,
                corner_radius_m=0.020,
                mounting_hole_diameter_m=0.012,
                mounting_spacing_x_m=0.095,
                mounting_spacing_y_m=0.055,
                lightening_radius_m=0.0,
            )

    def test_mounting_hole_to_hole_web_is_enforced(self) -> None:
        with self.assertRaises(GrammarViolation):
            replace(self.spec, mounting_spacing_y_m=0.015, mounting_hole_diameter_m=0.012)

    def test_lightening_cut_outer_ligament_is_enforced(self) -> None:
        with self.assertRaises(GrammarViolation):
            replace(self.spec, lightening_radius_m=0.055)

    def test_lightening_cut_web_to_mounting_hole_is_enforced(self) -> None:
        with self.assertRaises(GrammarViolation):
            replace(
                self.spec,
                mounting_spacing_x_m=0.040,
                mounting_spacing_y_m=0.040,
                lightening_radius_m=0.020,
            )

    def test_analytical_volume_decreases_with_lightening_radius(self) -> None:
        volumes = [
            replace(self.spec, lightening_radius_m=radius).analytical_volume_m3
            for radius in (0.0, 0.025, 0.040)
        ]
        self.assertGreater(volumes[0], volumes[1])
        self.assertGreater(volumes[1], volumes[2])


if __name__ == "__main__":
    unittest.main()
