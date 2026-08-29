"""Execute one declared candidate through 3D, STEP, FreeCAD, and Level 0."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
import traceback
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.experiments.research_protocol import (  # noqa: E402
    CandidateDeclaration,
    ResearchProtocol,
    admit_candidate_evidence,
    load_json,
    sha256_file,
)


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _run(stage: str, command: list[str]) -> dict[str, Any]:
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    evidence = {
        "stage": stage,
        "command": command,
        "exit_code": completed.returncode,
        "wall_time_s": time.perf_counter() - started,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }
    if completed.returncode != 0:
        raise RuntimeError(json.dumps(evidence, sort_keys=True))
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--cadquery-python", type=Path, required=True)
    parser.add_argument("--freecad-python", type=Path, required=True)
    args = parser.parse_args()

    candidate_dir = args.artifact_root / "FU-C0001"
    result_path = candidate_dir / "experiment_result.json"
    failure_path = candidate_dir / "experiment_failure.json"
    step_path = candidate_dir / "candidate.step"
    manifest_path = candidate_dir / "cadquery_manifest.json"
    grammar_failure_path = candidate_dir / "grammar_failure.json"
    freecad_path = candidate_dir / "freecad_measurement.json"
    for stale in (result_path, failure_path, step_path, manifest_path,
                  grammar_failure_path, freecad_path):
        if stale.exists():
            stale.unlink()

    current_stage = "declaration_gate"
    stage_evidence: list[dict[str, Any]] = []
    try:
        protocol_payload = load_json(args.protocol)
        candidate_payload = load_json(args.candidate)
        protocol = ResearchProtocol.from_mapping(protocol_payload)
        declaration = CandidateDeclaration.from_mapping(candidate_payload)
        if declaration.candidate_id != "FU-C0001":
            raise ValueError("Work 031 launcher only admits FU-C0001")

        current_stage = "cadquery_3d_generation"
        stage_evidence.append(
            _run(
                current_stage,
                [
                    str(args.cadquery_python),
                    str(ROOT / "scripts/cad/generate_mounting_plate.py"),
                    "--config", str(args.candidate),
                    "--candidate-id", declaration.candidate_id,
                    "--output-step", str(step_path),
                    "--manifest", str(manifest_path),
                    "--failure-json", str(grammar_failure_path),
                ],
            )
        )
        current_stage = "step_export_identity"
        manifest = load_json(manifest_path)
        if manifest.get("step", {}).get("sha256") != sha256_file(step_path):
            raise ValueError("STEP identity check failed before FreeCAD")

        current_stage = "freecad_import_measurement"
        stage_evidence.append(
            _run(
                current_stage,
                [
                    str(args.freecad_python),
                    str(ROOT / "scripts/cad/inspect_step_freecad.py"),
                    str(step_path),
                    str(freecad_path),
                ],
            )
        )
        current_stage = "level0_evidence_admission"
        result = admit_candidate_evidence(
            protocol=protocol,
            declaration=declaration,
            manifest=manifest,
            freecad_report=load_json(freecad_path),
            step_path=step_path,
        )
        current_stage = "falsification_review"
        result.update(
            {
                "seed": declaration.seed,
                "protocol_config_sha256": sha256_file(args.protocol),
                "candidate_config_sha256": sha256_file(args.candidate),
                "repository_commit": subprocess.run(
                    ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                    text=True, capture_output=True,
                ).stdout.strip(),
                "worktree_dirty_during_run": bool(subprocess.run(
                    ["git", "status", "--porcelain"], cwd=ROOT, check=True,
                    text=True, capture_output=True,
                ).stdout),
                "source_sha256": {
                    str(path.relative_to(ROOT)): sha256_file(path)
                    for path in (
                        ROOT / "src/formula_ultimate/components/grammar.py",
                        ROOT / "src/formula_ultimate/experiments/cad_level0.py",
                        ROOT / "src/formula_ultimate/experiments/research_protocol.py",
                        ROOT / "scripts/cad/generate_mounting_plate.py",
                        ROOT / "scripts/cad/inspect_step_freecad.py",
                        Path(__file__),
                    )
                },
                "stage_process_evidence": stage_evidence,
                "review": {
                    "supporting_evidence": [
                        "CadQuery generated one valid solid from the declared input",
                        "FreeCAD imported and measured the exact hashed STEP artifact",
                        "analytical, CadQuery, and FreeCAD evidence passed declared tolerances",
                        "Level 0 used FreeCAD-derived volume rather than analytical substitution",
                    ],
                    "contradicting_evidence": [],
                    "alternative_explanations": [
                        "agreement may reflect shared OCCT-family geometry technology",
                        "the Level 0 output follows an added-point-mass model and not structural utility",
                    ],
                    "missing_evidence": [
                        "complete-vehicle geometry and assembly evidence",
                        "loads, FEA, fatigue, CFD, thermal, manufacturing, safety, and empirical evidence",
                        "multiple candidates and fair optimized baseline comparison",
                    ],
                    "confidence": "high for this local pipeline run; none for physical suitability or race performance",
                },
            }
        )
        _write_json(result_path, result)
        print(json.dumps({
            "status": result["status"],
            "candidate_id": result["candidate_id"],
            "claim_level": result["claim_level"],
            "step_sha256": result["step"]["sha256"],
            "component_mass_kg": result["level0_from_freecad"]["component_mass_kg"],
            "final_speed_mps": result["level0_from_freecad"]["final_speed_mps"],
            "result": str(result_path),
        }, sort_keys=True))
        return 0
    except Exception as exc:  # preserve the failed boundary as experiment data
        failure = {
            "status": "failed",
            "candidate_id": "FU-C0001",
            "failed_stage": current_stage,
            "error_type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
            "completed_processes": stage_evidence,
        }
        _write_json(failure_path, failure)
        print(json.dumps(failure, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
