"""Run the frozen Work 068 drive-ground reference and falsification suite."""

from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
from typing import Any

from formula_ultimate.simulation.drive_ground_coupling import (
    analytical_ground_partition,
    load_drive_ground_config,
    result_to_mapping,
    run_drive_ground,
)
from formula_ultimate.simulation.powertrain_dynamics import load_powertrain_config


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _relative(left: float, right: float) -> float:
    return abs(left - right) / max(abs(right), 1.0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--vehicle-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    declaration = json.loads(args.config.read_text(encoding="utf-8"))
    architecture_raw = json.loads((args.vehicle_root / declaration["architecture_source"]).read_text(encoding="utf-8"))
    powertrain_raw = json.loads((args.vehicle_root / declaration["powertrain_source"]).read_text(encoding="utf-8"))
    powertrain = load_powertrain_config(powertrain_raw)
    config = load_drive_ground_config(declaration, powertrain=powertrain, architecture_raw=architecture_raw)
    experiment = declaration["reference_experiment"]
    arguments = {
        "throttle": float(experiment["throttle"]),
        "duration_s": float(experiment["duration_s"]),
        "step_s": float(experiment["step_s"]),
        "sample_stride": int(experiment["sample_stride"]),
    }
    reference = run_drive_ground(config, powertrain, **arguments)
    replay = run_drive_ground(config, powertrain, **arguments)
    refined = run_drive_ground(config, powertrain, **{**arguments, "step_s": arguments["step_s"] / 2.0, "sample_stride": arguments["sample_stride"] * 2})
    zero_throttle = run_drive_ground(config, powertrain, **{**arguments, "throttle": 0.0})
    zero_energy = run_drive_ground(config, powertrain, **arguments, initial_storage_energy_j=0.0)
    overload = run_drive_ground(config, replace(powertrain, shaft_maximum_torque_nm=50.0), **arguments)
    analytical = analytical_ground_partition(
        wheel_speed_rad_per_s=100.0,
        vehicle_speed_m_per_s=12.0,
        forces_n=tuple(1000.0 for _ in config.ground_units),
        radii_m=tuple(item.effective_radius_m for item in config.ground_units),
    )
    refinement = {
        field: _relative(getattr(reference.final_state, field), getattr(refined.final_state, field))
        for field in ("speed_m_per_s", "position_m", "slip_heat_j", "aerodynamic_work_j", "rolling_work_j")
    }
    checks = {
        "reference_passed": reference.status == "passed" and reference.outcome == "finished",
        "force_limits_passed": reference.maximum_contact_utilization <= 1.0 + 1.0e-12,
        "global_energy_passed": reference.maximum_global_relative_energy_residual <= config.energy_relative_tolerance,
        "torque_partition_passed": reference.maximum_abs_torque_residual_nm <= 1.0e-9 and reference.maximum_abs_interface_partition_residual_j <= 1.0e-9,
        "analytical_partition_passed": abs(analytical["power_residual_w"]) <= 1.0e-9,
        "exact_replay_passed": reference.result_sha256 == replay.result_sha256,
        "refinement_passed": max(refinement.values()) <= config.refinement_relative_tolerance,
        "zero_throttle_passed": zero_throttle.final_state.position_m == 0.0 and zero_throttle.maximum_ground_force_n == 0.0,
        "zero_energy_passed": zero_energy.final_state.position_m == 0.0 and zero_energy.maximum_ground_force_n == 0.0,
        "dnf_coupling_passed": overload.outcome == "DNF" and overload.terminal_reason == "shaft_connection_failure" and overload.trace[-1].powertrain.output_drive_torque_nm == 0.0,
    }
    body = {
        "protocol_id": config.protocol_id,
        "model_version": declaration["model_version"],
        "declaration_sha256": hashlib.sha256(_canonical(declaration).encode("utf-8")).hexdigest(),
        "architecture_declaration_sha256": hashlib.sha256(_canonical(architecture_raw).encode("utf-8")).hexdigest(),
        "powertrain_declaration_sha256": hashlib.sha256(_canonical(powertrain_raw).encode("utf-8")).hexdigest(),
        "checks": checks,
        "analytical_ground_partition": analytical,
        "refinement_relative_differences": refinement,
        "reference": result_to_mapping(reference),
        "zero_throttle_control": result_to_mapping(zero_throttle),
        "zero_energy_control": result_to_mapping(zero_energy),
        "drive_failure_control": result_to_mapping(overload),
    }
    body["status"] = "passed" if all(checks.values()) else "failed"
    body["evidence_sha256"] = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(body, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(_canonical({
        "status": body["status"],
        "evidence_sha256": body["evidence_sha256"],
        "reference_result_sha256": reference.result_sha256,
        "final_speed_m_per_s": reference.final_state.speed_m_per_s,
        "final_distance_m": reference.final_state.position_m,
        "maximum_contact_utilization": reference.maximum_contact_utilization,
        "maximum_global_relative_energy_residual": reference.maximum_global_relative_energy_residual,
        "maximum_refinement_difference": max(refinement.values()),
        "failure_outcome": overload.outcome,
        "failure_reason": overload.terminal_reason,
    }))
    return 0 if body["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
