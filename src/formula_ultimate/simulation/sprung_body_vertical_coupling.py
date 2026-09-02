"""Work 073 sprung-body, tyre-vertical, and deterministic road coupling."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
import math
from typing import Any, Mapping

from formula_ultimate.topology.functional_vehicle import (
    from_functional_mapping,
    functional_mass_properties,
    validate_functional_vehicle,
)

from .coupled_planar_differential import (
    CoupledPlanarDifferentialState,
    CoupledStepEvidence,
    initial_coupled_state,
    step_coupled_planar_differential,
    total_accounted_energy_j as total_coupled_accounted_energy_j,
)
from .powertrain_dynamics import (
    PowertrainConfig,
    total_accounted_energy_j as total_powertrain_accounted_energy_j,
)
from .transient_suspension_coupling import (
    TransientSuspensionConfig,
    with_transient_steer,
)


MODEL_VERSION = "sprung_body_road_tyre_vertical_v1"


class SprungBodyVerticalError(ValueError):
    """Raised when Work 073 declaration or runtime evidence is invalid."""


def _finite(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SprungBodyVerticalError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise SprungBodyVerticalError(f"{name} must be finite")
    return result


def _positive(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result <= 0.0:
        raise SprungBodyVerticalError(f"{name} must be positive")
    return result


def _nonnegative(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result < 0.0:
        raise SprungBodyVerticalError(f"{name} must be non-negative")
    return result


def _section(raw: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    result = raw.get(name)
    if not isinstance(result, Mapping):
        raise SprungBodyVerticalError(f"missing section {name}")
    return result


@dataclass(frozen=True, slots=True)
class VerticalContactConfig:
    contact_id: str
    component_id: str
    powered: bool
    x_position_m: float
    y_position_m: float
    static_preload_n: float
    unsprung_mass_kg: float
    suspension_stiffness_n_per_m: float
    suspension_damping_n_s_per_m: float
    tyre_stiffness_n_per_m: float
    tyre_damping_ratio: float
    tyre_damping_n_s_per_m: float
    maximum_compression_m: float
    maximum_rebound_m: float


@dataclass(frozen=True, slots=True)
class SprungBodyVerticalConfig:
    protocol_id: str
    transient: TransientSuspensionConfig
    sprung_mass_kg: float
    sprung_roll_inertia_kg_m2: float
    sprung_pitch_inertia_kg_m2: float
    contacts: tuple[VerticalContactConfig, ...]
    force_relative_tolerance: float
    energy_relative_tolerance: float
    global_energy_relative_tolerance: float
    mirror_relative_tolerance: float
    refinement_relative_tolerance: float


@dataclass(frozen=True, slots=True)
class RaisedCosineRoadProfile:
    contact_id: str
    amplitude_m: float
    start_time_s: float
    duration_s: float
    shape: str = "bump"

    def __post_init__(self) -> None:
        if not isinstance(self.contact_id, str) or not self.contact_id:
            raise SprungBodyVerticalError("road profile contact_id must be non-empty")
        _finite("road amplitude_m", self.amplitude_m)
        _nonnegative("road start_time_s", self.start_time_s)
        _positive("road duration_s", self.duration_s)
        if self.shape not in {"bump", "ramp_hold"}:
            raise SprungBodyVerticalError("road profile shape must be bump or ramp_hold")


@dataclass(frozen=True, slots=True)
class SprungBodyVerticalState:
    coupled: CoupledPlanarDifferentialState
    coordinates: tuple[float, ...]
    velocities: tuple[float, ...]
    suspension_damping_heat_j: float
    tyre_damping_heat_j: float
    inertial_work_j: float
    road_work_j: float
    outcome: str
    vertical_subsystem_state: str
    dnf_reason: str | None
    dnf_time_s: float | None


@dataclass(frozen=True, slots=True)
class VerticalContactEvidence:
    contact_id: str
    road_start_m: float
    road_end_m: float
    road_velocity_m_per_s: float
    suspension_start_m: float
    suspension_end_m: float
    suspension_midpoint_m: float
    tyre_start_m: float
    tyre_end_m: float
    tyre_midpoint_m: float
    suspension_force_n: float
    tyre_force_n: float
    actual_normal_load_n: float
    suspension_damping_heat_j: float
    tyre_damping_heat_j: float
    road_work_j: float
    contact_lost: bool
    travel_limit_exceeded: bool


@dataclass(frozen=True, slots=True)
class SprungBodyVerticalStepEvidence:
    status: str
    reason: str
    time_s: float
    body_heave_m: float
    body_pitch_rad: float
    body_roll_rad: float
    contacts: tuple[VerticalContactEvidence, ...]
    coupled: CoupledStepEvidence
    maximum_abs_equation_residual: float
    vertical_energy_residual_j: float
    horizontal_energy_residual_j: float
    total_global_energy_residual_j: float
    total_global_relative_energy_residual: float
    committed: bool
    outcome: str
    dnf_reason: str | None


@dataclass(frozen=True, slots=True)
class SprungBodyVerticalRunResult:
    model_version: str
    protocol_id: str
    status: str
    outcome: str
    terminal_reason: str
    requested_steps: int
    executed_steps: int
    initial_coupled_energy_j: float
    initial_vertical_energy_j: float
    initial_total_energy_j: float
    final_state: SprungBodyVerticalState
    minimum_actual_normal_load_n: float
    maximum_actual_normal_load_n: float
    maximum_abs_heave_m: float
    maximum_abs_pitch_rad: float
    maximum_abs_roll_rad: float
    maximum_abs_suspension_travel_m: float
    maximum_abs_equation_residual: float
    maximum_abs_vertical_energy_residual_j: float
    maximum_abs_total_global_energy_residual_j: float
    maximum_total_global_relative_energy_residual: float
    trace: tuple[SprungBodyVerticalStepEvidence, ...]
    result_sha256: str


def load_sprung_body_vertical_config(
    raw: Mapping[str, Any],
    *,
    transient: TransientSuspensionConfig,
    architecture_raw: Mapping[str, Any],
) -> SprungBodyVerticalConfig:
    if raw.get("model_version") != MODEL_VERSION:
        raise SprungBodyVerticalError("sprung-body vertical model version mismatch")
    protocol = raw.get("protocol_id")
    if not isinstance(protocol, str) or not protocol:
        raise SprungBodyVerticalError("protocol_id must be non-empty")
    if not isinstance(raw.get("transient_suspension_source"), str):
        raise SprungBodyVerticalError("transient_suspension_source must be declared")
    profiles = _section(raw, "tyre_vertical_profiles")
    powered_profile = _section(profiles, "powered_contact")
    passive_profile = _section(profiles, "passive_contact")
    numerical = _section(raw, "numerical")
    force_tolerance = _positive("force_relative_tolerance", numerical.get("force_relative_tolerance"))
    energy_tolerance = _positive("energy_relative_tolerance", numerical.get("energy_relative_tolerance"))
    global_tolerance = _positive("global_energy_relative_tolerance", numerical.get("global_energy_relative_tolerance"))
    mirror_tolerance = _positive("mirror_relative_tolerance", numerical.get("mirror_relative_tolerance"))
    refinement_tolerance = _positive("refinement_relative_tolerance", numerical.get("refinement_relative_tolerance"))
    if force_tolerance > 1.0e-9 or energy_tolerance > 1.0e-9:
        raise SprungBodyVerticalError("force or vertical energy tolerance exceeds protocol ceiling")
    if global_tolerance > 1.0e-3 or mirror_tolerance > 1.0e-6 or refinement_tolerance > 0.02:
        raise SprungBodyVerticalError("global, mirror, or refinement tolerance exceeds protocol ceiling")

    vehicle = from_functional_mapping(architecture_raw)
    validate_functional_vehicle(vehicle)
    properties = functional_mass_properties(vehicle)
    components = {item.component_id: item for item in vehicle.components}
    ground_components = {item.component_id for item in transient.units}
    sprung_components = tuple(item for item in vehicle.components if item.component_id not in ground_components)
    sprung_mass = math.fsum(item.mass_kg for item in sprung_components)
    centre = properties["centre_of_mass_m"]
    sprung_inertia = [0.0, 0.0]
    for component in sprung_components:
        dx, dy, dz = (component.position_m[index] - centre[index] for index in range(3))
        centroidal = component.centroidal_inertia_kg_m2
        sprung_inertia[0] += centroidal[0] + component.mass_kg * (dy * dy + dz * dz)
        sprung_inertia[1] += centroidal[1] + component.mass_kg * (dx * dx + dz * dz)
    mass_closure = sprung_mass + math.fsum(item.effective_mass_kg for item in transient.units)
    tolerance = transient.coupled.geometry_relative_tolerance
    if abs(mass_closure - transient.coupled.vehicle_mass_kg) > tolerance * max(mass_closure, 1.0):
        raise SprungBodyVerticalError("sprung plus unsprung mass does not close vehicle mass")
    contacts: list[VerticalContactConfig] = []
    coupled_contacts = {item.contact_id: item for item in transient.coupled.contacts}
    for unit in transient.units:
        contact = coupled_contacts[unit.contact_id]
        component = components.get(unit.component_id)
        if component is None or abs(component.mass_kg - unit.effective_mass_kg) > tolerance * max(component.mass_kg, 1.0):
            raise SprungBodyVerticalError("unsprung component identity or mass mismatch")
        profile = powered_profile if unit.powered else passive_profile
        tyre_stiffness = _positive(f"{unit.contact_id}.tyre_stiffness", profile.get("stiffness_n_per_m"))
        tyre_ratio = _nonnegative(f"{unit.contact_id}.tyre_damping_ratio", profile.get("damping_ratio"))
        if tyre_ratio > 2.0:
            raise SprungBodyVerticalError("tyre damping ratio exceeds [0, 2]")
        tyre_damping = 2.0 * tyre_ratio * math.sqrt(tyre_stiffness * unit.effective_mass_kg)
        contacts.append(VerticalContactConfig(
            unit.contact_id, unit.component_id, unit.powered,
            contact.x_position_m, contact.y_position_m, unit.static_preload_n,
            unit.effective_mass_kg, unit.spring_stiffness_n_per_m,
            unit.damping_n_s_per_m, tyre_stiffness, tyre_ratio, tyre_damping,
            unit.maximum_compression_m, unit.maximum_rebound_m,
        ))
    return SprungBodyVerticalConfig(
        protocol, transient, _positive("sprung_mass_kg", sprung_mass),
        _positive("sprung_roll_inertia", sprung_inertia[0]),
        _positive("sprung_pitch_inertia", sprung_inertia[1]), tuple(contacts),
        force_tolerance, energy_tolerance, global_tolerance,
        mirror_tolerance, refinement_tolerance,
    )


def with_vertical_steer(config: SprungBodyVerticalConfig, steer: float) -> SprungBodyVerticalConfig:
    return replace(config, transient=with_transient_steer(config.transient, steer))


def with_tyre_stiffness_scale(config: SprungBodyVerticalConfig, scale: float) -> SprungBodyVerticalConfig:
    factor = _positive("tyre_stiffness_scale", scale)
    contacts = tuple(replace(
        item,
        tyre_stiffness_n_per_m=item.tyre_stiffness_n_per_m * factor,
        tyre_damping_n_s_per_m=2.0 * item.tyre_damping_ratio * math.sqrt(
            item.tyre_stiffness_n_per_m * factor * item.unsprung_mass_kg
        ),
    ) for item in config.contacts)
    return replace(config, contacts=contacts)


def with_tyre_damping_scale(config: SprungBodyVerticalConfig, scale: float) -> SprungBodyVerticalConfig:
    factor = _nonnegative("tyre_damping_scale", scale)
    return replace(config, contacts=tuple(replace(
        item, tyre_damping_ratio=item.tyre_damping_ratio * factor,
        tyre_damping_n_s_per_m=item.tyre_damping_n_s_per_m * factor,
    ) for item in config.contacts))


def road_displacement_m(profile: RaisedCosineRoadProfile, time_s: float) -> float:
    time = _nonnegative("road query time_s", time_s)
    if time <= profile.start_time_s:
        return 0.0
    if time >= profile.start_time_s + profile.duration_s:
        return profile.amplitude_m if profile.shape == "ramp_hold" else 0.0
    phase = (time - profile.start_time_s) / profile.duration_s
    angle = math.pi * phase if profile.shape == "ramp_hold" else 2.0 * math.pi * phase
    return 0.5 * profile.amplitude_m * (1.0 - math.cos(angle))


def _road_values(
    contacts: tuple[VerticalContactConfig, ...], profiles: tuple[RaisedCosineRoadProfile, ...],
    start_time: float, dt: float,
) -> tuple[tuple[float, ...], tuple[float, ...]]:
    known = {item.contact_id for item in contacts}
    if len({item.contact_id for item in profiles}) != len(profiles) or any(item.contact_id not in known for item in profiles):
        raise SprungBodyVerticalError("road profiles contain duplicate or unknown contacts")
    by_contact = {item.contact_id: item for item in profiles}
    start = tuple(road_displacement_m(by_contact[item.contact_id], start_time) if item.contact_id in by_contact else 0.0 for item in contacts)
    end = tuple(road_displacement_m(by_contact[item.contact_id], start_time + dt) if item.contact_id in by_contact else 0.0 for item in contacts)
    return start, end


def _zeros(size: int) -> list[list[float]]:
    return [[0.0 for _ in range(size)] for _ in range(size)]


def _outer_add(matrix: list[list[float]], vector: tuple[float, ...], scale: float) -> None:
    for row in range(len(vector)):
        for column in range(len(vector)):
            matrix[row][column] += scale * vector[row] * vector[column]


def _matvec(matrix: list[list[float]], vector: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(math.fsum(value * vector[column] for column, value in enumerate(row)) for row in matrix)


def _solve(matrix: list[list[float]], vector: tuple[float, ...]) -> tuple[float, ...]:
    size = len(vector)
    augmented = [list(matrix[row]) + [vector[row]] for row in range(size)]
    scale = max(abs(value) for row in matrix for value in row)
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) <= 1.0e-14 * max(scale, 1.0):
            raise SprungBodyVerticalError("vertical implicit matrix is singular")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        for index in range(column, size + 1):
            augmented[column][index] /= divisor
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            for index in range(column, size + 1):
                augmented[row][index] -= factor * augmented[column][index]
    result = tuple(augmented[row][-1] for row in range(size))
    if not all(math.isfinite(item) for item in result):
        raise SprungBodyVerticalError("vertical solve produced non-finite state")
    return result


def _matrices(config: SprungBodyVerticalConfig) -> tuple[tuple[float, ...], list[list[float]], list[list[float]]]:
    size = 3 + len(config.contacts)
    masses = (config.sprung_mass_kg, config.sprung_pitch_inertia_kg_m2, config.sprung_roll_inertia_kg_m2) + tuple(item.unsprung_mass_kg for item in config.contacts)
    stiffness, damping = _zeros(size), _zeros(size)
    for index, item in enumerate(config.contacts):
        a = tuple([-1.0, item.x_position_m, -item.y_position_m] + [1.0 if j == index else 0.0 for j in range(len(config.contacts))])
        _outer_add(stiffness, a, item.suspension_stiffness_n_per_m)
        _outer_add(damping, a, item.suspension_damping_n_s_per_m)
        stiffness[3 + index][3 + index] += item.tyre_stiffness_n_per_m
        damping[3 + index][3 + index] += item.tyre_damping_n_s_per_m
    return masses, stiffness, damping


def _body_point(q: tuple[float, ...], item: VerticalContactConfig) -> float:
    return q[0] - item.x_position_m * q[1] + item.y_position_m * q[2]


def _vertical_energy(
    config: SprungBodyVerticalConfig, q: tuple[float, ...], v: tuple[float, ...], road: tuple[float, ...],
) -> float:
    masses, _, _ = _matrices(config)
    kinetic = 0.5 * math.fsum(mass * speed * speed for mass, speed in zip(masses, v))
    suspension = tyre = 0.0
    for index, item in enumerate(config.contacts):
        travel = q[3 + index] - _body_point(q, item)
        compression = road[index] - q[3 + index]
        suspension += 0.5 * item.suspension_stiffness_n_per_m * travel * travel
        tyre += 0.5 * item.tyre_stiffness_n_per_m * compression * compression
    return kinetic + suspension + tyre


def conservation_accounted_energy_j(
    config: SprungBodyVerticalConfig, powertrain: PowertrainConfig,
    state: SprungBodyVerticalState, road: tuple[float, ...],
) -> float:
    return (
        total_coupled_accounted_energy_j(config.transient.coupled, powertrain, state.coupled)
        + _vertical_energy(config, state.coordinates, state.velocities, road)
        + state.suspension_damping_heat_j + state.tyre_damping_heat_j
        - state.inertial_work_j - state.road_work_j
    )


def initial_sprung_body_vertical_state(
    config: SprungBodyVerticalConfig, powertrain: PowertrainConfig,
    *, coordinates: tuple[float, ...] | None = None, velocities: tuple[float, ...] | None = None,
) -> SprungBodyVerticalState:
    size = 3 + len(config.contacts)
    q = tuple(0.0 for _ in range(size)) if coordinates is None else tuple(_finite("initial coordinate", item) for item in coordinates)
    v = tuple(0.0 for _ in range(size)) if velocities is None else tuple(_finite("initial velocity", item) for item in velocities)
    if len(q) != size or len(v) != size:
        raise SprungBodyVerticalError("initial vertical state has wrong dimension")
    for item in config.contacts:
        travel = q[3 + config.contacts.index(item)] - _body_point(q, item)
        if not -item.maximum_rebound_m <= travel <= item.maximum_compression_m:
            raise SprungBodyVerticalError("initial suspension travel lies outside its envelope")
    coupled = initial_coupled_state(config.transient.coupled, powertrain)
    vertical_energy = _vertical_energy(config, q, v, tuple(0.0 for _ in config.contacts))
    remaining = coupled.powertrain.storage_energy_j - vertical_energy
    if remaining < 0.0:
        raise SprungBodyVerticalError("storage cannot fund initial vertical energy")
    coupled = replace(coupled, powertrain=replace(coupled.powertrain, storage_energy_j=remaining))
    return SprungBodyVerticalState(coupled, q, v, 0.0, 0.0, 0.0, 0.0, "running", "operational", None, None)


@dataclass(frozen=True, slots=True)
class _VerticalCandidate:
    coordinates: tuple[float, ...]
    velocities: tuple[float, ...]
    contacts: tuple[VerticalContactEvidence, ...]
    maximum_residual: float
    energy_residual_j: float
    suspension_heat_j: float
    tyre_heat_j: float
    inertial_work_j: float
    road_work_j: float


def _advance_vertical(
    config: SprungBodyVerticalConfig, state: SprungBodyVerticalState,
    targets: tuple[float, ...], road_start: tuple[float, ...], road_end: tuple[float, ...], dt: float,
) -> _VerticalCandidate:
    size = len(state.coordinates)
    masses, stiffness, damping = _matrices(config)
    road_mid = tuple(0.5 * (left + right) for left, right in zip(road_start, road_end))
    road_velocity = tuple((right - left) / dt for left, right in zip(road_start, road_end))
    moment_x = math.fsum(item.x_position_m * load for item, load in zip(config.contacts, targets))
    moment_y = math.fsum(item.y_position_m * load for item, load in zip(config.contacts, targets))
    force = [0.0] * size
    force[1] = moment_x
    force[2] = -moment_y
    for index, item in enumerate(config.contacts):
        force[3 + index] += item.tyre_stiffness_n_per_m * road_mid[index] + item.tyre_damping_n_s_per_m * road_velocity[index]
    q0, v0 = state.coordinates, state.velocities
    matrix = _zeros(size)
    rhs = [0.0] * size
    kv0 = _matvec(stiffness, v0)
    kq0 = _matvec(stiffness, q0)
    cv0 = _matvec(damping, v0)
    for row in range(size):
        for column in range(size):
            matrix[row][column] = damping[row][column] / 2.0 + stiffness[row][column] * dt / 4.0
        matrix[row][row] += masses[row] / dt
        rhs[row] = force[row] + masses[row] * v0[row] / dt - cv0[row] / 2.0 - kq0[row] - kv0[row] * dt / 4.0
    v1 = _solve(matrix, tuple(rhs))
    q1 = tuple(q0[index] + 0.5 * dt * (v0[index] + v1[index]) for index in range(size))
    qmid = tuple(0.5 * (q0[index] + q1[index]) for index in range(size))
    vmid = tuple(0.5 * (v0[index] + v1[index]) for index in range(size))
    acceleration = tuple((v1[index] - v0[index]) / dt for index in range(size))
    damping_force = _matvec(damping, vmid)
    stiffness_force = _matvec(stiffness, qmid)
    residual = tuple(
        masses[row] * acceleration[row] + damping_force[row] + stiffness_force[row] - force[row]
        for row in range(size)
    )
    evidence: list[VerticalContactEvidence] = []
    suspension_heat = tyre_heat = road_work = 0.0
    for index, item in enumerate(config.contacts):
        body0, body1, bodymid = _body_point(q0, item), _body_point(q1, item), _body_point(qmid, item)
        bodyv_mid = vmid[0] - item.x_position_m * vmid[1] + item.y_position_m * vmid[2]
        s0, s1, smid = q0[3 + index] - body0, q1[3 + index] - body1, qmid[3 + index] - bodymid
        svelocity = vmid[3 + index] - bodyv_mid
        t0, t1, tmid = road_start[index] - q0[3 + index], road_end[index] - q1[3 + index], road_mid[index] - qmid[3 + index]
        tvelocity = road_velocity[index] - vmid[3 + index]
        suspension_force = item.suspension_stiffness_n_per_m * smid + item.suspension_damping_n_s_per_m * svelocity
        tyre_force = item.tyre_stiffness_n_per_m * tmid + item.tyre_damping_n_s_per_m * tvelocity
        actual = item.static_preload_n + tyre_force
        suspension_loss = item.suspension_damping_n_s_per_m * svelocity * svelocity * dt
        tyre_loss = item.tyre_damping_n_s_per_m * tvelocity * tvelocity * dt
        road_input = tyre_force * (road_end[index] - road_start[index])
        suspension_heat += suspension_loss
        tyre_heat += tyre_loss
        road_work += road_input
        evidence.append(VerticalContactEvidence(
            item.contact_id, road_start[index], road_end[index], road_velocity[index],
            s0, s1, smid, t0, t1, tmid, suspension_force, tyre_force, actual,
            suspension_loss, tyre_loss, road_input, actual <= 0.0,
            s1 > item.maximum_compression_m or s1 < -item.maximum_rebound_m,
        ))
    inertial_work = force[1] * (q1[1] - q0[1]) + force[2] * (q1[2] - q0[2])
    start_energy = _vertical_energy(config, q0, v0, road_start)
    end_energy = _vertical_energy(config, q1, v1, road_end)
    energy_residual = end_energy - start_energy + suspension_heat + tyre_heat - inertial_work - road_work
    return _VerticalCandidate(q1, v1, tuple(evidence), max(abs(item) for item in residual), energy_residual, suspension_heat, tyre_heat, inertial_work, road_work)


class _VerticalTransform:
    def __init__(self, config: SprungBodyVerticalConfig, state: SprungBodyVerticalState, profiles: tuple[RaisedCosineRoadProfile, ...], dt: float) -> None:
        self.config, self.state, self.dt = config, state, dt
        self.road_start, self.road_end = _road_values(config.contacts, profiles, state.coupled.planar.time_s, dt)
        self.last: _VerticalCandidate | None = None

    def __call__(self, targets: tuple[float, ...]) -> tuple[float, ...]:
        self.last = _advance_vertical(self.config, self.state, targets, self.road_start, self.road_end, self.dt)
        return tuple(item.actual_normal_load_n for item in self.last.contacts)


def step_sprung_body_vertical_coupling(
    config: SprungBodyVerticalConfig, powertrain: PowertrainConfig, state: SprungBodyVerticalState,
    *, initial_powertrain_energy_j: float, initial_coupled_energy_j: float,
    initial_total_energy_j: float, road_profiles: tuple[RaisedCosineRoadProfile, ...] = (),
    time_step_s: float | None = None,
) -> tuple[SprungBodyVerticalState, SprungBodyVerticalStepEvidence]:
    if state.outcome != "running":
        raise SprungBodyVerticalError("DNF state cannot execute another vertical step")
    dt = config.transient.coupled.time_step_s if time_step_s is None else _positive("time_step_s", time_step_s)
    transform = _VerticalTransform(config, state, road_profiles, dt)
    coupled_after, coupled_evidence = step_coupled_planar_differential(
        config.transient.coupled, powertrain, state.coupled,
        initial_powertrain_energy_j=initial_powertrain_energy_j,
        initial_total_energy_j=initial_coupled_energy_j, time_step_s=dt,
        normal_load_transform=transform,
    )
    candidate = transform.last
    if candidate is None:
        raise SprungBodyVerticalError("vertical transform produced no evidence")
    force_scale = max(*(abs(item.actual_normal_load_n) for item in candidate.contacts), 1.0)
    energy_scale = max(abs(_vertical_energy(config, state.coordinates, state.velocities, transform.road_start)), abs(_vertical_energy(config, candidate.coordinates, candidate.velocities, transform.road_end)), abs(candidate.inertial_work_j), abs(candidate.road_work_j), candidate.suspension_heat_j + candidate.tyre_heat_j, 1.0)
    if candidate.maximum_residual > config.force_relative_tolerance * force_scale:
        raise SprungBodyVerticalError("vertical generalized-force residual exceeds tolerance")
    if abs(candidate.energy_residual_j) > config.energy_relative_tolerance * energy_scale:
        raise SprungBodyVerticalError("vertical energy residual exceeds tolerance")
    contact_loss = any(item.contact_lost for item in candidate.contacts)
    travel_failure = any(item.travel_limit_exceeded for item in candidate.contacts)
    committed = not contact_loss
    reason = "contact_loss" if contact_loss else "suspension_travel" if travel_failure else coupled_after.dnf_reason if coupled_after.outcome == "DNF" else None
    if reason:
        failure_time = state.coupled.planar.time_s if contact_loss else coupled_after.planar.time_s
        coupled_after = replace(coupled_after, outcome="DNF", drive_subsystem_state="failed", dnf_reason=reason, dnf_time_s=failure_time)
    else:
        failure_time = None
    result = SprungBodyVerticalState(
        coupled_after,
        candidate.coordinates if committed else state.coordinates,
        candidate.velocities if committed else state.velocities,
        state.suspension_damping_heat_j + (candidate.suspension_heat_j if committed else 0.0),
        state.tyre_damping_heat_j + (candidate.tyre_heat_j if committed else 0.0),
        state.inertial_work_j + (candidate.inertial_work_j if committed else 0.0),
        state.road_work_j + (candidate.road_work_j if committed else 0.0),
        "DNF" if reason else "running", "failed" if reason else "operational", reason, failure_time,
    )
    road_for_result = transform.road_end if committed else transform.road_start
    total_residual = initial_total_energy_j - conservation_accounted_energy_j(config, powertrain, result, road_for_result)
    relative = abs(total_residual) / max(abs(initial_total_energy_j), 1.0)
    if relative > config.global_energy_relative_tolerance:
        raise SprungBodyVerticalError("combined global energy residual exceeds tolerance")
    evidence = SprungBodyVerticalStepEvidence(
        "physical_failure" if reason else "ok", reason or "sprung-body vertical step passed",
        coupled_after.planar.time_s, candidate.coordinates[0], candidate.coordinates[1], candidate.coordinates[2],
        candidate.contacts, coupled_evidence, candidate.maximum_residual, candidate.energy_residual_j,
        coupled_evidence.global_energy_residual_j, total_residual, relative, committed,
        "DNF" if reason else "running", reason,
    )
    return result, evidence


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def run_sprung_body_vertical_coupling(
    config: SprungBodyVerticalConfig, powertrain: PowertrainConfig,
    *, road_profiles: tuple[RaisedCosineRoadProfile, ...] = (),
    time_step_s: float | None = None, sample_stride: int = 1,
    initial_coordinates: tuple[float, ...] | None = None,
    initial_velocities: tuple[float, ...] | None = None,
) -> SprungBodyVerticalRunResult:
    dt = config.transient.coupled.time_step_s if time_step_s is None else _positive("time_step_s", time_step_s)
    if not isinstance(sample_stride, int) or isinstance(sample_stride, bool) or sample_stride <= 0:
        raise SprungBodyVerticalError("sample_stride must be a positive integer")
    count_value = config.transient.coupled.duration_s / dt
    steps = round(count_value)
    if not math.isclose(count_value, steps, rel_tol=0.0, abs_tol=1.0e-10):
        raise SprungBodyVerticalError("duration must be an integer multiple of time step")
    state = initial_sprung_body_vertical_state(
        config, powertrain, coordinates=initial_coordinates, velocities=initial_velocities
    )
    initial_powertrain = total_powertrain_accounted_energy_j(powertrain, state.coupled.powertrain)
    initial_coupled = total_coupled_accounted_energy_j(config.transient.coupled, powertrain, state.coupled)
    zero_road = tuple(0.0 for _ in config.contacts)
    initial_vertical = _vertical_energy(config, state.coordinates, state.velocities, zero_road)
    initial_total = conservation_accounted_energy_j(config, powertrain, state, zero_road)
    trace: list[SprungBodyVerticalStepEvidence] = []
    minimum, maximum = math.inf, 0.0
    maxima = {key: 0.0 for key in ("heave", "pitch", "roll", "travel", "equation", "vertical_energy", "global", "relative")}
    executed = 0
    for index in range(steps):
        state, evidence = step_sprung_body_vertical_coupling(
            config, powertrain, state, initial_powertrain_energy_j=initial_powertrain,
            initial_coupled_energy_j=initial_coupled, initial_total_energy_j=initial_total,
            road_profiles=road_profiles, time_step_s=dt,
        )
        executed += 1
        loads = tuple(item.actual_normal_load_n for item in evidence.contacts)
        minimum, maximum = min(minimum, *loads), max(maximum, *loads)
        maxima["heave"] = max(maxima["heave"], abs(evidence.body_heave_m))
        maxima["pitch"] = max(maxima["pitch"], abs(evidence.body_pitch_rad))
        maxima["roll"] = max(maxima["roll"], abs(evidence.body_roll_rad))
        maxima["travel"] = max(maxima["travel"], *(abs(item.suspension_end_m) for item in evidence.contacts))
        maxima["equation"] = max(maxima["equation"], evidence.maximum_abs_equation_residual)
        maxima["vertical_energy"] = max(maxima["vertical_energy"], abs(evidence.vertical_energy_residual_j))
        maxima["global"] = max(maxima["global"], abs(evidence.total_global_energy_residual_j))
        maxima["relative"] = max(maxima["relative"], evidence.total_global_relative_energy_residual)
        if index % sample_stride == 0 or index == steps - 1 or state.outcome == "DNF":
            trace.append(evidence)
        if state.outcome == "DNF":
            break
    outcome = "finished" if state.outcome == "running" else "DNF"
    terminal = "finished" if outcome == "finished" else str(state.dnf_reason)
    status = "passed" if maxima["relative"] <= config.global_energy_relative_tolerance else "failed"
    body = {
        "model_version": MODEL_VERSION, "protocol_id": config.protocol_id, "status": status,
        "outcome": outcome, "terminal_reason": terminal, "requested_steps": steps,
        "executed_steps": executed, "initial_coupled_energy_j": initial_coupled,
        "initial_vertical_energy_j": initial_vertical, "initial_total_energy_j": initial_total,
        "final_state": asdict(state), "minimum_actual_normal_load_n": minimum,
        "maximum_actual_normal_load_n": maximum, "maximum_abs_heave_m": maxima["heave"],
        "maximum_abs_pitch_rad": maxima["pitch"], "maximum_abs_roll_rad": maxima["roll"],
        "maximum_abs_suspension_travel_m": maxima["travel"],
        "maximum_abs_equation_residual": maxima["equation"],
        "maximum_abs_vertical_energy_residual_j": maxima["vertical_energy"],
        "maximum_abs_total_global_energy_residual_j": maxima["global"],
        "maximum_total_global_relative_energy_residual": maxima["relative"],
        "trace": [asdict(item) for item in trace],
    }
    identity = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    return SprungBodyVerticalRunResult(
        MODEL_VERSION, config.protocol_id, status, outcome, terminal, steps, executed,
        initial_coupled, initial_vertical, initial_total, state, minimum, maximum,
        maxima["heave"], maxima["pitch"], maxima["roll"], maxima["travel"],
        maxima["equation"], maxima["vertical_energy"], maxima["global"], maxima["relative"],
        tuple(trace), identity,
    )


def result_to_mapping(result: SprungBodyVerticalRunResult) -> dict[str, Any]:
    return asdict(result)
