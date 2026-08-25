from __future__ import annotations

import math
import unittest

from formula_ultimate.physics.tyre import (
    TyreContactParameters,
    TyreForceRequest,
    TyreInputError,
    TyreNumericalError,
    resolve_tyre_force,
)


class TyreRoadForceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.circle = TyreContactParameters(
            friction_coefficient_longitudinal=1.0,
            friction_coefficient_lateral=1.0,
        )

    def resolve(
        self,
        fx_n: float,
        fy_n: float,
        *,
        normal_load_n: float = 4_000.0,
        parameters: TyreContactParameters | None = None,
    ):
        return resolve_tyre_force(
            parameters=parameters or self.circle,
            normal_load_n=normal_load_n,
            request=TyreForceRequest(fx_n, fy_n),
        )

    def test_inside_circle_request_passes_unchanged(self) -> None:
        result = self.resolve(1_200.0, -1_600.0)
        self.assertEqual("within_limit", result.status)
        self.assertFalse(result.saturated)
        self.assertEqual(1.0, result.saturation_scale)
        self.assertEqual(1_200.0, result.applied_longitudinal_force_n)
        self.assertEqual(-1_600.0, result.applied_lateral_force_n)
        self.assertAlmostEqual(0.5, result.requested_utilization)

    def test_diagonal_circle_request_is_radially_projected(self) -> None:
        result = self.resolve(3_000.0, 4_000.0)
        self.assertEqual("saturated", result.status)
        self.assertTrue(result.saturated)
        self.assertAlmostEqual(1.25, result.requested_utilization)
        self.assertAlmostEqual(0.8, result.saturation_scale)
        self.assertAlmostEqual(2_400.0, result.applied_longitudinal_force_n)
        self.assertAlmostEqual(3_200.0, result.applied_lateral_force_n)
        self.assertAlmostEqual(600.0, result.residual_longitudinal_force_n)
        self.assertAlmostEqual(800.0, result.residual_lateral_force_n)
        self.assertAlmostEqual(1.0, result.applied_utilization)

    def test_exact_anisotropic_ellipse_boundary_is_unchanged(self) -> None:
        parameters = TyreContactParameters(1.5, 1.0)
        fx_n = 3_000.0
        fy_n = 4_000.0 * math.sqrt(0.75)
        result = self.resolve(fx_n, fy_n, parameters=parameters)
        self.assertFalse(result.saturated)
        self.assertEqual(fx_n, result.applied_longitudinal_force_n)
        self.assertEqual(fy_n, result.applied_lateral_force_n)
        self.assertAlmostEqual(1.0, result.requested_utilization)

    def test_projection_preserves_force_direction_in_every_quadrant(self) -> None:
        for sx in (-1.0, 1.0):
            for sy in (-1.0, 1.0):
                with self.subTest(sx=sx, sy=sy):
                    result = self.resolve(sx * 3_000.0, sy * 4_000.0)
                    self.assertAlmostEqual(
                        sx * 2_400.0, result.applied_longitudinal_force_n
                    )
                    self.assertAlmostEqual(
                        sy * 3_200.0, result.applied_lateral_force_n
                    )

    def test_increasing_normal_load_does_not_increase_utilization(self) -> None:
        utilizations = [
            self.resolve(2_000.0, 1_000.0, normal_load_n=load).requested_utilization
            for load in (2_000.0, 4_000.0, 8_000.0)
        ]
        self.assertTrue(all(value is not None for value in utilizations))
        self.assertGreater(utilizations[0], utilizations[1])  # type: ignore[operator]
        self.assertGreater(utilizations[1], utilizations[2])  # type: ignore[operator]

    def test_zero_load_with_request_is_explicit_saturation_without_nan(self) -> None:
        result = self.resolve(100.0, -50.0, normal_load_n=0.0)
        self.assertEqual("no_normal_load", result.status)
        self.assertTrue(result.saturated)
        self.assertEqual(0.0, result.saturation_scale)
        self.assertIsNone(result.requested_utilization)
        self.assertEqual(0.0, result.applied_longitudinal_force_n)
        self.assertEqual(0.0, result.applied_lateral_force_n)
        self.assertEqual(100.0, result.residual_longitudinal_force_n)
        self.assertEqual(-50.0, result.residual_lateral_force_n)

    def test_zero_load_and_zero_request_is_distinct_no_contact_state(self) -> None:
        result = self.resolve(0.0, 0.0, normal_load_n=0.0)
        self.assertEqual("no_contact_zero_request", result.status)
        self.assertFalse(result.saturated)
        self.assertEqual(0.0, result.requested_utilization)
        self.assertEqual(0.0, result.applied_utilization)

    def test_boundary_tolerance_is_explicit(self) -> None:
        parameters = TyreContactParameters(1.0, 1.0, boundary_tolerance=1.0e-9)
        result = self.resolve(4_000.0 * (1.0 + 5.0e-10), 0.0, parameters=parameters)
        self.assertFalse(result.saturated)
        self.assertGreater(result.applied_utilization, 1.0)
        self.assertLessEqual(result.applied_utilization, 1.0 + 1.0e-9)

    def test_invalid_inputs_are_rejected(self) -> None:
        invalid_constructors = (
            lambda: TyreContactParameters(0.0, 1.0),
            lambda: TyreContactParameters(1.0, -1.0),
            lambda: TyreContactParameters(1.0, 1.0, boundary_tolerance=-1.0),
            lambda: TyreContactParameters(1.0, 1.0, boundary_tolerance=1.0e-5),
            lambda: TyreForceRequest(math.nan, 0.0),
            lambda: TyreForceRequest(0.0, math.inf),
            lambda: self.resolve(0.0, 0.0, normal_load_n=-1.0),
        )
        for constructor in invalid_constructors:
            with self.subTest(constructor=constructor):
                with self.assertRaises(TyreInputError):
                    constructor()

    def test_capacity_underflow_is_observable_numerical_failure(self) -> None:
        with self.assertRaises(TyreNumericalError):
            self.resolve(
                1.0,
                0.0,
                normal_load_n=1.0e-300,
                parameters=TyreContactParameters(1.0e-300, 1.0e-300),
            )

    def test_identical_inputs_replay_identically(self) -> None:
        request = TyreForceRequest(-5_000.0, 2_750.0)
        parameters = TyreContactParameters(1.2, 0.9)
        first = resolve_tyre_force(
            parameters=parameters, normal_load_n=3_500.0, request=request
        )
        second = resolve_tyre_force(
            parameters=parameters, normal_load_n=3_500.0, request=request
        )
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
