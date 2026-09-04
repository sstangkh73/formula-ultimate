"""Strict declarations for the Work 092 free-form B-rep solid grammar."""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping, Sequence


GRAMMAR_VERSION = "freeform_brep_solid_grammar_v2"
OPERATORS = (
    "section", "path", "extrude", "revolve", "sweep", "loft", "shell",
    "rib_web", "gusset", "pocket", "bore", "linear_pattern", "fillet",
    "chamfer", "boolean_union", "boolean_subtract", "boolean_intersect", "transform",
)
REQUIRED_FAMILIES = {
    "curved_branch", "tapered_hollow_duct", "lofted_rotary_member",
    "organic_load_bridge", "variable_section_shell",
}
DATUM_KINDS = ("bbox_center", "longest_bbox_axis", "extreme_plane")


class FreeformSolidGrammarError(ValueError):
    """Raised when a solid declaration is outside the bounded grammar."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")


def declaration_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise FreeformSolidGrammarError(f"{label} must be an object")
    return value


def _sequence(value: Any, label: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise FreeformSolidGrammarError(f"{label} must be an array")
    return value


def _exact(value: Mapping[str, Any], fields: set[str], label: str) -> None:
    if set(value) != fields:
        raise FreeformSolidGrammarError(f"{label} schema mismatch")


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FreeformSolidGrammarError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise FreeformSolidGrammarError(f"{label} must be finite")
    return result


def _positive(value: Any, label: str, maximum: float | None = None) -> float:
    result = _number(value, label)
    if result <= 0.0 or (maximum is not None and result > maximum):
        raise FreeformSolidGrammarError(f"{label} is outside positive bounds")
    return result


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or not value[0].islower() or any(
        not (character.islower() or character.isdigit() or character in "_-.") for character in value
    ):
        raise FreeformSolidGrammarError(f"{label} must be a lower-case identifier")
    return value


def _point(value: Any, label: str, maximum: float) -> tuple[float, float, float]:
    raw = _sequence(value, label)
    if len(raw) != 3:
        raise FreeformSolidGrammarError(f"{label} must contain three coordinates")
    point = tuple(_number(item, label) for item in raw)
    if max(abs(item) for item in point) > maximum:
        raise FreeformSolidGrammarError(f"{label} exceeds coordinate bounds")
    return point  # type: ignore[return-value]


def _bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise FreeformSolidGrammarError(f"{label} must be boolean")
    return value


PARAMETER_FIELDS = {
    "section": {"profile_id", "scale", "translation_m", "rotation_rad"},
    "path": {"path_kind", "points_m"},
    "extrude": {"vector_m", "taper_rad"},
    "revolve": {"axis_start_m", "axis_end_m", "angle_rad"},
    "sweep": {"is_frenet", "transition_mode"},
    "loft": {"ruled"},
    "shell": {"thickness_m", "opening_axis", "opening_side", "kind"},
    "rib_web": {"size_m", "center_m"},
    "gusset": {"size_m", "center_m", "axis"},
    "pocket": {"size_m", "center_m"},
    "bore": {"radius_m", "length_m", "origin_m", "direction"},
    "linear_pattern": {"count", "spacing_m", "direction", "fuse"},
    "fillet": {"radius_m", "selector_axis"},
    "chamfer": {"distance_m", "selector_axis"},
    "boolean_union": set(),
    "boolean_subtract": set(),
    "boolean_intersect": set(),
    "transform": {"translation_m", "axis_start_m", "axis_end_m", "angle_rad"},
}


INPUT_COUNTS = {
    "section": (0, 0), "path": (0, 0), "extrude": (1, 1), "revolve": (1, 1),
    "sweep": (2, 2), "loft": (2, 8), "shell": (1, 1), "rib_web": (1, 1),
    "gusset": (1, 1), "pocket": (1, 1), "bore": (1, 1), "linear_pattern": (1, 1),
    "fillet": (1, 1), "chamfer": (1, 1), "boolean_union": (2, 8),
    "boolean_subtract": (2, 2), "boolean_intersect": (2, 2), "transform": (1, 1),
}


def validate_solid_grammar(value: Mapping[str, Any], profile_ids: set[str]) -> dict[str, Any]:
    root = _mapping(value, "grammar")
    _exact(root, {"grammar_version", "units", "source_wire_declaration_sha256", "limits", "candidates"}, "grammar")
    if root["grammar_version"] != GRAMMAR_VERSION or root["units"] != "SI_m_rad":
        raise FreeformSolidGrammarError("grammar identity or units mismatch")
    if not isinstance(root["source_wire_declaration_sha256"], str) or len(root["source_wire_declaration_sha256"]) != 64:
        raise FreeformSolidGrammarError("source wire identity must be SHA-256")
    limits = _mapping(root["limits"], "limits")
    _exact(limits, {"maximum_coordinate_m", "maximum_dimension_m", "minimum_feature_m", "maximum_features_per_candidate", "measurement_relative_tolerance", "position_absolute_tolerance_m"}, "limits")
    coordinate_bound = _positive(limits["maximum_coordinate_m"], "maximum coordinate")
    dimension_bound = _positive(limits["maximum_dimension_m"], "maximum dimension")
    minimum_feature = _positive(limits["minimum_feature_m"], "minimum feature")
    measurement_tolerance = _positive(limits["measurement_relative_tolerance"], "measurement tolerance")
    position_tolerance = _positive(limits["position_absolute_tolerance_m"], "position tolerance")
    if measurement_tolerance > 0.002 or position_tolerance >= minimum_feature:
        raise FreeformSolidGrammarError("tolerance policy exceeds V2 bounds")
    maximum_features = limits["maximum_features_per_candidate"]
    if isinstance(maximum_features, bool) or not isinstance(maximum_features, int) or not 4 <= maximum_features <= 64:
        raise FreeformSolidGrammarError("maximum feature count is outside bounds")
    candidates = _sequence(root["candidates"], "candidates")
    if len(candidates) < 10:
        raise FreeformSolidGrammarError("at least ten solid candidates are required")
    candidate_ids: set[str] = set()
    family_coverage: set[str] = set()
    operator_coverage: set[str] = set()
    for candidate_index, raw_candidate in enumerate(candidates):
        candidate = _mapping(raw_candidate, f"candidates[{candidate_index}]")
        _exact(candidate, {"candidate_id", "family", "expected_body_count", "features", "final_feature_id", "datums"}, "candidate")
        candidate_id = _identifier(candidate["candidate_id"], "candidate_id")
        if candidate_id in candidate_ids:
            raise FreeformSolidGrammarError("duplicate candidate identity")
        candidate_ids.add(candidate_id)
        family_coverage.add(_identifier(candidate["family"], "family"))
        expected_body_count = candidate["expected_body_count"]
        if isinstance(expected_body_count, bool) or not isinstance(expected_body_count, int) or not 1 <= expected_body_count <= 8:
            raise FreeformSolidGrammarError("expected body count is outside bounds")
        features = _sequence(candidate["features"], "features")
        if not 1 <= len(features) <= maximum_features:
            raise FreeformSolidGrammarError("candidate feature count is outside bounds")
        feature_ids: set[str] = set()
        feature_types: dict[str, str] = {}
        for feature_index, raw_feature in enumerate(features):
            feature = _mapping(raw_feature, f"{candidate_id}.features[{feature_index}]")
            _exact(feature, {"feature_id", "operator", "inputs", "parameters"}, "feature")
            feature_id = _identifier(feature["feature_id"], "feature_id")
            if feature_id in feature_ids:
                raise FreeformSolidGrammarError("duplicate feature identity")
            operator = feature["operator"]
            if operator not in OPERATORS:
                raise FreeformSolidGrammarError("unsupported solid operator")
            inputs = [_identifier(item, "feature input") for item in _sequence(feature["inputs"], "feature inputs")]
            lower, upper = INPUT_COUNTS[operator]
            if not lower <= len(inputs) <= upper or any(item not in feature_ids for item in inputs):
                raise FreeformSolidGrammarError("feature inputs must have valid earlier ancestry")
            parameters = _mapping(feature["parameters"], "feature parameters")
            _exact(parameters, PARAMETER_FIELDS[operator], f"{operator} parameters")
            if operator == "section":
                if parameters["profile_id"] not in profile_ids:
                    raise FreeformSolidGrammarError("unknown Work 091 profile")
                _positive(parameters["scale"], "section scale", 4.0)
                _point(parameters["translation_m"], "section translation", coordinate_bound)
                _number(parameters["rotation_rad"], "section rotation")
                feature_types[feature_id] = "section"
            elif operator == "path":
                if parameters["path_kind"] not in {"polyline", "spline"}:
                    raise FreeformSolidGrammarError("unsupported path kind")
                points = [_point(item, "path point", coordinate_bound) for item in _sequence(parameters["points_m"], "path points")]
                if len(points) < 2 or any(math.dist(a, b) < minimum_feature for a, b in zip(points, points[1:])):
                    raise FreeformSolidGrammarError("path is zero length or underspecified")
                feature_types[feature_id] = "path"
            else:
                expected_inputs = {
                    "extrude": ("section",), "revolve": ("section",), "sweep": ("section", "path"),
                    "loft": tuple("section" for _ in inputs),
                }.get(operator)
                if expected_inputs is not None and tuple(feature_types[item] for item in inputs) != expected_inputs:
                    raise FreeformSolidGrammarError("feature input types are incompatible")
                if operator not in {"extrude", "revolve", "sweep", "loft"} and any(feature_types[item] != "solid" for item in inputs):
                    raise FreeformSolidGrammarError("solid operator requires solid ancestry")
                feature_types[feature_id] = "solid"
                _validate_parameters(operator, parameters, coordinate_bound, dimension_bound, minimum_feature)
            feature_ids.add(feature_id)
            operator_coverage.add(operator)
        final_feature_id = _identifier(candidate["final_feature_id"], "final_feature_id")
        if final_feature_id not in feature_ids or feature_types[final_feature_id] != "solid":
            raise FreeformSolidGrammarError("final feature must identify a solid")
        datums = _sequence(candidate["datums"], "datums")
        if len(datums) < 3:
            raise FreeformSolidGrammarError("each candidate requires point, axis, and plane datums")
        datum_ids: set[str] = set()
        datum_kinds: set[str] = set()
        for raw_datum in datums:
            datum = _mapping(raw_datum, "datum")
            _exact(datum, {"datum_id", "kind", "parameters"}, "datum")
            datum_id = _identifier(datum["datum_id"], "datum_id")
            if datum_id in datum_ids or datum["kind"] not in DATUM_KINDS:
                raise FreeformSolidGrammarError("duplicate or unsupported datum")
            datum_ids.add(datum_id); datum_kinds.add(datum["kind"])
            params = _mapping(datum["parameters"], "datum parameters")
            expected = {"bbox_center": set(), "longest_bbox_axis": set(), "extreme_plane": {"axis", "side"}}[datum["kind"]]
            _exact(params, expected, "datum parameters")
            if datum["kind"] == "extreme_plane" and (params["axis"] not in {"x", "y", "z"} or params["side"] not in {"min", "max"}):
                raise FreeformSolidGrammarError("invalid extreme-plane datum")
        if datum_kinds != set(DATUM_KINDS):
            raise FreeformSolidGrammarError("datum kind coverage is incomplete")
    if not REQUIRED_FAMILIES.issubset(family_coverage):
        raise FreeformSolidGrammarError("required solid family coverage mismatch")
    return {
        "status": "passed", "candidate_count": len(candidates),
        "family_coverage": sorted(family_coverage), "operator_coverage": sorted(operator_coverage),
        "declaration_sha256": declaration_sha256(value),
    }


def _validate_parameters(operator: str, parameters: Mapping[str, Any], coordinate: float, dimension: float, minimum: float) -> None:
    if operator == "extrude":
        vector = _point(parameters["vector_m"], "extrude vector", dimension)
        if math.sqrt(sum(item * item for item in vector)) < minimum:
            raise FreeformSolidGrammarError("extrude vector is too short")
        _number(parameters["taper_rad"], "taper")
    elif operator == "revolve":
        start = _point(parameters["axis_start_m"], "revolve axis start", coordinate)
        end = _point(parameters["axis_end_m"], "revolve axis end", coordinate)
        if math.dist(start, end) < minimum or not 0 < _number(parameters["angle_rad"], "revolve angle") <= 2 * math.pi:
            raise FreeformSolidGrammarError("revolve axis or angle is invalid")
    elif operator == "sweep":
        _bool(parameters["is_frenet"], "is_frenet")
        if parameters["transition_mode"] not in {"transformed", "round", "right"}:
            raise FreeformSolidGrammarError("unsupported sweep transition")
    elif operator == "loft":
        _bool(parameters["ruled"], "ruled")
    elif operator == "shell":
        _positive(parameters["thickness_m"], "shell thickness", dimension)
        if parameters["opening_axis"] not in {"x", "y", "z"} or parameters["opening_side"] not in {"min", "max"} or parameters["kind"] not in {"arc", "intersection"}:
            raise FreeformSolidGrammarError("invalid shell parameters")
    elif operator in {"rib_web", "pocket"}:
        sizes = _sequence(parameters["size_m"], "tool size")
        if len(sizes) != 3 or any(_positive(item, "tool dimension", dimension) < minimum for item in sizes):
            raise FreeformSolidGrammarError("invalid tool dimensions")
        _point(parameters["center_m"], "tool centre", coordinate)
    elif operator == "gusset":
        sizes = _sequence(parameters["size_m"], "gusset size")
        if len(sizes) != 3 or any(_positive(item, "gusset dimension", dimension) < minimum for item in sizes):
            raise FreeformSolidGrammarError("invalid gusset dimensions")
        _point(parameters["center_m"], "gusset centre", coordinate)
        if parameters["axis"] not in {"x", "y", "z"}:
            raise FreeformSolidGrammarError("invalid gusset axis")
    elif operator == "bore":
        _positive(parameters["radius_m"], "bore radius", dimension)
        _positive(parameters["length_m"], "bore length", dimension)
        _point(parameters["origin_m"], "bore origin", coordinate)
        direction = _point(parameters["direction"], "bore direction", 1.0)
        if math.sqrt(sum(item * item for item in direction)) < minimum:
            raise FreeformSolidGrammarError("bore direction is zero")
    elif operator == "linear_pattern":
        count = parameters["count"]
        if isinstance(count, bool) or not isinstance(count, int) or not 2 <= count <= 16:
            raise FreeformSolidGrammarError("pattern count is outside bounds")
        _positive(parameters["spacing_m"], "pattern spacing", dimension)
        if parameters["direction"] not in {"x", "y", "z"}:
            raise FreeformSolidGrammarError("invalid pattern direction")
        _bool(parameters["fuse"], "pattern fuse")
    elif operator in {"fillet", "chamfer"}:
        _positive(parameters["radius_m"] if operator == "fillet" else parameters["distance_m"], operator, dimension)
        if parameters["selector_axis"] not in {"x", "y", "z"}:
            raise FreeformSolidGrammarError("invalid edge selector axis")
    elif operator == "transform":
        _point(parameters["translation_m"], "transform translation", coordinate)
        start = _point(parameters["axis_start_m"], "transform axis start", coordinate)
        end = _point(parameters["axis_end_m"], "transform axis end", coordinate)
        if math.dist(start, end) < minimum:
            raise FreeformSolidGrammarError("transform axis is zero")
        _number(parameters["angle_rad"], "transform angle")
