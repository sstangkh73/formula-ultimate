"""Work 072 transient suspension and wheel-contact coupling gate."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
import math
from typing import Any, Mapping

from formula_ultimate.topology.functional_vehicle import (
    from_functional_mapping,
    validate_functional_vehicle,
)

from .coupled_planar_differential import (
    CoupledPlanarDifferentialConfig,
    CoupledPlanarDifferentialState,
    CoupledStepEvidence,
    initial_coupled_state,
    step_coupled_planar_differential,
    total_accounted_energy_j as total_coupled_accounted_energy_j,
    with_steer,
)
from .powertrain_dynamics import (
    PowertrainConfig,
    total_accounted_energy_j as total_powertrain_accounted_energy_j,
)


MODEL_VERSION = "transient_suspension_wheel_contact_v1"


class TransientSuspensionError(ValueError):
    """Raised when Work 072 declarations or runtime evidence are invalid."""


def _finite(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TransientSuspensionError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise TransientSuspensionError(f"{name} must be finite")
    return result


def _positive(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result <= 0.0:
        raise TransientSuspensionError(f"{name} must be positive")
    return result


def _nonnegative(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result < 0.0:
        raise TransientSuspensionError(f"{name} must be non-negative")
    return result


def _section(raw: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    value = raw.get(name)
    if not isinstance(value, Mapping):
        raise TransientSuspensionError(f"missing section {name}")
    return value


@dataclass(frozen=True, slots=True)
class TransientSuspensionUnitConfig:
    contact_id: str
    component_id: str
    powered: bool
    effective_mass_kg: float
    static_preload_n: float
    spring_stiffness_n_per_m: float
    damping_ratio: float
    damping_n_s_per_m: float
    maximum_compression_m: float
    maximum_rebound_m: float


@dataclass(frozen=True, slots=True)
class TransientSuspensionConfig:
    protocol_id: str
    coupled: CoupledPlanarDifferentialConfig
    units: tuple[TransientSuspensionUnitConfig, ...]
    force_relative_tolerance: float
    energy_relative_tolerance: float
    global_energy_relative_tolerance: float
    mirror_relative_tolerance: float
    refinement_relative_tolerance: float


@dataclass(frozen=True, slots=True)
class SuspensionContactState:
    contact_id: str
    travel_m: float
    velocity_m_per_s: float


@dataclass(frozen=True, slots=True)
class TransientSuspensionState:
    coupled: CoupledPlanarDifferentialState
    contacts: tuple[SuspensionContactState, ...]
    suspension_boundary_work_j: float
    suspension_damping_heat_j: float
    outcome: str
    suspension_subsystem_state: str
    dnf_reason: str | None
    dnf_time_s: float | None


@dataclass(frozen=True, slots=True)
class SuspensionContactStepEvidence:
    contact_id: str
    component_id: str
    target_normal_load_n: float
    actual_normal_load_n: float
    start_travel_m: float
    end_travel_m: float
    start_velocity_m_per_s: float
    end_velocity_m_per_s: float
    midpoint_travel_m: float
    midpoint_velocity_m_per_s: float
    acceleration_m_per_s2: float
    spring_force_n: float
    damping_force_n: float
    boundary_work_j: float
    damping_heat_j: float
    start_energy_j: float
    end_energy_j: float
    force_residual_n: float
    energy_residual_j: float
    contact_lost: bool
    travel_limit_exceeded: bool


@dataclass(frozen=True, slots=True)
class TransientSuspensionStepEvidence:
    status: str
    reason: str
    time_s: float
    contacts: tuple[SuspensionContactStepEvidence, ...]
    coupled: CoupledStepEvidence
    maximum_target_actual_load_difference_n: float
    maximum_abs_force_residual_n: float
    maximum_abs_energy_residual_j: float
    horizontal_global_energy_residual_j: float
    total_global_energy_residual_j: float
    total_global_relative_energy_residual: float
    committed: bool
    outcome: str
    dnf_reason: str | None


@dataclass(frozen=True, slots=True)
class TransientSuspensionRunResult:
    model_version: str
    protocol_id: str
    status: str
    outcome: str
    terminal_reason: str
    requested_steps: int
    executed_steps: int
    initial_coupled_energy_j: float
    initial_suspension_energy_j: float
    initial_total_energy_j: float
    final_state: TransientSuspensionState
    minimum_actual_normal_load_n: float
    maximum_actual_normal_load_n: float
    maximum_abs_travel_m: float
    maximum_abs_velocity_m_per_s: float
    maximum_target_actual_load_difference_n: float
    maximum_abs_force_residual_n: float
    maximum_abs_suspension_energy_residual_j: float
    maximum_abs_horizontal_energy_residual_j: float
    maximum_abs_total_global_energy_residual_j: float
    maximum_total_global_relative_energy_residual: float
    trace: tuple[TransientSuspensionStepEvidence, ...]
    result_sha256: str


def load_transient_suspension_config(
    raw: Mapping[str, Any],
    *,
    coupled: CoupledPlanarDifferentialConfig,
    architecture_raw: Mapping[str, Any],
) -> TransientSuspensionConfig:
    if raw.get("model_version") != MODEL_VERSION:
        raise TransientSuspensionError("transient suspension model version mismatch")
    protocol_id = raw.get("protocol_id")
    if not isinstance(protocol_id, str) or not protocol_id:
        raise TransientSuspensionError("protocol_id must be a non-empty string")
    source = raw.get("coupled_planar_source")
    if not isinstance(source, str) or not source:
        raise TransientSuspensionError("coupled_planar_source must be a non-empty string")
    profiles = _section(raw, "profiles")
    powered_profile = _section(profiles, "powered_contact")
    passive_profile = _section(profiles, "passive_contact")
    numerical = _section(raw, "numerical")
    force_tolerance = _positive(
        "force_relative_tolerance", numerical.get("force_relative_tolerance")
    )
    energy_tolerance = _positive(
        "energy_relative_tolerance", numerical.get("energy_relative_tolerance")
    )
    global_tolerance = _positive(
        "global_energy_relative_tolerance",
        numerical.get("global_energy_relative_tolerance"),
    )
    mirror_tolerance = _positive(
        "mirror_relative_tolerance", numerical.get("mirror_relative_tolerance")
    )
    refinement_tolerance = _positive(
        "refinement_relative_tolerance",
        numerical.get("refinement_relative_tolerance"),
    )
    if force_tolerance > 1.0e-9 or energy_tolerance > 1.0e-9:
        raise TransientSuspensionError("force or suspension energy tolerance exceeds protocol ceiling")
    if global_tolerance > 1.0e-3:
        raise TransientSuspensionError("global energy tolerance exceeds protocol ceiling")
    if mirror_tolerance > 1.0e-6 or refinement_tolerance > 0.02:
        raise TransientSuspensionError("mirror or refinement tolerance exceeds protocol ceiling")

    vehicle = from_functional_mapping(architecture_raw)
    validate_functional_vehicle(vehicle)
    components = {item.component_id: item for item in vehicle.components}
    units: list[TransientSuspensionUnitConfig] = []
    for contact in coupled.contacts:
        component = components.get(contact.component_id)
        if component is None:
            raise TransientSuspensionError(
                f"contact component {contact.component_id!r} is absent from architecture"
            )
        profile = powered_profile if contact.powered else passive_profile
        stiffness = _positive(
            f"{contact.contact_id}.spring_stiffness_n_per_m",
            profile.get("spring_stiffness_n_per_m"),
        )
        damping_ratio = _nonnegative(
            f"{contact.contact_id}.damping_ratio", profile.get("damping_ratio")
        )
        if damping_ratio > 2.0:
            raise TransientSuspensionError("damping_ratio exceeds the declared domain [0, 2]")
        effective_mass = _positive(
            f"{contact.contact_id}.effective_mass_kg", component.mass_kg
        )
        damping = 2.0 * damping_ratio * math.sqrt(stiffness * effective_mass)
        units.append(
            TransientSuspensionUnitConfig(
                contact.contact_id,
                contact.component_id,
                contact.powered,
                effective_mass,
                contact.baseline_normal_load_n,
                stiffness,
                damping_ratio,
                damping,
                _positive(
                    f"{contact.contact_id}.maximum_compression_m",
                    profile.get("maximum_compression_m"),
                ),
                _positive(
                    f"{contact.contact_id}.maximum_rebound_m",
                    profile.get("maximum_rebound_m"),
                ),
            )
        )
    if tuple(item.contact_id for item in units) != tuple(
        item.contact_id for item in coupled.contacts
    ):
        raise TransientSuspensionError("suspension/contact ordering mismatch")
    return TransientSuspensionConfig(
        protocol_id,
        coupled,
        tuple(units),
        force_tolerance,
        energy_tolerance,
        global_tolerance,
        mirror_tolerance,
        refinement_tolerance,
    )


def with_transient_steer(
    config: TransientSuspensionConfig, steer_angle_rad: float
) -> TransientSuspensionConfig:
    return replace(config, coupled=with_steer(config.coupled, steer_angle_rad))


def with_stiffness_scale(
    config: TransientSuspensionConfig, scale: float
) -> TransientSuspensionConfig:
    factor = _positive("stiffness_scale", scale)
    units = tuple(
        replace(
            unit,
            spring_stiffness_n_per_m=unit.spring_stiffness_n_per_m * factor,
            damping_n_s_per_m=(
                2.0
                * unit.damping_ratio
                * math.sqrt(unit.spring_stiffness_n_per_m * factor * unit.effective_mass_kg)
            ),
        )
        for unit in config.units
    )
    return replace(config, units=units)


def with_damping_scale(
    config: TransientSuspensionConfig, scale: float
) -> TransientSuspensionConfig:
    factor = _nonnegative("damping_scale", scale)
    return replace(
        config,
        units=tuple(
            replace(
                unit,
                damping_ratio=unit.damping_ratio * factor,
                damping_n_s_per_m=unit.damping_n_s_per_m * factor,
            )
            for unit in config.units
        ),
    )


def suspension_contact_energy_j(
    unit: TransientSuspensionUnitConfig, state: SuspensionContactState
) -> float:
    return (
        0.5 * unit.effective_mass_kg * state.velocity_m_per_s**2
        + 0.5 * unit.spring_stiffness_n_per_m * state.travel_m**2
    )


def total_suspension_energy_j(
    config: TransientSuspensionConfig, state: TransientSuspensionState
) -> float:
    return math.fsum(
        suspension_contact_energy_j(unit, contact)
        for unit, contact in zip(config.units, state.contacts)
    )


def conservation_accounted_energy_j(
    config: TransientSuspensionConfig,
    powertrain: PowertrainConfig,
    state: TransientSuspensionState,
) -> float:
    return (
        total_coupled_accounted_energy_j(config.coupled, powertrain, state.coupled)
        + total_suspension_energy_j(config, state)
        + state.suspension_damping_heat_j
        - state.suspension_boundary_work_j
    )


def initial_transient_suspension_state(
    config: TransientSuspensionConfig,
    powertrain: PowertrainConfig,
    *,
    initial_contact_states: Mapping[str, tuple[float, float]] | None = None,
) -> TransientSuspensionState:
    overrides = dict(initial_contact_states or {})
    known = {item.contact_id for item in config.units}
    if set(overrides) - known:
        raise TransientSuspensionError("initial suspension state references an unknown contact")
    contacts: list[SuspensionContactState] = []
    for unit in config.units:
        travel, velocity = overrides.get(unit.contact_id, (0.0, 0.0))
        travel = _finite(f"{unit.contact_id}.initial_travel_m", travel)
        velocity = _finite(f"{unit.contact_id}.initial_velocity_m_per_s", velocity)
        if not -unit.maximum_rebound_m <= travel <= unit.maximum_compression_m:
            raise TransientSuspensionError("initial suspension travel lies outside its declared envelope")
        contacts.append(SuspensionContactState(unit.contact_id, travel, velocity))
    provisional = TransientSuspensionState(
        initial_coupled_state(config.coupled, powertrain),
        tuple(contacts),
        0.0,
        0.0,
        "running",
        "operational",
        None,
        None,
    )
    suspension_energy = total_suspension_energy_j(config, provisional)
    remaining_storage = provisional.coupled.powertrain.storage_energy_j - suspension_energy
    if remaining_storage < 0.0:
        raise TransientSuspensionError("initial storage cannot fund suspension perturbation energy")
    coupled = replace(
        provisional.coupled,
        powertrain=replace(
            provisional.coupled.powertrain, storage_energy_j=remaining_storage
        ),
    )
    result = replace(provisional, coupled=coupled)
    total = conservation_accounted_energy_j(config, powertrain, result)
    scale = max(abs(powertrain.initial_storage_energy_j), 1.0)
    if abs(total - powertrain.initial_storage_energy_j) > 1.0e-12 * scale:
        raise TransientSuspensionError("initial total energy does not match the fixed budget")
    return result


def _advance_contact(
    unit: TransientSuspensionUnitConfig,
    state: SuspensionContactState,
    target_normal_load_n: float,
    dt: float,
) -> tuple[SuspensionContactState, SuspensionContactStepEvidence]:
    target = _finite(f"{unit.contact_id}.target_normal_load_n", target_normal_load_n)
    m = unit.effective_mass_kg
    k = unit.spring_stiffness_n_per_m
    c = unit.damping_n_s_per_m
    x0 = state.travel_m
    v0 = state.velocity_m_per_s
    incremental_target = target - unit.static_preload_n
    denominator = m / dt + k * dt / 4.0 + c / 2.0
    v1 = (
        incremental_target
        - k * x0
        - k * dt * v0 / 4.0
        + m * v0 / dt
        - c * v0 / 2.0
    ) / denominator
    x1 = x0 + 0.5 * dt * (v0 + v1)
    x_mid = 0.5 * (x0 + x1)
    v_mid = 0.5 * (v0 + v1)
    spring_force = k * x_mid
    damping_force = c * v_mid
    actual_load = unit.static_preload_n + spring_force + damping_force
    acceleration = (v1 - v0) / dt
    force_residual = m * acceleration - (target - actual_load)
    start_energy = 0.5 * m * v0**2 + 0.5 * k * x0**2
    end_energy = 0.5 * m * v1**2 + 0.5 * k * x1**2
    boundary_work = incremental_target * (x1 - x0)
    damping_heat = c * v_mid**2 * dt
    energy_residual = end_energy - start_energy - boundary_work + damping_heat
    values = (
        v1,
        x1,
        x_mid,
        v_mid,
        actual_load,
        acceleration,
        force_residual,
        start_energy,
        end_energy,
        boundary_work,
        damping_heat,
        energy_residual,
    )
    if not all(math.isfinite(value) for value in values):
        raise TransientSuspensionError("transient suspension step produced non-finite output")
    end = SuspensionContactState(unit.contact_id, x1, v1)
    evidence = SuspensionContactStepEvidence(
        unit.contact_id,
        unit.component_id,
        target,
        actual_load,
        x0,
        x1,
        v0,
        v1,
        x_mid,
        v_mid,
        acceleration,
        spring_force,
        damping_force,
        boundary_work,
        damping_heat,
        start_energy,
        end_energy,
        force_residual,
        energy_residual,
        actual_load <= 0.0,
        x1 > unit.maximum_compression_m or x1 < -unit.maximum_rebound_m,
    )
    return end, evidence


class _SuspensionLoadTransform:
    def __init__(
        self,
        config: TransientSuspensionConfig,
        contacts: tuple[SuspensionContactState, ...],
        dt: float,
    ) -> None:
        self.config = config
        self.contacts = contacts
        self.dt = dt
        self.last_states: tuple[SuspensionContactState, ...] | None = None
        self.last_evidence: tuple[SuspensionContactStepEvidence, ...] | None = None

    def __call__(self, targets: tuple[float, ...]) -> tuple[float, ...]:
        if len(targets) != len(self.config.units):
            raise TransientSuspensionError("target load count does not match suspension units")
        resolved = tuple(
            _advance_contact(unit, state, target, self.dt)
            for unit, state, target in zip(self.config.units, self.contacts, targets)
        )
        self.last_states = tuple(item[0] for item in resolved)
        self.last_evidence = tuple(item[1] for item in resolved)
        return tuple(item.actual_normal_load_n for item in self.last_evidence)


def step_transient_suspension_coupling(
    config: TransientSuspensionConfig,
    powertrain: PowertrainConfig,
    state: TransientSuspensionState,
    *,
    initial_powertrain_energy_j: float,
    initial_coupled_energy_j: float,
    initial_total_energy_j: float,
    time_step_s: float | None = None,
) -> tuple[TransientSuspensionState, TransientSuspensionStepEvidence]:
    if state.outcome != "running":
        raise TransientSuspensionError("DNF state cannot execute another transient step")
    dt = config.coupled.time_step_s if time_step_s is None else _positive("time_step_s", time_step_s)
    transform = _SuspensionLoadTransform(config, state.contacts, dt)
    coupled_after, coupled_evidence = step_coupled_planar_differential(
        config.coupled,
        powertrain,
        state.coupled,
        initial_powertrain_energy_j=initial_powertrain_energy_j,
        initial_total_energy_j=initial_coupled_energy_j,
        time_step_s=dt,
        normal_load_transform=transform,
    )
    if transform.last_states is None or transform.last_evidence is None:
        raise TransientSuspensionError("suspension transform produced no evidence")
    contact_evidence = transform.last_evidence
    contact_loss = any(item.contact_lost for item in contact_evidence)
    travel_failure = any(item.travel_limit_exceeded for item in contact_evidence)
    committed = not contact_loss
    committed_contacts = transform.last_states if committed else state.contacts
    boundary_increment = (
        math.fsum(item.boundary_work_j for item in contact_evidence) if committed else 0.0
    )
    damping_increment = (
        math.fsum(item.damping_heat_j for item in contact_evidence) if committed else 0.0
    )
    reason: str | None
    if contact_loss:
        reason = "contact_loss"
    elif travel_failure:
        reason = "suspension_travel"
    elif coupled_after.outcome == "DNF":
        reason = coupled_after.dnf_reason
    else:
        reason = None
    outcome = "DNF" if reason else "running"
    failure_time = (
        state.coupled.planar.time_s
        if contact_loss
        else (coupled_after.planar.time_s if reason else None)
    )
    if reason:
        coupled_after = replace(
            coupled_after,
            outcome="DNF",
            drive_subsystem_state="failed",
            dnf_reason=reason,
            dnf_time_s=failure_time,
        )
    candidate = TransientSuspensionState(
        coupled_after,
        committed_contacts,
        state.suspension_boundary_work_j + boundary_increment,
        state.suspension_damping_heat_j + damping_increment,
        outcome,
        "failed" if reason else "operational",
        reason,
        failure_time,
    )
    maximum_force_residual = max(abs(item.force_residual_n) for item in contact_evidence)
    maximum_energy_residual = max(abs(item.energy_residual_j) for item in contact_evidence)
    maximum_difference = max(
        abs(item.target_normal_load_n - item.actual_normal_load_n)
        for item in contact_evidence
    )
    for item in contact_evidence:
        force_scale = max(
            abs(item.target_normal_load_n), abs(item.actual_normal_load_n), 1.0
        )
        energy_scale = max(
            abs(item.start_energy_j),
            abs(item.end_energy_j),
            abs(item.boundary_work_j),
            item.damping_heat_j,
            1.0,
        )
        if abs(item.force_residual_n) > config.force_relative_tolerance * force_scale:
            raise TransientSuspensionError("suspension force residual exceeds tolerance")
        if abs(item.energy_residual_j) > config.energy_relative_tolerance * energy_scale:
            raise TransientSuspensionError("suspension energy residual exceeds tolerance")
    total_residual = initial_total_energy_j - conservation_accounted_energy_j(
        config, powertrain, candidate
    )
    relative = abs(total_residual) / max(abs(initial_total_energy_j), 1.0)
    if relative > config.global_energy_relative_tolerance:
        raise TransientSuspensionError("transient global energy residual exceeds tolerance")
    evidence = TransientSuspensionStepEvidence(
        "physical_failure" if reason else "ok",
        reason or "transient suspension step passed",
        coupled_after.planar.time_s,
        contact_evidence,
        coupled_evidence,
        maximum_difference,
        maximum_force_residual,
        maximum_energy_residual,
        coupled_evidence.global_energy_residual_j,
        total_residual,
        relative,
        committed,
        outcome,
        reason,
    )
    return candidate, evidence


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def run_transient_suspension_coupling(
    config: TransientSuspensionConfig,
    powertrain: PowertrainConfig,
    *,
    time_step_s: float | None = None,
    sample_stride: int = 1,
    initial_contact_states: Mapping[str, tuple[float, float]] | None = None,
) -> TransientSuspensionRunResult:
    dt = config.coupled.time_step_s if time_step_s is None else _positive("time_step_s", time_step_s)
    if not isinstance(sample_stride, int) or isinstance(sample_stride, bool) or sample_stride <= 0:
        raise TransientSuspensionError("sample_stride must be a positive integer")
    count_value = config.coupled.duration_s / dt
    requested_steps = round(count_value)
    if not math.isclose(count_value, requested_steps, rel_tol=0.0, abs_tol=1.0e-10):
        raise TransientSuspensionError("duration must be an integer multiple of time step")
    state = initial_transient_suspension_state(
        config, powertrain, initial_contact_states=initial_contact_states
    )
    initial_powertrain_energy = total_powertrain_accounted_energy_j(
        powertrain, state.coupled.powertrain
    )
    initial_coupled_energy = total_coupled_accounted_energy_j(
        config.coupled, powertrain, state.coupled
    )
    initial_suspension_energy = total_suspension_energy_j(config, state)
    initial_total_energy = conservation_accounted_energy_j(config, powertrain, state)
    trace: list[TransientSuspensionStepEvidence] = []
    minima = math.inf
    maxima = {
        name: 0.0
        for name in (
            "load",
            "travel",
            "velocity",
            "difference",
            "force",
            "suspension_energy",
            "horizontal_energy",
            "global_energy",
            "global_relative",
        )
    }
    executed = 0
    for index in range(requested_steps):
        state, evidence = step_transient_suspension_coupling(
            config,
            powertrain,
            state,
            initial_powertrain_energy_j=initial_powertrain_energy,
            initial_coupled_energy_j=initial_coupled_energy,
            initial_total_energy_j=initial_total_energy,
            time_step_s=dt,
        )
        executed += 1
        actual = tuple(item.actual_normal_load_n for item in evidence.contacts)
        minima = min(minima, *actual)
        maxima["load"] = max(maxima["load"], *actual)
        maxima["travel"] = max(
            maxima["travel"], *(abs(item.end_travel_m) for item in evidence.contacts)
        )
        maxima["velocity"] = max(
            maxima["velocity"],
            *(abs(item.end_velocity_m_per_s) for item in evidence.contacts),
        )
        maxima["difference"] = max(
            maxima["difference"], evidence.maximum_target_actual_load_difference_n
        )
        maxima["force"] = max(maxima["force"], evidence.maximum_abs_force_residual_n)
        maxima["suspension_energy"] = max(
            maxima["suspension_energy"], evidence.maximum_abs_energy_residual_j
        )
        maxima["horizontal_energy"] = max(
            maxima["horizontal_energy"], abs(evidence.horizontal_global_energy_residual_j)
        )
        maxima["global_energy"] = max(
            maxima["global_energy"], abs(evidence.total_global_energy_residual_j)
        )
        maxima["global_relative"] = max(
            maxima["global_relative"], evidence.total_global_relative_energy_residual
        )
        if index % sample_stride == 0 or index == requested_steps - 1 or state.outcome == "DNF":
            trace.append(evidence)
        if state.outcome == "DNF":
            break
    outcome = "finished" if state.outcome == "running" else "DNF"
    terminal = "finished" if outcome == "finished" else str(state.dnf_reason)
    status = "passed" if maxima["global_relative"] <= config.global_energy_relative_tolerance else "failed"
    body = {
        "model_version": MODEL_VERSION,
        "protocol_id": config.protocol_id,
        "status": status,
        "outcome": outcome,
        "terminal_reason": terminal,
        "requested_steps": requested_steps,
        "executed_steps": executed,
        "initial_coupled_energy_j": initial_coupled_energy,
        "initial_suspension_energy_j": initial_suspension_energy,
        "initial_total_energy_j": initial_total_energy,
        "final_state": asdict(state),
        "minimum_actual_normal_load_n": minima,
        "maximum_actual_normal_load_n": maxima["load"],
        "maximum_abs_travel_m": maxima["travel"],
        "maximum_abs_velocity_m_per_s": maxima["velocity"],
        "maximum_target_actual_load_difference_n": maxima["difference"],
        "maximum_abs_force_residual_n": maxima["force"],
        "maximum_abs_suspension_energy_residual_j": maxima["suspension_energy"],
        "maximum_abs_horizontal_energy_residual_j": maxima["horizontal_energy"],
        "maximum_abs_total_global_energy_residual_j": maxima["global_energy"],
        "maximum_total_global_relative_energy_residual": maxima["global_relative"],
        "trace": [asdict(item) for item in trace],
    }
    identity = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    return TransientSuspensionRunResult(
        MODEL_VERSION,
        config.protocol_id,
        status,
        outcome,
        terminal,
        requested_steps,
        executed,
        initial_coupled_energy,
        initial_suspension_energy,
        initial_total_energy,
        state,
        minima,
        maxima["load"],
        maxima["travel"],
        maxima["velocity"],
        maxima["difference"],
        maxima["force"],
        maxima["suspension_energy"],
        maxima["horizontal_energy"],
        maxima["global_energy"],
        maxima["global_relative"],
        tuple(trace),
        identity,
    )


def result_to_mapping(result: TransientSuspensionRunResult) -> dict[str, Any]:
    return asdict(result)
