from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from formula_ultimate.simulation.coupled_planar_differential import (
    load_coupled_planar_config,
    run_coupled_planar_differential,
)
from formula_ultimate.simulation.differential_drive_coupling import (
    load_differential_drive_config,
)
from formula_ultimate.simulation.planar_support_gate import (
    load_support_gate_config,
    materialize_architecture_variant,
)
from formula_ultimate.simulation.powertrain_dynamics import load_powertrain_config
from formula_ultimate.simulation.transient_suspension_coupling import (
    TransientSuspensionError,
    conservation_accounted_energy_j,
    initial_transient_suspension_state,
    load_transient_suspension_config,
    run_transient_suspension_coupling,
    total_suspension_energy_j,
    with_damping_scale,
    with_stiffness_scale,
    with_transient_steer,
)


ROOT = Path(__file__).resolve().parents[1]
VEHICLE = ROOT / "config" / "vehicle"


def loaded():
    raw = json.loads((VEHICLE / "transient_suspension_coupling_v1.json").read_text(encoding="utf-8"))
    coupled_raw = json.loads((VEHICLE / raw["coupled_planar_source"]).read_text(encoding="utf-8"))
    differential_raw = json.loads((VEHICLE / coupled_raw["differential_source"]).read_text(encoding="utf-8"))
    variant_raw = json.loads((VEHICLE / differential_raw["architecture_variant_source"]).read_text(encoding="utf-8"))
    base_raw = json.loads((VEHICLE / variant_raw["base_architecture_source"]).read_text(encoding="utf-8"))
    support_raw = json.loads((VEHICLE / differential_raw["support_gate_source"]).read_text(encoding="utf-8"))
    powertrain_raw = json.loads((VEHICLE / differential_raw["powertrain_source"]).read_text(encoding="utf-8"))
    architecture = materialize_architecture_variant(base_raw, variant_raw)
    support = load_support_gate_config(support_raw)
    powertrain = load_powertrain_config(powertrain_raw)
    differential = load_differential_drive_config(
        differential_raw,
        powertrain=powertrain,
        architecture_raw=architecture,
        support_config=support,
    )
    coupled = load_coupled_planar_config(
        coupled_raw,
        differential=differential,
        architecture_raw=architecture,
        support_config=support,
    )
    config = load_transient_suspension_config(raw, coupled=coupled, architecture_raw=architecture)
    return raw, architecture, config, powertrain


def relative(left: float, right: float) -> float:
    return abs(left - right) / max(abs(right), 1.0)


class TransientSuspensionCouplingTests(unittest.TestCase):
    def test_loader_derives_effective_mass_and_initial_energy_budget(self) -> None:
        _, _, config, powertrain = loaded()
        masses = {item.component_id: item.effective_mass_kg for item in config.units}
        self.assertAlmostEqual(13.30024665823775, masses["left_ground_unit"])
        self.assertAlmostEqual(13.30024665823775, masses["right_ground_unit"])
        self.assertAlmostEqual(4.342937684322531, masses["rear_ground_support"])
        self.assertTrue(all(item.damping_n_s_per_m > 0.0 for item in config.units))
        state = initial_transient_suspension_state(config, powertrain)
        self.assertEqual(0.0, total_suspension_energy_j(config, state))
        self.assertAlmostEqual(
            powertrain.initial_storage_energy_j,
            conservation_accounted_energy_j(config, powertrain, state),
            places=8,
        )

    def test_reference_finishes_and_actual_load_changes_horizontal_response(self) -> None:
        _, _, config, powertrain = loaded()
        transient = run_transient_suspension_coupling(config, powertrain, sample_stride=50)
        rigid = run_coupled_planar_differential(config.coupled, powertrain, sample_stride=50)
        self.assertEqual(("passed", "finished"), (transient.status, transient.outcome))
        self.assertEqual(500, transient.executed_steps)
        self.assertGreater(transient.minimum_actual_normal_load_n, 0.0)
        self.assertGreater(transient.maximum_target_actual_load_difference_n, 1.0)
        self.assertNotEqual(
            rigid.final_state.planar.y_position_m,
            transient.final_state.coupled.planar.y_position_m,
        )
        self.assertLess(transient.maximum_abs_travel_m, 0.05)

    def test_contact_actual_load_is_the_load_used_by_tyre_transaction(self) -> None:
        _, _, config, powertrain = loaded()
        result = run_transient_suspension_coupling(config, powertrain, sample_stride=1)
        for step in result.trace:
            actual = {item.contact_id: item.actual_normal_load_n for item in step.contacts}
            used = dict(step.coupled.normal_loads_n)
            self.assertEqual(actual, used)
            for item in step.contacts:
                self.assertLessEqual(abs(item.force_residual_n), 1.0e-9)
                self.assertLessEqual(abs(item.energy_residual_j), 1.0e-9)

    def test_zero_steer_preserves_left_right_suspension_symmetry(self) -> None:
        _, _, config, powertrain = loaded()
        result = run_transient_suspension_coupling(
            with_transient_steer(config, 0.0), powertrain, sample_stride=100
        )
        contacts = {item.contact_id: item for item in result.final_state.contacts}
        left = contacts["left_ground_contact"]
        right = contacts["right_ground_contact"]
        self.assertEqual(left.travel_m, right.travel_m)
        self.assertEqual(left.velocity_m_per_s, right.velocity_m_per_s)
        self.assertEqual(0.0, result.final_state.coupled.planar.y_position_m)
        self.assertEqual(0.0, result.final_state.coupled.planar.yaw_rate_rad_per_s)

    def test_opposite_steer_mirrors_vertical_and_planar_states(self) -> None:
        _, _, config, powertrain = loaded()
        positive = run_transient_suspension_coupling(config, powertrain, sample_stride=100)
        negative = run_transient_suspension_coupling(
            with_transient_steer(config, -config.coupled.steer_angle_rad),
            powertrain,
            sample_stride=100,
        )
        pos = {item.contact_id: item for item in positive.final_state.contacts}
        neg = {item.contact_id: item for item in negative.final_state.contacts}
        self.assertEqual(pos["left_ground_contact"].travel_m, neg["right_ground_contact"].travel_m)
        self.assertEqual(pos["right_ground_contact"].travel_m, neg["left_ground_contact"].travel_m)
        self.assertEqual(pos["left_ground_contact"].velocity_m_per_s, neg["right_ground_contact"].velocity_m_per_s)
        self.assertEqual(
            positive.final_state.coupled.planar.y_position_m,
            -negative.final_state.coupled.planar.y_position_m,
        )
        self.assertEqual(
            positive.final_state.coupled.planar.yaw_rate_rad_per_s,
            -negative.final_state.coupled.planar.yaw_rate_rad_per_s,
        )

    def test_zero_damping_and_soft_spring_controls_are_observable(self) -> None:
        raw, _, config, powertrain = loaded()
        reference = run_transient_suspension_coupling(config, powertrain, sample_stride=100)
        undamped = run_transient_suspension_coupling(
            with_damping_scale(config, 0.0), powertrain, sample_stride=100
        )
        soft = run_transient_suspension_coupling(
            with_stiffness_scale(config, raw["falsification_controls"]["stiffness_scale"]),
            powertrain,
            sample_stride=100,
        )
        self.assertEqual(0.0, undamped.final_state.suspension_damping_heat_j)
        self.assertGreater(reference.final_state.suspension_damping_heat_j, 0.0)
        self.assertNotEqual(reference.maximum_abs_travel_m, soft.maximum_abs_travel_m)
        self.assertGreater(soft.maximum_abs_travel_m, reference.maximum_abs_travel_m)

    def test_contact_loss_and_travel_controls_fail_without_clipping(self) -> None:
        raw, _, config, powertrain = loaded()
        controls = raw["falsification_controls"]
        loss = run_transient_suspension_coupling(
            config,
            powertrain,
            initial_contact_states={
                controls["contact_loss_contact_id"]: (
                    controls["contact_loss_initial_travel_m"],
                    controls["contact_loss_initial_velocity_m_per_s"],
                )
            },
        )
        travel = run_transient_suspension_coupling(
            config,
            powertrain,
            initial_contact_states={
                controls["travel_failure_contact_id"]: (
                    controls["travel_failure_initial_travel_m"],
                    controls["travel_failure_initial_velocity_m_per_s"],
                )
            },
        )
        self.assertEqual(("passed", "DNF", "contact_loss"), (loss.status, loss.outcome, loss.terminal_reason))
        self.assertLessEqual(loss.minimum_actual_normal_load_n, 0.0)
        self.assertFalse(loss.trace[-1].committed)
        self.assertEqual(("passed", "DNF", "suspension_travel"), (travel.status, travel.outcome, travel.terminal_reason))
        self.assertGreater(travel.maximum_abs_travel_m, 0.05)
        self.assertTrue(travel.trace[-1].committed)
        self.assertAlmostEqual(powertrain.initial_storage_energy_j, loss.initial_total_energy_j, places=8)
        self.assertAlmostEqual(powertrain.initial_storage_energy_j, travel.initial_total_energy_j, places=8)
        self.assertGreater(loss.initial_suspension_energy_j, 0.0)
        self.assertGreater(travel.initial_suspension_energy_j, 0.0)

    def test_horizontal_and_vertical_energy_residuals_are_bounded(self) -> None:
        _, _, config, powertrain = loaded()
        result = run_transient_suspension_coupling(config, powertrain, sample_stride=20)
        self.assertLess(result.maximum_abs_force_residual_n, 1.0e-9)
        self.assertLess(result.maximum_abs_suspension_energy_residual_j, 1.0e-9)
        self.assertLess(result.maximum_total_global_relative_energy_residual, 1.0e-8)
        self.assertGreater(result.final_state.suspension_boundary_work_j, 0.0)
        self.assertGreater(result.final_state.suspension_damping_heat_j, 0.0)

    def test_half_step_refinement_is_within_frozen_bound(self) -> None:
        _, _, config, powertrain = loaded()
        base = run_transient_suspension_coupling(config, powertrain, sample_stride=100)
        refined = run_transient_suspension_coupling(
            config, powertrain, time_step_s=config.coupled.time_step_s / 2.0, sample_stride=200
        )
        values = (
            relative(base.final_state.coupled.planar.x_position_m, refined.final_state.coupled.planar.x_position_m),
            relative(base.final_state.coupled.planar.y_position_m, refined.final_state.coupled.planar.y_position_m),
            relative(base.final_state.coupled.planar.yaw_rate_rad_per_s, refined.final_state.coupled.planar.yaw_rate_rad_per_s),
            relative(base.maximum_abs_travel_m, refined.maximum_abs_travel_m),
            relative(base.final_state.suspension_damping_heat_j, refined.final_state.suspension_damping_heat_j),
        )
        self.assertLessEqual(max(values), config.refinement_relative_tolerance)

    def test_invalid_declarations_and_initial_states_fail_closed(self) -> None:
        raw, architecture, config, powertrain = loaded()
        invalid = deepcopy(raw)
        invalid["model_version"] = "wrong"
        with self.assertRaises(TransientSuspensionError):
            load_transient_suspension_config(invalid, coupled=config.coupled, architecture_raw=architecture)
        invalid = deepcopy(raw)
        invalid["profiles"]["powered_contact"]["damping_ratio"] = 2.1
        with self.assertRaises(TransientSuspensionError):
            load_transient_suspension_config(invalid, coupled=config.coupled, architecture_raw=architecture)
        invalid = deepcopy(raw)
        invalid["numerical"]["force_relative_tolerance"] = 1.0e-6
        with self.assertRaises(TransientSuspensionError):
            load_transient_suspension_config(invalid, coupled=config.coupled, architecture_raw=architecture)
        with self.assertRaises(TransientSuspensionError):
            initial_transient_suspension_state(config, powertrain, initial_contact_states={"unknown": (0.0, 0.0)})
        with self.assertRaises(TransientSuspensionError):
            initial_transient_suspension_state(
                config,
                powertrain,
                initial_contact_states={"left_ground_contact": (0.051, 0.0)},
            )

    def test_exact_replay_and_command_identity(self) -> None:
        _, _, config, powertrain = loaded()
        first = run_transient_suspension_coupling(config, powertrain, sample_stride=25)
        replay = run_transient_suspension_coupling(config, powertrain, sample_stride=25)
        changed = run_transient_suspension_coupling(
            with_transient_steer(config, 0.0), powertrain, sample_stride=25
        )
        self.assertEqual(first, replay)
        self.assertEqual(first.result_sha256, replay.result_sha256)
        self.assertNotEqual(first.result_sha256, changed.result_sha256)


if __name__ == "__main__":
    unittest.main()
