"""Run Work 074 deterministic closed-loop corridor evidence."""

from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
from typing import Any

from formula_ultimate.physics.corridor import load_corridors
from formula_ultimate.simulation.closed_loop_corridor_controller import (
    load_closed_loop_controller_config,
    result_to_mapping,
    run_closed_loop_controller,
    with_feedback_gains,
)
from formula_ultimate.simulation.coupled_planar_differential import load_coupled_planar_config
from formula_ultimate.simulation.differential_drive_coupling import load_differential_drive_config
from formula_ultimate.simulation.planar_support_gate import load_support_gate_config, materialize_architecture_variant
from formula_ultimate.simulation.powertrain_dynamics import load_powertrain_config
from formula_ultimate.simulation.sprung_body_vertical_coupling import (
    load_sprung_body_vertical_config,
    run_sprung_body_vertical_coupling,
)
from formula_ultimate.simulation.transient_suspension_coupling import load_transient_suspension_config
from formula_ultimate.topology.functional_vehicle import functional_declaration_sha256


WORK073_REFERENCE_SHA256 = "802330a0566c746d00beb3f5a6cddb725cfee4a9e9f85e08a8bd509b4a6ce973"


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--vehicle-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    raw = json.loads(args.config.read_text(encoding="utf-8"))
    vertical_raw = json.loads((args.vehicle_root / raw["sprung_body_vertical_source"]).read_text(encoding="utf-8"))
    transient_raw = json.loads((args.vehicle_root / vertical_raw["transient_suspension_source"]).read_text(encoding="utf-8"))
    coupled_raw = json.loads((args.vehicle_root / transient_raw["coupled_planar_source"]).read_text(encoding="utf-8"))
    differential_raw = json.loads((args.vehicle_root / coupled_raw["differential_source"]).read_text(encoding="utf-8"))
    variant_raw = json.loads((args.vehicle_root / differential_raw["architecture_variant_source"]).read_text(encoding="utf-8"))
    base_raw = json.loads((args.vehicle_root / variant_raw["base_architecture_source"]).read_text(encoding="utf-8"))
    support_raw = json.loads((args.vehicle_root / differential_raw["support_gate_source"]).read_text(encoding="utf-8"))
    powertrain_raw = json.loads((args.vehicle_root / differential_raw["powertrain_source"]).read_text(encoding="utf-8"))
    architecture = materialize_architecture_variant(base_raw, variant_raw)
    support = load_support_gate_config(support_raw)
    powertrain = load_powertrain_config(powertrain_raw)
    differential = load_differential_drive_config(
        differential_raw, powertrain=powertrain, architecture_raw=architecture, support_config=support
    )
    coupled = load_coupled_planar_config(
        coupled_raw, differential=differential, architecture_raw=architecture, support_config=support
    )
    transient = load_transient_suspension_config(transient_raw, coupled=coupled, architecture_raw=architecture)
    vertical = load_sprung_body_vertical_config(vertical_raw, transient=transient, architecture_raw=architecture)
    corridor_path = (args.vehicle_root / raw["corridor_source"]).resolve()
    corridors = {item.corridor_id: item for item in load_corridors(corridor_path)}
    config = load_closed_loop_controller_config(raw)
    controls = raw["falsification_controls"]

    reference = run_closed_loop_controller(config, vertical, powertrain, corridors[config.corridor_id], sample_stride=25)
    replay = run_closed_loop_controller(config, vertical, powertrain, corridors[config.corridor_id], sample_stride=25)
    fixed = run_sprung_body_vertical_coupling(vertical, powertrain, sample_stride=25)
    zero = run_closed_loop_controller(
        with_feedback_gains(config, heading_gain=controls["zero_feedback_gain"], cross_track_gain_rad_per_m=controls["zero_feedback_gain"]),
        vertical, powertrain, corridors[config.corridor_id], sample_stride=25,
    )
    wrong = run_closed_loop_controller(
        with_feedback_gains(config, cross_track_gain_rad_per_m=controls["wrong_sign_cross_track_gain_rad_per_m"]),
        vertical, powertrain, corridors[config.corridor_id], sample_stride=25,
    )
    mirror_id = raw["mirror_corridor_id"]
    mirror_config = replace(
        load_closed_loop_controller_config(raw, corridor_id=mirror_id),
        initial_lateral_error_m=-config.initial_lateral_error_m,
        initial_heading_error_rad=-config.initial_heading_error_rad,
    )
    mirror = run_closed_loop_controller(mirror_config, vertical, powertrain, corridors[mirror_id], sample_stride=25)
    straight_id = raw["straight_corridor_id"]
    straight_config = replace(
        load_closed_loop_controller_config(raw, corridor_id=straight_id),
        initial_lateral_error_m=0.0,
        initial_heading_error_rad=0.0,
    )
    straight = run_closed_loop_controller(straight_config, vertical, powertrain, corridors[straight_id], sample_stride=25)
    saturated = run_closed_loop_controller(
        replace(config, initial_lateral_error_m=controls["saturation_initial_lateral_error_m"]),
        vertical, powertrain, corridors[config.corridor_id], sample_stride=25,
    )
    departed = run_closed_loop_controller(
        replace(config, initial_lateral_error_m=controls["departure_initial_lateral_error_m"]),
        vertical, powertrain, corridors[config.corridor_id], sample_stride=25,
    )
    refined = run_closed_loop_controller(
        replace(config, time_step_s=config.time_step_s / 2.0),
        vertical, powertrain, corridors[config.corridor_id], sample_stride=50,
    )
    mirror_residuals = {
        "cross_track": abs(reference.final_cross_track_error_m + mirror.final_cross_track_error_m),
        "lateral_position": abs(reference.final_state.coupled.planar.y_position_m + mirror.final_state.coupled.planar.y_position_m),
        "heading": abs(reference.final_state.coupled.planar.heading_rad + mirror.final_state.coupled.planar.heading_rad),
        "yaw_rate": abs(reference.final_state.coupled.planar.yaw_rate_rad_per_s + mirror.final_state.coupled.planar.yaw_rate_rad_per_s),
    }
    refinement = {
        "cross_track": abs(reference.final_cross_track_error_m - refined.final_cross_track_error_m),
        "heading": abs(reference.final_heading_error_rad - refined.final_heading_error_rad),
        "progress": abs(reference.final_progress_m - refined.final_progress_m) / max(abs(refined.final_progress_m), 1.0),
    }
    checks = {
        "reference_finished": reference.status == "passed" and reference.outcome == "finished",
        "fixed_work073_unchanged": fixed.result_sha256 == WORK073_REFERENCE_SHA256,
        "exact_replay": reference == replay,
        "feedback_beats_zero": abs(reference.final_cross_track_error_m) < abs(zero.final_cross_track_error_m),
        "wrong_sign_is_worse": abs(wrong.final_cross_track_error_m) > abs(reference.final_cross_track_error_m),
        "positive_contact_and_bounded_travel": reference.minimum_actual_normal_load_n > 0.0 and reference.maximum_abs_suspension_travel_m < 0.05,
        "commands_bounded": all(abs(item.command.applied_steer_rad) <= config.maximum_steer_angle_rad for item in reference.trace),
        "actual_load_used": all(dict(item.vertical.coupled.normal_loads_n) == {contact.contact_id: contact.actual_normal_load_n for contact in item.vertical.contacts} for item in reference.trace),
        "straight_control": straight.outcome == "finished" and max(abs(item.command.applied_steer_rad) for item in straight.trace) < 1.0e-15,
        "mirror": max(mirror_residuals.values()) <= config.mirror_absolute_tolerance,
        "saturation_observable": saturated.steering_saturation_count > 0,
        "departure_observable": departed.outcome == "DNF" and departed.terminal_reason == "corridor_departure" and departed.executed_steps == 0,
        "energy": reference.maximum_total_global_relative_energy_residual <= vertical.global_energy_relative_tolerance,
        "refinement": max(refinement.values()) <= config.refinement_relative_tolerance,
    }
    payload = {
        "model_version": raw["model_version"],
        "protocol_id": raw["protocol_id"],
        "claim_level": raw["claim_level"],
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "declaration_sha256": _sha256(raw),
        "corridor_declaration_sha256": _sha256(json.loads(corridor_path.read_text(encoding="utf-8"))),
        "materialized_architecture_sha256": functional_declaration_sha256(architecture),
        "fixed_work073_result_sha256": fixed.result_sha256,
        "reference": result_to_mapping(reference),
        "zero_feedback_control": result_to_mapping(zero),
        "wrong_sign_control": result_to_mapping(wrong),
        "mirror_control": result_to_mapping(mirror),
        "straight_control": result_to_mapping(straight),
        "saturation_control": result_to_mapping(saturated),
        "departure_control": result_to_mapping(departed),
        "mirror_absolute_residuals": mirror_residuals,
        "refinement_differences": refinement,
    }
    payload["evidence_sha256"] = _sha256(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(_canonical({
        "status": payload["status"],
        "evidence_sha256": payload["evidence_sha256"],
        "result_sha256": reference.result_sha256,
        "initial_cross_track_error_m": reference.initial_cross_track_error_m,
        "final_cross_track_error_m": reference.final_cross_track_error_m,
        "zero_feedback_final_error_m": zero.final_cross_track_error_m,
        "wrong_sign_final_error_m": wrong.final_cross_track_error_m,
        "maximum_cross_track_error_m": reference.maximum_abs_cross_track_error_m,
        "minimum_actual_normal_load_n": reference.minimum_actual_normal_load_n,
        "maximum_suspension_travel_m": reference.maximum_abs_suspension_travel_m,
        "saturation_count": reference.steering_saturation_count,
        "maximum_mirror_residual": max(mirror_residuals.values()),
        "maximum_refinement_difference": max(refinement.values()),
    }))
    return 0 if payload["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
