"""Fail-closed Work 084 energy-conversion and torque-path candidate evaluation."""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "energy_torque_path_candidate_v1"
STRUCTURE_TERMINAL = "structure_terminal"
REQUIRED_CONTROLS = {
    "mirror",
    "locked_converter",
    "seized_support",
    "broken_coupling",
    "zero_loss_exploit",
    "efficiency_over_one",
    "reversed_torque",
    "overspeed",
    "inadequate_cooling",
    "disconnected_housing_reaction",
}
REQUIRED_PART_IDS = (
    "energy_store",
    "converter_housing",
    "converter_rotor",
    "input_shaft",
    "ratio_drum",
    "output_shaft",
    "support_block",
)
REQUIRED_STRUCTURAL_CASES = (
    "output_shaft_combined",
    "input_shaft_combined",
    "support_block_bearing",
    "converter_housing_mount",
)


class EnergyTorquePathViolation(ValueError):
    """Raised when declaration or evidence cannot support the bounded claim."""


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise EnergyTorquePathViolation(f"{label} must be a mapping")
    return value


def _exact(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise EnergyTorquePathViolation(
            f"{label} fields mismatch: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}"
        )


def _finite(value: Any, label: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise EnergyTorquePathViolation(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0.0):
        raise EnergyTorquePathViolation(f"{label} is outside its finite domain")
    return result


def _vector3(value: Any, label: str) -> tuple[float, float, float]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 3:
        raise EnergyTorquePathViolation(f"{label} must contain three values")
    return tuple(_finite(item, f"{label}[{index}]") for index, item in enumerate(value))  # type: ignore[return-value]


def _sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise EnergyTorquePathViolation(f"{label} must be a lowercase SHA-256")
    return value


def _relative(actual: float, expected: float) -> float:
    return abs(actual - expected) / max(abs(expected), 1.0)


def unique_path_count(edges: Sequence[Sequence[str]], source: str, target: str) -> int:
    """Count simple undirected paths between two declared nodes, saturating at two."""
    graph: dict[str, set[str]] = defaultdict(set)
    for index, edge in enumerate(edges):
        if not isinstance(edge, Sequence) or isinstance(edge, (str, bytes)) or len(edge) != 2:
            raise EnergyTorquePathViolation(f"path edge {index} must have two endpoints")
        a, b = edge
        if not isinstance(a, str) or not isinstance(b, str) or a == b:
            raise EnergyTorquePathViolation(f"path edge {index} is invalid")
        graph[a].add(b)
        graph[b].add(a)

    count = 0

    def visit(node: str, seen: frozenset[str]) -> None:
        nonlocal count
        if count > 1:
            return
        if node == target:
            count += 1
            return
        for nxt in sorted(graph[node] - seen):
            visit(nxt, seen | {nxt})

    visit(source, frozenset({source}))
    return count


def _validate_material(raw: Mapping[str, Any]) -> Mapping[str, Any]:
    material = _mapping(raw["material"], "material")
    _exact(
        material,
        {
            "material_id", "material_record_sha256", "density_kg_per_m3", "youngs_modulus_pa",
            "yield_strength_pa", "specific_heat_j_per_kg_k", "allowable_bearing_pressure_pa",
            "maximum_temperature_k", "evidence_class", "design_use_allowed",
        },
        "material",
    )
    _sha(material["material_record_sha256"], "material_record_sha256")
    for key in (
        "density_kg_per_m3", "youngs_modulus_pa", "yield_strength_pa", "specific_heat_j_per_kg_k",
        "allowable_bearing_pressure_pa", "maximum_temperature_k",
    ):
        _finite(material[key], key, positive=True)
    if material["evidence_class"] != "synthetic_verification" or material["design_use_allowed"] is not False:
        raise EnergyTorquePathViolation("material evidence must remain synthetic-only")
    return material


def _validate_kinematics(raw: Mapping[str, Any], part_ids: list[str]) -> tuple[int, float, float, float]:
    joints = raw["joints"]
    if not isinstance(joints, list) or len(joints) != len(part_ids):
        raise EnergyTorquePathViolation("each part requires exactly one tree joint")
    children: set[str] = set()
    joint_rows = 0
    for index, joint_raw in enumerate(joints):
        joint = _mapping(joint_raw, f"joints[{index}]")
        allowed = {"joint_id", "parent", "child", "type", "constraint_rows"}
        if joint.get("type") == "revolute":
            allowed.add("axis")
        _exact(joint, allowed, f"joints[{index}]")
        if joint["child"] not in part_ids or joint["child"] in children:
            raise EnergyTorquePathViolation("each part must be a tree child exactly once")
        if joint["parent"] not in set(part_ids) | {STRUCTURE_TERMINAL}:
            raise EnergyTorquePathViolation("joint parent is not a declared part or the structure terminal")
        children.add(joint["child"])
        rows = joint["constraint_rows"]
        if isinstance(rows, bool) or not isinstance(rows, int) or rows not in {5, 6}:
            raise EnergyTorquePathViolation("joint constraint_rows must be five or six")
        if rows != (5 if joint["type"] == "revolute" else 6):
            raise EnergyTorquePathViolation("joint constraint rows disagree with joint type")
        if "axis" in joint and _vector3(joint["axis"], "joint axis") != (0.0, 1.0, 0.0):
            raise EnergyTorquePathViolation("declared revolute joints must use the frozen +y axis")
        joint_rows += rows

    couplings = raw["couplings"]
    if not isinstance(couplings, list) or len(couplings) != 1:
        raise EnergyTorquePathViolation("exactly one loop-closing coupling is required")
    coupling = _mapping(couplings[0], "couplings[0]")
    _exact(
        coupling,
        {
            "coupling_id", "drive_part_id", "driven_part_id", "type", "constraint_rows",
            "drive_radius_m", "driven_radius_m", "engagement_gap_m", "engagement_elements_modelled",
        },
        "couplings[0]",
    )
    if coupling["type"] != "rolling" or coupling["constraint_rows"] != 1:
        raise EnergyTorquePathViolation("the loop closure must be one rolling constraint row")
    if coupling["drive_part_id"] not in part_ids or coupling["driven_part_id"] not in part_ids:
        raise EnergyTorquePathViolation("coupling members must be declared parts")
    if coupling["engagement_elements_modelled"] is not False:
        raise EnergyTorquePathViolation("engagement elements are not modelled and may not be claimed")
    drive_radius = _finite(coupling["drive_radius_m"], "drive_radius_m", positive=True)
    driven_radius = _finite(coupling["driven_radius_m"], "driven_radius_m", positive=True)
    gap = _finite(coupling["engagement_gap_m"], "engagement_gap_m", positive=True)
    if driven_radius <= drive_radius:
        raise EnergyTorquePathViolation("the declared transformation must change the torque magnitude")

    mobility = 6 * len(part_ids) - joint_rows - int(coupling["constraint_rows"])
    if mobility != raw["gates"]["required_mobility_dof"] or mobility != 1:
        raise EnergyTorquePathViolation("calculated mobility does not equal one DOF")

    rotation = _mapping(raw["rotation"], "rotation")
    _exact(rotation, {"axis", "input_group", "output_group"}, "rotation")
    if _vector3(rotation["axis"], "rotation axis") != (0.0, 1.0, 0.0):
        raise EnergyTorquePathViolation("rotation must use the declared +y axis")
    if set(rotation["input_group"]) != {"converter_rotor", "input_shaft"}:
        raise EnergyTorquePathViolation("input rotating group changed")
    if set(rotation["output_group"]) != {"output_shaft", "ratio_drum"}:
        raise EnergyTorquePathViolation("output rotating group changed")
    return mobility, drive_radius, driven_radius, gap


def _validate_paths(raw: Mapping[str, Any]) -> dict[str, int]:
    paths = _mapping(raw["paths"], "paths")
    _exact(
        paths,
        {
            "torque_edges", "reaction_edges", "recovery_return_edge", "torque_source", "torque_sink",
            "reaction_source", "reaction_sink", "recovery_source", "recovery_sink",
        },
        "paths",
    )
    torque = unique_path_count(paths["torque_edges"], paths["torque_source"], paths["torque_sink"])
    if torque != 1:
        raise EnergyTorquePathViolation("exactly one continuous torque path is required")
    reaction = unique_path_count(paths["reaction_edges"], paths["reaction_source"], paths["reaction_sink"])
    if reaction != 1:
        raise EnergyTorquePathViolation("exactly one continuous reaction path is required")
    recovery_edges = list(paths["torque_edges"]) + [list(paths["recovery_return_edge"])]
    recovery = unique_path_count(recovery_edges, paths["recovery_source"], paths["recovery_sink"])
    if recovery != 1:
        raise EnergyTorquePathViolation("exactly one continuous recovery path is required")
    return {"torque_path_count": torque, "reaction_path_count": reaction, "recovery_path_count": recovery}


def validate_declaration(raw: Mapping[str, Any]) -> dict[str, Any]:
    _exact(
        raw,
        {
            "schema_version", "candidate_id", "claim_level", "declared_technology", "coordinate_system",
            "material", "parts", "joints", "couplings", "rotation", "clearance", "work083_interface",
            "paths", "energy_store_state", "drive_case", "brake_case", "thermal", "limits",
            "structural_analytic", "gates", "controls", "control_settings", "evidence_policy", "non_claims",
        },
        "declaration",
    )
    if raw["schema_version"] != SCHEMA_VERSION:
        raise EnergyTorquePathViolation("unsupported schema_version")
    if raw["candidate_id"] != "energy_torque_path_candidate_001":
        raise EnergyTorquePathViolation("unexpected candidate_id")

    coordinate = _mapping(raw["coordinate_system"], "coordinate_system")
    _exact(coordinate, {"units", "x_axis", "y_axis", "z_axis"}, "coordinate_system")
    if coordinate != {
        "units": "SI", "x_axis": "longitudinal_forward", "y_axis": "lateral_left", "z_axis": "vertical_up",
    }:
        raise EnergyTorquePathViolation("coordinate system must use the frozen SI frame")

    parts = raw["parts"]
    if not isinstance(parts, list):
        raise EnergyTorquePathViolation("parts must be a list")
    part_ids = []
    for index, item_raw in enumerate(parts):
        item = _mapping(item_raw, f"parts[{index}]")
        _exact(item, {"part_id", "role", "geometry"}, f"parts[{index}]")
        _mapping(item["geometry"], "part geometry")
        part_ids.append(item["part_id"])
    if tuple(part_ids) != REQUIRED_PART_IDS:
        raise EnergyTorquePathViolation("frozen part set or order changed")

    gates = _mapping(raw["gates"], "gates")
    _exact(
        gates,
        {
            "required_part_count", "required_mobility_dof", "torque_residual_relative",
            "reaction_residual_relative", "energy_residual_relative", "thermal_residual_relative",
            "area_cross_check_relative",
        },
        "gates",
    )
    if len(parts) != gates["required_part_count"] or gates["required_part_count"] != 7:
        raise EnergyTorquePathViolation("the frozen candidate requires seven parts")

    material = _validate_material(raw)
    mobility, drive_radius, driven_radius, gap = _validate_kinematics(raw, part_ids)
    path_counts = _validate_paths(raw)

    drive = _mapping(raw["drive_case"], "drive_case")
    _exact(
        drive,
        {"rotor_torque_nm", "rotor_angular_speed_rad_s", "converter_efficiency", "support_drag_torque_nm", "duration_s"},
        "drive_case",
    )
    for key in ("rotor_torque_nm", "rotor_angular_speed_rad_s", "duration_s"):
        _finite(drive[key], key, positive=True)
    efficiency = _finite(drive["converter_efficiency"], "converter_efficiency")
    if not 0.0 <= efficiency <= 1.0:
        raise EnergyTorquePathViolation("converter efficiency must be inside [0,1]")
    drag = _finite(drive["support_drag_torque_nm"], "support_drag_torque_nm", positive=True)

    limits = _mapping(raw["limits"], "limits")
    _exact(
        limits,
        {"maximum_rotor_angular_speed_rad_s", "maximum_rotor_surface_speed_m_s", "maximum_efficiency"},
        "limits",
    )
    maximum_efficiency = _finite(limits["maximum_efficiency"], "maximum_efficiency", positive=True)
    if maximum_efficiency >= 1.0:
        raise EnergyTorquePathViolation("a positive declared loss is required below unit efficiency")
    if efficiency > maximum_efficiency:
        raise EnergyTorquePathViolation("declared converter efficiency exceeds the maximum")
    if drag >= drive["rotor_torque_nm"] * (driven_radius / drive_radius):
        raise EnergyTorquePathViolation("declared drag torque cannot exceed the transformed torque")

    brake = _mapping(raw["brake_case"], "brake_case")
    _exact(
        brake,
        {
            "source_kinetic_energy_j", "output_brake_torque_nm", "output_angular_speed_rad_s",
            "recovery_efficiency", "duration_s",
        },
        "brake_case",
    )
    for key in ("source_kinetic_energy_j", "output_angular_speed_rad_s", "duration_s"):
        _finite(brake[key], key, positive=True)
    if _finite(brake["output_brake_torque_nm"], "output_brake_torque_nm") >= 0.0:
        raise EnergyTorquePathViolation("brake torque must oppose positive rotation")
    recovery_efficiency = _finite(brake["recovery_efficiency"], "recovery_efficiency")
    if not 0.0 <= recovery_efficiency <= maximum_efficiency:
        raise EnergyTorquePathViolation("recovery efficiency must be inside the declared loss domain")

    store = _mapping(raw["energy_store_state"], "energy_store_state")
    _exact(
        store,
        {"medium_density_kg_per_m3", "medium_specific_energy_j_per_kg", "external_primary_inflow_j"},
        "energy_store_state",
    )
    _finite(store["medium_density_kg_per_m3"], "medium density", positive=True)
    _finite(store["medium_specific_energy_j_per_kg"], "medium specific energy", positive=True)
    if _finite(store["external_primary_inflow_j"], "external_primary_inflow_j") != 0.0:
        raise EnergyTorquePathViolation("external primary energy inflow must be exactly zero")

    thermal = _mapping(raw["thermal"], "thermal")
    _exact(
        thermal,
        {
            "coolant_mass_flow_kg_s", "coolant_specific_heat_j_per_kg_k", "coolant_density_kg_per_m3",
            "coolant_inlet_temperature_k", "coolant_wall_coefficient_w_per_m2_k", "air_temperature_k",
            "air_fin_coefficient_w_per_m2_k", "maximum_coolant_temperature_rise_k", "maximum_coolant_velocity_m_s",
        },
        "thermal",
    )
    for key, value in thermal.items():
        _finite(value, key, positive=True)

    interface = _mapping(raw["work083_interface"], "work083_interface")
    _exact(
        interface,
        {
            "result_path", "result_sha256", "assembly_step_sha256", "axle_step_sha256", "axle_axis_xz_m",
            "axle_radius_m", "axle_outboard_y_m", "contact_plane_z_m", "coupling_position_tolerance_m",
            "coupling_radius_tolerance_m", "fastener_modelled",
        },
        "work083_interface",
    )
    for key in ("result_sha256", "assembly_step_sha256", "axle_step_sha256"):
        _sha(interface[key], key)
    if interface["fastener_modelled"] is not False:
        raise EnergyTorquePathViolation("no fastener is modelled and none may be claimed")

    clearance = _mapping(raw["clearance"], "clearance")
    _exact(
        clearance,
        {"contact_pairs", "coupling_pairs", "minimum_clearance_m", "maximum_mate_gap_m", "maximum_overlap_m3"},
        "clearance",
    )
    for key in ("minimum_clearance_m", "maximum_mate_gap_m", "maximum_overlap_m3"):
        _finite(clearance[key], key, positive=True)

    structural = _mapping(raw["structural_analytic"], "structural_analytic")
    _exact(structural, {"evidence_class", "meshed_solver_evidence", "cases", "maximum_utilization"}, "structural_analytic")
    if structural["evidence_class"] != "analytic_synthetic_verification":
        raise EnergyTorquePathViolation("analytic structural evidence may not be relabelled")
    if structural["meshed_solver_evidence"] is not False:
        raise EnergyTorquePathViolation("this work provides no meshed solver evidence")
    if tuple(structural["cases"]) != REQUIRED_STRUCTURAL_CASES:
        raise EnergyTorquePathViolation("declared structural case set changed")

    if set(raw["controls"]) != REQUIRED_CONTROLS or len(raw["controls"]) != len(REQUIRED_CONTROLS):
        raise EnergyTorquePathViolation("required falsification controls changed")
    settings = _mapping(raw["control_settings"], "control_settings")
    _exact(
        settings,
        {
            "locked_converter_angular_speed_rad_s", "zero_loss_drag_torque_nm", "zero_loss_converter_efficiency",
            "efficiency_over_one_value", "overspeed_angular_speed_rad_s", "inadequate_cooling_mass_flow_kg_s",
        },
        "control_settings",
    )

    policy = _mapping(raw["evidence_policy"], "evidence_policy")
    _exact(
        policy,
        {
            "hidden_geometry_repair_allowed", "result_conditioned_geometry_mutation_allowed",
            "design_evidence_required_for_admission", "available_evidence_class",
        },
        "evidence_policy",
    )
    if policy != {
        "hidden_geometry_repair_allowed": False,
        "result_conditioned_geometry_mutation_allowed": False,
        "design_evidence_required_for_admission": True,
        "available_evidence_class": "synthetic_verification",
    }:
        raise EnergyTorquePathViolation("evidence policy may not admit synthetic or repaired evidence")

    return {
        "status": "passed",
        "candidate_id": raw["candidate_id"],
        "part_ids": part_ids,
        "mobility_dof": mobility,
        "torque_ratio": driven_radius / drive_radius,
        "drive_radius_m": drive_radius,
        "driven_radius_m": driven_radius,
        "engagement_gap_m": gap,
        "material_id": material["material_id"],
        "paths": path_counts,
        "declaration_sha256": canonical_sha256(raw),
    }


def _geometry_expectations(raw: Mapping[str, Any]) -> dict[str, float]:
    """Analytic surface quantities implied by the frozen parameters that build the B-rep."""
    housing = raw["parts"][1]["geometry"]
    length = _finite(housing["box_size_m"][1], "housing y length", positive=True)
    radius = _finite(housing["coolant_passage_radius_m"], "coolant_passage_radius_m", positive=True)
    passages = len(housing["coolant_passage_x_m"])
    fin_length = _finite(housing["fin_length_m"], "fin_length_m", positive=True)
    fin_thickness = _finite(housing["fin_thickness_m"], "fin_thickness_m", positive=True)
    fin_height = _finite(housing["fin_height_m"], "fin_height_m", positive=True)
    fins = len(housing["fin_center_y_m"])
    lateral = passages * 2.0 * math.pi * radius * length
    openings = passages * 2.0 * math.pi * radius * radius
    fin_area = fins * 2.0 * fin_height * (fin_length + fin_thickness)
    return {
        "coolant_wall_area_m2": lateral,
        "coolant_area_delta_m2": lateral - openings,
        "coolant_passage_section_m2": passages * math.pi * radius * radius,
        "fin_area_m2": fin_area,
    }


def _verify_geometry(raw: Mapping[str, Any], manifest_raw: Mapping[str, Any]) -> dict[str, Any]:
    manifest = _mapping(manifest_raw, "geometry manifest")
    required = {
        "candidate_id", "declaration_sha256", "hidden_geometry_repair", "parts", "assembly",
        "derived", "pair_clearance", "manifest_sha256",
    }
    _exact(manifest, required, "geometry manifest")
    draft = {key: manifest[key] for key in required - {"manifest_sha256"}}
    if _sha(manifest["manifest_sha256"], "manifest_sha256") != canonical_sha256(draft):
        raise EnergyTorquePathViolation("geometry manifest identity mismatch")
    if manifest["candidate_id"] != raw["candidate_id"] or manifest["declaration_sha256"] != canonical_sha256(raw):
        raise EnergyTorquePathViolation("geometry was not generated from this declaration")
    if manifest["hidden_geometry_repair"] is not False:
        raise EnergyTorquePathViolation("hidden geometry repair is forbidden")

    parts = manifest["parts"]
    if not isinstance(parts, list) or len(parts) != raw["gates"]["required_part_count"]:
        raise EnergyTorquePathViolation("geometry part count mismatch")
    if [part.get("part_id") for part in parts] != [item["part_id"] for item in raw["parts"]]:
        raise EnergyTorquePathViolation("geometry part order or identities changed")
    masses: dict[str, float] = {}
    for part in parts:
        if part.get("valid") is not True or part.get("solid_count") != 1:
            raise EnergyTorquePathViolation(f"part {part.get('part_id')} is not one valid solid")
        _sha(part.get("step_sha256"), "part STEP hash")
        volume = _finite(part.get("volume_m3"), "part volume", positive=True)
        mass = _finite(part.get("mass_kg"), "part mass", positive=True)
        if _relative(mass, volume * raw["material"]["density_kg_per_m3"]) > 1e-9:
            raise EnergyTorquePathViolation(f"part {part['part_id']} mass is not geometry-derived")
        masses[part["part_id"]] = mass

    assembly = _mapping(manifest["assembly"], "assembly")
    if assembly.get("valid") is not True or assembly.get("solid_count") != len(parts):
        raise EnergyTorquePathViolation("assembly must retain seven separate valid solids")
    _sha(assembly.get("step_sha256"), "assembly STEP hash")

    clearance_gate = raw["clearance"]
    contact = {tuple(sorted(pair)) for pair in clearance_gate["contact_pairs"]}
    coupling = {tuple(sorted(pair)) for pair in clearance_gate["coupling_pairs"]}
    part_ids = [item["part_id"] for item in raw["parts"]]
    expected_pairs = {
        tuple(sorted((first, second)))
        for index, first in enumerate(part_ids)
        for second in part_ids[index + 1:]
    }
    measured: dict[tuple[str, ...], Mapping[str, Any]] = {}
    for record in manifest["pair_clearance"]:
        key = tuple(sorted(record["parts"]))
        if key in measured:
            raise EnergyTorquePathViolation("duplicate clearance record")
        measured[key] = record
    if set(measured) != expected_pairs:
        raise EnergyTorquePathViolation("clearance evidence does not cover every part pair exactly once")

    minimum_forbidden = math.inf
    maximum_overlap = 0.0
    for key, record in measured.items():
        gap = _finite(record.get("clearance_m"), "pair clearance")
        overlap = _finite(record.get("overlap_m3"), "pair overlap")
        if overlap > clearance_gate["maximum_overlap_m3"]:
            raise EnergyTorquePathViolation(f"parts {key} interfere beyond the frozen gate")
        maximum_overlap = max(maximum_overlap, overlap)
        if key in contact:
            expected = "contact"
        elif key in coupling:
            expected = "coupling"
        else:
            expected = "forbidden"
        if record.get("classification") != expected:
            raise EnergyTorquePathViolation(f"parts {key} carry the wrong clearance classification")
        if expected == "forbidden":
            if gap < clearance_gate["minimum_clearance_m"]:
                raise EnergyTorquePathViolation(f"parts {key} fall below the frozen clearance gate")
            minimum_forbidden = min(minimum_forbidden, gap)
        elif gap > clearance_gate["maximum_mate_gap_m"]:
            raise EnergyTorquePathViolation(f"parts {key} exceed the declared mate gap")

    derived = _mapping(manifest["derived"], "derived")
    _exact(
        derived,
        {
            "store_cavity_volume_m3", "housing_coolant_area_delta_m2", "housing_fin_area_delta_m2",
            "output_shaft_interface", "drum_ground_clearance_m",
        },
        "derived",
    )
    expectations = _geometry_expectations(raw)
    tolerance = raw["gates"]["area_cross_check_relative"]
    coolant_delta = _finite(derived["housing_coolant_area_delta_m2"], "coolant area delta", positive=True)
    fin_delta = _finite(derived["housing_fin_area_delta_m2"], "fin area delta", positive=True)
    if _relative(coolant_delta, expectations["coolant_area_delta_m2"]) > tolerance:
        raise EnergyTorquePathViolation("measured coolant passage area disagrees with the frozen geometry")
    if _relative(fin_delta, expectations["fin_area_m2"]) > tolerance:
        raise EnergyTorquePathViolation("measured fin area disagrees with the frozen geometry")

    interface = _mapping(derived["output_shaft_interface"], "output_shaft_interface")
    _exact(interface, {"y_m", "radius_m", "axis_x_m", "axis_z_m"}, "output_shaft_interface")
    frozen = raw["work083_interface"]
    position_tolerance = frozen["coupling_position_tolerance_m"]
    if abs(_finite(interface["y_m"], "interface y") - frozen["axle_outboard_y_m"]) > position_tolerance:
        raise EnergyTorquePathViolation("output shaft does not meet the frozen Work 083 axle end plane")
    if abs(_finite(interface["axis_x_m"], "interface x") - frozen["axle_axis_xz_m"][0]) > position_tolerance:
        raise EnergyTorquePathViolation("output shaft is not coaxial with the Work 083 axle in x")
    if abs(_finite(interface["axis_z_m"], "interface z") - frozen["axle_axis_xz_m"][1]) > position_tolerance:
        raise EnergyTorquePathViolation("output shaft is not coaxial with the Work 083 axle in z")
    if abs(_finite(interface["radius_m"], "interface radius") - frozen["axle_radius_m"]) > frozen["coupling_radius_tolerance_m"]:
        raise EnergyTorquePathViolation("output shaft radius does not match the Work 083 axle")

    ground_clearance = _finite(derived["drum_ground_clearance_m"], "drum ground clearance")
    if ground_clearance <= 0.0:
        raise EnergyTorquePathViolation("the transformation body reaches the declared ground plane")

    return {
        "part_count": len(parts),
        "assembly_step_sha256": assembly["step_sha256"],
        "part_mass_kg": masses,
        "total_mass_kg": math.fsum(masses.values()),
        "minimum_forbidden_clearance_m": minimum_forbidden,
        "maximum_overlap_m3": maximum_overlap,
        "store_cavity_volume_m3": _finite(derived["store_cavity_volume_m3"], "cavity volume", positive=True),
        "coolant_wall_area_m2": expectations["coolant_wall_area_m2"],
        "coolant_passage_section_m2": expectations["coolant_passage_section_m2"],
        "fin_area_m2": expectations["fin_area_m2"],
        "measured_coolant_area_delta_m2": coolant_delta,
        "measured_fin_area_delta_m2": fin_delta,
        "drum_ground_clearance_m": ground_clearance,
        "work083_coupling_y_m": interface["y_m"],
    }


def _verify_freecad(manifest: Mapping[str, Any], freecad_raw: Mapping[str, Any]) -> dict[str, Any]:
    report = _mapping(freecad_raw, "FreeCAD report")
    required = {
        "source_manifest_sha256", "freecad_version", "occt_version", "hidden_geometry_repair",
        "parts", "assembly", "report_sha256",
    }
    _exact(report, required, "FreeCAD report")
    draft = {key: report[key] for key in required - {"report_sha256"}}
    if report["report_sha256"] != canonical_sha256(draft):
        raise EnergyTorquePathViolation("FreeCAD report identity mismatch")
    if report["source_manifest_sha256"] != manifest["manifest_sha256"] or report["hidden_geometry_repair"] is not False:
        raise EnergyTorquePathViolation("FreeCAD report source or repair state is invalid")
    expected = {item["part_id"]: item["step_sha256"] for item in manifest["parts"]}
    measured = report["parts"]
    if not isinstance(measured, list) or {item.get("part_id"): item.get("step_sha256") for item in measured} != expected:
        raise EnergyTorquePathViolation("FreeCAD did not inspect the exact part STEP set")
    if any(item.get("valid") is not True or item.get("solid_count") != 1 for item in measured):
        raise EnergyTorquePathViolation("FreeCAD part validity failed")
    if report["assembly"].get("valid") is not True or report["assembly"].get("solid_count") != len(expected):
        raise EnergyTorquePathViolation("FreeCAD assembly did not retain separate solids")
    return {
        "report_sha256": report["report_sha256"],
        "part_count": len(measured),
        "assembly_solid_count": report["assembly"]["solid_count"],
    }


def _verify_work083(raw: Mapping[str, Any], result_raw: Mapping[str, Any]) -> dict[str, Any]:
    frozen = raw["work083_interface"]
    result = _mapping(result_raw, "Work 083 result")
    if result.get("result_sha256") != frozen["result_sha256"]:
        raise EnergyTorquePathViolation("Work 083 result identity mismatch")
    if result.get("assembly_step_sha256") != frozen["assembly_step_sha256"]:
        raise EnergyTorquePathViolation("Work 083 assembly identity mismatch")
    axle = result.get("part_step_sha256")
    if not isinstance(axle, Mapping) or axle.get("axle") != frozen["axle_step_sha256"]:
        raise EnergyTorquePathViolation("Work 083 axle identity mismatch")
    if result.get("status") != "passed":
        raise EnergyTorquePathViolation("the Work 083 witness did not pass")
    if result.get("design_use_allowed") is not False:
        raise EnergyTorquePathViolation("Work 083 synthetic evidence was relabelled")
    if result.get("candidate_verdict") != "not_admitted_synthetic_evidence":
        raise EnergyTorquePathViolation("unexpected Work 083 candidate verdict")
    return {
        "result_sha256": result["result_sha256"],
        "assembly_step_sha256": result["assembly_step_sha256"],
        "axle_step_sha256": axle["axle"],
        "candidate_verdict": result["candidate_verdict"],
        "design_use_allowed": False,
    }


def _thermal_segment(
    heat_rate_w: float,
    wall_conductance: float,
    air_conductance: float,
    capacity_rate: float,
    inlet_k: float,
    air_k: float,
) -> dict[str, float]:
    """Solve one quasi-steady segment with parallel coolant-wall and fin-air rejection."""
    effective = wall_conductance / (1.0 + wall_conductance / (2.0 * capacity_rate))
    housing_k = (heat_rate_w + effective * inlet_k + air_conductance * air_k) / (effective + air_conductance)
    coolant_w = effective * (housing_k - inlet_k)
    air_w = air_conductance * (housing_k - air_k)
    return {
        "heat_rate_w": heat_rate_w,
        "housing_temperature_k": housing_k,
        "coolant_heat_rate_w": coolant_w,
        "air_heat_rate_w": air_w,
        "coolant_temperature_rise_k": coolant_w / capacity_rate,
        "residual_relative": abs(heat_rate_w - coolant_w - air_w) / max(abs(heat_rate_w), 1.0),
    }


def _geometry_index(raw: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {item["part_id"]: item["geometry"] for item in raw["parts"]}


def _physics(
    raw: Mapping[str, Any],
    geometry: Mapping[str, Any],
    overrides: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Compute the frozen operating case, returning declared-domain rejections as data."""
    option = dict(overrides or {})
    rejections: list[str] = []
    drive = raw["drive_case"]
    brake = raw["brake_case"]
    thermal = raw["thermal"]
    limits = raw["limits"]
    material = raw["material"]
    coupling = raw["couplings"][0]
    parts = _geometry_index(raw)

    drive_radius = float(coupling["drive_radius_m"])
    driven_radius = float(coupling["driven_radius_m"])
    ratio = driven_radius / drive_radius

    rotor_torque = float(option.get("rotor_torque_nm", drive["rotor_torque_nm"]))
    rotor_speed = float(option.get("rotor_angular_speed_rad_s", drive["rotor_angular_speed_rad_s"]))
    converter_efficiency = float(option.get("converter_efficiency", drive["converter_efficiency"]))
    drag_torque = float(option.get("support_drag_torque_nm", drive["support_drag_torque_nm"]))
    coolant_flow = float(option.get("coolant_mass_flow_kg_s", thermal["coolant_mass_flow_kg_s"]))
    torque_edges = option.get("torque_edges", raw["paths"]["torque_edges"])
    reaction_edges = option.get("reaction_edges", raw["paths"]["reaction_edges"])

    torque_path_count = unique_path_count(torque_edges, raw["paths"]["torque_source"], raw["paths"]["torque_sink"])
    reaction_path_count = unique_path_count(
        reaction_edges, raw["paths"]["reaction_source"], raw["paths"]["reaction_sink"]
    )
    if torque_path_count != 1:
        rejections.append("open_torque_path")
    if reaction_path_count != 1:
        rejections.append("open_reaction_path")

    if not 0.0 < converter_efficiency <= 1.0:
        rejections.append("efficiency_outside_unit_interval")
        converter_efficiency = 1.0
    elif converter_efficiency > limits["maximum_efficiency"]:
        rejections.append("declared_efficiency_exceeds_maximum")
    if rotor_torque <= 0.0:
        rejections.append("undeclared_energy_source")
    if rotor_speed > limits["maximum_rotor_angular_speed_rad_s"]:
        rejections.append("speed_domain_exceeded")
    rotor_surface_speed = rotor_speed * float(parts["converter_rotor"]["radius_m"])
    if rotor_surface_speed > limits["maximum_rotor_surface_speed_m_s"]:
        rejections.append("surface_speed_domain_exceeded")

    output_speed = rotor_speed / ratio
    ideal_torque = rotor_torque * ratio
    output_torque = ideal_torque - drag_torque
    mechanism_efficiency = output_torque / ideal_torque if ideal_torque != 0.0 else 1.0
    if mechanism_efficiency > limits["maximum_efficiency"]:
        rejections.append("declared_efficiency_exceeds_maximum")

    rotor_power = rotor_torque * rotor_speed
    output_power = output_torque * output_speed
    drag_power = drag_torque * output_speed
    primary_power = rotor_power / converter_efficiency
    converter_loss_power = primary_power - rotor_power

    rolling_residual = abs(rotor_speed * drive_radius - output_speed * driven_radius) / max(
        abs(rotor_speed * drive_radius), 1.0
    )
    traction_force_input = rotor_torque / drive_radius
    traction_force_output = ideal_torque / driven_radius
    force_residual = abs(traction_force_input - traction_force_output) / max(abs(traction_force_input), 1.0)
    power_residual = abs(rotor_power - output_power - drag_power) / max(abs(rotor_power), 1.0)
    torque_residual = max(rolling_residual, force_residual, power_residual)

    support_y = float(parts["support_block"]["box_center_m"][1])
    interface_y = float(raw["work083_interface"]["axle_outboard_y_m"])
    drum_y = 0.5 * (float(parts["ratio_drum"]["y_min_m"]) + float(parts["ratio_drum"]["y_max_m"]))
    if not interface_y < drum_y < support_y:
        raise EnergyTorquePathViolation("the transformation body must lie between the two output supports")
    span = support_y - interface_y
    support_reaction = traction_force_input * (drum_y - interface_y) / span
    interface_reaction = traction_force_input * (support_y - drum_y) / span
    reaction_residual = abs(support_reaction + interface_reaction - traction_force_input) / max(
        abs(traction_force_input), 1.0
    )

    duration = float(drive["duration_s"])
    primary_energy = primary_power * duration
    rotor_work = rotor_power * duration
    delivered_work = output_power * duration if torque_path_count == 1 else 0.0
    drag_energy = drag_power * duration
    converter_heat = converter_loss_power * duration
    energy_residuals = [
        abs(primary_energy - rotor_work - converter_heat) / max(abs(primary_energy), 1.0),
        abs(rotor_work - output_power * duration - drag_energy) / max(abs(rotor_work), 1.0),
    ]

    brake_speed = float(brake["output_angular_speed_rad_s"])
    brake_duration = float(brake["duration_s"])
    brake_power = abs(float(brake["output_brake_torque_nm"])) * brake_speed
    brake_source_energy = brake_power * brake_duration
    recovered_energy = brake_source_energy * float(brake["recovery_efficiency"])
    brake_heat = brake_source_energy - recovered_energy
    energy_residuals.append(
        abs(brake_source_energy - recovered_energy - brake_heat) / max(abs(brake_source_energy), 1.0)
    )
    if brake_source_energy > float(brake["source_kinetic_energy_j"]):
        rejections.append("brake_source_energy_exceeded")

    store = raw["energy_store_state"]
    cavity_volume = float(geometry["store_cavity_volume_m3"])
    medium_mass = cavity_volume * float(store["medium_density_kg_per_m3"])
    initial_energy = medium_mass * float(store["medium_specific_energy_j_per_kg"])
    energy_after_drive = initial_energy - primary_energy
    final_energy = energy_after_drive + recovered_energy
    energy_residuals.append(
        abs(initial_energy - primary_energy + recovered_energy - final_energy) / max(abs(initial_energy), 1.0)
    )
    if energy_after_drive <= 0.0:
        rejections.append("primary_energy_exhausted")
    if recovered_energy > brake_source_energy:
        rejections.append("recovered_energy_exceeds_source")
    energy_residual = max(energy_residuals)

    capacity_rate = coolant_flow * float(thermal["coolant_specific_heat_j_per_kg_k"])
    wall_conductance = float(thermal["coolant_wall_coefficient_w_per_m2_k"]) * float(geometry["coolant_wall_area_m2"])
    air_conductance = float(thermal["air_fin_coefficient_w_per_m2_k"]) * float(geometry["fin_area_m2"])
    drive_heat_rate = converter_loss_power + drag_power
    brake_heat_rate = brake_heat / brake_duration
    segments = {
        name: _thermal_segment(
            rate,
            wall_conductance,
            air_conductance,
            capacity_rate,
            float(thermal["coolant_inlet_temperature_k"]),
            float(thermal["air_temperature_k"]),
        )
        for name, rate in (("drive", drive_heat_rate), ("brake", brake_heat_rate))
    }
    coolant_velocity = (coolant_flow / float(thermal["coolant_density_kg_per_m3"])) / float(
        geometry["coolant_passage_section_m2"]
    )
    if coolant_velocity > float(thermal["maximum_coolant_velocity_m_s"]):
        rejections.append("coolant_velocity_exceeded")
    for name, segment in segments.items():
        if segment["coolant_temperature_rise_k"] > float(thermal["maximum_coolant_temperature_rise_k"]):
            rejections.append(f"coolant_temperature_rise_exceeded_{name}")
        if segment["housing_temperature_k"] > float(material["maximum_temperature_k"]):
            rejections.append(f"housing_temperature_exceeded_{name}")
    generated_energy = drive_heat_rate * duration + brake_heat_rate * brake_duration
    thermal_residual = max(
        max(segment["residual_relative"] for segment in segments.values()),
        abs(generated_energy - converter_heat - drag_energy - brake_heat) / max(abs(generated_energy), 1.0),
    )

    if rejections:
        state = "rejected"
    elif delivered_work == 0.0:
        state = "no_delivered_power"
    else:
        state = "operational_in_synthetic_verification"

    return {
        "subsystem_state": state,
        "rejections": sorted(set(rejections)),
        "torque_ratio": ratio,
        "rotor_torque_nm": rotor_torque,
        "rotor_angular_speed_rad_s": rotor_speed,
        "rotor_surface_speed_m_s": rotor_surface_speed,
        "output_angular_speed_rad_s": output_speed,
        "ideal_output_torque_nm": ideal_torque,
        "delivered_output_torque_nm": output_torque if torque_path_count == 1 else 0.0,
        "support_drag_torque_nm": drag_torque,
        "converter_efficiency": converter_efficiency,
        "mechanism_efficiency": mechanism_efficiency,
        "overall_drive_efficiency": delivered_work / primary_energy if primary_energy != 0.0 else 0.0,
        "traction_force_n": traction_force_input,
        "support_reaction_n": support_reaction,
        "work083_interface_reaction_n": interface_reaction,
        "torque_path_count": torque_path_count,
        "reaction_path_count": reaction_path_count,
        "torque_residual_relative": torque_residual,
        "reaction_residual_relative": reaction_residual,
        "primary_energy_j": primary_energy,
        "rotor_work_j": rotor_work,
        "delivered_work_j": delivered_work,
        "converter_heat_j": converter_heat,
        "mechanism_heat_j": drag_energy,
        "brake_source_energy_j": brake_source_energy,
        "recovered_energy_j": recovered_energy,
        "brake_heat_j": brake_heat,
        "external_primary_inflow_j": float(store["external_primary_inflow_j"]),
        "store_medium_mass_kg": medium_mass,
        "store_initial_energy_j": initial_energy,
        "store_final_energy_j": final_energy,
        "energy_residual_relative": energy_residual,
        "coolant_velocity_m_s": coolant_velocity,
        "thermal_segments": segments,
        "generated_heat_j": generated_energy,
        "thermal_residual_relative": thermal_residual,
    }


def _round_section(radius: float) -> tuple[float, float]:
    """Polar second moment and bending section modulus of a solid circular section."""
    return math.pi * radius ** 4 / 2.0, math.pi * radius ** 3 / 4.0


def _structural_margins(raw: Mapping[str, Any], physics: Mapping[str, Any]) -> dict[str, Any]:
    parts = _geometry_index(raw)
    material = raw["material"]
    yield_pa = float(material["yield_strength_pa"])
    shear_yield_pa = yield_pa / math.sqrt(3.0)
    force = physics["traction_force_n"]

    interface_y = float(raw["work083_interface"]["axle_outboard_y_m"])
    support_y = float(parts["support_block"]["box_center_m"][1])
    drum_y = 0.5 * (float(parts["ratio_drum"]["y_min_m"]) + float(parts["ratio_drum"]["y_max_m"]))
    span = support_y - interface_y

    output_radius = float(parts["output_shaft"]["radius_m"])
    output_polar, output_modulus = _round_section(output_radius)
    output_moment = force * (drum_y - interface_y) * (support_y - drum_y) / span
    output_shear = abs(physics["delivered_output_torque_nm"]) * output_radius / output_polar
    output_bending = output_moment / output_modulus
    output_vm = math.sqrt(output_bending ** 2 + 3.0 * output_shear ** 2)

    input_radius = float(parts["input_shaft"]["radius_m"])
    input_polar, input_modulus = _round_section(input_radius)
    cantilever = drum_y - float(parts["converter_rotor"]["y_max_m"])
    if cantilever <= 0.0:
        raise EnergyTorquePathViolation("the traction band must lie outboard of the rotor bearing")
    input_moment = force * cantilever
    input_shear = abs(physics["rotor_torque_nm"]) * input_radius / input_polar
    input_bending = input_moment / input_modulus
    input_vm = math.sqrt(input_bending ** 2 + 3.0 * input_shear ** 2)

    block = parts["support_block"]
    block_width = float(block["box_size_m"][1])
    block_height = float(block["box_size_m"][2])
    bore_radius = float(block["bore_radius_m"])
    ligament = block_height - 2.0 * bore_radius
    if ligament <= 0.0:
        raise EnergyTorquePathViolation("the support bore removes the whole block section")
    reaction = physics["support_reaction_n"]
    bearing_pressure = reaction / (2.0 * bore_radius * block_width)
    ligament_shear = reaction / (ligament * block_width)

    housing_size = parts["converter_housing"]["box_size_m"]
    mount_area = float(housing_size[1]) * float(housing_size[2])
    mount_modulus = float(housing_size[2]) * float(housing_size[1]) ** 2 / 6.0
    mount_direct = force / mount_area
    mount_bending = input_moment / mount_modulus
    mount_couple = abs(physics["rotor_torque_nm"]) / float(housing_size[2])
    mount_shear = mount_couple / (0.5 * mount_area)
    mount_combined = mount_direct + mount_bending + mount_shear

    cases = {
        "output_shaft_combined": {
            "bending_moment_nm": output_moment,
            "torsional_shear_pa": output_shear,
            "bending_stress_pa": output_bending,
            "von_mises_pa": output_vm,
            "utilization": output_vm / yield_pa,
        },
        "input_shaft_combined": {
            "cantilever_m": cantilever,
            "bending_moment_nm": input_moment,
            "torsional_shear_pa": input_shear,
            "bending_stress_pa": input_bending,
            "von_mises_pa": input_vm,
            "utilization": input_vm / yield_pa,
        },
        "support_block_bearing": {
            "radial_reaction_n": reaction,
            "bearing_pressure_pa": bearing_pressure,
            "ligament_shear_pa": ligament_shear,
            "utilization": max(
                bearing_pressure / float(material["allowable_bearing_pressure_pa"]),
                ligament_shear / shear_yield_pa,
            ),
        },
        "converter_housing_mount": {
            "mount_area_m2": mount_area,
            "direct_stress_pa": mount_direct,
            "bending_stress_pa": mount_bending,
            "torque_shear_pa": mount_shear,
            "combined_stress_pa": mount_combined,
            "utilization": mount_combined / yield_pa,
        },
    }
    if tuple(cases) != REQUIRED_STRUCTURAL_CASES:
        raise EnergyTorquePathViolation("analytic structural case set changed")
    return {
        "evidence_class": "analytic_synthetic_verification",
        "meshed_solver_evidence": False,
        "design_use_allowed": False,
        "cases": cases,
        "maximum_utilization": max(case["utilization"] for case in cases.values()),
        "unsupported_modes": ["fatigue", "fracture", "buckling", "contact", "thermal_stress", "meshed_stress_field"],
    }


def _controls(raw: Mapping[str, Any], geometry: Mapping[str, Any], physics: Mapping[str, Any]) -> dict[str, Any]:
    settings = raw["control_settings"]
    paths = raw["paths"]
    coupling = raw["couplings"][0]
    parts = _geometry_index(raw)
    results: dict[str, Any] = {}

    interface_y = -float(raw["work083_interface"]["axle_outboard_y_m"])
    support_y = -float(parts["support_block"]["box_center_m"][1])
    drum_y = -0.5 * (float(parts["ratio_drum"]["y_min_m"]) + float(parts["ratio_drum"]["y_max_m"]))
    mirrored_span = support_y - interface_y
    mirrored_support_reaction = physics["traction_force_n"] * (drum_y - interface_y) / mirrored_span
    results["mirror"] = {
        "status": "passed",
        "rotation_axis_y_sign": -1,
        "torque_ratio": physics["torque_ratio"],
        "delivered_work_j": physics["delivered_work_j"],
        "support_reaction_n": mirrored_support_reaction,
        "support_reaction_matches_reference": math.isclose(
            mirrored_support_reaction, physics["support_reaction_n"], rel_tol=1e-12, abs_tol=0.0
        ),
        "subsystem_state": physics["subsystem_state"],
    }
    if not results["mirror"]["support_reaction_matches_reference"]:
        raise EnergyTorquePathViolation("the mirrored candidate broke the declared lateral symmetry")

    broken_torque_edges = [
        edge for edge in paths["torque_edges"]
        if sorted(edge) != sorted([coupling["drive_part_id"], coupling["driven_part_id"]])
    ]
    if len(broken_torque_edges) != len(paths["torque_edges"]) - 1:
        raise EnergyTorquePathViolation("the broken-coupling control did not remove exactly one edge")
    open_reaction_edges = [
        edge for edge in paths["reaction_edges"] if sorted(edge) != sorted(["converter_housing", "energy_store"])
    ]
    if len(open_reaction_edges) != len(paths["reaction_edges"]) - 1:
        raise EnergyTorquePathViolation("the housing-reaction control did not remove exactly one edge")

    injections = {
        "locked_converter": (
            {"rotor_angular_speed_rad_s": settings["locked_converter_angular_speed_rad_s"]},
            "no_delivered_power",
            None,
            True,
        ),
        "seized_support": (
            {"support_drag_torque_nm": physics["ideal_output_torque_nm"]},
            "rejected",
            "housing_temperature_exceeded_drive",
            True,
        ),
        "broken_coupling": ({"torque_edges": broken_torque_edges}, "rejected", "open_torque_path", True),
        "zero_loss_exploit": (
            {
                "converter_efficiency": settings["zero_loss_converter_efficiency"],
                "support_drag_torque_nm": settings["zero_loss_drag_torque_nm"],
            },
            "rejected",
            "declared_efficiency_exceeds_maximum",
            False,
        ),
        "efficiency_over_one": (
            {"converter_efficiency": settings["efficiency_over_one_value"]},
            "rejected",
            "efficiency_outside_unit_interval",
            False,
        ),
        "reversed_torque": (
            {"rotor_torque_nm": -float(raw["drive_case"]["rotor_torque_nm"])},
            "rejected",
            "undeclared_energy_source",
            False,
        ),
        "overspeed": (
            {"rotor_angular_speed_rad_s": settings["overspeed_angular_speed_rad_s"]},
            "rejected",
            "speed_domain_exceeded",
            False,
        ),
        "inadequate_cooling": (
            {"coolant_mass_flow_kg_s": settings["inadequate_cooling_mass_flow_kg_s"]},
            "rejected",
            "coolant_temperature_rise_exceeded_brake",
            False,
        ),
        "disconnected_housing_reaction": (
            {"reaction_edges": open_reaction_edges},
            "rejected",
            "open_reaction_path",
            False,
        ),
    }

    for name, (overrides, expected_state, expected_rejection, expect_zero_work) in injections.items():
        outcome = _physics(raw, geometry, overrides)
        if outcome["subsystem_state"] != expected_state:
            raise EnergyTorquePathViolation(f"control {name} did not reach its preregistered state")
        if expected_rejection is not None and expected_rejection not in outcome["rejections"]:
            raise EnergyTorquePathViolation(f"control {name} did not produce its preregistered rejection")
        if expect_zero_work and outcome["delivered_work_j"] != 0.0:
            raise EnergyTorquePathViolation(f"control {name} still delivered work")
        results[name] = {
            "status": "passed",
            "subsystem_state": outcome["subsystem_state"],
            "rejections": outcome["rejections"],
            "delivered_work_j": outcome["delivered_work_j"],
            "delivered_output_torque_nm": outcome["delivered_output_torque_nm"],
            "torque_path_count": outcome["torque_path_count"],
            "reaction_path_count": outcome["reaction_path_count"],
            "brake_coolant_temperature_rise_k": outcome["thermal_segments"]["brake"]["coolant_temperature_rise_k"],
            "brake_housing_temperature_k": outcome["thermal_segments"]["brake"]["housing_temperature_k"],
        }

    if set(results) != REQUIRED_CONTROLS:
        raise EnergyTorquePathViolation("executed control set does not equal the declared control set")
    return results


def evaluate_candidate(
    raw: Mapping[str, Any],
    geometry_manifest: Mapping[str, Any],
    freecad_report: Mapping[str, Any],
    work083_result: Mapping[str, Any],
) -> dict[str, Any]:
    declaration = validate_declaration(raw)
    geometry = _verify_geometry(raw, geometry_manifest)
    freecad = _verify_freecad(geometry_manifest, freecad_report)
    work083 = _verify_work083(raw, work083_result)
    physics = _physics(raw, geometry)
    gates = raw["gates"]

    if physics["rejections"]:
        raise EnergyTorquePathViolation(
            "the reference case violated declared domains: " + ", ".join(physics["rejections"])
        )
    if physics["torque_residual_relative"] > gates["torque_residual_relative"]:
        raise EnergyTorquePathViolation("torque residual exceeds gate")
    if physics["reaction_residual_relative"] > gates["reaction_residual_relative"]:
        raise EnergyTorquePathViolation("reaction residual exceeds gate")
    if physics["energy_residual_relative"] > gates["energy_residual_relative"]:
        raise EnergyTorquePathViolation("energy residual exceeds gate")
    if physics["thermal_residual_relative"] > gates["thermal_residual_relative"]:
        raise EnergyTorquePathViolation("thermal residual exceeds gate")
    if physics["external_primary_inflow_j"] != 0.0:
        raise EnergyTorquePathViolation("external primary energy inflow is not zero")
    if physics["store_final_energy_j"] > physics["store_initial_energy_j"]:
        raise EnergyTorquePathViolation("the reference sequence ends above its onboard pre-race energy")
    if physics["subsystem_state"] != "operational_in_synthetic_verification":
        raise EnergyTorquePathViolation("the reference case is not operational")

    structural = _structural_margins(raw, physics)
    if structural["maximum_utilization"] > raw["structural_analytic"]["maximum_utilization"]:
        raise EnergyTorquePathViolation("an analytic structural case exceeds its declared utilization limit")

    controls = _controls(raw, geometry, physics)
    if any(control["status"] != "passed" for control in controls.values()):
        raise EnergyTorquePathViolation("a required control did not pass")

    draft = {
        "status": "passed",
        "candidate_id": raw["candidate_id"],
        "candidate_verdict": "not_admitted_synthetic_evidence",
        "design_use_allowed": False,
        "subsystem_state": physics["subsystem_state"],
        "declaration": declaration,
        "geometry": geometry,
        "freecad": freecad,
        "work083_interface": work083,
        "physics": physics,
        "structural_analytic": structural,
        "controls": controls,
        "unmet_program_gates": [
            "meshed structural cases for the shaft, support, and housing under Work 082 gates were not run",
        ],
        "limitations": [
            "synthetic material, process, and measurement evidence",
            "quasi-static drive and constant-speed braking segments with no modelled speed decay",
            "declared quasi-steady thermal segments with zero housing thermal storage",
            "traction engagement elements, fasteners, and lubrication flow are not modelled",
            "the Work 083 axle is loaded by this candidate beyond any load case Work 082 evaluated",
            "no tyre, fatigue, bearing life, dynamic, manufacturing, safety, or physical validation",
        ],
    }
    return {**draft, "evaluation_sha256": canonical_sha256(draft)}
