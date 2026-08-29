from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from formula_ultimate.structural import (  # noqa: E402
    TensionSpec,
    build_element_column_input,
    imperfect_element_mesh,
    parse_element_column_dat,
    parse_element_msh2,
)
from scripts.structural.run_eigenvalue_buckling_acceptance import mode_vectors  # noqa: E402


def run(command: list[str], cwd: Path) -> tuple[subprocess.CompletedProcess[str], float]:
    started = time.perf_counter()
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    return completed, time.perf_counter() - started


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def geometry_text(length: float, width: float, height: float, size: float, order: int) -> str:
    lines = [
        'SetFactory("OpenCASCADE");', f"Box(1)={{0,0,0,{length},{width},{height}}};",
        f"Mesh.CharacteristicLengthMin={size};", f"Mesh.CharacteristicLengthMax={size};",
        f"Mesh.ElementOrder={order};",
    ]
    if order == 2:
        lines.append("Mesh.SecondOrderLinear=1;")
    lines.extend(("Mesh.MshFileVersion=2.2;", "Mesh.Binary=0;", "Mesh.SaveAll=1;", "Physical Volume(1)={1};", ""))
    return "\n".join(lines)


def nonlinear_deck(static_deck: str) -> str:
    marker = "*STEP\n*STATIC\n*CLOAD"
    if static_deck.count(marker) != 1:
        raise RuntimeError("static step marker is missing or ambiguous")
    return static_deck.replace(marker, "*STEP, NLGEOM\n*STATIC\n1., 1.\n*CLOAD")


def buckling_deck(static_deck: str) -> str:
    marker = "*STEP\n*STATIC\n*CLOAD"
    printed_tables = (
        "*NODE PRINT, NSET=LOADED\nU\n*NODE PRINT, NSET=FIXED, TOTALS=YES\nRF\n"
        "*EL PRINT, ELSET=EALL\nS, E\n"
    )
    if static_deck.count(marker) != 1 or static_deck.count(printed_tables) != 1:
        raise RuntimeError("buckling deck transformation contract failed")
    return static_deck.replace(marker, "*STEP\n*BUCKLE\n4, 0.001\n*CLOAD").replace(printed_tables, "")


def von_mises(tensor: tuple[float, float, float, float, float, float]) -> float:
    sx, sy, sz, txy, txz, tyz = tensor
    return math.sqrt(
        0.5 * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2)
        + 3.0 * (txy * txy + txz * txz + tyz * tyz)
    )


def relative_difference(first: float, second: float) -> float:
    scale = 0.5 * (abs(first) + abs(second))
    return abs(first - second) / scale if scale else 0.0


def spec_for(config: dict, force_n: float, specimen_id: str) -> TensionSpec:
    geometry, material = config["geometry"], config["material"]
    return TensionSpec(
        config["protocol_id"], "work041", specimen_id,
        "precritical numerical element verification only", float(geometry["length_m"]),
        float(geometry["width_m"]), float(geometry["height_m"]), material["material_id"],
        float(material["youngs_modulus_pa"]), float(material["poisson_ratio"]),
        float(material["density_kg_per_m3"]), material["provenance"], force_n,
    )


def solve_static(
    *, case_dir: Path, ccx: Path, deck: str, loads: dict[int, float],
    amplitude_m: float, load_n: float, critical_load_n: float,
) -> dict:
    case_dir.mkdir(parents=True)
    input_path = case_dir / "column.inp"
    input_path.write_text(nonlinear_deck(deck), encoding="ascii")
    completed, wall_time = run([str(ccx), "column"], case_dir)
    (case_dir / "solver_stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (case_dir / "solver_stderr.txt").write_text(completed.stderr, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(f"CalculiX nonlinear solve failed in {case_dir}: {completed.stdout[-1500:]}")
    if "nonlinear geometric" not in completed.stdout.lower():
        raise RuntimeError(f"NLGEOM confirmation is missing in {case_dir}")
    parsed = parse_element_column_dat(case_dir / "column.dat")
    weights = {node: abs(value) for node, value in loads.items()}
    total_weight = math.fsum(weights.values())
    tip_ux = math.fsum(weights[node] * parsed["displacements"][node][0] for node in weights) / total_weight
    tip_uz = math.fsum(weights[node] * parsed["displacements"][node][2] for node in weights) / total_weight
    total_offset = amplitude_m + tip_uz
    amplification = total_offset / amplitude_m
    reference = 1.0 / (1.0 - load_n / critical_load_n)
    evidence = [input_path, case_dir / "column.dat", case_dir / "column.frd", case_dir / "solver_stdout.txt"]
    return {
        "load_n": load_n, "incremental_tip_lateral_displacement_m": tip_uz,
        "total_tip_offset_m": total_offset, "tip_axial_displacement_m": tip_ux,
        "measured_amplification": amplification, "secant_reference_amplification": reference,
        "secant_error_relative": abs(amplification - reference) / reference,
        "reaction_error_relative": abs(parsed["total_reaction"][0] - load_n) / load_n,
        "maximum_von_mises_stress_pa": max(von_mises(value) for value in parsed["stress_tensors_pa"].values()),
        "integration_point_count": len(parsed["stress_tensors_pa"]), "solver_wall_time_s": wall_time,
        "strain_energy": {"status": "not_requested", "reason": "no independently validated Work 041 energy parser"},
        "evidence_sha256": {path.name: sha256(path) for path in evidence},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--gmsh", type=Path, required=True)
    parser.add_argument("--ccx", type=Path, required=True)
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        geometry, material, tolerances = config["geometry"], config["material"], config["tolerances"]
        loads_n = [float(value) for value in config["absolute_compression_loads_n"]]
        amplitude = float(config["tip_imperfection_m"])
        if args.artifact_root.exists():
            shutil.rmtree(args.artifact_root)
        args.artifact_root.mkdir(parents=True)
        mesh_results: list[dict] = []

        for mesh_case in config["mesh_cases"]:
            mesh_id, order = mesh_case["mesh_id"], int(mesh_case["order"])
            mesh_dir = args.artifact_root / mesh_id
            mesh_dir.mkdir()
            geo_path, mesh_path = mesh_dir / "column.geo", mesh_dir / "column.msh"
            geo_path.write_text(
                geometry_text(
                    float(geometry["length_m"]), float(geometry["width_m"]),
                    float(geometry["height_m"]), float(mesh_case["characteristic_size_m"]), order,
                ), encoding="ascii",
            )
            meshed, mesh_time = run([str(args.gmsh), str(geo_path), "-3", "-format", "msh2", "-o", str(mesh_path)], mesh_dir)
            (mesh_dir / "gmsh_stdout.txt").write_text(meshed.stdout, encoding="utf-8")
            if meshed.returncode != 0:
                raise RuntimeError(f"Gmsh failed for {mesh_id}: {meshed.stdout[-1500:]}")
            mesh = parse_element_msh2(mesh_path, expected_order=order)

            reference_spec = spec_for(config, -float(config["reference_compression_n"]), mesh_id)
            reference_deck, _, _, _ = build_element_column_input(
                spec=reference_spec, mesh=mesh,
                boundary_tolerance_m=float(tolerances["boundary_coordinate_absolute_m"]),
            )
            static_dir = mesh_dir / "reference_static"
            static_dir.mkdir()
            (static_dir / "column.inp").write_text(reference_deck.replace("*STATIC\n*CLOAD", "*STATIC\n1., 1.\n*CLOAD"), encoding="ascii")
            static_run, static_time = run([str(args.ccx), "column"], static_dir)
            (static_dir / "solver_stdout.txt").write_text(static_run.stdout, encoding="utf-8")
            if static_run.returncode != 0:
                raise RuntimeError(f"CalculiX reference static failed for {mesh_id}: {static_run.stdout[-1500:]}")
            static_data = parse_element_column_dat(static_dir / "column.dat")
            reference_reaction_error = abs(
                static_data["total_reaction"][0] - float(config["reference_compression_n"])
            ) / float(config["reference_compression_n"])

            buckling_dir = mesh_dir / "buckling"
            buckling_dir.mkdir()
            buckling_input = buckling_dir / "column.inp"
            buckling_input.write_text(buckling_deck(reference_deck), encoding="ascii")
            buckled, buckling_time = run([str(args.ccx), "column"], buckling_dir)
            (buckling_dir / "solver_stdout.txt").write_text(buckled.stdout, encoding="utf-8")
            if buckled.returncode != 0:
                raise RuntimeError(f"CalculiX buckling failed for {mesh_id}: {buckled.stdout[-1500:]}")
            dat_text = (buckling_dir / "column.dat").read_text(encoding="ascii", errors="replace")
            factors = [float(value) for value in re.findall(r"^\s*\d+\s+([-+0-9.Ee]+)\s*$", dat_text, re.MULTILINE)]
            modes = mode_vectors((buckling_dir / "column.frd").read_text(encoding="ascii", errors="replace"))
            if not factors or len(modes) < 2 or len(modes[0][1]) != len(mesh.nodes):
                raise RuntimeError(f"buckling factor/mode evidence is incomplete for {mesh_id}")
            positive = [value for value in factors if value > 0.0]
            if not positive:
                raise RuntimeError(f"positive compression buckling factor is missing for {mesh_id}")
            critical_load = min(positive) * float(config["reference_compression_n"])
            first_vectors = modes[0][1]
            transverse = math.sqrt(math.fsum(y * y + z * z for _, y, z in first_vectors))
            axial = math.sqrt(math.fsum(x * x for x, _, _ in first_vectors))
            transverse_ratio = transverse / max(axial, 1e-300)
            pair_split = abs(positive[1] - positive[0]) / positive[0]
            inertia = float(geometry["width_m"]) * float(geometry["height_m"]) ** 3 / 12.0
            analytical_pcr = math.pi**2 * float(material["youngs_modulus_pa"]) * inertia / (
                float(geometry["effective_length_factor"]) * float(geometry["length_m"])
            ) ** 2

            imperfect = imperfect_element_mesh(mesh, length_m=float(geometry["length_m"]), tip_amplitude_m=amplitude)
            nonlinear_cases = []
            for load_n in loads_n:
                if load_n >= critical_load:
                    raise RuntimeError(f"absolute load {load_n} is not subcritical for {mesh_id} Pcr={critical_load}")
                load_spec = spec_for(config, -load_n, mesh_id)
                static_deck, nodal_loads, _, _ = build_element_column_input(
                    spec=load_spec, mesh=imperfect,
                    boundary_tolerance_m=float(tolerances["boundary_coordinate_absolute_m"]),
                )
                case = solve_static(
                    case_dir=mesh_dir / f"nonlinear_{round(load_n)}n", ccx=args.ccx,
                    deck=static_deck, loads=nodal_loads, amplitude_m=amplitude,
                    load_n=load_n, critical_load_n=critical_load,
                )
                nonlinear_cases.append(case)

            result = {
                "mesh_id": mesh_id, "element_type": mesh.calculix_element_type, "order": order,
                "characteristic_size_m": float(mesh_case["characteristic_size_m"]), "nodes": len(mesh.nodes),
                "estimated_displacement_dofs": 3 * len(mesh.nodes), "tetrahedra": len(mesh.tetrahedra),
                "mesh_wall_time_s": mesh_time, "reference_static_wall_time_s": static_time,
                "buckling_wall_time_s": buckling_time, "mesh_sha256": sha256(mesh_path),
                "critical_load_n": critical_load, "analytical_critical_load_n": analytical_pcr,
                "analytical_eigenvalue_error_relative": abs(critical_load - analytical_pcr) / analytical_pcr,
                "reference_reaction_error_relative": reference_reaction_error,
                "mode_pair_split_relative": pair_split, "mode_transverse_axial_ratio": transverse_ratio,
                "buckling_factors": factors, "nonlinear_cases": nonlinear_cases,
                "memory_evidence": {"status": "proxy_only", "estimated_displacement_dofs": 3 * len(mesh.nodes)},
            }
            mesh_results.append(result)

        reaction_limit = float(tolerances["reaction_error_relative"])
        for result in mesh_results:
            if result["reference_reaction_error_relative"] > reaction_limit:
                raise RuntimeError(f"reference reaction gate failed for {result['mesh_id']}")
            if result["mode_pair_split_relative"] > float(tolerances["mode_pair_split_relative"]):
                raise RuntimeError(f"mode pair gate failed for {result['mesh_id']}")
            if result["mode_transverse_axial_ratio"] < float(tolerances["mode_transverse_axial_minimum"]):
                raise RuntimeError(f"mode identity gate failed for {result['mesh_id']}")
            if any(case["reaction_error_relative"] > reaction_limit for case in result["nonlinear_cases"]):
                raise RuntimeError(f"nonlinear reaction gate failed for {result['mesh_id']}")

        by_id = {result["mesh_id"]: result for result in mesh_results}
        c3d4_changes, element_differences = {}, {}
        for index, load_n in enumerate(loads_n):
            medium = by_id["c3d4_0p8mm"]["nonlinear_cases"][index]["measured_amplification"]
            fine = by_id["c3d4_0p65mm"]["nonlinear_cases"][index]["measured_amplification"]
            quadratic = by_id["c3d10_1p4mm"]["nonlinear_cases"][index]["measured_amplification"]
            c3d4_changes[str(load_n)] = relative_difference(medium, fine)
            element_differences[str(load_n)] = relative_difference(fine, quadratic)
        secant_errors = [
            case["secant_error_relative"] for result in mesh_results for case in result["nonlinear_cases"]
        ]
        eigen_errors = [result["analytical_eigenvalue_error_relative"] for result in mesh_results]
        node_difference = relative_difference(
            float(by_id["c3d4_0p65mm"]["nodes"]), float(by_id["c3d10_1p4mm"]["nodes"])
        )
        convergence_supported = (
            max(c3d4_changes.values()) <= float(tolerances["last_two_c3d4_amplification_change_relative"])
            and max(element_differences.values()) <= float(tolerances["refined_c3d4_c3d10_amplification_difference_relative"])
            and max(secant_errors) <= float(tolerances["secant_error_relative"])
            and max(eigen_errors) <= float(tolerances["analytical_eigenvalue_error_relative"])
        )
        compute_comparable = node_difference <= float(config["mesh_only_pilot"]["maximum_relative_node_count_difference"])
        summary = {
            "status": "passed", "claim_level": "precritical numerical element verification only",
            "execution_gates": {"complete": True, "reaction_closure": True, "mode_identity": True},
            "convergence_hypothesis": {
                "status": "supported" if convergence_supported else "rejected",
                "last_two_c3d4_amplification_change_relative": c3d4_changes,
                "refined_c3d4_c3d10_amplification_difference_relative": element_differences,
                "maximum_secant_error_relative": max(secant_errors),
                "maximum_analytical_eigenvalue_error_relative": max(eigen_errors),
            },
            "compute_comparability": {
                "status": "comparable" if compute_comparable else "not_compute_comparable",
                "relative_node_count_difference": node_difference,
                "limit": float(config["mesh_only_pilot"]["maximum_relative_node_count_difference"]),
            },
            "mesh_results": mesh_results,
            "sources": {
                "gmsh_element_types": "https://gmsh.info/doc/texinfo/gmsh.html#MSH-file-format",
                "calculix_c3d10": "https://www.feacluster.com/CalculiX/ccx_2.18/doc/ccx/node34.html",
            },
            "repository_commit": run(["git", "rev-parse", "HEAD"], ROOT)[0].stdout.strip(),
            "worktree_dirty_during_run": bool(run(["git", "status", "--porcelain"], ROOT)[0].stdout),
        }
        (args.artifact_root / "experiment_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({
            "status": summary["status"], "hypothesis": summary["convergence_hypothesis"],
            "compute_comparability": summary["compute_comparability"],
            "summary": str(args.artifact_root / "experiment_summary.json"),
        }))
        return 0
    except Exception as error:
        args.artifact_root.mkdir(parents=True, exist_ok=True)
        (args.artifact_root / "experiment_failure.json").write_text(
            json.dumps({"status": "failed", "message": str(error), "traceback": traceback.format_exc()}, indent=2) + "\n",
            encoding="utf-8",
        )
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
