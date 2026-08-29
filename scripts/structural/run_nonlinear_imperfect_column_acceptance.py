from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import traceback

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.structural import (  # noqa: E402
    ResponsePoint,
    TensionSpec,
    build_calculix_input,
    imperfect_mesh,
    parse_calculix_dat,
    parse_msh2,
    response_is_strictly_monotonic,
    secant_amplification,
)


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def geometry_text(length_m: float, width_m: float, height_m: float, mesh_size_m: float) -> str:
    return "\n".join((
        'SetFactory("OpenCASCADE");',
        f"Box(1)={{0,0,0,{length_m},{width_m},{height_m}}};",
        f"Mesh.CharacteristicLengthMin={mesh_size_m};",
        f"Mesh.CharacteristicLengthMax={mesh_size_m};",
        "Mesh.ElementOrder=1;",
        "Mesh.MshFileVersion=2.2;",
        "Mesh.Binary=0;",
        "Mesh.SaveAll=1;",
        "Physical Volume(1)={1};",
        "",
    ))


def nonlinear_deck(static_deck: str) -> str:
    marker = "*STEP\n*STATIC\n*CLOAD"
    if static_deck.count(marker) != 1:
        raise ValueError("static deck step marker is missing or ambiguous")
    return static_deck.replace(marker, "*STEP, NLGEOM\n*STATIC\n1., 1.\n*CLOAD")


def single_increment_linear_deck(static_deck: str) -> str:
    marker = "*STEP\n*STATIC\n*CLOAD"
    if static_deck.count(marker) != 1:
        raise ValueError("static deck step marker is missing or ambiguous")
    return static_deck.replace(marker, "*STEP\n*STATIC\n1., 1.\n*CLOAD")


def von_mises(tensor: tuple[float, float, float, float, float, float]) -> float:
    sx, sy, sz, txy, txz, tyz = tensor
    return math.sqrt(
        0.5 * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2)
        + 3.0 * (txy * txy + txz * txz + tyz * tyz)
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def solve_case(
    *,
    case_dir: Path,
    ccx: Path,
    spec: TensionSpec,
    mesh,
    tolerance_m: float,
    amplitude_m: float,
    critical_load_n: float,
    load_fraction: float,
    nlgeom: bool,
) -> dict[str, object]:
    case_dir.mkdir(parents=True)
    static_deck, nodal_loads, _, loaded = build_calculix_input(
        spec=spec, mesh=mesh, boundary_tolerance_m=tolerance_m
    )
    deck = nonlinear_deck(static_deck) if nlgeom else single_increment_linear_deck(static_deck)
    # CalculiX 2.22 rejects lower-case scientific notation on *NODE cards.
    deck = deck.replace("e-", "E-").replace("e+", "E+")
    input_path = case_dir / "column.inp"
    input_path.write_text(deck, encoding="ascii")
    solved = run([str(ccx), "column"], case_dir)
    (case_dir / "solver_stdout.txt").write_text(solved.stdout, encoding="utf-8")
    (case_dir / "solver_stderr.txt").write_text(solved.stderr, encoding="utf-8")
    if solved.returncode != 0:
        raise RuntimeError(f"CalculiX failed in {case_dir.name}: {solved.stdout[-1000:]}")
    if nlgeom and "nonlinear geometric" not in solved.stdout.lower():
        raise RuntimeError(f"NLGEOM confirmation is missing in {case_dir.name}")
    data = parse_calculix_dat(case_dir / "column.dat")
    weights = {node: abs(nodal_loads[node]) for node in loaded}
    weight_sum = math.fsum(weights.values())
    tip_ux = math.fsum(weights[node] * data["displacements"][node][0] for node in loaded) / weight_sum
    tip_uz = math.fsum(weights[node] * data["displacements"][node][2] for node in loaded) / weight_sum
    reaction_error = abs(data["total_reaction"][0] - abs(spec.resultant_force_n)) / abs(spec.resultant_force_n)
    total_offset = amplitude_m + tip_uz
    amplification = total_offset / amplitude_m if amplitude_m > 0.0 else None
    reference = secant_amplification(abs(spec.resultant_force_n), critical_load_n) if amplitude_m > 0.0 else None
    reference_error = abs(amplification - reference) / reference if amplitude_m > 0.0 else None
    evidence_paths = [input_path, case_dir / "column.dat", case_dir / "column.frd", case_dir / "solver_stdout.txt"]
    return {
        "load_fraction": load_fraction,
        "load_n": abs(spec.resultant_force_n),
        "initial_tip_imperfection_m": amplitude_m,
        "incremental_tip_lateral_displacement_m": tip_uz,
        "total_tip_offset_m": total_offset,
        "tip_axial_displacement_m": tip_ux,
        "measured_amplification": amplification,
        "secant_reference_amplification": reference,
        "secant_reference_error_relative": reference_error,
        "reaction_error_relative": reaction_error,
        "maximum_von_mises_stress_pa": max(von_mises(value) for value in data["stress_tensor_by_element_pa"].values()),
        "nlgeom": nlgeom,
        "evidence_sha256": {path.name: sha256(path) for path in evidence_paths},
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
        geometry = config["geometry"]
        material = config["material"]
        mesh_config = config["mesh"]
        tolerances = config["tolerances"]
        critical_load = float(mesh_config["work037_critical_load_n"])

        prior_path = ROOT / "artifacts" / "work037" / "experiment_summary.json"
        prior = json.loads(prior_path.read_text(encoding="utf-8"))
        matching = [item for item in prior["mesh_results"] if item["mesh_id"] == mesh_config["mesh_id"]]
        if prior.get("status") != "passed" or len(matching) != 1 or not math.isclose(
            matching[0]["critical_load_n"], critical_load, rel_tol=1e-12
        ):
            raise RuntimeError("Work 037 matched-mesh critical-load evidence is missing or inconsistent")
        ancestry = run(
            ["git", "merge-base", "--is-ancestor", mesh_config["work037_source_commit"], "HEAD"], ROOT
        )
        if ancestry.returncode != 0:
            raise RuntimeError("declared Work 037 source commit is not an ancestor of HEAD")

        if args.artifact_root.exists():
            shutil.rmtree(args.artifact_root)
        args.artifact_root.mkdir(parents=True)
        geo_path = args.artifact_root / "column.geo"
        mesh_path = args.artifact_root / "column.msh"
        geo_path.write_text(
            geometry_text(
                float(geometry["length_m"]),
                float(geometry["width_m"]),
                float(geometry["height_m"]),
                float(mesh_config["characteristic_size_m"]),
            ),
            encoding="ascii",
        )
        meshed = run([str(args.gmsh), str(geo_path), "-3", "-format", "msh2", "-o", str(mesh_path)], args.artifact_root)
        (args.artifact_root / "gmsh_stdout.txt").write_text(meshed.stdout, encoding="utf-8")
        if meshed.returncode != 0:
            raise RuntimeError(f"Gmsh failed: {meshed.stdout[-1000:]}")
        base_mesh = parse_msh2(mesh_path)

        amplitudes = [float(value) for value in config["imperfection_tip_amplitudes_m"]]
        fractions = [float(value) for value in config["load_fractions_of_mesh_pcr"]]
        cases: list[dict[str, object]] = []
        for amplitude_index, amplitude in enumerate(amplitudes):
            mesh = imperfect_mesh(base_mesh, length_m=float(geometry["length_m"]), tip_amplitude_m=amplitude)
            for fraction in fractions:
                load = fraction * critical_load
                spec = TensionSpec(
                    config["protocol_id"],
                    "work038",
                    "cantilever_imperfect_column",
                    "precritical geometric-nonlinearity only",
                    float(geometry["length_m"]),
                    float(geometry["width_m"]),
                    float(geometry["height_m"]),
                    material["material_id"],
                    float(material["youngs_modulus_pa"]),
                    float(material["poisson_ratio"]),
                    float(material["density_kg_per_m3"]),
                    material["provenance"],
                    -load,
                )
                case = solve_case(
                    case_dir=args.artifact_root / f"e{amplitude_index + 1}_p{round(100 * fraction):02d}",
                    ccx=args.ccx,
                    spec=spec,
                    mesh=mesh,
                    tolerance_m=float(tolerances["boundary_coordinate_absolute_m"]),
                    amplitude_m=amplitude,
                    critical_load_n=critical_load,
                    load_fraction=fraction,
                    nlgeom=True,
                )
                cases.append(case)

        reaction_limit = float(tolerances["reaction_error_relative"])
        reference_limit = float(tolerances["secant_reference_error_relative"])
        if any(float(case["reaction_error_relative"]) > reaction_limit for case in cases):
            raise RuntimeError("reaction-closure gate failed")
        if any(float(case["secant_reference_error_relative"]) > reference_limit for case in cases):
            raise RuntimeError("secant-reference gate failed")
        for amplitude in amplitudes:
            points = [
                ResponsePoint(
                    float(case["load_fraction"]),
                    float(case["total_tip_offset_m"]),
                    float(case["measured_amplification"]),
                    float(case["secant_reference_amplification"]),
                )
                for case in cases
                if math.isclose(float(case["initial_tip_imperfection_m"]), amplitude)
            ]
            if not response_is_strictly_monotonic(points):
                raise RuntimeError(f"non-monotonic nonlinear response for imperfection {amplitude}")
        cross_amplitude_spread: dict[str, float] = {}
        for fraction in fractions:
            values = [float(case["measured_amplification"]) for case in cases if math.isclose(float(case["load_fraction"]), fraction)]
            spread = (max(values) - min(values)) / (math.fsum(values) / len(values))
            cross_amplitude_spread[str(fraction)] = spread
            if spread > float(tolerances["cross_amplitude_spread_relative"]):
                raise RuntimeError(f"cross-amplitude consistency gate failed at {fraction}: {spread}")

        highest_fraction = max(fractions)
        perfect_spec = TensionSpec(
            config["protocol_id"], "work038", "perfect_control", "negative control",
            float(geometry["length_m"]), float(geometry["width_m"]), float(geometry["height_m"]),
            material["material_id"], float(material["youngs_modulus_pa"]), float(material["poisson_ratio"]),
            float(material["density_kg_per_m3"]), material["provenance"], -highest_fraction * critical_load,
        )
        perfect = solve_case(
            case_dir=args.artifact_root / "control_perfect_nlgeom", ccx=args.ccx, spec=perfect_spec,
            mesh=base_mesh, tolerance_m=float(tolerances["boundary_coordinate_absolute_m"]),
            amplitude_m=0.0, critical_load_n=critical_load, load_fraction=highest_fraction, nlgeom=True,
        )
        if abs(float(perfect["incremental_tip_lateral_displacement_m"])) > float(tolerances["perfect_control_lateral_displacement_m"]):
            raise RuntimeError("perfect symmetric control invented excessive lateral motion")

        control_amplitude = amplitudes[0]
        linear = solve_case(
            case_dir=args.artifact_root / "control_imperfect_linear", ccx=args.ccx, spec=perfect_spec,
            mesh=imperfect_mesh(base_mesh, length_m=float(geometry["length_m"]), tip_amplitude_m=control_amplitude),
            tolerance_m=float(tolerances["boundary_coordinate_absolute_m"]), amplitude_m=control_amplitude,
            critical_load_n=critical_load, load_fraction=highest_fraction, nlgeom=False,
        )
        if float(linear["secant_reference_error_relative"]) < float(tolerances["linear_control_minimum_secant_error_relative"]):
            raise RuntimeError("geometrically linear negative control unexpectedly reproduced secant amplification")

        euler_inertia = float(geometry["width_m"]) * float(geometry["height_m"]) ** 3 / 12.0
        euler_load = math.pi**2 * float(material["youngs_modulus_pa"]) * euler_inertia / (
            float(geometry["effective_length_factor"]) * float(geometry["length_m"])
        ) ** 2
        summary = {
            "status": "passed",
            "claim_level": "precritical geometric-nonlinearity and imperfection sensitivity only",
            "mesh": {"nodes": len(base_mesh.nodes), "tetrahedra": len(base_mesh.tetrahedra), "sha256": sha256(mesh_path)},
            "work037_mesh_critical_load_n": critical_load,
            "analytical_euler_critical_load_n": euler_load,
            "cases": cases,
            "cross_amplitude_spread_relative": cross_amplitude_spread,
            "negative_controls": {"perfect_symmetric_nlgeom": perfect, "imperfect_geometrically_linear": linear},
            "tools": {"gmsh": str(args.gmsh), "ccx": str(args.ccx)},
            "repository_commit": run(["git", "rev-parse", "HEAD"], ROOT).stdout.strip(),
            "worktree_dirty_during_run": bool(run(["git", "status", "--porcelain"], ROOT).stdout),
        }
        (args.artifact_root / "experiment_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary))
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
