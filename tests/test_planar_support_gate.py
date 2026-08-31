from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import unittest

from formula_ultimate.simulation.planar_support_gate import (
    PlanarSupportGateError,
    assess_support_polygon,
    load_support_gate_config,
    materialize_architecture_variant,
    run_planar_steering,
    solve_support_load_case,
)
from formula_ultimate.topology.functional_vehicle import (
    from_functional_mapping,
    validate_functional_vehicle,
)


ROOT = Path(__file__).resolve().parents[1]


def declarations():
    base = json.loads((ROOT / "config/vehicle/functional_vehicle_architecture_v2.json").read_text(encoding="utf-8"))
    variant = json.loads((ROOT / "config/vehicle/functional_vehicle_architecture_v3_planar.json").read_text(encoding="utf-8"))
    gate = json.loads((ROOT / "config/vehicle/planar_support_gate_v1.json").read_text(encoding="utf-8"))
    return base, variant, gate


def loaded():
    base, variant, gate = declarations()
    materialized = materialize_architecture_variant(base, variant)
    return base, materialized, load_support_gate_config(gate)


def relative(left: float, right: float) -> float:
    return abs(left - right) / max(abs(right), 1.0)


class PlanarSupportGateTests(unittest.TestCase):
    def test_frozen_v2_negative_control_has_degenerate_support(self) -> None:
        base, _, _ = loaded()
        assessment = assess_support_polygon(base)
        self.assertEqual("unstable", assessment.status)
        self.assertEqual("support hull is degenerate", assessment.reason)
        self.assertEqual(2, len(assessment.contacts))
        self.assertEqual(2, len(assessment.convex_hull_xy_m))
        self.assertEqual(0.0, assessment.polygon_area_m2)
        self.assertLess(assessment.signed_margin_m, 0.0)

    def test_v3_materializes_as_valid_stable_three_contact_architecture(self) -> None:
        _, materialized, _ = loaded()
        vehicle = from_functional_mapping(materialized)
        validation = validate_functional_vehicle(vehicle)
        assessment = assess_support_polygon(materialized)
        self.assertEqual(11, validation["component_count"])
        self.assertEqual(3, validation["ground_contact_count"])
        self.assertEqual("stable", assessment.status)
        self.assertEqual(3, len(assessment.convex_hull_xy_m))
        self.assertGreater(assessment.polygon_area_m2, 0.0)
        self.assertGreater(assessment.signed_margin_m, 0.0)

    def test_quasi_static_cases_close_equilibrium_and_expose_contact_lift(self) -> None:
        _, materialized, config = loaded()
        results = tuple(solve_support_load_case(materialized, config, case) for case in config.load_cases)
        self.assertEqual(tuple(case.expected_status for case in config.load_cases), tuple(item.status for item in results))
        for case, result in zip(config.load_cases, results):
            with self.subTest(case=case.case_id):
                self.assertAlmostEqual(0.0, result.vertical_residual_n, places=9)
                self.assertAlmostEqual(0.0, result.pitch_residual_nm, places=9)
                self.assertAlmostEqual(0.0, result.roll_residual_nm, places=9)
                if case.expected_status == "passed":
                    self.assertGreater(result.minimum_normal_load_n, 0.0)
                    self.assertLessEqual(result.maximum_normal_utilization, 1.0)
                else:
                    self.assertLess(result.minimum_normal_load_n, 0.0)

    def test_zero_and_opposite_steering_controls_respond_with_correct_sign(self) -> None:
        _, materialized, config = loaded()
        zero = run_planar_steering(materialized, config, steer_angle_rad=0.0)
        positive = run_planar_steering(materialized, config, steer_angle_rad=config.steer_angle_rad)
        negative = run_planar_steering(materialized, config, steer_angle_rad=-config.steer_angle_rad)
        self.assertEqual(("passed", "passed", "passed"), (zero.status, positive.status, negative.status))
        self.assertEqual(0.0, zero.final_state.y_position_m)
        self.assertEqual(0.0, zero.final_state.heading_rad)
        self.assertEqual(0.0, zero.final_state.yaw_rate_rad_per_s)
        self.assertGreater(positive.final_state.heading_rad, 0.0)
        self.assertLess(negative.final_state.heading_rad, 0.0)
        for field in ("y_position_m", "heading_rad", "lateral_velocity_m_per_s", "yaw_rate_rad_per_s"):
            self.assertAlmostEqual(getattr(positive.final_state, field), -getattr(negative.final_state, field), places=12)
        self.assertLessEqual(positive.maximum_contact_utilization, 1.0 + 1.0e-12)
        self.assertGreater(positive.minimum_normal_load_n, 0.0)

    def test_half_step_refinement_is_within_frozen_bound(self) -> None:
        _, materialized, config = loaded()
        coarse = run_planar_steering(materialized, config, steer_angle_rad=config.steer_angle_rad)
        fine = run_planar_steering(materialized, config, steer_angle_rad=config.steer_angle_rad, time_step_s=config.time_step_s / 2.0)
        fields = (
            "x_position_m", "y_position_m", "heading_rad", "longitudinal_velocity_m_per_s",
            "lateral_velocity_m_per_s", "yaw_rate_rad_per_s",
        )
        for field in fields:
            with self.subTest(field=field):
                self.assertLessEqual(relative(getattr(coarse.final_state, field), getattr(fine.final_state, field)), config.refinement_relative_tolerance)

    def test_replay_is_exact_and_command_changes_identity(self) -> None:
        _, materialized, config = loaded()
        first = run_planar_steering(materialized, config, steer_angle_rad=config.steer_angle_rad)
        replay = run_planar_steering(materialized, config, steer_angle_rad=config.steer_angle_rad)
        changed = run_planar_steering(materialized, config, steer_angle_rad=0.0)
        self.assertEqual(first, replay)
        self.assertEqual(first.result_sha256, replay.result_sha256)
        self.assertNotEqual(first.result_sha256, changed.result_sha256)

    def test_variant_identity_and_numerical_limits_fail_closed(self) -> None:
        base, variant, gate = declarations()
        changed_base = deepcopy(base)
        changed_base["components"][0]["translation_m"][0] += 0.001
        with self.assertRaisesRegex(PlanarSupportGateError, "hash mismatch"):
            materialize_architecture_variant(changed_base, variant)
        invalid_gate = deepcopy(gate)
        invalid_gate["numerical"]["refinement_relative_tolerance"] = 0.021
        with self.assertRaisesRegex(PlanarSupportGateError, "tolerance"):
            load_support_gate_config(invalid_gate)

    def test_architecture_steering_limit_is_enforced(self) -> None:
        _, materialized, config = loaded()
        too_permissive = replace(config, maximum_steer_angle_rad=0.61)
        with self.assertRaisesRegex(PlanarSupportGateError, "protocol steering limit exceeds architecture"):
            run_planar_steering(materialized, too_permissive, steer_angle_rad=0.02)
        with self.assertRaisesRegex(PlanarSupportGateError, "protocol limit"):
            run_planar_steering(materialized, config, steer_angle_rad=0.61)


if __name__ == "__main__":
    unittest.main()
