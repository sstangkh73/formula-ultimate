"""Deterministic whole-candidate closure checks for Work 126."""
from __future__ import annotations

import hashlib
import json
from collections import deque
from typing import Any, Mapping

PROTOCOL_VERSION = "detailed_vehicle_closure_v1"


class DetailedVehicleClosureViolation(ValueError):
    pass


def canonical_sha256(value):
    try:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        raise DetailedVehicleClosureViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()


def _box(component, offset_y=0.0):
    center = component["center_m"][:]
    center[1] += offset_y
    half = [x / 2 for x in component["size_m"]]
    return ([center[i] - half[i] for i in range(3)], [center[i] + half[i] for i in range(3)])


def _overlap(a, b, tolerance):
    return all(min(a[1][i], b[1][i]) - max(a[0][i], b[0][i]) > tolerance for i in range(3))


def _connected(network):
    graph = {node: [] for node in network["nodes"]}
    for left, right in network["edges"]:
        if left not in graph or right not in graph:
            return False
        graph[left].append(right)
        graph[right].append(left)
    # Explicit BFS avoids relying on edge direction.
    seen = {network["source"]}
    queue = deque(seen)
    while queue:
        node = queue.popleft()
        for next_node in graph[node]:
            if next_node not in seen:
                seen.add(next_node)
                queue.append(next_node)
    return network["sink"] in seen


def validate_protocol(raw: Mapping[str, Any]):
    required = {"protocol_version", "units", "dependencies", "inputs", "registration", "components", "functions", "networks", "motion", "ledgers", "unresolved", "coverage", "experiment"}
    if set(raw) != required or raw.get("protocol_version") != PROTOCOL_VERSION:
        raise DetailedVehicleClosureViolation("protocol schema or identity mismatch")
    if raw.get("units") != "SI":
        raise DetailedVehicleClosureViolation("SI units are required")
    if {item.get("work") for item in raw["dependencies"]} != set(range(118, 126)):
        raise DetailedVehicleClosureViolation("Work 118 through 125 dependencies are required")
    if raw["registration"].get("geometry_detail") != "G3_registry":
        raise DetailedVehicleClosureViolation("G3 registry was not frozen")
    if not raw["unresolved"]:
        raise DetailedVehicleClosureViolation("essential unresolved evidence must remain observable")
    return {"status": "passed", "protocol_sha256": canonical_sha256(raw)}


def evaluate_closure(raw: Mapping[str, Any]):
    validate_protocol(raw)
    components = raw["components"]
    ids = [item["id"] for item in components]
    regions = [item["region_id"] for item in components]
    if len(ids) != len(set(ids)):
        raise DetailedVehicleClosureViolation("duplicate component identity")
    if len(regions) != len(set(regions)):
        raise DetailedVehicleClosureViolation("double mass ownership")
    required_roles = set(raw["registration"]["required_hardware_roles"])
    roles = {item["role"] for item in components}
    missing_roles = sorted(required_roles - roles)
    if missing_roles:
        raise DetailedVehicleClosureViolation("missing required hardware role: " + ",".join(missing_roles))
    component_ids = set(ids)
    missing_functions = sorted(name for name, owners in raw["functions"].items() if not owners or not set(owners) <= component_ids)
    if missing_functions:
        raise DetailedVehicleClosureViolation("unclosed external function: " + ",".join(missing_functions))

    tolerance = raw["registration"]["tolerance_m"]
    envelope = raw["registration"]["envelope_m"]
    if any(item["envelope_revision"] != raw["registration"]["subsystem_envelope_revision"] for item in components):
        raise DetailedVehicleClosureViolation("stale subsystem envelope")
    boxes = {item["id"]: _box(item) for item in components}
    for item in components:
        bounds = boxes[item["id"]]
        if any(bounds[0][i] < envelope[0][i] - tolerance or bounds[1][i] > envelope[1][i] + tolerance for i in range(3)):
            raise DetailedVehicleClosureViolation("hidden void or out-of-envelope geometry")
    collisions = []
    for index, left in enumerate(ids):
        for right in ids[index + 1 :]:
            if _overlap(boxes[left], boxes[right], tolerance):
                collisions.append([left, right])
    if collisions:
        raise DetailedVehicleClosureViolation("assembly interference")

    motion = raw["motion"]
    mover = next(item for item in components if item["id"] == motion["component"])
    motion_collisions = []
    for sample in motion["offset_y_samples_m"]:
        moved = _box(mover, sample)
        for other in components:
            if other["id"] != mover["id"] and _overlap(moved, boxes[other["id"]], tolerance):
                motion_collisions.append({"sample_m": sample, "other": other["id"]})
    if motion_collisions:
        raise DetailedVehicleClosureViolation("swept motion interference")

    network_status = {name: _connected(network) for name, network in raw["networks"].items()}
    if not all(network_status.values()):
        raise DetailedVehicleClosureViolation("open energy, signal, heat, or load path")
    mass = sum(item["mass_kg"] for item in components)
    center = [sum(item["mass_kg"] * item["center_m"][i] for item in components) / mass for i in range(3)]
    inertia = []
    for axis in range(3):
        other = [i for i in range(3) if i != axis]
        inertia.append(sum(item["mass_kg"] * ((item["size_m"][other[0]] ** 2 + item["size_m"][other[1]] ** 2) / 12 + sum((item["center_m"][i] - center[i]) ** 2 for i in other)) for item in components))
    volume = sum(item["size_m"][0] * item["size_m"][1] * item["size_m"][2] for item in components)
    computed = {"mass_kg": mass, "center_m": center, "inertia_kg_m2": inertia, "occupied_volume_m3": volume}
    residuals = {
        key: (computed[key] - raw["ledgers"][key] if isinstance(computed[key], float) else [a - b for a, b in zip(computed[key], raw["ledgers"][key])])
        for key in computed
    }
    numeric_residuals = [abs(value) for value in residuals.values() if isinstance(value, float)] + [abs(value) for values in residuals.values() if isinstance(values, list) for value in values]
    if max(numeric_residuals, default=0.0) > raw["registration"]["ledger_tolerance"]:
        raise DetailedVehicleClosureViolation("mass, inertia, or volume ledger does not close")
    return {"component_count": len(components), "function_count": len(raw["functions"]), "hardware_roles": sorted(roles), "network_status": network_status, "collisions": collisions, "motion_collisions": motion_collisions, "computed_ledgers": computed, "ledger_residuals": residuals, "all_paths_closed": True}
