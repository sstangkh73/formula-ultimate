"""Run Work 072 transient suspension and wheel-contact evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from formula_ultimate.simulation.coupled_planar_differential import (
    load_coupled_planar_config,
    result_to_mapping as coupled_result_to_mapping,
    run_coupled_planar_differential,
)
from formula_ultimate.simulation.differential_drive_coupling import load_differential_drive_config
from formula_ultimate.simulation.planar_support_gate import load_support_gate_config, materialize_architecture_variant
from formula_ultimate.simulation.powertrain_dynamics import load_powertrain_config
from formula_ultimate.simulation.transient_suspension_coupling import (
    load_transient_suspension_config,
    result_to_mapping,
    run_transient_suspension_coupling,
    with_damping_scale,
    with_stiffness_scale,
    with_transient_steer,
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

    raw = json.loads(args.config.read_text(encoding="utf-8"))
    coupled_raw = json.loads((args.vehicle_root / raw["coupled_planar_source"]).read_text(encoding="utf-8"))
    differential_raw = json.loads((args.vehicle_root / coupled_raw["differential_source"]).read_text(encoding="utf-8"))
    variant_raw = json.loads((args.vehicle_root / differential_raw["architecture_variant_source"]).read_text(encoding="utf-8"))
    base_raw = json.loads((args.vehicle_root / variant_raw["base_architecture_source"]).read_text(encoding="utf-8"))
    support_raw = json.loads((args.vehicle_root / differential_raw["support_gate_source"]).read_text(encoding="utf-8"))
    powertrain_raw = json.loads((args.vehicle_root / differential_raw["powertrain_source"]).read_text(encoding="utf-8"))
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
    args.materialized_architecture.parent.mkdir(parents=True, exist_ok=True)
    args.materialized_architecture.write_text(
        json.dumps(architecture, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )

    controls = raw["falsification_controls"]
    reference = run_transient_suspension_coupling(config, powertrain, sample_stride=25)
    replay = run_transient_suspension_coupling(config, powertrain, sample_stride=25)
    rigid = run_coupled_planar_differential(coupled, powertrain, sample_stride=25)
    zero = run_transient_suspension_coupling(
        with_transient_steer(config, 0.0), powertrain, sample_stride=25
    )
    negative = run_transient_suspension_coupling(
        with_transient_steer(config, -config.coupled.steer_angle_rad),
        powertrain,
        sample_stride=25,
    )
    undamped = run_transient_suspension_coupling(
        with_damping_scale(config, 0.0), powertrain, sample_stride=25
    )
    soft = run_transient_suspension_coupling(
        with_stiffness_scale(config, controls["stiffness_scale"]),
        powertrain,
        sample_stride=25,
    )
    contact_loss = run_transient_suspension_coupling(
        config,
        powertrain,
        sample_stride=25,
        initial_contact_states={
            controls["contact_loss_contact_id"]: (
                controls["contact_loss_initial_travel_m"],
                controls["contact_loss_initial_velocity_m_per_s"],
            )
        },
    )
    travel_failure = run_transient_suspension_coupling(
        config,
        powertrain,
        sample_stride=25,
        initial_contact_states={
            controls["travel_failure_contact_id"]: (
                controls["travel_failure_initial_travel_m"],
                controls["travel_failure_initial_velocity_m_per_s"],
            )
        },
    )
    refined = run_transient_suspension_coupling(
        config,
        powertrain,
        time_step_s=config.coupled.time_step_s / 2.0,
        sample_stride=50,
    )

    reference_contacts = {item.contact_id: item for item in reference.final_state.contacts}
    negative_contacts = {item.contact_id: item for item in negative.final_state.contacts}
    zero_contacts = {item.contact_id: item for item in zero.final_state.contacts}
    refined_contacts = {item.contact_id: item for item in refined.final_state.contacts}
    mirror = {
        "x": abs(reference.final_state.coupled.planar.x_position_m - negative.final_state.coupled.planar.x_position_m),
        "y": abs(reference.final_state.coupled.planar.y_position_m + negative.final_state.coupled.planar.y_position_m),
        "heading": abs(reference.final_state.coupled.planar.heading_rad + negative.final_state.coupled.planar.heading_rad),
        "yaw_rate": abs(reference.final_state.coupled.planar.yaw_rate_rad_per_s + negative.final_state.coupled.planar.yaw_rate_rad_per_s),
        "left_right_travel": abs(reference_contacts["left_ground_contact"].travel_m - negative_contacts["right_ground_contact"].travel_m),
        "right_left_travel": abs(reference_contacts["right_ground_contact"].travel_m - negative_contacts["left_ground_contact"].travel_m),
        "left_right_velocity": abs(reference_contacts["left_ground_contact"].velocity_m_per_s - negative_contacts["right_ground_contact"].velocity_m_per_s),
        "right_left_velocity": abs(reference_contacts["right_ground_contact"].velocity_m_per_s - negative_contacts["left_ground_contact"].velocity_m_per_s),
    }
    zero_symmetry = {
        "travel": abs(zero_contacts["left_ground_contact"].travel_m - zero_contacts["right_ground_contact"].travel_m),
        "velocity": abs(zero_contacts["left_ground_contact"].velocity_m_per_s - zero_contacts["right_ground_contact"].velocity_m_per_s),
        "lateral_position": abs(zero.final_state.coupled.planar.y_position_m),
        "yaw_rate": abs(zero.final_state.coupled.planar.yaw_rate_rad_per_s),
    }
    refinement = {
        "x": _relative(reference.final_state.coupled.planar.x_position_m, refined.final_state.coupled.planar.x_position_m),
        "y": _relative(reference.final_state.coupled.planar.y_position_m, refined.final_state.coupled.planar.y_position_m),
        "yaw_rate": _relative(reference.final_state.coupled.planar.yaw_rate_rad_per_s, refined.final_state.coupled.planar.yaw_rate_rad_per_s),
        "maximum_travel": _relative(reference.maximum_abs_travel_m, refined.maximum_abs_travel_m),
        "damper_heat": _relative(reference.final_state.suspension_damping_heat_j, refined.final_state.suspension_damping_heat_j),
    }
    for contact_id, contact in reference_contacts.items():
        refinement[f"{contact_id}.travel"] = _relative(
            contact.travel_m, refined_contacts[contact_id].travel_m
        )
        refinement[f"{contact_id}.velocity"] = _relative(
            contact.velocity_m_per_s, refined_contacts[contact_id].velocity_m_per_s
        )

    actual_load_is_used = all(
        dict(step.coupled.normal_loads_n)
        == {item.contact_id: item.actual_normal_load_n for item in step.contacts}
        for step in reference.trace
    )
    checks = {
        "reference_finished": reference.status == "passed" and reference.outcome == "finished",
        "work071_unchanged": rigid.result_sha256 == "f8f3d888b23a9e21b7bb9ad8b7153ecd5bd4752c7937ebf8cc42a952b64c9cdd",
        "exact_replay": reference == replay,
        "actual_load_used_by_tyre": actual_load_is_used,
        "transient_response_observable": reference.maximum_target_actual_load_difference_n > 1.0,
        "positive_reference_contact": reference.minimum_actual_normal_load_n > 0.0,
        "reference_travel_bounded": reference.maximum_abs_travel_m < min(
            min(item.maximum_compression_m, item.maximum_rebound_m) for item in config.units
        ),
        "zero_steer_symmetric": max(zero_symmetry.values()) <= config.mirror_relative_tolerance,
        "steering_mirror": max(mirror.values()) <= config.mirror_relative_tolerance,
        "undamped_heat_zero": undamped.final_state.suspension_damping_heat_j == 0.0,
        "stiffness_control_observable": soft.maximum_abs_travel_m != reference.maximum_abs_travel_m,
        "contact_loss_dnf": contact_loss.status == "passed" and contact_loss.terminal_reason == "contact_loss" and contact_loss.minimum_actual_normal_load_n <= 0.0,
        "travel_failure_dnf": travel_failure.status == "passed" and travel_failure.terminal_reason == "suspension_travel" and travel_failure.maximum_abs_travel_m > 0.05,
        "initial_energy_budget": all(
            item.initial_total_energy_j == powertrain.initial_storage_energy_j
            for item in (reference, contact_loss, travel_failure)
        ),
        "force_and_energy_residuals": reference.maximum_abs_force_residual_n <= 1.0e-9 and reference.maximum_abs_suspension_energy_residual_j <= 1.0e-9,
        "global_energy": reference.maximum_total_global_relative_energy_residual <= config.global_energy_relative_tolerance,
        "refinement": max(refinement.values()) <= config.refinement_relative_tolerance,
    }
    payload = {
        "model_version": raw["model_version"],
        "protocol_id": raw["protocol_id"],
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "declaration_sha256": _sha256(raw),
        "coupled_declaration_sha256": _sha256(coupled_raw),
        "differential_declaration_sha256": _sha256(differential_raw),
        "powertrain_declaration_sha256": _sha256(powertrain_raw),
        "base_architecture_sha256": functional_declaration_sha256(base_raw),
        "materialized_architecture_sha256": functional_declaration_sha256(architecture),
        "rigid_work071_control": coupled_result_to_mapping(rigid),
        "reference": result_to_mapping(reference),
        "zero_steer_control": result_to_mapping(zero),
        "negative_steer_control": result_to_mapping(negative),
        "undamped_control": result_to_mapping(undamped),
        "soft_spring_control": result_to_mapping(soft),
        "contact_loss_control": result_to_mapping(contact_loss),
        "travel_failure_control": result_to_mapping(travel_failure),
        "mirror_absolute_residuals": mirror,
        "zero_symmetry_absolute_residuals": zero_symmetry,
        "refinement_relative_differences": refinement,
    }
    payload["evidence_sha256"] = _sha256(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    summary = {
        "status": payload["status"],
        "evidence_sha256": payload["evidence_sha256"],
        "final_position_m": [
            reference.final_state.coupled.planar.x_position_m,
            reference.final_state.coupled.planar.y_position_m,
        ],
        "final_yaw_rate_rad_per_s": reference.final_state.coupled.planar.yaw_rate_rad_per_s,
        "minimum_actual_normal_load_n": reference.minimum_actual_normal_load_n,
        "maximum_abs_travel_m": reference.maximum_abs_travel_m,
        "maximum_target_actual_load_difference_n": reference.maximum_target_actual_load_difference_n,
        "maximum_force_residual_n": reference.maximum_abs_force_residual_n,
        "maximum_suspension_energy_residual_j": reference.maximum_abs_suspension_energy_residual_j,
        "maximum_total_global_relative_residual": reference.maximum_total_global_relative_energy_residual,
        "maximum_refinement_difference": max(refinement.values()),
        "contact_loss_step": contact_loss.executed_steps,
        "contact_loss_minimum_load_n": contact_loss.minimum_actual_normal_load_n,
        "travel_failure_step": travel_failure.executed_steps,
        "travel_failure_maximum_travel_m": travel_failure.maximum_abs_travel_m,
    }
    print(_canonical(summary))
    return 0 if payload["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
