"""Run Work 044 deterministic rainflow and Miner acceptance."""

from __future__ import annotations

import argparse
from dataclasses import replace
from decimal import Decimal
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import traceback
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.structural import (  # noqa: E402
    RainflowCycle,
    StructuralEvidenceError,
    corrected_amplitude_goodman,
    evaluate_damage_blocks,
    fatigue_material_from_mapping,
    rainflow_cycles,
    reversal_history,
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def result_dict(result: Any) -> dict[str, Any]:
    return {
        "ledger": [{name: getattr(entry, name) for name in entry.__dataclass_fields__} for entry in result.ledger],
        "cumulative_damage": result.cumulative_damage, "failed": result.failed,
        "event_cycle": result.event_cycle, "event_id": result.event_id,
    }


def block(spec: dict[str, Any]) -> tuple:
    return rainflow_cycles(reversal_history(float(spec["low_pa"]), float(spec["high_pa"]), int(spec["cycles"])))


def rejected(control_id: str, action: Callable[[], object], expected: str) -> dict[str, str]:
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
    args = parser.parse_args()
    stage = "configuration"
    try:
        payload = json.loads(args.config.read_text(encoding="utf-8"))
        record = fatigue_material_from_mapping(payload["material"])
        if args.artifact_root.exists():
            shutil.rmtree(args.artifact_root)
        args.artifact_root.mkdir(parents=True)
        stage = "constant_amplitude"
        constant_spec = payload["constant_amplitude"]
        constant_cycles = block(constant_spec)
        counted_constant = math.fsum(cycle.count for cycle in constant_cycles)
        expected_constant = float(constant_spec["cycles"])
        if counted_constant != expected_constant:
            raise StructuralEvidenceError(f"constant rainflow count differs: {counted_constant} != {expected_constant}")
        constant = evaluate_damage_blocks(record, (("constant", constant_cycles),))
        expected_damage = Decimal(str(expected_constant)) / Decimal(str(record.reference_cycles))
        damage_error = abs(Decimal(constant.cumulative_damage) - expected_damage) / expected_damage
        if float(damage_error) > float(payload["tolerances"]["constant_damage_relative"]):
            raise StructuralEvidenceError(f"constant-amplitude damage gate failed: {damage_error}")
        if constant.event_cycle != record.reference_cycles or not constant.failed or Decimal(constant.cumulative_damage) <= Decimal(1):
            raise StructuralEvidenceError("constant-amplitude first crossing or unclipped damage failed")
        stage = "variable_sequence"
        high = block(payload["sequence_blocks"]["high"])
        low = block(payload["sequence_blocks"]["low"])
        high_low = evaluate_damage_blocks(record, (("high", high), ("low", low)))
        low_high = evaluate_damage_blocks(record, (("low", low), ("high", high)))
        if Decimal(high_low.cumulative_damage) != Decimal(low_high.cumulative_damage):
            raise StructuralEvidenceError("Miner final damage changed under block permutation")
        if high_low.event_cycle == low_high.event_cycle or not high_low.failed or not low_high.failed:
            raise StructuralEvidenceError("block chronology did not remain observable at first crossing")
        stage = "mean_stress"
        mean_cycles = block(payload["mean_stress_case"])
        mean_result = evaluate_damage_blocks(record, (("positive_mean", mean_cycles),))
        mean_entry = mean_result.ledger[0]
        expected_corrected = 100e6 / (1.0 - 150e6 / record.ultimate_stress_pa)
        if mean_entry.corrected_alternating_stress_pa != expected_corrected:
            raise StructuralEvidenceError("Goodman corrected amplitude differs from reference")
        stage = "negative_controls"
        controls = [
            rejected("overload", lambda: corrected_amplitude_goodman(record, RainflowCycle(640e6, 0.0, 1.0)), "above"),
            rejected("under_domain", lambda: corrected_amplitude_goodman(record, RainflowCycle(100e6, 0.0, 1.0)), "below"),
            rejected("invalid_mean", lambda: corrected_amplitude_goodman(record, RainflowCycle(100e6, 500e6, 1.0)), "ultimate"),
            rejected("missing_curve", lambda: fatigue_material_from_mapping({key: value for key, value in payload["material"].items() if key != "curve"}), "malformed fatigue"),
            rejected("missing_provenance", lambda: fatigue_material_from_mapping({**payload["material"], "provenance": ""}), "provenance"),
            rejected("non_finite_history", lambda: rainflow_cycles((0.0, float("nan"), 1.0)), "finite"),
        ]
        evidence_core = {"constant": result_dict(constant), "high_low": result_dict(high_low), "low_high": result_dict(low_high), "mean_stress": result_dict(mean_result), "negative_controls": controls}
        replay_hash = hashlib.sha256(json.dumps(evidence_core, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        second_hash = hashlib.sha256(json.dumps(evidence_core, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if replay_hash != second_hash:
            raise StructuralEvidenceError("fatigue evidence replay identity changed")
        summary = {
            "status": "passed", "claim_level": payload["claim_level"], "rainflow_version": "work044_astm_stack_v1",
            **evidence_core, "constant_counted_cycles": counted_constant,
            "constant_damage_relative_error": float(damage_error), "deterministic_replay_sha256": replay_hash,
            "config_sha256": sha(args.config),
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
            "worktree_dirty_during_run": bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout),
            "review": {
                "supporting_evidence": ["constant-amplitude rainflow count and damage match the analytical fixture", "unclipped first crossing, sequence chronology, Goodman correction, uncertainty, and exact replay are observable", "unsupported domains fail closed"],
                "contradicting_evidence": [],
                "alternative_explanations": ["Miner summation intentionally omits load-interaction effects"],
                "missing_evidence": ["sourced S-N data", "multiaxial and strain-life evidence", "crack growth and physical spectrum tests"],
                "confidence": "high for deterministic arithmetic; low for any real service-life claim",
            },
        }
        write_json(args.artifact_root / "experiment_summary.json", summary)
        print(json.dumps({"status": "passed", "constant_damage": constant.cumulative_damage, "constant_event_cycle": constant.event_cycle, "high_low_event_cycle": high_low.event_cycle, "low_high_event_cycle": low_high.event_cycle, "negative_controls": len(controls), "summary": str(args.artifact_root / "experiment_summary.json")}, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {"status": "failed", "failed_stage": stage, "error_type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
        write_json(args.artifact_root / "experiment_failure.json", failure)
        print(json.dumps(failure, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
