"""Execute Work 127 fair optimized vehicle-control evidence."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
for item in (ROOT, SRC):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from formula_ultimate.experiments.optimized_vehicle_controls import (  # noqa: E402
    OptimizedVehicleControlsViolation,
    canonical_sha256,
    run_comparison,
    validate_protocol,
)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rejected(action, phrase):
    try:
        action()
    except OptimizedVehicleControlsViolation as exc:
        if phrase not in str(exc):
            raise
        return {"status": "rejected", "reason": str(exc)}
    raise OptimizedVehicleControlsViolation("negative control accepted")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()
    config = args.config if args.config.is_absolute() else ROOT / args.config
    output = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    raw = read(config)
    validation = validate_protocol(raw)
    for dependency in raw["dependencies"]:
        if sha(ROOT / dependency["contract_path"]) != dependency["contract_sha256"]:
            raise OptimizedVehicleControlsViolation("stale dependency contract")
        if subprocess.run(["git", "cat-file", "-e", dependency["commit"] + "^{commit}"], cwd=ROOT, capture_output=True).returncode:
            raise OptimizedVehicleControlsViolation("missing dependency commit")
    inputs = {}
    for item in raw["inputs"]:
        upstream = read(ROOT / item["path"])
        if upstream.get("result_sha256") != item["result_sha256"]:
            raise OptimizedVehicleControlsViolation(f"stale Work {item['work']} result")
        inputs[item["work"]] = upstream
    if inputs[123]["body"]["decision"]["promotion_allowed"] or inputs[124]["body"]["promotion"]["allowed"] or inputs[126]["body"]["decision"]["promotion_allowed"]:
        raise OptimizedVehicleControlsViolation("upstream non-promotion boundary mismatch")
    comparison = run_comparison(raw)
    if len(set(comparison["complete_costs"].values())) != 1:
        raise OptimizedVehicleControlsViolation("complete costs are unequal")

    untuned = copy.deepcopy(raw)
    untuned["arms"]["reference"]["baseline_tuned"] = False
    omitted = copy.deepcopy(raw)
    del omitted["arms"]["open_candidate"]["burdens"]["cooling_mass_kg"]
    energy = copy.deepcopy(raw)
    energy["arms"]["open_candidate"]["source_energy_j"] += 1.0
    free = copy.deepcopy(raw)
    free["budgets"]["open_candidate"]["controller_tuning"] = 0
    controls = {
        "untuned_baseline": rejected(lambda: validate_protocol(untuned), "untuned baseline"),
        "omitted_cooling_mass": rejected(lambda: validate_protocol(omitted), "incomplete burden ledger"),
        "unequal_source_energy": rejected(lambda: validate_protocol(energy), "source energy is unequal"),
        "free_controller_effort": rejected(lambda: validate_protocol(free), "search or tuning budgets are unequal"),
    }
    optimized_artifact = {name: {"tuning": comparison["tuning"][name], "burdens": raw["arms"][name]["burdens"], "complete_cost": comparison["complete_costs"][name]} for name in raw["arms"]}
    substitution = {"common_controller": comparison["common_controller"], "matched_retuned": comparison["retuned"]}
    write(output / "optimized_baselines.json", optimized_artifact)
    write(output / "substitution_matrix.json", substitution)
    body = {
        "status": "completed_negative_result",
        "claim_scope": "registered synthetic optimized-control and causal-substitution accounting; not held-out race evidence, novelty, promotion, or physical validation",
        "validation": validation,
        "dependencies": raw["dependencies"],
        "input_result_sha256": {str(k): v["result_sha256"] for k, v in sorted(inputs.items())},
        "registration": raw["registration"],
        "comparison": comparison,
        "controls": controls,
        "artifact_sha256": {name: sha(output / name) for name in ("optimized_baselines.json", "substitution_matrix.json")},
        "coverage": raw["coverage"],
        "decision": {"system_benefit_supported": False, "promotion_allowed": False, "reason": "paired burden-complete effect is below the registered meaningful threshold and the assembly remains exploratory"},
        "review": {
            "supporting_evidence": ["all arms received matched search and controller-tuning budgets", "common-controller substitution preceded equal retuning", "cooling, containment, support, energy and manufacturing burdens were included"],
            "contradicting_evidence": ["the open candidate did not exceed the registered meaningful-effect gate after transferred burdens", "Work 126 remains a box registry with unresolved physical evidence"],
            "alternative_explanations": ["synthetic burden weights can determine the ranking", "different manufactured controller integration may change transferred burdens"],
            "missing_evidence": ["held-out race evaluation from Work 128", "measured manufacturing and physical performance", "external novelty assessment"],
            "confidence": "high for deterministic fairness/accounting; none for physical system superiority",
        },
    }
    result = {"body": body, "result_sha256": canonical_sha256(body)}
    write(output / "result.json", result)
    if args.replay_reference:
        reference_path = args.replay_reference if args.replay_reference.is_absolute() else ROOT / args.replay_reference
        reference = read(reference_path)
        exact = reference.get("result_sha256") == result["result_sha256"]
        write(output / "replay.json", {"reference_result_sha256": reference.get("result_sha256"), "current_result_sha256": result["result_sha256"], "exact": exact})
        if not exact:
            raise OptimizedVehicleControlsViolation("decision replay differs from reference")
    print(json.dumps({"status": body["status"], "result_sha256": result["result_sha256"], "mean_effect": comparison["mean_effect"], "system_benefit_supported": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
