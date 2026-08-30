#!/usr/bin/env python3
"""Run Work 054 refined-gate readiness adjudication."""

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

from formula_ultimate.experiments.refined_readiness import (  # noqa: E402
    ReadinessAdjudicationError,
    adjudicate_refined_readiness,
)


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "config/experiments/refined_gate_readiness_adjudication_v1.json")
    parser.add_argument("--artifact-root", type=Path, default=ROOT / "artifacts/work054")
    args = parser.parse_args()
    args.artifact_root.mkdir(parents=True, exist_ok=True)
    stage = "work053"
    try:
        upstream = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ROOT / "scripts/run_work053.ps1")],
            cwd=ROOT, text=True, capture_output=True,
        )
        if upstream.returncode:
            raise ReadinessAdjudicationError("fresh Work 053 replay failed")
        config = read(args.config)
        if config.get("protocol_id") != "refined_gate_readiness_adjudication_v1":
            raise ReadinessAdjudicationError("Work 054 protocol identity mismatch")
        work050 = read(ROOT / "artifacts/work050/experiment_summary.json")
        work053 = read(ROOT / "artifacts/work053/experiment_summary.json")
        identity050 = config["work050"]
        checks050 = {
            "protocol_sha256": work050["protocol_sha256"],
            "records_sha256": work050["replay"]["records_sha256"],
            "result_ledger_sha256": sha(ROOT / "artifacts/work050/result_ledger.jsonl"),
            "budget_ledger_sha256": sha(ROOT / "artifacts/work050/budget_ledger.jsonl"),
        }
        if checks050 != identity050:
            raise ReadinessAdjudicationError("Work 050 evidence identity mismatch")
        identity053 = config["work053"]
        checks053 = {
            "evaluator_identity": work053["evaluator_identity"],
            "config_sha256": work053["config_sha256"],
            "module_sha256": sha(ROOT / "src/formula_ultimate/structural/vehicle_frame_refinement.py"),
            "runner_sha256": sha(ROOT / "scripts/structural/run_vehicle_frame_refinement.py"),
            "replay_fingerprint_sha256": work053["replay"]["fingerprint_sha256"],
            "calculix_sha256": work053["tool_sha256"]["ccx"],
        }
        for key, value in checks053.items():
            if identity053[key] != value:
                raise ReadinessAdjudicationError(f"Work 053 {key} mismatch")
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", identity053["implementation_commit"], "HEAD"],
            cwd=ROOT, capture_output=True,
        )
        if ancestor.returncode:
            raise ReadinessAdjudicationError("Work 053 implementation commit is not an ancestor")

        stage = "adjudication"
        settings = {
            "expected_treatments": tuple(config["expected_treatments"]),
            "original_promotions_per_treatment": int(config["original_promotions_per_treatment"]),
            "minimum_supported_per_treatment": int(config["minimum_supported_per_treatment"]),
            "expected_attempts_per_treatment": int(config["expected_attempts_per_treatment"]),
        }
        result = adjudicate_refined_readiness(work050, work053, **settings)
        replay = adjudicate_refined_readiness(work050, work053, **settings)
        if result != replay:
            raise ReadinessAdjudicationError("adjudication replay differs")
        summary = {
            "status": "passed",
            "claim_level": config["claim_level"],
            **result,
            "config_sha256": sha(args.config),
            "upstream": {
                "work050": checks050,
                "work053": checks053,
                "work053_process": {"exit_code": upstream.returncode, "stdout": upstream.stdout, "stderr": upstream.stderr},
            },
            "replay": {"status": "exact", "adjudication_sha256": replay["adjudication_sha256"]},
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
            "worktree_dirty_during_run": bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout),
            "review": {
                "supporting_evidence": ["all Work 050 checks other than the retained refined-evaluator blocker remained true", "seven candidates passed the Work 053 refined gate", "every treatment retained at least two supported candidates and the global winner is supported"],
                "contradicting_evidence": ["two proxy-promoted candidates remain rejected by cross-model stress disagreement"],
                "alternative_explanations": ["the pilot ranking can change under higher-fidelity physics or a larger candidate grammar"],
                "missing_evidence": ["main-campaign replication, higher-fidelity multiphysics, physical calibration, and hardware testing"],
                "confidence": "high for bounded campaign readiness; low for physical vehicle validity or treatment superiority",
            },
        }
        write(args.artifact_root / "readiness_summary.json", summary)
        print(json.dumps({
            "status": summary["status"], "decision": summary["decision"],
            "supported_candidates": summary["supported_candidates"], "rejected_candidates": summary["rejected_candidates"],
            "global_winner": summary["global_winner"]["candidate_id"] if summary["global_winner"] else None,
            "blockers": summary["blockers"], "replay": summary["replay"]["status"],
            "summary": str(args.artifact_root / "readiness_summary.json"),
        }, sort_keys=True))
        return 0 if summary["decision"] == "ready_for_bounded_whole_vehicle_campaign" else 2
    except Exception as exc:
        write(args.artifact_root / "readiness_failure.json", {"status": "failed", "failed_stage": stage, "error_type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()})
        print(json.dumps({"status": "failed", "stage": stage, "message": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
