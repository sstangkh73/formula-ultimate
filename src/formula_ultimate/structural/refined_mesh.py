"""Identity-locked refinement for the Work 085 housing convergence failure."""

from __future__ import annotations

from copy import deepcopy
import math
from typing import Any, Mapping

from .generalized_coupling import canonical_sha256, validate_config


class RefinedMeshViolation(ValueError):
    """Raised when refinement scope or prior-failure evidence changes."""


def validate_refinement(raw: Mapping[str, Any]) -> dict[str, Any]:
    expected = {"schema_version", "experiment_id", "base_config_path", "base_config_sha256", "failed_evidence_path", "failed_evidence_file_sha256", "failed_case_id", "failed_metric", "observed_last_two_relative_change", "unchanged_gate", "replacement_mesh_levels_m", "allowed_changed_path", "evidence_policy"}
    if set(raw) != expected or raw.get("schema_version") != "refined_housing_mesh_convergence_v1":
        raise RefinedMeshViolation("refinement schema fields mismatch")
    for key in ("base_config_sha256", "failed_evidence_file_sha256"):
        value = raw.get(key)
        if not isinstance(value, str) or len(value) != 64:
            raise RefinedMeshViolation(f"{key} must be SHA-256")
    if raw.get("failed_case_id") != "converter_housing_mount" or raw.get("failed_metric") != "maximum_displacement_m" or raw.get("allowed_changed_path") != "cases[2].mesh_levels_m":
        raise RefinedMeshViolation("refinement target changed")
    gate = float(raw["unchanged_gate"]); observed = float(raw["observed_last_two_relative_change"])
    if not math.isfinite(gate) or gate != 0.12 or not math.isfinite(observed) or observed <= gate:
        raise RefinedMeshViolation("frozen failed value or gate changed")
    levels = raw["replacement_mesh_levels_m"]
    if not isinstance(levels, list) or len(levels) != 3 or not levels[0] > levels[1] > levels[2] > 0:
        raise RefinedMeshViolation("replacement meshes must strictly refine")
    if raw.get("evidence_policy") != {"design_use_allowed": False, "evidence_class": "synthetic_meshed_verification"}:
        raise RefinedMeshViolation("evidence policy changed")
    return {"status": "passed", "refinement_sha256": canonical_sha256(raw)}


def prior_failure_change(evidence: Mapping[str, Any], case_id: str, metric: str) -> float:
    cases = evidence.get("case_results")
    if not isinstance(cases, list):
        raise RefinedMeshViolation("prior case evidence missing")
    case = next((item for item in cases if item.get("case_id") == case_id), None)
    if not case or not isinstance(case.get("mesh_results"), list) or len(case["mesh_results"]) != 3:
        raise RefinedMeshViolation("prior failed case missing")
    a, b = case["mesh_results"][-2:]
    first, second = float(a[metric]), float(b[metric])
    return abs(second-first)/max(abs(first), abs(second), 1e-30)


def derive_config(refinement: Mapping[str, Any], base: Mapping[str, Any], prior: Mapping[str, Any]) -> dict[str, Any]:
    validate_refinement(refinement)
    base_validation = validate_config(base)
    if base_validation["config_sha256"] != refinement["base_config_sha256"]:
        raise RefinedMeshViolation("base config identity mismatch")
    observed = prior_failure_change(prior, refinement["failed_case_id"], refinement["failed_metric"])
    if not math.isclose(observed, float(refinement["observed_last_two_relative_change"]), rel_tol=0.0, abs_tol=1e-15):
        raise RefinedMeshViolation("prior failure value mismatch")
    if observed <= float(refinement["unchanged_gate"]):
        raise RefinedMeshViolation("prior evidence did not fail the frozen gate")
    derived = deepcopy(base)
    target = next(item for item in derived["cases"] if item["case_id"] == refinement["failed_case_id"])
    target["mesh_levels_m"] = list(refinement["replacement_mesh_levels_m"])
    if derived["tolerances"]["last_two_mesh_relative_change"] != refinement["unchanged_gate"]:
        raise RefinedMeshViolation("derived config changed the convergence gate")
    validate_config(derived)
    return derived
