"""Independent FreeCAD witness for Work 091 planar profile STEP files."""
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


def main() -> int:
    manifest_path = Path(os.environ["FORMULA_ULTIMATE_W091_MANIFEST"])
    step_root = Path(os.environ["FORMULA_ULTIMATE_W091_STEP_ROOT"])
    report_path = Path(os.environ["FORMULA_ULTIMATE_W091_REPORT"])
    fcstd_path = Path(os.environ["FORMULA_ULTIMATE_W091_FCSTD"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    document = FreeCAD.newDocument("FreeformWireCorpusV2")
    records = []
    for expected in manifest["profiles"]:
        path = step_root / expected["step_file"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected["step_sha256"]:
            raise RuntimeError("STEP identity mismatch before FreeCAD inspection")
        shape = Part.read(str(path))
        # Use OCCT's geometry-derived box rather than the display/triangulation box.
        # CadQuery's Shape.BoundingBox uses this same optimal calculation.
        bounds = shape.optimalBoundingBox(False, False)
        if shape.isNull() or not shape.isValid():
            raise RuntimeError(f"invalid imported profile {expected['profile_id']}")
        feature = document.addObject("PartDesign::Feature", expected["profile_id"]); feature.Label = expected["profile_id"]; feature.Shape = shape
        records.append({
            "profile_id": expected["profile_id"], "step_sha256": expected["step_sha256"],
            "valid": shape.isValid(), "face_count": len(shape.Faces), "wire_count": len(shape.Wires), "edge_count": len(shape.Edges),
            "area_m2": shape.Area * 1e-6, "perimeter_m": sum(edge.Length for edge in shape.Edges) / MM,
            "bounding_box_m": {"minimum": [bounds.XMin / MM, bounds.YMin / MM, bounds.ZMin / MM], "maximum": [bounds.XMax / MM, bounds.YMax / MM, bounds.ZMax / MM]},
        })
    document.recompute(); document.saveAs(str(fcstd_path)); FreeCAD.closeDocument(document.Name)
    body = {"source_manifest_sha256": manifest["manifest_sha256"], "freecad_version": FreeCAD.Version()[0] + "." + FreeCAD.Version()[1] + "." + FreeCAD.Version()[2], "profile_count": len(records), "profiles": records, "hidden_geometry_repair": False}
    report = {**body, "report_sha256": canonical_sha256(body)}
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
