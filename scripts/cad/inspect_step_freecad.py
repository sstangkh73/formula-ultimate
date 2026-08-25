"""Independently import and measure one Work 006 STEP artifact in FreeCAD."""

from __future__ import annotations

import hashlib
import json
import os
import sys

import FreeCAD as App
import Part


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main() -> int:
    if len(sys.argv) < 3:
        raise SystemExit("pass INPUT.step OUTPUT.json")
    step_path, output_path = sys.argv[-2:]
    shape = Part.Shape()
    shape.read(step_path)
    bounds = shape.BoundBox
    solids = shape.Solids
    if len(solids) != 1:
        raise RuntimeError(f"expected exactly one STEP solid; received {len(solids)}")
    centre = solids[0].CenterOfMass
    version = App.Version()
    report = {
        "source": "FreeCAD STEP import",
        "freecad_version": ".".join(str(item) for item in version[:3]),
        "step_path": step_path,
        "step_sha256": _sha256(step_path),
        "volume_m3": shape.Volume * 1.0e-9,
        "volume_mm3": shape.Volume,
        "solid_count": len(solids),
        "is_valid": shape.isValid(),
        "bounds_m": [
            bounds.XLength * 1.0e-3,
            bounds.YLength * 1.0e-3,
            bounds.ZLength * 1.0e-3,
        ],
        "centre_of_mass_m": [
            centre.x * 1.0e-3,
            centre.y * 1.0e-3,
            centre.z * 1.0e-3,
        ],
    }
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    App.Console.PrintMessage(json.dumps(report, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
