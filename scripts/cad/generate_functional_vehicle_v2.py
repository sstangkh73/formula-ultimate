"""Generate deterministic component and assembly STEP evidence for Work 066."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import cadquery as cq

from formula_ultimate.topology import (
    from_functional_mapping,
    functional_declaration_sha256,
    validate_functional_vehicle,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonicalize_step(path: Path) -> None:
    text = path.read_text(encoding="ascii")
    updated, count = re.subn(r"(FILE_NAME\('[^']*',)'[^']*'", r"\1'1970-01-01T00:00:00'", text, count=1)
    if count != 1:
        raise RuntimeError("STEP timestamp is missing or ambiguous")
    path.write_text(updated, encoding="ascii", newline="\n")


def shape_for(component):
    scale = 1000.0
    if component.primitive_kind == "box":
        shape = cq.Workplane("XY").box(*(value * scale for value in component.dimensions_m)).val()
    else:
        radius, length = (value * scale for value in component.dimensions_m)
        axes = {
            "cylinder_x": (cq.Vector(-length / 2.0, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0)),
            "cylinder_y": (cq.Vector(0.0, -length / 2.0, 0.0), cq.Vector(0.0, 1.0, 0.0)),
            "cylinder_z": (cq.Vector(0.0, 0.0, -length / 2.0), cq.Vector(0.0, 0.0, 1.0)),
        }
        base, direction = axes[component.primitive_kind]
        shape = cq.Solid.makeCylinder(radius, length, base, direction)
    return shape.translate(tuple(value * scale for value in component.position_m))


def relative_error(actual: float, reference: float) -> float:
    return abs(actual - reference) / max(abs(reference), 1.0e-300)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    raw = json.loads(args.config.read_text(encoding="utf-8"))
    vehicle = from_functional_mapping(raw)
    validation = validate_functional_vehicle(vehicle)
    tolerance = vehicle.tolerances["mass_property_relative"]
    args.output_root.mkdir(parents=True, exist_ok=True)
    shapes, records = [], []
    for component in sorted(vehicle.components, key=lambda item: item.component_id):
        shape = shape_for(component)
        if not shape.isValid() or len(shape.Solids()) != 1:
            raise RuntimeError(f"component {component.component_id} is not one valid solid")
        volume_m3 = shape.Volume() * 1.0e-9
        if relative_error(volume_m3, component.volume_m3) > tolerance:
            raise RuntimeError(f"component {component.component_id} volume disagrees with declaration")
        path = args.output_root / f"{component.component_id}.step"
        cq.exporters.export(shape, str(path), exportType="STEP")
        canonicalize_step(path)
        shapes.append(shape)
        records.append({
            "component_id": component.component_id,
            "function_tags": component.function_tags,
            "material_id": component.material_id,
            "density_kg_per_m3": component.density_kg_per_m3,
            "volume_m3": volume_m3,
            "centre_of_mass_m": [value * 1.0e-3 for value in shape.Center().toTuple()],
            "port_count": len(component.ports),
            "step_path": str(path),
            "step_sha256": sha256(path),
            "valid": True,
            "solid_count": 1,
        })
    compound = cq.Compound.makeCompound(shapes)
    assembly_path = args.output_root / "assembly.step"
    cq.exporters.export(compound, str(assembly_path), exportType="STEP")
    canonicalize_step(assembly_path)
    if not compound.isValid() or len(compound.Solids()) != len(vehicle.components):
        raise RuntimeError("functional assembly is invalid or lost component solids")
    manifest = {
        "status": "passed",
        "protocol_id": vehicle.protocol_id,
        "candidate_id": vehicle.candidate_id,
        "grammar_version": raw["grammar_version"],
        "declaration_sha256": functional_declaration_sha256(raw),
        "cadquery_version": cq.__version__,
        "components": records,
        "assembly": {
            "step_path": str(assembly_path),
            "step_sha256": sha256(assembly_path),
            "solid_count": len(compound.Solids()),
            "valid": compound.isValid(),
            "volume_m3": compound.Volume() * 1.0e-9,
        },
        "grammar_validation": validation,
        "hidden_geometry_repair": False,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "component_count": len(records), "assembly_sha256": manifest["assembly"]["step_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
