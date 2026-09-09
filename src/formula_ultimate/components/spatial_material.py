"""Validated spatial material ownership and mass-property utilities for Work 108."""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping, Sequence


CONTRACT_VERSION = "spatial_material_v1"


class SpatialMaterialViolation(ValueError):
    """Raised when spatial material evidence is incomplete or inconsistent."""


def canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise SpatialMaterialViolation("evidence must be finite canonical JSON") from exc


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise SpatialMaterialViolation(f"{label} must be an object")
    return value


def _sequence(value: Any, label: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise SpatialMaterialViolation(f"{label} must be an array")
    return value


def _exact(value: Mapping[str, Any], fields: set[str], label: str) -> None:
    if set(value) != fields:
        raise SpatialMaterialViolation(f"{label} schema mismatch")


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SpatialMaterialViolation(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise SpatialMaterialViolation(f"{label} must be finite")
    return result


def _positive(value: Any, label: str) -> float:
    result = _number(value, label)
    if result <= 0.0:
        raise SpatialMaterialViolation(f"{label} must be positive")
    return result


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or any(
        not (character.islower() or character.isdigit() or character in "_-.")
        for character in value
    ):
        raise SpatialMaterialViolation(f"{label} must be a lower-case identifier")
    return value


def _sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(
        character not in "0123456789abcdef" for character in value
    ):
        raise SpatialMaterialViolation(f"{label} must be a lower-case SHA-256")
    return value


def _vector3(value: Any, label: str, maximum: float | None = None) -> tuple[float, float, float]:
    values = _sequence(value, label)
    if len(values) != 3:
        raise SpatialMaterialViolation(f"{label} must have three components")
    vector = tuple(_number(item, label) for item in values)
    if maximum is not None and max(abs(item) for item in vector) > maximum:
        raise SpatialMaterialViolation(f"{label} exceeds its bound")
    return vector  # type: ignore[return-value]


def validate_declaration(value: Mapping[str, Any]) -> dict[str, Any]:
    root = _mapping(value, "declaration")
    _exact(
        root,
        {
            "contract_version",
            "units",
            "source",
            "limits",
            "tolerances",
            "materials",
            "cases",
            "experiment",
        },
        "declaration",
    )
    if root["contract_version"] != CONTRACT_VERSION or root["units"] != "SI_m_kg_s_rad":
        raise SpatialMaterialViolation("contract identity or SI units mismatch")

    source = _mapping(root["source"], "source")
    _exact(
        source,
        {
            "solid_config",
            "wire_config",
            "solid_declaration_sha256",
            "wire_declaration_sha256",
        },
        "source",
    )
    for path_field in ("solid_config", "wire_config"):
        if not isinstance(source[path_field], str) or not source[path_field]:
            raise SpatialMaterialViolation(f"{path_field} must be a repository path")
    _sha256(source["solid_declaration_sha256"], "solid declaration identity")
    _sha256(source["wire_declaration_sha256"], "wire declaration identity")

    limits = _mapping(root["limits"], "limits")
    _exact(limits, {"maximum_coordinate_m", "maximum_cases", "maximum_regions_per_case"}, "limits")
    coordinate_bound = _positive(limits["maximum_coordinate_m"], "maximum coordinate")
    maximum_cases = limits["maximum_cases"]
    maximum_regions = limits["maximum_regions_per_case"]
    if (
        isinstance(maximum_cases, bool)
        or not isinstance(maximum_cases, int)
        or not 1 <= maximum_cases <= 64
        or isinstance(maximum_regions, bool)
        or not isinstance(maximum_regions, int)
        or not 1 <= maximum_regions <= 64
    ):
        raise SpatialMaterialViolation("case or region limits are invalid")

    tolerances = _mapping(root["tolerances"], "tolerances")
    _exact(
        tolerances,
        {
            "volume_relative",
            "mass_relative",
            "centre_absolute_m",
            "inertia_relative",
            "overlap_volume_m3",
            "cavity_closure_relative",
        },
        "tolerances",
    )
    for name, tolerance in tolerances.items():
        numeric = _positive(tolerance, name)
        if numeric >= (coordinate_bound if name == "centre_absolute_m" else 0.01):
            raise SpatialMaterialViolation(f"{name} is too permissive")

    materials = _mapping(root["materials"], "materials")
    if not materials:
        raise SpatialMaterialViolation("at least one material is required")
    for material_id, raw_material in materials.items():
        _identifier(material_id, "material_id")
        material = _mapping(raw_material, f"material {material_id}")
        _exact(material, {"density_kg_m3", "provenance", "validity"}, f"material {material_id}")
        _positive(material["density_kg_m3"], f"{material_id} density")
        if material["provenance"] not in {"synthetic_fixture", "measured"}:
            raise SpatialMaterialViolation("material provenance is unsupported")
        if not isinstance(material["validity"], str) or not material["validity"]:
            raise SpatialMaterialViolation("material validity must be disclosed")

    cases = _sequence(root["cases"], "cases")
    if not 3 <= len(cases) <= maximum_cases:
        raise SpatialMaterialViolation("curved, hollow, and multi-body cases are required")
    case_ids: set[str] = set()
    families: set[str] = set()
    for case_index, raw_case in enumerate(cases):
        case = _mapping(raw_case, f"cases[{case_index}]")
        _exact(
            case,
            {
                "case_id",
                "source_candidate_id",
                "family",
                "source_step_sha256",
                "expected_body_count",
                "material_regions",
                "void_regions",
                "placement",
            },
            "case",
        )
        case_id = _identifier(case["case_id"], "case_id")
        if case_id in case_ids:
            raise SpatialMaterialViolation("duplicate case identity")
        case_ids.add(case_id)
        _identifier(case["source_candidate_id"], "source candidate")
        families.add(_identifier(case["family"], "family"))
        _sha256(case["source_step_sha256"], "source STEP identity")
        body_count = case["expected_body_count"]
        if isinstance(body_count, bool) or not isinstance(body_count, int) or not 1 <= body_count <= 32:
            raise SpatialMaterialViolation("expected body count is invalid")

        regions = _sequence(case["material_regions"], "material regions")
        if not 1 <= len(regions) <= maximum_regions:
            raise SpatialMaterialViolation("material region count is invalid")
        region_ids: set[str] = set()
        owned: list[int] = []
        for raw_region in regions:
            region = _mapping(raw_region, "material region")
            _exact(region, {"region_id", "material_id", "body_indices"}, "material region")
            region_id = _identifier(region["region_id"], "region_id")
            if region_id in region_ids:
                raise SpatialMaterialViolation("duplicate material region identity")
            region_ids.add(region_id)
            if region["material_id"] not in materials:
                raise SpatialMaterialViolation("material region references an unknown material")
            indices = _sequence(region["body_indices"], "body indices")
            if not indices:
                raise SpatialMaterialViolation("a material region must own at least one body")
            for body_index in indices:
                if isinstance(body_index, bool) or not isinstance(body_index, int) or not 0 <= body_index < body_count:
                    raise SpatialMaterialViolation("body ownership index is invalid")
                owned.append(body_index)
        if len(owned) != len(set(owned)):
            raise SpatialMaterialViolation("duplicate body ownership")
        if sorted(owned) != list(range(body_count)):
            raise SpatialMaterialViolation("every occupied body must have exactly one owner")

        void_ids: set[str] = set()
        for raw_void in _sequence(case["void_regions"], "void regions"):
            void = _mapping(raw_void, "void region")
            _exact(
                void,
                {"region_id", "operation", "outer_feature_id", "cavity_feature_id", "occupied_feature_id"},
                "void region",
            )
            void_id = _identifier(void["region_id"], "void region_id")
            if void_id in void_ids or void_id in region_ids:
                raise SpatialMaterialViolation("void identity overlaps another region")
            void_ids.add(void_id)
            if void["operation"] != "boolean_subtract":
                raise SpatialMaterialViolation("only explicit subtractive void evidence is admitted")
            for field in ("outer_feature_id", "cavity_feature_id", "occupied_feature_id"):
                _identifier(void[field], field)

        placement = _mapping(case["placement"], "placement")
        _exact(placement, {"translation_m", "rotation_axis", "rotation_rad"}, "placement")
        _vector3(placement["translation_m"], "placement translation", coordinate_bound)
        axis = _vector3(placement["rotation_axis"], "placement rotation axis")
        axis_norm = math.sqrt(sum(item * item for item in axis))
        if abs(axis_norm - 1.0) > 1e-12:
            raise SpatialMaterialViolation("placement rotation axis must be unit length")
        angle = _number(placement["rotation_rad"], "placement rotation")
        if abs(angle) > 2.0 * math.pi:
            raise SpatialMaterialViolation("placement rotation is outside bounds")

    if not {"curved", "hollow", "multi_body"}.issubset(families):
        raise SpatialMaterialViolation("required spatial family coverage is incomplete")

    experiment = _mapping(root["experiment"], "experiment")
    _exact(
        experiment,
        {"independent_variables", "dependent_variables", "controls", "failure_criteria"},
        "experiment",
    )
    for field in experiment:
        values = _sequence(experiment[field], f"experiment {field}")
        if not values or any(not isinstance(item, str) or not item for item in values):
            raise SpatialMaterialViolation(f"experiment {field} must be explicit")

    return {
        "status": "passed",
        "case_count": len(cases),
        "material_count": len(materials),
        "family_coverage": sorted(families),
        "declaration_sha256": canonical_sha256(root),
    }


def combine_mass_properties(regions: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Combine central region inertias into system properties in one world frame."""
    if not regions:
        raise SpatialMaterialViolation("at least one measured material region is required")
    masses: list[float] = []
    centers: list[tuple[float, float, float]] = []
    inertias: list[list[list[float]]] = []
    volumes: list[float] = []
    for index, raw_region in enumerate(regions):
        region = _mapping(raw_region, f"measured region {index}")
        _exact(region, {"volume_m3", "density_kg_m3", "centre_m", "centroidal_inertia_per_density_m5"}, "measured region")
        volume = _positive(region["volume_m3"], "region volume")
        density = _positive(region["density_kg_m3"], "region density")
        center = _vector3(region["centre_m"], "region centre")
        rows = _sequence(region["centroidal_inertia_per_density_m5"], "region inertia")
        if len(rows) != 3:
            raise SpatialMaterialViolation("region inertia must be 3x3")
        matrix: list[list[float]] = []
        for row in rows:
            values = _sequence(row, "region inertia row")
            if len(values) != 3:
                raise SpatialMaterialViolation("region inertia must be 3x3")
            matrix.append([_number(item, "region inertia") * density for item in values])
        for i in range(3):
            if matrix[i][i] <= 0.0:
                raise SpatialMaterialViolation("region inertia diagonal must be positive")
            for j in range(3):
                if abs(matrix[i][j] - matrix[j][i]) > 1e-10 * max(1.0, abs(matrix[i][j]), abs(matrix[j][i])):
                    raise SpatialMaterialViolation("region inertia must be symmetric")
        volumes.append(volume)
        masses.append(volume * density)
        centers.append(center)
        inertias.append(matrix)

    total_mass = sum(masses)
    center = tuple(sum(mass * point[axis] for mass, point in zip(masses, centers)) / total_mass for axis in range(3))
    total_inertia = [[0.0 for _ in range(3)] for _ in range(3)]
    for mass, point, inertia in zip(masses, centers, inertias):
        displacement = [point[axis] - center[axis] for axis in range(3)]
        squared = sum(item * item for item in displacement)
        for i in range(3):
            for j in range(3):
                parallel = mass * ((squared if i == j else 0.0) - displacement[i] * displacement[j])
                total_inertia[i][j] += inertia[i][j] + parallel
    return {
        "volume_m3": sum(volumes),
        "mass_kg": total_mass,
        "centre_of_mass_m": list(center),
        "centroidal_inertia_kg_m2": total_inertia,
    }


def relative_error(reference: float, measured: float) -> float:
    return abs(measured - reference) / max(abs(reference), 1e-30)


def maximum_matrix_relative_error(reference: Sequence[Sequence[float]], measured: Sequence[Sequence[float]]) -> float:
    errors = []
    for reference_row, measured_row in zip(reference, measured):
        for expected, actual in zip(reference_row, measured_row):
            scale = max(abs(float(expected)), abs(float(actual)))
            if scale > 1e-18:
                errors.append(abs(float(actual) - float(expected)) / scale)
            else:
                errors.append(abs(float(actual) - float(expected)))
    return max(errors, default=0.0)


def dependent_evidence_identity(
    source_step_sha256: str,
    material_regions: Sequence[Mapping[str, Any]],
    placement: Mapping[str, Any],
    void_regions: Sequence[Mapping[str, Any]],
) -> str:
    _sha256(source_step_sha256, "source STEP identity")
    return canonical_sha256(
        {
            "source_step_sha256": source_step_sha256,
            "material_regions": material_regions,
            "placement": placement,
            "void_regions": void_regions,
        }
    )
