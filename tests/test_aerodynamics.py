from __future__ import annotations

from dataclasses import replace
import math
import unittest

from formula_ultimate.physics.aerodynamics import (
    AerodynamicCoefficientMap,
    AerodynamicCoefficientSample,
    AerodynamicEvidence,
    AerodynamicInputError,
    AerodynamicOperatingPoint,
    AerodynamicReference,
    AerodynamicStateGrid,
    evaluate_aerodynamics,
)


SPEEDS = (0.0, 20.0, 40.0)
HEIGHTS = (0.04, 0.08)
YAWS = (-0.1, 0.0, 0.1)


def coefficient_sample(active_state: str, height: float, yaw: float):
    is_open = active_state == "cooling_open"
    return AerodynamicCoefficientSample(
        drag_coefficient=(0.72 if is_open else 0.60)
        + 0.4 * abs(yaw)
        + 0.5 * (0.08 - height),
        side_force_coefficient=0.7 * yaw,
        downforce_coefficient=(1.10 if is_open else 1.20)
        + 1.5 * (0.08 - height)
        - 0.2 * abs(yaw),
        pitching_moment_coefficient=0.05 + 0.5 * (height - 0.06),
        yawing_moment_coefficient=0.2 * yaw,
        cooling_flow_coefficient=(0.80 if is_open else 0.40)
        - 0.3 * abs(yaw)
        + 0.2 * (height - 0.04),
    )


def state_grid(active_state: str) -> AerodynamicStateGrid:
    return AerodynamicStateGrid(
        active_state,
        tuple(
            coefficient_sample(active_state, height, yaw)
            for _speed in SPEEDS
            for height in HEIGHTS
            for yaw in YAWS
        ),
    )


def coefficient_map() -> AerodynamicCoefficientMap:
    return AerodynamicCoefficientMap(
        map_id="synthetic-reference-map",
        airspeeds_m_per_s=SPEEDS,
        ride_heights_m=HEIGHTS,
        yaw_angles_rad=YAWS,
        state_grids=(state_grid("nominal"), state_grid("cooling_open")),
        evidence=AerodynamicEvidence(
            "work017-synthetic",
            "synthetic_reference",
            "analytical unit-test fixture; not geometry-derived",
        ),
    )


REFERENCE = AerodynamicReference(
    reference_area_m2=1.5,
    reference_length_m=3.0,
    cooling_inlet_area_m2=0.08,
    air_specific_heat_j_per_kg_k=1_005.0,
    cooling_effectiveness=0.7,
)


def point(
    *,
    speed: float = 20.0,
    height: float = 0.04,
    yaw: float = 0.0,
    active_state: str = "nominal",
    density: float = 1.2,
    air_temperature: float = 300.0,
    component_temperature: float = 360.0,
) -> AerodynamicOperatingPoint:
    return AerodynamicOperatingPoint(
        speed,
        density,
        height,
        yaw,
        active_state,
        air_temperature,
        component_temperature,
    )


class AerodynamicMapTests(unittest.TestCase):
    def test_exact_grid_node_reproduces_sample_and_balances(self) -> None:
        result = evaluate_aerodynamics(
            coefficient_map=coefficient_map(),
            reference=REFERENCE,
            operating_point=point(speed=20.0, height=0.08, yaw=-0.1),
        )
        self.assertEqual("ok", result.status)
        self.assertTrue(result.interpolation.exact_grid_node)  # type: ignore[union-attr]
        self.assertEqual(
            coefficient_sample("nominal", 0.08, -0.1),
            result.coefficients,
        )
        self.assertIsNotNone(result.residuals)
        for value in (
            result.residuals.drag_force_n,  # type: ignore[union-attr]
            result.residuals.side_force_n,  # type: ignore[union-attr]
            result.residuals.downforce_n,  # type: ignore[union-attr]
            result.residuals.pitching_moment_n_m,  # type: ignore[union-attr]
            result.residuals.yawing_moment_n_m,  # type: ignore[union-attr]
            result.residuals.cooling_mass_flow_kg_per_s,  # type: ignore[union-attr]
            result.residuals.cooling_conductance_w_per_k,  # type: ignore[union-attr]
            result.residuals.heat_rejection_w,  # type: ignore[union-attr]
        ):
            self.assertEqual(0.0, value)

    def test_tensor_interpolation_matches_piecewise_linear_reference(self) -> None:
        operating_point = point(speed=30.0, height=0.06, yaw=0.05)
        result = evaluate_aerodynamics(
            coefficient_map=coefficient_map(),
            reference=REFERENCE,
            operating_point=operating_point,
        )
        self.assertEqual("ok", result.status)
        self.assertFalse(result.interpolation.exact_grid_node)  # type: ignore[union-attr]
        expected = coefficient_sample("nominal", 0.06, 0.05)
        self.assertAlmostEqual(expected.drag_coefficient, result.coefficients.drag_coefficient)  # type: ignore[union-attr]
        self.assertAlmostEqual(expected.side_force_coefficient, result.coefficients.side_force_coefficient)  # type: ignore[union-attr]
        self.assertAlmostEqual(expected.downforce_coefficient, result.coefficients.downforce_coefficient)  # type: ignore[union-attr]
        self.assertAlmostEqual(expected.pitching_moment_coefficient, result.coefficients.pitching_moment_coefficient)  # type: ignore[union-attr]
        self.assertAlmostEqual(expected.yawing_moment_coefficient, result.coefficients.yawing_moment_coefficient)  # type: ignore[union-attr]
        self.assertAlmostEqual(expected.cooling_flow_coefficient, result.coefficients.cooling_flow_coefficient)  # type: ignore[union-attr]
        self.assertAlmostEqual(0.5, result.interpolation.airspeed.fraction)  # type: ignore[union-attr]
        self.assertAlmostEqual(0.5, result.interpolation.ride_height.fraction)  # type: ignore[union-attr]
        self.assertAlmostEqual(0.5, result.interpolation.yaw_angle.fraction)  # type: ignore[union-attr]

    def test_force_scales_with_speed_squared_and_mass_flow_with_speed(self) -> None:
        map_ = coefficient_map()
        low = evaluate_aerodynamics(
            coefficient_map=map_, reference=REFERENCE, operating_point=point(speed=20.0)
        )
        high = evaluate_aerodynamics(
            coefficient_map=map_, reference=REFERENCE, operating_point=point(speed=40.0)
        )
        self.assertAlmostEqual(4.0, high.drag_force_n / low.drag_force_n)  # type: ignore[operator]
        self.assertAlmostEqual(4.0, high.downforce_n / low.downforce_n)  # type: ignore[operator]
        self.assertAlmostEqual(4.0, high.pitching_moment_n_m / low.pitching_moment_n_m)  # type: ignore[operator]
        self.assertAlmostEqual(
            2.0,
            high.cooling_air_mass_flow_kg_per_s / low.cooling_air_mass_flow_kg_per_s,  # type: ignore[operator]
        )

    def test_reference_yaw_symmetry_and_antisymmetry_are_observable(self) -> None:
        map_ = coefficient_map()
        negative = evaluate_aerodynamics(
            coefficient_map=map_, reference=REFERENCE, operating_point=point(yaw=-0.1)
        )
        positive = evaluate_aerodynamics(
            coefficient_map=map_, reference=REFERENCE, operating_point=point(yaw=0.1)
        )
        self.assertEqual(negative.drag_force_n, positive.drag_force_n)
        self.assertEqual(negative.downforce_n, positive.downforce_n)
        self.assertAlmostEqual(-negative.side_force_n, positive.side_force_n)  # type: ignore[arg-type]
        self.assertAlmostEqual(-negative.yawing_moment_n_m, positive.yawing_moment_n_m)  # type: ignore[arg-type]

    def test_active_cooling_state_exposes_drag_and_flow_tradeoff(self) -> None:
        map_ = coefficient_map()
        nominal = evaluate_aerodynamics(
            coefficient_map=map_, reference=REFERENCE, operating_point=point()
        )
        cooling = evaluate_aerodynamics(
            coefficient_map=map_,
            reference=REFERENCE,
            operating_point=point(active_state="cooling_open"),
        )
        self.assertGreater(cooling.drag_force_n, nominal.drag_force_n)  # type: ignore[arg-type]
        self.assertGreater(
            cooling.cooling_air_mass_flow_kg_per_s,
            nominal.cooling_air_mass_flow_kg_per_s,  # type: ignore[arg-type]
        )
        self.assertGreater(
            cooling.cooling_heat_rejection_w,
            nominal.cooling_heat_rejection_w,  # type: ignore[arg-type]
        )

    def test_zero_speed_has_zero_force_and_ram_flow(self) -> None:
        result = evaluate_aerodynamics(
            coefficient_map=coefficient_map(),
            reference=REFERENCE,
            operating_point=point(speed=0.0),
        )
        self.assertEqual("ok", result.status)
        self.assertEqual(0.0, result.dynamic_pressure_pa)
        self.assertEqual(0.0, result.drag_force_n)
        self.assertEqual(0.0, result.side_force_n)
        self.assertEqual(0.0, result.downforce_n)
        self.assertEqual(0.0, result.cooling_air_mass_flow_kg_per_s)
        self.assertEqual(0.0, result.cooling_heat_rejection_w)
        self.assertIsNone(result.longitudinal_centre_of_pressure_m)

    def test_cooling_heat_flow_is_signed(self) -> None:
        hot = evaluate_aerodynamics(
            coefficient_map=coefficient_map(),
            reference=REFERENCE,
            operating_point=point(component_temperature=360.0),
        )
        cold = evaluate_aerodynamics(
            coefficient_map=coefficient_map(),
            reference=REFERENCE,
            operating_point=point(component_temperature=280.0),
        )
        self.assertGreater(hot.cooling_heat_rejection_w, 0.0)  # type: ignore[arg-type]
        self.assertLess(cold.cooling_heat_rejection_w, 0.0)  # type: ignore[arg-type]

    def test_outside_each_axis_and_unknown_state_are_invalid_without_clamp(self) -> None:
        cases = (
            point(speed=41.0),
            point(height=0.039),
            point(yaw=0.11),
            point(active_state="missing"),
        )
        for operating_point in cases:
            with self.subTest(operating_point=operating_point):
                result = evaluate_aerodynamics(
                    coefficient_map=coefficient_map(),
                    reference=REFERENCE,
                    operating_point=operating_point,
                )
                self.assertEqual("invalid", result.status)
                self.assertIsNone(result.coefficients)
                self.assertIsNone(result.dynamic_pressure_pa)

    def test_evidence_contract_distinguishes_geometry_derived_map(self) -> None:
        digest = "a" * 64
        evidence = AerodynamicEvidence(
            "geometry-map", "geometry_derived", "verified STEP digest", digest
        )
        map_ = replace(coefficient_map(), evidence=evidence)
        result = evaluate_aerodynamics(
            coefficient_map=map_, reference=REFERENCE, operating_point=point()
        )
        self.assertEqual("ok", result.status)
        self.assertEqual("geometry_derived", result.evidence.basis)
        self.assertEqual(digest, result.evidence.geometry_sha256)
        with self.assertRaises(AerodynamicInputError):
            AerodynamicEvidence("bad", "geometry_derived", "missing digest")

    def test_malformed_grid_and_declared_inputs_are_rejected(self) -> None:
        map_ = coefficient_map()
        invalid = (
            lambda: replace(map_, airspeeds_m_per_s=(0.0, 20.0, 20.0)),
            lambda: replace(map_, yaw_angles_rad=(0.1, 0.0)),
            lambda: replace(
                map_,
                state_grids=(
                    AerodynamicStateGrid("nominal", map_.state_grids[0].samples[:-1]),
                ),
            ),
            lambda: replace(
                map_, state_grids=(map_.state_grids[0], map_.state_grids[0])
            ),
            lambda: AerodynamicCoefficientSample(-0.1, 0.0, 0.0, 0.0, 0.0, 0.0),
            lambda: AerodynamicReference(0.0, 1.0, 0.0, 1_005.0, 0.5),
            lambda: point(density=math.inf),
        )
        for constructor in invalid:
            with self.subTest(constructor=constructor):
                with self.assertRaises(AerodynamicInputError):
                    constructor()

    def test_non_finite_runtime_and_replay_are_observable(self) -> None:
        map_ = coefficient_map()
        operating_point = point(speed=40.0, density=1.0e308)
        invalid = evaluate_aerodynamics(
            coefficient_map=map_, reference=REFERENCE, operating_point=operating_point
        )
        self.assertEqual("invalid", invalid.status)
        self.assertIn("non-finite", invalid.reason)

        ordinary = point(speed=30.0, height=0.06, yaw=-0.05)
        first = evaluate_aerodynamics(
            coefficient_map=map_, reference=REFERENCE, operating_point=ordinary
        )
        second = evaluate_aerodynamics(
            coefficient_map=map_, reference=REFERENCE, operating_point=ordinary
        )
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
