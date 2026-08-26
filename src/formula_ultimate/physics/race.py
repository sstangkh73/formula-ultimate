"""Deterministic Level-0 full-race completion loop.

The circuit is reduced to published race distance and reference air density.
This module is an outcome/evidence gate, not a lap-time or physical-validation
model.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from .circuit import CircuitProfile
from .longitudinal import (
    EnvironmentParameters,
    PhysicsNumericalError,
    SimulationConfig,
    VehicleParameters,
    simulate_constant_traction,
)
from .thermal import (
    ThermalNumericalError,
    ThermalParameters,
    ThermalState,
    ThermalStepInput,
    ThermalStepResult,
    step_thermal_state,
    thermal_derating_factor,
)


class RaceInputError(ValueError):
    """Raised when a race contract is invalid before execution."""


class RaceNumericalError(ArithmeticError):
    """Raised internally and converted into an observable invalid outcome."""


def _finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise RaceInputError(f"{name} must be finite; received {value!r}")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise RaceInputError(f"{name} must be > 0; received {value!r}")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise RaceInputError(f"{name} must be >= 0; received {value!r}")


@dataclass(frozen=True, slots=True)
class RaceVehicle:
    vehicle_id: str
    longitudinal: VehicleParameters
    commanded_tractive_force_n: float
    initial_onboard_energy_j: float
    waste_heat_power_w: float
    auxiliary_power_w: float
    thermal_parameters: ThermalParameters
    initial_temperature_k: float

    def __post_init__(self) -> None:
        if not self.vehicle_id.strip():
            raise RaceInputError("vehicle_id must not be blank")
        _nonnegative("commanded_tractive_force_n", self.commanded_tractive_force_n)
        _nonnegative("initial_onboard_energy_j", self.initial_onboard_energy_j)
        _nonnegative("waste_heat_power_w", self.waste_heat_power_w)
        _nonnegative("auxiliary_power_w", self.auxiliary_power_w)
        _positive("initial_temperature_k", self.initial_temperature_k)


@dataclass(frozen=True, slots=True)
class RaceControl:
    time_step_s: float
    timeout_s: float
    ambient_temperature_k: float
    active_cooling_command: float
    random_seed: int = 0
    event_bisection_iterations: int = 64
    energy_event_absolute_tolerance_j: float = 1.0e-6
    energy_event_relative_tolerance: float = 1.0e-12

    def __post_init__(self) -> None:
        _positive("time_step_s", self.time_step_s)
        _positive("timeout_s", self.timeout_s)
        _positive("ambient_temperature_k", self.ambient_temperature_k)
        _finite("active_cooling_command", self.active_cooling_command)
        if not 0.0 <= self.active_cooling_command <= 1.0:
            raise RaceInputError("active_cooling_command must be in [0, 1]")
        if not isinstance(self.random_seed, int):
            raise RaceInputError("random_seed must be an integer")
        if not isinstance(self.event_bisection_iterations, int) or not (
            16 <= self.event_bisection_iterations <= 128
        ):
            raise RaceInputError(
                "event_bisection_iterations must be an integer in [16, 128]"
            )
        _nonnegative(
            "energy_event_absolute_tolerance_j",
            self.energy_event_absolute_tolerance_j,
        )
        _nonnegative(
            "energy_event_relative_tolerance", self.energy_event_relative_tolerance
        )
        if self.energy_event_relative_tolerance > 1.0e-6:
            raise RaceInputError(
                "energy_event_relative_tolerance must be <= 1e-6"
            )


@dataclass(frozen=True, slots=True)
class RaceReplayMetadata:
    schema_version: str
    model_version: str
    circuit_id: str
    layout_reference: str
    vehicle_id: str
    time_step_s: float
    timeout_s: float
    random_seed: int
    event_bisection_iterations: int
    energy_event_absolute_tolerance_j: float
    energy_event_relative_tolerance: float
    stochastic_draw_count: int


@dataclass(frozen=True, slots=True)
class RaceState:
    time_s: float
    distance_m: float
    speed_mps: float
    remaining_energy_j: float
    thermal_state: ThermalState


@dataclass(frozen=True, slots=True)
class RaceStepTelemetry:
    step_index: int
    start_time_s: float
    requested_duration_s: float
    executed_duration_s: float
    event: str
    start_distance_m: float
    end_distance_m: float
    start_speed_mps: float
    end_speed_mps: float
    start_derating_factor: float
    applied_tractive_force_n: float
    wheel_work_j: float
    waste_heat_energy_j: float
    auxiliary_energy_j: float
    source_energy_used_j: float
    energy_accounting_residual_j: float
    energy_boundary_residual_j: float
    remaining_energy_j: float
    thermal_status: str
    end_temperature_k: float


@dataclass(frozen=True, slots=True)
class RaceResult:
    outcome: str
    reason: str
    target_distance_m: float
    final_state: RaceState
    consumed_energy_j: float
    finish_distance_residual_m: float | None
    depletion_energy_residual_j: float | None
    terminal_energy_boundary_residual_j: float
    telemetry: tuple[RaceStepTelemetry, ...]
    replay: RaceReplayMetadata


@dataclass(frozen=True, slots=True)
class _MotionResult:
    distance_m: float
    speed_mps: float
    wheel_work_j: float
    source_energy_j: float


def _motion_result(
    *,
    vehicle: RaceVehicle,
    circuit: CircuitProfile,
    state: RaceState,
    duration_s: float,
    applied_force_n: float,
) -> _MotionResult:
    if duration_s == 0.0:
        return _MotionResult(state.distance_m, state.speed_mps, 0.0, 0.0)
    density = circuit.isa_air_density_kg_per_m3
    if density is None:
        density = 1.225
    simulation = simulate_constant_traction(
        vehicle=vehicle.longitudinal,
        environment=EnvironmentParameters(air_density_kg_per_m3=density),
        config=SimulationConfig(duration_s=duration_s, time_step_s=duration_s),
        tractive_force_n=applied_force_n,
        initial_speed_mps=state.speed_mps,
        initial_position_m=state.distance_m,
    )
    end = simulation.final_state
    delta_m = end.position_m - state.distance_m
    wheel_work_j = applied_force_n * delta_m
    source_energy_j = wheel_work_j + (
        vehicle.waste_heat_power_w + vehicle.auxiliary_power_w
    ) * duration_s
    values = (end.position_m, end.speed_mps, wheel_work_j, source_energy_j)
    if not all(math.isfinite(value) for value in values):
        raise RaceNumericalError("race motion or energy became non-finite")
    if delta_m < 0.0 or wheel_work_j < 0.0 or source_energy_j < 0.0:
        raise RaceNumericalError("race motion or source energy became negative")
    return _MotionResult(
        end.position_m, end.speed_mps, wheel_work_j, source_energy_j
    )


def _bisect_event(
    *, high_s: float, iterations: int, predicate
) -> tuple[float, float]:
    """Return the last false and first true deterministic bounds."""

    low_s = 0.0
    if not predicate(high_s):
        raise RaceNumericalError("event bisection high bound does not contain event")
    for _ in range(iterations):
        middle_s = 0.5 * (low_s + high_s)
        if predicate(middle_s):
            high_s = middle_s
        else:
            low_s = middle_s
    return low_s, high_s


def run_full_race(
    *, circuit: CircuitProfile, vehicle: RaceVehicle, control: RaceControl
) -> RaceResult:
    """Run until exactly one terminal outcome becomes observable."""

    replay = RaceReplayMetadata(
        "1.0",
        "race-level0-v1",
        circuit.circuit_id,
        circuit.layout_reference,
        vehicle.vehicle_id,
        control.time_step_s,
        control.timeout_s,
        control.random_seed,
        control.event_bisection_iterations,
        control.energy_event_absolute_tolerance_j,
        control.energy_event_relative_tolerance,
        0,
    )
    state = RaceState(
        0.0,
        0.0,
        0.0,
        vehicle.initial_onboard_energy_j,
        ThermalState(0.0, vehicle.initial_temperature_k),
    )
    telemetry: list[RaceStepTelemetry] = []
    latest_energy_boundary_residual_j = 0.0
    target_m = circuit.race_distance_m
    max_steps = math.ceil(control.timeout_s / control.time_step_s) + 2
    event_time_tolerance_s = 1.0e-12

    def finish(
        outcome: str,
        reason: str,
        *,
        finish_residual: float | None = None,
        depletion_residual: float | None = None,
    ) -> RaceResult:
        return RaceResult(
            outcome,
            reason,
            target_m,
            state,
            sum(item.source_energy_used_j for item in telemetry),
            finish_residual,
            depletion_residual,
            latest_energy_boundary_residual_j,
            tuple(telemetry),
            replay,
        )

    try:
        for step_index in range(max_steps):
            if state.distance_m >= target_m:
                return finish(
                    "finished",
                    "published race distance reached",
                    finish_residual=state.distance_m - target_m,
                )
            if state.remaining_energy_j <= 0.0:
                return finish(
                    "depleted",
                    "onboard primary energy exhausted",
                    depletion_residual=state.remaining_energy_j,
                )
            if state.thermal_state.failed:
                return finish("failed", "thermal failure is latched")
            remaining_timeout_s = control.timeout_s - state.time_s
            if remaining_timeout_s <= 0.0:
                return finish("timeout", "race timeout reached before finish")
            requested_s = min(control.time_step_s, remaining_timeout_s)
            if requested_s <= 0.0 or state.time_s + requested_s <= state.time_s:
                raise RaceNumericalError("race step cannot advance time")

            derating = thermal_derating_factor(
                vehicle.thermal_parameters, state.thermal_state.temperature_k
            )
            applied_force_n = vehicle.commanded_tractive_force_n * derating
            base_motion = _motion_result(
                vehicle=vehicle,
                circuit=circuit,
                state=state,
                duration_s=requested_s,
                applied_force_n=applied_force_n,
            )
            thermal_candidate = step_thermal_state(
                parameters=vehicle.thermal_parameters,
                state=state.thermal_state,
                step_input=ThermalStepInput(
                    requested_s,
                    vehicle.waste_heat_power_w,
                    control.ambient_temperature_k,
                    control.active_cooling_command,
                ),
            )

            candidates: list[tuple[float, int, str, float]] = []
            if base_motion.distance_m >= target_m:
                _, high = _bisect_event(
                    high_s=requested_s,
                    iterations=control.event_bisection_iterations,
                    predicate=lambda duration: _motion_result(
                        vehicle=vehicle,
                        circuit=circuit,
                        state=state,
                        duration_s=duration,
                        applied_force_n=applied_force_n,
                    ).distance_m
                    >= target_m,
                )
                candidates.append((high, 0, "finished", high))
            if thermal_candidate.status in {"failed", "failed_at_start"}:
                candidates.append(
                    (
                        thermal_candidate.executed_duration_s,
                        1,
                        "failed",
                        thermal_candidate.executed_duration_s,
                    )
                )
            if base_motion.source_energy_j >= state.remaining_energy_j:
                low, high = _bisect_event(
                    high_s=requested_s,
                    iterations=control.event_bisection_iterations,
                    predicate=lambda duration: _motion_result(
                        vehicle=vehicle,
                        circuit=circuit,
                        state=state,
                        duration_s=duration,
                        applied_force_n=applied_force_n,
                    ).source_energy_j
                    >= state.remaining_energy_j,
                )
                candidates.append((high, 2, "depleted", low))
            reaches_timeout = requested_s == remaining_timeout_s
            if reaches_timeout:
                candidates.append((requested_s, 3, "timeout", requested_s))
            candidates.append((requested_s, 4, "step", requested_s))

            earliest_s = min(candidate[0] for candidate in candidates)
            event = min(
                (
                    candidate
                    for candidate in candidates
                    if abs(candidate[0] - earliest_s) <= event_time_tolerance_s
                ),
                key=lambda candidate: candidate[1],
            )
            _, _, event_name, executed_s = event

            motion = _motion_result(
                vehicle=vehicle,
                circuit=circuit,
                state=state,
                duration_s=executed_s,
                applied_force_n=applied_force_n,
            )
            if event_name == "failed":
                thermal = thermal_candidate
            elif executed_s > 0.0:
                thermal = step_thermal_state(
                    parameters=vehicle.thermal_parameters,
                    state=state.thermal_state,
                    step_input=ThermalStepInput(
                        executed_s,
                        vehicle.waste_heat_power_w,
                        control.ambient_temperature_k,
                        control.active_cooling_command,
                    ),
                )
            else:
                thermal = ThermalStepResult(
                    "normal",
                    state.thermal_state,
                    state.thermal_state,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    derating,
                    derating,
                    None,
                )

            raw_remaining_energy_j = (
                state.remaining_energy_j - motion.source_energy_j
            )
            energy_tolerance_j = (
                control.energy_event_absolute_tolerance_j
                + control.energy_event_relative_tolerance
                * max(
                    state.remaining_energy_j,
                    motion.source_energy_j,
                    vehicle.initial_onboard_energy_j,
                )
            )
            energy_boundary_residual_j = min(0.0, raw_remaining_energy_j)
            if raw_remaining_energy_j < 0.0:
                if event_name in {"finished", "failed"} and (
                    -raw_remaining_energy_j <= energy_tolerance_j
                ):
                    remaining_energy_j = 0.0
                else:
                    raise RaceNumericalError(
                        "event ordering overspent onboard energy by "
                        f"{-raw_remaining_energy_j!r} J; tolerance "
                        f"{energy_tolerance_j!r} J"
                    )
            else:
                remaining_energy_j = raw_remaining_energy_j
            residual_j = motion.source_energy_j - (
                motion.wheel_work_j
                + vehicle.waste_heat_power_w * executed_s
                + vehicle.auxiliary_power_w * executed_s
            )
            if not math.isfinite(residual_j):
                raise RaceNumericalError("race energy residual is non-finite")
            next_state = RaceState(
                state.time_s + executed_s,
                motion.distance_m,
                motion.speed_mps,
                remaining_energy_j,
                thermal.end_state,
            )
            telemetry.append(
                RaceStepTelemetry(
                    step_index,
                    state.time_s,
                    requested_s,
                    executed_s,
                    event_name,
                    state.distance_m,
                    next_state.distance_m,
                    state.speed_mps,
                    next_state.speed_mps,
                    derating,
                    applied_force_n,
                    motion.wheel_work_j,
                    vehicle.waste_heat_power_w * executed_s,
                    vehicle.auxiliary_power_w * executed_s,
                    motion.source_energy_j,
                    residual_j,
                    energy_boundary_residual_j,
                    remaining_energy_j,
                    thermal.status,
                    thermal.end_state.temperature_k,
                )
            )
            state = next_state
            latest_energy_boundary_residual_j = energy_boundary_residual_j

            if event_name == "finished":
                return finish(
                    "finished",
                    "published race distance reached",
                    finish_residual=state.distance_m - target_m,
                )
            if event_name == "failed":
                return finish("failed", "thermal failure occurred during race")
            if event_name == "depleted":
                return finish(
                    "depleted",
                    "onboard primary energy exhausted before finish",
                    depletion_residual=state.remaining_energy_j,
                )
            if event_name == "timeout":
                return finish("timeout", "race timeout reached before finish")
        raise RaceNumericalError("race exceeded deterministic maximum step count")
    except (PhysicsNumericalError, ThermalNumericalError, RaceNumericalError, OverflowError) as exc:
        return finish("invalid", f"runtime numerical failure: {exc}")
