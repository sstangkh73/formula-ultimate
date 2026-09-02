"""Bounded, fail-closed parametric B-rep feature declarations for Work 078."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping, Sequence


BREP_GRAMMAR_VERSION = "parametric_brep_feature_grammar_v1"
REQUIRED_FAMILIES = frozenset(
    {"shaft", "bracket", "hollow_housing", "ribbed_plate", "hub_like_rotating_part"}
)
OPERATORS = frozenset(
    {
        "sketch_profile",
        "extrude",
        "revolve",
        "pocket_cut",
        "through_hole",
        "stepped_bore",
        "shaft_shoulder",
        "rib_web",
        "shell_wall",
        "linear_pattern",
        "circular_pattern",
        "fillet_chamfer",
        "boolean_union",
        "boolean_subtract",
        "boolean_intersect",
    }
)


class BrepGrammarViolation(ValueError):
    """Raised before CAD execution when a feature declaration is invalid."""


def _mapping(value: Any, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise BrepGrammarViolation(f"{context} must be an object")
    return value


def _sequence(value: Any, context: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise BrepGrammarViolation(f"{context} must be an array")
    return value


def _exact(value: Mapping[str, Any], keys: set[str], context: str) -> None:
    missing = keys - set(value)
    unknown = set(value) - keys
    if missing or unknown:
        raise BrepGrammarViolation(
            f"{context} keys mismatch; missing={sorted(missing)}, unknown={sorted(unknown)}"
        )


def _identifier(value: Any, context: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or not value[0].islower()
        or any(not (char.islower() or char.isdigit() or char in "_.-") for char in value)
    ):
        raise BrepGrammarViolation(f"{context} must be a lower-case identifier")
    return value


def _number(value: Any, context: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise BrepGrammarViolation(f"{context} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise BrepGrammarViolation(f"{context} must be finite")
    return result


def _length(value: Any, context: str, *, allow_zero: bool = False) -> float:
    result = _number(value, context)
    lower = 0.0 if allow_zero else 1.0e-6
    if result < lower or (not allow_zero and result == 0.0) or result > 5.0:
        comparator = ">= 0" if allow_zero else "> 0"
        raise BrepGrammarViolation(f"{context} must be {comparator} and <= 5 m")
    return result


def _count(value: Any, context: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 2 <= value <= 64:
        raise BrepGrammarViolation(f"{context} must be an integer in [2, 64]")
    return value


def _parameter_keys(operator: str, parameters: Mapping[str, Any]) -> None:
    schemas: dict[str, set[str]] = {
        "sketch_profile": {"profile_type", "center_x_m", "center_y_m", "size_a_m", "size_b_m"},
        "extrude": {"distance_m"},
        "revolve": {"angle_rad"},
        "pocket_cut": {"width_m", "height_m", "depth_m", "center_x_m", "center_y_m"},
        "through_hole": {"diameter_m", "center_x_m", "center_y_m"},
        "stepped_bore": {"through_diameter_m", "counterbore_diameter_m", "counterbore_depth_m", "center_x_m", "center_y_m"},
        "shaft_shoulder": {"diameter_m", "length_m", "offset_z_m"},
        "rib_web": {"length_m", "width_m", "height_m", "center_x_m", "center_y_m", "base_z_m"},
        "shell_wall": {"wall_thickness_m", "opening"},
        "linear_pattern": {"count", "spacing_m", "direction"},
        "circular_pattern": {"count", "angle_rad"},
        "fillet_chamfer": {"mode", "selector", "size_m"},
        "boolean_union": set(),
        "boolean_subtract": set(),
        "boolean_intersect": set(),
    }
    _exact(parameters, schemas[operator], f"{operator} parameters")


def _validate_parameters(operator: str, parameters: Mapping[str, Any]) -> None:
    _parameter_keys(operator, parameters)
    for name, value in parameters.items():
        if name in {"profile_type", "opening", "direction", "mode", "selector"}:
            continue
        if name == "count":
            _count(value, f"{operator}.{name}")
        elif name.endswith("_rad"):
            angle = _number(value, f"{operator}.{name}")
            if not 0.0 < angle <= 2.0 * math.pi:
                raise BrepGrammarViolation(f"{operator}.{name} must be in (0, 2*pi]")
        elif name in {"center_x_m", "center_y_m", "offset_z_m", "base_z_m"}:
            coordinate = _number(value, f"{operator}.{name}")
            if abs(coordinate) > 5.0:
                raise BrepGrammarViolation(f"{operator}.{name} magnitude must be <= 5 m")
        elif name.endswith("_m"):
            _length(
                value,
                f"{operator}.{name}",
                allow_zero=operator == "sketch_profile" and name == "size_b_m",
            )
        else:
            raise BrepGrammarViolation(f"{operator}.{name} has an unknown SI unit")

    if operator == "sketch_profile":
        if parameters["profile_type"] not in {"rectangle", "circle", "annulus", "shaft_section"}:
            raise BrepGrammarViolation("unsupported sketch profile_type")
        a = _length(parameters["size_a_m"], "sketch_profile.size_a_m")
        b = _length(parameters["size_b_m"], "sketch_profile.size_b_m", allow_zero=True)
        if parameters["profile_type"] == "annulus" and not 0.0 < b < a:
            raise BrepGrammarViolation("annulus inner radius must be in (0, outer radius)")
        if parameters["profile_type"] in {"rectangle", "shaft_section"} and b <= 0.0:
            raise BrepGrammarViolation("two-dimensional profile size must be > 0")
        if parameters["profile_type"] == "circle" and b != 0.0:
            raise BrepGrammarViolation("circle size_b_m must be zero")
    elif operator == "shell_wall" and parameters["opening"] != "top":
        raise BrepGrammarViolation("shell_wall opening must be top")
    elif operator == "linear_pattern" and parameters["direction"] not in {"x", "y", "z"}:
        raise BrepGrammarViolation("linear_pattern direction is unsupported")
    elif operator == "fillet_chamfer":
        if parameters["mode"] not in {"fillet", "chamfer"}:
            raise BrepGrammarViolation("fillet_chamfer mode is unsupported")
        if parameters["selector"] not in {"vertical", "circular"}:
            raise BrepGrammarViolation("fillet_chamfer selector is unsupported")
    elif operator == "stepped_bore":
        if parameters["counterbore_diameter_m"] <= parameters["through_diameter_m"]:
            raise BrepGrammarViolation("counterbore diameter must exceed through diameter")


def validate_brep_grammar(value: Mapping[str, Any]) -> dict[str, Any]:
    root = _mapping(value, "grammar")
    _exact(root, {"grammar_version", "candidates"}, "grammar")
    if root["grammar_version"] != BREP_GRAMMAR_VERSION:
        raise BrepGrammarViolation("grammar_version mismatch")
    candidates = _sequence(root["candidates"], "candidates")
    if not candidates:
        raise BrepGrammarViolation("candidates must not be empty")
    candidate_ids: list[str] = []
    families: set[str] = set()
    coverage: set[str] = set()
    feature_count = 0
    for candidate_index, raw_candidate in enumerate(candidates):
        candidate = _mapping(raw_candidate, f"candidates[{candidate_index}]")
        _exact(candidate, {"candidate_id", "family", "features", "final_feature_id"}, f"candidates[{candidate_index}]")
        candidate_id = _identifier(candidate["candidate_id"], "candidate_id")
        candidate_ids.append(candidate_id)
        family = _identifier(candidate["family"], "family")
        if family not in REQUIRED_FAMILIES:
            raise BrepGrammarViolation("unsupported candidate family")
        families.add(family)
        known_features: list[str] = []
        for feature_index, raw_feature in enumerate(_sequence(candidate["features"], "features")):
            feature = _mapping(raw_feature, f"{candidate_id}.features[{feature_index}]")
            _exact(feature, {"feature_id", "operator", "inputs", "parameters"}, f"{candidate_id}.features[{feature_index}]")
            feature_id = _identifier(feature["feature_id"], "feature_id")
            if feature_id in known_features:
                raise BrepGrammarViolation("duplicate feature identity")
            operator = feature["operator"]
            if operator not in OPERATORS:
                raise BrepGrammarViolation("unsupported feature operator")
            inputs = tuple(
                _identifier(item, "feature input")
                for item in _sequence(feature["inputs"], "feature inputs")
            )
            expected_inputs = 0 if operator == "sketch_profile" else 2 if operator.startswith("boolean_") else 1
            if len(inputs) != expected_inputs:
                raise BrepGrammarViolation(f"{operator} requires {expected_inputs} inputs")
            if any(item not in known_features for item in inputs):
                raise BrepGrammarViolation("feature input must precede its consumer")
            _validate_parameters(operator, _mapping(feature["parameters"], "feature parameters"))
            known_features.append(feature_id)
            coverage.add(operator)
            feature_count += 1
        if not known_features or candidate["final_feature_id"] not in known_features:
            raise BrepGrammarViolation("final_feature_id must reference a declared feature")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise BrepGrammarViolation("duplicate candidate identity")
    if families != REQUIRED_FAMILIES:
        raise BrepGrammarViolation(f"required family coverage mismatch: {sorted(REQUIRED_FAMILIES - families)}")
    if coverage != OPERATORS:
        raise BrepGrammarViolation(f"operator coverage mismatch: {sorted(OPERATORS - coverage)}")
    return {
        "status": "passed",
        "candidate_count": len(candidates),
        "feature_count": feature_count,
        "operator_coverage": tuple(sorted(coverage)),
        "family_coverage": tuple(sorted(families)),
        "declaration_sha256": brep_declaration_sha256(value),
    }


def canonical_brep_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def brep_declaration_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_brep_bytes(value)).hexdigest()
