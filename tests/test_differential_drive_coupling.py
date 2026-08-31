from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.simulation.differential_drive_coupling import (
    DifferentialDriveError,
    branch_speeds,
    differential_modal_energy_j,
    load_differential_drive_config,
    run_differential_drive,
    step_differential_drive,
    total_differential_drive_accounted_energy_j,
    with_branch_friction,
)
from formula_ultimate.simulation.planar_support_gate import (
    load_support_gate_config,
    materialize_architecture_variant,
)
from formula_ultimate.simulation.powertrain_dynamics import load_powertrain_config


ROOT = Path(__file__).resolve().parents[1]


def declarations():
    vehicle_root = ROOT / "config/vehicle"
    raw = json.loads((vehicle_root / "functional_differential_drive_v1.json").read_text(encoding="utf-8"))
    variant = json.loads((vehicle_root / raw["architecture_variant_source"]).read_text(encoding="utf-8"))
    base = json.loads((vehicle_root / variant["base_architecture_source"]).read_text(encoding="utf-8"))
    support_raw = json.loads((vehicle_root / raw["support_gate_source"]).read_text(encoding="utf-8"))
    powertrain_raw = json.loads((vehicle_root / raw["powertrain_source"]).read_text(encoding="utf-8"))
    return raw, variant, base, support_raw, powertrain_raw


def loaded():
    raw, variant, base, support_raw, powertrain_raw = declarations()
    architecture = materialize_architecture_variant(base, variant)
    support = load_support_gate_config(support_raw)
    powertrain = load_powertrain_config(powertrain_raw)
    config = load_differential_drive_config(raw, powertrain=powertrain, architecture_raw=architecture, support_config=support)
    return raw, architecture, config, powertrain


def reference_arguments(raw):
    experiment = raw["reference_experiment"]
    return {
        "throttle": float(experiment["throttle"]),
        "duration_s": float(experiment["duration_s"]),
        "step_s": float(experiment["step_s"]),
        "sample_stride": int(experiment["sample_stride"]),
    }


def relative(left: float, right: float) -> float:
    return abs(left - right) / max(abs(right), 1.0)


class DifferentialDriveCouplingTests(unittest.TestCase):
    def test_geometry_support_ports_efficiency_and_inertia_close(self) -> None:
        _, _, config, powertrain = loaded()
        self.assertEqual(("left", "right"), tuple(item.side for item in config.branches))
        self.assertAlmostEqual(2.5, config.other_output_inertia_kg_m2 + config.modal_inertia_kg_m2)
        self.assertAlmostEqual(powertrain.output_inertia_kg_m2, config.other_output_inertia_kg_m2 + config.modal_inertia_kg_m2)
        self.assertAlmostEqual(1403.3621854316146, sum(item.static_normal_load_n for item in config.branches))
        self.assertEqual((0.98, 0.98), tuple(item.connection_efficiency for item in config.branches))

    def test_symmetric_grip_keeps_independent_mode_exactly_zero(self) -> None:
        raw, _, config, powertrain = loaded()
        result = run_differential_drive(config, powertrain, **reference_arguments(raw))
        self.assertEqual("passed", result.status)
        self.assertEqual("finished", result.outcome)
        self.assertEqual(0.0, result.final_state.differential_speed_rad_s)
        self.assertEqual(0.0, result.maximum_differential_modal_energy_j)
        self.assertEqual(result.final_branch_speeds_rad_s[0][1], result.final_branch_speeds_rad_s[1][1])
        self.assertGreater(result.final_state.speed_m_per_s, 0.0)
        self.assertGreater(result.final_state.position_m, 0.0)
        self.assertGreater(result.final_state.branch_connection_heat_j, 0.0)
        self.assertLessEqual(result.maximum_contact_utilization, 1.0)

    def test_split_grip_creates_independent_speeds_and_mirror_exchanges_branches(self) -> None:
        raw, _, config, powertrain = loaded()
        controls = raw["falsification_controls"]
        left_mu, right_mu = controls["split_grip_left_friction"], controls["split_grip_right_friction"]
        split = run_differential_drive(with_branch_friction(config, left=left_mu, right=right_mu), powertrain, **reference_arguments(raw))
        mirror = run_differential_drive(with_branch_friction(config, left=right_mu, right=left_mu), powertrain, **reference_arguments(raw))
        self.assertEqual(("finished", "finished"), (split.outcome, mirror.outcome))
        self.assertLess(split.final_state.differential_speed_rad_s, 0.0)
        self.assertGreater(mirror.final_state.differential_speed_rad_s, 0.0)
        self.assertGreater(split.maximum_differential_modal_energy_j, 0.0)
        self.assertAlmostEqual(split.final_branch_speeds_rad_s[0][1], mirror.final_branch_speeds_rad_s[1][1], places=12)
        self.assertAlmostEqual(split.final_branch_speeds_rad_s[1][1], mirror.final_branch_speeds_rad_s[0][1], places=12)
        self.assertAlmostEqual(split.final_state.speed_m_per_s, mirror.final_state.speed_m_per_s, places=12)
        self.assertAlmostEqual(split.final_state.position_m, mirror.final_state.position_m, places=12)

    def test_kinematic_modal_and_energy_residuals_are_bounded(self) -> None:
        raw, _, config, powertrain = loaded()
        controls = raw["falsification_controls"]
        split_config = with_branch_friction(config, left=controls["split_grip_left_friction"], right=controls["split_grip_right_friction"])
        result = run_differential_drive(split_config, powertrain, **reference_arguments(raw))
        self.assertLessEqual(result.maximum_abs_carrier_average_residual_rad_s, 1.0e-12)
        self.assertLessEqual(result.maximum_abs_modal_equation_residual_nm, 1.0e-9)
        self.assertLessEqual(result.maximum_abs_torque_residual_nm, 1.0e-9)
        self.assertLessEqual(result.maximum_abs_interface_energy_residual_j, 1.0e-9)
        self.assertLessEqual(result.maximum_global_relative_energy_residual, split_config.energy_relative_tolerance)
        self.assertAlmostEqual(
            result.initial_total_energy_j,
            total_differential_drive_accounted_energy_j(split_config, powertrain, result.final_state),
            delta=result.maximum_abs_global_energy_residual_j + 1.0e-8,
        )
        carrier = result.final_state.powertrain.output_speed_rad_s
        left, right = branch_speeds(split_config, result.final_state)
        self.assertAlmostEqual(carrier, 0.5 * (left + right), places=14)
        self.assertGreater(differential_modal_energy_j(split_config, result.final_state), 0.0)

    def test_zero_energy_cannot_create_drive_force_motion_or_modal_energy(self) -> None:
        raw, _, config, powertrain = loaded()
        result = run_differential_drive(config, powertrain, initial_storage_energy_j=0.0, **reference_arguments(raw))
        self.assertEqual("finished", result.outcome)
        self.assertEqual(0.0, result.final_state.speed_m_per_s)
        self.assertEqual(0.0, result.final_state.position_m)
        self.assertEqual(0.0, result.final_state.contact_body_work_j)
        self.assertEqual(0.0, result.final_state.differential_speed_rad_s)
        self.assertEqual(0.0, result.maximum_differential_modal_energy_j)

    def test_branch_overspeed_is_dnf_and_terminal_state_cannot_continue(self) -> None:
        raw, _, config, powertrain = loaded()
        limit = raw["falsification_controls"]["overspeed_control_maximum_branch_speed_rad_s"]
        failing = replace(config, maximum_branch_speed_rad_s=limit)
        result = run_differential_drive(failing, powertrain, **reference_arguments(raw))
        self.assertEqual("passed", result.status)
        self.assertEqual("DNF", result.outcome)
        self.assertEqual("differential_branch_overspeed", result.terminal_reason)
        self.assertEqual("failed", result.final_state.drive_subsystem_state)
        self.assertGreater(max(value for _, value in result.final_branch_speeds_rad_s), limit)
        with self.assertRaisesRegex(DifferentialDriveError, "DNF"):
            step_differential_drive(
                failing, powertrain, result.final_state, throttle=0.5,
                step_s=raw["reference_experiment"]["step_s"],
                initial_total_energy_j=result.initial_total_energy_j,
            )

    def test_half_step_refinement_is_within_frozen_bound(self) -> None:
        raw, _, config, powertrain = loaded()
        controls = raw["falsification_controls"]
        split_config = with_branch_friction(config, left=controls["split_grip_left_friction"], right=controls["split_grip_right_friction"])
        arguments = reference_arguments(raw)
        coarse = run_differential_drive(split_config, powertrain, **arguments)
        fine = run_differential_drive(split_config, powertrain, **{**arguments, "step_s": arguments["step_s"] / 2.0, "sample_stride": arguments["sample_stride"] * 2})
        values = (
            (coarse.final_state.speed_m_per_s, fine.final_state.speed_m_per_s),
            (coarse.final_state.position_m, fine.final_state.position_m),
            (coarse.final_state.differential_speed_rad_s, fine.final_state.differential_speed_rad_s),
            (coarse.final_state.slip_heat_j, fine.final_state.slip_heat_j),
            (coarse.final_state.branch_connection_heat_j, fine.final_state.branch_connection_heat_j),
        )
        for left, right in values:
            self.assertLessEqual(relative(left, right), split_config.refinement_relative_tolerance)

    def test_invalid_identity_geometry_split_and_numerics_fail_closed(self) -> None:
        raw, variant, base, support_raw, powertrain_raw = declarations()
        architecture = materialize_architecture_variant(base, variant)
        support = load_support_gate_config(support_raw)
        powertrain = load_powertrain_config(powertrain_raw)
        invalid_values = []
        value = deepcopy(raw); value["branches"][0]["rotational_inertia_kg_m2"] += 0.01; invalid_values.append(value)
        value = deepcopy(raw); value["branches"][0]["connection_efficiency"] = 1.0; invalid_values.append(value)
        value = deepcopy(raw); value["branches"][0]["contact_id"] = "rear_ground_contact"; invalid_values.append(value)
        value = deepcopy(raw); value["differential"]["maximum_branch_speed_rad_s"] = 151.0; invalid_values.append(value)
        value = deepcopy(raw); value["differential"]["nominal_left_torque_fraction"] = 0.6; value["differential"]["nominal_right_torque_fraction"] = 0.4; invalid_values.append(value)
        value = deepcopy(raw); value["numerical"]["energy_relative_tolerance"] = 0.0011; invalid_values.append(value)
        value = deepcopy(raw); value["branches"][0]["friction_coefficient"] = math.inf; invalid_values.append(value)
        for invalid in invalid_values:
            with self.subTest(invalid=invalid), self.assertRaises(DifferentialDriveError):
                load_differential_drive_config(invalid, powertrain=powertrain, architecture_raw=architecture, support_config=support)

    def test_replay_is_exact_and_grip_changes_identity(self) -> None:
        raw, _, config, powertrain = loaded()
        arguments = reference_arguments(raw)
        first = run_differential_drive(config, powertrain, **arguments)
        replay = run_differential_drive(config, powertrain, **arguments)
        changed = run_differential_drive(with_branch_friction(config, left=1.0, right=1.2), powertrain, **arguments)
        self.assertEqual(first, replay)
        self.assertEqual(first.result_sha256, replay.result_sha256)
        self.assertNotEqual(first.result_sha256, changed.result_sha256)


if __name__ == "__main__":
    unittest.main()
