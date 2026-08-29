"""Run Work 034 through Gmsh, CalculiX, parsing, and analytical gates."""

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
    StructuralEvidenceError,
    TensionSpec,
    build_calculix_input,
    parse_calculix_dat,
    parse_msh2,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _run(command: list[str], cwd: Path) -> dict[str, Any]:
    started = time.time_ns()
    monotonic = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": command,
        "exit_code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "started_time_ns": started,
        "wall_time_s": time.perf_counter() - monotonic,
    }


def _geo(spec: TensionSpec, size_m: float) -> str:
    return "\n".join((
        'SetFactory("OpenCASCADE");',
        f"Box(1) = {{0, 0, 0, {spec.length_m:.17g}, {spec.width_m:.17g}, {spec.height_m:.17g}}};",
        f"Mesh.CharacteristicLengthMin = {size_m:.17g};",
        f"Mesh.CharacteristicLengthMax = {size_m:.17g};",
        "Mesh.Algorithm3D = 1;",
        "Mesh.ElementOrder = 1;",
        "Mesh.MshFileVersion = 2.2;",
        "Mesh.Binary = 0;",
        "Mesh.SaveAll = 1;",
        "Physical Volume(1) = {1};",
        "",
    ))


def _relative(actual: float, expected: float) -> float:
    return abs(actual - expected) / max(abs(expected), 1.0e-300)


def _tetrahedron_volume(
    nodes: dict[int, tuple[float, float, float]],
    connectivity: tuple[int, int, int, int],
) -> float:
    a, b, c, d = (nodes[node] for node in connectivity)
    ab = tuple(b[index] - a[index] for index in range(3))
    ac = tuple(c[index] - a[index] for index in range(3))
    ad = tuple(d[index] - a[index] for index in range(3))
    cross = (
        ac[1] * ad[2] - ac[2] * ad[1],
        ac[2] * ad[0] - ac[0] * ad[2],
        ac[0] * ad[1] - ac[1] * ad[0],
    )
    return abs(math.fsum(ab[index] * cross[index] for index in range(3))) / 6.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--gmsh", type=Path, required=True)
    parser.add_argument("--ccx", type=Path, required=True)
    args = parser.parse_args()

    summary_path = args.artifact_root / "experiment_summary.json"
    failure_path = args.artifact_root / "experiment_failure.json"
    current_stage = "configuration"
    process_evidence: list[dict[str, Any]] = []
    try:
        payload = json.loads(args.config.read_text(encoding="utf-8"))
        spec = TensionSpec.from_mapping(payload)
        tolerances = payload["tolerances"]
        mesh_levels = payload["mesh_levels"]
        if len(mesh_levels) != 3:
            raise StructuralEvidenceError("exactly three predeclared mesh levels are required")
        sizes = [float(item["characteristic_size_m"]) for item in mesh_levels]
        if not all(math.isfinite(value) and value > 0.0 for value in sizes):
            raise StructuralEvidenceError("mesh sizes must be finite and > 0")
        if not all(left > right for left, right in zip(sizes, sizes[1:])):
            raise StructuralEvidenceError("mesh levels must be strictly finer")
        for executable in (args.gmsh, args.ccx):
            if not executable.is_file():
                raise StructuralEvidenceError(f"required executable is missing: {executable}")

        if args.artifact_root.exists():
            shutil.rmtree(args.artifact_root)
        args.artifact_root.mkdir(parents=True)
        results: list[dict[str, Any]] = []
        for level in mesh_levels:
            mesh_id = str(level["mesh_id"])
            size_m = float(level["characteristic_size_m"])
            run_dir = args.artifact_root / mesh_id
            run_dir.mkdir()
            geo_path = run_dir / "tension.geo"
            mesh_path = run_dir / "tension.msh"
            deck_path = run_dir / "tension.inp"
            geo_path.write_text(_geo(spec, size_m), encoding="ascii")

            current_stage = f"gmsh:{mesh_id}"
            gmsh_evidence = _run(
                [str(args.gmsh), str(geo_path), "-3", "-format", "msh2", "-o", str(mesh_path)],
                run_dir,
            )
            gmsh_evidence["stage"] = current_stage
            process_evidence.append(gmsh_evidence)
            if gmsh_evidence["exit_code"] != 0:
                raise StructuralEvidenceError(f"Gmsh failed for {mesh_id}: {gmsh_evidence}")
            if not mesh_path.is_file() or mesh_path.stat().st_mtime_ns < gmsh_evidence["started_time_ns"]:
                raise StructuralEvidenceError(f"Gmsh did not create fresh mesh evidence for {mesh_id}")
            mesh = parse_msh2(mesh_path)
            deck, nodal_loads, fixed, loaded = build_calculix_input(
                spec=spec,
                mesh=mesh,
                boundary_tolerance_m=float(tolerances["boundary_coordinate_absolute_m"]),
            )
            deck_path.write_text(deck, encoding="ascii")

            current_stage = f"calculix:{mesh_id}"
            ccx_evidence = _run([str(args.ccx), "tension"], run_dir)
            ccx_evidence["stage"] = current_stage
            process_evidence.append(ccx_evidence)
            dat_path = run_dir / "tension.dat"
            frd_path = run_dir / "tension.frd"
            if ccx_evidence["exit_code"] != 0:
                raise StructuralEvidenceError(f"CalculiX failed for {mesh_id}: {ccx_evidence}")
            for evidence_path in (dat_path, frd_path):
                if not evidence_path.is_file() or evidence_path.stat().st_mtime_ns < ccx_evidence["started_time_ns"]:
                    raise StructuralEvidenceError(
                        f"CalculiX did not create fresh {evidence_path.name} evidence for {mesh_id}"
                    )
            parsed = parse_calculix_dat(dat_path)
            missing_loaded = set(loaded) - set(parsed["displacements"])
            missing_fixed = set(fixed) - set(parsed["reactions"])
            if missing_loaded or missing_fixed:
                raise StructuralEvidenceError(
                    f"solver evidence omitted boundary nodes: loaded={sorted(missing_loaded)}, fixed={sorted(missing_fixed)}"
                )
            loaded_displacement = math.fsum(
                nodal_loads[node] * parsed["displacements"][node][0]
                for node in loaded
            ) / spec.resultant_force_n
            reaction_x = math.fsum(parsed["reactions"][node][0] for node in fixed)
            stress_by_element = parsed["axial_stress_by_element_pa"]
            if set(stress_by_element) != set(mesh.tetrahedra):
                raise StructuralEvidenceError("solver stress evidence does not cover the exact tetrahedral mesh")
            element_volumes = {
                element: _tetrahedron_volume(mesh.nodes, connectivity)
                for element, connectivity in mesh.tetrahedra.items()
            }
            mesh_volume = math.fsum(element_volumes.values())
            if not math.isclose(mesh_volume, spec.volume_m3, rel_tol=1.0e-8, abs_tol=1.0e-14):
                raise StructuralEvidenceError(
                    f"tetrahedral volume {mesh_volume} differs from declared {spec.volume_m3}"
                )
            stress_x = math.fsum(
                stress_by_element[element] * element_volumes[element]
                for element in mesh.tetrahedra
            ) / mesh_volume
            external_work = 0.5 * math.fsum(
                nodal_loads[node] * parsed["displacements"][node][0]
                for node in loaded
            )
            force_residual = spec.resultant_force_n + reaction_x
            metrics = {
                "loaded_displacement_m": loaded_displacement,
                "support_reaction_x_n": reaction_x,
                "force_residual_n": force_residual,
                "mean_axial_stress_pa": stress_x,
                "external_work_j": external_work,
                "displacement_analytical_relative": _relative(
                    loaded_displacement, spec.analytical_displacement_m
                ),
                "stress_analytical_relative": _relative(
                    stress_x, spec.analytical_stress_pa
                ),
                "energy_analytical_relative": _relative(
                    external_work, spec.analytical_energy_j
                ),
                "force_closure_relative": abs(force_residual) / abs(spec.resultant_force_n),
            }
            limits = {
                "displacement_analytical_relative": tolerances["displacement_analytical_relative"],
                "stress_analytical_relative": tolerances["stress_analytical_relative"],
                "energy_analytical_relative": tolerances["energy_analytical_relative"],
                "force_closure_relative": tolerances["force_closure_relative"],
            }
            failures = [name for name, limit in limits.items() if metrics[name] > limit]
            if failures:
                raise StructuralEvidenceError(
                    f"{mesh_id} analytical/equilibrium gates failed: {failures}; metrics={metrics}"
                )
            results.append({
                "mesh_id": mesh_id,
                "characteristic_size_m": size_m,
                "node_count": len(mesh.nodes),
                "tetrahedron_count": len(mesh.tetrahedra),
                "surface_triangle_count": len(mesh.triangles),
                "mesh_volume_m3": mesh_volume,
                "fixed_node_count": len(fixed),
                "loaded_node_count": len(loaded),
                "distributed_load_sum_n": math.fsum(nodal_loads.values()),
                "mesh_sha256": _sha256(mesh_path),
                "deck_sha256": _sha256(deck_path),
                "dat_sha256": _sha256(dat_path),
                "frd_sha256": _sha256(frd_path),
                "metrics": metrics,
            })

        current_stage = "mesh_convergence"
        medium, fine = results[-2:]
        convergence = {
            "last_two_displacement_relative": _relative(
                fine["metrics"]["loaded_displacement_m"],
                medium["metrics"]["loaded_displacement_m"],
            ),
            "last_two_stress_relative": _relative(
                fine["metrics"]["mean_axial_stress_pa"],
                medium["metrics"]["mean_axial_stress_pa"],
            ),
            "last_two_energy_relative": _relative(
                fine["metrics"]["external_work_j"],
                medium["metrics"]["external_work_j"],
            ),
        }
        convergence_failures = [
            name for name, value in convergence.items() if value > tolerances[name]
        ]
        if convergence_failures:
            raise StructuralEvidenceError(
                f"last-two-mesh convergence failed: {convergence_failures}; values={convergence}"
            )
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
            text=True, capture_output=True,
        ).stdout.strip()
        summary = {
            "status": "passed",
            "protocol_id": spec.protocol_id,
            "experiment_id": spec.experiment_id,
            "specimen_id": spec.specimen_id,
            "claim_level": spec.claim_level,
            "analytical_reference": {
                "area_m2": spec.area_m2,
                "volume_m3": spec.volume_m3,
                "stress_pa": spec.analytical_stress_pa,
                "strain": spec.analytical_strain,
                "displacement_m": spec.analytical_displacement_m,
                "energy_j": spec.analytical_energy_j,
            },
            "mesh_results": results,
            "mesh_convergence": convergence,
            "process_evidence": process_evidence,
            "config_sha256": _sha256(args.config),
            "tool_sha256": {"gmsh": _sha256(args.gmsh), "ccx": _sha256(args.ccx)},
            "source_sha256": {
                str(path.relative_to(ROOT)): _sha256(path)
                for path in (
                    ROOT / "src/formula_ultimate/structural/acceptance.py",
                    Path(__file__),
                    ROOT / "scripts/run_work034.ps1",
                )
            },
            "repository_commit": commit,
            "worktree_dirty_during_run": bool(subprocess.run(
                ["git", "status", "--porcelain"], cwd=ROOT, check=True,
                text=True, capture_output=True,
            ).stdout),
            "review": {
                "supporting_evidence": [
                    "three declared Gmsh meshes produced connected tetrahedral solids",
                    "CalculiX produced fresh parsed displacement, reaction, and stress evidence",
                    "all meshes passed analytical and force-closure gates",
                    "the two finest meshes passed declared convergence gates",
                ],
                "contradicting_evidence": [],
                "alternative_explanations": [
                    "the prismatic uniform-tension fixture is unusually simple",
                    "agreement does not validate arbitrary geometry or nonlinear material failure",
                ],
                "missing_evidence": [
                    "independent solver agreement and physical coupon data",
                    "bending, torsion, buckling, loaded interfaces, plasticity, fracture, and fatigue",
                ],
                "confidence": "high for this local linear tension route only",
            },
        }
        _write_json(summary_path, summary)
        print(json.dumps({
            "status": summary["status"],
            "mesh_count": len(results),
            "finest_nodes": results[-1]["node_count"],
            "finest_tetrahedra": results[-1]["tetrahedron_count"],
            "finest_displacement_m": results[-1]["metrics"]["loaded_displacement_m"],
            "finest_stress_pa": results[-1]["metrics"]["mean_axial_stress_pa"],
            "force_closure_relative": results[-1]["metrics"]["force_closure_relative"],
            "summary": str(summary_path),
        }, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {
            "status": "failed",
            "failed_stage": current_stage,
            "error_type": type(exc).__name__,
            "message": str(exc),
            "process_evidence": process_evidence,
            "traceback": traceback.format_exc(),
        }
        _write_json(failure_path, failure)
        print(json.dumps(failure, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
