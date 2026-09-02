"""Run Work 073 sprung-body, tyre-vertical, and road-coupling evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from formula_ultimate.simulation.coupled_planar_differential import load_coupled_planar_config
from formula_ultimate.simulation.differential_drive_coupling import load_differential_drive_config
from formula_ultimate.simulation.planar_support_gate import (
    load_support_gate_config,
    materialize_architecture_variant,
)
from formula_ultimate.simulation.powertrain_dynamics import load_powertrain_config
from formula_ultimate.simulation.sprung_body_vertical_coupling import (
    RaisedCosineRoadProfile,
    load_sprung_body_vertical_config,
    result_to_mapping,
    run_sprung_body_vertical_coupling,
    with_tyre_damping_scale,
    with_tyre_stiffness_scale,
    with_vertical_steer,
)
from formula_ultimate.simulation.transient_suspension_coupling import (
    load_transient_suspension_config,
    run_transient_suspension_coupling,
)
from formula_ultimate.topology.functional_vehicle import (
    functional_declaration_sha256,
)


WORK072_REFERENCE_SHA256 = "2e70e32766915af2237b92cee20aa9ee415f65bfc5ab14e56fd02d1bf41628ad"


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
    transient_raw = json.loads(
        (args.vehicle_root / raw["transient_suspension_source"]).read_text(encoding="utf-8")
    )
    coupled_raw = json.loads(
        (args.vehicle_root / transient_raw["coupled_planar_source"]).read_text(encoding="utf-8")
    )
    differential_raw = json.loads(
        (args.vehicle_root / coupled_raw["differential_source"]).read_text(encoding="utf-8")
    )
    variant_raw = json.loads(
        (args.vehicle_root / differential_raw["architecture_variant_source"]).read_text(encoding="utf-8")
    )
    base_raw = json.loads(
        (args.vehicle_root / variant_raw["base_architecture_source"]).read_text(encoding="utf-8")
    )
    support_raw = json.loads(
        (args.vehicle_root / differential_raw["support_gate_source"]).read_text(encoding="utf-8")
    )
    powertrain_raw = json.loads(
        (args.vehicle_root / differential_raw["powertrain_source"]).read_text(encoding="utf-8")
    )
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
    transient = load_transient_suspension_config(
        transient_raw, coupled=coupled, architecture_raw=architecture
    )
    config = load_sprung_body_vertical_config(
        raw, transient=transient, architecture_raw=architecture
    )
    args.materialized_architecture.parent.mkdir(parents=True, exist_ok=True)
    args.materialized_architecture.write_text(
        json.dumps(architecture, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )

    controls = raw["falsification_controls"]
    reference = run_sprung_body_vertical_coupling(config, powertrain, sample_stride=25)
    replay = run_sprung_body_vertical_coupling(config, powertrain, sample_stride=25)
    work072 = run_transient_suspension_coupling(transient, powertrain, sample_stride=25)
    zero = run_sprung_body_vertical_coupling(
        with_vertical_steer(config, 0.0), powertrain, sample_stride=25
    )
    negative = run_sprung_body_vertical_coupling(
        with_vertical_steer(config, -config.transient.coupled.steer_angle_rad),
        powertrain,
        sample_stride=25,
    )
    bump_left_profile = RaisedCosineRoadProfile(
        controls["bump_contact_id"], controls["bump_amplitude_m"],
        controls["bump_start_s"], controls["bump_duration_s"],
    )
    bump_right_profile = RaisedCosineRoadProfile(
        "right_ground_contact", controls["bump_amplitude_m"],
        controls["bump_start_s"], controls["bump_duration_s"],
    )
    bump_left = run_sprung_body_vertical_coupling(
        config, powertrain, road_profiles=(bump_left_profile,), sample_stride=25
    )
    bump_right = run_sprung_body_vertical_coupling(
        with_vertical_steer(config, -config.transient.coupled.steer_angle_rad),
        powertrain,
        road_profiles=(bump_right_profile,),
        sample_stride=25,
    )
    undamped = run_sprung_body_vertical_coupling(
        with_tyre_damping_scale(config, 0.0), powertrain, sample_stride=25
    )
    soft = run_sprung_body_vertical_coupling(
        with_tyre_stiffness_scale(config, controls["soft_tyre_scale"]),
        powertrain,
        sample_stride=25,
    )
    contact_loss = run_sprung_body_vertical_coupling(
        config,
        powertrain,
        road_profiles=(RaisedCosineRoadProfile(
            controls["bump_contact_id"], controls["contact_loss_amplitude_m"],
            controls["contact_loss_start_s"], controls["contact_loss_duration_s"],
        ),),
        sample_stride=25,
    )
    large_ramp = run_sprung_body_vertical_coupling(
        config,
        powertrain,
        road_profiles=(RaisedCosineRoadProfile(
            controls["bump_contact_id"], controls["travel_failure_amplitude_m"],
            controls["travel_failure_start_s"], controls["travel_failure_duration_s"],
            controls["travel_failure_profile_shape"],
        ),),
        sample_stride=25,
    )
    initial_coordinates = (controls["travel_state_initial_heave_m"], 0.0, 0.0, 0.0, 0.0, 0.0)
    initial_velocities = (
        controls["travel_state_initial_heave_velocity_m_per_s"], 0.0, 0.0, 0.0, 0.0, 0.0
    )
    travel_failure = run_sprung_body_vertical_coupling(
        config,
        powertrain,
        initial_coordinates=initial_coordinates,
        initial_velocities=initial_velocities,
        sample_stride=25,
    )
    refined = run_sprung_body_vertical_coupling(
        config,
        powertrain,
        time_step_s=config.transient.coupled.time_step_s / 2.0,
        sample_stride=50,
    )

    zero_symmetry = {
        "roll": abs(zero.final_state.coordinates[2]),
        "left_right_unsprung": abs(zero.final_state.coordinates[3] - zero.final_state.coordinates[5]),
        "lateral_position": abs(zero.final_state.coupled.planar.y_position_m),
        "yaw_rate": abs(zero.final_state.coupled.planar.yaw_rate_rad_per_s),
    }
    mirror = {
        "roll": abs(reference.final_state.coordinates[2] + negative.final_state.coordinates[2]),
        "left_right_unsprung": abs(reference.final_state.coordinates[3] - negative.final_state.coordinates[5]),
        "right_left_unsprung": abs(reference.final_state.coordinates[5] - negative.final_state.coordinates[3]),
        "lateral_position": abs(
            reference.final_state.coupled.planar.y_position_m
            + negative.final_state.coupled.planar.y_position_m
        ),
        "yaw_rate": abs(
            reference.final_state.coupled.planar.yaw_rate_rad_per_s
            + negative.final_state.coupled.planar.yaw_rate_rad_per_s
        ),
    }
    bump_mirror = {
        "road_work": abs(bump_left.final_state.road_work_j - bump_right.final_state.road_work_j),
        "maximum_roll": abs(bump_left.maximum_abs_roll_rad - bump_right.maximum_abs_roll_rad),
        "final_roll": abs(bump_left.final_state.coordinates[2] + bump_right.final_state.coordinates[2]),
    }
    refinement = {
        "heave": _relative(reference.maximum_abs_heave_m, refined.maximum_abs_heave_m),
        "pitch": _relative(reference.maximum_abs_pitch_rad, refined.maximum_abs_pitch_rad),
        "roll": _relative(reference.maximum_abs_roll_rad, refined.maximum_abs_roll_rad),
        "travel": _relative(
            reference.maximum_abs_suspension_travel_m,
            refined.maximum_abs_suspension_travel_m,
        ),
        "suspension_heat": _relative(
            reference.final_state.suspension_damping_heat_j,
            refined.final_state.suspension_damping_heat_j,
        ),
        "tyre_heat": _relative(
            reference.final_state.tyre_damping_heat_j,
            refined.final_state.tyre_damping_heat_j,
        ),
    }
    actual_load_is_used = all(
        dict(step.coupled.normal_loads_n)
        == {item.contact_id: item.actual_normal_load_n for item in step.contacts}
        for step in reference.trace
    )
    checks = {
        "reference_finished": reference.status == "passed" and reference.outcome == "finished",
        "work072_unchanged": work072.result_sha256 == WORK072_REFERENCE_SHA256,
        "exact_replay": reference == replay,
        "actual_load_used_by_tyre": actual_load_is_used,
        "positive_reference_contact": reference.minimum_actual_normal_load_n > 0.0,
        "reference_travel_bounded": reference.maximum_abs_suspension_travel_m < 0.05,
        "body_modes_observable": min(
            reference.maximum_abs_heave_m,
            reference.maximum_abs_pitch_rad,
            reference.maximum_abs_roll_rad,
        ) > 0.0,
        "zero_steer_symmetric": max(zero_symmetry.values()) <= config.mirror_relative_tolerance,
        "steering_mirror": max(mirror.values()) <= config.mirror_relative_tolerance,
        "bump_finished_and_did_work": (
            bump_left.outcome == "finished" and bump_left.final_state.road_work_j != 0.0
        ),
        "bump_spatial_mirror": max(bump_mirror.values()) <= config.mirror_relative_tolerance,
        "undamped_tyre_heat_zero": undamped.final_state.tyre_damping_heat_j == 0.0,
        "soft_tyre_observable": soft.maximum_abs_heave_m != reference.maximum_abs_heave_m,
        "road_drop_contact_loss": (
            contact_loss.status == "passed"
            and contact_loss.terminal_reason == "contact_loss"
            and contact_loss.minimum_actual_normal_load_n <= 0.0
            and not contact_loss.trace[-1].committed
        ),
        "large_ramp_first_limit_observable": (
            large_ramp.status == "passed"
            and large_ramp.terminal_reason in {"contact_loss", "suspension_travel"}
        ),
        "initial_state_travel_failure": (
            travel_failure.status == "passed"
            and travel_failure.terminal_reason == "suspension_travel"
            and travel_failure.maximum_abs_suspension_travel_m > 0.05
        ),
        "initial_energy_budget": all(
            item.initial_total_energy_j == powertrain.initial_storage_energy_j
            for item in (reference, contact_loss, large_ramp, travel_failure)
        ),
        "force_and_vertical_energy_residuals": (
            reference.maximum_abs_equation_residual <= 1.0e-9
            and reference.maximum_abs_vertical_energy_residual_j <= 1.0e-9
        ),
        "global_energy": (
            reference.maximum_total_global_relative_energy_residual
            <= config.global_energy_relative_tolerance
        ),
        "refinement": max(refinement.values()) <= config.refinement_relative_tolerance,
    }
    payload = {
        "model_version": raw["model_version"],
        "protocol_id": raw["protocol_id"],
        "claim_level": raw["claim_level"],
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "declaration_sha256": _sha256(raw),
        "transient_declaration_sha256": _sha256(transient_raw),
        "coupled_declaration_sha256": _sha256(coupled_raw),
        "differential_declaration_sha256": _sha256(differential_raw),
        "powertrain_declaration_sha256": _sha256(powertrain_raw),
        "base_architecture_sha256": functional_declaration_sha256(base_raw),
        "materialized_architecture_sha256": functional_declaration_sha256(architecture),
        "sprung_properties": {
            "mass_kg": config.sprung_mass_kg,
            "roll_inertia_kg_m2": config.sprung_roll_inertia_kg_m2,
            "pitch_inertia_kg_m2": config.sprung_pitch_inertia_kg_m2,
        },
        "work072_result_sha256": work072.result_sha256,
        "reference": result_to_mapping(reference),
        "zero_steer_control": result_to_mapping(zero),
        "negative_steer_control": result_to_mapping(negative),
        "bump_left_control": result_to_mapping(bump_left),
        "bump_right_mirror_control": result_to_mapping(bump_right),
        "undamped_tyre_control": result_to_mapping(undamped),
        "soft_tyre_control": result_to_mapping(soft),
        "contact_loss_control": result_to_mapping(contact_loss),
        "large_ramp_control": result_to_mapping(large_ramp),
        "travel_failure_control": result_to_mapping(travel_failure),
        "zero_symmetry_absolute_residuals": zero_symmetry,
        "steering_mirror_absolute_residuals": mirror,
        "bump_mirror_absolute_residuals": bump_mirror,
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
        "result_sha256": reference.result_sha256,
        "final_position_m": [
            reference.final_state.coupled.planar.x_position_m,
            reference.final_state.coupled.planar.y_position_m,
        ],
        "minimum_actual_normal_load_n": reference.minimum_actual_normal_load_n,
        "maximum_actual_normal_load_n": reference.maximum_actual_normal_load_n,
        "maximum_abs_heave_m": reference.maximum_abs_heave_m,
        "maximum_abs_pitch_rad": reference.maximum_abs_pitch_rad,
        "maximum_abs_roll_rad": reference.maximum_abs_roll_rad,
        "maximum_abs_suspension_travel_m": reference.maximum_abs_suspension_travel_m,
        "maximum_equation_residual": reference.maximum_abs_equation_residual,
        "maximum_vertical_energy_residual_j": reference.maximum_abs_vertical_energy_residual_j,
        "maximum_global_relative_residual": reference.maximum_total_global_relative_energy_residual,
        "maximum_refinement_difference": max(refinement.values()),
        "bump_road_work_j": bump_left.final_state.road_work_j,
        "contact_loss_step": contact_loss.executed_steps,
        "large_ramp_terminal": large_ramp.terminal_reason,
        "travel_failure_step": travel_failure.executed_steps,
    }
    print(_canonical(summary))
    return 0 if payload["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
