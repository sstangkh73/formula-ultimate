"""Execute Work 126 deterministic detailed-vehicle closure evidence."""
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

from formula_ultimate.assembly.detailed_vehicle_closure import (  # noqa: E402
    DetailedVehicleClosureViolation,
    canonical_sha256,
    evaluate_closure,
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
    except DetailedVehicleClosureViolation as exc:
        if phrase not in str(exc):
            raise
        return {"status": "rejected", "reason": str(exc)}
    raise DetailedVehicleClosureViolation("negative control accepted")


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
            raise DetailedVehicleClosureViolation("stale dependency contract")
        if subprocess.run(["git", "cat-file", "-e", dependency["commit"] + "^{commit}"], cwd=ROOT, capture_output=True).returncode:
            raise DetailedVehicleClosureViolation("missing dependency commit")
    inputs = {}
    for item in raw["inputs"]:
        value = read(ROOT / item["path"])
        if value.get("result_sha256") != item["result_sha256"]:
            raise DetailedVehicleClosureViolation(f"stale Work {item['work']} result")
        inputs[item["work"]] = value
    if inputs[123]["body"]["decision"]["promotion_allowed"] or inputs[125]["body"]["decision"]["discovery_benefit_supported"]:
        raise DetailedVehicleClosureViolation("upstream exploratory boundary mismatch")
    closure = evaluate_closure(raw)

    missing_fastener = copy.deepcopy(raw)
    missing_fastener["components"] = [item for item in missing_fastener["components"] if item["role"] != "fastener"]
    duplicate = copy.deepcopy(raw)
    duplicate["components"][1]["region_id"] = duplicate["components"][0]["region_id"]
    collision = copy.deepcopy(raw)
    collision["components"][1]["center_m"] = collision["components"][0]["center_m"][:]
    stale = copy.deepcopy(raw)
    stale["components"][0]["envelope_revision"] = "stale"
    controls = {
        "missing_fastener": rejected(lambda: evaluate_closure(missing_fastener), "missing required hardware role"),
        "double_mass": rejected(lambda: evaluate_closure(duplicate), "double mass ownership"),
        "interference": rejected(lambda: evaluate_closure(collision), "assembly interference"),
        "stale_envelope": rejected(lambda: evaluate_closure(stale), "stale subsystem envelope"),
    }
    registry = {"geometry_detail": raw["registration"]["geometry_detail"], "envelope_m": raw["registration"]["envelope_m"], "components": raw["components"], "networks": raw["networks"], "motion": raw["motion"]}
    exploded = {item["id"]: {"source_center_m": item["center_m"], "display_center_m": [item["center_m"][0], item["center_m"][1] + (index % 3 - 1) * 0.6, item["center_m"][2]]} for index, item in enumerate(raw["components"])}
    section = {"plane": "y=0", "intersected_component_ids": [item["id"] for item in raw["components"] if abs(item["center_m"][1]) <= item["size_m"][1] / 2]}
    write(output / "assembly_registry.json", registry)
    write(output / "exploded_view.json", exploded)
    write(output / "section_view.json", section)
    body = {
        "status": "detailed_exploratory",
        "claim_scope": "deterministic G3 component-bound registry and closure accounting; not native CAD, manufacturability, promotion, or physical validation",
        "validation": validation,
        "dependencies": raw["dependencies"],
        "input_result_sha256": {str(k): v["result_sha256"] for k, v in sorted(inputs.items())},
        "closure": closure,
        "controls": controls,
        "artifact_sha256": {name: sha(output / name) for name in ("assembly_registry.json", "exploded_view.json", "section_view.json")},
        "coverage": raw["coverage"],
        "unresolved": raw["unresolved"],
        "decision": {"promotion_allowed": False, "reason": "essential material, native-CAD, manufacturing and physical-test evidence remains unresolved"},
        "review": {
            "supporting_evidence": ["all registered hardware roles and external functions have explicit owners", "mass, center, inertia and occupied-volume residuals close", "energy, signal, heat and load graphs connect and sampled motion is collision-free"],
            "contradicting_evidence": ["the geometry is a bounded box registry rather than native detailed CAD", "upstream vehicle benefit remains unsupported"],
            "alternative_explanations": ["unmodeled surfaces or tolerances may introduce real interference", "registry closure may omit manufacturing-specific hardware not represented by the checklist"],
            "missing_evidence": raw["unresolved"],
            "confidence": "high for deterministic registry bookkeeping; none for physical closure or promotion",
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
            raise DetailedVehicleClosureViolation("decision replay differs from reference")
    print(json.dumps({"status": body["status"], "result_sha256": result["result_sha256"], "components": closure["component_count"], "promotion_allowed": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
