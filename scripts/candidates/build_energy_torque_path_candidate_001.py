"""Build and evaluate the Work 084 energy-conversion and torque-path candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import cadquery as cq  # noqa: E402

from formula_ultimate.subsystems.energy_torque_path import (  # noqa: E402
    EnergyTorquePathViolation,
    canonical_sha256,
    evaluate_candidate,
    validate_declaration,
)


MM = 1000.0
THROUGH_MARGIN_M = 0.002


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
        raise EnergyTorquePathViolation("STEP timestamp is missing or ambiguous")
    path.write_text(updated, encoding="ascii", newline="\n")


def _box(size_m: list[float], center_m: tuple[float, float, float]) -> cq.Shape:
    return (
        cq.Workplane("XY")
        .box(*(value * MM for value in size_m), centered=(True, True, True))
        .val()
        .translate(tuple(value * MM for value in center_m))
    )


def _y_cylinder(radius_m: float, x_m: float, z_m: float, y_min_m: float, y_max_m: float) -> cq.Shape:
    return cq.Solid.makeCylinder(
        radius_m * MM,
        (y_max_m - y_min_m) * MM,
        cq.Vector(x_m * MM, y_min_m * MM, z_m * MM),
        cq.Vector(0.0, 1.0, 0.0),
    )


def _z_cylinder(radius_m: float, x_m: float, y_m: float, top_z_m: float, depth_m: float) -> cq.Shape:
    return cq.Solid.makeCylinder(
        radius_m * MM,
        depth_m * MM,
        cq.Vector(x_m * MM, y_m * MM, (top_z_m - depth_m) * MM),
        cq.Vector(0.0, 0.0, 1.0),
    )


def _hollow_vessel(geometry: dict[str, Any]) -> tuple[cq.Shape, float]:
    size = geometry["outer_size_m"]
    center = tuple(geometry["outer_center_m"])
    wall = geometry["wall_thickness_m"]
    cavity_size = [value - 2.0 * wall for value in size]
    if min(cavity_size) <= 0.0:
        raise EnergyTorquePathViolation("vessel wall thickness removes the whole cavity")
    cavity = _box(cavity_size, center)
    shell = _box(size, center).cut(cavity)
    top_z = center[2] + size[2] / 2.0
    port = _z_cylinder(
        geometry["fill_port_radius_m"],
        geometry["fill_port_center_xy_m"][0],
        geometry["fill_port_center_xy_m"][1],
        top_z,
        wall + THROUGH_MARGIN_M,
    )
    return shell.cut(port), cavity.Volume() * 1.0e-9


def _converter_housing(geometry: dict[str, Any]) -> tuple[cq.Shape, float, float]:
    size = geometry["box_size_m"]
    center = tuple(geometry["box_center_m"])
    bore_x, bore_z = geometry["bore_axis_xz_m"]
    y_min = center[1] - size[1] / 2.0 - THROUGH_MARGIN_M
    y_max = center[1] + size[1] / 2.0 + THROUGH_MARGIN_M
    top_z = center[2] + size[2] / 2.0

    body = _box(size, center).cut(_y_cylinder(geometry["bore_radius_m"], bore_x, bore_z, y_min, y_max))
    body = body.cut(
        _z_cylinder(
            geometry["lubrication_port_radius_m"],
            geometry["lubrication_port_center_xy_m"][0],
            geometry["lubrication_port_center_xy_m"][1],
            top_z,
            geometry["lubrication_port_depth_m"],
        )
    )
    base_area = body.Area() * 1.0e-6

    for passage_x in geometry["coolant_passage_x_m"]:
        body = body.cut(
            _y_cylinder(geometry["coolant_passage_radius_m"], passage_x, bore_z, y_min, y_max)
        )
    passage_area = body.Area() * 1.0e-6

    fin_size = [geometry["fin_length_m"], geometry["fin_thickness_m"], geometry["fin_height_m"]]
    for fin_y in geometry["fin_center_y_m"]:
        body = body.fuse(_box(fin_size, (center[0], fin_y, top_z + fin_size[2] / 2.0)))
    final_area = body.Area() * 1.0e-6

    return body, passage_area - base_area, final_area - passage_area


def _build_part(geometry: dict[str, Any]) -> tuple[cq.Shape, dict[str, float]]:
    kind = geometry["kind"]
    if kind == "hollow_vessel":
        shape, cavity = _hollow_vessel(geometry)
        return shape, {"store_cavity_volume_m3": cavity}
    if kind == "converter_housing":
        shape, coolant_delta, fin_delta = _converter_housing(geometry)
        return shape, {
            "housing_coolant_area_delta_m2": coolant_delta,
            "housing_fin_area_delta_m2": fin_delta,
        }
    if kind == "cylinder":
        axis_x, axis_z = geometry["axis_xz_m"]
        return _y_cylinder(geometry["radius_m"], axis_x, axis_z, geometry["y_min_m"], geometry["y_max_m"]), {}
    if kind == "annular_drum":
        axis_x, axis_z = geometry["axis_xz_m"]
        outer = _y_cylinder(geometry["outer_radius_m"], axis_x, axis_z, geometry["y_min_m"], geometry["y_max_m"])
        bore = _y_cylinder(
            geometry["bore_radius_m"],
            axis_x,
            axis_z,
            geometry["y_min_m"] - THROUGH_MARGIN_M,
            geometry["y_max_m"] + THROUGH_MARGIN_M,
        )
        return outer.cut(bore), {}
    if kind == "bored_block":
        size = geometry["box_size_m"]
        center = tuple(geometry["box_center_m"])
        axis_x, axis_z = geometry["bore_axis_xz_m"]
        bore = _y_cylinder(
            geometry["bore_radius_m"],
            axis_x,
            axis_z,
            center[1] - size[1] / 2.0 - THROUGH_MARGIN_M,
            center[1] + size[1] / 2.0 + THROUGH_MARGIN_M,
        )
        return _box(size, center).cut(bore), {}
    raise EnergyTorquePathViolation(f"unsupported part geometry kind: {kind}")


def _build_shapes(
    raw: dict[str, Any], output_root: Path
) -> tuple[dict[str, cq.Shape], list[dict[str, Any]], dict[str, float]]:
    density = raw["material"]["density_kg_per_m3"]
    shapes: dict[str, cq.Shape] = {}
    records: list[dict[str, Any]] = []
    derived: dict[str, float] = {}
    for part in raw["parts"]:
        part_id = part["part_id"]
        shape, extra = _build_part(part["geometry"])
        if not shape.isValid() or len(shape.Solids()) != 1 or shape.Volume() <= 0.0:
            raise EnergyTorquePathViolation(f"{part_id} is not one valid positive-volume solid")
        derived.update(extra)
        step_path = output_root / f"{part_id}.step"
        cq.exporters.export(shape, str(step_path), exportType="STEP")
        _canonicalize_step(step_path)
        bounds = shape.BoundingBox()
        volume = shape.Volume() * 1.0e-9
        shapes[part_id] = shape
        records.append(
            {
                "part_id": part_id,
                "step_file": step_path.name,
                "step_sha256": _sha256(step_path),
                "valid": True,
                "solid_count": 1,
                "volume_m3": volume,
                "mass_kg": volume * density,
                "bounding_box_m": {
                    "minimum": [bounds.xmin / MM, bounds.ymin / MM, bounds.zmin / MM],
                    "maximum": [bounds.xmax / MM, bounds.ymax / MM, bounds.zmax / MM],
                },
            }
        )
    return shapes, records, derived


def _pair_clearance(raw: dict[str, Any], shapes: dict[str, cq.Shape]) -> list[dict[str, Any]]:
    part_ids = [part["part_id"] for part in raw["parts"]]
    contact = {tuple(sorted(pair)) for pair in raw["clearance"]["contact_pairs"]}
    coupling = {tuple(sorted(pair)) for pair in raw["clearance"]["coupling_pairs"]}
    output = []
    for index, first in enumerate(part_ids):
        for second in part_ids[index + 1:]:
            key = tuple(sorted((first, second)))
            if key in contact:
                classification = "contact"
            elif key in coupling:
                classification = "coupling"
            else:
                classification = "forbidden"
            output.append(
                {
                    "parts": list(key),
                    "classification": classification,
                    "clearance_m": float(shapes[first].distance(shapes[second])) / MM,
                    "overlap_m3": shapes[first].intersect(shapes[second]).Volume() * 1.0e-9,
                }
            )
    return output


def _interface_measurements(raw: dict[str, Any], shapes: dict[str, cq.Shape]) -> dict[str, Any]:
    output_bounds = shapes["output_shaft"].BoundingBox()
    drum_bounds = shapes["ratio_drum"].BoundingBox()
    return {
        "output_shaft_interface": {
            "y_m": output_bounds.ymin / MM,
            "radius_m": 0.5 * (output_bounds.xmax - output_bounds.xmin) / MM,
            "axis_x_m": 0.5 * (output_bounds.xmax + output_bounds.xmin) / MM,
            "axis_z_m": 0.5 * (output_bounds.zmax + output_bounds.zmin) / MM,
        },
        "drum_ground_clearance_m": drum_bounds.zmin / MM - raw["work083_interface"]["contact_plane_z_m"],
    }


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _run_freecad(freecad_python: Path, output_root: Path, manifest_path: Path) -> dict[str, Any]:
    report_path = output_root / "freecad_report.json"
    fcstd_path = output_root / "energy_torque_path_candidate_001.FCStd"
    env = os.environ.copy()
    env.update(
        {
            "FORMULA_ULTIMATE_W084_MANIFEST": str(manifest_path.resolve()),
            "FORMULA_ULTIMATE_W084_STEP_ROOT": str(output_root.resolve()),
            "FORMULA_ULTIMATE_W084_FREECAD_REPORT": str(report_path.resolve()),
            "FORMULA_ULTIMATE_W084_FCSTD": str(fcstd_path.resolve()),
        }
    )
    process = subprocess.run(
        [str(freecad_python), str(ROOT / "scripts/candidates/inspect_energy_torque_path_freecad.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode != 0:
        raise EnergyTorquePathViolation(
            f"FreeCAD inspection failed with exit {process.returncode}: {process.stderr or process.stdout}"
        )
    if not report_path.is_file() or not fcstd_path.is_file():
        raise EnergyTorquePathViolation(
            "FreeCAD did not create its report and FCStd witness: " + (process.stderr or process.stdout)
        )
    return json.loads(report_path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--work083-result", type=Path, required=True)
    parser.add_argument("--freecad-python", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()

    raw = json.loads(args.config.read_text(encoding="utf-8"))
    declaration = validate_declaration(raw)
    if args.work083_result.resolve() != (ROOT / raw["work083_interface"]["result_path"]).resolve():
        raise EnergyTorquePathViolation("Work 083 result path differs from the frozen declaration")
    work083 = json.loads(args.work083_result.read_text(encoding="utf-8"))

    args.output_root.mkdir(parents=True, exist_ok=True)
    shapes, parts, derived = _build_shapes(raw, args.output_root)
    derived.update(_interface_measurements(raw, shapes))
    pair_clearance = _pair_clearance(raw, shapes)

    compound = cq.Compound.makeCompound([shapes[item["part_id"]] for item in raw["parts"]])
    assembly_path = args.output_root / "energy_torque_path_candidate_001.step"
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
        "derived": derived,
        "pair_clearance": pair_clearance,
    }
    manifest = {**manifest_body, "manifest_sha256": canonical_sha256(manifest_body)}
    manifest_path = args.output_root / "geometry_manifest.json"
    _write_json(manifest_path, manifest)

    freecad = _run_freecad(args.freecad_python, args.output_root, manifest_path)
    evaluation = evaluate_candidate(raw, manifest, freecad, work083)
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
        "work083_result_sha256": work083["result_sha256"],
    }
    result = {**result_body, "result_sha256": canonical_sha256(result_body)}
    _write_json(args.output_root / "result.json", result)

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
            "work083_result_sha256",
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
            raise EnergyTorquePathViolation("exact replay identity comparison failed")

    print(
        json.dumps(
            {
                "status": "passed",
                "candidate_verdict": result["candidate_verdict"],
                "part_count": len(parts),
                "assembly_solid_count": manifest["assembly"]["solid_count"],
                "mobility_dof": evaluation["declaration"]["mobility_dof"],
                "torque_ratio": evaluation["declaration"]["torque_ratio"],
                "total_mass_kg": evaluation["geometry"]["total_mass_kg"],
                "minimum_clearance_m": evaluation["geometry"]["minimum_forbidden_clearance_m"],
                "maximum_overlap_m3": evaluation["geometry"]["maximum_overlap_m3"],
                "drum_ground_clearance_m": evaluation["geometry"]["drum_ground_clearance_m"],
                "torque_residual_relative": evaluation["physics"]["torque_residual_relative"],
                "reaction_residual_relative": evaluation["physics"]["reaction_residual_relative"],
                "energy_residual_relative": evaluation["physics"]["energy_residual_relative"],
                "thermal_residual_relative": evaluation["physics"]["thermal_residual_relative"],
                "maximum_structural_utilization": evaluation["structural_analytic"]["maximum_utilization"],
                "result_sha256": result["result_sha256"],
                "replay_exact": None if replay is None else replay["exact"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
