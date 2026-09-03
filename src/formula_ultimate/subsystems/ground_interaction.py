"""Fail-closed Work 083 ground-interaction candidate evaluation."""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "ground_interaction_candidate_v1"
REQUIRED_CONTROLS = {
    "mirror",
    "rigid_no_travel",
    "disconnected_mount",
    "blocked_translation",
    "seized_rotation",
    "broken_torque_path",
    "undersized_capacity",
    "contact_loss",
}


class GroundInteractionViolation(ValueError):
    """Raised when declaration or evidence cannot support the bounded claim."""


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise GroundInteractionViolation(f"{label} must be a mapping")
    return value


def _exact(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise GroundInteractionViolation(
            f"{label} fields mismatch: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}"
        )


def _finite(value: Any, label: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise GroundInteractionViolation(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0.0):
        raise GroundInteractionViolation(f"{label} is outside its finite domain")
    return result


def _vector3(value: Any, label: str) -> tuple[float, float, float]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 3:
        raise GroundInteractionViolation(f"{label} must contain three values")
    return tuple(_finite(item, f"{label}[{index}]") for index, item in enumerate(value))  # type: ignore[return-value]


def _sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise GroundInteractionViolation(f"{label} must be a lowercase SHA-256")
    return value


def _unique_path_count(edges: Sequence[Sequence[str]], source: str, target: str) -> int:
    graph: dict[str, set[str]] = defaultdict(set)
    for index, edge in enumerate(edges):
        if not isinstance(edge, Sequence) or isinstance(edge, (str, bytes)) or len(edge) != 2:
            raise GroundInteractionViolation(f"path edge {index} must have two endpoints")
        a, b = edge
        if not isinstance(a, str) or not isinstance(b, str) or a == b:
            raise GroundInteractionViolation(f"path edge {index} is invalid")
        graph[a].add(b)
        graph[b].add(a)

    count = 0

    def visit(node: str, seen: set[str]) -> None:
        nonlocal count
        if count > 1:
            return
        if node == target:
            count += 1
            return
        for nxt in sorted(graph[node] - seen):
            visit(nxt, seen | {nxt})

    visit(source, {source})
    return count


def validate_declaration(raw: Mapping[str, Any]) -> dict[str, Any]:
    _exact(
        raw,
        {
            "schema_version", "candidate_id", "claim_level", "coordinate_system", "parts",
            "joints", "motion", "clearance", "ground_interface", "torque_case", "paths",
            "capacity", "structural_evidence", "gates", "controls", "evidence_policy", "non_claims",
        },
        "declaration",
    )
    if raw["schema_version"] != SCHEMA_VERSION:
        raise GroundInteractionViolation("unsupported schema_version")
    if raw["candidate_id"] != "ground_interaction_candidate_001":
        raise GroundInteractionViolation("unexpected candidate_id")

    coordinate = _mapping(raw["coordinate_system"], "coordinate_system")
    _exact(coordinate, {"units", "x_axis", "y_axis", "z_axis"}, "coordinate_system")
    if coordinate != {"units": "SI", "x_axis": "longitudinal_forward", "y_axis": "lateral_left", "z_axis": "vertical_up"}:
        raise GroundInteractionViolation("coordinate system must use the frozen SI frame")

    parts = raw["parts"]
    if not isinstance(parts, list):
        raise GroundInteractionViolation("parts must be a list")
    part_ids: list[str] = []
    for index, item_raw in enumerate(parts):
        item = _mapping(item_raw, f"parts[{index}]")
        _exact(item, {"part_id", "role", "geometry", "synthetic_density_kg_per_m3"}, f"parts[{index}]")
        if not isinstance(item["part_id"], str) or not item["part_id"]:
            raise GroundInteractionViolation("part_id must be non-empty")
        _finite(item["synthetic_density_kg_per_m3"], "synthetic density", positive=True)
        _mapping(item["geometry"], "part geometry")
        part_ids.append(item["part_id"])
    if len(part_ids) != len(set(part_ids)):
        raise GroundInteractionViolation("part ids must be unique")

    gates = _mapping(raw["gates"], "gates")
    _exact(gates, {"required_part_count", "required_mobility_dof", "force_residual_relative", "moment_residual_relative", "energy_residual_relative"}, "gates")
    if len(parts) != gates["required_part_count"] or gates["required_part_count"] != 5:
        raise GroundInteractionViolation("the frozen candidate requires five parts")

    joints = raw["joints"]
    if not isinstance(joints, list) or len(joints) != 5:
        raise GroundInteractionViolation("five joint declarations are required")
    constraint_rows = 0
    children: set[str] = set()
    for index, joint_raw in enumerate(joints):
        joint = _mapping(joint_raw, f"joints[{index}]")
        allowed = {"joint_id", "parent", "child", "type", "constraint_rows"}
        if joint.get("type") in {"prismatic", "revolute"}:
            allowed.add("axis")
        _exact(joint, allowed, f"joints[{index}]")
        if joint["child"] not in part_ids or joint["child"] in children:
            raise GroundInteractionViolation("each part must be constrained exactly once")
        children.add(joint["child"])
        rows = joint["constraint_rows"]
        if isinstance(rows, bool) or not isinstance(rows, int) or rows not in {5, 6}:
            raise GroundInteractionViolation("joint constraint_rows must be five or six")
        expected_rows = 5 if joint["type"] in {"prismatic", "revolute"} else 6
        if rows != expected_rows:
            raise GroundInteractionViolation("joint constraint rows disagree with joint type")
        if "axis" in joint:
            axis = _vector3(joint["axis"], "joint axis")
            if not math.isclose(math.sqrt(sum(x * x for x in axis)), 1.0, rel_tol=0.0, abs_tol=1e-12):
                raise GroundInteractionViolation("joint axis must be a unit vector")
        constraint_rows += rows
    mobility = 6 * len(parts) - constraint_rows
    if mobility != gates["required_mobility_dof"] or mobility != 2:
        raise GroundInteractionViolation("calculated mobility does not equal two DOF")

    motion = _mapping(raw["motion"], "motion")
    _exact(motion, {"translation_axis", "travel_min_m", "travel_max_m", "reference_translation_m", "moving_parts"}, "motion")
    if _vector3(motion["translation_axis"], "translation_axis") != (0.0, 0.0, 1.0):
        raise GroundInteractionViolation("translation must use the declared vertical axis")
    lo = _finite(motion["travel_min_m"], "travel_min_m")
    hi = _finite(motion["travel_max_m"], "travel_max_m")
    ref = _finite(motion["reference_translation_m"], "reference_translation_m")
    if not lo < ref < hi:
        raise GroundInteractionViolation("reference translation must lie strictly inside travel")
    if set(motion["moving_parts"]) != {"carrier", "axle", "contact_roller"}:
        raise GroundInteractionViolation("moving part set changed")

    ground = _mapping(raw["ground_interface"], "ground_interface")
    _exact(ground, {"contact_part_id", "contact_point_m", "force_on_candidate_n", "force_direction_angle_rad"}, "ground_interface")
    point = _vector3(ground["contact_point_m"], "contact_point_m")
    force = _vector3(ground["force_on_candidate_n"], "force_on_candidate_n")
    if ground["contact_part_id"] != "contact_roller" or force[2] <= 0.0:
        raise GroundInteractionViolation("reference ground contact must have positive normal force")
    expected_angle = math.atan2(force[1], force[0])
    if not math.isclose(_finite(ground["force_direction_angle_rad"], "force direction"), expected_angle, rel_tol=0.0, abs_tol=1e-12):
        raise GroundInteractionViolation("force direction is inconsistent with force components")

    paths = _mapping(raw["paths"], "paths")
    _exact(paths, {"force_edges", "torque_edges"}, "paths")
    if _unique_path_count(paths["force_edges"], "contact_roller", "structural_mount") != 1:
        raise GroundInteractionViolation("exactly one continuous force path is required")
    torque = _mapping(raw["torque_case"], "torque_case")
    _exact(torque, {"input_part_id", "output_part_id", "drive_torque_nm", "brake_torque_nm", "angular_speed_rad_s", "duration_s", "drive_efficiency"}, "torque_case")
    if _unique_path_count(paths["torque_edges"], torque["input_part_id"], torque["output_part_id"]) != 1:
        raise GroundInteractionViolation("exactly one continuous torque path is required")
    if not 0.0 <= _finite(torque["drive_efficiency"], "drive_efficiency") <= 1.0:
        raise GroundInteractionViolation("drive efficiency must be inside [0,1]")
    for key in ("drive_torque_nm", "angular_speed_rad_s", "duration_s"):
        _finite(torque[key], key, positive=True)
    if _finite(torque["brake_torque_nm"], "brake_torque_nm") >= 0.0:
        raise GroundInteractionViolation("brake torque must oppose positive rotation")

    if set(raw["controls"]) != REQUIRED_CONTROLS or len(raw["controls"]) != len(REQUIRED_CONTROLS):
        raise GroundInteractionViolation("required falsification controls changed")
    policy = _mapping(raw["evidence_policy"], "evidence_policy")
    _exact(policy, {"hidden_geometry_repair_allowed", "result_conditioned_geometry_mutation_allowed", "design_evidence_required_for_admission", "available_evidence_class"}, "evidence_policy")
    if policy != {"hidden_geometry_repair_allowed": False, "result_conditioned_geometry_mutation_allowed": False, "design_evidence_required_for_admission": True, "available_evidence_class": "synthetic_verification"}:
        raise GroundInteractionViolation("evidence policy may not admit synthetic or repaired evidence")

    capacity = _mapping(raw["capacity"], "capacity")
    _exact(capacity, {"reference_force_capacity_n", "undersized_scale"}, "capacity")
    _finite(capacity["reference_force_capacity_n"], "reference capacity", positive=True)
    scale = _finite(capacity["undersized_scale"], "undersized scale", positive=True)
    if scale >= 1.0:
        raise GroundInteractionViolation("undersized scale must be below one")

    structural = _mapping(raw["structural_evidence"], "structural_evidence")
    _exact(structural, {"result_path", "result_sha256", "geometry_step_sha256", "material_record_sha256", "evidence_class", "design_use_allowed"}, "structural_evidence")
    for key in ("result_sha256", "geometry_step_sha256", "material_record_sha256"):
        _sha(structural[key], key)
    if structural["evidence_class"] != "synthetic_verification" or structural["design_use_allowed"] is not False:
        raise GroundInteractionViolation("structural evidence must remain synthetic-only")

    clearance = _mapping(raw["clearance"], "clearance")
    _exact(clearance, {"forbidden_pairs", "minimum_clearance_m", "maximum_overlap_m3"}, "clearance")
    _finite(clearance["minimum_clearance_m"], "minimum clearance", positive=True)
    _finite(clearance["maximum_overlap_m3"], "maximum overlap", positive=True)

    return {
        "status": "passed",
        "candidate_id": raw["candidate_id"],
        "part_ids": part_ids,
        "mobility_dof": mobility,
        "travel_m": hi - lo,
        "contact_point_m": list(point),
        "force_n": list(force),
        "declaration_sha256": canonical_sha256(raw),
    }


def _verify_geometry(raw: Mapping[str, Any], manifest_raw: Mapping[str, Any]) -> dict[str, Any]:
    manifest = _mapping(manifest_raw, "geometry manifest")
    required = {"candidate_id", "declaration_sha256", "hidden_geometry_repair", "parts", "assembly", "motion_clearance", "manifest_sha256"}
    _exact(manifest, required, "geometry manifest")
    draft = {key: manifest[key] for key in required - {"manifest_sha256"}}
    if _sha(manifest["manifest_sha256"], "manifest_sha256") != canonical_sha256(draft):
        raise GroundInteractionViolation("geometry manifest identity mismatch")
    if manifest["candidate_id"] != raw["candidate_id"] or manifest["declaration_sha256"] != canonical_sha256(raw):
        raise GroundInteractionViolation("geometry was not generated from this declaration")
    if manifest["hidden_geometry_repair"] is not False:
        raise GroundInteractionViolation("hidden geometry repair is forbidden")
    parts = manifest["parts"]
    if not isinstance(parts, list) or len(parts) != raw["gates"]["required_part_count"]:
        raise GroundInteractionViolation("geometry part count mismatch")
    expected_ids = [part["part_id"] for part in raw["parts"]]
    if [part.get("part_id") for part in parts] != expected_ids:
        raise GroundInteractionViolation("geometry part order or identities changed")
    for part in parts:
        if part.get("valid") is not True or part.get("solid_count") != 1:
            raise GroundInteractionViolation(f"part {part.get('part_id')} is not one valid solid")
        _sha(part.get("step_sha256"), "part STEP hash")
        _finite(part.get("volume_m3"), "part volume", positive=True)
    mount_expected = raw["parts"][0]["geometry"]["expected_step_sha256"]
    if parts[0]["step_sha256"] != mount_expected or parts[0]["step_sha256"] != raw["structural_evidence"]["geometry_step_sha256"]:
        raise GroundInteractionViolation("structural mount STEP identity changed")
    assembly = _mapping(manifest["assembly"], "assembly")
    if assembly.get("valid") is not True or assembly.get("solid_count") != len(parts):
        raise GroundInteractionViolation("assembly must retain five separate valid solids")
    _sha(assembly.get("step_sha256"), "assembly STEP hash")
    states = manifest["motion_clearance"]
    if not isinstance(states, list) or [state.get("state") for state in states] != ["minimum", "reference", "maximum"]:
        raise GroundInteractionViolation("all three frozen clearance states are required")
    clearance_gate = raw["clearance"]
    for state in states:
        if _finite(state.get("maximum_overlap_m3"), "maximum overlap") > clearance_gate["maximum_overlap_m3"]:
            raise GroundInteractionViolation("part interference exceeds the frozen gate")
        if _finite(state.get("minimum_forbidden_clearance_m"), "minimum forbidden clearance") < clearance_gate["minimum_clearance_m"]:
            raise GroundInteractionViolation("forbidden clearance is below the frozen gate")
    return {
        "part_count": len(parts),
        "assembly_step_sha256": assembly["step_sha256"],
        "minimum_forbidden_clearance_m": min(state["minimum_forbidden_clearance_m"] for state in states),
        "maximum_overlap_m3": max(state["maximum_overlap_m3"] for state in states),
    }


def _verify_freecad(manifest: Mapping[str, Any], freecad_raw: Mapping[str, Any]) -> dict[str, Any]:
    report = _mapping(freecad_raw, "FreeCAD report")
    required = {"source_manifest_sha256", "freecad_version", "occt_version", "hidden_geometry_repair", "parts", "assembly", "report_sha256"}
    _exact(report, required, "FreeCAD report")
    draft = {key: report[key] for key in required - {"report_sha256"}}
    if report["report_sha256"] != canonical_sha256(draft):
        raise GroundInteractionViolation("FreeCAD report identity mismatch")
    if report["source_manifest_sha256"] != manifest["manifest_sha256"] or report["hidden_geometry_repair"] is not False:
        raise GroundInteractionViolation("FreeCAD report source or repair state is invalid")
    expected = {item["part_id"]: item["step_sha256"] for item in manifest["parts"]}
    measured = report["parts"]
    if not isinstance(measured, list) or {item.get("part_id"): item.get("step_sha256") for item in measured} != expected:
        raise GroundInteractionViolation("FreeCAD did not inspect the exact part STEP set")
    if any(item.get("valid") is not True or item.get("solid_count") != 1 for item in measured):
        raise GroundInteractionViolation("FreeCAD part validity failed")
    if report["assembly"].get("valid") is not True or report["assembly"].get("solid_count") != len(expected):
        raise GroundInteractionViolation("FreeCAD assembly did not retain separate solids")
    return {"report_sha256": report["report_sha256"], "part_count": len(measured), "assembly_solid_count": report["assembly"]["solid_count"]}


def _verify_structural(raw: Mapping[str, Any], structural_raw: Mapping[str, Any]) -> dict[str, Any]:
    expected = raw["structural_evidence"]
    if structural_raw.get("result_sha256") != expected["result_sha256"]:
        raise GroundInteractionViolation("structural result identity mismatch")
    if structural_raw.get("geometry_step_sha256") != expected["geometry_step_sha256"]:
        raise GroundInteractionViolation("structural geometry identity mismatch")
    if structural_raw.get("material_record_sha256") != expected["material_record_sha256"]:
        raise GroundInteractionViolation("structural material identity mismatch")
    adjudication = _mapping(structural_raw.get("adjudication"), "structural adjudication")
    if structural_raw.get("status") != "passed" or adjudication.get("status") != "passed":
        raise GroundInteractionViolation("structural solver witness did not pass")
    if structural_raw.get("design_use_allowed") is not False or adjudication.get("design_use_allowed") is not False:
        raise GroundInteractionViolation("synthetic structural evidence was relabelled")
    if adjudication.get("evidence_class") != "synthetic_verification":
        raise GroundInteractionViolation("unexpected structural evidence class")
    return {
        "result_sha256": structural_raw["result_sha256"],
        "structural_state": adjudication["structural_state"],
        "maximum_displacement_m": adjudication["fine_metrics"]["maximum_displacement_m"],
        "p90_von_mises_stress_pa": adjudication["fine_metrics"]["p90_von_mises_stress_pa"],
        "evidence_class": "synthetic_verification",
        "design_use_allowed": False,
    }


def _reference_physics(raw: Mapping[str, Any]) -> dict[str, Any]:
    ground = raw["ground_interface"]
    force = tuple(float(x) for x in ground["force_on_candidate_n"])
    point = tuple(float(x) for x in ground["contact_point_m"])
    drive = raw["torque_case"]
    torque = float(drive["drive_torque_nm"])
    reaction_force = tuple(-x for x in force)
    applied_moment = (
        point[1] * force[2] - point[2] * force[1],
        point[2] * force[0] - point[0] * force[2] + torque,
        point[0] * force[1] - point[1] * force[0],
    )
    reaction_moment = tuple(-x for x in applied_moment)
    force_residual = math.sqrt(sum((force[i] + reaction_force[i]) ** 2 for i in range(3))) / max(math.sqrt(sum(x * x for x in force)), 1.0)
    moment_residual = math.sqrt(sum((applied_moment[i] + reaction_moment[i]) ** 2 for i in range(3))) / max(math.sqrt(sum(x * x for x in applied_moment)), 1.0)
    input_work = torque * drive["angular_speed_rad_s"] * drive["duration_s"]
    delivered_work = input_work * drive["drive_efficiency"]
    loss_work = input_work - delivered_work
    energy_residual = abs(input_work - delivered_work - loss_work) / max(abs(input_work), 1.0)
    brake_work = abs(drive["brake_torque_nm"]) * drive["angular_speed_rad_s"] * drive["duration_s"]
    normal = force[2]
    resultant = math.sqrt(sum(x * x for x in force))
    utilization = resultant / raw["capacity"]["reference_force_capacity_n"]
    return {
        "normal_force_n": normal,
        "resultant_force_n": resultant,
        "reaction_force_n": list(reaction_force),
        "reaction_moment_nm": list(reaction_moment),
        "force_residual_relative": force_residual,
        "moment_residual_relative": moment_residual,
        "drive_input_work_j": input_work,
        "drive_delivered_work_j": delivered_work,
        "drive_loss_work_j": loss_work,
        "drive_energy_residual_relative": energy_residual,
        "brake_opposing_torque_nm": drive["brake_torque_nm"],
        "brake_work_to_rejection_j": brake_work,
        "reference_capacity_utilization": utilization,
    }


def _controls(raw: Mapping[str, Any], physics: Mapping[str, Any]) -> dict[str, Any]:
    force = raw["ground_interface"]["force_on_candidate_n"]
    reference_angle = raw["ground_interface"]["force_direction_angle_rad"]
    undersized_util = physics["resultant_force_n"] / (raw["capacity"]["reference_force_capacity_n"] * raw["capacity"]["undersized_scale"])
    return {
        "mirror": {
            "status": "passed",
            "mirrored_force_n": [force[0], -force[1], force[2]],
            "mirrored_force_direction_angle_rad": -reference_angle,
            "normal_force_unchanged": True,
        },
        "rigid_no_travel": {"status": "passed", "travel_m": 0.0, "mobility_dof": 1, "subsystem_state": "rigid_control"},
        "disconnected_mount": {"status": "passed", "force_path_count": 0, "transmitted_force_n": [0.0, 0.0, 0.0], "subsystem_state": "dnf"},
        "blocked_translation": {"status": "passed", "realized_travel_m": 0.0, "subsystem_state": "degraded"},
        "seized_rotation": {"status": "passed", "angular_speed_rad_s": 0.0, "delivered_mechanical_power_w": 0.0, "subsystem_state": "degraded"},
        "broken_torque_path": {"status": "passed", "torque_path_count": 0, "delivered_torque_nm": 0.0, "subsystem_state": "degraded"},
        "undersized_capacity": {"status": "passed", "capacity_utilization": undersized_util, "subsystem_state": "dnf" if undersized_util > 1.0 else "invalid_control"},
        "contact_loss": {"status": "passed", "normal_force_n": 0.0, "longitudinal_force_n": 0.0, "lateral_force_n": 0.0, "subsystem_state": "dnf"},
    }


def evaluate_candidate(
    raw: Mapping[str, Any],
    geometry_manifest: Mapping[str, Any],
    freecad_report: Mapping[str, Any],
    structural_result: Mapping[str, Any],
) -> dict[str, Any]:
    declaration = validate_declaration(raw)
    geometry = _verify_geometry(raw, geometry_manifest)
    freecad = _verify_freecad(geometry_manifest, freecad_report)
    structural = _verify_structural(raw, structural_result)
    physics = _reference_physics(raw)
    gates = raw["gates"]
    if physics["force_residual_relative"] > gates["force_residual_relative"]:
        raise GroundInteractionViolation("force equilibrium residual exceeds gate")
    if physics["moment_residual_relative"] > gates["moment_residual_relative"]:
        raise GroundInteractionViolation("moment equilibrium residual exceeds gate")
    if physics["drive_energy_residual_relative"] > gates["energy_residual_relative"]:
        raise GroundInteractionViolation("energy residual exceeds gate")
    controls = _controls(raw, physics)
    if controls["undersized_capacity"]["subsystem_state"] != "dnf":
        raise GroundInteractionViolation("undersized falsification control did not fail")
    if any(control["status"] != "passed" for control in controls.values()):
        raise GroundInteractionViolation("a required control did not pass")
    draft = {
        "status": "passed",
        "candidate_id": raw["candidate_id"],
        "candidate_verdict": "not_admitted_synthetic_evidence",
        "design_use_allowed": False,
        "subsystem_state": "operational_in_synthetic_verification",
        "declaration": declaration,
        "geometry": geometry,
        "freecad": freecad,
        "structural_mount_witness": structural,
        "paths": {"force_path_count": 1, "torque_path_count": 1},
        "physics": physics,
        "controls": controls,
        "limitations": [
            "synthetic material and process evidence",
            "quasi-static bookkeeping only",
            "structural witness covers only the exact mount bracket and Work 082 load family",
            "no tyre, fatigue, bearing, dynamic, manufacturing, safety, or physical validation",
        ],
    }
    return {**draft, "evaluation_sha256": canonical_sha256(draft)}
