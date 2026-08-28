from __future__ import annotations

from dataclasses import replace
import math
import unittest

from formula_ultimate.physics.suspension_braking import (
    BrakeParameters,
    RegenerationParameters,
    SuspensionBrakeInputError,
    SuspensionBrakeModule,
    SuspensionBrakeState,
    SuspensionBrakeStepInput,
    SuspensionParameters,
    evaluate_suspension_brake_step,
)
from formula_ultimate.physics.thermal import ThermalParameters


def module(
    *,
    regeneration: RegenerationParameters | None = None,
    thermal: ThermalParameters | None = None,
    suspension: SuspensionParameters | None = None,
    maximum_mechanical_torque_n_m: float = 200.0,
) -> SuspensionBrakeModule:
    return SuspensionBrakeModule(
        module_id="contact-alpha",
        suspension=suspension
        or SuspensionParameters(100.0, 10_000.0, 0.0, 1_000.0, 0.1, 0.1),
        brake=BrakeParameters(
            effective_radius_m=0.3,
            tyre_friction_coefficient=1.0,
            maximum_mechanical_torque_n_m=maximum_mechanical_torque_n_m,
            thermal_parameters=thermal
            or ThermalParameters(1_000.0, 0.0, 0.0, 370.0, 400.0),
        ),
        regeneration=regeneration
        or RegenerationParameters(100.0, 2_000.0, 1_600.0, 10_000.0, 0.8, 1.0),
    )


def state(
    *,
    travel: float = 0.0,
    velocity: float = 0.0,
    temperature: float = 300.0,
    stored: float = 0.0,
    suspension_failed: bool = False,
    brake_failed: bool = False,
) -> SuspensionBrakeState:
    return SuspensionBrakeState(
        0.0,
        travel,
        velocity,
        temperature,
        stored,
        suspension_failed,
        brake_failed,
    )


def step_input(
    *,
    duration: float = 1.0,
    normal_load: float = 1_000.0,
    omega: float = 10.0,
    torque: float = 0.0,
) -> SuspensionBrakeStepInput:
    return SuspensionBrakeStepInput(duration, normal_load, omega, torque, 300.0)


class SuspensionBrakingTests(unittest.TestCase):
    def test_static_suspension_equilibrium_closes_force_balance(self) -> None:
        result = evaluate_suspension_brake_step(
            module=module(), state=state(), step_input=step_input()
        )
        self.assertEqual("ok", result.status)
        self.assertEqual("none", result.failure_mode)
        self.assertEqual(1_000.0, result.suspension_force_n)
        self.assertEqual(0.0, result.suspension_acceleration_m_per_s2)
        self.assertEqual(0.0, result.end_state.suspension_travel_m)
        self.assertEqual(0.0, result.residuals.suspension_force_n)  # type: ignore[union-attr]

    def test_constant_acceleration_suspension_step_matches_analytical_motion(self) -> None:
        result = evaluate_suspension_brake_step(
            module=module(),
            state=state(),
            step_input=step_input(duration=0.1, normal_load=1_200.0),
        )
        self.assertEqual("ok", result.status)
        self.assertEqual(2.0, result.suspension_acceleration_m_per_s2)
        self.assertAlmostEqual(0.01, result.end_state.suspension_travel_m)
        self.assertAlmostEqual(0.2, result.end_state.suspension_velocity_m_per_s)

    def test_suspension_travel_failure_is_localized_without_clipping(self) -> None:
        result = evaluate_suspension_brake_step(
            module=module(),
            state=state(velocity=0.02),
            step_input=step_input(duration=10.0),
        )
        self.assertEqual("failed", result.status)
        self.assertEqual("suspension_travel", result.failure_mode)
        self.assertAlmostEqual(5.0, result.executed_duration_s)
        self.assertAlmostEqual(5.0, result.unexecuted_duration_s)
        self.assertAlmostEqual(0.1, result.end_state.suspension_travel_m)
        self.assertTrue(result.end_state.suspension_failed)
        self.assertFalse(result.end_state.brake_failed)

    def test_regen_first_then_mechanical_energy_closes(self) -> None:
        result = evaluate_suspension_brake_step(
            module=module(),
            state=state(),
            step_input=step_input(torque=150.0),
        )
        self.assertEqual("ok", result.status)
        self.assertEqual(100.0, result.applied_regen_torque_n_m)
        self.assertEqual(50.0, result.applied_mechanical_torque_n_m)
        self.assertEqual(1_500.0, result.wheel_energy_removed_j)
        self.assertEqual(1_000.0, result.regenerative_wheel_energy_j)
        self.assertEqual(800.0, result.recovered_storage_energy_j)
        self.assertEqual(200.0, result.regenerative_conversion_loss_j)
        self.assertEqual(500.0, result.mechanical_brake_heat_j)
        self.assertEqual(800.0, result.end_state.stored_recovered_energy_j)
        self.assertEqual(0.0, result.residuals.brake_energy_j)  # type: ignore[union-attr]
        self.assertEqual(0.0, result.residuals.brake_torque_n_m)  # type: ignore[union-attr]

    def test_regen_torque_power_charge_and_storage_limits_are_observable(self) -> None:
        base = module()
        cases = (
            (base.regeneration, state(), 100.0),
            (replace(base.regeneration, maximum_generator_input_power_w=500.0), state(), 50.0),
            (replace(base.regeneration, maximum_storage_charge_power_w=320.0), state(), 40.0),
            (base.regeneration, state(stored=9_968.0), 4.0),
        )
        for regeneration, initial_state, expected in cases:
            with self.subTest(regeneration=regeneration, state=initial_state):
                result = evaluate_suspension_brake_step(
                    module=replace(base, regeneration=regeneration),
                    state=initial_state,
                    step_input=step_input(torque=150.0),
                )
                self.assertEqual("ok", result.status)
                self.assertAlmostEqual(expected, result.available_regen_torque_n_m)
                self.assertAlmostEqual(expected, result.applied_regen_torque_n_m)
                self.assertLessEqual(
                    result.end_state.stored_recovered_energy_j,
                    regeneration.storage_capacity_j,
                )

    def test_zero_speed_disables_regen_and_removes_no_wheel_energy(self) -> None:
        result = evaluate_suspension_brake_step(
            module=module(),
            state=state(),
            step_input=step_input(omega=0.0, torque=150.0),
        )
        self.assertEqual("ok", result.status)
        self.assertEqual(0.0, result.available_regen_torque_n_m)
        self.assertEqual(0.0, result.applied_regen_torque_n_m)
        self.assertEqual(150.0, result.applied_mechanical_torque_n_m)
        self.assertEqual(0.0, result.wheel_energy_removed_j)
        self.assertEqual(0.0, result.mechanical_brake_heat_j)

    def test_tyre_limit_scales_blend_and_preserves_unserved_torque(self) -> None:
        tyre_limit_suspension = SuspensionParameters(
            100.0, 10_000.0, 0.0, 100.0, 0.1, 0.1
        )
        result = evaluate_suspension_brake_step(
            module=module(suspension=tyre_limit_suspension),
            state=state(),
            step_input=step_input(normal_load=100.0, torque=150.0),
        )
        self.assertEqual("ok", result.status)
        self.assertAlmostEqual(30.0, result.tyre_torque_limit_n_m)
        self.assertAlmostEqual(0.2, result.tyre_limit_scale)
        self.assertAlmostEqual(20.0, result.applied_regen_torque_n_m)
        self.assertAlmostEqual(10.0, result.applied_mechanical_torque_n_m)
        self.assertAlmostEqual(120.0, result.unserved_brake_torque_n_m)

    def test_thermal_failure_localizes_and_truncates_brake_energy(self) -> None:
        no_regen = RegenerationParameters(0.0, 0.0, 0.0, 10_000.0, 0.8)
        result = evaluate_suspension_brake_step(
            module=module(regeneration=no_regen),
            state=state(temperature=350.0),
            step_input=step_input(duration=100.0, torque=100.0),
        )
        self.assertEqual("failed", result.status)
        self.assertEqual("brake_overtemperature", result.failure_mode)
        self.assertEqual(50.0, result.executed_duration_s)
        self.assertEqual(50.0, result.unexecuted_duration_s)
        self.assertEqual(400.0, result.end_state.brake_temperature_k)
        self.assertTrue(result.end_state.brake_failed)
        self.assertEqual(50_000.0, result.mechanical_brake_heat_j)
        self.assertEqual(50_000.0, result.wheel_energy_removed_j)
        self.assertEqual(0.0, result.residuals.brake_energy_j)  # type: ignore[union-attr]

    def test_exact_travel_and_thermal_tie_is_simultaneous(self) -> None:
        no_regen = RegenerationParameters(0.0, 0.0, 0.0, 10_000.0, 0.8)
        result = evaluate_suspension_brake_step(
            module=module(regeneration=no_regen),
            state=state(velocity=0.002, temperature=350.0),
            step_input=step_input(duration=100.0, torque=100.0),
        )
        self.assertEqual("failed", result.status)
        self.assertEqual("simultaneous", result.failure_mode)
        self.assertEqual(50.0, result.executed_duration_s)
        self.assertAlmostEqual(0.1, result.end_state.suspension_travel_m)
        self.assertEqual(400.0, result.end_state.brake_temperature_k)
        self.assertTrue(result.end_state.suspension_failed)
        self.assertTrue(result.end_state.brake_failed)

    def test_thermal_derating_limits_mechanical_torque(self) -> None:
        no_regen = RegenerationParameters(0.0, 0.0, 0.0, 10_000.0, 0.8)
        result = evaluate_suspension_brake_step(
            module=module(regeneration=no_regen),
            state=state(temperature=385.0),
            step_input=step_input(torque=200.0),
        )
        self.assertEqual("ok", result.status)
        self.assertEqual(100.0, result.available_mechanical_torque_n_m)
        self.assertEqual(100.0, result.applied_mechanical_torque_n_m)
        self.assertEqual(100.0, result.unserved_brake_torque_n_m)

    def test_already_failed_state_executes_nothing(self) -> None:
        initial = state(suspension_failed=True)
        result = evaluate_suspension_brake_step(
            module=module(),
            state=initial,
            step_input=step_input(duration=2.0, torque=100.0),
        )
        self.assertEqual("failed", result.status)
        self.assertEqual("already_failed", result.failure_mode)
        self.assertEqual(0.0, result.executed_duration_s)
        self.assertEqual(2.0, result.unexecuted_duration_s)
        self.assertEqual(initial, result.end_state)

    def test_invalid_contracts_and_runtime_numerical_failure_are_observable(self) -> None:
        invalid = (
            lambda: SuspensionParameters(0.0, 1.0, 0.0, 0.0, 0.1, 0.1),
            lambda: RegenerationParameters(1.0, 1.0, 1.0, 1.0, 1.1),
            lambda: SuspensionBrakeStepInput(0.0, 0.0, 0.0, 0.0, 300.0),
            lambda: state(travel=0.2),
        )
        for constructor in invalid[:3]:
            with self.subTest(constructor=constructor):
                with self.assertRaises(SuspensionBrakeInputError):
                    constructor()
        with self.assertRaises(SuspensionBrakeInputError):
            evaluate_suspension_brake_step(
                module=module(), state=invalid[3](), step_input=step_input()
            )
        with self.assertRaises(SuspensionBrakeInputError):
            evaluate_suspension_brake_step(
                module=module(), state=state(stored=10_001.0), step_input=step_input()
            )

        extreme_suspension = SuspensionParameters(
            100.0, 10_000.0, 1.0e308, 1_000.0, 0.1, 0.1
        )
        numerical = evaluate_suspension_brake_step(
            module=module(suspension=extreme_suspension),
            state=state(velocity=1.0e308),
            step_input=step_input(),
        )
        self.assertEqual("invalid", numerical.status)
        self.assertIn("non-finite", numerical.reason)

    def test_identical_inputs_replay_identically(self) -> None:
        configured = module()
        initial = state(travel=0.01, velocity=-0.02, temperature=320.0, stored=100.0)
        request = step_input(duration=0.02, normal_load=1_100.0, omega=30.0, torque=180.0)
        first = evaluate_suspension_brake_step(
            module=configured, state=initial, step_input=request
        )
        second = evaluate_suspension_brake_step(
            module=configured, state=initial, step_input=request
        )
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
