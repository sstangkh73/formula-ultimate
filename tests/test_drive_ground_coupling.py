from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.simulation.drive_ground_coupling import (
    DriveGroundCouplingError,
    analytical_ground_partition,
    ground_force_request,
    load_drive_ground_config,
    run_drive_ground,
    step_drive_ground,
    total_drive_ground_accounted_energy_j,
)
from formula_ultimate.simulation.powertrain_dynamics import load_powertrain_config


ROOT = Path(__file__).resolve().parents[1]


def declarations():
    architecture = json.loads((ROOT / "config/vehicle/functional_vehicle_architecture_v2.json").read_text(encoding="utf-8"))
    powertrain_raw = json.loads((ROOT / "config/vehicle/functional_powertrain_dynamics_v1.json").read_text(encoding="utf-8"))
    coupling_raw = json.loads((ROOT / "config/vehicle/functional_drive_ground_coupling_v1.json").read_text(encoding="utf-8"))
    return architecture, powertrain_raw, coupling_raw


def loaded():
    architecture, powertrain_raw, coupling_raw = declarations()
    powertrain = load_powertrain_config(powertrain_raw)
    coupling = load_drive_ground_config(coupling_raw, powertrain=powertrain, architecture_raw=architecture)
    return coupling, powertrain


class DriveGroundCouplingTests(unittest.TestCase):
    def test_geometry_inertia_and_analytical_power_partition_close(self) -> None:
        coupling, powertrain = loaded()
        self.assertEqual(2, len(coupling.ground_units))
        self.assertAlmostEqual(
            powertrain.output_inertia_kg_m2,
            coupling.other_output_inertia_kg_m2 + sum(item.rotational_inertia_kg_m2 for item in coupling.ground_units),
        )
        result = analytical_ground_partition(
            wheel_speed_rad_per_s=100.0,
            vehicle_speed_m_per_s=12.0,
            forces_n=(1000.0, 1000.0),
            radii_m=(0.14, 0.14),
        )
        self.assertAlmostEqual(280.0, result["load_torque_nm"])
        self.assertAlmostEqual(0.0, result["power_residual_w"], places=10)
        self.assertGreater(result["slip_heat_w"], 0.0)

    def test_reference_accelerates_with_bounded_force_and_global_energy(self) -> None:
        coupling, powertrain = loaded()
        result = run_drive_ground(coupling, powertrain, throttle=0.5, duration_s=2.0, step_s=0.0005, sample_stride=20)
        self.assertEqual("passed", result.status)
        self.assertEqual("finished", result.outcome)
        self.assertEqual(4000, result.executed_steps)
        self.assertGreater(result.final_state.speed_m_per_s, 0.0)
        self.assertGreater(result.final_state.position_m, 0.0)
        self.assertGreater(result.final_state.slip_heat_j, 0.0)
        self.assertLessEqual(result.maximum_contact_utilization, 1.0)
        self.assertLessEqual(result.maximum_global_relative_energy_residual, coupling.energy_relative_tolerance)
        self.assertAlmostEqual(result.initial_total_energy_j, total_drive_ground_accounted_energy_j(coupling, powertrain, result.final_state), delta=result.maximum_abs_global_energy_residual_j + 1.0e-8)
        for step in result.trace:
            self.assertAlmostEqual(step.applied_axle_load_torque_nm, sum(item.load_torque_nm for item in step.contacts), places=10)
            self.assertAlmostEqual(0.0, step.interface_power_partition_residual_j, places=9)
            for unit, evidence in zip(coupling.ground_units, step.contacts):
                self.assertLessEqual(evidence.applied_force_n, min(unit.friction_coefficient * unit.normal_load_n, unit.maximum_longitudinal_force_n) + 1.0e-10)

    def test_zero_throttle_and_zero_energy_cannot_move_vehicle(self) -> None:
        coupling, powertrain = loaded()
        zero_throttle = run_drive_ground(coupling, powertrain, throttle=0.0, duration_s=0.1, step_s=0.0005, sample_stride=10)
        zero_energy = run_drive_ground(coupling, powertrain, throttle=1.0, duration_s=0.1, step_s=0.0005, initial_storage_energy_j=0.0, sample_stride=10)
        for result in (zero_throttle, zero_energy):
            self.assertEqual("passed", result.status)
            self.assertEqual(0.0, result.final_state.speed_m_per_s)
            self.assertEqual(0.0, result.final_state.position_m)
            self.assertEqual(0.0, result.maximum_ground_force_n)
            self.assertEqual(0.0, result.final_state.contact_body_work_j)

    def test_slip_law_is_bounded_and_negative_slip_has_no_undeclared_regeneration(self) -> None:
        coupling, _ = loaded()
        unit = coupling.ground_units[0]
        high = ground_force_request(unit, wheel_speed_rad_per_s=1000.0, vehicle_speed_m_per_s=1.0, regularization_speed_m_per_s=0.5)
        negative = ground_force_request(unit, wheel_speed_rad_per_s=0.0, vehicle_speed_m_per_s=10.0, regularization_speed_m_per_s=0.5)
        self.assertLessEqual(high["requested_force_n"], high["force_capacity_n"])
        self.assertGreater(high["requested_force_n"], 0.99 * high["force_capacity_n"])
        self.assertLess(negative["slip_ratio"], 0.0)
        self.assertEqual(0.0, negative["requested_force_n"])

    def test_drive_path_failure_propagates_to_dnf_and_zero_output_drive(self) -> None:
        coupling, powertrain = loaded()
        failed_powertrain = replace(powertrain, shaft_maximum_torque_nm=50.0)
        result = run_drive_ground(coupling, failed_powertrain, throttle=0.5, duration_s=2.0, step_s=0.0005, sample_stride=1)
        self.assertEqual("passed", result.status)
        self.assertEqual("DNF", result.outcome)
        self.assertEqual("shaft_connection_failure", result.terminal_reason)
        self.assertEqual("failed", result.final_state.drive_subsystem_state)
        self.assertEqual(0.0, result.trace[-1].powertrain.output_drive_torque_nm)
        with self.assertRaisesRegex(DriveGroundCouplingError, "DNF"):
            step_drive_ground(
                coupling, failed_powertrain, result.final_state, throttle=1.0,
                step_s=0.0005, initial_total_energy_j=result.initial_total_energy_j,
            )

    def test_half_step_refinement_is_within_frozen_bound(self) -> None:
        coupling, powertrain = loaded()
        coarse = run_drive_ground(coupling, powertrain, throttle=0.5, duration_s=2.0, step_s=0.0005, sample_stride=10000)
        fine = run_drive_ground(coupling, powertrain, throttle=0.5, duration_s=2.0, step_s=0.00025, sample_stride=10000)
        for field in ("speed_m_per_s", "position_m", "slip_heat_j", "aerodynamic_work_j", "rolling_work_j"):
            left, right = getattr(coarse.final_state, field), getattr(fine.final_state, field)
            relative = abs(left - right) / max(abs(right), 1.0)
            with self.subTest(field=field):
                self.assertLessEqual(relative, coupling.refinement_relative_tolerance)

    def test_invalid_geometry_inertia_contact_and_numerics_fail_closed(self) -> None:
        architecture, powertrain_raw, raw = declarations()
        powertrain = load_powertrain_config(powertrain_raw)
        cases = []
        value = deepcopy(raw); value["ground_units"][0]["effective_radius_m"] = 0.15; cases.append(value)
        value = deepcopy(raw); value["ground_units"][0]["rotational_inertia_kg_m2"] = 0.2; cases.append(value)
        value = deepcopy(raw); value["ground_units"][0]["maximum_longitudinal_force_n"] = 5000.0; cases.append(value)
        value = deepcopy(raw); value["ground_units"][0]["normal_load_n"] = 9000.0; cases.append(value)
        value = deepcopy(raw); value["inertia_closure"]["other_output_inertia_kg_m2"] = 0.0; cases.append(value)
        value = deepcopy(raw); value["numerical"]["energy_relative_tolerance"] = 0.01; cases.append(value)
        value = deepcopy(raw); value["ground_units"][0]["friction_coefficient"] = math.inf; cases.append(value)
        for invalid in cases:
            with self.subTest(invalid=invalid), self.assertRaises(DriveGroundCouplingError):
                load_drive_ground_config(invalid, powertrain=powertrain, architecture_raw=architecture)

    def test_replay_is_exact_and_command_changes_identity(self) -> None:
        coupling, powertrain = loaded()
        first = run_drive_ground(coupling, powertrain, throttle=0.5, duration_s=0.2, step_s=0.0005, sample_stride=10)
        replay = run_drive_ground(coupling, powertrain, throttle=0.5, duration_s=0.2, step_s=0.0005, sample_stride=10)
        changed = run_drive_ground(coupling, powertrain, throttle=0.4, duration_s=0.2, step_s=0.0005, sample_stride=10)
        self.assertEqual(first, replay)
        self.assertEqual(first.result_sha256, replay.result_sha256)
        self.assertNotEqual(first.result_sha256, changed.result_sha256)


if __name__ == "__main__":
    unittest.main()
