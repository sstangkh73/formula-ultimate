"""Validate Work 019 multi-event strategy and seeded reliability evidence."""

from __future__ import annotations

import json
import math
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.circuit import load_circuit_catalog  # noqa: E402
from formula_ultimate.physics.digital_race import (  # noqa: E402
    DigitalRaceControl,
    DigitalRaceScenario,
    DigitalRaceSector,
    DigitalRaceStrategy,
    DigitalRaceVehicle,
    LapStrategyCommand,
    TrafficCondition,
    TrafficEvent,
    WeatherCondition,
    WeatherEvent,
    run_digital_race,
)


def race_sectors(**overrides):
    values = dict(
        base_speed_mps=90.0,
        base_energy_j_per_m=1_000.0,
        degradation_per_m=1.0e-9,
        damage_per_m=5.0e-10,
    )
    values.update(overrides)
    return tuple(
        DigitalRaceSector(f"sector-{index}", fraction, **values)
        for index, fraction in enumerate((0.2, 0.3, 0.5))
    )


def race_strategy(circuit, pace=1.0):
    return DigitalRaceStrategy(
        f"pace-{pace}",
        tuple(
            LapStrategyCommand(f"lap-{lap_index}", pace)
            for lap_index in range(circuit.race_laps)
        ),
    )


def race_scenario(circuit, **overrides):
    values = dict(
        scenario_id="validator-scenario",
        sectors=race_sectors(),
        strategy=race_strategy(circuit),
    )
    values.update(overrides)
    return DigitalRaceScenario(**values)


def race_vehicle(**overrides):
    values = dict(
        vehicle_id="validator-vehicle",
        initial_onboard_energy_j=1.0e10,
        auxiliary_power_w=500.0,
        initial_degradation=0.0,
        degradation_limit=1.0,
        degradation_speed_loss_per_unit=0.2,
        initial_damage=0.0,
        damage_limit=1.0,
        base_reliability_hazard_per_s=0.0,
        hazard_degradation_coefficient=1.0,
        hazard_damage_coefficient=1.0,
        hazard_pace_exponent=3.0,
    )
    values.update(overrides)
    return DigitalRaceVehicle(**values)


def race_control(**overrides):
    values = dict(timeout_s=1.0e6, random_seed=17)
    values.update(overrides)
    return DigitalRaceControl(**values)


def main() -> int:
    circuits = load_circuit_catalog(
        ROOT / "config" / "circuits" / "real_circuits_v1.json"
    )
    finishes = {}
    replay_equal = True
    energy_monotonic = True
    for circuit in circuits:
        scenario = race_scenario(circuit)
        first = run_digital_race(
            circuit=circuit,
            scenario=scenario,
            vehicle=race_vehicle(),
            control=race_control(),
        )
        second = run_digital_race(
            circuit=circuit,
            scenario=scenario,
            vehicle=race_vehicle(),
            control=race_control(),
        )
        replay_equal = replay_equal and first == second
        energy_values = [race_vehicle().initial_onboard_energy_j] + [
            event.end_remaining_energy_j for event in first.telemetry
        ]
        energy_monotonic = energy_monotonic and all(
            after <= before for before, after in zip(energy_values, energy_values[1:])
        )
        finishes[circuit.circuit_id] = {
            "outcome": first.outcome,
            "time_s": first.final_state.time_s,
            "completed_laps": first.final_state.completed_laps,
            "events": first.final_state.completed_events,
            "distance_residual_m": first.finish_distance_residual_m,
            "official_final_adjustment_m": (
                first.telemetry[-1].official_distance_adjustment_m
            ),
            "energy_residual_j": first.total_energy_accounting_residual_j,
        }

    reference = circuits[0]
    conservative = run_digital_race(
        circuit=reference,
        scenario=race_scenario(
            reference, strategy=race_strategy(reference, pace=0.8)
        ),
        vehicle=race_vehicle(base_reliability_hazard_per_s=1.0e-12),
        control=race_control(random_seed=8),
    )
    aggressive = run_digital_race(
        circuit=reference,
        scenario=race_scenario(
            reference, strategy=race_strategy(reference, pace=1.2)
        ),
        vehicle=race_vehicle(base_reliability_hazard_per_s=1.0e-12),
        control=race_control(random_seed=8),
    )
    baseline = run_digital_race(
        circuit=reference,
        scenario=race_scenario(reference),
        vehicle=race_vehicle(auxiliary_power_w=0.0),
        control=race_control(),
    )
    traffic = run_digital_race(
        circuit=reference,
        scenario=race_scenario(
            reference,
            traffic_events=(
                TrafficEvent(0, 0, TrafficCondition("queue", delay_s=7.5)),
            ),
        ),
        vehicle=race_vehicle(auxiliary_power_w=0.0),
        control=race_control(),
    )
    wet = run_digital_race(
        circuit=reference,
        scenario=race_scenario(
            reference,
            weather_events=(
                WeatherEvent(
                    0,
                    0,
                    WeatherCondition(
                        "wet",
                        speed_multiplier=0.7,
                        energy_multiplier=1.2,
                        degradation_multiplier=1.4,
                        damage_multiplier=1.1,
                        reliability_multiplier=1.3,
                    ),
                ),
            ),
        ),
        vehicle=race_vehicle(auxiliary_power_w=0.0),
        control=race_control(),
    )

    seed = 23
    expected_draw = random.Random(seed).random()
    expected_failure_time_s = -math.log1p(-expected_draw)
    reliability = run_digital_race(
        circuit=reference,
        scenario=race_scenario(
            reference,
            sectors=race_sectors(degradation_per_m=0.0, damage_per_m=0.0),
        ),
        vehicle=race_vehicle(
            auxiliary_power_w=0.0,
            base_reliability_hazard_per_s=1.0,
        ),
        control=race_control(random_seed=seed),
    )
    depleted = run_digital_race(
        circuit=reference,
        scenario=race_scenario(reference),
        vehicle=race_vehicle(initial_onboard_energy_j=1_000.0),
        control=race_control(),
    )
    degraded = run_digital_race(
        circuit=reference,
        scenario=race_scenario(
            reference,
            sectors=race_sectors(degradation_per_m=1.0e-3, damage_per_m=0.0),
        ),
        vehicle=race_vehicle(degradation_limit=0.1, auxiliary_power_w=0.0),
        control=race_control(),
    )
    damaged = run_digital_race(
        circuit=reference,
        scenario=race_scenario(
            reference,
            sectors=race_sectors(degradation_per_m=0.0, damage_per_m=1.0e-3),
        ),
        vehicle=race_vehicle(damage_limit=0.2, auxiliary_power_w=0.0),
        control=race_control(),
    )
    timed_out = run_digital_race(
        circuit=reference,
        scenario=race_scenario(reference),
        vehicle=race_vehicle(auxiliary_power_w=0.0),
        control=race_control(timeout_s=2.5),
    )
    invalid = run_digital_race(
        circuit=reference,
        scenario=race_scenario(reference),
        vehicle=race_vehicle(
            initial_degradation=0.5,
            degradation_speed_loss_per_unit=3.0,
        ),
        control=race_control(),
    )

    if len(circuits) != 10 or any(
        evidence["outcome"] != "finished" for evidence in finishes.values()
    ):
        raise RuntimeError("not all ten real-circuit digital races finished")
    if not replay_equal or not energy_monotonic:
        raise RuntimeError("replay or onboard-energy monotonicity failed")
    if not (
        aggressive.final_state.time_s < conservative.final_state.time_s
        and aggressive.consumed_energy_j > conservative.consumed_energy_j
        and aggressive.final_state.degradation > conservative.final_state.degradation
        and aggressive.final_state.damage > conservative.final_state.damage
    ):
        raise RuntimeError("strategy trade-off direction failed")
    if not (
        math.isclose(traffic.final_state.time_s - baseline.final_state.time_s, 7.5)
        and wet.final_state.time_s > baseline.final_state.time_s
        and wet.consumed_energy_j > baseline.consumed_energy_j
    ):
        raise RuntimeError("traffic or weather reference direction failed")
    if not (
        reliability.failure_mode == "reliability"
        and math.isclose(reliability.final_state.time_s, expected_failure_time_s)
    ):
        raise RuntimeError("seeded reliability localization failed")
    terminal = {
        "depleted": (depleted.outcome, depleted.failure_mode),
        "degradation": (degraded.outcome, degraded.failure_mode),
        "damage": (damaged.outcome, damaged.failure_mode),
        "timeout": (timed_out.outcome, timed_out.failure_mode),
        "invalid": (invalid.outcome, invalid.failure_mode),
    }
    expected_terminal = {
        "depleted": ("depleted", "energy"),
        "degradation": ("failed", "degradation"),
        "damage": ("failed", "damage"),
        "timeout": ("timeout", "timeout"),
        "invalid": ("invalid", "numerical"),
    }
    if terminal != expected_terminal:
        raise RuntimeError(f"terminal outcome mismatch: {terminal!r}")

    print(
        json.dumps(
            {
                "schema_version": "1.0",
                "ten_circuit_finishes": finishes,
                "replay_equal": replay_equal,
                "energy_monotonic": energy_monotonic,
                "strategy_tradeoff": {
                    "conservative_time_s": conservative.final_state.time_s,
                    "aggressive_time_s": aggressive.final_state.time_s,
                    "conservative_energy_j": conservative.consumed_energy_j,
                    "aggressive_energy_j": aggressive.consumed_energy_j,
                    "conservative_degradation": conservative.final_state.degradation,
                    "aggressive_degradation": aggressive.final_state.degradation,
                    "conservative_damage": conservative.final_state.damage,
                    "aggressive_damage": aggressive.final_state.damage,
                },
                "environment": {
                    "traffic_delay_delta_s": (
                        traffic.final_state.time_s - baseline.final_state.time_s
                    ),
                    "wet_time_delta_s": wet.final_state.time_s - baseline.final_state.time_s,
                    "wet_energy_delta_j": wet.consumed_energy_j - baseline.consumed_energy_j,
                },
                "seeded_reliability": {
                    "seed": seed,
                    "draw": reliability.telemetry[0].reliability_draw,
                    "expected_time_s": expected_failure_time_s,
                    "actual_time_s": reliability.final_state.time_s,
                },
                "terminal_outcomes": terminal,
                "energy_replenishment_events": 0,
                "claim_boundary": (
                    "Level-0 strategy and failure-selection evidence only"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
