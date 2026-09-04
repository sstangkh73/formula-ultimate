"""Deterministic Work 090 search-space diversity descriptors and census."""
from __future__ import annotations

from collections import Counter, deque
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence


class DesignDiversityError(ValueError):
    """Raised when the diversity declaration or candidate evidence is invalid."""


SOURCE_IDS = ("base_assembly", "search_protocol", "load_protocol", "failure_contract", "baseline_protocol")
INVARIANCES = ("component_interface_renaming", "global_translation", "signed_axis_permutation", "uniform_scale")
CHANGE_CONTROLS = ("branch_addition", "connectivity_reroute", "primitive_family_change", "interface_topology_change")
METRICS = ("topology_signature", "geometry_signature", "unique_topology_ratio", "unique_geometry_ratio", "duplicate_phenotype_rate", "primitive_fraction", "primitive_type_entropy_bits", "curved_surface_area_fraction", "functional_path_signature", "failure_mode_coverage")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _exact(value: Mapping[str, Any], keys: set[str], label: str) -> None:
    if set(value) != keys:
        raise DesignDiversityError(f"{label} schema mismatch")


def _finite(value: Any, label: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise DesignDiversityError(f"{label} must be numeric")
    ready = float(value)
    if not math.isfinite(ready) or (positive and ready <= 0.0):
        raise DesignDiversityError(f"{label} must be finite" + (" and positive" if positive else ""))
    return ready


def _vec(value: Any, label: str) -> tuple[float, float, float]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) or len(value) != 3:
        raise DesignDiversityError(f"{label} must contain three values")
    return tuple(_finite(item, label) for item in value)  # type: ignore[return-value]


def validate_config(config: Mapping[str, Any]) -> dict[str, str]:
    _exact(config, {"schema_version", "census_id", "claim_level", "sources", "census", "invariances", "change_controls", "metrics"}, "config")
    if config["schema_version"] != "design_diversity_v1" or config["census_id"] != "current_bounded_search_bias_001":
        raise DesignDiversityError("diversity config identity mismatch")
    sources = config["sources"]
    if not isinstance(sources, Mapping) or tuple(sources) != SOURCE_IDS:
        raise DesignDiversityError("source set or order mismatch")
    for source in sources.values():
        if not isinstance(source, Mapping):
            raise DesignDiversityError("source schema mismatch")
        _exact(source, {"path", "file_sha256"}, "source")
        if not all(isinstance(source[key], str) and source[key] for key in source):
            raise DesignDiversityError("source values must be non-empty strings")
    census = config["census"]
    if not isinstance(census, Mapping):
        raise DesignDiversityError("census schema mismatch")
    _exact(census, {"treatments", "seeds", "attempts_per_treatment_seed", "expected_attempts", "expected_variable_names"}, "census")
    if tuple(census["treatments"]) != ("GRID", "RANDOM", "EVOLUTION") or tuple(census["seeds"]) != (101, 202, 303):
        raise DesignDiversityError("frozen treatment or seed ledger mismatch")
    if census["attempts_per_treatment_seed"] != 32 or census["expected_attempts"] != 288:
        raise DesignDiversityError("frozen census budget mismatch")
    if tuple(census["expected_variable_names"]) != ("contact_radius_scale", "core_length_scale", "core_width_scale", "propulsor_size_scale", "source_size_scale"):
        raise DesignDiversityError("candidate variable opportunity set mismatch")
    if tuple(config["invariances"]) != INVARIANCES or tuple(config["change_controls"]) != CHANGE_CONTROLS or tuple(config["metrics"]) != METRICS:
        raise DesignDiversityError("metric or control declaration mismatch")
    return {"status": "passed", "config_sha256": canonical_sha256(config)}


def load_sources(root: Path, config: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    validate_config(config)
    output: dict[str, dict[str, Any]] = {}
    for source_id in SOURCE_IDS:
        spec = config["sources"][source_id]
        path = Path(root) / spec["path"]
        if not path.is_file() or file_sha256(path) != spec["file_sha256"]:
            raise DesignDiversityError(f"{source_id} source identity mismatch")
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise DesignDiversityError(f"{source_id} source JSON is invalid") from exc
        if not isinstance(value, dict):
            raise DesignDiversityError(f"{source_id} source must be an object")
        output[source_id] = value
    return output


def _component_data(raw: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int], list[tuple[int, int, str]]]:
    components = raw.get("components")
    interfaces = raw.get("interfaces")
    if not isinstance(components, list) or not components or not isinstance(interfaces, list):
        raise DesignDiversityError("candidate components or interfaces are missing")
    ids = [item.get("component_id") for item in components]
    if any(not isinstance(item, str) or not item for item in ids) or len(ids) != len(set(ids)):
        raise DesignDiversityError("component identities are invalid")
    index = {item: offset for offset, item in enumerate(ids)}
    iface_owner: dict[str, int] = {}
    for item in interfaces:
        if not isinstance(item, Mapping) or not isinstance(item.get("interface_id"), str) or item.get("component_id") not in index:
            raise DesignDiversityError("interface reference is invalid")
        if item["interface_id"] in iface_owner:
            raise DesignDiversityError("duplicate interface identity")
        _vec(item.get("local_position_m"), "interface local position")
        iface_owner[item["interface_id"]] = index[item["component_id"]]
    edges: list[tuple[int, int, str]] = []
    for connection in raw.get("connections", []):
        try:
            a, b = iface_owner[connection["interface_a"]], iface_owner[connection["interface_b"]]
        except (KeyError, TypeError) as exc:
            raise DesignDiversityError("connection reference is invalid") from exc
        edges.append((min(a, b), max(a, b), "structural_interface"))
    for edge in raw.get("energy_edges", []):
        if not isinstance(edge, list) or len(edge) != 2 or edge[0] not in index or edge[1] not in index:
            raise DesignDiversityError("energy edge reference is invalid")
        a, b = index[edge[0]], index[edge[1]]
        edges.append((min(a, b), max(a, b), "energy"))
    return components, iface_owner, edges


def _wl_labels(raw: Mapping[str, Any]) -> tuple[list[str], list[tuple[int, int, str]]]:
    components, iface_owner, edges = _component_data(raw)
    contacts = {item.get("interface_id") for item in raw.get("contacts", []) if isinstance(item, Mapping)}
    contact_nodes = {owner for identity, owner in iface_owner.items() if identity in contacts}
    load_ids = set(raw.get("external_load_components", []))
    labels = []
    for offset, component in enumerate(components):
        material = raw.get("materials", {}).get(component.get("material_id"), {})
        base = {
            "function_tags": sorted(component.get("function_tags", [])),
            "material_density_kg_per_m3": material.get("density_kg_per_m3"),
            "ground_contact": offset in contact_nodes,
            "external_load": component.get("component_id") in load_ids,
            "interface_count": sum(owner == offset for owner in iface_owner.values()),
        }
        labels.append(canonical_sha256(base))
    adjacency: list[list[tuple[str, int]]] = [[] for _ in components]
    for a, b, edge_type in edges:
        adjacency[a].append((edge_type, b)); adjacency[b].append((edge_type, a))
    for _ in range(len(components)):
        labels = [canonical_sha256({"self": labels[i], "neighbors": sorted((kind, labels[j]) for kind, j in adjacency[i])}) for i in range(len(components))]
    return labels, edges


def topology_signature(raw: Mapping[str, Any]) -> str:
    labels, edges = _wl_labels(raw)
    graph = {
        "node_labels": sorted(labels),
        "edges": sorted((kind, min(labels[a], labels[b]), max(labels[a], labels[b])) for a, b, kind in edges),
    }
    return canonical_sha256(graph)


def _primitive(component: Mapping[str, Any]) -> tuple[str, tuple[float, ...], float, float]:
    primitive = component.get("primitive")
    if not isinstance(primitive, Mapping):
        raise DesignDiversityError("component primitive is missing")
    kind = primitive.get("type")
    if kind == "box":
        dims = tuple(_finite(value, "box dimension", positive=True) for value in primitive.get("size_m", []))
        if len(dims) != 3:
            raise DesignDiversityError("box must have three dimensions")
        area = 2.0 * (dims[0] * dims[1] + dims[0] * dims[2] + dims[1] * dims[2])
        return "box", tuple(sorted(dims)), area, 0.0
    if kind in {"cylinder_x", "cylinder_y", "cylinder_z"}:
        radius = _finite(primitive.get("radius_m"), "cylinder radius", positive=True)
        height = _finite(primitive.get("height_m", primitive.get("length_m")), "cylinder length", positive=True)
        lateral = 2.0 * math.pi * radius * height
        total = lateral + 2.0 * math.pi * radius * radius
        return "cylinder", (radius, height), total, lateral
    raise DesignDiversityError("unsupported primitive family in diversity census")


def _shortest_lengths(node_count: int, edges: Sequence[tuple[int, int]], starts: set[int], goals: set[int]) -> list[int | None]:
    graph = [set() for _ in range(node_count)]
    for a, b in edges:
        graph[a].add(b); graph[b].add(a)
    output: list[int | None] = []
    for start in sorted(starts):
        distance = {start: 0}; queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in distance:
                    distance[neighbor] = distance[node] + 1; queue.append(neighbor)
        output.extend(distance.get(goal) for goal in sorted(goals))
    return output


def functional_path_signature(raw: Mapping[str, Any]) -> str:
    components, iface_owner, typed_edges = _component_data(raw)
    ids = {item["component_id"]: index for index, item in enumerate(components)}
    tags = [set(item.get("function_tags", [])) for item in components]
    structural = [(a, b) for a, b, kind in typed_edges if kind == "structural_interface"]
    energy = [(a, b) for a, b, kind in typed_edges if kind == "energy"]
    contacts = {iface_owner[item["interface_id"]] for item in raw.get("contacts", []) if item.get("interface_id") in iface_owner}
    load_nodes = {ids[item] for item in raw.get("external_load_components", []) if item in ids}
    sources = {i for i, item in enumerate(tags) if "energy_source" in item}
    propulsors = {i for i, item in enumerate(tags) if "propulsion" in item}
    return canonical_sha256({
        "load_to_ground_lengths": _shortest_lengths(len(components), structural, load_nodes, contacts),
        "energy_to_propulsion_lengths": _shortest_lengths(len(components), energy, sources, propulsors),
    })


def describe_candidate(raw: Mapping[str, Any]) -> dict[str, Any]:
    components, iface_owner, _ = _component_data(raw)
    labels, _ = _wl_labels(raw)
    positions = [_vec(item.get("translation_m"), "component translation") for item in components]
    primitive_data = [_primitive(item) for item in components]
    lengths = [value for _, dims, _, _ in primitive_data for value in dims]
    pair_distances = [math.dist(positions[i], positions[j]) for i in range(len(positions)) for j in range(i + 1, len(positions))]
    scale_values = lengths + pair_distances
    scale = math.sqrt(math.fsum(value * value for value in scale_values) / len(scale_values))
    if not math.isfinite(scale) or scale <= 0.0:
        raise DesignDiversityError("candidate characteristic scale is invalid")
    records = []
    interface_positions: dict[int, list[float]] = {i: [] for i in range(len(components))}
    for item in raw["interfaces"]:
        interface_positions[iface_owner[item["interface_id"]]].append(math.sqrt(math.fsum(value * value for value in _vec(item["local_position_m"], "interface local position"))) / scale)
    for index, (family, dims, _, _) in enumerate(primitive_data):
        neighbor_distances = sorted((labels[other], round(math.dist(positions[index], positions[other]) / scale, 12)) for other in range(len(positions)) if other != index)
        records.append({
            "node_label": labels[index],
            "family": family,
            "normalized_dimensions": [round(value / scale, 12) for value in dims],
            "interface_radial_positions": sorted(round(value, 12) for value in interface_positions[index]),
            "pair_distances": neighbor_distances,
        })
    counts = Counter(family for family, _, _, _ in primitive_data)
    total = len(primitive_data)
    entropy = -math.fsum((count / total) * math.log2(count / total) for count in counts.values())
    total_area = math.fsum(area for _, _, area, _ in primitive_data)
    curved_area = math.fsum(curved for _, _, _, curved in primitive_data)
    return {
        "topology_signature": topology_signature(raw),
        "geometry_signature": canonical_sha256(sorted(records, key=lambda item: canonical_bytes(item))),
        "functional_path_signature": functional_path_signature(raw),
        "characteristic_length_m": scale,
        "component_count": total,
        "primitive_fraction": 1.0,
        "primitive_type_entropy_bits": entropy,
        "curved_surface_area_fraction": curved_area / total_area,
        "primitive_type_counts": dict(sorted(counts.items())),
    }


def summarize_census(rows: Sequence[Mapping[str, Any]], expected_attempts: int) -> dict[str, Any]:
    if len(rows) != expected_attempts:
        raise DesignDiversityError("census attempt count mismatch")
    topology = [row["descriptor"]["topology_signature"] for row in rows]
    geometry = [row["descriptor"]["geometry_signature"] for row in rows]
    valid = [row for row in rows if row["evaluation_status"] != "failed" or row.get("failure_code") != "grammar_invalid"]
    failures = Counter((row.get("failure_code") or "none") for row in rows)
    return {
        "attempted_candidates": len(rows),
        "descriptor_valid_candidates": len(valid),
        "unique_topology_signatures": len(set(topology)),
        "unique_topology_ratio": len(set(topology)) / len(rows),
        "unique_geometry_signatures": len(set(geometry)),
        "unique_geometry_ratio": len(set(geometry)) / len(rows),
        "duplicate_phenotype_rate": 1.0 - len(set(geometry)) / len(rows),
        "mean_primitive_fraction": math.fsum(row["descriptor"]["primitive_fraction"] for row in rows) / len(rows),
        "mean_primitive_type_entropy_bits": math.fsum(row["descriptor"]["primitive_type_entropy_bits"] for row in rows) / len(rows),
        "mean_curved_surface_area_fraction": math.fsum(row["descriptor"]["curved_surface_area_fraction"] for row in rows) / len(rows),
        "unique_functional_path_signatures": len({row["descriptor"]["functional_path_signature"] for row in rows}),
        "failure_mode_coverage": dict(sorted(failures.items())),
        "failure_mode_scope": "bounded Work 050 evaluator outcomes; not general physical failure modes",
    }
