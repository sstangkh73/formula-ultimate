from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import shutil
import sys
import traceback

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from formula_ultimate.structural import (  # noqa: E402
    ResponsePoint,
    TensionSpec,
    parse_msh2,
    response_is_strictly_monotonic,
    shaped_imperfect_mesh,
)
from scripts.structural.run_nonlinear_imperfect_column_acceptance import (  # noqa: E402
    geometry_text,
    run,
    sha256,
    solve_case,
)


def relative_difference(first: float, second: float) -> float:
    denominator = 0.5 * (abs(first) + abs(second))
    if denominator == 0.0:
        return 0.0
    return abs(first - second) / denominator


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--gmsh", type=Path, required=True)
    parser.add_argument("--ccx", type=Path, required=True)
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        geometry, material = config["geometry"], config["material"]
        tolerance = config["tolerances"]
        prior_path = ROOT / "artifacts" / "work037" / "experiment_summary.json"
        prior = json.loads(prior_path.read_text(encoding="utf-8"))
        if prior.get("status") != "passed":
            raise RuntimeError("Work 037 evidence has not passed")
        ancestry = run(["git", "merge-base", "--is-ancestor", config["work037_source_commit"], "HEAD"], ROOT)
        if ancestry.returncode != 0:
            raise RuntimeError("declared Work 037 source commit is not an ancestor of HEAD")
        prior_by_mesh = {item["mesh_id"]: item for item in prior["mesh_results"]}
        for level in config["mesh_levels"]:
            recorded = prior_by_mesh.get(level["mesh_id"])
            if recorded is None or not math.isclose(
                float(recorded["critical_load_n"]), float(level["work037_critical_load_n"]), rel_tol=1e-12
            ):
                raise RuntimeError(f"Work 037 evidence mismatch for {level['mesh_id']}")

        if args.artifact_root.exists():
            shutil.rmtree(args.artifact_root)
        args.artifact_root.mkdir(parents=True)
        fine_critical_load = float(config["mesh_levels"][-1]["work037_critical_load_n"])
        fractions = [float(value) for value in config["absolute_load_fractions_of_fine_pcr"]]
        amplitude = float(config["tip_amplitude_m"])
        shapes = [str(value) for value in config["imperfection_shapes"]]
        cases: list[dict[str, object]] = []
        mesh_evidence: list[dict[str, object]] = []

        for level in config["mesh_levels"]:
            mesh_dir = args.artifact_root / level["mesh_id"]
            mesh_dir.mkdir()
            geo_path, mesh_path = mesh_dir / "column.geo", mesh_dir / "column.msh"
            geo_path.write_text(
                geometry_text(
                    float(geometry["length_m"]), float(geometry["width_m"]),
                    float(geometry["height_m"]), float(level["characteristic_size_m"]),
                ), encoding="ascii"
            )
            meshed = run([str(args.gmsh), str(geo_path), "-3", "-format", "msh2", "-o", str(mesh_path)], mesh_dir)
            (mesh_dir / "gmsh_stdout.txt").write_text(meshed.stdout, encoding="utf-8")
            if meshed.returncode != 0:
                raise RuntimeError(f"Gmsh failed for {level['mesh_id']}: {meshed.stdout[-1000:]}")
            base_mesh = parse_msh2(mesh_path)
            mesh_evidence.append({
                "mesh_id": level["mesh_id"], "nodes": len(base_mesh.nodes),
                "tetrahedra": len(base_mesh.tetrahedra), "sha256": sha256(mesh_path),
                "work037_critical_load_n": float(level["work037_critical_load_n"]),
            })
            for shape in shapes:
                changed = shaped_imperfect_mesh(
                    base_mesh, length_m=float(geometry["length_m"]),
                    tip_amplitude_m=amplitude, shape_id=shape,
                )
                for fraction in fractions:
                    load = fraction * fine_critical_load
                    if load >= float(level["work037_critical_load_n"]):
                        raise RuntimeError(f"declared load is not subcritical for {level['mesh_id']}")
                    spec = TensionSpec(
                        config["protocol_id"], "work039", f"{level['mesh_id']}_{shape}",
                        "precritical robustness study only", float(geometry["length_m"]),
                        float(geometry["width_m"]), float(geometry["height_m"]),
                        material["material_id"], float(material["youngs_modulus_pa"]),
                        float(material["poisson_ratio"]), float(material["density_kg_per_m3"]),
                        material["provenance"], -load,
                    )
                    case = solve_case(
                        case_dir=mesh_dir / f"{shape}_p{round(100 * fraction):02d}",
                        ccx=args.ccx, spec=spec, mesh=changed,
                        tolerance_m=float(tolerance["boundary_coordinate_absolute_m"]),
                        amplitude_m=amplitude, critical_load_n=float(level["work037_critical_load_n"]),
                        load_fraction=fraction, nlgeom=True,
                    )
                    case["mesh_id"] = level["mesh_id"]
                    case["imperfection_shape"] = shape
                    case["absolute_load_fraction_of_fine_pcr"] = case.pop("load_fraction")
                    cases.append(case)

        if any(float(case["reaction_error_relative"]) > float(tolerance["reaction_error_relative"]) for case in cases):
            raise RuntimeError("reaction-closure execution gate failed")
        for level in config["mesh_levels"]:
            for shape in shapes:
                points = [
                    ResponsePoint(
                        float(case["absolute_load_fraction_of_fine_pcr"]),
                        float(case["total_tip_offset_m"]), float(case["measured_amplification"]),
                        float(case["secant_reference_amplification"]),
                    )
                    for case in cases
                    if case["mesh_id"] == level["mesh_id"] and case["imperfection_shape"] == shape
                ]
                if not response_is_strictly_monotonic(points):
                    raise RuntimeError(f"non-monotonic execution evidence for {level['mesh_id']} {shape}")

        eigenmode_errors = [
            float(case["secant_reference_error_relative"])
            for case in cases if case["imperfection_shape"] == "cantilever_eigenmode"
        ]
        last_two_changes: dict[str, float] = {}
        shape_differences: dict[str, float] = {}
        medium_id, fine_id = config["mesh_levels"][-2]["mesh_id"], config["mesh_levels"][-1]["mesh_id"]
        for fraction in fractions:
            def value(mesh_id: str, shape: str) -> float:
                matches = [
                    float(case["measured_amplification"]) for case in cases
                    if case["mesh_id"] == mesh_id and case["imperfection_shape"] == shape
                    and math.isclose(float(case["absolute_load_fraction_of_fine_pcr"]), fraction)
                ]
                if len(matches) != 1:
                    raise RuntimeError("case identity is missing or duplicated")
                return matches[0]
            last_two_changes[str(fraction)] = relative_difference(
                value(medium_id, "cantilever_eigenmode"), value(fine_id, "cantilever_eigenmode")
            )
            shape_differences[str(fraction)] = relative_difference(
                value(fine_id, "cantilever_eigenmode"), value(fine_id, "smoothstep_cubic")
            )

        numerical_supported = (
            max(eigenmode_errors) <= float(tolerance["eigenmode_secant_error_relative"])
            and max(last_two_changes.values()) <= float(tolerance["last_two_mesh_change_relative"])
        )
        robustness_supported = max(shape_differences.values()) <= float(tolerance["fine_mesh_shape_difference_relative"])
        summary = {
            "status": "passed",
            "claim_level": "precritical numerical and imperfection-shape sensitivity evidence only",
            "execution_gates": {"all_cases_converged": True, "reaction_closure": True, "monotonic_response": True},
            "hypotheses": {
                "eigenmode_mesh_convergence": {
                    "status": "supported" if numerical_supported else "rejected",
                    "maximum_secant_error_relative": max(eigenmode_errors),
                    "last_two_mesh_change_relative": last_two_changes,
                    "limits": {
                        "secant_error_relative": float(tolerance["eigenmode_secant_error_relative"]),
                        "last_two_mesh_change_relative": float(tolerance["last_two_mesh_change_relative"]),
                    },
                },
                "fine_mesh_shape_robustness": {
                    "status": "supported" if robustness_supported else "rejected",
                    "shape_difference_relative": shape_differences,
                    "limit": float(tolerance["fine_mesh_shape_difference_relative"]),
                },
            },
            "mesh_evidence": mesh_evidence,
            "cases": cases,
            "repository_commit": run(["git", "rev-parse", "HEAD"], ROOT).stdout.strip(),
            "worktree_dirty_during_run": bool(run(["git", "status", "--porcelain"], ROOT).stdout),
        }
        (args.artifact_root / "experiment_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({
            "status": summary["status"], "cases": len(cases), "hypotheses": summary["hypotheses"],
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
