"""Execute Work 117 architecture-to-part feedback evidence."""
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

from formula_ultimate.experiments.architecture_part_feedback import (  # noqa: E402
    ArchitectureFeedbackViolation,
    canonical_sha256,
    generate_candidate,
    merge_region_mass,
    run_loop,
    validate_protocol,
)


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rejected(action, phrase: str) -> dict:
    try:
        action()
    except ArchitectureFeedbackViolation as exc:
        if phrase not in str(exc):
            raise
        return {"status": "rejected", "reason": str(exc)}
    raise ArchitectureFeedbackViolation("negative control was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()

    config_path = (ROOT / args.config).resolve() if not args.config.is_absolute() else args.config
    output_root = (ROOT / args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    raw = read(config_path)
    validation = validate_protocol(raw)

    for dependency in raw["dependencies"]:
        if sha256(ROOT / dependency["contract_path"]) != dependency["contract_sha256"]:
            raise ArchitectureFeedbackViolation("stale dependency contract")
        commit = subprocess.run(
            ["git", "cat-file", "-e", dependency["commit"] + "^{commit}"],
            cwd=ROOT,
            capture_output=True,
        )
        if commit.returncode:
            raise ArchitectureFeedbackViolation("missing dependency commit")

    inputs = {}
    for item in raw["inputs"]:
        result = read(ROOT / item["path"])
        if result.get("result_sha256") != item["result_sha256"]:
            raise ArchitectureFeedbackViolation(f"stale Work {item['work']} result")
        inputs[item["work"]] = result

    moving = inputs[114]["body"]["levels"][-1]
    thermal = inputs[115]["body"]["levels"][-1]
    thermal_duration_s = 5.0
    conditions = {
        "assembly_load_n": moving["maximum_contact_force_n"],
        "assembly_heat_w": thermal["supplied_energy_j"] / thermal_duration_s,
        "assembly_motion_m": moving["maximum_abs_position_m"],
        "unknowns": sorted(
            key for key, status in raw["model_coverage"].items() if status != "implemented"
        ),
    }

    feedback = run_loop(raw, conditions, feedback_enabled=True)
    frozen = run_loop(raw, conditions, feedback_enabled=False)
    expected_evaluations = (
        raw["resource_cap"]["iterations"] * raw["resource_cap"]["evaluations_per_iteration"]
    )
    if feedback["total_evaluations"] != expected_evaluations or frozen["total_evaluations"] != expected_evaluations:
        raise ArchitectureFeedbackViolation("feedback and frozen controls do not have equal compute")
    if feedback["external_task_sha256"] != frozen["external_task_sha256"]:
        raise ArchitectureFeedbackViolation("external task identity differs across controls")
    if len(feedback["invalidations"]) != raw["resource_cap"]["iterations"] - 1:
        raise ArchitectureFeedbackViolation("feedback did not invalidate every stale task")
    if frozen["invalidations"]:
        raise ArchitectureFeedbackViolation("frozen control unexpectedly invalidated evidence")
    if feedback["records"][0]["candidate"]["geometry_sha256"] == feedback["records"][1]["candidate"]["geometry_sha256"]:
        raise ArchitectureFeedbackViolation("feedback did not regenerate geometry")
    if feedback["records"][0]["candidate"]["task_sha256"] == feedback["records"][1]["candidate"]["task_sha256"]:
        raise ArchitectureFeedbackViolation("feedback did not revise the internal task")
    if any(record["complete_feasibility"] for record in feedback["records"] + frozen["records"]):
        raise ArchitectureFeedbackViolation("incomplete model was promoted to complete feasibility")

    regions = [
        {"cells": [(0, 0, 0), (1, 0, 0)], "cell_volume_m3": 1e-6, "density_kg_m3": 2700.0},
        {"cells": [(1, 0, 0), (2, 0, 0)], "cell_volume_m3": 1e-6, "density_kg_m3": 2700.0},
    ]
    merged_mass = merge_region_mass(regions)
    naive_mass = sum(len(region["cells"]) * region["cell_volume_m3"] * region["density_kg_m3"] for region in regions)
    if merged_mass >= naive_mass:
        raise ArchitectureFeedbackViolation("multifunctional merge did not remove duplicate mass")

    missing = copy.deepcopy(raw["coefficients"])
    del missing["allowable_stress_pa"]
    controls = {
        "immutable_external_task": {"status": "passed", "sha256": feedback["external_task_sha256"]},
        "equal_compute": {"status": "passed", "evaluations_per_mode": expected_evaluations},
        "multifunctional_merge": {
            "status": "passed",
            "merged_mass_kg": merged_mass,
            "naive_duplicate_mass_kg": naive_mass,
        },
        "missing_coefficient": rejected(
            lambda: generate_candidate(raw["initial_internal_task"], missing, 7),
            "missing coefficient",
        ),
    }
    initial_mass = feedback["records"][0]["candidate"]["mass_kg"]
    final_mass = feedback["records"][-1]["candidate"]["mass_kg"]
    comparison = {
        "feedback_final_mass_kg": final_mass,
        "feedback_initial_mass_kg": initial_mass,
        "mass_change_kg": final_mass - initial_mass,
        "improvement_required": False,
        "interpretation": "regeneration evidence only; lower mass or improved margins are not admission gates",
    }
    body = {
        "status": "passed",
        "claim_scope": "bounded architecture-to-part task feedback and deterministic regeneration; not optimization, complete feasibility, vehicle readiness, or physical validation",
        "validation": validation,
        "dependencies": raw["dependencies"],
        "input_result_sha256": {str(work): result["result_sha256"] for work, result in sorted(inputs.items())},
        "derived_conditions": conditions,
        "feedback": feedback,
        "frozen_control": frozen,
        "controls": controls,
        "comparison": comparison,
        "review": {
            "supporting_evidence": [
                "assembly-derived load, heat and motion changed the versioned internal task and regenerated geometry",
                "stale internal-task evidence was explicitly invalidated while the external task stayed immutable",
                "feedback and frozen controls used identical coefficients, seeds and evaluation counts",
            ],
            "contradicting_evidence": [
                "the bounded generator does not search general topology and improvement is not guaranteed"
            ],
            "alternative_explanations": [
                "candidate changes also include the registered seed perturbation, so task and seed identities are both retained"
            ],
            "missing_evidence": [
                "measured material behavior",
                "ground interaction",
                "full vehicle integration",
                "physical validation",
            ],
            "confidence": "high for deterministic task ancestry/invalidation; low for physical design quality",
        },
    }
    result = {"body": body, "result_sha256": canonical_sha256(body)}
    write(output_root / "result.json", result)

    if args.replay_reference:
        reference_path = (ROOT / args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference
        previous = read(reference_path)
        exact = previous.get("result_sha256") == result["result_sha256"]
        write(
            output_root / "replay.json",
            {
                "reference_result_sha256": previous.get("result_sha256"),
                "current_result_sha256": result["result_sha256"],
                "exact": exact,
            },
        )
        if not exact:
            raise ArchitectureFeedbackViolation("replay differs from reference")

    print(
        json.dumps(
            {
                "status": "passed",
                "result_sha256": result["result_sha256"],
                "evaluations_per_mode": expected_evaluations,
                "invalidations": len(feedback["invalidations"]),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
