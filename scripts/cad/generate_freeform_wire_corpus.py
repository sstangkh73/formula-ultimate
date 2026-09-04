#!/usr/bin/env python3
"""Execute Work 091 free-form profiles and export deterministic STEP evidence."""
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

import cadquery as cq  # noqa: E402

from formula_ultimate.components.freeform_wire_grammar import (  # noqa: E402
    canonical_bytes, compare_measurement_witnesses, declaration_sha256, validate_grammar,
)

MM = 1000.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def canonicalize_step(path: Path) -> None:
    text = path.read_text(encoding="ascii", errors="strict")
    updated, count = re.subn(r"(FILE_NAME\('[^']*',)'[^']*'", r"\1'1970-01-01T00:00:00'", text, count=1)
    if count != 1:
        raise RuntimeError("STEP timestamp is missing or ambiguous")
    path.write_text(updated, encoding="ascii", newline="\n")


def vector(point: list[float]) -> cq.Vector:
    return cq.Vector(point[0] * MM, point[1] * MM, 0.0)


def segment_edges(segment: dict[str, Any]) -> list[cq.Edge]:
    operator, parameters = segment["operator"], segment["parameters"]
    if operator == "line":
        edges = [cq.Edge.makeLine(vector(parameters["start_m"]), vector(parameters["end_m"]))]
    elif operator == "polyline":
        points = [vector(item) for item in parameters["points_m"]]
        edges = [cq.Edge.makeLine(points[index], points[index + 1]) for index in range(len(points) - 1)]
    elif operator == "tangent_arc":
        edges = [cq.Edge.makeTangentArc(vector(parameters["start_m"]), vector(parameters["tangent"]), vector(parameters["end_m"]))]
    elif operator == "three_point_arc":
        edges = [cq.Edge.makeThreePointArc(vector(parameters["start_m"]), vector(parameters["mid_m"]), vector(parameters["end_m"]))]
    elif operator == "circle":
        edges = [cq.Edge.makeCircle(parameters["radius_m"] * MM, vector(parameters["center_m"]))]
    elif operator == "ellipse":
        edge = cq.Edge.makeEllipse(parameters["radii_m"][0] * MM, parameters["radii_m"][1] * MM, vector(parameters["center_m"]))
        edges = [edge.rotate((0, 0, 0), (0, 0, 1), math.degrees(parameters["rotation_rad"]))]
    elif operator == "bezier":
        edges = [cq.Edge.makeBezier([vector(item) for item in parameters["control_points_m"]])]
    elif operator == "bspline":
        edges = [cq.Edge.makeSpline([vector(item) for item in parameters["control_points_m"]], periodic=parameters["periodic"], tol=1e-6)]
    else:  # pragma: no cover - validator blocks this route
        raise RuntimeError(f"unsupported operator {operator}")
    start, end = segment["trim_fraction"]
    if (start, end) != (0, 1):
        if len(edges) != 1:
            raise RuntimeError("trim requires one source edge")
        edge = edges[0]
        edges = [edge.trim(edge.paramAt(start), edge.paramAt(end))]
    return edges


def execute_loop(loop: dict[str, Any], profile: dict[str, Any]) -> cq.Wire:
    edges = [edge for segment in loop["segments"] for edge in segment_edges(segment)]
    wire = cq.Wire.assembleEdges(edges)
    distance = profile["offset"]["distance_m"]
    if distance:
        offset = wire.offset2D(distance * MM, profile["offset"]["kind"])
        if len(offset) != 1:
            raise RuntimeError(f"offset changed topology for {profile['profile_id']}")
        wire = offset[0]
    for transform in profile["transforms"]:
        operator, parameters = transform["operator"], transform["parameters"]
        if operator == "translate":
            wire = wire.translate(vector(parameters["offset_m"]))
        elif operator == "rotate":
            wire = wire.rotate((0, 0, 0), (0, 0, 1), math.degrees(parameters["angle_rad"]))
        elif operator == "mirror":
            wire = wire.mirror("XZ" if parameters["axis"] == "x" else "YZ")
    if not wire.isValid() or not wire.IsClosed():
        raise RuntimeError(f"loop {loop['loop_id']} is not a valid closed wire")
    return wire


def validate_loop_nesting(wires: list[cq.Wire], profile_id: str, closure_tolerance_m: float) -> None:
    """Reject holes outside the outer loop or overlapping other holes."""
    outer = cq.Face.makeFromWires(wires[0])
    if not outer.isValid() or outer.Area() <= 0.0:
        raise RuntimeError(f"outer loop is invalid for {profile_id}")
    area_tolerance_mm2 = max((closure_tolerance_m * MM) ** 2, outer.Area() * 1e-12)
    holes: list[cq.Face] = []
    for wire in wires[1:]:
        hole = cq.Face.makeFromWires(wire)
        if not hole.isValid() or hole.Area() <= area_tolerance_mm2:
            raise RuntimeError(f"hole loop is invalid for {profile_id}")
        intersection = outer.intersect(hole)
        if abs(intersection.Area() - hole.Area()) > area_tolerance_mm2:
            raise RuntimeError(f"hole loop is not nested inside outer loop for {profile_id}")
        for prior in holes:
            if prior.intersect(hole).Area() > area_tolerance_mm2:
                raise RuntimeError(f"hole loops overlap for {profile_id}")
        holes.append(hole)


def enforce_constraints(profile: dict[str, Any], face: cq.Face, perimeter_m: float) -> None:
    bounds = face.BoundingBox()
    for constraint in profile["constraints"]:
        kind, value = constraint["kind"], constraint["value"]
        if kind == "positive_area" and face.Area() * 1e-6 < value:
            raise RuntimeError(f"positive_area constraint failed for {profile['profile_id']}")
        if kind == "minimum_perimeter" and perimeter_m < value:
            raise RuntimeError(f"minimum_perimeter constraint failed for {profile['profile_id']}")
        if kind == "hole_count" and len(face.Wires()) - 1 != value:
            raise RuntimeError(f"hole_count constraint failed for {profile['profile_id']}")
        if kind == "symmetric_axis":
            residual = abs(bounds.ymin + bounds.ymax) if value == "x" else abs(bounds.xmin + bounds.xmax)
            if residual > 1e-5:
                raise RuntimeError(f"symmetric_axis constraint failed for {profile['profile_id']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--freecad-python", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()
    if args.output_root.exists() and any(args.output_root.iterdir()):
        raise SystemExit("output-root must be absent or empty")
    args.output_root.mkdir(parents=True, exist_ok=True)
    raw = json.loads(args.config.read_text(encoding="utf-8"))
    validation = validate_grammar(raw)
    records = []
    for profile in raw["profiles"]:
        wires = [execute_loop(loop, profile) for loop in profile["loops"]]
        validate_loop_nesting(wires, profile["profile_id"], raw["limits"]["closure_tolerance_m"])
        face = cq.Face.makeFromWires(wires[0], wires[1:])
        if not face.isValid() or face.Area() <= 0.0:
            raise RuntimeError(f"profile {profile['profile_id']} did not produce one valid positive-area face")
        perimeter_m = math.fsum(edge.Length() for edge in face.Edges()) / MM
        enforce_constraints(profile, face, perimeter_m)
        path = args.output_root / f"{profile['profile_id']}.step"
        cq.exporters.export(face, str(path), exportType="STEP")
        canonicalize_step(path)
        bounds = face.BoundingBox()
        records.append({
            "profile_id": profile["profile_id"], "family": profile["family"],
            "step_file": path.name, "step_sha256": sha256(path), "valid": face.isValid(),
            "face_count": 1, "wire_count": len(face.Wires()), "edge_count": len(face.Edges()),
            "curved_edge_count": sum(edge.geomType() != "LINE" for edge in face.Edges()),
            "area_m2": face.Area() * 1e-6, "perimeter_m": perimeter_m,
            "bounding_box_m": {"minimum": [bounds.xmin / MM, bounds.ymin / MM, bounds.zmin / MM], "maximum": [bounds.xmax / MM, bounds.ymax / MM, bounds.zmax / MM]},
        })
    manifest_body = {"grammar_version": raw["grammar_version"], "declaration_sha256": declaration_sha256(raw), "validation": validation, "profiles": records, "hidden_geometry_repair": False}
    manifest = {**manifest_body, "manifest_sha256": hashlib.sha256(canonical_bytes(manifest_body)).hexdigest()}
    manifest_path = args.output_root / "manifest.json"; write(manifest_path, manifest)
    report_path = args.output_root / "freecad_report.json"; fcstd_path = args.output_root / "freeform_wire_corpus_v2.FCStd"
    environment = os.environ.copy(); environment.update({"FORMULA_ULTIMATE_W091_MANIFEST": str(manifest_path.resolve()), "FORMULA_ULTIMATE_W091_STEP_ROOT": str(args.output_root.resolve()), "FORMULA_ULTIMATE_W091_REPORT": str(report_path.resolve()), "FORMULA_ULTIMATE_W091_FCSTD": str(fcstd_path.resolve())})
    process = subprocess.run([str(args.freecad_python), str(ROOT / "scripts/cad/inspect_freeform_wire_corpus_freecad.py")], cwd=ROOT, env=environment, text=True, capture_output=True)
    if process.returncode:
        raise RuntimeError(process.stderr or process.stdout)
    freecad = json.loads(report_path.read_text(encoding="utf-8"))
    agreement = compare_measurement_witnesses(
        records,
        freecad["profiles"],
        measurement_relative_tolerance=raw["limits"]["measurement_relative_tolerance"],
        bounds_absolute_tolerance_m=raw["limits"]["closure_tolerance_m"],
    )
    result_body = {"status": "passed", "grammar_version": raw["grammar_version"], "profile_count": len(records), "family_count": validation["family_count"], "operator_coverage": validation["operator_coverage"], "transform_coverage": validation["transform_coverage"], "constraint_coverage": validation["constraint_coverage"], "nonzero_offset_profiles": validation["nonzero_offset_profiles"], "nontrivial_trim_segments": validation["nontrivial_trim_segments"], "declaration_sha256": validation["declaration_sha256"], "manifest_sha256": manifest["manifest_sha256"], "freecad_report_sha256": freecad["report_sha256"], "step_sha256": {item["profile_id"]: item["step_sha256"] for item in records}, "cad_kernel_agreement": agreement, "measurement_relative_tolerance": raw["limits"]["measurement_relative_tolerance"], "bounds_absolute_tolerance_m": raw["limits"]["closure_tolerance_m"], "hidden_geometry_repair": False}
    result = {**result_body, "result_sha256": hashlib.sha256(canonical_bytes(result_body)).hexdigest()}; write(args.output_root / "result.json", result)
    if args.replay_reference:
        reference = json.loads(args.replay_reference.read_text(encoding="utf-8")); exact = reference == result
        write(args.output_root / "replay.json", {"status": "passed" if exact else "failed", "exact": exact, "reference_result_sha256": reference.get("result_sha256"), "replay_result_sha256": result["result_sha256"]})
        if not exact: raise RuntimeError("replay mismatch")
    print(json.dumps({"status": "passed", "profile_count": len(records), "family_count": validation["family_count"], "operator_coverage": validation["operator_coverage"], "manifest_sha256": manifest["manifest_sha256"], "result_sha256": result["result_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
