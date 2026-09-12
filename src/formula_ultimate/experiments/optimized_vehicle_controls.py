"""Fair optimized vehicle-control comparison for Work 127."""
from __future__ import annotations

import hashlib
import json
import math
import statistics
from typing import Any, Mapping

PROTOCOL_VERSION = "optimized_vehicle_controls_v1"
BURDEN_FIELDS = {"base_mass_kg", "cooling_mass_kg", "containment_mass_kg", "support_mass_kg", "manufacturing_penalty", "energy_j"}


class OptimizedVehicleControlsViolation(ValueError):
    pass


def canonical_sha256(value):
    try:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        raise OptimizedVehicleControlsViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()


def validate_protocol(raw: Mapping[str, Any]):
    required = {"protocol_version", "units", "dependencies", "inputs", "registration", "arms", "conditions", "budgets", "burden_weights", "coverage", "experiment"}
    if set(raw) != required or raw.get("protocol_version") != PROTOCOL_VERSION:
        raise OptimizedVehicleControlsViolation("protocol schema or identity mismatch")
    if raw.get("units") != "SI_and_dimensionless_score":
        raise OptimizedVehicleControlsViolation("unit boundary mismatch")
    if {item.get("work") for item in raw["dependencies"]} != {123, 124, 126}:
        raise OptimizedVehicleControlsViolation("Work 123, 124 and 126 dependencies are required")
    if set(raw["arms"]) != {"fixed_topology", "reference", "random_control", "open_candidate"}:
        raise OptimizedVehicleControlsViolation("comparison arms are incomplete")
    budget_identities = {canonical_sha256(value) for value in raw["budgets"].values()}
    if len(budget_identities) != 1:
        raise OptimizedVehicleControlsViolation("search or tuning budgets are unequal")
    source_energies = {arm["source_energy_j"] for arm in raw["arms"].values()}
    if len(source_energies) != 1:
        raise OptimizedVehicleControlsViolation("source energy is unequal")
    for name, arm in raw["arms"].items():
        if not arm.get("baseline_tuned", False):
            raise OptimizedVehicleControlsViolation(f"untuned baseline: {name}")
        if set(arm["burdens"]) != BURDEN_FIELDS:
            raise OptimizedVehicleControlsViolation(f"incomplete burden ledger: {name}")
        if raw["budgets"][name]["controller_tuning"] <= 0:
            raise OptimizedVehicleControlsViolation("free controller effort")
    return {"status": "passed", "protocol_sha256": canonical_sha256(raw)}


def _burden_penalty(raw, arm):
    burdens = arm["burdens"]
    weights = raw["burden_weights"]
    installed_mass = sum(burdens[key] for key in ("base_mass_kg", "cooling_mass_kg", "containment_mass_kg", "support_mass_kg"))
    return installed_mass * weights["mass_per_kg"] + burdens["energy_j"] * weights["energy_per_j"] + burdens["manufacturing_penalty"], installed_mass


def _score(raw, name, parameter, condition, controller):
    arm = raw["arms"][name]
    penalty, installed_mass = _burden_penalty(raw, arm)
    value = arm["base_score"] + arm["parameter_effects"][str(parameter)] + raw["conditions"]["effects"][condition] - penalty
    if controller == "common":
        value -= arm["common_controller_penalty"]
    return {"score": value, "installed_mass_kg": installed_mass, "source_energy_j": arm["source_energy_j"], "failure": False}


def optimize_arm(raw, name):
    arm = raw["arms"][name]
    records = []
    for parameter in arm["parameters"]:
        scores = [_score(raw, name, parameter, condition, "retuned")["score"] for condition in raw["conditions"]["training"]]
        records.append({"parameter": parameter, "mean_training_score": statistics.fmean(scores)})
    best = max(records, key=lambda item: (item["mean_training_score"], -item["parameter"]))
    return {"best_parameter": best["parameter"], "records": records, "search_evaluations": len(records)}


def run_comparison(raw):
    validate_protocol(raw)
    tuned = {name: optimize_arm(raw, name) for name in raw["arms"]}
    common = {name: [_score(raw, name, 0, condition, "common") for condition in raw["conditions"]["holdout"]] for name in raw["arms"]}
    retuned = {name: [_score(raw, name, tuned[name]["best_parameter"], condition, "retuned") for condition in raw["conditions"]["holdout"]] for name in raw["arms"]}
    controls = [name for name in raw["arms"] if name != "open_candidate"]
    best_control = max(controls, key=lambda name: statistics.fmean(item["score"] for item in retuned[name]))
    effects = [open_item["score"] - control_item["score"] for open_item, control_item in zip(retuned["open_candidate"], retuned[best_control])]
    mean = statistics.fmean(effects)
    sem = statistics.stdev(effects) / math.sqrt(len(effects)) if len(effects) > 1 else 0.0
    half = raw["registration"]["t_multiplier"] * sem
    interval = [mean - half, mean + half]
    complete_costs = {name: raw["budgets"][name]["vehicle_search"] + raw["budgets"][name]["controller_tuning"] for name in raw["arms"]}
    benefit = interval[0] >= raw["registration"]["meaningful_system_effect"] and not any(item["failure"] for item in retuned["open_candidate"])
    return {"tuning": tuned, "common_controller": common, "retuned": retuned, "best_control": best_control, "paired_effects": effects, "mean_effect": mean, "interval": interval, "complete_costs": complete_costs, "system_benefit_gate": benefit}
