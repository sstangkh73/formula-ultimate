from __future__ import annotations

import math
import unittest

from formula_ultimate.physics.thermal import (
    ThermalInputError,
    ThermalNumericalError,
    ThermalParameters,
    ThermalState,
    ThermalStepInput,
    step_thermal_state,
    thermal_derating_factor,
)


def parameters(**overrides: float) -> ThermalParameters:
    values = {
        "heat_capacity_j_per_k": 1_000.0,
        "passive_conductance_w_per_k": 0.0,
        "active_conductance_w_per_k": 0.0,
        "derating_start_temperature_k": 370.0,
        "failure_temperature_k": 400.0,
    }
    values.update(overrides)
    return ThermalParameters(**values)


def step_input(**overrides: float) -> ThermalStepInput:
    values = {
        "duration_s": 10.0,
        "heat_generation_w": 0.0,
        "ambient_temperature_k": 300.0,
        "active_cooling_command": 0.0,
    }
    values.update(overrides)
    return ThermalStepInput(**values)


class ThermalPhysicsTests(unittest.TestCase):
    def test_adiabatic_heating_matches_closed_form(self) -> None:
        result = step_thermal_state(
            parameters=parameters(),
            state=ThermalState(0.0, 300.0),
            step_input=step_input(heat_generation_w=100.0),
        )
        self.assertEqual("normal", result.status)
        self.assertAlmostEqual(301.0, result.end_state.temperature_k, places=12)
        self.assertEqual(1_000.0, result.heat_generated_j)
        self.assertEqual(1_000.0, result.stored_energy_change_j)
        self.assertEqual(0.0, result.energy_residual_j)

    def test_newton_cooldown_matches_exponential_reference(self) -> None:
        result = step_thermal_state(
            parameters=parameters(passive_conductance_w_per_k=100.0),
            state=ThermalState(0.0, 390.0),
            step_input=step_input(),
        )
        expected_k = 300.0 + 90.0 * math.exp(-1.0)
        self.assertAlmostEqual(expected_k, result.end_state.temperature_k, places=12)
        self.assertEqual("derated", result.status)
        self.assertLess(abs(result.energy_residual_j), 1.0e-9)

    def test_heat_generation_equilibrium_remains_fixed(self) -> None:
        result = step_thermal_state(
            parameters=parameters(passive_conductance_w_per_k=10.0),
            state=ThermalState(5.0, 350.0),
            step_input=step_input(duration_s=100.0, heat_generation_w=500.0),
        )
        self.assertAlmostEqual(350.0, result.end_state.temperature_k, places=12)
        self.assertAlmostEqual(50_000.0, result.passive_heat_rejected_j, places=9)
        self.assertAlmostEqual(0.0, result.stored_energy_change_j, places=9)

    def test_active_conductance_increases_cooling_and_is_separately_accounted(self) -> None:
        params = parameters(
            passive_conductance_w_per_k=10.0,
            active_conductance_w_per_k=30.0,
        )
        passive = step_thermal_state(
            parameters=params,
            state=ThermalState(0.0, 360.0),
            step_input=step_input(active_cooling_command=0.0),
        )
        active = step_thermal_state(
            parameters=params,
            state=ThermalState(0.0, 360.0),
            step_input=step_input(active_cooling_command=1.0),
        )
        self.assertLess(active.end_state.temperature_k, passive.end_state.temperature_k)
        self.assertGreater(active.active_heat_rejected_j, 0.0)
        self.assertAlmostEqual(
            3.0 * active.passive_heat_rejected_j,
            active.active_heat_rejected_j,
            places=9,
        )

    def test_derating_factor_is_piecewise_linear(self) -> None:
        params = parameters()
        self.assertEqual(1.0, thermal_derating_factor(params, 350.0))
        self.assertEqual(1.0, thermal_derating_factor(params, 370.0))
        self.assertAlmostEqual(0.5, thermal_derating_factor(params, 385.0))
        self.assertEqual(0.0, thermal_derating_factor(params, 400.0))
        self.assertEqual(0.0, thermal_derating_factor(params, 450.0))

    def test_failure_crossing_is_localized_and_latched(self) -> None:
        params = parameters()
        result = step_thermal_state(
            parameters=params,
            state=ThermalState(10.0, 350.0),
            step_input=step_input(duration_s=100.0, heat_generation_w=1_000.0),
        )
        self.assertEqual("failed", result.status)
        self.assertEqual(50.0, result.executed_duration_s)
        self.assertEqual(50.0, result.unexecuted_duration_s)
        self.assertEqual(60.0, result.failure_time_s)
        self.assertEqual(400.0, result.end_state.temperature_k)
        self.assertTrue(result.end_state.failed)
        self.assertEqual(0.0, result.end_derating_factor)
        followup = step_thermal_state(
            parameters=params,
            state=result.end_state,
            step_input=step_input(duration_s=10.0),
        )
        self.assertEqual("already_failed", followup.status)
        self.assertEqual(result.end_state, followup.end_state)
        self.assertEqual(10.0, followup.unexecuted_duration_s)

    def test_threshold_at_start_is_failure_not_temperature_clipping(self) -> None:
        result = step_thermal_state(
            parameters=parameters(),
            state=ThermalState(3.0, 410.0),
            step_input=step_input(),
        )
        self.assertEqual("failed_at_start", result.status)
        self.assertEqual(410.0, result.end_state.temperature_k)
        self.assertEqual(0.0, result.executed_duration_s)

    def test_colder_component_receives_signed_ambient_heat(self) -> None:
        result = step_thermal_state(
            parameters=parameters(passive_conductance_w_per_k=20.0),
            state=ThermalState(0.0, 280.0),
            step_input=step_input(ambient_temperature_k=300.0),
        )
        self.assertGreater(result.end_state.temperature_k, 280.0)
        self.assertLess(result.passive_heat_rejected_j, 0.0)
        self.assertLess(abs(result.energy_residual_j), 1.0e-9)

    def test_invalid_inputs_are_rejected(self) -> None:
        invalid = (
            lambda: parameters(heat_capacity_j_per_k=0.0),
            lambda: parameters(passive_conductance_w_per_k=-1.0),
            lambda: parameters(derating_start_temperature_k=400.0),
            lambda: ThermalState(-1.0, 300.0),
            lambda: ThermalState(0.0, 0.0),
            lambda: ThermalStepInput(0.0, 0.0, 300.0, 0.0),
            lambda: ThermalStepInput(1.0, -1.0, 300.0, 0.0),
            lambda: ThermalStepInput(1.0, 0.0, 300.0, 1.1),
            lambda: thermal_derating_factor(parameters(), math.nan),
        )
        for constructor in invalid:
            with self.subTest(constructor=constructor):
                with self.assertRaises(ThermalInputError):
                    constructor()

    def test_extreme_finite_inputs_surface_numerical_failure(self) -> None:
        with self.assertRaises(ThermalNumericalError):
            step_thermal_state(
                parameters=parameters(
                    passive_conductance_w_per_k=1.0e-300,
                    active_conductance_w_per_k=0.0,
                ),
                state=ThermalState(0.0, 300.0),
                step_input=step_input(heat_generation_w=1.0e300),
            )

    def test_replay_is_deterministic(self) -> None:
        kwargs = {
            "parameters": parameters(
                passive_conductance_w_per_k=12.0,
                active_conductance_w_per_k=25.0,
            ),
            "state": ThermalState(4.0, 345.0),
            "step_input": step_input(
                duration_s=7.5,
                heat_generation_w=800.0,
                ambient_temperature_k=305.0,
                active_cooling_command=0.4,
            ),
        }
        self.assertEqual(step_thermal_state(**kwargs), step_thermal_state(**kwargs))


if __name__ == "__main__":
    unittest.main()
