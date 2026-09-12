"""Execute Work 125 registered detailed-part comparison evidence."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
for item in (ROOT, SRC):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from formula_ultimate.experiments.detailed_part_comparison import (  # noqa: E402
    DetailedPartComparisonViolation,
    canonical_sha256,
    optimize,
    paired_study,
    utility,
    validate_protocol,
)


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rejected(action, phrase):
    try:
        action()
    except DetailedPartComparisonViolation as exc:
        if phrase not in str(exc):
            raise
        return {"status": "rejected", "reason": str(exc)}
    raise DetailedPartComparisonViolation("negative control was accepted")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()
    config_path = args.config if args.config.is_absolute() else ROOT / args.config
    output_root = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    raw = read(config_path)
    validation = validate_protocol(raw)

    for dependency in raw["dependencies"]:
        if sha256(ROOT / dependency["contract_path"]) != dependency["contract_sha256"]:
            raise DetailedPartComparisonViolation("stale dependency contract")
        check = subprocess.run(
            ["git", "cat-file", "-e", dependency["commit"] + "^{commit}"],
            cwd=ROOT,
            capture_output=True,
        )
        if check.returncode:
            raise DetailedPartComparisonViolation("missing dependency commit")

    inputs = {}
    for item in raw["inputs"]:
        upstream = read(ROOT / item["path"])
        if upstream.get("result_sha256") != item["result_sha256"]:
            raise DetailedPartComparisonViolation(f"stale Work {item['work']} result")
        inputs[item["work"]] = upstream
    if inputs[124]["body"]["promotion"]["allowed"]:
        raise DetailedPartComparisonViolation("Work 124 promotion boundary mismatch")
    if not inputs[116]["body"]["missing_domains"]:
        raise DetailedPartComparisonViolation("Work 116 unresolved material scope was lost")

    coarse = paired_study(raw, "coarse")
    fine = paired_study(raw, "fine")
    if coarse["mean_effect"] <= 0 or fine["mean_effect"] >= 0:
        raise DetailedPartComparisonViolation("registered fidelity reversal fixture did not reverse")
    if len({tuple(x["total_evaluations_by_arm"].values()) for x in (coarse, fine)}) != 1:
        raise DetailedPartComparisonViolation("comparison cost changed across fidelity")
    if len(set(fine["total_evaluations_by_arm"].values())) != 1:
        raise DetailedPartComparisonViolation("arm costs were unequal")

    open_parameter = fine["tuning"]["open_material"]["best_parameter"]
    fixed_parameter = fine["tuning"]["fixed_family"]["best_parameter"]
    active = [utility(raw, "open_material", open_parameter, c, "fine") for c in raw["conditions"]["holdout"]]
    ablated = [utility(raw, "open_material", open_parameter, c, "fine", active=False) for c in raw["conditions"]["holdout"]]
    fixed_active = utility(raw, "fixed_family", fixed_parameter, raw["conditions"]["holdout"][0], "fine")
    fixed_inactive = utility(raw, "fixed_family", fixed_parameter, raw["conditions"]["holdout"][0], "fine", active=False)
    ablation_effect = statistics.fmean(a["utility"] - b["utility"] for a, b in zip(active, ablated))
    if abs(ablation_effect - raw["arms"]["open_material"]["active_coupling_effect"]) > 1e-12:
        raise DetailedPartComparisonViolation("active coupling ablation was not causal")
    if fixed_active != fixed_inactive:
        raise DetailedPartComparisonViolation("inactive appendage changed the fixed control")
    omitted = utility(raw, "open_material", open_parameter, raw["conditions"]["holdout"][0], hardware_complete=False)
    if omitted["status"] != "invalid_omitted_hardware":
        raise DetailedPartComparisonViolation("omitted hardware was accepted")
    leaked = copy.deepcopy(raw)
    leaked["conditions"]["training"].append(raw["conditions"]["holdout"][0])
    controls = {
        "holdout_leak": rejected(lambda: validate_protocol(leaked), "holdout leakage"),
        "omitted_hardware": omitted,
        "active_coupling_ablation": {"mean_removed_effect": ablation_effect, "causal": True},
        "inactive_appendage": {"unchanged": True, "active": fixed_active, "inactive": fixed_inactive},
        "ranking_reversal": {
            "coarse_open_minus_best_control": coarse["mean_effect"],
            "fine_open_minus_best_control": fine["mean_effect"],
            "reversed": True,
        },
    }
    audits = {
        "score_independent_ids": raw["audits"]["score_independent_ids"],
        "performed_independent_of_arm_score": True,
        "statuses": {item: "retained_for_failure_review" for item in raw["audits"]["score_independent_ids"]},
    }
    body = {
        "status": "completed_negative_result",
        "claim_scope": "registered synthetic detailed-part comparison with matched optimization and untouched paired holdout; not novelty, whole-vehicle benefit, or physical validation",
        "validation": validation,
        "dependencies": raw["dependencies"],
        "input_result_sha256": {str(k): v["result_sha256"] for k, v in sorted(inputs.items())},
        "registration": raw["registration"],
        "coarse_study": coarse,
        "fine_study": fine,
        "controls": controls,
        "audits": audits,
        "coverage": raw["coverage"],
        "decision": {
            "discovery_benefit_supported": False,
            "reason": "the stronger fine-fidelity paired effect is negative and unresolved material/whole-vehicle evidence remains",
        },
        "review": {
            "supporting_evidence": [
                "all four arms were optimized with equal evaluation counts",
                "training and registered holdout conditions were disjoint",
                "the claimed active coupling effect disappeared under its targeted ablation",
            ],
            "contradicting_evidence": [
                "the coarse positive open-arm ranking reversed to a negative effect at fine fidelity",
                "Work 116 material survival and Work 124 vehicle promotion remain unresolved",
            ],
            "alternative_explanations": [
                "the bounded synthetic response model may not represent manufactured hardware",
                "the coarse model can systematically favor the open arm",
            ],
            "missing_evidence": [
                "measured process-qualified material behavior",
                "external novelty review",
                "whole-vehicle closure and physical tests",
            ],
            "confidence": "high for deterministic protocol execution; none for physical superiority",
        },
    }
    result = {"body": body, "result_sha256": canonical_sha256(body)}
    write(output_root / "result.json", result)
    if args.replay_reference:
        reference_path = args.replay_reference if args.replay_reference.is_absolute() else ROOT / args.replay_reference
        reference = read(reference_path)
        exact = reference.get("result_sha256") == result["result_sha256"]
        write(output_root / "replay.json", {"reference_result_sha256": reference.get("result_sha256"), "current_result_sha256": result["result_sha256"], "exact": exact})
        if not exact:
            raise DetailedPartComparisonViolation("decision replay differs from reference")
    print(json.dumps({"status": body["status"], "result_sha256": result["result_sha256"], "fine_mean_effect": fine["mean_effect"], "benefit_supported": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
