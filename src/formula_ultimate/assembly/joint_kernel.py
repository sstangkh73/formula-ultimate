"""Deterministic mechanical assembly and joint kernel for Work 080.

The kernel evaluates declaration geometry, constraint rank, realized DOF,
clearance, and conservative continuous swept-envelope collision.  It does not
silently align, repair, clip, or infer an assembly.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any, Mapping, Sequence


ASSEMBLY_KERNEL_VERSION = "mechanical_assembly_joint_kernel_v1"
GROUND_ID = "__ground__"
JOINT_DOFS = {
    "fixed": (),
    "revolute": ("rotation_about_joint_axis",),
    "prismatic": ("translation_along_joint_axis",),
    "spherical": (
        "rotation_about_joint_x",
        "rotation_about_joint_y",
        "rotation_about_joint_z",
    ),
}
INTERFACE_TYPES = {
    "fixed_mount",
    "revolute",
    "prismatic",
    "spherical",
    "bearing_seat",
    "shaft_coupling",
    "bolted",
    "welded",
}
JOINT_INTERFACE_TYPES = {
    "fixed": {"fixed_mount", "bolted", "welded", "shaft_coupling"},
    "revolute": {"revolute", "bearing_seat", "shaft_coupling"},
    "prismatic": {"prismatic"},
    "spherical": {"spherical"},
}
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ID = re.compile(r"^[a-z][a-z0-9_.-]*$")


class AssemblyKernelViolation(ValueError):
    """Stable coded rejection from the Work 080 assembly kernel."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"[{code}] {message}")


def _fail(code: str, message: str) -> None:
    raise AssemblyKernelViolation(code, message)


def _mapping(value: Any, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail("schema_error", f"{context} must be an object")
    return value


def _sequence(value: Any, context: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        _fail("schema_error", f"{context} must be an array")
    return value


def _exact(value: Mapping[str, Any], expected: set[str], context: str) -> None:
    missing = expected - set(value)
    unknown = set(value) - expected
    if missing or unknown:
        _fail(
            "schema_error",
            f"{context} keys mismatch; missing={sorted(missing)}, unknown={sorted(unknown)}",
        )


def _identifier(value: Any, context: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        _fail("schema_error", f"{context} must be a lower-case identifier")
    return value


def _number(value: Any, context: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail("invalid_numeric_value", f"{context} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        _fail("invalid_numeric_value", f"{context} must be finite")
    return result


def _integer(value: Any, context: str) -> int:
    result = _number(value, context)
    if not result.is_integer():
        _fail("invalid_numeric_value", f"{context} must be an integer")
    return int(result)


def _positive(value: Any, context: str) -> float:
    result = _number(value, context)
    if result <= 0.0:
        _fail("invalid_numeric_value", f"{context} must be > 0")
    return result


def _nonnegative(value: Any, context: str) -> float:
    result = _number(value, context)
    if result < 0.0:
        _fail("invalid_numeric_value", f"{context} must be >= 0")
    return result


def _sha(value: Any, context: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        _fail("invalid_hash", f"{context} must be a lower-case SHA-256")
    return value


Vector = tuple[float, float, float]
Frame = tuple[Vector, Vector, Vector, Vector]


def _vec(value: Any, context: str) -> Vector:
    items = _sequence(value, context)
    if len(items) != 3:
        _fail("invalid_frame", f"{context} must contain three values")
    return tuple(_number(item, context) for item in items)  # type: ignore[return-value]


def _add(a: Vector, b: Vector) -> Vector:
    return tuple(a[index] + b[index] for index in range(3))  # type: ignore[return-value]


def _sub(a: Vector, b: Vector) -> Vector:
    return tuple(a[index] - b[index] for index in range(3))  # type: ignore[return-value]


def _scale(a: Vector, value: float) -> Vector:
    return tuple(item * value for item in a)  # type: ignore[return-value]


def _dot(a: Vector, b: Vector) -> float:
    return math.fsum(a[index] * b[index] for index in range(3))


def _cross(a: Vector, b: Vector) -> Vector:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _norm(a: Vector) -> float:
    return math.sqrt(_dot(a, a))


def _unit(a: Vector, context: str) -> Vector:
    length = _norm(a)
    if length <= 1e-15:
        _fail("invalid_frame", f"{context} has zero length")
    return _scale(a, 1.0 / length)


def _frame(value: Any, context: str) -> Frame:
    raw = _mapping(value, context)
    _exact(raw, {"origin_m", "x_axis", "y_axis", "z_axis"}, context)
    origin = _vec(raw["origin_m"], f"{context}.origin_m")
    x_axis = _vec(raw["x_axis"], f"{context}.x_axis")
    y_axis = _vec(raw["y_axis"], f"{context}.y_axis")
    z_axis = _vec(raw["z_axis"], f"{context}.z_axis")
    tolerance = 1e-9
    if any(abs(_norm(axis) - 1.0) > tolerance for axis in (x_axis, y_axis, z_axis)):
        _fail("invalid_frame", f"{context} axes must have unit length")
    if any(
        abs(value) > tolerance
        for value in (_dot(x_axis, y_axis), _dot(x_axis, z_axis), _dot(y_axis, z_axis))
    ):
        _fail("invalid_frame", f"{context} axes must be orthogonal")
    if _norm(_sub(_cross(x_axis, y_axis), z_axis)) > tolerance:
        _fail("invalid_frame", f"{context} must be right-handed")
    return origin, x_axis, y_axis, z_axis


def _basis_transform(frame: Frame, local: Vector) -> Vector:
    return _add(
        frame[0],
        _add(
            _scale(frame[1], local[0]),
            _add(_scale(frame[2], local[1]), _scale(frame[3], local[2])),
        ),
    )


def _direction_transform(frame: Frame, local: Vector) -> Vector:
    return _add(
        _scale(frame[1], local[0]),
        _add(_scale(frame[2], local[1]), _scale(frame[3], local[2])),
    )


def _compose(parent: Frame, local: Frame) -> Frame:
    return (
        _basis_transform(parent, local[0]),
        _direction_transform(parent, local[1]),
        _direction_transform(parent, local[2]),
        _direction_transform(parent, local[3]),
    )


def _angle(a: Vector, b: Vector, *, unsigned_axis: bool) -> float:
    cosine = _dot(_unit(a, "axis"), _unit(b, "axis"))
    if unsigned_axis:
        cosine = abs(cosine)
    return math.acos(max(-1.0, min(1.0, cosine)))


def _orthogonal_basis(axis: Vector) -> tuple[Vector, Vector]:
    z_axis = _unit(axis, "joint axis")
    helper = (1.0, 0.0, 0.0) if abs(z_axis[0]) < 0.8 else (0.0, 1.0, 0.0)
    first = _unit(_cross(z_axis, helper), "joint perpendicular")
    second = _unit(_cross(z_axis, first), "joint perpendicular")
    return first, second


def _rank(matrix: Sequence[Sequence[float]], tolerance: float) -> int:
    if not matrix:
        return 0
    work = [list(row) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = max(range(pivot_row, rows), key=lambda row: abs(work[row][column]), default=pivot_row)
        if abs(work[pivot][column]) <= tolerance:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = work[row][column]
            if abs(factor) <= tolerance:
                continue
            work[row] = [
                work[row][index] - factor * work[pivot_row][index]
                for index in range(columns)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def _segment_distance(a0: Vector, a1: Vector, b0: Vector, b1: Vector) -> float:
    # Closest distance between two finite 3D segments (Ericson form).
    u = _sub(a1, a0)
    v = _sub(b1, b0)
    w = _sub(a0, b0)
    aa = _dot(u, u)
    bb = _dot(u, v)
    cc = _dot(v, v)
    dd = _dot(u, w)
    ee = _dot(v, w)
    denominator = aa * cc - bb * bb
    small = 1e-18
    if aa <= small and cc <= small:
        return _norm(w)
    if aa <= small:
        s_value = 0.0
        t_value = max(0.0, min(1.0, ee / cc))
    elif cc <= small:
        t_value = 0.0
        s_value = max(0.0, min(1.0, -dd / aa))
    else:
        s_value = 0.0 if denominator <= small else max(0.0, min(1.0, (bb * ee - cc * dd) / denominator))
        t_value = (bb * s_value + ee) / cc
        if t_value < 0.0:
            t_value = 0.0
            s_value = max(0.0, min(1.0, -dd / aa))
        elif t_value > 1.0:
            t_value = 1.0
            s_value = max(0.0, min(1.0, (bb - dd) / aa))
    closest = _sub(_add(w, _scale(u, s_value)), _scale(v, t_value))
    return _norm(closest)


def canonical_assembly_bytes(value: Mapping[str, Any]) -> bytes:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        _fail("canonicalization_error", str(exc))


def assembly_declaration_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_assembly_bytes(value)).hexdigest()


def _validate_interface(raw_value: Any, context: str) -> dict[str, Any]:
    raw = _mapping(raw_value, context)
    _exact(raw, {"interface_id", "interface_type", "frame", "tolerance_m"}, context)
    interface_id = _identifier(raw["interface_id"], f"{context}.interface_id")
    if raw["interface_type"] not in INTERFACE_TYPES:
        _fail("unsupported_interface", f"{context} interface_type is unsupported")
    frame = _frame(raw["frame"], f"{context}.frame")
    tolerance = _positive(raw["tolerance_m"], f"{context}.tolerance_m")
    return {
        "interface_id": interface_id,
        "interface_type": raw["interface_type"],
        "frame": frame,
        "tolerance_m": tolerance,
    }


def _parse(value: Mapping[str, Any]) -> dict[str, Any]:
    root = _mapping(value, "assembly")
    _exact(
        root,
        {
            "kernel_version",
            "assembly_id",
            "tolerances",
            "ground_interfaces",
            "components",
            "joints",
            "expected",
            "claim_boundary",
        },
        "assembly",
    )
    if root["kernel_version"] != ASSEMBLY_KERNEL_VERSION:
        _fail("version_mismatch", "kernel_version mismatch")
    assembly_id = _identifier(root["assembly_id"], "assembly_id")
    tolerance_raw = _mapping(root["tolerances"], "tolerances")
    _exact(
        tolerance_raw,
        {"mate_position_m", "mate_angle_rad", "rank_absolute", "collision_m"},
        "tolerances",
    )
    tolerances = {
        name: _positive(item, name) for name, item in tolerance_raw.items()
    }

    ground_interfaces: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(_sequence(root["ground_interfaces"], "ground_interfaces")):
        interface = _validate_interface(item, f"ground_interfaces[{index}]")
        if interface["interface_id"] in ground_interfaces:
            _fail("duplicate_interface", "duplicate ground interface")
        ground_interfaces[interface["interface_id"]] = interface
    if not ground_interfaces:
        _fail("missing_interface", "ground_interfaces must not be empty")

    components: dict[str, dict[str, Any]] = {}
    for index, raw_component in enumerate(_sequence(root["components"], "components")):
        component = _mapping(raw_component, f"components[{index}]")
        _exact(
            component,
            {"component_id", "geometry_sha256", "frame", "interfaces", "collision_spheres"},
            f"components[{index}]",
        )
        component_id = _identifier(component["component_id"], "component_id")
        if component_id in components or component_id == GROUND_ID:
            _fail("duplicate_component", "duplicate or reserved component_id")
        geometry_sha = _sha(component["geometry_sha256"], "component geometry_sha256")
        frame = _frame(component["frame"], f"component {component_id}.frame")
        interfaces: dict[str, dict[str, Any]] = {}
        for interface_index, raw_interface in enumerate(
            _sequence(component["interfaces"], f"component {component_id}.interfaces")
        ):
            interface = _validate_interface(
                raw_interface, f"component {component_id}.interfaces[{interface_index}]"
            )
            if interface["interface_id"] in interfaces:
                _fail("duplicate_interface", f"component {component_id} has duplicate interface")
            interfaces[interface["interface_id"]] = interface
        if not interfaces:
            _fail("missing_interface", f"component {component_id} has no interface")
        spheres = []
        for sphere_index, raw_sphere in enumerate(
            _sequence(component["collision_spheres"], f"component {component_id}.collision_spheres")
        ):
            sphere = _mapping(raw_sphere, "collision sphere")
            _exact(sphere, {"sphere_id", "center_m", "radius_m"}, "collision sphere")
            spheres.append(
                {
                    "sphere_id": _identifier(sphere["sphere_id"], "sphere_id"),
                    "center_m": _vec(sphere["center_m"], "collision sphere center_m"),
                    "radius_m": _positive(sphere["radius_m"], "collision sphere radius_m"),
                }
            )
        if not spheres or len({item["sphere_id"] for item in spheres}) != len(spheres):
            _fail("invalid_collision_proxy", f"component {component_id} collision spheres are missing or duplicate")
        components[component_id] = {
            "component_id": component_id,
            "geometry_sha256": geometry_sha,
            "frame": frame,
            "interfaces": interfaces,
            "collision_spheres": spheres,
        }
    if not components:
        _fail("missing_component", "components must not be empty")

    joints = []
    joint_ids: set[str] = set()
    for index, raw_joint in enumerate(_sequence(root["joints"], "joints")):
        joint = _mapping(raw_joint, f"joints[{index}]")
        _exact(
            joint,
            {
                "joint_id",
                "joint_type",
                "component_a",
                "interface_a",
                "component_b",
                "interface_b",
                "limits",
                "declared_dofs",
                "clearance",
                "preload_n",
                "stiffness",
            },
            f"joints[{index}]",
        )
        joint_id = _identifier(joint["joint_id"], "joint_id")
        if joint_id in joint_ids:
            _fail("duplicate_joint", "duplicate joint_id")
        joint_ids.add(joint_id)
        joint_type = joint["joint_type"]
        if joint_type not in JOINT_DOFS:
            _fail("unsupported_joint", "joint_type is unsupported")
        component_a = joint["component_a"]
        component_b = joint["component_b"]
        for name, component_id in (("component_a", component_a), ("component_b", component_b)):
            if component_id != GROUND_ID and component_id not in components:
                _fail("unknown_component", f"{name} references an unknown component")
        if component_a == component_b:
            _fail("invalid_joint", "a joint cannot connect a component to itself")
        interface_a = _identifier(joint["interface_a"], "interface_a")
        interface_b = _identifier(joint["interface_b"], "interface_b")

        limits_raw = _mapping(joint["limits"], "joint limits")
        _exact(limits_raw, {"minimum", "home", "maximum"}, "joint limits")
        limits = tuple(_number(limits_raw[name], f"limits.{name}") for name in ("minimum", "home", "maximum"))
        if not limits[0] <= limits[1] <= limits[2]:
            _fail("invalid_joint_limits", "joint limits must contain home in increasing order")
        if joint_type == "fixed" and limits != (0.0, 0.0, 0.0):
            _fail("invalid_joint_limits", "fixed joint limits must be zero")

        declared_dofs = tuple(_sequence(joint["declared_dofs"], "declared_dofs"))
        if declared_dofs != JOINT_DOFS[joint_type]:
            _fail("declared_dof_mismatch", "declared_dofs disagree with joint_type")

        clearance_raw = _mapping(joint["clearance"], "joint clearance")
        _exact(clearance_raw, {"axial_m", "radial_m", "maximum_axial_m", "maximum_radial_m"}, "joint clearance")
        clearance = {
            name: _nonnegative(value, f"clearance.{name}")
            for name, value in clearance_raw.items()
        }
        if clearance["axial_m"] > clearance["maximum_axial_m"] or clearance["radial_m"] > clearance["maximum_radial_m"]:
            _fail("excessive_clearance", "joint clearance exceeds its declared maximum")

        stiffness_raw = _mapping(joint["stiffness"], "joint stiffness")
        _exact(stiffness_raw, {"translational_n_per_m", "rotational_nm_per_rad"}, "joint stiffness")
        stiffness = {
            name: _positive(value, f"stiffness.{name}")
            for name, value in stiffness_raw.items()
        }
        joints.append(
            {
                "joint_id": joint_id,
                "joint_type": joint_type,
                "component_a": component_a,
                "interface_a": interface_a,
                "component_b": component_b,
                "interface_b": interface_b,
                "limits": limits,
                "declared_dofs": declared_dofs,
                "clearance": clearance,
                "preload_n": _nonnegative(joint["preload_n"], "preload_n"),
                "stiffness": stiffness,
            }
        )
    if not joints:
        _fail("missing_joint", "joints must not be empty")

    expected_raw = _mapping(root["expected"], "expected")
    _exact(expected_raw, {"constraint_rank", "realized_dof_count", "component_dofs"}, "expected")
    expected_component_dofs = _mapping(expected_raw["component_dofs"], "expected.component_dofs")
    if set(expected_component_dofs) != set(components):
        _fail("schema_error", "expected.component_dofs must cover every component exactly")
    expected = {
        "constraint_rank": _integer(expected_raw["constraint_rank"], "expected.constraint_rank"),
        "realized_dof_count": _integer(expected_raw["realized_dof_count"], "expected.realized_dof_count"),
        "component_dofs": {key: tuple(_sequence(value, f"component_dofs.{key}")) for key, value in expected_component_dofs.items()},
    }

    claim = _mapping(root["claim_boundary"], "claim_boundary")
    _exact(claim, {"admitted_claims", "prohibited_claims"}, "claim_boundary")
    admitted = set(_sequence(claim["admitted_claims"], "admitted_claims"))
    prohibited = set(_sequence(claim["prohibited_claims"], "prohibited_claims"))
    if not {"calculated_dof", "deterministic_assembly", "conservative_motion_envelope"} <= admitted or not {"physical_validation", "bearing_life", "joint_strength", "continuous_exact_brep_collision"} <= prohibited:
        _fail("claim_boundary_mismatch", "assembly claim boundary is incomplete")

    return {
        "assembly_id": assembly_id,
        "tolerances": tolerances,
        "ground_interfaces": ground_interfaces,
        "components": components,
        "joints": joints,
        "expected": expected,
    }


def _world_interface(parsed: Mapping[str, Any], component_id: str, interface_id: str) -> dict[str, Any]:
    if component_id == GROUND_ID:
        if interface_id not in parsed["ground_interfaces"]:
            _fail("missing_interface", f"ground interface {interface_id} is missing")
        return parsed["ground_interfaces"][interface_id]
    component = parsed["components"][component_id]
    if interface_id not in component["interfaces"]:
        _fail("missing_interface", f"component {component_id} interface {interface_id} is missing")
    interface = component["interfaces"][interface_id]
    return {**interface, "frame": _compose(component["frame"], interface["frame"])}


def _constraint_vectors(joint_type: str, axis: Vector) -> tuple[list[Vector], list[Vector]]:
    x_axis, y_axis = _orthogonal_basis(axis)
    global_axes = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
    if joint_type == "fixed":
        return global_axes, global_axes
    if joint_type == "revolute":
        return global_axes, [x_axis, y_axis]
    if joint_type == "prismatic":
        return [x_axis, y_axis], global_axes
    return global_axes, []


def _row(component_index: Mapping[str, int], component_a: str, component_b: str, vector: Vector, rotational: bool) -> list[float]:
    result = [0.0] * (6 * len(component_index))
    offset = 3 if rotational else 0
    if component_a != GROUND_ID:
        start = 6 * component_index[component_a] + offset
        for index in range(3):
            result[start + index] -= vector[index]
    if component_b != GROUND_ID:
        start = 6 * component_index[component_b] + offset
        for index in range(3):
            result[start + index] += vector[index]
    return result


def _component_envelopes(parsed: Mapping[str, Any], joint_by_component: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    envelopes = []
    for component_id, component in parsed["components"].items():
        if component_id not in joint_by_component:
            _fail("underconstrained_component", f"component {component_id} has no joint")
        joint = joint_by_component[component_id]
        interface_a = _world_interface(parsed, joint["component_a"], joint["interface_a"])
        interface_b = _world_interface(parsed, joint["component_b"], joint["interface_b"])
        allowed_interfaces = JOINT_INTERFACE_TYPES[joint["joint_type"]]
        if (
            interface_a["interface_type"] not in allowed_interfaces
            or interface_b["interface_type"] not in allowed_interfaces
        ):
            _fail(
                "incompatible_interface",
                f"joint {joint['joint_id']} interface types are incompatible with {joint['joint_type']}",
            )
        joint_origin = _scale(_add(interface_a["frame"][0], interface_b["frame"][0]), 0.5)
        axis = _unit(interface_a["frame"][3], "joint axis")
        for sphere in component["collision_spheres"]:
            home_center = _basis_transform(component["frame"], sphere["center_m"])
            radius = sphere["radius_m"]
            if joint["joint_type"] == "prismatic":
                start = _add(home_center, _scale(axis, joint["limits"][0] - joint["limits"][1]))
                end = _add(home_center, _scale(axis, joint["limits"][2] - joint["limits"][1]))
            elif joint["joint_type"] in {"revolute", "spherical"}:
                # A sphere about the joint origin is a conservative continuous
                # bound for every allowed rotation angle.
                radius += _norm(_sub(home_center, joint_origin))
                start = joint_origin
                end = joint_origin
            else:
                start = home_center
                end = home_center
            envelopes.append(
                {
                    "component_id": component_id,
                    "sphere_id": sphere["sphere_id"],
                    "start_m": start,
                    "end_m": end,
                    "radius_m": radius,
                    "method": "continuous_segment" if joint["joint_type"] == "prismatic" else "conservative_swept_sphere",
                }
            )
    return envelopes


def evaluate_assembly(value: Mapping[str, Any]) -> dict[str, Any]:
    parsed = _parse(value)
    component_ids = tuple(sorted(parsed["components"]))
    component_index = {component_id: index for index, component_id in enumerate(component_ids)}
    matrix: list[list[float]] = []
    joint_results = []
    joint_by_component: dict[str, Mapping[str, Any]] = {}
    component_dofs: dict[str, list[str]] = {component_id: [] for component_id in component_ids}

    for joint in parsed["joints"]:
        interface_a = _world_interface(parsed, joint["component_a"], joint["interface_a"])
        interface_b = _world_interface(parsed, joint["component_b"], joint["interface_b"])
        origin_residual = _norm(_sub(interface_a["frame"][0], interface_b["frame"][0]))
        unsigned_axis = joint["joint_type"] != "fixed"
        if joint["joint_type"] == "fixed":
            angle_residual = max(
                _angle(interface_a["frame"][axis], interface_b["frame"][axis], unsigned_axis=False)
                for axis in (1, 2, 3)
            )
        else:
            angle_residual = _angle(interface_a["frame"][3], interface_b["frame"][3], unsigned_axis=True)
        position_limit = min(
            parsed["tolerances"]["mate_position_m"],
            interface_a["tolerance_m"],
            interface_b["tolerance_m"],
        )
        angle_limit = parsed["tolerances"]["mate_angle_rad"]
        if origin_residual > position_limit:
            _fail("mate_position_mismatch", f"joint {joint['joint_id']} origin residual exceeds tolerance")
        if angle_residual > angle_limit:
            _fail("mate_axis_mismatch", f"joint {joint['joint_id']} axis residual exceeds tolerance")

        translation_vectors, rotation_vectors = _constraint_vectors(
            joint["joint_type"], interface_a["frame"][3]
        )
        for vector in translation_vectors:
            matrix.append(
                _row(component_index, joint["component_a"], joint["component_b"], vector, False)
            )
        for vector in rotation_vectors:
            matrix.append(
                _row(component_index, joint["component_a"], joint["component_b"], vector, True)
            )
        for component_id in (joint["component_a"], joint["component_b"]):
            if component_id == GROUND_ID:
                continue
            component_dofs[component_id].extend(joint["declared_dofs"])
            if component_id not in joint_by_component:
                joint_by_component[component_id] = joint
        joint_results.append(
            {
                "joint_id": joint["joint_id"],
                "joint_type": joint["joint_type"],
                "position_residual_m": origin_residual,
                "angle_residual_rad": angle_residual,
                "axial_clearance_m": joint["clearance"]["axial_m"],
                "radial_clearance_m": joint["clearance"]["radial_m"],
                "preload_n": joint["preload_n"],
                "constraint_rows": len(translation_vectors) + len(rotation_vectors),
            }
        )

    rank = _rank(matrix, parsed["tolerances"]["rank_absolute"])
    redundancy = len(matrix) - rank
    realized_dof_count = 6 * len(component_ids) - rank
    if redundancy > 0:
        _fail("overconstrained_assembly", f"constraint matrix has {redundancy} redundant rows")
    if rank != parsed["expected"]["constraint_rank"] or realized_dof_count != parsed["expected"]["realized_dof_count"]:
        _fail("realized_dof_mismatch", "calculated constraint rank/DOF differs from expected")
    normalized_component_dofs = {
        component_id: tuple(sorted(set(values)))
        for component_id, values in component_dofs.items()
    }
    expected_component_dofs = {
        component_id: tuple(sorted(values))
        for component_id, values in parsed["expected"]["component_dofs"].items()
    }
    if normalized_component_dofs != expected_component_dofs:
        _fail("realized_dof_type_mismatch", "calculated component DOF types differ from expected")

    envelopes = _component_envelopes(parsed, joint_by_component)
    collisions = []
    minimum_gap = math.inf
    for left_index, left in enumerate(envelopes):
        for right in envelopes[left_index + 1 :]:
            if left["component_id"] == right["component_id"]:
                continue
            gap = _segment_distance(
                left["start_m"], left["end_m"], right["start_m"], right["end_m"]
            ) - left["radius_m"] - right["radius_m"]
            minimum_gap = min(minimum_gap, gap)
            if gap < -parsed["tolerances"]["collision_m"]:
                collisions.append(
                    {
                        "component_a": left["component_id"],
                        "sphere_a": left["sphere_id"],
                        "component_b": right["component_id"],
                        "sphere_b": right["sphere_id"],
                        "penetration_m": -gap,
                    }
                )
    if collisions:
        _fail("motion_envelope_collision", "continuous conservative motion envelopes collide")

    body = {
        "status": "passed",
        "kernel_version": ASSEMBLY_KERNEL_VERSION,
        "assembly_id": parsed["assembly_id"],
        "declaration_sha256": assembly_declaration_sha256(value),
        "component_geometry_sha256": {
            component_id: parsed["components"][component_id]["geometry_sha256"]
            for component_id in component_ids
        },
        "component_count": len(component_ids),
        "joint_count": len(parsed["joints"]),
        "constraint_row_count": len(matrix),
        "constraint_rank": rank,
        "constraint_redundancy_count": redundancy,
        "realized_dof_count": realized_dof_count,
        "component_dofs": normalized_component_dofs,
        "joint_results": joint_results,
        "collision_method": "continuous_segment_and_conservative_swept_sphere",
        "minimum_motion_envelope_gap_m": minimum_gap,
        "collision_count": 0,
        "hidden_alignment_or_repair": False,
    }
    return {**body, "result_sha256": hashlib.sha256(canonical_assembly_bytes(body)).hexdigest()}
