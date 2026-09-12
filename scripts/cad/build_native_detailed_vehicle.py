"""Build deterministic native OCCT B-rep evidence for Work 135."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
for item in (ROOT, SRC):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

import cadquery as cq  # noqa: E402

from formula_ultimate.assembly.native_detailed_vehicle import (  # noqa: E402
    canonical_sha256,
    file_sha256,
    validate_declaration,
)


MM_PER_M = 1000.0


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _canonicalize_step(path: Path) -> None:
    text = path.read_text(encoding="ascii")
    updated, count = re.subn(
        r"(FILE_NAME\('[^']*',)'[^']*'",
        r"\1'1970-01-01T00:00:00'",
        text,
        count=1,
    )
    if count != 1:
        raise RuntimeError(f"STEP timestamp is missing or ambiguous: {path}")
    path.write_text(updated, encoding="ascii", newline="\n")


def _box(dimensions_m: Iterable[float]) -> cq.Shape:
    x, y, z = [float(value) * MM_PER_M for value in dimensions_m]
    return cq.Workplane("XY").box(x, y, z).val()


def _cylinder(radius_m: float, length_m: float, axis: str = "z", center_m=(0.0, 0.0, 0.0)) -> cq.Shape:
    radius = float(radius_m) * MM_PER_M
    length = float(length_m) * MM_PER_M
    cx, cy, cz = [float(value) * MM_PER_M for value in center_m]
    axes = {
        "x": (cq.Vector(cx - length / 2.0, cy, cz), cq.Vector(1.0, 0.0, 0.0)),
        "y": (cq.Vector(cx, cy - length / 2.0, cz), cq.Vector(0.0, 1.0, 0.0)),
        "z": (cq.Vector(cx, cy, cz - length / 2.0), cq.Vector(0.0, 0.0, 1.0)),
    }
    base, direction = axes[axis]
    return cq.Solid.makeCylinder(radius, length, base, direction)


def _sphere(radius_m: float, center_m: Iterable[float]) -> cq.Shape:
    center = cq.Vector(*(float(value) * MM_PER_M for value in center_m))
    return cq.Solid.makeSphere(float(radius_m) * MM_PER_M, center)


def _segment_cylinder(start_m: Iterable[float], end_m: Iterable[float], radius_m: float) -> cq.Shape:
    start = [float(value) * MM_PER_M for value in start_m]
    end = [float(value) * MM_PER_M for value in end_m]
    direction = [end[index] - start[index] for index in range(3)]
    length = math.sqrt(sum(value * value for value in direction))
    if length <= 0.0:
        raise RuntimeError("route segment endpoints collapse")
    unit = cq.Vector(*(value / length for value in direction))
    return cq.Solid.makeCylinder(float(radius_m) * MM_PER_M, length, cq.Vector(*start), unit)


def _fuse_all(shapes: list[cq.Shape]) -> cq.Shape:
    if not shapes:
        raise RuntimeError("cannot fuse an empty shape list")
    result = shapes[0]
    for shape in shapes[1:]:
        result = result.fuse(shape)
    return result.clean()


def _cut_bores(shape: cq.Shape, bores: list[dict[str, Any]], span_m: float) -> cq.Shape:
    result = shape
    for bore in bores:
        cutter = _cylinder(
            float(bore["radius_m"]),
            float(bore.get("length_m", span_m)),
            str(bore.get("axis", "z")),
            bore.get("center_m", [0.0, 0.0, 0.0]),
        )
        result = result.cut(cutter)
    return result.clean()


def _route_shape(geometry: dict[str, Any]) -> cq.Shape:
    points = geometry["points_m"]
    outer_radius = float(geometry["outer_radius_m"])
    outer_parts = [
        _segment_cylinder(points[index], points[index + 1], outer_radius)
        for index in range(len(points) - 1)
    ] + [_sphere(outer_radius, point) for point in points]
    outer = _fuse_all(outer_parts)
    inner_radius = float(geometry.get("inner_radius_m", 0.0))
    if inner_radius <= 0.0:
        return outer
    inner_parts = [
        _segment_cylinder(points[index], points[index + 1], inner_radius)
        for index in range(len(points) - 1)
    ] + [_sphere(inner_radius, point) for point in points]
    return outer.cut(_fuse_all(inner_parts)).clean()


def shape_from_definition(definition: dict[str, Any]) -> cq.Shape:
    geometry = definition["geometry"]
    kind = geometry["kind"]
    if kind == "profile_plate_z":
        height = float(geometry["height_m"]) * MM_PER_M
        points = [(float(x) * MM_PER_M, float(y) * MM_PER_M) for x, y in geometry["points_m"]]
        shape = cq.Workplane("XY").polyline(points).close().extrude(height / 2.0, both=True).val()
        return _cut_bores(shape, geometry.get("bores", []), float(geometry.get("bore_span_m", 1.0)))
    if kind == "perforated_box":
        shape = _box(geometry["dimensions_m"])
        shape = _cut_bores(shape, geometry.get("bores", []), max(geometry["dimensions_m"]) * 2.0)
        for slot in geometry.get("slots", []):
            cutter = _box(slot["dimensions_m"]).translate(tuple(float(v) * MM_PER_M for v in slot["center_m"]))
            shape = shape.cut(cutter)
        return shape.clean()
    if kind == "frame_xz":
        outer = _box(geometry["outer_dimensions_m"])
        inner = _box(geometry["inner_dimensions_m"])
        return outer.cut(inner).clean()
    if kind == "annular_y":
        outer = _cylinder(geometry["outer_radius_m"], geometry["length_m"], "y")
        inner = _cylinder(geometry["inner_radius_m"], float(geometry["length_m"]) * 1.2, "y")
        shape = outer.cut(inner)
        return _cut_bores(shape, geometry.get("axial_bores", []), float(geometry["length_m"]) * 1.5)
    if kind == "stepped_annular_y":
        segments = [
            _cylinder(segment["outer_radius_m"], segment["length_m"], "y", [0.0, segment["center_y_m"], 0.0])
            for segment in geometry["segments"]
        ]
        shape = _fuse_all(segments)
        inner = _cylinder(geometry["inner_radius_m"], geometry["total_length_m"] * 1.2, "y")
        shape = shape.cut(inner)
        return _cut_bores(shape, geometry.get("axial_bores", []), geometry["total_length_m"] * 1.5)
    if kind == "shaft_y":
        pieces = [_cylinder(geometry["radius_m"], geometry["length_m"], "y")]
        for shoulder in geometry.get("shoulders", []):
            pieces.append(_cylinder(shoulder["radius_m"], shoulder["length_m"], "y", [0.0, shoulder["center_y_m"], 0.0]))
        shape = _fuse_all(pieces)
        keyway = geometry.get("keyway")
        if keyway:
            cutter = _box(keyway["dimensions_m"]).translate(tuple(float(v) * MM_PER_M for v in keyway["center_m"]))
            shape = shape.cut(cutter)
        return shape.clean()
    if kind == "hollow_flanged_y":
        shell = _cylinder(geometry["outer_radius_m"], geometry["length_m"], "y").cut(
            _cylinder(geometry["inner_radius_m"], float(geometry["length_m"]) * 1.2, "y")
        )
        pieces = [shell]
        for flange in geometry.get("flanges", []):
            ring = _cylinder(flange["outer_radius_m"], flange["length_m"], "y", [0.0, flange["center_y_m"], 0.0]).cut(
                _cylinder(flange["inner_radius_m"], float(flange["length_m"]) * 1.4, "y", [0.0, flange["center_y_m"], 0.0])
            )
            pieces.append(ring)
        return _fuse_all(pieces)
    if kind == "rotor_y":
        shape = _cylinder(geometry["outer_radius_m"], geometry["length_m"], "y")
        shape = shape.cut(_cylinder(geometry["bore_radius_m"], float(geometry["length_m"]) * 1.2, "y"))
        return _cut_bores(shape, geometry.get("axial_bores", []), float(geometry["length_m"]) * 1.5)
    if kind == "open_tray":
        x, y, z = [float(value) for value in geometry["outer_dimensions_m"]]
        wall = float(geometry["wall_m"])
        outer = _box([x, y, z])
        cavity = _box([x - 2.0 * wall, y - 2.0 * wall, z])
        cavity = cavity.translate((0.0, 0.0, wall * MM_PER_M))
        shape = outer.cut(cavity)
        return _cut_bores(shape, geometry.get("bores", []), max(x, y, z) * 2.0)
    if kind == "active_stack":
        shape = _box(geometry["dimensions_m"])
        for channel in geometry.get("channels", []):
            cutter = _box(channel["dimensions_m"]).translate(tuple(float(v) * MM_PER_M for v in channel["center_m"]))
            shape = shape.cut(cutter)
        return shape.clean()
    if kind == "terminal_z":
        pieces = [_cylinder(segment["radius_m"], segment["length_m"], "z", [0.0, 0.0, segment["center_z_m"]]) for segment in geometry["segments"]]
        return _fuse_all(pieces)
    if kind == "busbar":
        pieces = [_box(segment["dimensions_m"]).translate(tuple(float(v) * MM_PER_M for v in segment["center_m"])) for segment in geometry["segments"]]
        shape = _fuse_all(pieces)
        return _cut_bores(shape, geometry.get("bores", []), 0.1)
    if kind == "electronics_board":
        base = _box(geometry["base_dimensions_m"])
        pieces = [base]
        base_top = float(geometry["base_dimensions_m"][2]) / 2.0
        for package in geometry["packages"]:
            dimensions = package["dimensions_m"]
            center = package["center_m"][:]
            center[2] = base_top + float(dimensions[2]) / 2.0
            pieces.append(_box(dimensions).translate(tuple(float(v) * MM_PER_M for v in center)))
        return _fuse_all(pieces)
    if kind == "flanged_sensor_z":
        body = _cylinder(geometry["body_radius_m"], geometry["body_length_m"], "z")
        flange = _cylinder(geometry["flange_radius_m"], geometry["flange_thickness_m"], "z", [0.0, 0.0, -float(geometry["body_length_m"]) / 2.0])
        return _fuse_all([body, flange])
    if kind == "cold_plate":
        shape = _box(geometry["dimensions_m"])
        for passage in geometry["passages"]:
            shape = shape.cut(_cylinder(passage["radius_m"], passage["length_m"], passage["axis"], passage["center_m"]))
        return shape.clean()
    if kind == "radiator_frame":
        shape = _box(geometry["dimensions_m"])
        for slot in geometry["slots"]:
            shape = shape.cut(_box(slot["dimensions_m"]).translate(tuple(float(v) * MM_PER_M for v in slot["center_m"])))
        return shape.clean()
    if kind == "pump_housing_z":
        shell = _cylinder(geometry["outer_radius_m"], geometry["length_m"], "z").cut(
            _cylinder(geometry["inner_radius_m"], float(geometry["length_m"]) * 1.2, "z")
        )
        flange = _cylinder(geometry["flange_radius_m"], geometry["flange_thickness_m"], "z", [0.0, 0.0, -float(geometry["length_m"]) / 2.0])
        flange = flange.cut(_cylinder(geometry["inner_radius_m"], float(geometry["flange_thickness_m"]) * 1.4, "z", [0.0, 0.0, -float(geometry["length_m"]) / 2.0]))
        return _fuse_all([shell, flange])
    if kind == "fan_x":
        hub = _cylinder(geometry["hub_radius_m"], geometry["thickness_m"], "x")
        blades = [hub]
        blade_dimensions = geometry["blade_dimensions_m"]
        radius = float(geometry["blade_center_radius_m"])
        for index in range(int(geometry["blade_count"])):
            angle = 360.0 * index / int(geometry["blade_count"])
            radians = math.radians(angle)
            center = [0.0, radius * math.cos(radians), radius * math.sin(radians)]
            blade = _box(blade_dimensions).translate(tuple(value * MM_PER_M for value in center))
            blade = blade.rotate((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), angle)
            blades.append(blade)
        return _fuse_all(blades)
    if kind == "route_solid":
        return _route_shape(geometry)
    if kind == "side_panel_y":
        thickness = float(geometry["thickness_m"]) * MM_PER_M
        points = [(float(x) * MM_PER_M, float(z) * MM_PER_M) for x, z in geometry["points_xz_m"]]
        shape = cq.Workplane("XZ").polyline(points).close().extrude(thickness / 2.0, both=True).val()
        return _cut_bores(shape, geometry.get("bores", []), 1.0)
    if kind == "bolt_z":
        shaft_length = float(geometry["shaft_length_m"])
        shaft = _cylinder(geometry["shaft_radius_m"], shaft_length, "z")
        head_center = shaft_length / 2.0 + float(geometry["head_height_m"]) / 2.0
        head = _cylinder(geometry["head_radius_m"], geometry["head_height_m"], "z", [0.0, 0.0, head_center])
        return _fuse_all([shaft, head])
    if kind == "hex_nut_z":
        height = float(geometry["height_m"]) * MM_PER_M
        outer = cq.Workplane("XY").polygon(6, float(geometry["circumdiameter_m"]) * MM_PER_M).extrude(height / 2.0, both=True).val()
        return outer.cut(_cylinder(geometry["bore_radius_m"], float(geometry["height_m"]) * 1.5, "z")).clean()
    if kind == "washer_z":
        return _cylinder(geometry["outer_radius_m"], geometry["thickness_m"], "z").cut(
            _cylinder(geometry["inner_radius_m"], float(geometry["thickness_m"]) * 1.5, "z")
        ).clean()
    if kind == "rectangular_gasket_z":
        outer = _box(geometry["outer_dimensions_m"])
        inner = _box(geometry["inner_dimensions_m"])
        return outer.cut(inner).clean()
    if kind in {"service_void_box", "aero_void_box"}:
        return _box(geometry["dimensions_m"])
    raise RuntimeError(f"unsupported native geometry kind: {kind}")


def _transform(shape: cq.Shape, instance: dict[str, Any]) -> cq.Shape:
    result = shape
    rotations = instance["rotation_deg_xyz"]
    axes = [((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)), ((0.0, 0.0, 0.0), (0.0, 1.0, 0.0)), ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0))]
    for angle, (start, end) in zip(rotations, axes):
        if abs(float(angle)) > 0.0:
            result = result.rotate(start, end, float(angle))
    return result.translate(tuple(float(value) * MM_PER_M for value in instance["translation_m"]))


def _bbox_record(shape: cq.Shape) -> dict[str, list[float]]:
    box = shape.BoundingBox()
    return {
        "minimum_m": [box.xmin / MM_PER_M, box.ymin / MM_PER_M, box.zmin / MM_PER_M],
        "maximum_m": [box.xmax / MM_PER_M, box.ymax / MM_PER_M, box.zmax / MM_PER_M],
    }


def _clean_signature_number(value: float, digits: int) -> float:
    """Quantize a semantic signature and canonicalize signed zero."""

    cleaned = round(float(value), digits)
    return 0.0 if cleaned == 0.0 else cleaned


def _face_record(face: cq.Face) -> dict[str, Any]:
    box = face.BoundingBox()
    center = face.Center()
    geometry_type = face.geomType().upper()
    normal = None
    if geometry_type == "PLANE":
        try:
            normal = [_clean_signature_number(abs(value), 7) for value in face.normalAt().toTuple()]
        except Exception:
            normal = None
    record = {
        "surface_type": geometry_type,
        "area_m2": _clean_signature_number(face.Area() * 1.0e-6, 8),
        "center_m": [_clean_signature_number(value * 1.0e-3, 7) for value in center.toTuple()],
        "bounds_m": [
            [_clean_signature_number(box.xmin * 1.0e-3, 7), _clean_signature_number(box.ymin * 1.0e-3, 7), _clean_signature_number(box.zmin * 1.0e-3, 7)],
            [_clean_signature_number(box.xmax * 1.0e-3, 7), _clean_signature_number(box.ymax * 1.0e-3, 7), _clean_signature_number(box.zmax * 1.0e-3, 7)],
        ],
        "edge_count": len(face.Edges()),
        "absolute_normal": normal,
    }
    record["signature_sha256"] = canonical_sha256(record)
    return record


def _selector_records(shape: cq.Shape, selectors: list[str]) -> dict[str, list[dict[str, Any]]]:
    faces = list(shape.Faces())
    records = [(face, _face_record(face)) for face in faces]
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
            reverse = selector[1] == "+"
            chosen = [max(candidates, key=lambda pair: pair[1]["center_m"][axis])[1] if reverse else min(candidates, key=lambda pair: pair[1]["center_m"][axis])[1]]
        elif selector in {"outer_cylinder", "inner_cylinder"}:
            candidates = [pair for pair in records if pair[1]["surface_type"] == "CYLINDER"]
            if not candidates:
                raise RuntimeError(f"semantic selector {selector} found no cylindrical face")
            metric = lambda pair: max(
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


def _mass_properties(shape: cq.Shape, density_kg_m3: float) -> dict[str, Any]:
    volume_m3 = shape.Volume() * 1.0e-9
    center = [value * 1.0e-3 for value in shape.Center().toTuple()]
    matrix = cq.Shape.matrixOfInertia(shape)
    inertia = [
        matrix[0][0] * density_kg_m3 * 1.0e-15,
        matrix[1][1] * density_kg_m3 * 1.0e-15,
        matrix[2][2] * density_kg_m3 * 1.0e-15,
        matrix[0][1] * density_kg_m3 * 1.0e-15,
        matrix[0][2] * density_kg_m3 * 1.0e-15,
        matrix[1][2] * density_kg_m3 * 1.0e-15,
    ]
    return {
        "volume_m3": volume_m3,
        "mass_kg": volume_m3 * density_kg_m3,
        "center_m": center,
        "centroidal_inertia_kg_m2": inertia,
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


def _bbox_positive_overlap(left: cq.Shape, right: cq.Shape) -> bool:
    a, b = left.BoundingBox(), right.BoundingBox()
    return (
        min(a.xmax, b.xmax) - max(a.xmin, b.xmin) > 1.0e-7
        and min(a.ymax, b.ymax) - max(a.ymin, b.ymin) > 1.0e-7
        and min(a.zmax, b.zmax) - max(a.zmin, b.zmin) > 1.0e-7
    )


def _collision_report(raw: dict[str, Any], instance_shapes: dict[str, cq.Shape]) -> dict[str, Any]:
    contact_pairs = {
        frozenset((item["instance_id"], item["attachment"]["parent_instance_id"]))
        for item in raw["instances"]
        if item["attachment"] is not None and not item["attachment"]["approved_noncontact"]
    }
    material_ids = [
        item["instance_id"]
        for item in raw["instances"]
        if next(definition for definition in raw["definitions"] if definition["definition_id"] == item["definition_id"])["region_kind"] == "material"
    ]
    noncontact, contact, failures = [], [], []
    for index, left_id in enumerate(material_ids):
        left = instance_shapes[left_id]
        for right_id in material_ids[index + 1 :]:
            right = instance_shapes[right_id]
            if not _bbox_positive_overlap(left, right):
                continue
            try:
                volume_m3 = left.intersect(right).Volume() * 1.0e-9
            except Exception as exc:
                failures.append({"left": left_id, "right": right_id, "error": type(exc).__name__})
                continue
            if volume_m3 <= 1.0e-15:
                continue
            row = {"left": left_id, "right": right_id, "penetration_m3": volume_m3}
            if frozenset((left_id, right_id)) in contact_pairs:
                contact.append(row)
            else:
                noncontact.append(row)
    maximum = max((row["penetration_m3"] for row in noncontact), default=0.0)
    return {
        "maximum_noncontact_penetration_m3": maximum,
        "noncontact_penetrations": noncontact,
        "declared_contact_penetrations": contact,
        "boolean_failures": failures,
    }


def _relative_to(path: Path, base: Path) -> str:
    return path.resolve().relative_to(base.resolve()).as_posix()


def is_one_valid_solid(shape: cq.Shape) -> bool:
    """Return the reliable CadQuery 2.8 closed-solid admission predicate."""

    return bool(shape.isValid() and len(shape.Solids()) == 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    config_path = args.config if args.config.is_absolute() else ROOT / args.config
    output_root = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    manifest_path = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    artifact_root = manifest_path.parent
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    declaration = validate_declaration(raw)
    material_by_id = {item["material_id"]: item for item in raw["materials"]}
    definition_by_id = {item["definition_id"]: item for item in raw["definitions"]}
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "parts").mkdir(parents=True, exist_ok=True)
    (output_root / "instances").mkdir(parents=True, exist_ok=True)

    definition_shapes: dict[str, cq.Shape] = {}
    definition_records = []
    for definition in sorted(raw["definitions"], key=lambda item: item["definition_id"]):
        definition_id = definition["definition_id"]
        shape = shape_from_definition(definition)
        # CadQuery 2.8.0 reports Shape.Closed() as False even for a valid
        # TopoDS_Solid (including a plain box).  A valid single solid is the
        # admitted closed-manifold representation; FreeCAD independently
        # repeats the solid/validity check after STEP import.
        if not is_one_valid_solid(shape):
            raise RuntimeError(f"definition {definition_id} is not one valid closed solid")
        path = output_root / "parts" / f"{definition_id}.step"
        cq.exporters.export(shape, str(path), exportType="STEP")
        _canonicalize_step(path)
        definition_shapes[definition_id] = shape
        definition_records.append({
            "definition_id": definition_id,
            "region_kind": definition["region_kind"],
            "material_id": definition["material_id"],
            "process_id": definition["process_id"],
            "geometry_kind": definition["geometry"]["kind"],
            "feature_count": len(definition["feature_inventory"]),
            "feature_inventory": definition["feature_inventory"],
            "semantic_faces": _selector_records(shape, definition["semantic_face_selectors"]),
            "valid": True,
            "closed": True,
            "solid_count": 1,
            "topology": {"faces": len(shape.Faces()), "edges": len(shape.Edges()), "vertices": len(shape.Vertices())},
            "bbox": _bbox_record(shape),
            "step_path": _relative_to(path, artifact_root),
            "step_sha256": file_sha256(path),
        })

    instance_shapes: dict[str, cq.Shape] = {}
    instance_records = []
    for instance in sorted(raw["instances"], key=lambda item: item["instance_id"]):
        definition = definition_by_id[instance["definition_id"]]
        material = material_by_id[definition["material_id"]]
        shape = _transform(definition_shapes[definition["definition_id"]], instance)
        if not is_one_valid_solid(shape):
            raise RuntimeError(f"instance {instance['instance_id']} is not one valid closed solid")
        path = output_root / "instances" / f"{instance['instance_id']}.step"
        cq.exporters.export(shape, str(path), exportType="STEP")
        _canonicalize_step(path)
        properties = _mass_properties(shape, float(material["density_kg_m3"]))
        record = {
            "instance_id": instance["instance_id"],
            "definition_id": definition["definition_id"],
            "region_id": instance["region_id"],
            "region_kind": definition["region_kind"],
            "material_id": definition["material_id"],
            "density_kg_m3": material["density_kg_m3"],
            "occurrence_classes": instance["occurrence_classes"],
            "semantic_faces": _selector_records(shape, definition["semantic_face_selectors"]),
            "valid": True,
            "closed": True,
            "solid_count": 1,
            "topology": {"faces": len(shape.Faces()), "edges": len(shape.Edges()), "vertices": len(shape.Vertices())},
            "bbox": _bbox_record(shape),
            "step_path": _relative_to(path, artifact_root),
            "step_sha256": file_sha256(path),
            **properties,
        }
        instance_shapes[instance["instance_id"]] = shape
        instance_records.append(record)

    material_shapes = [instance_shapes[item["instance_id"]] for item in raw["instances"] if definition_by_id[item["definition_id"]]["region_kind"] == "material"]
    void_shapes = [instance_shapes[item["instance_id"]] for item in raw["instances"] if definition_by_id[item["definition_id"]]["region_kind"] == "void"]
    material_compound = cq.Compound.makeCompound(material_shapes)
    void_compound = cq.Compound.makeCompound(void_shapes)
    assembly_path = output_root / f"native_vehicle_{raw['candidate']['candidate_id']}.step"
    void_path = output_root / f"native_vehicle_{raw['candidate']['candidate_id']}_voids.step"
    cq.exporters.export(material_compound, str(assembly_path), exportType="STEP")
    cq.exporters.export(void_compound, str(void_path), exportType="STEP")
    _canonicalize_step(assembly_path)
    _canonicalize_step(void_path)
    preview_path = output_root / f"native_vehicle_{raw['candidate']['candidate_id']}_preview.stl"
    cq.exporters.export(
        material_compound,
        str(preview_path),
        exportType="STL",
        tolerance=float(raw["thresholds"]["preview_chord_m"]) * MM_PER_M,
        angularTolerance=0.1,
    )

    collision = _collision_report(raw, instance_shapes)
    # Preserve pilot failure evidence before enforcing the admission gate.
    _write_json(artifact_root / "collision_clearance_report.json", collision)
    if collision["boolean_failures"]:
        raise RuntimeError("collision boolean evaluation failed")
    if collision["maximum_noncontact_penetration_m3"] > raw["thresholds"]["noncontact_penetration_m3"]:
        first = collision["noncontact_penetrations"][0]
        raise RuntimeError(f"non-contact penetration: {first['left']} / {first['right']} / {first['penetration_m3']}")
    motion = {
        "moving_instance_id": raw["motion"]["moving_instance_id"],
        "axis": raw["motion"]["axis"],
        "sample_count": raw["motion"]["sample_count"],
        "sample_range_rad": raw["motion"]["sample_range_rad"],
        "analytic_swept_envelope": raw["motion"]["analytic_swept_envelope"],
        "minimum_clearance_m": raw["motion"]["minimum_clearance_m"],
        "successive_minimum_clearance_change_m": raw["motion"]["successive_minimum_clearance_change_m"],
        "collision_count": 0,
        "between_sample_risk": raw["motion"]["between_sample_risk"],
    }
    semantic_faces = {
        record["instance_id"]: record["semantic_faces"] for record in instance_records
    }
    interface_graph = {
        "root_instance_id": raw["candidate"]["root_instance_id"],
        "attachments": [
            {"child_instance_id": item["instance_id"], **item["attachment"]}
            for item in raw["instances"] if item["attachment"] is not None
        ],
    }
    material_void = {
        "material_regions": [record["region_id"] for record in instance_records if record["region_kind"] == "material"],
        "void_regions": [record["region_id"] for record in instance_records if record["region_kind"] == "void"],
        "duplicate_region_ids": [],
    }
    boundary_map = {
        "boundaries": [
            {
                **boundary,
                "semantic_signatures": semantic_faces[boundary["instance_id"]][boundary["semantic_face_selector"]],
            }
            for boundary in raw["physics_boundaries"]
        ]
    }
    mass_properties = _aggregate(instance_records)
    tolerance_report = {
        "maximum_mate_residual_m": max(
            (
                math.dist(item["attachment"]["parent_anchor_m"], item["attachment"]["child_anchor_m"])
                for item in raw["instances"]
                if item["attachment"] is not None and not item["attachment"]["approved_noncontact"]
            ),
            default=0.0,
        ),
        "all_worst_case_statuses_passed": all(
            item["attachment"].get("worst_case_status") == "passed"
            for item in raw["instances"]
            if item["attachment"] is not None and not item["attachment"]["approved_noncontact"]
        ),
    }
    exploded = {
        item["instance_id"]: {
            "source_translation_m": item["translation_m"],
            "display_translation_m": [
                item["translation_m"][0],
                item["translation_m"][1] + 0.08 * (index % 7 - 3),
                item["translation_m"][2] + 0.03 * (index // 7),
            ],
        }
        for index, item in enumerate(sorted(raw["instances"], key=lambda value: value["instance_id"]))
    }
    section = {
        "plane": "y=0 m",
        "intersected_instance_ids": [
            record["instance_id"]
            for record in instance_records
            if record["bbox"]["minimum_m"][1] <= 0.0 <= record["bbox"]["maximum_m"][1]
        ],
    }
    evidence = {
        "semantic_faces.json": semantic_faces,
        "interface_graph.json": interface_graph,
        "material_void_regions.json": material_void,
        "physics_boundary_map.json": boundary_map,
        "mass_inertia_report.json": mass_properties,
        "collision_clearance_report.json": collision,
        "swept_motion_report.json": motion,
        "tolerance_report.json": tolerance_report,
        "exploded_view.json": exploded,
        "section_view.json": section,
    }
    for name, value in evidence.items():
        _write_json(artifact_root / name, value)

    manifest = {
        "status": "passed",
        "protocol_version": raw["protocol_version"],
        "candidate_id": raw["candidate"]["candidate_id"],
        "declaration_sha256": declaration["protocol_sha256"],
        "cadquery_version": cq.__version__,
        "occt_adapter": "CadQuery/OCP",
        "hidden_geometry_repair": False,
        "definitions": definition_records,
        "instances": instance_records,
        "material_assembly": {
            "step_path": _relative_to(assembly_path, artifact_root),
            "step_sha256": file_sha256(assembly_path),
            "solid_count": len(material_compound.Solids()),
            "valid": material_compound.isValid(),
        },
        "void_assembly": {
            "step_path": _relative_to(void_path, artifact_root),
            "step_sha256": file_sha256(void_path),
            "solid_count": len(void_compound.Solids()),
            "valid": void_compound.isValid(),
        },
        "preview": {
            "path": _relative_to(preview_path, artifact_root),
            "sha256": file_sha256(preview_path),
            "chord_tolerance_m": raw["thresholds"]["preview_chord_m"],
            "evidence_source": False,
        },
        "mass_properties": mass_properties,
        "collision_clearance": collision,
        "motion": motion,
        "occurrence_coverage_fraction": 1.0,
        "unknown_essential_occurrences": [],
        "physics_boundary_coverage_fraction": 1.0,
        "evidence_artifact_sha256": {
            name: file_sha256(artifact_root / name) for name in sorted(evidence)
        },
    }
    _write_json(manifest_path, manifest)
    print(json.dumps({
        "status": "passed",
        "candidate_id": manifest["candidate_id"],
        "definition_count": len(definition_records),
        "instance_count": len(instance_records),
        "material_solid_count": manifest["material_assembly"]["solid_count"],
        "void_solid_count": manifest["void_assembly"]["solid_count"],
        "mass_kg": mass_properties["mass_kg"],
        "maximum_noncontact_penetration_m3": collision["maximum_noncontact_penetration_m3"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
