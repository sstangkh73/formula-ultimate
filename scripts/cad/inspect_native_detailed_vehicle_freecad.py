"""Exact no-repair FreeCAD inspection for Work 135 native STEP evidence."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import zipfile
from pathlib import Path
from typing import Any


import FreeCAD as App

FREECAD_HOME = Path(App.getHomePath())
PART_MODULE = FREECAD_HOME / "Mod" / "Part"
if str(PART_MODULE) not in sys.path:
    sys.path.insert(0, str(PART_MODULE))
import Part  # noqa: E402


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False)
        stream.write("\n")


def _surface_type(face) -> str:
    name = type(face.Surface).__name__.upper()
    aliases = {
        "PLANE": "PLANE",
        "CYLINDER": "CYLINDER",
        "CONE": "CONE",
        "SPHERE": "SPHERE",
        "TORUS": "TORUS",
        "BSPLINESURFACE": "BSPLINE",
        "BEZIERSURFACE": "BEZIER",
    }
    return aliases.get(name, name.replace("SURFACE", ""))


def _clean_signature_number(value: float, digits: int) -> float:
    """Quantize a semantic signature and canonicalize signed zero."""

    cleaned = round(float(value), digits)
    return 0.0 if cleaned == 0.0 else cleaned


def _face_record(face) -> dict[str, Any]:
    box = face.BoundBox
    center = face.CenterOfMass
    geometry_type = _surface_type(face)
    normal = None
    if geometry_type == "PLANE":
        try:
            u0, u1, v0, v1 = face.ParameterRange
            vector = face.normalAt((u0 + u1) / 2.0, (v0 + v1) / 2.0)
            normal = [_clean_signature_number(abs(value), 7) for value in (vector.x, vector.y, vector.z)]
        except Exception:
            normal = None
    record = {
        "surface_type": geometry_type,
        "area_m2": _clean_signature_number(face.Area * 1.0e-6, 8),
        "center_m": [_clean_signature_number(center.x * 1.0e-3, 7), _clean_signature_number(center.y * 1.0e-3, 7), _clean_signature_number(center.z * 1.0e-3, 7)],
        "bounds_m": [
            [_clean_signature_number(box.XMin * 1.0e-3, 7), _clean_signature_number(box.YMin * 1.0e-3, 7), _clean_signature_number(box.ZMin * 1.0e-3, 7)],
            [_clean_signature_number(box.XMax * 1.0e-3, 7), _clean_signature_number(box.YMax * 1.0e-3, 7), _clean_signature_number(box.ZMax * 1.0e-3, 7)],
        ],
        "edge_count": len(face.Edges),
        "absolute_normal": normal,
    }
    record["signature_sha256"] = _canonical_sha256(record)
    return record


def _selector_records(shape, selectors: list[str]) -> dict[str, list[dict[str, Any]]]:
    records = [(face, _face_record(face)) for face in shape.Faces]
    result: dict[str, list[dict[str, Any]]] = {}
    axis_index = {"x": 0, "y": 1, "z": 2}
    for selector in selectors:
        if selector == "all_faces":
            chosen = [record for _, record in records]
        elif selector in {"x+", "x-", "y+", "y-", "z+", "z-"}:
            axis = axis_index[selector[0]]
            candidates = [
                pair for pair in records
                if pair[1]["surface_type"] == "PLANE"
                and pair[1]["absolute_normal"] is not None
                and pair[1]["absolute_normal"][axis] >= 0.999999
            ]
            if not candidates:
                candidates = records
            if selector[1] == "+":
                chosen = [max(candidates, key=lambda pair: pair[1]["center_m"][axis])[1]]
            else:
                chosen = [min(candidates, key=lambda pair: pair[1]["center_m"][axis])[1]]
        elif selector in {"outer_cylinder", "inner_cylinder"}:
            candidates = [pair for pair in records if pair[1]["surface_type"] == "CYLINDER"]
            if not candidates:
                raise RuntimeError(f"semantic selector {selector} found no cylindrical face")

            def metric(pair):
                return max(
                    pair[1]["bounds_m"][1][axis] - pair[1]["bounds_m"][0][axis]
                    for axis in range(3)
                )

            selected = max(candidates, key=metric) if selector == "outer_cylinder" else min(candidates, key=metric)
            chosen = [selected[1]]
        elif selector == "largest_area":
            chosen = [max(records, key=lambda pair: pair[1]["area_m2"])[1]]
        else:
            raise RuntimeError(f"unknown semantic face selector: {selector}")
        result[selector] = sorted(chosen, key=lambda item: item["signature_sha256"])
    return result


def _mass_properties(solid, density_kg_m3: float) -> dict[str, Any]:
    volume_m3 = solid.Volume * 1.0e-9
    center = solid.CenterOfMass
    matrix = solid.MatrixOfInertia
    return {
        "volume_m3": volume_m3,
        "mass_kg": volume_m3 * density_kg_m3,
        "center_m": [center.x * 1.0e-3, center.y * 1.0e-3, center.z * 1.0e-3],
        "centroidal_inertia_kg_m2": [
            matrix.A11 * density_kg_m3 * 1.0e-15,
            matrix.A22 * density_kg_m3 * 1.0e-15,
            matrix.A33 * density_kg_m3 * 1.0e-15,
            matrix.A12 * density_kg_m3 * 1.0e-15,
            matrix.A13 * density_kg_m3 * 1.0e-15,
            matrix.A23 * density_kg_m3 * 1.0e-15,
        ],
    }


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    material = [row for row in rows if row["mass_kg"] > 0.0]
    mass = math.fsum(row["mass_kg"] for row in material)
    center = [math.fsum(row["mass_kg"] * row["center_m"][axis] for row in material) / mass for axis in range(3)]
    inertia = [0.0] * 6
    for row in material:
        dx, dy, dz = [row["center_m"][axis] - center[axis] for axis in range(3)]
        parallel = [
            row["mass_kg"] * (dy * dy + dz * dz),
            row["mass_kg"] * (dx * dx + dz * dz),
            row["mass_kg"] * (dx * dx + dy * dy),
            -row["mass_kg"] * dx * dy,
            -row["mass_kg"] * dx * dz,
            -row["mass_kg"] * dy * dz,
        ]
        inertia = [inertia[index] + row["centroidal_inertia_kg_m2"][index] + parallel[index] for index in range(6)]
    return {"mass_kg": mass, "center_m": center, "inertia_kg_m2": inertia}


def _relative(actual: float, expected: float) -> float:
    return abs(actual - expected) / max(abs(expected), 1.0e-300)


def _numbers_close(left: Any, right: Any, absolute_tolerance: float) -> bool:
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(
            _numbers_close(left_value, right_value, absolute_tolerance)
            for left_value, right_value in zip(left, right)
        )
    return abs(float(left) - float(right)) <= absolute_tolerance


def _face_records_match(expected: list[dict[str, Any]], measured: list[dict[str, Any]]) -> bool:
    """Match STEP face signatures using the declared cross-kernel precision."""

    if len(expected) != len(measured):
        return False
    unmatched = list(measured)
    for expected_face in expected:
        matched_index = None
        for index, measured_face in enumerate(unmatched):
            if expected_face["surface_type"] != measured_face["surface_type"]:
                continue
            # Periodic curved surfaces may gain or lose a parameter-seam edge
            # during STEP transfer.  A planar edge-count change is physical;
            # a curved seam-count change is not.
            if (
                expected_face["surface_type"] == "PLANE"
                and expected_face["edge_count"] != measured_face["edge_count"]
            ):
                continue
            area_tolerance = max(1.0e-8, abs(float(expected_face["area_m2"])) * 1.0e-8)
            if not _numbers_close(expected_face["area_m2"], measured_face["area_m2"], area_tolerance):
                continue
            if not _numbers_close(expected_face["center_m"], measured_face["center_m"], 1.0e-7):
                continue
            # STEP may move the parameter seam of curved faces, changing the
            # axis-aligned face bounds without changing the physical surface.
            # Planar bounds remain stable and are therefore part of the match.
            if expected_face["surface_type"] == "PLANE" and not _numbers_close(
                expected_face["bounds_m"], measured_face["bounds_m"], 1.0e-7
            ):
                continue
            expected_normal = expected_face["absolute_normal"]
            measured_normal = measured_face["absolute_normal"]
            if (expected_normal is None) != (measured_normal is None):
                continue
            if expected_normal is not None and not _numbers_close(expected_normal, measured_normal, 1.0e-7):
                continue
            matched_index = index
            break
        if matched_index is None:
            return False
        unmatched.pop(matched_index)
    return not unmatched


def _canonicalize_fcstd(path: Path) -> None:
    temporary = path.with_suffix(".canonical.tmp")
    with zipfile.ZipFile(path, "r") as source, zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as target:
        for name in sorted(source.namelist()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 0
            info.external_attr = 0
            payload = source.read(name)
            if name == "Document.xml":
                text = payload.decode("utf-8")
                text = re.sub(
                    r'(<Property name="(?:CreationDate|LastModifiedDate)"[\s\S]*?<String value=")[^"]+("/>)',
                    r'\g<1>1970-01-01T00:00:00Z\g<2>',
                    text,
                    count=2,
                )
                text = re.sub(
                    r'<Uuid value="[^"]+"/>',
                    '<Uuid value="00000000-0000-0000-0000-000000000135"/>',
                    text,
                    count=1,
                )
                object_ids: dict[str, str] = {}

                def replace_id(match: re.Match[str]) -> str:
                    source_id = match.group(1)
                    canonical_id = object_ids.setdefault(source_id, str(len(object_ids) + 1))
                    return f' id="{canonical_id}"'

                text = re.sub(r' id="(\d+)"', replace_id, text)
                payload = text.encode("utf-8")
            target.writestr(info, payload)
    os.replace(temporary, path)


def main() -> int:
    if len(sys.argv) < 5:
        raise SystemExit("pass MANIFEST CONFIG OUTPUT_REPORT OUTPUT_FCSTD")
    manifest_path = Path(sys.argv[-4]).resolve()
    config_path = Path(sys.argv[-3]).resolve()
    output_path = Path(sys.argv[-2]).resolve()
    fcstd_path = Path(sys.argv[-1]).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    artifact_root = manifest_path.parent
    definition_by_id = {item["definition_id"]: item for item in config["definitions"]}
    definition_rows = []
    rows = []
    maximum = {"volume_relative": 0.0, "mass_relative": 0.0, "center_absolute_m": 0.0, "inertia_relative": 0.0}
    semantic_total = 0
    semantic_matched = 0
    semantic_failures: list[dict[str, str]] = []
    definition_invalid_or_null = 0
    instance_invalid_or_null = 0
    step_hash_match = True
    for reference in manifest["definitions"]:
        step_path = artifact_root / reference["step_path"]
        observed_hash = _sha256(step_path)
        step_hash_match = step_hash_match and observed_hash == reference["step_sha256"]
        shape = Part.Shape()
        shape.read(str(step_path))
        if shape.isNull() or not shape.isValid() or len(shape.Solids) != 1:
            definition_invalid_or_null += 1
            continue
        solid = shape.Solids[0]
        selectors = definition_by_id[reference["definition_id"]]["semantic_face_selectors"]
        measured_faces = _selector_records(solid, selectors)
        for selector in selectors:
            semantic_total += 1
            if _face_records_match(reference["semantic_faces"][selector], measured_faces[selector]):
                semantic_matched += 1
            else:
                semantic_failures.append({
                    "entity_kind": "definition",
                    "entity_id": reference["definition_id"],
                    "selector": selector,
                })
        definition_rows.append({
            "definition_id": reference["definition_id"],
            "step_path": reference["step_path"],
            "step_sha256": observed_hash,
            "valid": True,
            "solid_count": 1,
            "semantic_faces": measured_faces,
        })

    imported_shapes: dict[str, Any] = {}
    for reference in manifest["instances"]:
        step_path = artifact_root / reference["step_path"]
        observed_hash = _sha256(step_path)
        step_hash_match = step_hash_match and observed_hash == reference["step_sha256"]
        shape = Part.Shape()
        shape.read(str(step_path))
        if shape.isNull() or not shape.isValid() or len(shape.Solids) != 1:
            instance_invalid_or_null += 1
            continue
        solid = shape.Solids[0]
        imported_shapes[reference["instance_id"]] = solid
        measured = _mass_properties(solid, float(reference["density_kg_m3"]))
        maximum["volume_relative"] = max(maximum["volume_relative"], _relative(measured["volume_m3"], reference["volume_m3"]))
        maximum["mass_relative"] = max(maximum["mass_relative"], _relative(measured["mass_kg"], reference["mass_kg"]))
        maximum["center_absolute_m"] = max(maximum["center_absolute_m"], *(abs(left - right) for left, right in zip(measured["center_m"], reference["center_m"])))
        inertia_scale = max(max(abs(value) for value in reference["centroidal_inertia_kg_m2"]), 1.0e-300)
        maximum["inertia_relative"] = max(
            maximum["inertia_relative"],
            max(abs(left - right) for left, right in zip(measured["centroidal_inertia_kg_m2"], reference["centroidal_inertia_kg_m2"])) / inertia_scale,
        )
        selectors = definition_by_id[reference["definition_id"]]["semantic_face_selectors"]
        measured_faces = _selector_records(solid, selectors)
        for selector in selectors:
            semantic_total += 1
            if _face_records_match(reference["semantic_faces"][selector], measured_faces[selector]):
                semantic_matched += 1
            else:
                semantic_failures.append({
                    "entity_kind": "instance",
                    "entity_id": reference["instance_id"],
                    "selector": selector,
                })
        rows.append({
            "instance_id": reference["instance_id"],
            "definition_id": reference["definition_id"],
            "region_id": reference["region_id"],
            "region_kind": reference["region_kind"],
            "material_id": reference["material_id"],
            "density_kg_m3": reference["density_kg_m3"],
            "step_path": reference["step_path"],
            "step_sha256": observed_hash,
            "valid": True,
            "solid_count": 1,
            "semantic_faces": measured_faces,
            **measured,
        })

    material_assembly_path = artifact_root / manifest["material_assembly"]["step_path"]
    void_assembly_path = artifact_root / manifest["void_assembly"]["step_path"]
    material_assembly = Part.Shape()
    material_assembly.read(str(material_assembly_path))
    void_assembly = Part.Shape()
    void_assembly.read(str(void_assembly_path))
    step_hash_match = (
        step_hash_match
        and _sha256(material_assembly_path) == manifest["material_assembly"]["step_sha256"]
        and _sha256(void_assembly_path) == manifest["void_assembly"]["step_sha256"]
    )

    fcstd_path.parent.mkdir(parents=True, exist_ok=True)
    raw_fcstd_path = fcstd_path.with_name(f"{fcstd_path.stem}.uncanonicalized.FCStd")
    if raw_fcstd_path.exists():
        raw_fcstd_path.unlink()
    document = App.newDocument("Work135NativeDetailedVehicle")
    try:
        for reference in sorted(manifest["instances"], key=lambda item: item["instance_id"]):
            instance_id = reference["instance_id"]
            if instance_id not in imported_shapes:
                continue
            obj = document.addObject("Part::Feature", instance_id)
            obj.Label = instance_id
            obj.Shape = imported_shapes[instance_id]
            obj.addProperty("App::PropertyString", "DefinitionId", "Work135")
            obj.DefinitionId = reference["definition_id"]
            obj.addProperty("App::PropertyString", "RegionId", "Work135")
            obj.RegionId = reference["region_id"]
            obj.addProperty("App::PropertyString", "MaterialId", "Work135")
            obj.MaterialId = reference["material_id"]
        document.recompute()
        # Save to a disposable name so FreeCAD cannot create timestamped
        # FCBak files beside an existing admitted witness.
        document.saveAs(str(raw_fcstd_path))
    finally:
        App.closeDocument(document.Name)
    _canonicalize_fcstd(raw_fcstd_path)
    os.replace(raw_fcstd_path, fcstd_path)

    survival = semantic_matched / semantic_total if semantic_total else 0.0
    thresholds = config["thresholds"]
    material_assembly_valid = material_assembly.isValid()
    void_assembly_valid = void_assembly.isValid()
    material_count_matches = len(material_assembly.Solids) == manifest["material_assembly"]["solid_count"]
    void_count_matches = len(void_assembly.Solids) == manifest["void_assembly"]["solid_count"]
    residuals_pass = (
        maximum["volume_relative"] <= thresholds["volume_relative"]
        and maximum["mass_relative"] <= thresholds["mass_relative"]
        and maximum["center_absolute_m"] <= thresholds["center_absolute_m"]
        and maximum["inertia_relative"] <= thresholds["inertia_relative"]
    )
    invalid_or_null = definition_invalid_or_null + instance_invalid_or_null
    inspection_passed = (
        invalid_or_null == 0
        and len(definition_rows) == len(manifest["definitions"])
        and len(rows) == len(manifest["instances"])
        and step_hash_match
        and material_assembly_valid
        and void_assembly_valid
        and material_count_matches
        and void_count_matches
        and residuals_pass
        and survival == 1.0
    )
    report = {
        "status": "passed" if inspection_passed else "failed_exact_import_gate",
        "candidate_id": manifest["candidate_id"],
        "freecad_version": ".".join(str(value) for value in App.Version()[:3]),
        "occt_version": App.ConfigGet("OCC_VERSION"),
        "hidden_geometry_repair": False,
        "step_hash_match": step_hash_match,
        "invalid_or_null_solids": invalid_or_null,
        "definition_invalid_or_null_solids": definition_invalid_or_null,
        "instance_invalid_or_null_solids": instance_invalid_or_null,
        "definitions": definition_rows,
        "instances": rows,
        "material_assembly": {
            "step_sha256": _sha256(material_assembly_path),
            "valid": material_assembly_valid,
            "solid_count": len(material_assembly.Solids),
        },
        "void_assembly": {
            "step_sha256": _sha256(void_assembly_path),
            "valid": void_assembly_valid,
            "solid_count": len(void_assembly.Solids),
        },
        "mass_properties": _aggregate(rows),
        "maximum_residuals": maximum,
        "semantic_selector_checks": semantic_total,
        "semantic_selector_matches": semantic_matched,
        "semantic_selector_failures": semantic_failures,
        "semantic_boundary_survival_rate": survival,
        "semantic_match_tolerances": {
            "area_absolute_or_relative": 1.0e-8,
            "position_absolute_m": 1.0e-7,
            "planar_bounds_absolute_m": 1.0e-7,
            "absolute_normal": 1.0e-7,
        },
        "fcstd_path": fcstd_path.name,
        "fcstd_sha256": _sha256(fcstd_path),
    }
    _write_json(output_path, report)
    if report["status"] != "passed":
        raise RuntimeError("FreeCAD exact no-repair import gate failed")
    print(json.dumps({
        "status": report["status"],
        "instance_count": len(rows),
        "material_solid_count": report["material_assembly"]["solid_count"],
        "void_solid_count": report["void_assembly"]["solid_count"],
        "mass_kg": report["mass_properties"]["mass_kg"],
        "maximum_residuals": maximum,
        "semantic_boundary_survival_rate": survival,
        "fcstd_sha256": report["fcstd_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
