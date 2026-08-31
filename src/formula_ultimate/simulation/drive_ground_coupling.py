"""Work 068 drive torque, longitudinal slip, ground force, and DNF coupling."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from typing import Any, Mapping, Sequence

from formula_ultimate.topology.functional_vehicle import (
    FunctionalVehicle,
    from_functional_mapping,
    functional_mass_properties,
)

from .powertrain_dynamics import (
    PowertrainConfig,
    PowertrainState,
    StepEvidence as PowertrainStepEvidence,
    initial_powertrain_state,
    step_powertrain,
    total_accounted_energy_j as total_powertrain_accounted_energy_j,
)


MODEL_VERSION = "drive_ground_slip_coupling_v1"


class DriveGroundCouplingError(ValueError):
    """Raised when drive-ground evidence is incomplete or physically invalid."""


def _finite(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise DriveGroundCouplingError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise DriveGroundCouplingError(f"{name} must be finite")
    return result


def _positive(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result <= 0.0:
        raise DriveGroundCouplingError(f"{name} must be positive")
    return result


def _nonnegative(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result < 0.0:
        raise DriveGroundCouplingError(f"{name} must be non-negative")
    return result


@dataclass(frozen=True, slots=True)
class GroundUnitConfig:
    contact_id: str
    component_id: str
    effective_radius_m: float
    rotational_inertia_kg_m2: float
    normal_load_n: float
    friction_coefficient: float
    longitudinal_stiffness_n_per_slip: float
    maximum_longitudinal_force_n: float


@dataclass(frozen=True, slots=True)
class DriveGroundConfig:
    protocol_id: str
    architecture_candidate_id: str
    vehicle_mass_kg: float
    gravity_m_per_s2: float
    air_density_kg_per_m3: float
    drag_area_m2: float
    rolling_resistance_coefficient: float
    slip_regularization_speed_m_per_s: float
    other_output_inertia_kg_m2: float
    ground_units: tuple[GroundUnitConfig, ...]
    geometry_relative_tolerance: float
    torque_power_relative_tolerance: float
    energy_relative_tolerance: float
    refinement_relative_tolerance: float


@dataclass(frozen=True, slots=True)
class DriveGroundState:
    powertrain: PowertrainState
    position_m: float
    speed_m_per_s: float
    slip_heat_j: float
    aerodynamic_work_j: float
    rolling_work_j: float
    contact_body_work_j: float
    outcome: str
    drive_subsystem_state: str
    dnf_reason: str | None
    dnf_time_s: float | None


@dataclass(frozen=True, slots=True)
class GroundUnitEvidence:
    contact_id: str
    component_id: str
    wheel_speed_rad_per_s: float
    surface_speed_m_per_s: float
    slip_velocity_m_per_s: float
    slip_ratio: float
    force_capacity_n: float
    requested_force_n: float
    applied_force_n: float
    utilization: float
    load_torque_nm: float
    body_work_j: float
    slip_heat_j: float


@dataclass(frozen=True, slots=True)
class DriveGroundStepEvidence:
    time_s: float
    powertrain: PowertrainStepEvidence
    contacts: tuple[GroundUnitEvidence, ...]
    requested_axle_load_torque_nm: float
    applied_axle_load_torque_nm: float
    total_ground_force_n: float
    aerodynamic_drag_n: float
    rolling_resistance_n: float
    acceleration_m_per_s2: float
    distance_increment_m: float
    torque_to_force_residual_nm: float
    interface_power_partition_residual_j: float
    global_energy_residual_j: float
    global_relative_energy_residual: float
    outcome: str
    dnf_reason: str | None


@dataclass(frozen=True, slots=True)
class DriveGroundRunResult:
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
    final_state: DriveGroundState
    maximum_ground_force_n: float
    maximum_contact_utilization: float
    maximum_slip_ratio: float
    maximum_abs_torque_residual_nm: float
    maximum_abs_interface_partition_residual_j: float
    maximum_abs_global_energy_residual_j: float
    maximum_global_relative_energy_residual: float
    trace: tuple[DriveGroundStepEvidence, ...]
    result_sha256: str


def _section(raw: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    value = raw.get(name)
    if not isinstance(value, Mapping):
        raise DriveGroundCouplingError(f"missing section {name}")
    return value


def _close(name: str, actual: float, expected: float, tolerance: float) -> None:
    scale = max(abs(actual), abs(expected), 1.0)
    if abs(actual - expected) > tolerance * scale:
        raise DriveGroundCouplingError(f"{name} mismatch: {actual!r} versus {expected!r}")


def load_drive_ground_config(
    raw: Mapping[str, Any],
    *,
    powertrain: PowertrainConfig,
    architecture_raw: Mapping[str, Any],
) -> DriveGroundConfig:
    if raw.get("model_version") != MODEL_VERSION:
        raise DriveGroundCouplingError("drive-ground model version mismatch")
    architecture = from_functional_mapping(architecture_raw)
    vehicle = _section(raw, "vehicle")
    inertia = _section(raw, "inertia_closure")
    numerical = _section(raw, "numerical")
    geometry_tolerance = _positive("geometry_relative_tolerance", numerical.get("geometry_relative_tolerance"))
    units_raw = raw.get("ground_units")
    if not isinstance(units_raw, Sequence) or isinstance(units_raw, (str, bytes)) or not units_raw:
        raise DriveGroundCouplingError("ground_units must be nonempty")
    units: list[GroundUnitConfig] = []
    for item in units_raw:
        if not isinstance(item, Mapping):
            raise DriveGroundCouplingError("ground unit must be a mapping")
        contact_id, component_id = str(item.get("contact_id", "")), str(item.get("component_id", ""))
        if not contact_id or not component_id:
            raise DriveGroundCouplingError("ground identities must be nonblank")
        units.append(GroundUnitConfig(
            contact_id,
            component_id,
            _positive("effective_radius_m", item.get("effective_radius_m")),
            _positive("rotational_inertia_kg_m2", item.get("rotational_inertia_kg_m2")),
            _positive("normal_load_n", item.get("normal_load_n")),
            _positive("friction_coefficient", item.get("friction_coefficient")),
            _positive("longitudinal_stiffness_n_per_slip", item.get("longitudinal_stiffness_n_per_slip")),
            _positive("maximum_longitudinal_force_n", item.get("maximum_longitudinal_force_n")),
        ))
    ids = tuple(item.contact_id for item in units)
    component_ids = tuple(item.component_id for item in units)
    if len(ids) != len(set(ids)) or len(component_ids) != len(set(component_ids)):
        raise DriveGroundCouplingError("ground unit identities must be unique")
    config = DriveGroundConfig(
        str(raw.get("protocol_id", "")),
        str(raw.get("architecture_candidate_id", "")),
        _positive("vehicle_mass_kg", vehicle.get("mass_kg")),
        _positive("gravity_m_per_s2", vehicle.get("gravity_m_per_s2")),
        _nonnegative("air_density_kg_per_m3", vehicle.get("air_density_kg_per_m3")),
        _nonnegative("drag_area_m2", vehicle.get("drag_area_m2")),
        _nonnegative("rolling_resistance_coefficient", vehicle.get("rolling_resistance_coefficient")),
        _positive("slip_regularization_speed_m_per_s", vehicle.get("slip_regularization_speed_m_per_s")),
        _nonnegative("other_output_inertia_kg_m2", inertia.get("other_output_inertia_kg_m2")),
        tuple(units),
        geometry_tolerance,
        _positive("torque_power_relative_tolerance", numerical.get("torque_power_relative_tolerance")),
        _positive("energy_relative_tolerance", numerical.get("energy_relative_tolerance")),
        _positive("refinement_relative_tolerance", numerical.get("refinement_relative_tolerance")),
    )
    if not config.protocol_id.strip() or config.architecture_candidate_id != architecture.candidate_id:
        raise DriveGroundCouplingError("protocol or architecture candidate identity mismatch")
    if config.torque_power_relative_tolerance > 1.0e-3 or config.energy_relative_tolerance > 1.0e-3 or config.refinement_relative_tolerance > 0.02:
        raise DriveGroundCouplingError("numerical tolerance exceeds protocol ceiling")
    _validate_geometry(config, powertrain, architecture)
    return config


def _validate_geometry(config: DriveGroundConfig, powertrain: PowertrainConfig, architecture: FunctionalVehicle) -> None:
    components = {item.component_id: item for item in architecture.components}
    contacts = {item.contact_id: item for item in architecture.ground_contacts}
    expected_contacts = set(contacts)
    if {item.contact_id for item in config.ground_units} != expected_contacts:
        raise DriveGroundCouplingError("ground contact set differs from architecture")
    mass = functional_mass_properties(architecture)["mass_kg"]
    _close("geometry-derived vehicle mass", config.vehicle_mass_kg, mass, config.geometry_relative_tolerance)
    for unit in config.ground_units:
        if unit.contact_id not in contacts or unit.component_id not in components:
            raise DriveGroundCouplingError("ground unit references unknown architecture identity")
        contact, component = contacts[unit.contact_id], components[unit.component_id]
        if contact.component_id != unit.component_id or "ground_propulsion" not in component.function_tags:
            raise DriveGroundCouplingError("ground unit capability/contact mismatch")
        if component.cylinder_axis is None:
            raise DriveGroundCouplingError("v1 ground radius requires a cylindrical component")
        radius = component.dimensions_m[0]
        axial_inertia = component.centroidal_inertia_kg_m2[component.cylinder_axis]
        _close(f"{unit.component_id} radius", unit.effective_radius_m, radius, config.geometry_relative_tolerance)
        _close(f"{unit.component_id} axial inertia", unit.rotational_inertia_kg_m2, axial_inertia, config.geometry_relative_tolerance)
        if unit.normal_load_n > contact.maximum_normal_force_n:
            raise DriveGroundCouplingError("normal load exceeds declared contact limit")
        if unit.maximum_longitudinal_force_n > contact.maximum_longitudinal_force_n:
            raise DriveGroundCouplingError("longitudinal force exceeds declared contact limit")
        port = next(item for item in component.ports if item.port_id == contact.port_id)
        if unit.maximum_longitudinal_force_n > port.limits["maximum_longitudinal_force_n"]:
            raise DriveGroundCouplingError("longitudinal force exceeds ground port limit")
        drive_port = next(item for item in component.ports if item.domain == "mechanical_rotary" and "drive" in item.port_id)
        if unit.maximum_longitudinal_force_n * unit.effective_radius_m > drive_port.limits["maximum_torque_nm"]:
            raise DriveGroundCouplingError("force-radius demand exceeds drive-port torque")
    _close(
        "static normal-load closure",
        math.fsum(item.normal_load_n for item in config.ground_units),
        config.vehicle_mass_kg * config.gravity_m_per_s2,
        config.geometry_relative_tolerance,
    )
    _close(
        "output inertia closure",
        math.fsum(item.rotational_inertia_kg_m2 for item in config.ground_units) + config.other_output_inertia_kg_m2,
        powertrain.output_inertia_kg_m2,
        config.geometry_relative_tolerance,
    )


def initial_drive_ground_state(
    config: DriveGroundConfig,
    powertrain: PowertrainConfig,
    *,
    initial_storage_energy_j: float | None = None,
    initial_speed_m_per_s: float = 0.0,
) -> DriveGroundState:
    speed = _nonnegative("initial_speed_m_per_s", initial_speed_m_per_s)
    return DriveGroundState(
        initial_powertrain_state(powertrain, storage_energy_j=initial_storage_energy_j),
        0.0, speed, 0.0, 0.0, 0.0, 0.0, "running", "operational", None, None,
    )


def ground_force_request(unit: GroundUnitConfig, *, wheel_speed_rad_per_s: float, vehicle_speed_m_per_s: float, regularization_speed_m_per_s: float) -> dict[str, float]:
    omega = _nonnegative("wheel_speed_rad_per_s", wheel_speed_rad_per_s)
    speed = _nonnegative("vehicle_speed_m_per_s", vehicle_speed_m_per_s)
    regularization = _positive("regularization_speed_m_per_s", regularization_speed_m_per_s)
    surface = unit.effective_radius_m * omega
    slip_velocity = surface - speed
    slip_ratio = slip_velocity / max(speed, regularization)
    capacity = min(unit.friction_coefficient * unit.normal_load_n, unit.maximum_longitudinal_force_n)
    requested = 0.0 if slip_ratio <= 0.0 else capacity * math.tanh(unit.longitudinal_stiffness_n_per_slip * slip_ratio / capacity)
    if not all(math.isfinite(item) for item in (surface, slip_velocity, slip_ratio, capacity, requested)):
        raise DriveGroundCouplingError("slip law produced a non-finite state")
    return {
        "surface_speed_m_per_s": surface,
        "slip_velocity_m_per_s": slip_velocity,
        "slip_ratio": slip_ratio,
        "force_capacity_n": capacity,
        "requested_force_n": requested,
    }


def analytical_ground_partition(*, wheel_speed_rad_per_s: float, vehicle_speed_m_per_s: float, forces_n: Sequence[float], radii_m: Sequence[float]) -> dict[str, float]:
    omega = _nonnegative("wheel_speed_rad_per_s", wheel_speed_rad_per_s)
    speed = _nonnegative("vehicle_speed_m_per_s", vehicle_speed_m_per_s)
    if len(forces_n) != len(radii_m) or not forces_n:
        raise DriveGroundCouplingError("forces and radii must have equal nonzero length")
    forces = tuple(_nonnegative("force_n", value) for value in forces_n)
    radii = tuple(_positive("radius_m", value) for value in radii_m)
    torque = math.fsum(force * radius for force, radius in zip(forces, radii))
    input_power = torque * omega
    body_power = math.fsum(forces) * speed
    slip_heat = math.fsum(force * (radius * omega - speed) for force, radius in zip(forces, radii))
    return {
        "load_torque_nm": torque,
        "input_power_w": input_power,
        "body_power_w": body_power,
        "slip_heat_w": slip_heat,
        "power_residual_w": input_power - body_power - slip_heat,
    }


def total_drive_ground_accounted_energy_j(config: DriveGroundConfig, powertrain: PowertrainConfig, state: DriveGroundState) -> float:
    return (
        total_powertrain_accounted_energy_j(powertrain, state.powertrain)
        - state.powertrain.useful_work_j
        + 0.5 * config.vehicle_mass_kg * state.speed_m_per_s ** 2
        + state.slip_heat_j + state.aerodynamic_work_j + state.rolling_work_j
    )


def step_drive_ground(
    config: DriveGroundConfig,
    powertrain: PowertrainConfig,
    state: DriveGroundState,
    *,
    throttle: float,
    step_s: float,
    initial_total_energy_j: float,
) -> tuple[DriveGroundState, DriveGroundStepEvidence]:
    if state.outcome != "running":
        raise DriveGroundCouplingError("DNF state cannot execute another drive-ground step")
    dt = _positive("step_s", step_s)
    requests = tuple(
        ground_force_request(
            unit,
            wheel_speed_rad_per_s=state.powertrain.output_speed_rad_s,
            vehicle_speed_m_per_s=state.speed_m_per_s,
            regularization_speed_m_per_s=config.slip_regularization_speed_m_per_s,
        )
        for unit in config.ground_units
    )
    requested_torque = math.fsum(
        request["requested_force_n"] * unit.effective_radius_m
        for unit, request in zip(config.ground_units, requests)
    )
    old_powertrain = state.powertrain
    new_powertrain, powertrain_evidence = step_powertrain(
        powertrain,
        old_powertrain,
        throttle=throttle,
        requested_load_torque_nm=requested_torque,
        step_s=dt,
        initial_energy_j=initial_total_energy_j,
    )
    applied_torque = powertrain_evidence.applied_load_torque_nm
    scale = 0.0 if requested_torque == 0.0 else applied_torque / requested_torque
    if scale < -config.torque_power_relative_tolerance or scale > 1.0 + config.torque_power_relative_tolerance:
        raise DriveGroundCouplingError("powertrain returned an invalid ground-load scale")
    scale = min(1.0, max(0.0, scale))
    applied_forces = tuple(request["requested_force_n"] * scale for request in requests)
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
    mean_output_speed = 0.5 * (old_powertrain.output_speed_rad_s + new_powertrain.output_speed_rad_s)
    body_work_total = total_force * distance
    drag_work = drag * distance
    rolling_work = rolling * distance
    ground_input_work = new_powertrain.useful_work_j - old_powertrain.useful_work_j
    contacts: list[GroundUnitEvidence] = []
    slip_heat_total = 0.0
    for unit, request, applied_force in zip(config.ground_units, requests, applied_forces):
        body_work = 0.0 if total_force == 0.0 else body_work_total * applied_force / total_force
        input_work = applied_force * unit.effective_radius_m * mean_output_speed * dt
        slip_heat = input_work - body_work
        if slip_heat < -config.torque_power_relative_tolerance * max(abs(input_work), abs(body_work), 1.0):
            raise DriveGroundCouplingError("negative slip dissipation exceeds coupling tolerance")
        slip_heat = max(0.0, slip_heat)
        slip_heat_total += slip_heat
        capacity = request["force_capacity_n"]
        contacts.append(GroundUnitEvidence(
            unit.contact_id, unit.component_id, old_powertrain.output_speed_rad_s,
            request["surface_speed_m_per_s"], request["slip_velocity_m_per_s"],
            request["slip_ratio"], capacity, request["requested_force_n"], applied_force,
            0.0 if capacity == 0.0 else applied_force / capacity,
            applied_force * unit.effective_radius_m, body_work, slip_heat,
        ))
    torque_residual = applied_torque - math.fsum(item.load_torque_nm for item in contacts)
    interface_residual = ground_input_work - body_work_total - slip_heat_total
    outcome = "DNF" if new_powertrain.failure_code is not None else "running"
    candidate = DriveGroundState(
        new_powertrain,
        state.position_m + distance,
        new_speed,
        state.slip_heat_j + slip_heat_total,
        state.aerodynamic_work_j + drag_work,
        state.rolling_work_j + rolling_work,
        state.contact_body_work_j + body_work_total,
        outcome,
        "failed" if outcome == "DNF" else "operational",
        new_powertrain.failure_code,
        new_powertrain.failure_time_s,
    )
    global_residual = initial_total_energy_j - total_drive_ground_accounted_energy_j(config, powertrain, candidate)
    relative = abs(global_residual) / max(abs(initial_total_energy_j), candidate.powertrain.source_energy_used_j, 1.0)
    if abs(torque_residual) > config.torque_power_relative_tolerance * max(abs(applied_torque), 1.0):
        raise DriveGroundCouplingError("torque-to-force residual exceeds tolerance")
    if abs(interface_residual) > config.torque_power_relative_tolerance * max(abs(ground_input_work), 1.0):
        raise DriveGroundCouplingError("interface power partition residual exceeds tolerance")
    evidence = DriveGroundStepEvidence(
        new_powertrain.time_s, powertrain_evidence, tuple(contacts), requested_torque,
        applied_torque, total_force, drag, rolling, acceleration, distance,
        torque_residual, interface_residual, global_residual, relative, outcome,
        candidate.dnf_reason,
    )
    return candidate, evidence


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def run_drive_ground(
    config: DriveGroundConfig,
    powertrain: PowertrainConfig,
    *,
    throttle: float,
    duration_s: float,
    step_s: float,
    initial_storage_energy_j: float | None = None,
    sample_stride: int = 1,
) -> DriveGroundRunResult:
    duration = _positive("duration_s", duration_s)
    dt = _positive("step_s", step_s)
    if not isinstance(sample_stride, int) or isinstance(sample_stride, bool) or sample_stride <= 0:
        raise DriveGroundCouplingError("sample_stride must be a positive integer")
    count_value = duration / dt
    count = round(count_value)
    if count <= 0 or not math.isclose(count_value, count, rel_tol=0.0, abs_tol=1.0e-10):
        raise DriveGroundCouplingError("duration_s must be an integer multiple of step_s")
    state = initial_drive_ground_state(config, powertrain, initial_storage_energy_j=initial_storage_energy_j)
    initial_total = total_drive_ground_accounted_energy_j(config, powertrain, state)
    trace: list[DriveGroundStepEvidence] = []
    max_force = max_utilization = max_slip = max_torque_residual = 0.0
    max_partition = max_energy = max_relative = 0.0
    for index in range(count):
        state, evidence = step_drive_ground(
            config, powertrain, state, throttle=throttle, step_s=dt,
            initial_total_energy_j=initial_total,
        )
        max_force = max(max_force, evidence.total_ground_force_n)
        max_utilization = max(max_utilization, *(item.utilization for item in evidence.contacts))
        max_slip = max(max_slip, *(abs(item.slip_ratio) for item in evidence.contacts))
        max_torque_residual = max(max_torque_residual, abs(evidence.torque_to_force_residual_nm))
        max_partition = max(max_partition, abs(evidence.interface_power_partition_residual_j))
        max_energy = max(max_energy, abs(evidence.global_energy_residual_j))
        max_relative = max(max_relative, evidence.global_relative_energy_residual)
        if index % sample_stride == 0 or index == count - 1 or state.outcome == "DNF":
            trace.append(evidence)
        if state.outcome == "DNF":
            break
    status = "passed"
    reason = "completed" if state.outcome == "running" else state.dnf_reason or "drive_subsystem_failure"
    if max_relative > config.energy_relative_tolerance:
        status, reason = "failed", "global_energy_conservation_residual"
    body = {
        "model_version": MODEL_VERSION,
        "protocol_id": config.protocol_id,
        "status": status,
        "outcome": "finished" if state.outcome == "running" else "DNF",
        "terminal_reason": reason,
        "duration_s": duration,
        "step_s": dt,
        "requested_steps": count,
        "executed_steps": round(state.powertrain.time_s / dt),
        "initial_total_energy_j": initial_total,
        "final_state": asdict(state),
        "maximum_ground_force_n": max_force,
        "maximum_contact_utilization": max_utilization,
        "maximum_slip_ratio": max_slip,
        "maximum_abs_torque_residual_nm": max_torque_residual,
        "maximum_abs_interface_partition_residual_j": max_partition,
        "maximum_abs_global_energy_residual_j": max_energy,
        "maximum_global_relative_energy_residual": max_relative,
        "trace": [asdict(item) for item in trace],
    }
    identity = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    return DriveGroundRunResult(
        MODEL_VERSION, config.protocol_id, status, body["outcome"], reason, duration, dt,
        count, body["executed_steps"], initial_total, state, max_force, max_utilization,
        max_slip, max_torque_residual, max_partition, max_energy, max_relative,
        tuple(trace), identity,
    )


def result_to_mapping(result: DriveGroundRunResult) -> dict[str, Any]:
    return asdict(result)
