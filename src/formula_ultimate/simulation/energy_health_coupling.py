"""Work 027 central energy, thermal, health, and event coupling."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
import hashlib
import math
import random

from formula_ultimate.physics.energy_audit import (
    ComponentEnergyBalance,
    ConnectionEnergyTransfer,
    EnergyAuditResult,
    audit_energy_conservation,
)
from formula_ultimate.physics.energy_graph import (
    EnergyConnection,
    EnergyGraph,
    compile_energy_graph,
    converter_component,
    sink_component,
    source_component,
)
from formula_ultimate.physics.thermal import (
    ThermalParameters,
    ThermalState,
    ThermalStepInput,
    ThermalStepResult,
    step_thermal_state,
)

from .aero_load_coupling import AerodynamicCoolingEvidence
from .contact_coupling import (
    ContactEnergyTransfer,
    ContactEnergyTransfers,
    ContactHealthInputs,
)
from .coupling import (
    ComponentHealthState,
    ContactRuntimeState,
    EventCandidate,
    EventDecision,
    ResidualEntry,
    SharedVehicleState,
    arbitrate_event_candidates,
)
from .transaction import AdapterOutput, AdapterReadView, RuntimeSignal


ENERGY_ADAPTER_VERSION = "work027-central-energy-v1"
HEALTH_ADAPTER_VERSION = "work027-central-health-v1"


class EnergyHealthCouplingError(ValueError):
    """Raised when Work 027 declarations or typed evidence are inconsistent."""


def _finite(name: str, value: float) -> None:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
    ):
        raise EnergyHealthCouplingError(f"{name} must be finite")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise EnergyHealthCouplingError(f"{name} must be non-negative")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise EnergyHealthCouplingError(f"{name} must be positive")


_POWER_LIMIT_W = 1.0e30
_DRIVE_GRAPH = compile_energy_graph(EnergyGraph(
    "1.0", "work027-drive-chain",
    (
        source_component("onboard", carrier="electrical", maximum_power_w=_POWER_LIMIT_W),
        converter_component("drive", input_carrier="electrical", output_carrier="mechanical_translational", maximum_input_power_w=_POWER_LIMIT_W, maximum_output_power_w=_POWER_LIMIT_W),
        sink_component("road", carrier="mechanical_translational", maximum_power_w=_POWER_LIMIT_W),
    ),
    (
        EnergyConnection("onboard-drive", "onboard", "power_out", "drive", "power_in"),
        EnergyConnection("drive-road", "drive", "power_out", "road", "power_in"),
    ),
))
_AUX_GRAPH = compile_energy_graph(EnergyGraph(
    "1.0", "work027-aux-chain",
    (
        source_component("onboard", carrier="electrical", maximum_power_w=_POWER_LIMIT_W),
        sink_component("auxiliary", carrier="electrical", maximum_power_w=_POWER_LIMIT_W),
    ),
    (EnergyConnection("onboard-aux", "onboard", "power_out", "auxiliary", "power_in"),),
))
_RECOVERY_GRAPH = compile_energy_graph(EnergyGraph(
    "1.0", "work027-recovery-chain",
    (
        source_component("wheel-braking", carrier="mechanical_rotational", maximum_power_w=_POWER_LIMIT_W),
        converter_component("recovery", input_carrier="mechanical_rotational", output_carrier="electrical", maximum_input_power_w=_POWER_LIMIT_W, maximum_output_power_w=_POWER_LIMIT_W),
        sink_component("recovered-store", carrier="electrical", maximum_power_w=_POWER_LIMIT_W),
    ),
    (
        EnergyConnection("wheel-recovery", "wheel-braking", "power_out", "recovery", "power_in"),
        EnergyConnection("recovery-store", "recovery", "power_out", "recovered-store", "power_in"),
    ),
))


@dataclass(frozen=True, slots=True)
class CentralEnergyConfiguration:
    drive_efficiency: float
    auxiliary_power_w: float
    recovered_capacity_j: float

    def __post_init__(self) -> None:
        _positive("drive_efficiency", self.drive_efficiency)
        if self.drive_efficiency > 1.0:
            raise EnergyHealthCouplingError("drive_efficiency must be <= 1")
        _nonnegative("auxiliary_power_w", self.auxiliary_power_w)
        _positive("recovered_capacity_j", self.recovered_capacity_j)


@dataclass(frozen=True, slots=True)
class CentralEnergyEvidence:
    requested_duration_s: float
    contact_executed_duration_s: float
    executed_duration_s: float
    duration_scale: float
    drive_wheel_energy_j: float
    auxiliary_energy_j: float
    drive_source_energy_j: float
    propulsion_loss_j: float
    recovered_energy_added_j: float
    recovered_energy_used_j: float
    primary_energy_used_j: float
    regeneration_conversion_loss_j: float
    mechanical_brake_heat_j: float
    central_store_residual_j: float
    contact_braking_residual_j: float
    scaled_contact_transfers: ContactEnergyTransfers
    drive_audit: EnergyAuditResult
    auxiliary_audit: EnergyAuditResult
    recovery_audit: EnergyAuditResult
    depletion_event: EventCandidate | None
    residuals: tuple[ResidualEntry, ...]


@dataclass(frozen=True, slots=True)
class CentralEnergyStepResult:
    status: str
    reason: str
    candidate_state: SharedVehicleState | None
    evidence: CentralEnergyEvidence | None
    residuals: tuple[ResidualEntry, ...]
    events: tuple[EventCandidate, ...]


def _scale_contact_transfers(
    transfers: ContactEnergyTransfers, executed_duration_s: float
) -> ContactEnergyTransfers:
    if transfers.executed_duration_s <= 0.0:
        raise EnergyHealthCouplingError("contact executed duration must be positive")
    if not 0.0 <= executed_duration_s <= transfers.executed_duration_s:
        raise EnergyHealthCouplingError("scaled duration lies outside contact duration")
    scale = executed_duration_s / transfers.executed_duration_s
    items = tuple(replace(
        item,
        wheel_energy_removed_j=item.wheel_energy_removed_j * scale,
        recovered_storage_energy_j=item.recovered_storage_energy_j * scale,
        regenerative_conversion_loss_j=item.regenerative_conversion_loss_j * scale,
        mechanical_brake_heat_j=item.mechanical_brake_heat_j * scale,
        drive_wheel_energy_j=item.drive_wheel_energy_j * scale,
    ) for item in transfers.contacts)
    return ContactEnergyTransfers(
        items,
        math.fsum(x.wheel_energy_removed_j for x in items),
        math.fsum(x.recovered_storage_energy_j for x in items),
        math.fsum(x.regenerative_conversion_loss_j for x in items),
        math.fsum(x.mechanical_brake_heat_j for x in items),
        math.fsum(x.drive_wheel_energy_j for x in items),
        transfers.requested_duration_s,
        executed_duration_s,
    )


def _audit_drive(source_j: float, wheel_j: float, loss_j: float) -> EnergyAuditResult:
    return audit_energy_conservation(
        graph=_DRIVE_GRAPH,
        balances=(
            ComponentEnergyBalance("onboard", 0.0, source_j, 0.0, -source_j),
            ComponentEnergyBalance("drive", source_j, wheel_j, loss_j, 0.0),
            ComponentEnergyBalance("road", wheel_j, 0.0, 0.0, wheel_j),
        ),
        transfers=(
            ConnectionEnergyTransfer("onboard-drive", "onboard", "drive", source_j),
            ConnectionEnergyTransfer("drive-road", "drive", "road", wheel_j),
        ),
    )


def _audit_auxiliary(energy_j: float) -> EnergyAuditResult:
    return audit_energy_conservation(
        graph=_AUX_GRAPH,
        balances=(
            ComponentEnergyBalance("onboard", 0.0, energy_j, 0.0, -energy_j),
            ComponentEnergyBalance("auxiliary", energy_j, 0.0, 0.0, energy_j),
        ),
        transfers=(ConnectionEnergyTransfer("onboard-aux", "onboard", "auxiliary", energy_j),),
    )


def _audit_recovery(transfers: ContactEnergyTransfers) -> EnergyAuditResult:
    wheel = transfers.total_wheel_energy_removed_j
    recovered = transfers.total_recovered_storage_energy_j
    loss = transfers.total_conversion_loss_j + transfers.total_mechanical_brake_heat_j
    return audit_energy_conservation(
        graph=_RECOVERY_GRAPH,
        balances=(
            ComponentEnergyBalance("wheel-braking", 0.0, wheel, 0.0, -wheel),
            ComponentEnergyBalance("recovery", wheel, recovered, loss, 0.0),
            ComponentEnergyBalance("recovered-store", recovered, 0.0, 0.0, recovered),
        ),
        transfers=(
            ConnectionEnergyTransfer("wheel-recovery", "wheel-braking", "recovery", wheel),
            ConnectionEnergyTransfer("recovery-store", "recovery", "recovered-store", recovered),
        ),
    )


def evaluate_central_energy(
    *,
    config: CentralEnergyConfiguration,
    transfers: ContactEnergyTransfers,
    state: SharedVehicleState,
    maximum_duration_s: float | None = None,
) -> CentralEnergyStepResult:
    if transfers.requested_duration_s <= 0.0 or transfers.executed_duration_s <= 0.0:
        raise EnergyHealthCouplingError("contact duration evidence must be positive")
    duration = transfers.executed_duration_s
    if maximum_duration_s is not None:
        _nonnegative("maximum_duration_s", maximum_duration_s)
        duration = min(duration, maximum_duration_s)
    base_scale = duration / transfers.executed_duration_s
    full_drive_wheel = transfers.total_drive_wheel_energy_j * base_scale
    full_recovery = transfers.total_recovered_storage_energy_j * base_scale
    full_source = full_drive_wheel / config.drive_efficiency
    full_aux = config.auxiliary_power_w * duration
    demand_rate = (full_source + full_aux) / duration
    recovery_rate = full_recovery / duration
    start_available = state.primary_energy_j + state.recovered_energy_j
    depletion_duration = None
    if demand_rate > recovery_rate:
        crossing = start_available / (demand_rate - recovery_rate)
        if crossing < duration - 1.0e-15:
            depletion_duration = max(0.0, crossing)
            duration = depletion_duration
    scaled = _scale_contact_transfers(transfers, duration)
    drive_wheel = scaled.total_drive_wheel_energy_j
    recovered_added = scaled.total_recovered_storage_energy_j
    drive_source = drive_wheel / config.drive_efficiency
    auxiliary = config.auxiliary_power_w * duration
    demand = drive_source + auxiliary
    recovered_available = state.recovered_energy_j + recovered_added
    recovered_used = min(demand, recovered_available)
    primary_used = demand - recovered_used
    end_recovered = recovered_available - recovered_used
    end_primary = state.primary_energy_j - primary_used
    if end_primary < -1.0e-8:
        raise EnergyHealthCouplingError("depletion localization produced negative primary energy")
    if end_recovered > config.recovered_capacity_j + 1.0e-9:
        raise EnergyHealthCouplingError("recovered energy exceeds central declared capacity")
    end_primary = max(0.0, end_primary)
    propulsion_loss = drive_source - drive_wheel
    store_residual = (
        state.primary_energy_j + state.recovered_energy_j + recovered_added
        - end_primary - end_recovered - demand
    )
    braking_residual = (
        scaled.total_wheel_energy_removed_j
        - scaled.total_recovered_storage_energy_j
        - scaled.total_conversion_loss_j
        - scaled.total_mechanical_brake_heat_j
    )
    drive_audit = _audit_drive(drive_source, drive_wheel, propulsion_loss)
    auxiliary_audit = _audit_auxiliary(auxiliary)
    recovery_audit = _audit_recovery(scaled)
    residuals = (
        ResidualEntry("energy.central-store", "energy", store_residual, "J", 1.0e-8, 1.0e-12, max(1.0, demand)),
        ResidualEntry("energy.contact-braking", "energy", braking_residual, "J", 1.0e-8, 1.0e-12, max(1.0, scaled.total_wheel_energy_removed_j)),
        ResidualEntry("energy.drive-audit", "energy", drive_audit.total_balance_residual_j, "J", 1.0e-8, 1.0e-12, max(1.0, drive_source)),
        ResidualEntry("energy.auxiliary-audit", "energy", auxiliary_audit.total_balance_residual_j, "J", 1.0e-8, 1.0e-12, max(1.0, auxiliary)),
        ResidualEntry("energy.recovery-audit", "energy", recovery_audit.total_balance_residual_j, "J", 1.0e-8, 1.0e-12, max(1.0, scaled.total_wheel_energy_removed_j)),
    )
    audits = (drive_audit, auxiliary_audit, recovery_audit)
    if any(item.status != "valid" for item in audits) or any(not x.passed for x in residuals):
        return CentralEnergyStepResult("invalid", "independent energy audit failed", None, None, residuals, ())
    depletion_event = None
    if depletion_duration is not None:
        depletion_event = EventCandidate("energy.depletion", "energy_depletion", state.time_s + duration, "energy_graph_audit")
    candidate = replace(
        state,
        time_s=state.time_s + duration,
        primary_energy_j=end_primary,
        recovered_energy_j=end_recovered,
        status="depleted" if depletion_event is not None else state.status,
    )
    evidence = CentralEnergyEvidence(
        transfers.requested_duration_s, transfers.executed_duration_s, duration,
        duration / transfers.executed_duration_s, drive_wheel, auxiliary,
        drive_source, propulsion_loss, recovered_added, recovered_used, primary_used,
        scaled.total_conversion_loss_j, scaled.total_mechanical_brake_heat_j,
        store_residual, braking_residual, scaled, drive_audit, auxiliary_audit,
        recovery_audit, depletion_event, residuals,
    )
    return CentralEnergyStepResult(
        "ok", "central energy and independent audits passed", candidate,
        evidence, residuals, (depletion_event,) if depletion_event else (),
    )


@dataclass(frozen=True, slots=True)
class ComponentHealthConfiguration:
    component_id: str
    thermal: ThermalParameters
    base_heat_generation_w: float
    loss_heat_fraction: float
    cooling_fraction: float
    degradation_rate_per_s: float
    degradation_per_heat_j: float
    degradation_limit: float
    damage_rate_per_s: float
    damage_per_heat_j: float
    damage_limit: float
    reliability_base_hazard_per_s: float
    reliability_degradation_coefficient: float = 0.0
    reliability_damage_coefficient: float = 0.0

    def __post_init__(self) -> None:
        if not self.component_id.strip():
            raise EnergyHealthCouplingError("component_id must not be blank")
        for name in (
            "base_heat_generation_w", "loss_heat_fraction", "cooling_fraction",
            "degradation_rate_per_s", "degradation_per_heat_j",
            "damage_rate_per_s", "damage_per_heat_j",
            "reliability_base_hazard_per_s", "reliability_degradation_coefficient",
            "reliability_damage_coefficient",
        ):
            _nonnegative(name, getattr(self, name))
        _positive("degradation_limit", self.degradation_limit)
        _positive("damage_limit", self.damage_limit)


@dataclass(frozen=True, slots=True)
class CentralHealthConfiguration:
    components: tuple[ComponentHealthConfiguration, ...]
    random_seed: int
    step_index: int
    ambient_temperature_k: float
    event_time_tolerance_s: float = 1.0e-12

    def __post_init__(self) -> None:
        if not self.components:
            raise EnergyHealthCouplingError("health configuration requires components")
        ids = tuple(x.component_id for x in self.components)
        if len(ids) != len(set(ids)):
            raise EnergyHealthCouplingError("health component IDs must be unique")
        if not isinstance(self.random_seed, int) or isinstance(self.random_seed, bool):
            raise EnergyHealthCouplingError("random_seed must be an integer")
        if not isinstance(self.step_index, int) or isinstance(self.step_index, bool) or self.step_index < 0:
            raise EnergyHealthCouplingError("step_index must be a non-negative integer")
        _positive("ambient_temperature_k", self.ambient_temperature_k)
        _nonnegative("event_time_tolerance_s", self.event_time_tolerance_s)
        for label in ("loss_heat_fraction", "cooling_fraction"):
            total = math.fsum(getattr(x, label) for x in self.components)
            if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1.0e-12):
                raise EnergyHealthCouplingError(f"{label} values must sum to 1")


@dataclass(frozen=True, slots=True)
class ComponentHealthEvidence:
    component_id: str
    heat_generation_w: float
    thermal_result: ThermalStepResult
    degradation_increment: float
    damage_increment: float
    reliability_hazard_per_s: float
    reliability_draw: float
    reliability_candidate_time_s: float | None
    derating_factor: float


@dataclass(frozen=True, slots=True)
class CentralHealthEvidence:
    requested_duration_s: float
    executed_duration_s: float
    decision: EventDecision | None
    event_candidates: tuple[EventCandidate, ...]
    components: tuple[ComponentHealthEvidence, ...]
    exact_contact_state_count: int
    retained_start_contact_state_count: int
    cooling_conductance_w_per_k: float
    cooling_reference_heat_rejection_w: float
    residuals: tuple[ResidualEntry, ...]


@dataclass(frozen=True, slots=True)
class CentralHealthStepResult:
    status: str
    reason: str
    candidate_state: SharedVehicleState | None
    evidence: CentralHealthEvidence | None
    residuals: tuple[ResidualEntry, ...]
    events: tuple[EventCandidate, ...]


def _component_draw(seed: int, step_index: int, component_id: str) -> float:
    payload = f"{seed}:{step_index}:{component_id}".encode("utf-8")
    stream_seed = int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")
    return random.Random(stream_seed).random()


def _interpolate_motion(
    start: SharedVehicleState, motion: SharedVehicleState, duration_s: float
) -> SharedVehicleState:
    full = motion.time_s - start.time_s
    if full <= 0.0:
        raise EnergyHealthCouplingError("motion candidate must advance time")
    if not 0.0 <= duration_s <= full + 1.0e-12:
        raise EnergyHealthCouplingError("health duration lies outside motion candidate")
    fraction = min(1.0, duration_s / full)
    velocity = tuple(a + (b - a) * fraction for a, b in zip(start.velocity_mps, motion.velocity_mps))
    acceleration = tuple((b - a) / full for a, b in zip(start.velocity_mps, motion.velocity_mps))
    position = tuple(p + v * duration_s + 0.5 * a * duration_s**2 for p, v, a in zip(start.position_m, start.velocity_mps, acceleration))
    yaw_alpha = (motion.yaw_rate_rad_per_s - start.yaw_rate_rad_per_s) / full
    yaw_rate = start.yaw_rate_rad_per_s + yaw_alpha * duration_s
    yaw = start.yaw_rad + start.yaw_rate_rad_per_s * duration_s + 0.5 * yaw_alpha * duration_s**2
    race_distance = start.race_distance_m + (motion.race_distance_m - start.race_distance_m) * fraction
    return replace(start, time_s=start.time_s + duration_s, position_m=position,
        velocity_mps=velocity, yaw_rad=yaw, yaw_rate_rad_per_s=yaw_rate,
        race_distance_m=race_distance)


def evaluate_central_health(
    *,
    health_config: CentralHealthConfiguration,
    energy_config: CentralEnergyConfiguration,
    cooling: AerodynamicCoolingEvidence,
    contact_health: ContactHealthInputs,
    energy: CentralEnergyEvidence,
    state: SharedVehicleState,
    energy_candidate: SharedVehicleState,
    motion_candidate: SharedVehicleState,
) -> CentralHealthStepResult:
    configs = {x.component_id: x for x in health_config.components}
    starts = {x.component_id: x for x in state.components}
    if set(configs) != set(starts):
        raise EnergyHealthCouplingError("health configuration must match shared components exactly")
    if energy_candidate.time_s != state.time_s + energy.executed_duration_s:
        raise EnergyHealthCouplingError("energy candidate time differs from energy evidence")
    requested = min(energy.executed_duration_s, motion_candidate.time_s - state.time_s)
    if requested <= 0.0:
        raise EnergyHealthCouplingError("health requested duration must be positive")
    total_central_loss = energy.propulsion_loss_j + energy.regeneration_conversion_loss_j
    event_candidates = list((energy.depletion_event,) if energy.depletion_event else ())
    preliminary = []
    for config in sorted(health_config.components, key=lambda x: x.component_id):
        start = starts[config.component_id]
        if start.failed:
            event_candidates.append(EventCandidate(f"health.{config.component_id}.latched", "damage_failure", state.time_s, "health_event_solver"))
            continue
        heat_rate = config.base_heat_generation_w + total_central_loss / energy.executed_duration_s * config.loss_heat_fraction
        thermal_parameters = replace(config.thermal, active_conductance_w_per_k=cooling.conductance_w_per_k * config.cooling_fraction)
        thermal = step_thermal_state(parameters=thermal_parameters,
            state=ThermalState(state.time_s, start.temperature_k, start.failed),
            step_input=ThermalStepInput(requested, heat_rate, health_config.ambient_temperature_k, 1.0))
        if thermal.failure_time_s is not None:
            event_candidates.append(EventCandidate(f"health.{config.component_id}.thermal", "thermal_failure", thermal.failure_time_s, "health_event_solver"))
        degradation_rate = config.degradation_rate_per_s + config.degradation_per_heat_j * heat_rate
        damage_rate = config.damage_rate_per_s + config.damage_per_heat_j * heat_rate
        if degradation_rate > 0.0:
            crossing = (config.degradation_limit - start.degradation) / degradation_rate
            if 0.0 <= crossing <= requested:
                event_candidates.append(EventCandidate(f"health.{config.component_id}.degradation", "degradation_failure", state.time_s + crossing, "health_event_solver"))
        if damage_rate > 0.0:
            crossing = (config.damage_limit - start.damage) / damage_rate
            if 0.0 <= crossing <= requested:
                event_candidates.append(EventCandidate(f"health.{config.component_id}.damage", "damage_failure", state.time_s + crossing, "health_event_solver"))
        hazard = config.reliability_base_hazard_per_s * (1.0 + config.reliability_degradation_coefficient * start.degradation + config.reliability_damage_coefficient * start.damage)
        draw = _component_draw(health_config.random_seed, health_config.step_index, config.component_id)
        reliability_time = None if hazard == 0.0 else -math.log1p(-draw) / hazard
        if reliability_time is not None and reliability_time <= requested:
            event_candidates.append(EventCandidate(f"health.{config.component_id}.reliability", "reliability_failure", state.time_s + reliability_time, "health_event_solver"))
        preliminary.append((config, start, heat_rate, degradation_rate, damage_rate, draw, reliability_time))
    for item in contact_health.contacts:
        if item.failure_time_s is not None:
            event_candidates.append(EventCandidate(f"contact.{item.contact_id}.{item.failure_mode}", "damage_failure", item.failure_time_s, "health_event_solver"))
    decision = arbitrate_event_candidates(tuple(event_candidates), time_tolerance_s=health_config.event_time_tolerance_s) if event_candidates else None
    executed = requested if decision is None else max(0.0, decision.earliest_time_s - state.time_s)
    truncated_energy = evaluate_central_energy(config=energy_config,
        transfers=energy.scaled_contact_transfers, state=state,
        maximum_duration_s=executed)
    if truncated_energy.status != "ok":
        return CentralHealthStepResult("invalid", truncated_energy.reason, None, None, truncated_energy.residuals, tuple(event_candidates))
    motion = _interpolate_motion(state, motion_candidate, executed)
    component_states = []
    component_evidence = []
    residuals = list(truncated_energy.residuals)
    for config, start, heat_rate, degradation_rate, damage_rate, draw, reliability_time in preliminary:
        parameters = replace(config.thermal, active_conductance_w_per_k=cooling.conductance_w_per_k * config.cooling_fraction)
        thermal = step_thermal_state(parameters=parameters,
            state=ThermalState(state.time_s, start.temperature_k, start.failed),
            step_input=ThermalStepInput(max(executed, 1.0e-15), heat_rate, health_config.ambient_temperature_k, 1.0))
        degradation_increment = degradation_rate * executed
        damage_increment = damage_rate * executed
        failed_ids = set(decision.tied_candidate_ids if decision else ())
        failed = any(x.startswith(f"health.{config.component_id}.") for x in failed_ids)
        component_states.append(ComponentHealthState(config.component_id,
            thermal.end_state.temperature_k, start.degradation + degradation_increment,
            start.damage + damage_increment, failed))
        component_evidence.append(ComponentHealthEvidence(config.component_id,
            heat_rate, thermal, degradation_increment, damage_increment,
            config.reliability_base_hazard_per_s * (1.0 + config.reliability_degradation_coefficient * start.degradation + config.reliability_damage_coefficient * start.damage),
            draw, None if reliability_time is None else state.time_s + reliability_time,
            thermal.end_derating_factor))
        residuals.append(ResidualEntry(f"health.{config.component_id}.thermal-energy",
            "energy", thermal.energy_residual_j, "J", 1.0e-8, 1.0e-12,
            max(1.0, thermal.heat_generated_j)))
    exact_contacts = []
    retained = 0
    health_by_id = {x.contact_id: x for x in contact_health.contacts}
    for start_contact in state.contacts:
        item = health_by_id.get(start_contact.contact_id)
        if item is None:
            raise EnergyHealthCouplingError("contact health IDs must match shared contacts")
        if math.isclose(item.end_state.time_s, state.time_s + executed, rel_tol=0.0, abs_tol=1.0e-10):
            end = item.end_state
            exact_contacts.append(replace(start_contact,
                suspension_travel_m=end.suspension_travel_m,
                suspension_velocity_m_per_s=end.suspension_velocity_m_per_s,
                brake_temperature_k=end.brake_temperature_k,
                stored_recovered_energy_j=end.stored_recovered_energy_j,
                suspension_failed=end.suspension_failed,
                brake_failed=end.brake_failed))
        else:
            exact_contacts.append(start_contact)
            retained += 1
    status = state.status
    if decision is not None:
        status = "depleted" if decision.winner.event_type == "energy_depletion" else "failed"
    energy_state = truncated_energy.candidate_state
    candidate = replace(motion,
        primary_energy_j=energy_state.primary_energy_j,
        recovered_energy_j=energy_state.recovered_energy_j,
        contacts=tuple(exact_contacts), components=tuple(component_states), status=status)
    residuals.append(ResidualEntry("health.common-event-time", "time",
        candidate.time_s - (state.time_s + executed), "s", 1.0e-12, 1.0e-12,
        max(1.0, candidate.time_s)))
    evidence = CentralHealthEvidence(requested, executed, decision,
        tuple(sorted(event_candidates, key=lambda x:(x.time_s,x.event_id))),
        tuple(component_evidence), len(exact_contacts)-retained, retained,
        cooling.conductance_w_per_k, cooling.heat_rejection_w, tuple(residuals))
    if any(not x.passed for x in residuals):
        return CentralHealthStepResult("invalid", "health residual failed", None, evidence, tuple(residuals), tuple(event_candidates))
    return CentralHealthStepResult("ok", "central health and earliest-event coupling passed",
        candidate, evidence, tuple(residuals), tuple(event_candidates))


@dataclass(frozen=True, slots=True)
class CentralEnergyAuditAdapter:
    config: CentralEnergyConfiguration
    module_id: str = field(default="energy_graph_audit", init=False)
    model_version: str = field(default=ENERGY_ADAPTER_VERSION, init=False)

    def execute(self, view: AdapterReadView) -> AdapterOutput:
        transfers = view.read("contact.energy_transfers")
        state = view.read("state.current")
        if not isinstance(transfers, ContactEnergyTransfers) or not isinstance(state, SharedVehicleState):
            return AdapterOutput(self.module_id, "invalid", (), reason="central energy payload types are invalid")
        try:
            result = evaluate_central_energy(config=self.config, transfers=transfers, state=state)
        except (ArithmeticError, ValueError) as exc:
            return AdapterOutput(self.module_id, "invalid", (), reason=str(exc))
        if result.status != "ok":
            return AdapterOutput(self.module_id, "invalid", (), residuals=result.residuals, events=result.events, reason=result.reason)
        return AdapterOutput(self.module_id, "ok", (
            RuntimeSignal("energy.residuals", result.evidence),
            RuntimeSignal("state.energy_candidate", result.candidate_state),
        ), residuals=result.residuals, events=result.events)


@dataclass(frozen=True, slots=True)
class CentralHealthEventAdapter:
    health_config: CentralHealthConfiguration
    energy_config: CentralEnergyConfiguration
    module_id: str = field(default="health_event_solver", init=False)
    model_version: str = field(default=HEALTH_ADAPTER_VERSION, init=False)

    def execute(self, view: AdapterReadView) -> AdapterOutput:
        cooling=view.read("aero.cooling_evidence"); contact=view.read("contact.health_inputs")
        energy=view.read("energy.residuals"); state=view.read("state.current")
        energy_state=view.read("state.energy_candidate"); motion=view.read("state.motion_candidate")
        if not isinstance(cooling,AerodynamicCoolingEvidence) or not isinstance(contact,ContactHealthInputs) or not isinstance(energy,CentralEnergyEvidence) or not isinstance(state,SharedVehicleState) or not isinstance(energy_state,SharedVehicleState) or not isinstance(motion,SharedVehicleState):
            return AdapterOutput(self.module_id,"invalid",(),reason="central health payload types are invalid")
        try:
            result=evaluate_central_health(health_config=self.health_config,
                energy_config=self.energy_config,cooling=cooling,contact_health=contact,
                energy=energy,state=state,energy_candidate=energy_state,
                motion_candidate=motion)
        except (ArithmeticError,ValueError) as exc:
            return AdapterOutput(self.module_id,"invalid",(),reason=str(exc))
        if result.status!="ok":
            own_events=tuple(x for x in result.events if x.source_module_id==self.module_id)
            return AdapterOutput(self.module_id,"invalid",(),residuals=result.residuals,events=own_events,reason=result.reason)
        own_events=tuple(x for x in result.events if x.source_module_id==self.module_id)
        return AdapterOutput(self.module_id,"ok",(
            RuntimeSignal("health.event_candidates",result.evidence),
            RuntimeSignal("health.residuals",result.evidence),
            RuntimeSignal("state.health_candidate",result.candidate_state),
        ),residuals=result.residuals,events=own_events)
