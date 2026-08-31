"""Run Work 070 differential-drive reference and falsification evidence."""

from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
from typing import Any

from formula_ultimate.simulation.differential_drive_coupling import (
    load_differential_drive_config,
    result_to_mapping,
    run_differential_drive,
    with_branch_friction,
)
from formula_ultimate.simulation.planar_support_gate import (
    load_support_gate_config,
    materialize_architecture_variant,
)
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
    variant_raw = json.loads((args.vehicle_root / raw["architecture_variant_source"]).read_text(encoding="utf-8"))
    base_raw = json.loads((args.vehicle_root / variant_raw["base_architecture_source"]).read_text(encoding="utf-8"))
    support_raw = json.loads((args.vehicle_root / raw["support_gate_source"]).read_text(encoding="utf-8"))
    powertrain_raw = json.loads((args.vehicle_root / raw["powertrain_source"]).read_text(encoding="utf-8"))
    architecture = materialize_architecture_variant(base_raw, variant_raw)
    support = load_support_gate_config(support_raw)
    powertrain = load_powertrain_config(powertrain_raw)
    config = load_differential_drive_config(raw, powertrain=powertrain, architecture_raw=architecture, support_config=support)
    args.materialized_architecture.parent.mkdir(parents=True, exist_ok=True)
    args.materialized_architecture.write_text(json.dumps(architecture, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")

    experiment = raw["reference_experiment"]
    run_arguments = {
        "throttle": float(experiment["throttle"]),
        "duration_s": float(experiment["duration_s"]),
        "step_s": float(experiment["step_s"]),
        "sample_stride": int(experiment["sample_stride"]),
    }
    controls = raw["falsification_controls"]
    left_mu = float(controls["split_grip_left_friction"])
    right_mu = float(controls["split_grip_right_friction"])
    reference = run_differential_drive(config, powertrain, **run_arguments)
    replay = run_differential_drive(config, powertrain, **run_arguments)
    split_config = with_branch_friction(config, left=left_mu, right=right_mu)
    mirror_config = with_branch_friction(config, left=right_mu, right=left_mu)
    split = run_differential_drive(split_config, powertrain, **run_arguments)
    mirror = run_differential_drive(mirror_config, powertrain, **run_arguments)
    zero_energy = run_differential_drive(config, powertrain, initial_storage_energy_j=0.0, **run_arguments)
    overspeed = run_differential_drive(
        replace(config, maximum_branch_speed_rad_s=float(controls["overspeed_control_maximum_branch_speed_rad_s"])),
        powertrain, **run_arguments,
    )
    refined = run_differential_drive(
        split_config, powertrain,
        **{**run_arguments, "step_s": run_arguments["step_s"] / 2.0, "sample_stride": run_arguments["sample_stride"] * 2},
    )
    refinement = {
        "vehicle_speed": _relative(split.final_state.speed_m_per_s, refined.final_state.speed_m_per_s),
        "position": _relative(split.final_state.position_m, refined.final_state.position_m),
        "differential_speed": _relative(split.final_state.differential_speed_rad_s, refined.final_state.differential_speed_rad_s),
        "slip_heat": _relative(split.final_state.slip_heat_j, refined.final_state.slip_heat_j),
        "branch_connection_heat": _relative(split.final_state.branch_connection_heat_j, refined.final_state.branch_connection_heat_j),
    }
    split_speeds = dict(split.final_branch_speeds_rad_s)
    mirror_speeds = dict(mirror.final_branch_speeds_rad_s)
    mirror_residuals = {
        "left_to_right_speed_rad_s": abs(split_speeds["left"] - mirror_speeds["right"]),
        "right_to_left_speed_rad_s": abs(split_speeds["right"] - mirror_speeds["left"]),
        "vehicle_speed_m_per_s": abs(split.final_state.speed_m_per_s - mirror.final_state.speed_m_per_s),
        "position_m": abs(split.final_state.position_m - mirror.final_state.position_m),
    }
    checks = {
        "reference_finished": reference.status == "passed" and reference.outcome == "finished",
        "symmetric_mode_zero": reference.final_state.differential_speed_rad_s == 0.0 and reference.maximum_differential_modal_energy_j == 0.0,
        "split_grip_finished": split.status == "passed" and split.outcome == "finished" and split.final_state.differential_speed_rad_s != 0.0,
        "carrier_average_passed": max(reference.maximum_abs_carrier_average_residual_rad_s, split.maximum_abs_carrier_average_residual_rad_s) <= 1.0e-12,
        "modal_equation_passed": split.maximum_abs_modal_equation_residual_nm <= 1.0e-9,
        "interface_energy_passed": split.maximum_abs_interface_energy_residual_j <= 1.0e-9,
        "global_energy_passed": max(reference.maximum_global_relative_energy_residual, split.maximum_global_relative_energy_residual) <= config.energy_relative_tolerance,
        "contact_limits_passed": max(reference.maximum_contact_utilization, split.maximum_contact_utilization) <= 1.0 + 1.0e-12,
        "mirror_passed": max(mirror_residuals.values()) <= 1.0e-10,
        "zero_energy_passed": zero_energy.final_state.position_m == 0.0 and zero_energy.final_state.differential_speed_rad_s == 0.0,
        "overspeed_dnf_passed": overspeed.outcome == "DNF" and overspeed.terminal_reason == "differential_branch_overspeed",
        "exact_replay_passed": reference == replay,
        "refinement_passed": max(refinement.values()) <= config.refinement_relative_tolerance,
    }
    body = {
        "protocol_id": config.protocol_id,
        "model_version": raw["model_version"],
        "declaration_sha256": _sha256(raw),
        "base_architecture_sha256": functional_declaration_sha256(base_raw),
        "materialized_architecture_sha256": functional_declaration_sha256(architecture),
        "powertrain_declaration_sha256": _sha256(powertrain_raw),
        "checks": checks,
        "refinement_relative_differences": refinement,
        "mirror_absolute_residuals": mirror_residuals,
        "reference": result_to_mapping(reference),
        "split_grip": result_to_mapping(split),
        "mirrored_split_grip": result_to_mapping(mirror),
        "zero_energy_control": result_to_mapping(zero_energy),
        "overspeed_control": result_to_mapping(overspeed),
    }
    body["status"] = "passed" if all(checks.values()) else "failed"
    body["evidence_sha256"] = _sha256(body)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(body, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(_canonical({
        "status": body["status"],
        "evidence_sha256": body["evidence_sha256"],
        "reference_final_speed_m_per_s": reference.final_state.speed_m_per_s,
        "split_final_speed_m_per_s": split.final_state.speed_m_per_s,
        "split_final_branch_speeds_rad_s": split.final_branch_speeds_rad_s,
        "split_final_differential_speed_rad_s": split.final_state.differential_speed_rad_s,
        "split_maximum_modal_energy_j": split.maximum_differential_modal_energy_j,
        "split_maximum_interface_residual_j": split.maximum_abs_interface_energy_residual_j,
        "split_maximum_global_relative_residual": split.maximum_global_relative_energy_residual,
        "maximum_refinement_difference": max(refinement.values()),
        "overspeed_outcome": overspeed.outcome,
        "overspeed_reason": overspeed.terminal_reason,
    }))
    return 0 if body["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
