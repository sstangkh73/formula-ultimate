from __future__ import annotations

from dataclasses import replace
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.simulation.powertrain_dynamics import (
    PowertrainDynamicsError,
    analytical_power_partition,
    initial_powertrain_state,
    load_powertrain_config,
    run_powertrain,
    step_powertrain,
    total_accounted_energy_j,
)


ROOT = Path(__file__).resolve().parents[1]


def raw() -> dict:
    return json.loads((ROOT / "config/vehicle/functional_powertrain_dynamics_v1.json").read_text(encoding="utf-8"))


def config():
    return load_powertrain_config(raw())


class FunctionalPowertrainDynamicsTests(unittest.TestCase):
    def test_analytical_power_partition_conserves_and_respects_limits(self) -> None:
        value = config()
        result = analytical_power_partition(value, throttle=0.5, converter_speed_rad_s=200.0)
        self.assertAlmostEqual(0.0, result["power_residual_w"], places=10)
        self.assertLessEqual(result["storage_power_w"], value.maximum_storage_power_w)
        self.assertLessEqual(result["converter_mechanical_power_w"], value.converter_maximum_output_power_w)
        self.assertLessEqual(result["output_torque_nm"], value.transmission_maximum_output_torque_nm)
        self.assertGreater(result["electrical_connection_heat_w"], 0.0)
        self.assertGreater(result["converter_heat_w"], 0.0)
        self.assertGreater(result["transmission_heat_w"], 0.0)

    def test_reference_transient_conserves_energy_and_respects_local_limits(self) -> None:
        value = config()
        result = run_powertrain(
            value, throttle=0.5, requested_load_torque_nm=200.0,
            duration_s=2.0, step_s=0.0005, sample_stride=20,
        )
        self.assertEqual("passed", result.status)
        self.assertEqual("completed", result.terminal_reason)
        self.assertEqual(4000, result.executed_steps)
        self.assertLessEqual(result.maximum_relative_energy_residual, value.energy_relative_tolerance)
        self.assertLessEqual(result.maximum_abs_connection_demand_torque_nm, value.shaft_maximum_torque_nm)
        self.assertLessEqual(result.maximum_abs_shaft_twist_rad, value.shaft_maximum_twist_rad)
        self.assertLessEqual(result.maximum_output_drive_torque_nm, value.transmission_maximum_output_torque_nm)
        self.assertGreater(result.final_state.useful_work_j, 0.0)
        self.assertGreater(result.final_state.converter_temperature_k, value.ambient_temperature_k)
        self.assertGreater(result.final_state.transmission_temperature_k, value.ambient_temperature_k)
        self.assertAlmostEqual(result.initial_energy_j, total_accounted_energy_j(value, result.final_state), delta=result.maximum_abs_energy_residual_j + 1.0e-8)
        generated_heat = sum((
            result.final_state.electrical_connection_heat_j,
            result.final_state.converter_conversion_heat_j,
            result.final_state.converter_viscous_heat_j,
            result.final_state.shaft_damping_heat_j,
            result.final_state.shaft_efficiency_heat_j,
            result.final_state.transmission_efficiency_heat_j,
            result.final_state.output_viscous_heat_j,
            result.final_state.fracture_heat_j,
        ))
        stored_heat = (
            value.converter_heat_capacity_j_per_k * (result.final_state.converter_temperature_k - value.ambient_temperature_k)
            + value.transmission_heat_capacity_j_per_k * (result.final_state.transmission_temperature_k - value.ambient_temperature_k)
        )
        self.assertAlmostEqual(generated_heat, stored_heat + result.final_state.rejected_heat_j, places=7)

    def test_zero_energy_cannot_create_torque_motion_or_work(self) -> None:
        value = config()
        first = run_powertrain(
            value, throttle=1.0, requested_load_torque_nm=200.0,
            duration_s=0.1, step_s=0.0005, initial_storage_energy_j=0.0, sample_stride=10,
        )
        second = run_powertrain(
            value, throttle=1.0, requested_load_torque_nm=200.0,
            duration_s=0.1, step_s=0.0005, initial_storage_energy_j=0.0, sample_stride=10,
        )
        self.assertEqual("passed", first.status)
        self.assertEqual(first.result_sha256, second.result_sha256)
        self.assertEqual(0.0, first.final_state.converter_speed_rad_s)
        self.assertEqual(0.0, first.final_state.output_speed_rad_s)
        self.assertEqual(0.0, first.final_state.useful_work_j)
        self.assertEqual(0.0, first.final_state.source_energy_used_j)
        self.assertTrue(all(item.converter_torque_nm == 0.0 and item.output_drive_torque_nm == 0.0 for item in first.trace))

    def test_shaft_overload_breaks_irreversibly_and_stops_output_torque(self) -> None:
        value = replace(config(), shaft_maximum_torque_nm=50.0)
        result = run_powertrain(
            value, throttle=0.5, requested_load_torque_nm=200.0,
            duration_s=2.0, step_s=0.0005, sample_stride=1,
        )
        self.assertEqual("failed", result.status)
        self.assertEqual("shaft_connection_failure", result.terminal_reason)
        self.assertTrue(result.final_state.connection_failed)
        self.assertGreater(result.maximum_abs_connection_demand_torque_nm, value.shaft_maximum_torque_nm)
        next_state, evidence = step_powertrain(
            value, result.final_state, throttle=1.0, requested_load_torque_nm=0.0,
            step_s=0.0005, initial_energy_j=result.initial_energy_j,
        )
        self.assertTrue(next_state.connection_failed)
        self.assertEqual(0.0, evidence.shaft_torque_nm)
        self.assertEqual(0.0, evidence.output_drive_torque_nm)

    def test_overtemperature_is_terminal_and_identifies_component(self) -> None:
        value = replace(
            config(), converter_heat_capacity_j_per_k=10.0,
            converter_cooling_w_per_k=0.0, converter_maximum_temperature_k=300.1,
        )
        result = run_powertrain(
            value, throttle=1.0, requested_load_torque_nm=200.0,
            duration_s=2.0, step_s=0.0005, sample_stride=1,
        )
        self.assertEqual("failed", result.status)
        self.assertEqual("converter_overtemperature", result.terminal_reason)
        self.assertGreater(result.final_state.converter_temperature_k, value.converter_maximum_temperature_k)

    def test_half_step_refinement_is_within_frozen_bound(self) -> None:
        value = config()
        coarse = run_powertrain(value, throttle=0.5, requested_load_torque_nm=200.0, duration_s=2.0, step_s=0.0005, sample_stride=10000)
        fine = run_powertrain(value, throttle=0.5, requested_load_torque_nm=200.0, duration_s=2.0, step_s=0.00025, sample_stride=10000)
        for field in ("converter_speed_rad_s", "output_speed_rad_s", "storage_energy_j", "converter_temperature_k", "transmission_temperature_k"):
            left, right = getattr(coarse.final_state, field), getattr(fine.final_state, field)
            relative = abs(left - right) / max(abs(right), 1.0)
            with self.subTest(field=field):
                self.assertLessEqual(relative, value.refinement_relative_tolerance)

    def test_invalid_configuration_and_runtime_values_fail_closed(self) -> None:
        cases = []
        value = raw(); value["energy_converter"]["torque_speed_curve_nm"][1][0] = 0.0; cases.append(value)
        value = raw(); value["energy_converter"]["efficiency_curve"][1][1] = 1.01; cases.append(value)
        value = raw(); value["energy_converter"]["maximum_output_power_w"] = 130000.0; cases.append(value)
        value = raw(); value["transmission"]["maximum_output_torque_nm"] = 1400.0; cases.append(value)
        value = raw(); value["thermal"]["converter"]["maximum_temperature_k"] = 299.0; cases.append(value)
        value = raw(); value["numerical"]["energy_relative_tolerance"] = 0.01; cases.append(value)
        for invalid in cases:
            with self.subTest(invalid=invalid), self.assertRaises(PowertrainDynamicsError):
                load_powertrain_config(invalid)
        with self.assertRaises(PowertrainDynamicsError):
            run_powertrain(config(), throttle=math.nan, requested_load_torque_nm=0.0, duration_s=1.0, step_s=0.001)
        with self.assertRaises(PowertrainDynamicsError):
            run_powertrain(config(), throttle=0.5, requested_load_torque_nm=0.0, duration_s=1.0, step_s=0.003)
        state = replace(initial_powertrain_state(config()), converter_speed_rad_s=math.inf)
        with self.assertRaises(PowertrainDynamicsError):
            step_powertrain(config(), state, throttle=0.0, requested_load_torque_nm=0.0, step_s=0.001, initial_energy_j=1.0)

    def test_replay_identity_changes_with_physical_command(self) -> None:
        value = config()
        first = run_powertrain(value, throttle=0.5, requested_load_torque_nm=200.0, duration_s=0.2, step_s=0.0005, sample_stride=10)
        replay = run_powertrain(value, throttle=0.5, requested_load_torque_nm=200.0, duration_s=0.2, step_s=0.0005, sample_stride=10)
        changed = run_powertrain(value, throttle=0.4, requested_load_torque_nm=200.0, duration_s=0.2, step_s=0.0005, sample_stride=10)
        self.assertEqual(first, replay)
        self.assertEqual(first.result_sha256, replay.result_sha256)
        self.assertNotEqual(first.result_sha256, changed.result_sha256)


if __name__ == "__main__":
    unittest.main()
