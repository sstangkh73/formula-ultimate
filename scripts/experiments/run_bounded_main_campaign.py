#!/usr/bin/env python3
"""Execute or verify the frozen burn-in and admitted whole-vehicle campaign."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import traceback


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.experiments.campaign_physics import (  # noqa: E402
    CampaignPhysicsError,
    adjudicate_seed_outcomes,
    analyze_main_campaign,
    downstream_fingerprint,
    evaluate_level0,
    file_sha256,
    json_compatible,
    read_json,
    refine_candidate,
    run_cad_witness,
    run_refinement_benchmark,
    training_evaluator_identity,
    validate_campaign_environment,
    validate_campaign_admission,
    write_json,
)
from formula_ultimate.experiments.campaign_runner import (  # noqa: E402
    CampaignExecutionAuthorization,
    CampaignLedgerStore,
    CampaignRunnerError,
    ChainedJsonlLedger,
    decode_evaluation_evidence,
    execute_training_opportunities,
    execution_protocol_from_main,
    select_training_promotions,
)
from formula_ultimate.experiments.whole_vehicle_search import canonical_sha256  # noqa: E402


def _load_stage_records(ledger: ChainedJsonlLedger) -> dict[str, object]:
    benchmark = None
    selections = []
    holdouts, refinements, witnesses = {}, {}, {}
    for row in ledger.read_rows():
        payload = row.payload
        kind = payload.get("record_type")
        if kind == "refinement_benchmark":
            if benchmark is not None:
                raise CampaignPhysicsError("refinement benchmark is duplicated")
            benchmark = payload["benchmark"]
        elif kind == "promotion_selection":
            key = (payload["selection"]["treatment"], int(payload["selection"]["seed"]))
            if any((item["treatment"], int(item["seed"])) == key for item in selections):
                raise CampaignPhysicsError("promotion selection stream is duplicated")
            selections.append(payload["selection"])
        elif kind == "holdout_result":
            evaluation = decode_evaluation_evidence(payload["evaluation"])
            candidate_id = evaluation.candidate.candidate_id
            if candidate_id in holdouts:
                raise CampaignPhysicsError("holdout result is duplicated")
            if evaluation.partition != "holdout":
                raise CampaignPhysicsError("downstream ledger contains a non-holdout evaluation")
            holdouts[candidate_id] = evaluation
        elif kind in {"refinement_result", "cad_witness_result"}:
            result = payload["result"]
            candidate_id = result.get("candidate_id")
            expected = canonical_sha256({key: value for key, value in result.items() if key != "result_sha256"})
            if result.get("result_sha256") != expected:
                raise CampaignPhysicsError(f"{kind} identity hash mismatch")
            destination = refinements if kind == "refinement_result" else witnesses
            if candidate_id in destination:
                raise CampaignPhysicsError(f"{kind} is duplicated")
            destination[candidate_id] = result
        else:
            raise CampaignPhysicsError("downstream ledger contains an unsupported record type")
    return {"benchmark": benchmark, "selections": selections, "holdouts": holdouts, "refinements": refinements, "witnesses": witnesses}


def _skipped_result(candidate_id: str, stage: str, reason: str) -> dict:
    draft = {"candidate_id": candidate_id, "status": "not_run", "failure_code": reason, "stage": stage}
    return {**draft, "result_sha256": canonical_sha256(draft)}


def _counts(training_results, treatments, seeds):
    return {
        f"{treatment}:{seed}": sum(item.candidate.treatment == treatment and item.candidate.seed == seed for item in training_results)
        for treatment in treatments for seed in seeds
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=("burn-in", "main"), required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--admission", type=Path, default=ROOT / "artifacts/work057/campaign_summary.json")
    parser.add_argument("--protocol", type=Path, default=ROOT / "config/experiments/bounded_whole_vehicle_main_campaign_v1.json")
    parser.add_argument("--ccx", type=Path, default=Path(r"C:\Program Files\FreeCAD 1.1\bin\ccx.exe"))
    parser.add_argument("--cadquery-python", type=Path, default=ROOT / ".tools/cadquery-mcp/Scripts/python.exe")
    parser.add_argument("--freecad-python", type=Path, default=Path(r"C:\Program Files\FreeCAD 1.1\bin\python.exe"))
    args = parser.parse_args()
    args.artifact_root.mkdir(parents=True, exist_ok=True)
    stage = "environment"
    try:
        protocol = read_json(args.protocol)
        environment = validate_campaign_environment(ROOT, protocol, ccx=args.ccx, cadquery_python=args.cadquery_python, freecad_python=args.freecad_python)
        if args.kind == "burn-in":
            seeds, campaign_id, evidence_class = (55999,), f"{protocol['campaign_id']}-BURNIN", "burn_in"
            admitted = False
        else:
            seeds = tuple(protocol["design"]["paired_seeds"])
            campaign_id, evidence_class, admitted = protocol["campaign_id"], "admitted_campaign", True
            stage = "admission"
            implementation = {
                "campaign_runner_sha256": file_sha256(ROOT / "src/formula_ultimate/experiments/campaign_runner.py"),
                "campaign_physics_sha256": file_sha256(ROOT / "src/formula_ultimate/experiments/campaign_physics.py"),
                "campaign_command_sha256": file_sha256(Path(__file__)),
            }
            validate_campaign_admission(ROOT, args.admission, args.protocol, protocol, environment, implementation)
        execution = execution_protocol_from_main(protocol, seeds=seeds)
        evaluator_sha = training_evaluator_identity(protocol, environment)
        budget = ChainedJsonlLedger(args.artifact_root / "budget_ledger.jsonl", protocol_id=protocol["protocol_id"], campaign_id=campaign_id, evidence_class=evidence_class, ledger_kind="budget")
        result = ChainedJsonlLedger(args.artifact_root / "result_ledger.jsonl", protocol_id=protocol["protocol_id"], campaign_id=campaign_id, evidence_class=evidence_class, ledger_kind="result")
        stages = ChainedJsonlLedger(args.artifact_root / "stage_ledger.jsonl", protocol_id=protocol["protocol_id"], campaign_id=campaign_id, evidence_class=evidence_class, ledger_kind="stage")
        store = CampaignLedgerStore(budget, result)
        store.initialize()
        stages.initialize()
        authorization = CampaignExecutionAuthorization(
            f"WORK057-BURNIN-{environment['protocol_summary']['protocol_fingerprint_sha256'][:12]}" if args.kind == "burn-in" else f"WORK058-MAIN-{environment['protocol_summary']['protocol_fingerprint_sha256'][:12]}",
            campaign_id, evidence_class, tuple(seeds), admitted,
        )
        stage = "training"
        started = time.perf_counter()
        if not args.verify_only:
            for treatment in execution["treatments"]:
                for seed in seeds:
                    execute_training_opportunities(
                        store, execution, treatment, seed,
                        lambda candidate: evaluate_level0(execution, candidate, environment, evaluator_sha, partition="training"),
                        target_attempts=int(execution["attempted_evaluations_per_treatment_seed"]), authorization=authorization,
                    )
        state = store.validate()
        training_results = tuple(state["results"].values())
        expected_attempts = len(seeds) * len(execution["treatments"]) * int(execution["attempted_evaluations_per_treatment_seed"])
        counts = _counts(training_results, execution["treatments"], seeds)
        expected_stream_count = int(execution["attempted_evaluations_per_treatment_seed"])
        if len(state["reservations"]) != expected_attempts or len(training_results) != expected_attempts or state["pending_candidate_ids"]:
            raise CampaignPhysicsError("campaign training ledger is incomplete")
        if set(counts.values()) != {expected_stream_count}:
            raise CampaignPhysicsError("campaign treatment/seed opportunity counts differ")
        grid_variables = [item.candidate.variables for item in training_results if item.candidate.treatment == "GRID"]
        if len(grid_variables) != len(set(grid_variables)):
            raise CampaignPhysicsError("GRID opportunities repeat")

        stage = "downstream"
        downstream = _load_stage_records(stages)
        if downstream["benchmark"] is None:
            if args.verify_only:
                raise CampaignPhysicsError("refinement benchmark evidence is missing")
            benchmark = run_refinement_benchmark(environment["inputs"]["refinement_config"], ccx=args.ccx, artifact_root=args.artifact_root / "benchmark")
            stages.append({"record_type": "refinement_benchmark", "benchmark": benchmark})
            downstream = _load_stage_records(stages)
        elif downstream["benchmark"].get("status") != "passed":
            raise CampaignPhysicsError("refinement benchmark did not pass")

        selections = select_training_promotions(training_results, execution["treatments"], seeds, per_treatment_seed=int(protocol["promotion"]["training_feasible_candidates_per_treatment_seed"]))
        expected_selections = json_compatible([asdict(item) for item in selections])
        if not downstream["selections"]:
            if args.verify_only:
                raise CampaignPhysicsError("promotion evidence is missing")
            for selection in expected_selections:
                stages.append({"record_type": "promotion_selection", "selection": selection})
            downstream = _load_stage_records(stages)
        if sorted(downstream["selections"], key=lambda row: (row["treatment"], row["seed"])) != sorted(expected_selections, key=lambda row: (row["treatment"], row["seed"])):
            raise CampaignPhysicsError("stored promotion selection differs from training-only replay")

        by_candidate = {item.candidate.candidate_id: item.candidate for item in training_results}
        selected_ids = [candidate_id for selection in expected_selections for candidate_id in selection["candidate_ids"]]
        if len(selected_ids) != len(set(selected_ids)):
            raise CampaignPhysicsError("promoted candidate identity is duplicated")
        for candidate_id in selected_ids:
            candidate = by_candidate[candidate_id]
            if candidate_id not in downstream["holdouts"]:
                if args.verify_only:
                    raise CampaignPhysicsError("holdout evidence is missing")
                holdout = evaluate_level0(execution, candidate, environment, evaluator_sha, partition="holdout")
                stages.append({"record_type": "holdout_result", "evaluation": asdict(holdout)})
                downstream = _load_stage_records(stages)
            holdout = downstream["holdouts"][candidate_id]
            if candidate_id not in downstream["refinements"]:
                if args.verify_only:
                    raise CampaignPhysicsError("refinement evidence is missing")
                refinement = refine_candidate(candidate, environment, ccx=args.ccx, artifact_root=args.artifact_root / "refinement") if holdout.status == "feasible" else _skipped_result(candidate_id, "refinement", "holdout_failure")
                stages.append({"record_type": "refinement_result", "result": refinement})
                downstream = _load_stage_records(stages)
            refinement = downstream["refinements"][candidate_id]
            if candidate_id not in downstream["witnesses"]:
                if args.verify_only:
                    raise CampaignPhysicsError("CAD witness evidence is missing")
                witness = run_cad_witness(ROOT, candidate, environment, cadquery_python=args.cadquery_python, freecad_python=args.freecad_python, artifact_root=args.artifact_root / "cad") if refinement["status"] == "passed" else _skipped_result(candidate_id, "cad_witness", refinement.get("failure_code") or "refinement_failure")
                stages.append({"record_type": "cad_witness_result", "result": witness})
                downstream = _load_stage_records(stages)

        if set(downstream["holdouts"]) != set(selected_ids) or set(downstream["refinements"]) != set(selected_ids) or set(downstream["witnesses"]) != set(selected_ids):
            raise CampaignPhysicsError("downstream evidence set differs from promotions")
        outcomes = adjudicate_seed_outcomes(execution["treatments"], seeds, expected_selections, downstream["holdouts"], downstream["refinements"], downstream["witnesses"])
        supported = sum(row["supported_finisher_present"] for row in outcomes)
        if args.kind == "burn-in":
            decision = "burn_in_accepted_for_admitted_main_campaign"
            analysis = None
            final_status = "passed"
        else:
            analysis = analyze_main_campaign(outcomes, training_results, analysis_seed=int(protocol["analysis"]["analysis_seed"]))
            decision = "completed_with_supported_finishers" if supported else "completed_without_supported_finisher"
            final_status = decision
        stage_rows = [row.payload for row in stages.read_rows()]
        implementation = {
            "campaign_runner_sha256": file_sha256(ROOT / "src/formula_ultimate/experiments/campaign_runner.py"),
            "campaign_physics_sha256": file_sha256(ROOT / "src/formula_ultimate/experiments/campaign_physics.py"),
            "campaign_command_sha256": file_sha256(Path(__file__)),
        }
        summary = {
            "status": "passed", "final_status": final_status, "decision": decision,
            "campaign_kind": args.kind, "protocol_id": protocol["protocol_id"], "campaign_id": campaign_id, "evidence_class": evidence_class,
            "claim_level": protocol["claim_level"], "protocol_sha256": file_sha256(args.protocol),
            "protocol_fingerprint_sha256": environment["protocol_summary"]["protocol_fingerprint_sha256"],
            "upstream_identity": environment["upstream_identity"], "tool_identity": environment["tool_identity"],
            "implementation_identity": implementation, "authorization": asdict(authorization),
            "training": {
                "expected_attempts": expected_attempts, "reservations": len(state["reservations"]),
                "terminal_results": len(training_results), "pending": len(state["pending_candidate_ids"]),
                "stream_counts": counts, "failure_counts": dict(sorted(Counter(item.failure_code or "feasible" for item in training_results).items())),
                "budget_fingerprint_sha256": state["budget_fingerprint_sha256"],
                "result_fingerprint_sha256": state["result_fingerprint_sha256"], "combined_fingerprint_sha256": store.fingerprint(),
                "grid_unique": len(set(grid_variables)), "training_evaluator_sha256": evaluator_sha,
            },
            "downstream": {
                "promotion_streams": len(expected_selections), "promoted_candidates": len(selected_ids),
                "promotion_shortfall": sum(item.shortfall for item in selections),
                "holdout_terminal": len(downstream["holdouts"]), "refinement_terminal": len(downstream["refinements"]),
                "cad_witness_terminal": len(downstream["witnesses"]),
                "refinement_passed": sum(item["status"] == "passed" for item in downstream["refinements"].values()),
                "cad_witness_passed": sum(item["status"] == "passed" for item in downstream["witnesses"].values()),
                "stage_fingerprint_sha256": stages.fingerprint(), "records_fingerprint_sha256": downstream_fingerprint(stage_rows),
            },
            "seed_outcomes": list(outcomes), "supported_treatment_seed_outcomes": supported,
            "analysis": analysis, "elapsed_this_invocation_s": time.perf_counter() - started,
            "replay": {"status": "exact", "training_fingerprint_sha256": store.fingerprint(), "stage_fingerprint_sha256": stages.fingerprint()},
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
            "worktree_dirty_during_run": bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout),
            "review": {
                "supporting_evidence": ["equal opportunity ledgers and downstream evidence replay exactly", "promotions replay from training-only terminal results", "all promoted candidates have terminal holdout, refinement, and CAD-witness records"],
                "contradicting_evidence": ["the refined evaluator is a linear beam network and Level 0 remains a selection gate"],
                "alternative_explanations": ["treatment outcomes can depend on the frozen five-variable grammar rather than general search quality"],
                "missing_evidence": ["solid/contact/nonlinear vehicle analysis", "physical material calibration", "manufacturing tolerance", "hardware testing", "independent campaign replication"],
                "confidence": "high for bounded campaign execution and replay; low outside the frozen evaluator domain",
            },
        }
        write_json(args.artifact_root / "campaign_summary.json", summary)
        print(json.dumps({
            "status": "passed", "decision": decision, "kind": args.kind, "verify_only": args.verify_only,
            "attempts": len(training_results), "promotions": len(selected_ids), "refined_passed": summary["downstream"]["refinement_passed"],
            "witness_passed": summary["downstream"]["cad_witness_passed"], "supported_streams": supported,
            "replay": "exact", "summary": str(args.artifact_root / "campaign_summary.json"),
        }, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {"status": "failed", "failed_stage": stage, "error_type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
        write_json(args.artifact_root / "campaign_failure.json", failure)
        print(json.dumps({"status": "failed", "stage": stage, "message": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
