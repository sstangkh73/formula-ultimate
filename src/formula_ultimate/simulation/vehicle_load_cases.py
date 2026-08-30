"""Balanced quasi-static whole-vehicle load cases for Work 048."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from typing import Any, Mapping, Sequence

from formula_ultimate.topology.vehicle_assembly import (
    Assembly,
    declaration_sha256,
    from_mapping,
    mass_properties,
    validate,
)
from .structural_failure_coupling import (
    ConnectionDefinition,
    FailureEvidence,
    GateAIdentity,
    evaluate_structural_failure_step,
    initial_network_state,
)


LOAD_CASE_ADAPTER_VERSION = "quasi_static_tree_wrench_v1"


class VehicleLoadCaseError(ValueError):
    """Raised when Work 048 evidence is missing, inconsistent, or unbalanced."""


@dataclass(frozen=True, slots=True)
class ConnectionLoad:
    connection_id: str
    force_n: tuple[float, float, float]
    moment_nm: tuple[float, float, float]
    force_magnitude_n: float
    moment_magnitude_nm: float
    utilization: float
    health_state: str


@dataclass(frozen=True, slots=True)
class VehicleLoadCaseResult:
    case_id: str
    partition: str
    snapshot_sha256: str
    global_residual: tuple[float, float, float, float, float, float]
    maximum_component_residual: float
    maximum_interface_residual: float
    connection_loads: tuple[ConnectionLoad, ...]
    outcome: str
    failure_contract_status: str
    result_sha256: str


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _vector(value: Sequence[Any], size: int, name: str) -> tuple[float, ...]:
    if len(value) != size:
        raise VehicleLoadCaseError(f"{name} must contain {size} values")
    result = tuple(float(item) for item in value)
    if not all(math.isfinite(item) for item in result):
        raise VehicleLoadCaseError(f"{name} must be finite")
    return result


def _add(*values: Sequence[float]) -> tuple[float, ...]:
    return tuple(math.fsum(value[index] for value in values) for index in range(len(values[0])))


def _neg(value: Sequence[float]) -> tuple[float, ...]:
    return tuple(-item for item in value)


def _cross(a: Sequence[float], b: Sequence[float]) -> tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _norm(value: Sequence[float]) -> float:
    return math.sqrt(math.fsum(item * item for item in value))


def _wrench(force: Sequence[float], moment: Sequence[float]) -> tuple[float, ...]:
    return tuple(force) + tuple(moment)


def _relative_error(actual: float, expected: float) -> float:
    return abs(actual - expected) / max(abs(expected), 1.0e-300)


def validate_protocol(
    protocol: Mapping[str, Any],
    assembly_raw: Mapping[str, Any],
    *,
    assembly_config_sha256: str,
    assembly_step_sha256: str,
    failure_config_sha256: str,
) -> Assembly:
    if protocol.get("protocol_id") != "whole_vehicle_load_cases_v1":
        raise VehicleLoadCaseError("load-case protocol identity mismatch")
    if protocol.get("adapter_version") != LOAD_CASE_ADAPTER_VERSION:
        raise VehicleLoadCaseError("load-case adapter version mismatch")
    identity = protocol["assembly_identity"]
    expected = {
        "protocol_id": assembly_raw.get("protocol_id"),
        "config_sha256": assembly_config_sha256,
        "declaration_sha256": declaration_sha256(assembly_raw),
        "assembly_step_sha256": assembly_step_sha256,
    }
    for key, value in expected.items():
        if identity.get(key) != value:
            raise VehicleLoadCaseError(f"assembly {key} identity mismatch")
    failure_identity = protocol["failure_identity"]
    if failure_identity.get("protocol_id") != assembly_raw.get("failure_contract"):
        raise VehicleLoadCaseError("failure protocol identity mismatch")
    if failure_identity.get("config_sha256") != failure_config_sha256:
        raise VehicleLoadCaseError("failure config identity mismatch")
    assembly = from_mapping(assembly_raw)
    validate(assembly)
    actual = mass_properties(assembly)
    pinned = identity["mass_properties"]
    tolerance = float(protocol["tolerances"]["mass_property_relative"])
    comparisons = [(actual["mass_kg"], pinned["mass_kg"])]
    comparisons.extend(zip(actual["centre_of_mass_m"], pinned["centre_of_mass_m"]))
    comparisons.extend(zip(actual["inertia_kg_m2"], pinned["inertia_kg_m2"]))
    if max(_relative_error(float(a), float(b)) for a, b in comparisons) > tolerance:
        raise VehicleLoadCaseError("mapped mass properties differ from pinned FreeCAD evidence")
    partitions = protocol["partitions"]
    membership = [case_id for values in partitions.values() for case_id in values]
    case_ids = [item["case_id"] for item in protocol["cases"]]
    if len(membership) != len(set(membership)):
        raise VehicleLoadCaseError("load-case partition membership overlaps")
    if set(membership) != set(case_ids) or len(case_ids) != len(set(case_ids)):
        raise VehicleLoadCaseError("load-case partition identities are incomplete or duplicated")
    for item in protocol["cases"]:
        if item["case_id"] not in partitions.get(item["partition"], []):
            raise VehicleLoadCaseError("case partition declaration mismatch")
        if item.get("evidence") != protocol.get("required_evidence"):
            raise VehicleLoadCaseError("unsupported or incomplete load-case evidence")
    return assembly


def _external_wrenches(
    assembly: Assembly, case: Mapping[str, Any]
) -> dict[str, tuple[float, ...]]:
    acceleration = _vector(case["acceleration_m_per_s2"], 3, "acceleration")
    gravity = _vector(case["gravity_m_per_s2"], 3, "gravity")
    centre = mass_properties(assembly)["centre_of_mass_m"]
    external: dict[str, tuple[float, ...]] = {}
    for component in assembly.components:
        force = tuple(component.mass * (gravity[index] - acceleration[index]) for index in range(3))
        arm = tuple(component.position[index] - centre[index] for index in range(3))
        external[component.component_id] = _wrench(force, _cross(arm, force))
    aero_component = str(case["aero_component_id"])
    if aero_component not in external:
        raise VehicleLoadCaseError("aerodynamic wrench references unknown component")
    external[aero_component] = _add(external[aero_component], _vector(case["aero_wrench_at_com"], 6, "aero wrench"))
    interface_by_id = {item["interface_id"]: item for item in assembly.interfaces}
    contact_components = {
        interface_by_id[item["interface_id"]]["component_id"] for item in assembly.contacts
    }
    if len(contact_components) != 1:
        raise VehicleLoadCaseError("Work 048 admits exactly one ground-contact component")
    root = next(iter(contact_components))
    external[root] = _add(external[root], _vector(case["contact_wrench_at_com"], 6, "contact wrench"))
    return external


def _tree(assembly: Assembly) -> tuple[str, dict[str, str], dict[str, str], dict[str, list[str]]]:
    interface_by_id = {item["interface_id"]: item for item in assembly.interfaces}
    adjacency: dict[str, list[tuple[str, str]]] = {item.component_id: [] for item in assembly.components}
    for connection in assembly.connections:
        a = interface_by_id[connection["interface_a"]]["component_id"]
        b = interface_by_id[connection["interface_b"]]["component_id"]
        adjacency[a].append((b, connection["connection_id"]))
        adjacency[b].append((a, connection["connection_id"]))
    root = interface_by_id[assembly.contacts[0]["interface_id"]]["component_id"]
    parent: dict[str, str] = {}
    parent_connection: dict[str, str] = {}
    children: dict[str, list[str]] = {item.component_id: [] for item in assembly.components}
    stack = [root]
    seen = {root}
    while stack:
        node = stack.pop()
        for neighbour, connection_id in adjacency[node]:
            if neighbour in seen:
                continue
            seen.add(neighbour)
            parent[neighbour] = node
            parent_connection[neighbour] = connection_id
            children[node].append(neighbour)
            stack.append(neighbour)
    if len(seen) != len(assembly.components) or len(assembly.connections) != len(assembly.components) - 1:
        raise VehicleLoadCaseError("Work 048 requires one connected acyclic load tree")
    return root, parent, parent_connection, children


def _failure_contract(
    failed: ConnectionLoad | None,
    failure_raw: Mapping[str, Any],
    snapshot_sha256: str,
) -> tuple[str, str]:
    if failed is None:
        return "not_triggered", "running"
    gate_raw = failure_raw["gate_a_identity"]
    gate = GateAIdentity(
        gate_raw["remediation_protocol_id"], gate_raw["decision"], gate_raw["element_route_id"],
        gate_raw["support_topology_sha256"], gate_raw["boundary_model_id"],
    )
    definition = ConnectionDefinition(failed.connection_id, "whole_vehicle_critical_path", 1.0)
    applied = failed.force_n + failed.moment_nm
    state = initial_network_state(
        time_s=0.0,
        definitions=(definition,),
        stored_energy_by_connection_j={failed.connection_id: 1.0},
        applied_wrench=applied,
    )
    evidence = FailureEvidence(
        "overload_" + failed.connection_id,
        failed.connection_id,
        "fracture",
        0.5,
        failure_raw["mechanism_protocols"]["fracture"],
        snapshot_sha256,
        0.7,
    )
    coupled = evaluate_structural_failure_step(
        state=state,
        duration_s=1.0,
        definitions=(definition,),
        applied_wrench=applied,
        evidence=(evidence,),
        gate_identity=gate,
        expected_gate_identity=gate,
        mechanism_protocols=failure_raw["mechanism_protocols"],
        residual_relative_tolerance=float(failure_raw["tolerances"]["force_moment_residual_relative"]),
    )
    if coupled.status != "ok" or coupled.candidate_state is None:
        raise VehicleLoadCaseError("Work 046 failure contract rejected overload evidence")
    return coupled.status, coupled.outcome


def evaluate_load_case(
    protocol: Mapping[str, Any],
    assembly: Assembly,
    failure_raw: Mapping[str, Any],
    case_id: str,
) -> VehicleLoadCaseResult:
    cases = {item["case_id"]: item for item in protocol["cases"]}
    if case_id not in cases:
        raise VehicleLoadCaseError("unknown load case")
    case = cases[case_id]
    snapshot_sha = canonical_sha256(case)
    external = _external_wrenches(assembly, case)
    global_residual = _add(*external.values())
    tolerances = protocol["tolerances"]
    if max(abs(item) for item in global_residual[:3]) > float(tolerances["force_residual_n"]):
        raise VehicleLoadCaseError("global force equilibrium residual exceeded")
    if max(abs(item) for item in global_residual[3:]) > float(tolerances["moment_residual_nm"]):
        raise VehicleLoadCaseError("global moment equilibrium residual exceeded")
    root, parent, parent_connection, children = _tree(assembly)
    subtree: dict[str, tuple[float, ...]] = {}

    def accumulate(node: str) -> tuple[float, ...]:
        value = external[node]
        for child in children[node]:
            value = _add(value, accumulate(child))
        subtree[node] = value
        return value

    accumulate(root)
    connection_wrench = {parent_connection[node]: _neg(subtree[node]) for node in parent}
    component_residuals: list[float] = []
    for node in external:
        balance = external[node]
        if node in parent:
            balance = _add(balance, connection_wrench[parent_connection[node]])
        for child in children[node]:
            balance = _add(balance, _neg(connection_wrench[parent_connection[child]]))
        component_residuals.append(max(abs(item) for item in balance))
    maximum_component_residual = max(component_residuals, default=0.0)
    maximum_interface_residual = 0.0
    if maximum_component_residual > max(float(tolerances["force_residual_n"]), float(tolerances["moment_residual_nm"])):
        raise VehicleLoadCaseError("component equilibrium residual exceeded")
    loads: list[ConnectionLoad] = []
    for connection_id in sorted(connection_wrench):
        wrench = connection_wrench[connection_id]
        capacity = protocol["connection_capacities"][connection_id]
        force_magnitude = _norm(wrench[:3])
        moment_magnitude = _norm(wrench[3:])
        utilization = max(force_magnitude / float(capacity["force_n"]), moment_magnitude / float(capacity["moment_nm"]))
        state = "failed" if utilization > float(tolerances["failure_utilization"]) else "degraded" if utilization > float(tolerances["yield_utilization"]) else "intact"
        loads.append(ConnectionLoad(connection_id, tuple(wrench[:3]), tuple(wrench[3:]), force_magnitude, moment_magnitude, utilization, state))
    failed = next((item for item in loads if item.health_state == "failed"), None)
    failure_status, outcome = _failure_contract(failed, failure_raw, snapshot_sha)
    fingerprint_payload = {
        "case_id": case_id,
        "partition": case["partition"],
        "snapshot_sha256": snapshot_sha,
        "global_residual": global_residual,
        "maximum_component_residual": maximum_component_residual,
        "maximum_interface_residual": maximum_interface_residual,
        "connection_loads": [asdict(item) for item in loads],
        "outcome": outcome,
        "failure_contract_status": failure_status,
    }
    return VehicleLoadCaseResult(
        case_id=case_id,
        partition=case["partition"],
        snapshot_sha256=snapshot_sha,
        global_residual=tuple(global_residual),
        maximum_component_residual=maximum_component_residual,
        maximum_interface_residual=maximum_interface_residual,
        connection_loads=tuple(loads),
        outcome=outcome,
        failure_contract_status=failure_status,
        result_sha256=canonical_sha256(fingerprint_payload),
    )


def evaluate_all_load_cases(
    protocol: Mapping[str, Any], assembly: Assembly, failure_raw: Mapping[str, Any]
) -> tuple[VehicleLoadCaseResult, ...]:
    return tuple(evaluate_load_case(protocol, assembly, failure_raw, item["case_id"]) for item in protocol["cases"])
