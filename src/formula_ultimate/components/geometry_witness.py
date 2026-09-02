"""Fail-closed comparison for Work 081 FreeCAD geometry witnesses."""

from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any, Mapping, Sequence


WITNESS_VERSION = "step_freecad_geometry_witness_v2"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ID = re.compile(r"^[a-z][a-z0-9_.-]*$")


class GeometryWitnessViolation(ValueError):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")


def _fail(code: str, message: str) -> None:
    raise GeometryWitnessViolation(code, message)


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
        _fail("schema_error", f"{context} keys mismatch; missing={sorted(missing)}, unknown={sorted(unknown)}")


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


def _identifier(value: Any, context: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        _fail("schema_error", f"{context} must be a lower-case identifier")
    return value


def _sha(value: Any, context: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        _fail("invalid_hash", f"{context} must be a lower-case SHA-256")
    return value


def _vec(value: Any, context: str) -> tuple[float, float, float]:
    items = _sequence(value, context)
    if len(items) != 3:
        _fail("schema_error", f"{context} must contain three values")
    return tuple(_number(item, context) for item in items)  # type: ignore[return-value]


def _pair(value: Any, context: str) -> tuple[float, float]:
    items = _sequence(value, context)
    if len(items) != 2:
        _fail("schema_error", f"{context} must contain two values")
    result = (_number(items[0], context), _number(items[1], context))
    if result[0] >= result[1]:
        _fail("invalid_bounds", f"{context} must increase")
    return result


def _norm(value: Sequence[float]) -> float:
    return math.sqrt(math.fsum(item * item for item in value))


def _unit(value: Sequence[float], context: str) -> tuple[float, float, float]:
    length = _norm(value)
    if length <= 1e-15:
        _fail("invalid_axis", f"{context} has zero length")
    return tuple(item / length for item in value)  # type: ignore[return-value]


def canonical_bytes(value: Mapping[str, Any]) -> bytes:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        _fail("canonicalization_error", str(exc))


def canonical_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def validate_witness_config(raw_value: Mapping[str, Any]) -> dict[str, Any]:
    raw = _mapping(raw_value, "witness config")
    _exact(raw, {"witness_version", "source_manifest_sha256", "tolerances", "parts", "claim_boundary"}, "witness config")
    if raw["witness_version"] != WITNESS_VERSION:
        _fail("version_mismatch", "witness_version mismatch")
    _sha(raw["source_manifest_sha256"], "source_manifest_sha256")
    tolerances = _mapping(raw["tolerances"], "tolerances")
    _exact(tolerances, {"relative", "length_absolute_m", "axis_angle_rad"}, "tolerances")
    tolerance_values = {name: _positive(value, f"tolerances.{name}") for name, value in tolerances.items()}

    part_ids: set[str] = set()
    parts = []
    for index, raw_part in enumerate(_sequence(raw["parts"], "parts")):
        part = _mapping(raw_part, f"parts[{index}]")
        _exact(part, {"part_id", "step_file", "step_sha256", "material_density_kg_per_m3", "expected", "interfaces", "unsupported_measurements"}, f"parts[{index}]")
        part_id = _identifier(part["part_id"], "part_id")
        if part_id in part_ids:
            _fail("duplicate_part", f"duplicate part_id {part_id}")
        part_ids.add(part_id)
        if not isinstance(part["step_file"], str) or part["step_file"] != f"{part_id}.step":
            _fail("schema_error", f"part {part_id} step_file must be {part_id}.step")
        _sha(part["step_sha256"], f"{part_id}.step_sha256")
        density = _positive(part["material_density_kg_per_m3"], "material density")
        expected = _mapping(part["expected"], f"{part_id}.expected")
        _exact(expected, {"solid_count", "volume_m3", "bounding_box_m"}, f"{part_id}.expected")
        if expected["solid_count"] != 1:
            _fail("invalid_topology_expectation", "V2 expects exactly one solid")
        volume = _positive(expected["volume_m3"], "expected volume_m3")
        bounds = _mapping(expected["bounding_box_m"], "expected bounding_box_m")
        _exact(bounds, {"minimum", "maximum"}, "expected bounding_box_m")
        minimum = _vec(bounds["minimum"], "expected minimum")
        maximum = _vec(bounds["maximum"], "expected maximum")
        if any(low >= high for low, high in zip(minimum, maximum)):
            _fail("invalid_bounds", f"part {part_id} bounds must increase")
        interfaces = []
        interface_ids: set[str] = set()
        for interface_index, raw_interface in enumerate(_sequence(part["interfaces"], f"{part_id}.interfaces")):
            interface = _mapping(raw_interface, f"{part_id}.interfaces[{interface_index}]")
            _exact(interface, {"interface_id", "geometry_type", "radius_m", "axis", "axis_offset_point_m", "axial_bounds_m", "radius_tolerance_m", "position_tolerance_m", "axial_tolerance_m"}, "interface")
            interface_id = _identifier(interface["interface_id"], "interface_id")
            if interface_id in interface_ids:
                _fail("duplicate_interface", f"duplicate interface {interface_id}")
            interface_ids.add(interface_id)
            if interface["geometry_type"] != "cylindrical_surface":
                _fail("unsupported_interface_signature", "V2 supports cylindrical_surface signatures")
            interfaces.append({
                "interface_id": interface_id,
                "geometry_type": interface["geometry_type"],
                "radius_m": _positive(interface["radius_m"], "interface radius_m"),
                "axis": _unit(_vec(interface["axis"], "interface axis"), "interface axis"),
                "axis_offset_point_m": _vec(interface["axis_offset_point_m"], "axis_offset_point_m"),
                "axial_bounds_m": _pair(interface["axial_bounds_m"], "axial_bounds_m"),
                "radius_tolerance_m": _positive(interface["radius_tolerance_m"], "radius_tolerance_m"),
                "position_tolerance_m": _positive(interface["position_tolerance_m"], "position_tolerance_m"),
                "axial_tolerance_m": _positive(interface["axial_tolerance_m"], "axial_tolerance_m"),
            })
        if not interfaces:
            _fail("missing_interface", f"part {part_id} needs a semantic interface")
        unsupported = tuple(_sequence(part["unsupported_measurements"], "unsupported_measurements"))
        if not unsupported or any(not isinstance(item, str) or not item for item in unsupported):
            _fail("missing_limitation", "unsupported_measurements must be explicit")
        parts.append({
            "part_id": part_id,
            "step_file": part["step_file"],
            "step_sha256": part["step_sha256"],
            "material_density_kg_per_m3": density,
            "expected": {"solid_count": 1, "volume_m3": volume, "bounding_box_m": {"minimum": minimum, "maximum": maximum}},
            "interfaces": interfaces,
            "unsupported_measurements": unsupported,
        })
    if len(parts) != 5:
        _fail("missing_part", "V2 reference must cover exactly five Work 078 parts")

    claim = _mapping(raw["claim_boundary"], "claim_boundary")
    _exact(claim, {"evidence_class", "admitted_claims", "prohibited_claims"}, "claim_boundary")
    if claim["evidence_class"] != "toolchain_cross_check":
        _fail("claim_boundary_mismatch", "evidence class must be toolchain_cross_check")
    admitted = set(_sequence(claim["admitted_claims"], "admitted_claims"))
    prohibited = set(_sequence(claim["prohibited_claims"], "prohibited_claims"))
    if not {"exact_step_identity", "freecad_geometry_measurement", "geometry_signature_recovery"} <= admitted:
        _fail("claim_boundary_mismatch", "required admitted claims are missing")
    if not {"physical_validation", "design_material_approved", "exact_arbitrary_wall_thickness", "manufacturability_proof"} <= prohibited:
        _fail("claim_boundary_mismatch", "required prohibited claims are missing")
    return {"status": "passed", "config_sha256": canonical_sha256(raw), "source_manifest_sha256": raw["source_manifest_sha256"], "tolerances": tolerance_values, "parts": parts}


def _axis_angle(a: Sequence[float], b: Sequence[float]) -> float:
    ua = _unit(a, "measured axis")
    ub = _unit(b, "expected axis")
    cosine = abs(math.fsum(x * y for x, y in zip(ua, ub)))
    return math.acos(max(-1.0, min(1.0, cosine)))


def compare_geometry_witness(config_raw: Mapping[str, Any], report_raw: Mapping[str, Any]) -> dict[str, Any]:
    config = validate_witness_config(config_raw)
    report = _mapping(report_raw, "FreeCAD report")
    _exact(report, {"witness_version", "source_manifest_sha256", "freecad_version", "occt_version", "import_mode", "hidden_geometry_repair", "parts", "report_sha256"}, "FreeCAD report")
    if report["witness_version"] != WITNESS_VERSION:
        _fail("version_mismatch", "report witness_version mismatch")
    if report["import_mode"] != "Part.Shape.read_step_no_repair" or report["hidden_geometry_repair"] is not False:
        _fail("hidden_geometry_repair", "report must use the declared no-repair import route")
    if report["source_manifest_sha256"] != config["source_manifest_sha256"]:
        _fail("source_manifest_mismatch", "report source manifest identity differs")
    report_body = {key: value for key, value in report.items() if key != "report_sha256"}
    if report["report_sha256"] != canonical_sha256(report_body):
        _fail("report_identity_mismatch", "FreeCAD report hash does not match its content")
    measured_parts = _sequence(report["parts"], "report.parts")
    by_id = {}
    for item in measured_parts:
        part = _mapping(item, "measured part")
        part_id = part.get("part_id")
        if part_id in by_id:
            _fail("duplicate_part", "report contains a duplicate part")
        by_id[part_id] = part
    if set(by_id) != {part["part_id"] for part in config["parts"]}:
        _fail("part_set_mismatch", "report part set differs from config")

    comparisons = []
    relative_tolerance = config["tolerances"]["relative"]
    absolute_length = config["tolerances"]["length_absolute_m"]
    for expected_part in config["parts"]:
        measured = by_id[expected_part["part_id"]]
        required = {"part_id", "step_file", "step_sha256", "step_bytes", "shape_type", "solid_count", "shell_count", "is_valid", "volume_m3", "bounding_box_m", "centre_of_mass_m", "geometric_inertia_tensor_m5", "material_density_kg_per_m3", "mass_kg", "mass_inertia_tensor_kg_m2", "principal_moments_kg_m2", "principal_axes", "cylindrical_surfaces", "unsupported_measurements", "hidden_geometry_repair"}
        _exact(measured, required, f"measured {expected_part['part_id']}")
        if measured["step_sha256"] != expected_part["step_sha256"]:
            _fail("step_hash_mismatch", f"{expected_part['part_id']} STEP hash mismatch")
        if measured["step_file"] != expected_part["step_file"]:
            _fail("step_file_mismatch", "STEP filename mismatch")
        if measured["solid_count"] != 1 or measured["is_valid"] is not True:
            _fail("invalid_imported_topology", f"{expected_part['part_id']} is not one valid solid")
        if measured["hidden_geometry_repair"] is not False:
            _fail("hidden_geometry_repair", f"{expected_part['part_id']} reports repair")
        if isinstance(measured["step_bytes"], bool) or not isinstance(measured["step_bytes"], int) or measured["step_bytes"] <= 0:
            _fail("invalid_imported_topology", "STEP byte count must be a positive integer")
        if isinstance(measured["shell_count"], bool) or not isinstance(measured["shell_count"], int) or measured["shell_count"] <= 0:
            _fail("invalid_imported_topology", "shell count must be a positive integer")
        volume = _positive(measured["volume_m3"], "measured volume_m3")
        volume_residual = abs(volume - expected_part["expected"]["volume_m3"]) / expected_part["expected"]["volume_m3"]
        if volume_residual > relative_tolerance:
            _fail("volume_mismatch", f"{expected_part['part_id']} volume residual exceeds tolerance")
        bounds = _mapping(measured["bounding_box_m"], "measured bounding_box_m")
        _exact(bounds, {"minimum", "maximum"}, "measured bounding_box_m")
        measured_min = _vec(bounds["minimum"], "measured bounds minimum")
        measured_max = _vec(bounds["maximum"], "measured bounds maximum")
        expected_min = expected_part["expected"]["bounding_box_m"]["minimum"]
        expected_max = expected_part["expected"]["bounding_box_m"]["maximum"]
        extent = max(high - low for low, high in zip(expected_min, expected_max))
        bound_error = max(abs(a - b) for a, b in zip(measured_min + measured_max, expected_min + expected_max))
        if bound_error > absolute_length + relative_tolerance * extent:
            _fail("bounding_box_mismatch", f"{expected_part['part_id']} bounding box exceeds tolerance")
        _vec(measured["centre_of_mass_m"], "centre_of_mass_m")
        mass = _positive(measured["mass_kg"], "mass_kg")
        density = _number(measured["material_density_kg_per_m3"], "material density")
        if density != expected_part["material_density_kg_per_m3"]:
            _fail("density_mismatch", "measured report material density differs")
        expected_mass = volume * density
        if abs(mass - expected_mass) / expected_mass > relative_tolerance:
            _fail("mass_mismatch", "mass does not equal measured volume times declared density")

        def tensor3(value: Any, context: str) -> list[list[float]]:
            rows = _sequence(value, context)
            if len(rows) != 3:
                _fail("schema_error", f"{context} must have three rows")
            result = []
            for row in rows:
                items = _sequence(row, context)
                if len(items) != 3:
                    _fail("schema_error", f"{context} rows must have three values")
                result.append([_number(item, context) for item in items])
            return result

        geometric_tensor = tensor3(measured["geometric_inertia_tensor_m5"], "geometric inertia tensor")
        mass_tensor = tensor3(measured["mass_inertia_tensor_kg_m2"], "mass inertia tensor")
        for row in range(3):
            if geometric_tensor[row][row] <= 0.0 or mass_tensor[row][row] <= 0.0:
                _fail("invalid_inertia", "inertia tensor diagonal must be positive")
            for column in range(3):
                if abs(geometric_tensor[row][column] - geometric_tensor[column][row]) > 1e-15:
                    _fail("invalid_inertia", "geometric inertia tensor must be symmetric")
                expected_mass_inertia = geometric_tensor[row][column] * density
                scale = max(abs(expected_mass_inertia), 1e-18)
                if abs(mass_tensor[row][column] - expected_mass_inertia) / scale > relative_tolerance:
                    _fail("inertia_density_mismatch", "mass inertia does not equal geometric inertia times density")
        principal = _sequence(measured["principal_moments_kg_m2"], "principal moments")
        if len(principal) != 3 or any(_positive(value, "principal moment") <= 0.0 for value in principal):
            _fail("invalid_inertia", "three positive principal moments are required")
        trace = math.fsum(mass_tensor[index][index] for index in range(3))
        if abs(math.fsum(float(value) for value in principal) - trace) / trace > relative_tolerance:
            _fail("principal_inertia_mismatch", "principal moments do not preserve tensor trace")
        axes = _sequence(measured["principal_axes"], "principal axes")
        if len(axes) != 3:
            _fail("invalid_inertia", "three principal axes are required")
        normalized_axes = [_unit(_vec(axis, "principal axis"), "principal axis") for axis in axes]
        if any(abs(math.fsum(normalized_axes[left][i] * normalized_axes[right][i] for i in range(3))) > 1e-9 for left, right in ((0, 1), (0, 2), (1, 2))):
            _fail("invalid_inertia", "principal axes must be orthogonal")
        if tuple(_sequence(measured["unsupported_measurements"], "unsupported_measurements")) != expected_part["unsupported_measurements"]:
            _fail("limitation_mismatch", "unsupported measurement list differs from config")
        surfaces = _sequence(measured["cylindrical_surfaces"], "cylindrical_surfaces")
        recovered = []
        for interface in expected_part["interfaces"]:
            matches = []
            for surface in surfaces:
                candidate = _mapping(surface, "cylindrical surface")
                _exact(candidate, {"geometry_type", "surface_class", "radius_m", "axis", "axis_offset_point_m", "axial_bounds_m", "area_m2", "surface_signature_sha256"}, "cylindrical surface")
                signature_body = {key: value for key, value in candidate.items() if key != "surface_signature_sha256"}
                if candidate["surface_signature_sha256"] != canonical_sha256(signature_body):
                    _fail("surface_identity_mismatch", "surface signature hash differs from measured content")
                _positive(candidate["area_m2"], "surface area_m2")
                radius_error = abs(_positive(candidate["radius_m"], "surface radius") - interface["radius_m"])
                position_error = _norm(tuple(a - b for a, b in zip(_vec(candidate["axis_offset_point_m"], "surface axis offset"), interface["axis_offset_point_m"])))
                angle_error = _axis_angle(_vec(candidate["axis"], "surface axis"), interface["axis"])
                measured_axial = _sequence(candidate["axial_bounds_m"], "surface axial bounds")
                if len(measured_axial) != 2:
                    _fail("schema_error", "surface axial bounds must contain two values")
                axial_error = max(abs(_number(measured_axial[index], "surface axial bound") - interface["axial_bounds_m"][index]) for index in range(2))
                if radius_error <= interface["radius_tolerance_m"] and position_error <= interface["position_tolerance_m"] and angle_error <= config["tolerances"]["axis_angle_rad"] and axial_error <= interface["axial_tolerance_m"]:
                    matches.append((candidate, radius_error, position_error, angle_error, axial_error))
            if len(matches) != 1:
                code = "missing_interface_signature" if not matches else "ambiguous_interface_signature"
                _fail(code, f"{expected_part['part_id']} interface {interface['interface_id']} matched {len(matches)} surfaces")
            candidate, radius_error, position_error, angle_error, axial_error = matches[0]
            recovered.append({"interface_id": interface["interface_id"], "surface_signature_sha256": candidate["surface_signature_sha256"], "radius_error_m": radius_error, "axis_position_error_m": position_error, "axis_angle_error_rad": angle_error, "axial_bounds_error_m": axial_error})
        comparisons.append({"part_id": expected_part["part_id"], "step_sha256": measured["step_sha256"], "volume_relative_residual": volume_residual, "maximum_bound_error_m": bound_error, "interfaces": recovered})
    body = {"status": "passed", "witness_version": WITNESS_VERSION, "config_sha256": config["config_sha256"], "source_manifest_sha256": config["source_manifest_sha256"], "freecad_report_sha256": report["report_sha256"], "part_count": len(comparisons), "comparisons": comparisons, "evidence_class": "toolchain_cross_check", "design_use_allowed": False, "hidden_geometry_repair": False}
    return {**body, "comparison_sha256": canonical_sha256(body)}


def symmetric_eigen_3x3(matrix: Sequence[Sequence[float]]) -> tuple[list[float], list[list[float]]]:
    """Deterministic Jacobi eigensolver for a finite symmetric 3x3 tensor."""
    a = [[_number(matrix[i][j], "matrix") for j in range(3)] for i in range(3)]
    vectors = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    for _ in range(64):
        p, q = max(((0, 1), (0, 2), (1, 2)), key=lambda pair: abs(a[pair[0]][pair[1]]))
        if abs(a[p][q]) <= 1e-18 * max(1.0, max(abs(a[i][i]) for i in range(3))):
            break
        angle = 0.5 * math.atan2(2.0 * a[p][q], a[q][q] - a[p][p])
        c, s = math.cos(angle), math.sin(angle)
        for row in range(3):
            ap, aq = a[row][p], a[row][q]
            a[row][p], a[row][q] = c * ap - s * aq, s * ap + c * aq
        for column in range(3):
            ap, aq = a[p][column], a[q][column]
            a[p][column], a[q][column] = c * ap - s * aq, s * ap + c * aq
        for row in range(3):
            vp, vq = vectors[row][p], vectors[row][q]
            vectors[row][p], vectors[row][q] = c * vp - s * vq, s * vp + c * vq
    order = sorted(range(3), key=lambda index: a[index][index])
    return [a[index][index] for index in order], [[vectors[row][index] for row in range(3)] for index in order]
