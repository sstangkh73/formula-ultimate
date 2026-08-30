"""Work 049 fixed-topology end-to-end baseline evaluator."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from typing import Any, Mapping, Sequence


BASELINE_EVALUATOR_VERSION = "bounded_end_to_end_baseline_v1"


class WholeVehicleBaselineError(ValueError):
    """Raised when fixed-baseline evidence is invalid or incomplete."""


@dataclass(frozen=True, slots=True)
class BaselineCaseRecord:
    case_id: str
    partition: str
    maximum_utilization: float
    structural_state: str


@dataclass(frozen=True, slots=True)
class WholeVehicleBaselineResult:
    variant_id: str
    timestep_s: float
    structural_resolution_id: str
    outcome: str
    reason: str
    finish_time_s: float | None
    energy_used_j: float | None
    remaining_energy_j: float | None
    maximum_utilization: float
    attempted_steps: int
    case_records: tuple[BaselineCaseRecord, ...]
    fitness: float | None
    result_sha256: str


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_baseline_inputs(
    protocol: Mapping[str, Any],
    work048: Mapping[str, Any],
    *,
    load_case_protocol_sha256: str,
    work048_source_commit: str,
) -> None:
    if protocol.get("protocol_id") != "fixed_topology_end_to_end_baseline_v1":
        raise WholeVehicleBaselineError("baseline protocol identity mismatch")
    if protocol.get("evaluator_version") != BASELINE_EVALUATOR_VERSION:
        raise WholeVehicleBaselineError("baseline evaluator version mismatch")
    identity = protocol["upstream_identity"]
    expected = {
        "work048_source_commit": work048_source_commit,
        "load_case_protocol_sha256": load_case_protocol_sha256,
        "load_case_result_sha256": work048["replay"]["result_set_sha256"],
        "assembly_step_sha256": work048["assembly_step_sha256"],
        "training_partition_sha256": work048["partitions"]["training_sha256"],
        "holdout_partition_sha256": work048["partitions"]["holdout_sha256"],
    }
    for key, value in expected.items():
        if identity.get(key) != value:
            raise WholeVehicleBaselineError(f"upstream {key} mismatch")
    required = tuple(protocol["required_evidence"])
    if not required or len(required) != len(set(required)):
        raise WholeVehicleBaselineError("required evidence declaration is invalid")
    variants = protocol["variants"]
    if {item["variant_id"] for item in variants} != {"reference", "weak_control", "disconnected_control", "heavy_feasible_control"}:
        raise WholeVehicleBaselineError("baseline control variants are incomplete")
    for item in variants:
        if tuple(item.get("evidence", ())) != required:
            raise WholeVehicleBaselineError("unsupported or incomplete baseline evidence")
        for name in ("capacity_scale", "mass_scale"):
            value = float(item[name])
            if not math.isfinite(value) or value <= 0.0:
                raise WholeVehicleBaselineError(f"{name} must be positive")
    nominal = [item for item in work048["results"] if item["partition"] in {"training", "holdout"}]
    expected_ids = set(work048["partitions"]["training"] + work048["partitions"]["holdout"])
    if {item["case_id"] for item in nominal} != expected_ids:
        raise WholeVehicleBaselineError("Work 048 nominal case set is incomplete")
    if any(item["outcome"] != "running" for item in nominal):
        raise WholeVehicleBaselineError("Work 048 nominal evidence is not feasible")


def _base_utilization(case: Mapping[str, Any]) -> float:
    return max(float(item["utilization"]) for item in case["connection_loads"])


def evaluate_baseline(
    protocol: Mapping[str, Any],
    work048: Mapping[str, Any],
    *,
    variant_id: str,
    timestep_s: float,
    structural_resolution_id: str,
) -> WholeVehicleBaselineResult:
    variants = {item["variant_id"]: item for item in protocol["variants"]}
    resolutions = {item["resolution_id"]: item for item in protocol["structural_resolution"]}
    if variant_id not in variants:
        raise WholeVehicleBaselineError("unknown baseline variant")
    if structural_resolution_id not in resolutions:
        raise WholeVehicleBaselineError("unknown structural resolution")
    if timestep_s not in tuple(float(item) for item in protocol["timestep_refinement_s"]):
        raise WholeVehicleBaselineError("timestep is outside the frozen refinement set")
    variant = variants[variant_id]
    if tuple(variant.get("evidence", ())) != tuple(protocol["required_evidence"]):
        raise WholeVehicleBaselineError("unsupported or incomplete baseline evidence")
    capacity_scale = float(variant["capacity_scale"])
    mass_scale = float(variant["mass_scale"])
    resolution_factor = float(resolutions[structural_resolution_id]["capacity_factor"])
    nominal = [item for item in work048["results"] if item["partition"] in {"training", "holdout"}]
    records = tuple(
        BaselineCaseRecord(
            item["case_id"], item["partition"],
            _base_utilization(item) * mass_scale / (capacity_scale * resolution_factor),
            "failed" if _base_utilization(item) * mass_scale / (capacity_scale * resolution_factor) > 1.0 else "intact",
        )
        for item in nominal
    )
    maximum_utilization = max(item.maximum_utilization for item in records)
    disconnected = not bool(variant["load_path_connected"])
    structural_failure = any(item.structural_state == "failed" for item in records)
    fixture = protocol["race_fixture"]
    if disconnected or structural_failure:
        outcome = "DNF"
        reason = "disconnected_load_path" if disconnected else "structural_failure"
        finish_time = energy_used = remaining = fitness = None
        attempted_steps = 0
    else:
        distance = float(fixture["distance_m"])
        speed = float(fixture["reference_speed_m_per_s"]) / math.sqrt(mass_scale)
        finish_time = distance / speed
        attempted_steps = math.ceil(finish_time / timestep_s)
        propulsion_energy = float(fixture["base_energy_j_per_m"]) * distance * mass_scale
        auxiliary_energy = float(fixture["auxiliary_power_w"]) * finish_time
        energy_used = propulsion_energy + auxiliary_energy
        remaining = float(fixture["initial_energy_j"]) - energy_used
        energy_residual = float(fixture["initial_energy_j"]) - energy_used - remaining
        if abs(energy_residual) > float(protocol["tolerances"]["energy_residual_j"]):
            raise WholeVehicleBaselineError("Level 0 energy residual exceeded")
        if remaining < 0.0:
            outcome, reason, fitness = "DNF", "energy_depletion", None
            finish_time = None
        else:
            outcome, reason, fitness = "finished", "bounded_level0_finish", finish_time
    draft = {
        "variant_id": variant_id,
        "timestep_s": timestep_s,
        "structural_resolution_id": structural_resolution_id,
        "outcome": outcome,
        "reason": reason,
        "finish_time_s": finish_time,
        "energy_used_j": energy_used,
        "remaining_energy_j": remaining,
        "maximum_utilization": maximum_utilization,
        "attempted_steps": attempted_steps,
        "case_records": [asdict(item) for item in records],
        "fitness": fitness,
    }
    return WholeVehicleBaselineResult(
        variant_id, timestep_s, structural_resolution_id, outcome, reason,
        finish_time, energy_used, remaining, maximum_utilization, attempted_steps,
        records, fitness, canonical_sha256(draft),
    )


def evaluate_reference_matrix(protocol: Mapping[str, Any], work048: Mapping[str, Any]) -> tuple[WholeVehicleBaselineResult, ...]:
    return tuple(
        evaluate_baseline(
            protocol, work048, variant_id="reference", timestep_s=float(timestep),
            structural_resolution_id=resolution["resolution_id"],
        )
        for timestep in protocol["timestep_refinement_s"]
        for resolution in protocol["structural_resolution"]
    )


def convergence_metrics(protocol: Mapping[str, Any], matrix: Sequence[WholeVehicleBaselineResult]) -> dict[str, float | str]:
    finish = [item.finish_time_s for item in matrix if item.finish_time_s is not None]
    if len(finish) != len(matrix):
        raise WholeVehicleBaselineError("reference refinement matrix did not finish")
    time_relative = (max(finish) - min(finish)) / max(abs(finish[-1]), 1.0e-300)
    by_timestep: dict[float, list[float]] = {}
    for item in matrix:
        by_timestep.setdefault(item.timestep_s, []).append(item.maximum_utilization)
    utilization_relative = max((max(values) - min(values)) / max(abs(values[-1]), 1.0e-300) for values in by_timestep.values())
    if time_relative > float(protocol["tolerances"]["timestep_finish_time_relative"]):
        raise WholeVehicleBaselineError("timestep convergence gate failed")
    if utilization_relative > float(protocol["tolerances"]["structural_utilization_relative"]):
        raise WholeVehicleBaselineError("structural resolution gate failed")
    return {"status": "passed", "finish_time_maximum_relative": time_relative, "utilization_maximum_relative": utilization_relative}
