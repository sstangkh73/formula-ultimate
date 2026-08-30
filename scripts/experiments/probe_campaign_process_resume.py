#!/usr/bin/env python3
"""Exercise one pending reservation across two independent Python processes."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.experiments.campaign_physics import (  # noqa: E402
    evaluate_level0,
    read_json,
    training_evaluator_identity,
    validate_campaign_environment,
    write_json,
)
from formula_ultimate.experiments.campaign_runner import (  # noqa: E402
    CampaignExecutionAuthorization,
    CampaignLedgerStore,
    ChainedJsonlLedger,
    execute_training_opportunities,
    execution_protocol_from_main,
    reconstruct_training_agent,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=("reserve", "resume", "verify"), required=True)
    parser.add_argument("--artifact-root", type=Path, default=ROOT / "artifacts/work057/process_resume_probe")
    args = parser.parse_args()
    protocol = read_json(ROOT / "config/experiments/bounded_whole_vehicle_main_campaign_v1.json")
    ccx = Path(r"C:\Program Files\FreeCAD 1.1\bin\ccx.exe")
    cadquery = ROOT / ".tools/cadquery-mcp/Scripts/python.exe"
    freecad = Path(r"C:\Program Files\FreeCAD 1.1\bin\python.exe")
    environment = validate_campaign_environment(ROOT, protocol, ccx=ccx, cadquery_python=cadquery, freecad_python=freecad)
    execution = execution_protocol_from_main(protocol, seeds=(55999,))
    budget = ChainedJsonlLedger(args.artifact_root / "budget_ledger.jsonl", protocol_id=protocol["protocol_id"], campaign_id="PROBE-FU-BMC-001", evidence_class="interruption_probe", ledger_kind="budget")
    result = ChainedJsonlLedger(args.artifact_root / "result_ledger.jsonl", protocol_id=protocol["protocol_id"], campaign_id="PROBE-FU-BMC-001", evidence_class="interruption_probe", ledger_kind="result")
    store = CampaignLedgerStore(budget, result)
    store.initialize()
    agent, pending = reconstruct_training_agent(store, execution, "GRID", 55999)
    if args.action == "reserve":
        if not agent.history and pending is None:
            pending = agent.propose(0)
            store.reserve_attempt(pending)
        state = store.validate()
        candidate_id = pending.candidate_id if pending is not None else next(iter(state["results"]), None)
        write_json(args.artifact_root / "reservation_process.json", {
            "status": "intentionally_stopped_after_reservation", "candidate_id": candidate_id,
            "reservations": len(state["reservations"]), "results": len(state["results"]),
            "pending": len(state["pending_candidate_ids"]),
            "process_id": os.getpid(),
        })
        print(json.dumps({"status": "intentional_process_stop", "candidate_id": candidate_id, "pending": len(state["pending_candidate_ids"])}))
        return 75
    authorization = CampaignExecutionAuthorization("WORK057-PROCESS-RESUME", "PROBE-FU-BMC-001", "interruption_probe", (55999,), False)
    evaluator_sha = training_evaluator_identity(protocol, environment)
    completed = execute_training_opportunities(
        store, execution, "GRID", 55999,
        lambda candidate: evaluate_level0(execution, candidate, environment, evaluator_sha, partition="training"),
        target_attempts=1, authorization=authorization,
    ) if args.action == "resume" else ()
    state = store.validate()
    if len(state["reservations"]) != 1 or len(state["results"]) != 1 or state["pending_candidate_ids"]:
        raise RuntimeError("process-resume probe did not finish exactly one reservation")
    candidate_id = next(iter(state["results"]))
    reservation = read_json(args.artifact_root / "reservation_process.json")
    if reservation["candidate_id"] != candidate_id:
        raise RuntimeError("resumed process completed a different candidate")
    summary = {
        "status": "passed", "decision": "separate_process_resume_exact",
        "candidate_id": candidate_id, "completed_this_process": len(completed),
        "reservations": 1, "results": 1, "pending": 0,
        "budget_fingerprint_sha256": state["budget_fingerprint_sha256"],
        "result_fingerprint_sha256": state["result_fingerprint_sha256"],
        "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
    }
    write_json(args.artifact_root / "probe_summary.json", summary)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
