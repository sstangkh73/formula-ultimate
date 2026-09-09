"""Bounded implicit material-field generation and surface extraction for Work 109."""
from __future__ import annotations

from collections import defaultdict, deque
import hashlib
import json
import math
from typing import Any, Iterable, Mapping, Sequence


PROTOCOL_VERSION = "freeform_material_generator_v1"
OPERATORS = ("boundary_displacement", "cavity_route", "branch", "split", "merge", "material_redistribution")
Cell = tuple[int, int, int]
Point = tuple[float, float, float]


class FreeformMaterialViolation(ValueError):
    """Raised when a field, edit, surface, or budget is invalid."""


def canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise FreeformMaterialViolation("state must be finite canonical JSON") from exc


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise FreeformMaterialViolation(f"{label} must be finite numeric")
    return float(value)


def _point(value: Any, label: str) -> Point:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) or len(value) != 3:
        raise FreeformMaterialViolation(f"{label} must contain three coordinates")
    return tuple(_number(item, label) for item in value)  # type: ignore[return-value]


def validate_protocol(raw: Mapping[str, Any]) -> dict[str, Any]:
    required = {"protocol_version", "units", "dependency", "representation", "materials", "source_primitives", "operator_chain", "refinement_resolutions_m", "experiment"}
    if set(raw) != required or raw.get("protocol_version") != PROTOCOL_VERSION or raw.get("units") != "SI_m":
        raise FreeformMaterialViolation("protocol schema, identity, or units mismatch")
    dependency = raw["dependency"]
    if not isinstance(dependency, Mapping) or set(dependency) != {"work108_commit", "spatial_contract_path", "spatial_contract_sha256"}:
        raise FreeformMaterialViolation("Work 108 dependency schema mismatch")
    if not isinstance(dependency["work108_commit"], str) or len(dependency["work108_commit"]) != 40 or not isinstance(dependency["spatial_contract_path"], str):
        raise FreeformMaterialViolation("Work 108 dependency identity is invalid")
    if not isinstance(dependency["spatial_contract_sha256"], str) or len(dependency["spatial_contract_sha256"]) != 64:
        raise FreeformMaterialViolation("Work 108 contract identity is invalid")
    representation = raw["representation"]
    if not isinstance(representation, Mapping) or set(representation) != {
        "domain_min_m", "domain_max_m", "resolution_m", "minimum_feature_m", "surface_volume_relative_tolerance",
        "maximum_occupied_cells", "maximum_changed_cells_per_edit", "maximum_surface_triangles",
    }:
        raise FreeformMaterialViolation("representation schema mismatch")
    minimum = _point(representation["domain_min_m"], "domain minimum")
    maximum = _point(representation["domain_max_m"], "domain maximum")
    resolution = _number(representation["resolution_m"], "resolution")
    feature = _number(representation["minimum_feature_m"], "minimum feature")
    tolerance = _number(representation["surface_volume_relative_tolerance"], "surface tolerance")
    if resolution <= 0 or feature < resolution or not 0 < tolerance <= 1e-9 or any(a >= b for a, b in zip(minimum, maximum)):
        raise FreeformMaterialViolation("representation bounds are invalid")
    dimensions = []
    for low, high in zip(minimum, maximum):
        cells = (high - low) / resolution
        if abs(cells - round(cells)) > 1e-9 or not 4 <= round(cells) <= 256:
            raise FreeformMaterialViolation("domain must contain an integral bounded grid")
        dimensions.append(int(round(cells)))
    for field, low, high in (
        ("maximum_occupied_cells", 1, math.prod(dimensions)),
        ("maximum_changed_cells_per_edit", 1, math.prod(dimensions)),
        ("maximum_surface_triangles", 12, 1_000_000),
    ):
        value = representation[field]
        if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
            raise FreeformMaterialViolation(f"{field} is outside bounds")
    materials = raw["materials"]
    if not isinstance(materials, list) or len(materials) < 2 or len(materials) != len(set(materials)) or any(not isinstance(item, str) or not item for item in materials):
        raise FreeformMaterialViolation("at least two unique material labels are required")
    primitives = raw["source_primitives"]
    if not isinstance(primitives, list) or not primitives:
        raise FreeformMaterialViolation("source primitives are required")
    for primitive in primitives:
        if not isinstance(primitive, Mapping) or primitive.get("kind") not in {"sphere", "capsule"} or primitive.get("material") not in materials:
            raise FreeformMaterialViolation("source primitive is unsupported")
        _number(primitive.get("radius_m"), "primitive radius")
        if primitive["radius_m"] < feature:
            raise FreeformMaterialViolation("source primitive is below minimum feature")
        if primitive["kind"] == "sphere":
            _point(primitive.get("centre_m"), "sphere centre")
            if set(primitive) != {"kind", "centre_m", "radius_m", "material"}:
                raise FreeformMaterialViolation("sphere schema mismatch")
        else:
            if set(primitive) != {"kind", "path_m", "radius_m", "material", "feature_tag"}:
                raise FreeformMaterialViolation("capsule schema mismatch")
            path = primitive["path_m"]
            if not isinstance(path, list) or len(path) < 2:
                raise FreeformMaterialViolation("capsule path is incomplete")
            for point in path:
                _point(point, "capsule point")
            if not isinstance(primitive["feature_tag"], str) or not primitive["feature_tag"]:
                raise FreeformMaterialViolation("feature tag is required")
    chain = raw["operator_chain"]
    if not isinstance(chain, list) or not chain:
        raise FreeformMaterialViolation("operator chain is required")
    coverage = set()
    for slot, edit in enumerate(chain):
        if not isinstance(edit, Mapping) or set(edit) != {"operator", "parameters", "seed", "slot"} or edit["operator"] not in OPERATORS:
            raise FreeformMaterialViolation("operator declaration is invalid")
        if edit["slot"] != slot or isinstance(edit["seed"], bool) or not isinstance(edit["seed"], int):
            raise FreeformMaterialViolation("operator slots and seeds must be fixed")
        if not isinstance(edit["parameters"], Mapping):
            raise FreeformMaterialViolation("operator parameters must be an object")
        coverage.add(edit["operator"])
    if coverage != set(OPERATORS):
        raise FreeformMaterialViolation("operator coverage is incomplete")
    refinements = raw["refinement_resolutions_m"]
    if not isinstance(refinements, list) or len(refinements) < 3 or any(_number(item, "refinement resolution") <= 0 for item in refinements):
        raise FreeformMaterialViolation("at least three refinement levels are required")
    experiment = raw["experiment"]
    if not isinstance(experiment, Mapping) or set(experiment) != {"independent_variables", "dependent_variables", "controls", "success_criteria", "failure_criteria"}:
        raise FreeformMaterialViolation("experiment registration is incomplete")
    for values in experiment.values():
        if not isinstance(values, list) or not values or any(not isinstance(item, str) or not item for item in values):
            raise FreeformMaterialViolation("experiment fields must be explicit")
    return {"status": "passed", "dimensions": dimensions, "operator_coverage": sorted(coverage), "protocol_sha256": canonical_sha256(raw)}


def grid_spec(representation: Mapping[str, Any], resolution: float | None = None) -> dict[str, Any]:
    step = float(representation["resolution_m"] if resolution is None else resolution)
    minimum = tuple(float(item) for item in representation["domain_min_m"])
    maximum = tuple(float(item) for item in representation["domain_max_m"])
    dimensions = tuple(int(round((high - low) / step)) for low, high in zip(minimum, maximum))
    if any(abs(low + size * step - high) > 1e-9 for low, high, size in zip(minimum, maximum, dimensions)):
        raise FreeformMaterialViolation("refinement does not divide the registered domain")
    return {"minimum": minimum, "maximum": maximum, "resolution": step, "dimensions": dimensions}


def cell_center(cell: Cell, spec: Mapping[str, Any]) -> Point:
    return tuple(spec["minimum"][axis] + (cell[axis] + 0.5) * spec["resolution"] for axis in range(3))  # type: ignore[return-value]


def _distance_segment(point: Point, start: Point, end: Point) -> float:
    direction = tuple(b - a for a, b in zip(start, end))
    length2 = sum(item * item for item in direction)
    if length2 <= 0:
        raise FreeformMaterialViolation("path segment has zero length")
    t = max(0.0, min(1.0, sum((p - a) * d for p, a, d in zip(point, start, direction)) / length2))
    nearest = tuple(a + t * d for a, d in zip(start, direction))
    return math.dist(point, nearest)


def _inside_path(point: Point, path: Sequence[Sequence[float]], radius: float) -> bool:
    points = [_point(item, "path point") for item in path]
    return any(_distance_segment(point, a, b) <= radius for a, b in zip(points, points[1:]))


def generate_source(protocol: Mapping[str, Any], resolution: float | None = None) -> tuple[dict[Cell, str], dict[str, Any]]:
    spec = grid_spec(protocol["representation"], resolution)
    field: dict[Cell, str] = {}
    visits = 0
    for i in range(spec["dimensions"][0]):
        for j in range(spec["dimensions"][1]):
            for k in range(spec["dimensions"][2]):
                cell = (i, j, k)
                point = cell_center(cell, spec)
                visits += 1
                for primitive in protocol["source_primitives"]:
                    inside = (
                        math.dist(point, _point(primitive["centre_m"], "sphere centre")) <= primitive["radius_m"]
                        if primitive["kind"] == "sphere"
                        else _inside_path(point, primitive["path_m"], primitive["radius_m"])
                    )
                    if inside:
                        field[cell] = primitive["material"]
    if not field or len(field) > protocol["representation"]["maximum_occupied_cells"]:
        raise FreeformMaterialViolation("source occupancy is empty or over budget")
    return field, {"grid_visits": visits, "occupied_cells": len(field)}


NEIGHBORS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def _components(cells: set[Cell]) -> int:
    remaining = set(cells)
    count = 0
    while remaining:
        count += 1
        queue = [remaining.pop()]
        while queue:
            cell = queue.pop()
            for delta in NEIGHBORS:
                neighbor = tuple(cell[axis] + delta[axis] for axis in range(3))
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    queue.append(neighbor)  # type: ignore[arg-type]
    return count


def field_descriptor(field: Mapping[Cell, str], spec: Mapping[str, Any]) -> dict[str, Any]:
    dimensions = spec["dimensions"]
    occupied = set(field)
    all_cells = {(i, j, k) for i in range(dimensions[0]) for j in range(dimensions[1]) for k in range(dimensions[2])}
    empty = all_cells - occupied
    exterior = deque(cell for cell in empty if any(cell[axis] in {0, dimensions[axis] - 1} for axis in range(3)))
    exterior_seen = set(exterior)
    while exterior:
        cell = exterior.popleft()
        for delta in NEIGHBORS:
            neighbor = tuple(cell[axis] + delta[axis] for axis in range(3))
            if neighbor in empty and neighbor not in exterior_seen:
                exterior_seen.add(neighbor)  # type: ignore[arg-type]
                exterior.append(neighbor)  # type: ignore[arg-type]
    enclosed = empty - exterior_seen
    labels: dict[str, int] = defaultdict(int)
    for label in field.values():
        if not isinstance(label, str):
            raise FreeformMaterialViolation("label mixing or non-scalar material label")
        labels[label] += 1
    return {
        "occupied_cells": len(field),
        "occupied_volume_m3": len(field) * spec["resolution"] ** 3,
        "connected_components": _components(occupied),
        "enclosed_void_components": _components(enclosed) if enclosed else 0,
        "material_cell_counts": dict(sorted(labels.items())),
        "geometry_sha256": canonical_sha256([[*cell, field[cell]] for cell in sorted(field)]),
    }


def apply_edit(field: Mapping[Cell, str], spec: Mapping[str, Any], edit: Mapping[str, Any], materials: set[str], maximum_changed: int) -> tuple[dict[Cell, str], dict[str, Any]]:
    result = dict(field)
    operator = edit["operator"]
    parameters = edit["parameters"]
    changed = 0
    for i in range(spec["dimensions"][0]):
        for j in range(spec["dimensions"][1]):
            for k in range(spec["dimensions"][2]):
                cell = (i, j, k)
                point = cell_center(cell, spec)
                before = result.get(cell)
                after = before
                if operator in {"boundary_displacement", "branch", "merge"}:
                    if set(parameters) != {"path_m", "radius_m", "material"} or parameters["material"] not in materials:
                        raise FreeformMaterialViolation("additive edit schema or material is invalid")
                    if _inside_path(point, parameters["path_m"], _number(parameters["radius_m"], "edit radius")):
                        after = parameters["material"]
                elif operator == "cavity_route":
                    if set(parameters) != {"path_m", "radius_m"}:
                        raise FreeformMaterialViolation("cavity route schema mismatch")
                    if _inside_path(point, parameters["path_m"], _number(parameters["radius_m"], "cavity radius")):
                        after = None
                elif operator == "split":
                    if set(parameters) != {"axis", "coordinate_m", "thickness_m"} or parameters["axis"] not in {"x", "y", "z"}:
                        raise FreeformMaterialViolation("split schema mismatch")
                    axis = "xyz".index(parameters["axis"])
                    if abs(point[axis] - _number(parameters["coordinate_m"], "split coordinate")) <= _number(parameters["thickness_m"], "split thickness") / 2:
                        after = None
                elif operator == "material_redistribution":
                    if set(parameters) != {"centre_m", "radius_m", "from_material", "to_material"} or not {parameters["from_material"], parameters["to_material"]}.issubset(materials):
                        raise FreeformMaterialViolation("redistribution schema or material is invalid")
                    if before == parameters["from_material"] and math.dist(point, _point(parameters["centre_m"], "redistribution centre")) <= _number(parameters["radius_m"], "redistribution radius"):
                        after = parameters["to_material"]
                else:
                    raise FreeformMaterialViolation("unsupported edit operator")
                if after != before:
                    changed += 1
                    if after is None:
                        result.pop(cell, None)
                    else:
                        result[cell] = after
    if changed == 0:
        raise FreeformMaterialViolation("edit produced a no-op")
    if changed > maximum_changed:
        raise FreeformMaterialViolation("edit exceeded changed-cell budget")
    return result, {"changed_cells": changed, "operator": operator, "seed": edit["seed"], "slot": edit["slot"]}


FACE_VERTICES = {
    (-1, 0, 0): ((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)),
    (1, 0, 0): ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)),
    (0, -1, 0): ((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)),
    (0, 1, 0): ((0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)),
    (0, 0, -1): ((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)),
    (0, 0, 1): ((0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)),
}


def extract_surface(field: Mapping[Cell, str], spec: Mapping[str, Any], maximum_triangles: int) -> dict[str, Any]:
    vertices: list[Point] = []
    vertex_index: dict[Point, int] = {}
    triangles: list[tuple[int, int, int]] = []
    for cell in sorted(field):
        for delta, offsets in FACE_VERTICES.items():
            neighbor = tuple(cell[axis] + delta[axis] for axis in range(3))
            if neighbor in field:
                continue
            quad = []
            for offset in offsets:
                point = tuple(spec["minimum"][axis] + (cell[axis] + offset[axis]) * spec["resolution"] for axis in range(3))
                if point not in vertex_index:
                    vertex_index[point] = len(vertices)
                    vertices.append(point)  # type: ignore[arg-type]
                quad.append(vertex_index[point])
            triangles.extend(((quad[0], quad[1], quad[2]), (quad[0], quad[2], quad[3])))
    if len(triangles) > maximum_triangles:
        raise FreeformMaterialViolation("surface exceeded triangle budget")
    edge_faces: dict[tuple[int, int], list[int]] = defaultdict(list)
    for face_index, triangle in enumerate(triangles):
        for a, b in ((triangle[0], triangle[1]), (triangle[1], triangle[2]), (triangle[2], triangle[0])):
            edge_faces[tuple(sorted((a, b)))].append(face_index)
    if any(len(faces) != 2 for faces in edge_faces.values()):
        raise FreeformMaterialViolation("surface is not closed two-manifold")
    adjacency: dict[int, set[int]] = defaultdict(set)
    for faces in edge_faces.values():
        adjacency[faces[0]].add(faces[1]); adjacency[faces[1]].add(faces[0])
    remaining = set(range(len(triangles)))
    boundary_components = 0
    while remaining:
        boundary_components += 1
        stack = [remaining.pop()]
        while stack:
            for neighbor in adjacency[stack.pop()]:
                if neighbor in remaining:
                    remaining.remove(neighbor); stack.append(neighbor)
    signed_volume = 0.0
    for a, b, c in triangles:
        p, q, r = vertices[a], vertices[b], vertices[c]
        cross = (q[1] * r[2] - q[2] * r[1], q[2] * r[0] - q[0] * r[2], q[0] * r[1] - q[1] * r[0])
        signed_volume += sum(p[axis] * cross[axis] for axis in range(3)) / 6.0
    chi = len(vertices) - len(edge_faces) + len(triangles)
    genus_sum = (2 * boundary_components - chi) // 2
    return {
        "vertices": vertices,
        "triangles": triangles,
        "vertex_count": len(vertices),
        "triangle_count": len(triangles),
        "edge_count": len(edge_faces),
        "boundary_components": boundary_components,
        "euler_characteristic": chi,
        "genus_sum": genus_sum,
        "enclosed_volume_m3": abs(signed_volume),
        "surface_sha256": canonical_sha256({"vertices": vertices, "triangles": triangles}),
    }


def write_obj(surface: Mapping[str, Any]) -> str:
    lines = ["# Work 109 deterministic voxel boundary"]
    lines.extend(f"v {x:.12g} {y:.12g} {z:.12g}" for x, y, z in surface["vertices"])
    lines.extend(f"f {a + 1} {b + 1} {c + 1}" for a, b, c in surface["triangles"])
    return "\n".join(lines) + "\n"
