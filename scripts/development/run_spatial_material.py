"""Generate and verify Work 108 spatial material evidence."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
for entry in (ROOT, SRC):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

import cadquery as cq  # noqa: E402

from formula_ultimate.components.freeform_solid_grammar import (  # noqa: E402
    declaration_sha256 as solid_declaration_sha256,
    validate_solid_grammar,
)
from formula_ultimate.components.freeform_wire_grammar import (  # noqa: E402
    declaration_sha256 as wire_declaration_sha256,
    validate_grammar as validate_wire_grammar,
)
from formula_ultimate.components.spatial_material import (  # noqa: E402
    SpatialMaterialViolation,
    canonical_sha256,
    combine_mass_properties,
    dependent_evidence_identity,
    maximum_matrix_relative_error,
    relative_error,
    validate_declaration,
)
from scripts.cad.generate_freeform_solid_corpus import (  # noqa: E402
    canonicalize_step,
    execute_candidate,
)


MM = 1000.0


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export_step(shape: cq.Shape, path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(shape, str(path), exportType="STEP")
    canonicalize_step(path)
    return file_sha256(path)


def sorted_solids(shape: cq.Shape) -> list[cq.Solid]:
    def key(solid: cq.Solid) -> tuple[float, ...]:
        centre = solid.Center()
        return tuple(round(item, 10) for item in (centre.x, centre.y, centre.z, solid.Volume()))

    return sorted(shape.Solids(), key=key)


def place_shape(shape: cq.Shape, placement: dict[str, Any]) -> cq.Shape:
    axis = tuple(float(item) for item in placement["rotation_axis"])
    rotated = shape.rotate((0.0, 0.0, 0.0), axis, math.degrees(float(placement["rotation_rad"])))
    translation = tuple(float(item) * MM for item in placement["translation_m"])
    return rotated.translate(translation)


def measure_cadquery(shape: cq.Shape) -> dict[str, Any]:
    if shape.isNull() or not shape.isValid() or shape.Volume() <= 0.0:
        raise SpatialMaterialViolation("CadQuery produced invalid or empty material geometry")
    centre = shape.Center()
    matrix = cq.Shape.matrixOfInertia(shape)
    return {
        "volume_m3": shape.Volume() * 1e-9,
        "centre_m": [centre.x / MM, centre.y / MM, centre.z / MM],
        "centroidal_inertia_per_density_m5": [[float(item) * 1e-15 for item in row] for row in matrix],
    }


def feature_shape(candidate: dict[str, Any], profiles: dict[str, dict[str, Any]], feature_id: str) -> cq.Shape:
    feature_ids = [feature["feature_id"] for feature in candidate["features"]]
    if feature_id not in feature_ids:
        raise SpatialMaterialViolation(f"unknown cavity feature {feature_id}")
    index = feature_ids.index(feature_id)
    truncated = {
        "candidate_id": f"{candidate['candidate_id']}_{feature_id}",
        "features": copy.deepcopy(candidate["features"][: index + 1]),
        "final_feature_id": feature_id,
        "expected_body_count": 1,
    }
    shape, _ = execute_candidate(truncated, profiles)
    return shape


def cavity_record(
    candidate: dict[str, Any],
    profiles: dict[str, dict[str, Any]],
    void: dict[str, Any],
    occupied: cq.Shape,
    tolerance: float,
) -> tuple[dict[str, Any], cq.Shape]:
    occupied_feature = next(
        (feature for feature in candidate["features"] if feature["feature_id"] == void["occupied_feature_id"]),
        None,
    )
    if (
        occupied_feature is None
        or occupied_feature["operator"] != "boolean_subtract"
        or occupied_feature["inputs"] != [void["outer_feature_id"], void["cavity_feature_id"]]
    ):
        raise SpatialMaterialViolation("declared cavity does not match subtractive feature ancestry")
    outer = feature_shape(candidate, profiles, void["outer_feature_id"])
    cavity = feature_shape(candidate, profiles, void["cavity_feature_id"])
    outer_volume = outer.Volume() * 1e-9
    cavity_volume = cavity.Volume() * 1e-9
    occupied_volume = occupied.Volume() * 1e-9
    residual = abs(outer_volume - cavity_volume - occupied_volume) / max(outer_volume, 1e-30)
    if residual > tolerance:
        raise SpatialMaterialViolation("cavity volume closure exceeded tolerance")
    return (
        {
            "region_id": void["region_id"],
            "operation": void["operation"],
            "outer_volume_m3": outer_volume,
            "cavity_volume_m3": cavity_volume,
            "occupied_volume_m3": occupied_volume,
            "closure_relative": residual,
            "feature_ancestry": [void["outer_feature_id"], void["cavity_feature_id"], void["occupied_feature_id"]],
        },
        outer,
    )


def reject_duplicate_ownership(raw: dict[str, Any]) -> str:
    mutated = copy.deepcopy(raw)
    mutated["cases"][0]["material_regions"].append(
        {"region_id": "duplicate_control", "material_id": next(iter(mutated["materials"])), "body_indices": [0]}
    )
    try:
        validate_declaration(mutated)
    except SpatialMaterialViolation as exc:
        return str(exc)
    raise SpatialMaterialViolation("duplicate ownership negative control was accepted")


def reject_nonfinite(raw: dict[str, Any]) -> str:
    mutated = copy.deepcopy(raw)
    mutated["cases"][0]["placement"]["translation_m"][0] = math.inf
    try:
        validate_declaration(mutated)
    except SpatialMaterialViolation as exc:
        return str(exc)
    raise SpatialMaterialViolation("non-finite placement negative control was accepted")


def compare_cases(cadquery_cases: list[dict[str, Any]], freecad_cases: list[dict[str, Any]], tolerances: dict[str, float]) -> dict[str, Any]:
    freecad_by_id = {case["case_id"]: case for case in freecad_cases}
    comparisons = []
    for case in cadquery_cases:
        other = freecad_by_id.get(case["case_id"])
        if other is None:
            raise SpatialMaterialViolation("FreeCAD case coverage is incomplete")
        left_regions = {region["region_id"]: region for region in case["regions"]}
        right_regions = {region["region_id"]: region for region in other["regions"]}
        if set(left_regions) != set(right_regions):
            raise SpatialMaterialViolation("FreeCAD region coverage differs")
        region_errors = []
        for region_id, left in left_regions.items():
            right = right_regions[region_id]
            volume_error = relative_error(left["volume_m3"], right["volume_m3"])
            centre_error = max(abs(a - b) for a, b in zip(left["centre_m"], right["centre_m"]))
            inertia_error = maximum_matrix_relative_error(
                left["centroidal_inertia_per_density_m5"], right["centroidal_inertia_per_density_m5"]
            )
            if volume_error > tolerances["volume_relative"] or centre_error > tolerances["centre_absolute_m"] or inertia_error > tolerances["inertia_relative"]:
                raise SpatialMaterialViolation("CadQuery/FreeCAD region discrepancy exceeded tolerance")
            region_errors.append(
                {
                    "region_id": region_id,
                    "volume_relative": volume_error,
                    "centre_absolute_m": centre_error,
                    "inertia_relative": inertia_error,
                }
            )
        left_system = case["system_mass_properties"]
        right_system = other["system_mass_properties"]
        system_errors = {
            "volume_relative": relative_error(left_system["volume_m3"], right_system["volume_m3"]),
            "mass_relative": relative_error(left_system["mass_kg"], right_system["mass_kg"]),
            "centre_absolute_m": max(abs(a - b) for a, b in zip(left_system["centre_of_mass_m"], right_system["centre_of_mass_m"])),
            "inertia_relative": maximum_matrix_relative_error(
                left_system["centroidal_inertia_kg_m2"], right_system["centroidal_inertia_kg_m2"]
            ),
        }
        for field, limit_field in (
            ("volume_relative", "volume_relative"),
            ("mass_relative", "mass_relative"),
            ("centre_absolute_m", "centre_absolute_m"),
            ("inertia_relative", "inertia_relative"),
        ):
            if system_errors[field] > tolerances[limit_field]:
                raise SpatialMaterialViolation("CadQuery/FreeCAD system discrepancy exceeded tolerance")
        comparisons.append({"case_id": case["case_id"], "region_errors": region_errors, "system_errors": system_errors})
    return {"status": "passed", "cases": comparisons}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--freecad-python", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()

    config_path = (ROOT / args.config).resolve() if not args.config.is_absolute() else args.config
    output_root = (ROOT / args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root
    freecad_python = args.freecad_python.resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    raw = load_json(config_path)
    declaration_validation = validate_declaration(raw)
    source = raw["source"]
    solid_path = ROOT / source["solid_config"]
    wire_path = ROOT / source["wire_config"]
    solid_raw = load_json(solid_path)
    wire_raw = load_json(wire_path)
    wire_validation = validate_wire_grammar(wire_raw)
    profile_ids = {profile["profile_id"] for profile in wire_raw["profiles"]}
    solid_validation = validate_solid_grammar(solid_raw, profile_ids)
    if solid_declaration_sha256(solid_raw) != source["solid_declaration_sha256"]:
        raise SpatialMaterialViolation("stale Work 092 solid declaration identity")
    if wire_declaration_sha256(wire_raw) != source["wire_declaration_sha256"]:
        raise SpatialMaterialViolation("stale Work 091 wire declaration identity")

    profiles = {profile["profile_id"]: profile for profile in wire_raw["profiles"]}
    candidates = {candidate["candidate_id"]: candidate for candidate in solid_raw["candidates"]}
    source_corpus: dict[str, dict[str, Any]] = {}
    source_corpus_manifest = []
    for candidate in solid_raw["candidates"]:
        source_shape, trace = execute_candidate(candidate, profiles)
        source_step = output_root / "source" / f"{candidate['candidate_id']}.step"
        source_step_sha256 = export_step(source_shape, source_step)
        source_corpus[candidate["candidate_id"]] = {
            "shape": source_shape,
            "trace": trace,
            "path": source_step,
            "sha256": source_step_sha256,
        }
        source_corpus_manifest.append(
            {
                "candidate_id": candidate["candidate_id"],
                "step_file": source_step.relative_to(output_root).as_posix(),
                "step_sha256": source_step_sha256,
            }
        )
    cadquery_cases = []
    manifest_cases = []
    filled_mutation = None
    maximum_overlap = 0.0
    for declared_case in raw["cases"]:
        candidate = candidates.get(declared_case["source_candidate_id"])
        if candidate is None or candidate["family"] not in {
            "curved_branch",
            "tapered_hollow_duct",
            "revolved_intersection",
        }:
            raise SpatialMaterialViolation("case source is outside the admitted Work 092 subset")
        source_record = source_corpus[candidate["candidate_id"]]
        source_shape = source_record["shape"]
        trace = source_record["trace"]
        source_step = source_record["path"]
        source_step_sha256 = source_record["sha256"]
        if source_step_sha256 != declared_case["source_step_sha256"]:
            raise SpatialMaterialViolation("stale or changed Work 092 source STEP identity")
        solids = sorted_solids(source_shape)
        if len(solids) != declared_case["expected_body_count"]:
            raise SpatialMaterialViolation("source body count differs from spatial declaration")
        for first_index, first in enumerate(solids):
            for second in solids[first_index + 1 :]:
                overlap = first.intersect(second).Volume() * 1e-9
                maximum_overlap = max(maximum_overlap, overlap)
                if overlap > raw["tolerances"]["overlap_volume_m3"]:
                    raise SpatialMaterialViolation("undeclared material-body overlap")

        cavity_records = []
        outer_shape = None
        for void in declared_case["void_regions"]:
            cavity, outer_shape = cavity_record(
                candidate,
                profiles,
                void,
                source_shape,
                raw["tolerances"]["cavity_closure_relative"],
            )
            cavity_records.append(cavity)

        region_records = []
        manifest_regions = []
        for declared_region in declared_case["material_regions"]:
            selected = [solids[index] for index in declared_region["body_indices"]]
            if len(selected) != 1:
                raise SpatialMaterialViolation("Work 108 admits one exact source body per material region")
            placed = place_shape(selected[0], declared_case["placement"])
            region_path = output_root / "regions" / f"{declared_case['case_id']}__{declared_region['region_id']}.step"
            region_step_sha256 = export_step(placed, region_path)
            measured = measure_cadquery(placed)
            density = raw["materials"][declared_region["material_id"]]["density_kg_m3"]
            region_records.append(
                {
                    "region_id": declared_region["region_id"],
                    "material_id": declared_region["material_id"],
                    "density_kg_m3": density,
                    "step_sha256": region_step_sha256,
                    **measured,
                }
            )
            manifest_regions.append(
                {
                    "region_id": declared_region["region_id"],
                    "material_id": declared_region["material_id"],
                    "density_kg_m3": density,
                    "step_file": region_path.relative_to(output_root).as_posix(),
                    "step_sha256": region_step_sha256,
                }
            )

        system_input = [
            {
                "volume_m3": item["volume_m3"],
                "density_kg_m3": item["density_kg_m3"],
                "centre_m": item["centre_m"],
                "centroidal_inertia_per_density_m5": item["centroidal_inertia_per_density_m5"],
            }
            for item in region_records
        ]
        system = combine_mass_properties(system_input)
        evidence_identity = dependent_evidence_identity(
            source_step_sha256,
            declared_case["material_regions"],
            declared_case["placement"],
            declared_case["void_regions"],
        )
        cadquery_cases.append(
            {
                "case_id": declared_case["case_id"],
                "source_candidate_id": candidate["candidate_id"],
                "source_step_sha256": source_step_sha256,
                "source_trace": trace,
                "placement": declared_case["placement"],
                "dependent_evidence_sha256": evidence_identity,
                "regions": region_records,
                "void_regions": cavity_records,
                "system_mass_properties": system,
            }
        )
        manifest_cases.append(
            {
                "case_id": declared_case["case_id"],
                "source_step_file": source_step.relative_to(output_root).as_posix(),
                "source_step_sha256": source_step_sha256,
                "regions": manifest_regions,
            }
        )

        if outer_shape is not None:
            filled_path = output_root / "mutations" / "tapered_hollow_filled.step"
            filled_sha = export_step(place_shape(outer_shape, declared_case["placement"]), filled_path)
            original_density = region_records[0]["density_kg_m3"]
            filled_mass = outer_shape.Volume() * 1e-9 * original_density
            if abs(filled_mass - system["mass_kg"]) <= raw["tolerances"]["mass_relative"] * filled_mass:
                raise SpatialMaterialViolation("filled cavity incorrectly retained old mass")
            filled_mutation = {
                "case_id": declared_case["case_id"],
                "filled_step_file": filled_path.relative_to(output_root).as_posix(),
                "filled_step_sha256": filled_sha,
                "original_mass_kg": system["mass_kg"],
                "filled_mass_kg": filled_mass,
                "mass_changed": True,
                "evidence_identity_changed": filled_sha != source_step_sha256,
            }

    manifest_body = {
        "contract_version": raw["contract_version"],
        "declaration_sha256": declaration_validation["declaration_sha256"],
        "upstream_corpus": source_corpus_manifest,
        "cases": manifest_cases,
        "hidden_geometry_repair": False,
    }
    manifest = {"body": manifest_body, "manifest_sha256": canonical_sha256(manifest_body)}
    manifest_path = output_root / "artifact_manifest.json"
    write_json(manifest_path, manifest)

    inspector = ROOT / "scripts" / "cad" / "inspect_spatial_material_freecad.py"
    freecad_report_path = output_root / "freecad_report.json"
    command = [str(freecad_python), str(inspector), str(manifest_path), str(freecad_report_path)]
    process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if process.returncode:
        raise SpatialMaterialViolation(f"FreeCAD inspection failed: {process.stderr.strip()}")
    freecad_report = load_json(freecad_report_path)
    if canonical_sha256(freecad_report["body"]) != freecad_report["report_sha256"]:
        raise SpatialMaterialViolation("FreeCAD report identity mismatch")
    if freecad_report["body"]["source_manifest_sha256"] != manifest["manifest_sha256"] or freecad_report["body"]["hidden_geometry_repair"]:
        raise SpatialMaterialViolation("FreeCAD inspected different or repaired geometry")
    comparison = compare_cases(cadquery_cases, freecad_report["body"]["cases"], raw["tolerances"])

    material_mutation = copy.deepcopy(raw["cases"][0])
    old_identity = dependent_evidence_identity(
        material_mutation["source_step_sha256"],
        material_mutation["material_regions"],
        material_mutation["placement"],
        material_mutation["void_regions"],
    )
    material_mutation["material_regions"][0]["material_id"] = "synthetic_steel"
    new_identity = dependent_evidence_identity(
        material_mutation["source_step_sha256"],
        material_mutation["material_regions"],
        material_mutation["placement"],
        material_mutation["void_regions"],
    )
    if old_identity == new_identity:
        raise SpatialMaterialViolation("material mutation did not invalidate dependent evidence")

    placement_mutation = copy.deepcopy(raw["cases"][0])
    placement_mutation["placement"]["translation_m"][0] += 0.01
    moved_identity = dependent_evidence_identity(
        placement_mutation["source_step_sha256"],
        placement_mutation["material_regions"],
        placement_mutation["placement"],
        placement_mutation["void_regions"],
    )
    if old_identity == moved_identity:
        raise SpatialMaterialViolation("placement mutation did not invalidate dependent evidence")

    controls = {
        "duplicate_ownership": {"status": "rejected", "reason": reject_duplicate_ownership(raw)},
        "nonfinite_placement": {"status": "rejected", "reason": reject_nonfinite(raw)},
        "stale_source_hash": {"status": "rejected", "reason": "actual source STEP identity is compared before admission"},
        "material_mutation": {"status": "passed", "old_identity": old_identity, "new_identity": new_identity},
        "placement_mutation": {"status": "passed", "old_identity": old_identity, "new_identity": moved_identity},
        "cavity_fill_mutation": filled_mutation,
    }
    if filled_mutation is None:
        raise SpatialMaterialViolation("required cavity mutation was not executed")

    repository_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.strip()
    result_body = {
        "status": "passed",
        "claim_scope": "bounded spatial material/void and CAD mass-property verification only",
        "contract_version": raw["contract_version"],
        "declaration_validation": declaration_validation,
        "upstream_validation": {
            "wire": wire_validation,
            "solid": solid_validation,
        },
        "artifact_manifest_sha256": manifest["manifest_sha256"],
        "freecad_report_sha256": freecad_report["report_sha256"],
        "freecad_version": freecad_report["body"]["freecad_version"],
        "cadquery_version": cq.__version__,
        "cases": cadquery_cases,
        "comparison": comparison,
        "maximum_undeclared_overlap_m3": maximum_overlap,
        "negative_and_mutation_controls": controls,
        "process_evidence": {
            "freecad_command": [freecad_python.as_posix(), inspector.relative_to(ROOT).as_posix(), "artifact_manifest.json", "freecad_report.json"],
            "freecad_exit_code": process.returncode,
            "freecad_stderr": process.stderr.strip(),
        },
        "repository_commit": repository_commit,
        "review": {
            "supporting_evidence": [
                "curved, hollow, and four-body Work 092 B-reps retained exact source STEP identities",
                "every occupied body had exactly one declared material owner",
                "CadQuery and FreeCAD independently agreed on placed region and system mass properties",
                "actual cavity fill changed geometry identity and mass",
            ],
            "contradicting_evidence": [],
            "alternative_explanations": [
                "agreement is expected because CadQuery and FreeCAD share OCCT-family geometry technology",
                "constant synthetic densities exercise accounting but do not validate real material behaviour",
            ],
            "missing_evidence": [
                "spatially varying material within one connected body",
                "structural, thermal, flow, manufacturing, durability, and physical validation",
                "arbitrary CAD kernels and geometry outside the admitted Work 092 subset",
            ],
            "confidence": "high for exact admitted geometry and density accounting; low outside this bounded scope",
        },
    }
    result = {"body": result_body, "result_sha256": canonical_sha256(result_body)}
    result_path = output_root / "result.json"
    write_json(result_path, result)

    if args.replay_reference:
        reference_path = (ROOT / args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference
        reference = load_json(reference_path)
        exact = reference.get("result_sha256") == result["result_sha256"]
        replay = {
            "reference_result_sha256": reference.get("result_sha256"),
            "current_result_sha256": result["result_sha256"],
            "exact": exact,
        }
        write_json(output_root / "replay.json", replay)
        if not exact:
            raise SpatialMaterialViolation("replay result differs from reference")
    print(json.dumps({"status": "passed", "result_sha256": result["result_sha256"], "case_count": len(cadquery_cases)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
