"""Fail-closed constructive and manufacturing fixture gate for Work 095."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
import re
from typing import Any, Mapping


GATE_VERSION = "constructive_validity_manufacturing_gate_v1"
REPAIR_OPERATIONS = ("add_support", "increase_escape_hole", "increase_joining_access")
EVIDENCE_FIELDS = {
    "brep_valid", "solid_count", "self_intersection_count", "zero_thickness_entity_count",
    "minimum_wall_m", "minimum_ligament_m", "minimum_radius_m", "minimum_feature_m",
    "tool_access_fraction", "maximum_unsupported_overhang_rad", "support_present",
    "enclosed_void_count", "minimum_escape_hole_m", "requested_tolerance_m",
    "joining_access_fraction",
}
LIMIT_FIELDS = {
    "minimum_wall_m", "minimum_ligament_m", "minimum_radius_m", "minimum_feature_m",
    "minimum_tool_access_fraction", "maximum_unsupported_overhang_rad", "support_allowed",
    "enclosed_void_allowed", "minimum_escape_hole_m", "minimum_achievable_tolerance_m",
    "minimum_joining_access_fraction",
}
_ID = re.compile(r"^[a-z][a-z0-9_.-]*$")
_SHA = re.compile(r"^[0-9a-f]{64}$")


class ConstructiveValidityError(ValueError):
    """Raised for invalid gate declarations rather than candidate rejection."""


def canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ConstructiveValidityError(f"canonicalization failed: {error}") from error


def declaration_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _exact(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    if not isinstance(value, Mapping) or set(value) != expected:
        raise ConstructiveValidityError(f"{label} schema mismatch")


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise ConstructiveValidityError(f"{label} must be a lower-case identifier")
    return value


def _sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or not _SHA.fullmatch(value):
        raise ConstructiveValidityError(f"{label} must be SHA-256")
    return value


def _finite(value: Any, label: str, *, minimum: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < minimum:
        raise ConstructiveValidityError(f"{label} must be finite and >= {minimum}")
    return float(value)


def _processes(config: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {item["process_id"]: item for item in config["process_profiles"]}


def validate_gate_config(config: Mapping[str, Any], *, mutation_protocol_sha256: str) -> dict[str, Any]:
    _exact(config, {"gate_version", "source_mutation_protocol_sha256", "source_solid_declaration_sha256", "source_primitive_manifest_sha256", "evaluation_phase", "measurement_evidence", "repair_policy", "process_profiles", "representation_families", "base_candidate", "scenarios"}, "gate")
    if config["gate_version"] != GATE_VERSION or config["source_mutation_protocol_sha256"] != mutation_protocol_sha256:
        raise ConstructiveValidityError("gate version or mutation protocol identity mismatch")
    _sha(config["source_solid_declaration_sha256"], "source solid declaration")
    _sha(config["source_primitive_manifest_sha256"], "source primitive manifest")
    if config["evaluation_phase"] != "pre_performance_evaluation":
        raise ConstructiveValidityError("gate must run before performance evaluation")
    measurement = config["measurement_evidence"]
    _exact(measurement, {"status", "method", "claim_boundary"}, "measurement evidence")
    if measurement["status"] != "synthetic_contract_fixture" or not all(isinstance(measurement[key], str) and measurement[key] for key in ("method", "claim_boundary")):
        raise ConstructiveValidityError("synthetic measurement boundary is missing")
    repair = config["repair_policy"]
    _exact(repair, {"allowed_operations", "maximum_operations", "hidden_repair_policy"}, "repair policy")
    if tuple(repair["allowed_operations"]) != REPAIR_OPERATIONS or isinstance(repair["maximum_operations"], bool) or not isinstance(repair["maximum_operations"], int) or not 0 <= repair["maximum_operations"] <= 3 or repair["hidden_repair_policy"] != "reject":
        raise ConstructiveValidityError("repair policy mismatch")
    process_ids = set()
    for process in config["process_profiles"]:
        _exact(process, {"process_id", "process_type", "compatible_material_ids", "limits"}, "process profile")
        process_id = _identifier(process["process_id"], "process_id")
        if process_id in process_ids or process["process_type"] not in {"additive", "machining", "casting", "forming", "composite"}:
            raise ConstructiveValidityError("duplicate or unsupported process")
        process_ids.add(process_id)
        materials = process["compatible_material_ids"]
        if not isinstance(materials, list) or not materials or len(materials) != len(set(materials)):
            raise ConstructiveValidityError("process compatibility list is invalid")
        for material in materials: _identifier(material, "material_id")
        limits = process["limits"]; _exact(limits, LIMIT_FIELDS, "process limits")
        for key in LIMIT_FIELDS - {"support_allowed", "enclosed_void_allowed"}: _finite(limits[key], key)
        if type(limits["support_allowed"]) is not bool or type(limits["enclosed_void_allowed"]) is not bool:
            raise ConstructiveValidityError("process Boolean limit is invalid")
        if limits["maximum_unsupported_overhang_rad"] > math.pi or any(not 0 <= limits[key] <= 1 for key in ("minimum_tool_access_fraction", "minimum_joining_access_fraction")):
            raise ConstructiveValidityError("process fractional or angular limit is invalid")
    families = config["representation_families"]
    if not isinstance(families, list) or len(families) != 6:
        raise ConstructiveValidityError("six representation families are required")
    family_ids = set(); source_ids = set()
    for family in families:
        _exact(family, {"family", "source_collection", "source_candidate_id", "source_geometry_sha256"}, "representation family")
        family_id = _identifier(family["family"], "family")
        if family_id in family_ids or family["source_candidate_id"] in source_ids or family["source_collection"] not in {"primitive_witness", "work092_solid"}:
            raise ConstructiveValidityError("representation family is duplicated or invalid")
        family_ids.add(family_id); source_ids.add(_identifier(family["source_candidate_id"], "source candidate")); _sha(family["source_geometry_sha256"], "source geometry")
    base = config["base_candidate"]
    _exact(base, {"material_id", "process_id", "evaluation_observed", "evidence"}, "base candidate")
    _identifier(base["material_id"], "base material"); _identifier(base["process_id"], "base process")
    if base["process_id"] not in process_ids or base["evaluation_observed"] is not False:
        raise ConstructiveValidityError("base process or evaluation state is invalid")
    _validate_evidence(base["evidence"])
    scenarios = config["scenarios"]
    if not isinstance(scenarios, list) or len(scenarios) != 8:
        raise ConstructiveValidityError("eight matched scenarios are required")
    scenario_ids = set()
    for scenario in scenarios:
        _exact(scenario, {"scenario_id", "evidence_overrides", "proposed_repairs", "unrecorded_repair_detected"}, "scenario")
        scenario_id = _identifier(scenario["scenario_id"], "scenario_id")
        if scenario_id in scenario_ids or not isinstance(scenario["evidence_overrides"], Mapping) or not set(scenario["evidence_overrides"]).issubset(EVIDENCE_FIELDS):
            raise ConstructiveValidityError("scenario is duplicated or overrides unknown evidence")
        scenario_ids.add(scenario_id)
        candidate_evidence = {**base["evidence"], **scenario["evidence_overrides"]}; _validate_evidence(candidate_evidence)
        if not isinstance(scenario["proposed_repairs"], list) or any(item not in REPAIR_OPERATIONS for item in scenario["proposed_repairs"]) or type(scenario["unrecorded_repair_detected"]) is not bool:
            raise ConstructiveValidityError("scenario repair declaration is invalid")
    return {"status": "passed", "family_count": len(families), "scenarios_per_family": len(scenarios), "total_opportunities": len(families) * len(scenarios), "gate_sha256": declaration_sha256(config)}


def _validate_evidence(evidence: Mapping[str, Any]) -> None:
    _exact(evidence, EVIDENCE_FIELDS, "candidate evidence")
    if type(evidence["brep_valid"]) is not bool or type(evidence["support_present"]) is not bool:
        raise ConstructiveValidityError("candidate evidence Boolean is invalid")
    for key in {"solid_count", "self_intersection_count", "zero_thickness_entity_count", "enclosed_void_count"}:
        if isinstance(evidence[key], bool) or not isinstance(evidence[key], int) or evidence[key] < 0:
            raise ConstructiveValidityError(f"{key} must be a non-negative integer")
    for key in EVIDENCE_FIELDS - {"brep_valid", "support_present", "solid_count", "self_intersection_count", "zero_thickness_entity_count", "enclosed_void_count"}:
        _finite(evidence[key], key)
    if evidence["maximum_unsupported_overhang_rad"] > math.pi or any(not 0 <= evidence[key] <= 1 for key in ("tool_access_fraction", "joining_access_fraction")):
        raise ConstructiveValidityError("candidate fractional or angular evidence is invalid")


def build_candidate(config: Mapping[str, Any], family: Mapping[str, Any], scenario: Mapping[str, Any]) -> dict[str, Any]:
    evidence = {**deepcopy(config["base_candidate"]["evidence"]), **deepcopy(scenario["evidence_overrides"])}
    return {
        "candidate_id": f"{family['family']}_{scenario['scenario_id']}", "representation_family": family["family"],
        "source_candidate_id": family["source_candidate_id"], "source_geometry_sha256": family["source_geometry_sha256"],
        "material_id": config["base_candidate"]["material_id"], "process_id": config["base_candidate"]["process_id"],
        "evaluation_observed": config["base_candidate"]["evaluation_observed"], "evidence_status": config["measurement_evidence"]["status"],
        "evidence": evidence, "proposed_repairs": list(scenario["proposed_repairs"]),
        "unrecorded_repair_detected": scenario["unrecorded_repair_detected"],
    }


def evaluate_candidate(candidate: Mapping[str, Any], config: Mapping[str, Any]) -> dict[str, Any]:
    expected = {"candidate_id", "representation_family", "source_candidate_id", "source_geometry_sha256", "material_id", "process_id", "evaluation_observed", "evidence_status", "evidence", "proposed_repairs", "unrecorded_repair_detected"}
    _exact(candidate, expected, "candidate")
    _identifier(candidate["candidate_id"], "candidate_id"); _identifier(candidate["representation_family"], "representation_family")
    _identifier(candidate["source_candidate_id"], "source_candidate_id"); _sha(candidate["source_geometry_sha256"], "source_geometry_sha256")
    _identifier(candidate["material_id"], "material_id"); _identifier(candidate["process_id"], "process_id")
    if type(candidate["evaluation_observed"]) is not bool or type(candidate["unrecorded_repair_detected"]) is not bool or candidate["evidence_status"] != "synthetic_contract_fixture":
        raise ConstructiveValidityError("candidate phase, repair, or evidence declaration is invalid")
    _validate_evidence(candidate["evidence"])
    repairs = candidate["proposed_repairs"]
    if not isinstance(repairs, list): raise ConstructiveValidityError("proposed repairs must be an array")
    original_sha = declaration_sha256(candidate); working = deepcopy(candidate); trace = []; pre_violations = []
    policy = config["repair_policy"]
    if candidate["unrecorded_repair_detected"]: pre_violations.append("hidden_repair")
    if len(repairs) > policy["maximum_operations"]: pre_violations.append("repair_budget_exceeded")
    if repairs and candidate["evaluation_observed"]: pre_violations.append("post_observation_repair_prohibited")
    for index, operation in enumerate(repairs):
        if operation not in policy["allowed_operations"]:
            pre_violations.append("unregistered_repair"); continue
        if pre_violations: continue
        before = declaration_sha256(working["evidence"])
        limits = _processes(config).get(working["process_id"], {}).get("limits", {})
        if operation == "add_support": working["evidence"]["support_present"] = True
        elif operation == "increase_escape_hole": working["evidence"]["minimum_escape_hole_m"] = limits["minimum_escape_hole_m"]
        elif operation == "increase_joining_access": working["evidence"]["joining_access_fraction"] = limits["minimum_joining_access_fraction"]
        trace.append({"index": index, "operation": operation, "evidence_sha256_before": before, "evidence_sha256_after": declaration_sha256(working["evidence"])})
    violations = list(dict.fromkeys(pre_violations + _violations(working, config)))
    status = "rejected" if violations else ("repaired" if trace else "accepted")
    repaired_sha = declaration_sha256(working)
    body = {
        "status": status, "candidate_id": candidate["candidate_id"], "representation_family": candidate["representation_family"],
        "source_candidate_id": candidate["source_candidate_id"], "source_geometry_sha256": candidate["source_geometry_sha256"],
        "process_id": candidate["process_id"], "material_id": candidate["material_id"], "evidence_status": candidate["evidence_status"],
        "violations": violations, "repair_trace": trace, "original_genotype_sha256": original_sha,
        "evaluated_genotype_sha256": repaired_sha, "geometry_changed_by_declared_repair": bool(trace),
        "performance_evidence_used": False,
    }
    return {**body, "provenance_sha256": declaration_sha256(body)}


def _violations(candidate: Mapping[str, Any], config: Mapping[str, Any]) -> list[str]:
    evidence = candidate["evidence"]; process = _processes(config).get(candidate["process_id"]); result = []
    if process is None: return ["unknown_process"]
    limits = process["limits"]
    if candidate["material_id"] not in process["compatible_material_ids"]: result.append("material_process_incompatible")
    if not evidence["brep_valid"]: result.append("invalid_brep")
    if evidence["solid_count"] != 1: result.append("invalid_solid_count")
    if evidence["self_intersection_count"]: result.append("self_intersection")
    if evidence["zero_thickness_entity_count"]: result.append("zero_thickness")
    for field, limit, code in (
        ("minimum_wall_m", "minimum_wall_m", "wall_below_minimum"),
        ("minimum_ligament_m", "minimum_ligament_m", "ligament_below_minimum"),
        ("minimum_radius_m", "minimum_radius_m", "radius_below_minimum"),
        ("minimum_feature_m", "minimum_feature_m", "sliver_feature"),
    ):
        if evidence[field] < limits[limit]: result.append(code)
    if evidence["tool_access_fraction"] < limits["minimum_tool_access_fraction"]: result.append("tool_access_blocked")
    if evidence["maximum_unsupported_overhang_rad"] > limits["maximum_unsupported_overhang_rad"] and not evidence["support_present"]: result.append("unsupported_overhang")
    if evidence["support_present"] and not limits["support_allowed"]: result.append("support_forbidden")
    if evidence["enclosed_void_count"] and (not limits["enclosed_void_allowed"] or evidence["minimum_escape_hole_m"] < limits["minimum_escape_hole_m"]): result.append("enclosed_void_not_vented")
    if evidence["requested_tolerance_m"] < limits["minimum_achievable_tolerance_m"]: result.append("tolerance_too_tight")
    if evidence["joining_access_fraction"] < limits["minimum_joining_access_fraction"]: result.append("joining_access_blocked")
    return result
