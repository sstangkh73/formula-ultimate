#!/usr/bin/env python3
"""Measure part resolution and joint interfaces for Work 140.

Runs under the pinned CadQuery runtime. Every number here is measured on a
built solid: nothing is copied from a declaration. A kernel refusal is written
down as evidence instead of being worked around.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
for item in (ROOT, ROOT / "src"):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

import cadquery as cq  # noqa: E402
from OCP.BRepExtrema import BRepExtrema_DistShapeShape  # noqa: E402

from formula_ultimate.assembly.part_resolution import (  # noqa: E402
    PartResolutionError,
    validate_protocol,
)
from scripts.cad.detailed_part_builders import BUILDERS  # noqa: E402

MM = 1000.0
#: Faces whose surface is neither a plane nor a simple cylinder count as
#: engagement geometry: a swept thread, a knurl or a formed flank.
ENGAGEMENT_SURFACES = {"BSPLINE", "BEZIER", "SURFACE_OF_EXTRUSION", "SURFACE_OF_REVOLUTION", "OFFSET", "OTHER"}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonicalize_step(path: Path) -> None:
    """Remove the two session-dependent fields OCCT writes into a STEP file."""

    text = path.read_text(encoding="ascii", errors="strict")
    stamped = re.subn(r"(FILE_NAME\('[^']*',)'[^']*'", r"\g<1>'1970-01-01T00:00:00'", text, count=1)
    if stamped[1] != 1:
        raise PartResolutionError("STEP timestamp is missing or ambiguous")
    # OCCT appends a per-process export counter to the product name, so the
    # same solid exported twice in one process differs in its header alone.
    updated = re.sub(r"(Open CASCADE STEP translator [0-9.]+) \d+", r"\g<1>", stamped[0])
    path.write_text(updated, encoding="ascii", newline=chr(10))


def _repository_path(path: Path) -> str:
    """Repository-relative when the output sits inside the checkout, else absolute."""

    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def load_part(part: dict[str, Any]) -> cq.Shape:
    geometry = part["geometry"]
    if geometry["kind"] == "step_file":
        path = ROOT / geometry["path"]
        if not path.is_file():
            raise PartResolutionError(f"declared STEP file is missing: {path}")
        return cq.importers.importStep(str(path)).val()
    builder = BUILDERS.get(geometry["builder"])
    if builder is None:
        raise PartResolutionError(f"unknown reference builder: {geometry['builder']}")
    return builder(geometry["parameters"])


def measure_part(shape: cq.Shape) -> dict[str, Any]:
    """Faces, edges, surface types and the smallest feature actually present."""

    faces, edges = shape.Faces(), shape.Edges()
    if not faces or not edges:
        return {"status": "unresolved_measurement", "cause": "shape carries no faces or edges"}
    types = collections.Counter(face.geomType() for face in faces)
    edge_lengths = sorted(edge.Length() / MM for edge in edges)
    face_areas = sorted(face.Area() / (MM * MM) for face in faces)
    bounds = shape.BoundingBox()
    # Two different questions. The shortest edge says whether the part contains
    # a sliver; the tenth-percentile edge says what scale the part is modelled
    # at, and that is what a mesh has to resolve.
    smallest = edge_lengths[0]
    index = max(0, min(len(edge_lengths) - 1, int(math.ceil(0.1 * len(edge_lengths))) - 1))
    feature_scale = edge_lengths[index]
    return {
        "status": "measured",
        "valid": bool(shape.isValid()),
        "solid_count": len(shape.Solids()),
        "single_solid": len(shape.Solids()) == 1,
        "face_count": len(faces),
        "edge_count": len(edges),
        "curved_face_count": int(sum(1 for face in faces if face.geomType() != "PLANE")),
        "engagement_face_count": int(sum(1 for face in faces if face.geomType() in ENGAGEMENT_SURFACES)),
        "surface_types": dict(sorted(types.items())),
        "smallest_feature_m": smallest,
        "feature_scale_m": feature_scale,
        "smallest_face_area_m2": face_areas[0],
        "edge_lengths_m": edge_lengths,
        "volume_m3": shape.Volume() * 1e-9,
        "bounding_box_m": [
            (bounds.xmax - bounds.xmin) / MM, (bounds.ymax - bounds.ymin) / MM, (bounds.zmax - bounds.zmin) / MM
        ],
    }


def place(shape: cq.Shape, placement: dict[str, Any]) -> cq.Shape:
    result = shape
    for index, (start, end) in enumerate((((0, 0, 0), (1, 0, 0)), ((0, 0, 0), (0, 1, 0)), ((0, 0, 0), (0, 0, 1)))):
        angle = float(placement["rotation_deg_xyz"][index])
        if angle:
            result = result.rotate(cq.Vector(*start), cq.Vector(*end), angle)
    translation = [value * MM for value in placement["translation_m"]]
    return result.translate(cq.Vector(*translation)) if any(translation) else result


def measure_joint(first: cq.Shape, second: cq.Shape, tolerance_m: float) -> dict[str, Any]:
    """Minimum distance, interference and mating faces between two built parts."""

    try:
        distance = BRepExtrema_DistShapeShape(first.wrapped, second.wrapped)
        distance.Perform()
        if not distance.IsDone():
            return {"status": "unresolved_joint_measurement", "cause": "distance solver did not complete"}
        gap = distance.Value() / MM
    except Exception as exc:  # noqa: BLE001 - a kernel refusal is evidence
        return {"status": "unresolved_joint_measurement", "cause": f"{type(exc).__name__}: {exc}"}
    try:
        common = first.intersect(second)
        solid = common is not None and bool(common.Solids())
        interference = common.Volume() * 1e-9 if solid else 0.0
        # Mean penetration of an interference fit, from the intersection solid
        # itself: a thin shell of volume V and surface A is about 2V/A thick.
        penetration = (2.0 * common.Volume() / common.Area()) / MM if solid and common.Area() > 0.0 else 0.0
    except Exception as exc:  # noqa: BLE001
        return {"status": "unresolved_joint_measurement", "cause": f"intersection refused: {type(exc).__name__}"}

    first_engagement = sum(1 for face in first.Faces() if face.geomType() in ENGAGEMENT_SURFACES)
    second_engagement = sum(1 for face in second.Faces() if face.geomType() in ENGAGEMENT_SURFACES)
    tolerance_mm = tolerance_m * MM
    pairs = 0
    overlap = 0.0
    for face_a in first.Faces():
        for face_b in second.Faces():
            try:
                pair = BRepExtrema_DistShapeShape(face_a.wrapped, face_b.wrapped)
                pair.Perform()
                if pair.IsDone() and pair.Value() <= max(tolerance_mm, abs(distance.Value()) + 1e-9):
                    pairs += 1
                    overlap += min(face_a.Area(), face_b.Area()) / (MM * MM)
            except Exception:  # noqa: BLE001, PERF203 - refusal on one pair is not fatal
                continue
    return {
        "status": "measured",
        "clearance_m": gap if interference <= 0.0 else -penetration,
        "penetration_depth_m": penetration,
        "interference_volume_m3": interference,
        "mating_face_pairs": pairs,
        "overlap_area_m2": overlap,
        "engagement_face_count": int(first_engagement + second_engagement),
        # Per side, because a thread bears on a thread: one threaded part and
        # one plain one is not a threaded joint.
        "engagement_face_counts": [int(first_engagement), int(second_engagement)],
        "single_solid": len(first.Solids()) == 1 and len(second.Solids()) == 1,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--measurement", type=Path, required=True)
    args = parser.parse_args()

    raw = json.loads(args.config.read_text(encoding="utf-8"))
    validate_protocol(raw)
    args.output_root.mkdir(parents=True, exist_ok=True)

    shapes: dict[str, cq.Shape] = {}
    parts: dict[str, Any] = {}
    for part in raw["parts"]:
        part_id = part["part_id"]
        try:
            shape = load_part(part)
            measurement = measure_part(shape)
        except Exception as exc:  # noqa: BLE001 - a kernel refusal is evidence
            parts[part_id] = {"status": "unresolved_measurement", "cause": f"{type(exc).__name__}: {exc}"}
            continue
        if measurement["status"] == "measured":
            path = args.output_root / f"{part_id}.step"
            cq.exporters.export(shape, str(path), exportType="STEP")
            canonicalize_step(path)
            digest = file_sha256(path)
            # Build it a second time and compare. A part whose own build is not
            # byte-reproducible cannot carry a reproducible measurement, and
            # saying so is better than letting the run's replay drift. Only the
            # verdict is recorded, because the varying bytes are what differ.
            repeat = args.output_root / f"{part_id}.repeat.step"
            try:
                cq.exporters.export(load_part(part), str(repeat), exportType="STEP")
                canonicalize_step(repeat)
                reproducible = file_sha256(repeat) == digest
            except Exception as exc:  # noqa: BLE001
                parts[part_id] = {"status": "unresolved_measurement", "cause": f"second build refused: {type(exc).__name__}"}
                continue
            finally:
                if repeat.exists():
                    repeat.unlink()
            if not reproducible:
                parts[part_id] = {
                    "status": "unresolved_measurement",
                    "cause": "build is not byte-reproducible across two builds in one run",
                }
                continue
            measurement["step_path"] = _repository_path(path)
            measurement["step_sha256"] = digest
            shapes[part_id] = shape
        parts[part_id] = measurement

    joints: dict[str, Any] = {}
    for joint in raw["joints"]:
        first_id, second_id = joint["parts"]
        if first_id not in shapes or second_id not in shapes:
            joints[joint["joint_id"]] = {"status": "unresolved_joint_measurement", "cause": "a joined part was not measured"}
            continue
        first = place(shapes[first_id], joint["placement"][first_id])
        second = place(shapes[second_id], joint["placement"][second_id])
        joints[joint["joint_id"]] = measure_joint(first, second, float(raw["resolution"]["minimum_feature_m"]))

    payload = {"cadquery_version": cq.__version__, "parts": parts, "joints": joints}
    args.measurement.parent.mkdir(parents=True, exist_ok=True)
    args.measurement.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": "measured",
        "part_count": len(parts),
        "joint_count": len(joints),
        "unresolved_parts": sorted(k for k, v in parts.items() if v["status"] != "measured"),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
