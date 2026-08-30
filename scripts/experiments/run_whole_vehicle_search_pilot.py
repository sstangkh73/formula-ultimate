#!/usr/bin/env python3
"""Run Work 050 equal-budget search pilot and readiness review."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, replace
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time
import traceback
import tracemalloc


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.experiments.whole_vehicle_search import (  # noqa: E402
    DesignSearchAgentV0,
    WholeVehicleSearchError,
    canonical_sha256,
    evaluate_candidate,
    promote_candidates,
    readiness_decision,
    run_search_pilot,
    validate_search_protocol,
)


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rejected(control_id: str, action, expected: str) -> dict:
    try:
        action()
    except (KeyError, TypeError, ValueError, WholeVehicleSearchError) as exc:
        if expected.lower() not in str(exc).lower():
            raise
        return {"control_id": control_id, "status": "rejected_as_expected", "reason": str(exc)}
    raise WholeVehicleSearchError(f"exploit control {control_id} was admitted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=ROOT / "config/experiments/bounded_whole_vehicle_search_pilot_v1.json")
    parser.add_argument("--baseline-protocol", type=Path, default=ROOT / "config/vehicle/fixed_topology_end_to_end_baseline_v1.json")
    parser.add_argument("--assembly", type=Path, default=ROOT / "config/vehicle/topology_neutral_vehicle_v1.json")
    parser.add_argument("--artifact-root", type=Path, default=ROOT / "artifacts/work050")
    args = parser.parse_args()
    args.artifact_root.mkdir(parents=True, exist_ok=True)
    stage = "work049"
    try:
        upstream = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ROOT / "scripts/run_work049.ps1")],
            cwd=ROOT, text=True, capture_output=True,
        )
        if upstream.returncode:
            raise WholeVehicleSearchError(f"Work 049 upstream failed: {upstream.stderr.strip()}")
        protocol = read(args.protocol)
        baseline_protocol = read(args.baseline_protocol)
        base_assembly = read(args.assembly)
        baseline = read(ROOT / "artifacts/work049/experiment_summary.json")
        work048 = read(ROOT / "artifacts/work048/experiment_summary.json")
        stage = "identity"
        evaluator_sha = validate_search_protocol(
            protocol, baseline, baseline_protocol_sha256=sha(args.baseline_protocol),
        )
        stage = "pilot"
        tracemalloc.start()
        started = time.perf_counter()
        records = run_search_pilot(protocol, base_assembly, work048, baseline_protocol, evaluator_sha)
        wall_time = time.perf_counter() - started
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        stage = "replay"
        replay = run_search_pilot(protocol, base_assembly, work048, baseline_protocol, evaluator_sha)
        exact = records == replay
        if not exact:
            raise WholeVehicleSearchError("same-seed pilot replay differs")
        stage = "promotion"
        promotions = promote_candidates(protocol, records, base_assembly, work048, baseline_protocol, evaluator_sha)
        stage = "exploit_controls"
        agent = DesignSearchAgentV0(protocol, "RANDOM", 101)
        candidate = agent.propose(0)
        hidden = replace(candidate, variables=candidate.variables + (("hidden_tolerance", 0.0),))
        nan_values = list(candidate.variables); nan_values[0] = (nan_values[0][0], float("nan"))
        out_values = list(candidate.variables); out_values[0] = (out_values[0][0], -1.0)
        changed_seed = json.loads(json.dumps(protocol)); changed_seed["seeds"] = [101, 202, 304]
        controls = [
            rejected("hidden_evaluator_mutation", lambda: evaluate_candidate(
                protocol, hidden, base_assembly, work048, baseline_protocol, evaluator_sha, partition="training",
            ), "opportunity"),
            rejected("nan_variable", lambda: evaluate_candidate(
                protocol, replace(candidate, variables=tuple(nan_values)), base_assembly, work048,
                baseline_protocol, evaluator_sha, partition="training",
            ), "outside"),
            rejected("out_of_bounds", lambda: evaluate_candidate(
                protocol, replace(candidate, variables=tuple(out_values)), base_assembly, work048,
                baseline_protocol, evaluator_sha, partition="training",
            ), "outside"),
            rejected("changed_seed", lambda: validate_search_protocol(
                changed_seed, baseline, baseline_protocol_sha256=sha(args.baseline_protocol),
            ), "seeds"),
        ]
        skipped_agent = DesignSearchAgentV0(protocol, "RANDOM", 101)
        skipped = skipped_agent.propose(1)
        skipped_result = evaluate_candidate(protocol, skipped, base_assembly, work048, baseline_protocol, evaluator_sha, partition="training")
        controls.append(rejected("skipped_attempt", lambda: skipped_agent.observe(skipped_result), "append-only"))
        stage = "review"
        review = readiness_decision(protocol, records, promotions, exact_replay=exact, exploit_controls_passed=len(controls) == 5)
        if review["decision"] != "not_ready" or tuple(review["blockers"]) != ("independent_refined_evaluation",):
            raise WholeVehicleSearchError("readiness decision did not retain the refined-evaluator blocker")
        ready_records = [asdict(item) for item in records]
        ready_replay = [asdict(item) for item in replay]
        ready_promotions = [asdict(item) for item in promotions]
        result_ledger = args.artifact_root / "result_ledger.jsonl"
        replay_ledger = args.artifact_root / "replay_result_ledger.jsonl"
        budget_ledger = args.artifact_root / "budget_ledger.jsonl"
        write_jsonl(result_ledger, ready_records)
        write_jsonl(replay_ledger, ready_replay)
        write_jsonl(budget_ledger, ({
            "attempt_index": item.candidate.attempt_index,
            "candidate_id": item.candidate.candidate_id,
            "treatment": item.candidate.treatment,
            "seed": item.candidate.seed,
            "consumed_attempts": 1,
            "status": item.status,
            "failure_code": item.failure_code,
        } for item in records))
        summaries = {}
        for treatment in protocol["treatments"]:
            subset = [item for item in records if item.candidate.treatment == treatment]
            feasible = [item for item in subset if item.status == "feasible"]
            failures = Counter(item.failure_code or "none" for item in subset)
            summaries[treatment] = {
                "attempts": len(subset),
                "feasible": len(feasible),
                "feasible_rate": len(feasible) / len(subset),
                "failure_codes": dict(sorted(failures.items())),
                "best_training_objective_s": min((item.objective for item in feasible), default=None),
            }
        summary = {
            "status": "passed",
            "claim_level": protocol["claim_level"],
            "protocol_sha256": sha(args.protocol),
            "baseline_protocol_sha256": sha(args.baseline_protocol),
            "evaluator_sha256": evaluator_sha,
            "attempted_evaluations": len(records),
            "treatment_summaries": summaries,
            "promotions": ready_promotions,
            "refined_evaluator": protocol["refined_evaluator"],
            "readiness": review,
            "replay": {
                "status": "exact", "result_ledger_sha256": sha(result_ledger),
                "replay_ledger_sha256": sha(replay_ledger),
                "ledger_content_equal": result_ledger.read_bytes() == replay_ledger.read_bytes(),
                "records_sha256": canonical_sha256(ready_records),
            },
            "budget_ledger": {"sha256": sha(budget_ledger), "attempts": len(records), "failed_attempts_counted": True},
            "exploit_controls": controls,
            "performance": {"wall_time_s": wall_time, "tracemalloc_peak_bytes": peak_memory},
            "upstream": {
                "work049_result_sha256": baseline["replay"]["result_sha256"],
                "work049_matrix_sha256": baseline["replay"]["matrix_sha256"],
                "work049_process": {"exit_code": upstream.returncode, "stdout": upstream.stdout, "stderr": upstream.stderr},
            },
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
            "worktree_dirty_during_run": bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout),
            "review": {
                "supporting_evidence": [
                    "all three treatments consumed identical attempted budgets through one evaluator and opportunity set",
                    "geometry variables causally changed assembly mass and declared capacity proxy while material densities stayed fixed",
                    "all selected training-feasible candidates had explicit holdout evaluations and exact ancestry/RNG provenance",
                    "same-seed replay reproduced the complete append-only result and budget content",
                ],
                "contradicting_evidence": [
                    "no independent refined whole-vehicle stress-field evaluator exists, so no selected candidate is a winner",
                ],
                "alternative_explanations": [
                    "treatment differences can be artifacts of the five-variable bounds and analytical capacity proxy",
                ],
                "missing_evidence": [
                    "independent stress/deformation refinement, arbitrary topology, calibrated material laws, contact/aero/transient fidelity, and physical tests",
                ],
                "confidence": "high for equal-budget deterministic search mechanics; low for engineering merit of candidates",
            },
        }
        write(args.artifact_root / "experiment_summary.json", summary)
        print(json.dumps({
            "status": "passed", "attempts": len(records),
            "budgets": review["attempt_counts"], "promotions": len(promotions),
            "holdout_passed": sum(item.holdout_status == "feasible" for item in promotions),
            "refined_passed": sum(item.refined_status == "passed" for item in promotions),
            "replay": "exact", "decision": review["decision"],
            "blockers": review["blockers"], "exploit_controls": len(controls),
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
