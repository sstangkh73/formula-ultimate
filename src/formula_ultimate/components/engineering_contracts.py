"""Evidence-bearing material and manufacturing contracts for Work 079."""

from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any, Mapping, Sequence


MATERIAL_CONTRACT_VERSION = "engineering_material_v1"
MANUFACTURING_CONTRACT_VERSION = "manufacturing_process_v1"
GEOMETRY_WITNESS_VERSION = "manufacturing_geometry_witness_v1"

MATERIAL_PROPERTIES = frozenset(
    {
        "density_kg_per_m3",
        "youngs_modulus_pa",
        "poisson_ratio",
        "shear_modulus_pa",
        "yield_strength_pa",
        "ultimate_strength_pa",
        "fracture_toughness_pa_sqrt_m",
        "thermal_conductivity_w_per_m_k",
        "specific_heat_capacity_j_per_kg_k",
        "thermal_expansion_per_k",
        "allowable_temperature_min_k",
        "allowable_temperature_max_k",
    }
)
PROCESS_LIMITS = frozenset(
    {
        "minimum_wall_thickness_m",
        "minimum_hole_diameter_m",
        "minimum_ligament_m",
        "minimum_web_thickness_m",
        "minimum_internal_radius_m",
        "minimum_bend_radius_m",
    }
)
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ID = re.compile(r"^[a-z][a-z0-9_.-]*$")


class EngineeringContractViolation(ValueError):
    """A stable coded rejection from a Work 079 contract."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")


def _fail(code: str, message: str) -> None:
    raise EngineeringContractViolation(code, message)


def _mapping(value: Any, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail("schema_error", f"{context} must be an object")
    return value


def _sequence(value: Any, context: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        _fail("schema_error", f"{context} must be an array")
    return value


def _exact(value: Mapping[str, Any], expected: set[str], context: str) -> None:
    missing = expected - set(value)
    unknown = set(value) - expected
    if missing or unknown:
        _fail(
            "schema_error",
            f"{context} keys mismatch; missing={sorted(missing)}, unknown={sorted(unknown)}",
        )


def _identifier(value: Any, context: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        _fail("schema_error", f"{context} must be a lower-case identifier")
    return value


def _text(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("schema_error", f"{context} must be non-empty text")
    return value


def _number(value: Any, context: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail("invalid_numeric_value", f"{context} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        _fail("invalid_numeric_value", f"{context} must be finite")
    return result


def _positive(value: Any, context: str) -> float:
    result = _number(value, context)
    if result <= 0.0:
        _fail("invalid_numeric_value", f"{context} must be > 0")
    return result


def _sha(value: Any, context: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        _fail("invalid_hash", f"{context} must be a lower-case SHA-256")
    return value


def _evidence_records(raw: Any) -> dict[str, Mapping[str, Any]]:
    records: dict[str, Mapping[str, Any]] = {}
    for index, raw_record in enumerate(_sequence(raw, "evidence_records")):
        record = _mapping(raw_record, f"evidence_records[{index}]")
        _exact(
            record,
            {"source_id", "citation", "source_sha256", "evidence_class", "confidence", "domain"},
            f"evidence_records[{index}]",
        )
        source_id = _identifier(record["source_id"], "source_id")
        if source_id in records:
            _fail("duplicate_evidence", "duplicate source_id")
        _text(record["citation"], "citation")
        _sha(record["source_sha256"], "source_sha256")
        if record["evidence_class"] not in {"synthetic", "coupon", "handbook", "standard", "test"}:
            _fail("unsupported_evidence", "unsupported evidence_class")
        confidence = _number(record["confidence"], "confidence")
        if not 0.0 <= confidence <= 1.0:
            _fail("invalid_confidence", "confidence must be in [0, 1]")
        domain = _mapping(record["domain"], "evidence domain")
        _exact(domain, {"temperature_min_k", "temperature_max_k", "material_condition", "process_condition"}, "evidence domain")
        low = _positive(domain["temperature_min_k"], "domain.temperature_min_k")
        high = _positive(domain["temperature_max_k"], "domain.temperature_max_k")
        if low >= high:
            _fail("invalid_evidence_domain", "evidence temperature domain must increase")
        _text(domain["material_condition"], "domain.material_condition")
        _text(domain["process_condition"], "domain.process_condition")
        records[source_id] = record
    if not records:
        _fail("missing_evidence", "at least one evidence record is required")
    return records


def canonical_record_bytes(value: Mapping[str, Any]) -> bytes:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        _fail("canonicalization_error", str(exc))


def record_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_record_bytes(value)).hexdigest()


def validate_material_record(raw: Mapping[str, Any]) -> dict[str, Any]:
    material = _mapping(raw, "material")
    _exact(
        material,
        {
            "contract_version",
            "material_id",
            "display_name",
            "evidence_status",
            "properties",
            "fatigue",
            "evidence_records",
            "property_sources",
            "validation_tolerances",
            "claim_boundary",
        },
        "material",
    )
    if material["contract_version"] != MATERIAL_CONTRACT_VERSION:
        _fail("version_mismatch", "material contract_version mismatch")
    _identifier(material["material_id"], "material_id")
    _text(material["display_name"], "display_name")
    if material["evidence_status"] not in {"synthetic", "sourced"}:
        _fail("unsupported_evidence", "material evidence_status is unsupported")

    properties = _mapping(material["properties"], "material properties")
    _exact(properties, set(MATERIAL_PROPERTIES), "material properties")
    positive_names = MATERIAL_PROPERTIES - {
        "poisson_ratio",
        "thermal_expansion_per_k",
    }
    values = {
        name: (_positive(value, name) if name in positive_names else _number(value, name))
        for name, value in properties.items()
    }
    if not -1.0 < values["poisson_ratio"] < 0.5:
        _fail("invalid_poisson_ratio", "poisson_ratio must be in (-1, 0.5)")
    if abs(values["thermal_expansion_per_k"]) > 0.01:
        _fail("invalid_thermal_property", "thermal expansion magnitude is unsupported")
    if values["yield_strength_pa"] > values["ultimate_strength_pa"]:
        _fail("invalid_strength_order", "yield strength exceeds ultimate strength")
    if values["allowable_temperature_min_k"] >= values["allowable_temperature_max_k"]:
        _fail("invalid_temperature_range", "allowable temperature range must increase")

    tolerances = _mapping(material["validation_tolerances"], "validation_tolerances")
    _exact(tolerances, {"elastic_consistency_relative"}, "validation_tolerances")
    elastic_tolerance = _positive(tolerances["elastic_consistency_relative"], "elastic consistency tolerance")
    if elastic_tolerance > 0.05:
        _fail("invalid_validation_tolerance", "elastic consistency tolerance must be <= 0.05")
    expected_shear = values["youngs_modulus_pa"] / (2.0 * (1.0 + values["poisson_ratio"]))
    elastic_residual = abs(values["shear_modulus_pa"] - expected_shear) / expected_shear
    if elastic_residual > elastic_tolerance:
        _fail("inconsistent_elastic_constants", "E, G, and poisson_ratio are inconsistent")

    evidence = _evidence_records(material["evidence_records"])
    sources = _mapping(material["property_sources"], "property_sources")
    _exact(sources, set(MATERIAL_PROPERTIES), "property_sources")
    if any(source_id not in evidence for source_id in sources.values()):
        _fail("missing_property_source", "property_sources references missing evidence")
    if material["evidence_status"] == "sourced" and any(
        evidence[source_id]["evidence_class"] == "synthetic" for source_id in sources.values()
    ):
        _fail("synthetic_design_material", "a sourced material cannot use synthetic property evidence")

    fatigue = _mapping(material["fatigue"], "fatigue")
    _exact(fatigue, {"evidence_status", "model", "points", "source_id"}, "fatigue")
    fatigue_status = fatigue["evidence_status"]
    if fatigue_status == "missing":
        if fatigue["model"] is not None or fatigue["source_id"] is not None or list(fatigue["points"]):
            _fail("unsupported_fatigue_claim", "missing fatigue evidence must not contain a model or curve")
    elif fatigue_status == "available":
        if fatigue["model"] != "sn_curve" or fatigue["source_id"] not in evidence:
            _fail("unsupported_fatigue_claim", "available fatigue requires an evidenced sn_curve")
        points = _sequence(fatigue["points"], "fatigue points")
        if len(points) < 2:
            _fail("unsupported_fatigue_claim", "sn_curve requires at least two points")
        previous_cycles = 0.0
        previous_stress = math.inf
        for index, raw_point in enumerate(points):
            point = _mapping(raw_point, f"fatigue.points[{index}]")
            _exact(point, {"cycles", "alternating_stress_pa"}, f"fatigue.points[{index}]")
            cycles = _positive(point["cycles"], "fatigue cycles")
            stress = _positive(point["alternating_stress_pa"], "fatigue alternating stress")
            if cycles <= previous_cycles or stress > previous_stress:
                _fail("invalid_fatigue_curve", "cycles must increase and alternating stress must not increase")
            previous_cycles, previous_stress = cycles, stress
    else:
        _fail("unsupported_fatigue_claim", "fatigue evidence_status is unsupported")

    claim = _mapping(material["claim_boundary"], "material claim_boundary")
    _exact(claim, {"design_use_allowed", "prohibited_claims"}, "material claim_boundary")
    expected_design_use = material["evidence_status"] == "sourced"
    if claim["design_use_allowed"] is not expected_design_use:
        _fail("claim_boundary_mismatch", "design_use_allowed disagrees with evidence_status")
    prohibited = set(_sequence(claim["prohibited_claims"], "prohibited_claims"))
    if not {"maximum_force_without_geometry", "physical_validation"} <= prohibited:
        _fail("claim_boundary_mismatch", "required prohibited material claims are missing")

    return {
        "status": "passed",
        "material_id": material["material_id"],
        "record_sha256": record_sha256(material),
        "elastic_consistency_relative_residual": elastic_residual,
        "fatigue_evidence_status": fatigue_status,
        "design_use_allowed": expected_design_use,
    }


def validate_manufacturing_process(raw: Mapping[str, Any]) -> dict[str, Any]:
    process = _mapping(raw, "manufacturing process")
    _exact(
        process,
        {
            "contract_version",
            "process_id",
            "process_type",
            "evidence_status",
            "limits",
            "tool_access",
            "tolerance_class",
            "unsupported_feature_policy",
            "evidence_records",
            "limit_sources",
            "claim_boundary",
        },
        "manufacturing process",
    )
    if process["contract_version"] != MANUFACTURING_CONTRACT_VERSION:
        _fail("version_mismatch", "manufacturing contract_version mismatch")
    _identifier(process["process_id"], "process_id")
    if process["process_type"] not in {"machining", "additive", "casting", "forming", "welding", "composite"}:
        _fail("unsupported_process", "process_type is unsupported")
    if process["evidence_status"] not in {"synthetic", "sourced"}:
        _fail("unsupported_evidence", "process evidence_status is unsupported")

    limits = _mapping(process["limits"], "manufacturing limits")
    _exact(limits, set(PROCESS_LIMITS), "manufacturing limits")
    for name, value in limits.items():
        _positive(value, name)

    access = _mapping(process["tool_access"], "tool_access")
    _exact(access, {"required_clearance_m", "maximum_depth_to_diameter_ratio", "allowed_directions"}, "tool_access")
    _positive(access["required_clearance_m"], "required_clearance_m")
    _positive(access["maximum_depth_to_diameter_ratio"], "maximum_depth_to_diameter_ratio")
    directions = tuple(_sequence(access["allowed_directions"], "allowed_directions"))
    if not directions or len(directions) != len(set(directions)) or any(item not in {"x", "y", "z", "-x", "-y", "-z"} for item in directions):
        _fail("invalid_tool_access", "allowed tool directions are invalid")

    tolerance = _mapping(process["tolerance_class"], "tolerance_class")
    _exact(tolerance, {"class_id", "minimum_achievable_tolerance_m"}, "tolerance_class")
    _identifier(tolerance["class_id"], "tolerance class_id")
    _positive(tolerance["minimum_achievable_tolerance_m"], "minimum_achievable_tolerance_m")
    if process["unsupported_feature_policy"] != "reject":
        _fail("unsupported_feature_policy", "unsupported features must be rejected")

    evidence = _evidence_records(process["evidence_records"])
    source_targets = set(PROCESS_LIMITS) | {
        "required_clearance_m",
        "maximum_depth_to_diameter_ratio",
        "minimum_achievable_tolerance_m",
    }
    sources = _mapping(process["limit_sources"], "limit_sources")
    _exact(sources, source_targets, "limit_sources")
    if any(source_id not in evidence for source_id in sources.values()):
        _fail("missing_limit_source", "limit_sources references missing evidence")
    if process["evidence_status"] == "sourced" and any(
        evidence[source_id]["evidence_class"] == "synthetic" for source_id in sources.values()
    ):
        _fail("synthetic_manufacturing_process", "a sourced process cannot use synthetic limits")

    claim = _mapping(process["claim_boundary"], "manufacturing claim_boundary")
    _exact(claim, {"production_use_allowed", "prohibited_claims"}, "manufacturing claim_boundary")
    expected_production_use = process["evidence_status"] == "sourced"
    if claim["production_use_allowed"] is not expected_production_use:
        _fail("claim_boundary_mismatch", "production_use_allowed disagrees with evidence_status")
    if "manufacturability_proof" not in set(_sequence(claim["prohibited_claims"], "prohibited_claims")):
        _fail("claim_boundary_mismatch", "manufacturability_proof must be prohibited")
    return {
        "status": "passed",
        "process_id": process["process_id"],
        "record_sha256": record_sha256(process),
        "production_use_allowed": expected_production_use,
    }


def evaluate_manufacturing_witness(
    process_raw: Mapping[str, Any], witness_raw: Mapping[str, Any]
) -> dict[str, Any]:
    process_result = validate_manufacturing_process(process_raw)
    process = process_raw
    witness = _mapping(witness_raw, "geometry witness")
    _exact(
        witness,
        {
            "witness_version",
            "part_id",
            "geometry_sha256",
            "measurement_evidence",
            "wall_thicknesses_m",
            "hole_diameters_m",
            "ligaments_m",
            "web_thicknesses_m",
            "internal_radii_m",
            "bend_radii_m",
            "tool_access_checks",
            "unsupported_features",
            "requested_tolerance_m",
        },
        "geometry witness",
    )
    if witness["witness_version"] != GEOMETRY_WITNESS_VERSION:
        _fail("version_mismatch", "geometry witness version mismatch")
    _identifier(witness["part_id"], "witness part_id")
    _sha(witness["geometry_sha256"], "geometry_sha256")
    measurement = _mapping(witness["measurement_evidence"], "measurement_evidence")
    _exact(
        measurement,
        {"evidence_status", "method", "report_sha256"},
        "measurement_evidence",
    )
    if measurement["evidence_status"] not in {"synthetic", "independently_measured"}:
        _fail("unsupported_measurement_evidence", "measurement evidence status is unsupported")
    _text(measurement["method"], "measurement method")
    _sha(measurement["report_sha256"], "measurement report_sha256")

    limits = process["limits"]
    arrays = {
        "wall": ("wall_thicknesses_m", "minimum_wall_thickness_m"),
        "hole": ("hole_diameters_m", "minimum_hole_diameter_m"),
        "ligament": ("ligaments_m", "minimum_ligament_m"),
        "web": ("web_thicknesses_m", "minimum_web_thickness_m"),
        "internal_radius": ("internal_radii_m", "minimum_internal_radius_m"),
        "bend_radius": ("bend_radii_m", "minimum_bend_radius_m"),
    }
    margins: dict[str, float] = {}
    failure_codes = {
        "wall": "wall_too_thin",
        "hole": "hole_too_small",
        "ligament": "ligament_too_small",
        "web": "web_too_thin",
        "internal_radius": "internal_radius_too_small",
        "bend_radius": "bend_radius_too_small",
    }
    for label, (witness_key, limit_key) in arrays.items():
        measurements = tuple(
            _positive(value, witness_key)
            for value in _sequence(witness[witness_key], witness_key)
        )
        if not measurements:
            _fail("missing_geometry_measurement", f"{witness_key} must not be empty")
        margin = min(measurements) - float(limits[limit_key])
        margins[f"{label}_margin_m"] = margin
        if margin < 0.0:
            _fail(failure_codes[label], f"{witness_key} violates {limit_key}")

    if list(_sequence(witness["unsupported_features"], "unsupported_features")):
        _fail("unsupported_feature", "geometry contains unsupported manufacturing features")

    access = process["tool_access"]
    access_margins: list[dict[str, float | str]] = []
    checks = _sequence(witness["tool_access_checks"], "tool_access_checks")
    if not checks:
        _fail("missing_tool_access", "tool_access_checks must not be empty")
    for index, raw_check in enumerate(checks):
        check = _mapping(raw_check, f"tool_access_checks[{index}]")
        _exact(check, {"direction", "clearance_m", "depth_m", "diameter_m"}, f"tool_access_checks[{index}]")
        if check["direction"] not in access["allowed_directions"]:
            _fail("tool_direction_blocked", "tool direction is not admitted")
        clearance = _positive(check["clearance_m"], "tool clearance_m")
        depth = _positive(check["depth_m"], "tool depth_m")
        diameter = _positive(check["diameter_m"], "tool diameter_m")
        clearance_margin = clearance - float(access["required_clearance_m"])
        ratio_margin = float(access["maximum_depth_to_diameter_ratio"]) - depth / diameter
        if clearance_margin < 0.0:
            _fail("tool_clearance_blocked", "tool clearance is below process limit")
        if ratio_margin < 0.0:
            _fail("tool_depth_ratio_exceeded", "tool depth-to-diameter ratio exceeds process limit")
        access_margins.append(
            {
                "direction": check["direction"],
                "clearance_margin_m": clearance_margin,
                "depth_to_diameter_ratio_margin": ratio_margin,
            }
        )

    requested_tolerance = _positive(witness["requested_tolerance_m"], "requested_tolerance_m")
    tolerance_margin = requested_tolerance - float(
        process["tolerance_class"]["minimum_achievable_tolerance_m"]
    )
    if tolerance_margin < 0.0:
        _fail("tolerance_too_tight", "requested tolerance is tighter than process evidence")
    margins["tolerance_margin_m"] = tolerance_margin
    draft = {
        "status": "passed",
        "part_id": witness["part_id"],
        "geometry_sha256": witness["geometry_sha256"],
        "measurement_evidence_status": measurement["evidence_status"],
        "measurement_report_sha256": measurement["report_sha256"],
        "process_record_sha256": process_result["record_sha256"],
        "margins": margins,
        "tool_access_margins": access_margins,
        "hidden_geometry_repair": False,
    }
    return {**draft, "report_sha256": record_sha256(draft)}


def validate_engineering_assignment(
    assignment_raw: Mapping[str, Any],
    material_raw: Mapping[str, Any],
    process_raw: Mapping[str, Any],
    witness_raw: Mapping[str, Any],
) -> dict[str, Any]:
    material = validate_material_record(material_raw)
    process = validate_manufacturing_process(process_raw)
    manufacturing = evaluate_manufacturing_witness(process_raw, witness_raw)
    assignment = _mapping(assignment_raw, "engineering assignment")
    _exact(
        assignment,
        {
            "part_id",
            "geometry_sha256",
            "material_id",
            "material_record_sha256",
            "process_id",
            "process_record_sha256",
            "claim_boundary",
        },
        "engineering assignment",
    )
    comparisons = {
        "part_id": (assignment["part_id"], witness_raw["part_id"]),
        "geometry_sha256": (assignment["geometry_sha256"], witness_raw["geometry_sha256"]),
        "material_id": (assignment["material_id"], material["material_id"]),
        "material_record_sha256": (assignment["material_record_sha256"], material["record_sha256"]),
        "process_id": (assignment["process_id"], process["process_id"]),
        "process_record_sha256": (assignment["process_record_sha256"], process["record_sha256"]),
    }
    for name, (declared, actual) in comparisons.items():
        if declared != actual:
            _fail("assignment_identity_mismatch", f"{name} differs from validated evidence")
    claim = _mapping(assignment["claim_boundary"], "assignment claim_boundary")
    _exact(claim, {"admitted_claims", "prohibited_claims"}, "assignment claim_boundary")
    if "contract_bound" not in set(_sequence(claim["admitted_claims"], "admitted_claims")):
        _fail("claim_boundary_mismatch", "contract_bound claim is required")
    if not {"physical_validation", "design_material_approved"} <= set(
        _sequence(claim["prohibited_claims"], "prohibited_claims")
    ):
        _fail("claim_boundary_mismatch", "assignment prohibited claims are incomplete")
    draft = {
        "status": "passed",
        "part_id": assignment["part_id"],
        "geometry_sha256": assignment["geometry_sha256"],
        "material": material,
        "manufacturing_process": process,
        "manufacturing_witness": manufacturing,
        "assignment_sha256": record_sha256(assignment),
        "design_use_allowed": (
            material["design_use_allowed"]
            and process["production_use_allowed"]
            and manufacturing["measurement_evidence_status"] == "independently_measured"
        ),
    }
    return {**draft, "result_sha256": record_sha256(draft)}
