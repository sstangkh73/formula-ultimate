"""Fail-closed evidence adjudication for Work 082 geometry/solver coupling."""

from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any, Mapping, Sequence


COUPLING_VERSION = "geometry_structural_coupling_v1"
_SHA = re.compile(r"^[0-9a-f]{64}$")


class GeometryStructuralViolation(ValueError):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")


def _fail(code: str, message: str) -> None:
    raise GeometryStructuralViolation(code, message)


def canonical_sha256(value: Mapping[str, Any]) -> str:
    try:
        data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        _fail("canonicalization_error", str(exc))
    return hashlib.sha256(data).hexdigest()


def _map(value: Any, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail("schema_error", f"{context} must be an object")
    return value


def _seq(value: Any, context: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        _fail("schema_error", f"{context} must be an array")
    return value


def _exact(value: Mapping[str, Any], keys: set[str], context: str) -> None:
    if set(value) != keys:
        _fail("schema_error", f"{context} keys mismatch")


def _num(value: Any, context: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        _fail("invalid_numeric_value", f"{context} must be finite numeric")
    result = float(value)
    if positive and result <= 0.0:
        _fail("invalid_numeric_value", f"{context} must be > 0")
    return result


def _sha(value: Any, context: str) -> str:
    if not isinstance(value, str) or not _SHA.fullmatch(value):
        _fail("invalid_identity", f"{context} must be a SHA-256")
    return value


def validate_coupling_config(raw_value: Mapping[str, Any]) -> dict[str, Any]:
    raw = _map(raw_value, "config")
    _exact(raw, {"coupling_version", "experiment_id", "claim_level", "geometry", "material", "load_case", "mesh_levels", "tolerances", "claim_boundary"}, "config")
    if raw["coupling_version"] != COUPLING_VERSION or raw["claim_level"] != "synthetic_verification":
        _fail("version_or_claim_mismatch", "Work 082 version/claim level differs")
    geometry = _map(raw["geometry"], "geometry")
    _exact(geometry, {"part_id", "step_file", "step_sha256", "freecad_report_sha256", "loaded_interface_id", "loaded_surface_signature_sha256", "hole_center_m", "hole_radius_m", "support_plane_x_m", "characteristic_length_m"}, "geometry")
    for key in ("step_sha256", "freecad_report_sha256", "loaded_surface_signature_sha256"):
        _sha(geometry[key], key)
    center = _seq(geometry["hole_center_m"], "hole_center_m")
    if len(center) != 3:
        _fail("schema_error", "hole_center_m must have three values")
    tuple(_num(item, "hole center") for item in center)
    _num(geometry["hole_radius_m"], "hole radius", positive=True)
    _num(geometry["support_plane_x_m"], "support plane")
    _num(geometry["characteristic_length_m"], "characteristic length", positive=True)
    material = _map(raw["material"], "material")
    _exact(material, {"material_id", "material_record_sha256", "evidence_status", "youngs_modulus_pa", "poisson_ratio", "density_kg_per_m3", "yield_strength_pa", "ultimate_strength_pa", "fracture_evidence_status", "fatigue_evidence_status"}, "material")
    _sha(material["material_record_sha256"], "material record")
    if material["evidence_status"] != "synthetic" or material["fracture_evidence_status"] != "unsupported" or material["fatigue_evidence_status"] != "unsupported":
        _fail("unsupported_evidence", "reference must preserve synthetic/missing evidence status")
    for key in ("youngs_modulus_pa", "density_kg_per_m3", "yield_strength_pa", "ultimate_strength_pa"):
        _num(material[key], key, positive=True)
    poisson = _num(material["poisson_ratio"], "poisson_ratio")
    if not -1.0 < poisson < 0.5 or material["yield_strength_pa"] > material["ultimate_strength_pa"]:
        _fail("invalid_material", "elastic or strength domain is invalid")
    load = _map(raw["load_case"], "load case")
    _exact(load, {"load_case_id", "force_n", "application", "connection_id", "connection_criticality"}, "load case")
    force = _seq(load["force_n"], "force_n")
    if len(force) != 3 or math.sqrt(math.fsum(_num(item, "force") ** 2 for item in force)) <= 0.0:
        _fail("invalid_load", "force must be a non-zero 3-vector")
    if load["application"] != "consistent_cylindrical_surface_load" or load["connection_criticality"] not in {"critical", "redundant"}:
        _fail("invalid_load", "load application/criticality is unsupported")
    meshes = _seq(raw["mesh_levels"], "mesh_levels")
    if len(meshes) != 3:
        _fail("invalid_refinement", "exactly three mesh levels are required")
    sizes = []
    ids = set()
    for item in meshes:
        mesh = _map(item, "mesh level"); _exact(mesh, {"mesh_id", "characteristic_size_m"}, "mesh level")
        if mesh["mesh_id"] in ids:
            _fail("invalid_refinement", "duplicate mesh id")
        ids.add(mesh["mesh_id"]); sizes.append(_num(mesh["characteristic_size_m"], "mesh size", positive=True))
    if not sizes[0] > sizes[1] > sizes[2]:
        _fail("invalid_refinement", "mesh sizes must strictly decrease")
    tolerances = _map(raw["tolerances"], "tolerances")
    required_tolerances = {"interface_radial_m", "support_plane_m", "force_residual_relative", "moment_residual_relative", "energy_residual_relative", "last_two_displacement_relative", "last_two_compliance_relative", "last_two_p90_stress_relative"}
    _exact(tolerances, required_tolerances, "tolerances")
    for key, value in tolerances.items():
        if _num(value, key, positive=True) > (0.1 if "relative" in key else 0.001):
            _fail("invalid_tolerance", f"{key} is too permissive")
    claim = _map(raw["claim_boundary"], "claim_boundary")
    _exact(claim, {"design_use_allowed", "admitted_claims", "prohibited_claims"}, "claim_boundary")
    if claim["design_use_allowed"] is not False or "real_part_capacity" not in set(_seq(claim["prohibited_claims"], "prohibited claims")):
        _fail("claim_boundary_mismatch", "synthetic evidence cannot allow design use")
    return {"status": "passed", "config_sha256": canonical_sha256(raw)}


def adjudicate_solver_evidence(config_raw: Mapping[str, Any], raw_value: Mapping[str, Any]) -> dict[str, Any]:
    config = validate_coupling_config(config_raw)
    raw = _map(raw_value, "solver evidence")
    _exact(raw, {"geometry_identities", "mesh_results", "solver_converged", "hidden_geometry_repair"}, "solver evidence")
    if raw["solver_converged"] is not True:
        _fail("solver_nonconvergence", "solver did not converge")
    if raw["hidden_geometry_repair"] is not False:
        _fail("hidden_geometry_repair", "geometry repair is forbidden")
    expected_geometry = config_raw["geometry"]
    identities = _map(raw["geometry_identities"], "geometry identities")
    expected_ids = {key: expected_geometry[key] for key in ("step_sha256", "freecad_report_sha256", "loaded_surface_signature_sha256")}
    if identities != expected_ids:
        _fail("geometry_identity_mismatch", "solver evidence does not bind exact Work 081 identities")
    results = _seq(raw["mesh_results"], "mesh results")
    if len(results) != 3:
        _fail("invalid_refinement", "three mesh results are required")
    metrics = []
    for index, item in enumerate(results):
        row = _map(item, "mesh result")
        required = {"mesh_id", "nodes", "elements", "maximum_displacement_m", "compliance_m_per_n", "p90_von_mises_stress_pa", "force_residual_relative", "moment_residual_relative", "energy_residual_relative"}
        _exact(row, required, "mesh result")
        if row["mesh_id"] != config_raw["mesh_levels"][index]["mesh_id"] or row["nodes"] <= 0 or row["elements"] <= 0:
            _fail("invalid_refinement", "mesh identity/count differs")
        for key in required - {"mesh_id", "nodes", "elements"}:
            _num(row[key], key, positive=key in {"maximum_displacement_m", "compliance_m_per_n", "p90_von_mises_stress_pa"})
        for key in ("force_residual_relative", "moment_residual_relative", "energy_residual_relative"):
            if row[key] > config_raw["tolerances"][key]:
                _fail("residual_gate_failed", f"{key} exceeds tolerance")
        metrics.append(row)
    medium, fine = metrics[-2:]
    changes = {}
    for metric, tolerance_key in (("maximum_displacement_m", "last_two_displacement_relative"), ("compliance_m_per_n", "last_two_compliance_relative"), ("p90_von_mises_stress_pa", "last_two_p90_stress_relative")):
        change = abs(fine[metric] - medium[metric]) / abs(medium[metric])
        changes[metric] = change
        if change > config_raw["tolerances"][tolerance_key]:
            _fail("mesh_nonconvergence", f"{metric} did not meet last-two gate")
    stress = fine["p90_von_mises_stress_pa"]
    material = config_raw["material"]
    state = "elastic" if stress < material["yield_strength_pa"] else "yield_domain_exceeded" if stress < material["ultimate_strength_pa"] else "ultimate_domain_exceeded"
    body = {"status": "passed", "config_sha256": config["config_sha256"], "structural_state": state, "last_two_relative_changes": changes, "fine_metrics": fine, "unsupported_failure_modes": ["fracture", "fatigue"], "evidence_class": "synthetic_verification", "design_use_allowed": False}
    return {**body, "adjudication_sha256": canonical_sha256(body)}


def propagate_connection_state(config_raw: Mapping[str, Any], structural_state: str) -> dict[str, Any]:
    validate_coupling_config(config_raw)
    if structural_state not in {"elastic", "yield_domain_exceeded", "ultimate_domain_exceeded", "severed_load_path"}:
        _fail("invalid_failure_state", "unknown structural state")
    failed = structural_state in {"ultimate_domain_exceeded", "severed_load_path"}
    critical = config_raw["load_case"]["connection_criticality"] == "critical"
    force = config_raw["load_case"]["force_n"]
    body = {"connection_id": config_raw["load_case"]["connection_id"], "connection_state": "failed" if failed else "degraded" if structural_state == "yield_domain_exceeded" else "intact", "transmitted_force_n": [0.0, 0.0, 0.0] if failed else list(force), "subsystem_state": "dnf" if failed and critical else "operational_degraded" if failed or structural_state == "yield_domain_exceeded" else "operational", "structural_state": structural_state}
    return {**body, "state_sha256": canonical_sha256(body)}
