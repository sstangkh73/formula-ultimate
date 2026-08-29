"""Run Work 035 through Gmsh, CalculiX, and beam-bending evidence gates."""

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
    BendingSpec,
    StructuralEvidenceError,
    build_bending_calculix_input,
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
        command, cwd=cwd, text=True, capture_output=True, check=False
    )
    return {
        "command": command,
        "exit_code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "started_time_ns": started,
        "wall_time_s": time.perf_counter() - monotonic,
    }


def _geo(spec: BendingSpec, size_m: float) -> str:
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


def _tetrahedron_volume_and_centroid(
    nodes: dict[int, tuple[float, float, float]],
    connectivity: tuple[int, int, int, int],
) -> tuple[float, tuple[float, float, float]]:
    points = tuple(nodes[node] for node in connectivity)
    a, b, c, d = points
    ab = tuple(b[index] - a[index] for index in range(3))
    ac = tuple(c[index] - a[index] for index in range(3))
    ad = tuple(d[index] - a[index] for index in range(3))
    cross = (
        ac[1] * ad[2] - ac[2] * ad[1],
        ac[2] * ad[0] - ac[0] * ad[2],
        ac[0] * ad[1] - ac[1] * ad[0],
    )
    volume = abs(math.fsum(ab[index] * cross[index] for index in range(3))) / 6.0
    centroid = tuple(math.fsum(point[index] for point in points) / 4.0 for index in range(3))
    return volume, centroid  # type: ignore[return-value]


def _moment_about(
    origin: tuple[float, float, float],
    position: tuple[float, float, float],
    force: tuple[float, float, float],
) -> tuple[float, float, float]:
    radius = tuple(position[index] - origin[index] for index in range(3))
    return (
        radius[1] * force[2] - radius[2] * force[1],
        radius[2] * force[0] - radius[0] * force[2],
        radius[0] * force[1] - radius[1] * force[0],
    )


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
        spec = BendingSpec.from_mapping(payload)
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
        origin = (0.0, spec.width_m / 2.0, spec.height_m / 2.0)
        for level in mesh_levels:
            mesh_id = str(level["mesh_id"])
            size_m = float(level["characteristic_size_m"])
            run_dir = args.artifact_root / mesh_id
            run_dir.mkdir()
            geo_path = run_dir / "beam.geo"
            mesh_path = run_dir / "beam.msh"
            deck_path = run_dir / "beam.inp"
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
            deck, nodal_loads, fixed, loaded = build_bending_calculix_input(
                spec=spec,
                mesh=mesh,
                boundary_tolerance_m=float(tolerances["boundary_coordinate_absolute_m"]),
            )
            deck_path.write_text(deck, encoding="ascii")

            current_stage = f"calculix:{mesh_id}"
            ccx_evidence = _run([str(args.ccx), "beam"], run_dir)
            ccx_evidence["stage"] = current_stage
            process_evidence.append(ccx_evidence)
            dat_path = run_dir / "beam.dat"
            frd_path = run_dir / "beam.frd"
            if ccx_evidence["exit_code"] != 0:
                raise StructuralEvidenceError(f"CalculiX failed for {mesh_id}: {ccx_evidence}")
            for evidence_path in (dat_path, frd_path):
                if not evidence_path.is_file() or evidence_path.stat().st_mtime_ns < ccx_evidence["started_time_ns"]:
                    raise StructuralEvidenceError(
                        f"CalculiX did not create fresh {evidence_path.name} evidence for {mesh_id}"
                    )
            parsed = parse_calculix_dat(dat_path)
            if set(loaded) - set(parsed["displacements"]) or set(fixed) - set(parsed["reactions"]):
                raise StructuralEvidenceError("solver evidence omitted declared boundary nodes")
            stress_tensors = parsed["stress_tensor_by_element_pa"]
            if set(stress_tensors) != set(mesh.tetrahedra):
                raise StructuralEvidenceError("solver stress evidence does not cover the exact tetrahedral mesh")

            volume_centroid = {
                element: _tetrahedron_volume_and_centroid(mesh.nodes, connectivity)
                for element, connectivity in mesh.tetrahedra.items()
            }
            mesh_volume = math.fsum(item[0] for item in volume_centroid.values())
            if not math.isclose(mesh_volume, spec.volume_m3, rel_tol=1.0e-8, abs_tol=1.0e-14):
                raise StructuralEvidenceError(
                    f"tetrahedral volume {mesh_volume} differs from declared {spec.volume_m3}"
                )

            tip_displacement_signed = math.fsum(
                (-nodal_loads[node]) * parsed["displacements"][node][2]
                for node in loaded
            ) / spec.force_magnitude_n
            tip_displacement_magnitude = -tip_displacement_signed
            external_work = 0.5 * math.fsum(
                nodal_loads[node] * parsed["displacements"][node][2]
                for node in loaded
            )
            reaction_force = parsed["total_reaction"]
            applied_force = (0.0, 0.0, -spec.force_magnitude_n)
            force_residual = tuple(applied_force[axis] + reaction_force[axis] for axis in range(3))
            reaction_moment = tuple(
                math.fsum(
                    _moment_about(origin, mesh.nodes[node], parsed["reactions"][node])[axis]
                    for node in fixed
                )
                for axis in range(3)
            )
            applied_moment = tuple(
                math.fsum(
                    _moment_about(origin, mesh.nodes[node], (0.0, 0.0, nodal_loads[node]))[axis]
                    for node in loaded
                )
                for axis in range(3)
            )
            moment_residual = tuple(applied_moment[axis] + reaction_moment[axis] for axis in range(3))

            gauge = []
            for element, (volume, centroid) in volume_centroid.items():
                if spec.gauge_x_min_m <= centroid[0] <= spec.gauge_x_max_m:
                    actual = stress_tensors[element][0]
                    reference = spec.analytical_sxx_pa(x_m=centroid[0], z_m=centroid[2])
                    gauge.append((volume, actual, reference))
            if not gauge:
                raise StructuralEvidenceError("declared interior stress gauge contains no elements")
            error_square = math.fsum(
                volume * (actual - reference) ** 2 for volume, actual, reference in gauge
            )
            reference_square = math.fsum(volume * reference**2 for volume, _, reference in gauge)
            actual_square = math.fsum(volume * actual**2 for volume, actual, _ in gauge)
            cross = math.fsum(volume * actual * reference for volume, actual, reference in gauge)
            if reference_square <= 0.0 or actual_square <= 0.0:
                raise StructuralEvidenceError("stress gauge has zero analytical or solver magnitude")
            stress_error = math.sqrt(error_square / reference_square)
            stress_correlation = cross / math.sqrt(actual_square * reference_square)

            force_residual_norm = math.sqrt(math.fsum(value * value for value in force_residual))
            moment_residual_norm = math.sqrt(math.fsum(value * value for value in moment_residual))
            metrics = {
                "tip_displacement_signed_m": tip_displacement_signed,
                "tip_displacement_magnitude_m": tip_displacement_magnitude,
                "reaction_force_n": reaction_force,
                "force_residual_n": force_residual,
                "reaction_moment_nm": reaction_moment,
                "applied_moment_nm": applied_moment,
                "moment_residual_nm": moment_residual,
                "external_work_j": external_work,
                "stress_gauge_element_count": len(gauge),
                "stress_field_normalized_rms": stress_error,
                "stress_field_signed_correlation": stress_correlation,
                "tip_displacement_analytical_relative": _relative(
                    tip_displacement_magnitude, spec.analytical_tip_displacement_m
                ),
                "energy_analytical_relative": _relative(external_work, spec.analytical_energy_j),
                "force_closure_relative": force_residual_norm / spec.force_magnitude_n,
                "moment_closure_relative": moment_residual_norm / spec.analytical_root_moment_nm,
            }
            failures = []
            for name in (
                "tip_displacement_analytical_relative",
                "stress_field_normalized_rms",
                "energy_analytical_relative",
                "force_closure_relative",
                "moment_closure_relative",
            ):
                if metrics[name] > float(tolerances[name]):
                    failures.append(name)
            if stress_correlation < float(tolerances["stress_field_signed_correlation_minimum"]):
                failures.append("stress_field_signed_correlation")
            if failures:
                raise StructuralEvidenceError(
                    f"{mesh_id} bending gates failed: {failures}; metrics={metrics}"
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
                fine["metrics"]["tip_displacement_magnitude_m"],
                medium["metrics"]["tip_displacement_magnitude_m"],
            ),
            "last_two_stress_error_absolute_change": abs(
                fine["metrics"]["stress_field_normalized_rms"]
                - medium["metrics"]["stress_field_normalized_rms"]
            ),
            "last_two_energy_relative": _relative(
                fine["metrics"]["external_work_j"], medium["metrics"]["external_work_j"]
            ),
        }
        convergence_failures = [
            name for name, value in convergence.items() if value > float(tolerances[name])
        ]
        if convergence_failures:
            raise StructuralEvidenceError(
                f"last-two-mesh convergence failed: {convergence_failures}; values={convergence}"
            )

        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True
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
                "second_moment_m4": spec.second_moment_m4,
                "tip_displacement_m": spec.analytical_tip_displacement_m,
                "root_moment_nm": spec.analytical_root_moment_nm,
                "root_outer_stress_pa": spec.analytical_root_outer_stress_pa,
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
                    ROOT / "scripts/run_work035.ps1",
                )
            },
            "repository_commit": commit,
            "worktree_dirty_during_run": bool(subprocess.run(
                ["git", "status", "--porcelain"], cwd=ROOT, check=True,
                text=True, capture_output=True,
            ).stdout),
            "review": {
                "supporting_evidence": [
                    "three declared Gmsh meshes produced connected finite-volume solids",
                    "CalculiX produced fresh displacement, reaction, and full stress-tensor evidence",
                    "force and moment equilibrium and analytical response gates passed",
                    "the two finest meshes passed declared convergence gates",
                ],
                "contradicting_evidence": [],
                "alternative_explanations": [
                    "the regular slender beam is a deliberately simple fixture",
                    "Euler-Bernoulli agreement does not validate arbitrary short/deep geometry",
                ],
                "missing_evidence": [
                    "independent solver agreement and physical beam data",
                    "torsion, buckling, interfaces, plasticity, fracture, and fatigue",
                ],
                "confidence": "high for this local linear slender-beam route only",
            },
        }
        _write_json(summary_path, summary)
        print(json.dumps({
            "status": summary["status"],
            "mesh_count": len(results),
            "finest_nodes": results[-1]["node_count"],
            "finest_tetrahedra": results[-1]["tetrahedron_count"],
            "finest_tip_displacement_m": results[-1]["metrics"]["tip_displacement_magnitude_m"],
            "finest_stress_normalized_rms": results[-1]["metrics"]["stress_field_normalized_rms"],
            "force_closure_relative": results[-1]["metrics"]["force_closure_relative"],
            "moment_closure_relative": results[-1]["metrics"]["moment_closure_relative"],
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
