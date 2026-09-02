"""Run Work 076 integrated synthetic closed-loop lap evidence."""

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
    run_closed_loop_controller,
)
from formula_ultimate.simulation.coupled_planar_differential import load_coupled_planar_config
from formula_ultimate.simulation.differential_drive_coupling import load_differential_drive_config
from formula_ultimate.simulation.integrated_lap_gate import (
    load_integrated_lap_gate_config,
    result_to_mapping,
    run_integrated_lap_gate,
)
from formula_ultimate.simulation.linkage_motion_ratio import (
    apply_linkage_motion_ratios,
    load_linkage_motion_ratio_config,
)
from formula_ultimate.simulation.planar_support_gate import load_support_gate_config, materialize_architecture_variant
from formula_ultimate.simulation.powertrain_dynamics import load_powertrain_config
from formula_ultimate.simulation.sprung_body_vertical_coupling import RaisedCosineRoadProfile, load_sprung_body_vertical_config
from formula_ultimate.simulation.transient_suspension_coupling import load_transient_suspension_config
from formula_ultimate.topology.functional_vehicle import functional_declaration_sha256


WORK074_RESULT_SHA256 = "a400e8a9c1c0768d11647aa6c2fde3855a5d12898b548edef0b2fd6911244374"
WORK075_APPLICATION_SHA256 = "51b6255347e4a6a59428ee309f4f78c8e981baa437386bdcf3505df9d8403487"


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
    controller_raw = json.loads((args.vehicle_root / raw["controller_source"]).read_text(encoding="utf-8"))
    linkage_raw = json.loads((args.vehicle_root / raw["linkage_source"]).read_text(encoding="utf-8"))
    vertical_raw = json.loads((args.vehicle_root / linkage_raw["sprung_body_vertical_source"]).read_text(encoding="utf-8"))
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
    differential = load_differential_drive_config(differential_raw, powertrain=powertrain, architecture_raw=architecture, support_config=support)
    coupled = load_coupled_planar_config(coupled_raw, differential=differential, architecture_raw=architecture, support_config=support)
    transient = load_transient_suspension_config(transient_raw, coupled=coupled, architecture_raw=architecture)
    vertical = load_sprung_body_vertical_config(vertical_raw, transient=transient, architecture_raw=architecture)
    controller_source = load_closed_loop_controller_config(controller_raw)
    linkage = apply_linkage_motion_ratios(load_linkage_motion_ratio_config(linkage_raw), vertical)
    corridor_path = (args.vehicle_root / controller_raw["corridor_source"]).resolve()
    corridors = {item.corridor_id: item for item in load_corridors(corridor_path)}
    config = load_integrated_lap_gate_config(raw, controller_source=controller_source)
    controls = raw["falsification_controls"]

    reference = run_integrated_lap_gate(config, linkage.transformed_vertical, powertrain, corridors[config.corridor_id], sample_stride=250)
    replay = run_integrated_lap_gate(config, linkage.transformed_vertical, powertrain, corridors[config.corridor_id], sample_stride=250)
    work074 = run_closed_loop_controller(controller_source, vertical, powertrain, corridors[controller_source.corridor_id], sample_stride=25)
    mirror_id = raw["mirror_corridor_id"]
    mirror_config = load_integrated_lap_gate_config(raw, controller_source=controller_source, corridor_id=mirror_id)
    mirror_config = replace(mirror_config, controller=replace(
        mirror_config.controller,
        initial_lateral_error_m=-config.controller.initial_lateral_error_m,
        initial_heading_error_rad=-config.controller.initial_heading_error_rad,
    ))
    mirror = run_integrated_lap_gate(mirror_config, linkage.transformed_vertical, powertrain, corridors[mirror_id], sample_stride=250)
    open_loop = run_integrated_lap_gate(config, linkage.transformed_vertical, powertrain, corridors[config.corridor_id], controller_enabled=False, sample_stride=100)
    corridor = corridors[config.corridor_id]
    narrow = replace(corridor, segments=tuple(replace(
        item, width_left_m=controls["narrow_half_width_m"], width_right_m=controls["narrow_half_width_m"]
    ) for item in corridor.segments))
    narrow_result = run_integrated_lap_gate(config, linkage.transformed_vertical, powertrain, narrow, sample_stride=100)
    timeout = run_integrated_lap_gate(replace(config, timeout_s=controls["timeout_s"]), linkage.transformed_vertical, powertrain, corridor, sample_stride=20)
    contact_loss = run_integrated_lap_gate(
        config,
        linkage.transformed_vertical,
        powertrain,
        corridor,
        road_profiles=(RaisedCosineRoadProfile(
            controls["contact_loss_contact_id"], controls["contact_loss_amplitude_m"],
            controls["contact_loss_start_s"], controls["contact_loss_duration_s"],
        ),),
        sample_stride=1,
    )
    segment_target = controls["refinement_segment_distance_m"]
    segment = run_integrated_lap_gate(
        replace(config, timeout_s=2.0), linkage.transformed_vertical, powertrain, corridor,
        target_progress_m=segment_target, require_loop_closure=False, sample_stride=100,
    )
    refined_segment = run_integrated_lap_gate(
        replace(config, time_step_s=config.time_step_s / 2.0, timeout_s=2.0),
        linkage.transformed_vertical, powertrain, corridor,
        target_progress_m=segment_target, require_loop_closure=False, sample_stride=200,
    )
    mirror_residuals = {
        "elapsed_time": abs(reference.elapsed_time_s - mirror.elapsed_time_s),
        "final_x": abs(reference.final_state.coupled.planar.x_position_m - mirror.final_state.coupled.planar.x_position_m),
        "final_y": abs(reference.final_state.coupled.planar.y_position_m + mirror.final_state.coupled.planar.y_position_m),
        "yaw_rate": abs(reference.final_state.coupled.planar.yaw_rate_rad_per_s + mirror.final_state.coupled.planar.yaw_rate_rad_per_s),
        "cross_track": abs(reference.maximum_abs_cross_track_error_m - mirror.maximum_abs_cross_track_error_m),
    }
    refinement = {
        "elapsed_time": abs(segment.elapsed_time_s - refined_segment.elapsed_time_s) / max(abs(refined_segment.elapsed_time_s), 1.0),
        "maximum_cross_track": abs(segment.maximum_abs_cross_track_error_m - refined_segment.maximum_abs_cross_track_error_m),
        "maximum_travel": abs(segment.maximum_abs_suspension_travel_m - refined_segment.maximum_abs_suspension_travel_m),
    }
    finish = reference.finish
    checks = {
        "reference_lap_finished": reference.status == "passed" and reference.outcome == "finished" and reference.terminal_reason == "lap_complete",
        "exact_finish_progress": reference.credited_progress_m == reference.target_progress_m,
        "spatial_loop_closure": finish is not None and finish.position_closure_residual_m <= config.finish_position_tolerance_m and finish.heading_closure_residual_rad <= config.finish_heading_tolerance_rad,
        "progress_requires_motion": reference.maximum_abs_progress_spatial_residual_m <= config.progress_spatial_residual_tolerance_m,
        "physical_gates": reference.minimum_actual_normal_load_n > 0.0 and reference.maximum_abs_suspension_travel_m < min(item.maximum_compression_m for item in linkage.transformed_vertical.contacts),
        "energy": reference.maximum_total_global_relative_energy_residual <= config.energy_relative_tolerance,
        "exact_replay": reference == replay,
        "work074_unchanged": work074.result_sha256 == WORK074_RESULT_SHA256,
        "work075_unchanged": linkage.application_sha256 == WORK075_APPLICATION_SHA256,
        "mirror": mirror.outcome == "finished" and max(mirror_residuals.values()) <= config.mirror_absolute_tolerance,
        "open_loop_departure": open_loop.terminal_reason == "corridor_departure",
        "narrow_corridor_departure": narrow_result.terminal_reason == "corridor_departure",
        "timeout_control": timeout.terminal_reason == "timeout",
        "contact_loss_control": contact_loss.terminal_reason == "contact_loss" and contact_loss.credited_progress_m < contact_loss.target_progress_m,
        "refinement": segment.outcome == "finished" and refined_segment.outcome == "finished" and max(refinement.values()) <= config.refinement_relative_tolerance,
    }
    payload = {
        "model_version": raw["model_version"],
        "protocol_id": raw["protocol_id"],
        "claim_level": raw["claim_level"],
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "declaration_sha256": _sha256(raw),
        "controller_declaration_sha256": _sha256(controller_raw),
        "linkage_declaration_sha256": _sha256(linkage_raw),
        "corridor_declaration_sha256": _sha256(json.loads(corridor_path.read_text(encoding="utf-8"))),
        "materialized_architecture_sha256": functional_declaration_sha256(architecture),
        "work074_result_sha256": work074.result_sha256,
        "work075_application_sha256": linkage.application_sha256,
        "reference": result_to_mapping(reference),
        "mirror_control": result_to_mapping(mirror),
        "open_loop_control": result_to_mapping(open_loop),
        "narrow_corridor_control": result_to_mapping(narrow_result),
        "timeout_control": result_to_mapping(timeout),
        "contact_loss_control": result_to_mapping(contact_loss),
        "short_segment": result_to_mapping(segment),
        "refined_short_segment": result_to_mapping(refined_segment),
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
        "lap_time_s": reference.elapsed_time_s,
        "target_progress_m": reference.target_progress_m,
        "finish_position_residual_m": finish.position_closure_residual_m if finish else None,
        "finish_heading_residual_rad": finish.heading_closure_residual_rad if finish else None,
        "maximum_cross_track_error_m": reference.maximum_abs_cross_track_error_m,
        "minimum_load_n": reference.minimum_actual_normal_load_n,
        "maximum_travel_m": reference.maximum_abs_suspension_travel_m,
        "maximum_energy_residual": reference.maximum_total_global_relative_energy_residual,
        "maximum_progress_spatial_residual_m": reference.maximum_abs_progress_spatial_residual_m,
        "maximum_mirror_residual": max(mirror_residuals.values()),
        "maximum_refinement_difference": max(refinement.values()),
        "open_loop_terminal": open_loop.terminal_reason,
        "contact_loss_terminal": contact_loss.terminal_reason,
    }))
    return 0 if payload["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
