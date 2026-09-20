#!/usr/bin/env python3
"""Build one Work 139 vehicle candidate from primitives and admitted free-form solids.

Runs under the pinned CadQuery runtime. Every packaging number written here is
measured on the built solids, never taken from the declaration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
for item in (ROOT, ROOT / "src"):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

import cadquery as cq  # noqa: E402

from formula_ultimate.components.freeform_solid_grammar import (  # noqa: E402
    declaration_sha256,
    validate_solid_grammar,
)
from formula_ultimate.components.freeform_wire_grammar import (  # noqa: E402
    validate_grammar as validate_wire_grammar,
)
from formula_ultimate.search.freeform_vehicle_candidate import (  # noqa: E402
    FreeformVehicleError,
    canonical_sha256,
    validate_protocol,
)
from scripts.cad.generate_freeform_solid_corpus import execute_candidate  # noqa: E402

MM = 1000.0


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonicalize_step(path: Path) -> None:
    text = path.read_text(encoding="ascii", errors="strict")
    updated, count = re.subn(r"(FILE_NAME\('[^']*',)'[^']*'", r"\1'1970-01-01T00:00:00'", text, count=1)
    if count != 1:
        raise FreeformVehicleError("STEP timestamp is missing or ambiguous")
    path.write_text(updated, encoding="ascii", newline="\n")


def _repository_path(path: Path) -> str:
    """Repository-relative POSIX path, whichever way the caller passed it."""

    resolved = path if path.is_absolute() else (Path.cwd() / path)
    return resolved.resolve().relative_to(ROOT).as_posix()


def primitive_shape(geometry: dict[str, Any]) -> cq.Shape:
    dimensions = [value * MM for value in geometry["dimensions_m"]]
    if geometry["primitive_type"] == "box":
        return cq.Workplane("XY").box(*dimensions).val()
    radius, height = dimensions
    return cq.Solid.makeCylinder(radius, height, cq.Vector(0, 0, -height / 2.0))


def place(shape: cq.Shape, placement: dict[str, Any]) -> cq.Shape:
    result = shape
    for index, (axis_start, axis_end) in enumerate(
        (((0, 0, 0), (1, 0, 0)), ((0, 0, 0), (0, 1, 0)), ((0, 0, 0), (0, 0, 1)))
    ):
        angle = float(placement["rotation_deg_xyz"][index])
        if angle:
            result = result.rotate(cq.Vector(*axis_start), cq.Vector(*axis_end), angle)
    translation = [value * MM for value in placement["translation_m"]]
    return result.translate(cq.Vector(*translation)) if any(translation) else result


def box_solid(minimum: list[float], maximum: list[float]) -> cq.Solid:
    sizes = [(high - low) * MM for low, high in zip(minimum, maximum)]
    centre = [(high + low) * MM / 2.0 for low, high in zip(minimum, maximum)]
    return cq.Workplane("XY").box(*sizes).val().translate(cq.Vector(*centre))


def intersection_volume(first: cq.Shape, second: cq.Shape) -> float:
    try:
        common = first.intersect(second)
    except Exception:  # noqa: BLE001 - kernel refusal is evidence, not a crash
        return float("nan")
    if common is None or not common.Solids():
        return 0.0
    return common.Volume() * 1e-9


def build_candidate(
    raw: dict[str, Any], candidate: dict[str, Any], corpus: dict[str, Any], profiles: dict[str, Any], output_root: Path
) -> dict[str, Any]:
    by_corpus_id = {item["candidate_id"]: item for item in corpus["candidates"]}
    output_root.mkdir(parents=True, exist_ok=True)
    shapes: dict[str, cq.Shape] = {}
    records: list[dict[str, Any]] = []
    for component in candidate["components"]:
        geometry = component["geometry"]
        if geometry["kind"] == "primitive":
            shape = primitive_shape(geometry)
            provenance = {"kind": "primitive", "primitive_type": geometry["primitive_type"]}
        else:
            corpus_candidate = by_corpus_id.get(geometry["corpus_candidate_id"])
            if corpus_candidate is None:
                raise FreeformVehicleError(f"corpus member is missing: {geometry['corpus_candidate_id']}")
            shape, _ = execute_candidate(corpus_candidate, profiles)
            provenance = {
                "kind": "freeform_reference",
                "corpus_candidate_id": corpus_candidate["candidate_id"],
                "family": corpus_candidate["family"],
            }
        shape = place(shape, component["placement"])
        if not shape.isValid() or len(shape.Solids()) != 1:
            raise FreeformVehicleError(f"component {component['component_id']} is not one valid solid")
        path = output_root / f"{component['component_id']}.step"
        cq.exporters.export(shape, str(path), exportType="STEP")
        canonicalize_step(path)
        bounds, centre = shape.BoundingBox(), shape.Center()
        density = float(raw["materials"][component["material_id"]]["density_kg_m3"])
        volume = shape.Volume() * 1e-9
        shapes[component["component_id"]] = shape
        records.append({
            "component_id": component["component_id"],
            "function_tags": sorted(component["function_tags"]),
            "material_id": component["material_id"],
            "provenance": provenance,
            "valid": bool(shape.isValid()),
            "solid_count": len(shape.Solids()),
            "face_count": len(shape.Faces()),
            "curved_face_count": sum(face.geomType() != "PLANE" for face in shape.Faces()),
            "volume_m3": volume,
            "mass_kg": volume * density,
            "center_m": [centre.x / MM, centre.y / MM, centre.z / MM],
            "bounding_box_m": {
                "minimum": [bounds.xmin / MM, bounds.ymin / MM, bounds.zmin / MM],
                "maximum": [bounds.xmax / MM, bounds.ymax / MM, bounds.zmax / MM],
            },
            "step_path": _repository_path(path),
            "step_sha256": file_sha256(path),
        })

    pairwise = []
    identities = sorted(shapes)
    for index, first in enumerate(identities):
        for second in identities[index + 1:]:
            pairwise.append({
                "components": [first, second],
                "intersection_m3": intersection_volume(shapes[first], shapes[second]),
            })
    keep_outs = []
    for keep_out in raw["keep_outs"]:
        region = box_solid(keep_out["minimum_m"], keep_out["maximum_m"])
        for component_id in identities:
            keep_outs.append({
                "keep_out_id": keep_out["keep_out_id"],
                "component_id": component_id,
                "intersection_m3": intersection_volume(shapes[component_id], region),
            })

    assembly = cq.Compound.makeCompound(list(shapes.values()))
    assembly_path = output_root / "assembly.step"
    cq.exporters.export(assembly, str(assembly_path), exportType="STEP")
    canonicalize_step(assembly_path)
    body = {
        "candidate_id": candidate["candidate_id"],
        "role": candidate["role"],
        "cadquery_version": cq.__version__,
        "components": records,
        "pairwise_intersections": pairwise,
        "keep_out_intersections": keep_outs,
        "mass_kg": sum(item["mass_kg"] for item in records),
        "volume_m3": sum(item["volume_m3"] for item in records),
        "assembly_step_path": _repository_path(assembly_path),
        "assembly_step_sha256": file_sha256(assembly_path),
        "assembly_solid_count": len(assembly.Solids()),
        "declared_mass_kg": None,
        "hidden_geometry_repair": False,
    }
    # Hash the geometry identity, not the output location: the same candidate
    # built into run_a and run_b must carry the same manifest hash.
    identity = json.loads(json.dumps(body))
    identity.pop("assembly_step_path", None)
    for record in identity["components"]:
        record.pop("step_path", None)
    return {**body, "manifest_sha256": canonical_sha256(identity)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    raw = json.loads(args.config.read_text(encoding="utf-8"))
    validate_protocol(raw)
    corpus_reference = raw["corpus"]
    wire_raw = json.loads((ROOT / corpus_reference["wire_config"]).read_text(encoding="utf-8"))
    validate_wire_grammar(wire_raw)
    corpus = json.loads((ROOT / corpus_reference["solid_config"]).read_text(encoding="utf-8"))
    if declaration_sha256(corpus) != corpus_reference["declaration_sha256"]:
        raise FreeformVehicleError("free-form corpus declaration identity mismatch")
    profiles = {item["profile_id"]: item for item in wire_raw["profiles"]}
    validate_solid_grammar(corpus, set(profiles))
    declared = {item["candidate_id"] for item in corpus["candidates"]}
    missing = sorted(set(corpus_reference["admitted_candidate_ids"]) - declared)
    if missing:
        raise FreeformVehicleError(f"admitted identities are absent from the corpus: {missing}")

    candidate = next((item for item in raw["candidates"] if item["candidate_id"] == args.candidate_id), None)
    if candidate is None:
        raise FreeformVehicleError(f"candidate is not declared: {args.candidate_id}")
    manifest = build_candidate(raw, candidate, corpus, profiles, args.output_root)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": "built",
        "candidate_id": manifest["candidate_id"],
        "component_count": len(manifest["components"]),
        "mass_kg": manifest["mass_kg"],
        "manifest_sha256": manifest["manifest_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
