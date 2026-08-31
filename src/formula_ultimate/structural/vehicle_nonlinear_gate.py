"""Fail-closed geometric-nonlinearity gate for bounded whole-vehicle frames."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from typing import Any, Mapping, Sequence

from .vehicle_frame_refinement import VehicleFrameError


NONLINEAR_GATE_IDENTITY = "whole_vehicle_geometric_nonlinearity_gate_v1"


def _sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def _positive(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise VehicleFrameError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result) or result <= 0.0:
        raise VehicleFrameError(f"{name} must be finite and positive")
    return result


@dataclass(frozen=True, slots=True)
class NonlinearGateConfig:
    gate_identity: str
    mesh_subdivisions: int
    maximum_displacement_amplification: float
    maximum_stress_amplification: float
    minimum_yield_margin: float
    yield_stress_pa: float
    required_confirmation: str
    required_case_ids: tuple[str, ...]


def nonlinear_gate_config_from_mapping(raw: Mapping[str, Any]) -> NonlinearGateConfig:
    """Validate and decode the frozen nonlinear-gate configuration."""

    if raw.get("protocol_id") != NONLINEAR_GATE_IDENTITY:
        raise VehicleFrameError("nonlinear gate protocol identity mismatch")
    execution = raw.get("execution")
    thresholds = raw.get("thresholds")
    material = raw.get("material")
    if not all(isinstance(item, Mapping) for item in (execution, thresholds, material)):
        raise VehicleFrameError("nonlinear gate configuration sections are missing")
    subdivisions = execution.get("mesh_subdivisions")
    if isinstance(subdivisions, bool) or not isinstance(subdivisions, int) or subdivisions <= 0:
        raise VehicleFrameError("mesh subdivisions must be a positive integer")
    confirmation = execution.get("required_solver_confirmation")
    if not isinstance(confirmation, str) or not confirmation.strip():
        raise VehicleFrameError("solver confirmation text must be nonblank")
    cases = execution.get("required_holdout_case_ids")
    if not isinstance(cases, list) or not cases or not all(isinstance(item, str) and item for item in cases):
        raise VehicleFrameError("required holdout cases must be a nonempty string list")
    if len(cases) != len(set(cases)):
        raise VehicleFrameError("required holdout cases must be unique")
    return NonlinearGateConfig(
        gate_identity=NONLINEAR_GATE_IDENTITY,
        mesh_subdivisions=subdivisions,
        maximum_displacement_amplification=_positive(
            "maximum displacement amplification", thresholds.get("maximum_displacement_amplification")
        ),
        maximum_stress_amplification=_positive(
            "maximum stress amplification", thresholds.get("maximum_stress_amplification")
        ),
        minimum_yield_margin=_positive("minimum yield margin", thresholds.get("minimum_yield_margin")),
        yield_stress_pa=_positive("yield stress", material.get("yield_stress_pa")),
        required_confirmation=confirmation.strip().lower(),
        required_case_ids=tuple(cases),
    )


def adjudicate_nonlinear_case(
    config: NonlinearGateConfig,
    *,
    candidate_id: str,
    case_id: str,
    linear_displacement_m: float,
    linear_surface_stress_pa: float,
    nonlinear_displacement_m: float,
    nonlinear_surface_stress_pa: float,
    process_exit_code: int,
    solver_stdout: str,
) -> dict[str, Any]:
    """Adjudicate one frozen load case without clipping or silent repair."""

    if not isinstance(candidate_id, str) or not candidate_id:
        raise VehicleFrameError("candidate identity must be nonblank")
    if case_id not in config.required_case_ids:
        raise VehicleFrameError("nonlinear case identity is not preregistered")
    if isinstance(process_exit_code, bool) or not isinstance(process_exit_code, int):
        raise VehicleFrameError("process exit code must be an integer")
    if not isinstance(solver_stdout, str):
        raise VehicleFrameError("solver stdout must be text")

    failures: list[str] = []
    if process_exit_code != 0:
        failures.append("nonlinear_process_failure")
    confirmed = config.required_confirmation in solver_stdout.lower()
    if not confirmed:
        failures.append("nonlinear_confirmation_missing")

    numeric: dict[str, float] = {}
    for name, value in (
        ("linear_displacement_m", linear_displacement_m),
        ("linear_surface_stress_pa", linear_surface_stress_pa),
        ("nonlinear_displacement_m", nonlinear_displacement_m),
        ("nonlinear_surface_stress_pa", nonlinear_surface_stress_pa),
    ):
        try:
            numeric[name] = _positive(name, value)
        except VehicleFrameError:
            failures.append("invalid_nonlinear_evidence")
            numeric[name] = float("nan")

    valid_numeric = all(math.isfinite(value) for value in numeric.values())
    displacement_amplification = (
        numeric["nonlinear_displacement_m"] / numeric["linear_displacement_m"] if valid_numeric else None
    )
    stress_amplification = (
        numeric["nonlinear_surface_stress_pa"] / numeric["linear_surface_stress_pa"] if valid_numeric else None
    )
    yield_margin = config.yield_stress_pa / numeric["nonlinear_surface_stress_pa"] if valid_numeric else None
    if valid_numeric:
        if displacement_amplification > config.maximum_displacement_amplification:
            failures.append("nonlinear_displacement_amplification")
        if stress_amplification > config.maximum_stress_amplification:
            failures.append("nonlinear_stress_amplification")
        if yield_margin < config.minimum_yield_margin:
            failures.append("nonlinear_yield_margin")

    failure_codes = tuple(dict.fromkeys(failures))
    draft = {
        "gate_identity": config.gate_identity,
        "candidate_id": candidate_id,
        "case_id": case_id,
        "status": "passed" if not failure_codes else "failed",
        "failure_codes": failure_codes,
        "process_exit_code": process_exit_code,
        "solver_confirmation_present": confirmed,
        "linear_displacement_m": numeric["linear_displacement_m"] if valid_numeric else None,
        "linear_surface_stress_pa": numeric["linear_surface_stress_pa"] if valid_numeric else None,
        "nonlinear_displacement_m": numeric["nonlinear_displacement_m"] if valid_numeric else None,
        "nonlinear_surface_stress_pa": numeric["nonlinear_surface_stress_pa"] if valid_numeric else None,
        "displacement_amplification": displacement_amplification,
        "stress_amplification": stress_amplification,
        "yield_margin": yield_margin,
        "thresholds": {
            "maximum_displacement_amplification": config.maximum_displacement_amplification,
            "maximum_stress_amplification": config.maximum_stress_amplification,
            "minimum_yield_margin": config.minimum_yield_margin,
        },
    }
    return {**draft, "result_sha256": _sha256(draft)}


def aggregate_candidate_nonlinear_gate(
    config: NonlinearGateConfig,
    *,
    candidate_id: str,
    case_results: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Require one exact terminal result for each preregistered holdout case."""

    if not case_results:
        raise VehicleFrameError("candidate nonlinear case evidence is empty")
    by_case: dict[str, Mapping[str, Any]] = {}
    for row in case_results:
        if row.get("candidate_id") != candidate_id or row.get("gate_identity") != config.gate_identity:
            raise VehicleFrameError("candidate nonlinear evidence identity mismatch")
        case_id = row.get("case_id")
        if case_id in by_case:
            raise VehicleFrameError("candidate nonlinear evidence contains a duplicate case")
        by_case[str(case_id)] = row
    if set(by_case) != set(config.required_case_ids):
        raise VehicleFrameError("candidate nonlinear evidence case set mismatch")
    ordered = [by_case[case_id] for case_id in config.required_case_ids]
    for row in ordered:
        expected = _sha256({key: row[key] for key in row if key != "result_sha256"})
        if row.get("result_sha256") != expected:
            raise VehicleFrameError("candidate nonlinear case hash mismatch")
        if row.get("status") not in {"passed", "failed"}:
            raise VehicleFrameError("candidate nonlinear case is not terminal")
    failures = tuple(dict.fromkeys(code for row in ordered for code in row["failure_codes"]))
    draft = {
        "gate_identity": config.gate_identity,
        "candidate_id": candidate_id,
        "status": "passed" if not failures else "failed",
        "failure_codes": failures,
        "case_result_sha256": tuple(row["result_sha256"] for row in ordered),
    }
    return {**draft, "result_sha256": _sha256(draft)}
