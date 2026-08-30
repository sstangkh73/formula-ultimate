"""Import the exact Work 045 STEP and identify cylindrical interface faces."""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys

import FreeCAD as App
import Part


def sha(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if len(sys.argv) < 4:
        raise SystemExit("pass INPUT.step CONFIG.json OUTPUT.json")
    step_path, config_path, output_path = sys.argv[-3:]
    with open(config_path, encoding="utf-8") as handle:
        config = json.load(handle)
    shape = Part.Shape()
    shape.read(step_path)
    if len(shape.Solids) != 1 or not shape.isValid():
        raise RuntimeError("FreeCAD did not import one valid solid")
    interfaces = []
    for declared in config["interfaces"]:
        expected_radius_mm = declared["radius_m"] * 1000.0
        expected_x_mm = declared["center_x_m"] * 1000.0
        expected_y_mm = declared["center_y_m"] * 1000.0
        matches = []
        for index, face in enumerate(shape.Faces, start=1):
            surface = face.Surface
            if not hasattr(surface, "Radius") or not hasattr(surface, "Center") or not hasattr(surface, "Axis"):
                continue
            centre, axis = surface.Center, surface.Axis
            if abs(surface.Radius - expected_radius_mm) <= 1e-6 and abs(centre.x - expected_x_mm) <= 1e-6 and abs(centre.y - expected_y_mm) <= 1e-6 and abs(abs(axis.z) - 1.0) <= 1e-9:
                matches.append((index, face))
        if len(matches) != 1:
            raise RuntimeError("interface %s matched %d cylindrical faces" % (declared["interface_id"], len(matches)))
        index, face = matches[0]
        interfaces.append({"interface_id": declared["interface_id"], "role": declared["role"], "face_index": index, "radius_m": face.Surface.Radius * 1e-3, "center_m": [face.Surface.Center.x * 1e-3, face.Surface.Center.y * 1e-3, config["geometry"]["thickness_m"] / 2], "axis": [face.Surface.Axis.x, face.Surface.Axis.y, face.Surface.Axis.z], "area_m2": face.Area * 1e-6})
    report = {"status": "passed", "source": "FreeCAD STEP import", "freecad_version": ".".join(str(item) for item in App.Version()[:3]), "step_sha256": sha(step_path), "solid_count": len(shape.Solids), "is_valid": shape.isValid(), "volume_m3": shape.Volume * 1e-9, "interfaces": interfaces}
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True); handle.write("\n")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
