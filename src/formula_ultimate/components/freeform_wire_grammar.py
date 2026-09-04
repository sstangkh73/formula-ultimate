"""Bounded, deterministic free-form planar wire declarations for Work 091."""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping, Sequence


GRAMMAR_VERSION = "constrained_freeform_wire_grammar_v2"
OPERATORS = ("line", "polyline", "tangent_arc", "three_point_arc", "circle", "ellipse", "bezier", "bspline")
TRANSFORMS = ("translate", "rotate", "mirror")
CONSTRAINTS = ("positive_area", "minimum_perimeter", "hole_count", "symmetric_axis")


class FreeformWireGrammarError(ValueError):
    """Raised before CAD execution when a wire declaration is invalid."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")


def declaration_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _relative_difference(reference: float, measured: float) -> float:
    return abs(reference - measured) / max(abs(reference), abs(measured), 1e-15)


def compare_measurement_witnesses(
    expected: Sequence[Mapping[str, Any]],
    measured: Sequence[Mapping[str, Any]],
    *,
    measurement_relative_tolerance: float,
    bounds_absolute_tolerance_m: float,
) -> dict[str, float]:
    """Compare independent CAD measurements without hiding topology changes."""
    relative_tolerance = _positive(measurement_relative_tolerance, "measurement relative tolerance")
    bounds_tolerance = _positive(bounds_absolute_tolerance_m, "bounds absolute tolerance")
    measured_by_id = {item.get("profile_id"): item for item in measured}
    if len(measured_by_id) != len(measured) or len(expected) != len(measured):
        raise FreeformWireGrammarError("measurement witness profile identity mismatch")
    maximum_area = 0.0
    maximum_perimeter = 0.0
    maximum_bounds = 0.0
    for reference in expected:
        profile_id = reference.get("profile_id")
        witness = measured_by_id.get(profile_id)
        if witness is None:
            raise FreeformWireGrammarError(f"missing measurement witness for {profile_id}")
        for field in ("face_count", "wire_count", "edge_count"):
            if witness.get(field) != reference.get(field):
                raise FreeformWireGrammarError(f"{profile_id} {field} witness mismatch")
        area = _relative_difference(float(reference["area_m2"]), float(witness["area_m2"]))
        perimeter = _relative_difference(float(reference["perimeter_m"]), float(witness["perimeter_m"]))
        maximum_area = max(maximum_area, area)
        maximum_perimeter = max(maximum_perimeter, perimeter)
        if area > relative_tolerance or perimeter > relative_tolerance:
            raise FreeformWireGrammarError(
                f"{profile_id} measurement witness exceeds relative tolerance: "
                f"area={area:.17g}, perimeter={perimeter:.17g}, limit={relative_tolerance:.17g}"
            )
        reference_bounds = reference["bounding_box_m"]
        measured_bounds = witness["bounding_box_m"]
        for end in ("minimum", "maximum"):
            reference_values = reference_bounds[end]
            measured_values = measured_bounds[end]
            if len(reference_values) != 3 or len(measured_values) != 3:
                raise FreeformWireGrammarError(f"{profile_id} bounding-box witness schema mismatch")
            for reference_value, measured_value in zip(reference_values, measured_values):
                difference = abs(float(reference_value) - float(measured_value))
                maximum_bounds = max(maximum_bounds, difference)
                if difference > bounds_tolerance:
                    raise FreeformWireGrammarError(
                        f"{profile_id} bounding-box witness exceeds absolute tolerance: "
                        f"difference_m={difference:.17g}, limit_m={bounds_tolerance:.17g}"
                    )
    return {
        "maximum_area_relative_difference": maximum_area,
        "maximum_perimeter_relative_difference": maximum_perimeter,
        "maximum_bounds_absolute_difference_m": maximum_bounds,
    }


def _exact(value: Mapping[str, Any], keys: set[str], label: str) -> None:
    if set(value) != keys:
        raise FreeformWireGrammarError(f"{label} schema mismatch")


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise FreeformWireGrammarError(f"{label} must be an object")
    return value


def _sequence(value: Any, label: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise FreeformWireGrammarError(f"{label} must be an array")
    return value


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FreeformWireGrammarError(f"{label} must be numeric")
    ready = float(value)
    if not math.isfinite(ready):
        raise FreeformWireGrammarError(f"{label} must be finite")
    return ready


def _positive(value: Any, label: str) -> float:
    ready = _number(value, label)
    if ready <= 0.0:
        raise FreeformWireGrammarError(f"{label} must be positive")
    return ready


def _point(value: Any, label: str, maximum_coordinate_m: float) -> tuple[float, float]:
    items = _sequence(value, label)
    if len(items) != 2:
        raise FreeformWireGrammarError(f"{label} must contain two coordinates")
    point = (_number(items[0], label), _number(items[1], label))
    if max(abs(point[0]), abs(point[1])) > maximum_coordinate_m:
        raise FreeformWireGrammarError(f"{label} exceeds coordinate bounds")
    return point


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or not value[0].islower() or any(not (char.islower() or char.isdigit() or char in "_-." ) for char in value):
        raise FreeformWireGrammarError(f"{label} must be a lower-case identifier")
    return value


def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _orientation(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _proper_intersection(a, b, c, d, tolerance: float) -> bool:
    o1, o2, o3, o4 = _orientation(a, b, c), _orientation(a, b, d), _orientation(c, d, a), _orientation(c, d, b)
    return o1 * o2 < -(tolerance * tolerance) and o3 * o4 < -(tolerance * tolerance)


def _validate_polyline(points: list[tuple[float, float]], tolerance: float, minimum_feature_m: float) -> None:
    if len(points) < 4 or _distance(points[0], points[-1]) > tolerance:
        raise FreeformWireGrammarError("polyline must be explicitly closed")
    if any(_distance(points[i], points[i + 1]) < minimum_feature_m for i in range(len(points) - 1)):
        raise FreeformWireGrammarError("polyline contains a zero or sub-tolerance segment")
    edges = list(zip(points[:-1], points[1:]))
    for i, (a, b) in enumerate(edges):
        for j, (c, d) in enumerate(edges[i + 1:], start=i + 1):
            if j in {i, i + 1} or (i == 0 and j == len(edges) - 1):
                continue
            if _proper_intersection(a, b, c, d, tolerance):
                raise FreeformWireGrammarError("polyline self-intersection detected")


def _segment_endpoints(operator: str, parameters: Mapping[str, Any], trim: tuple[float, float], maximum_coordinate_m: float) -> tuple[tuple[float, float], tuple[float, float]] | None:
    if operator == "line":
        start = _point(parameters["start_m"], "line start", maximum_coordinate_m)
        end = _point(parameters["end_m"], "line end", maximum_coordinate_m)
        return (
            (start[0] + trim[0] * (end[0] - start[0]), start[1] + trim[0] * (end[1] - start[1])),
            (start[0] + trim[1] * (end[0] - start[0]), start[1] + trim[1] * (end[1] - start[1])),
        )
    if operator == "polyline":
        points = parameters["points_m"]
        return points[0], points[-1]
    if operator in {"tangent_arc", "three_point_arc"}:
        return parameters["start_m"], parameters["end_m"]
    if operator in {"bezier", "bspline"}:
        points = parameters["control_points_m"]
        return None if operator == "bspline" and parameters["periodic"] else (points[0], points[-1])
    return None


def validate_grammar(value: Mapping[str, Any]) -> dict[str, Any]:
    root = _mapping(value, "grammar")
    _exact(root, {"grammar_version", "units", "limits", "profiles"}, "grammar")
    if root["grammar_version"] != GRAMMAR_VERSION or root["units"] != "SI_m_rad":
        raise FreeformWireGrammarError("grammar identity or units mismatch")
    limits = _mapping(root["limits"], "limits")
    _exact(limits, {"closure_tolerance_m", "measurement_relative_tolerance", "minimum_feature_m", "maximum_coordinate_m", "maximum_points_per_segment", "maximum_segments_per_loop", "maximum_loops_per_profile", "maximum_offset_m"}, "limits")
    closure = _positive(limits["closure_tolerance_m"], "closure tolerance")
    minimum = _positive(limits["minimum_feature_m"], "minimum feature")
    maximum_coordinate = _positive(limits["maximum_coordinate_m"], "maximum coordinate")
    maximum_offset = _positive(limits["maximum_offset_m"], "maximum offset")
    measurement_relative_tolerance = _positive(limits["measurement_relative_tolerance"], "measurement relative tolerance")
    if closure >= minimum:
        raise FreeformWireGrammarError("closure tolerance must be below minimum feature")
    if measurement_relative_tolerance > 0.01:
        raise FreeformWireGrammarError("measurement relative tolerance must not exceed one percent")
    for name in ("maximum_points_per_segment", "maximum_segments_per_loop", "maximum_loops_per_profile"):
        if isinstance(limits[name], bool) or not isinstance(limits[name], int) or limits[name] < 2:
            raise FreeformWireGrammarError(f"{name} must be an integer >= 2")
    profiles = _sequence(root["profiles"], "profiles")
    if len(profiles) < 12:
        raise FreeformWireGrammarError("at least twelve profiles are required")
    profile_ids: set[str] = set(); families: set[str] = set(); operator_coverage: set[str] = set(); transform_coverage: set[str] = set(); constraint_coverage: set[str] = set(); nonzero_offsets = 0; nontrivial_trims = 0
    for profile_index, raw_profile in enumerate(profiles):
        profile = _mapping(raw_profile, f"profiles[{profile_index}]")
        _exact(profile, {"profile_id", "family", "loops", "transforms", "offset", "constraints"}, "profile")
        profile_id = _identifier(profile["profile_id"], "profile_id")
        if profile_id in profile_ids:
            raise FreeformWireGrammarError("duplicate profile identity")
        profile_ids.add(profile_id); families.add(_identifier(profile["family"], "family"))
        loops = _sequence(profile["loops"], "loops")
        if not 1 <= len(loops) <= limits["maximum_loops_per_profile"]:
            raise FreeformWireGrammarError("profile loop count is outside bounds")
        loop_ids: set[str] = set(); roles: list[str] = []
        for loop_index, raw_loop in enumerate(loops):
            loop = _mapping(raw_loop, f"{profile_id}.loops[{loop_index}]")
            _exact(loop, {"loop_id", "role", "segments"}, "loop")
            loop_id = _identifier(loop["loop_id"], "loop_id")
            if loop_id in loop_ids:
                raise FreeformWireGrammarError("duplicate loop identity")
            loop_ids.add(loop_id)
            if loop["role"] not in {"outer", "hole"}:
                raise FreeformWireGrammarError("loop role must be outer or hole")
            roles.append(loop["role"])
            segments = _sequence(loop["segments"], "segments")
            if not 1 <= len(segments) <= limits["maximum_segments_per_loop"]:
                raise FreeformWireGrammarError("segment count is outside bounds")
            segment_ids: set[str] = set(); endpoints = []
            for segment_index, raw_segment in enumerate(segments):
                segment = _mapping(raw_segment, f"{loop_id}.segments[{segment_index}]")
                _exact(segment, {"segment_id", "operator", "parameters", "trim_fraction"}, "segment")
                segment_id = _identifier(segment["segment_id"], "segment_id")
                if segment_id in segment_ids:
                    raise FreeformWireGrammarError("duplicate segment identity")
                segment_ids.add(segment_id)
                operator = segment["operator"]
                if operator not in OPERATORS:
                    raise FreeformWireGrammarError("unsupported wire operator")
                operator_coverage.add(operator)
                trim_raw = _sequence(segment["trim_fraction"], "trim_fraction")
                if len(trim_raw) != 2:
                    raise FreeformWireGrammarError("trim_fraction must contain two values")
                trim = (_number(trim_raw[0], "trim start"), _number(trim_raw[1], "trim end"))
                if not 0.0 <= trim[0] < trim[1] <= 1.0:
                    raise FreeformWireGrammarError("trim_fraction must satisfy 0 <= start < end <= 1")
                if trim != (0.0, 1.0):
                    if operator != "line":
                        raise FreeformWireGrammarError("V2 trim is bounded to line segments")
                    nontrivial_trims += 1
                parameters = _mapping(segment["parameters"], "segment parameters")
                schemas = {
                    "line": {"start_m", "end_m"}, "polyline": {"points_m"},
                    "tangent_arc": {"start_m", "tangent", "end_m"},
                    "three_point_arc": {"start_m", "mid_m", "end_m"},
                    "circle": {"center_m", "radius_m"}, "ellipse": {"center_m", "radii_m", "rotation_rad"},
                    "bezier": {"control_points_m"}, "bspline": {"control_points_m", "degree", "periodic"},
                }
                _exact(parameters, schemas[operator], f"{operator} parameters")
                if operator == "line":
                    start = _point(parameters["start_m"], "line start", maximum_coordinate); end = _point(parameters["end_m"], "line end", maximum_coordinate)
                    if _distance(start, end) < minimum:
                        raise FreeformWireGrammarError("zero or sub-tolerance line")
                elif operator == "polyline":
                    points = [_point(item, "polyline point", maximum_coordinate) for item in _sequence(parameters["points_m"], "polyline points")]
                    if len(points) > limits["maximum_points_per_segment"]:
                        raise FreeformWireGrammarError("polyline point count exceeds bounds")
                    _validate_polyline(points, closure, minimum); parameters = dict(parameters); parameters["points_m"] = points
                elif operator == "tangent_arc":
                    start = _point(parameters["start_m"], "tangent arc start", maximum_coordinate); end = _point(parameters["end_m"], "tangent arc end", maximum_coordinate); tangent = _point(parameters["tangent"], "tangent vector", maximum_coordinate)
                    if _distance(start, end) < minimum or math.hypot(*tangent) < minimum:
                        raise FreeformWireGrammarError("invalid tangent arc")
                elif operator == "three_point_arc":
                    points = [_point(parameters[key], key, maximum_coordinate) for key in ("start_m", "mid_m", "end_m")]
                    if abs(_orientation(*points)) < minimum * minimum:
                        raise FreeformWireGrammarError("three-point arc is collinear")
                elif operator == "circle":
                    _point(parameters["center_m"], "circle center", maximum_coordinate); _positive(parameters["radius_m"], "circle radius")
                elif operator == "ellipse":
                    _point(parameters["center_m"], "ellipse center", maximum_coordinate); radii = _sequence(parameters["radii_m"], "ellipse radii")
                    if len(radii) != 2 or any(_positive(item, "ellipse radius") < minimum for item in radii): raise FreeformWireGrammarError("invalid ellipse radii")
                    _number(parameters["rotation_rad"], "ellipse rotation")
                elif operator == "bezier":
                    points = [_point(item, "Bezier control point", maximum_coordinate) for item in _sequence(parameters["control_points_m"], "Bezier control points")]
                    if len(points) not in {3, 4}: raise FreeformWireGrammarError("Bezier requires three or four control points")
                elif operator == "bspline":
                    points = [_point(item, "B-spline control point", maximum_coordinate) for item in _sequence(parameters["control_points_m"], "B-spline control points")]
                    if len(points) > limits["maximum_points_per_segment"] or len(points) < 4: raise FreeformWireGrammarError("B-spline point count is outside bounds")
                    if isinstance(parameters["degree"], bool) or not isinstance(parameters["degree"], int) or not 2 <= parameters["degree"] <= 5 or parameters["degree"] >= len(points): raise FreeformWireGrammarError("B-spline degree is outside bounds")
                    if not isinstance(parameters["periodic"], bool): raise FreeformWireGrammarError("B-spline periodic must be boolean")
                endpoints.append(_segment_endpoints(operator, parameters, trim, maximum_coordinate))
            if len(segments) == 1 and endpoints[0] is None:
                pass
            else:
                if any(item is None for item in endpoints):
                    raise FreeformWireGrammarError("closed primitive or periodic spline must be the only segment")
                ready = [item for item in endpoints if item is not None]
                for index, (_, end) in enumerate(ready):
                    next_start = ready[(index + 1) % len(ready)][0]
                    if _distance(end, next_start) > closure:
                        raise FreeformWireGrammarError("open loop or non-coincident segment endpoints")
        if roles.count("outer") != 1 or roles[0] != "outer":
            raise FreeformWireGrammarError("exactly one first outer loop is required")
        transforms = _sequence(profile["transforms"], "transforms")
        for raw_transform in transforms:
            transform = _mapping(raw_transform, "transform"); _exact(transform, {"operator", "parameters"}, "transform")
            operator = transform["operator"]
            if operator not in TRANSFORMS: raise FreeformWireGrammarError("unsupported transform")
            transform_coverage.add(operator); parameters = _mapping(transform["parameters"], "transform parameters")
            if operator == "translate": _exact(parameters, {"offset_m"}, "translate parameters"); _point(parameters["offset_m"], "translation", maximum_coordinate)
            elif operator == "rotate": _exact(parameters, {"angle_rad"}, "rotate parameters"); _number(parameters["angle_rad"], "rotation")
            else: _exact(parameters, {"axis"}, "mirror parameters");
            if operator == "mirror" and parameters["axis"] not in {"x", "y"}: raise FreeformWireGrammarError("mirror axis must be x or y")
        offset = _mapping(profile["offset"], "offset"); _exact(offset, {"distance_m", "kind"}, "offset")
        distance = _number(offset["distance_m"], "offset distance")
        if abs(distance) > maximum_offset or (0.0 < abs(distance) < minimum): raise FreeformWireGrammarError("offset is outside bounds")
        if offset["kind"] not in {"arc", "intersection", "tangent"}: raise FreeformWireGrammarError("unsupported offset kind")
        nonzero_offsets += int(distance != 0.0)
        constraints = _sequence(profile["constraints"], "constraints")
        if not constraints: raise FreeformWireGrammarError("each profile requires constraints")
        for raw_constraint in constraints:
            constraint = _mapping(raw_constraint, "constraint"); _exact(constraint, {"kind", "value"}, "constraint")
            if constraint["kind"] not in CONSTRAINTS: raise FreeformWireGrammarError("unsupported constraint")
            constraint_coverage.add(constraint["kind"])
            if constraint["kind"] in {"positive_area", "minimum_perimeter"}: _positive(constraint["value"], "constraint value")
            elif constraint["kind"] == "hole_count":
                if isinstance(constraint["value"], bool) or not isinstance(constraint["value"], int) or constraint["value"] < 0: raise FreeformWireGrammarError("hole_count must be a nonnegative integer")
            elif constraint["value"] not in {"x", "y"}: raise FreeformWireGrammarError("symmetric_axis value must be x or y")
    if len(families) < 6 or set(OPERATORS) != operator_coverage or set(TRANSFORMS) != transform_coverage or set(CONSTRAINTS) != constraint_coverage or nonzero_offsets < 1 or nontrivial_trims < 1:
        raise FreeformWireGrammarError("required corpus coverage mismatch")
    return {"status": "passed", "profile_count": len(profiles), "family_count": len(families), "operator_coverage": sorted(operator_coverage), "transform_coverage": sorted(transform_coverage), "constraint_coverage": sorted(constraint_coverage), "nonzero_offset_profiles": nonzero_offsets, "nontrivial_trim_segments": nontrivial_trims, "declaration_sha256": declaration_sha256(value)}
