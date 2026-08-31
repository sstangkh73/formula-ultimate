"""Independently inspect Work 066 functional STEP evidence with FreeCAD."""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys

import FreeCAD as App
import Part


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def aggregate(rows):
    mass = math.fsum(row["mass_kg"] for row in rows)
    centre = [math.fsum(row["mass_kg"] * row["centre_of_mass_m"][index] for row in rows) / mass for index in range(3)]
    inertia = [0.0] * 6
    for row in rows:
        dx, dy, dz = [row["centre_of_mass_m"][index] - centre[index] for index in range(3)]
        m = row["mass_kg"]
        parallel = (m*(dy*dy+dz*dz), m*(dx*dx+dz*dz), m*(dx*dx+dy*dy), -m*dx*dy, -m*dx*dz, -m*dy*dz)
        inertia = [inertia[index] + row["centroidal_inertia_kg_m2"][index] + parallel[index] for index in range(6)]
    return {"mass_kg": mass, "centre_of_mass_m": centre, "inertia_kg_m2": inertia}


def scalar_relative(actual, reference):
    return abs(actual - reference) / max(abs(reference), 1.0e-12)


def vector_relative(actual, reference):
    return max(abs(actual[index] - reference[index]) for index in range(len(reference))) / max(max(abs(value) for value in reference), 1.0e-12)


def main():
    if len(sys.argv) < 4:
        raise SystemExit("pass MANIFEST CONFIG OUTPUT")
    manifest_path, config_path, output_path = sys.argv[-3:]
    with open(manifest_path, encoding="utf-8") as stream:
        manifest = json.load(stream)
    with open(config_path, encoding="utf-8") as stream:
        config = json.load(stream)
    expected_ids = sorted(item["component_id"] for item in config["components"])
    manifest_ids = sorted(item["component_id"] for item in manifest["components"])
    if expected_ids != manifest_ids:
        raise RuntimeError("functional component identity set mismatch")
    rows = []
    for record in manifest["components"]:
        shape = Part.Shape()
        shape.read(record["step_path"])
        if len(shape.Solids) != 1 or not shape.isValid():
            raise RuntimeError("FreeCAD functional component import is invalid")
        solid = shape.Solids[0]
        density = float(record["density_kg_per_m3"])
        volume = solid.Volume * 1.0e-9
        mass = volume * density
        centre = solid.CenterOfMass
        matrix = solid.MatrixOfInertia
        inertia = [
            matrix.A11*density*1.0e-15, matrix.A22*density*1.0e-15, matrix.A33*density*1.0e-15,
            matrix.A12*density*1.0e-15, matrix.A13*density*1.0e-15, matrix.A23*density*1.0e-15,
        ]
        rows.append({
            "component_id": record["component_id"], "step_sha256": sha256(record["step_path"]),
            "valid": True, "solid_count": 1, "volume_m3": volume, "mass_kg": mass,
            "centre_of_mass_m": [centre.x*1.0e-3, centre.y*1.0e-3, centre.z*1.0e-3],
            "centroidal_inertia_kg_m2": inertia,
        })
    assembly = Part.Shape()
    assembly.read(manifest["assembly"]["step_path"])
    if len(assembly.Solids) != len(rows) or not assembly.isValid():
        raise RuntimeError("FreeCAD functional assembly solid count or validity failed")
    measured = aggregate(rows)
    reference = manifest["grammar_validation"]["mass_properties"]
    residuals = {
        "mass_relative": scalar_relative(measured["mass_kg"], reference["mass_kg"]),
        "centre_relative": vector_relative(measured["centre_of_mass_m"], reference["centre_of_mass_m"]),
        "inertia_relative": vector_relative(measured["inertia_kg_m2"], reference["inertia_kg_m2"]),
    }
    tolerance = float(config["tolerances"]["mass_property_relative"])
    if max(residuals.values()) > tolerance:
        raise RuntimeError("FreeCAD functional mass-property residual failed")
    report = {
        "status": "passed", "freecad_version": ".".join(str(value) for value in App.Version()[:3]),
        "components": rows, "mass_properties": measured, "residuals": residuals,
        "assembly": {"step_sha256": sha256(manifest["assembly"]["step_path"]), "solid_count": len(assembly.Solids), "valid": True, "volume_m3": assembly.Volume*1.0e-9},
        "hidden_geometry_repair": False,
    }
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"status": "passed", "component_count": len(rows), "mass_kg": measured["mass_kg"], "maximum_residual": max(residuals.values())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
