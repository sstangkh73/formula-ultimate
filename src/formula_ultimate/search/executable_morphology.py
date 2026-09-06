"""Bounded executable swept-solid morphology and architecture mutations for Work 099."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
import random
from typing import Any, Mapping, Sequence


GENOME_VERSION = "executable_swept_network_v1"
DOMAINS = ("load", "energy", "motion", "fluid", "thermal", "control")
ROLES = ("source", "sink", "bidirectional")
INTERFACE_KINDS = ("fixed", "revolute", "prismatic", "fluid_coupling", "thermal_contact", "control_link")
OPERATORS = (
    "perturb_node",
    "grow_branch",
    "split_part",
    "rewire_interface",
    "merge_parts",
    "mutate_radius_field",
    "mutate_controller",
)
GEOMETRY_OPERATORS = {"perturb_node", "grow_branch", "split_part", "merge_parts", "mutate_radius_field"}
ARCHITECTURE_OPERATORS = {"split_part", "rewire_interface", "merge_parts"}


class MorphologyViolation(ValueError):
    """Raised when a genotype or mutation violates the bounded representation."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise MorphologyViolation(f"{label} must be an object")
    return value


def _sequence(value: Any, label: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise MorphologyViolation(f"{label} must be an array")
    return value


def _exact(value: Mapping[str, Any], fields: set[str], label: str) -> None:
    if set(value) != fields:
        raise MorphologyViolation(f"{label} schema mismatch")


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or not value[0].islower() or any(
        not (c.islower() or c.isdigit() or c in "_.-") for c in value
    ):
        raise MorphologyViolation(f"{label} must be a lower-case identifier")
    return value


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise MorphologyViolation(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise MorphologyViolation(f"{label} must be finite")
    return result


def _point(value: Any, label: str, bound: float) -> tuple[float, float, float]:
    raw = _sequence(value, label)
    if len(raw) != 3:
        raise MorphologyViolation(f"{label} must have three coordinates")
    point = tuple(_number(item, label) for item in raw)
    if max(abs(item) for item in point) > bound:
        raise MorphologyViolation(f"{label} exceeds coordinate bounds")
    return point  # type: ignore[return-value]


def _domains(value: Any, label: str) -> tuple[str, ...]:
    result = tuple(_sequence(value, label))
    if not result or len(set(result)) != len(result) or any(item not in DOMAINS for item in result):
        raise MorphologyViolation(f"{label} contains duplicate or unsupported domains")
    return tuple(sorted(result))


def validate_config(config: Mapping[str, Any]) -> dict[str, Any]:
    _exact(config, {"schema", "seeds", "limits", "operators", "measurement", "archive", "claim_boundary"}, "config")
    if config["schema"] != "executable_morphology_qd_v1":
        raise MorphologyViolation("config schema mismatch")
    seeds = list(_sequence(config["seeds"], "seeds"))
    if len(seeds) < 2 or len(set(seeds)) != len(seeds) or any(isinstance(s, bool) or not isinstance(s, int) for s in seeds):
        raise MorphologyViolation("at least two unique integer seeds are required")
    limits = _mapping(config["limits"], "limits")
    _exact(limits, {"maximum_parts", "maximum_nodes_per_part", "maximum_edges_per_part", "maximum_interfaces", "maximum_terminals", "maximum_coordinate_m", "minimum_radius_m", "maximum_radius_m", "minimum_edge_length_m", "mutation_step_m"}, "limits")
    integer_bounds = (("maximum_parts", 2, 8), ("maximum_nodes_per_part", 3, 32), ("maximum_edges_per_part", 2, 48), ("maximum_interfaces", 1, 24), ("maximum_terminals", 2, 24))
    for key, low, high in integer_bounds:
        value = limits[key]
        if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
            raise MorphologyViolation(f"{key} is outside bounds")
    for key in ("maximum_coordinate_m", "minimum_radius_m", "maximum_radius_m", "minimum_edge_length_m", "mutation_step_m"):
        if _number(limits[key], key) <= 0.0:
            raise MorphologyViolation(f"{key} must be positive")
    if not limits["minimum_radius_m"] < limits["maximum_radius_m"] < limits["maximum_coordinate_m"]:
        raise MorphologyViolation("radius bounds are inconsistent")
    if tuple(config["operators"]) != OPERATORS:
        raise MorphologyViolation("operator schedule mismatch")
    measurement = _mapping(config["measurement"], "measurement")
    _exact(measurement, {"required_fields", "relative_tolerance", "absolute_position_tolerance_m"}, "measurement")
    expected_fields = {"volume_m3", "surface_area_m2", "bounds_m", "center_m", "solid_count", "face_count", "edge_count", "terminal_positions_m"}
    if set(measurement["required_fields"]) != expected_fields:
        raise MorphologyViolation("measurement field coverage mismatch")
    if not 0.0 < _number(measurement["relative_tolerance"], "relative tolerance") <= 0.01:
        raise MorphologyViolation("relative tolerance is outside bounds")
    if not 0.0 < _number(measurement["absolute_position_tolerance_m"], "position tolerance") <= 1e-4:
        raise MorphologyViolation("position tolerance is outside bounds")
    archive = _mapping(config["archive"], "archive")
    _exact(archive, {"descriptors", "capacity_per_niche", "reproduction_caps"}, "archive")
    if tuple(archive["descriptors"]) != ("part_count", "interface_cycle_rank", "branch_node_count", "terminal_domain_count"):
        raise MorphologyViolation("archive descriptor declaration mismatch")
    for disposition in ("feasible", "failed", "unresolved"):
        capacity = archive["capacity_per_niche"].get(disposition)
        cap = archive["reproduction_caps"].get(disposition)
        if isinstance(capacity, bool) or not isinstance(capacity, int) or not 1 <= capacity <= 8:
            raise MorphologyViolation("archive capacity is outside bounds")
        if isinstance(cap, bool) or not isinstance(cap, int) or not 0 <= cap <= capacity:
            raise MorphologyViolation("archive reproduction cap is outside bounds")
    boundary = _mapping(config["claim_boundary"], "claim boundary")
    _exact(boundary, {"evidence_scope", "admitted_claims", "prohibited_claims"}, "claim boundary")
    if boundary["evidence_scope"] != "software_fixture_with_executed_cad" or "physical_validation" not in boundary["prohibited_claims"]:
        raise MorphologyViolation("claim boundary is too broad")
    return {"status": "passed", "seed_count": len(seeds), "operator_count": len(OPERATORS), "config_sha256": digest(config)}


def validate_genome(genome: Mapping[str, Any], limits: Mapping[str, Any]) -> dict[str, Any]:
    _exact(genome, {"version", "genome_id", "seed", "parts", "interfaces", "terminals", "controller"}, "genome")
    if genome["version"] != GENOME_VERSION:
        raise MorphologyViolation("genome version mismatch")
    _identifier(genome["genome_id"], "genome_id")
    if isinstance(genome["seed"], bool) or not isinstance(genome["seed"], int):
        raise MorphologyViolation("seed must be an integer")
    coordinate_bound = float(limits["maximum_coordinate_m"])
    parts = list(_sequence(genome["parts"], "parts"))
    if not 1 <= len(parts) <= limits["maximum_parts"]:
        raise MorphologyViolation("part count is outside bounds")
    part_ids: set[str] = set()
    nodes_by_part: dict[str, dict[str, Mapping[str, Any]]] = {}
    total_nodes = total_edges = branch_nodes = 0
    for raw_part in parts:
        part = _mapping(raw_part, "part")
        _exact(part, {"part_id", "material_id", "nodes", "edges"}, "part")
        part_id = _identifier(part["part_id"], "part_id")
        if part_id in part_ids:
            raise MorphologyViolation("duplicate part identity")
        part_ids.add(part_id)
        _identifier(part["material_id"], "material_id")
        nodes = list(_sequence(part["nodes"], "nodes"))
        edges = list(_sequence(part["edges"], "edges"))
        if not 2 <= len(nodes) <= limits["maximum_nodes_per_part"] or not 1 <= len(edges) <= limits["maximum_edges_per_part"]:
            raise MorphologyViolation("part node or edge count is outside bounds")
        node_map: dict[str, Mapping[str, Any]] = {}
        for raw_node in nodes:
            node = _mapping(raw_node, "node")
            _exact(node, {"node_id", "point_m", "radius_m"}, "node")
            node_id = _identifier(node["node_id"], "node_id")
            if node_id in node_map:
                raise MorphologyViolation("duplicate node identity")
            _point(node["point_m"], "node point", coordinate_bound)
            radius = _number(node["radius_m"], "node radius")
            if not limits["minimum_radius_m"] <= radius <= limits["maximum_radius_m"]:
                raise MorphologyViolation("node radius is outside bounds")
            node_map[node_id] = node
        edge_ids: set[str] = set()
        adjacency = {node_id: set() for node_id in node_map}
        for raw_edge in edges:
            edge = _mapping(raw_edge, "edge")
            _exact(edge, {"edge_id", "a", "b"}, "edge")
            edge_id = _identifier(edge["edge_id"], "edge_id")
            a, b = edge["a"], edge["b"]
            if edge_id in edge_ids or a == b or a not in node_map or b not in node_map:
                raise MorphologyViolation("duplicate, self, or unknown edge")
            if math.dist(node_map[a]["point_m"], node_map[b]["point_m"]) < limits["minimum_edge_length_m"]:
                raise MorphologyViolation("edge length is below minimum")
            edge_ids.add(edge_id)
            adjacency[a].add(b)
            adjacency[b].add(a)
        reached = {next(iter(node_map))}
        frontier = list(reached)
        while frontier:
            current = frontier.pop()
            for neighbor in adjacency[current] - reached:
                reached.add(neighbor)
                frontier.append(neighbor)
        if reached != set(node_map):
            raise MorphologyViolation("part graph is disconnected")
        branch_nodes += sum(len(neighbors) >= 3 for neighbors in adjacency.values())
        nodes_by_part[part_id] = node_map
        total_nodes += len(nodes)
        total_edges += len(edges)
    interfaces = list(_sequence(genome["interfaces"], "interfaces"))
    if len(interfaces) > limits["maximum_interfaces"]:
        raise MorphologyViolation("interface count exceeds bounds")
    interface_ids: set[str] = set()
    part_adjacency = {part_id: set() for part_id in part_ids}
    for raw in interfaces:
        interface = _mapping(raw, "interface")
        _exact(interface, {"interface_id", "part_a", "node_a", "part_b", "node_b", "kind", "domains", "ancestry"}, "interface")
        iid = _identifier(interface["interface_id"], "interface_id")
        a, b = interface["part_a"], interface["part_b"]
        if iid in interface_ids or a == b or a not in nodes_by_part or b not in nodes_by_part:
            raise MorphologyViolation("duplicate, self, or unknown interface")
        if interface["node_a"] not in nodes_by_part[a] or interface["node_b"] not in nodes_by_part[b]:
            raise MorphologyViolation("interface node is missing")
        if interface["kind"] not in INTERFACE_KINDS:
            raise MorphologyViolation("unsupported interface kind")
        _domains(interface["domains"], "interface domains")
        ancestry = list(_sequence(interface["ancestry"], "interface ancestry"))
        if not ancestry or any(not isinstance(item, str) or not item for item in ancestry):
            raise MorphologyViolation("interface ancestry is missing")
        interface_ids.add(iid)
        part_adjacency[a].add(b)
        part_adjacency[b].add(a)
    if len(parts) > 1:
        reached_parts = {next(iter(part_ids))}
        frontier = list(reached_parts)
        while frontier:
            current = frontier.pop()
            for neighbor in part_adjacency[current] - reached_parts:
                reached_parts.add(neighbor)
                frontier.append(neighbor)
        if reached_parts != part_ids:
            raise MorphologyViolation("architecture part graph is disconnected")
    terminals = list(_sequence(genome["terminals"], "terminals"))
    if not 2 <= len(terminals) <= limits["maximum_terminals"]:
        raise MorphologyViolation("terminal count is outside bounds")
    terminal_ids: set[str] = set()
    roles: set[str] = set()
    terminal_domains: set[str] = set()
    for raw in terminals:
        terminal = _mapping(raw, "terminal")
        _exact(terminal, {"terminal_id", "part_id", "node_id", "role", "domains", "ancestry"}, "terminal")
        tid = _identifier(terminal["terminal_id"], "terminal_id")
        part_id = terminal["part_id"]
        if tid in terminal_ids or part_id not in nodes_by_part or terminal["node_id"] not in nodes_by_part[part_id]:
            raise MorphologyViolation("duplicate or unknown terminal")
        if terminal["role"] not in ROLES:
            raise MorphologyViolation("unsupported terminal role")
        ancestry = list(_sequence(terminal["ancestry"], "terminal ancestry"))
        if not ancestry or any(not isinstance(item, str) or not item for item in ancestry):
            raise MorphologyViolation("terminal ancestry is missing")
        roles.add(terminal["role"])
        terminal_domains.update(_domains(terminal["domains"], "terminal domains"))
        terminal_ids.add(tid)
    if "source" not in roles or "sink" not in roles:
        raise MorphologyViolation("source and sink terminal roles are required")
    controller = _mapping(genome["controller"], "controller")
    _exact(controller, {"enabled", "gain", "sensor_terminal_id", "actuator_terminal_id"}, "controller")
    if type(controller["enabled"]) is not bool:
        raise MorphologyViolation("controller enabled must be boolean")
    _number(controller["gain"], "controller gain")
    if controller["enabled"] and (controller["sensor_terminal_id"] not in terminal_ids or controller["actuator_terminal_id"] not in terminal_ids):
        raise MorphologyViolation("controller references unknown terminals")
    if not controller["enabled"] and (controller["sensor_terminal_id"] is not None or controller["actuator_terminal_id"] is not None):
        raise MorphologyViolation("disabled controller carries terminal references")
    descriptors = topology_descriptors(genome)
    return {
        "status": "passed",
        "genotype_sha256": digest(genome),
        "functional_signature": functional_signature(genome),
        "part_count": len(parts),
        "interface_count": len(interfaces),
        "node_count": total_nodes,
        "edge_count": total_edges,
        "branch_node_count": branch_nodes,
        "terminal_domain_count": len(terminal_domains),
        "descriptors": descriptors,
    }


def functional_signature(genome: Mapping[str, Any]) -> str:
    """Return an ID-invariant refined signature of the typed part/interface graph."""
    parts = {part["part_id"]: part for part in genome["parts"]}
    terminals: dict[str, list[Any]] = {part_id: [] for part_id in parts}
    for terminal in genome["terminals"]:
        terminals[terminal["part_id"]].append([terminal["role"], sorted(terminal["domains"]), list(terminal["ancestry"])])
    colors = {}
    for part_id, part in parts.items():
        degrees = {node["node_id"]: 0 for node in part["nodes"]}
        for edge in part["edges"]:
            degrees[edge["a"]] += 1
            degrees[edge["b"]] += 1
        colors[part_id] = digest([sorted(degrees.values()), sorted(terminals[part_id])])
    for _ in range(len(parts) + 1):
        updated = {}
        for part_id in parts:
            neighbors = []
            for interface in genome["interfaces"]:
                if interface["part_a"] == part_id:
                    other = interface["part_b"]
                elif interface["part_b"] == part_id:
                    other = interface["part_a"]
                else:
                    continue
                neighbors.append([interface["kind"], sorted(interface["domains"]), colors[other]])
            updated[part_id] = digest([colors[part_id], sorted(neighbors)])
        if updated == colors:
            break
        colors = updated
    edges = []
    for interface in genome["interfaces"]:
        edges.append(sorted((colors[interface["part_a"]], colors[interface["part_b"]])) + [interface["kind"], sorted(interface["domains"])])
    return digest({"part_colors": sorted(colors.values()), "typed_edges": sorted(edges), "controller_enabled": genome["controller"]["enabled"]})


def topology_descriptors(genome: Mapping[str, Any]) -> dict[str, int]:
    part_count = len(genome["parts"])
    interfaces = len(genome["interfaces"])
    branch_nodes = 0
    for part in genome["parts"]:
        degrees = {node["node_id"]: 0 for node in part["nodes"]}
        for edge in part["edges"]:
            degrees[edge["a"]] += 1
            degrees[edge["b"]] += 1
        branch_nodes += sum(degree >= 3 for degree in degrees.values())
    return {
        "part_count": part_count,
        "interface_cycle_rank": max(0, interfaces - part_count + 1),
        "branch_node_count": branch_nodes,
        "terminal_domain_count": len({domain for terminal in genome["terminals"] for domain in terminal["domains"]}),
    }


def root_genome(seed: int) -> dict[str, Any]:
    """Create the same bounded external task with seed-local identity only."""
    return {
        "version": GENOME_VERSION,
        "genome_id": f"root_{seed}",
        "seed": seed,
        "parts": [
            {"part_id": "region_a", "material_id": "material_hypothesis_001", "nodes": [
                {"node_id": "a0", "point_m": [-0.08, 0.0, 0.0], "radius_m": 0.010},
                {"node_id": "a1", "point_m": [0.0, 0.0, 0.0], "radius_m": 0.014},
                {"node_id": "a2", "point_m": [0.04, 0.025, 0.0], "radius_m": 0.009},
            ], "edges": [
                {"edge_id": "a0_a1", "a": "a0", "b": "a1"},
                {"edge_id": "a1_a2", "a": "a1", "b": "a2"},
            ]},
            {"part_id": "region_b", "material_id": "material_hypothesis_001", "nodes": [
                {"node_id": "b0", "point_m": [0.04, 0.025, 0.0], "radius_m": 0.009},
                {"node_id": "b1", "point_m": [0.09, 0.0, 0.015], "radius_m": 0.011},
            ], "edges": [{"edge_id": "b0_b1", "a": "b0", "b": "b1"}]},
        ],
        "interfaces": [{"interface_id": "i0", "part_a": "region_a", "node_a": "a2", "part_b": "region_b", "node_b": "b0", "kind": "fixed", "domains": ["load", "thermal"], "ancestry": ["root_interface"]}],
        "terminals": [
            {"terminal_id": "source", "part_id": "region_a", "node_id": "a0", "role": "source", "domains": ["load", "thermal"], "ancestry": ["external_source"]},
            {"terminal_id": "sink", "part_id": "region_b", "node_id": "b1", "role": "sink", "domains": ["load", "thermal"], "ancestry": ["external_sink"]},
        ],
        "controller": {"enabled": True, "gain": 1.0, "sensor_terminal_id": "source", "actuator_terminal_id": "sink"},
    }


def _unique(genome: Mapping[str, Any], prefix: str) -> str:
    used = {part["part_id"] for part in genome["parts"]}
    used |= {node["node_id"] for part in genome["parts"] for node in part["nodes"]}
    used |= {edge["edge_id"] for part in genome["parts"] for edge in part["edges"]}
    used |= {interface["interface_id"] for interface in genome["interfaces"]}
    index = 0
    while f"{prefix}_{index}" in used:
        index += 1
    return f"{prefix}_{index}"


def _part(genome: dict[str, Any], part_id: str) -> dict[str, Any]:
    return next(part for part in genome["parts"] if part["part_id"] == part_id)


def _node(part: dict[str, Any], node_id: str) -> dict[str, Any]:
    return next(node for node in part["nodes"] if node["node_id"] == node_id)


def mutate(parent: Mapping[str, Any], operator: str, *, seed: int, step: int, limits: Mapping[str, Any]) -> dict[str, Any]:
    """Return a deterministic child and immutable, executable mutation trace."""
    if operator not in OPERATORS:
        raise MorphologyViolation("unsupported mutation operator")
    validate_genome(parent, limits)
    child = deepcopy(parent)
    child["genome_id"] = f"candidate_{seed}_{step}_{operator}"
    child["seed"] = seed
    rng = random.Random((seed << 20) ^ (step << 8) ^ OPERATORS.index(operator))
    parameters: dict[str, Any]
    if operator == "perturb_node":
        part = rng.choice(child["parts"])
        terminal_nodes = {(terminal["part_id"], terminal["node_id"]) for terminal in child["terminals"]}
        candidates = [node for node in part["nodes"] if (part["part_id"], node["node_id"]) not in terminal_nodes] or list(part["nodes"])
        node = rng.choice(candidates)
        axis = rng.randrange(3)
        delta = limits["mutation_step_m"] * (-1.0 if rng.randrange(2) else 1.0)
        node["point_m"][axis] += delta
        parameters = {"part_id": part["part_id"], "node_id": node["node_id"], "axis": axis, "delta_m": delta}
    elif operator == "grow_branch":
        part = rng.choice(child["parts"])
        anchor = rng.choice(part["nodes"])
        node_id = _unique(child, "grown_node")
        edge_id = _unique(child, "grown_edge")
        axis = rng.randrange(3)
        point = list(anchor["point_m"])
        point[axis] += limits["mutation_step_m"] * 2.0 * (-1.0 if rng.randrange(2) else 1.0)
        part["nodes"].append({"node_id": node_id, "point_m": point, "radius_m": anchor["radius_m"] * 0.8})
        part["edges"].append({"edge_id": edge_id, "a": anchor["node_id"], "b": node_id})
        parameters = {"part_id": part["part_id"], "anchor_node_id": anchor["node_id"], "new_node_id": node_id, "new_edge_id": edge_id, "axis": axis}
    elif operator == "split_part":
        candidates = []
        for part in child["parts"]:
            degree = {node["node_id"]: 0 for node in part["nodes"]}
            for edge in part["edges"]:
                degree[edge["a"]] += 1
                degree[edge["b"]] += 1
            terminal_nodes = {terminal["node_id"] for terminal in child["terminals"] if terminal["part_id"] == part["part_id"]}
            interface_nodes = {
                interface[f"node_{side}"]
                for interface in child["interfaces"]
                for side in ("a", "b")
                if interface[f"part_{side}"] == part["part_id"]
            }
            for edge in part["edges"]:
                for leaf, anchor in ((edge["a"], edge["b"]), (edge["b"], edge["a"])):
                    if degree[leaf] == 1 and leaf not in terminal_nodes | interface_nodes and len(part["nodes"]) > 2:
                        candidates.append((part, edge, leaf, anchor))
        if not candidates:
            raise MorphologyViolation("no non-terminal leaf is available for split")
        part, edge, leaf_id, anchor_id = rng.choice(candidates)
        leaf = deepcopy(_node(part, leaf_id))
        anchor = deepcopy(_node(part, anchor_id))
        new_part_id = _unique(child, "split_region")
        child_anchor_id = _unique(child, "split_anchor")
        child_leaf_id = _unique(child, "split_leaf")
        anchor["node_id"] = child_anchor_id
        leaf["node_id"] = child_leaf_id
        new_edge_id = _unique(child, "split_edge")
        part["nodes"] = [node for node in part["nodes"] if node["node_id"] != leaf_id]
        part["edges"] = [item for item in part["edges"] if item["edge_id"] != edge["edge_id"]]
        child["parts"].append({"part_id": new_part_id, "material_id": part["material_id"], "nodes": [anchor, leaf], "edges": [{"edge_id": new_edge_id, "a": child_anchor_id, "b": child_leaf_id}]})
        interface_id = _unique(child, "split_interface")
        child["interfaces"].append({"interface_id": interface_id, "part_a": part["part_id"], "node_a": anchor_id, "part_b": new_part_id, "node_b": child_anchor_id, "kind": "fixed", "domains": ["load", "thermal"], "ancestry": ["split_part", parent["genome_id"], part["part_id"]]})
        parameters = {"source_part_id": part["part_id"], "new_part_id": new_part_id, "source_edge_id": edge["edge_id"], "interface_id": interface_id}
    elif operator == "rewire_interface":
        if not child["interfaces"]:
            raise MorphologyViolation("no interface is available for rewiring")
        interface = rng.choice(child["interfaces"])
        side = "a" if rng.randrange(2) == 0 else "b"
        part_id = interface[f"part_{side}"]
        part = _part(child, part_id)
        current = interface[f"node_{side}"]
        choices = [node["node_id"] for node in part["nodes"] if node["node_id"] != current]
        if not choices:
            raise MorphologyViolation("interface part has no alternate node")
        replacement = rng.choice(choices)
        interface[f"node_{side}"] = replacement
        interface["ancestry"] = list(interface["ancestry"]) + [f"rewired_{side}", parent["genome_id"]]
        parameters = {"interface_id": interface["interface_id"], "side": side, "old_node_id": current, "new_node_id": replacement}
    elif operator == "merge_parts":
        if not child["interfaces"]:
            raise MorphologyViolation("no interface is available for merge")
        interface = rng.choice(child["interfaces"])
        keep_id, remove_id = interface["part_a"], interface["part_b"]
        keep, remove = _part(child, keep_id), _part(child, remove_id)
        node_map: dict[str, str] = {interface["node_b"]: interface["node_a"]}
        for node in remove["nodes"]:
            if node["node_id"] == interface["node_b"]:
                continue
            renamed = _unique(child, "merged_node")
            node_map[node["node_id"]] = renamed
            copied = deepcopy(node)
            copied["node_id"] = renamed
            keep["nodes"].append(copied)
        for edge in remove["edges"]:
            a, b = node_map[edge["a"]], node_map[edge["b"]]
            if a == b:
                continue
            keep["edges"].append({"edge_id": _unique(child, "merged_edge"), "a": a, "b": b})
        for terminal in child["terminals"]:
            if terminal["part_id"] == remove_id:
                terminal["part_id"] = keep_id
                terminal["node_id"] = node_map[terminal["node_id"]]
        child["interfaces"] = [item for item in child["interfaces"] if item["interface_id"] != interface["interface_id"]]
        for other in child["interfaces"]:
            for side in ("a", "b"):
                if other[f"part_{side}"] == remove_id:
                    other[f"part_{side}"] = keep_id
                    other[f"node_{side}"] = node_map[other[f"node_{side}"]]
                    other["ancestry"] = list(other["ancestry"]) + ["merged_interface", parent["genome_id"]]
        child["parts"] = [part for part in child["parts"] if part["part_id"] != remove_id]
        parameters = {"kept_part_id": keep_id, "removed_part_id": remove_id, "removed_interface_id": interface["interface_id"]}
    elif operator == "mutate_radius_field":
        part = rng.choice(child["parts"])
        node = rng.choice(part["nodes"])
        factor = 0.85 if rng.randrange(2) else 1.15
        old = node["radius_m"]
        node["radius_m"] = min(limits["maximum_radius_m"], max(limits["minimum_radius_m"], old * factor))
        parameters = {"part_id": part["part_id"], "node_id": node["node_id"], "old_radius_m": old, "new_radius_m": node["radius_m"]}
    else:
        old = child["controller"]["gain"]
        child["controller"]["gain"] = old * (0.9 if rng.randrange(2) else 1.1)
        parameters = {"old_gain": old, "new_gain": child["controller"]["gain"]}
    validation = validate_genome(child, limits)
    trace = {
        "operator": operator,
        "parameters": parameters,
        "seed": seed,
        "step": step,
        "parent_genotype_sha256": digest(parent),
        "child_genotype_sha256": validation["genotype_sha256"],
        "parent_functional_signature": functional_signature(parent),
        "child_functional_signature": validation["functional_signature"],
        "declared_geometry_change": operator in GEOMETRY_OPERATORS,
        "declared_architecture_change": operator in ARCHITECTURE_OPERATORS,
    }
    return {"child": child, "trace": trace, "lineage_sha256": digest(trace)}
