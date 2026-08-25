"""Gate Work 006 CAD evidence, execute Level 0, and write the summary."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.components.grammar import MountingPlateSpec  # noqa: E402
from formula_ultimate.experiments.cad_level0 import (  # noqa: E402
    CadMeasurement,
    EvidenceViolation,
    Level0Controls,
    evaluate_cad_measurement,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _strict(values: list[float], direction: str) -> bool:
    pairs = zip(values, values[1:])
    if direction == "decreasing":
        return all(left > right for left, right in pairs)
    return all(left < right for left, right in pairs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    controls = Level0Controls(**config["level0_controls"])
    tolerance = config["tolerances"]
    candidate_results: list[dict[str, Any]] = []

    for candidate in config["valid_candidates"]:
        candidate_id = candidate["candidate_id"]
        candidate_dir = args.artifact_root / candidate_id
        manifest = json.loads(
            (candidate_dir / "cadquery_manifest.json").read_text(encoding="utf-8")
        )
        freecad_report = json.loads(
            (candidate_dir / "freecad_measurement.json").read_text(encoding="utf-8")
        )
        step_path = candidate_dir / "component.step"
        actual_step_sha = _sha256(step_path)
        if manifest["candidate_id"] != candidate_id:
            raise EvidenceViolation("candidate ID differs between config and manifest")
        if manifest["step"]["header"] != "ISO-10303-21;":
            raise EvidenceViolation("STEP artifact has an unexpected header")
        if manifest["step"]["sha256"] != actual_step_sha:
            raise EvidenceViolation("STEP hash differs from the CadQuery manifest")
        if freecad_report["step_sha256"] != actual_step_sha:
            raise EvidenceViolation("FreeCAD measured a different STEP hash")

        spec = MountingPlateSpec.from_mapping(manifest["spec"])
        cadquery_measurement = CadMeasurement.from_mapping(
            manifest["cadquery_measurement"]
        )
        freecad_measurement = CadMeasurement.from_mapping(freecad_report)
        kwargs = {
            "spec": spec,
            "controls": controls,
            "volume_absolute_tolerance_m3": tolerance["volume_absolute_m3"],
            "volume_relative_tolerance": tolerance["volume_relative"],
            "bounds_absolute_tolerance_m": tolerance["bounds_absolute_m"],
        }
        cadquery_gate = evaluate_cad_measurement(
            measurement=cadquery_measurement,
            **kwargs,
        )
        level0_result = evaluate_cad_measurement(
            measurement=freecad_measurement,
            **kwargs,
        )
        candidate_results.append(
            {
                "candidate_id": candidate_id,
                "lightening_radius_m": spec.lightening_radius_m,
                "spec": spec.to_dict(),
                "step_sha256": actual_step_sha,
                "step_bytes": step_path.stat().st_size,
                "cadquery_version": manifest["generator"]["cadquery_version"],
                "freecad_version": freecad_report["freecad_version"],
                "cadquery_volume_m3": cadquery_measurement.volume_m3,
                "freecad_volume_m3": freecad_measurement.volume_m3,
                "cadquery_to_freecad_residual_m3": (
                    freecad_measurement.volume_m3 - cadquery_measurement.volume_m3
                ),
                "cadquery_gate_relative_residual": (
                    cadquery_gate.volume_relative_residual
                ),
                "level0_from_freecad": level0_result.to_dict(),
            }
        )

    invalid = config["invalid_candidate"]
    invalid_dir = args.artifact_root / invalid["candidate_id"]
    invalid_report = json.loads(
        (invalid_dir / "grammar_failure.json").read_text(encoding="utf-8")
    )
    if invalid_report["stage"] != "grammar_validation_before_cad":
        raise EvidenceViolation("invalid candidate was not rejected before CAD")
    if invalid_report["cadquery_executed"]:
        raise EvidenceViolation("invalid candidate reports that CadQuery executed")
    if invalid["expected_error_contains"] not in invalid_report["message"]:
        raise EvidenceViolation("invalid candidate failed for the wrong reason")
    if (invalid_dir / "component.step").exists():
        raise EvidenceViolation("invalid candidate unexpectedly has a STEP artifact")

    volumes = [item["freecad_volume_m3"] for item in candidate_results]
    masses = [
        item["level0_from_freecad"]["component_mass_kg"]
        for item in candidate_results
    ]
    speeds = [
        item["level0_from_freecad"]["final_speed_mps"]
        for item in candidate_results
    ]
    distances = [
        item["level0_from_freecad"]["final_distance_m"]
        for item in candidate_results
    ]
    monotonic_checks = {
        "freecad_volume_strictly_decreases": _strict(volumes, "decreasing"),
        "component_mass_strictly_decreases": _strict(masses, "decreasing"),
        "level0_final_speed_strictly_increases": _strict(speeds, "increasing"),
        "level0_final_distance_strictly_increases": _strict(
            distances, "increasing"
        ),
    }
    contradicting = [name for name, passed in monotonic_checks.items() if not passed]
    if contradicting:
        raise EvidenceViolation(f"controlled hypothesis contradicted: {contradicting}")

    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    dirty = bool(
        subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout
    )
    summary = {
        "experiment_id": config["experiment_id"],
        "status": "passed",
        "claim_level": "pipeline coherence at Level 0 only",
        "seed": config["seed"],
        "config_path": str(args.config),
        "config_sha256": _sha256(args.config),
        "repository_commit": commit,
        "worktree_dirty_during_run": dirty,
        "source_sha256": {
            str(path.relative_to(ROOT)): _sha256(path)
            for path in (
                ROOT / "src/formula_ultimate/components/grammar.py",
                ROOT / "src/formula_ultimate/experiments/cad_level0.py",
                ROOT / "scripts/cad/generate_mounting_plate.py",
                ROOT / "scripts/cad/inspect_step_freecad.py",
                ROOT / "scripts/cad/aggregate_work006.py",
                ROOT / "scripts/run_work006.ps1",
            )
        },
        "controls": config["level0_controls"],
        "tolerances": tolerance,
        "candidates": candidate_results,
        "invalid_candidate_evidence": invalid_report,
        "monotonic_checks": monotonic_checks,
        "review": {
            "supporting_evidence": [
                "all three declared valid candidates passed both CAD volume gates",
                "FreeCAD imported each exact hashed STEP artifact as one valid solid",
                "the predeclared mass and Level 0 monotonic checks passed",
                "the deliberate invalid candidate was rejected before CadQuery",
            ],
            "contradicting_evidence": [],
            "alternative_explanations": [
                "the Level 0 change follows the declared point-mass equation and does not establish structural utility",
                "CadQuery and FreeCAD both rely on OCCT-family geometry technology",
            ],
            "missing_evidence": [
                "structural loads and boundary conditions",
                "FEA and mesh convergence",
                "fatigue, manufacturing, assembly, and empirical evidence",
            ],
            "confidence": "high for this local pipeline run; none for physical suitability",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": summary["status"],
                "candidate_count": len(candidate_results),
                "monotonic_checks": monotonic_checks,
                "output": str(args.output),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
