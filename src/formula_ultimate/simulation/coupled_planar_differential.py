"""Work 071 coupled planar, differential, and per-step load-transfer gate."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
import math
from typing import Any, Mapping

from formula_ultimate.physics.lateral import (
    PlanarContact,
    PlanarState,
    PlanarVehicle,
    PlanarVehicleParameters,
    solve_quasi_static_normal_loads,
)
from formula_ultimate.physics.tyre import (
    TyreContactParameters,
    TyreForceRequest,
    TyreForceResult,
    resolve_tyre_force,
)
from formula_ultimate.topology.functional_vehicle import (
    from_functional_mapping,
    functional_mass_properties,
    validate_functional_vehicle,
)

from .differential_drive_coupling import (
    DifferentialBranchConfig,
    DifferentialDriveConfig,
    with_branch_friction,
)
from .drive_ground_coupling import GroundUnitConfig, ground_force_request
from .planar_support_gate import SupportGateConfig, solve_support_load_case
from .powertrain_dynamics import (
    PowertrainConfig,
    PowertrainState,
    StepEvidence as PowertrainStepEvidence,
    initial_powertrain_state,
    step_powertrain,
    total_accounted_energy_j as total_powertrain_accounted_energy_j,
)


MODEL_VERSION = "coupled_planar_differential_load_transfer_v1"


class CoupledPlanarDifferentialError(ValueError):
    """Raised when Work 071 declarations or runtime evidence are invalid."""


def _finite(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CoupledPlanarDifferentialError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise CoupledPlanarDifferentialError(f"{name} must be finite")
    return result


def _positive(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result <= 0.0:
        raise CoupledPlanarDifferentialError(f"{name} must be positive")
    return result


def _nonnegative(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result < 0.0:
        raise CoupledPlanarDifferentialError(f"{name} must be non-negative")
    return result


def _section(raw: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    value = raw.get(name)
    if not isinstance(value, Mapping):
        raise CoupledPlanarDifferentialError(f"missing section {name}")
    return value


def _close(name: str, actual: float, expected: float, tolerance: float) -> None:
    scale = max(abs(actual), abs(expected), 1.0)
    if abs(actual - expected) > tolerance * scale:
        raise CoupledPlanarDifferentialError(f"{name} mismatch: {actual!r} versus {expected!r}")


@dataclass(frozen=True, slots=True)
class CoupledContactConfig:
    contact_id: str
    component_id: str
    x_position_m: float
    y_position_m: float
    baseline_normal_load_n: float
    powered: bool
    cornering_stiffness_n_per_rad: float
    longitudinal_friction_coefficient: float
    lateral_friction_coefficient: float
    maximum_normal_force_n: float
    maximum_longitudinal_force_n: float
    maximum_lateral_force_n: float


@dataclass(frozen=True, slots=True)
class CoupledPlanarDifferentialConfig:
    protocol_id: str
    differential: DifferentialDriveConfig
    contacts: tuple[CoupledContactConfig, ...]
    vehicle_mass_kg: float
    yaw_inertia_kg_m2: float
    centre_of_mass_height_m: float
    gravity_m_per_s2: float
    initial_longitudinal_speed_m_per_s: float
    steer_angle_rad: float
    maximum_steer_angle_rad: float
    throttle: float
    duration_s: float
    time_step_s: float
    lateral_speed_regularization_m_per_s: float
    maximum_load_iterations: int
    acceleration_absolute_tolerance_m_per_s2: float
    acceleration_relative_tolerance: float
    relaxation_factor: float
    geometry_relative_tolerance: float
    balance_relative_tolerance: float
    interface_energy_relative_tolerance: float
    body_energy_relative_tolerance: float
    global_energy_relative_tolerance: float
    mirror_relative_tolerance: float
    refinement_relative_tolerance: float


@dataclass(frozen=True, slots=True)
class CoupledPlanarDifferentialState:
    powertrain: PowertrainState
    differential_angle_rad: float
    differential_speed_rad_s: float
    planar: PlanarState
    longitudinal_acceleration_m_per_s2: float
    lateral_acceleration_m_per_s2: float
    longitudinal_slip_heat_j: float
    lateral_slip_heat_j: float
    branch_connection_heat_j: float
    differential_heat_j: float
    aerodynamic_work_j: float
    rolling_work_j: float
    contact_body_work_j: float
    outcome: str
    drive_subsystem_state: str
    dnf_reason: str | None
    dnf_time_s: float | None


@dataclass(frozen=True, slots=True)
class CoupledContactEvidence:
    contact_id: str
    component_id: str
    powered: bool
    normal_load_n: float
    steer_angle_rad: float
    local_longitudinal_velocity_m_per_s: float
    local_lateral_velocity_m_per_s: float
    slip_angle_rad: float
    longitudinal_slip_ratio: float
    requested_longitudinal_force_n: float
    requested_lateral_force_n: float
    applied_longitudinal_force_n: float
    applied_lateral_force_n: float
    applied_body_longitudinal_force_n: float
    applied_body_lateral_force_n: float
    yaw_moment_nm: float
    combined_utilization: float
    saturated: bool
    wheel_speed_rad_s: float | None
    reflected_load_torque_nm: float
    longitudinal_slip_heat_j: float
    lateral_slip_heat_j: float
    body_work_j: float


@dataclass(frozen=True, slots=True)
class CoupledStepEvidence:
    status: str
    reason: str
    time_s: float
    load_iterations: int
    normal_loads_n: tuple[tuple[str, float], ...]
    contacts: tuple[CoupledContactEvidence, ...]
    powertrain: PowertrainStepEvidence | None
    total_body_longitudinal_force_n: float
    total_body_lateral_force_n: float
    total_yaw_moment_nm: float
    longitudinal_acceleration_m_per_s2: float
    lateral_acceleration_m_per_s2: float
    yaw_acceleration_rad_per_s2: float
    carrier_average_residual_rad_s: float
    modal_equation_residual_nm: float
    torque_residual_nm: float
    load_balance_maximum_abs_residual: float
    differential_interface_energy_residual_j: float
    contact_energy_residual_j: float
    body_energy_residual_j: float
    global_energy_residual_j: float
    global_relative_energy_residual: float
    minimum_normal_load_n: float
    maximum_contact_utilization: float
    outcome: str
    dnf_reason: str | None


@dataclass(frozen=True, slots=True)
class CoupledRunResult:
    model_version: str
    protocol_id: str
    status: str
    outcome: str
    terminal_reason: str
    requested_steps: int
    executed_steps: int
    initial_powertrain_energy_j: float
    initial_total_energy_j: float
    final_state: CoupledPlanarDifferentialState
    final_branch_speeds_rad_s: tuple[tuple[str, float], ...]
    minimum_normal_load_n: float
    maximum_contact_utilization: float
    maximum_abs_differential_speed_rad_s: float
    maximum_modal_energy_j: float
    maximum_abs_load_balance_residual: float
    maximum_abs_carrier_average_residual_rad_s: float
    maximum_abs_modal_equation_residual_nm: float
    maximum_abs_torque_residual_nm: float
    maximum_abs_differential_interface_energy_residual_j: float
    maximum_abs_contact_energy_residual_j: float
    maximum_abs_body_energy_residual_j: float
    maximum_abs_global_energy_residual_j: float
    maximum_global_relative_energy_residual: float
    saturated_step_count: int
    trace: tuple[CoupledStepEvidence, ...]
    result_sha256: str


@dataclass(frozen=True, slots=True)
class _ResolvedContact:
    config: CoupledContactConfig
    normal_load_n: float
    steer_angle_rad: float
    local_vx_m_per_s: float
    local_vy_m_per_s: float
    slip_angle_rad: float
    longitudinal_slip_ratio: float
    tyre: TyreForceResult
    applied_local_fx_n: float
    applied_local_fy_n: float
    body_fx_n: float
    body_fy_n: float
    yaw_moment_nm: float
    wheel_speed_rad_s: float | None
    reflected_load_torque_nm: float


def load_coupled_planar_config(
    raw: Mapping[str, Any],
    *,
    differential: DifferentialDriveConfig,
    architecture_raw: Mapping[str, Any],
    support_config: SupportGateConfig,
) -> CoupledPlanarDifferentialConfig:
    if raw.get("model_version") != MODEL_VERSION:
        raise CoupledPlanarDifferentialError("coupled planar model version mismatch")
    planar = _section(raw, "planar")
    solver = _section(raw, "solver")
    numerical = _section(raw, "numerical")
    maximum_iterations = solver.get("maximum_load_iterations")
    if isinstance(maximum_iterations, bool) or not isinstance(maximum_iterations, int) or not 1 <= maximum_iterations <= 10_000:
        raise CoupledPlanarDifferentialError("maximum_load_iterations must be an integer in [1, 10000]")
    config_values = {
        "geometry": _positive("geometry_relative_tolerance", numerical.get("geometry_relative_tolerance")),
        "balance": _positive("balance_relative_tolerance", numerical.get("balance_relative_tolerance")),
        "interface": _positive("interface_energy_relative_tolerance", numerical.get("interface_energy_relative_tolerance")),
        "body": _positive("body_energy_relative_tolerance", numerical.get("body_energy_relative_tolerance")),
        "global": _positive("global_energy_relative_tolerance", numerical.get("global_energy_relative_tolerance")),
        "mirror": _positive("mirror_relative_tolerance", numerical.get("mirror_relative_tolerance")),
        "refinement": _positive("refinement_relative_tolerance", numerical.get("refinement_relative_tolerance")),
    }
    if config_values["geometry"] > 1.0e-9 or config_values["balance"] > 1.0e-9:
        raise CoupledPlanarDifferentialError("geometry or balance tolerance exceeds protocol ceiling")
    if max(config_values["interface"], config_values["body"], config_values["global"]) > 1.0e-3:
        raise CoupledPlanarDifferentialError("energy tolerance exceeds protocol ceiling")
    if config_values["mirror"] > 1.0e-6 or config_values["refinement"] > 0.02:
        raise CoupledPlanarDifferentialError("mirror or refinement tolerance exceeds protocol ceiling")

    vehicle = from_functional_mapping(architecture_raw)
    validate_functional_vehicle(vehicle)
    properties = functional_mass_properties(vehicle)
    static_case = next((item for item in support_config.load_cases if item.case_id == "static"), None)
    if static_case is None:
        raise CoupledPlanarDifferentialError("support protocol has no static case")
    static_result = solve_support_load_case(architecture_raw, support_config, static_case)
    if static_result.status != "passed":
        raise CoupledPlanarDifferentialError("static support solution did not pass")
    static_loads = dict(static_result.normal_loads_n)
    components = {item.component_id: item for item in vehicle.components}
    branch_by_component = {item.component_id: item for item in differential.branches}
    contact_configs: list[CoupledContactConfig] = []
    front_cornering = _positive("front_cornering_stiffness", planar.get("front_cornering_stiffness_n_per_rad"))
    rear_cornering = _positive("rear_cornering_stiffness", planar.get("rear_cornering_stiffness_n_per_rad"))
    lateral_mu = _positive("lateral_friction_coefficient", planar.get("lateral_friction_coefficient"))
    for ground in vehicle.ground_contacts:
        component = components[ground.component_id]
        port = next(item for item in component.ports if item.port_id == ground.port_id)
        world = tuple(component.position_m[index] + port.local_position_m[index] for index in range(3))
        centre = properties["centre_of_mass_m"]
        powered = component.component_id in branch_by_component
        longitudinal_mu = branch_by_component[component.component_id].friction_coefficient if powered else 1.0
        contact_configs.append(CoupledContactConfig(
            ground.contact_id, component.component_id,
            world[0] - centre[0], world[1] - centre[1], static_loads[ground.contact_id], powered,
            front_cornering if powered else rear_cornering,
            longitudinal_mu, lateral_mu,
            ground.maximum_normal_force_n, ground.maximum_longitudinal_force_n, ground.maximum_lateral_force_n,
        ))
    contact_configs.sort(key=lambda item: item.contact_id)
    powered_contacts = {item.component_id for item in contact_configs if item.powered}
    if powered_contacts != set(branch_by_component):
        raise CoupledPlanarDifferentialError("powered planar contacts differ from differential branches")
    steer = _finite("steer_angle_rad", planar.get("steer_angle_rad"))
    maximum_steer = _positive("maximum_steer_angle_rad", planar.get("maximum_steer_angle_rad"))
    if abs(steer) > maximum_steer:
        raise CoupledPlanarDifferentialError("steering command exceeds protocol limit")
    direction = tuple(item for item in vehicle.components if "direction_control" in item.function_tags)
    if len(direction) != 1 or maximum_steer > direction[0].parameters["maximum_angle_rad"]:
        raise CoupledPlanarDifferentialError("protocol steering limit exceeds architecture direction actuator")
    mass = properties["mass_kg"]
    _close("differential vehicle mass", differential.vehicle_mass_kg, mass, config_values["geometry"])
    result = CoupledPlanarDifferentialConfig(
        str(raw.get("protocol_id", "")), differential, tuple(contact_configs), mass,
        properties["inertia_kg_m2"][2], properties["centre_of_mass_m"][2], differential.gravity_m_per_s2,
        _positive("initial_longitudinal_speed", planar.get("initial_longitudinal_speed_m_per_s")),
        steer, maximum_steer, _nonnegative("throttle", planar.get("throttle")),
        _positive("duration_s", planar.get("duration_s")), _positive("time_step_s", planar.get("time_step_s")),
        _positive("lateral_speed_regularization", planar.get("lateral_speed_regularization_m_per_s")),
        maximum_iterations,
        _positive("acceleration_absolute_tolerance", solver.get("acceleration_absolute_tolerance_m_per_s2")),
        _nonnegative("acceleration_relative_tolerance", solver.get("acceleration_relative_tolerance")),
        _positive("relaxation_factor", solver.get("relaxation_factor")),
        config_values["geometry"], config_values["balance"], config_values["interface"], config_values["body"],
        config_values["global"], config_values["mirror"], config_values["refinement"],
    )
    if not result.protocol_id or result.throttle > 1.0 or result.relaxation_factor > 1.0:
        raise CoupledPlanarDifferentialError("protocol identity, throttle, or relaxation is invalid")
    count = result.duration_s / result.time_step_s
    if not math.isclose(count, round(count), rel_tol=0.0, abs_tol=1.0e-10):
        raise CoupledPlanarDifferentialError("duration must be an integer multiple of time step")
    _planar_vehicle(result)
    return result


def with_steer(config: CoupledPlanarDifferentialConfig, steer_angle_rad: float) -> CoupledPlanarDifferentialConfig:
    steer = _finite("steer_angle_rad", steer_angle_rad)
    if abs(steer) > config.maximum_steer_angle_rad:
        raise CoupledPlanarDifferentialError("steering command exceeds protocol limit")
    return replace(config, steer_angle_rad=steer)


def with_coupled_branch_friction(
    config: CoupledPlanarDifferentialConfig, *, left: float, right: float,
) -> CoupledPlanarDifferentialConfig:
    differential = with_branch_friction(config.differential, left=left, right=right)
    values = {item.component_id: item.friction_coefficient for item in differential.branches}
    contacts = tuple(
        replace(item, longitudinal_friction_coefficient=values[item.component_id]) if item.powered else item
        for item in config.contacts
    )
    return replace(config, differential=differential, contacts=contacts)


def _planar_vehicle(config: CoupledPlanarDifferentialConfig) -> PlanarVehicle:
    contacts = tuple(PlanarContact(
        item.contact_id, item.x_position_m, item.y_position_m, item.baseline_normal_load_n,
        config.steer_angle_rad if item.powered else 0.0,
        item.cornering_stiffness_n_per_rad, 0.0,
        TyreContactParameters(item.longitudinal_friction_coefficient, item.lateral_friction_coefficient),
    ) for item in config.contacts)
    return PlanarVehicle(
        config.differential.architecture_candidate_id,
        PlanarVehicleParameters(
            config.vehicle_mass_kg, config.yaw_inertia_kg_m2,
            config.centre_of_mass_height_m, config.gravity_m_per_s2,
        ),
        contacts,
    )


def initial_coupled_state(
    config: CoupledPlanarDifferentialConfig,
    powertrain: PowertrainConfig,
) -> CoupledPlanarDifferentialState:
    radii = tuple(item.effective_radius_m for item in config.differential.branches)
    if not math.isclose(radii[0], radii[1], rel_tol=config.geometry_relative_tolerance, abs_tol=0.0):
        raise CoupledPlanarDifferentialError("v1 matched-speed initialization requires equal driven radii")
    carrier_speed = config.initial_longitudinal_speed_m_per_s / radii[0]
    converter_speed = powertrain.transmission_ratio * carrier_speed
    initial_kinetic_energy = (
        0.5 * config.vehicle_mass_kg * config.initial_longitudinal_speed_m_per_s ** 2
        + 0.5 * powertrain.converter_inertia_kg_m2 * converter_speed ** 2
        + 0.5 * powertrain.output_inertia_kg_m2 * carrier_speed ** 2
    )
    remaining_storage_energy = powertrain.initial_storage_energy_j - initial_kinetic_energy
    if remaining_storage_energy < 0.0:
        raise CoupledPlanarDifferentialError(
            "initial storage energy cannot fund the requested body and rotating kinetic energy"
        )
    base = initial_powertrain_state(powertrain, storage_energy_j=remaining_storage_energy)
    powertrain_state = replace(
        base,
        converter_speed_rad_s=converter_speed,
        output_speed_rad_s=carrier_speed,
    )
    planar = PlanarState(0.0, 0.0, 0.0, 0.0, config.initial_longitudinal_speed_m_per_s, 0.0, 0.0)
    return CoupledPlanarDifferentialState(
        powertrain_state, 0.0, 0.0, planar, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        "running", "operational", None, None,
    )


def branch_speeds(state: CoupledPlanarDifferentialState) -> tuple[float, float]:
    carrier = state.powertrain.output_speed_rad_s
    return carrier - state.differential_speed_rad_s, carrier + state.differential_speed_rad_s


def modal_energy_j(config: CoupledPlanarDifferentialConfig, state: CoupledPlanarDifferentialState) -> float:
    return 0.5 * config.differential.modal_inertia_kg_m2 * state.differential_speed_rad_s ** 2


def body_kinetic_energy_j(config: CoupledPlanarDifferentialConfig, state: CoupledPlanarDifferentialState) -> float:
    planar = state.planar
    return (
        0.5 * config.vehicle_mass_kg * (planar.longitudinal_velocity_m_per_s ** 2 + planar.lateral_velocity_m_per_s ** 2)
        + 0.5 * config.yaw_inertia_kg_m2 * planar.yaw_rate_rad_per_s ** 2
    )


def total_accounted_energy_j(
    config: CoupledPlanarDifferentialConfig,
    powertrain: PowertrainConfig,
    state: CoupledPlanarDifferentialState,
) -> float:
    return (
        total_powertrain_accounted_energy_j(powertrain, state.powertrain)
        - state.powertrain.useful_work_j
        + modal_energy_j(config, state)
        + body_kinetic_energy_j(config, state)
        + state.longitudinal_slip_heat_j + state.lateral_slip_heat_j
        + state.branch_connection_heat_j + state.differential_heat_j
        + state.aerodynamic_work_j + state.rolling_work_j
    )


def _local_velocity(planar: PlanarState, contact: CoupledContactConfig, steer: float) -> tuple[float, float]:
    body_vx = planar.longitudinal_velocity_m_per_s - planar.yaw_rate_rad_per_s * contact.y_position_m
    body_vy = planar.lateral_velocity_m_per_s + planar.yaw_rate_rad_per_s * contact.x_position_m
    cosine, sine = math.cos(steer), math.sin(steer)
    return cosine * body_vx + sine * body_vy, -sine * body_vx + cosine * body_vy


def _branch_for_component(config: CoupledPlanarDifferentialConfig, component_id: str) -> DifferentialBranchConfig:
    return next(item for item in config.differential.branches if item.component_id == component_id)


def _resolve_iteration(
    config: CoupledPlanarDifferentialConfig,
    powertrain: PowertrainConfig,
    state: CoupledPlanarDifferentialState,
    normal_loads: tuple[float, ...],
    initial_powertrain_energy_j: float,
    dt: float,
) -> tuple[tuple[_ResolvedContact, ...], PowertrainState, PowertrainStepEvidence, float, float, float, float, float, float]:
    old_wheels = dict(zip((item.component_id for item in config.differential.branches), branch_speeds(state)))
    preliminary: list[tuple[CoupledContactConfig, float, float, float, float, TyreForceResult, float | None]] = []
    reflected_requests: list[float] = []
    for contact, normal_load in zip(config.contacts, normal_loads):
        steer = config.steer_angle_rad if contact.powered else 0.0
        local_vx, local_vy = _local_velocity(state.planar, contact, steer)
        slip_angle = math.atan2(local_vy, max(abs(local_vx), config.lateral_speed_regularization_m_per_s))
        requested_lateral = -contact.cornering_stiffness_n_per_rad * slip_angle
        wheel_speed: float | None = None
        slip_ratio = 0.0
        requested_longitudinal = 0.0
        if contact.powered:
            branch = _branch_for_component(config, contact.component_id)
            wheel_speed = old_wheels[contact.component_id]
            unit = GroundUnitConfig(
                branch.contact_id, branch.component_id, branch.effective_radius_m,
                branch.rotational_inertia_kg_m2, normal_load,
                branch.friction_coefficient, branch.longitudinal_stiffness_n_per_slip,
                branch.maximum_longitudinal_force_n,
            )
            request = ground_force_request(
                unit, wheel_speed_rad_per_s=wheel_speed,
                vehicle_speed_m_per_s=max(local_vx, 0.0),
                regularization_speed_m_per_s=config.differential.slip_regularization_speed_m_per_s,
            )
            slip_ratio = request["slip_ratio"]
            requested_longitudinal = request["requested_force_n"]
        tyre = resolve_tyre_force(
            parameters=TyreContactParameters(contact.longitudinal_friction_coefficient, contact.lateral_friction_coefficient),
            normal_load_n=normal_load,
            request=TyreForceRequest(requested_longitudinal, requested_lateral),
        )
        if abs(tyre.applied_longitudinal_force_n) > contact.maximum_longitudinal_force_n or abs(tyre.applied_lateral_force_n) > contact.maximum_lateral_force_n:
            raise CoupledPlanarDifferentialError("combined tyre force exceeds architecture contact limit")
        preliminary.append((contact, steer, local_vx, local_vy, slip_angle, tyre, wheel_speed))
        if contact.powered:
            branch = _branch_for_component(config, contact.component_id)
            reflected_requests.append(tyre.applied_longitudinal_force_n * branch.effective_radius_m / branch.connection_efficiency)
    requested_carrier_torque = math.fsum(reflected_requests)
    new_powertrain, powertrain_evidence = step_powertrain(
        powertrain, state.powertrain, throttle=config.throttle,
        requested_load_torque_nm=requested_carrier_torque, step_s=dt,
        initial_energy_j=initial_powertrain_energy_j,
    )
    applied_carrier_torque = powertrain_evidence.applied_load_torque_nm
    scale = 0.0 if requested_carrier_torque == 0.0 else applied_carrier_torque / requested_carrier_torque
    if scale < -config.interface_energy_relative_tolerance or scale > 1.0 + config.interface_energy_relative_tolerance:
        raise CoupledPlanarDifferentialError("powertrain returned invalid longitudinal-force scale")
    scale = min(1.0, max(0.0, scale))
    resolved: list[_ResolvedContact] = []
    for contact, steer, local_vx, local_vy, slip_angle, tyre, wheel_speed in preliminary:
        local_fx = tyre.applied_longitudinal_force_n * scale if contact.powered else 0.0
        local_fy = tyre.applied_lateral_force_n
        cosine, sine = math.cos(steer), math.sin(steer)
        body_fx = cosine * local_fx - sine * local_fy
        body_fy = sine * local_fx + cosine * local_fy
        yaw = contact.x_position_m * body_fy - contact.y_position_m * body_fx
        reflected = 0.0
        if contact.powered:
            branch = _branch_for_component(config, contact.component_id)
            reflected = local_fx * branch.effective_radius_m / branch.connection_efficiency
        resolved.append(_ResolvedContact(
            contact, tyre.normal_load_n, steer, local_vx, local_vy, slip_angle,
            0.0 if wheel_speed is None else (
                branch.effective_radius_m * wheel_speed - max(local_vx, 0.0)
            ) / max(max(local_vx, 0.0), config.differential.slip_regularization_speed_m_per_s),
            tyre, local_fx, local_fy, body_fx, body_fy, yaw, wheel_speed, reflected,
        ))
    tyre_fx = math.fsum(item.body_fx_n for item in resolved)
    tyre_fy = math.fsum(item.body_fy_n for item in resolved)
    yaw_moment = math.fsum(item.yaw_moment_nm for item in resolved)
    speed = max(state.planar.longitudinal_velocity_m_per_s, 0.0)
    drag = 0.5 * config.differential.air_density_kg_per_m3 * config.differential.drag_area_m2 * speed ** 2
    rolling_capacity = config.differential.rolling_resistance_coefficient * config.vehicle_mass_kg * config.gravity_m_per_s2
    rolling = rolling_capacity if speed > 0.0 else min(rolling_capacity, max(tyre_fx, 0.0))
    total_fx = tyre_fx - drag - rolling
    return tuple(resolved), new_powertrain, powertrain_evidence, total_fx, tyre_fy, yaw_moment, drag, rolling, applied_carrier_torque


def _terminal_contact_step(
    config: CoupledPlanarDifferentialConfig,
    state: CoupledPlanarDifferentialState,
    reason: str,
    normal_loads: tuple[float, ...],
    iterations: int,
) -> tuple[CoupledPlanarDifferentialState, CoupledStepEvidence]:
    failure = "contact_lift" if "contact lift" in reason else "load_transfer_invalid"
    terminal = replace(
        state, outcome="DNF", drive_subsystem_state="failed", dnf_reason=failure,
        dnf_time_s=state.planar.time_s,
    )
    evidence = CoupledStepEvidence(
        status="physical_failure",
        reason=reason,
        time_s=state.planar.time_s,
        load_iterations=iterations,
        normal_loads_n=tuple((item.contact_id, value) for item, value in zip(config.contacts, normal_loads)),
        contacts=(),
        powertrain=None,
        total_body_longitudinal_force_n=0.0,
        total_body_lateral_force_n=0.0,
        total_yaw_moment_nm=0.0,
        longitudinal_acceleration_m_per_s2=state.longitudinal_acceleration_m_per_s2,
        lateral_acceleration_m_per_s2=state.lateral_acceleration_m_per_s2,
        yaw_acceleration_rad_per_s2=0.0,
        carrier_average_residual_rad_s=0.0,
        modal_equation_residual_nm=0.0,
        torque_residual_nm=0.0,
        load_balance_maximum_abs_residual=0.0,
        differential_interface_energy_residual_j=0.0,
        contact_energy_residual_j=0.0,
        body_energy_residual_j=0.0,
        global_energy_residual_j=0.0,
        global_relative_energy_residual=0.0,
        minimum_normal_load_n=min(normal_loads) if normal_loads else math.inf,
        maximum_contact_utilization=0.0,
        outcome="DNF",
        dnf_reason=failure,
    )
    return terminal, evidence


def step_coupled_planar_differential(
    config: CoupledPlanarDifferentialConfig,
    powertrain: PowertrainConfig,
    state: CoupledPlanarDifferentialState,
    *,
    initial_powertrain_energy_j: float,
    initial_total_energy_j: float,
    time_step_s: float | None = None,
) -> tuple[CoupledPlanarDifferentialState, CoupledStepEvidence]:
    if state.outcome != "running":
        raise CoupledPlanarDifferentialError("DNF state cannot execute another coupled step")
    dt = config.time_step_s if time_step_s is None else _positive("time_step_s", time_step_s)
    vehicle = _planar_vehicle(config)
    guess_ax, guess_ay = state.longitudinal_acceleration_m_per_s2, state.lateral_acceleration_m_per_s2
    final = None
    normal_loads: tuple[float, ...] = ()
    load_residual = 0.0
    for iteration in range(1, config.maximum_load_iterations + 1):
        load_solution = solve_quasi_static_normal_loads(
            vehicle=vehicle,
            longitudinal_acceleration_m_per_s2=guess_ax,
            lateral_acceleration_m_per_s2=guess_ay,
        )
        normal_loads = load_solution.normal_loads_n
        if load_solution.status != "ok":
            return _terminal_contact_step(config, state, load_solution.reason, normal_loads, iteration)
        final = _resolve_iteration(config, powertrain, state, normal_loads, initial_powertrain_energy_j, dt)
        resolved, _, _, total_fx, total_fy, _, _, _, _ = final
        new_ax, new_ay = total_fx / config.vehicle_mass_kg, total_fy / config.vehicle_mass_kg
        tolerance_x = config.acceleration_absolute_tolerance_m_per_s2 + config.acceleration_relative_tolerance * max(abs(guess_ax), abs(new_ax))
        tolerance_y = config.acceleration_absolute_tolerance_m_per_s2 + config.acceleration_relative_tolerance * max(abs(guess_ay), abs(new_ay))
        if abs(new_ax - guess_ax) <= tolerance_x and abs(new_ay - guess_ay) <= tolerance_y:
            residuals = load_solution.residuals
            if residuals is None:
                raise CoupledPlanarDifferentialError("normal-load residual evidence is missing")
            load_residual = max(abs(residuals.vertical_force_n), abs(residuals.pitch_moment_n_m), abs(residuals.roll_moment_n_m))
            break
        guess_ax += config.relaxation_factor * (new_ax - guess_ax)
        guess_ay += config.relaxation_factor * (new_ay - guess_ay)
    else:
        raise CoupledPlanarDifferentialError("coupled load-transfer fixed point did not converge")
    assert final is not None
    resolved, new_powertrain, powertrain_evidence, total_fx, total_fy, yaw_moment, drag, rolling, applied_carrier_torque = final
    new_ax, new_ay = total_fx / config.vehicle_mass_kg, total_fy / config.vehicle_mass_kg
    yaw_acceleration = yaw_moment / config.yaw_inertia_kg_m2
    old_planar = state.planar
    new_yaw_rate = old_planar.yaw_rate_rad_per_s + yaw_acceleration * dt
    mean_yaw_rate = 0.5 * (old_planar.yaw_rate_rad_per_s + new_yaw_rate)
    coupling = 0.5 * dt * mean_yaw_rate
    right_u = (
        old_planar.longitudinal_velocity_m_per_s + new_ax * dt
        + coupling * old_planar.lateral_velocity_m_per_s
    )
    right_v = (
        old_planar.lateral_velocity_m_per_s + new_ay * dt
        - coupling * old_planar.longitudinal_velocity_m_per_s
    )
    determinant = 1.0 + coupling * coupling
    new_u = (right_u + coupling * right_v) / determinant
    new_v = (right_v - coupling * right_u) / determinant
    new_heading = old_planar.heading_rad + mean_yaw_rate * dt
    mean_u = 0.5 * (old_planar.longitudinal_velocity_m_per_s + new_u)
    mean_v = 0.5 * (old_planar.lateral_velocity_m_per_s + new_v)
    mean_heading = 0.5 * (old_planar.heading_rad + new_heading)
    cosine, sine = math.cos(mean_heading), math.sin(mean_heading)
    x_dot = cosine * mean_u - sine * mean_v
    y_dot = sine * mean_u + cosine * mean_v
    new_planar = PlanarState(
        old_planar.time_s + dt, old_planar.x_position_m + x_dot * dt, old_planar.y_position_m + y_dot * dt,
        new_heading, new_u, new_v, new_yaw_rate,
    )

    reflected = tuple(item.reflected_load_torque_nm for item in resolved if item.config.powered)
    modal_inertia = config.differential.modal_inertia_kg_m2
    old_delta = state.differential_speed_rad_s
    load_difference = reflected[0] - reflected[1]
    damping = config.differential.differential_damping_nm_per_rad_s
    new_delta = ((modal_inertia / dt - 0.5 * damping) * old_delta + load_difference) / (modal_inertia / dt + 0.5 * damping)
    mean_delta = 0.5 * (old_delta + new_delta)
    new_angle = state.differential_angle_rad + mean_delta * dt
    old_wheels = branch_speeds(state)
    new_wheels = (new_powertrain.output_speed_rad_s - new_delta, new_powertrain.output_speed_rad_s + new_delta)
    mean_wheels = tuple(0.5 * (old + new) for old, new in zip(old_wheels, new_wheels))
    mean_carrier = 0.5 * (state.powertrain.output_speed_rad_s + new_powertrain.output_speed_rad_s)
    modal_change = 0.5 * modal_inertia * (new_delta ** 2 - old_delta ** 2)
    differential_heat = damping * mean_delta ** 2 * dt

    mean_planar = replace(
        old_planar,
        longitudinal_velocity_m_per_s=0.5 * (old_planar.longitudinal_velocity_m_per_s + new_planar.longitudinal_velocity_m_per_s),
        lateral_velocity_m_per_s=0.5 * (old_planar.lateral_velocity_m_per_s + new_planar.lateral_velocity_m_per_s),
        yaw_rate_rad_per_s=0.5 * (old_planar.yaw_rate_rad_per_s + new_planar.yaw_rate_rad_per_s),
    )
    branch_index = {item.component_id: index for index, item in enumerate(config.differential.branches)}
    records: list[CoupledContactEvidence] = []
    longitudinal_heat = lateral_heat = connection_heat = contact_body_work = 0.0
    reflected_work = 0.0
    for item in resolved:
        mean_local_vx, mean_local_vy = _local_velocity(mean_planar, item.config, item.steer_angle_rad)
        wheel_input = 0.0
        branch_connection_heat = 0.0
        longitudinal_ground_work = item.applied_local_fx_n * mean_local_vx * dt
        if item.config.powered:
            index = branch_index[item.config.component_id]
            branch = config.differential.branches[index]
            reflected_branch_work = item.reflected_load_torque_nm * mean_wheels[index] * dt
            wheel_input = item.applied_local_fx_n * branch.effective_radius_m * mean_wheels[index] * dt
            branch_connection_heat = reflected_branch_work - wheel_input
            reflected_work += reflected_branch_work
        longitudinal_loss = wheel_input - longitudinal_ground_work
        lateral_loss = -item.applied_local_fy_n * mean_local_vy * dt
        scale = max(abs(wheel_input), abs(longitudinal_ground_work), abs(item.applied_local_fy_n * mean_local_vy * dt), 1.0)
        if longitudinal_loss < -config.interface_energy_relative_tolerance * scale or lateral_loss < -config.interface_energy_relative_tolerance * scale or branch_connection_heat < -config.interface_energy_relative_tolerance * scale:
            raise CoupledPlanarDifferentialError("negative contact or connection dissipation exceeds tolerance")
        longitudinal_loss, lateral_loss, branch_connection_heat = max(0.0, longitudinal_loss), max(0.0, lateral_loss), max(0.0, branch_connection_heat)
        body_work = (item.applied_local_fx_n * mean_local_vx + item.applied_local_fy_n * mean_local_vy) * dt
        longitudinal_heat += longitudinal_loss
        lateral_heat += lateral_loss
        connection_heat += branch_connection_heat
        contact_body_work += body_work
        utilization = math.hypot(
            item.applied_local_fx_n / max(item.tyre.longitudinal_limit_n, 1.0e-300),
            item.applied_local_fy_n / max(item.tyre.lateral_limit_n, 1.0e-300),
        )
        records.append(CoupledContactEvidence(
            item.config.contact_id, item.config.component_id, item.config.powered, item.normal_load_n,
            item.steer_angle_rad, item.local_vx_m_per_s, item.local_vy_m_per_s, item.slip_angle_rad,
            item.longitudinal_slip_ratio, item.tyre.requested_longitudinal_force_n, item.tyre.requested_lateral_force_n,
            item.applied_local_fx_n, item.applied_local_fy_n, item.body_fx_n, item.body_fy_n, item.yaw_moment_nm,
            utilization, item.tyre.saturated, item.wheel_speed_rad_s, item.reflected_load_torque_nm,
            longitudinal_loss, lateral_loss, body_work,
        ))

    carrier_input_work = new_powertrain.useful_work_j - state.powertrain.useful_work_j
    differential_interface_residual = carrier_input_work - reflected_work - modal_change - differential_heat
    contact_energy_residual = carrier_input_work - modal_change - differential_heat - connection_heat - contact_body_work - longitudinal_heat - lateral_heat
    mean_u = max(0.0, mean_planar.longitudinal_velocity_m_per_s)
    drag_work, rolling_work = drag * mean_u * dt, rolling * mean_u * dt
    old_body_energy = body_kinetic_energy_j(config, state)
    provisional_for_energy = replace(state, planar=new_planar)
    body_change = body_kinetic_energy_j(config, provisional_for_energy) - old_body_energy
    body_energy_residual = body_change - (contact_body_work - drag_work - rolling_work)

    carrier_average_residual = new_powertrain.output_speed_rad_s - 0.5 * math.fsum(new_wheels)
    modal_residual = modal_inertia * (new_delta - old_delta) / dt - (load_difference - damping * mean_delta)
    torque_residual = applied_carrier_torque - math.fsum(reflected)
    failure = new_powertrain.failure_code
    if failure is None and min(new_wheels) < -config.interface_energy_relative_tolerance:
        failure = "differential_branch_reverse_rotation"
    if failure is None and max(new_wheels) > config.differential.maximum_branch_speed_rad_s:
        failure = "differential_branch_overspeed"
    if failure is None and abs(new_delta) > config.differential.maximum_differential_speed_rad_s:
        failure = "differential_mode_overspeed"
    if failure is None and any(load > contact.maximum_normal_force_n for load, contact in zip(normal_loads, config.contacts)):
        failure = "contact_normal_force_limit"
    outcome = "DNF" if failure else "running"
    candidate = CoupledPlanarDifferentialState(
        new_powertrain, new_angle, new_delta, new_planar, new_ax, new_ay,
        state.longitudinal_slip_heat_j + longitudinal_heat,
        state.lateral_slip_heat_j + lateral_heat,
        state.branch_connection_heat_j + connection_heat,
        state.differential_heat_j + differential_heat,
        state.aerodynamic_work_j + drag_work, state.rolling_work_j + rolling_work,
        state.contact_body_work_j + contact_body_work,
        outcome, "failed" if failure else "operational", failure,
        new_powertrain.failure_time_s if new_powertrain.failure_code else (new_planar.time_s if failure else None),
    )
    global_residual = initial_total_energy_j - total_accounted_energy_j(config, powertrain, candidate)
    global_relative = abs(global_residual) / max(abs(initial_total_energy_j), 1.0)
    contact_scale = max(abs(carrier_input_work), abs(contact_body_work), longitudinal_heat + lateral_heat + connection_heat + abs(modal_change) + differential_heat, 1.0)
    body_scale = max(abs(body_change), abs(contact_body_work), drag_work + rolling_work, 1.0)
    if abs(differential_interface_residual) > config.interface_energy_relative_tolerance * contact_scale:
        raise CoupledPlanarDifferentialError("differential interface residual exceeds tolerance")
    if abs(contact_energy_residual) > config.interface_energy_relative_tolerance * contact_scale:
        raise CoupledPlanarDifferentialError("contact energy residual exceeds tolerance")
    if abs(body_energy_residual) > config.body_energy_relative_tolerance * body_scale:
        raise CoupledPlanarDifferentialError("body integration energy residual exceeds tolerance")
    weight = config.vehicle_mass_kg * config.gravity_m_per_s2
    if load_residual > config.balance_relative_tolerance * max(weight, weight * max(config.centre_of_mass_height_m, 1.0)):
        raise CoupledPlanarDifferentialError("normal-load balance residual exceeds tolerance")
    evidence = CoupledStepEvidence(
        "ok" if not failure else "physical_failure", "coupled step passed" if not failure else failure,
        new_planar.time_s, iteration, tuple((item.contact_id, load) for item, load in zip(config.contacts, normal_loads)),
        tuple(records), powertrain_evidence, total_fx, total_fy, yaw_moment, new_ax, new_ay, yaw_acceleration,
        carrier_average_residual, modal_residual, torque_residual, load_residual,
        differential_interface_residual, contact_energy_residual, body_energy_residual,
        global_residual, global_relative, min(normal_loads), max(item.combined_utilization for item in records),
        "DNF" if failure else "running", failure,
    )
    return candidate, evidence


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def run_coupled_planar_differential(
    config: CoupledPlanarDifferentialConfig,
    powertrain: PowertrainConfig,
    *,
    time_step_s: float | None = None,
    sample_stride: int = 1,
) -> CoupledRunResult:
    dt = config.time_step_s if time_step_s is None else _positive("time_step_s", time_step_s)
    if not isinstance(sample_stride, int) or isinstance(sample_stride, bool) or sample_stride <= 0:
        raise CoupledPlanarDifferentialError("sample_stride must be a positive integer")
    count_value = config.duration_s / dt
    requested_steps = round(count_value)
    if not math.isclose(count_value, requested_steps, rel_tol=0.0, abs_tol=1.0e-10):
        raise CoupledPlanarDifferentialError("duration must be an integer multiple of time step")
    state = initial_coupled_state(config, powertrain)
    initial_powertrain_energy = total_powertrain_accounted_energy_j(powertrain, state.powertrain)
    initial_total_energy = total_accounted_energy_j(config, powertrain, state)
    trace: list[CoupledStepEvidence] = []
    maxima = {name: 0.0 for name in (
        "util", "delta", "modal_energy", "load", "carrier", "modal", "torque", "interface", "contact", "body", "global", "relative",
    )}
    minimum_load = math.inf
    saturated_steps = 0
    executed = 0
    for index in range(requested_steps):
        state, evidence = step_coupled_planar_differential(
            config, powertrain, state, initial_powertrain_energy_j=initial_powertrain_energy,
            initial_total_energy_j=initial_total_energy, time_step_s=dt,
        )
        executed += 1
        minimum_load = min(minimum_load, evidence.minimum_normal_load_n)
        maxima["util"] = max(maxima["util"], evidence.maximum_contact_utilization)
        maxima["delta"] = max(maxima["delta"], abs(state.differential_speed_rad_s))
        maxima["modal_energy"] = max(maxima["modal_energy"], modal_energy_j(config, state))
        maxima["load"] = max(maxima["load"], abs(evidence.load_balance_maximum_abs_residual))
        maxima["carrier"] = max(maxima["carrier"], abs(evidence.carrier_average_residual_rad_s))
        maxima["modal"] = max(maxima["modal"], abs(evidence.modal_equation_residual_nm))
        maxima["torque"] = max(maxima["torque"], abs(evidence.torque_residual_nm))
        maxima["interface"] = max(maxima["interface"], abs(evidence.differential_interface_energy_residual_j))
        maxima["contact"] = max(maxima["contact"], abs(evidence.contact_energy_residual_j))
        maxima["body"] = max(maxima["body"], abs(evidence.body_energy_residual_j))
        maxima["global"] = max(maxima["global"], abs(evidence.global_energy_residual_j))
        maxima["relative"] = max(maxima["relative"], evidence.global_relative_energy_residual)
        saturated_steps += int(any(item.saturated for item in evidence.contacts))
        if index % sample_stride == 0 or index == requested_steps - 1 or state.outcome == "DNF":
            trace.append(evidence)
        if state.outcome == "DNF":
            break
    outcome = "finished" if state.outcome == "running" else "DNF"
    status = "passed" if maxima["relative"] <= config.global_energy_relative_tolerance else "failed"
    terminal = "finished" if outcome == "finished" else str(state.dnf_reason)
    final_speeds = tuple(zip((item.side for item in config.differential.branches), branch_speeds(state)))
    body = {
        "model_version": MODEL_VERSION, "protocol_id": config.protocol_id, "status": status,
        "outcome": outcome, "terminal_reason": terminal, "requested_steps": requested_steps,
        "executed_steps": executed, "initial_powertrain_energy_j": initial_powertrain_energy,
        "initial_total_energy_j": initial_total_energy, "final_state": asdict(state),
        "final_branch_speeds_rad_s": final_speeds, "minimum_normal_load_n": minimum_load,
        "maximum_contact_utilization": maxima["util"], "maximum_abs_differential_speed_rad_s": maxima["delta"],
        "maximum_modal_energy_j": maxima["modal_energy"], "maximum_abs_load_balance_residual": maxima["load"],
        "maximum_abs_carrier_average_residual_rad_s": maxima["carrier"],
        "maximum_abs_modal_equation_residual_nm": maxima["modal"], "maximum_abs_torque_residual_nm": maxima["torque"],
        "maximum_abs_differential_interface_energy_residual_j": maxima["interface"],
        "maximum_abs_contact_energy_residual_j": maxima["contact"],
        "maximum_abs_body_energy_residual_j": maxima["body"],
        "maximum_abs_global_energy_residual_j": maxima["global"],
        "maximum_global_relative_energy_residual": maxima["relative"],
        "saturated_step_count": saturated_steps, "trace": [asdict(item) for item in trace],
    }
    identity = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    return CoupledRunResult(
        MODEL_VERSION, config.protocol_id, status, outcome, terminal, requested_steps, executed,
        initial_powertrain_energy, initial_total_energy, state, final_speeds, minimum_load,
        maxima["util"], maxima["delta"], maxima["modal_energy"], maxima["load"], maxima["carrier"],
        maxima["modal"], maxima["torque"], maxima["interface"], maxima["contact"], maxima["body"],
        maxima["global"], maxima["relative"], saturated_steps, tuple(trace), identity,
    )


def result_to_mapping(result: CoupledRunResult) -> dict[str, Any]:
    return asdict(result)
