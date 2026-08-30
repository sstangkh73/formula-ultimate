"""Run Work 042 bilinear plasticity acceptance through CalculiX."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.structural import (  # noqa: E402
    BilinearPlasticitySpec,
    StructuralEvidenceError,
    build_plasticity_deck,
    parse_plasticity_dat,
    structured_hex_mesh,
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relative(actual: float, expected: float) -> float:
    return abs(actual - expected) / max(abs(expected), 1e-300)


def run_process(command: list[str], cwd: Path) -> dict[str, Any]:
    started = time.time_ns()
    monotonic = time.perf_counter()
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    return {"command": command, "exit_code": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr, "started_time_ns": started, "wall_time_s": time.perf_counter() - monotonic}


def weighted(values: dict[int, tuple[float, float, float]], weights: dict[int, float], axis: int) -> float:
    missing = set(weights) - set(values)
    if missing:
        raise StructuralEvidenceError(f"solver omitted weighted nodes: {sorted(missing)}")
    total = math.fsum(weights.values())
    return math.fsum(weights[node] * values[node][axis] for node in weights) / total


def mean_component(rows: list[tuple[int, int, tuple[float, ...]]], component: int) -> float:
    return math.fsum(row[2][component] for row in rows) / len(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--ccx", type=Path, required=True)
    args = parser.parse_args()
    stage = "configuration"
    processes: list[dict[str, Any]] = []
    try:
        payload = json.loads(args.config.read_text(encoding="utf-8"))
        spec = BilinearPlasticitySpec.from_mapping(payload)
        factors = tuple(float(value) for value in payload["load_factors_of_initial_yield"])
        if factors != (0.8, 1.0, 1.08, 0.0, -0.8, 0.0):
            raise StructuralEvidenceError("Work 042 load history must remain exactly preregistered")
        meshes = payload["mesh_levels"]
        if len(meshes) != 2:
            raise StructuralEvidenceError("Work 042 requires exactly two mesh levels")
        tolerances = payload["tolerances"]
        if not args.ccx.is_file():
            raise StructuralEvidenceError(f"CalculiX is missing: {args.ccx}")
        if args.artifact_root.exists():
            shutil.rmtree(args.artifact_root)
        args.artifact_root.mkdir(parents=True)
        mesh_results: list[dict[str, Any]] = []
        for declaration in meshes:
            mesh_id = str(declaration["mesh_id"])
            mesh = structured_hex_mesh(spec, nx=int(declaration["nx"]), ny=int(declaration["ny"]), nz=int(declaration["nz"]))
            run_dir = args.artifact_root / mesh_id
            run_dir.mkdir()
            deck_path = run_dir / "plasticity.inp"
            deck_path.write_text(build_plasticity_deck(spec, mesh, load_factors=factors, maximum_plastic_strain=float(payload["material"]["maximum_plastic_strain"])), encoding="ascii")
            stage = f"calculix:{mesh_id}"
            process = run_process([str(args.ccx), "plasticity"], run_dir)
            process["stage"] = stage
            processes.append(process)
            (run_dir / "solver_stdout.txt").write_text(process["stdout"], encoding="utf-8")
            (run_dir / "solver_stderr.txt").write_text(process["stderr"], encoding="utf-8")
            if process["exit_code"] != 0:
                raise StructuralEvidenceError(f"CalculiX failed for {mesh_id}: {process['stderr'][-2000:]}")
            dat_path, frd_path = run_dir / "plasticity.dat", run_dir / "plasticity.frd"
            for evidence in (dat_path, frd_path):
                if not evidence.is_file() or evidence.stat().st_mtime_ns < process["started_time_ns"]:
                    raise StructuralEvidenceError(f"missing fresh {evidence.name} for {mesh_id}")
            parsed = parse_plasticity_dat(dat_path)
            if len(parsed) != len(factors):
                raise StructuralEvidenceError("solver step count differs from the frozen load history")
            steps: list[dict[str, Any]] = []
            previous_force = 0.0
            previous_displacement = 0.0
            external_work = 0.0
            for index, (factor, evidence) in enumerate(zip(factors, parsed), start=1):
                force = factor * spec.yield_force_n
                displacement = weighted(evidence["displacements"], mesh.tributary_area_m2, 0)
                reaction = math.fsum(vector[0] for vector in evidence["reactions"].values())
                stress = mean_component(evidence["stresses"], 0)
                strain = mean_component(evidence["strains"], 0)
                peeq = math.fsum(row[2] for row in evidence["peeq"]) / len(evidence["peeq"])
                internal_energy = math.fsum(evidence["element_internal_energy_j"].values())
                external_work += 0.5 * (previous_force + force) * (displacement - previous_displacement)
                step = {
                    "step": index, "load_factor": factor, "force_n": force,
                    "displacement_m": displacement, "nominal_strain": displacement / spec.length_m,
                    "mean_sxx_pa": stress, "mean_exx": strain, "mean_peeq": peeq,
                    "reaction_x_n": reaction,
                    "reaction_residual_relative": abs(force + reaction) / max(abs(force), spec.yield_force_n),
                    "solver_internal_energy_j": internal_energy,
                    "accumulated_external_work_j": external_work,
                    "energy_ledger_relative": abs(external_work - internal_energy) / max(abs(external_work), abs(internal_energy), 1e-12),
                }
                if step["reaction_residual_relative"] > float(tolerances["reaction_residual_relative"]):
                    raise StructuralEvidenceError(f"{mesh_id} step {index} reaction gate failed: {step}")
                if step["energy_ledger_relative"] > float(tolerances["energy_ledger_relative"]):
                    raise StructuralEvidenceError(f"{mesh_id} step {index} energy gate failed: {step}")
                steps.append(step)
                previous_force, previous_displacement = force, displacement
            elastic, at_yield, peak, unloaded, reversed_step, final = steps
            elastic_slope = elastic["mean_sxx_pa"] / elastic["nominal_strain"]
            plastic_slope = (peak["mean_sxx_pa"] - at_yield["mean_sxx_pa"]) / (peak["nominal_strain"] - at_yield["nominal_strain"])
            plastic_intercept = at_yield["mean_sxx_pa"] - plastic_slope * at_yield["nominal_strain"]
            onset_strain = plastic_intercept / (elastic_slope - plastic_slope)
            onset_stress = elastic_slope * onset_strain
            analytical_peak_stress = factors[2] * spec.yield_stress_pa
            analytical_peak_strain = spec.monotonic_strain(analytical_peak_stress)
            analytical_residual = spec.monotonic_plastic_strain(analytical_peak_stress)
            metrics = {
                "yield_onset_stress_pa": onset_stress,
                "yield_onset_relative": relative(onset_stress, spec.yield_stress_pa),
                "post_yield_tangent_pa": plastic_slope,
                "post_yield_tangent_relative": relative(plastic_slope, spec.tangent_modulus_pa),
                "peak_plastic_strain_relative": relative(peak["mean_peeq"], analytical_residual),
                "peak_total_strain_relative": relative(peak["nominal_strain"], analytical_peak_strain),
                "residual_strain": final["nominal_strain"],
                "residual_strain_relative": relative(final["nominal_strain"], analytical_residual),
                "below_yield_peeq": elastic["mean_peeq"],
                "reverse_elastic_slope_relative": relative((reversed_step["mean_sxx_pa"] - unloaded["mean_sxx_pa"]) / (reversed_step["nominal_strain"] - unloaded["nominal_strain"]), spec.youngs_modulus_pa),
                "maximum_reaction_residual_relative": max(step["reaction_residual_relative"] for step in steps),
                "maximum_energy_ledger_relative": max(step["energy_ledger_relative"] for step in steps),
            }
            limits = {
                "yield_onset_relative": tolerances["yield_onset_relative"],
                "post_yield_tangent_relative": tolerances["post_yield_tangent_relative"],
                "peak_plastic_strain_relative": tolerances["peak_plastic_strain_relative"],
                "residual_strain_relative": tolerances["residual_strain_relative"],
            }
            failures = [name for name, limit in limits.items() if metrics[name] > float(limit)]
            if metrics["below_yield_peeq"] > float(tolerances["below_yield_peeq_absolute"]):
                failures.append("below_yield_peeq")
            if failures:
                raise StructuralEvidenceError(f"{mesh_id} plasticity gates failed: {failures}; metrics={metrics}")
            mesh_results.append({
                "mesh_id": mesh_id, "nodes": len(mesh.nodes), "c3d8_elements": len(mesh.elements),
                "steps": steps, "metrics": metrics,
                "evidence_sha256": {path.name: sha(path) for path in (deck_path, dat_path, frd_path)},
                "solver_wall_time_s": process["wall_time_s"],
            })
        stage = "mesh_convergence"
        coarse, fine = mesh_results
        convergence = {
            "peak_strain_relative": relative(fine["steps"][2]["nominal_strain"], coarse["steps"][2]["nominal_strain"]),
            "peak_peeq_relative": relative(fine["steps"][2]["mean_peeq"], coarse["steps"][2]["mean_peeq"]),
            "residual_strain_relative": relative(fine["metrics"]["residual_strain"], coarse["metrics"]["residual_strain"]),
        }
        if any(value > float(tolerances["last_two_nominal_response_relative"]) for value in convergence.values()):
            raise StructuralEvidenceError(f"mesh convergence failed: {convergence}")
        summary = {
            "status": "passed", "claim_level": spec.claim_level,
            "analytical_reference": {
                "yield_force_n": spec.yield_force_n, "yield_stress_pa": spec.yield_stress_pa,
                "youngs_modulus_pa": spec.youngs_modulus_pa, "total_tangent_modulus_pa": spec.tangent_modulus_pa,
                "plastic_hardening_modulus_pa": spec.hardening_modulus_pa,
                "peak_stress_pa": factors[2] * spec.yield_stress_pa,
                "peak_total_strain": spec.monotonic_strain(factors[2] * spec.yield_stress_pa),
                "residual_plastic_strain": spec.monotonic_plastic_strain(factors[2] * spec.yield_stress_pa),
            },
            "mesh_results": mesh_results, "mesh_convergence": convergence,
            "process_evidence": processes, "config_sha256": sha(args.config), "tool_sha256": {"ccx": sha(args.ccx)},
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip(),
            "worktree_dirty_during_run": bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, check=True, text=True, capture_output=True).stdout),
            "review": {
                "supporting_evidence": ["solver plastic strain, residual deformation, hardening tangent, reaction, and internal-energy evidence were parsed", "below-yield, unloading, reverse-elastic, and mesh controls were retained"],
                "contradicting_evidence": [],
                "alternative_explanations": ["the homogeneous coupon suppresses geometric stress concentrations", "a synthetic bilinear law is simpler than a real processed material"],
                "missing_evidence": ["physical coupon data", "temperature/rate dependence", "cyclic plasticity, fracture, and fatigue"],
                "confidence": "high for this synthetic uniaxial CalculiX material-law route only",
            },
        }
        write_json(args.artifact_root / "experiment_summary.json", summary)
        print(json.dumps({"status": "passed", "fine_metrics": fine["metrics"], "mesh_convergence": convergence, "summary": str(args.artifact_root / "experiment_summary.json")}, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {"status": "failed", "failed_stage": stage, "error_type": type(exc).__name__, "message": str(exc), "process_evidence": processes, "traceback": traceback.format_exc()}
        write_json(args.artifact_root / "experiment_failure.json", failure)
        print(json.dumps(failure, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
