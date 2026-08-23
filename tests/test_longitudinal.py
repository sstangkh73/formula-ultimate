from __future__ import annotations

import math
import unittest

from formula_ultimate.physics.longitudinal import (
    EnvironmentParameters,
    PhysicsInputError,
    SimulationConfig,
    VehicleParameters,
    aerodynamic_drag_force_n,
    simulate_constant_traction,
)


class LongitudinalReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.lossless_vehicle = VehicleParameters(mass_kg=1_000.0)
        self.environment = EnvironmentParameters()

    def test_zero_input_at_rest_remains_at_rest(self) -> None:
        result = simulate_constant_traction(
            vehicle=self.lossless_vehicle,
            environment=self.environment,
            config=SimulationConfig(duration_s=5.0, time_step_s=0.3),
            tractive_force_n=0.0,
        )

        self.assertEqual(0.0, result.final_state.position_m)
        self.assertEqual(0.0, result.final_state.speed_mps)
        self.assertEqual(5.0, result.final_state.time_s)
        self.assertTrue(
            all(
                sample.unconstrained_net_force_n == 0.0
                for sample in result.telemetry
            )
        )

    def test_constant_force_matches_closed_form_solution(self) -> None:
        duration_s = 5.0
        acceleration_mps2 = 2.0
        result = simulate_constant_traction(
            vehicle=self.lossless_vehicle,
            environment=self.environment,
            config=SimulationConfig(duration_s=duration_s, time_step_s=0.3),
            tractive_force_n=self.lossless_vehicle.mass_kg * acceleration_mps2,
        )

        self.assertAlmostEqual(
            acceleration_mps2 * duration_s,
            result.final_state.speed_mps,
            places=12,
        )
        self.assertAlmostEqual(
            0.5 * acceleration_mps2 * duration_s**2,
            result.final_state.position_m,
            places=12,
        )
        self.assertEqual(duration_s, result.final_state.time_s)
        self.assertAlmostEqual(0.2, result.telemetry[-1].time_step_s, places=12)

    def test_drag_only_coastdown_converges_toward_closed_form_solution(self) -> None:
        vehicle = VehicleParameters(mass_kg=1_000.0, drag_area_m2=0.8)
        initial_speed_mps = 30.0
        duration_s = 10.0
        drag_constant = (
            0.5
            * self.environment.air_density_kg_per_m3
            * vehicle.drag_area_m2
            / vehicle.mass_kg
        )
        analytical_speed_mps = initial_speed_mps / (
            1.0 + drag_constant * initial_speed_mps * duration_s
        )

        coarse = simulate_constant_traction(
            vehicle=vehicle,
            environment=self.environment,
            config=SimulationConfig(duration_s=duration_s, time_step_s=0.5),
            tractive_force_n=0.0,
            initial_speed_mps=initial_speed_mps,
        )
        fine = simulate_constant_traction(
            vehicle=vehicle,
            environment=self.environment,
            config=SimulationConfig(duration_s=duration_s, time_step_s=0.05),
            tractive_force_n=0.0,
            initial_speed_mps=initial_speed_mps,
        )

        coarse_error = abs(coarse.final_state.speed_mps - analytical_speed_mps)
        fine_error = abs(fine.final_state.speed_mps - analytical_speed_mps)
        self.assertLess(fine_error, coarse_error)
        self.assertLess(fine_error, 0.01)

    def test_grade_equilibrium_maintains_speed(self) -> None:
        grade_radians = 0.08
        environment = EnvironmentParameters(grade_radians=grade_radians)
        equilibrium_force_n = (
            self.lossless_vehicle.mass_kg
            * environment.gravity_mps2
            * math.sin(grade_radians)
        )
        result = simulate_constant_traction(
            vehicle=self.lossless_vehicle,
            environment=environment,
            config=SimulationConfig(duration_s=8.0, time_step_s=0.1),
            tractive_force_n=equilibrium_force_n,
            initial_speed_mps=12.0,
        )

        self.assertAlmostEqual(12.0, result.final_state.speed_mps, places=12)
        self.assertAlmostEqual(96.0, result.final_state.position_m, places=10)

    def test_rolling_resistance_matches_constant_deceleration(self) -> None:
        coefficient = 0.01
        vehicle = VehicleParameters(
            mass_kg=1_000.0,
            rolling_resistance_coefficient=coefficient,
        )
        duration_s = 1.0
        initial_speed_mps = 10.0
        expected_deceleration_mps2 = coefficient * self.environment.gravity_mps2
        result = simulate_constant_traction(
            vehicle=vehicle,
            environment=self.environment,
            config=SimulationConfig(duration_s=duration_s, time_step_s=0.1),
            tractive_force_n=0.0,
            initial_speed_mps=initial_speed_mps,
        )

        self.assertAlmostEqual(
            initial_speed_mps - expected_deceleration_mps2 * duration_s,
            result.final_state.speed_mps,
            places=12,
        )
        self.assertAlmostEqual(
            initial_speed_mps * duration_s
            - 0.5 * expected_deceleration_mps2 * duration_s**2,
            result.final_state.position_m,
            places=12,
        )

    def test_underpowered_uphill_case_stops_without_reversing(self) -> None:
        result = simulate_constant_traction(
            vehicle=self.lossless_vehicle,
            environment=EnvironmentParameters(grade_radians=0.2),
            config=SimulationConfig(duration_s=3.0, time_step_s=1.0),
            tractive_force_n=0.0,
            initial_speed_mps=1.0,
        )

        positions = [state.position_m for state in result.states]
        self.assertEqual(0.0, result.final_state.speed_mps)
        self.assertTrue(all(position >= 0.0 for position in positions))
        self.assertEqual(sorted(positions), positions)
        self.assertTrue(result.telemetry[0].stopped_within_step)
        self.assertGreater(
            result.telemetry[0].zero_speed_constraint_impulse_ns,
            0.0,
        )

    def test_identical_inputs_replay_identically(self) -> None:
        kwargs = {
            "vehicle": VehicleParameters(
                mass_kg=850.0,
                drag_area_m2=0.7,
                rolling_resistance_coefficient=0.012,
            ),
            "environment": EnvironmentParameters(grade_radians=-0.01),
            "config": SimulationConfig(duration_s=4.3, time_step_s=0.07),
            "tractive_force_n": 1_900.0,
            "initial_speed_mps": 3.0,
        }

        first = simulate_constant_traction(**kwargs)
        second = simulate_constant_traction(**kwargs)
        self.assertEqual(first, second)

    def test_invalid_inputs_are_rejected(self) -> None:
        invalid_constructors = (
            lambda: VehicleParameters(mass_kg=0.0),
            lambda: VehicleParameters(mass_kg=1.0, drag_area_m2=-1.0),
            lambda: EnvironmentParameters(air_density_kg_per_m3=-1.0),
            lambda: EnvironmentParameters(grade_radians=math.pi / 2.0),
            lambda: SimulationConfig(duration_s=-1.0, time_step_s=0.1),
            lambda: SimulationConfig(duration_s=1.0, time_step_s=0.0),
            lambda: aerodynamic_drag_force_n(
                speed_mps=math.inf,
                air_density_kg_per_m3=1.225,
                drag_area_m2=1.0,
            ),
        )
        for constructor in invalid_constructors:
            with self.subTest(constructor=constructor):
                with self.assertRaises(PhysicsInputError):
                    constructor()

        with self.assertRaises(PhysicsInputError):
            simulate_constant_traction(
                vehicle=self.lossless_vehicle,
                environment=self.environment,
                config=SimulationConfig(duration_s=1.0, time_step_s=0.1),
                tractive_force_n=-1.0,
            )


if __name__ == "__main__":
    unittest.main()
