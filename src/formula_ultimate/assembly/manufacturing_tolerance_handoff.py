"""Manufacturing-route, assembly-access and tolerance checks for Work 130."""
from __future__ import annotations

import hashlib
import json
from collections import deque
from typing import Any, Mapping

PROTOCOL_VERSION = "manufacturing_tolerance_handoff_v1"
SUPPORTED_EVIDENCE = {"measured_process_capability", "qualified_supplier_process"}


class ManufacturingHandoffViolation(ValueError):
    pass


def canonical_sha256(value):
    try:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        raise ManufacturingHandoffViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()


def validate_protocol(raw: Mapping[str, Any]):
    required = {"protocol_version", "units", "dependencies", "inputs", "registry", "registration", "routes", "assembly_steps", "tolerance_cases", "unresolved", "coverage", "experiment"}
    if set(raw) != required or raw.get("protocol_version") != PROTOCOL_VERSION:
        raise ManufacturingHandoffViolation("protocol schema or identity mismatch")
    if raw.get("units") != "SI":
        raise ManufacturingHandoffViolation("SI units are required")
    if {item.get("work") for item in raw["dependencies"]} != {126, 129}:
        raise ManufacturingHandoffViolation("Work 126 and 129 dependencies are required")
    required_regions = set(raw["registration"]["required_regions"])
    mapped_regions = [item["region_id"] for item in raw["routes"]]
    if set(mapped_regions) != required_regions or len(mapped_regions) != len(set(mapped_regions)):
        raise ManufacturingHandoffViolation("region route mapping is incomplete or duplicated")
    if not raw["unresolved"]:
        raise ManufacturingHandoffViolation("unresolved process evidence must remain observable")
    return {"status": "passed", "protocol_sha256": canonical_sha256(raw)}


def _assembly_order(steps):
    ids = {item["id"] for item in steps}
    if any(not set(item["after"]) <= ids for item in steps):
        raise ManufacturingHandoffViolation("assembly order references unknown step")
    outgoing = {item: [] for item in ids}
    indegree = {item: 0 for item in ids}
    for step in steps:
        for parent in step["after"]:
            outgoing[parent].append(step["id"])
            indegree[step["id"]] += 1
    queue = deque(sorted(item for item, count in indegree.items() if count == 0))
    order = []
    while queue:
        item = queue.popleft(); order.append(item)
        for child in outgoing[item]:
            indegree[child] -= 1
            if indegree[child] == 0: queue.append(child)
    if len(order) != len(ids):
        raise ManufacturingHandoffViolation("impossible cyclic assembly order")
    return order


def evaluate_handoff(raw: Mapping[str, Any]):
    validate_protocol(raw)
    inaccessible = [item["region_id"] for item in raw["routes"] if not item["tool_access"] or not item["inspection_access"]]
    if inaccessible:
        raise ManufacturingHandoffViolation("inaccessible fastener or inspection feature")
    trapped = [item["region_id"] for item in raw["routes"] if item["trapped_internal_core"]]
    if trapped:
        raise ManufacturingHandoffViolation("trapped internal core")
    order = _assembly_order(raw["assembly_steps"])
    tolerance_results = []
    for case in raw["tolerance_cases"]:
        if case["kind"] == "clearance":
            nominal = case["nominal_clearance_m"]
            worst = nominal - case["feature_a_tolerance_m"] - case["feature_b_tolerance_m"]
            passed = worst >= case["required_minimum_m"]
            tolerance_results.append({"id": case["id"], "kind": case["kind"], "nominal_m": nominal, "worst_case_m": worst, "required_minimum_m": case["required_minimum_m"], "passed": passed})
        elif case["kind"] == "preload":
            nominal = case["nominal_preload_n"]
            worst = nominal - case["preload_tolerance_n"]
            passed = worst >= case["required_minimum_n"]
            tolerance_results.append({"id": case["id"], "kind": case["kind"], "nominal_n": nominal, "worst_case_n": worst, "required_minimum_n": case["required_minimum_n"], "passed": passed})
        else:
            raise ManufacturingHandoffViolation("unknown tolerance case")
    if not all(item["passed"] for item in tolerance_results):
        raise ManufacturingHandoffViolation("worst-case clearance or preload fails")
    route_status = {item["region_id"]: ("supported" if item["evidence_class"] in SUPPORTED_EVIDENCE else "unknown_missing_capability_evidence") for item in raw["routes"]}
    readiness = all(value == "supported" for value in route_status.values()) and raw["coverage"]["native_manufacturing_CAD"] == "available"
    return {"route_status": route_status, "assembly_order": order, "tolerance_results": tolerance_results, "all_accessible": True, "manufacturing_ready": readiness, "unknown_route_count": sum(value.startswith("unknown") for value in route_status.values())}
