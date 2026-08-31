from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import unittest

from formula_ultimate.simulation.coupled_planar_differential import (
    CoupledPlanarDifferentialError,
    body_kinetic_energy_j,
    branch_speeds,
    initial_coupled_state,
    load_coupled_planar_config,
    run_coupled_planar_differential,
    step_coupled_planar_differential,
    total_accounted_energy_j,
    with_coupled_branch_friction,
    with_steer,
)
from formula_ultimate.simulation.differential_drive_coupling import load_differential_drive_config
from formula_ultimate.simulation.planar_support_gate import load_support_gate_config, materialize_architecture_variant
from formula_ultimate.simulation.powertrain_dynamics import (
    load_powertrain_config,
    total_accounted_energy_j as total_powertrain_accounted_energy_j,
)


ROOT = Path(__file__).resolve().parents[1]


def declarations():
    vehicle_root = ROOT / "config/vehicle"
    raw = json.loads((vehicle_root / "coupled_planar_differential_v1.json").read_text(encoding="utf-8"))
    differential_raw = json.loads((vehicle_root / raw["differential_source"]).read_text(encoding="utf-8"))
    variant = json.loads((vehicle_root / differential_raw["architecture_variant_source"]).read_text(encoding="utf-8"))
    base = json.loads((vehicle_root / variant["base_architecture_source"]).read_text(encoding="utf-8"))
    support_raw = json.loads((vehicle_root / differential_raw["support_gate_source"]).read_text(encoding="utf-8"))
    powertrain_raw = json.loads((vehicle_root / differential_raw["powertrain_source"]).read_text(encoding="utf-8"))
    return raw, differential_raw, variant, base, support_raw, powertrain_raw


def loaded():
    raw, differential_raw, variant, base, support_raw, powertrain_raw = declarations()
    architecture = materialize_architecture_variant(base, variant)
    support = load_support_gate_config(support_raw)
    powertrain = load_powertrain_config(powertrain_raw)
    differential = load_differential_drive_config(
        differential_raw, powertrain=powertrain, architecture_raw=architecture, support_config=support,
    )
    config = load_coupled_planar_config(raw, differential=differential, architecture_raw=architecture, support_config=support)
    return raw, architecture, support, config, powertrain


def relative(left: float, right: float) -> float:
    return abs(left - right) / max(abs(right), 1.0)


class CoupledPlanarDifferentialTests(unittest.TestCase):
    def test_geometry_identity_and_matched_initial_energy_are_explicit(self) -> None:
        _, _, _, config, powertrain = loaded()
        state = initial_coupled_state(config, powertrain)
        left, right = branch_speeds(state)
        expected_wheel_speed = config.initial_longitudinal_speed_m_per_s / config.differential.branches[0].effective_radius_m
        self.assertAlmostEqual(expected_wheel_speed, left)
        self.assertAlmostEqual(expected_wheel_speed, right)
        self.assertAlmostEqual(powertrain.transmission_ratio * expected_wheel_speed, state.powertrain.converter_speed_rad_s)
        initial_powertrain = total_powertrain_accounted_energy_j(powertrain, state.powertrain)
        initial_total = total_accounted_energy_j(config, powertrain, state)
        self.assertAlmostEqual(body_kinetic_energy_j(config, state), initial_total - initial_powertrain, places=8)
        self.assertAlmostEqual(powertrain.initial_storage_energy_j, initial_total, places=8)
        self.assertLess(state.powertrain.storage_energy_j, powertrain.initial_storage_energy_j)
        self.assertEqual(3, len(config.contacts))
        self.assertEqual(2, sum(item.powered for item in config.contacts))

    def test_zero_steer_retains_symmetric_straight_response(self) -> None:
        _, _, _, config, powertrain = loaded()
        result = run_coupled_planar_differential(with_steer(config, 0.0), powertrain, sample_stride=50)
        self.assertEqual(("passed", "finished"), (result.status, result.outcome))
        self.assertEqual(0.0, result.final_state.planar.y_position_m)
        self.assertEqual(0.0, result.final_state.planar.heading_rad)
        self.assertEqual(0.0, result.final_state.planar.lateral_velocity_m_per_s)
        self.assertEqual(0.0, result.final_state.planar.yaw_rate_rad_per_s)
        self.assertEqual(0.0, result.final_state.differential_speed_rad_s)
        self.assertEqual(result.final_branch_speeds_rad_s[0][1], result.final_branch_speeds_rad_s[1][1])

    def test_opposite_steer_is_mirrored_and_has_correct_yaw_sign(self) -> None:
        _, _, _, config, powertrain = loaded()
        positive = run_coupled_planar_differential(config, powertrain, sample_stride=100)
        negative = run_coupled_planar_differential(with_steer(config, -config.steer_angle_rad), powertrain, sample_stride=100)
        self.assertEqual(("finished", "finished"), (positive.outcome, negative.outcome))
        self.assertGreater(positive.final_state.planar.heading_rad, 0.0)
        self.assertLess(negative.final_state.planar.heading_rad, 0.0)
        for field in ("y_position_m", "heading_rad", "lateral_velocity_m_per_s", "yaw_rate_rad_per_s"):
            self.assertAlmostEqual(getattr(positive.final_state.planar, field), -getattr(negative.final_state.planar, field), places=12)
        for field in ("x_position_m", "longitudinal_velocity_m_per_s"):
            self.assertAlmostEqual(getattr(positive.final_state.planar, field), getattr(negative.final_state.planar, field), places=12)
        self.assertAlmostEqual(positive.final_state.differential_speed_rad_s, -negative.final_state.differential_speed_rad_s, places=12)

    def test_split_grip_and_spatial_mirror_exchange_independent_branches(self) -> None:
        raw, _, _, config, powertrain = loaded()
        controls = raw["falsification_controls"]
        split = with_coupled_branch_friction(
            config, left=controls["split_grip_left_friction"], right=controls["split_grip_right_friction"],
        )
        mirror = with_steer(with_coupled_branch_friction(
            config, left=controls["split_grip_right_friction"], right=controls["split_grip_left_friction"],
        ), -config.steer_angle_rad)
        left_result = run_coupled_planar_differential(split, powertrain, sample_stride=100)
        right_result = run_coupled_planar_differential(mirror, powertrain, sample_stride=100)
        self.assertEqual(("finished", "finished"), (left_result.outcome, right_result.outcome))
        self.assertAlmostEqual(left_result.final_branch_speeds_rad_s[0][1], right_result.final_branch_speeds_rad_s[1][1], places=12)
        self.assertAlmostEqual(left_result.final_branch_speeds_rad_s[1][1], right_result.final_branch_speeds_rad_s[0][1], places=12)
        self.assertAlmostEqual(left_result.final_state.differential_speed_rad_s, -right_result.final_state.differential_speed_rad_s, places=12)
        self.assertAlmostEqual(left_result.final_state.planar.y_position_m, -right_result.final_state.planar.y_position_m, places=12)

    def test_per_step_load_transfer_limits_passive_support_and_residuals(self) -> None:
        _, _, _, config, powertrain = loaded()
        result = run_coupled_planar_differential(config, powertrain, sample_stride=25)
        baseline_minimum = min(item.baseline_normal_load_n for item in config.contacts)
        self.assertLess(result.minimum_normal_load_n, baseline_minimum)
        self.assertGreater(result.minimum_normal_load_n, 0.0)
        self.assertLessEqual(result.maximum_contact_utilization, 1.0 + 1.0e-12)
        self.assertLessEqual(result.maximum_abs_load_balance_residual, 1.0e-8)
        self.assertLessEqual(result.maximum_abs_carrier_average_residual_rad_s, 1.0e-12)
        self.assertLessEqual(result.maximum_abs_modal_equation_residual_nm, 1.0e-9)
        self.assertLessEqual(result.maximum_abs_torque_residual_nm, 1.0e-9)
        for step in result.trace:
            rear = next(item for item in step.contacts if not item.powered)
            self.assertEqual(0.0, rear.applied_longitudinal_force_n)
            self.assertEqual(0.0, rear.reflected_load_torque_nm)
            self.assertIsNone(rear.wheel_speed_rad_s)

    def test_contact_body_and_global_energy_residuals_are_bounded(self) -> None:
        _, _, _, config, powertrain = loaded()
        result = run_coupled_planar_differential(config, powertrain, sample_stride=50)
        self.assertLessEqual(result.maximum_abs_differential_interface_energy_residual_j, 1.0e-9)
        self.assertLessEqual(result.maximum_abs_contact_energy_residual_j, 1.0e-9)
        self.assertLessEqual(result.maximum_abs_body_energy_residual_j, 1.0e-8)
        self.assertLessEqual(result.maximum_global_relative_energy_residual, config.global_energy_relative_tolerance)
        self.assertGreater(result.final_state.longitudinal_slip_heat_j, 0.0)
        self.assertGreater(result.final_state.lateral_slip_heat_j, 0.0)
        self.assertGreater(result.final_state.branch_connection_heat_j, 0.0)

    def test_excessive_steer_exposes_contact_lift_and_terminal_state(self) -> None:
        raw, _, _, config, powertrain = loaded()
        excessive = with_steer(config, raw["falsification_controls"]["excessive_steer_angle_rad"])
        result = run_coupled_planar_differential(excessive, powertrain, sample_stride=100)
        self.assertEqual(("passed", "DNF", "contact_lift"), (result.status, result.outcome, result.terminal_reason))
        self.assertLess(result.minimum_normal_load_n, 0.0)
        self.assertEqual("failed", result.final_state.drive_subsystem_state)
        with self.assertRaisesRegex(CoupledPlanarDifferentialError, "DNF"):
            step_coupled_planar_differential(
                excessive, powertrain, result.final_state,
                initial_powertrain_energy_j=result.initial_powertrain_energy_j,
                initial_total_energy_j=result.initial_total_energy_j,
            )

    def test_half_step_refinement_is_within_frozen_bound(self) -> None:
        _, _, _, config, powertrain = loaded()
        coarse = run_coupled_planar_differential(config, powertrain, sample_stride=10_000)
        fine = run_coupled_planar_differential(config, powertrain, time_step_s=config.time_step_s / 2.0, sample_stride=10_000)
        pairs = [
            (getattr(coarse.final_state.planar, field), getattr(fine.final_state.planar, field))
            for field in ("x_position_m", "y_position_m", "heading_rad", "longitudinal_velocity_m_per_s", "lateral_velocity_m_per_s", "yaw_rate_rad_per_s")
        ] + [
            (coarse.final_state.differential_speed_rad_s, fine.final_state.differential_speed_rad_s),
            (coarse.final_state.longitudinal_slip_heat_j, fine.final_state.longitudinal_slip_heat_j),
            (coarse.final_state.lateral_slip_heat_j, fine.final_state.lateral_slip_heat_j),
        ]
        self.assertLessEqual(max(relative(left, right) for left, right in pairs), config.refinement_relative_tolerance)

    def test_invalid_steer_tolerance_solver_and_runtime_nonconvergence_fail_closed(self) -> None:
        raw, differential_raw, variant, base, support_raw, powertrain_raw = declarations()
        architecture = materialize_architecture_variant(base, variant)
        support = load_support_gate_config(support_raw)
        powertrain = load_powertrain_config(powertrain_raw)
        differential = load_differential_drive_config(
            differential_raw, powertrain=powertrain, architecture_raw=architecture, support_config=support,
        )
        invalid_values = []
        value = deepcopy(raw); value["planar"]["maximum_steer_angle_rad"] = 0.61; invalid_values.append(value)
        value = deepcopy(raw); value["planar"]["throttle"] = 1.01; invalid_values.append(value)
        value = deepcopy(raw); value["solver"]["maximum_load_iterations"] = 0; invalid_values.append(value)
        value = deepcopy(raw); value["numerical"]["global_energy_relative_tolerance"] = 0.0011; invalid_values.append(value)
        value = deepcopy(raw); value["numerical"]["refinement_relative_tolerance"] = 0.021; invalid_values.append(value)
        for invalid in invalid_values:
            with self.subTest(invalid=invalid), self.assertRaises(CoupledPlanarDifferentialError):
                load_coupled_planar_config(invalid, differential=differential, architecture_raw=architecture, support_config=support)
        config = load_coupled_planar_config(raw, differential=differential, architecture_raw=architecture, support_config=support)
        with self.assertRaisesRegex(CoupledPlanarDifferentialError, "fixed point"):
            run_coupled_planar_differential(replace(config, maximum_load_iterations=1), powertrain)

    def test_replay_is_exact_and_command_changes_identity(self) -> None:
        _, _, _, config, powertrain = loaded()
        first = run_coupled_planar_differential(config, powertrain, sample_stride=25)
        replay = run_coupled_planar_differential(config, powertrain, sample_stride=25)
        changed = run_coupled_planar_differential(with_steer(config, 0.0), powertrain, sample_stride=25)
        self.assertEqual(first, replay)
        self.assertEqual(first.result_sha256, replay.result_sha256)
        self.assertNotEqual(first.result_sha256, changed.result_sha256)


if __name__ == "__main__":
    unittest.main()
