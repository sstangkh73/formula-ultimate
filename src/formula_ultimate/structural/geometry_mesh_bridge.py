"""Deterministic labelled-cell to tetrahedral mesh bridge for Work 110."""
from __future__ import annotations

from collections import defaultdict
import hashlib
import json
import math
from typing import Any, Mapping


PROTOCOL_VERSION = "geometry_mesh_bridge_v1"
Cell = tuple[int, int, int]


class GeometryMeshViolation(ValueError):
    pass


def canonical_sha256(value: Any) -> str:
    try:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        raise GeometryMeshViolation("mesh evidence must be finite canonical JSON") from exc
    return hashlib.sha256(encoded).hexdigest()


def validate_protocol(raw: Mapping[str, Any]) -> dict[str, Any]:
    if set(raw) != {"protocol_version", "units", "dependencies", "refinement_resolutions_m", "limits", "routes", "experiment"} or raw.get("protocol_version") != PROTOCOL_VERSION or raw.get("units") != "SI_m_kg":
        raise GeometryMeshViolation("protocol schema, identity, or units mismatch")
    dependencies = raw["dependencies"]
    if not isinstance(dependencies, list) or len(dependencies) != 2:
        raise GeometryMeshViolation("Work 108 and Work 109 dependencies are required")
    for item in dependencies:
        if set(item) != {"work", "commit", "contract_path", "contract_sha256"} or item["work"] not in {108, 109} or len(item["commit"]) != 40 or len(item["contract_sha256"]) != 64:
            raise GeometryMeshViolation("dependency identity is invalid")
    if {item["work"] for item in dependencies} != {108, 109}:
        raise GeometryMeshViolation("dependency work coverage mismatch")
    levels = raw["refinement_resolutions_m"]
    if not isinstance(levels, list) or len(levels) < 3 or any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x <= 0 for x in levels) or levels != sorted(levels, reverse=True):
        raise GeometryMeshViolation("three coarse-to-fine refinement levels are required")
    limits = raw["limits"]
    if set(limits) != {"maximum_elements", "minimum_jacobian_m3", "maximum_edge_ratio", "field_volume_relative", "brep_volume_relative", "mass_relative"}:
        raise GeometryMeshViolation("mesh limits schema mismatch")
    if not isinstance(limits["maximum_elements"], int) or limits["maximum_elements"] < 100:
        raise GeometryMeshViolation("element budget is invalid")
    for key in set(limits) - {"maximum_elements"}:
        value = limits[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise GeometryMeshViolation("mesh limit must be positive finite")
    routes = raw["routes"]
    if not isinstance(routes, list) or {item.get("representation") for item in routes} != {"work109_field", "work108_brep"}:
        raise GeometryMeshViolation("both upstream representation routes are required")
    for route in routes:
        if set(route) != {"route_id", "representation", "source_config", "source_identity", "material_density_kg_m3", "required_boundary_sets"} or len(route["source_identity"]) != 64:
            raise GeometryMeshViolation("route schema or identity is invalid")
        if not route["required_boundary_sets"] or len(route["required_boundary_sets"]) != len(set(route["required_boundary_sets"])):
            raise GeometryMeshViolation("required boundary sets are invalid")
    experiment = raw["experiment"]
    if set(experiment) != {"independent_variables", "dependent_variables", "controls", "success_criteria", "failure_criteria"} or any(not v for v in experiment.values()):
        raise GeometryMeshViolation("experiment registration is incomplete")
    return {"status": "passed", "level_count": len(levels), "route_count": len(routes), "protocol_sha256": canonical_sha256(raw)}


CORNERS = ((0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1))
TETS = ((0, 1, 2, 6), (0, 2, 3, 6), (0, 3, 7, 6), (0, 7, 4, 6), (0, 4, 5, 6), (0, 5, 1, 6))
FACES = {
    (-1, 0, 0): (0, 4, 7, 3), (1, 0, 0): (1, 2, 6, 5),
    (0, -1, 0): (0, 1, 5, 4), (0, 1, 0): (3, 7, 6, 2),
    (0, 0, -1): (0, 3, 2, 1), (0, 0, 1): (4, 5, 6, 7),
}


def _det(a, b, c, d) -> float:
    u = [b[i] - a[i] for i in range(3)]; v = [c[i] - a[i] for i in range(3)]; w = [d[i] - a[i] for i in range(3)]
    return u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0]) + u[2] * (v[0] * w[1] - v[1] * w[0])


def build_mesh(field: Mapping[Cell, str], spec: Mapping[str, Any], *, maximum_elements: int) -> dict[str, Any]:
    if not field:
        raise GeometryMeshViolation("cannot mesh an empty field")
    resolution = float(spec["resolution"]); minimum = spec["minimum"]
    node_ids: dict[tuple[int, int, int], int] = {}
    nodes: list[tuple[float, float, float]] = []
    tets: list[dict[str, Any]] = []
    surfaces: list[dict[str, Any]] = []

    def node(grid_point):
        if grid_point not in node_ids:
            node_ids[grid_point] = len(nodes) + 1
            nodes.append(tuple(minimum[i] + grid_point[i] * resolution for i in range(3)))
        return node_ids[grid_point]

    for cell in sorted(field):
        corner_nodes = [node(tuple(cell[i] + offset[i] for i in range(3))) for offset in CORNERS]
        for local in TETS:
            ids = [corner_nodes[i] for i in local]
            points = [nodes[i - 1] for i in ids]
            determinant = _det(*points)
            if determinant < 0:
                ids[1], ids[2] = ids[2], ids[1]
                determinant = -determinant
            edges = [math.dist(points[i], points[j]) for i in range(4) for j in range(i + 1, 4)]
            tets.append({"nodes": ids, "material": field[cell], "jacobian_m3": determinant, "edge_ratio": max(edges) / min(edges)})
        for delta, local_face in FACES.items():
            neighbor = tuple(cell[i] + delta[i] for i in range(3))
            if neighbor in field and field[neighbor] == field[cell]:
                continue
            if neighbor in field:
                if cell > neighbor:
                    continue
                set_name = "material_interface"
            else:
                normal_name = {(-1, 0, 0): "load_surface", (0, 0, -1): "contact_surface"}.get(delta, "external_surface")
                set_name = normal_name
            quad = [corner_nodes[i] for i in local_face]
            surfaces.extend(({"nodes": [quad[0], quad[1], quad[2]], "set": set_name}, {"nodes": [quad[0], quad[2], quad[3]], "set": set_name}))
    if len(tets) + len(surfaces) > maximum_elements:
        raise GeometryMeshViolation("mesh exceeded element budget")
    return {"nodes": nodes, "tetrahedra": tets, "triangles": surfaces}


def validate_mesh(mesh: Mapping[str, Any], required_sets: list[str], limits: Mapping[str, Any]) -> dict[str, Any]:
    nodes = mesh["nodes"]; tets = mesh["tetrahedra"]; triangles = mesh["triangles"]
    if not nodes or not tets or not triangles:
        raise GeometryMeshViolation("mesh nodes, volume elements, or surfaces are missing")
    node_count = len(nodes)
    materials = defaultdict(int); sets = defaultdict(int); volume = 0.0; minimum_jacobian = math.inf; maximum_edge_ratio = 0.0
    for tet in tets:
        if len(set(tet["nodes"])) != 4 or any(not 1 <= item <= node_count for item in tet["nodes"]) or tet["jacobian_m3"] <= limits["minimum_jacobian_m3"]:
            raise GeometryMeshViolation("inverted, zero, stale, or invalid tetrahedron")
        volume += tet["jacobian_m3"] / 6.0; minimum_jacobian = min(minimum_jacobian, tet["jacobian_m3"]); maximum_edge_ratio = max(maximum_edge_ratio, tet["edge_ratio"]); materials[tet["material"]] += 1
    if maximum_edge_ratio > limits["maximum_edge_ratio"]:
        raise GeometryMeshViolation("element edge-ratio quality limit exceeded")
    for triangle in triangles:
        if len(set(triangle["nodes"])) != 3 or any(not 1 <= item <= node_count for item in triangle["nodes"]):
            raise GeometryMeshViolation("invalid or stale surface element")
        sets[triangle["set"]] += 1
    missing = sorted(set(required_sets) - set(sets))
    if missing:
        raise GeometryMeshViolation(f"required boundary sets are missing: {missing}")
    return {"status": "passed", "node_count": node_count, "tetrahedron_count": len(tets), "triangle_count": len(triangles), "volume_m3": volume, "minimum_jacobian_m3": minimum_jacobian, "maximum_edge_ratio": maximum_edge_ratio, "material_element_counts": dict(sorted(materials.items())), "boundary_element_counts": dict(sorted(sets.items()))}


def gmsh_text(mesh: Mapping[str, Any]) -> str:
    materials = sorted({item["material"] for item in mesh["tetrahedra"]}); boundaries = sorted({item["set"] for item in mesh["triangles"]})
    physical = {name: index + 1 for index, name in enumerate(boundaries + materials)}
    lines = ["$MeshFormat", "2.2 0 8", "$EndMeshFormat", "$PhysicalNames", str(len(physical))]
    lines.extend(f'{2 if name in boundaries else 3} {physical[name]} "{name}"' for name in boundaries + materials)
    lines.extend(["$EndPhysicalNames", "$Nodes", str(len(mesh["nodes"]))])
    lines.extend(f"{i} {p[0]:.12g} {p[1]:.12g} {p[2]:.12g}" for i, p in enumerate(mesh["nodes"], 1))
    lines.extend(["$EndNodes", "$Elements", str(len(mesh["triangles"]) + len(mesh["tetrahedra"]))])
    element_id = 1
    for tri in mesh["triangles"]:
        lines.append(f"{element_id} 2 2 {physical[tri['set']]} {physical[tri['set']]} " + " ".join(map(str, tri["nodes"]))); element_id += 1
    for tet in mesh["tetrahedra"]:
        lines.append(f"{element_id} 4 2 {physical[tet['material']]} {physical[tet['material']]} " + " ".join(map(str, tet["nodes"]))); element_id += 1
    return "\n".join(lines + ["$EndElements", ""])
