"""Work 069 geometry-derived support polygon, load-transfer, and planar gate."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from typing import Any, Mapping, Sequence

from formula_ultimate.physics.lateral import (
    PlanarContact,
    PlanarSolverControl,
    PlanarState,
    PlanarVehicle,
    PlanarVehicleParameters,
    step_planar_dynamics,
)
from formula_ultimate.physics.tyre import TyreContactParameters
from formula_ultimate.topology.functional_vehicle import (
    FunctionalVehicle,
    from_functional_mapping,
    functional_declaration_sha256,
    functional_mass_properties,
    validate_functional_vehicle,
)


MODEL_VERSION = "stable_support_planar_gate_v1"
VARIANT_VERSION = "functional_vehicle_architecture_variant_v1"


class PlanarSupportGateError(ValueError):
    """Raised when support or planar-gate evidence is inadmissible."""


def _finite(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PlanarSupportGateError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise PlanarSupportGateError(f"{name} must be finite")
    return result


def _positive(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result <= 0.0:
        raise PlanarSupportGateError(f"{name} must be positive")
    return result


def _nonnegative(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result < 0.0:
        raise PlanarSupportGateError(f"{name} must be non-negative")
    return result


@dataclass(frozen=True, slots=True)
class LoadCase:
    case_id: str
    longitudinal_acceleration_m_per_s2: float
    lateral_acceleration_m_per_s2: float
    expected_status: str


@dataclass(frozen=True, slots=True)
class SupportGateConfig:
    protocol_id: str
    load_cases: tuple[LoadCase, ...]
    gravity_m_per_s2: float
    initial_longitudinal_speed_m_per_s: float
    steer_angle_rad: float
    duration_s: float
    time_step_s: float
    front_cornering_stiffness_n_per_rad: float
    rear_cornering_stiffness_n_per_rad: float
    front_requested_longitudinal_force_n: float
    friction_coefficient_longitudinal: float
    friction_coefficient_lateral: float
    maximum_steer_angle_rad: float
    geometry_relative_tolerance: float
    equilibrium_relative_tolerance: float
    refinement_relative_tolerance: float


@dataclass(frozen=True, slots=True)
class ContactPoint:
    contact_id: str
    component_id: str
    x_m: float
    y_m: float
    maximum_normal_force_n: float
    maximum_longitudinal_force_n: float
    maximum_lateral_force_n: float


@dataclass(frozen=True, slots=True)
class SupportAssessment:
    candidate_id: str
    status: str
    reason: str
    centre_of_mass_xy_m: tuple[float, float]
    contacts: tuple[ContactPoint, ...]
    convex_hull_xy_m: tuple[tuple[float, float], ...]
    polygon_area_m2: float
    signed_margin_m: float


@dataclass(frozen=True, slots=True)
class LoadCaseResult:
    case_id: str
    status: str
    normal_loads_n: tuple[tuple[str, float], ...]
    minimum_normal_load_n: float
    maximum_normal_utilization: float
    vertical_residual_n: float
    pitch_residual_nm: float
    roll_residual_nm: float


@dataclass(frozen=True, slots=True)
class PlanarRunResult:
    steer_angle_rad: float
    status: str
    reason: str
    requested_steps: int
    executed_steps: int
    final_state: PlanarState
    maximum_contact_utilization: float
    minimum_normal_load_n: float
    maximum_abs_balance_residual: float
    result_sha256: str


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def materialize_architecture_variant(base_raw: Mapping[str, Any], variant_raw: Mapping[str, Any]) -> dict[str, Any]:
    if variant_raw.get("variant_version") != VARIANT_VERSION:
        raise PlanarSupportGateError("architecture variant version mismatch")
    expected_hash = str(variant_raw.get("base_declaration_sha256", ""))
    if functional_declaration_sha256(base_raw) != expected_hash:
        raise PlanarSupportGateError("base architecture declaration hash mismatch")
    if base_raw.get("candidate_id") != variant_raw.get("base_candidate_id"):
        raise PlanarSupportGateError("base architecture candidate mismatch")
    result = deepcopy(dict(base_raw))
    result["protocol_id"] = str(variant_raw.get("protocol_id", ""))
    result["candidate_id"] = str(variant_raw.get("candidate_id", ""))
    result["claim_level"] = str(variant_raw.get("claim_level", ""))
    spine = next((item for item in result["components"] if item["component_id"] == "load_spine"), None)
    if spine is None:
        raise PlanarSupportGateError("base load_spine is missing")
    spine["ports"].append(deepcopy(variant_raw.get("load_spine_port")))
    result["components"].append(deepcopy(variant_raw.get("added_component")))
    result["connections"].append(deepcopy(variant_raw.get("added_connection")))
    result["ground_contacts"].append(deepcopy(variant_raw.get("added_ground_contact")))
    vehicle = from_functional_mapping(result)
    validate_functional_vehicle(vehicle)
    return result


def load_support_gate_config(raw: Mapping[str, Any]) -> SupportGateConfig:
    if raw.get("model_version") != MODEL_VERSION:
        raise PlanarSupportGateError("support gate model version mismatch")
    planar, numerical = raw.get("planar"), raw.get("numerical")
    if not isinstance(planar, Mapping) or not isinstance(numerical, Mapping):
        raise PlanarSupportGateError("planar or numerical section is missing")
    cases_raw = raw.get("load_cases")
    if not isinstance(cases_raw, Sequence) or isinstance(cases_raw, (str, bytes)) or not cases_raw:
        raise PlanarSupportGateError("load_cases must be nonempty")
    cases: list[LoadCase] = []
    for item in cases_raw:
        if not isinstance(item, Mapping):
            raise PlanarSupportGateError("load case must be a mapping")
        identity, expected = str(item.get("case_id", "")), str(item.get("expected_status", ""))
        if not identity or expected not in {"passed", "contact_lift"}:
            raise PlanarSupportGateError("load case identity or expected status is invalid")
        cases.append(LoadCase(
            identity,
            _finite("longitudinal_acceleration", item.get("longitudinal_acceleration_m_per_s2")),
            _finite("lateral_acceleration", item.get("lateral_acceleration_m_per_s2")),
            expected,
        ))
    if len({item.case_id for item in cases}) != len(cases):
        raise PlanarSupportGateError("load case identities are duplicated")
    config = SupportGateConfig(
        str(raw.get("protocol_id", "")), tuple(cases),
        _positive("gravity_m_per_s2", planar.get("gravity_m_per_s2")),
        _positive("initial_longitudinal_speed_m_per_s", planar.get("initial_longitudinal_speed_m_per_s")),
        _finite("steer_angle_rad", planar.get("steer_angle_rad")),
        _positive("duration_s", planar.get("duration_s")),
        _positive("time_step_s", planar.get("time_step_s")),
        _positive("front_cornering_stiffness", planar.get("front_cornering_stiffness_n_per_rad")),
        _positive("rear_cornering_stiffness", planar.get("rear_cornering_stiffness_n_per_rad")),
        _nonnegative("front_requested_longitudinal_force", planar.get("front_requested_longitudinal_force_n")),
        _positive("friction_coefficient_longitudinal", planar.get("friction_coefficient_longitudinal")),
        _positive("friction_coefficient_lateral", planar.get("friction_coefficient_lateral")),
        _positive("maximum_steer_angle_rad", planar.get("maximum_steer_angle_rad")),
        _positive("geometry_relative_tolerance", numerical.get("geometry_relative_tolerance")),
        _positive("equilibrium_relative_tolerance", numerical.get("equilibrium_relative_tolerance")),
        _positive("refinement_relative_tolerance", numerical.get("refinement_relative_tolerance")),
    )
    if not config.protocol_id.strip() or abs(config.steer_angle_rad) > config.maximum_steer_angle_rad:
        raise PlanarSupportGateError("protocol identity or steering command is invalid")
    if config.geometry_relative_tolerance > 1.0e-6 or config.equilibrium_relative_tolerance > 1.0e-6 or config.refinement_relative_tolerance > 0.02:
        raise PlanarSupportGateError("support numerical tolerance exceeds protocol ceiling")
    count = config.duration_s / config.time_step_s
    if not math.isclose(count, round(count), rel_tol=0.0, abs_tol=1.0e-10):
        raise PlanarSupportGateError("planar duration must be an integer multiple of step")
    return config


def _contact_points(vehicle: FunctionalVehicle) -> tuple[ContactPoint, ...]:
    components = {item.component_id: item for item in vehicle.components}
    points: list[ContactPoint] = []
    for contact in vehicle.ground_contacts:
        component = components[contact.component_id]
        port = next(item for item in component.ports if item.port_id == contact.port_id)
        world = tuple(component.position_m[index] + port.local_position_m[index] for index in range(3))
        if abs(world[2]) > vehicle.tolerances["geometry_m"]:
            raise PlanarSupportGateError("ground contact is not on z=0")
        points.append(ContactPoint(
            contact.contact_id, contact.component_id, world[0], world[1],
            contact.maximum_normal_force_n, contact.maximum_longitudinal_force_n,
            contact.maximum_lateral_force_n,
        ))
    return tuple(points)


def _cross(origin: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
    return (a[0] - origin[0]) * (b[1] - origin[1]) - (a[1] - origin[1]) * (b[0] - origin[0])


def _convex_hull(points: Sequence[tuple[float, float]]) -> tuple[tuple[float, float], ...]:
    unique = sorted(set(points))
    if len(unique) <= 1:
        return tuple(unique)
    lower: list[tuple[float, float]] = []
    for point in unique:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], point) <= 0.0:
            lower.pop()
        lower.append(point)
    upper: list[tuple[float, float]] = []
    for point in reversed(unique):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], point) <= 0.0:
            upper.pop()
        upper.append(point)
    return tuple(lower[:-1] + upper[:-1])


def _point_segment_distance(point: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
    dx, dy = b[0] - a[0], b[1] - a[1]
    length2 = dx * dx + dy * dy
    if length2 == 0.0:
        return math.hypot(point[0] - a[0], point[1] - a[1])
    t = max(0.0, min(1.0, ((point[0] - a[0]) * dx + (point[1] - a[1]) * dy) / length2))
    return math.hypot(point[0] - (a[0] + t * dx), point[1] - (a[1] + t * dy))


def assess_support_polygon(architecture_raw: Mapping[str, Any]) -> SupportAssessment:
    vehicle = from_functional_mapping(architecture_raw)
    validate_functional_vehicle(vehicle)
    mass = functional_mass_properties(vehicle)
    centre = (mass["centre_of_mass_m"][0], mass["centre_of_mass_m"][1])
    contacts = _contact_points(vehicle)
    hull = _convex_hull(tuple((item.x_m, item.y_m) for item in contacts))
    if len(hull) < 3:
        if len(hull) == 2:
            distance = _point_segment_distance(centre, hull[0], hull[1])
        elif hull:
            distance = math.hypot(centre[0] - hull[0][0], centre[1] - hull[0][1])
        else:
            distance = math.inf
        return SupportAssessment(vehicle.candidate_id, "unstable", "support hull is degenerate", centre, contacts, hull, 0.0, -distance)
    area2 = math.fsum(hull[index][0] * hull[(index + 1) % len(hull)][1] - hull[(index + 1) % len(hull)][0] * hull[index][1] for index in range(len(hull)))
    area = abs(area2) / 2.0
    if area2 < 0.0:
        hull = tuple(reversed(hull))
    distances = []
    for index, a in enumerate(hull):
        b = hull[(index + 1) % len(hull)]
        length = math.hypot(b[0] - a[0], b[1] - a[1])
        distances.append(_cross(a, b, centre) / length)
    margin = min(distances)
    status = "stable" if margin > vehicle.tolerances["geometry_m"] else "unstable"
    reason = "centre-of-mass projection is strictly inside support polygon" if status == "stable" else "centre-of-mass projection is outside or on support boundary"
    return SupportAssessment(vehicle.candidate_id, status, reason, centre, contacts, hull, area, margin)


def _solve_three(matrix: tuple[tuple[float, float, float], ...], vector: tuple[float, float, float]) -> tuple[float, float, float]:
    augmented = [list(row) + [value] for row, value in zip(matrix, vector)]
    for column in range(3):
        pivot = max(range(column, 3), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) <= 1.0e-14:
            raise PlanarSupportGateError("support load matrix is singular")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(3):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [value - factor * source for value, source in zip(augmented[row], augmented[column])]
    result = tuple(augmented[index][3] for index in range(3))
    if not all(math.isfinite(value) for value in result):
        raise PlanarSupportGateError("support load solution is non-finite")
    return result  # type: ignore[return-value]


def solve_support_load_case(architecture_raw: Mapping[str, Any], config: SupportGateConfig, case: LoadCase) -> LoadCaseResult:
    vehicle = from_functional_mapping(architecture_raw)
    properties = functional_mass_properties(vehicle)
    contacts = _contact_points(vehicle)
    if len(contacts) != 3:
        raise PlanarSupportGateError("v1 support load solver requires exactly three contacts")
    centre = properties["centre_of_mass_m"]
    relative = tuple((item.x_m - centre[0], item.y_m - centre[1]) for item in contacts)
    mass, height = properties["mass_kg"], centre[2]
    matrix = (
        (1.0, 1.0, 1.0),
        tuple(point[0] for point in relative),
        tuple(point[1] for point in relative),
    )
    target = (
        mass * config.gravity_m_per_s2,
        -mass * case.longitudinal_acceleration_m_per_s2 * height,
        -mass * case.lateral_acceleration_m_per_s2 * height,
    )
    loads = _solve_three(matrix, target)
    vertical = math.fsum(loads) - target[0]
    pitch = math.fsum(point[0] * load for point, load in zip(relative, loads)) - target[1]
    roll = math.fsum(point[1] * load for point, load in zip(relative, loads)) - target[2]
    minimum = min(loads)
    utilization = max(load / contact.maximum_normal_force_n for load, contact in zip(loads, contacts))
    if minimum <= 0.0:
        status = "contact_lift"
    elif utilization > 1.0:
        status = "normal_limit_exceeded"
    else:
        status = "passed"
    scale = max(target[0], 1.0)
    moment_scale = max(target[0] * max(1.0, *(abs(value) for point in relative for value in point)), 1.0)
    if abs(vertical) > config.equilibrium_relative_tolerance * scale or abs(pitch) > config.equilibrium_relative_tolerance * moment_scale or abs(roll) > config.equilibrium_relative_tolerance * moment_scale:
        raise PlanarSupportGateError("support equilibrium residual exceeds tolerance")
    return LoadCaseResult(
        case.case_id, status, tuple((contact.contact_id, load) for contact, load in zip(contacts, loads)),
        minimum, utilization, vertical, pitch, roll,
    )


def _static_loads(architecture_raw: Mapping[str, Any], config: SupportGateConfig) -> tuple[tuple[str, float], ...]:
    case = LoadCase("static_internal", 0.0, 0.0, "passed")
    result = solve_support_load_case(architecture_raw, config, case)
    if result.status != "passed":
        raise PlanarSupportGateError("static support load case did not pass")
    return result.normal_loads_n


def _planar_vehicle(architecture_raw: Mapping[str, Any], config: SupportGateConfig, steer_angle_rad: float) -> PlanarVehicle:
    vehicle = from_functional_mapping(architecture_raw)
    properties = functional_mass_properties(vehicle)
    contacts = _contact_points(vehicle)
    components = {item.component_id: item for item in vehicle.components}
    static = dict(_static_loads(architecture_raw, config))
    centre = properties["centre_of_mass_m"]
    planar_contacts: list[PlanarContact] = []
    for contact in contacts:
        powered = "ground_propulsion" in components[contact.component_id].function_tags
        planar_contacts.append(PlanarContact(
            contact.contact_id,
            contact.x_m - centre[0],
            contact.y_m - centre[1],
            static[contact.contact_id],
            steer_angle_rad if powered else 0.0,
            config.front_cornering_stiffness_n_per_rad if powered else config.rear_cornering_stiffness_n_per_rad,
            config.front_requested_longitudinal_force_n if powered else 0.0,
            TyreContactParameters(config.friction_coefficient_longitudinal, config.friction_coefficient_lateral),
        ))
    return PlanarVehicle(
        vehicle.candidate_id,
        PlanarVehicleParameters(properties["mass_kg"], properties["inertia_kg_m2"][2], centre[2], config.gravity_m_per_s2),
        tuple(planar_contacts),
    )


def run_planar_steering(architecture_raw: Mapping[str, Any], config: SupportGateConfig, *, steer_angle_rad: float, time_step_s: float | None = None) -> PlanarRunResult:
    steer = _finite("steer_angle_rad", steer_angle_rad)
    if abs(steer) > config.maximum_steer_angle_rad:
        raise PlanarSupportGateError("steering command exceeds protocol limit")
    dt = config.time_step_s if time_step_s is None else _positive("time_step_s", time_step_s)
    count_value = config.duration_s / dt
    count = round(count_value)
    if not math.isclose(count_value, count, rel_tol=0.0, abs_tol=1.0e-10):
        raise PlanarSupportGateError("duration must be an integer multiple of steering step")
    vehicle = _planar_vehicle(architecture_raw, config, steer)
    architecture = from_functional_mapping(architecture_raw)
    direction_components = tuple(
        item for item in architecture.components if "direction_control" in item.function_tags
    )
    if len(direction_components) != 1:
        raise PlanarSupportGateError("architecture must declare exactly one direction-control component")
    architecture_steer_limit = direction_components[0].parameters["maximum_angle_rad"]
    if config.maximum_steer_angle_rad > architecture_steer_limit:
        raise PlanarSupportGateError("protocol steering limit exceeds architecture limit")
    if abs(steer) > architecture_steer_limit:
        raise PlanarSupportGateError("steering command exceeds architecture limit")
    contact_limits = {item.contact_id: item for item in _contact_points(architecture)}
    state = PlanarState(0.0, 0.0, 0.0, 0.0, config.initial_longitudinal_speed_m_per_s, 0.0, 0.0)
    max_utilization = max_residual = 0.0
    minimum_load = math.inf
    status, reason, executed = "passed", "completed", 0
    for _ in range(count):
        result = step_planar_dynamics(vehicle=vehicle, state=state, control=PlanarSolverControl(time_step_s=dt))
        executed += 1
        if result.status != "ok":
            status, reason = "failed", result.reason
            break
        state = result.end_state
        minimum_load = min(minimum_load, *result.normal_loads_n)
        max_utilization = max(max_utilization, *(item.tyre_force.applied_utilization or 0.0 for item in result.contact_results))
        if result.residuals is not None:
            max_residual = max(max_residual, *(abs(value) for value in asdict(result.residuals).values()))
        for item in result.contact_results:
            limit = contact_limits[item.contact_id]
            force_tolerance = config.equilibrium_relative_tolerance * max(
                limit.maximum_longitudinal_force_n,
                limit.maximum_lateral_force_n,
                1.0,
            )
            if (
                abs(item.tyre_force.applied_longitudinal_force_n) > limit.maximum_longitudinal_force_n + force_tolerance
                or abs(item.tyre_force.applied_lateral_force_n) > limit.maximum_lateral_force_n + force_tolerance
            ):
                status, reason = "failed", "architecture contact force limit exceeded"
                break
        if status != "passed":
            break
    body = {
        "steer_angle_rad": steer,
        "status": status,
        "reason": reason,
        "requested_steps": count,
        "executed_steps": executed,
        "final_state": asdict(state),
        "maximum_contact_utilization": max_utilization,
        "minimum_normal_load_n": minimum_load,
        "maximum_abs_balance_residual": max_residual,
    }
    identity = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    return PlanarRunResult(steer, status, reason, count, executed, state, max_utilization, minimum_load, max_residual, identity)


def mapping(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {name: mapping(getattr(value, name)) for name in value.__dataclass_fields__}
    if isinstance(value, tuple):
        return [mapping(item) for item in value]
    if isinstance(value, dict):
        return {str(key): mapping(item) for key, item in value.items()}
    return value
