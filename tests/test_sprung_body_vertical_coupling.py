from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from formula_ultimate.simulation.sprung_body_vertical_coupling import (
    RaisedCosineRoadProfile,
    SprungBodyVerticalError,
    conservation_accounted_energy_j,
    initial_sprung_body_vertical_state,
    load_sprung_body_vertical_config,
    run_sprung_body_vertical_coupling,
    with_tyre_damping_scale,
    with_tyre_stiffness_scale,
    with_vertical_steer,
)
from tests.test_transient_suspension_coupling import loaded as loaded_transient


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "vehicle" / "sprung_body_road_tyre_vertical_v1.json"


def loaded():
    _, architecture, transient, powertrain = loaded_transient()
    raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    config = load_sprung_body_vertical_config(raw, transient=transient, architecture_raw=architecture)
    return raw, architecture, config, powertrain


def relative(left: float, right: float) -> float:
    return abs(left - right) / max(abs(right), 1.0)


class SprungBodyVerticalCouplingTests(unittest.TestCase):
    def test_geometry_derived_sprung_properties_and_initial_budget(self) -> None:
        _, _, config, powertrain = loaded()
        self.assertAlmostEqual(245.95200000000003, config.sprung_mass_kg)
        self.assertAlmostEqual(4.218672483307425, config.sprung_roll_inertia_kg_m2)
        self.assertAlmostEqual(46.253188363933454, config.sprung_pitch_inertia_kg_m2)
        self.assertAlmostEqual(
            config.transient.coupled.vehicle_mass_kg,
            config.sprung_mass_kg + sum(item.unsprung_mass_kg for item in config.contacts),
        )
        state = initial_sprung_body_vertical_state(config, powertrain)
        self.assertAlmostEqual(
            powertrain.initial_storage_energy_j,
            conservation_accounted_energy_j(
                config, powertrain, state, tuple(0.0 for _ in config.contacts)
            ),
            places=8,
        )

    def test_flat_reference_finishes_with_coupled_body_modes(self) -> None:
        _, _, config, powertrain = loaded()
        result = run_sprung_body_vertical_coupling(config, powertrain, sample_stride=50)
        self.assertEqual(("passed", "finished", 500), (result.status, result.outcome, result.executed_steps))
        self.assertGreater(result.minimum_actual_normal_load_n, 0.0)
        self.assertGreater(result.maximum_abs_heave_m, 0.0)
        self.assertGreater(result.maximum_abs_pitch_rad, 0.0)
        self.assertGreater(result.maximum_abs_roll_rad, 0.0)
        self.assertLess(result.maximum_abs_suspension_travel_m, 0.05)

    def test_actual_tyre_load_is_used_by_horizontal_contact(self) -> None:
        _, _, config, powertrain = loaded()
        result = run_sprung_body_vertical_coupling(config, powertrain, sample_stride=1)
        for step in result.trace:
            actual = {item.contact_id: item.actual_normal_load_n for item in step.contacts}
            self.assertEqual(actual, dict(step.coupled.normal_loads_n))

    def test_generalized_equations_and_energy_close(self) -> None:
        _, _, config, powertrain = loaded()
        result = run_sprung_body_vertical_coupling(config, powertrain, sample_stride=20)
        self.assertLess(result.maximum_abs_equation_residual, 1.0e-9)
        self.assertLess(result.maximum_abs_vertical_energy_residual_j, 1.0e-9)
        self.assertLess(result.maximum_total_global_relative_energy_residual, 1.0e-8)
        self.assertGreater(result.final_state.inertial_work_j, 0.0)

    def test_zero_steer_is_symmetric_and_opposite_steer_mirrors(self) -> None:
        _, _, config, powertrain = loaded()
        zero = run_sprung_body_vertical_coupling(with_vertical_steer(config, 0.0), powertrain, sample_stride=100)
        positive = run_sprung_body_vertical_coupling(config, powertrain, sample_stride=100)
        negative = run_sprung_body_vertical_coupling(
            with_vertical_steer(config, -config.transient.coupled.steer_angle_rad), powertrain, sample_stride=100
        )
        self.assertAlmostEqual(0.0, zero.final_state.coordinates[2], places=15)
        self.assertAlmostEqual(zero.final_state.coordinates[3], zero.final_state.coordinates[5], places=15)
        self.assertAlmostEqual(positive.final_state.coordinates[2], -negative.final_state.coordinates[2], places=15)
        self.assertAlmostEqual(positive.final_state.coordinates[3], negative.final_state.coordinates[5], places=15)
        self.assertAlmostEqual(positive.final_state.coordinates[5], negative.final_state.coordinates[3], places=15)
        self.assertAlmostEqual(
            positive.final_state.coupled.planar.y_position_m,
            -negative.final_state.coupled.planar.y_position_m,
            places=15,
        )

    def test_road_bump_and_spatial_mirror_exchange_response(self) -> None:
        raw, _, config, powertrain = loaded()
        controls = raw["falsification_controls"]
        left_profile = RaisedCosineRoadProfile(
            controls["bump_contact_id"], controls["bump_amplitude_m"],
            controls["bump_start_s"], controls["bump_duration_s"],
        )
        right_profile = RaisedCosineRoadProfile(
            "right_ground_contact", controls["bump_amplitude_m"],
            controls["bump_start_s"], controls["bump_duration_s"],
        )
        left = run_sprung_body_vertical_coupling(config, powertrain, road_profiles=(left_profile,), sample_stride=100)
        right = run_sprung_body_vertical_coupling(
            with_vertical_steer(config, -config.transient.coupled.steer_angle_rad),
            powertrain, road_profiles=(right_profile,), sample_stride=100,
        )
        self.assertEqual("finished", left.outcome)
        self.assertNotEqual(0.0, left.final_state.road_work_j)
        self.assertAlmostEqual(left.final_state.road_work_j, right.final_state.road_work_j, places=12)
        self.assertAlmostEqual(left.maximum_abs_roll_rad, right.maximum_abs_roll_rad, places=12)
        self.assertAlmostEqual(left.final_state.coordinates[2], -right.final_state.coordinates[2], places=15)

    def test_zero_tyre_damping_and_soft_tyre_are_observable(self) -> None:
        raw, _, config, powertrain = loaded()
        reference = run_sprung_body_vertical_coupling(config, powertrain, sample_stride=100)
        undamped = run_sprung_body_vertical_coupling(
            with_tyre_damping_scale(config, 0.0), powertrain, sample_stride=100
        )
        soft = run_sprung_body_vertical_coupling(
            with_tyre_stiffness_scale(config, raw["falsification_controls"]["soft_tyre_scale"]),
            powertrain, sample_stride=100,
        )
        self.assertEqual(0.0, undamped.final_state.tyre_damping_heat_j)
        self.assertGreater(reference.final_state.tyre_damping_heat_j, 0.0)
        self.assertNotEqual(reference.maximum_abs_heave_m, soft.maximum_abs_heave_m)

    def test_contact_loss_and_travel_exhaustion_are_not_clipped(self) -> None:
        raw, _, config, powertrain = loaded()
        controls = raw["falsification_controls"]
        drop = RaisedCosineRoadProfile(
            controls["bump_contact_id"], controls["contact_loss_amplitude_m"],
            controls["contact_loss_start_s"], controls["contact_loss_duration_s"],
        )
        loss = run_sprung_body_vertical_coupling(config, powertrain, road_profiles=(drop,))
        q = (controls["travel_state_initial_heave_m"], 0.0, 0.0, 0.0, 0.0, 0.0)
        v = (controls["travel_state_initial_heave_velocity_m_per_s"], 0.0, 0.0, 0.0, 0.0, 0.0)
        travel = run_sprung_body_vertical_coupling(
            config, powertrain, initial_coordinates=q, initial_velocities=v
        )
        self.assertEqual(("passed", "DNF", "contact_loss"), (loss.status, loss.outcome, loss.terminal_reason))
        self.assertLessEqual(loss.minimum_actual_normal_load_n, 0.0)
        self.assertFalse(loss.trace[-1].committed)
        self.assertEqual(("passed", "DNF", "suspension_travel"), (travel.status, travel.outcome, travel.terminal_reason))
        self.assertGreater(travel.maximum_abs_suspension_travel_m, 0.05)
        self.assertTrue(travel.trace[-1].committed)
        self.assertEqual(powertrain.initial_storage_energy_j, travel.initial_total_energy_j)
        self.assertGreater(travel.initial_vertical_energy_j, 0.0)

    def test_large_road_ramp_exposes_first_physical_limit(self) -> None:
        raw, _, config, powertrain = loaded()
        controls = raw["falsification_controls"]
        profile = RaisedCosineRoadProfile(
            controls["bump_contact_id"], controls["travel_failure_amplitude_m"],
            controls["travel_failure_start_s"], controls["travel_failure_duration_s"],
            controls["travel_failure_profile_shape"],
        )
        result = run_sprung_body_vertical_coupling(config, powertrain, road_profiles=(profile,))
        self.assertEqual(("passed", "DNF", "contact_loss"), (result.status, result.outcome, result.terminal_reason))
        self.assertLess(result.minimum_actual_normal_load_n, 0.0)

    def test_half_step_refinement_is_within_gate(self) -> None:
        _, _, config, powertrain = loaded()
        base = run_sprung_body_vertical_coupling(config, powertrain, sample_stride=100)
        refined = run_sprung_body_vertical_coupling(
            config, powertrain, time_step_s=config.transient.coupled.time_step_s / 2.0, sample_stride=200
        )
        differences = (
            relative(base.maximum_abs_heave_m, refined.maximum_abs_heave_m),
            relative(base.maximum_abs_pitch_rad, refined.maximum_abs_pitch_rad),
            relative(base.maximum_abs_roll_rad, refined.maximum_abs_roll_rad),
            relative(base.maximum_abs_suspension_travel_m, refined.maximum_abs_suspension_travel_m),
            relative(base.final_state.suspension_damping_heat_j, refined.final_state.suspension_damping_heat_j),
            relative(base.final_state.tyre_damping_heat_j, refined.final_state.tyre_damping_heat_j),
        )
        self.assertLessEqual(max(differences), config.refinement_relative_tolerance)

    def test_invalid_contracts_profiles_and_initial_state_fail_closed(self) -> None:
        raw, architecture, config, powertrain = loaded()
        invalid = deepcopy(raw)
        invalid["model_version"] = "wrong"
        with self.assertRaises(SprungBodyVerticalError):
            load_sprung_body_vertical_config(invalid, transient=config.transient, architecture_raw=architecture)
        invalid = deepcopy(raw)
        invalid["tyre_vertical_profiles"]["powered_contact"]["damping_ratio"] = 2.1
        with self.assertRaises(SprungBodyVerticalError):
            load_sprung_body_vertical_config(invalid, transient=config.transient, architecture_raw=architecture)
        with self.assertRaises(SprungBodyVerticalError):
            RaisedCosineRoadProfile("left_ground_contact", 0.1, 0.0, 0.1, "wrong")
        with self.assertRaises(SprungBodyVerticalError):
            run_sprung_body_vertical_coupling(
                config, powertrain,
                road_profiles=(RaisedCosineRoadProfile("unknown", 0.1, 0.0, 0.1),),
            )
        with self.assertRaises(SprungBodyVerticalError):
            initial_sprung_body_vertical_state(
                config, powertrain, coordinates=(-0.051, 0.0, 0.0, 0.0, 0.0, 0.0)
            )

    def test_exact_replay_and_road_command_change_identity(self) -> None:
        raw, _, config, powertrain = loaded()
        first = run_sprung_body_vertical_coupling(config, powertrain, sample_stride=25)
        replay = run_sprung_body_vertical_coupling(config, powertrain, sample_stride=25)
        controls = raw["falsification_controls"]
        bump = RaisedCosineRoadProfile(
            controls["bump_contact_id"], controls["bump_amplitude_m"],
            controls["bump_start_s"], controls["bump_duration_s"],
        )
        changed = run_sprung_body_vertical_coupling(
            config, powertrain, road_profiles=(bump,), sample_stride=25
        )
        self.assertEqual(first, replay)
        self.assertNotEqual(first.result_sha256, changed.result_sha256)


if __name__ == "__main__":
    unittest.main()
