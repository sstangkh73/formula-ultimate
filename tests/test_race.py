from __future__ import annotations

import math
from pathlib import Path
import unittest

from formula_ultimate.physics.circuit import load_circuit_catalog
from formula_ultimate.physics.longitudinal import VehicleParameters
from formula_ultimate.physics.race import (
    RaceControl,
    RaceInputError,
    RaceVehicle,
    run_full_race,
)
from formula_ultimate.physics.thermal import ThermalParameters


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "config" / "circuits" / "real_circuits_v1.json"


def safe_thermal(**overrides: float) -> ThermalParameters:
    values = {
        "heat_capacity_j_per_k": 1.0e9,
        "passive_conductance_w_per_k": 0.0,
        "active_conductance_w_per_k": 0.0,
        "derating_start_temperature_k": 1_000.0,
        "failure_temperature_k": 2_000.0,
    }
    values.update(overrides)
    return ThermalParameters(**values)


def vehicle(**overrides) -> RaceVehicle:
    values = {
        "vehicle_id": "reference",
        "longitudinal": VehicleParameters(mass_kg=1_000.0),
        "commanded_tractive_force_n": 10_000.0,
        "initial_onboard_energy_j": 4.0e9,
        "waste_heat_power_w": 0.0,
        "auxiliary_power_w": 0.0,
        "thermal_parameters": safe_thermal(),
        "initial_temperature_k": 300.0,
    }
    values.update(overrides)
    return RaceVehicle(**values)


def control(**overrides) -> RaceControl:
    values = {
        "time_step_s": 10.0,
        "timeout_s": 1_000.0,
        "ambient_temperature_k": 300.0,
        "active_cooling_command": 0.0,
        "random_seed": 17,
        "event_bisection_iterations": 64,
    }
    values.update(overrides)
    return RaceControl(**values)


class RaceCompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.circuits = load_circuit_catalog(CATALOG)
        cls.reference = cls.circuits[0]

    def test_all_ten_profiles_finish_and_replay_exactly(self) -> None:
        self.assertEqual(10, len(self.circuits))
        for circuit in self.circuits:
            with self.subTest(circuit=circuit.circuit_id):
                first = run_full_race(
                    circuit=circuit, vehicle=vehicle(), control=control()
                )
                second = run_full_race(
                    circuit=circuit, vehicle=vehicle(), control=control()
                )
                self.assertEqual(first, second)
                self.assertEqual("finished", first.outcome)
                self.assertGreaterEqual(first.final_state.distance_m, circuit.race_distance_m)
                self.assertGreater(first.final_state.remaining_energy_j, 0.0)
                self.assertEqual(0, first.replay.stochastic_draw_count)
                self.assertEqual(circuit.circuit_id, first.replay.circuit_id)

    def test_energy_depletion_is_localized_without_negative_energy(self) -> None:
        result = run_full_race(
            circuit=self.reference,
            vehicle=vehicle(
                commanded_tractive_force_n=1_000.0,
                initial_onboard_energy_j=1_000.0,
            ),
            control=control(time_step_s=10.0, timeout_s=100.0),
        )
        self.assertEqual("depleted", result.outcome)
        self.assertGreaterEqual(result.final_state.remaining_energy_j, 0.0)
        self.assertLess(result.final_state.distance_m, self.reference.race_distance_m)
        remaining = [item.remaining_energy_j for item in result.telemetry]
        self.assertEqual(sorted(remaining, reverse=True), remaining)
        self.assertTrue(all(item.energy_accounting_residual_j == 0.0 for item in result.telemetry))

    def test_zero_force_times_out_at_exact_control_limit(self) -> None:
        result = run_full_race(
            circuit=self.reference,
            vehicle=vehicle(commanded_tractive_force_n=0.0),
            control=control(time_step_s=2.0, timeout_s=5.0),
        )
        self.assertEqual("timeout", result.outcome)
        self.assertEqual(5.0, result.final_state.time_s)
        self.assertEqual(0.0, result.final_state.distance_m)
        self.assertEqual((2.0, 2.0, 1.0), tuple(item.executed_duration_s for item in result.telemetry))

    def test_finish_wins_exact_depletion_and_timeout_tie(self) -> None:
        finish_time_s = 10.0
        mass_kg = 1_000.0
        force_n = (
            2.0
            * self.reference.race_distance_m
            * mass_kg
            / finish_time_s**2
        )
        exact_finish_energy_j = force_n * self.reference.race_distance_m
        result = run_full_race(
            circuit=self.reference,
            vehicle=vehicle(
                longitudinal=VehicleParameters(mass_kg=mass_kg),
                commanded_tractive_force_n=force_n,
                initial_onboard_energy_j=exact_finish_energy_j,
            ),
            control=control(
                time_step_s=finish_time_s,
                timeout_s=finish_time_s,
            ),
        )
        self.assertEqual("finished", result.outcome)
        self.assertAlmostEqual(finish_time_s, result.final_state.time_s, places=12)
        self.assertGreaterEqual(result.final_state.remaining_energy_j, 0.0)
        self.assertLess(result.terminal_energy_boundary_residual_j, 0.0)
        self.assertAlmostEqual(
            -0.000244140625,
            result.terminal_energy_boundary_residual_j,
            places=12,
        )

    def test_event_energy_residual_beyond_declared_tolerance_is_invalid(self) -> None:
        finish_time_s = 10.0
        mass_kg = 1_000.0
        force_n = 2.0 * self.reference.race_distance_m * mass_kg / finish_time_s**2
        result = run_full_race(
            circuit=self.reference,
            vehicle=vehicle(
                longitudinal=VehicleParameters(mass_kg=mass_kg),
                commanded_tractive_force_n=force_n,
                initial_onboard_energy_j=force_n * self.reference.race_distance_m,
            ),
            control=control(
                time_step_s=finish_time_s,
                timeout_s=finish_time_s,
                energy_event_absolute_tolerance_j=0.0,
                energy_event_relative_tolerance=0.0,
            ),
        )
        self.assertEqual("invalid", result.outcome)
        self.assertIn("overspent onboard energy", result.reason)

    def test_thermal_failure_executes_only_to_crossing(self) -> None:
        result = run_full_race(
            circuit=self.reference,
            vehicle=vehicle(
                commanded_tractive_force_n=0.0,
                initial_onboard_energy_j=100_000.0,
                waste_heat_power_w=1_000.0,
                thermal_parameters=ThermalParameters(1_000.0, 0.0, 0.0, 370.0, 400.0),
                initial_temperature_k=350.0,
            ),
            control=control(time_step_s=100.0, timeout_s=200.0),
        )
        self.assertEqual("failed", result.outcome)
        self.assertEqual(50.0, result.final_state.time_s)
        self.assertEqual(400.0, result.final_state.thermal_state.temperature_k)
        self.assertTrue(result.final_state.thermal_state.failed)
        self.assertEqual(50.0, result.telemetry[-1].executed_duration_s)
        self.assertEqual(50_000.0, result.consumed_energy_j)

    def test_start_temperature_derates_applied_force(self) -> None:
        result = run_full_race(
            circuit=self.reference,
            vehicle=vehicle(
                commanded_tractive_force_n=1_000.0,
                thermal_parameters=ThermalParameters(1.0e9, 0.0, 0.0, 370.0, 400.0),
                initial_temperature_k=385.0,
            ),
            control=control(time_step_s=1.0, timeout_s=1.0),
        )
        self.assertEqual("timeout", result.outcome)
        self.assertAlmostEqual(0.5, result.telemetry[0].start_derating_factor)
        self.assertAlmostEqual(500.0, result.telemetry[0].applied_tractive_force_n)

    def test_runtime_numerical_failure_is_invalid_outcome(self) -> None:
        result = run_full_race(
            circuit=self.reference,
            vehicle=vehicle(
                commanded_tractive_force_n=0.0,
                initial_onboard_energy_j=1.0e308,
                waste_heat_power_w=1.0e300,
                thermal_parameters=ThermalParameters(1_000.0, 1.0e-300, 0.0, 370.0, 400.0),
            ),
            control=control(time_step_s=1.0, timeout_s=2.0),
        )
        self.assertEqual("invalid", result.outcome)
        self.assertIn("runtime numerical failure", result.reason)
        self.assertFalse(result.telemetry)

    def test_onboard_energy_never_increases(self) -> None:
        result = run_full_race(
            circuit=self.reference,
            vehicle=vehicle(waste_heat_power_w=100.0, auxiliary_power_w=50.0),
            control=control(),
        )
        values = [vehicle().initial_onboard_energy_j] + [
            item.remaining_energy_j for item in result.telemetry
        ]
        self.assertTrue(all(after <= before for before, after in zip(values, values[1:])))
        self.assertAlmostEqual(
            result.consumed_energy_j,
            sum(item.source_energy_used_j for item in result.telemetry),
            places=6,
        )

    def test_invalid_contracts_fail_before_execution(self) -> None:
        invalid = (
            lambda: vehicle(vehicle_id=""),
            lambda: vehicle(commanded_tractive_force_n=-1.0),
            lambda: vehicle(initial_onboard_energy_j=-1.0),
            lambda: vehicle(waste_heat_power_w=math.nan),
            lambda: control(time_step_s=0.0),
            lambda: control(timeout_s=-1.0),
            lambda: control(active_cooling_command=2.0),
            lambda: control(random_seed=1.5),
            lambda: control(event_bisection_iterations=4),
            lambda: control(energy_event_absolute_tolerance_j=-1.0),
            lambda: control(energy_event_relative_tolerance=1.0e-5),
        )
        for constructor in invalid:
            with self.subTest(constructor=constructor):
                with self.assertRaises(RaceInputError):
                    constructor()


if __name__ == "__main__":
    unittest.main()
