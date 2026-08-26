"""Deterministic lumped thermal physics with explicit failure events."""

from __future__ import annotations

from dataclasses import dataclass
import math


class ThermalInputError(ValueError):
    """Raised when a declared thermal input violates the model contract."""


class ThermalNumericalError(ArithmeticError):
    """Raised when finite inputs produce a non-finite thermal calculation."""


def _finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ThermalInputError(f"{name} must be finite; received {value!r}")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise ThermalInputError(f"{name} must be > 0; received {value!r}")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise ThermalInputError(f"{name} must be >= 0; received {value!r}")


@dataclass(frozen=True, slots=True)
class ThermalParameters:
    heat_capacity_j_per_k: float
    passive_conductance_w_per_k: float
    active_conductance_w_per_k: float
    derating_start_temperature_k: float
    failure_temperature_k: float

    def __post_init__(self) -> None:
        _positive("heat_capacity_j_per_k", self.heat_capacity_j_per_k)
        _nonnegative(
            "passive_conductance_w_per_k", self.passive_conductance_w_per_k
        )
        _nonnegative(
            "active_conductance_w_per_k", self.active_conductance_w_per_k
        )
        _positive(
            "derating_start_temperature_k", self.derating_start_temperature_k
        )
        _positive("failure_temperature_k", self.failure_temperature_k)
        if self.derating_start_temperature_k >= self.failure_temperature_k:
            raise ThermalInputError(
                "derating_start_temperature_k must be < failure_temperature_k"
            )


@dataclass(frozen=True, slots=True)
class ThermalState:
    time_s: float
    temperature_k: float
    failed: bool = False

    def __post_init__(self) -> None:
        _nonnegative("time_s", self.time_s)
        _positive("temperature_k", self.temperature_k)
        if not isinstance(self.failed, bool):
            raise ThermalInputError("failed must be a boolean")


@dataclass(frozen=True, slots=True)
class ThermalStepInput:
    duration_s: float
    heat_generation_w: float
    ambient_temperature_k: float
    active_cooling_command: float

    def __post_init__(self) -> None:
        _positive("duration_s", self.duration_s)
        _nonnegative("heat_generation_w", self.heat_generation_w)
        _positive("ambient_temperature_k", self.ambient_temperature_k)
        _finite("active_cooling_command", self.active_cooling_command)
        if not 0.0 <= self.active_cooling_command <= 1.0:
            raise ThermalInputError("active_cooling_command must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class ThermalStepResult:
    status: str
    start_state: ThermalState
    end_state: ThermalState
    requested_duration_s: float
    executed_duration_s: float
    unexecuted_duration_s: float
    effective_conductance_w_per_k: float
    heat_generated_j: float
    passive_heat_rejected_j: float
    active_heat_rejected_j: float
    stored_energy_change_j: float
    energy_residual_j: float
    start_derating_factor: float
    end_derating_factor: float
    failure_time_s: float | None


def thermal_derating_factor(
    parameters: ThermalParameters, temperature_k: float
) -> float:
    """Return the declared temperature-only power availability factor."""

    _positive("temperature_k", temperature_k)
    if temperature_k <= parameters.derating_start_temperature_k:
        return 1.0
    if temperature_k >= parameters.failure_temperature_k:
        return 0.0
    return (
        parameters.failure_temperature_k - temperature_k
    ) / (
        parameters.failure_temperature_k
        - parameters.derating_start_temperature_k
    )


def _temperature_after(
    *,
    start_temperature_k: float,
    duration_s: float,
    heat_generation_w: float,
    ambient_temperature_k: float,
    conductance_w_per_k: float,
    heat_capacity_j_per_k: float,
) -> float:
    if conductance_w_per_k == 0.0:
        value = (
            start_temperature_k
            + heat_generation_w * duration_s / heat_capacity_j_per_k
        )
    else:
        equilibrium_k = (
            ambient_temperature_k + heat_generation_w / conductance_w_per_k
        )
        if not math.isfinite(equilibrium_k):
            raise ThermalNumericalError("thermal equilibrium is non-finite")
        decay = math.exp(
            -conductance_w_per_k * duration_s / heat_capacity_j_per_k
        )
        value = equilibrium_k + (start_temperature_k - equilibrium_k) * decay
    if not math.isfinite(value) or value <= 0.0:
        raise ThermalNumericalError(
            f"thermal integration produced invalid temperature {value!r} K"
        )
    return value


def _failure_crossing_duration_s(
    *,
    start_temperature_k: float,
    failure_temperature_k: float,
    heat_generation_w: float,
    ambient_temperature_k: float,
    conductance_w_per_k: float,
    heat_capacity_j_per_k: float,
) -> float:
    if conductance_w_per_k == 0.0:
        if heat_generation_w <= 0.0:
            raise ThermalNumericalError("failure crossing requested without heating")
        return (
            (failure_temperature_k - start_temperature_k)
            * heat_capacity_j_per_k
            / heat_generation_w
        )
    equilibrium_k = ambient_temperature_k + heat_generation_w / conductance_w_per_k
    numerator = failure_temperature_k - equilibrium_k
    denominator = start_temperature_k - equilibrium_k
    ratio = numerator / denominator
    if not 0.0 < ratio <= 1.0:
        raise ThermalNumericalError(
            f"invalid analytical failure-crossing ratio {ratio!r}"
        )
    return -heat_capacity_j_per_k / conductance_w_per_k * math.log(ratio)


def step_thermal_state(
    *,
    parameters: ThermalParameters,
    state: ThermalState,
    step_input: ThermalStepInput,
) -> ThermalStepResult:
    """Advance one constant-input interval or terminate at first failure."""

    start_factor = (
        0.0 if state.failed else thermal_derating_factor(parameters, state.temperature_k)
    )
    if state.failed or state.temperature_k >= parameters.failure_temperature_k:
        failed_state = ThermalState(state.time_s, state.temperature_k, True)
        status = "already_failed" if state.failed else "failed_at_start"
        return ThermalStepResult(
            status,
            state,
            failed_state,
            step_input.duration_s,
            0.0,
            step_input.duration_s,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            start_factor,
            0.0,
            state.time_s,
        )

    active_conductance = (
        step_input.active_cooling_command
        * parameters.active_conductance_w_per_k
    )
    total_conductance = (
        parameters.passive_conductance_w_per_k + active_conductance
    )
    requested_end_k = _temperature_after(
        start_temperature_k=state.temperature_k,
        duration_s=step_input.duration_s,
        heat_generation_w=step_input.heat_generation_w,
        ambient_temperature_k=step_input.ambient_temperature_k,
        conductance_w_per_k=total_conductance,
        heat_capacity_j_per_k=parameters.heat_capacity_j_per_k,
    )

    failed = requested_end_k >= parameters.failure_temperature_k
    if failed:
        executed_s = _failure_crossing_duration_s(
            start_temperature_k=state.temperature_k,
            failure_temperature_k=parameters.failure_temperature_k,
            heat_generation_w=step_input.heat_generation_w,
            ambient_temperature_k=step_input.ambient_temperature_k,
            conductance_w_per_k=total_conductance,
            heat_capacity_j_per_k=parameters.heat_capacity_j_per_k,
        )
        if not 0.0 <= executed_s <= step_input.duration_s:
            raise ThermalNumericalError(
                f"failure event time {executed_s!r} s is outside the step"
            )
        end_temperature_k = parameters.failure_temperature_k
        status = "failed"
    else:
        executed_s = step_input.duration_s
        end_temperature_k = requested_end_k
        status = (
            "derated"
            if start_factor < 1.0
            or end_temperature_k > parameters.derating_start_temperature_k
            else "normal"
        )

    end_time_s = state.time_s + executed_s
    if not math.isfinite(end_time_s):
        raise ThermalNumericalError("thermal step produced non-finite time")
    end_state = ThermalState(end_time_s, end_temperature_k, failed)
    heat_generated_j = step_input.heat_generation_w * executed_s
    stored_change_j = (
        parameters.heat_capacity_j_per_k
        * (end_temperature_k - state.temperature_k)
    )
    total_rejected_j = heat_generated_j - stored_change_j
    if total_conductance > 0.0:
        passive_rejected_j = (
            total_rejected_j
            * parameters.passive_conductance_w_per_k
            / total_conductance
        )
        active_rejected_j = (
            total_rejected_j * active_conductance / total_conductance
        )
    else:
        passive_rejected_j = 0.0
        active_rejected_j = 0.0
    residual_j = (
        heat_generated_j
        - passive_rejected_j
        - active_rejected_j
        - stored_change_j
    )
    values = (
        heat_generated_j,
        passive_rejected_j,
        active_rejected_j,
        stored_change_j,
        residual_j,
    )
    if not all(math.isfinite(value) for value in values):
        raise ThermalNumericalError("thermal energy accounting is non-finite")

    return ThermalStepResult(
        status,
        state,
        end_state,
        step_input.duration_s,
        executed_s,
        step_input.duration_s - executed_s,
        total_conductance,
        heat_generated_j,
        passive_rejected_j,
        active_rejected_j,
        stored_change_j,
        residual_j,
        start_factor,
        0.0 if failed else thermal_derating_factor(parameters, end_temperature_k),
        end_time_s if failed else None,
    )
