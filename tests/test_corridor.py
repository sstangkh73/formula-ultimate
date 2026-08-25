from __future__ import annotations

from dataclasses import replace
import math
from pathlib import Path
import unittest

from formula_ultimate.physics.corridor import (
    CircuitCorridor,
    CorridorEvidence,
    CorridorInputError,
    CorridorSegment,
    VehicleEnvelope,
    assess_vehicle_corridor,
    closure_residual,
    corridor_from_mapping,
    integrate_corridor,
    load_corridors,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "config" / "circuits" / "corridor_schema_v1.json"


def evidence(evidence_class: str = "synthetic_validation", uncertainty: float = 0.0):
    return CorridorEvidence(
        evidence_class=evidence_class,
        source_id="test-source",
        source_title="Analytical test source",
        source_url="urn:formula-ultimate:test",
        coordinate_reference_system="local Cartesian ENU metres",
        horizontal_uncertainty_m=uncertainty,
        vertical_uncertainty_m=0.0,
    )


def segment(**overrides: float | str) -> CorridorSegment:
    values: dict[str, float | str] = {
        "segment_id": "s1",
        "length_m": 10.0,
        "curvature_1pm": 0.0,
        "grade_rad": 0.0,
        "bank_rad": 0.0,
        "width_left_m": 3.0,
        "width_right_m": 3.0,
    }
    values.update(overrides)
    return CorridorSegment(**values)  # type: ignore[arg-type]


def corridor(
    *segments: CorridorSegment,
    evidence_class: str = "synthetic_validation",
    uncertainty: float = 0.0,
    closed_loop: bool = False,
) -> CircuitCorridor:
    return CircuitCorridor(
        schema_version="1.0",
        corridor_id="test-corridor",
        circuit_id="test-circuit",
        layout_reference="unit test",
        start_x_m=0.0,
        start_y_m=0.0,
        start_z_m=0.0,
        start_heading_rad=0.0,
        closed_loop=closed_loop,
        evidence=evidence(evidence_class, uncertainty),
        segments=segments or (segment(),),
    )


def vehicle(**overrides: float) -> VehicleEnvelope:
    values = {
        "width_m": 2.0,
        "wheelbase_m": 3.0,
        "front_overhang_m": 1.0,
        "rear_overhang_m": 1.0,
        "max_steering_angle_rad": 0.7,
    }
    values.update(overrides)
    return VehicleEnvelope(**values)


class CorridorPhysicsTests(unittest.TestCase):
    def test_versioned_fixture_loads_deterministically(self) -> None:
        first = load_corridors(FIXTURES)
        second = load_corridors(FIXTURES)
        self.assertEqual(first, second)
        self.assertEqual(3, len(first))

    def test_straight_integration_includes_grade(self) -> None:
        stations = integrate_corridor(
            corridor(segment(length_m=10.0, grade_rad=math.atan(0.1))),
            maximum_station_spacing_m=4.0,
        )
        self.assertEqual(4, len(stations))
        self.assertAlmostEqual(10.0, stations[-1].x_m)
        self.assertAlmostEqual(0.0, stations[-1].y_m)
        self.assertAlmostEqual(1.0, stations[-1].z_m)

    def test_quarter_circle_has_exact_endpoint(self) -> None:
        radius_m = 20.0
        stations = integrate_corridor(
            corridor(
                segment(
                    length_m=math.pi * radius_m / 2.0,
                    curvature_1pm=1.0 / radius_m,
                )
            ),
            maximum_station_spacing_m=100.0,
        )
        self.assertAlmostEqual(radius_m, stations[-1].x_m, places=12)
        self.assertAlmostEqual(radius_m, stations[-1].y_m, places=12)
        self.assertAlmostEqual(math.pi / 2.0, stations[-1].heading_rad, places=12)

    def test_right_turn_is_mirrored(self) -> None:
        radius_m = 20.0
        station = integrate_corridor(
            corridor(
                segment(
                    length_m=math.pi * radius_m / 2.0,
                    curvature_1pm=-1.0 / radius_m,
                )
            ),
            maximum_station_spacing_m=100.0,
        )[-1]
        self.assertAlmostEqual(radius_m, station.x_m, places=12)
        self.assertAlmostEqual(-radius_m, station.y_m, places=12)

    def test_full_circle_closure_residual_is_observable_and_near_zero(self) -> None:
        radius_m = 20.0
        residual = closure_residual(
            corridor(
                segment(
                    length_m=2.0 * math.pi * radius_m,
                    curvature_1pm=1.0 / radius_m,
                ),
                closed_loop=True,
            )
        )
        self.assertLess(residual.horizontal_m, 1.0e-12)
        self.assertEqual(0.0, residual.vertical_m)
        self.assertLess(residual.heading_rad, 1.0e-12)

    def test_static_width_can_pass_while_overhang_sweep_rejects(self) -> None:
        assessment = assess_vehicle_corridor(
            corridor(
                segment(
                    length_m=5.0,
                    curvature_1pm=0.2,
                    width_left_m=1.5,
                    width_right_m=1.5,
                )
            ),
            vehicle(),
        )
        self.assertEqual("rejected", assessment.status)
        self.assertLess(assessment.minimum_margin_m, 0.0)
        self.assertEqual("s1", assessment.first_failing_segment_id)

    def test_steering_limit_rejects_tight_curvature(self) -> None:
        assessment = assess_vehicle_corridor(
            corridor(segment(curvature_1pm=1.0 / 3.0, width_left_m=6.0, width_right_m=6.0)),
            vehicle(max_steering_angle_rad=0.7),
        )
        self.assertEqual("rejected", assessment.status)
        self.assertGreater(
            assessment.segment_assessments[0].required_steering_angle_rad, 0.7
        )

    def test_synthetic_pass_is_not_real_circuit_admission(self) -> None:
        assessment = assess_vehicle_corridor(corridor(), vehicle())
        self.assertEqual("verification_passed", assessment.status)
        self.assertNotEqual("admitted", assessment.status)

    def test_admission_capable_evidence_can_admit_passing_geometry(self) -> None:
        assessment = assess_vehicle_corridor(
            corridor(evidence_class="operator_engineering"), vehicle()
        )
        self.assertEqual("admitted", assessment.status)

    def test_approximate_geometry_remains_indeterminate(self) -> None:
        assessment = assess_vehicle_corridor(
            corridor(evidence_class="digitized_approximate"), vehicle()
        )
        self.assertEqual("indeterminate", assessment.status)

    def test_absent_real_geometry_is_indeterminate(self) -> None:
        assessment = assess_vehicle_corridor(None, vehicle(), circuit_id="monaco_2026")
        self.assertEqual("indeterminate", assessment.status)
        self.assertIsNone(assessment.minimum_margin_m)

    def test_uncertainty_reduces_available_width_and_can_reject(self) -> None:
        assessment = assess_vehicle_corridor(
            corridor(
                segment(width_left_m=1.1, width_right_m=1.1),
                uncertainty=0.2,
            ),
            vehicle(),
        )
        self.assertEqual("rejected", assessment.status)
        self.assertAlmostEqual(-0.1, assessment.minimum_margin_m)

    def test_nonfinite_and_negative_inputs_are_rejected(self) -> None:
        with self.assertRaises(CorridorInputError):
            segment(length_m=-1.0)
        with self.assertRaises(CorridorInputError):
            segment(curvature_1pm=math.nan)
        with self.assertRaises(CorridorInputError):
            vehicle(max_steering_angle_rad=math.pi / 2.0)
        with self.assertRaises(CorridorInputError):
            evidence("invented_evidence_class")
        with self.assertRaises(CorridorInputError):
            evidence(uncertainty=-0.01)

    def test_duplicate_segment_ids_are_rejected(self) -> None:
        with self.assertRaises(CorridorInputError):
            corridor(segment(), replace(segment(), length_m=2.0))

    def test_mapping_requires_all_contract_fields(self) -> None:
        with self.assertRaisesRegex(CorridorInputError, "evidence"):
            corridor_from_mapping({"schema_version": "1.0", "segments": []})


if __name__ == "__main__":
    unittest.main()
