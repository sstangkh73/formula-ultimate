from __future__ import annotations

from dataclasses import replace
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.physics.corridor import load_corridors
from formula_ultimate.simulation.closed_loop_corridor_controller import (
    ClosedLoopControllerError,
    load_closed_loop_controller_config,
    project_to_corridor,
    run_closed_loop_controller,
    steering_command,
    with_feedback_gains,
)
from tests.test_sprung_body_vertical_coupling import loaded as loaded_vertical


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "vehicle" / "closed_loop_corridor_controller_v1.json"
CORRIDOR_PATH = ROOT / "config" / "circuits" / "closed_loop_controller_corridors_v1.json"


def loaded():
    _, _, vertical, powertrain = loaded_vertical()
    raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    corridors = {item.corridor_id: item for item in load_corridors(CORRIDOR_PATH)}
    config = load_closed_loop_controller_config(raw)
    return raw, config, corridors, vertical, powertrain


class ClosedLoopCorridorControllerTests(unittest.TestCase):
    def test_projection_matches_analytical_circle_with_bounded_chord_error(self) -> None:
        _, config, corridors, _, _ = loaded()
        radius, angle = 50.0, 0.4
        x, y = radius * math.sin(angle), radius * (1.0 - math.cos(angle))
        projection = project_to_corridor(
            corridors[config.corridor_id], x, y, station_spacing_m=config.station_spacing_m
        )
        self.assertLess(projection.distance_m, config.projection_distance_tolerance_m)
        self.assertAlmostEqual(radius * angle, projection.progress_m, places=3)
        self.assertLess(
            abs(angle - projection.desired_heading_rad),
            config.projection_distance_tolerance_m,
        )

    def test_reference_finishes_and_feedback_beats_zero_feedback(self) -> None:
        _, config, corridors, vertical, powertrain = loaded()
        reference = run_closed_loop_controller(
            config, vertical, powertrain, corridors[config.corridor_id], sample_stride=50
        )
        zero = run_closed_loop_controller(
            with_feedback_gains(config, heading_gain=0.0, cross_track_gain_rad_per_m=0.0),
            vertical, powertrain, corridors[config.corridor_id], sample_stride=50,
        )
        self.assertEqual(("passed", "finished"), (reference.status, reference.outcome))
        self.assertGreater(reference.minimum_actual_normal_load_n, 0.0)
        self.assertLess(reference.maximum_abs_suspension_travel_m, 0.05)
        self.assertLess(
            abs(reference.final_cross_track_error_m), abs(zero.final_cross_track_error_m)
        )

    def test_straight_zero_error_commands_zero_steer(self) -> None:
        raw, _, corridors, vertical, powertrain = loaded()
        straight_id = raw["straight_corridor_id"]
        config = replace(
            load_closed_loop_controller_config(raw, corridor_id=straight_id),
            initial_lateral_error_m=0.0,
            initial_heading_error_rad=0.0,
        )
        result = run_closed_loop_controller(
            config, vertical, powertrain, corridors[straight_id], sample_stride=100
        )
        self.assertEqual("finished", result.outcome)
        self.assertLess(
            max(abs(step.command.applied_steer_rad) for step in result.trace), 1.0e-15
        )
        self.assertAlmostEqual(0.0, result.final_cross_track_error_m, places=15)

    def test_left_right_corridors_and_disturbances_mirror(self) -> None:
        raw, left_config, corridors, vertical, powertrain = loaded()
        right_id = raw["mirror_corridor_id"]
        right_config = replace(
            load_closed_loop_controller_config(raw, corridor_id=right_id),
            initial_lateral_error_m=-left_config.initial_lateral_error_m,
            initial_heading_error_rad=-left_config.initial_heading_error_rad,
        )
        left = run_closed_loop_controller(
            left_config, vertical, powertrain, corridors[left_config.corridor_id], sample_stride=50
        )
        right = run_closed_loop_controller(
            right_config, vertical, powertrain, corridors[right_id], sample_stride=50
        )
        self.assertAlmostEqual(left.final_cross_track_error_m, -right.final_cross_track_error_m, places=12)
        self.assertAlmostEqual(
            left.final_state.coupled.planar.y_position_m,
            -right.final_state.coupled.planar.y_position_m,
            places=12,
        )
        self.assertAlmostEqual(
            left.final_state.coupled.planar.yaw_rate_rad_per_s,
            -right.final_state.coupled.planar.yaw_rate_rad_per_s,
            places=12,
        )

    def test_saturation_and_departure_are_explicit(self) -> None:
        raw, config, corridors, vertical, powertrain = loaded()
        controls = raw["falsification_controls"]
        saturated = run_closed_loop_controller(
            replace(config, initial_lateral_error_m=controls["saturation_initial_lateral_error_m"]),
            vertical, powertrain, corridors[config.corridor_id], sample_stride=50,
        )
        departed = run_closed_loop_controller(
            replace(config, initial_lateral_error_m=controls["departure_initial_lateral_error_m"]),
            vertical, powertrain, corridors[config.corridor_id], sample_stride=50,
        )
        self.assertGreater(saturated.steering_saturation_count, 0)
        self.assertEqual(("DNF", "corridor_departure", 0), (
            departed.outcome, departed.terminal_reason, departed.executed_steps
        ))

    def test_wrong_sign_control_is_worse_than_reference(self) -> None:
        raw, config, corridors, vertical, powertrain = loaded()
        reference = run_closed_loop_controller(
            config, vertical, powertrain, corridors[config.corridor_id], sample_stride=100
        )
        wrong = run_closed_loop_controller(
            with_feedback_gains(
                config,
                cross_track_gain_rad_per_m=raw["falsification_controls"][
                    "wrong_sign_cross_track_gain_rad_per_m"
                ],
            ),
            vertical, powertrain, corridors[config.corridor_id], sample_stride=100,
        )
        self.assertGreater(
            abs(wrong.final_cross_track_error_m), abs(reference.final_cross_track_error_m)
        )

    def test_commands_are_bounded_and_actual_load_reaches_tyre_model(self) -> None:
        _, config, corridors, vertical, powertrain = loaded()
        result = run_closed_loop_controller(
            config, vertical, powertrain, corridors[config.corridor_id], sample_stride=1
        )
        for step in result.trace:
            self.assertLessEqual(abs(step.command.applied_steer_rad), config.maximum_steer_angle_rad)
            self.assertEqual(
                dict(step.vertical.coupled.normal_loads_n),
                {item.contact_id: item.actual_normal_load_n for item in step.vertical.contacts},
            )

    def test_half_step_refinement_and_exact_replay(self) -> None:
        _, config, corridors, vertical, powertrain = loaded()
        first = run_closed_loop_controller(
            config, vertical, powertrain, corridors[config.corridor_id], sample_stride=50
        )
        replay = run_closed_loop_controller(
            config, vertical, powertrain, corridors[config.corridor_id], sample_stride=50
        )
        refined = run_closed_loop_controller(
            replace(config, time_step_s=config.time_step_s / 2.0),
            vertical, powertrain, corridors[config.corridor_id], sample_stride=100,
        )
        difference = abs(first.final_cross_track_error_m - refined.final_cross_track_error_m)
        self.assertEqual(first, replay)
        self.assertLessEqual(difference, config.refinement_relative_tolerance)

    def test_invalid_config_identity_geometry_and_runtime_fail_closed(self) -> None:
        raw, config, corridors, vertical, powertrain = loaded()
        invalid = dict(raw)
        invalid["model_version"] = "wrong"
        with self.assertRaises(ClosedLoopControllerError):
            load_closed_loop_controller_config(invalid)
        invalid = json.loads(json.dumps(raw))
        invalid["controller"]["heading_gain"] = -1.0
        with self.assertRaises(ClosedLoopControllerError):
            load_closed_loop_controller_config(invalid)
        with self.assertRaises(ClosedLoopControllerError):
            run_closed_loop_controller(
                config, vertical, powertrain, corridors[raw["mirror_corridor_id"]]
            )
        with self.assertRaises(ClosedLoopControllerError):
            steering_command(
                config, corridors[config.corridor_id], wheelbase_m=0.0,
                x_m=0.0, y_m=0.0, heading_rad=0.0,
            )


if __name__ == "__main__":
    unittest.main()
