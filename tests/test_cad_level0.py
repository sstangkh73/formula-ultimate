from __future__ import annotations

import math
import unittest

from formula_ultimate.components.grammar import Material, MountingPlateSpec
from formula_ultimate.experiments.cad_level0 import (
    CadMeasurement,
    EvidenceViolation,
    Level0Controls,
    evaluate_cad_measurement,
)


class CadLevel0EvidenceTests(unittest.TestCase):
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
        self.controls = Level0Controls(300.0, 1200.0, 5.0, 0.05)

    def measurement(self, **changes: object) -> CadMeasurement:
        values: dict[str, object] = {
            "source": "FreeCAD STEP import",
            "volume_m3": self.spec.analytical_volume_m3,
            "solid_count": 1,
            "is_valid": True,
            "bounds_m": (0.200, 0.120, 0.008),
            "centre_of_mass_m": (0.0, 0.0, 0.004),
        }
        values.update(changes)
        return CadMeasurement(**values)  # type: ignore[arg-type]

    def test_freecad_volume_is_used_for_component_and_vehicle_mass(self) -> None:
        result = evaluate_cad_measurement(
            spec=self.spec,
            measurement=self.measurement(),
            controls=self.controls,
        )
        self.assertAlmostEqual(
            result.component_mass_kg,
            self.spec.analytical_volume_m3 * 2700.0,
        )
        self.assertAlmostEqual(
            result.total_vehicle_mass_kg,
            300.0 + result.component_mass_kg,
        )
        expected_speed = 1200.0 / result.total_vehicle_mass_kg * 5.0
        self.assertAlmostEqual(result.final_speed_mps, expected_speed, places=12)

    def test_invalid_topology_and_non_finite_measurement_are_observable(self) -> None:
        for changes in (
            {"solid_count": 2},
            {"is_valid": False},
            {"volume_m3": 0.0},
            {"volume_m3": math.nan},
        ):
            with self.subTest(changes=changes), self.assertRaises(EvidenceViolation):
                self.measurement(**changes)

    def test_malformed_measurement_types_and_vector_lengths_are_rejected(self) -> None:
        for changes in (
            {"source": ""},
            {"solid_count": 1.5},
            {"is_valid": 1},
            {"bounds_m": (0.200, 0.120)},
            {"centre_of_mass_m": (0.0, 0.0)},
        ):
            with self.subTest(changes=changes), self.assertRaises(EvidenceViolation):
                self.measurement(**changes)

    def test_volume_disagreement_is_rejected_not_corrected(self) -> None:
        with self.assertRaises(EvidenceViolation):
            evaluate_cad_measurement(
                spec=self.spec,
                measurement=self.measurement(
                    volume_m3=self.spec.analytical_volume_m3 * 1.01
                ),
                controls=self.controls,
            )

    def test_bounding_box_disagreement_is_rejected(self) -> None:
        with self.assertRaises(EvidenceViolation):
            evaluate_cad_measurement(
                spec=self.spec,
                measurement=self.measurement(bounds_m=(0.210, 0.120, 0.008)),
                controls=self.controls,
            )

    def test_control_contract_rejects_invalid_values(self) -> None:
        for values in (
            (0.0, 1200.0, 5.0, 0.05),
            (300.0, -1.0, 5.0, 0.05),
            (300.0, 1200.0, -1.0, 0.05),
            (300.0, 1200.0, 5.0, 0.0),
        ):
            with self.subTest(values=values), self.assertRaises(EvidenceViolation):
                Level0Controls(*values)


if __name__ == "__main__":
    unittest.main()
