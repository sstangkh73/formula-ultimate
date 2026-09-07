from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import unittest

from formula_ultimate.physics.corridor import load_corridors
from formula_ultimate.simulation.closed_loop_corridor_controller import (
    load_closed_loop_controller_config,
    run_closed_loop_controller,
)
from formula_ultimate.simulation.integrated_lap_gate import (
    IntegratedLapGateError,
    load_integrated_lap_gate_config,
    run_integrated_lap_gate,
)
from formula_ultimate.simulation.linkage_motion_ratio import (
    LinkageMotionRatioError,
    apply_linkage_motion_ratios,
    derive_motion_ratio,
    load_linkage_motion_ratio_config,
)
from formula_ultimate.simulation.sprung_body_vertical_coupling import RaisedCosineRoadProfile
from tests.test_sprung_body_vertical_coupling import loaded as loaded_vertical


ROOT = Path(__file__).resolve().parents[1]
LAP_PATH = ROOT / "config" / "vehicle" / "integrated_level0_lap_gate_v1.json"
CONTROLLER_PATH = ROOT / "config" / "vehicle" / "closed_loop_corridor_controller_v1.json"
LINKAGE_PATH = ROOT / "config" / "vehicle" / "geometry_linkage_motion_ratio_v1.json"
CORRIDOR_PATH = ROOT / "config" / "circuits" / "closed_loop_controller_corridors_v1.json"
WORK074_REFERENCE_SHA256 = "ab4470e28004cc78f87288a4ab2a7828881514362d8dffbb7d5326cdff5a8c6d"
WORK075_APPLICATION_SHA256 = "51b6255347e4a6a59428ee309f4f78c8e981baa437386bdcf3505df9d8403487"


def loaded(corridor_id: str | None = None):
    _, _, vertical, powertrain = loaded_vertical()
    controller_raw = json.loads(CONTROLLER_PATH.read_text(encoding="utf-8"))
    linkage_raw = json.loads(LINKAGE_PATH.read_text(encoding="utf-8"))
    lap_raw = json.loads(LAP_PATH.read_text(encoding="utf-8"))
    controller = load_closed_loop_controller_config(controller_raw)
    linkage = apply_linkage_motion_ratios(
        load_linkage_motion_ratio_config(linkage_raw), vertical
    )
    config = load_integrated_lap_gate_config(
        lap_raw, controller_source=controller, corridor_id=corridor_id
    )
    corridors = {item.corridor_id: item for item in load_corridors(CORRIDOR_PATH)}
    return lap_raw, controller_raw, linkage_raw, config, linkage, corridors, powertrain


class IntegratedLapGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        raw, controller_raw, linkage_raw, config, linkage, corridors, powertrain = loaded()
        cls.raw = raw
        cls.controller_raw = controller_raw
        cls.linkage_raw = linkage_raw
        cls.config = config
        cls.linkage = linkage
        cls.corridors = corridors
        cls.powertrain = powertrain
        cls.reference = run_integrated_lap_gate(
            config,
            linkage.transformed_vertical,
            powertrain,
            corridors[config.corridor_id],
            sample_stride=250,
        )

    def test_reference_completes_exact_spatially_closed_lap(self) -> None:
        result = self.reference
        self.assertEqual(("passed", "finished", "lap_complete"), (
            result.status, result.outcome, result.terminal_reason
        ))
        self.assertEqual(result.target_progress_m, result.credited_progress_m)
        self.assertIsNotNone(result.finish)
        assert result.finish is not None
        self.assertLessEqual(
            result.finish.position_closure_residual_m,
            self.config.finish_position_tolerance_m,
        )
        self.assertLessEqual(
            result.finish.heading_closure_residual_rad,
            self.config.finish_heading_tolerance_rad,
        )
        self.assertGreater(result.minimum_actual_normal_load_n, 0.0)
        self.assertLess(result.maximum_abs_suspension_travel_m, 0.0625)

    def test_progress_is_bounded_by_spatial_motion(self) -> None:
        self.assertLessEqual(
            self.reference.maximum_abs_progress_spatial_residual_m,
            self.config.progress_spatial_residual_tolerance_m,
        )
        for step in self.reference.trace:
            self.assertLessEqual(
                abs(step.progress_spatial_residual_m),
                self.config.progress_spatial_residual_tolerance_m,
            )

    def test_exact_replay_and_upstream_identities(self) -> None:
        replay = run_integrated_lap_gate(
            self.config,
            self.linkage.transformed_vertical,
            self.powertrain,
            self.corridors[self.config.corridor_id],
            sample_stride=250,
        )
        _, _, vertical, _ = loaded_vertical()
        short = run_closed_loop_controller(
            load_closed_loop_controller_config(self.controller_raw),
            vertical,
            self.powertrain,
            self.corridors[self.controller_raw["reference_corridor_id"]],
            sample_stride=25,
        )
        self.assertEqual(self.reference, replay)
        self.assertEqual(WORK074_REFERENCE_SHA256, short.result_sha256)
        self.assertEqual(WORK075_APPLICATION_SHA256, self.linkage.application_sha256)

    def test_opposite_direction_lap_mirrors(self) -> None:
        mirror_id = self.raw["mirror_corridor_id"]
        _, _, _, config, linkage, corridors, powertrain = loaded(mirror_id)
        config = replace(
            config,
            controller=replace(
                config.controller,
                initial_heading_error_rad=-self.config.controller.initial_heading_error_rad,
            ),
        )
        mirror = run_integrated_lap_gate(
            config, linkage.transformed_vertical, powertrain, corridors[mirror_id],
            sample_stride=250,
        )
        self.assertEqual("finished", mirror.outcome)
        self.assertAlmostEqual(self.reference.elapsed_time_s, mirror.elapsed_time_s, places=9)
        self.assertAlmostEqual(
            self.reference.final_state.coupled.planar.y_position_m,
            -mirror.final_state.coupled.planar.y_position_m,
            places=8,
        )

    def test_open_loop_narrow_corridor_and_timeout_fail_causally(self) -> None:
        open_loop = run_integrated_lap_gate(
            self.config,
            self.linkage.transformed_vertical,
            self.powertrain,
            self.corridors[self.config.corridor_id],
            controller_enabled=False,
            sample_stride=100,
        )
        narrow_width = self.raw["falsification_controls"]["narrow_half_width_m"]
        corridor = self.corridors[self.config.corridor_id]
        narrow = replace(
            corridor,
            segments=tuple(
                replace(item, width_left_m=narrow_width, width_right_m=narrow_width)
                for item in corridor.segments
            ),
        )
        narrow_result = run_integrated_lap_gate(
            self.config, self.linkage.transformed_vertical, self.powertrain, narrow,
            sample_stride=100,
        )
        timeout = run_integrated_lap_gate(
            replace(
                self.config,
                timeout_s=self.raw["falsification_controls"]["timeout_s"],
            ),
            self.linkage.transformed_vertical,
            self.powertrain,
            corridor,
            sample_stride=100,
        )
        self.assertEqual("corridor_departure", open_loop.terminal_reason)
        self.assertEqual("corridor_departure", narrow_result.terminal_reason)
        self.assertEqual("timeout", timeout.terminal_reason)

    def test_contact_loss_precedes_any_lap_credit(self) -> None:
        controls = self.raw["falsification_controls"]
        result = run_integrated_lap_gate(
            self.config,
            self.linkage.transformed_vertical,
            self.powertrain,
            self.corridors[self.config.corridor_id],
            road_profiles=(RaisedCosineRoadProfile(
                controls["contact_loss_contact_id"],
                controls["contact_loss_amplitude_m"],
                controls["contact_loss_start_s"],
                controls["contact_loss_duration_s"],
            ),),
            sample_stride=1,
        )
        self.assertEqual(("DNF", "contact_loss"), (result.outcome, result.terminal_reason))
        self.assertLess(result.credited_progress_m, result.target_progress_m)

    def test_short_segment_half_step_refinement(self) -> None:
        target = self.raw["falsification_controls"]["refinement_segment_distance_m"]
        base = run_integrated_lap_gate(
            replace(self.config, timeout_s=2.0),
            self.linkage.transformed_vertical,
            self.powertrain,
            self.corridors[self.config.corridor_id],
            target_progress_m=target,
            require_loop_closure=False,
            sample_stride=100,
        )
        refined = run_integrated_lap_gate(
            replace(self.config, time_step_s=self.config.time_step_s / 2.0, timeout_s=2.0),
            self.linkage.transformed_vertical,
            self.powertrain,
            self.corridors[self.config.corridor_id],
            target_progress_m=target,
            require_loop_closure=False,
            sample_stride=200,
        )
        self.assertEqual(("finished", "finished"), (base.outcome, refined.outcome))
        relative = abs(base.elapsed_time_s - refined.elapsed_time_s) / refined.elapsed_time_s
        self.assertLessEqual(relative, self.config.refinement_relative_tolerance)

    def test_invalid_config_identity_and_degenerate_linkage_fail_closed(self) -> None:
        invalid = deepcopy(self.raw)
        invalid["model_version"] = "wrong"
        with self.assertRaises(IntegratedLapGateError):
            load_integrated_lap_gate_config(
                invalid,
                controller_source=load_closed_loop_controller_config(self.controller_raw),
            )
        with self.assertRaises(IntegratedLapGateError):
            run_integrated_lap_gate(
                self.config,
                self.linkage.transformed_vertical,
                self.powertrain,
                self.corridors[self.raw["mirror_corridor_id"]],
            )
        bad = replace(
            load_linkage_motion_ratio_config(self.linkage_raw).linkages[0],
            wheel_pickup_m=(0.0, 0.0, 0.0),
        )
        with self.assertRaises(LinkageMotionRatioError):
            derive_motion_ratio(bad)


if __name__ == "__main__":
    unittest.main()
