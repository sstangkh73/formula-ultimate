from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.experiments.whole_mechanical_vehicle_candidate import (  # noqa: E402
    build_bundle, canonical_bytes, canonical_sha256, file_sha256, load_evidence,
)


def write_json(path: Path, value: object) -> None:
    path.write_bytes(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False).encode("utf-8") + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/candidates/whole_mechanical_vehicle_candidate_001.json")
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--replay-reference")
    args = parser.parse_args()

    config_path = ROOT / args.config
    config = json.loads(config_path.read_text(encoding="utf-8"))
    evidence = load_evidence(ROOT, config)
    bundle = build_bundle(config, evidence)
    output_root = ROOT / args.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    for filename, payload in bundle.items():
        write_json(output_root / filename, payload)

    artifact_hashes = {filename: file_sha256(output_root / filename) for filename in sorted(bundle)}
    class_coverage = {
        "individual_step_per_part": {"evidence": "geometry_artifact_index.json", "count": 17},
        "complete_assembly_step": {"evidence": "geometry_artifact_index.json"},
        "freecad_fcstd": {"evidence": "geometry_artifact_index.json"},
        "assembly_tree": {"evidence": "assembly_tree.json"},
        "joint_dof_manifest": {"evidence": "joint_dof_manifest.json"},
        "material_manifest": {"evidence": "material_manifest.json"},
        "mass_com_inertia_report": {"evidence": "mass_com_inertia_report.json"},
        "interference_report": {"evidence": "interference_report.json"},
        "structural_load_case_report": {"evidence": "structural_load_case_report.json"},
        "torque_power_energy_ledger": {"evidence": "torque_power_energy_ledger.json"},
        "failure_propagation_report": {"evidence": "failure_propagation_report.json"},
        "deterministic_replay_manifest": {"evidence": "deterministic_replay_manifest.json"},
        "level0_simulation_decision": {"evidence": "level0_simulation_decision.json"},
    }
    if tuple(class_coverage) != tuple(config["required_artifact_classes"]):
        raise SystemExit("required artifact class coverage mismatch")
    artifact_manifest = {
        "candidate_id": config["candidate_id"],
        "required_artifact_classes": config["required_artifact_classes"],
        "class_coverage": class_coverage,
        "generated_report_sha256": artifact_hashes,
        "external_geometry": bundle["geometry_artifact_index.json"],
    }
    artifact_manifest["artifact_manifest_sha256"] = canonical_sha256(artifact_manifest)
    write_json(output_root / "artifact_manifest.json", artifact_manifest)

    result = {
        "candidate_id": config["candidate_id"],
        "status": "passed",
        "audit_status": "passed",
        "candidate_verdict": "not_ready",
        "level0_simulation_status": "not_run_pre_admission_blocked",
        "blockers": bundle["admission_report.json"]["blockers"],
        "admission_report_sha256": bundle["admission_report.json"]["admission_report_sha256"],
        "artifact_manifest_sha256": artifact_manifest["artifact_manifest_sha256"],
        "config_sha256": canonical_sha256(config),
        "source_result_sha256": bundle["admission_report.json"]["source_result_sha256"],
    }
    result["result_sha256"] = canonical_sha256(result)
    write_json(output_root / "result.json", result)

    if args.replay_reference:
        reference = ROOT / args.replay_reference
        if not reference.is_file() or reference.read_bytes() != (output_root / "result.json").read_bytes():
            raise SystemExit("replay result mismatch")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
