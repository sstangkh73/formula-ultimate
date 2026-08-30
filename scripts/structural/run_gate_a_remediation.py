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
    classify_boundary_comparison,
    evaluate_c3d10_refinement,
    support_topology_signature,
)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path) -> dict[str, Any]:
    started = time.time_ns()
    monotonic = time.perf_counter()
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    return {
        "command": command,
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "started_time_ns": started,
        "wall_time_s": time.perf_counter() - monotonic,
    }


def norm(values: list[float]) -> float:
    return math.sqrt(math.fsum(float(value) ** 2 for value in values))


def relative(first: float, second: float) -> float:
    scale = 0.5 * (abs(first) + abs(second))
    return abs(first - second) / scale if scale else 0.0


def rejected(control_id: str, action: Any, expected: str) -> dict[str, str]:
    try:
        action()
    except StructuralEvidenceError as exc:
        if expected not in str(exc):
            raise StructuralEvidenceError(f"{control_id} rejected for wrong reason: {exc}") from exc
        return {"control_id": control_id, "status": "rejected_as_expected", "reason": str(exc)}
    raise StructuralEvidenceError(f"negative control {control_id} was admitted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--gmsh", type=Path, required=True)
    parser.add_argument("--ccx", type=Path, required=True)
    parser.add_argument("--cadquery-python", type=Path, required=True)
    parser.add_argument("--freecad-python", type=Path, required=True)
    args = parser.parse_args()
    processes: list[dict[str, Any]] = []
    stage = "configuration"
    try:
        payload = json.loads(args.config.read_text(encoding="utf-8"))
        if payload.get("protocol_id") != "gate_a_remediation_v1":
            raise StructuralEvidenceError("unexpected Work 051 protocol identity")
        for executable in (args.gmsh, args.ccx, args.cadquery_python, args.freecad_python):
            if not executable.is_file():
                raise StructuralEvidenceError(f"required executable is missing: {executable}")
        if args.artifact_root.exists():
            shutil.rmtree(args.artifact_root)
        args.artifact_root.mkdir(parents=True)

        element_config = payload["element_remediation"]
        work041_source = ROOT / element_config["source_config"]
        work041 = json.loads(work041_source.read_text(encoding="utf-8"))
        existing_ids = {item["mesh_id"] for item in work041["mesh_cases"]}
        for item in element_config["additional_mesh_cases"]:
            if item["mesh_id"] in existing_ids:
                raise StructuralEvidenceError("additional C3D10 mesh identity is duplicated")
            work041["mesh_cases"].append(item)
            existing_ids.add(item["mesh_id"])
        work041_config = args.artifact_root / "work041_remediation_config.json"
        write_json(work041_config, work041)
        element_root = args.artifact_root / "element"
        stage = "element_remediation"
        process = run([
            sys.executable,
            str(ROOT / "scripts/structural/run_near_critical_element_verification.py"),
            "--config", str(work041_config),
            "--artifact-root", str(element_root),
            "--gmsh", str(args.gmsh),
            "--ccx", str(args.ccx),
        ], ROOT)
        process["stage"] = stage
        processes.append(process)
        if process["exit_code"] != 0:
            raise StructuralEvidenceError(f"element remediation runner failed: {process['stderr'][-2000:]}")
        element_summary_path = element_root / "experiment_summary.json"
        element_summary = json.loads(element_summary_path.read_text(encoding="utf-8"))
        element_decision = evaluate_c3d10_refinement(
            element_summary["mesh_results"],
            ordered_mesh_ids=tuple(element_config["refinement_mesh_ids"]),
            maximum_last_two_change_relative=float(element_config["maximum_last_two_amplification_change_relative"]),
            maximum_secant_error_relative=float(element_config["maximum_secant_error_relative"]),
            maximum_eigenvalue_error_relative=float(element_config["maximum_eigenvalue_error_relative"]),
        )
        element_decision["retained_work041_cross_family_status"] = element_summary["convergence_hypothesis"]["status"]
        element_decision["excluded_route"] = element_config["excluded_route"]

        boundary_config = payload["boundary_remediation"]
        work045_source = ROOT / boundary_config["source_config"]
        work045_reference = json.loads(work045_source.read_text(encoding="utf-8"))
        allowed_supports = tuple(
            item["interface_id"] for item in work045_reference["interfaces"] if item["role"] == "support"
        )
        reference_supports = tuple(boundary_config["reference_supports"])
        equivalent_supports = tuple(boundary_config["equivalent_encoding_supports"])
        mutation_supports = tuple(boundary_config["topology_mutation_supports"])
        if tuple(work045_reference["support_policies"]["baseline"]) != reference_supports:
            raise StructuralEvidenceError("Work 051 reference support identity differs from Work 045")
        if tuple(work045_reference["support_policies"]["sensitivity"]) != mutation_supports:
            raise StructuralEvidenceError("Work 051 topology mutation differs from retained Work 045 evidence")

        boundary_summaries: dict[str, dict[str, Any]] = {}
        for identity, supports in (("reference", reference_supports), ("equivalent_encoding", equivalent_supports)):
            variant = json.loads(json.dumps(work045_reference))
            variant["support_policies"]["baseline"] = list(supports)
            variant_path = args.artifact_root / f"work045_{identity}_config.json"
            write_json(variant_path, variant)
            variant_root = args.artifact_root / f"boundary_{identity}"
            stage = f"boundary_{identity}"
            process = run([
                sys.executable,
                str(ROOT / "scripts/structural/run_loaded_interface_acceptance.py"),
                "--config", str(variant_path),
                "--artifact-root", str(variant_root),
                "--cadquery-python", str(args.cadquery_python),
                "--freecad-python", str(args.freecad_python),
                "--gmsh", str(args.gmsh),
                "--ccx", str(args.ccx),
            ], ROOT)
            process["stage"] = stage
            processes.append(process)
            if process["exit_code"] != 0:
                raise StructuralEvidenceError(f"{identity} boundary runner failed: {process['stderr'][-2000:]}")
            boundary_summaries[identity] = json.loads(
                (variant_root / "experiment_summary.json").read_text(encoding="utf-8")
            )

        reference = boundary_summaries["reference"]
        equivalent = boundary_summaries["equivalent_encoding"]
        reference_metrics = reference["mesh_results"][-1]["metrics"]
        equivalent_metrics = equivalent["mesh_results"][-1]["metrics"]
        mutation_metrics = reference["boundary_sensitivity"]["fine_sensitivity_result"]["metrics"]
        model_id = str(boundary_config["boundary_model_id"])
        equivalent_decision = classify_boundary_comparison(
            reference_supports=reference_supports,
            candidate_supports=equivalent_supports,
            allowed_support_ids=allowed_supports,
            reference_model_id=model_id,
            candidate_model_id=model_id,
            reference_compliance=float(reference_metrics["compliance_m_per_n"]),
            candidate_compliance=float(equivalent_metrics["compliance_m_per_n"]),
            maximum_equivalent_change_relative=float(boundary_config["maximum_equivalent_compliance_change_relative"]),
        )
        resultant_change = relative(
            norm(reference_metrics["reaction_force_n"]),
            norm(equivalent_metrics["reaction_force_n"]),
        )
        equivalent_decision["reaction_resultant_change_relative"] = resultant_change
        equivalent_decision["reaction_resultant_limit"] = float(
            boundary_config["maximum_equivalent_resultant_change_relative"]
        )
        if resultant_change > equivalent_decision["reaction_resultant_limit"]:
            equivalent_decision["status"] = "rejected"
        topology_mutation = classify_boundary_comparison(
            reference_supports=reference_supports,
            candidate_supports=mutation_supports,
            allowed_support_ids=allowed_supports,
            reference_model_id=model_id,
            candidate_model_id=model_id,
            reference_compliance=float(reference_metrics["compliance_m_per_n"]),
            candidate_compliance=float(mutation_metrics["compliance_m_per_n"]),
            maximum_equivalent_change_relative=float(boundary_config["maximum_equivalent_compliance_change_relative"]),
        )
        boundary_decision = {
            "status": "narrowly_bounded" if equivalent_decision["status"] == "supported" and topology_mutation["status"] == "topology_mutation" else "blocked",
            "boundary_model_id": model_id,
            "reference_topology_signature": support_topology_signature(reference_supports, allowed_support_ids=allowed_supports),
            "equivalent_topology_signature": support_topology_signature(equivalent_supports, allowed_support_ids=allowed_supports),
            "equivalent_representation": equivalent_decision,
            "retained_topology_mutation": topology_mutation,
            "retained_work045_transferability_status": reference["boundary_sensitivity"]["status"],
            "reference_step_sha256": reference["interface_identity"]["step_sha256"],
            "equivalent_step_sha256": equivalent["interface_identity"]["step_sha256"],
        }

        controls = [
            rejected(
                "duplicate_support_identity",
                lambda: support_topology_signature((allowed_supports[0], allowed_supports[0]), allowed_support_ids=allowed_supports),
                "duplicated",
            ),
            rejected(
                "undeclared_support_identity",
                lambda: support_topology_signature(("undeclared_support",), allowed_support_ids=allowed_supports),
                "undeclared",
            ),
            rejected(
                "non_c3d10_refinement_evidence",
                lambda: evaluate_c3d10_refinement(
                    [{**element_summary["mesh_results"][0], "mesh_id": mesh_id} for mesh_id in element_config["refinement_mesh_ids"]],
                    ordered_mesh_ids=tuple(element_config["refinement_mesh_ids"]),
                    maximum_last_two_change_relative=0.05,
                    maximum_secant_error_relative=0.05,
                    maximum_eigenvalue_error_relative=0.05,
                ),
                "non-C3D10",
            ),
        ]
        bounded = element_decision["status"] == "supported" and boundary_decision["status"] == "narrowly_bounded"
        summary = {
            "status": "passed",
            "claim_level": payload["claim_level"],
            "gate_a_decision": "narrowly_bounded" if bounded else "blocked",
            "work046_may_start_bounded_policy_experiment": bounded,
            "element_remediation": element_decision,
            "boundary_remediation": boundary_decision,
            "negative_controls": controls,
            "source_evidence": {
                "work041_summary_sha256": sha256(element_summary_path),
                "work045_reference_summary_sha256": sha256(args.artifact_root / "boundary_reference/experiment_summary.json"),
                "work045_equivalent_summary_sha256": sha256(args.artifact_root / "boundary_equivalent_encoding/experiment_summary.json"),
            },
            "process_evidence": processes,
            "config_sha256": sha256(args.config),
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
            "worktree_dirty_during_run": bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout),
            "review": {
                "supporting_evidence": [
                    "the preregistered C3D10 refinement series was evaluated without averaging element families",
                    "equivalent two-support encodings retained one topology signature and were compared solver-to-solver",
                    "the retained one-support case was classified as a topology deletion rather than relabeled as transferability support",
                ],
                "contradicting_evidence": [
                    "Work 041 retains the rejected C3D4/C3D10 near-critical comparison",
                    "Work 045 retains the 299 percent one-support compliance change",
                ],
                "alternative_explanations": [
                    "C3D4 interpolation error grows near the critical load",
                    "support deletion changes the physical load-path topology rather than only its encoding",
                ],
                "missing_evidence": [
                    "post-critical continuation and an independent solver",
                    "joint contact, preload, friction, fastener flexibility, and physical calibration",
                ],
                "confidence": "high for the narrow numerical domain; low outside the exact element and boundary identities",
            },
        }
        write_json(args.artifact_root / "experiment_summary.json", summary)
        print(json.dumps({
            "status": summary["status"],
            "gate_a_decision": summary["gate_a_decision"],
            "work046_may_start_bounded_policy_experiment": bounded,
            "element_status": element_decision["status"],
            "boundary_status": boundary_decision["status"],
            "summary": str(args.artifact_root / "experiment_summary.json"),
        }, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {
            "status": "failed",
            "failed_stage": stage,
            "error_type": type(exc).__name__,
            "message": str(exc),
            "process_evidence": processes,
            "traceback": traceback.format_exc(),
        }
        write_json(args.artifact_root / "experiment_failure.json", failure)
        print(json.dumps(failure, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
