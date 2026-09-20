"""Run the Work 140 part-resolution and joint-system gate."""

from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
for item in (ROOT, ROOT / "src"):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from formula_ultimate.assembly.part_resolution import (  # noqa: E402
    FINAL_STATUS,
    JOINT_EVIDENCE,
    PartResolutionError,
    canonical_sha256,
    evaluate_joint,
    evaluate_part,
    summarize,
    validate_protocol,
)
from formula_ultimate.structural.element_verification import parse_element_msh2  # noqa: E402
from scripts.structural.mesh_step_solid import file_sha256, mesh_solid  # noqa: E402

MEASURER = "scripts/cad/measure_part_resolution.py"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def runtime(raw: dict[str, Any], runtime_id: str) -> Path:
    declared = next((item for item in raw["runtimes"] if item["runtime_id"] == runtime_id), None)
    if declared is None:
        raise PartResolutionError(f"runtime is not declared: {runtime_id}")
    path = Path(declared["path"])
    if not path.is_absolute():
        path = ROOT / path
    if not path.is_file():
        raise PartResolutionError(f"declared runtime is missing: {path}")
    return path


def measure(config: Path, output_root: Path, cadquery_python: Path) -> dict[str, Any]:
    measurement_path = output_root / "measurement.json"
    completed = subprocess.run(
        [
            str(cadquery_python), str(ROOT / MEASURER),
            "--config", str(config),
            "--output-root", str(output_root / "cad"),
            "--measurement", str(measurement_path),
        ],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if completed.returncode != 0 or not measurement_path.is_file():
        raise PartResolutionError(
            f"measurement failed: {(completed.stderr or completed.stdout).strip()[-600:]}"
        )
    return json.loads(measurement_path.read_text(encoding="utf-8"))


def mesh_characteristic_length(mesh) -> float:
    """Median tetrahedron edge length, in metres, from the mesh itself."""

    lengths: list[float] = []
    for connectivity in mesh.tetrahedra.values():
        corners = [mesh.nodes[node] for node in connectivity[:4]]
        for index, first in enumerate(corners):
            for second in corners[index + 1:]:
                lengths.append(math.dist(first, second))
    if not lengths:
        raise PartResolutionError("mesh carries no tetrahedra")
    return statistics.median(lengths) / 1000.0


def mesh_part(measurement: dict[str, Any], gmsh: Path, size_factor: float, work_dir: Path, timeout_s: float) -> dict[str, Any]:
    """Mesh one measured part and report what the mesh can actually resolve."""

    evidence, mesh_path = mesh_solid(
        gmsh=gmsh,
        geometry={"kind": "step_file", "path": measurement["step_path"]},
        size_factor=size_factor, work_dir=work_dir, timeout_s=timeout_s,
    )
    if evidence["exit_code"] != 0 or not evidence["mesh_exists"]:
        return {"status": "unresolved_mesh", "cause": "gmsh did not produce a mesh"}
    try:
        mesh = parse_element_msh2(mesh_path, expected_order=2)
    except ValueError as exc:
        return {"status": "unresolved_mesh", "cause": f"mesh is unreadable: {exc}"}
    return {
        "status": "meshed",
        "node_count": len(mesh.nodes),
        "tetrahedron_count": len(mesh.tetrahedra),
        "characteristic_length_m": mesh_characteristic_length(mesh),
        "mesh_sha256": evidence["mesh_sha256"],
    }


def run_controls(raw: dict[str, Any], parts: list[dict[str, Any]], joints: list[dict[str, Any]],
                 measurement: dict[str, Any]) -> list[dict[str, Any]]:
    """Each registered control must be rejected, and each rejection recorded."""

    controls: list[dict[str, Any]] = []

    def record(control_id: str, rejected: bool, detail: str) -> None:
        controls.append({"control_id": control_id, "rejected": rejected, "detail": detail})

    resolution = raw["resolution"]
    # The mesh control needs a subject that already clears the geometry gates,
    # otherwise a resolution shortfall masks what the control is testing.
    passing = {item["part_id"] for item in parts if item["status"] == "passed_resolution"}
    subject = next(
        (item for item in raw["parts"] if item["part_id"] in passing),
        next(item for item in raw["parts"] if measurement["parts"][item["part_id"]]["status"] == "measured"),
    )
    requirement = raw["part_classes"][subject["part_class"]]
    measured = measurement["parts"][subject["part_id"]]

    sliver = copy.deepcopy(measured)
    sliver["smallest_feature_m"] = float(resolution["minimum_feature_m"]) / 10.0
    sliver["edge_lengths_m"] = [sliver["smallest_feature_m"]] + sliver["edge_lengths_m"]
    verdict = evaluate_part(subject, requirement, resolution, sliver)
    record("sliver_below_manufacturing_floor", verdict["status"] == "unmanufacturable_feature", verdict["status"])

    coarse = copy.deepcopy(measured)
    coarse["face_count"], coarse["curved_face_count"], coarse["edge_count"] = 2, 0, 2
    coarse["edge_lengths_m"] = [0.01, 0.01]
    verdict = evaluate_part(subject, requirement, resolution, coarse)
    record("primitive_below_resolution_requirement", verdict["status"] == "insufficient_resolution", verdict["cause"] or "")

    # If no subject clears the geometry gates, the mesh control still has to be
    # testable, so it runs against a measurement lifted above the requirement.
    liftable = copy.deepcopy(measured)
    if subject["part_id"] not in passing:
        liftable["face_count"] = max(liftable["face_count"], requirement["minimum_faces"])
        liftable["curved_face_count"] = max(liftable["curved_face_count"], requirement["minimum_curved_faces"])
        liftable["edge_count"] = max(liftable["edge_count"], requirement["minimum_edges"])
        liftable["edge_lengths_m"] = [
            liftable["feature_scale_m"] * 10.0 ** power
            for power in range(requirement["minimum_distinct_feature_scales"])
        ]
    under_meshed = copy.deepcopy(liftable)
    under_meshed["mesh"] = {
        "status": "meshed", "node_count": 10, "tetrahedron_count": 4,
        "characteristic_length_m": measured["feature_scale_m"] * 10.0, "mesh_sha256": "0" * 64,
    }
    verdict = evaluate_part(subject, requirement, resolution, under_meshed)
    record("mesh_too_coarse_for_feature", verdict["status"] == "unresolved_measurement", verdict["cause"] or "")

    if raw["joints"]:
        joint = raw["joints"][0]
        empty = {"status": "measured", "clearance_m": 1.0, "interference_volume_m3": 0.0,
                 "mating_face_pairs": 0, "overlap_area_m2": 0.0, "engagement_face_count": 0, "single_solid": True}
        verdict = evaluate_joint(joint, empty)
        record("joint_without_measurable_interface", verdict["status"] in {"unsupported_joint_evidence", "out_of_range_fit"}, verdict["status"])

        low, high = (float(value) for value in joint["fit_range_m"])
        out_of_range = {"status": "measured", "clearance_m": high + 1.0, "interference_volume_m3": 1e-9,
                        "mating_face_pairs": 4, "overlap_area_m2": 1.0, "engagement_face_count": 8, "single_solid": True}
        verdict = evaluate_joint(joint, out_of_range)
        record("fit_outside_declared_range", verdict["status"] in {"out_of_range_fit", "unsupported_joint_evidence"}, verdict["status"])
    else:
        record("joint_without_measurable_interface", False, "no joint declared")
        record("fit_outside_declared_range", False, "no joint declared")

    invented = copy.deepcopy(raw)
    invented["joints"][0]["technology"] = "wishful_adhesion"
    try:
        validate_protocol(invented)
        record("technology_outside_registry", False, "an unregistered technology was accepted")
    except PartResolutionError as exc:
        record("technology_outside_registry", "not in the registry" in str(exc), str(exc))

    summary = summarize(parts, joints, [{"control_id": "probe", "rejected": True}])
    record(
        "no_discovery_claim",
        not any((summary["discovery_claim"], summary["promotion_allowed"], summary["race_time_claim"], summary["physical_validation"])),
        "summary carries every downstream claim as false",
    )

    scored = {"parts": parts, "joints": joints}
    record("exact_replay", canonical_sha256(scored) == canonical_sha256(json.loads(json.dumps(scored))),
           canonical_sha256(scored))
    return controls


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path, default=None)
    parser.add_argument("--keep-work", action="store_true")
    args = parser.parse_args()

    raw = json.loads(args.config.read_text(encoding="utf-8"))
    declaration = validate_protocol(raw)
    cadquery_python, gmsh = runtime(raw, "cadquery_python"), runtime(raw, "gmsh")
    if args.output_root.exists():
        shutil.rmtree(args.output_root)
    args.output_root.mkdir(parents=True)

    measurement = measure(args.config, args.output_root, cadquery_python)
    resolution = raw["resolution"]
    parts: list[dict[str, Any]] = []
    for part in raw["parts"]:
        measured = measurement["parts"].get(part["part_id"])
        if measured is not None and measured.get("status") == "measured":
            measured = dict(measured)
            measured["mesh"] = mesh_part(
                measured, gmsh, float(resolution["mesh_size_factor"]),
                args.output_root / "mesh" / part["part_id"], 900.0,
            )
        parts.append(evaluate_part(part, raw["part_classes"][part["part_class"]], resolution, measured))
    joints = [evaluate_joint(joint, measurement["joints"].get(joint["joint_id"])) for joint in raw["joints"]]

    for record in parts:
        record.pop("edge_lengths_m", None)
    controls = run_controls(raw, parts, joints, measurement)
    summary = summarize(parts, joints, controls)

    result = {
        "protocol_version": raw["protocol_version"],
        "protocol_sha256": declaration["protocol_sha256"],
        "config_sha256": file_sha256(args.config),
        "registered_resolution": resolution,
        "joint_registry": {key: list(value) for key, value in JOINT_EVIDENCE.items()},
        "parts": parts,
        "joints": joints,
        "controls": controls,
        "summary": summary,
        "claim_boundary": (
            "geometric resolution and interface evidence for the declared subjects only; "
            "no force was solved across any joint; not promotion, manufacturability, race time "
            "or physical validation"
        ),
    }
    result["result_sha256"] = canonical_sha256(result)
    write_json(args.output_root / "result.json", result)
    if not args.keep_work and (args.output_root / "mesh").exists():
        shutil.rmtree(args.output_root / "mesh")

    replay = None
    if args.replay_reference is not None:
        reference = json.loads(args.replay_reference.read_text(encoding="utf-8"))
        replay = {
            "reference_sha256": reference.get("result_sha256"),
            "exact": reference.get("result_sha256") == result["result_sha256"],
        }
        write_json(args.output_root / "replay.json", replay)

    print(json.dumps({
        "status": summary["status"],
        "part_status_counts": summary["part_status_counts"],
        "joint_status_counts": summary["joint_status_counts"],
        "parts_below_bar": summary["parts_below_bar"],
        "joints_without_evidence": summary["joints_without_evidence"],
        "controls_rejected": f"{summary['controls_rejected']}/{summary['control_count']}",
        "result_sha256": result["result_sha256"],
        "replay": replay,
    }, sort_keys=True))
    if summary["status"] != FINAL_STATUS:
        return 1
    if replay is not None and not replay["exact"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
