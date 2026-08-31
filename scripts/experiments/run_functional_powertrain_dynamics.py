"""Run the frozen Work 067 reference and falsification cases."""

from __future__ import annotations

import argparse
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
from typing import Any

from formula_ultimate.simulation.powertrain_dynamics import (
    analytical_power_partition,
    load_powertrain_config,
    result_to_mapping,
    run_powertrain,
)


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _relative(left: float, right: float) -> float:
    return abs(left - right) / max(abs(right), 1.0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    declaration = json.loads(args.config.read_text(encoding="utf-8"))
    config = load_powertrain_config(declaration)
    experiment = declaration["reference_experiment"]
    arguments = {
        "throttle": float(experiment["throttle"]),
        "requested_load_torque_nm": float(experiment["requested_load_torque_nm"]),
        "duration_s": float(experiment["duration_s"]),
        "step_s": float(experiment["step_s"]),
        "sample_stride": int(experiment["sample_stride"]),
    }
    reference = run_powertrain(config, **arguments)
    replay = run_powertrain(config, **arguments)
    refined = run_powertrain(config, **{**arguments, "step_s": arguments["step_s"] / 2.0, "sample_stride": arguments["sample_stride"] * 2})
    zero_energy = run_powertrain(config, **arguments, initial_storage_energy_j=0.0)
    overload = run_powertrain(replace(config, shaft_maximum_torque_nm=50.0), **arguments)
    thermal = run_powertrain(
        replace(config, converter_heat_capacity_j_per_k=10.0, converter_cooling_w_per_k=0.0, converter_maximum_temperature_k=300.1),
        **arguments,
    )
    analytical = analytical_power_partition(config, throttle=0.5, converter_speed_rad_s=200.0)
    refinement = {
        field: _relative(getattr(reference.final_state, field), getattr(refined.final_state, field))
        for field in ("converter_speed_rad_s", "output_speed_rad_s", "storage_energy_j", "converter_temperature_k", "transmission_temperature_k")
    }
    checks = {
        "reference_passed": reference.status == "passed",
        "energy_residual_passed": reference.maximum_relative_energy_residual <= config.energy_relative_tolerance,
        "exact_replay_passed": reference.result_sha256 == replay.result_sha256,
        "refinement_passed": max(refinement.values()) <= config.refinement_relative_tolerance,
        "zero_energy_passed": zero_energy.final_state.source_energy_used_j == 0.0 and zero_energy.final_state.useful_work_j == 0.0,
        "shaft_failure_passed": overload.terminal_reason == "shaft_connection_failure" and overload.final_state.connection_failed,
        "thermal_failure_passed": thermal.terminal_reason == "converter_overtemperature",
        "analytical_balance_passed": abs(analytical["power_residual_w"]) <= 1.0e-9,
    }
    body = {
        "protocol_id": config.protocol_id,
        "model_version": declaration["model_version"],
        "declaration_sha256": hashlib.sha256(_canonical(declaration).encode("utf-8")).hexdigest(),
        "checks": checks,
        "analytical_power_partition": analytical,
        "refinement_relative_differences": refinement,
        "reference": result_to_mapping(reference),
        "zero_energy_control": result_to_mapping(zero_energy),
        "shaft_overload_control": result_to_mapping(overload),
        "thermal_failure_control": result_to_mapping(thermal),
    }
    status = "passed" if all(checks.values()) else "failed"
    body["status"] = status
    body["evidence_sha256"] = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(body, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(_canonical({
        "status": status,
        "reference_result_sha256": reference.result_sha256,
        "evidence_sha256": body["evidence_sha256"],
        "maximum_relative_energy_residual": reference.maximum_relative_energy_residual,
        "maximum_refinement_difference": max(refinement.values()),
        "shaft_failure": overload.terminal_reason,
        "thermal_failure": thermal.terminal_reason,
    }))
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
