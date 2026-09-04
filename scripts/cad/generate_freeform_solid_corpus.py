#!/usr/bin/env python3
"""Execute Work 092 declarations and export deterministic STEP evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

import cadquery as cq  # noqa: E402

from formula_ultimate.components.freeform_solid_grammar import (  # noqa: E402
    canonical_bytes,
    validate_solid_grammar,
)
from formula_ultimate.components.freeform_wire_grammar import (  # noqa: E402
    declaration_sha256 as wire_declaration_sha256,
    validate_grammar as validate_wire_grammar,
)
from scripts.cad.generate_freeform_wire_corpus import execute_loop  # noqa: E402

MM = 1000.0


class SolidExecutionError(RuntimeError):
    """Raised when an admitted declaration fails in the CAD kernel."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def canonicalize_step(path: Path) -> None:
    text = path.read_text(encoding="ascii", errors="strict")
    updated, count = re.subn(r"(FILE_NAME\('[^']*',)'[^']*'", r"\1'1970-01-01T00:00:00'", text, count=1)
    if count != 1:
        raise SolidExecutionError("STEP timestamp is missing or ambiguous")
    path.write_text(updated, encoding="ascii", newline="\n")


def vector(point: list[float]) -> cq.Vector:
    return cq.Vector(*(item * MM for item in point))


def _transform(shape, translation: list[float], axis_start: list[float], axis_end: list[float], angle_rad: float):
    result = shape.rotate(vector(axis_start), vector(axis_end), math.degrees(angle_rad)) if angle_rad else shape
    return result.translate(vector(translation)) if any(translation) else result


def _section(profile: dict[str, Any], parameters: dict[str, Any]) -> dict[str, Any]:
    wires = [execute_loop(loop, profile) for loop in profile["loops"]]
    result = []
    for wire in wires:
        transformed = wire.scale(parameters["scale"])
        if parameters["rotation_rad"]:
            transformed = transformed.rotate((0, 0, 0), (0, 0, 1), math.degrees(parameters["rotation_rad"]))
        if any(parameters["translation_m"]):
            transformed = transformed.translate(vector(parameters["translation_m"]))
        result.append(transformed)
    return {"kind": "section", "outer": result[0], "inners": result[1:]}


def _path(parameters: dict[str, Any]) -> dict[str, Any]:
    points = [vector(item) for item in parameters["points_m"]]
    if parameters["path_kind"] == "spline":
        path = cq.Edge.makeSpline(points)
    else:
        path = cq.Wire.assembleEdges([cq.Edge.makeLine(a, b) for a, b in zip(points, points[1:])])
    return {"kind": "path", "shape": path}


def _tool_box(parameters: dict[str, Any]) -> cq.Solid:
    size = [item * MM for item in parameters["size_m"]]
    center = [item * MM for item in parameters["center_m"]]
    origin = tuple(center[index] - size[index] / 2 for index in range(3))
    return cq.Solid.makeBox(*size, origin)


def _gusset(parameters: dict[str, Any]) -> cq.Solid:
    sx, sy, sz = (item * MM for item in parameters["size_m"])
    cx, cy, cz = (item * MM for item in parameters["center_m"])
    face = cq.Face.makeFromWires(cq.Wire.makePolygon([
        (cx - sx / 2, cy - sy / 2, cz - sz / 2),
        (cx + sx / 2, cy - sy / 2, cz - sz / 2),
        (cx - sx / 2, cy + sy / 2, cz - sz / 2),
        (cx - sx / 2, cy - sy / 2, cz - sz / 2),
    ]))
    solid = cq.Solid.extrudeLinear(face.outerWire(), [], (0, 0, sz))
    if parameters["axis"] == "x":
        solid = solid.rotate((cx, cy, cz), (cx, cy + 1, cz), 90)
    elif parameters["axis"] == "y":
        solid = solid.rotate((cx, cy, cz), (cx + 1, cy, cz), -90)
    return solid


def _axis_edges(shape: cq.Shape, axis: str) -> list[cq.Edge]:
    index = {"x": 0, "y": 1, "z": 2}[axis]
    matches = []
    for edge in shape.Edges():
        vertices = edge.Vertices()
        if edge.geomType() != "LINE" or len(vertices) != 2:
            continue
        a = vertices[0].Center().toTuple(); b = vertices[1].Center().toTuple()
        delta = [abs(a[item] - b[item]) for item in range(3)]
        if delta[index] > 1e-6 and max(delta[item] for item in range(3) if item != index) < 1e-6:
            matches.append(edge)
    if not matches:
        raise SolidExecutionError(f"geometry-signature selector found no {axis}-parallel edges")
    return matches


def _extreme_faces(shape: cq.Shape, axis: str, side: str) -> list[cq.Face]:
    index = {"x": 0, "y": 1, "z": 2}[axis]
    faces = list(shape.Faces())
    values = [face.Center().toTuple()[index] for face in faces]
    extreme = (min if side == "min" else max)(values)
    selected = [face for face, value in zip(faces, values) if abs(value - extreme) <= 1e-7]
    if not selected:
        raise SolidExecutionError("extreme-face signature selected nothing")
    return selected


def _solid_state(shape: cq.Shape) -> dict[str, Any]:
    if shape.isNull() or not shape.isValid() or not math.isfinite(shape.Volume()) or shape.Volume() <= 0.0:
        raise SolidExecutionError("operation produced invalid, empty, or non-finite geometry")
    return {"kind": "solid", "shape": shape}


def execute_candidate(candidate: dict[str, Any], profiles: dict[str, dict[str, Any]]) -> tuple[cq.Shape, list[dict[str, Any]]]:
    states: dict[str, dict[str, Any]] = {}
    trace = []
    for feature in candidate["features"]:
        operator = feature["operator"]
        parameters = feature["parameters"]
        inputs = [states[item] for item in feature["inputs"]]
        if operator == "section":
            state = _section(profiles[parameters["profile_id"]], parameters)
        elif operator == "path":
            state = _path(parameters)
        elif operator == "extrude":
            section = inputs[0]
            state = _solid_state(cq.Solid.extrudeLinear(section["outer"], section["inners"], vector(parameters["vector_m"]), math.degrees(parameters["taper_rad"])))
        elif operator == "revolve":
            section = inputs[0]
            state = _solid_state(cq.Solid.revolve(section["outer"], section["inners"], math.degrees(parameters["angle_rad"]), vector(parameters["axis_start_m"]), vector(parameters["axis_end_m"])))
        elif operator == "sweep":
            section, path = inputs
            state = _solid_state(cq.Solid.sweep(section["outer"], section["inners"], path["shape"], True, parameters["is_frenet"], transitionMode=parameters["transition_mode"]))
        elif operator == "loft":
            state = _solid_state(cq.Solid.makeLoft([item["outer"] for item in inputs], parameters["ruled"]))
        else:
            base = inputs[0]["shape"]
            if operator == "shell":
                bounds = base.BoundingBox()
                minimum_span = min(bounds.xlen, bounds.ylen, bounds.zlen)
                if 2.0 * parameters["thickness_m"] * MM >= minimum_span:
                    raise SolidExecutionError("shell thickness would self-erase the source body")
                faces = _extreme_faces(base, parameters["opening_axis"], parameters["opening_side"])
                shape = base.hollow(faces, -parameters["thickness_m"] * MM, kind=parameters["kind"])
            elif operator == "rib_web":
                shape = base.fuse(_tool_box(parameters))
            elif operator == "gusset":
                shape = base.fuse(_gusset(parameters))
            elif operator == "pocket":
                shape = base.cut(_tool_box(parameters))
            elif operator == "bore":
                direction = vector(parameters["direction"]).normalized()
                tool = cq.Solid.makeCylinder(parameters["radius_m"] * MM, parameters["length_m"] * MM, vector(parameters["origin_m"]), direction)
                shape = base.cut(tool)
            elif operator == "linear_pattern":
                axis = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[parameters["direction"]]
                copies = [base.translate(tuple(axis[item] * parameters["spacing_m"] * MM * count for item in range(3))) for count in range(parameters["count"])]
                shape = copies[0]
                for copy in copies[1:]:
                    shape = shape.fuse(copy) if parameters["fuse"] else cq.Compound.makeCompound([shape, copy])
            elif operator == "fillet":
                shape = base.fillet(parameters["radius_m"] * MM, _axis_edges(base, parameters["selector_axis"]))
            elif operator == "chamfer":
                shape = base.chamfer(parameters["distance_m"] * MM, None, _axis_edges(base, parameters["selector_axis"]))
            elif operator == "boolean_union":
                shape = base
                for item in inputs[1:]: shape = shape.fuse(item["shape"])
            elif operator == "boolean_subtract":
                shape = base.cut(inputs[1]["shape"])
            elif operator == "boolean_intersect":
                shape = base.intersect(inputs[1]["shape"])
            elif operator == "transform":
                shape = _transform(base, parameters["translation_m"], parameters["axis_start_m"], parameters["axis_end_m"], parameters["angle_rad"])
            else:  # pragma: no cover - declaration validator blocks this
                raise SolidExecutionError(f"unsupported operator {operator}")
            state = _solid_state(shape)
        states[feature["feature_id"]] = state
        shape = state.get("shape")
        trace.append({"feature_id": feature["feature_id"], "operator": operator, "kind": state["kind"], "solid_count": len(shape.Solids()) if shape is not None else 0})
    final = states[candidate["final_feature_id"]]["shape"]
    solid_count = len(final.Solids())
    if solid_count != candidate["expected_body_count"]:
        raise SolidExecutionError(f"final body policy failed for {candidate['candidate_id']}: {solid_count}")
    return final, trace


def derived_datums(shape: cq.Shape, declarations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    bounds = shape.BoundingBox()
    minimum = [bounds.xmin / MM, bounds.ymin / MM, bounds.zmin / MM]
    maximum = [bounds.xmax / MM, bounds.ymax / MM, bounds.zmax / MM]
    center = [(a + b) / 2 for a, b in zip(minimum, maximum)]
    spans = [b - a for a, b in zip(minimum, maximum)]
    longest = max(range(3), key=lambda index: (spans[index], -index))
    result = []
    for datum in declarations:
        if datum["kind"] == "bbox_center":
            value = {"point_m": center}
        elif datum["kind"] == "longest_bbox_axis":
            direction = [0.0, 0.0, 0.0]; direction[longest] = 1.0
            value = {"origin_m": center, "direction": direction}
        else:
            axis = {"x": 0, "y": 1, "z": 2}[datum["parameters"]["axis"]]
            origin = list(center); origin[axis] = minimum[axis] if datum["parameters"]["side"] == "min" else maximum[axis]
            normal = [0.0, 0.0, 0.0]; normal[axis] = -1.0 if datum["parameters"]["side"] == "min" else 1.0
            value = {"origin_m": origin, "normal": normal}
        result.append({"datum_id": datum["datum_id"], "kind": datum["kind"], **value})
    return result


def _relative(reference: float, measured: float) -> float:
    return abs(reference - measured) / max(abs(reference), abs(measured), 1e-18)


def _datum_residual(expected: list[dict[str, Any]], measured: list[dict[str, Any]]) -> float:
    if [(item["datum_id"], item["kind"]) for item in expected] != [(item["datum_id"], item["kind"]) for item in measured]:
        raise SolidExecutionError("datum identity or kind mismatch")
    maximum = 0.0
    for reference, witness in zip(expected, measured):
        if set(reference) != set(witness):
            raise SolidExecutionError("datum witness schema mismatch")
        for field in set(reference) - {"datum_id", "kind"}:
            reference_values = reference[field]; measured_values = witness[field]
            if len(reference_values) != len(measured_values):
                raise SolidExecutionError("datum witness vector length mismatch")
            maximum = max(maximum, *(abs(float(a) - float(b)) for a, b in zip(reference_values, measured_values)))
    return maximum


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--wire-config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--freecad-python", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()
    if args.output_root.exists() and any(args.output_root.iterdir()):
        raise SystemExit("output-root must be absent or empty")
    args.output_root.mkdir(parents=True, exist_ok=True)
    wire_raw = json.loads(args.wire_config.read_text(encoding="utf-8"))
    validate_wire_grammar(wire_raw)
    raw = json.loads(args.config.read_text(encoding="utf-8"))
    if raw["source_wire_declaration_sha256"] != wire_declaration_sha256(wire_raw):
        raise SolidExecutionError("source wire declaration identity mismatch")
    profiles = {item["profile_id"]: item for item in wire_raw["profiles"]}
    validation = validate_solid_grammar(raw, set(profiles))
    records = []
    for candidate in raw["candidates"]:
        shape, trace = execute_candidate(candidate, profiles)
        path = args.output_root / f"{candidate['candidate_id']}.step"
        cq.exporters.export(shape, str(path), exportType="STEP")
        canonicalize_step(path)
        bounds = shape.BoundingBox(); center = shape.Center()
        records.append({
            "candidate_id": candidate["candidate_id"], "family": candidate["family"],
            "step_file": path.name, "step_sha256": sha256(path), "valid": shape.isValid(),
            "solid_count": len(shape.Solids()), "face_count": len(shape.Faces()), "edge_count": len(shape.Edges()),
            "curved_face_count": sum(face.geomType() != "PLANE" for face in shape.Faces()),
            "volume_m3": shape.Volume() * 1e-9, "surface_area_m2": shape.Area() * 1e-6,
            "center_m": [center.x / MM, center.y / MM, center.z / MM],
            "bounding_box_m": {"minimum": [bounds.xmin / MM, bounds.ymin / MM, bounds.zmin / MM], "maximum": [bounds.xmax / MM, bounds.ymax / MM, bounds.zmax / MM]},
            "datum_declarations": candidate["datums"],
            "datums": derived_datums(shape, candidate["datums"]), "trace": trace,
        })
    manifest_body = {"grammar_version": raw["grammar_version"], "declaration_sha256": validation["declaration_sha256"], "source_wire_declaration_sha256": raw["source_wire_declaration_sha256"], "validation": validation, "candidates": records, "hidden_geometry_repair": False}
    manifest = {**manifest_body, "manifest_sha256": hashlib.sha256(canonical_bytes(manifest_body)).hexdigest()}
    manifest_path = args.output_root / "manifest.json"; write_json(manifest_path, manifest)
    report_path = args.output_root / "freecad_report.json"; fcstd_path = args.output_root / "freeform_solid_corpus_v2.FCStd"
    environment = os.environ.copy(); environment.update({"FORMULA_ULTIMATE_W092_MANIFEST": str(manifest_path.resolve()), "FORMULA_ULTIMATE_W092_STEP_ROOT": str(args.output_root.resolve()), "FORMULA_ULTIMATE_W092_REPORT": str(report_path.resolve()), "FORMULA_ULTIMATE_W092_FCSTD": str(fcstd_path.resolve())})
    process = subprocess.run([str(args.freecad_python), str(ROOT / "scripts/cad/inspect_freeform_solid_corpus_freecad.py")], cwd=ROOT, env=environment, text=True, capture_output=True)
    if process.returncode:
        raise SolidExecutionError(process.stderr or process.stdout)
    freecad = json.loads(report_path.read_text(encoding="utf-8")); by_id = {item["candidate_id"]: item for item in freecad["candidates"]}
    max_volume = max_area = max_position = 0.0
    for expected in records:
        measured = by_id.get(expected["candidate_id"])
        if measured is None or any(measured[field] != expected[field] for field in ("solid_count", "face_count", "edge_count")):
            raise SolidExecutionError(f"FreeCAD topology mismatch for {expected['candidate_id']}")
        volume = _relative(expected["volume_m3"], measured["volume_m3"]); area = _relative(expected["surface_area_m2"], measured["surface_area_m2"])
        positions = [abs(a - b) for a, b in zip(expected["center_m"], measured["center_m"])]
        positions += [abs(a - b) for end in ("minimum", "maximum") for a, b in zip(expected["bounding_box_m"][end], measured["bounding_box_m"][end])]
        datum_position = _datum_residual(expected["datums"], measured["datums"])
        max_volume = max(max_volume, volume); max_area = max(max_area, area); max_position = max(max_position, *positions, datum_position)
        if volume > raw["limits"]["measurement_relative_tolerance"] or area > raw["limits"]["measurement_relative_tolerance"] or max(*positions, datum_position) > raw["limits"]["position_absolute_tolerance_m"]:
            raise SolidExecutionError(f"FreeCAD metric or datum mismatch for {expected['candidate_id']}")
    result_body = {"status": "passed", "candidate_count": len(records), "family_count": len(validation["family_coverage"]), "operator_coverage": validation["operator_coverage"], "declaration_sha256": validation["declaration_sha256"], "manifest_sha256": manifest["manifest_sha256"], "freecad_report_sha256": freecad["report_sha256"], "step_sha256": {item["candidate_id"]: item["step_sha256"] for item in records}, "maximum_volume_relative_difference": max_volume, "maximum_area_relative_difference": max_area, "maximum_position_absolute_difference_m": max_position, "hidden_geometry_repair": False}
    result = {**result_body, "result_sha256": hashlib.sha256(canonical_bytes(result_body)).hexdigest()}; write_json(args.output_root / "result.json", result)
    if args.replay_reference:
        reference = json.loads(args.replay_reference.read_text(encoding="utf-8")); exact = reference == result
        write_json(args.output_root / "replay.json", {"status": "passed" if exact else "failed", "exact": exact, "reference_result_sha256": reference.get("result_sha256"), "replay_result_sha256": result["result_sha256"]})
        if not exact: raise SolidExecutionError("replay mismatch")
    print(json.dumps({"status": "passed", "candidate_count": len(records), "manifest_sha256": manifest["manifest_sha256"], "result_sha256": result["result_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
