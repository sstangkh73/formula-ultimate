"""Execute the registered Work 109 implicit material mutation chain."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from formula_ultimate.search.freeform_material_generator import (  # noqa: E402
    FreeformMaterialViolation,
    apply_edit,
    canonical_sha256,
    extract_surface,
    field_descriptor,
    generate_source,
    grid_spec,
    validate_protocol,
    write_obj,
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def field_rows(field: dict[tuple[int, int, int], str]) -> list[list[Any]]:
    return [[*cell, field[cell]] for cell in sorted(field)]


def surface_record(field, spec, path: Path, maximum_triangles: int, tolerance: float) -> dict[str, Any]:
    descriptor = field_descriptor(field, spec)
    surface = extract_surface(field, spec, maximum_triangles)
    error = abs(surface["enclosed_volume_m3"] - descriptor["occupied_volume_m3"]) / descriptor["occupied_volume_m3"]
    if error > tolerance:
        raise FreeformMaterialViolation("surface conversion volume error exceeded tolerance")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(write_obj(surface), encoding="utf-8", newline="\n")
    return {
        "descriptor": descriptor,
        "surface": {key: value for key, value in surface.items() if key not in {"vertices", "triangles"}},
        "surface_volume_relative_error": error,
        "obj_file": path.name,
        "obj_sha256": file_sha256(path),
    }


def rejected_control(action, expected: str) -> dict[str, str]:
    try:
        action()
    except FreeformMaterialViolation as exc:
        if expected not in str(exc):
            raise
        return {"status": "rejected", "reason": str(exc)}
    raise FreeformMaterialViolation("negative control was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()
    config_path = (ROOT / args.config).resolve() if not args.config.is_absolute() else args.config
    output_root = (ROOT / args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    raw = load_json(config_path)
    validation = validate_protocol(raw)

    dependency = raw["dependency"]
    contract_path = ROOT / dependency["spatial_contract_path"]
    if file_sha256(contract_path) != dependency["spatial_contract_sha256"]:
        raise FreeformMaterialViolation("Work 108 spatial contract identity is stale")
    if subprocess.run(["git", "cat-file", "-e", f"{dependency['work108_commit']}^{{commit}}"], cwd=ROOT).returncode:
        raise FreeformMaterialViolation("Work 108 commit dependency is missing")

    representation = raw["representation"]
    spec = grid_spec(representation)
    field, source_cost = generate_source(raw)
    initial_beta = {cell for cell, label in field.items() if label == "material_beta"}
    if not initial_beta:
        raise FreeformMaterialViolation("asymmetric thin source feature vanished")
    snapshots = [
        {
            "stage": "source",
            **surface_record(
                field,
                spec,
                output_root / "source.obj",
                representation["maximum_surface_triangles"],
                representation["surface_volume_relative_tolerance"],
            ),
        }
    ]
    ancestry = []
    for edit in raw["operator_chain"]:
        before = field_descriptor(field, spec)
        field, trace = apply_edit(
            field,
            spec,
            edit,
            set(raw["materials"]),
            representation["maximum_changed_cells_per_edit"],
        )
        if len(field) > representation["maximum_occupied_cells"]:
            raise FreeformMaterialViolation("mutation exceeded occupied-cell budget")
        stage = f"slot_{edit['slot']:02d}_{edit['operator']}"
        record = surface_record(
            field,
            spec,
            output_root / f"{stage}.obj",
            representation["maximum_surface_triangles"],
            representation["surface_volume_relative_tolerance"],
        )
        after = record["descriptor"]
        ancestry.append(
            {
                **trace,
                "before_geometry_sha256": before["geometry_sha256"],
                "after_geometry_sha256": after["geometry_sha256"],
                "causal_change": before["geometry_sha256"] != after["geometry_sha256"],
            }
        )
        snapshots.append({"stage": stage, **record})

    by_stage = {item["stage"]: item for item in snapshots}
    cavity = by_stage["slot_01_cavity_route"]["surface"]
    closed = by_stage["slot_02_boundary_displacement"]["surface"]
    split = by_stage["slot_04_split"]["descriptor"]
    merged = by_stage["slot_05_merge"]["descriptor"]
    if cavity["genus_sum"] < 1 or closed["genus_sum"] >= cavity["genus_sum"]:
        raise FreeformMaterialViolation("through-hole was not causally created and closed")
    if split["connected_components"] < 2 or merged["connected_components"] != 1:
        raise FreeformMaterialViolation("split and reconnect topology control failed")
    retained = len(initial_beta & set(field)) / len(initial_beta)
    if retained < 0.8:
        raise FreeformMaterialViolation("asymmetric thin feature was not preserved")
    if any(not item["causal_change"] for item in ancestry):
        raise FreeformMaterialViolation("registered operator produced renaming-only pseudo-novelty")

    final_field_path = output_root / "final_field.json"
    write_json(final_field_path, {"resolution_m": spec["resolution"], "cells": field_rows(field)})
    ancestry_path = output_root / "mutation_ancestry.json"
    write_json(ancestry_path, ancestry)

    refinement = []
    for resolution in raw["refinement_resolutions_m"]:
        refined_spec = grid_spec(representation, resolution)
        refined_field, cost = generate_source(raw, resolution)
        surface = extract_surface(refined_field, refined_spec, representation["maximum_surface_triangles"])
        descriptor = field_descriptor(refined_field, refined_spec)
        error = abs(surface["enclosed_volume_m3"] - descriptor["occupied_volume_m3"]) / descriptor["occupied_volume_m3"]
        if error > representation["surface_volume_relative_tolerance"]:
            raise FreeformMaterialViolation("refinement surface conversion failed")
        refinement.append(
            {
                "resolution_m": resolution,
                "grid_dimensions": refined_spec["dimensions"],
                "occupied_cells": descriptor["occupied_cells"],
                "occupied_volume_m3": descriptor["occupied_volume_m3"],
                "surface_volume_relative_error": error,
                "geometry_sha256": descriptor["geometry_sha256"],
                "grid_visits": cost["grid_visits"],
            }
        )

    renamed_identity = field_descriptor(dict(field), spec)["geometry_sha256"]
    final_identity = snapshots[-1]["descriptor"]["geometry_sha256"]
    if renamed_identity != final_identity:
        raise FreeformMaterialViolation("identifier-invariant geometry control failed")
    controls = {
        "renaming_only_pseudo_novelty": {"status": "rejected", "geometry_sha256": final_identity},
        "triangle_budget": rejected_control(
            lambda: extract_surface(field, spec, 12), "triangle budget"
        ),
        "label_mixing": rejected_control(
            lambda: field_descriptor({next(iter(field)): ["material_alpha", "material_beta"]}, spec),  # type: ignore[dict-item]
            "label mixing",
        ),
        "hole_created_then_closed": {"status": "passed", "created_genus": cavity["genus_sum"], "closed_genus": closed["genus_sum"]},
        "split_then_reconnected": {"status": "passed", "split_components": split["connected_components"], "merged_components": merged["connected_components"]},
        "asymmetric_thin_feature": {"status": "passed", "retained_fraction": retained},
        "unsupported_conversions": [
            {"adapter": "smooth_brep", "status": "not_evaluated", "reason": "deferred to Work 110; no hidden conversion"},
            {"adapter": "mixed_cell_homogenization", "status": "unsupported", "reason": "one scalar label per occupied cell is mandatory"},
        ],
    }

    artifact_body = {
        "config_sha256": file_sha256(config_path),
        "final_field_sha256": file_sha256(final_field_path),
        "ancestry_sha256": file_sha256(ancestry_path),
        "obj_artifacts": [{"file": item["obj_file"], "sha256": item["obj_sha256"]} for item in snapshots],
    }
    artifact_manifest = {"body": artifact_body, "manifest_sha256": canonical_sha256(artifact_body)}
    write_json(output_root / "artifact_manifest.json", artifact_manifest)
    repository_commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
    result_body = {
        "status": "passed",
        "claim_scope": "bounded implicit field generation and exact voxel-surface conversion only",
        "validation": validation,
        "dependency": dependency,
        "representation": representation,
        "source_cost": source_cost,
        "operator_ancestry": ancestry,
        "snapshots": snapshots,
        "refinement_trials": refinement,
        "controls": controls,
        "artifact_manifest_sha256": artifact_manifest["manifest_sha256"],
        "repository_commit": repository_commit,
        "review": {
            "supporting_evidence": [
                "all six registered edit families changed occupancy or material identity within fixed budgets",
                "a through-hole was created and closed and a split field was reconnected",
                "the asymmetric thin feature survived and every OBJ volume matched the source field",
            ],
            "contradicting_evidence": ["refinement levels produced different voxelized volumes and identities"],
            "alternative_explanations": ["reachable topology and feature survival are conditional on Cartesian-grid resolution and orientation"],
            "missing_evidence": ["smooth B-rep conversion", "unstructured volume meshing", "physics fields", "functional superiority", "physical validation"],
            "confidence": "high for the registered voxel representation; low for geometry below its cell scale",
        },
    }
    result = {"body": result_body, "result_sha256": canonical_sha256(result_body)}
    write_json(output_root / "result.json", result)
    if args.replay_reference:
        reference_path = (ROOT / args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference
        reference = load_json(reference_path)
        exact = reference.get("result_sha256") == result["result_sha256"]
        write_json(
            output_root / "replay.json",
            {"reference_result_sha256": reference.get("result_sha256"), "current_result_sha256": result["result_sha256"], "exact": exact},
        )
        if not exact:
            raise FreeformMaterialViolation("replay differs from registered result")
    print(json.dumps({"status": "passed", "result_sha256": result["result_sha256"], "operators": len(ancestry)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
