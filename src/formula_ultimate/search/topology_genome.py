"""Typed, identifier-invariant morphology/topology genomes for Work 093."""
from __future__ import annotations

import hashlib
import itertools
import json
from typing import Any, Mapping, Sequence

from formula_ultimate.components.freeform_solid_grammar import OPERATORS as SOLID_OPERATORS


GENOME_VERSION = "typed_morphology_topology_genome_v1"
DOMAINS = ("load", "energy", "motion", "fluid", "thermal", "control")
INTERFACE_TYPES = ("fixed", "revolute", "prismatic", "spherical", "fluid_coupling", "electrical", "thermal_contact", "control_link")
DOF_TYPES = ("tx", "ty", "tz", "rx", "ry", "rz", "flow", "current", "heat", "signal")


class TopologyGenomeError(ValueError):
    """Raised when a typed genome is invalid before CAD."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")


def declaration_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping): raise TopologyGenomeError(f"{label} must be an object")
    return value


def _sequence(value: Any, label: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence): raise TopologyGenomeError(f"{label} must be an array")
    return value


def _exact(value: Mapping[str, Any], fields: set[str], label: str) -> None:
    if set(value) != fields: raise TopologyGenomeError(f"{label} schema mismatch")


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or not value[0].islower() or any(not (c.islower() or c.isdigit() or c in "_-.") for c in value):
        raise TopologyGenomeError(f"{label} must be a lower-case identifier")
    return value


def _typed_domains(value: Any, required_domains: set[str], label: str) -> tuple[str, ...]:
    domains = tuple(_sequence(value, label))
    if not domains or len(set(domains)) != len(domains) or any(item not in required_domains for item in domains):
        raise TopologyGenomeError(f"{label} contains duplicate or unsupported domains")
    return tuple(sorted(domains))


def _feature_signature(part: Mapping[str, Any]) -> tuple[str, ...]:
    signatures: dict[str, str] = {}
    for feature in part["features"]:
        ancestry = sorted(signatures[item] for item in feature["inputs"])
        signatures[feature["feature_id"]] = json.dumps([feature["operator"], ancestry], separators=(",", ":"))
    return tuple(sorted(signatures.values())) + ("final=" + signatures[part["final_feature_id"]],)


def canonical_topology_signature(genome: Mapping[str, Any]) -> str:
    """Return an exact ID-invariant signature for bounded (<=8 part) typed graphs."""
    parts = list(genome["parts"])
    part_by_id = {part["part_id"]: part for part in parts}
    interface_by_id = {item["interface_id"]: item for item in genome["interfaces"]}
    best: bytes | None = None
    for order in itertools.permutations(part_by_id):
        position = {part_id: index for index, part_id in enumerate(order)}
        nodes = []
        for part_id in order:
            part = part_by_id[part_id]
            parent = part["parent_part_id"]
            nodes.append([part["solid_family"], part["source_solid_candidate_id"], part["material_id"], part["process_id"], _feature_signature(part), None if parent is None else position[parent]])
        interfaces = sorted([
            [min(position[item["part_a"]], position[item["part_b"]]), max(position[item["part_a"]], position[item["part_b"]]), item["interface_type"], sorted(item["domains"]), sorted(item["allowed_dof"])]
            for item in genome["interfaces"]
        ])
        terminals = sorted([[position[item["part_id"]], item["role"], sorted(item["domains"])] for item in genome["terminals"]])
        paths = []
        terminal_by_id = {item["terminal_id"]: item for item in genome["terminals"]}
        for path in genome["paths"]:
            path_interfaces = [interface_by_id[item]["interface_type"] for item in path["interface_ids"]]
            endpoints = [terminal_by_id[item]["role"] for item in path["terminal_ids"]]
            paths.append([sorted(path["domains"]), endpoints, [position[item] for item in path["part_ids"]], path_interfaces])
        representation = canonical_bytes({"nodes": nodes, "interfaces": interfaces, "terminals": terminals, "paths": sorted(paths), "symmetry": genome["symmetry"]})
        if best is None or representation < best: best = representation
    assert best is not None
    return hashlib.sha256(best).hexdigest()


def validate_topology_corpus(value: Mapping[str, Any], solid_candidates: Mapping[str, str]) -> dict[str, Any]:
    root = _mapping(value, "corpus")
    _exact(root, {"genome_version", "source_solid_declaration_sha256", "required_domains", "limits", "genomes"}, "corpus")
    if root["genome_version"] != GENOME_VERSION: raise TopologyGenomeError("genome version mismatch")
    if not isinstance(root["source_solid_declaration_sha256"], str) or len(root["source_solid_declaration_sha256"]) != 64: raise TopologyGenomeError("source solid identity must be SHA-256")
    required_domains = set(_sequence(root["required_domains"], "required_domains"))
    if required_domains != set(DOMAINS): raise TopologyGenomeError("required domain set mismatch")
    limits = _mapping(root["limits"], "limits")
    _exact(limits, {"maximum_parts", "maximum_interfaces", "maximum_features_per_part", "maximum_paths"}, "limits")
    for key, low, high in (("maximum_parts", 2, 8), ("maximum_interfaces", 1, 24), ("maximum_features_per_part", 1, 32), ("maximum_paths", 1, 24)):
        number = limits[key]
        if isinstance(number, bool) or not isinstance(number, int) or not low <= number <= high: raise TopologyGenomeError(f"{key} is outside bounds")
    genomes = _sequence(root["genomes"], "genomes")
    if len(genomes) < 6: raise TopologyGenomeError("at least six genomes are required")
    genome_ids: set[str] = set(); signatures = []; part_counts = set(); descriptors = []
    for index, raw_genome in enumerate(genomes):
        genome = _mapping(raw_genome, f"genomes[{index}]")
        _exact(genome, {"genome_id", "parts", "interfaces", "terminals", "paths", "symmetry"}, "genome")
        genome_id = _identifier(genome["genome_id"], "genome_id")
        if genome_id in genome_ids: raise TopologyGenomeError("duplicate genome identity")
        genome_ids.add(genome_id)
        parts = _sequence(genome["parts"], "parts")
        if not 1 <= len(parts) <= limits["maximum_parts"]: raise TopologyGenomeError("part count is outside bounds")
        part_counts.add(len(parts)); part_ids: set[str] = set(); parents: dict[str, str | None] = {}
        for raw_part in parts:
            part = _mapping(raw_part, "part")
            _exact(part, {"part_id", "parent_part_id", "solid_family", "source_solid_candidate_id", "material_id", "process_id", "features", "final_feature_id"}, "part")
            part_id = _identifier(part["part_id"], "part_id")
            if part_id in part_ids: raise TopologyGenomeError("duplicate part identity")
            part_ids.add(part_id)
            parent = part["parent_part_id"]
            if parent is not None: parent = _identifier(parent, "parent_part_id")
            parents[part_id] = parent
            source = _identifier(part["source_solid_candidate_id"], "source solid candidate")
            family = _identifier(part["solid_family"], "solid family")
            if solid_candidates.get(source) != family: raise TopologyGenomeError("solid candidate and family identity mismatch")
            _identifier(part["material_id"], "material_id"); _identifier(part["process_id"], "process_id")
            features = _sequence(part["features"], "features")
            if not 1 <= len(features) <= limits["maximum_features_per_part"]: raise TopologyGenomeError("feature count is outside bounds")
            feature_ids: set[str] = set()
            for raw_feature in features:
                feature = _mapping(raw_feature, "part feature"); _exact(feature, {"feature_id", "operator", "inputs"}, "part feature")
                feature_id = _identifier(feature["feature_id"], "feature_id")
                if feature_id in feature_ids or feature["operator"] not in SOLID_OPERATORS: raise TopologyGenomeError("duplicate feature or unsupported operator")
                inputs = [_identifier(item, "feature input") for item in _sequence(feature["inputs"], "feature inputs")]
                if any(item not in feature_ids for item in inputs): raise TopologyGenomeError("feature ancestry must reference earlier features")
                feature_ids.add(feature_id)
            if part["final_feature_id"] not in feature_ids: raise TopologyGenomeError("part final feature is missing")
        if any(parent is not None and parent not in part_ids for parent in parents.values()): raise TopologyGenomeError("unknown parent part")
        for start in part_ids:
            seen = set(); current = start
            while parents[current] is not None:
                current = parents[current]  # type: ignore[assignment]
                if current in seen or current == start: raise TopologyGenomeError("part containment cycle")
                seen.add(current)
        interfaces = _sequence(genome["interfaces"], "interfaces")
        if len(interfaces) > limits["maximum_interfaces"]: raise TopologyGenomeError("interface count exceeds bounds")
        interface_ids: set[str] = set(); interface_by_id = {}; endpoint_labels = set()
        for raw_interface in interfaces:
            interface = _mapping(raw_interface, "interface")
            _exact(interface, {"interface_id", "part_a", "part_b", "interface_type", "domains", "allowed_dof"}, "interface")
            interface_id = _identifier(interface["interface_id"], "interface_id")
            a = _identifier(interface["part_a"], "part_a"); b = _identifier(interface["part_b"], "part_b")
            if interface_id in interface_ids or a == b or a not in part_ids or b not in part_ids: raise TopologyGenomeError("duplicate, self, or unknown interface")
            if interface["interface_type"] not in INTERFACE_TYPES: raise TopologyGenomeError("unsupported interface type")
            domains = _typed_domains(interface["domains"], required_domains, "interface domains")
            dof = tuple(_sequence(interface["allowed_dof"], "allowed_dof"))
            if len(set(dof)) != len(dof) or any(item not in DOF_TYPES for item in dof): raise TopologyGenomeError("unsupported or duplicate DOF")
            label = (tuple(sorted((a, b))), interface["interface_type"], domains)
            if label in endpoint_labels: raise TopologyGenomeError("duplicate typed interface edge")
            endpoint_labels.add(label); interface_ids.add(interface_id); interface_by_id[interface_id] = interface
        terminals = _sequence(genome["terminals"], "terminals"); terminal_ids: set[str] = set(); terminal_by_id = {}
        for raw_terminal in terminals:
            terminal = _mapping(raw_terminal, "terminal")
            _exact(terminal, {"terminal_id", "part_id", "role", "domains", "required"}, "terminal")
            terminal_id = _identifier(terminal["terminal_id"], "terminal_id")
            if terminal_id in terminal_ids or terminal["part_id"] not in part_ids or terminal["role"] not in {"source", "sink", "bidirectional"} or terminal["required"] is not True:
                raise TopologyGenomeError("invalid, duplicate, or optional terminal")
            _typed_domains(terminal["domains"], required_domains, "terminal domains")
            terminal_ids.add(terminal_id); terminal_by_id[terminal_id] = terminal
        paths = _sequence(genome["paths"], "paths")
        if not 1 <= len(paths) <= limits["maximum_paths"]: raise TopologyGenomeError("path count is outside bounds")
        path_ids: set[str] = set(); covered_terminals: set[str] = set(); covered_domains: set[str] = set(); covered_parts: set[str] = set()
        for raw_path in paths:
            path = _mapping(raw_path, "path"); _exact(path, {"path_id", "domains", "terminal_ids", "part_ids", "interface_ids"}, "path")
            path_id = _identifier(path["path_id"], "path_id")
            if path_id in path_ids: raise TopologyGenomeError("duplicate path identity")
            path_ids.add(path_id); domains = set(_typed_domains(path["domains"], required_domains, "path domains"))
            path_terminals = list(_sequence(path["terminal_ids"], "path terminal_ids")); route = list(_sequence(path["part_ids"], "path part_ids")); route_interfaces = list(_sequence(path["interface_ids"], "path interface_ids"))
            if len(path_terminals) != 2 or any(item not in terminal_by_id for item in path_terminals) or not route or len(route_interfaces) != len(route) - 1 or any(item not in part_ids for item in route):
                raise TopologyGenomeError("path shape or identity mismatch")
            source, sink = (terminal_by_id[item] for item in path_terminals)
            if source["role"] not in {"source", "bidirectional"} or sink["role"] not in {"sink", "bidirectional"} or route[0] != source["part_id"] or route[-1] != sink["part_id"]:
                raise TopologyGenomeError("path endpoint role or placement mismatch")
            if not domains.issubset(set(source["domains"])) or not domains.issubset(set(sink["domains"])): raise TopologyGenomeError("path domain is absent from a terminal")
            for a, b, interface_id in zip(route, route[1:], route_interfaces):
                interface = interface_by_id.get(interface_id)
                if interface is None or {a, b} != {interface["part_a"], interface["part_b"]} or not domains.issubset(set(interface["domains"])):
                    raise TopologyGenomeError("path route is disconnected or domain-incompatible")
            covered_terminals.update(path_terminals); covered_domains.update(domains); covered_parts.update(route)
        if covered_terminals != terminal_ids or covered_domains != required_domains or covered_parts != part_ids:
            raise TopologyGenomeError("mandatory terminal, domain, or part is not traceable")
        symmetry = _mapping(genome["symmetry"], "symmetry"); _exact(symmetry, {"mode", "axis", "order"}, "symmetry")
        if symmetry["mode"] not in {"none", "mirror", "rotational"}: raise TopologyGenomeError("unsupported symmetry mode")
        if symmetry["mode"] == "none" and (symmetry["axis"] is not None or symmetry["order"] != 1): raise TopologyGenomeError("none symmetry carries hidden prior")
        if symmetry["mode"] != "none" and (symmetry["axis"] not in {"x", "y", "z"} or isinstance(symmetry["order"], bool) or not isinstance(symmetry["order"], int) or symmetry["order"] < 2): raise TopologyGenomeError("invalid active symmetry gene")
        signature = canonical_topology_signature(genome); signatures.append(signature)
        degrees = {part_id: 0 for part_id in part_ids}
        for interface in interfaces: degrees[interface["part_a"]] += 1; degrees[interface["part_b"]] += 1
        edge_count = len(interfaces); component_cycle_rank = edge_count - len(part_ids) + 1
        descriptors.append({"genome_id": genome_id, "part_count": len(parts), "interface_count": edge_count, "path_count": len(paths), "branch_part_count": sum(value >= 3 for value in degrees.values()), "interface_cycle_rank": max(0, component_cycle_rank), "topology_signature": signature})
    if len(part_counts) < 4 or len(set(signatures)) != len(genomes): raise TopologyGenomeError("corpus part-count or non-isomorphic topology coverage mismatch")
    return {"status": "passed", "genome_count": len(genomes), "distinct_part_counts": sorted(part_counts), "unique_topology_signature_count": len(set(signatures)), "descriptors": descriptors, "declaration_sha256": declaration_sha256(value)}
