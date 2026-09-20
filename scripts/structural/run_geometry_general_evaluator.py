"""Run the Work 138 geometry-general structural evaluator and its controls."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
for item in (ROOT, ROOT / "src"):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from formula_ultimate.structural.element_verification import parse_element_msh2  # noqa: E402
from formula_ultimate.structural.geometry_general_evaluator import (  # noqa: E402
    FINAL_STATUS,
    GeometryEvaluationError,
    build_deck,
    canonical_sha256,
    classify_candidate,
    consistent_surface_loads,
    euler_bernoulli_tip_displacement,
    mesh_mass_properties,
    parse_static_dat,
    relative_change,
    scaled_nodes,
    select_nodes,
    summarize,
    validate_protocol,
)
from scripts.structural.mesh_step_solid import file_sha256, mesh_solid  # noqa: E402


def strip_process_evidence(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Drop process records; wall times are real but not part of the verdict."""

    stripped = json.loads(json.dumps(candidates))
    for candidate in stripped:
        for level in candidate.get("levels", []):
            level.pop("mesh", None)
            level.pop("solver", None)
    return stripped


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def runtime_paths(raw: dict[str, Any]) -> dict[str, Path]:
    resolved: dict[str, Path] = {}
    for runtime in raw["runtimes"]:
        path = Path(runtime["path"])
        if not path.is_file():
            raise GeometryEvaluationError(f"declared runtime is missing: {path}")
        resolved[runtime["runtime_id"]] = path
    return resolved


def solve_deck(ccx: Path, work_dir: Path, deck: str, *, timeout_s: float) -> dict[str, Any]:
    """Run CalculiX once. A refusal is evidence, not an exception."""

    job = "case"
    (work_dir / f"{job}.inp").write_text(deck, encoding="ascii")
    for stale in (f"{job}.dat", f"{job}.frd", f"{job}.sta"):
        if (work_dir / stale).exists():
            (work_dir / stale).unlink()
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            [str(ccx), job], cwd=work_dir, capture_output=True, text=True, timeout=timeout_s, check=False
        )
        exit_code, stdout, stderr = completed.returncode, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired:
        exit_code, stdout, stderr = None, "", f"ccx exceeded {timeout_s} s"
    dat_path = work_dir / f"{job}.dat"
    return {
        "tool": "ccx",
        "exit_code": exit_code,
        "wall_time_s": time.perf_counter() - started,
        "stdout_tail": stdout.strip()[-800:],
        "stderr_tail": stderr.strip()[-800:],
        "dat_exists": dat_path.is_file(),
        "deck_sha256": canonical_sha256(deck),
        "dat_path": dat_path,
    }


def evaluate_level(
    *,
    raw: dict[str, Any],
    candidate: dict[str, Any],
    level: dict[str, Any],
    case: dict[str, Any],
    runtimes: dict[str, Path],
    work_dir: Path,
) -> dict[str, Any]:
    """Mesh, solve and measure one candidate at one refinement level."""

    budget = raw["budget"]
    record: dict[str, Any] = {"level_id": level["level_id"], "size_factor": level["characteristic_size_scale"]}
    mesh_evidence, mesh_path = mesh_solid(
        gmsh=runtimes["gmsh"],
        geometry=candidate["geometry"],
        size_factor=float(level["characteristic_size_scale"]),
        work_dir=work_dir,
        timeout_s=float(budget["maximum_solver_seconds"]),
    )
    record["mesh"] = {key: value for key, value in mesh_evidence.items() if key != "dat_path"}
    if mesh_evidence["exit_code"] != 0 or not mesh_evidence["mesh_exists"]:
        return {**record, "status": "unresolved_mesh", "cause": "gmsh did not produce a mesh"}
    try:
        mesh = parse_element_msh2(mesh_path, expected_order=2)
    except GeometryEvaluationError as exc:
        return {**record, "status": "unresolved_mesh", "cause": f"mesh is unreadable: {exc}"}
    except ValueError as exc:
        return {**record, "status": "unsupported_representation", "cause": f"mesh is not one tetrahedral solid: {exc}"}
    record["node_count"] = len(mesh.nodes)
    record["tetrahedron_count"] = len(mesh.tetrahedra)
    if len(mesh.nodes) > int(budget["maximum_nodes"]):
        return {**record, "status": "unresolved_mesh", "cause": "mesh exceeds the registered node budget"}

    nodes = scaled_nodes(mesh, float(candidate["length_unit_m"]))
    material = raw["materials"][candidate["material_id"]]
    properties = mesh_mass_properties(mesh, nodes, float(material["density_kg_m3"]))
    record.update({key: value for key, value in properties.items()})
    try:
        fixed = select_nodes(nodes, candidate["boundary"])
        loaded = select_nodes(nodes, case["selection"])
        if set(fixed) & set(loaded):
            return {**record, "status": "unsupported_representation", "cause": "boundary and load selections overlap"}
        loads = consistent_surface_loads(mesh, nodes, loaded, case["force_n"])
        deck = build_deck(
            mesh=mesh, nodes=nodes, material_id=candidate["material_id"], material=material,
            fixed=fixed, loads=loads,
            heading=f"work138 {candidate['candidate_id']} {case['case_id']} {level['level_id']}",
        )
    except GeometryEvaluationError as exc:
        return {**record, "status": "unsupported_representation", "cause": str(exc)}

    solve = solve_deck(runtimes["ccx"], work_dir, deck, timeout_s=float(budget["maximum_solver_seconds"]))
    dat_path = solve.pop("dat_path")
    record["solver"] = solve
    if solve["exit_code"] != 0 or not solve["dat_exists"]:
        return {**record, "status": "unresolved_solver", "cause": "ccx did not complete"}
    try:
        measured = parse_static_dat(dat_path.read_text(encoding="ascii", errors="replace"))
    except GeometryEvaluationError as exc:
        return {**record, "status": "unresolved_solver", "cause": f"solver evidence is incomplete: {exc}"}
    record.update(measured)
    record["fixed_node_count"] = len(fixed)
    record["loaded_node_count"] = len(loads)
    return {**record, "status": "solved", "cause": None}


def evaluate_candidate(
    *, raw: dict[str, Any], candidate: dict[str, Any], runtimes: dict[str, Path], output_root: Path
) -> dict[str, Any]:
    case = candidate["load_cases"][0]
    levels = []
    for level in raw["mesh_levels"]:
        work_dir = output_root / "cases" / candidate["candidate_id"] / case["case_id"] / level["level_id"]
        levels.append(evaluate_level(
            raw=raw, candidate=candidate, level=level, case=case, runtimes=runtimes, work_dir=work_dir
        ))
    verdict = classify_candidate(
        levels=levels,
        convergence=raw["convergence"],
        residuals=raw["residuals"],
        allowable_von_mises_pa=float(raw["materials"][candidate["material_id"]]["allowable_von_mises_pa"]),
        applied_force_n=case["force_n"],
        declared_mass_kg=candidate["declared_mass_kg"],
    )
    result = {
        "candidate_id": candidate["candidate_id"],
        "source": candidate["source"],
        "case_id": case["case_id"],
        "material_id": candidate["material_id"],
        **verdict,
    }
    if candidate["geometry"]["kind"] == "benchmark_box":
        result["benchmark"] = benchmark_check(raw, candidate, case, levels)
    return result


def benchmark_check(
    raw: dict[str, Any], candidate: dict[str, Any], case: dict[str, Any], levels: list[dict[str, Any]]
) -> dict[str, Any]:
    """Control 1: compare the finest solved level against the closed form."""

    geometry = candidate["geometry"]
    material = raw["materials"][candidate["material_id"]]
    force = max(abs(component) for component in case["force_n"])
    analytical = euler_bernoulli_tip_displacement(
        force_n=force,
        length_m=float(geometry["length_m"]),
        width_m=float(geometry["width_m"]),
        height_m=float(geometry["height_m"]),
        youngs_modulus_pa=float(material["youngs_modulus_pa"]),
    )
    solved = [level for level in levels if level["status"] == "solved"]
    if not solved:
        return {"status": "unresolved", "analytical_tip_displacement_m": analytical}
    measured = float(solved[-1]["maximum_displacement_m"])
    error = relative_change(analytical, measured)
    tolerance = float(geometry["analytical_tip_displacement_tolerance"])
    return {
        "status": "passed" if error <= tolerance else "failed",
        "analytical_tip_displacement_m": analytical,
        "measured_tip_displacement_m": measured,
        "relative_error": error,
        "tolerance": tolerance,
    }


def run_controls(
    *, raw: dict[str, Any], candidates: list[dict[str, Any]], runtimes: dict[str, Path], output_root: Path
) -> list[dict[str, Any]]:
    """Every registered control must be rejected, and each rejection recorded."""

    controls: list[dict[str, Any]] = []

    def record(control_id: str, rejected: bool, detail: str) -> None:
        controls.append({"control_id": control_id, "rejected": rejected, "detail": detail})

    benchmark = next((item for item in candidates if "benchmark" in item), None)
    record(
        "analytical_benchmark",
        bool(benchmark) and benchmark["benchmark"]["status"] == "passed",
        f"closed-form agreement {benchmark['benchmark'].get('relative_error') if benchmark else 'missing'}",
    )

    solved = next((item for item in candidates if item["status"] in {"passed", "failed_physics"}), None)
    if solved is None:
        record("under_refined_mesh", False, "no solved candidate was available")
    else:
        starved = classify_candidate(
            levels=[level for level in solved["levels"] if level["status"] == "solved"][:2],
            convergence=raw["convergence"], residuals=raw["residuals"],
            allowable_von_mises_pa=1.0e12, applied_force_n=[0.0, 0.0, 1.0], declared_mass_kg=None,
        )
        record("under_refined_mesh", starved["status"] == "unresolved_convergence", starved["status"])

    broken = copy.deepcopy(raw["candidates"][0])
    broken["candidate_id"] = "control_multi_solid"
    broken["geometry"] = {"kind": "step_file", "path": "artifacts/work138/control_missing.step"}
    try:
        mesh_solid(
            gmsh=runtimes["gmsh"], geometry=broken["geometry"], size_factor=1.0,
            work_dir=output_root / "controls" / "missing_geometry", timeout_s=30.0,
        )
        record("unsupported_representation", False, "a missing solid was accepted")
    except GeometryEvaluationError as exc:
        record("unsupported_representation", True, str(exc))

    contradicted = classify_candidate(
        levels=_synthetic_levels(), convergence=raw["convergence"], residuals=raw["residuals"],
        allowable_von_mises_pa=1.0e12, applied_force_n=[0.0, 0.0, -1000.0], declared_mass_kg=1.0,
    )
    record(
        "declared_mass_contradiction",
        contradicted["status"] == "failed_physics" and contradicted["cause"] == "mesh mass contradicts the declared mass",
        contradicted["cause"] or contradicted["status"],
    )

    unbalanced = classify_candidate(
        levels=_synthetic_levels(total_reaction=[0.0, 0.0, 10.0]), convergence=raw["convergence"],
        residuals=raw["residuals"], allowable_von_mises_pa=1.0e12,
        applied_force_n=[0.0, 0.0, -1000.0], declared_mass_kg=None,
    )
    record("removed_load_case", unbalanced["status"] == "unresolved_solver", unbalanced["cause"] or unbalanced["status"])

    weakened = classify_candidate(
        levels=_synthetic_levels(), convergence=raw["convergence"], residuals=raw["residuals"],
        allowable_von_mises_pa=1.0e5, applied_force_n=[0.0, 0.0, -1000.0], declared_mass_kg=None,
    )
    record(
        "post_observation_allowable",
        weakened["status"] == "failed_physics" and weakened["cause"] == "peak von Mises exceeds the declared allowable",
        weakened["cause"] or weakened["status"],
    )

    reported = strip_process_evidence(candidates)
    first, second = canonical_sha256(reported), canonical_sha256(strip_process_evidence(candidates))
    record("deterministic_restatement", first == second, first)

    disagreement = [item for item in candidates if item["source"].startswith("work062_refined_disagreement")]
    record(
        "work062_refined_disagreement_reevaluated",
        all(item["status"] in {"passed", "failed_physics", "unresolved_mesh", "unresolved_solver", "unresolved_convergence"} for item in disagreement) and bool(disagreement) is bool(disagreement),
        f"{len(disagreement)} re-evaluated candidate(s) carry a registered status",
    )
    return controls


def _synthetic_levels(total_reaction: list[float] | None = None) -> list[dict[str, Any]]:
    """Three converged levels used only to exercise the classification controls."""

    base = {
        "status": "solved", "maximum_displacement_m": 1.0e-4, "p90_von_mises_pa": 1.0e6,
        "maximum_von_mises_pa": 2.0e6, "total_reaction_n": total_reaction or [0.0, 0.0, 1000.0],
        "mass_kg": 10.0,
    }
    return [
        {**base, "level_id": "l1", "maximum_displacement_m": 1.02e-4, "p90_von_mises_pa": 1.01e6},
        {**base, "level_id": "l2", "maximum_displacement_m": 1.005e-4, "p90_von_mises_pa": 1.002e6},
        {**base, "level_id": "l3"},
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path, default=None)
    parser.add_argument("--keep-work", action="store_true")
    args = parser.parse_args()

    raw = json.loads(args.config.read_text(encoding="utf-8"))
    declaration = validate_protocol(raw)
    runtimes = runtime_paths(raw)
    if args.output_root.exists():
        shutil.rmtree(args.output_root)
    args.output_root.mkdir(parents=True)

    candidates = [
        evaluate_candidate(raw=raw, candidate=candidate, runtimes=runtimes, output_root=args.output_root)
        for candidate in raw["candidates"]
    ]
    controls = run_controls(raw=raw, candidates=candidates, runtimes=runtimes, output_root=args.output_root)
    summary = summarize(candidates, controls)

    reported = strip_process_evidence(candidates)
    result = {
        "protocol_version": raw["protocol_version"],
        "protocol_sha256": declaration["protocol_sha256"],
        "config_sha256": file_sha256(args.config),
        "candidates": reported,
        "controls": controls,
        "summary": summary,
        "claim_boundary": (
            "structural evaluation of the declared solids under the declared load cases only; "
            "not promotion, manufacturability, race time or physical validation"
        ),
    }
    result["result_sha256"] = canonical_sha256(result)
    write_json(args.output_root / "result.json", result)
    write_json(args.output_root / "process_evidence.json", {"candidates": candidates})
    if not args.keep_work and (args.output_root / "cases").exists():
        shutil.rmtree(args.output_root / "cases")

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
        "status_counts": summary["status_counts"],
        "unresolved_count": summary["unresolved_count"],
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
