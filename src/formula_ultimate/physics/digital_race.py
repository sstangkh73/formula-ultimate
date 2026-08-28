"""Deterministic Level-0 multi-event race strategy and reliability gate.

This reduced-order model makes traffic, weather, degradation, damage, energy,
strategy, and seeded uncertainty observable.  It is not a real lap-time,
reliability-calibration, safety, or physical-validation model.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import random

from .circuit import CircuitProfile


class DigitalRaceInputError(ValueError):
    """Raised when a digital-race contract is invalid before execution."""


class DigitalRaceNumericalError(ArithmeticError):
    """Raised internally and converted into an observable invalid outcome."""


def _finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise DigitalRaceInputError(f"{name} must be finite; received {value!r}")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise DigitalRaceInputError(f"{name} must be > 0; received {value!r}")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise DigitalRaceInputError(f"{name} must be >= 0; received {value!r}")


def _nonblank(name: str, value: str) -> None:
    if not value.strip():
        raise DigitalRaceInputError(f"{name} must not be blank")


def _index(name: str, value: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise DigitalRaceInputError(f"{name} must be a non-negative integer")


@dataclass(frozen=True, slots=True)
class DigitalRaceSector:
    sector_id: str
    lap_fraction: float
    base_speed_mps: float
    base_energy_j_per_m: float
    degradation_per_m: float
    damage_per_m: float

    def __post_init__(self) -> None:
        _nonblank("sector_id", self.sector_id)
        _positive("lap_fraction", self.lap_fraction)
        _positive("base_speed_mps", self.base_speed_mps)
        _nonnegative("base_energy_j_per_m", self.base_energy_j_per_m)
        _nonnegative("degradation_per_m", self.degradation_per_m)
        _nonnegative("damage_per_m", self.damage_per_m)


@dataclass(frozen=True, slots=True)
class LapStrategyCommand:
    command_id: str
    pace_factor: float

    def __post_init__(self) -> None:
        _nonblank("command_id", self.command_id)
        _positive("pace_factor", self.pace_factor)
        if self.pace_factor > 2.0:
            raise DigitalRaceInputError("pace_factor must be <= 2")


@dataclass(frozen=True, slots=True)
class DigitalRaceStrategy:
    strategy_id: str
    lap_commands: tuple[LapStrategyCommand, ...]

    def __post_init__(self) -> None:
        _nonblank("strategy_id", self.strategy_id)
        if not self.lap_commands:
            raise DigitalRaceInputError("lap_commands must not be empty")


@dataclass(frozen=True, slots=True)
class WeatherCondition:
    condition_id: str
    speed_multiplier: float = 1.0
    energy_multiplier: float = 1.0
    degradation_multiplier: float = 1.0
    damage_multiplier: float = 1.0
    reliability_multiplier: float = 1.0

    def __post_init__(self) -> None:
        _nonblank("condition_id", self.condition_id)
        for name in (
            "speed_multiplier",
            "energy_multiplier",
            "degradation_multiplier",
            "damage_multiplier",
            "reliability_multiplier",
        ):
            _positive(name, getattr(self, name))


@dataclass(frozen=True, slots=True)
class TrafficCondition:
    traffic_id: str
    delay_s: float = 0.0
    speed_multiplier: float = 1.0
    energy_multiplier: float = 1.0
    degradation_multiplier: float = 1.0
    damage_multiplier: float = 1.0
    reliability_multiplier: float = 1.0

    def __post_init__(self) -> None:
        _nonblank("traffic_id", self.traffic_id)
        _nonnegative("delay_s", self.delay_s)
        for name in (
            "speed_multiplier",
            "energy_multiplier",
            "degradation_multiplier",
            "damage_multiplier",
            "reliability_multiplier",
        ):
            _positive(name, getattr(self, name))


@dataclass(frozen=True, slots=True)
class WeatherEvent:
    lap_index: int
    sector_index: int
    condition: WeatherCondition

    def __post_init__(self) -> None:
        _index("lap_index", self.lap_index)
        _index("sector_index", self.sector_index)


@dataclass(frozen=True, slots=True)
class TrafficEvent:
    lap_index: int
    sector_index: int
    condition: TrafficCondition

    def __post_init__(self) -> None:
        _index("lap_index", self.lap_index)
        _index("sector_index", self.sector_index)


@dataclass(frozen=True, slots=True)
class DigitalRaceScenario:
    scenario_id: str
    sectors: tuple[DigitalRaceSector, ...]
    strategy: DigitalRaceStrategy
    weather_events: tuple[WeatherEvent, ...] = ()
    traffic_events: tuple[TrafficEvent, ...] = ()

    def __post_init__(self) -> None:
        _nonblank("scenario_id", self.scenario_id)
        if not self.sectors:
            raise DigitalRaceInputError("sectors must not be empty")
        sector_ids = tuple(sector.sector_id for sector in self.sectors)
        if len(sector_ids) != len(set(sector_ids)):
            raise DigitalRaceInputError("sector_id values must be unique")
        lap_fraction_sum = math.fsum(sector.lap_fraction for sector in self.sectors)
        if not math.isclose(lap_fraction_sum, 1.0, rel_tol=0.0, abs_tol=1.0e-12):
            raise DigitalRaceInputError(
                "sector lap_fraction values must sum to 1 within 1e-12; "
                f"received {lap_fraction_sum!r}"
            )
        for name, events in (
            ("weather", self.weather_events),
            ("traffic", self.traffic_events),
        ):
            keys = tuple((event.lap_index, event.sector_index) for event in events)
            if len(keys) != len(set(keys)):
                raise DigitalRaceInputError(f"duplicate {name} event key")


@dataclass(frozen=True, slots=True)
class DigitalRaceVehicle:
    vehicle_id: str
    initial_onboard_energy_j: float
    auxiliary_power_w: float
    initial_degradation: float
    degradation_limit: float
    degradation_speed_loss_per_unit: float
    initial_damage: float
    damage_limit: float
    base_reliability_hazard_per_s: float
    hazard_degradation_coefficient: float
    hazard_damage_coefficient: float
    hazard_pace_exponent: float

    def __post_init__(self) -> None:
        _nonblank("vehicle_id", self.vehicle_id)
        for name in (
            "initial_onboard_energy_j",
            "auxiliary_power_w",
            "initial_degradation",
            "degradation_speed_loss_per_unit",
            "initial_damage",
            "base_reliability_hazard_per_s",
            "hazard_degradation_coefficient",
            "hazard_damage_coefficient",
            "hazard_pace_exponent",
        ):
            _nonnegative(name, getattr(self, name))
        _positive("degradation_limit", self.degradation_limit)
        _positive("damage_limit", self.damage_limit)
        if self.initial_degradation >= self.degradation_limit:
            raise DigitalRaceInputError(
                "initial_degradation must be below degradation_limit"
            )
        if self.initial_damage >= self.damage_limit:
            raise DigitalRaceInputError("initial_damage must be below damage_limit")


@dataclass(frozen=True, slots=True)
class DigitalRaceControl:
    timeout_s: float
    random_seed: int = 0
    event_time_tolerance_s: float = 1.0e-12
    residual_absolute_tolerance: float = 1.0e-8

    def __post_init__(self) -> None:
        _positive("timeout_s", self.timeout_s)
        if not isinstance(self.random_seed, int) or isinstance(self.random_seed, bool):
            raise DigitalRaceInputError("random_seed must be an integer")
        _nonnegative("event_time_tolerance_s", self.event_time_tolerance_s)
        _nonnegative("residual_absolute_tolerance", self.residual_absolute_tolerance)


@dataclass(frozen=True, slots=True)
class DigitalRaceState:
    time_s: float
    distance_m: float
    remaining_energy_j: float
    degradation: float
    damage: float
    completed_laps: int
    completed_events: int


@dataclass(frozen=True, slots=True)
class DigitalRaceEventTelemetry:
    event_index: int
    lap_index: int
    sector_index: int
    sector_id: str
    strategy_command_id: str
    weather_condition_id: str
    traffic_condition_id: str
    pace_factor: float
    nominal_distance_m: float
    official_distance_adjustment_m: float
    requested_distance_m: float
    executed_distance_m: float
    start_time_s: float
    requested_duration_s: float
    executed_duration_s: float
    event: str
    effective_travel_speed_mps: float
    average_progress_speed_mps: float
    reliability_hazard_per_s: float
    reliability_draw: float
    reliability_candidate_time_s: float | None
    drive_energy_used_j: float
    auxiliary_energy_used_j: float
    source_energy_used_j: float
    start_remaining_energy_j: float
    end_remaining_energy_j: float
    degradation_increment: float
    end_degradation: float
    damage_increment: float
    end_damage: float
    distance_accounting_residual_m: float
    energy_accounting_residual_j: float
    energy_boundary_residual_j: float


@dataclass(frozen=True, slots=True)
class DigitalRaceReplayMetadata:
    schema_version: str
    model_version: str
    circuit_id: str
    layout_reference: str
    scenario_id: str
    vehicle_id: str
    strategy_id: str
    strategy_pace_factors: tuple[float, ...]
    weather_schedule: tuple[tuple[int, int, str], ...]
    traffic_schedule: tuple[tuple[int, int, str], ...]
    random_seed: int
    entered_event_count: int
    stochastic_draw_count: int


@dataclass(frozen=True, slots=True)
class DigitalRaceResult:
    outcome: str
    failure_mode: str
    reason: str
    target_distance_m: float
    final_state: DigitalRaceState
    consumed_energy_j: float
    finish_distance_residual_m: float
    total_energy_accounting_residual_j: float
    telemetry: tuple[DigitalRaceEventTelemetry, ...]
    replay: DigitalRaceReplayMetadata


_NEUTRAL_WEATHER = WeatherCondition("neutral-weather")
_CLEAR_TRAFFIC = TrafficCondition("clear-traffic")


def _validate_scenario_for_circuit(
    circuit: CircuitProfile, scenario: DigitalRaceScenario
) -> tuple[dict[tuple[int, int], WeatherCondition], dict[tuple[int, int], TrafficCondition]]:
    if len(scenario.strategy.lap_commands) != circuit.race_laps:
        raise DigitalRaceInputError(
            "strategy must provide exactly one command per published race lap"
        )
    weather = {
        (event.lap_index, event.sector_index): event.condition
        for event in scenario.weather_events
    }
    traffic = {
        (event.lap_index, event.sector_index): event.condition
        for event in scenario.traffic_events
    }
    for name, schedule in (("weather", weather), ("traffic", traffic)):
        for lap_index, sector_index in schedule:
            if lap_index >= circuit.race_laps:
                raise DigitalRaceInputError(
                    f"{name} event lap_index exceeds published race laps"
                )
            if sector_index >= len(scenario.sectors):
                raise DigitalRaceInputError(
                    f"{name} event sector_index exceeds scenario sectors"
                )
    final_nominal_m = circuit.lap_length_m * scenario.sectors[-1].lap_fraction
    if final_nominal_m + circuit.race_start_offset_m <= 0.0:
        raise DigitalRaceInputError(
            "official race-distance residual makes the final event non-positive"
        )
    return weather, traffic


def run_digital_race(
    *,
    circuit: CircuitProfile,
    scenario: DigitalRaceScenario,
    vehicle: DigitalRaceVehicle,
    control: DigitalRaceControl,
) -> DigitalRaceResult:
    """Execute a seeded multi-lap race until one observable outcome occurs."""

    weather_schedule, traffic_schedule = _validate_scenario_for_circuit(
        circuit, scenario
    )
    rng = random.Random(control.random_seed)
    state = DigitalRaceState(
        time_s=0.0,
        distance_m=0.0,
        remaining_energy_j=vehicle.initial_onboard_energy_j,
        degradation=vehicle.initial_degradation,
        damage=vehicle.initial_damage,
        completed_laps=0,
        completed_events=0,
    )
    telemetry: list[DigitalRaceEventTelemetry] = []
    draw_count = 0

    def finish(outcome: str, failure_mode: str, reason: str) -> DigitalRaceResult:
        consumed_j = math.fsum(item.source_energy_used_j for item in telemetry)
        total_energy_residual_j = (
            vehicle.initial_onboard_energy_j
            - consumed_j
            - state.remaining_energy_j
        )
        replay = DigitalRaceReplayMetadata(
            schema_version="1.0",
            model_version="digital-race-level0-v1",
            circuit_id=circuit.circuit_id,
            layout_reference=circuit.layout_reference,
            scenario_id=scenario.scenario_id,
            vehicle_id=vehicle.vehicle_id,
            strategy_id=scenario.strategy.strategy_id,
            strategy_pace_factors=tuple(
                command.pace_factor for command in scenario.strategy.lap_commands
            ),
            weather_schedule=tuple(
                (event.lap_index, event.sector_index, event.condition.condition_id)
                for event in scenario.weather_events
            ),
            traffic_schedule=tuple(
                (event.lap_index, event.sector_index, event.condition.traffic_id)
                for event in scenario.traffic_events
            ),
            random_seed=control.random_seed,
            entered_event_count=len(telemetry),
            stochastic_draw_count=draw_count,
        )
        return DigitalRaceResult(
            outcome=outcome,
            failure_mode=failure_mode,
            reason=reason,
            target_distance_m=circuit.race_distance_m,
            final_state=state,
            consumed_energy_j=consumed_j,
            finish_distance_residual_m=state.distance_m - circuit.race_distance_m,
            total_energy_accounting_residual_j=total_energy_residual_j,
            telemetry=tuple(telemetry),
            replay=replay,
        )

    try:
        if state.remaining_energy_j <= 0.0:
            return finish("depleted", "energy", "onboard primary energy is empty")

        event_index = 0
        for lap_index in range(circuit.race_laps):
            command = scenario.strategy.lap_commands[lap_index]
            for sector_index, sector in enumerate(scenario.sectors):
                if state.time_s >= control.timeout_s:
                    return finish("timeout", "timeout", "race timeout reached")
                if state.remaining_energy_j <= 0.0:
                    return finish(
                        "depleted", "energy", "onboard primary energy is empty"
                    )

                key = (lap_index, sector_index)
                weather = weather_schedule.get(key, _NEUTRAL_WEATHER)
                traffic = traffic_schedule.get(key, _CLEAR_TRAFFIC)
                final_event = (
                    lap_index == circuit.race_laps - 1
                    and sector_index == len(scenario.sectors) - 1
                )
                nominal_distance_m = circuit.lap_length_m * sector.lap_fraction
                if final_event:
                    requested_distance_m = circuit.race_distance_m - state.distance_m
                else:
                    requested_distance_m = nominal_distance_m
                distance_adjustment_m = requested_distance_m - nominal_distance_m
                if not math.isfinite(requested_distance_m) or requested_distance_m <= 0.0:
                    raise DigitalRaceNumericalError(
                        "event distance became non-positive or non-finite"
                    )

                degradation_speed_multiplier = (
                    1.0
                    - vehicle.degradation_speed_loss_per_unit * state.degradation
                )
                effective_speed_mps = (
                    sector.base_speed_mps
                    * command.pace_factor
                    * weather.speed_multiplier
                    * traffic.speed_multiplier
                    * degradation_speed_multiplier
                )
                travel_duration_s = requested_distance_m / effective_speed_mps
                requested_duration_s = travel_duration_s + traffic.delay_s
                drive_energy_requested_j = (
                    requested_distance_m
                    * sector.base_energy_j_per_m
                    * command.pace_factor**2
                    * weather.energy_multiplier
                    * traffic.energy_multiplier
                )
                degradation_requested = (
                    requested_distance_m
                    * sector.degradation_per_m
                    * command.pace_factor**2
                    * weather.degradation_multiplier
                    * traffic.degradation_multiplier
                )
                damage_requested = (
                    requested_distance_m
                    * sector.damage_per_m
                    * command.pace_factor**3
                    * weather.damage_multiplier
                    * traffic.damage_multiplier
                )
                source_energy_requested_j = (
                    drive_energy_requested_j
                    + vehicle.auxiliary_power_w * requested_duration_s
                )
                hazard_per_s = (
                    vehicle.base_reliability_hazard_per_s
                    * weather.reliability_multiplier
                    * traffic.reliability_multiplier
                    * command.pace_factor**vehicle.hazard_pace_exponent
                    * (
                        1.0
                        + vehicle.hazard_degradation_coefficient * state.degradation
                        + vehicle.hazard_damage_coefficient * state.damage
                    )
                )
                values = (
                    degradation_speed_multiplier,
                    effective_speed_mps,
                    travel_duration_s,
                    requested_duration_s,
                    drive_energy_requested_j,
                    degradation_requested,
                    damage_requested,
                    source_energy_requested_j,
                    hazard_per_s,
                )
                if not all(math.isfinite(value) for value in values):
                    raise DigitalRaceNumericalError(
                        "event rate calculation became non-finite"
                    )
                if degradation_speed_multiplier <= 0.0 or effective_speed_mps <= 0.0:
                    raise DigitalRaceNumericalError(
                        "accumulated degradation produced non-positive speed"
                    )
                if requested_duration_s <= 0.0:
                    raise DigitalRaceNumericalError("event cannot advance time")
                if min(
                    drive_energy_requested_j,
                    degradation_requested,
                    damage_requested,
                    source_energy_requested_j,
                    hazard_per_s,
                ) < 0.0:
                    raise DigitalRaceNumericalError("event rate became negative")

                reliability_draw = rng.random()
                draw_count += 1
                reliability_time_s = (
                    None
                    if hazard_per_s == 0.0
                    else -math.log1p(-reliability_draw) / hazard_per_s
                )
                energy_rate_w = source_energy_requested_j / requested_duration_s
                degradation_rate_per_s = degradation_requested / requested_duration_s
                damage_rate_per_s = damage_requested / requested_duration_s

                candidates: list[tuple[float, int, str]] = []
                if final_event:
                    candidates.append((requested_duration_s, 0, "finished"))
                if (
                    reliability_time_s is not None
                    and reliability_time_s <= requested_duration_s
                ):
                    candidates.append((reliability_time_s, 1, "reliability"))
                if damage_rate_per_s > 0.0:
                    damage_time_s = (
                        vehicle.damage_limit - state.damage
                    ) / damage_rate_per_s
                    if damage_time_s <= requested_duration_s:
                        candidates.append((damage_time_s, 2, "damage"))
                if degradation_rate_per_s > 0.0:
                    degradation_time_s = (
                        vehicle.degradation_limit - state.degradation
                    ) / degradation_rate_per_s
                    if degradation_time_s <= requested_duration_s:
                        candidates.append((degradation_time_s, 3, "degradation"))
                if energy_rate_w > 0.0:
                    depletion_time_s = state.remaining_energy_j / energy_rate_w
                    if depletion_time_s <= requested_duration_s:
                        candidates.append((depletion_time_s, 4, "depleted"))
                timeout_time_s = control.timeout_s - state.time_s
                if timeout_time_s <= requested_duration_s:
                    candidates.append((timeout_time_s, 5, "timeout"))
                if not final_event:
                    candidates.append((requested_duration_s, 6, "sector_complete"))

                earliest_s = min(candidate[0] for candidate in candidates)
                selected = min(
                    (
                        candidate
                        for candidate in candidates
                        if abs(candidate[0] - earliest_s)
                        <= control.event_time_tolerance_s
                    ),
                    key=lambda candidate: candidate[1],
                )
                executed_duration_s, _, event_name = selected
                if not 0.0 <= executed_duration_s <= requested_duration_s:
                    raise DigitalRaceNumericalError(
                        "localized event time lies outside the event"
                    )
                fraction = executed_duration_s / requested_duration_s
                executed_distance_m = requested_distance_m * fraction
                drive_energy_used_j = drive_energy_requested_j * fraction
                auxiliary_energy_used_j = (
                    vehicle.auxiliary_power_w * executed_duration_s
                )
                source_energy_used_j = drive_energy_used_j + auxiliary_energy_used_j
                raw_remaining_energy_j = (
                    state.remaining_energy_j - source_energy_used_j
                )
                energy_boundary_residual_j = min(0.0, raw_remaining_energy_j)
                if raw_remaining_energy_j < -control.residual_absolute_tolerance:
                    raise DigitalRaceNumericalError(
                        "event ordering overspent onboard energy"
                    )
                remaining_energy_j = (
                    0.0 if raw_remaining_energy_j < 0.0 else raw_remaining_energy_j
                )
                degradation_increment = degradation_requested * fraction
                damage_increment = damage_requested * fraction
                end_degradation = state.degradation + degradation_increment
                end_damage = state.damage + damage_increment
                if event_name == "degradation":
                    end_degradation = vehicle.degradation_limit
                if event_name == "damage":
                    end_damage = vehicle.damage_limit
                end_distance_m = state.distance_m + executed_distance_m
                if event_name == "finished":
                    end_distance_m = circuit.race_distance_m
                    executed_distance_m = end_distance_m - state.distance_m
                distance_residual_m = (
                    end_distance_m - state.distance_m - executed_distance_m
                )
                energy_residual_j = (
                    state.remaining_energy_j
                    - source_energy_used_j
                    - remaining_energy_j
                )
                end_completed_events = state.completed_events + (
                    1 if event_name in {"sector_complete", "finished"} else 0
                )
                end_completed_laps = state.completed_laps + (
                    1
                    if event_name in {"sector_complete", "finished"}
                    and sector_index == len(scenario.sectors) - 1
                    else 0
                )
                next_state = DigitalRaceState(
                    time_s=state.time_s + executed_duration_s,
                    distance_m=end_distance_m,
                    remaining_energy_j=remaining_energy_j,
                    degradation=end_degradation,
                    damage=end_damage,
                    completed_laps=end_completed_laps,
                    completed_events=end_completed_events,
                )
                telemetry.append(
                    DigitalRaceEventTelemetry(
                        event_index=event_index,
                        lap_index=lap_index,
                        sector_index=sector_index,
                        sector_id=sector.sector_id,
                        strategy_command_id=command.command_id,
                        weather_condition_id=weather.condition_id,
                        traffic_condition_id=traffic.traffic_id,
                        pace_factor=command.pace_factor,
                        nominal_distance_m=nominal_distance_m,
                        official_distance_adjustment_m=distance_adjustment_m,
                        requested_distance_m=requested_distance_m,
                        executed_distance_m=executed_distance_m,
                        start_time_s=state.time_s,
                        requested_duration_s=requested_duration_s,
                        executed_duration_s=executed_duration_s,
                        event=event_name,
                        effective_travel_speed_mps=effective_speed_mps,
                        average_progress_speed_mps=(
                            requested_distance_m / requested_duration_s
                        ),
                        reliability_hazard_per_s=hazard_per_s,
                        reliability_draw=reliability_draw,
                        reliability_candidate_time_s=reliability_time_s,
                        drive_energy_used_j=drive_energy_used_j,
                        auxiliary_energy_used_j=auxiliary_energy_used_j,
                        source_energy_used_j=source_energy_used_j,
                        start_remaining_energy_j=state.remaining_energy_j,
                        end_remaining_energy_j=remaining_energy_j,
                        degradation_increment=degradation_increment,
                        end_degradation=end_degradation,
                        damage_increment=damage_increment,
                        end_damage=end_damage,
                        distance_accounting_residual_m=distance_residual_m,
                        energy_accounting_residual_j=energy_residual_j,
                        energy_boundary_residual_j=energy_boundary_residual_j,
                    )
                )
                state = next_state
                event_index += 1

                if abs(distance_residual_m) > control.residual_absolute_tolerance:
                    raise DigitalRaceNumericalError(
                        "distance accounting residual exceeded tolerance"
                    )
                if abs(energy_residual_j) > control.residual_absolute_tolerance:
                    raise DigitalRaceNumericalError(
                        "energy accounting residual exceeded tolerance"
                    )
                if event_name == "finished":
                    return finish("finished", "none", "published race distance reached")
                if event_name == "reliability":
                    return finish(
                        "failed",
                        "reliability",
                        "seeded reliability failure occurred during an event",
                    )
                if event_name == "damage":
                    return finish("failed", "damage", "damage limit reached")
                if event_name == "degradation":
                    return finish(
                        "failed", "degradation", "degradation limit reached"
                    )
                if event_name == "depleted":
                    return finish(
                        "depleted",
                        "energy",
                        "onboard primary energy exhausted before finish",
                    )
                if event_name == "timeout":
                    return finish("timeout", "timeout", "race timeout reached")

        raise DigitalRaceNumericalError(
            "all declared race events completed without a finish outcome"
        )
    except (DigitalRaceNumericalError, OverflowError, ZeroDivisionError) as exc:
        return finish("invalid", "numerical", f"runtime numerical failure: {exc}")
