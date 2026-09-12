"""Strict native detailed-vehicle evidence contract for Work 135.

The module deliberately contains no CAD-kernel dependency.  It validates the
frozen declaration and the evidence emitted by the CadQuery and FreeCAD
adapters.  Geometry construction and inspection remain separate executables so
missing kernels cannot be mistaken for a passing in-process fallback.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, deque
from pathlib import Path
from typing import Any, Mapping, Sequence


PROTOCOL_VERSION = "native_detailed_vehicle_v1"
FINAL_STATUS = "passed_native_detailed_geometry"
REQUIRED_WORKS = {108, 110, *range(112, 124), 125, 126, 129, 130}
REQUIRED_BOUNDARY_DOMAINS = {
    "structural",
    "thermal",
    "internal_flow",
    "external_aero",
    "ground_motion",
    "energy",
    "control_sensor",
}
REQUIRED_TOP_LEVEL = {
    "protocol_version",
    "units",
    "candidate",
    "dependencies",
    "upstream_part_audit",
    "runtimes",
    "materials",
    "thresholds",
    "required_occurrence_classes",
    "definitions",
    "instances",
    "routes",
    "motion",
    "physics_boundaries",
    "replay",
    "experiment",
}


class NativeDetailedVehicleViolation(ValueError):
    """Raised whenever native detailed-vehicle evidence is inadmissible."""


def canonical_sha256(value: Any) -> str:
    try:
        payload = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise NativeDetailedVehicleViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise NativeDetailedVehicleViolation(message)


def _finite_number(value: Any, name: str) -> float:
    _require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{name} must be numeric")
    result = float(value)
    _require(math.isfinite(result), f"{name} must be finite")
    return result


def _vector(value: Any, length: int, name: str) -> list[float]:
    _require(isinstance(value, list) and len(value) == length, f"{name} must have {length} entries")
    return [_finite_number(item, f"{name}[{index}]") for index, item in enumerate(value)]


def _unit_axis(value: Any, name: str) -> list[float]:
    axis = _vector(value, 3, name)
    norm = math.sqrt(sum(item * item for item in axis))
    _require(abs(norm - 1.0) <= 1.0e-12, f"{name} must be a unit vector")
    return axis


def _sha256_text(value: Any, name: str) -> str:
    _require(isinstance(value, str) and len(value) == 64, f"{name} must be a SHA-256")
    _require(all(character in "0123456789abcdef" for character in value), f"{name} must be lowercase hexadecimal")
    return value


def _validate_dependencies(raw: Mapping[str, Any]) -> None:
    works = [item.get("work") for item in raw["dependencies"]]
    _require(set(works) == REQUIRED_WORKS and len(works) == len(REQUIRED_WORKS), "required dependency set mismatch")
    for item in raw["dependencies"]:
        work = item["work"]
        _require(isinstance(item.get("commit"), str) and len(item["commit"]) == 40, f"Work {work} commit is not pinned")
        for key in ("contract_path", "result_log_path", "artifact_result_path"):
            _require(isinstance(item.get(key), str) and item[key], f"Work {work} {key} is missing")
        for key in ("contract_sha256", "result_log_sha256", "artifact_file_sha256", "artifact_result_sha256"):
            _sha256_text(item.get(key), f"Work {work} {key}")


def _validate_materials(raw: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    materials: dict[str, Mapping[str, Any]] = {}
    for item in raw["materials"]:
        material_id = item.get("material_id")
        _require(isinstance(material_id, str) and material_id and material_id not in materials, "duplicate or empty material identity")
        density = _finite_number(item.get("density_kg_m3"), f"material {material_id} density")
        _require(density >= 0.0, f"material {material_id} density must be nonnegative")
        _require(item.get("evidence_class") in {"project_native_geometry", "synthetic_upstream_geometry_only", "void"}, f"material {material_id} evidence class is inadmissible")
        _require(item.get("geometry_only_eligible") is True, f"material {material_id} is not geometry-gate eligible")
        if item.get("structural_mass"):
            _require(density > 0.0, f"structural material {material_id} requires positive density")
        else:
            _require(density == 0.0, f"void material {material_id} must have zero structural density")
        materials[material_id] = item
    _require(any(item.get("structural_mass") for item in materials.values()), "no material mass is declared")
    _require(any(not item.get("structural_mass") for item in materials.values()), "no void material is declared")
    return materials


def _validate_definitions(raw: Mapping[str, Any], materials: Mapping[str, Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    definitions: dict[str, Mapping[str, Any]] = {}
    for item in raw["definitions"]:
        definition_id = item.get("definition_id")
        _require(isinstance(definition_id, str) and definition_id and definition_id not in definitions, "duplicate or empty definition identity")
        _require(item.get("representation") == "native_occt_brep", f"definition {definition_id} is not native B-rep")
        _require(item.get("solid_policy") == "one_closed_solid", f"definition {definition_id} solid policy is not admitted")
        _require(item.get("finished_form") is True, f"definition {definition_id} is not a finished form")
        _require(item.get("material_id") in materials, f"definition {definition_id} has unknown material")
        region_kind = item.get("region_kind")
        _require(region_kind in {"material", "void"}, f"definition {definition_id} region kind is invalid")
        material = materials[item["material_id"]]
        _require((region_kind == "material") == bool(material["structural_mass"]), f"definition {definition_id} material/void ownership mismatch")
        provenance = item.get("provenance", {})
        _require(provenance.get("kind") in {"project_native_manufactured", "evidence_bound_purchased"}, f"definition {definition_id} provenance is inadmissible")
        if provenance.get("kind") == "evidence_bound_purchased":
            _require(provenance.get("proxy") is False, f"definition {definition_id} uses an unsupported purchased proxy")
            _require(all(provenance.get(key) for key in ("supplier", "source_uri", "source_sha256")), f"definition {definition_id} purchased source is incomplete")
        geometry = item.get("geometry", {})
        _require(isinstance(geometry.get("kind"), str) and geometry["kind"], f"definition {definition_id} geometry kind is missing")
        _require(geometry.get("primitive_replacement") is False, f"definition {definition_id} is a same-envelope primitive substitution")
        features = item.get("feature_inventory")
        _require(isinstance(features, list) and len(features) >= 2 and len(features) == len(set(features)), f"definition {definition_id} feature inventory is incomplete")
        selectors = item.get("semantic_face_selectors")
        _require(isinstance(selectors, list) and selectors and len(selectors) == len(set(selectors)), f"definition {definition_id} semantic face selectors are incomplete")
        _require(not any(str(value).startswith(("Face", "Edge")) for value in selectors), f"definition {definition_id} uses persistent raw topology identity")
        _require(isinstance(item.get("process_id"), str) and item["process_id"], f"definition {definition_id} process identity is missing")
        definitions[definition_id] = item
    return definitions


def _validate_instances(
    raw: Mapping[str, Any], definitions: Mapping[str, Mapping[str, Any]]
) -> tuple[dict[str, Mapping[str, Any]], dict[str, int]]:
    instances: dict[str, Mapping[str, Any]] = {}
    regions: set[str] = set()
    occurrence_counts: Counter[str] = Counter()
    for item in raw["instances"]:
        instance_id = item.get("instance_id")
        _require(isinstance(instance_id, str) and instance_id and instance_id not in instances, "duplicate or empty instance identity")
        _require(item.get("definition_id") in definitions, f"instance {instance_id} has unknown definition")
        region_id = item.get("region_id")
        _require(isinstance(region_id, str) and region_id and region_id not in regions, "duplicate material/void ownership")
        regions.add(region_id)
        _vector(item.get("translation_m"), 3, f"instance {instance_id} translation")
        _vector(item.get("rotation_deg_xyz"), 3, f"instance {instance_id} rotation")
        classes = item.get("occurrence_classes")
        _require(isinstance(classes, list) and classes and len(classes) == len(set(classes)), f"instance {instance_id} occurrence classes are incomplete")
        occurrence_counts.update(classes)
        _require(item.get("mass_ownership") in {"unique_material", "zero_mass_void"}, f"instance {instance_id} mass ownership is invalid")
        definition = definitions[item["definition_id"]]
        expected = "unique_material" if definition["region_kind"] == "material" else "zero_mass_void"
        _require(item["mass_ownership"] == expected, f"instance {instance_id} mass ownership contradicts its definition")
        instances[instance_id] = item
    required = set(raw["required_occurrence_classes"])
    _require(required and len(required) == len(raw["required_occurrence_classes"]), "required occurrence classes are empty or duplicated")
    missing = sorted(item for item in required if occurrence_counts[item] == 0)
    _require(not missing, "missing required physical occurrence: " + ",".join(missing))
    return instances, dict(occurrence_counts)


def _validate_attachment_graph(raw: Mapping[str, Any], instances: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    root = raw["candidate"].get("root_instance_id")
    _require(root in instances, "assembly root instance is missing")
    parents: dict[str, str] = {}
    relation_types: Counter[str] = Counter()
    for instance_id, item in instances.items():
        attachment = item.get("attachment")
        if instance_id == root:
            _require(attachment is None, "assembly root must not have a parent attachment")
            continue
        _require(isinstance(attachment, dict), f"floating component: {instance_id}")
        parent = attachment.get("parent_instance_id")
        _require(parent in instances and parent != instance_id, f"floating component: {instance_id}")
        _require(instance_id not in parents, f"duplicate attachment for {instance_id}")
        parents[instance_id] = parent
        relation_type = attachment.get("relation_type")
        _require(isinstance(relation_type, str) and relation_type, f"instance {instance_id} relation type is missing")
        relation_types[relation_type] += 1
        approved_noncontact = attachment.get("approved_noncontact")
        _require(isinstance(approved_noncontact, bool), f"instance {instance_id} relation contact class is missing")
        if approved_noncontact:
            _require(isinstance(attachment.get("justification"), str) and attachment["justification"], f"instance {instance_id} non-contact relation lacks justification")
        else:
            for key in ("parent_face", "child_face"):
                selector = attachment.get(key)
                definition = definitions_for(instances[parent if key == "parent_face" else instance_id], raw)
                _require(selector in definition["semantic_face_selectors"], f"instance {instance_id} lost semantic mating face")
            parent_anchor = _vector(attachment.get("parent_anchor_m"), 3, f"instance {instance_id} parent anchor")
            child_anchor = _vector(attachment.get("child_anchor_m"), 3, f"instance {instance_id} child anchor")
            residual = math.dist(parent_anchor, child_anchor)
            _require(residual <= raw["thresholds"]["mate_residual_m"], f"instance {instance_id} mating residual failed")
            parent_axis = _unit_axis(attachment.get("parent_axis"), f"instance {instance_id} parent axis")
            child_axis = _unit_axis(attachment.get("child_axis"), f"instance {instance_id} child axis")
            dot = sum(left * right for left, right in zip(parent_axis, child_axis))
            _require(abs(abs(dot) - 1.0) <= 1.0e-12, f"instance {instance_id} mating axes mismatch")
            tolerance = attachment.get("tolerance_stack_m", {})
            low = _finite_number(tolerance.get("minimum"), f"instance {instance_id} minimum tolerance")
            high = _finite_number(tolerance.get("maximum"), f"instance {instance_id} maximum tolerance")
            nominal = _finite_number(attachment.get("nominal_gap_m"), f"instance {instance_id} nominal gap")
            _require(low <= nominal <= high, f"instance {instance_id} nominal-only tolerance declaration")
            _require(attachment.get("worst_case_status") == "passed", f"instance {instance_id} worst-case tolerance failed")
            ownership = attachment.get("ownership", {})
            _require(any(ownership.get(name) for name in ("load", "energy", "signal", "heat", "seal")), f"instance {instance_id} interface ownership is empty")
            if relation_type == "bolted":
                fasteners = attachment.get("fastener_instance_ids")
                _require(isinstance(fasteners, list) and fasteners, f"instance {instance_id} bolted joint has missing engagement")
                for fastener in fasteners:
                    _require(fastener in instances and "fastener" in instances[fastener]["occurrence_classes"], f"instance {instance_id} fastener identity is invalid")
                _require(_finite_number(attachment.get("engagement_m"), f"instance {instance_id} engagement") > 0.0, f"instance {instance_id} missing engagement")
            if attachment.get("sealed"):
                seals = attachment.get("seal_instance_ids")
                _require(isinstance(seals, list) and seals, f"instance {instance_id} seal is missing")
                for seal in seals:
                    _require(seal in instances and "seal" in instances[seal]["occurrence_classes"], f"instance {instance_id} seal identity is invalid")
                compression = _finite_number(attachment.get("seal_compression_fraction"), f"instance {instance_id} seal compression")
                limits = _vector(attachment.get("seal_compression_range"), 2, f"instance {instance_id} seal compression range")
                _require(limits[0] <= compression <= limits[1], f"instance {instance_id} seal compression failed")

    for start in instances:
        seen: set[str] = set()
        current = start
        while current != root:
            _require(current not in seen, "cyclic assembly order")
            seen.add(current)
            _require(current in parents, f"floating component: {current}")
            current = parents[current]
    return {"root_instance_id": root, "attached_instance_count": len(parents), "relation_type_counts": dict(sorted(relation_types.items()))}


def definitions_for(instance: Mapping[str, Any], raw: Mapping[str, Any]) -> Mapping[str, Any]:
    definition_id = instance["definition_id"]
    for definition in raw["definitions"]:
        if definition["definition_id"] == definition_id:
            return definition
    raise NativeDetailedVehicleViolation(f"unknown definition {definition_id}")


def _validate_routes(raw: Mapping[str, Any], instances: Mapping[str, Mapping[str, Any]]) -> None:
    routed_instances: set[str] = set()
    for route in raw["routes"]:
        instance_id = route.get("instance_id")
        _require(instance_id in instances and instance_id not in routed_instances, "route identity is missing or duplicated")
        routed_instances.add(instance_id)
        _vector(route.get("endpoint_a_m"), 3, f"route {instance_id} endpoint A")
        _vector(route.get("endpoint_b_m"), 3, f"route {instance_id} endpoint B")
        _require(route["endpoint_a_m"] != route["endpoint_b_m"], f"route {instance_id} endpoints collapse")
        required_radius = _finite_number(route.get("minimum_bend_radius_m"), f"route {instance_id} minimum bend radius")
        actual_radius = _finite_number(route.get("actual_minimum_bend_radius_m"), f"route {instance_id} actual bend radius")
        clearance = _finite_number(route.get("minimum_clearance_m"), f"route {instance_id} minimum clearance")
        _require(actual_radius >= required_radius, f"route {instance_id} bend-radius failure")
        _require(clearance >= 0.0, f"route {instance_id} intersection failure")
    required_route_instances = {
        instance_id
        for instance_id, item in instances.items()
        if set(item["occurrence_classes"]) & {"power_harness", "signal_harness", "coolant_tube", "fluid_void"}
    }
    _require(routed_instances == required_route_instances, "route endpoint coverage is incomplete")


def _validate_motion(raw: Mapping[str, Any], instances: Mapping[str, Mapping[str, Any]]) -> None:
    motion = raw["motion"]
    _require(motion.get("moving_instance_id") in instances, "motion component is missing")
    _unit_axis(motion.get("axis"), "motion axis")
    sample_count = motion.get("sample_count")
    _require(isinstance(sample_count, int) and not isinstance(sample_count, bool) and sample_count >= 101, "motion requires at least 101 samples")
    sample_range = _vector(motion.get("sample_range_rad"), 2, "motion sample range")
    _require(sample_range[0] < sample_range[1], "motion sample range is not ordered")
    convergence = _finite_number(motion.get("successive_minimum_clearance_change_m"), "motion refinement convergence")
    _require(convergence <= raw["thresholds"]["motion_clearance_convergence_m"], "motion refinement did not converge")
    _require(_finite_number(motion.get("minimum_clearance_m"), "motion minimum clearance") >= 0.0, "swept motion collision")
    _require(motion.get("analytic_swept_envelope") is True, "analytic swept envelope is required for the registered axial motion")
    _require(isinstance(motion.get("between_sample_risk"), str) and motion["between_sample_risk"], "between-sample risk disclosure is missing")


def _validate_boundaries(raw: Mapping[str, Any], instances: Mapping[str, Mapping[str, Any]]) -> None:
    domains: set[str] = set()
    boundary_ids: set[str] = set()
    for boundary in raw["physics_boundaries"]:
        boundary_id = boundary.get("boundary_id")
        _require(isinstance(boundary_id, str) and boundary_id and boundary_id not in boundary_ids, "physics boundary identity is empty or duplicated")
        boundary_ids.add(boundary_id)
        domain = boundary.get("domain")
        _require(domain in REQUIRED_BOUNDARY_DOMAINS, f"unknown physics boundary domain {domain}")
        domains.add(domain)
        instance_id = boundary.get("instance_id")
        _require(instance_id in instances, f"physics boundary {boundary_id} has unknown instance")
        definition = definitions_for(instances[instance_id], raw)
        selector = boundary.get("semantic_face_selector")
        _require(selector in definition["semantic_face_selectors"], f"physics boundary {boundary_id} lost semantic face")
        _require(isinstance(boundary.get("role"), str) and boundary["role"], f"physics boundary {boundary_id} has no role")
    _require(domains == REQUIRED_BOUNDARY_DOMAINS, "physics boundary domain coverage is incomplete")


def validate_declaration(raw: Mapping[str, Any]) -> dict[str, Any]:
    _require(set(raw) == REQUIRED_TOP_LEVEL, "protocol schema mismatch")
    _require(raw.get("protocol_version") == PROTOCOL_VERSION, "protocol identity mismatch")
    _require(raw.get("units") == "SI_m_kg_s_K_N_Pa_W_J_rad", "SI unit declaration mismatch")
    candidate = raw["candidate"]
    _require(candidate.get("candidate_id") not in {None, "", "final_126_r1"}, "new candidate identity is required")
    _require(candidate.get("revision") == "r1", "candidate revision mismatch")
    _require(candidate.get("source_geometry_policy") == "work126_function_checklist_only", "Work 126 geometry inheritance is prohibited")
    _require(candidate.get("claim_scope") == "native_geometry_and_assembly_only", "claim scope exceeds Work 135")
    energy_boundary = candidate.get("primary_energy_boundary", {})
    _require(energy_boundary.get("onboard_pre_race") is True and energy_boundary.get("external_replenishment") == "prohibited", "primary-energy boundary is not closed")
    _require(candidate.get("safety_scope") == "digital_geometry_only_no_fabrication_authority", "safety scope mismatch")
    _validate_dependencies(raw)
    for audit in raw["upstream_part_audit"]:
        _require(audit.get("work") in {83, 84, 87, 108, 113}, "unexpected upstream part audit")
        _sha256_text(audit.get("sha256"), f"Work {audit.get('work')} audit hash")
        _require(audit.get("disposition") in {"regenerate_for_candidate", "reuse_exact"}, "upstream part audit disposition is unresolved")
        _require(isinstance(audit.get("reason"), str) and audit["reason"], "upstream part audit reason is missing")
    _require({item["work"] for item in raw["upstream_part_audit"]} == {83, 84, 87, 108, 113}, "upstream part audit is incomplete")
    for runtime in raw["runtimes"]:
        _require(all(runtime.get(key) for key in ("runtime_id", "path", "version", "sha256")), "runtime identity is incomplete")
        _sha256_text(runtime["sha256"], f"runtime {runtime['runtime_id']} hash")
    _require({item["runtime_id"] for item in raw["runtimes"]} == {"cadquery_python", "cadquery", "freecad_python", "freecad", "occt", "gmsh", "calculix"}, "runtime set is incomplete")
    thresholds = raw["thresholds"]
    required_thresholds = {
        "volume_relative",
        "mass_relative",
        "center_absolute_m",
        "inertia_relative",
        "mate_residual_m",
        "noncontact_penetration_m3",
        "motion_clearance_convergence_m",
        "preview_chord_m",
    }
    _require(set(thresholds) == required_thresholds, "threshold set mismatch")
    for key in required_thresholds:
        _require(_finite_number(thresholds[key], key) >= 0.0, f"threshold {key} must be nonnegative")
    _require(thresholds["volume_relative"] <= 1.0e-8 and thresholds["mass_relative"] <= 1.0e-8, "mass/volume cross-import thresholds were weakened")
    _require(thresholds["center_absolute_m"] <= 1.0e-7 and thresholds["inertia_relative"] <= 1.0e-7, "center/inertia thresholds were weakened")
    _require(thresholds["mate_residual_m"] <= 1.0e-6 and thresholds["noncontact_penetration_m3"] <= 1.0e-12, "assembly thresholds were weakened")
    _require(thresholds["motion_clearance_convergence_m"] <= 1.0e-5 and thresholds["preview_chord_m"] <= 2.5e-4, "motion/preview thresholds were weakened")
    materials = _validate_materials(raw)
    definitions = _validate_definitions(raw, materials)
    instances, occurrence_counts = _validate_instances(raw, definitions)
    graph = _validate_attachment_graph(raw, instances)
    _validate_routes(raw, instances)
    _validate_motion(raw, instances)
    _validate_boundaries(raw, instances)
    replay = raw["replay"]
    _require(replay.get("pilot_reusable_as_admitted") is False, "pilot output cannot be admitted")
    _require(replay.get("required_runs") == ["run_a", "run_b"], "clean replay run identities mismatch")
    _require(replay.get("exact_hash_match") is True, "exact replay requirement is missing")
    experiment = raw["experiment"]
    for key in ("independent_variables", "dependent_variables", "controls", "metrics", "success_criteria", "failure_criteria", "falsification_review"):
        _require(isinstance(experiment.get(key), list) and experiment[key], f"experiment {key} is missing")
    return {
        "status": "passed",
        "protocol_sha256": canonical_sha256(raw),
        "definition_count": len(definitions),
        "instance_count": len(instances),
        "material_instance_count": sum(definitions[item["definition_id"]]["region_kind"] == "material" for item in instances.values()),
        "void_instance_count": sum(definitions[item["definition_id"]]["region_kind"] == "void" for item in instances.values()),
        "required_occurrence_count": len(raw["required_occurrence_classes"]),
        "occurrence_counts": dict(sorted(occurrence_counts.items())),
        "assembly_graph": graph,
    }


def _relative(actual: float, expected: float, floor: float = 1.0e-300) -> float:
    return abs(actual - expected) / max(abs(expected), floor)


def _verify_artifact_hashes(manifest: Mapping[str, Any], artifact_root: Path | None) -> None:
    if artifact_root is None:
        return
    paths: list[tuple[str, str]] = []
    for definition in manifest["definitions"]:
        paths.append((definition["step_path"], definition["step_sha256"]))
    for instance in manifest["instances"]:
        paths.append((instance["step_path"], instance["step_sha256"]))
    for key in ("material_assembly", "void_assembly"):
        paths.append((manifest[key]["step_path"], manifest[key]["step_sha256"]))
    for relative_path, expected in paths:
        path = artifact_root / relative_path
        _require(path.is_file(), f"native STEP artifact is missing: {relative_path}")
        _require(file_sha256(path) == expected, f"swapped or edited STEP bytes: {relative_path}")


def evaluate_admitted_evidence(
    raw: Mapping[str, Any],
    cad_manifest: Mapping[str, Any] | None,
    freecad_report: Mapping[str, Any] | None,
    *,
    artifact_root: str | Path | None = None,
) -> dict[str, Any]:
    declaration = validate_declaration(raw)
    _require(cad_manifest is not None, "native-solid manifest is required; render-only evidence is rejected")
    _require(freecad_report is not None, "exact FreeCAD import witness is required")
    root = Path(artifact_root) if artifact_root is not None else None
    _verify_artifact_hashes(cad_manifest, root)
    _require(cad_manifest.get("status") == "passed", "invalid native geometry")
    _require(cad_manifest.get("candidate_id") == raw["candidate"]["candidate_id"], "candidate identity mismatch")
    _require(cad_manifest.get("declaration_sha256") == declaration["protocol_sha256"], "declaration identity mismatch")
    _require(cad_manifest.get("hidden_geometry_repair") is False, "hidden geometry repair")
    _require(len(cad_manifest.get("definitions", [])) == declaration["definition_count"], "native definition count mismatch")
    _require(len(cad_manifest.get("instances", [])) == declaration["instance_count"], "native instance count mismatch")
    for record in cad_manifest["definitions"]:
        _require(record.get("valid") is True and record.get("solid_count") == 1, f"invalid native part: {record.get('definition_id')}")
        _require(record.get("closed") is True, f"open or non-manifold native part: {record.get('definition_id')}")
        _require(record.get("feature_count", 0) >= 2, f"native part feature inventory missing: {record.get('definition_id')}")
        _require(record.get("semantic_faces"), f"native part semantic faces missing: {record.get('definition_id')}")
    _require(cad_manifest["material_assembly"].get("solid_count") == declaration["material_instance_count"], "material assembly solid count mismatch")
    _require(cad_manifest["void_assembly"].get("solid_count") == declaration["void_instance_count"], "void assembly solid count mismatch")
    collision = cad_manifest.get("collision_clearance", {})
    _require(
        _finite_number(collision.get("maximum_noncontact_penetration_m3"), "non-contact penetration")
        <= raw["thresholds"]["noncontact_penetration_m3"],
        "non-contact penetration failed",
    )
    _require(collision.get("boolean_failures") == [], "collision boolean failure is observable and blocks admission")
    motion = cad_manifest.get("motion", {})
    _require(motion.get("sample_count", 0) >= 101, "motion evidence is undersampled")
    _require(motion.get("collision_count") == 0, "swept motion collision")
    _require(motion.get("successive_minimum_clearance_change_m", math.inf) <= raw["thresholds"]["motion_clearance_convergence_m"], "motion evidence did not converge")
    _require(cad_manifest.get("occurrence_coverage_fraction") == 1.0, "incomplete part realization")
    _require(cad_manifest.get("unknown_essential_occurrences") == [], "unknown essential occurrence")
    _require(cad_manifest.get("physics_boundary_coverage_fraction") == 1.0, "physics mapping unresolved")

    _require(freecad_report.get("status") == "passed", "FreeCAD exact import failed")
    _require(freecad_report.get("hidden_geometry_repair") is False, "hidden FreeCAD repair")
    _require(len(freecad_report.get("definitions", [])) == declaration["definition_count"], "FreeCAD definition count mismatch")
    _require(len(freecad_report.get("instances", [])) == declaration["instance_count"], "FreeCAD instance count mismatch")
    for record in freecad_report["definitions"]:
        _require(record.get("valid") is True and record.get("solid_count") == 1, f"FreeCAD invalid native definition: {record.get('definition_id')}")
    for record in freecad_report["instances"]:
        _require(record.get("valid") is True and record.get("solid_count") == 1, f"FreeCAD invalid native instance: {record.get('instance_id')}")
    _require(freecad_report.get("material_assembly", {}).get("solid_count") == declaration["material_instance_count"], "FreeCAD material solid count mismatch")
    _require(freecad_report.get("void_assembly", {}).get("solid_count") == declaration["void_instance_count"], "FreeCAD void solid count mismatch")
    residuals = freecad_report.get("maximum_residuals", {})
    limits = raw["thresholds"]
    _require(_finite_number(residuals.get("volume_relative"), "volume residual") <= limits["volume_relative"], "FreeCAD volume residual failed")
    _require(_finite_number(residuals.get("mass_relative"), "mass residual") <= limits["mass_relative"], "FreeCAD mass residual failed")
    _require(_finite_number(residuals.get("center_absolute_m"), "center residual") <= limits["center_absolute_m"], "FreeCAD center residual failed")
    _require(_finite_number(residuals.get("inertia_relative"), "inertia residual") <= limits["inertia_relative"], "FreeCAD inertia residual failed")
    _require(freecad_report.get("semantic_boundary_survival_rate") == 1.0, "lost semantic face or boundary after import")
    _require(freecad_report.get("step_hash_match") is True, "FreeCAD inspected different STEP bytes")
    _require(freecad_report.get("invalid_or_null_solids") == 0, "FreeCAD found invalid or null solids")

    return {
        "status": FINAL_STATUS,
        "claim_scope": "native geometry, assembly, ownership, interfaces and boundary availability only",
        "declaration": declaration,
        "definition_count": declaration["definition_count"],
        "instance_count": declaration["instance_count"],
        "required_occurrence_coverage": 1.0,
        "unknown_essential_occurrences": [],
        "mass_properties": freecad_report["mass_properties"],
        "maximum_residuals": residuals,
        "maximum_noncontact_penetration_m3": collision["maximum_noncontact_penetration_m3"],
        "motion": motion,
        "semantic_boundary_survival_rate": 1.0,
        "downstream_physics_revalidation_required": True,
        "promotion_allowed": False,
    }


def replay_projection(result: Mapping[str, Any]) -> dict[str, Any]:
    """Return only evidence fields required to match across clean runs."""

    return {
        "result_sha256": result["result_sha256"],
        "artifact_sha256": result["body"]["artifact_sha256"],
        "candidate_id": result["body"]["candidate_id"],
        "status": result["body"]["status"],
    }


__all__ = [
    "FINAL_STATUS",
    "NativeDetailedVehicleViolation",
    "PROTOCOL_VERSION",
    "canonical_sha256",
    "evaluate_admitted_evidence",
    "file_sha256",
    "replay_projection",
    "validate_declaration",
]
