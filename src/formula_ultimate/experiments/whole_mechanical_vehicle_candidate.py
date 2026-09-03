"""Fail-closed admission audit for Whole Mechanical Vehicle Candidate 001."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


class WholeMechanicalVehicleAuditError(ValueError):
    """Raised when evidence is corrupt rather than merely non-admissible."""


REQUIRED_SOURCES = ("work083", "work084", "work086", "work087")
REQUIRED_CASES = (
    "static_support", "acceleration", "braking", "steady_cornering",
    "combined_braking_cornering", "bump_vertical_event", "torque_reaction",
    "thermal_duration", "single_connection_failure", "refinement_replay",
    "mirrored_control",
)
REQUIRED_ARTIFACTS = (
    "individual_step_per_part", "complete_assembly_step", "freecad_fcstd",
    "assembly_tree", "joint_dof_manifest", "material_manifest",
    "mass_com_inertia_report", "interference_report",
    "structural_load_case_report", "torque_power_energy_ledger",
    "failure_propagation_report", "deterministic_replay_manifest",
    "level0_simulation_decision",
)
EXPECTED_BLOCKERS = (
    "forbidden_work083_work084_geometry_interference",
    "work083_vertical_motion_breaks_rigid_work084_coaxial_butt_interface",
    "new_load_frame_has_no_meshed_convergence_evidence",
    "synthetic_material_process_evidence",
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _exact(mapping: Mapping[str, Any], expected: set[str], label: str) -> None:
    if set(mapping) != expected:
        raise WholeMechanicalVehicleAuditError(f"{label} schema mismatch")


def validate_config(config: Mapping[str, Any]) -> dict[str, str]:
    _exact(config, {"schema_version", "candidate_id", "random_seed", "sources", "integration_evidence", "required_artifact_classes", "required_case_ids", "expected_blockers", "evidence_policy"}, "config")
    if config["schema_version"] != "whole_mechanical_vehicle_candidate_001_v1" or config["candidate_id"] != "whole_mechanical_vehicle_candidate_001":
        raise WholeMechanicalVehicleAuditError("candidate identity mismatch")
    if not isinstance(config["random_seed"], int) or isinstance(config["random_seed"], bool):
        raise WholeMechanicalVehicleAuditError("random_seed must be an integer")
    sources = config["sources"]
    if not isinstance(sources, Mapping) or tuple(sorted(sources)) != tuple(sorted(REQUIRED_SOURCES)):
        raise WholeMechanicalVehicleAuditError("source schema mismatch")
    for source in sources.values():
        if not isinstance(source, Mapping):
            raise WholeMechanicalVehicleAuditError("source schema mismatch")
        _exact(source, {"path", "result_sha256", "file_sha256"}, "source")
        if not all(isinstance(source[k], str) and source[k] for k in source):
            raise WholeMechanicalVehicleAuditError("source values must be non-empty strings")
    integration = config["integration_evidence"]
    if not isinstance(integration, Mapping):
        raise WholeMechanicalVehicleAuditError("integration evidence schema mismatch")
    _exact(integration, {"evaluation_path", "evaluation_file_sha256", "geometry_manifest_path", "geometry_manifest_file_sha256", "geometry_root", "assembly_step", "assembly_step_sha256", "freecad_file", "freecad_file_sha256", "part_count"}, "integration evidence")
    if integration["part_count"] != 17:
        raise WholeMechanicalVehicleAuditError("integration evidence must contain 17 parts")
    if tuple(config["required_case_ids"]) != REQUIRED_CASES:
        raise WholeMechanicalVehicleAuditError("required admission cases mismatch")
    if tuple(config["required_artifact_classes"]) != REQUIRED_ARTIFACTS:
        raise WholeMechanicalVehicleAuditError("required artifact classes mismatch")
    if tuple(config["expected_blockers"]) != EXPECTED_BLOCKERS:
        raise WholeMechanicalVehicleAuditError("expected blocker set mismatch")
    policy = config["evidence_policy"]
    if not isinstance(policy, Mapping):
        raise WholeMechanicalVehicleAuditError("evidence policy schema mismatch")
    expected_policy = {
        "hidden_geometry_repair_allowed": False,
        "result_conditioned_geometry_mutation_allowed": False,
        "design_use_allowed": False,
        "run_level0_when_blocked": False,
        "physical_validation_claim_allowed": False,
    }
    if dict(policy) != expected_policy:
        raise WholeMechanicalVehicleAuditError("evidence policy cannot be relaxed or relabelled")
    return {"status": "passed", "config_sha256": canonical_sha256(config)}


def _read_json(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise WholeMechanicalVehicleAuditError(f"missing required artifact: {label}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WholeMechanicalVehicleAuditError(f"invalid JSON artifact: {label}") from exc
    if not isinstance(value, dict):
        raise WholeMechanicalVehicleAuditError(f"invalid object artifact: {label}")
    return value


def load_evidence(root: Path, config: Mapping[str, Any]) -> dict[str, Any]:
    validate_config(config)
    root = Path(root)
    source_results: dict[str, Any] = {}
    source_files: dict[str, str] = {}
    for source_id in REQUIRED_SOURCES:
        spec = config["sources"][source_id]
        path = root / spec["path"]
        result = _read_json(path, source_id)
        actual_file_hash = file_sha256(path)
        if actual_file_hash != spec["file_sha256"] or result.get("result_sha256") != spec["result_sha256"]:
            raise WholeMechanicalVehicleAuditError(f"{source_id} source identity mismatch")
        source_results[source_id] = result
        source_files[source_id] = actual_file_hash

    integration = config["integration_evidence"]
    evaluation_path = root / integration["evaluation_path"]
    manifest_path = root / integration["geometry_manifest_path"]
    evaluation = _read_json(evaluation_path, "Work 087 evaluation")
    manifest = _read_json(manifest_path, "Work 087 geometry manifest")
    if file_sha256(evaluation_path) != integration["evaluation_file_sha256"]:
        raise WholeMechanicalVehicleAuditError("Work 087 evaluation identity mismatch")
    if file_sha256(manifest_path) != integration["geometry_manifest_file_sha256"]:
        raise WholeMechanicalVehicleAuditError("Work 087 geometry manifest identity mismatch")
    if evaluation.get("evaluation_sha256") != source_results["work087"].get("evaluation_sha256"):
        raise WholeMechanicalVehicleAuditError("Work 087 evaluation/result linkage mismatch")
    if manifest.get("manifest_sha256") != source_results["work087"].get("manifest_sha256"):
        raise WholeMechanicalVehicleAuditError("Work 087 manifest/result linkage mismatch")

    geometry_root = root / integration["geometry_root"]
    assembly_path = geometry_root / integration["assembly_step"]
    freecad_path = geometry_root / integration["freecad_file"]
    if not assembly_path.is_file() or file_sha256(assembly_path) != integration["assembly_step_sha256"]:
        raise WholeMechanicalVehicleAuditError("complete assembly STEP identity mismatch")
    if not freecad_path.is_file() or file_sha256(freecad_path) != integration["freecad_file_sha256"]:
        raise WholeMechanicalVehicleAuditError("FreeCAD FCStd identity mismatch")
    parts = manifest.get("parts")
    if not isinstance(parts, list) or len(parts) != integration["part_count"]:
        raise WholeMechanicalVehicleAuditError("individual STEP part count mismatch")
    part_files: dict[str, str] = {}
    for part in parts:
        if not isinstance(part, Mapping) or not isinstance(part.get("part_id"), str) or not isinstance(part.get("step_sha256"), str):
            raise WholeMechanicalVehicleAuditError("part manifest schema mismatch")
        part_path = geometry_root / f"{part['part_id']}.step"
        if not part_path.is_file() or file_sha256(part_path) != part["step_sha256"]:
            raise WholeMechanicalVehicleAuditError(f"individual STEP identity mismatch: {part['part_id']}")
        part_files[part["part_id"]] = part["step_sha256"]
    if len(part_files) != integration["part_count"]:
        raise WholeMechanicalVehicleAuditError("duplicate individual STEP identity")
    return {
        "source_results": source_results,
        "source_file_sha256": source_files,
        "evaluation": evaluation,
        "geometry_manifest": manifest,
        "part_step_sha256": dict(sorted(part_files.items())),
        "assembly_step_sha256": file_sha256(assembly_path),
        "freecad_file_sha256": file_sha256(freecad_path),
    }


def evaluate(config: Mapping[str, Any], evidence: Mapping[str, Any]) -> dict[str, Any]:
    validation = validate_config(config)
    results = evidence.get("source_results")
    if not isinstance(results, Mapping) or set(results) != set(REQUIRED_SOURCES):
        raise WholeMechanicalVehicleAuditError("source evidence set mismatch")
    for source_id in REQUIRED_SOURCES:
        if results[source_id].get("result_sha256") != config["sources"][source_id]["result_sha256"]:
            raise WholeMechanicalVehicleAuditError(f"{source_id} source identity mismatch")
    evaluation = evidence.get("evaluation")
    manifest = evidence.get("geometry_manifest")
    part_hashes = evidence.get("part_step_sha256")
    if not isinstance(evaluation, Mapping) or not isinstance(manifest, Mapping) or not isinstance(part_hashes, Mapping):
        raise WholeMechanicalVehicleAuditError("required evidence object missing")
    if len(part_hashes) != 17 or manifest.get("assembly", {}).get("solid_count") != 17:
        raise WholeMechanicalVehicleAuditError("required geometry artifact coverage mismatch")
    if evidence.get("assembly_step_sha256") != config["integration_evidence"]["assembly_step_sha256"] or evidence.get("freecad_file_sha256") != config["integration_evidence"]["freecad_file_sha256"]:
        raise WholeMechanicalVehicleAuditError("required geometry identity mismatch")
    blockers = evaluation.get("blockers")
    if not isinstance(blockers, list) or tuple(blockers) != EXPECTED_BLOCKERS:
        raise WholeMechanicalVehicleAuditError("upstream blocker suppression or mutation detected")
    if evaluation.get("design_use_allowed") is not False or results["work086"].get("design_use_allowed") is not False:
        raise WholeMechanicalVehicleAuditError("synthetic evidence was relabelled")
    if evaluation.get("candidate_verdict") != "not_admitted" or evaluation.get("integration_status") != "partial":
        raise WholeMechanicalVehicleAuditError("Work 087 admission state mismatch")

    geometry = evaluation.get("geometry", {})
    motion = evaluation.get("motion_interface", {})
    case_reasons = {
        "static_support": ["new_load_frame_has_no_meshed_convergence_evidence", "synthetic_material_process_evidence"],
        "acceleration": ["forbidden_work083_work084_geometry_interference", "new_load_frame_has_no_meshed_convergence_evidence"],
        "braking": ["forbidden_work083_work084_geometry_interference", "new_load_frame_has_no_meshed_convergence_evidence"],
        "steady_cornering": ["forbidden_work083_work084_geometry_interference", "new_load_frame_has_no_meshed_convergence_evidence"],
        "combined_braking_cornering": ["forbidden_work083_work084_geometry_interference", "new_load_frame_has_no_meshed_convergence_evidence"],
        "bump_vertical_event": ["work083_vertical_motion_breaks_rigid_work084_coaxial_butt_interface", "new_load_frame_has_no_meshed_convergence_evidence"],
        "torque_reaction": ["work083_vertical_motion_breaks_rigid_work084_coaxial_butt_interface", "new_load_frame_has_no_meshed_convergence_evidence"],
        "thermal_duration": ["synthetic_material_process_evidence"],
        "single_connection_failure": ["new_load_frame_has_no_meshed_convergence_evidence", "synthetic_material_process_evidence"],
        "refinement_replay": ["new_load_frame_has_no_meshed_convergence_evidence"],
        "mirrored_control": ["forbidden_work083_work084_geometry_interference", "synthetic_material_process_evidence"],
    }
    cases = [
        {"case_id": case_id, "ready": False, "status": "blocked", "blockers": case_reasons[case_id]}
        for case_id in REQUIRED_CASES
    ]
    report = {
        "candidate_id": config["candidate_id"],
        "audit_status": "passed",
        "candidate_verdict": "not_ready",
        "level0_admitted": False,
        "level0_simulation": {
            "status": "not_run_pre_admission_blocked",
            "attempted": False,
            "reason": "four preserved upstream blockers prevent whole-candidate Level-0 admission",
        },
        "blockers": list(blockers),
        "admission_cases": cases,
        "geometry_summary": {
            "part_count": len(part_hashes),
            "positive_forbidden_overlap_count": len(geometry.get("interfering_pairs", [])),
            "maximum_overlap_m3": geometry.get("maximum_overlap_m3"),
            "minimum_forbidden_clearance_m": geometry.get("minimum_forbidden_clearance_m"),
            "maximum_motion_misalignment_m": motion.get("maximum_misalignment_m"),
            "motion_tolerance_m": motion.get("tolerance_m"),
        },
        "config_sha256": validation["config_sha256"],
        "source_result_sha256": {source_id: results[source_id]["result_sha256"] for source_id in REQUIRED_SOURCES},
    }
    report["admission_report_sha256"] = canonical_sha256(report)
    return report


def build_bundle(config: Mapping[str, Any], evidence: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    admission = evaluate(config, evidence)
    evaluation = evidence["evaluation"]
    geometry = evaluation["geometry"]
    work083 = evidence["source_results"]["work083"]
    work084 = evidence["source_results"]["work084"]
    work086 = evidence["source_results"]["work086"]
    assembly_tree = {
        "candidate_id": config["candidate_id"],
        "root": {"node_id": "whole_candidate", "children": [
            {"node_id": "ground_interaction", "parts": sorted(work083["part_step_sha256"])},
            {"node_id": "energy_torque_path", "parts": sorted(work084["part_step_sha256"])},
            {"node_id": "integration", "parts": ["coolant_inlet_route", "coolant_outlet_route", "energy_mount_adapter", "ground_mount_adapter", "upper_load_bridge"]},
        ]},
        "part_count": 17,
    }
    joint_dof = {
        "ground_interaction_declared_mobility_dof": 2,
        "energy_torque_declared_mobility_dof": 1,
        "vertical_travel_m": 0.014,
        "interface_maximum_misalignment_m": evaluation["motion_interface"]["maximum_misalignment_m"],
        "interface_tolerance_m": evaluation["motion_interface"]["tolerance_m"],
        "interface_status": "blocked",
    }
    material = {
        "evidence_class": "synthetic_verification",
        "design_use_allowed": False,
        "physical_validation_claim_allowed": False,
        "material_record_sha256": "72a1b5527e4aede10c6de73523c54835f11458f80100c6383d2a304d4d912097",
    }
    mass = {key: geometry[key] for key in ("total_mass_kg", "centre_of_mass_m", "inertia_tensor_kg_m2")}
    interference = {
        "status": "failed",
        "positive_overlap_pairs": geometry["interfering_pairs"],
        "positive_overlap_count": len(geometry["interfering_pairs"]),
        "maximum_overlap_m3": geometry["maximum_overlap_m3"],
        "minimum_forbidden_clearance_m": geometry["minimum_forbidden_clearance_m"],
    }
    structural = {
        "component_mesh_status": "passed_synthetic_only",
        "component_cases": work086["cases"],
        "new_load_frame_mesh_status": "missing",
        "whole_candidate_structural_status": "blocked",
        "design_use_allowed": False,
    }
    energy = {
        "torque_energy_source_result_sha256": work084["result_sha256"],
        "integration_load_cases": evaluation["load_cases"],
        "thermal": evaluation["thermal"],
        "status": "algebraic_ledgers_passed_but_candidate_not_admitted",
    }
    failures = {
        "work083_controls": "passed",
        "work084_controls": "passed",
        "work087_controls": evaluation["controls"],
        "whole_candidate_failure_propagation": "not_executed_due_to_pre_admission_blockers",
    }
    replay = {
        "random_seed": config["random_seed"],
        "config_sha256": canonical_sha256(config),
        "source_file_sha256": evidence["source_file_sha256"],
        "part_step_sha256": evidence["part_step_sha256"],
        "assembly_step_sha256": evidence["assembly_step_sha256"],
        "freecad_file_sha256": evidence["freecad_file_sha256"],
        "result_conditioned_geometry_mutation": False,
    }
    level0 = admission["level0_simulation"] | {"candidate_verdict": admission["candidate_verdict"]}
    return {
        "admission_report.json": admission,
        "assembly_tree.json": assembly_tree,
        "joint_dof_manifest.json": joint_dof,
        "material_manifest.json": material,
        "mass_com_inertia_report.json": mass,
        "interference_report.json": interference,
        "structural_load_case_report.json": structural,
        "torque_power_energy_ledger.json": energy,
        "failure_propagation_report.json": failures,
        "deterministic_replay_manifest.json": replay,
        "level0_simulation_decision.json": level0,
        "geometry_artifact_index.json": {
            "individual_step_per_part": evidence["part_step_sha256"],
            "complete_assembly_step_sha256": evidence["assembly_step_sha256"],
            "freecad_fcstd_sha256": evidence["freecad_file_sha256"],
        },
    }
