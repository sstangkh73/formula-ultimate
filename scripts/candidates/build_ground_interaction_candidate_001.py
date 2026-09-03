"""Build and evaluate the Work 083 ground-interaction candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import cadquery as cq  # noqa: E402

from formula_ultimate.subsystems.ground_interaction import (  # noqa: E402
    GroundInteractionViolation,
    canonical_sha256,
    evaluate_candidate,
    validate_declaration,
)


MM = 1000.0


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonicalize_step(path: Path) -> None:
    text = path.read_text(encoding="ascii", errors="strict")
    updated, count = re.subn(
        r"(FILE_NAME\('[^']*',)'[^']*'",
        r"\1'1970-01-01T00:00:00'",
        text,
        count=1,
    )
    if count != 1:
        raise GroundInteractionViolation("STEP timestamp is missing or ambiguous")
    path.write_text(updated, encoding="ascii", newline="\n")


def _box(size_m: list[float], center_m: tuple[float, float, float]) -> cq.Shape:
    return (
        cq.Workplane("XY")
        .box(*(value * MM for value in size_m), centered=(True, True, True))
        .val()
        .translate(tuple(value * MM for value in center_m))
    )


def _guide(geometry: dict[str, Any]) -> cq.Shape:
    x = geometry["mount_hole_center_x_m"]
    bridge_size = geometry["bridge_size_m"]
    bridge = _box(bridge_size, (x, 0.0, -bridge_size[2] / 2.0))
    rail_size = geometry["rail_size_m"]
    rail_z = -bridge_size[2] - rail_size[2] / 2.0
    left = _box(rail_size, (x, geometry["rail_center_y_m"], rail_z))
    right = _box(rail_size, (x, -geometry["rail_center_y_m"], rail_z))
    pin = cq.Solid.makeCylinder(
        geometry["pin_radius_m"] * MM,
        geometry["pin_height_m"] * MM,
        cq.Vector(x * MM, 0.0, -bridge_size[2] * MM),
        cq.Vector(0.0, 0.0, 1.0),
    )
    return bridge.fuse(left).fuse(right).fuse(pin)


def _carrier(geometry: dict[str, Any]) -> cq.Shape:
    x = geometry["center_x_m"]
    stem = _box(geometry["stem_size_m"], (x, 0.0, geometry["stem_center_z_m"]))
    crossbar = _box(
        geometry["crossbar_size_m"], (x, 0.0, geometry["crossbar_center_z_m"])
    )
    arms = []
    for sign in (-1.0, 1.0):
        arm = _box(
            geometry["arm_size_m"],
            (x, sign * geometry["arm_center_y_m"], geometry["arm_center_z_m"]),
        )
        cutter = cq.Solid.makeCylinder(
            geometry["axle_bore_radius_m"] * MM,
            (geometry["arm_size_m"][1] + 0.004) * MM,
            cq.Vector(
                x * MM,
                (sign * geometry["arm_center_y_m"] - sign * (geometry["arm_size_m"][1] / 2.0 + 0.002)) * MM,
                geometry["axle_center_z_m"] * MM,
            ),
            cq.Vector(0.0, sign, 0.0),
        )
        arms.append(arm.cut(cutter))
    return stem.fuse(crossbar).fuse(arms[0]).fuse(arms[1])


def _axle(geometry: dict[str, Any]) -> cq.Shape:
    return cq.Solid.makeCylinder(
        geometry["radius_m"] * MM,
        geometry["length_m"] * MM,
        cq.Vector(
            geometry["center_x_m"] * MM,
            -geometry["length_m"] * MM / 2.0,
            geometry["center_z_m"] * MM,
        ),
        cq.Vector(0.0, 1.0, 0.0),
    )


def _roller(geometry: dict[str, Any]) -> cq.Shape:
    origin = cq.Vector(
        geometry["center_x_m"] * MM,
        -geometry["width_m"] * MM / 2.0,
        geometry["center_z_m"] * MM,
    )
    axis = cq.Vector(0.0, 1.0, 0.0)
    outer = cq.Solid.makeCylinder(
        geometry["outer_radius_m"] * MM, geometry["width_m"] * MM, origin, axis
    )
    inner = cq.Solid.makeCylinder(
        geometry["inner_radius_m"] * MM,
        (geometry["width_m"] + 0.002) * MM,
        cq.Vector(origin.x, origin.y - 1.0, origin.z),
        axis,
    )
    return outer.cut(inner)


def _build_shapes(raw: dict[str, Any], output_root: Path) -> tuple[dict[str, cq.Shape], list[dict[str, Any]]]:
    shapes: dict[str, cq.Shape] = {}
    records = []
    for part in raw["parts"]:
        part_id = part["part_id"]
        geometry = part["geometry"]
        step_path = output_root / f"{part_id}.step"
        kind = geometry["kind"]
        if kind == "frozen_step":
            source = ROOT / geometry["source_step"]
            if not source.is_file() or _sha256(source) != geometry["expected_step_sha256"]:
                raise GroundInteractionViolation("frozen structural mount STEP is missing or changed")
            shutil.copyfile(source, step_path)
            shape = cq.importers.importStep(str(step_path)).val()
        elif kind == "guide_frame":
            shape = _guide(geometry)
        elif kind == "carrier":
            shape = _carrier(geometry)
        elif kind == "axle":
            shape = _axle(geometry)
        elif kind == "annular_roller":
            shape = _roller(geometry)
        else:
            raise GroundInteractionViolation(f"unsupported part geometry kind: {kind}")
        if not shape.isValid() or len(shape.Solids()) != 1 or shape.Volume() <= 0.0:
            raise GroundInteractionViolation(f"{part_id} is not one valid positive-volume solid")
        if kind != "frozen_step":
            cq.exporters.export(shape, str(step_path), exportType="STEP")
            _canonicalize_step(step_path)
        bounds = shape.BoundingBox()
        shapes[part_id] = shape
        records.append(
            {
                "part_id": part_id,
                "step_file": step_path.name,
                "step_sha256": _sha256(step_path),
                "valid": True,
                "solid_count": 1,
                "volume_m3": shape.Volume() * 1.0e-9,
                "bounding_box_m": {
                    "minimum": [bounds.xmin / MM, bounds.ymin / MM, bounds.zmin / MM],
                    "maximum": [bounds.xmax / MM, bounds.ymax / MM, bounds.zmax / MM],
                },
                "synthetic_mass_kg": shape.Volume() * 1.0e-9 * part["synthetic_density_kg_per_m3"],
            }
        )
    return shapes, records


def _at_translation(
    shapes: dict[str, cq.Shape], moving_parts: set[str], translation_m: float
) -> dict[str, cq.Shape]:
    return {
        part_id: shape.translate((0.0, 0.0, translation_m * MM))
        if part_id in moving_parts
        else shape
        for part_id, shape in shapes.items()
    }


def _clearance_records(raw: dict[str, Any], shapes: dict[str, cq.Shape]) -> list[dict[str, Any]]:
    samples = [
        ("minimum", raw["motion"]["travel_min_m"]),
        ("reference", raw["motion"]["reference_translation_m"]),
        ("maximum", raw["motion"]["travel_max_m"]),
    ]
    moving = set(raw["motion"]["moving_parts"])
    part_ids = [part["part_id"] for part in raw["parts"]]
    forbidden = {tuple(pair) for pair in raw["clearance"]["forbidden_pairs"]}
    forbidden |= {(b, a) for a, b in forbidden}
    output = []
    for state, translation in samples:
        placed = _at_translation(shapes, moving, translation)
        maximum_overlap = 0.0
        forbidden_clearances = []
        pairs = []
        for i, first in enumerate(part_ids):
            for second in part_ids[i + 1 :]:
                overlap = placed[first].intersect(placed[second]).Volume() * 1.0e-9
                distance = float(placed[first].distance(placed[second])) / MM
                maximum_overlap = max(maximum_overlap, overlap)
                is_forbidden = (first, second) in forbidden
                if is_forbidden:
                    forbidden_clearances.append(distance)
                pairs.append(
                    {
                        "parts": [first, second],
                        "forbidden": is_forbidden,
                        "clearance_m": distance,
                        "overlap_m3": overlap,
                    }
                )
        output.append(
            {
                "state": state,
                "translation_m": translation,
                "minimum_forbidden_clearance_m": min(forbidden_clearances),
                "maximum_overlap_m3": maximum_overlap,
                "pairs": pairs,
            }
        )
    return output


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _run_freecad(freecad_python: Path, output_root: Path, manifest_path: Path) -> dict[str, Any]:
    report_path = output_root / "freecad_report.json"
    fcstd_path = output_root / "ground_interaction_candidate_001.FCStd"
    env = os.environ.copy()
    env.update(
        {
            "FORMULA_ULTIMATE_W083_MANIFEST": str(manifest_path.resolve()),
            "FORMULA_ULTIMATE_W083_STEP_ROOT": str(output_root.resolve()),
            "FORMULA_ULTIMATE_W083_FREECAD_REPORT": str(report_path.resolve()),
            "FORMULA_ULTIMATE_W083_FCSTD": str(fcstd_path.resolve()),
        }
    )
    process = subprocess.run(
        [str(freecad_python), str(ROOT / "scripts/candidates/inspect_ground_interaction_freecad.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode != 0:
        raise GroundInteractionViolation(
            f"FreeCAD inspection failed with exit {process.returncode}: {process.stderr or process.stdout}"
        )
    if not report_path.is_file() or not fcstd_path.is_file():
        raise GroundInteractionViolation(
            "FreeCAD did not create its report and FCStd witness: "
            + (process.stderr or process.stdout)
        )
    return json.loads(report_path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--structural-result", type=Path, required=True)
    parser.add_argument("--freecad-python", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()

    raw = json.loads(args.config.read_text(encoding="utf-8"))
    declaration = validate_declaration(raw)
    if args.structural_result.resolve() != (ROOT / raw["structural_evidence"]["result_path"]).resolve():
        raise GroundInteractionViolation("structural result path differs from the frozen declaration")
    structural = json.loads(args.structural_result.read_text(encoding="utf-8"))
    args.output_root.mkdir(parents=True, exist_ok=True)
    shapes, parts = _build_shapes(raw, args.output_root)
    clearance = _clearance_records(raw, shapes)
    compound = cq.Compound.makeCompound([shapes[item["part_id"]] for item in raw["parts"]])
    assembly_path = args.output_root / "ground_interaction_candidate_001.step"
    cq.exporters.export(compound, str(assembly_path), exportType="STEP")
    _canonicalize_step(assembly_path)
    manifest_body = {
        "candidate_id": raw["candidate_id"],
        "declaration_sha256": declaration["declaration_sha256"],
        "hidden_geometry_repair": False,
        "parts": parts,
        "assembly": {
            "step_file": assembly_path.name,
            "step_sha256": _sha256(assembly_path),
            "valid": bool(compound.isValid()),
            "solid_count": len(compound.Solids()),
            "volume_m3": compound.Volume() * 1.0e-9,
        },
        "motion_clearance": clearance,
    }
    manifest = {**manifest_body, "manifest_sha256": canonical_sha256(manifest_body)}
    manifest_path = args.output_root / "geometry_manifest.json"
    _write_json(manifest_path, manifest)

    freecad = _run_freecad(args.freecad_python, args.output_root, manifest_path)
    evaluation = evaluate_candidate(raw, manifest, freecad, structural)
    _write_json(args.output_root / "evaluation.json", evaluation)
    result_body = {
        "status": "passed",
        "candidate_id": raw["candidate_id"],
        "candidate_verdict": evaluation["candidate_verdict"],
        "design_use_allowed": False,
        "declaration_sha256": declaration["declaration_sha256"],
        "manifest_sha256": manifest["manifest_sha256"],
        "assembly_step_sha256": manifest["assembly"]["step_sha256"],
        "part_step_sha256": {item["part_id"]: item["step_sha256"] for item in parts},
        "freecad_report_sha256": freecad["report_sha256"],
        "evaluation_sha256": evaluation["evaluation_sha256"],
        "structural_result_sha256": structural["result_sha256"],
    }
    result = {**result_body, "result_sha256": canonical_sha256(result_body)}
    result_path = args.output_root / "result.json"
    _write_json(result_path, result)

    replay = None
    if args.replay_reference:
        reference = json.loads(args.replay_reference.read_text(encoding="utf-8"))
        identity_fields = [
            "declaration_sha256",
            "manifest_sha256",
            "assembly_step_sha256",
            "part_step_sha256",
            "freecad_report_sha256",
            "evaluation_sha256",
            "structural_result_sha256",
            "result_sha256",
        ]
        exact = all(reference.get(field) == result.get(field) for field in identity_fields)
        replay_body = {
            "status": "passed" if exact else "failed",
            "exact": exact,
            "identity_fields": identity_fields,
            "reference_result_sha256": reference.get("result_sha256"),
            "replay_result_sha256": result["result_sha256"],
        }
        replay = {**replay_body, "replay_sha256": canonical_sha256(replay_body)}
        _write_json(args.output_root / "replay.json", replay)
        if not exact:
            raise GroundInteractionViolation("exact replay identity comparison failed")

    print(
        json.dumps(
            {
                "status": "passed",
                "candidate_verdict": result["candidate_verdict"],
                "part_count": len(parts),
                "assembly_solid_count": manifest["assembly"]["solid_count"],
                "mobility_dof": evaluation["declaration"]["mobility_dof"],
                "minimum_clearance_m": evaluation["geometry"]["minimum_forbidden_clearance_m"],
                "maximum_overlap_m3": evaluation["geometry"]["maximum_overlap_m3"],
                "force_residual_relative": evaluation["physics"]["force_residual_relative"],
                "moment_residual_relative": evaluation["physics"]["moment_residual_relative"],
                "energy_residual_relative": evaluation["physics"]["drive_energy_residual_relative"],
                "result_sha256": result["result_sha256"],
                "replay_exact": None if replay is None else replay["exact"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
