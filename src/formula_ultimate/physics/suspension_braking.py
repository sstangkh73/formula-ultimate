"""Deterministic Level-0 suspension, braking, and regeneration interval model."""

from __future__ import annotations

from dataclasses import dataclass
import math

from .thermal import (
    ThermalInputError,
    ThermalNumericalError,
    ThermalParameters,
    ThermalState,
    ThermalStepInput,
    ThermalStepResult,
    step_thermal_state,
    thermal_derating_factor,
)


MODEL_VERSION = "work018-suspension-braking-v1"


class SuspensionBrakeInputError(ValueError):
    """Raised when a suspension/brake declaration violates its SI contract."""


def _finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise SuspensionBrakeInputError(
            f"{name} must be finite; received {value!r}"
        )


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise SuspensionBrakeInputError(f"{name} must be > 0; received {value!r}")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise SuspensionBrakeInputError(
            f"{name} must be >= 0; received {value!r}"
        )


@dataclass(frozen=True, slots=True)
class SuspensionParameters:
    effective_mass_kg: float
    spring_stiffness_n_per_m: float
    damping_n_s_per_m: float
    preload_n: float
    maximum_compression_m: float
    maximum_rebound_m: float

    def __post_init__(self) -> None:
        _positive("effective_mass_kg", self.effective_mass_kg)
        _positive("spring_stiffness_n_per_m", self.spring_stiffness_n_per_m)
        _nonnegative("damping_n_s_per_m", self.damping_n_s_per_m)
        _nonnegative("preload_n", self.preload_n)
        _positive("maximum_compression_m", self.maximum_compression_m)
        _positive("maximum_rebound_m", self.maximum_rebound_m)


@dataclass(frozen=True, slots=True)
class BrakeParameters:
    effective_radius_m: float
    tyre_friction_coefficient: float
    maximum_mechanical_torque_n_m: float
    thermal_parameters: ThermalParameters

    def __post_init__(self) -> None:
        _positive("effective_radius_m", self.effective_radius_m)
        _nonnegative("tyre_friction_coefficient", self.tyre_friction_coefficient)
        _nonnegative(
            "maximum_mechanical_torque_n_m",
            self.maximum_mechanical_torque_n_m,
        )
        if not isinstance(self.thermal_parameters, ThermalParameters):
            raise SuspensionBrakeInputError(
                "thermal_parameters must be a ThermalParameters instance"
            )


@dataclass(frozen=True, slots=True)
class RegenerationParameters:
    maximum_regen_torque_n_m: float
    maximum_generator_input_power_w: float
    maximum_storage_charge_power_w: float
    storage_capacity_j: float
    conversion_efficiency: float
    minimum_regen_speed_rad_per_s: float = 0.0

    def __post_init__(self) -> None:
        _nonnegative(
            "maximum_regen_torque_n_m", self.maximum_regen_torque_n_m
        )
        _nonnegative(
            "maximum_generator_input_power_w",
            self.maximum_generator_input_power_w,
        )
        _nonnegative(
            "maximum_storage_charge_power_w",
            self.maximum_storage_charge_power_w,
        )
        _positive("storage_capacity_j", self.storage_capacity_j)
        _positive("conversion_efficiency", self.conversion_efficiency)
        if self.conversion_efficiency > 1.0:
            raise SuspensionBrakeInputError("conversion_efficiency must be <= 1")
        _nonnegative(
            "minimum_regen_speed_rad_per_s",
            self.minimum_regen_speed_rad_per_s,
        )


@dataclass(frozen=True, slots=True)
class SuspensionBrakeModule:
    module_id: str
    suspension: SuspensionParameters
    brake: BrakeParameters
    regeneration: RegenerationParameters

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, str) or not self.module_id.strip():
            raise SuspensionBrakeInputError("module_id must be a non-empty string")
        if not isinstance(self.suspension, SuspensionParameters):
            raise SuspensionBrakeInputError(
                "suspension must be a SuspensionParameters instance"
            )
        if not isinstance(self.brake, BrakeParameters):
            raise SuspensionBrakeInputError(
                "brake must be a BrakeParameters instance"
            )
        if not isinstance(self.regeneration, RegenerationParameters):
            raise SuspensionBrakeInputError(
                "regeneration must be a RegenerationParameters instance"
            )


@dataclass(frozen=True, slots=True)
class SuspensionBrakeState:
    time_s: float
    suspension_travel_m: float
    suspension_velocity_m_per_s: float
    brake_temperature_k: float
    stored_recovered_energy_j: float
    suspension_failed: bool = False
    brake_failed: bool = False

    def __post_init__(self) -> None:
        _nonnegative("time_s", self.time_s)
        _finite("suspension_travel_m", self.suspension_travel_m)
        _finite(
            "suspension_velocity_m_per_s",
            self.suspension_velocity_m_per_s,
        )
        _positive("brake_temperature_k", self.brake_temperature_k)
        _nonnegative(
            "stored_recovered_energy_j",
            self.stored_recovered_energy_j,
        )
        if not isinstance(self.suspension_failed, bool):
            raise SuspensionBrakeInputError("suspension_failed must be a boolean")
        if not isinstance(self.brake_failed, bool):
            raise SuspensionBrakeInputError("brake_failed must be a boolean")


@dataclass(frozen=True, slots=True)
class SuspensionBrakeStepInput:
    duration_s: float
    normal_load_n: float
    wheel_angular_speed_rad_per_s: float
    requested_brake_torque_n_m: float
    ambient_temperature_k: float
    active_cooling_command: float = 0.0

    def __post_init__(self) -> None:
        _positive("duration_s", self.duration_s)
        _nonnegative("normal_load_n", self.normal_load_n)
        _nonnegative(
            "wheel_angular_speed_rad_per_s",
            self.wheel_angular_speed_rad_per_s,
        )
        _nonnegative(
            "requested_brake_torque_n_m",
            self.requested_brake_torque_n_m,
        )
        _positive("ambient_temperature_k", self.ambient_temperature_k)
        _finite("active_cooling_command", self.active_cooling_command)
        if not 0.0 <= self.active_cooling_command <= 1.0:
            raise SuspensionBrakeInputError(
                "active_cooling_command must be in [0, 1]"
            )


@dataclass(frozen=True, slots=True)
class SuspensionBrakeResiduals:
    suspension_force_n: float
    brake_torque_n_m: float
    brake_energy_j: float
    storage_capacity_margin_j: float


@dataclass(frozen=True, slots=True)
class SuspensionBrakeStepResult:
    model_version: str
    status: str
    reason: str
    module_id: str
    start_state: SuspensionBrakeState
    end_state: SuspensionBrakeState
    requested_duration_s: float
    executed_duration_s: float
    unexecuted_duration_s: float
    failure_mode: str
    failure_time_s: float | None
    normal_load_n: float
    suspension_force_n: float | None
    suspension_acceleration_m_per_s2: float | None
    tyre_torque_limit_n_m: float | None
    regen_torque_limit_by_component_n_m: float | None
    regen_torque_limit_by_generator_power_n_m: float | None
    regen_torque_limit_by_charge_power_n_m: float | None
    regen_torque_limit_by_storage_capacity_n_m: float | None
    available_regen_torque_n_m: float | None
    available_mechanical_torque_n_m: float | None
    allocated_regen_torque_n_m: float | None
    allocated_mechanical_torque_n_m: float | None
    tyre_limit_scale: float | None
    applied_regen_torque_n_m: float | None
    applied_mechanical_torque_n_m: float | None
    applied_total_brake_torque_n_m: float | None
    unserved_brake_torque_n_m: float | None
    wheel_energy_removed_j: float | None
    regenerative_wheel_energy_j: float | None
    recovered_storage_energy_j: float | None
    regenerative_conversion_loss_j: float | None
    mechanical_brake_heat_j: float | None
    thermal_result: ThermalStepResult | None
    residuals: SuspensionBrakeResiduals | None


def _invalid_result(
    *,
    module: SuspensionBrakeModule,
    state: SuspensionBrakeState,
    step_input: SuspensionBrakeStepInput,
    reason: str,
) -> SuspensionBrakeStepResult:
    return SuspensionBrakeStepResult(
        model_version=MODEL_VERSION,
        status="invalid",
        reason=reason,
        module_id=module.module_id,
        start_state=state,
        end_state=state,
        requested_duration_s=step_input.duration_s,
        executed_duration_s=0.0,
        unexecuted_duration_s=step_input.duration_s,
        failure_mode="none",
        failure_time_s=None,
        normal_load_n=step_input.normal_load_n,
        suspension_force_n=None,
        suspension_acceleration_m_per_s2=None,
        tyre_torque_limit_n_m=None,
        regen_torque_limit_by_component_n_m=None,
        regen_torque_limit_by_generator_power_n_m=None,
        regen_torque_limit_by_charge_power_n_m=None,
        regen_torque_limit_by_storage_capacity_n_m=None,
        available_regen_torque_n_m=None,
        available_mechanical_torque_n_m=None,
        allocated_regen_torque_n_m=None,
        allocated_mechanical_torque_n_m=None,
        tyre_limit_scale=None,
        applied_regen_torque_n_m=None,
        applied_mechanical_torque_n_m=None,
        applied_total_brake_torque_n_m=None,
        unserved_brake_torque_n_m=None,
        wheel_energy_removed_j=None,
        regenerative_wheel_energy_j=None,
        recovered_storage_energy_j=None,
        regenerative_conversion_loss_j=None,
        mechanical_brake_heat_j=None,
        thermal_result=None,
        residuals=None,
    )


def _travel_at(
    start_travel_m: float,
    start_velocity_m_per_s: float,
    acceleration_m_per_s2: float,
    duration_s: float,
) -> tuple[float, float]:
    travel = (
        start_travel_m
        + start_velocity_m_per_s * duration_s
        + 0.5 * acceleration_m_per_s2 * duration_s**2
    )
    velocity = start_velocity_m_per_s + acceleration_m_per_s2 * duration_s
    return travel, velocity


def _positive_roots(
    *,
    start_travel_m: float,
    start_velocity_m_per_s: float,
    acceleration_m_per_s2: float,
    boundary_m: float,
) -> tuple[float, ...]:
    constant = start_travel_m - boundary_m
    if acceleration_m_per_s2 == 0.0:
        if start_velocity_m_per_s == 0.0:
            return ()
        root = -constant / start_velocity_m_per_s
        return (root,) if root >= 0.0 and math.isfinite(root) else ()
    discriminant = (
        start_velocity_m_per_s**2
        - 2.0 * acceleration_m_per_s2 * constant
    )
    if not math.isfinite(discriminant) or discriminant < 0.0:
        return ()
    square_root = math.sqrt(discriminant)
    roots = (
        (-start_velocity_m_per_s - square_root) / acceleration_m_per_s2,
        (-start_velocity_m_per_s + square_root) / acceleration_m_per_s2,
    )
    return tuple(
        sorted(root for root in roots if root >= 0.0 and math.isfinite(root))
    )


def _suspension_failure_candidate(
    *,
    parameters: SuspensionParameters,
    state: SuspensionBrakeState,
    acceleration_m_per_s2: float,
    duration_s: float,
) -> tuple[float, str] | None:
    lower = -parameters.maximum_rebound_m
    upper = parameters.maximum_compression_m
    position = state.suspension_travel_m
    velocity = state.suspension_velocity_m_per_s
    if position < lower or position > upper:
        return (0.0, "state_outside_travel_envelope")
    candidates: list[tuple[float, str]] = []
    for boundary, label, direction in (
        (upper, "maximum_compression", 1.0),
        (lower, "maximum_rebound", -1.0),
    ):
        for root in _positive_roots(
            start_travel_m=position,
            start_velocity_m_per_s=velocity,
            acceleration_m_per_s2=acceleration_m_per_s2,
            boundary_m=boundary,
        ):
            if root > duration_s:
                continue
            crossing_velocity = velocity + acceleration_m_per_s2 * root
            outward = direction * crossing_velocity > 0.0
            if root == 0.0 and crossing_velocity == 0.0:
                outward = direction * acceleration_m_per_s2 > 0.0
            if outward:
                candidates.append((root, label))
                break
    return min(candidates, default=None, key=lambda item: (item[0], item[1]))


def _regen_torque_limits(
    *,
    module: SuspensionBrakeModule,
    state: SuspensionBrakeState,
    step_input: SuspensionBrakeStepInput,
) -> tuple[float, float, float, float, float]:
    regen = module.regeneration
    omega = step_input.wheel_angular_speed_rad_per_s
    component_limit = regen.maximum_regen_torque_n_m
    if omega == 0.0 or omega < regen.minimum_regen_speed_rad_per_s:
        return component_limit, 0.0, 0.0, 0.0, 0.0
    generator_limit = regen.maximum_generator_input_power_w / omega
    charge_limit = (
        regen.maximum_storage_charge_power_w
        / (regen.conversion_efficiency * omega)
    )
    remaining_capacity = regen.storage_capacity_j - state.stored_recovered_energy_j
    storage_limit = (
        remaining_capacity
        / (
            regen.conversion_efficiency
            * omega
            * step_input.duration_s
        )
    )
    available = min(component_limit, generator_limit, charge_limit, storage_limit)
    return component_limit, generator_limit, charge_limit, storage_limit, available


def evaluate_suspension_brake_step(
    *,
    module: SuspensionBrakeModule,
    state: SuspensionBrakeState,
    step_input: SuspensionBrakeStepInput,
) -> SuspensionBrakeStepResult:
    """Evaluate one contact interval with deterministic event truncation."""

    regen = module.regeneration
    suspension = module.suspension
    brake = module.brake
    if state.stored_recovered_energy_j > regen.storage_capacity_j:
        raise SuspensionBrakeInputError(
            "stored_recovered_energy_j exceeds declared storage_capacity_j"
        )
    lower = -suspension.maximum_rebound_m
    upper = suspension.maximum_compression_m
    if not lower <= state.suspension_travel_m <= upper:
        raise SuspensionBrakeInputError(
            "suspension_travel_m is outside declared travel limits"
        )

    if state.suspension_failed or state.brake_failed:
        end_state = SuspensionBrakeState(
            state.time_s,
            state.suspension_travel_m,
            state.suspension_velocity_m_per_s,
            state.brake_temperature_k,
            state.stored_recovered_energy_j,
            state.suspension_failed,
            state.brake_failed,
        )
        return SuspensionBrakeStepResult(
            model_version=MODEL_VERSION,
            status="failed",
            reason="module entered the interval with a latched failure",
            module_id=module.module_id,
            start_state=state,
            end_state=end_state,
            requested_duration_s=step_input.duration_s,
            executed_duration_s=0.0,
            unexecuted_duration_s=step_input.duration_s,
            failure_mode="already_failed",
            failure_time_s=state.time_s,
            normal_load_n=step_input.normal_load_n,
            suspension_force_n=None,
            suspension_acceleration_m_per_s2=None,
            tyre_torque_limit_n_m=None,
            regen_torque_limit_by_component_n_m=None,
            regen_torque_limit_by_generator_power_n_m=None,
            regen_torque_limit_by_charge_power_n_m=None,
            regen_torque_limit_by_storage_capacity_n_m=None,
            available_regen_torque_n_m=None,
            available_mechanical_torque_n_m=None,
            allocated_regen_torque_n_m=None,
            allocated_mechanical_torque_n_m=None,
            tyre_limit_scale=None,
            applied_regen_torque_n_m=None,
            applied_mechanical_torque_n_m=None,
            applied_total_brake_torque_n_m=None,
            unserved_brake_torque_n_m=None,
            wheel_energy_removed_j=None,
            regenerative_wheel_energy_j=None,
            recovered_storage_energy_j=None,
            regenerative_conversion_loss_j=None,
            mechanical_brake_heat_j=None,
            thermal_result=None,
            residuals=None,
        )

    try:
        suspension_force = (
            suspension.preload_n
            + suspension.spring_stiffness_n_per_m * state.suspension_travel_m
            + suspension.damping_n_s_per_m
            * state.suspension_velocity_m_per_s
        )
        suspension_acceleration = (
            step_input.normal_load_n - suspension_force
        ) / suspension.effective_mass_kg
        tyre_torque_limit = (
            brake.tyre_friction_coefficient
            * step_input.normal_load_n
            * brake.effective_radius_m
        )
        (
            regen_component_limit,
            regen_generator_limit,
            regen_charge_limit,
            regen_storage_limit,
            available_regen,
        ) = _regen_torque_limits(module=module, state=state, step_input=step_input)
        derating = thermal_derating_factor(
            brake.thermal_parameters,
            state.brake_temperature_k,
        )
        available_mechanical = brake.maximum_mechanical_torque_n_m * derating
        allocated_regen = min(
            step_input.requested_brake_torque_n_m,
            available_regen,
        )
        allocated_mechanical = min(
            step_input.requested_brake_torque_n_m - allocated_regen,
            available_mechanical,
        )
        total_allocated = allocated_regen + allocated_mechanical
        tyre_scale = (
            1.0
            if total_allocated == 0.0
            else min(1.0, tyre_torque_limit / total_allocated)
        )
        applied_regen = allocated_regen * tyre_scale
        applied_mechanical = allocated_mechanical * tyre_scale
        applied_total = applied_regen + applied_mechanical
        unserved_torque = step_input.requested_brake_torque_n_m - applied_total
        mechanical_heat_power = (
            applied_mechanical * step_input.wheel_angular_speed_rad_per_s
        )
        values = (
            suspension_force,
            suspension_acceleration,
            tyre_torque_limit,
            regen_component_limit,
            regen_generator_limit,
            regen_charge_limit,
            regen_storage_limit,
            available_regen,
            available_mechanical,
            allocated_regen,
            allocated_mechanical,
            tyre_scale,
            applied_regen,
            applied_mechanical,
            applied_total,
            unserved_torque,
            mechanical_heat_power,
        )
        if not all(math.isfinite(value) for value in values):
            return _invalid_result(
                module=module,
                state=state,
                step_input=step_input,
                reason="suspension or torque allocation produced non-finite output",
            )
        suspension_candidate = _suspension_failure_candidate(
            parameters=suspension,
            state=state,
            acceleration_m_per_s2=suspension_acceleration,
            duration_s=step_input.duration_s,
        )
        thermal_candidate = step_thermal_state(
            parameters=brake.thermal_parameters,
            state=ThermalState(
                state.time_s,
                state.brake_temperature_k,
                state.brake_failed,
            ),
            step_input=ThermalStepInput(
                duration_s=step_input.duration_s,
                heat_generation_w=mechanical_heat_power,
                ambient_temperature_k=step_input.ambient_temperature_k,
                active_cooling_command=step_input.active_cooling_command,
            ),
        )
    except (
        ArithmeticError,
        OverflowError,
        ThermalInputError,
        ThermalNumericalError,
        ValueError,
    ) as exc:
        return _invalid_result(
            module=module,
            state=state,
            step_input=step_input,
            reason=f"runtime suspension/brake evaluation failed: {exc}",
        )

    brake_candidate_time = (
        thermal_candidate.executed_duration_s
        if thermal_candidate.status in {"failed", "failed_at_start", "already_failed"}
        else None
    )
    suspension_time = suspension_candidate[0] if suspension_candidate else None
    candidate_times = tuple(
        value for value in (suspension_time, brake_candidate_time) if value is not None
    )
    if not candidate_times:
        executed_duration = step_input.duration_s
        failure_mode = "none"
    else:
        executed_duration = min(candidate_times)
        suspension_at_event = suspension_time == executed_duration
        brake_at_event = brake_candidate_time == executed_duration
        if suspension_at_event and brake_at_event:
            failure_mode = "simultaneous"
        elif suspension_at_event:
            failure_mode = "suspension_travel"
        else:
            failure_mode = "brake_overtemperature"

    try:
        end_travel, end_suspension_velocity = _travel_at(
            state.suspension_travel_m,
            state.suspension_velocity_m_per_s,
            suspension_acceleration,
            executed_duration,
        )
        if executed_duration == thermal_candidate.executed_duration_s:
            thermal_result = thermal_candidate
        elif executed_duration > 0.0:
            thermal_result = step_thermal_state(
                parameters=brake.thermal_parameters,
                state=ThermalState(
                    state.time_s,
                    state.brake_temperature_k,
                    state.brake_failed,
                ),
                step_input=ThermalStepInput(
                    duration_s=executed_duration,
                    heat_generation_w=mechanical_heat_power,
                    ambient_temperature_k=step_input.ambient_temperature_k,
                    active_cooling_command=step_input.active_cooling_command,
                ),
            )
        else:
            thermal_result = None
        omega = step_input.wheel_angular_speed_rad_per_s
        regen_wheel_energy = applied_regen * omega * executed_duration
        recovered_energy = regen.conversion_efficiency * regen_wheel_energy
        regen_loss = regen_wheel_energy - recovered_energy
        mechanical_heat = applied_mechanical * omega * executed_duration
        removed_energy = (applied_regen + applied_mechanical) * omega * executed_duration
        end_stored_energy = state.stored_recovered_energy_j + recovered_energy
        energy_residual = (
            removed_energy - recovered_energy - regen_loss - mechanical_heat
        )
        suspension_residual = (
            suspension.effective_mass_kg * suspension_acceleration
            - (step_input.normal_load_n - suspension_force)
        )
        torque_residual = (
            step_input.requested_brake_torque_n_m
            - applied_total
            - unserved_torque
        )
        storage_margin = regen.storage_capacity_j - end_stored_energy
        result_values = (
            end_travel,
            end_suspension_velocity,
            regen_wheel_energy,
            recovered_energy,
            regen_loss,
            mechanical_heat,
            removed_energy,
            end_stored_energy,
            energy_residual,
            suspension_residual,
            torque_residual,
            storage_margin,
        )
        if not all(math.isfinite(value) for value in result_values):
            return _invalid_result(
                module=module,
                state=state,
                step_input=step_input,
                reason="event integration or energy accounting produced non-finite output",
            )
        if storage_margin < -1.0e-9:
            return _invalid_result(
                module=module,
                state=state,
                step_input=step_input,
                reason=f"recovered storage exceeded capacity by {-storage_margin!r} J",
            )
        if abs(energy_residual) > 1.0e-6:
            return _invalid_result(
                module=module,
                state=state,
                step_input=step_input,
                reason=f"brake energy residual {energy_residual!r} J exceeded tolerance",
            )
    except (ArithmeticError, OverflowError, ThermalNumericalError, ValueError) as exc:
        return _invalid_result(
            module=module,
            state=state,
            step_input=step_input,
            reason=f"runtime event integration failed: {exc}",
        )

    suspension_failed = failure_mode in {"suspension_travel", "simultaneous"}
    brake_failed = (
        failure_mode in {"brake_overtemperature", "simultaneous"}
        or (thermal_result.end_state.failed if thermal_result else False)
    )
    end_temperature = (
        thermal_result.end_state.temperature_k
        if thermal_result
        else state.brake_temperature_k
    )
    end_state = SuspensionBrakeState(
        time_s=state.time_s + executed_duration,
        suspension_travel_m=end_travel,
        suspension_velocity_m_per_s=end_suspension_velocity,
        brake_temperature_k=end_temperature,
        stored_recovered_energy_j=end_stored_energy,
        suspension_failed=suspension_failed,
        brake_failed=brake_failed,
    )
    failure_time = (
        state.time_s + executed_duration if failure_mode != "none" else None
    )
    failure_detail = (
        suspension_candidate[1]
        if suspension_candidate and suspension_time == executed_duration
        else None
    )
    reason = (
        "interval completed with all declared balances closed"
        if failure_mode == "none"
        else f"interval terminated by {failure_mode}"
        + (f" ({failure_detail})" if failure_detail else "")
    )
    residuals = SuspensionBrakeResiduals(
        suspension_force_n=suspension_residual,
        brake_torque_n_m=torque_residual,
        brake_energy_j=energy_residual,
        storage_capacity_margin_j=storage_margin,
    )
    return SuspensionBrakeStepResult(
        model_version=MODEL_VERSION,
        status="ok" if failure_mode == "none" else "failed",
        reason=reason,
        module_id=module.module_id,
        start_state=state,
        end_state=end_state,
        requested_duration_s=step_input.duration_s,
        executed_duration_s=executed_duration,
        unexecuted_duration_s=step_input.duration_s - executed_duration,
        failure_mode=failure_mode,
        failure_time_s=failure_time,
        normal_load_n=step_input.normal_load_n,
        suspension_force_n=suspension_force,
        suspension_acceleration_m_per_s2=suspension_acceleration,
        tyre_torque_limit_n_m=tyre_torque_limit,
        regen_torque_limit_by_component_n_m=regen_component_limit,
        regen_torque_limit_by_generator_power_n_m=regen_generator_limit,
        regen_torque_limit_by_charge_power_n_m=regen_charge_limit,
        regen_torque_limit_by_storage_capacity_n_m=regen_storage_limit,
        available_regen_torque_n_m=available_regen,
        available_mechanical_torque_n_m=available_mechanical,
        allocated_regen_torque_n_m=allocated_regen,
        allocated_mechanical_torque_n_m=allocated_mechanical,
        tyre_limit_scale=tyre_scale,
        applied_regen_torque_n_m=applied_regen,
        applied_mechanical_torque_n_m=applied_mechanical,
        applied_total_brake_torque_n_m=applied_total,
        unserved_brake_torque_n_m=unserved_torque,
        wheel_energy_removed_j=removed_energy,
        regenerative_wheel_energy_j=regen_wheel_energy,
        recovered_storage_energy_j=recovered_energy,
        regenerative_conversion_loss_j=regen_loss,
        mechanical_brake_heat_j=mechanical_heat,
        thermal_result=thermal_result,
        residuals=residuals,
    )
