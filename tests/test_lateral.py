from __future__ import annotations

from dataclasses import astuple, replace
import math
import unittest

from formula_ultimate.physics.lateral import (
    LateralInputError,
    PlanarContact,
    PlanarSolverControl,
    PlanarState,
    PlanarVehicle,
    PlanarVehicleParameters,
    solve_quasi_static_normal_loads,
    step_planar_dynamics,
)
from formula_ultimate.physics.tyre import TyreContactParameters


TYRE = TyreContactParameters(1.2, 1.1)


def contact(
    contact_id: str,
    x_m: float,
    y_m: float,
    load_n: float,
    *,
    steer_rad: float = 0.0,
    stiffness: float = 20_000.0,
    fx_n: float = 0.0,
) -> PlanarContact:
    return PlanarContact(
        contact_id=contact_id,
        x_position_m=x_m,
        y_position_m=y_m,
        baseline_normal_load_n=load_n,
        steer_angle_rad=steer_rad,
        cornering_stiffness_n_per_rad=stiffness,
        requested_longitudinal_force_n=fx_n,
        tyre_parameters=TYRE,
    )


def four_contact_vehicle(
    *,
    front_steer_rad: float = 0.0,
    fx_n: float = 0.0,
    height_m: float = 0.5,
) -> PlanarVehicle:
    mass = 1_200.0
    load = mass * 9.81 / 4.0
    contacts = (
        contact("front-left", 1.5, 0.8, load, steer_rad=front_steer_rad, fx_n=fx_n),
        contact("front-right", 1.5, -0.8, load, steer_rad=front_steer_rad, fx_n=fx_n),
        contact("rear-left", -1.5, 0.8, load, fx_n=fx_n),
        contact("rear-right", -1.5, -0.8, load, fx_n=fx_n),
    )
    return PlanarVehicle(
        vehicle_id="reference-four-contact",
        parameters=PlanarVehicleParameters(mass, 1_800.0, height_m),
        contacts=contacts,
    )


def state(*, u: float = 20.0, v: float = 0.0, yaw_rate: float = 0.0) -> PlanarState:
    return PlanarState(0.0, 0.0, 0.0, 0.0, u, v, yaw_rate)


class LateralYawLoadTransferTests(unittest.TestCase):
    def test_steady_straight_equilibrium_converges_and_balances(self) -> None:
        result = step_planar_dynamics(
            vehicle=four_contact_vehicle(),
            state=state(u=30.0),
            control=PlanarSolverControl(time_step_s=0.1),
        )
        self.assertEqual("ok", result.status)
        self.assertTrue(result.converged)
        self.assertEqual(1, result.load_iterations)
        self.assertEqual(0.0, result.longitudinal_acceleration_m_per_s2)
        self.assertEqual(0.0, result.lateral_acceleration_m_per_s2)
        self.assertEqual(0.0, result.yaw_acceleration_rad_per_s2)
        self.assertEqual(3.0, result.end_state.x_position_m)
        self.assertEqual(30.0, result.end_state.longitudinal_velocity_m_per_s)
        self.assertIsNotNone(result.residuals)
        for residual in astuple(result.residuals):  # type: ignore[arg-type]
            self.assertAlmostEqual(0.0, residual, places=9)

    def test_positive_front_steer_produces_positive_lateral_and_yaw_response(self) -> None:
        result = step_planar_dynamics(
            vehicle=four_contact_vehicle(front_steer_rad=0.02),
            state=state(),
            control=PlanarSolverControl(time_step_s=0.01),
        )
        self.assertEqual("ok", result.status)
        self.assertGreater(result.lateral_acceleration_m_per_s2, 0.0)  # type: ignore[arg-type]
        self.assertGreater(result.yaw_acceleration_rad_per_s2, 0.0)  # type: ignore[arg-type]
        self.assertGreater(result.end_state.lateral_velocity_m_per_s, 0.0)
        self.assertGreater(result.end_state.yaw_rate_rad_per_s, 0.0)
        front = result.contact_results[:2]
        self.assertTrue(all(item.slip_angle_rad < 0.0 for item in front))
        self.assertTrue(
            all(item.tyre_force.requested_lateral_force_n > 0.0 for item in front)
        )

    def test_longitudinal_and_lateral_load_transfer_have_expected_direction(self) -> None:
        vehicle = four_contact_vehicle()
        solution = solve_quasi_static_normal_loads(
            vehicle=vehicle,
            longitudinal_acceleration_m_per_s2=2.0,
            lateral_acceleration_m_per_s2=3.0,
        )
        self.assertEqual("ok", solution.status)
        front = sum(solution.normal_loads_n[:2])
        rear = sum(solution.normal_loads_n[2:])
        left = solution.normal_loads_n[0] + solution.normal_loads_n[2]
        right = solution.normal_loads_n[1] + solution.normal_loads_n[3]
        self.assertGreater(rear, front)
        self.assertGreater(right, left)
        self.assertIsNotNone(solution.residuals)
        self.assertAlmostEqual(0.0, solution.residuals.vertical_force_n, places=9)  # type: ignore[union-attr]
        self.assertAlmostEqual(0.0, solution.residuals.pitch_moment_n_m, places=9)  # type: ignore[union-attr]
        self.assertAlmostEqual(0.0, solution.residuals.roll_moment_n_m, places=9)  # type: ignore[union-attr]

    def test_non_conventional_three_contact_layout_is_supported(self) -> None:
        mass = 900.0
        weight = mass * 9.81
        vehicle = PlanarVehicle(
            vehicle_id="three-contact-delta",
            parameters=PlanarVehicleParameters(mass, 1_100.0, 0.35),
            contacts=(
                contact("forward", 1.2, 0.0, 0.4 * weight),
                contact("rear-left", -0.8, 0.7, 0.3 * weight),
                contact("rear-right", -0.8, -0.7, 0.3 * weight),
            ),
        )
        result = step_planar_dynamics(
            vehicle=vehicle,
            state=state(u=15.0),
            control=PlanarSolverControl(time_step_s=0.02),
        )
        self.assertEqual("ok", result.status)
        self.assertEqual(3, len(result.contact_results))

    def test_combined_force_is_saturated_per_contact(self) -> None:
        result = step_planar_dynamics(
            vehicle=four_contact_vehicle(front_steer_rad=0.2, fx_n=5_000.0),
            state=state(u=25.0),
            control=PlanarSolverControl(
                time_step_s=0.01,
                max_load_iterations=256,
                relaxation_factor=0.25,
            ),
        )
        self.assertEqual("ok", result.status)
        self.assertGreater(result.saturated_contact_count, 0)
        for item in result.contact_results:
            self.assertLessEqual(item.tyre_force.applied_utilization, 1.0 + 1.0e-12)  # type: ignore[operator]
            if item.tyre_force.saturated:
                self.assertLess(item.tyre_force.saturation_scale, 1.0)

    def test_identical_inputs_replay_identically(self) -> None:
        vehicle = four_contact_vehicle(front_steer_rad=0.015, fx_n=200.0)
        initial = state(u=22.0, v=0.1, yaw_rate=0.02)
        control = PlanarSolverControl(time_step_s=0.005)
        first = step_planar_dynamics(vehicle=vehicle, state=initial, control=control)
        second = step_planar_dynamics(vehicle=vehicle, state=initial, control=control)
        self.assertEqual(first, second)

    def test_rank_deficient_contact_geometry_is_observable_invalid(self) -> None:
        mass = 1_000.0
        load = mass * 9.81 / 2.0
        vehicle = PlanarVehicle(
            vehicle_id="collinear",
            parameters=PlanarVehicleParameters(mass, 1_000.0, 0.4),
            contacts=(
                contact("front", 1.0, 0.0, load),
                contact("rear", -1.0, 0.0, load),
            ),
        )
        result = step_planar_dynamics(
            vehicle=vehicle,
            state=state(),
            control=PlanarSolverControl(time_step_s=0.01),
        )
        self.assertEqual("invalid", result.status)
        self.assertIn("rank-deficient", result.reason)
        self.assertEqual(state(), result.end_state)

    def test_contact_lift_is_rejected_without_clipping(self) -> None:
        solution = solve_quasi_static_normal_loads(
            vehicle=four_contact_vehicle(height_m=1.0),
            longitudinal_acceleration_m_per_s2=30.0,
            lateral_acceleration_m_per_s2=0.0,
        )
        self.assertEqual("invalid", solution.status)
        self.assertIn("contact lift", solution.reason)
        self.assertTrue(any(load < 0.0 for load in solution.normal_loads_n))

    def test_insufficient_iteration_budget_is_observable_non_convergence(self) -> None:
        result = step_planar_dynamics(
            vehicle=four_contact_vehicle(front_steer_rad=0.03),
            state=state(),
            control=PlanarSolverControl(time_step_s=0.01, max_load_iterations=1),
        )
        self.assertEqual("invalid", result.status)
        self.assertIn("did not converge", result.reason)
        self.assertEqual(1, result.load_iterations)
        self.assertFalse(result.converged)

    def test_dynamic_force_and_moment_balances_close(self) -> None:
        result = step_planar_dynamics(
            vehicle=four_contact_vehicle(front_steer_rad=-0.025, fx_n=-150.0),
            state=state(u=18.0, v=-0.2, yaw_rate=-0.03),
            control=PlanarSolverControl(time_step_s=0.01),
        )
        self.assertEqual("ok", result.status)
        self.assertIsNotNone(result.residuals)
        self.assertLess(abs(result.residuals.longitudinal_force_n), 1.0e-9)  # type: ignore[union-attr]
        self.assertLess(abs(result.residuals.lateral_force_n), 1.0e-9)  # type: ignore[union-attr]
        self.assertLess(abs(result.residuals.yaw_moment_n_m), 1.0e-9)  # type: ignore[union-attr]

    def test_invalid_declared_inputs_are_rejected(self) -> None:
        vehicle = four_contact_vehicle()
        invalid = (
            lambda: PlanarVehicleParameters(0.0, 1.0, 0.0),
            lambda: PlanarContact("", 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, TYRE),
            lambda: PlanarState(0.0, 0.0, 0.0, 0.0, math.nan, 0.0, 0.0),
            lambda: PlanarSolverControl(time_step_s=0.0),
            lambda: replace(vehicle, contacts=(vehicle.contacts[0], vehicle.contacts[0])),
            lambda: replace(
                vehicle,
                contacts=(
                    replace(
                        vehicle.contacts[0],
                        baseline_normal_load_n=vehicle.contacts[0].baseline_normal_load_n + 1.0,
                    ),
                    *vehicle.contacts[1:],
                ),
            ),
        )
        for constructor in invalid:
            with self.subTest(constructor=constructor):
                with self.assertRaises(LateralInputError):
                    constructor()


if __name__ == "__main__":
    unittest.main()
