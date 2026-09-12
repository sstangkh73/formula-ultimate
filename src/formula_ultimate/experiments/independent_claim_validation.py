"""Independent numerical reinterpretation for Work 129."""
from __future__ import annotations

import hashlib
import json
import statistics
from typing import Any, Mapping

PROTOCOL_VERSION = "independent_claim_validation_v1"


class IndependentClaimViolation(ValueError):
    pass


def canonical_sha256(value):
    try:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        raise IndependentClaimViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()


def validate_protocol(raw: Mapping[str, Any]):
    required = {"protocol_version", "units", "dependencies", "inputs", "telemetry", "independence", "registration", "shared_assumptions", "critical_claims", "coverage", "experiment"}
    if set(raw) != required or raw.get("protocol_version") != PROTOCOL_VERSION:
        raise IndependentClaimViolation("protocol schema or identity mismatch")
    if raw.get("units") != "SI":
        raise IndependentClaimViolation("SI units are required")
    if {item.get("work") for item in raw["dependencies"]} != {125, 126, 127, 128}:
        raise IndependentClaimViolation("Work 125 through 128 dependencies are required")
    declaration = raw["independence"]
    if declaration["independent_backend"] == declaration["upstream_backend"] or declaration["independent_source_module"] == declaration["upstream_source_module"]:
        raise IndependentClaimViolation("shared-function wrapper is not independent")
    if not raw["shared_assumptions"]:
        raise IndependentClaimViolation("common-mode assumptions are undeclared")
    if set(raw["critical_claims"]) != {"paired_time", "energy_cap", "thermal_margin", "structural_margin"}:
        raise IndependentClaimViolation("critical claim selection is incomplete")
    return {"status": "passed", "protocol_sha256": canonical_sha256(raw)}


def independent_analysis(raw: Mapping[str, Any], telemetry):
    validate_protocol(raw)
    expected = raw["registration"]["expected_telemetry_records"]
    if len(telemetry) != expected:
        raise IndependentClaimViolation("telemetry identity or record count mismatch")
    by_condition = {}
    for item in telemetry:
        by_condition.setdefault(item["condition_id"], {})[item["finalist"]] = item
    paired = []
    corrected = []
    for condition_id in sorted(by_condition):
        pair = by_condition[condition_id]
        if set(pair) != {"fixed", "open"} or not pair["fixed"]["completed"] or not pair["open"]["completed"]:
            raise IndependentClaimViolation("unpaired or incomplete critical telemetry")
        raw_effect = pair["fixed"]["race_time_s"] - pair["open"]["race_time_s"]
        severity = max(0.0, 20.0 - pair["fixed"]["thermal_margin_k"])
        correction = severity * raw["registration"]["open_boundary_penalty_s_per_severity"]
        paired.append(raw_effect)
        corrected.append(raw_effect - correction)
    raw_mean = statistics.fmean(paired)
    corrected_mean = statistics.fmean(corrected)
    discrepancy = raw_mean - corrected_mean
    energy_max = {name: max(item["primary_energy_j"] for item in telemetry if item["finalist"] == name) for name in ("fixed", "open")}
    thermal_min = {name: min(item["thermal_margin_k"] for item in telemetry if item["finalist"] == name) for name in ("fixed", "open")}
    structural_min = {name: min(item["structural_margin"] for item in telemetry if item["finalist"] == name) for name in ("fixed", "open")}
    discrepancy_class = "explained_model_boundary" if discrepancy >= raw["registration"]["discrepancy_trigger_s"] else "within_tolerance"
    ranking_stable = corrected_mean > 0
    claim_survives = corrected_mean >= raw["registration"]["meaningful_time_improvement_s"] and discrepancy_class == "within_tolerance"
    return {"raw_paired_effects_s": paired, "corrected_paired_effects_s": corrected, "raw_mean_s": raw_mean, "independent_mean_s": corrected_mean, "disagreement_s": discrepancy, "discrepancy_class": discrepancy_class, "ranking_stable": ranking_stable, "energy_max_j": energy_max, "thermal_min_k": thermal_min, "structural_min": structural_min, "time_superiority_survives": claim_survives}


def detect_known_omission(raw: Mapping[str, Any], telemetry):
    result = independent_analysis(raw, telemetry)
    detected = result["disagreement_s"] >= raw["registration"]["known_omission_detection_s"]
    if not detected:
        raise IndependentClaimViolation("known modeling omission was not detected")
    return {"detected": True, "magnitude_s": result["disagreement_s"]}
