"""Run Work 043 analytical LEFM initiation acceptance."""

from __future__ import annotations

import argparse
from dataclasses import replace
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
    StructuralEvidenceError,
    coupon_from_mapping,
    crack_representation,
    evaluate_fracture,
    material_from_mapping,
    validate_lefm_domain,
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relative(actual: float, expected: float) -> float:
    return abs(actual - expected) / max(abs(expected), 1e-300)


def rejected_control(control_id: str, action: Callable[[], object], expected: str) -> dict[str, str]:
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
        material = material_from_mapping(payload["material"])
        crack_lengths = tuple(float(value) for value in payload["crack_half_lengths_m"])
        load_factors = tuple(float(value) for value in payload["load_factors_of_initiation"])
        representation_levels = tuple(int(value) for value in payload["representation_segments_per_half_crack"])
        if len(crack_lengths) != 3 or not all(left < right for left, right in zip(crack_lengths, crack_lengths[1:])):
            raise StructuralEvidenceError("three strictly increasing crack lengths are required")
        if load_factors != (0.8, 1.0, 1.2):
            raise StructuralEvidenceError("frozen fracture load factors changed")
        if len(representation_levels) != 3 or not all(left < right for left, right in zip(representation_levels, representation_levels[1:])):
            raise StructuralEvidenceError("three increasing representation levels are required")
        domain_config, tolerances = payload["domain"], payload["tolerances"]
        width_limit = float(domain_config["maximum_full_crack_width_ratio"])
        plastic_limit = float(domain_config["maximum_plastic_zone_crack_ratio"])
        if args.artifact_root.exists():
            shutil.rmtree(args.artifact_root)
        args.artifact_root.mkdir(parents=True)
        stage = "admitted_cases"
        cases: list[dict[str, Any]] = []
        maximum_reaction = maximum_energy = maximum_initiation_error = 0.0
        for crack_length in crack_lengths:
            coupon = coupon_from_mapping(payload["coupon"], crack_half_length_m=crack_length)
            domain = validate_lefm_domain(material, coupon, maximum_full_crack_width_ratio=width_limit, maximum_plastic_zone_crack_ratio=plastic_limit)
            representation_results: list[dict[str, Any]] = []
            for resolution in representation_levels:
                representation = crack_representation(coupon, segments_per_half_crack=resolution)
                evaluations = []
                for factor in load_factors:
                    result = evaluate_fracture(material, coupon, applied_force_n=factor * domain["initiation_force_n"], maximum_full_crack_width_ratio=width_limit, maximum_plastic_zone_crack_ratio=plastic_limit)
                    maximum_reaction = max(maximum_reaction, result.reaction_residual_relative)
                    maximum_energy = max(maximum_energy, result.energy_residual_relative)
                    evaluations.append({name: getattr(result, name) for name in result.__dataclass_fields__})
                before, _, after = evaluations
                crossing_fraction = (1.0 - before["utilization"]) / (after["utilization"] - before["utilization"])
                localized_force = before["applied_force_n"] + crossing_fraction * (after["applied_force_n"] - before["applied_force_n"])
                initiation_error = relative(localized_force, domain["initiation_force_n"])
                maximum_initiation_error = max(maximum_initiation_error, initiation_error)
                representation_results.append({"segments_per_half_crack": resolution, "representation": representation, "evaluations": evaluations, "localized_initiation_force_n": localized_force, "initiation_load_relative_error": initiation_error, "crossing_fraction_between_0p8_and_1p2": crossing_fraction})
            k_values = [item["evaluations"][1]["stress_intensity_pa_sqrt_m"] for item in representation_results]
            convergence = relative(k_values[-1], k_values[-2])
            if convergence > float(tolerances["last_two_parameter_relative"]):
                raise StructuralEvidenceError(f"fracture parameter representation convergence failed: {convergence}")
            cases.append({"crack_half_length_m": crack_length, "domain": domain, "representation_results": representation_results, "last_two_parameter_relative": convergence})
        stage = "negative_controls"
        base_coupon = coupon_from_mapping(payload["coupon"], crack_half_length_m=crack_lengths[1])
        controls = [
            rejected_control("too_thin", lambda: validate_lefm_domain(material, replace(base_coupon, thickness_m=0.001), maximum_full_crack_width_ratio=width_limit, maximum_plastic_zone_crack_ratio=plastic_limit), "plane-strain"),
            rejected_control("finite_width", lambda: validate_lefm_domain(material, replace(base_coupon, crack_half_length_m=0.02), maximum_full_crack_width_ratio=width_limit, maximum_plastic_zone_crack_ratio=plastic_limit), "finite-width"),
            rejected_control("missing_flaw", lambda: coupon_from_mapping(payload["coupon"], crack_half_length_m=0.0), "crack_half_length_m"),
            rejected_control("missing_toughness", lambda: material_from_mapping({key: value for key, value in payload["material"].items() if key != "toughness_pa_sqrt_m"}), "malformed fracture material"),
            rejected_control("missing_provenance", lambda: material_from_mapping({**payload["material"], "provenance": ""}), "provenance"),
            rejected_control("yield_before_fracture", lambda: validate_lefm_domain(replace(material, toughness_pa_sqrt_m=40e6), replace(base_coupon, width_m=0.4, thickness_m=0.1, crack_half_length_m=0.005), maximum_full_crack_width_ratio=width_limit, maximum_plastic_zone_crack_ratio=plastic_limit), "yield precedes"),
        ]
        if maximum_initiation_error > float(tolerances["initiation_load_relative"]):
            raise StructuralEvidenceError(f"initiation load gate failed: {maximum_initiation_error}")
        if maximum_reaction > float(tolerances["reaction_residual_relative"]) or maximum_energy > float(tolerances["energy_residual_relative"]):
            raise StructuralEvidenceError("fracture accounting residual gate failed")
        canonical = json.dumps({"protocol_id": payload["protocol_id"], "cases": cases, "negative_controls": controls}, sort_keys=True, separators=(",", ":"))
        summary = {
            "status": "passed", "claim_level": payload["claim_level"], "evaluator": "independently verified ideal LEFM; no crack-tip solver field",
            "cases": cases, "negative_controls": controls,
            "maximum_initiation_load_relative_error": maximum_initiation_error,
            "maximum_reaction_residual_relative": maximum_reaction,
            "maximum_energy_residual_relative": maximum_energy,
            "deterministic_evidence_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
            "config_sha256": sha(args.config),
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
            "worktree_dirty_during_run": bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout),
            "review": {
                "supporting_evidence": ["three crack lengths reproduce the closed-form first crossing", "geometry representation changes preserve exact tagged crack tips and K_I", "all invalid-domain fixtures fail closed"],
                "contradicting_evidence": [],
                "alternative_explanations": ["the Y=1 ideal infinite-plate model removes finite-geometry complexity"],
                "missing_evidence": ["crack-tip FEA contour integral", "physical toughness data", "propagation path and dissipated fracture energy"],
                "confidence": "high for evaluator arithmetic and domain rejection; low beyond ideal initiation",
            },
        }
        write_json(args.artifact_root / "experiment_summary.json", summary)
        print(json.dumps({"status": "passed", "case_count": len(cases), "maximum_initiation_load_relative_error": maximum_initiation_error, "negative_controls": len(controls), "summary": str(args.artifact_root / "experiment_summary.json")}, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {"status": "failed", "failed_stage": stage, "error_type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
        write_json(args.artifact_root / "experiment_failure.json", failure)
        print(json.dumps(failure, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
