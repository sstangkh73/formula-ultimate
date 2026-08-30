#!/usr/bin/env python3
"""Run Work 049 fixed-topology end-to-end baseline acceptance."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import traceback


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.experiments.whole_vehicle_baseline import (  # noqa: E402
    WholeVehicleBaselineError,
    canonical_sha256,
    convergence_metrics,
    evaluate_baseline,
    evaluate_reference_matrix,
    validate_baseline_inputs,
)


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rejected(control_id: str, action, expected: str) -> dict:
    try:
        action()
    except (KeyError, TypeError, ValueError, WholeVehicleBaselineError) as exc:
        if expected.lower() not in str(exc).lower():
            raise
        return {"control_id": control_id, "status": "rejected_as_expected", "reason": str(exc)}
    raise WholeVehicleBaselineError(f"negative control {control_id} was admitted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=ROOT / "config/vehicle/fixed_topology_end_to_end_baseline_v1.json")
    parser.add_argument("--work048-protocol", type=Path, default=ROOT / "config/vehicle/whole_vehicle_load_cases_v1.json")
    parser.add_argument("--artifact-root", type=Path, default=ROOT / "artifacts/work049")
    args = parser.parse_args()
    args.artifact_root.mkdir(parents=True, exist_ok=True)
    stage = "work048"
    try:
        upstream = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ROOT / "scripts/run_work048.ps1")],
            cwd=ROOT, text=True, capture_output=True,
        )
        if upstream.returncode:
            raise WholeVehicleBaselineError(f"Work 048 upstream failed: {upstream.stderr.strip()}")
        work048_path = ROOT / "artifacts/work048/experiment_summary.json"
        work048 = read(work048_path)
        protocol = read(args.protocol)
        stage = "identity"
        validate_baseline_inputs(
            protocol, work048,
            load_case_protocol_sha256=sha(args.work048_protocol),
            work048_source_commit=protocol["upstream_identity"]["work048_source_commit"],
        )
        stage = "matrix"
        matrix = evaluate_reference_matrix(protocol, work048)
        convergence = convergence_metrics(protocol, matrix)
        common = {"timestep_s": 0.5, "structural_resolution_id": "bounded_reference"}
        reference = evaluate_baseline(protocol, work048, variant_id="reference", **common)
        weak = evaluate_baseline(protocol, work048, variant_id="weak_control", **common)
        disconnected = evaluate_baseline(protocol, work048, variant_id="disconnected_control", **common)
        heavy = evaluate_baseline(protocol, work048, variant_id="heavy_feasible_control", **common)
        replay = evaluate_baseline(protocol, work048, variant_id="reference", **common)
        if reference != replay:
            raise WholeVehicleBaselineError("same-input baseline replay differs")
        if reference.outcome != "finished" or heavy.outcome != "finished":
            raise WholeVehicleBaselineError("reference/heavy feasibility gate failed")
        if weak.outcome != "DNF" or disconnected.outcome != "DNF":
            raise WholeVehicleBaselineError("deliberate failure controls did not produce DNF")
        if not heavy.finish_time_s > reference.finish_time_s or not heavy.energy_used_j > reference.energy_used_j:
            raise WholeVehicleBaselineError("heavy control did not preserve expected mass penalty")
        stage = "negative_controls"
        import copy
        bad_identity = copy.deepcopy(work048); bad_identity["assembly_step_sha256"] = "0" * 64
        missing = copy.deepcopy(protocol); missing["variants"][0]["evidence"].pop()
        incomplete = copy.deepcopy(work048)
        removed_case = work048["partitions"]["training"][0]
        incomplete["results"] = [item for item in incomplete["results"] if item["case_id"] != removed_case]
        controls = [
            rejected("changed_step_identity", lambda: validate_baseline_inputs(
                protocol, bad_identity, load_case_protocol_sha256=sha(args.work048_protocol),
                work048_source_commit=protocol["upstream_identity"]["work048_source_commit"],
            ), "assembly_step"),
            rejected("missing_evidence", lambda: validate_baseline_inputs(
                missing, work048, load_case_protocol_sha256=sha(args.work048_protocol),
                work048_source_commit=protocol["upstream_identity"]["work048_source_commit"],
            ), "evidence"),
            rejected("incomplete_case_set", lambda: validate_baseline_inputs(
                protocol, incomplete, load_case_protocol_sha256=sha(args.work048_protocol),
                work048_source_commit=protocol["upstream_identity"]["work048_source_commit"],
            ), "incomplete"),
            rejected("unregistered_timestep", lambda: evaluate_baseline(
                protocol, work048, variant_id="reference", timestep_s=0.1,
                structural_resolution_id="bounded_reference",
            ), "timestep"),
        ]
        ready_matrix = [asdict(item) for item in matrix]
        summary = {
            "status": "passed",
            "claim_level": protocol["claim_level"],
            "protocol_sha256": sha(args.protocol),
            "work048_protocol_sha256": sha(args.work048_protocol),
            "upstream": {
                "assembly_step_sha256": work048["assembly_step_sha256"],
                "load_case_result_sha256": work048["replay"]["result_set_sha256"],
                "training_partition_sha256": work048["partitions"]["training_sha256"],
                "holdout_partition_sha256": work048["partitions"]["holdout_sha256"],
                "work048_process": {"exit_code": upstream.returncode, "stdout": upstream.stdout, "stderr": upstream.stderr},
            },
            "reference_matrix": ready_matrix,
            "reference": asdict(reference),
            "weak_control": asdict(weak),
            "disconnected_control": asdict(disconnected),
            "heavy_feasible_control": asdict(heavy),
            "convergence": convergence,
            "replay": {"status": "exact", "result_sha256": reference.result_sha256, "matrix_sha256": canonical_sha256(ready_matrix)},
            "negative_controls": controls,
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
            "worktree_dirty_during_run": bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout),
            "review": {
                "supporting_evidence": [
                    "one fixed candidate traversed deterministic CAD, STEP, FreeCAD, frozen load cases, failure coupling, and bounded Level 0 outcome",
                    "all seven training/holdout cases were present and structurally feasible for the reference",
                    "weak and disconnected controls produced DNF while a heavier control remained feasible with time and energy penalties",
                    "timestep and bounded capacity-resolution matrix passed its frozen gates and exact replay",
                ],
                "contradicting_evidence": [
                    "the structural resolution audit perturbs analytical capacities and is not a mesh-converged stress FEA",
                ],
                "alternative_explanations": [
                    "orchestration can be correct while local stresses or unsupported physics reverse candidate feasibility",
                ],
                "missing_evidence": [
                    "independent refined whole-vehicle stress solver, physical calibration, transient/contact/aero fidelity, and real-circuit admission",
                ],
                "confidence": "high for deterministic orchestration; low for whole-vehicle physical feasibility",
            },
        }
        write(args.artifact_root / "experiment_summary.json", summary)
        print(json.dumps({
            "status": "passed", "reference": reference.outcome, "weak": weak.outcome,
            "disconnected": disconnected.outcome, "heavy": heavy.outcome,
            "reference_time_s": reference.finish_time_s, "heavy_time_s": heavy.finish_time_s,
            "timestep_relative": convergence["finish_time_maximum_relative"],
            "structural_relative": convergence["utilization_maximum_relative"],
            "replay": "exact", "negative_controls": len(controls),
            "summary": str(args.artifact_root / "experiment_summary.json"),
        }, sort_keys=True))
        return 0
    except Exception as exc:
        write(args.artifact_root / "experiment_failure.json", {
            "status": "failed", "failed_stage": stage, "error_type": type(exc).__name__,
            "message": str(exc), "traceback": traceback.format_exc(),
        })
        print(json.dumps({"status": "failed", "stage": stage, "message": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
