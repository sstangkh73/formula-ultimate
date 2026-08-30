#!/usr/bin/env python3
"""Validate Work 055 campaign rules without evaluating candidates."""

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

from formula_ultimate.experiments.main_campaign_protocol import (  # noqa: E402
    MainCampaignProtocolError,
    summary_as_dict,
    validate_main_campaign_protocol,
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
    parser.add_argument("--config", type=Path, default=ROOT / "config/experiments/bounded_whole_vehicle_main_campaign_v1.json")
    parser.add_argument("--artifact-root", type=Path, default=ROOT / "artifacts/work055")
    args = parser.parse_args()
    args.artifact_root.mkdir(parents=True, exist_ok=True)
    stage = "declaration"
    try:
        protocol = read(args.config)
        summary = validate_main_campaign_protocol(protocol)
        replay = validate_main_campaign_protocol(protocol)
        if summary != replay:
            raise MainCampaignProtocolError("protocol validation replay differs")

        stage = "upstream_identity"
        upstream = protocol["upstream_identity"]
        local_checks = {
            "work047_assembly_config_sha256": sha(ROOT / "config/vehicle/topology_neutral_vehicle_v1.json"),
            "work048_protocol_sha256": sha(ROOT / "config/vehicle/whole_vehicle_load_cases_v1.json"),
            "work049_baseline_protocol_sha256": read(ROOT / "artifacts/work049/experiment_summary.json")["protocol_sha256"],
            "work053_config_sha256": sha(ROOT / "config/structural/section_force_vehicle_frame_refinement_v2.json"),
            "work054_config_sha256": sha(ROOT / "config/experiments/refined_gate_readiness_adjudication_v1.json"),
        }
        work048 = read(ROOT / "artifacts/work048/experiment_summary.json")
        work049 = read(ROOT / "artifacts/work049/experiment_summary.json")
        work053 = read(ROOT / "artifacts/work053/experiment_summary.json")
        work054 = read(ROOT / "artifacts/work054/readiness_summary.json")
        local_checks.update({
            "work048_training_partition_sha256": work048["partitions"]["training_sha256"],
            "work048_holdout_partition_sha256": work048["partitions"]["holdout_sha256"],
            "work049_reference_result_sha256": work049["reference"]["result_sha256"],
            "work049_reference_matrix_sha256": work049["replay"]["matrix_sha256"],
            "work053_evaluator_identity": work053["evaluator_identity"],
            "work053_replay_fingerprint_sha256": work053["replay"]["fingerprint_sha256"],
            "work053_calculix_sha256": work053["tool_sha256"]["ccx"],
            "work054_adjudication_sha256": work054["adjudication_sha256"],
        })
        if local_checks != upstream:
            differing = sorted(name for name in upstream if upstream.get(name) != local_checks.get(name))
            raise MainCampaignProtocolError(f"upstream identity mismatch: {differing}")
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", protocol["frozen_source_commit"], "HEAD"],
            cwd=ROOT, capture_output=True,
        )
        if ancestor.returncode:
            raise MainCampaignProtocolError("frozen source commit is not an ancestor of HEAD")

        evidence = {
            "status": "passed",
            "decision": "rules_frozen_campaign_not_run",
            "claim_level": protocol["claim_level"],
            "candidate_evaluations": 0,
            "config_sha256": sha(args.config),
            "protocol": summary_as_dict(summary),
            "upstream_identity": local_checks,
            "replay": {"status": "exact", "protocol_fingerprint_sha256": replay.protocol_fingerprint_sha256},
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
            "worktree_dirty_during_run": bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout),
            "review": {
                "supporting_evidence": ["equal paired-seed opportunity is explicit", "GRID budget remains below its non-repeating capacity", "holdout/refined/final-witness gates precede eligibility"],
                "contradicting_evidence": ["12 seeds do not guarantee power for small treatment effects", "GRID is discrete while RANDOM and EVOLUTION are continuous within bounds"],
                "alternative_explanations": ["observed treatment differences can arise from the frozen five-variable grammar rather than general algorithm quality"],
                "missing_evidence": ["burn-in infrastructure evidence", "admitted campaign results", "independent replication", "higher-fidelity and physical validation"],
                "confidence": "high that the rules are internally consistent; no confidence claim about campaign outcomes before execution",
            },
        }
        write(args.artifact_root / "protocol_validation.json", evidence)
        print(json.dumps({
            "status": evidence["status"], "decision": evidence["decision"],
            "candidate_evaluations": evidence["candidate_evaluations"],
            "paired_seeds": len(summary.paired_seeds), "total_attempts": summary.total_attempts,
            "grid_unique": summary.grid_unique_opportunities, "maximum_promotions": summary.maximum_promotions,
            "replay": evidence["replay"]["status"], "summary": str(args.artifact_root / "protocol_validation.json"),
        }, sort_keys=True))
        return 0
    except Exception as exc:
        write(args.artifact_root / "protocol_failure.json", {"status": "failed", "failed_stage": stage, "error_type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()})
        print(json.dumps({"status": "failed", "stage": stage, "message": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
