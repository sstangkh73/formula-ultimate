"""Validation and adjudication for generalized exact-geometry structural solves."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "generalized_meshed_structural_coupling_v1"
CASE_IDS = ("output_shaft_combined", "support_block_bearing", "converter_housing_mount")
METRICS = ("maximum_displacement_m", "compliance_m_per_n", "p90_von_mises_stress_pa")


class GeneralizedCouplingViolation(ValueError):
    """Raised when configuration or solver evidence fails closed."""


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")
    ).hexdigest()


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise GeneralizedCouplingViolation(f"{label} must be a mapping")
    return value


def _exact(value: Mapping[str, Any], fields: set[str], label: str) -> None:
    if set(value) != fields:
        raise GeneralizedCouplingViolation(f"{label} fields mismatch")


def _finite(value: Any, label: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise GeneralizedCouplingViolation(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0.0):
        raise GeneralizedCouplingViolation(f"{label} outside finite domain")
    return result


def _vec3(value: Any, label: str) -> tuple[float, float, float]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 3:
        raise GeneralizedCouplingViolation(f"{label} must have three entries")
    return tuple(_finite(item, label) for item in value)  # type: ignore[return-value]


def _sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise GeneralizedCouplingViolation(f"{label} must be lowercase SHA-256")
    return value


def validate_config(raw: Mapping[str, Any]) -> dict[str, Any]:
    _exact(raw, {"schema_version", "experiment_id", "claim_level", "source", "material", "cases", "tolerances", "failure_control", "evidence_policy"}, "config")
    if raw["schema_version"] != SCHEMA_VERSION:
        raise GeneralizedCouplingViolation("unsupported schema version")
    source = _mapping(raw["source"], "source")
    _exact(source, {"work084_result_path", "work084_result_sha256", "geometry_manifest_path", "geometry_manifest_sha256", "freecad_report_path", "freecad_report_sha256", "step_root"}, "source")
    for key in ("work084_result_sha256", "geometry_manifest_sha256", "freecad_report_sha256"):
        _sha(source[key], key)
    material = _mapping(raw["material"], "material")
    _exact(material, {"material_id", "material_record_sha256", "density_kg_per_m3", "youngs_modulus_pa", "poisson_ratio", "yield_strength_pa", "evidence_class", "design_use_allowed"}, "material")
    _sha(material["material_record_sha256"], "material identity")
    for key in ("density_kg_per_m3", "youngs_modulus_pa", "yield_strength_pa"):
        _finite(material[key], key, positive=True)
    poisson = _finite(material["poisson_ratio"], "poisson ratio")
    if not -1.0 < poisson < 0.5:
        raise GeneralizedCouplingViolation("poisson ratio outside elastic domain")
    if material["evidence_class"] != "synthetic_verification" or material["design_use_allowed"] is not False:
        raise GeneralizedCouplingViolation("material must remain synthetic-only")
    cases = raw["cases"]
    if not isinstance(cases, list) or tuple(item.get("case_id") for item in cases) != CASE_IDS:
        raise GeneralizedCouplingViolation("required structural cases changed")
    for index, case_raw in enumerate(cases):
        case = _mapping(case_raw, f"cases[{index}]")
        _exact(case, {"case_id", "part_id", "step_file", "step_sha256", "load_region", "support_region", "force_n", "torque_nm", "characteristic_length_m", "mesh_levels_m"}, f"cases[{index}]")
        _sha(case["step_sha256"], "STEP identity")
        force = _vec3(case["force_n"], "force")
        torque = _vec3(case["torque_nm"], "torque")
        if math.sqrt(sum(x*x for x in force)) == 0.0 and math.sqrt(sum(x*x for x in torque)) == 0.0:
            raise GeneralizedCouplingViolation("case must apply force or torque")
        _finite(case["characteristic_length_m"], "characteristic length", positive=True)
        levels = case["mesh_levels_m"]
        if not isinstance(levels, list) or len(levels) != 3 or any(_finite(x, "mesh size", positive=True) <= 0 for x in levels):
            raise GeneralizedCouplingViolation("three positive mesh levels required")
        if not levels[0] > levels[1] > levels[2]:
            raise GeneralizedCouplingViolation("mesh levels must refine strictly")
        load = _mapping(case["load_region"], "load region")
        if load.get("kind") not in {"end_plane", "cylinder_y"}:
            raise GeneralizedCouplingViolation("unsupported load region")
        support = _mapping(case["support_region"], "support region")
        if support.get("axis") not in {"x", "y", "z"}:
            raise GeneralizedCouplingViolation("unsupported support axis")
        _finite(support.get("coordinate_m"), "support coordinate")
    tolerances = _mapping(raw["tolerances"], "tolerances")
    _exact(tolerances, {"surface_m", "force_residual_relative", "moment_residual_relative", "energy_residual_relative", "last_two_mesh_relative_change"}, "tolerances")
    for key, value in tolerances.items():
        _finite(value, key, positive=True)
    failure = _mapping(raw["failure_control"], "failure control")
    if failure.get("kind") != "severed_support" or failure.get("expected_state") != "dnf" or _vec3(failure.get("expected_transmitted_force_n"), "failed force") != (0.0, 0.0, 0.0) or _vec3(failure.get("expected_transmitted_torque_nm"), "failed torque") != (0.0, 0.0, 0.0):
        raise GeneralizedCouplingViolation("severed-support control changed")
    policy = _mapping(raw["evidence_policy"], "policy")
    if policy != {"hidden_geometry_repair_allowed": False, "design_use_allowed": False, "evidence_class": "synthetic_meshed_verification"}:
        raise GeneralizedCouplingViolation("evidence policy changed")
    return {"status": "passed", "config_sha256": canonical_sha256(raw), "case_ids": list(CASE_IDS)}


def _relative(a: float, b: float) -> float:
    return abs(b - a) / max(abs(a), abs(b), 1e-30)


def adjudicate(raw: Mapping[str, Any], evidence: Mapping[str, Any]) -> dict[str, Any]:
    validation = validate_config(raw)
    if evidence.get("source_identities_verified") is not True or evidence.get("hidden_geometry_repair") is not False:
        raise GeneralizedCouplingViolation("source identity or repair evidence failed")
    case_results = evidence.get("case_results")
    if not isinstance(case_results, list) or [item.get("case_id") for item in case_results] != list(CASE_IDS):
        raise GeneralizedCouplingViolation("solver case evidence changed")
    tol = raw["tolerances"]
    summaries = []
    for case in case_results:
        meshes = case.get("mesh_results")
        if not isinstance(meshes, list) or len(meshes) != 3:
            raise GeneralizedCouplingViolation("three mesh results required per case")
        for mesh in meshes:
            if mesh.get("solver_converged") is not True or mesh.get("loaded_nodes", 0) <= 0 or mesh.get("support_nodes", 0) <= 0:
                raise GeneralizedCouplingViolation("solver convergence or region mapping failed")
            for metric in METRICS + ("force_residual_relative", "moment_residual_relative", "energy_residual_relative"):
                _finite(mesh.get(metric), metric)
            if mesh["force_residual_relative"] > tol["force_residual_relative"] or mesh["moment_residual_relative"] > tol["moment_residual_relative"] or mesh["energy_residual_relative"] > tol["energy_residual_relative"]:
                raise GeneralizedCouplingViolation("equilibrium or energy residual exceeds gate")
        changes = {metric: _relative(meshes[-2][metric], meshes[-1][metric]) for metric in METRICS}
        if any(value > tol["last_two_mesh_relative_change"] for value in changes.values()):
            raise GeneralizedCouplingViolation("last-two mesh convergence exceeds gate")
        fine = meshes[-1]
        state = "elastic" if fine["p90_von_mises_stress_pa"] < raw["material"]["yield_strength_pa"] else "yield_exceeded"
        failure = case.get("severed_support_control")
        if failure != {"connection_state": "severed", "transmitted_force_n": [0.0, 0.0, 0.0], "transmitted_torque_nm": [0.0, 0.0, 0.0], "subsystem_state": "dnf"}:
            raise GeneralizedCouplingViolation("severed-support control was not causal")
        summaries.append({"case_id": case["case_id"], "state": state, "fine_metrics": fine, "last_two_relative_changes": changes})
    body = {"status": "passed", "verdict": "synthetic_meshed_verification_only", "design_use_allowed": False, "config_sha256": validation["config_sha256"], "cases": summaries}
    return {**body, "adjudication_sha256": canonical_sha256(body)}
