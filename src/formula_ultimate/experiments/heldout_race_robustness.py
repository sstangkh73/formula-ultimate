"""Sealed synthetic held-out race evaluation for Work 128."""
from __future__ import annotations

import hashlib
import json
import math
import statistics
from typing import Any, Mapping

PROTOCOL_VERSION = "heldout_race_robustness_v1"


class HeldoutRaceViolation(ValueError):
    pass


def canonical_sha256(value):
    try:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        raise HeldoutRaceViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()


def validate_protocol(raw: Mapping[str, Any]):
    required = {"protocol_version", "units", "dependency", "input", "seals", "registration", "training_condition_ids", "holdout_conditions", "finalists", "coverage", "experiment"}
    if set(raw) != required or raw.get("protocol_version") != PROTOCOL_VERSION:
        raise HeldoutRaceViolation("protocol schema or identity mismatch")
    if raw.get("units") != "SI":
        raise HeldoutRaceViolation("SI units are required")
    if raw["dependency"].get("work") != 127:
        raise HeldoutRaceViolation("Work 127 dependency is required")
    holdout_ids = [item["id"] for item in raw["holdout_conditions"]]
    if set(holdout_ids) & set(raw["training_condition_ids"]):
        raise HeldoutRaceViolation("holdout reuse or training leakage")
    if len(holdout_ids) != len(set(holdout_ids)) or len(holdout_ids) != raw["registration"]["sample_size"]:
        raise HeldoutRaceViolation("holdout sample mismatch")
    seal_values = {
        "fixed_finalist": raw["finalists"]["fixed"]["identity"],
        "open_finalist": raw["finalists"]["open"]["identity"],
        "evaluator": raw["registration"]["evaluator_identity"],
        "rules": raw["registration"]["rules_identity"],
        "holdout": holdout_ids,
    }
    if any(canonical_sha256(value) != raw["seals"][name] for name, value in seal_values.items()):
        raise HeldoutRaceViolation("changed sealed source hash")
    if raw["registration"]["exposure_tuning_allowed"]:
        raise HeldoutRaceViolation("post-exposure tuning is forbidden")
    return {"status": "passed", "protocol_sha256": canonical_sha256(raw)}


def execute(raw: Mapping[str, Any]):
    validate_protocol(raw)
    telemetry = []
    for condition in raw["holdout_conditions"]:
        for name, finalist in raw["finalists"].items():
            completed = condition["severity"] <= finalist["maximum_severity"]
            telemetry.append({
                "condition_id": condition["id"],
                "finalist": name,
                "completed": completed,
                "race_time_s": finalist["base_time_s"] + condition["time_delta_s"] if completed else None,
                "primary_energy_j": finalist["base_energy_j"] + condition["energy_delta_j"],
                "thermal_margin_k": finalist["thermal_margin_k"] - condition["severity"],
                "structural_margin": finalist["structural_margin"] - condition["severity"] / 100,
                "numerical_uncertainty_s": condition["numerical_uncertainty_s"],
                "stop_reason": "finish" if completed else "registered_severity_limit",
            })
    return telemetry


def analyze(raw: Mapping[str, Any], telemetry):
    expected = len(raw["holdout_conditions"]) * len(raw["finalists"])
    if len(telemetry) != expected:
        raise HeldoutRaceViolation("incomplete races hidden from summary")
    keys = [(item["condition_id"], item["finalist"]) for item in telemetry]
    if len(keys) != len(set(keys)):
        raise HeldoutRaceViolation("duplicate race telemetry")
    failures = [item for item in telemetry if not item["completed"]]
    pairs = []
    for condition in raw["holdout_conditions"]:
        fixed = next(item for item in telemetry if item["condition_id"] == condition["id"] and item["finalist"] == "fixed")
        opened = next(item for item in telemetry if item["condition_id"] == condition["id"] and item["finalist"] == "open")
        if fixed["completed"] and opened["completed"]:
            pairs.append(fixed["race_time_s"] - opened["race_time_s"])
    if len(pairs) != raw["registration"]["sample_size"]:
        robust = False
        mean = None
        interval = None
    else:
        mean = statistics.fmean(pairs)
        statistical_sem = statistics.stdev(pairs) / math.sqrt(len(pairs)) if len(pairs) > 1 else 0.0
        numerical = max(item["numerical_uncertainty_s"] for item in telemetry)
        half = raw["registration"]["t_multiplier"] * statistical_sem + numerical
        interval = [mean - half, mean + half]
        robust = interval[0] >= raw["registration"]["meaningful_time_improvement_s"]
    constraints = all(item["primary_energy_j"] <= raw["registration"]["energy_cap_j"] and item["thermal_margin_k"] >= 0 and item["structural_margin"] >= 0 for item in telemetry)
    completion_rates = {name: statistics.fmean(1.0 if item["completed"] else 0.0 for item in telemetry if item["finalist"] == name) for name in raw["finalists"]}
    robust = robust and constraints and all(rate >= raw["registration"]["minimum_completion_rate"] for rate in completion_rates.values())
    return {"paired_time_improvements_s": pairs, "mean_time_improvement_s": mean, "interval_s": interval, "completion_rates": completion_rates, "failure_count": len(failures), "failures": failures, "constraint_gate": constraints, "robust_superiority_gate": robust}
