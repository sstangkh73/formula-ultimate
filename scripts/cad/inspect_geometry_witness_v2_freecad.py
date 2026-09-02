"""Import exact Work 078 STEP bytes with FreeCAD and measure without repair."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys

import FreeCAD as App
import Part


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.components.geometry_witness import (  # noqa: E402
    WITNESS_VERSION,
    canonical_sha256,
    symmetric_eigen_3x3,
    validate_witness_config,
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _vector(value) -> list[float]:
    return [float(value.x) * 1.0e-3, float(value.y) * 1.0e-3, float(value.z) * 1.0e-3]


def _unit(value) -> list[float]:
    items = [float(value.x), float(value.y), float(value.z)]
    length = math.sqrt(math.fsum(item * item for item in items))
    result = [item / length for item in items]
    for item in result:
        if abs(item) > 1e-15:
            if item < 0.0:
                result = [-entry for entry in result]
            break
    return result


def _axis_offset_point(center, axis) -> list[float]:
    c = _vector(center)
    a = _unit(axis)
    projection = math.fsum(c[i] * a[i] for i in range(3))
    return [c[i] - projection * a[i] for i in range(3)]


def _matrix3(matrix, scale: float) -> list[list[float]]:
    names = (("A11", "A12", "A13"), ("A21", "A22", "A23"), ("A31", "A32", "A33"))
    return [[float(getattr(matrix, name)) * scale for name in row] for row in names]


def _surface_records(shape) -> list[dict]:
    records = []
    for face in shape.Faces:
        surface = face.Surface
        if not all(hasattr(surface, name) for name in ("Radius", "Axis", "Center")):
            continue
        axis = _unit(surface.Axis)
        axis_offset = _axis_offset_point(surface.Center, surface.Axis)
        projections = []
        for vertex in face.Vertexes:
            point = _vector(vertex.Point)
            projections.append(math.fsum(point[index] * axis[index] for index in range(3)))
        body = {
            "geometry_type": "cylindrical_surface",
            "surface_class": type(surface).__name__,
            "radius_m": float(surface.Radius) * 1.0e-3,
            "axis": axis,
            "axis_offset_point_m": axis_offset,
            "axial_bounds_m": [min(projections), max(projections)] if projections else [0.0, 0.0],
            "area_m2": float(face.Area) * 1.0e-6,
        }
        records.append({**body, "surface_signature_sha256": canonical_sha256(body)})
    return sorted(records, key=lambda item: item["surface_signature_sha256"])


def _measure_part(part: dict, source_root: Path) -> dict:
    path = source_root / part["step_file"]
    if not path.is_file():
        raise RuntimeError(f"missing STEP file: {path}")
    step_sha = _sha256(path)
    if step_sha != part["step_sha256"]:
        raise RuntimeError(f"STEP hash mismatch before import for {part['part_id']}")
    shape = Part.Shape()
    shape.read(os.fspath(path))
    solids = shape.Solids
    if len(solids) != 1:
        raise RuntimeError(f"{part['part_id']} imported {len(solids)} solids")
    solid = solids[0]
    bounds = shape.optimalBoundingBox(True, False)
    centre = solid.CenterOfMass
    geometric_tensor = _matrix3(solid.MatrixOfInertia, 1.0e-15)
    density = part["material_density_kg_per_m3"]
    mass_tensor = [[density * value for value in row] for row in geometric_tensor]
    moments, axes = symmetric_eigen_3x3(mass_tensor)
    return {
        "part_id": part["part_id"],
        "step_file": part["step_file"],
        "step_sha256": step_sha,
        "step_bytes": path.stat().st_size,
        "shape_type": shape.ShapeType,
        "solid_count": len(solids),
        "shell_count": len(shape.Shells),
        "is_valid": bool(shape.isValid()),
        "volume_m3": float(shape.Volume) * 1.0e-9,
        "bounding_box_m": {
            "minimum": [bounds.XMin * 1.0e-3, bounds.YMin * 1.0e-3, bounds.ZMin * 1.0e-3],
            "maximum": [bounds.XMax * 1.0e-3, bounds.YMax * 1.0e-3, bounds.ZMax * 1.0e-3],
        },
        "centre_of_mass_m": _vector(centre),
        "geometric_inertia_tensor_m5": geometric_tensor,
        "material_density_kg_per_m3": density,
        "mass_kg": float(shape.Volume) * 1.0e-9 * density,
        "mass_inertia_tensor_kg_m2": mass_tensor,
        "principal_moments_kg_m2": moments,
        "principal_axes": axes,
        "cylindrical_surfaces": _surface_records(shape),
        "unsupported_measurements": list(part["unsupported_measurements"]),
        "hidden_geometry_repair": False,
    }


def main() -> int:
    env_config = os.environ.get("FORMULA_ULTIMATE_W081_CONFIG")
    env_manifest = os.environ.get("FORMULA_ULTIMATE_W081_SOURCE_MANIFEST")
    env_source = os.environ.get("FORMULA_ULTIMATE_W081_SOURCE_ROOT")
    env_output = os.environ.get("FORMULA_ULTIMATE_W081_OUTPUT")
    if env_config and env_manifest and env_source and env_output:
        config_path = Path(env_config)
        manifest_path = Path(env_manifest)
        source_root = Path(env_source)
        output_path = Path(env_output)
    else:
        tokens = sys.argv[sys.argv.index("--pass") + 1 :] if "--pass" in sys.argv else sys.argv[1:]
        parser = argparse.ArgumentParser()
        parser.add_argument("--config", type=Path, required=True)
        parser.add_argument("--source-manifest", type=Path, required=True)
        parser.add_argument("--source-root", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args(tokens)
        config_path = args.config
        manifest_path = args.source_manifest
        source_root = args.source_root
        output_path = args.output
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    config = validate_witness_config(raw)
    source_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if source_manifest.get("manifest_sha256") != config["source_manifest_sha256"]:
        raise RuntimeError("source manifest identity differs from witness config")
    if source_manifest.get("hidden_geometry_repair") is not False:
        raise RuntimeError("source manifest does not prove no hidden geometry repair")
    source_hashes = {item.get("candidate_id"): item.get("step_sha256") for item in source_manifest.get("candidates", [])}
    if source_hashes != {part["part_id"]: part["step_sha256"] for part in config["parts"]}:
        raise RuntimeError("source manifest part hashes differ from witness config")
    parts = [_measure_part(part, source_root) for part in config["parts"]]
    version = App.Version()
    body = {
        "witness_version": WITNESS_VERSION,
        "source_manifest_sha256": config["source_manifest_sha256"],
        "freecad_version": ".".join(str(item) for item in version[:3]),
        "occt_version": str(getattr(Part, "OCC_VERSION", "unavailable")),
        "import_mode": "Part.Shape.read_step_no_repair",
        "hidden_geometry_repair": False,
        "parts": parts,
    }
    report = {**body, "report_sha256": canonical_sha256(body)}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    App.Console.PrintMessage(json.dumps({"status": "measured", "part_count": len(parts), "report_sha256": report["report_sha256"]}, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
