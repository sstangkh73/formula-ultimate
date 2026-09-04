"""Validation and order-invariant comparison for Work 096 semantic witnesses."""
from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any, Mapping, Sequence

from .geometry_witness import symmetric_eigen_3x3


WITNESS_VERSION = "semantic_geometry_witness_v3"
REGION_INTENTS = ("support", "load", "contact", "thermal", "fluid")
REGION_SELECTORS = ("extreme_min_centroid", "extreme_max_centroid", "largest_area", "all_faces", "curved_faces_or_all")
_SHA = re.compile(r"^[0-9a-f]{64}$")
_ID = re.compile(r"^[a-z][a-z0-9_.-]*$")


class SemanticWitnessViolation(ValueError):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")


def _fail(code: str, message: str) -> None:
    raise SemanticWitnessViolation(code, message)


def canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as error:
        _fail("canonicalization_error", str(error))


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping): _fail("schema_error", f"{label} must be an object")
    return value


def _sequence(value: Any, label: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence): _fail("schema_error", f"{label} must be an array")
    return value


def _exact(value: Mapping[str, Any], fields: set[str], label: str) -> None:
    if set(value) != fields: _fail("schema_error", f"{label} schema mismatch")


def _id(value: Any, label: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value): _fail("schema_error", f"{label} must be a lower-case identifier")
    return value


def _sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or not _SHA.fullmatch(value): _fail("invalid_hash", f"{label} must be SHA-256")
    return value


def _number(value: Any, label: str, *, minimum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value): _fail("invalid_numeric_value", f"{label} must be finite")
    result = float(value)
    if minimum is not None and result < minimum: _fail("invalid_numeric_value", f"{label} is below {minimum}")
    return result


def _vec(value: Any, label: str) -> list[float]:
    items = _sequence(value, label)
    if len(items) != 3: _fail("schema_error", f"{label} must contain three values")
    return [_number(item, label) for item in items]


def _bounds(value: Any, label: str) -> dict[str, list[float]]:
    raw = _mapping(value, label); _exact(raw, {"minimum", "maximum"}, label)
    minimum, maximum = _vec(raw["minimum"], label), _vec(raw["maximum"], label)
    if any(a > b for a, b in zip(minimum, maximum)): _fail("invalid_bounds", label)
    return {"minimum": minimum, "maximum": maximum}


def _norm(value: Sequence[float]) -> float:
    return math.sqrt(math.fsum(item * item for item in value))


def derive_datums(bounds: Mapping[str, Sequence[float]], declarations: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    minimum, maximum = bounds["minimum"], bounds["maximum"]
    center = [(a + b) / 2 for a, b in zip(minimum, maximum)]; spans = [b - a for a, b in zip(minimum, maximum)]
    longest = max(range(3), key=lambda index: (spans[index], -index)); result = []
    for datum in declarations:
        if datum["kind"] == "bbox_center": body = {"point_m": center}
        elif datum["kind"] == "longest_bbox_axis":
            direction = [0.0, 0.0, 0.0]; direction[longest] = 1.0; body = {"origin_m": center, "direction": direction}
        elif datum["kind"] == "extreme_plane":
            axis = {"x": 0, "y": 1, "z": 2}[datum["parameters"]["axis"]]; side = datum["parameters"]["side"]
            origin = list(center); origin[axis] = minimum[axis] if side == "min" else maximum[axis]
            normal = [0.0, 0.0, 0.0]; normal[axis] = -1.0 if side == "min" else 1.0; body = {"origin_m": origin, "normal": normal}
        else: _fail("unsupported_datum", f"unsupported datum kind {datum['kind']}")
        signature_body = {"datum_id": datum["datum_id"], "kind": datum["kind"], **body}
        result.append({**signature_body, "datum_signature_sha256": canonical_sha256(signature_body)})
    return result


def select_face_signatures(faces: Sequence[Mapping[str, Any]], selector: str, path_axis: int, tie_relative: float) -> list[str]:
    if not faces: _fail("missing_face", "face catalog is empty")
    if selector == "all_faces": selected = list(faces)
    elif selector == "curved_faces_or_all":
        selected = [face for face in faces if face["surface_class"] != "Plane"] or list(faces)
    elif selector == "largest_area":
        extreme = max(float(face["area_m2"]) for face in faces)
        selected = [face for face in faces if abs(float(face["area_m2"]) - extreme) <= max(1e-18, abs(extreme) * tie_relative)]
    else:
        values = [float(face["center_m"][path_axis]) for face in faces]
        extreme = min(values) if selector == "extreme_min_centroid" else max(values)
        scale = max(1e-12, max(values) - min(values))
        selected = [face for face in faces if abs(float(face["center_m"][path_axis]) - extreme) <= scale * tie_relative + 1e-12]
    return sorted(str(face["face_signature_sha256"]) for face in selected)


def validate_config(config_raw: Mapping[str, Any], manifest_raw: Mapping[str, Any] | None = None) -> dict[str, Any]:
    config = _mapping(config_raw, "config")
    _exact(config, {"witness_version", "source_manifest_sha256", "material_density_kg_per_m3", "tolerances", "sampling_protocol", "semantic_regions", "candidate_bindings", "claim_boundary"}, "config")
    if config["witness_version"] != WITNESS_VERSION: _fail("version_mismatch", "witness version mismatch")
    _sha(config["source_manifest_sha256"], "source manifest"); density = _number(config["material_density_kg_per_m3"], "density", minimum=1e-12)
    tolerances = _mapping(config["tolerances"], "tolerances")
    _exact(tolerances, {"relative", "length_absolute_m", "axis_orthogonality", "curvature_zero_per_m", "region_tie_relative"}, "tolerances")
    tolerance_values = {key: _number(value, key, minimum=0.0) for key, value in tolerances.items()}
    sampling = _mapping(config["sampling_protocol"], "sampling protocol")
    _exact(sampling, {"curvature_parameter_fractions", "thickness_grid_fractions", "section_path_fractions", "section_slab_fraction", "oriented_bounds_tessellation_m", "swept_motion_model"}, "sampling protocol")
    for key in ("curvature_parameter_fractions", "thickness_grid_fractions", "section_path_fractions"):
        values = [_number(item, key) for item in _sequence(sampling[key], key)]
        if not values or values != sorted(set(values)) or any(not 0 < item < 1 for item in values): _fail("invalid_sampling_protocol", key)
    _number(sampling["section_slab_fraction"], "section slab", minimum=1e-9); _number(sampling["oriented_bounds_tessellation_m"], "tessellation", minimum=1e-9)
    if sampling["swept_motion_model"] != "static_identity_only": _fail("invalid_sampling_protocol", "unsupported sweep model")
    regions = _sequence(config["semantic_regions"], "semantic regions")
    if len(regions) != 5: _fail("missing_region", "five semantic regions are required")
    intents = set(); region_ids = set()
    for region in regions:
        item = _mapping(region, "region"); _exact(item, {"region_id", "intent", "selector"}, "region")
        region_id = _id(item["region_id"], "region id")
        if region_id in region_ids or item["intent"] in intents or item["intent"] not in REGION_INTENTS or item["selector"] not in REGION_SELECTORS: _fail("invalid_region", "region declarations must be unique and supported")
        region_ids.add(region_id); intents.add(item["intent"])
    if intents != set(REGION_INTENTS): _fail("missing_region", "required intent set differs")
    bindings = _sequence(config["candidate_bindings"], "candidate bindings")
    if len(bindings) != 10: _fail("missing_candidate", "all ten Work 092 candidates are required")
    candidate_ids = set(); hashes = set()
    for binding in bindings:
        item = _mapping(binding, "candidate binding"); _exact(item, {"candidate_id", "family", "step_sha256", "expected_solid_count", "path_datum_id", "datums"}, "candidate binding")
        candidate_id = _id(item["candidate_id"], "candidate id"); _id(item["family"], "family"); step_hash = _sha(item["step_sha256"], "STEP hash")
        if candidate_id in candidate_ids or step_hash in hashes: _fail("duplicate_candidate", candidate_id)
        candidate_ids.add(candidate_id); hashes.add(step_hash)
        count = item["expected_solid_count"]
        if isinstance(count, bool) or not isinstance(count, int) or count < 1: _fail("invalid_topology_expectation", candidate_id)
        datum_ids = set()
        for datum in _sequence(item["datums"], "datums"):
            raw = _mapping(datum, "datum"); _exact(raw, {"datum_id", "kind", "parameters"}, "datum")
            datum_id = _id(raw["datum_id"], "datum id")
            if datum_id in datum_ids or raw["kind"] not in {"bbox_center", "longest_bbox_axis", "extreme_plane"}: _fail("invalid_datum", datum_id)
            datum_ids.add(datum_id)
            params = _mapping(raw["parameters"], "datum parameters")
            if raw["kind"] == "extreme_plane":
                _exact(params, {"axis", "side"}, "extreme plane parameters")
                if params["axis"] not in {"x", "y", "z"} or params["side"] not in {"min", "max"}: _fail("invalid_datum", datum_id)
            elif params: _fail("invalid_datum", "non-extreme datum parameters must be empty")
        if item["path_datum_id"] not in datum_ids: _fail("missing_datum", "path datum is missing")
    claim = _mapping(config["claim_boundary"], "claim boundary"); _exact(claim, {"admitted_claims", "prohibited_claims"}, "claim boundary")
    prohibited = set(_sequence(claim["prohibited_claims"], "prohibited claims"))
    if not {"global_minimum_thickness", "assembly_clearance", "structural_validity", "manufacturability_proof", "physical_validation"}.issubset(prohibited): _fail("claim_boundary_mismatch", "required prohibitions are missing")
    if manifest_raw is not None:
        manifest = _mapping(manifest_raw, "source manifest")
        if manifest.get("manifest_sha256") != config["source_manifest_sha256"] or manifest.get("hidden_geometry_repair") is not False: _fail("source_manifest_mismatch", "manifest identity or repair state differs")
        source = {item["candidate_id"]: (item["family"], item["step_sha256"], item["solid_count"], item["datum_declarations"]) for item in manifest.get("candidates", [])}
        declared = {item["candidate_id"]: (item["family"], item["step_sha256"], item["expected_solid_count"], item["datums"]) for item in bindings}
        if source != declared: _fail("source_manifest_mismatch", "candidate bindings differ from manifest")
    return {"status": "passed", "config_sha256": canonical_sha256(config), "candidate_count": len(bindings), "density": density, "tolerances": tolerance_values}


def _tensor(value: Any, label: str) -> list[list[float]]:
    rows = _sequence(value, label)
    if len(rows) != 3: _fail("schema_error", label)
    result = [_vec(row, label) for row in rows]
    return result


def _face_record(face_raw: Mapping[str, Any]) -> dict[str, Any]:
    face = _mapping(face_raw, "face")
    _exact(face, {"surface_class", "area_m2", "center_m", "bounds_m", "normal", "curvature_samples", "face_signature_sha256"}, "face")
    body = {key: face[key] for key in face if key != "face_signature_sha256"}
    if face["face_signature_sha256"] != canonical_sha256(body): _fail("face_signature_mismatch", "face record hash differs")
    _number(face["area_m2"], "face area", minimum=1e-18); _vec(face["center_m"], "face center"); _bounds(face["bounds_m"], "face bounds"); _vec(face["normal"], "face normal")
    for sample in _sequence(face["curvature_samples"], "curvature samples"):
        item = _mapping(sample, "curvature sample"); _exact(item, {"u_fraction", "v_fraction", "k1_per_m", "k2_per_m", "radii_m"}, "curvature sample")
        _number(item["u_fraction"], "u fraction"); _number(item["v_fraction"], "v fraction"); _number(item["k1_per_m"], "k1"); _number(item["k2_per_m"], "k2")
        for radius in _sequence(item["radii_m"], "radii"): _number(radius, "radius", minimum=0.0)
    return dict(face)


def compare_report(config_raw: Mapping[str, Any], report_raw: Mapping[str, Any]) -> dict[str, Any]:
    config_result = validate_config(config_raw); config = config_raw; report = _mapping(report_raw, "report")
    _exact(report, {"witness_version", "source_manifest_sha256", "freecad_version", "occt_version", "import_mode", "hidden_geometry_repair", "candidates", "report_sha256"}, "report")
    if report["witness_version"] != WITNESS_VERSION or report["source_manifest_sha256"] != config["source_manifest_sha256"]: _fail("source_manifest_mismatch", "report source/version differs")
    if report["import_mode"] != "Part.Shape.read_step_no_repair" or report["hidden_geometry_repair"] is not False: _fail("hidden_geometry_repair", "report import route is not clean")
    body = {key: value for key, value in report.items() if key != "report_sha256"}
    if report["report_sha256"] != canonical_sha256(body): _fail("report_identity_mismatch", "report hash differs")
    measured = {}
    for raw in _sequence(report["candidates"], "report candidates"):
        candidate_id = raw.get("candidate_id") if isinstance(raw, Mapping) else None
        if candidate_id in measured: _fail("duplicate_candidate", "report candidate duplicated")
        measured[candidate_id] = raw
    bindings = {item["candidate_id"]: item for item in config["candidate_bindings"]}
    if set(measured) != set(bindings): _fail("candidate_set_mismatch", "report candidate set differs")
    semantic_summaries = []
    for candidate_id in sorted(bindings):
        binding, candidate = bindings[candidate_id], _mapping(measured[candidate_id], "candidate")
        required = {"candidate_id", "family", "step_sha256", "shape_type", "is_valid", "body_count", "solid_count", "shell_count", "volume_m3", "surface_area_m2", "material_density_kg_per_m3", "mass_kg", "centre_of_mass_m", "geometric_inertia_tensor_m5", "mass_inertia_tensor_kg_m2", "principal_moments_kg_m2", "principal_axes", "principal_axis_degeneracy_ratio", "axis_aligned_bounds_m", "principal_oriented_bounds_m", "faces", "curvature_spectrum", "thickness_field", "section_evolution", "datums", "regions", "path_witness", "clearance_interference", "swept_envelope", "limitations", "hidden_geometry_repair"}
        _exact(candidate, required, "candidate")
        if candidate["family"] != binding["family"] or candidate["step_sha256"] != binding["step_sha256"]: _fail("step_hash_mismatch", candidate_id)
        if candidate["hidden_geometry_repair"] is not False: _fail("hidden_geometry_repair", candidate_id)
        if candidate["is_valid"] is not True or candidate["solid_count"] != binding["expected_solid_count"] or candidate["body_count"] != candidate["solid_count"]: _fail("invalid_imported_topology", candidate_id)
        for count_key in ("body_count", "solid_count", "shell_count"):
            if isinstance(candidate[count_key], bool) or not isinstance(candidate[count_key], int) or candidate[count_key] < 1: _fail("invalid_imported_topology", count_key)
        volume = _number(candidate["volume_m3"], "volume", minimum=1e-18); density = _number(candidate["material_density_kg_per_m3"], "density", minimum=1e-18)
        mass = _number(candidate["mass_kg"], "mass", minimum=1e-18)
        if density != config_result["density"] or abs(mass - volume * density) > config_result["tolerances"]["relative"] * mass: _fail("mass_mismatch", candidate_id)
        _number(candidate["surface_area_m2"], "area", minimum=1e-18); _vec(candidate["centre_of_mass_m"], "centre of mass")
        geometric, mass_tensor = _tensor(candidate["geometric_inertia_tensor_m5"], "geometric inertia"), _tensor(candidate["mass_inertia_tensor_kg_m2"], "mass inertia")
        for i in range(3):
            for j in range(3):
                if abs(mass_tensor[i][j] - geometric[i][j] * density) > max(1e-18, abs(mass_tensor[i][j]) * config_result["tolerances"]["relative"]): _fail("inertia_mismatch", candidate_id)
        moments = [_number(item, "principal moment", minimum=0.0) for item in _sequence(candidate["principal_moments_kg_m2"], "principal moments")]
        axes = [_vec(item, "principal axis") for item in _sequence(candidate["principal_axes"], "principal axes")]
        if len(moments) != 3 or len(axes) != 3: _fail("invalid_inertia", candidate_id)
        expected_moments, _ = symmetric_eigen_3x3(mass_tensor)
        if any(abs(actual - expected) > max(1e-18, abs(expected) * config_result["tolerances"]["relative"]) for actual, expected in zip(moments, expected_moments)): _fail("principal_inertia_mismatch", candidate_id)
        for axis in axes:
            if abs(_norm(axis) - 1) > config_result["tolerances"]["axis_orthogonality"]: _fail("invalid_inertia", "principal axis norm")
        if any(abs(math.fsum(axes[i][k] * axes[j][k] for k in range(3))) > config_result["tolerances"]["axis_orthogonality"] for i, j in ((0, 1), (0, 2), (1, 2))): _fail("invalid_inertia", "principal axes not orthogonal")
        _number(candidate["principal_axis_degeneracy_ratio"], "degeneracy", minimum=0.0)
        bounds = _bounds(candidate["axis_aligned_bounds_m"], "axis bounds")
        oriented = _mapping(candidate["principal_oriented_bounds_m"], "oriented bounds"); _exact(oriented, {"method", "axes", "minimum", "maximum"}, "oriented bounds")
        if oriented["method"] != "vertex_and_tessellation_projection": _fail("unsupported_measurement", "oriented bounds method")
        oriented_axes = [_vec(item, "oriented axis") for item in _sequence(oriented["axes"], "oriented axes")]
        if oriented_axes != axes: _fail("oriented_bounds_mismatch", "oriented axes differ from principal axes")
        _bounds({"minimum": oriented["minimum"], "maximum": oriented["maximum"]}, "oriented extents")
        faces = [_face_record(item) for item in _sequence(candidate["faces"], "faces")]
        if not faces or len({item["face_signature_sha256"] for item in faces}) != len(faces): _fail("ambiguous_face_signature", candidate_id)
        spans = [high - low for low, high in zip(bounds["minimum"], bounds["maximum"])]
        path_axis = max(range(3), key=lambda index: (spans[index], -index))
        curvature = _mapping(candidate["curvature_spectrum"], "curvature spectrum")
        _exact(curvature, {"surface_class_counts", "surface_class_area_m2", "curvature_sample_count", "finite_radius_count", "minimum_sampled_radius_m", "maximum_sampled_radius_m"}, "curvature spectrum")
        classes: dict[str, int] = {}; class_areas: dict[str, float] = {}; radii = []; curvature_sample_count = 0
        for face in faces:
            classes[face["surface_class"]] = classes.get(face["surface_class"], 0) + 1; class_areas[face["surface_class"]] = class_areas.get(face["surface_class"], 0.0) + face["area_m2"]
            for sample in face["curvature_samples"]: curvature_sample_count += 1; radii.extend(sample["radii_m"])
        if curvature["surface_class_counts"] != dict(sorted(classes.items())) or set(curvature["surface_class_area_m2"]) != set(class_areas): _fail("curvature_spectrum_mismatch", candidate_id)
        if any(abs(_number(curvature["surface_class_area_m2"][key], "class area") - value) > max(1e-18, value * config_result["tolerances"]["relative"]) for key, value in class_areas.items()): _fail("curvature_spectrum_mismatch", candidate_id)
        if curvature["curvature_sample_count"] != curvature_sample_count or curvature["finite_radius_count"] != len(radii): _fail("curvature_spectrum_mismatch", candidate_id)
        expected_min_radius, expected_max_radius = (min(radii), max(radii)) if radii else (None, None)
        if curvature["minimum_sampled_radius_m"] != expected_min_radius or curvature["maximum_sampled_radius_m"] != expected_max_radius: _fail("curvature_spectrum_mismatch", candidate_id)
        expected_datums = derive_datums(bounds, binding["datums"])
        datums = sorted(_sequence(candidate["datums"], "datums"), key=lambda item: item["datum_id"])
        if datums != sorted(expected_datums, key=lambda item: item["datum_id"]): _fail("datum_correspondence_mismatch", candidate_id)
        region_by_id = {item.get("region_id"): item for item in _sequence(candidate["regions"], "regions") if isinstance(item, Mapping)}
        if set(region_by_id) != {item["region_id"] for item in config["semantic_regions"]}: _fail("missing_region", candidate_id)
        region_summaries = []
        for declaration in config["semantic_regions"]:
            region = _mapping(region_by_id[declaration["region_id"]], "region")
            _exact(region, {"region_id", "intent", "selector", "face_signatures", "area_m2", "region_signature_sha256"}, "region")
            selected = select_face_signatures(faces, declaration["selector"], path_axis, config_result["tolerances"]["region_tie_relative"])
            if region["intent"] != declaration["intent"] or region["selector"] != declaration["selector"] or region["face_signatures"] != selected: _fail("region_correspondence_mismatch", declaration["region_id"])
            area = math.fsum(item["area_m2"] for item in faces if item["face_signature_sha256"] in selected)
            if abs(_number(region["area_m2"], "region area") - area) > max(1e-18, area * config_result["tolerances"]["relative"]): _fail("region_correspondence_mismatch", "area")
            region_body = {key: region[key] for key in region if key != "region_signature_sha256"}
            if region["region_signature_sha256"] != canonical_sha256(region_body): _fail("region_signature_mismatch", declaration["region_id"])
            region_summaries.append({"region_id": region["region_id"], "signature": region["region_signature_sha256"]})
        thickness = _mapping(candidate["thickness_field"], "thickness field"); _exact(thickness, {"method", "probe_count", "material_span_count", "samples_m", "minimum_sampled_span_m"}, "thickness field")
        if thickness["method"] != "axis_aligned_brep_line_material_spans": _fail("unsupported_measurement", "thickness method")
        samples = [_number(item, "thickness sample", minimum=1e-18) for item in _sequence(thickness["samples_m"], "thickness samples")]
        if isinstance(thickness["probe_count"], bool) or not isinstance(thickness["probe_count"], int) or thickness["probe_count"] < 1 or not samples or thickness["material_span_count"] != len(samples) or abs(min(samples) - thickness["minimum_sampled_span_m"]) > 1e-15: _fail("invalid_thickness_field", candidate_id)
        sections = _mapping(candidate["section_evolution"], "section evolution"); _exact(sections, {"method", "path_axis_index", "path_length_m", "samples"}, "section evolution")
        section_samples = _sequence(sections["samples"], "section samples")
        if sections["method"] != "thin_brep_slab_volume" or sections["path_axis_index"] != path_axis or abs(_number(sections["path_length_m"], "section path length") - spans[path_axis]) > config_result["tolerances"]["length_absolute_m"] or len(section_samples) != len(config["sampling_protocol"]["section_path_fractions"]): _fail("invalid_section_evolution", candidate_id)
        for sample in section_samples:
            item = _mapping(sample, "section sample"); _exact(item, {"path_fraction", "area_m2", "equivalent_radius_m", "second_moment_proxy_m4"}, "section sample")
            for key in ("area_m2", "equivalent_radius_m", "second_moment_proxy_m4"): _number(item[key], key, minimum=0.0)
        path = _mapping(candidate["path_witness"], "path witness"); _exact(path, {"path_datum_id", "path_axis_index", "path_length_m", "minimum_sampled_bend_radius_m", "cross_section_sample_count"}, "path witness")
        if path["path_datum_id"] != binding["path_datum_id"] or path["path_axis_index"] != path_axis or path["path_length_m"] != sections["path_length_m"] or path["minimum_sampled_bend_radius_m"] != expected_min_radius or path["cross_section_sample_count"] != len(section_samples): _fail("path_correspondence_mismatch", candidate_id)
        clearance = _mapping(candidate["clearance_interference"], "clearance"); _exact(clearance, {"scope", "solid_pair_count", "minimum_clearance_m", "interference_volume_m3"}, "clearance")
        expected_pairs = candidate["solid_count"] * (candidate["solid_count"] - 1) // 2
        if clearance["scope"] != "within_imported_candidate_solids" or clearance["solid_pair_count"] != expected_pairs: _fail("clearance_scope_mismatch", candidate_id)
        if expected_pairs == 0 and clearance["minimum_clearance_m"] is not None: _fail("clearance_scope_mismatch", candidate_id)
        if expected_pairs and clearance["minimum_clearance_m"] is None: _fail("clearance_scope_mismatch", candidate_id)
        if clearance["minimum_clearance_m"] is not None: _number(clearance["minimum_clearance_m"], "minimum clearance", minimum=0.0)
        _number(clearance["interference_volume_m3"], "interference volume", minimum=0.0)
        swept = _mapping(candidate["swept_envelope"], "swept envelope"); _exact(swept, {"motion_model", "bounds_m", "envelope_volume_m3"}, "swept envelope")
        swept_bounds = _bounds(swept["bounds_m"], "swept bounds"); expected_envelope = math.prod(high - low for low, high in zip(bounds["minimum"], bounds["maximum"]))
        if swept["motion_model"] != config["sampling_protocol"]["swept_motion_model"] or swept_bounds != bounds or abs(_number(swept["envelope_volume_m3"], "envelope volume") - expected_envelope) > max(1e-18, expected_envelope * config_result["tolerances"]["relative"]): _fail("swept_envelope_mismatch", candidate_id)
        limitations = _sequence(candidate["limitations"], "limitations")
        if not limitations or any(not isinstance(item, str) or not item for item in limitations): _fail("missing_limitation", candidate_id)
        semantic_summaries.append({"candidate_id": candidate_id, "step_sha256": candidate["step_sha256"], "face_signatures": sorted(item["face_signature_sha256"] for item in faces), "datum_signatures": sorted(item["datum_signature_sha256"] for item in datums), "regions": sorted(region_summaries, key=lambda item: item["region_id"]), "minimum_sampled_span_m": thickness["minimum_sampled_span_m"], "section_evolution": list(section_samples)})
    semantic_body = {"status": "passed", "witness_version": WITNESS_VERSION, "config_sha256": config_result["config_sha256"], "source_manifest_sha256": config["source_manifest_sha256"], "candidate_count": len(semantic_summaries), "semantic_summaries": semantic_summaries, "hidden_geometry_repair": False, "structural_validity": False}
    return {**semantic_body, "freecad_report_sha256": report["report_sha256"], "comparison_sha256": canonical_sha256(semantic_body)}


__all__ = ["WITNESS_VERSION", "SemanticWitnessViolation", "canonical_sha256", "derive_datums", "select_face_signatures", "validate_config", "compare_report", "symmetric_eigen_3x3"]
