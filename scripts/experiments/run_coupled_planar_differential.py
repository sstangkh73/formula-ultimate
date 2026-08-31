"""Run Work 071 coupled planar/differential/load-transfer evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from formula_ultimate.simulation.coupled_planar_differential import (
    load_coupled_planar_config,
    result_to_mapping,
    run_coupled_planar_differential,
    with_coupled_branch_friction,
    with_steer,
)
from formula_ultimate.simulation.differential_drive_coupling import load_differential_drive_config
from formula_ultimate.simulation.planar_support_gate import load_support_gate_config, materialize_architecture_variant
from formula_ultimate.simulation.powertrain_dynamics import load_powertrain_config
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

    raw = json.loads(args.config.read_text(encoding="utf-8"))
    differential_raw = json.loads((args.vehicle_root / raw["differential_source"]).read_text(encoding="utf-8"))
    variant_raw = json.loads((args.vehicle_root / differential_raw["architecture_variant_source"]).read_text(encoding="utf-8"))
    base_raw = json.loads((args.vehicle_root / variant_raw["base_architecture_source"]).read_text(encoding="utf-8"))
    support_raw = json.loads((args.vehicle_root / differential_raw["support_gate_source"]).read_text(encoding="utf-8"))
    powertrain_raw = json.loads((args.vehicle_root / differential_raw["powertrain_source"]).read_text(encoding="utf-8"))
    architecture = materialize_architecture_variant(base_raw, variant_raw)
    support = load_support_gate_config(support_raw)
    powertrain = load_powertrain_config(powertrain_raw)
    differential = load_differential_drive_config(
        differential_raw, powertrain=powertrain, architecture_raw=architecture, support_config=support,
    )
    config = load_coupled_planar_config(raw, differential=differential, architecture_raw=architecture, support_config=support)
    args.materialized_architecture.parent.mkdir(parents=True, exist_ok=True)
    args.materialized_architecture.write_text(json.dumps(architecture, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")

    controls = raw["falsification_controls"]
    reference = run_coupled_planar_differential(config, powertrain, sample_stride=25)
    replay = run_coupled_planar_differential(config, powertrain, sample_stride=25)
    zero = run_coupled_planar_differential(with_steer(config, 0.0), powertrain, sample_stride=25)
    negative = run_coupled_planar_differential(with_steer(config, -config.steer_angle_rad), powertrain, sample_stride=25)
    split = run_coupled_planar_differential(with_coupled_branch_friction(
        config, left=controls["split_grip_left_friction"], right=controls["split_grip_right_friction"],
    ), powertrain, sample_stride=25)
    mirrored_split = run_coupled_planar_differential(with_steer(with_coupled_branch_friction(
        config, left=controls["split_grip_right_friction"], right=controls["split_grip_left_friction"],
    ), -config.steer_angle_rad), powertrain, sample_stride=25)
    excessive = run_coupled_planar_differential(
        with_steer(config, controls["excessive_steer_angle_rad"]), powertrain, sample_stride=25,
    )
    refined = run_coupled_planar_differential(
        config, powertrain, time_step_s=config.time_step_s / 2.0, sample_stride=50,
    )
    fields = ("x_position_m", "y_position_m", "heading_rad", "longitudinal_velocity_m_per_s", "lateral_velocity_m_per_s", "yaw_rate_rad_per_s")
    refinement = {field: _relative(getattr(reference.final_state.planar, field), getattr(refined.final_state.planar, field)) for field in fields}
    refinement.update({
        "differential_speed": _relative(reference.final_state.differential_speed_rad_s, refined.final_state.differential_speed_rad_s),
        "longitudinal_slip_heat": _relative(reference.final_state.longitudinal_slip_heat_j, refined.final_state.longitudinal_slip_heat_j),
        "lateral_slip_heat": _relative(reference.final_state.lateral_slip_heat_j, refined.final_state.lateral_slip_heat_j),
    })
    mirror = {
        "x": abs(reference.final_state.planar.x_position_m - negative.final_state.planar.x_position_m),
        "y": abs(reference.final_state.planar.y_position_m + negative.final_state.planar.y_position_m),
        "heading": abs(reference.final_state.planar.heading_rad + negative.final_state.planar.heading_rad),
        "lateral_velocity": abs(reference.final_state.planar.lateral_velocity_m_per_s + negative.final_state.planar.lateral_velocity_m_per_s),
        "yaw_rate": abs(reference.final_state.planar.yaw_rate_rad_per_s + negative.final_state.planar.yaw_rate_rad_per_s),
        "differential_speed": abs(reference.final_state.differential_speed_rad_s + negative.final_state.differential_speed_rad_s),
    }
    split_speeds, mirrored_speeds = dict(split.final_branch_speeds_rad_s), dict(mirrored_split.final_branch_speeds_rad_s)
    split_mirror = {
        "left_to_right_speed": abs(split_speeds["left"] - mirrored_speeds["right"]),
        "right_to_left_speed": abs(split_speeds["right"] - mirrored_speeds["left"]),
        "y": abs(split.final_state.planar.y_position_m + mirrored_split.final_state.planar.y_position_m),
        "yaw_rate": abs(split.final_state.planar.yaw_rate_rad_per_s + mirrored_split.final_state.planar.yaw_rate_rad_per_s),
    }
    checks = {
        "reference_finished": reference.status == "passed" and reference.outcome == "finished",
        "zero_steer_symmetric": zero.final_state.planar.y_position_m == 0.0 and zero.final_state.planar.yaw_rate_rad_per_s == 0.0 and zero.final_state.differential_speed_rad_s == 0.0,
        "steering_sign_passed": reference.final_state.planar.heading_rad > 0.0 and negative.final_state.planar.heading_rad < 0.0,
        "steering_mirror_passed": max(mirror.values()) <= config.mirror_relative_tolerance,
        "split_mirror_passed": max(split_mirror.values()) <= config.mirror_relative_tolerance,
        "load_transfer_passed": reference.minimum_normal_load_n > 0.0 and reference.minimum_normal_load_n < min(item.baseline_normal_load_n for item in config.contacts),
        "contact_limits_passed": reference.maximum_contact_utilization <= 1.0 + 1.0e-12,
        "balance_passed": reference.maximum_abs_load_balance_residual <= 1.0e-8,
        "differential_kinematics_passed": reference.maximum_abs_carrier_average_residual_rad_s <= 1.0e-12 and reference.maximum_abs_modal_equation_residual_nm <= 1.0e-9,
        "energy_passed": reference.maximum_abs_differential_interface_energy_residual_j <= 1.0e-9 and reference.maximum_abs_contact_energy_residual_j <= 1.0e-9 and reference.maximum_abs_body_energy_residual_j <= 1.0e-8 and reference.maximum_global_relative_energy_residual <= config.global_energy_relative_tolerance,
        "contact_lift_dnf_passed": excessive.outcome == "DNF" and excessive.terminal_reason == "contact_lift" and excessive.minimum_normal_load_n < 0.0,
        "exact_replay_passed": reference == replay,
        "refinement_passed": max(refinement.values()) <= config.refinement_relative_tolerance,
    }
    body = {
        "protocol_id": config.protocol_id,
        "model_version": raw["model_version"],
        "declaration_sha256": _sha256(raw),
        "differential_declaration_sha256": _sha256(differential_raw),
        "powertrain_declaration_sha256": _sha256(powertrain_raw),
        "base_architecture_sha256": functional_declaration_sha256(base_raw),
        "materialized_architecture_sha256": functional_declaration_sha256(architecture),
        "checks": checks,
        "mirror_absolute_residuals": mirror,
        "split_mirror_absolute_residuals": split_mirror,
        "refinement_relative_differences": refinement,
        "reference": result_to_mapping(reference),
        "zero_steer_control": result_to_mapping(zero),
        "negative_steer_control": result_to_mapping(negative),
        "split_grip": result_to_mapping(split),
        "mirrored_split_grip": result_to_mapping(mirrored_split),
        "contact_lift_control": result_to_mapping(excessive),
    }
    body["status"] = "passed" if all(checks.values()) else "failed"
    body["evidence_sha256"] = _sha256(body)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(body, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(_canonical({
        "status": body["status"], "evidence_sha256": body["evidence_sha256"],
        "final_position_m": [reference.final_state.planar.x_position_m, reference.final_state.planar.y_position_m],
        "final_heading_rad": reference.final_state.planar.heading_rad,
        "final_yaw_rate_rad_per_s": reference.final_state.planar.yaw_rate_rad_per_s,
        "final_branch_speeds_rad_s": reference.final_branch_speeds_rad_s,
        "minimum_normal_load_n": reference.minimum_normal_load_n,
        "maximum_contact_utilization": reference.maximum_contact_utilization,
        "maximum_global_relative_residual": reference.maximum_global_relative_energy_residual,
        "maximum_refinement_difference": max(refinement.values()),
        "contact_lift_step": excessive.executed_steps,
        "contact_lift_minimum_load_n": excessive.minimum_normal_load_n,
    }))
    return 0 if body["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
