"""Independently inspect Work 108 material-region STEP files with FreeCAD."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import FreeCAD
import Part


MM = 1000.0


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")


def canonical_sha256(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def measure(shape):
    if shape.isNull() or not shape.isValid() or not shape.Solids or not math.isfinite(shape.Volume) or shape.Volume <= 0.0:
        raise RuntimeError("FreeCAD imported invalid or empty region geometry")
    if len(shape.Solids) != 1:
        raise RuntimeError("each material region STEP must contain exactly one solid")
    measured = shape.Solids[0]
    matrix = measured.MatrixOfInertia
    return {
        "volume_m3": measured.Volume * 1e-9,
        "centre_m": [measured.CenterOfMass.x / MM, measured.CenterOfMass.y / MM, measured.CenterOfMass.z / MM],
        "centroidal_inertia_per_density_m5": [
            [matrix.A11 * 1e-15, matrix.A12 * 1e-15, matrix.A13 * 1e-15],
            [matrix.A21 * 1e-15, matrix.A22 * 1e-15, matrix.A23 * 1e-15],
            [matrix.A31 * 1e-15, matrix.A32 * 1e-15, matrix.A33 * 1e-15],
        ],
        "solid_count": 1,
        "valid": True,
    }


def combine(regions):
    masses = [item["volume_m3"] * item["density_kg_m3"] for item in regions]
    total_mass = sum(masses)
    centre = [
        sum(mass * region["centre_m"][axis] for mass, region in zip(masses, regions)) / total_mass
        for axis in range(3)
    ]
    inertia = [[0.0 for _ in range(3)] for _ in range(3)]
    for mass, region in zip(masses, regions):
        displacement = [region["centre_m"][axis] - centre[axis] for axis in range(3)]
        squared = sum(item * item for item in displacement)
        density = region["density_kg_m3"]
        for row in range(3):
            for column in range(3):
                central = region["centroidal_inertia_per_density_m5"][row][column] * density
                parallel = mass * ((squared if row == column else 0.0) - displacement[row] * displacement[column])
                inertia[row][column] += central + parallel
    return {
        "volume_m3": sum(item["volume_m3"] for item in regions),
        "mass_kg": total_mass,
        "centre_of_mass_m": centre,
        "centroidal_inertia_kg_m2": inertia,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if canonical_sha256(manifest["body"]) != manifest["manifest_sha256"]:
        raise RuntimeError("artifact manifest identity mismatch")
    root = args.manifest.parent
    cases = []
    for declared_case in manifest["body"]["cases"]:
        regions = []
        for declared_region in declared_case["regions"]:
            path = root / declared_region["step_file"]
            if file_sha256(path) != declared_region["step_sha256"]:
                raise RuntimeError("region STEP identity mismatch")
            measured = measure(Part.read(str(path)))
            regions.append(
                {
                    "region_id": declared_region["region_id"],
                    "material_id": declared_region["material_id"],
                    "density_kg_m3": declared_region["density_kg_m3"],
                    "step_sha256": declared_region["step_sha256"],
                    **measured,
                }
            )
        cases.append(
            {
                "case_id": declared_case["case_id"],
                "regions": regions,
                "system_mass_properties": combine(regions),
            }
        )
    body = {
        "source_manifest_sha256": manifest["manifest_sha256"],
        "freecad_version": ".".join(FreeCAD.Version()[:3]),
        "cases": cases,
        "hidden_geometry_repair": False,
    }
    report = {"body": body, "report_sha256": canonical_sha256(body)}
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
