#!/usr/bin/env python3
"""Independently inspect Work 092 STEP semantics with FreeCAD/OCCT."""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
import math
import os
from pathlib import Path
import sys

import FreeCAD
import Part

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.components.semantic_geometry_witness import (  # noqa: E402
    WITNESS_VERSION,
    canonical_sha256,
    derive_datums,
    select_face_signatures,
    symmetric_eigen_3x3,
    validate_config,
)

MM = 1000.0


def vector(value) -> list[float]:
    return [float(value.x) / MM, float(value.y) / MM, float(value.z) / MM]


def bounds(shape) -> dict[str, list[float]]:
    box = shape.optimalBoundingBox(False, False)
    return {"minimum": [box.XMin / MM, box.YMin / MM, box.ZMin / MM], "maximum": [box.XMax / MM, box.YMax / MM, box.ZMax / MM]}


def matrix3(matrix, scale: float) -> list[list[float]]:
    names = (("A11", "A12", "A13"), ("A21", "A22", "A23"), ("A31", "A32", "A33"))
    return [[float(getattr(matrix, item)) * scale for item in row] for row in names]


def aggregate_mass_properties(shape) -> tuple[float, object, list[list[float]]]:
    solids = list(shape.Solids); total_volume = math.fsum(float(solid.Volume) for solid in solids)
    if total_volume <= 0: raise RuntimeError("imported shape has no positive solid volume")
    center = FreeCAD.Vector(
        math.fsum(float(solid.CenterOfMass.x) * float(solid.Volume) for solid in solids) / total_volume,
        math.fsum(float(solid.CenterOfMass.y) * float(solid.Volume) for solid in solids) / total_volume,
        math.fsum(float(solid.CenterOfMass.z) * float(solid.Volume) for solid in solids) / total_volume,
    )
    tensor = [[0.0, 0.0, 0.0] for _ in range(3)]
    for solid in solids:
        local = matrix3(solid.MatrixOfInertia, 1.0); displacement = [float(solid.CenterOfMass.x - center.x), float(solid.CenterOfMass.y - center.y), float(solid.CenterOfMass.z - center.z)]
        squared = math.fsum(item * item for item in displacement); volume = float(solid.Volume)
        for row in range(3):
            for column in range(3):
                shift = volume * ((squared if row == column else 0.0) - displacement[row] * displacement[column])
                tensor[row][column] += local[row][column] + shift
    return total_volume, center, [[item * 1e-15 for item in row] for row in tensor]


def canonical_axis(axis: list[float]) -> list[float]:
    length = math.sqrt(math.fsum(item * item for item in axis))
    result = [item / length for item in axis]
    for item in result:
        if abs(item) > 1e-12:
            if item < 0: result = [-entry for entry in result]
            break
    return result


def face_record(face, fractions: list[float], curvature_zero: float) -> dict:
    surface_class = type(face.Surface).__name__
    parameter_range = face.ParameterRange; u0, u1, v0, v1 = (float(item) for item in parameter_range)
    samples = []
    for fraction in fractions:
        u, v = u0 + fraction * (u1 - u0), v0 + fraction * (v1 - v0)
        try:
            k1, k2 = (float(item) * MM for item in face.curvatureAt(u, v))
        except Exception:
            continue
        if not math.isfinite(k1) or not math.isfinite(k2): continue
        radii = sorted(1.0 / abs(item) for item in (k1, k2) if abs(item) > curvature_zero)
        samples.append({"u_fraction": fraction, "v_fraction": fraction, "k1_per_m": k1, "k2_per_m": k2, "radii_m": radii})
    try:
        normal_vector = face.normalAt((u0 + u1) / 2, (v0 + v1) / 2)
        normal = canonical_axis([float(normal_vector.x), float(normal_vector.y), float(normal_vector.z)])
    except Exception:
        normal = [0.0, 0.0, 0.0]
    body = {"surface_class": surface_class, "area_m2": float(face.Area) * 1e-6, "center_m": vector(face.CenterOfMass), "bounds_m": bounds(face), "normal": normal, "curvature_samples": samples}
    return {**body, "face_signature_sha256": canonical_sha256(body)}


def curvature_spectrum(faces: list[dict]) -> dict:
    counts = Counter(item["surface_class"] for item in faces); areas: dict[str, float] = defaultdict(float); radii = []; sample_count = 0
    for face in faces:
        areas[face["surface_class"]] += face["area_m2"]
        for sample in face["curvature_samples"]: sample_count += 1; radii.extend(sample["radii_m"])
    return {"surface_class_counts": dict(sorted(counts.items())), "surface_class_area_m2": dict(sorted(areas.items())), "curvature_sample_count": sample_count, "finite_radius_count": len(radii), "minimum_sampled_radius_m": min(radii) if radii else None, "maximum_sampled_radius_m": max(radii) if radii else None}


def thickness_field(shape, shape_bounds: dict, fractions: list[float]) -> dict:
    low, high = shape_bounds["minimum"], shape_bounds["maximum"]; spans = [high[i] - low[i] for i in range(3)]; samples = []; probes = 0
    def probe_axis(axis: int, coordinates: list[float]) -> None:
        nonlocal probes
        pad = max(spans[axis] * 0.05, 1e-5)
        start = list(coordinates); end = list(coordinates); start[axis] = low[axis] - pad; end[axis] = high[axis] + pad
        line = Part.makeLine(FreeCAD.Vector(*(item * MM for item in start)), FreeCAD.Vector(*(item * MM for item in end)))
        section = shape.section(line); probes += 1; coordinates_on_line = []
        for vertex in section.Vertexes:
            point = [float(vertex.Point.x) / MM, float(vertex.Point.y) / MM, float(vertex.Point.z) / MM]; coordinates_on_line.append(point[axis])
        coordinates_on_line.sort(); unique = []
        for item in coordinates_on_line:
            if not unique or abs(item - unique[-1]) > 1e-9: unique.append(item)
        for left, right in zip(unique, unique[1:]):
            midpoint = list(coordinates); midpoint[axis] = (left + right) / 2; point = FreeCAD.Vector(*(item * MM for item in midpoint))
            if any(solid.isInside(point, 1e-7, False) for solid in shape.Solids): samples.append(right - left)
    for axis in range(3):
        others = [index for index in range(3) if index != axis]
        for first in fractions:
            for second in fractions:
                coordinates = [(low[i] + high[i]) / 2 for i in range(3)]
                coordinates[others[0]] = low[others[0]] + first * spans[others[0]]
                coordinates[others[1]] = low[others[1]] + second * spans[others[1]]
                probe_axis(axis, coordinates)
    for solid in shape.Solids:
        center = vector(solid.CenterOfMass)
        for axis in range(3): probe_axis(axis, list(center))
    samples = sorted(samples)
    if not samples: raise RuntimeError("thickness probes recovered no material spans")
    return {"method": "axis_aligned_brep_line_material_spans", "probe_count": probes, "material_span_count": len(samples), "samples_m": samples, "minimum_sampled_span_m": min(samples)}


def section_evolution(shape, shape_bounds: dict, fractions: list[float], slab_fraction: float) -> dict:
    low, high = shape_bounds["minimum"], shape_bounds["maximum"]; spans = [high[i] - low[i] for i in range(3)]; axis = max(range(3), key=lambda index: (spans[index], -index))
    slab_m = max(spans[axis] * slab_fraction, 1e-6); pad_m = max(max(spans) * 0.05, 1e-5); samples = []
    for fraction in fractions:
        position = low[axis] + fraction * spans[axis]; origin = [low[i] - pad_m for i in range(3)]; dimensions = [spans[i] + 2 * pad_m for i in range(3)]
        origin[axis] = position - slab_m / 2; dimensions[axis] = slab_m
        slab = Part.makeBox(*(item * MM for item in dimensions), FreeCAD.Vector(*(item * MM for item in origin)))
        section = shape.common(slab); area_m2 = max(0.0, float(section.Volume) * 1e-9 / slab_m)
        equivalent_radius = math.sqrt(area_m2 / math.pi) if area_m2 > 0 else 0.0
        secondary = [index for index in range(3) if index != axis]
        if area_m2 > 0:
            section_box = section.BoundBox; section_spans = [section_box.XLength / MM, section_box.YLength / MM, section_box.ZLength / MM]
            second_moment = area_m2 * math.fsum(section_spans[index] ** 2 for index in secondary) / 12.0
        else:
            second_moment = 0.0
        samples.append({"path_fraction": fraction, "area_m2": area_m2, "equivalent_radius_m": equivalent_radius, "second_moment_proxy_m4": second_moment})
    return {"method": "thin_brep_slab_volume", "path_axis_index": axis, "path_length_m": spans[axis], "samples": samples}


def oriented_bounds(shape, axes: list[list[float]], deflection_m: float) -> dict:
    points = [vector(vertex.Point) for vertex in shape.Vertexes]
    tessellated, _ = shape.tessellate(deflection_m * MM); points.extend(vector(point) for point in tessellated)
    projections = [[math.fsum(point[i] * axis[i] for i in range(3)) for point in points] for axis in axes]
    return {"method": "vertex_and_tessellation_projection", "axes": axes, "minimum": [min(items) for items in projections], "maximum": [max(items) for items in projections]}


def regions(face_records: list[dict], declarations: list[dict], path_axis: int, tie_relative: float) -> list[dict]:
    by_signature = {item["face_signature_sha256"]: item for item in face_records}; result = []
    for declaration in declarations:
        selected = select_face_signatures(face_records, declaration["selector"], path_axis, tie_relative)
        body = {"region_id": declaration["region_id"], "intent": declaration["intent"], "selector": declaration["selector"], "face_signatures": selected, "area_m2": math.fsum(by_signature[item]["area_m2"] for item in selected)}
        result.append({**body, "region_signature_sha256": canonical_sha256(body)})
    return result


def clearance_interference(shape) -> dict:
    solids = list(shape.Solids); pair_count = 0; minimum_clearance = None; interference = 0.0
    for left in range(len(solids)):
        for right in range(left + 1, len(solids)):
            pair_count += 1; distance = float(solids[left].distToShape(solids[right])[0]) / MM
            minimum_clearance = distance if minimum_clearance is None else min(minimum_clearance, distance)
            interference += max(0.0, float(solids[left].common(solids[right]).Volume) * 1e-9)
    return {"scope": "within_imported_candidate_solids", "solid_pair_count": pair_count, "minimum_clearance_m": minimum_clearance, "interference_volume_m3": interference}


def measure(binding: dict, config: dict, source_root: Path) -> dict:
    path = source_root / f"{binding['candidate_id']}.step"
    if hashlib.sha256(path.read_bytes()).hexdigest() != binding["step_sha256"]: raise RuntimeError(f"STEP identity mismatch: {binding['candidate_id']}")
    shape = Part.Shape(); shape.read(os.fspath(path))
    if shape.isNull() or not shape.isValid(): raise RuntimeError(f"invalid STEP: {binding['candidate_id']}")
    shape_bounds = bounds(shape); density = config["material_density_kg_per_m3"]
    total_volume_mm3, aggregate_center, geometric = aggregate_mass_properties(shape); mass_tensor = [[item * density for item in row] for row in geometric]
    moments, axes = symmetric_eigen_3x3(mass_tensor); axes = [canonical_axis(axis) for axis in axes]
    moment_scale = max(moments[-1], 1e-30); degeneracy = min(abs(moments[i + 1] - moments[i]) / moment_scale for i in range(2))
    face_records = sorted((face_record(face, config["sampling_protocol"]["curvature_parameter_fractions"], config["tolerances"]["curvature_zero_per_m"]) for face in shape.Faces), key=lambda item: item["face_signature_sha256"])
    sections = section_evolution(shape, shape_bounds, config["sampling_protocol"]["section_path_fractions"], config["sampling_protocol"]["section_slab_fraction"])
    curvature = curvature_spectrum(face_records); min_radius = curvature["minimum_sampled_radius_m"]
    path_axis = sections["path_axis_index"]
    try:
        thickness = thickness_field(shape, shape_bounds, config["sampling_protocol"]["thickness_grid_fractions"])
    except RuntimeError as error:
        raise RuntimeError(f"{binding['candidate_id']}: {error}") from error
    record = {
        "candidate_id": binding["candidate_id"], "family": binding["family"], "step_sha256": binding["step_sha256"], "shape_type": shape.ShapeType,
        "is_valid": bool(shape.isValid()), "body_count": len(shape.Solids) or len(shape.Shells), "solid_count": len(shape.Solids), "shell_count": len(shape.Shells),
        "volume_m3": total_volume_mm3 * 1e-9, "surface_area_m2": float(shape.Area) * 1e-6, "material_density_kg_per_m3": density,
        "mass_kg": total_volume_mm3 * 1e-9 * density, "centre_of_mass_m": vector(aggregate_center),
        "geometric_inertia_tensor_m5": geometric, "mass_inertia_tensor_kg_m2": mass_tensor, "principal_moments_kg_m2": moments, "principal_axes": axes,
        "principal_axis_degeneracy_ratio": degeneracy, "axis_aligned_bounds_m": shape_bounds,
        "principal_oriented_bounds_m": oriented_bounds(shape, axes, config["sampling_protocol"]["oriented_bounds_tessellation_m"]),
        "faces": face_records, "curvature_spectrum": curvature,
        "thickness_field": thickness,
        "section_evolution": sections, "datums": derive_datums(shape_bounds, binding["datums"]),
        "regions": regions(face_records, config["semantic_regions"], path_axis, config["tolerances"]["region_tie_relative"]),
        "path_witness": {"path_datum_id": binding["path_datum_id"], "path_axis_index": path_axis, "path_length_m": sections["path_length_m"], "minimum_sampled_bend_radius_m": min_radius, "cross_section_sample_count": len(sections["samples"])},
        "clearance_interference": clearance_interference(shape),
        "swept_envelope": {"motion_model": "static_identity_only", "bounds_m": shape_bounds, "envelope_volume_m3": math.prod(high - low for low, high in zip(shape_bounds["minimum"], shape_bounds["maximum"]))},
        "limitations": ["sampled_not_global_thickness", "sampled_curvature_not_global", "section_second_moment_is_proxy", "static_self_clearance_only", "no_structural_validity"],
        "hidden_geometry_repair": False,
    }
    return record


def main() -> int:
    config_path = Path(os.environ["FORMULA_ULTIMATE_W096_CONFIG"]); manifest_path = Path(os.environ["FORMULA_ULTIMATE_W096_MANIFEST"])
    source_root = Path(os.environ["FORMULA_ULTIMATE_W096_SOURCE_ROOT"]); output_path = Path(os.environ["FORMULA_ULTIMATE_W096_OUTPUT"])
    config = json.loads(config_path.read_text(encoding="utf-8")); manifest = json.loads(manifest_path.read_text(encoding="utf-8")); validate_config(config, manifest)
    candidates = [measure(binding, config, source_root) for binding in config["candidate_bindings"]]
    body = {"witness_version": WITNESS_VERSION, "source_manifest_sha256": config["source_manifest_sha256"], "freecad_version": ".".join(FreeCAD.Version()[:3]), "occt_version": str(Part.OCC_VERSION), "import_mode": "Part.Shape.read_step_no_repair", "hidden_geometry_repair": False, "candidates": candidates}
    report = {**body, "report_sha256": canonical_sha256(body)}; output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "measured", "candidate_count": len(candidates), "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
