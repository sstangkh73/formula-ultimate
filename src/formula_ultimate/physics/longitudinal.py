"""Deterministic Level-0 longitudinal reference physics.

This module intentionally models only forward, one-dimensional point-mass
motion. It provides analytical-reference behavior for validating future
powertrain and topology work; it is not a full vehicle-dynamics model.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


class PhysicsInputError(ValueError):
    """Raised when a declared physics input is outside the model boundary."""


class PhysicsNumericalError(ArithmeticError):
    """Raised when a simulation produces a non-finite numerical state."""


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise PhysicsInputError(f"{name} must be finite; received {value!r}")


def _require_non_negative(name: str, value: float) -> None:
    _require_finite(name, value)
    if value < 0.0:
        raise PhysicsInputError(f"{name} must be >= 0; received {value!r}")


def _require_positive(name: str, value: float) -> None:
    _require_finite(name, value)
    if value <= 0.0:
        raise PhysicsInputError(f"{name} must be > 0; received {value!r}")


@dataclass(frozen=True, slots=True)
class VehicleParameters:
    """Fixed Level-0 vehicle parameters, expressed in SI units."""

    mass_kg: float
    drag_area_m2: float = 0.0
    rolling_resistance_coefficient: float = 0.0

    def __post_init__(self) -> None:
        _require_positive("mass_kg", self.mass_kg)
        _require_non_negative("drag_area_m2", self.drag_area_m2)
        _require_non_negative(
            "rolling_resistance_coefficient",
            self.rolling_resistance_coefficient,
        )


@dataclass(frozen=True, slots=True)
class EnvironmentParameters:
    """Constant environment for one analytical reference run."""

    air_density_kg_per_m3: float = 1.225
    gravity_mps2: float = 9.80665
    grade_radians: float = 0.0

    def __post_init__(self) -> None:
        _require_non_negative("air_density_kg_per_m3", self.air_density_kg_per_m3)
        _require_positive("gravity_mps2", self.gravity_mps2)
        _require_finite("grade_radians", self.grade_radians)
        if abs(self.grade_radians) >= math.pi / 2.0:
            raise PhysicsInputError("abs(grade_radians) must be < pi/2")


@dataclass(frozen=True, slots=True)
class SimulationConfig:
    """Deterministic integration controls."""

    duration_s: float
    time_step_s: float

    def __post_init__(self) -> None:
        _require_non_negative("duration_s", self.duration_s)
        _require_positive("time_step_s", self.time_step_s)


@dataclass(frozen=True, slots=True)
class LongitudinalState:
    time_s: float
    position_m: float
    speed_mps: float


@dataclass(frozen=True, slots=True)
class StepTelemetry:
    start_time_s: float
    time_step_s: float
    tractive_force_n: float
    aerodynamic_drag_n: float
    rolling_resistance_n: float
    grade_force_n: float
    unconstrained_net_force_n: float
    unconstrained_acceleration_mps2: float
    zero_speed_constraint_impulse_ns: float
    stopped_within_step: bool


@dataclass(frozen=True, slots=True)
class SimulationResult:
    states: tuple[LongitudinalState, ...]
    telemetry: tuple[StepTelemetry, ...]

    @property
    def final_state(self) -> LongitudinalState:
        return self.states[-1]


def aerodynamic_drag_force_n(
    *, speed_mps: float, air_density_kg_per_m3: float, drag_area_m2: float
) -> float:
    """Return the non-negative aerodynamic force opposing forward motion."""

    _require_non_negative("speed_mps", speed_mps)
    _require_non_negative("air_density_kg_per_m3", air_density_kg_per_m3)
    _require_non_negative("drag_area_m2", drag_area_m2)
    return 0.5 * air_density_kg_per_m3 * drag_area_m2 * speed_mps**2


def grade_force_n(
    *, mass_kg: float, gravity_mps2: float, grade_radians: float
) -> float:
    """Return signed grade resistance; downhill grades produce negative force."""

    _require_positive("mass_kg", mass_kg)
    _require_positive("gravity_mps2", gravity_mps2)
    _require_finite("grade_radians", grade_radians)
    if abs(grade_radians) >= math.pi / 2.0:
        raise PhysicsInputError("abs(grade_radians) must be < pi/2")
    return mass_kg * gravity_mps2 * math.sin(grade_radians)


def rolling_resistance_force_n(
    *,
    vehicle: VehicleParameters,
    environment: EnvironmentParameters,
    speed_mps: float,
    forward_force_before_rolling_n: float,
) -> float:
    """Return rolling resistance within the declared forward-only boundary.

    Resistance is active while moving or when the non-rolling force would start
    forward motion. This is not a static-friction or detailed tyre model.
    """

    _require_non_negative("speed_mps", speed_mps)
    _require_finite("forward_force_before_rolling_n", forward_force_before_rolling_n)
    if speed_mps == 0.0 and forward_force_before_rolling_n <= 0.0:
        return 0.0
    normal_force_n = (
        vehicle.mass_kg
        * environment.gravity_mps2
        * math.cos(environment.grade_radians)
    )
    return vehicle.rolling_resistance_coefficient * normal_force_n


def simulate_constant_traction(
    *,
    vehicle: VehicleParameters,
    environment: EnvironmentParameters,
    config: SimulationConfig,
    tractive_force_n: float,
    initial_speed_mps: float = 0.0,
    initial_position_m: float = 0.0,
) -> SimulationResult:
    """Simulate constant commanded traction with deterministic fixed steps.

    The last step is shortened so the final state lands exactly on
    ``config.duration_s``. Reverse motion is outside this model; when resistance
    would cross zero speed, the within-step stopping time is integrated and the
    remaining portion of the step stays at rest.
    """

    _require_non_negative("tractive_force_n", tractive_force_n)
    _require_non_negative("initial_speed_mps", initial_speed_mps)
    _require_non_negative("initial_position_m", initial_position_m)

    state = LongitudinalState(
        time_s=0.0,
        position_m=initial_position_m,
        speed_mps=initial_speed_mps,
    )
    states = [state]
    telemetry: list[StepTelemetry] = []

    while state.time_s < config.duration_s:
        next_time_s = min(config.duration_s, state.time_s + config.time_step_s)
        if next_time_s <= state.time_s:
            raise PhysicsNumericalError(
                "time_step_s is too small to advance time at the current state"
            )
        step_s = next_time_s - state.time_s

        drag_n = aerodynamic_drag_force_n(
            speed_mps=state.speed_mps,
            air_density_kg_per_m3=environment.air_density_kg_per_m3,
            drag_area_m2=vehicle.drag_area_m2,
        )
        grade_n = grade_force_n(
            mass_kg=vehicle.mass_kg,
            gravity_mps2=environment.gravity_mps2,
            grade_radians=environment.grade_radians,
        )
        forward_before_rolling_n = tractive_force_n - drag_n - grade_n
        rolling_n = rolling_resistance_force_n(
            vehicle=vehicle,
            environment=environment,
            speed_mps=state.speed_mps,
            forward_force_before_rolling_n=forward_before_rolling_n,
        )
        net_force_n = forward_before_rolling_n - rolling_n
        acceleration_mps2 = net_force_n / vehicle.mass_kg

        raw_next_speed_mps = state.speed_mps + acceleration_mps2 * step_s
        stopped_within_step = raw_next_speed_mps < 0.0
        if stopped_within_step:
            stop_time_s = state.speed_mps / -acceleration_mps2
            distance_delta_m = 0.5 * state.speed_mps * stop_time_s
            next_speed_mps = 0.0
            constraint_impulse_ns = -vehicle.mass_kg * raw_next_speed_mps
        else:
            next_speed_mps = raw_next_speed_mps
            distance_delta_m = (
                0.5 * (state.speed_mps + next_speed_mps) * step_s
            )
            constraint_impulse_ns = 0.0

        next_position_m = state.position_m + distance_delta_m
        if not all(
            math.isfinite(value)
            for value in (
                next_time_s,
                next_position_m,
                next_speed_mps,
                acceleration_mps2,
            )
        ):
            raise PhysicsNumericalError("simulation produced a non-finite state")

        telemetry.append(
            StepTelemetry(
                start_time_s=state.time_s,
                time_step_s=step_s,
                tractive_force_n=tractive_force_n,
                aerodynamic_drag_n=drag_n,
                rolling_resistance_n=rolling_n,
                grade_force_n=grade_n,
                unconstrained_net_force_n=net_force_n,
                unconstrained_acceleration_mps2=acceleration_mps2,
                zero_speed_constraint_impulse_ns=constraint_impulse_ns,
                stopped_within_step=stopped_within_step,
            )
        )
        state = LongitudinalState(
            time_s=next_time_s,
            position_m=next_position_m,
            speed_mps=next_speed_mps,
        )
        states.append(state)

    return SimulationResult(states=tuple(states), telemetry=tuple(telemetry))
