#!/usr/bin/env python3
"""Prepare and verify Work 056 runner state while keeping all execution locked."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import traceback


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.experiments.campaign_runner import (  # noqa: E402
    CampaignLedgerStore,
    CampaignRunnerError,
    ChainedJsonlLedger,
    execute_training_opportunities,
)
from formula_ultimate.experiments.main_campaign_protocol import validate_main_campaign_protocol  # noqa: E402


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=ROOT / "config/experiments/bounded_whole_vehicle_main_campaign_v1.json")
    parser.add_argument("--artifact-root", type=Path, default=ROOT / "artifacts/work056")
    parser.add_argument("--mode", choices=("prepare", "verify"), default="prepare")
    args = parser.parse_args()
    args.artifact_root.mkdir(parents=True, exist_ok=True)
    stage = "protocol"
    try:
        protocol = read(args.protocol)
        summary = validate_main_campaign_protocol(protocol)
        stage = "ledger"
        prep_root = args.artifact_root / "preparation_only"
        budget = ChainedJsonlLedger(prep_root / "budget_ledger.jsonl", protocol_id=summary.protocol_id, campaign_id="PREP-FU-BMC-001", evidence_class="preparation_only", ledger_kind="budget")
        result = ChainedJsonlLedger(prep_root / "result_ledger.jsonl", protocol_id=summary.protocol_id, campaign_id="PREP-FU-BMC-001", evidence_class="preparation_only", ledger_kind="result")
        store = CampaignLedgerStore(budget, result)
        store.initialize()
        state = store.validate()
        if state["reservations"] or state["results"] or state["pending_candidate_ids"]:
            raise CampaignRunnerError("Work 056 preparation ledgers must remain empty")
        stage = "execution_lock"
        lock_control = "not_run"
        try:
            execute_training_opportunities(store, {}, "GRID", 55001, lambda candidate: None, target_attempts=1, authorization=None)
        except CampaignRunnerError as exc:
            if "locked" not in str(exc):
                raise
            lock_control = "rejected_as_expected"
        if lock_control != "rejected_as_expected":
            raise CampaignRunnerError("unauthorized execution control was admitted")
        fingerprint = store.fingerprint()
        replay = store.fingerprint()
        if fingerprint != replay:
            raise CampaignRunnerError("empty runner-state replay differs")
        evidence = {
            "status": "passed",
            "decision": "runner_prepared_campaign_locked",
            "mode": args.mode,
            "candidate_evaluations": 0,
            "burn_in_evaluations": 0,
            "main_seed_evaluations": 0,
            "protocol_sha256": sha(args.protocol),
            "protocol_fingerprint_sha256": summary.protocol_fingerprint_sha256,
            "ledger_schema": "chained_campaign_jsonl_v1",
            "ledger_state": {"reservations": 0, "results": 0, "pending": 0, "fingerprint_sha256": fingerprint},
            "execution_lock_control": lock_control,
            "planned": {"paired_seeds": len(summary.paired_seeds), "total_attempts": summary.total_attempts, "maximum_promotions": summary.maximum_promotions},
            "replay": {"status": "exact", "fingerprint_sha256": replay},
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
            "worktree_dirty_during_run": bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout),
            "review": {
                "supporting_evidence": ["budget and result ledgers initialize as an exact empty hash-chained state", "unauthorized main-seed execution is rejected before evaluator invocation", "protocol budget and promotion plan are loaded without candidate evaluation"],
                "contradicting_evidence": ["no physical adapter or interruption recovery has been exercised outside unit fixtures"],
                "alternative_explanations": ["filesystem behavior during real long-running solver processes may expose failure modes absent from fixtures"],
                "missing_evidence": ["burn-in authorization", "CalculiX adapter", "STEP/FreeCAD finalist adapter", "admitted campaign execution"],
                "confidence": "high for prepared locked state; no campaign-outcome evidence",
            },
        }
        write(args.artifact_root / "runner_preparation.json", evidence)
        print(json.dumps({"status": evidence["status"], "decision": evidence["decision"], "candidate_evaluations": 0, "reservations": 0, "results": 0, "pending": 0, "execution_lock": lock_control, "replay": "exact", "summary": str(args.artifact_root / "runner_preparation.json")}, sort_keys=True))
        return 0
    except Exception as exc:
        write(args.artifact_root / "runner_preparation_failure.json", {"status": "failed", "failed_stage": stage, "error_type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()})
        print(json.dumps({"status": "failed", "stage": stage, "message": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
