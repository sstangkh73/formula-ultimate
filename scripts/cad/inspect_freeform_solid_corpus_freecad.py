#!/usr/bin/env python3
"""Independent FreeCAD STEP witness for the Work 092 solid corpus."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import FreeCAD
import Part

MM = 1000.0


def canonical_sha256(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")).hexdigest()


def datums(shape, declarations):
    bounds = shape.optimalBoundingBox(False, False)
    minimum = [bounds.XMin / MM, bounds.YMin / MM, bounds.ZMin / MM]
    maximum = [bounds.XMax / MM, bounds.YMax / MM, bounds.ZMax / MM]
    center = [(a + b) / 2 for a, b in zip(minimum, maximum)]
    spans = [b - a for a, b in zip(minimum, maximum)]
    longest = max(range(3), key=lambda index: (spans[index], -index))
    result = []
    for datum in declarations:
        if datum["kind"] == "bbox_center": value = {"point_m": center}
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


def main() -> int:
    manifest_path = Path(os.environ["FORMULA_ULTIMATE_W092_MANIFEST"]); root = Path(os.environ["FORMULA_ULTIMATE_W092_STEP_ROOT"])
    report_path = Path(os.environ["FORMULA_ULTIMATE_W092_REPORT"]); fcstd_path = Path(os.environ["FORMULA_ULTIMATE_W092_FCSTD"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")); document = FreeCAD.newDocument("FreeformSolidCorpusV2"); records = []
    for expected in manifest["candidates"]:
        path = root / expected["step_file"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected["step_sha256"]: raise RuntimeError("STEP identity mismatch")
        shape = Part.read(str(path))
        if shape.isNull() or not shape.isValid(): raise RuntimeError(f"invalid imported solid {expected['candidate_id']}")
        feature = document.addObject("PartDesign::Feature", expected["candidate_id"]); feature.Label = expected["candidate_id"]; feature.Shape = shape
        bounds = shape.optimalBoundingBox(False, False)
        solids = list(shape.Solids); total_volume = sum(solid.Volume for solid in solids)
        center = FreeCAD.Vector(
            sum(solid.CenterOfMass.x * solid.Volume for solid in solids) / total_volume,
            sum(solid.CenterOfMass.y * solid.Volume for solid in solids) / total_volume,
            sum(solid.CenterOfMass.z * solid.Volume for solid in solids) / total_volume,
        )
        datum_declarations = expected["datum_declarations"]
        records.append({
            "candidate_id": expected["candidate_id"], "step_sha256": expected["step_sha256"], "valid": shape.isValid(),
            "solid_count": len(shape.Solids), "face_count": len(shape.Faces), "edge_count": len(shape.Edges),
            "volume_m3": shape.Volume * 1e-9, "surface_area_m2": shape.Area * 1e-6,
            "center_m": [center.x / MM, center.y / MM, center.z / MM],
            "bounding_box_m": {"minimum": [bounds.XMin / MM, bounds.YMin / MM, bounds.ZMin / MM], "maximum": [bounds.XMax / MM, bounds.YMax / MM, bounds.ZMax / MM]},
            "datums": datums(shape, datum_declarations),
        })
    document.recompute(); document.saveAs(str(fcstd_path)); FreeCAD.closeDocument(document.Name)
    body = {"source_manifest_sha256": manifest["manifest_sha256"], "freecad_version": ".".join(FreeCAD.Version()[:3]), "candidate_count": len(records), "candidates": records, "hidden_geometry_repair": False}
    report = {**body, "report_sha256": canonical_sha256(body)}; report_path.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
