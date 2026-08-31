"""Run Work 069 stable-support and planar-steering admission evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from formula_ultimate.simulation.planar_support_gate import (
    assess_support_polygon,
    load_support_gate_config,
    mapping,
    materialize_architecture_variant,
    run_planar_steering,
    solve_support_load_case,
)
from formula_ultimate.topology.functional_vehicle import functional_declaration_sha256


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _relative(left: float, right: float) -> float:
    return abs(left - right) / max(abs(right), 1.0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--vehicle-root", required=True, type=Path)
    parser.add_argument("--materialized-architecture", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    gate_raw = json.loads(args.config.read_text(encoding="utf-8"))
    variant_raw = json.loads((args.vehicle_root / gate_raw["architecture_variant_source"]).read_text(encoding="utf-8"))
    base_raw = json.loads((args.vehicle_root / variant_raw["base_architecture_source"]).read_text(encoding="utf-8"))
    negative_raw = json.loads((args.vehicle_root / gate_raw["negative_control_source"]).read_text(encoding="utf-8"))
    if functional_declaration_sha256(base_raw) != functional_declaration_sha256(negative_raw):
        raise RuntimeError("variant base and negative control are not the same frozen declaration")
    config = load_support_gate_config(gate_raw)
    architecture = materialize_architecture_variant(base_raw, variant_raw)
    args.materialized_architecture.parent.mkdir(parents=True, exist_ok=True)
    args.materialized_architecture.write_text(
        json.dumps(architecture, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )

    negative_support = assess_support_polygon(negative_raw)
    candidate_support = assess_support_polygon(architecture)
    load_results = tuple(solve_support_load_case(architecture, config, case) for case in config.load_cases)
    positive = run_planar_steering(architecture, config, steer_angle_rad=config.steer_angle_rad)
    replay = run_planar_steering(architecture, config, steer_angle_rad=config.steer_angle_rad)
    zero = run_planar_steering(architecture, config, steer_angle_rad=0.0)
    negative = run_planar_steering(architecture, config, steer_angle_rad=-config.steer_angle_rad)
    refined = run_planar_steering(
        architecture,
        config,
        steer_angle_rad=config.steer_angle_rad,
        time_step_s=config.time_step_s / 2.0,
    )
    fields = (
        "x_position_m", "y_position_m", "heading_rad", "longitudinal_velocity_m_per_s",
        "lateral_velocity_m_per_s", "yaw_rate_rad_per_s",
    )
    refinement = {
        field: _relative(getattr(positive.final_state, field), getattr(refined.final_state, field))
        for field in fields
    }
    symmetry = {
        field: abs(getattr(positive.final_state, field) + getattr(negative.final_state, field))
        for field in ("y_position_m", "heading_rad", "lateral_velocity_m_per_s", "yaw_rate_rad_per_s")
    }
    checks = {
        "v2_negative_control_rejected": negative_support.status == "unstable" and negative_support.polygon_area_m2 == 0.0,
        "v3_support_polygon_passed": candidate_support.status == "stable" and candidate_support.signed_margin_m > 0.0,
        "load_case_expectations_passed": all(case.expected_status == result.status for case, result in zip(config.load_cases, load_results)),
        "load_case_residuals_passed": all(max(abs(result.vertical_residual_n), abs(result.pitch_residual_nm), abs(result.roll_residual_nm)) <= 1.0e-9 for result in load_results),
        "zero_steer_control_passed": zero.status == "passed" and zero.final_state.heading_rad == 0.0 and zero.final_state.yaw_rate_rad_per_s == 0.0,
        "steering_sign_passed": positive.status == "passed" and negative.status == "passed" and positive.final_state.heading_rad > 0.0 and negative.final_state.heading_rad < 0.0,
        "steering_symmetry_passed": max(symmetry.values()) <= 1.0e-12,
        "contact_limits_passed": max(positive.maximum_contact_utilization, negative.maximum_contact_utilization) <= 1.0 + 1.0e-12 and min(positive.minimum_normal_load_n, negative.minimum_normal_load_n) > 0.0,
        "exact_replay_passed": positive == replay,
        "refinement_passed": max(refinement.values()) <= config.refinement_relative_tolerance,
    }
    body = {
        "protocol_id": config.protocol_id,
        "model_version": gate_raw["model_version"],
        "gate_declaration_sha256": _sha256(gate_raw),
        "variant_declaration_sha256": _sha256(variant_raw),
        "base_declaration_sha256": functional_declaration_sha256(base_raw),
        "materialized_architecture_sha256": functional_declaration_sha256(architecture),
        "checks": checks,
        "negative_control_support": mapping(negative_support),
        "candidate_support": mapping(candidate_support),
        "load_cases": [mapping(item) for item in load_results],
        "positive_steer": mapping(positive),
        "negative_steer": mapping(negative),
        "zero_steer": mapping(zero),
        "refined_positive_steer": mapping(refined),
        "steering_symmetry_absolute_residuals": symmetry,
        "refinement_relative_differences": refinement,
    }
    body["status"] = "passed" if all(checks.values()) else "failed"
    body["evidence_sha256"] = _sha256(body)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(body, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(_canonical({
        "status": body["status"],
        "evidence_sha256": body["evidence_sha256"],
        "materialized_architecture_sha256": body["materialized_architecture_sha256"],
        "v2_signed_margin_m": negative_support.signed_margin_m,
        "v3_signed_margin_m": candidate_support.signed_margin_m,
        "minimum_admitted_load_n": min(item.minimum_normal_load_n for item in load_results if item.status == "passed"),
        "contact_lift_control_minimum_load_n": next(item.minimum_normal_load_n for item in load_results if item.case_id == "contact_lift_control"),
        "positive_final_heading_rad": positive.final_state.heading_rad,
        "positive_final_yaw_rate_rad_per_s": positive.final_state.yaw_rate_rad_per_s,
        "maximum_contact_utilization": positive.maximum_contact_utilization,
        "maximum_refinement_difference": max(refinement.values()),
    }))
    return 0 if body["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
