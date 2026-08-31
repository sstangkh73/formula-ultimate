"""Work 070 energy-conserving differential and independent wheel dynamics."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
import math
from typing import Any, Mapping, Sequence

from formula_ultimate.topology.functional_vehicle import (
    FunctionalVehicle,
    from_functional_mapping,
    functional_mass_properties,
    validate_functional_vehicle,
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


MODEL_VERSION = "differential_independent_wheel_dynamics_v1"


class DifferentialDriveError(ValueError):
    """Raised when differential evidence is incomplete or nonphysical."""


def _finite(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise DifferentialDriveError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise DifferentialDriveError(f"{name} must be finite")
    return result


def _positive(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result <= 0.0:
        raise DifferentialDriveError(f"{name} must be positive")
    return result


def _nonnegative(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result < 0.0:
        raise DifferentialDriveError(f"{name} must be non-negative")
    return result


def _fraction(name: str, value: Any) -> float:
    result = _positive(name, value)
    if result > 1.0:
        raise DifferentialDriveError(f"{name} must not exceed one")
    return result


def _section(raw: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    value = raw.get(name)
    if not isinstance(value, Mapping):
        raise DifferentialDriveError(f"missing section {name}")
    return value


def _close(name: str, actual: float, expected: float, tolerance: float) -> None:
    scale = max(abs(actual), abs(expected), 1.0)
    if abs(actual - expected) > tolerance * scale:
        raise DifferentialDriveError(f"{name} mismatch: {actual!r} versus {expected!r}")


@dataclass(frozen=True, slots=True)
class DifferentialBranchConfig:
    side: str
    contact_id: str
    component_id: str
    connection_id: str
    transmission_output_port_id: str
    ground_unit_drive_port_id: str
    effective_radius_m: float
    rotational_inertia_kg_m2: float
    static_normal_load_n: float
    connection_efficiency: float
    friction_coefficient: float
    longitudinal_stiffness_n_per_slip: float
    maximum_drive_torque_nm: float
    maximum_longitudinal_force_n: float


@dataclass(frozen=True, slots=True)
class DifferentialDriveConfig:
    protocol_id: str
    architecture_candidate_id: str
    differential_component_id: str
    differential_damping_nm_per_rad_s: float
    maximum_differential_speed_rad_s: float
    maximum_branch_speed_rad_s: float
    torque_fractions: tuple[float, float]
    vehicle_mass_kg: float
    gravity_m_per_s2: float
    air_density_kg_per_m3: float
    drag_area_m2: float
    rolling_resistance_coefficient: float
    slip_regularization_speed_m_per_s: float
    other_output_inertia_kg_m2: float
    branches: tuple[DifferentialBranchConfig, DifferentialBranchConfig]
    geometry_relative_tolerance: float
    torque_power_relative_tolerance: float
    energy_relative_tolerance: float
    refinement_relative_tolerance: float

    @property
    def modal_inertia_kg_m2(self) -> float:
        return math.fsum(item.rotational_inertia_kg_m2 for item in self.branches)


@dataclass(frozen=True, slots=True)
class DifferentialDriveState:
    powertrain: PowertrainState
    differential_angle_rad: float
    differential_speed_rad_s: float
    position_m: float
    speed_m_per_s: float
    slip_heat_j: float
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
class DifferentialBranchEvidence:
    side: str
    contact_id: str
    old_speed_rad_s: float
    new_speed_rad_s: float
    mean_speed_rad_s: float
    nominal_drive_torque_nm: float
    slip_ratio: float
    force_capacity_n: float
    requested_force_n: float
    applied_force_n: float
    utilization: float
    wheel_load_torque_nm: float
    reflected_load_torque_nm: float
    wheel_input_work_j: float
    connection_heat_j: float
    body_work_j: float
    slip_heat_j: float


@dataclass(frozen=True, slots=True)
class DifferentialDriveStepEvidence:
    time_s: float
    powertrain: PowertrainStepEvidence
    branches: tuple[DifferentialBranchEvidence, DifferentialBranchEvidence]
    old_differential_speed_rad_s: float
    new_differential_speed_rad_s: float
    differential_modal_energy_change_j: float
    differential_heat_j: float
    requested_carrier_load_torque_nm: float
    applied_carrier_load_torque_nm: float
    total_ground_force_n: float
    acceleration_m_per_s2: float
    carrier_average_residual_rad_s: float
    modal_equation_residual_nm: float
    torque_residual_nm: float
    interface_energy_residual_j: float
    global_energy_residual_j: float
    global_relative_energy_residual: float
    outcome: str
    dnf_reason: str | None


@dataclass(frozen=True, slots=True)
class DifferentialDriveRunResult:
    model_version: str
    protocol_id: str
    status: str
    outcome: str
    terminal_reason: str
    duration_s: float
    step_s: float
    requested_steps: int
    executed_steps: int
    initial_total_energy_j: float
    final_state: DifferentialDriveState
    final_branch_speeds_rad_s: tuple[tuple[str, float], ...]
    maximum_abs_differential_speed_rad_s: float
    maximum_differential_modal_energy_j: float
    maximum_contact_utilization: float
    maximum_abs_carrier_average_residual_rad_s: float
    maximum_abs_modal_equation_residual_nm: float
    maximum_abs_torque_residual_nm: float
    maximum_abs_interface_energy_residual_j: float
    maximum_abs_global_energy_residual_j: float
    maximum_global_relative_energy_residual: float
    trace: tuple[DifferentialDriveStepEvidence, ...]
    result_sha256: str


def _parse_branches(raw: Any) -> tuple[DifferentialBranchConfig, DifferentialBranchConfig]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)) or len(raw) != 2:
        raise DifferentialDriveError("branches must contain exactly two mappings")
    branches: list[DifferentialBranchConfig] = []
    for item in raw:
        if not isinstance(item, Mapping):
            raise DifferentialDriveError("branch must be a mapping")
        strings = tuple(str(item.get(name, "")) for name in (
            "side", "contact_id", "component_id", "connection_id",
            "transmission_output_port_id", "ground_unit_drive_port_id",
        ))
        if any(not value for value in strings):
            raise DifferentialDriveError("branch identities must be nonblank")
        branches.append(DifferentialBranchConfig(
            *strings,
            _positive("effective_radius_m", item.get("effective_radius_m")),
            _positive("rotational_inertia_kg_m2", item.get("rotational_inertia_kg_m2")),
            _positive("static_normal_load_n", item.get("static_normal_load_n")),
            _fraction("connection_efficiency", item.get("connection_efficiency")),
            _positive("friction_coefficient", item.get("friction_coefficient")),
            _positive("longitudinal_stiffness_n_per_slip", item.get("longitudinal_stiffness_n_per_slip")),
            _positive("maximum_drive_torque_nm", item.get("maximum_drive_torque_nm")),
            _positive("maximum_longitudinal_force_n", item.get("maximum_longitudinal_force_n")),
        ))
    branches.sort(key=lambda item: item.side)
    if tuple(item.side for item in branches) != ("left", "right"):
        raise DifferentialDriveError("branch sides must be exactly left and right")
    identity_fields = ("contact_id", "component_id", "connection_id", "transmission_output_port_id", "ground_unit_drive_port_id")
    for field in identity_fields:
        if len({getattr(item, field) for item in branches}) != 2:
            raise DifferentialDriveError(f"branch {field} values must be unique")
    return tuple(branches)  # type: ignore[return-value]


def load_differential_drive_config(
    raw: Mapping[str, Any],
    *,
    powertrain: PowertrainConfig,
    architecture_raw: Mapping[str, Any],
    support_config: SupportGateConfig,
) -> DifferentialDriveConfig:
    if raw.get("model_version") != MODEL_VERSION:
        raise DifferentialDriveError("differential model version mismatch")
    architecture = from_functional_mapping(architecture_raw)
    validate_functional_vehicle(architecture)
    differential = _section(raw, "differential")
    vehicle = _section(raw, "vehicle")
    inertia = _section(raw, "inertia_closure")
    numerical = _section(raw, "numerical")
    left_fraction = _fraction("nominal_left_torque_fraction", differential.get("nominal_left_torque_fraction"))
    right_fraction = _fraction("nominal_right_torque_fraction", differential.get("nominal_right_torque_fraction"))
    _close("nominal torque split", left_fraction + right_fraction, 1.0, 1.0e-12)
    _close("open-differential left torque split", left_fraction, 0.5, 1.0e-12)
    _close("open-differential right torque split", right_fraction, 0.5, 1.0e-12)
    config = DifferentialDriveConfig(
        str(raw.get("protocol_id", "")),
        str(raw.get("architecture_candidate_id", "")),
        str(differential.get("component_id", "")),
        _nonnegative("differential_damping_nm_per_rad_s", differential.get("differential_damping_nm_per_rad_s")),
        _positive("maximum_differential_speed_rad_s", differential.get("maximum_differential_speed_rad_s")),
        _positive("maximum_branch_speed_rad_s", differential.get("maximum_branch_speed_rad_s")),
        (left_fraction, right_fraction),
        _positive("vehicle_mass_kg", vehicle.get("mass_kg")),
        _positive("gravity_m_per_s2", vehicle.get("gravity_m_per_s2")),
        _nonnegative("air_density_kg_per_m3", vehicle.get("air_density_kg_per_m3")),
        _nonnegative("drag_area_m2", vehicle.get("drag_area_m2")),
        _nonnegative("rolling_resistance_coefficient", vehicle.get("rolling_resistance_coefficient")),
        _positive("slip_regularization_speed_m_per_s", vehicle.get("slip_regularization_speed_m_per_s")),
        _nonnegative("other_output_inertia_kg_m2", inertia.get("other_output_inertia_kg_m2")),
        _parse_branches(raw.get("branches")),
        _positive("geometry_relative_tolerance", numerical.get("geometry_relative_tolerance")),
        _positive("torque_power_relative_tolerance", numerical.get("torque_power_relative_tolerance")),
        _positive("energy_relative_tolerance", numerical.get("energy_relative_tolerance")),
        _positive("refinement_relative_tolerance", numerical.get("refinement_relative_tolerance")),
    )
    if not config.protocol_id or config.architecture_candidate_id != architecture.candidate_id:
        raise DifferentialDriveError("protocol or architecture candidate identity mismatch")
    if not config.differential_component_id:
        raise DifferentialDriveError("differential component identity is blank")
    if (
        config.geometry_relative_tolerance > 1.0e-9
        or config.torque_power_relative_tolerance > 1.0e-3
        or config.energy_relative_tolerance > 1.0e-3
        or config.refinement_relative_tolerance > 0.02
    ):
        raise DifferentialDriveError("numerical tolerance exceeds protocol ceiling")
    _validate_architecture(config, powertrain, architecture, support_config, architecture_raw)
    return config


def _validate_architecture(
    config: DifferentialDriveConfig,
    powertrain: PowertrainConfig,
    architecture: FunctionalVehicle,
    support_config: SupportGateConfig,
    architecture_raw: Mapping[str, Any],
) -> None:
    components = {item.component_id: item for item in architecture.components}
    contacts = {item.contact_id: item for item in architecture.ground_contacts}
    connections = {item.connection_id: item for item in architecture.connections}
    ports = {port.port_id: port for component in architecture.components for port in component.ports}
    powered = {item.component_id for item in architecture.components if "ground_propulsion" in item.function_tags}
    if {item.component_id for item in config.branches} != powered or len(powered) != 2:
        raise DifferentialDriveError("differential branches must cover exactly two powered components")
    differential = components.get(config.differential_component_id)
    if differential is None or "power_transmission" not in differential.function_tags:
        raise DifferentialDriveError("differential component lacks power-transmission capability")
    mass = functional_mass_properties(architecture)["mass_kg"]
    _close("geometry-derived vehicle mass", config.vehicle_mass_kg, mass, config.geometry_relative_tolerance)
    static_case = next((item for item in support_config.load_cases if item.case_id == "static"), None)
    if static_case is None:
        raise DifferentialDriveError("support gate has no static load case")
    static_result = solve_support_load_case(architecture_raw, support_config, static_case)
    if static_result.status != "passed":
        raise DifferentialDriveError("support gate static load case did not pass")
    static_loads = dict(static_result.normal_loads_n)
    for branch in config.branches:
        component = components[branch.component_id]
        contact = contacts.get(branch.contact_id)
        connection = connections.get(branch.connection_id)
        if contact is None or contact.component_id != branch.component_id:
            raise DifferentialDriveError("branch contact/component identity mismatch")
        if connection is None or (
            connection.from_port_id != branch.transmission_output_port_id
            or connection.to_port_id != branch.ground_unit_drive_port_id
        ):
            raise DifferentialDriveError("branch connection endpoint mismatch")
        output_port = ports[branch.transmission_output_port_id]
        drive_port = ports[branch.ground_unit_drive_port_id]
        if output_port.component_id != differential.component_id or drive_port.component_id != component.component_id:
            raise DifferentialDriveError("branch port ownership mismatch")
        _close("branch connection efficiency", branch.connection_efficiency, connection.efficiency, config.geometry_relative_tolerance)
        if component.cylinder_axis is None:
            raise DifferentialDriveError("powered branch component must be cylindrical")
        _close("branch effective radius", branch.effective_radius_m, component.dimensions_m[0], config.geometry_relative_tolerance)
        _close(
            "branch geometry-derived inertia", branch.rotational_inertia_kg_m2,
            component.centroidal_inertia_kg_m2[component.cylinder_axis], config.geometry_relative_tolerance,
        )
        _close("branch static normal load", branch.static_normal_load_n, static_loads[branch.contact_id], config.geometry_relative_tolerance)
        if branch.maximum_drive_torque_nm > min(output_port.limits["maximum_torque_nm"], drive_port.limits["maximum_torque_nm"], component.parameters["maximum_drive_torque_nm"]):
            raise DifferentialDriveError("branch torque limit exceeds architecture")
        if config.maximum_branch_speed_rad_s > min(output_port.limits["maximum_speed_rad_per_s"], drive_port.limits["maximum_speed_rad_per_s"]):
            raise DifferentialDriveError("branch speed limit exceeds architecture")
        if branch.maximum_longitudinal_force_n > min(contact.maximum_longitudinal_force_n, next(item for item in component.ports if item.port_id == contact.port_id).limits["maximum_longitudinal_force_n"]):
            raise DifferentialDriveError("branch longitudinal force limit exceeds architecture")
        if branch.static_normal_load_n > contact.maximum_normal_force_n:
            raise DifferentialDriveError("branch static normal load exceeds architecture")
    _close(
        "common output inertia closure",
        config.other_output_inertia_kg_m2 + config.modal_inertia_kg_m2,
        powertrain.output_inertia_kg_m2,
        config.geometry_relative_tolerance,
    )


def with_branch_friction(config: DifferentialDriveConfig, *, left: float, right: float) -> DifferentialDriveConfig:
    coefficients = (_positive("left friction", left), _positive("right friction", right))
    return replace(config, branches=tuple(replace(branch, friction_coefficient=value) for branch, value in zip(config.branches, coefficients)))  # type: ignore[arg-type]


def branch_speeds(config: DifferentialDriveConfig, state: DifferentialDriveState) -> tuple[float, float]:
    carrier = state.powertrain.output_speed_rad_s
    delta = state.differential_speed_rad_s
    return carrier - delta, carrier + delta


def differential_modal_energy_j(config: DifferentialDriveConfig, state: DifferentialDriveState) -> float:
    return 0.5 * config.modal_inertia_kg_m2 * state.differential_speed_rad_s ** 2


def initial_differential_drive_state(
    config: DifferentialDriveConfig,
    powertrain: PowertrainConfig,
    *,
    initial_storage_energy_j: float | None = None,
    initial_speed_m_per_s: float = 0.0,
) -> DifferentialDriveState:
    speed = _nonnegative("initial_speed_m_per_s", initial_speed_m_per_s)
    return DifferentialDriveState(
        initial_powertrain_state(powertrain, storage_energy_j=initial_storage_energy_j),
        0.0, 0.0, 0.0, speed, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        "running", "operational", None, None,
    )


def total_differential_drive_accounted_energy_j(
    config: DifferentialDriveConfig,
    powertrain: PowertrainConfig,
    state: DifferentialDriveState,
) -> float:
    return (
        total_powertrain_accounted_energy_j(powertrain, state.powertrain)
        - state.powertrain.useful_work_j
        + differential_modal_energy_j(config, state)
        + 0.5 * config.vehicle_mass_kg * state.speed_m_per_s ** 2
        + state.slip_heat_j
        + state.branch_connection_heat_j
        + state.differential_heat_j
        + state.aerodynamic_work_j
        + state.rolling_work_j
    )


def _ground_unit(branch: DifferentialBranchConfig) -> GroundUnitConfig:
    return GroundUnitConfig(
        branch.contact_id, branch.component_id, branch.effective_radius_m,
        branch.rotational_inertia_kg_m2, branch.static_normal_load_n,
        branch.friction_coefficient, branch.longitudinal_stiffness_n_per_slip,
        branch.maximum_longitudinal_force_n,
    )


def step_differential_drive(
    config: DifferentialDriveConfig,
    powertrain: PowertrainConfig,
    state: DifferentialDriveState,
    *,
    throttle: float,
    step_s: float,
    initial_total_energy_j: float,
) -> tuple[DifferentialDriveState, DifferentialDriveStepEvidence]:
    if state.outcome != "running":
        raise DifferentialDriveError("DNF state cannot execute another differential step")
    dt = _positive("step_s", step_s)
    old_branch_speeds = branch_speeds(config, state)
    if min(old_branch_speeds) < 0.0:
        raise DifferentialDriveError("reverse branch rotation is outside Work 070 scope")
    requests = tuple(
        ground_force_request(
            _ground_unit(branch), wheel_speed_rad_per_s=omega,
            vehicle_speed_m_per_s=state.speed_m_per_s,
            regularization_speed_m_per_s=config.slip_regularization_speed_m_per_s,
        )
        for branch, omega in zip(config.branches, old_branch_speeds)
    )
    requested_wheel_torques = tuple(request["requested_force_n"] * branch.effective_radius_m for branch, request in zip(config.branches, requests))
    requested_reflected_torques = tuple(torque / branch.connection_efficiency for torque, branch in zip(requested_wheel_torques, config.branches))
    requested_carrier_torque = math.fsum(requested_reflected_torques)
    old_powertrain = state.powertrain
    new_powertrain, powertrain_evidence = step_powertrain(
        powertrain, old_powertrain, throttle=throttle,
        requested_load_torque_nm=requested_carrier_torque,
        step_s=dt, initial_energy_j=initial_total_energy_j,
    )
    applied_carrier_torque = powertrain_evidence.applied_load_torque_nm
    scale = 0.0 if requested_carrier_torque == 0.0 else applied_carrier_torque / requested_carrier_torque
    if scale < -config.torque_power_relative_tolerance or scale > 1.0 + config.torque_power_relative_tolerance:
        raise DifferentialDriveError("powertrain returned an invalid carrier-load scale")
    scale = min(1.0, max(0.0, scale))
    applied_forces = tuple(request["requested_force_n"] * scale for request in requests)
    wheel_torques = tuple(force * branch.effective_radius_m for force, branch in zip(applied_forces, config.branches))
    reflected_torques = tuple(torque / branch.connection_efficiency for torque, branch in zip(wheel_torques, config.branches))

    modal_inertia = config.modal_inertia_kg_m2
    old_delta = state.differential_speed_rad_s
    load_difference = reflected_torques[0] - reflected_torques[1]
    damping = config.differential_damping_nm_per_rad_s
    new_delta = (
        (modal_inertia / dt - 0.5 * damping) * old_delta + load_difference
    ) / (modal_inertia / dt + 0.5 * damping)
    mean_delta = 0.5 * (old_delta + new_delta)
    new_angle = state.differential_angle_rad + mean_delta * dt
    new_branch_speeds = (
        new_powertrain.output_speed_rad_s - new_delta,
        new_powertrain.output_speed_rad_s + new_delta,
    )
    mean_carrier_speed = 0.5 * (old_powertrain.output_speed_rad_s + new_powertrain.output_speed_rad_s)
    mean_branch_speeds = tuple(0.5 * (old + new) for old, new in zip(old_branch_speeds, new_branch_speeds))
    modal_energy_change = 0.5 * modal_inertia * (new_delta ** 2 - old_delta ** 2)
    differential_heat = damping * mean_delta ** 2 * dt

    total_force = math.fsum(applied_forces)
    drag = 0.5 * config.air_density_kg_per_m3 * config.drag_area_m2 * state.speed_m_per_s ** 2
    rolling_capacity = config.rolling_resistance_coefficient * config.vehicle_mass_kg * config.gravity_m_per_s2
    rolling = rolling_capacity if state.speed_m_per_s > 0.0 else min(rolling_capacity, total_force)
    acceleration = (total_force - drag - rolling) / config.vehicle_mass_kg
    raw_speed = state.speed_m_per_s + acceleration * dt
    if raw_speed < 0.0:
        stop_time = state.speed_m_per_s / -acceleration
        distance = 0.5 * state.speed_m_per_s * stop_time
        new_speed = 0.0
    else:
        new_speed = raw_speed
        distance = 0.5 * (state.speed_m_per_s + new_speed) * dt
    body_work_total = total_force * distance

    branch_records: list[DifferentialBranchEvidence] = []
    slip_heat_total = connection_heat_total = 0.0
    for index, (branch, request, applied_force) in enumerate(zip(config.branches, requests, applied_forces)):
        body_work = 0.0 if total_force == 0.0 else body_work_total * applied_force / total_force
        reflected_work = reflected_torques[index] * mean_branch_speeds[index] * dt
        wheel_input_work = wheel_torques[index] * mean_branch_speeds[index] * dt
        connection_heat = reflected_work - wheel_input_work
        slip_heat = wheel_input_work - body_work
        scale_energy = max(abs(reflected_work), abs(wheel_input_work), abs(body_work), 1.0)
        if connection_heat < -config.torque_power_relative_tolerance * scale_energy:
            raise DifferentialDriveError("negative branch-connection dissipation exceeds tolerance")
        if slip_heat < -config.torque_power_relative_tolerance * scale_energy:
            raise DifferentialDriveError("negative slip dissipation exceeds tolerance")
        connection_heat = max(0.0, connection_heat)
        slip_heat = max(0.0, slip_heat)
        connection_heat_total += connection_heat
        slip_heat_total += slip_heat
        capacity = request["force_capacity_n"]
        nominal_drive_torque = powertrain_evidence.output_drive_torque_nm * config.torque_fractions[index] * branch.connection_efficiency
        branch_records.append(DifferentialBranchEvidence(
            branch.side, branch.contact_id, old_branch_speeds[index], new_branch_speeds[index], mean_branch_speeds[index],
            nominal_drive_torque, request["slip_ratio"], capacity, request["requested_force_n"], applied_force,
            0.0 if capacity == 0.0 else applied_force / capacity, wheel_torques[index], reflected_torques[index],
            wheel_input_work, connection_heat, body_work, slip_heat,
        ))

    carrier_input_work = new_powertrain.useful_work_j - old_powertrain.useful_work_j
    reflected_branch_work = math.fsum(torque * speed * dt for torque, speed in zip(reflected_torques, mean_branch_speeds))
    interface_residual = carrier_input_work - reflected_branch_work - modal_energy_change - differential_heat
    carrier_average_residual = new_powertrain.output_speed_rad_s - 0.5 * math.fsum(new_branch_speeds)
    modal_equation_residual = modal_inertia * (new_delta - old_delta) / dt - (load_difference - damping * mean_delta)
    torque_residual = applied_carrier_torque - math.fsum(reflected_torques)
    interface_scale = max(
        abs(carrier_input_work), abs(reflected_branch_work),
        abs(modal_energy_change), abs(differential_heat), 1.0,
    )
    if abs(interface_residual) > config.torque_power_relative_tolerance * interface_scale:
        raise DifferentialDriveError("differential interface energy residual exceeds tolerance")

    failure = new_powertrain.failure_code
    if failure is None and min(new_branch_speeds) < -config.torque_power_relative_tolerance:
        failure = "differential_branch_reverse_rotation"
    if failure is None and max(new_branch_speeds) > config.maximum_branch_speed_rad_s:
        failure = "differential_branch_overspeed"
    if failure is None and abs(new_delta) > config.maximum_differential_speed_rad_s:
        failure = "differential_mode_overspeed"
    if failure is None and any(abs(item.nominal_drive_torque_nm) > branch.maximum_drive_torque_nm for item, branch in zip(branch_records, config.branches)):
        failure = "differential_branch_overtorque"
    outcome = "DNF" if failure is not None else "running"
    candidate = DifferentialDriveState(
        new_powertrain, new_angle, new_delta, state.position_m + distance, new_speed,
        state.slip_heat_j + slip_heat_total,
        state.branch_connection_heat_j + connection_heat_total,
        state.differential_heat_j + differential_heat,
        state.aerodynamic_work_j + drag * distance,
        state.rolling_work_j + rolling * distance,
        state.contact_body_work_j + body_work_total,
        outcome, "failed" if outcome == "DNF" else "operational", failure,
        new_powertrain.failure_time_s if new_powertrain.failure_code is not None else (new_powertrain.time_s if failure is not None else None),
    )
    global_residual = initial_total_energy_j - total_differential_drive_accounted_energy_j(config, powertrain, candidate)
    relative_global = abs(global_residual) / max(abs(initial_total_energy_j), candidate.powertrain.source_energy_used_j, 1.0)
    evidence = DifferentialDriveStepEvidence(
        candidate.powertrain.time_s, powertrain_evidence, tuple(branch_records), old_delta, new_delta,
        modal_energy_change, differential_heat, requested_carrier_torque, applied_carrier_torque,
        total_force, acceleration, carrier_average_residual, modal_equation_residual, torque_residual,
        interface_residual, global_residual, relative_global, outcome, failure,
    )
    return candidate, evidence  # type: ignore[arg-type]


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def run_differential_drive(
    config: DifferentialDriveConfig,
    powertrain: PowertrainConfig,
    *,
    throttle: float,
    duration_s: float,
    step_s: float,
    initial_storage_energy_j: float | None = None,
    sample_stride: int = 1,
) -> DifferentialDriveRunResult:
    duration = _positive("duration_s", duration_s)
    dt = _positive("step_s", step_s)
    if not isinstance(sample_stride, int) or isinstance(sample_stride, bool) or sample_stride <= 0:
        raise DifferentialDriveError("sample_stride must be a positive integer")
    count_value = duration / dt
    requested_steps = round(count_value)
    if requested_steps <= 0 or not math.isclose(count_value, requested_steps, rel_tol=0.0, abs_tol=1.0e-10):
        raise DifferentialDriveError("duration must be an integer multiple of step")
    state = initial_differential_drive_state(config, powertrain, initial_storage_energy_j=initial_storage_energy_j)
    initial_energy = total_differential_drive_accounted_energy_j(config, powertrain, state)
    trace: list[DifferentialDriveStepEvidence] = []
    maxima = {name: 0.0 for name in (
        "delta", "modal_energy", "utilization", "carrier", "modal", "torque", "interface", "global", "relative",
    )}
    for index in range(requested_steps):
        state, evidence = step_differential_drive(
            config, powertrain, state, throttle=throttle, step_s=dt,
            initial_total_energy_j=initial_energy,
        )
        maxima["delta"] = max(maxima["delta"], abs(state.differential_speed_rad_s))
        maxima["modal_energy"] = max(maxima["modal_energy"], differential_modal_energy_j(config, state))
        maxima["utilization"] = max(maxima["utilization"], *(item.utilization for item in evidence.branches))
        maxima["carrier"] = max(maxima["carrier"], abs(evidence.carrier_average_residual_rad_s))
        maxima["modal"] = max(maxima["modal"], abs(evidence.modal_equation_residual_nm))
        maxima["torque"] = max(maxima["torque"], abs(evidence.torque_residual_nm))
        maxima["interface"] = max(maxima["interface"], abs(evidence.interface_energy_residual_j))
        maxima["global"] = max(maxima["global"], abs(evidence.global_energy_residual_j))
        maxima["relative"] = max(maxima["relative"], evidence.global_relative_energy_residual)
        if index % sample_stride == 0 or index == requested_steps - 1 or state.outcome == "DNF":
            trace.append(evidence)
        if state.outcome == "DNF":
            break
    branch_final = tuple(zip((item.side for item in config.branches), branch_speeds(config, state)))
    result_outcome = "finished" if state.outcome == "running" else "DNF"
    status, terminal = "passed", "finished" if result_outcome == "finished" else str(state.dnf_reason)
    if maxima["relative"] > config.energy_relative_tolerance:
        status, terminal = "failed", "global_energy_conservation_residual"
    body = {
        "model_version": MODEL_VERSION,
        "protocol_id": config.protocol_id,
        "status": status,
        "outcome": result_outcome,
        "terminal_reason": terminal,
        "duration_s": duration,
        "step_s": dt,
        "requested_steps": requested_steps,
        "executed_steps": round(state.powertrain.time_s / dt),
        "initial_total_energy_j": initial_energy,
        "final_state": asdict(state),
        "final_branch_speeds_rad_s": branch_final,
        "maximum_abs_differential_speed_rad_s": maxima["delta"],
        "maximum_differential_modal_energy_j": maxima["modal_energy"],
        "maximum_contact_utilization": maxima["utilization"],
        "maximum_abs_carrier_average_residual_rad_s": maxima["carrier"],
        "maximum_abs_modal_equation_residual_nm": maxima["modal"],
        "maximum_abs_torque_residual_nm": maxima["torque"],
        "maximum_abs_interface_energy_residual_j": maxima["interface"],
        "maximum_abs_global_energy_residual_j": maxima["global"],
        "maximum_global_relative_energy_residual": maxima["relative"],
        "trace": [asdict(item) for item in trace],
    }
    identity = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    return DifferentialDriveRunResult(
        MODEL_VERSION, config.protocol_id, status, result_outcome, terminal, duration, dt,
        requested_steps, body["executed_steps"], initial_energy, state, branch_final,
        maxima["delta"], maxima["modal_energy"], maxima["utilization"], maxima["carrier"],
        maxima["modal"], maxima["torque"], maxima["interface"], maxima["global"], maxima["relative"],
        tuple(trace), identity,
    )


def result_to_mapping(result: DifferentialDriveRunResult) -> dict[str, Any]:
    return asdict(result)
