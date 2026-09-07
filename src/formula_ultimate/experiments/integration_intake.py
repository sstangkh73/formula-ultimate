"""Causal survivor audit and fail-closed whole-vehicle integration intake."""

from __future__ import annotations

from copy import deepcopy
from itertools import permutations
import math
import re
from typing import Any, Mapping, Sequence

from formula_ultimate.experiments.discovery_registration import digest
from formula_ultimate.topology.functional_vehicle import REQUIRED_CAPABILITIES


SCHEMA = "work101_integration_intake_v1"
RESULT_SCHEMA = "work105_survivor_causality_intake_result_v1"


class IntegrationIntakeViolation(ValueError):
    """Raised when source evidence or an intake decision is not trustworthy."""


def _exact(value: Any, keys: set[str], label: str) -> None:
    if not isinstance(value, Mapping) or set(value) != keys:
        raise IntegrationIntakeViolation(f"{label} schema mismatch")


def _number(value: Any, label: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise IntegrationIntakeViolation(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0.0):
        raise IntegrationIntakeViolation(f"{label} is outside its finite range")
    return result


def _strings(value: Any, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item for item in value):
        raise IntegrationIntakeViolation(f"{label} must contain nonblank strings")
    if len(value) != len(set(value)):
        raise IntegrationIntakeViolation(f"{label} contains duplicates")
    return tuple(value)


def validate_config(config: Mapping[str, Any]) -> dict[str, Any]:
    _exact(config, {"schema", "source", "activity", "capabilities", "evidence", "claim_boundary"}, "config")
    if config["schema"] != SCHEMA:
        raise IntegrationIntakeViolation("config schema mismatch")
    source = config["source"]
    _exact(source, {"work100_registration_sha256", "work100_deterministic_sha256", "expected_candidate_count", "expected_survivor_count"}, "source")
    for key in ("work100_registration_sha256", "work100_deterministic_sha256"):
        if not isinstance(source[key], str) or re.fullmatch(r"[0-9a-f]{64}", source[key]) is None:
            raise IntegrationIntakeViolation(f"{key} must be a SHA-256 identity")
    for key in ("expected_candidate_count", "expected_survivor_count"):
        if isinstance(source[key], bool) or not isinstance(source[key], int) or source[key] < 1:
            raise IntegrationIntakeViolation(f"{key} must be a positive integer")
    activity = config["activity"]
    _exact(activity, {"mechanical_input_n", "thermal_input_w", "relative_flow_threshold", "minimum_meaningful_utilization_difference", "maximum_canonical_active_nodes"}, "activity")
    for key in ("mechanical_input_n", "thermal_input_w", "relative_flow_threshold", "minimum_meaningful_utilization_difference"):
        _number(activity[key], key, positive=True)
    if not 0.0 < activity["relative_flow_threshold"] < 1.0:
        raise IntegrationIntakeViolation("relative flow threshold must be within (0, 1)")
    if not 0.0 < activity["minimum_meaningful_utilization_difference"] <= 1.0:
        raise IntegrationIntakeViolation("meaningful effect must be within (0, 1]")
    if isinstance(activity["maximum_canonical_active_nodes"], bool) or not isinstance(activity["maximum_canonical_active_nodes"], int) or not 2 <= activity["maximum_canonical_active_nodes"] <= 9:
        raise IntegrationIntakeViolation("canonical active-node bound must be an integer from 2 to 9")
    capabilities = config["capabilities"]
    _exact(capabilities, {"required_vehicle", "work100_contribution"}, "capabilities")
    required = _strings(capabilities["required_vehicle"], "required capabilities")
    contributed = _strings(capabilities["work100_contribution"], "contributed capabilities")
    if set(required) != set(REQUIRED_CAPABILITIES):
        raise IntegrationIntakeViolation("required capabilities diverge from the functional vehicle contract")
    if set(contributed) != {"load_structure"} or not set(contributed) <= set(required):
        raise IntegrationIntakeViolation("Work 100 capability claim is too broad")
    evidence = config["evidence"]
    _exact(evidence, {"required_for_program_exit", "provided_by_work100"}, "evidence")
    required_evidence = _strings(evidence["required_for_program_exit"], "required evidence")
    provided = _strings(evidence["provided_by_work100"], "provided evidence")
    if not set(provided) < set(required_evidence) or not {"candidate_survivor", "holdout"} <= set(provided):
        raise IntegrationIntakeViolation("Work 100 evidence coverage must be a strict incomplete subset")
    boundary = config["claim_boundary"]
    _exact(boundary, {"intake_scope", "prohibited_claims"}, "claim boundary")
    prohibited = set(_strings(boundary["prohibited_claims"], "prohibited claims"))
    if boundary["intake_scope"] != "analysis_only_typed_subsystem_intake_not_vehicle_admission" or not {"promotion_ready", "whole_vehicle_admission", "technology_discovery", "physical_validation"} <= prohibited:
        raise IntegrationIntakeViolation("claim boundary is incomplete")
    return {"status": "passed", "config_sha256": digest(config)}


def _edge_rows(field: Mapping[str, Any], applied: float, threshold: float) -> dict[str, dict[str, Any]]:
    segments = field.get("segments")
    if not isinstance(segments, list) or not segments:
        raise IntegrationIntakeViolation("field segments are missing")
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for segment in segments:
        if not isinstance(segment, Mapping):
            raise IntegrationIntakeViolation("field segment is malformed")
        edge_id = segment.get("edge_id")
        if not isinstance(edge_id, str) or not edge_id:
            raise IntegrationIntakeViolation("field edge identity is missing")
        grouped.setdefault(edge_id, []).append(segment)
    result = {}
    for edge_id, rows in sorted(grouped.items()):
        try:
            ordered = sorted(rows, key=lambda row: int(row["segment"]))
            if [int(row["segment"]) for row in ordered] != list(range(len(ordered))):
                raise IntegrationIntakeViolation("field segment indices are not contiguous")
            a, b = str(ordered[0]["a"]), str(ordered[-1]["b"])
            maximum_flow = max(abs(_number(row["flow"], "segment flow")) for row in ordered)
        except KeyError as error:
            raise IntegrationIntakeViolation(f"field segment is missing {error}") from error
        fraction = maximum_flow / applied
        result[edge_id] = {"a": a, "b": b, "maximum_absolute_flow": maximum_flow, "relative_flow": fraction, "active": fraction > threshold}
    return result


def _canonical_unlabelled_topology(edges: Sequence[tuple[str, str]], maximum_nodes: int) -> str:
    nodes = sorted({node for edge in edges for node in edge})
    if len(nodes) < 2 or len(nodes) > maximum_nodes:
        raise IntegrationIntakeViolation("active topology is outside the registered canonicalization bound")
    simple = {tuple(sorted(edge)) for edge in edges}
    if any(a == b for a, b in simple):
        raise IntegrationIntakeViolation("active topology contains a self edge")
    best = None
    for order in permutations(nodes):
        bits = "".join("1" if tuple(sorted((order[i], order[j]))) in simple else "0" for i in range(len(order)) for j in range(i + 1, len(order)))
        if best is None or bits < best:
            best = bits
    descriptor = {"node_count": len(nodes), "edge_count": len(simple), "adjacency_upper_triangle": best}
    return digest(descriptor)


def active_path_evidence(candidate: Mapping[str, Any], activity: Mapping[str, Any]) -> dict[str, Any]:
    try:
        fine = candidate["training"]["primary"]["levels"][-1]
        mechanical = _edge_rows(fine["mechanical_field"], float(activity["mechanical_input_n"]), float(activity["relative_flow_threshold"]))
        thermal = _edge_rows(fine["thermal_field"], float(activity["thermal_input_w"]), float(activity["relative_flow_threshold"]))
    except (KeyError, IndexError, TypeError) as error:
        raise IntegrationIntakeViolation(f"candidate field evidence is incomplete: {error}") from error
    if set(mechanical) != set(thermal):
        raise IntegrationIntakeViolation("mechanical and thermal edge coverage differs")
    coupled = []
    rows = []
    for edge_id in sorted(mechanical):
        if (mechanical[edge_id]["a"], mechanical[edge_id]["b"]) != (thermal[edge_id]["a"], thermal[edge_id]["b"]):
            raise IntegrationIntakeViolation("mechanical and thermal edge endpoints differ")
        is_coupled = mechanical[edge_id]["active"] and thermal[edge_id]["active"]
        if is_coupled:
            coupled.append((mechanical[edge_id]["a"], mechanical[edge_id]["b"]))
        rows.append({"edge_id": edge_id, "a": mechanical[edge_id]["a"], "b": mechanical[edge_id]["b"], "mechanical_relative_flow": mechanical[edge_id]["relative_flow"], "thermal_relative_flow": thermal[edge_id]["relative_flow"], "coupled_active": is_coupled})
    signature = _canonical_unlabelled_topology(coupled, int(activity["maximum_canonical_active_nodes"]))
    return {"edges": rows, "active_mechanical_edge_count": sum(row["active"] for row in mechanical.values()), "active_thermal_edge_count": sum(row["active"] for row in thermal.values()), "active_coupled_edge_count": len(coupled), "inactive_edge_count": len(rows) - len(coupled), "active_topology_sha256": signature}


def _verify_source(config: Mapping[str, Any], report: Mapping[str, Any]) -> Mapping[str, Any]:
    allowed = {"deterministic_evidence", "decision_replay", "timing_observations", "scientific_admission", "limitations", "execution_replay"}
    if not isinstance(report, Mapping) or not set(report) <= allowed or not {"deterministic_evidence", "decision_replay", "scientific_admission"} <= set(report):
        raise IntegrationIntakeViolation("Work 100 report schema mismatch")
    deterministic = report["deterministic_evidence"]
    if not isinstance(deterministic, Mapping) or "deterministic_sha256" not in deterministic:
        raise IntegrationIntakeViolation("Work 100 deterministic evidence is missing")
    unsealed = deepcopy(dict(deterministic))
    observed_sha = unsealed.pop("deterministic_sha256")
    if digest(unsealed) != observed_sha or observed_sha != config["source"]["work100_deterministic_sha256"]:
        raise IntegrationIntakeViolation("Work 100 deterministic identity mismatch")
    if deterministic.get("registration_sha256") != config["source"]["work100_registration_sha256"]:
        raise IntegrationIntakeViolation("Work 100 registration identity mismatch")
    candidates = deterministic.get("candidates")
    survivors = deterministic.get("survivors")
    if not isinstance(candidates, list) or not isinstance(survivors, list):
        raise IntegrationIntakeViolation("Work 100 candidate evidence is missing")
    if len(candidates) != config["source"]["expected_candidate_count"] or len(survivors) != config["source"]["expected_survivor_count"]:
        raise IntegrationIntakeViolation("Work 100 candidate or survivor count mismatch")
    ids = [candidate.get("candidate_id") for candidate in candidates]
    flagged = {candidate.get("candidate_id") for candidate in candidates if candidate.get("candidate_survivor") is True}
    if len(ids) != len(set(ids)) or set(survivors) != flagged or len(flagged) != len(survivors):
        raise IntegrationIntakeViolation("Work 100 survivor membership mismatch")
    admission = report["scientific_admission"]
    if admission.get("accounting_admissible") is not True or admission.get("scientific_survivors") != len(survivors) or admission.get("physical_validation") is not False:
        raise IntegrationIntakeViolation("Work 100 scientific admission is not reusable for intake")
    return deterministic


def audit_work100_result(config: Mapping[str, Any], report: Mapping[str, Any]) -> dict[str, Any]:
    validation = validate_config(config)
    deterministic = _verify_source(config, report)
    candidates = deterministic["candidates"]
    fixed = {}
    for candidate in candidates:
        if candidate.get("treatment") == "FIXED_TOPOLOGY":
            seed = candidate.get("seed")
            if seed in fixed:
                raise IntegrationIntakeViolation("paired fixed control is duplicated")
            fixed[seed] = candidate
    seeds = {candidate.get("seed") for candidate in candidates}
    if set(fixed) != seeds:
        raise IntegrationIntakeViolation("paired fixed control is missing")
    path_by_id = {candidate["candidate_id"]: active_path_evidence(candidate, config["activity"]) for candidate in candidates}
    rows = []
    for candidate in sorted(candidates, key=lambda item: (item["treatment"], item["seed"], item["candidate_id"])):
        baseline = fixed[candidate["seed"]]
        path = path_by_id[candidate["candidate_id"]]
        baseline_path = path_by_id[baseline["candidate_id"]]
        try:
            delta = float(candidate["training"]["value"]) - float(baseline["training"]["value"])
            uncertainty = float(candidate["training"]["error"]) + float(baseline["training"]["error"])
        except (KeyError, TypeError, ValueError) as error:
            raise IntegrationIntakeViolation("candidate response evidence is malformed") from error
        active_distinct = path["active_topology_sha256"] != baseline_path["active_topology_sha256"]
        declared_distinct = candidate["functional_signature"] != baseline["functional_signature"]
        detectable = abs(delta) > uncertainty
        meaningful = abs(delta) >= float(config["activity"]["minimum_meaningful_utilization_difference"])
        if candidate["candidate_survivor"] is not True:
            classification = "not_a_scoped_survivor"
        elif active_distinct and meaningful:
            classification = "functional_mechanism_candidate"
        elif active_distinct:
            classification = "active_topology_change_below_meaningful_effect"
        elif declared_distinct:
            classification = "declared_topology_only_inactive_appendage"
        elif detectable and meaningful:
            classification = "meaningful_shape_response_same_active_topology"
        elif detectable:
            classification = "shape_response_variant_below_meaningful_effect"
        else:
            classification = "no_resolved_functional_difference"
        rows.append({
            "candidate_id": candidate["candidate_id"], "treatment": candidate["treatment"], "seed": candidate["seed"],
            "candidate_survivor": candidate["candidate_survivor"], "declared_signature_distinct_from_fixed": declared_distinct,
            "active_topology_distinct_from_fixed": active_distinct, "training_utilization_difference_from_fixed": delta,
            "combined_numerical_error": uncertainty, "response_difference_detectable": detectable,
            "response_difference_meaningful": meaningful, "classification": classification, "path_evidence": path,
            "typed_subsystem_intake_eligible": bool(candidate["candidate_survivor"]),
        })
    required_capabilities = set(config["capabilities"]["required_vehicle"])
    contributed = set(config["capabilities"]["work100_contribution"])
    required_evidence = set(config["evidence"]["required_for_program_exit"])
    provided_evidence = set(config["evidence"]["provided_by_work100"])
    mechanism_count = sum(row["classification"] == "functional_mechanism_candidate" for row in rows)
    shape_count = sum(row["classification"] in {"meaningful_shape_response_same_active_topology", "shape_response_variant_below_meaningful_effect"} for row in rows)
    inactive_count = sum(row["classification"] == "declared_topology_only_inactive_appendage" for row in rows)
    body = {
        "schema": RESULT_SCHEMA,
        "config_sha256": validation["config_sha256"],
        "source": {"registration_sha256": deterministic["registration_sha256"], "deterministic_sha256": deterministic["deterministic_sha256"]},
        "candidate_causality": rows,
        "summary": {"candidate_count": len(rows), "scoped_survivor_count": sum(row["candidate_survivor"] for row in rows), "functional_mechanism_candidate_count": mechanism_count, "shape_response_variant_count": shape_count, "inactive_declared_topology_count": inactive_count, "preferred_hypothesis_supported": mechanism_count > 0},
        "integration_intake": {
            "status": "blocked_incomplete_capability_and_evidence_coverage",
            "contributed_capabilities": sorted(contributed),
            "missing_vehicle_capabilities": sorted(required_capabilities - contributed),
            "provided_evidence": sorted(provided_evidence),
            "missing_program_exit_evidence": sorted(required_evidence - provided_evidence),
            "subsystem_survivors_preserved": True,
            "promotion_ready": False,
            "whole_vehicle_candidate_created": False,
            "work101_program_exit": False,
        },
        "claim_boundary": deepcopy(config["claim_boundary"]),
    }
    return {**body, "result_sha256": digest(body)}
