from __future__ import annotations

import math
from pathlib import Path
import random
import unittest

from formula_ultimate.physics.circuit import load_circuit_catalog
from formula_ultimate.physics.digital_race import (
    DigitalRaceControl,
    DigitalRaceInputError,
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


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "config" / "circuits" / "real_circuits_v1.json"


def sectors(**overrides) -> tuple[DigitalRaceSector, ...]:
    values = {
        "base_speed_mps": 90.0,
        "base_energy_j_per_m": 1_000.0,
        "degradation_per_m": 1.0e-9,
        "damage_per_m": 5.0e-10,
    }
    values.update(overrides)
    return tuple(
        DigitalRaceSector(
            sector_id=f"sector-{index}",
            lap_fraction=fraction,
            **values,
        )
        for index, fraction in enumerate((0.2, 0.3, 0.5))
    )


def strategy(circuit, pace: float = 1.0) -> DigitalRaceStrategy:
    return DigitalRaceStrategy(
        strategy_id=f"pace-{pace}",
        lap_commands=tuple(
            LapStrategyCommand(f"lap-{lap_index}", pace)
            for lap_index in range(circuit.race_laps)
        ),
    )


def scenario(circuit, **overrides) -> DigitalRaceScenario:
    values = {
        "scenario_id": "reference-scenario",
        "sectors": sectors(),
        "strategy": strategy(circuit),
    }
    values.update(overrides)
    return DigitalRaceScenario(**values)


def vehicle(**overrides) -> DigitalRaceVehicle:
    values = {
        "vehicle_id": "reference-vehicle",
        "initial_onboard_energy_j": 1.0e10,
        "auxiliary_power_w": 500.0,
        "initial_degradation": 0.0,
        "degradation_limit": 1.0,
        "degradation_speed_loss_per_unit": 0.2,
        "initial_damage": 0.0,
        "damage_limit": 1.0,
        "base_reliability_hazard_per_s": 0.0,
        "hazard_degradation_coefficient": 1.0,
        "hazard_damage_coefficient": 1.0,
        "hazard_pace_exponent": 3.0,
    }
    values.update(overrides)
    return DigitalRaceVehicle(**values)


def control(**overrides) -> DigitalRaceControl:
    values = {"timeout_s": 1.0e6, "random_seed": 17}
    values.update(overrides)
    return DigitalRaceControl(**values)


class DigitalRaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.circuits = load_circuit_catalog(CATALOG)
        cls.reference = cls.circuits[0]

    def test_all_ten_real_profiles_finish_and_replay_exactly(self) -> None:
        self.assertEqual(10, len(self.circuits))
        for circuit in self.circuits:
            with self.subTest(circuit=circuit.circuit_id):
                race_scenario = scenario(circuit)
                first = run_digital_race(
                    circuit=circuit,
                    scenario=race_scenario,
                    vehicle=vehicle(),
                    control=control(),
                )
                second = run_digital_race(
                    circuit=circuit,
                    scenario=race_scenario,
                    vehicle=vehicle(),
                    control=control(),
                )
                self.assertEqual(first, second)
                self.assertEqual("finished", first.outcome)
                self.assertEqual(circuit.race_distance_m, first.final_state.distance_m)
                expected_events = circuit.race_laps * len(race_scenario.sectors)
                self.assertEqual(expected_events, first.final_state.completed_events)
                self.assertEqual(circuit.race_laps, first.final_state.completed_laps)
                self.assertEqual(expected_events, first.replay.stochastic_draw_count)
                self.assertLessEqual(
                    abs(first.total_energy_accounting_residual_j)
                    / vehicle().initial_onboard_energy_j,
                    2.0e-15,
                )
                self.assertTrue(
                    all(
                        abs(item.energy_accounting_residual_j) <= 1.0e-8
                        for item in first.telemetry
                    )
                )
                adjustments = [
                    item.official_distance_adjustment_m for item in first.telemetry
                ]
                self.assertTrue(all(value == 0.0 for value in adjustments[:-1]))
                self.assertAlmostEqual(circuit.race_start_offset_m, adjustments[-1])

    def test_aggressive_strategy_is_faster_but_costlier_and_riskier(self) -> None:
        conservative = run_digital_race(
            circuit=self.reference,
            scenario=scenario(
                self.reference, strategy=strategy(self.reference, pace=0.8)
            ),
            vehicle=vehicle(base_reliability_hazard_per_s=1.0e-12),
            control=control(random_seed=8),
        )
        aggressive = run_digital_race(
            circuit=self.reference,
            scenario=scenario(
                self.reference, strategy=strategy(self.reference, pace=1.2)
            ),
            vehicle=vehicle(base_reliability_hazard_per_s=1.0e-12),
            control=control(random_seed=8),
        )
        self.assertEqual("finished", conservative.outcome)
        self.assertEqual("finished", aggressive.outcome)
        self.assertLess(aggressive.final_state.time_s, conservative.final_state.time_s)
        self.assertGreater(aggressive.consumed_energy_j, conservative.consumed_energy_j)
        self.assertGreater(
            aggressive.final_state.degradation, conservative.final_state.degradation
        )
        self.assertGreater(aggressive.final_state.damage, conservative.final_state.damage)
        self.assertGreater(
            aggressive.telemetry[0].reliability_hazard_per_s,
            conservative.telemetry[0].reliability_hazard_per_s,
        )

    def test_traffic_delay_and_weather_effects_are_observable(self) -> None:
        baseline = run_digital_race(
            circuit=self.reference,
            scenario=scenario(self.reference),
            vehicle=vehicle(auxiliary_power_w=0.0),
            control=control(),
        )
        traffic = run_digital_race(
            circuit=self.reference,
            scenario=scenario(
                self.reference,
                traffic_events=(
                    TrafficEvent(0, 0, TrafficCondition("queue", delay_s=7.5)),
                ),
            ),
            vehicle=vehicle(auxiliary_power_w=0.0),
            control=control(),
        )
        wet = run_digital_race(
            circuit=self.reference,
            scenario=scenario(
                self.reference,
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
            vehicle=vehicle(auxiliary_power_w=0.0),
            control=control(),
        )
        self.assertAlmostEqual(7.5, traffic.final_state.time_s - baseline.final_state.time_s)
        self.assertGreater(wet.final_state.time_s, baseline.final_state.time_s)
        self.assertGreater(wet.consumed_energy_j, baseline.consumed_energy_j)
        self.assertGreater(wet.final_state.degradation, baseline.final_state.degradation)
        self.assertEqual("wet", wet.telemetry[0].weather_condition_id)
        self.assertEqual("queue", traffic.telemetry[0].traffic_condition_id)

    def test_seeded_reliability_failure_is_analytically_localized(self) -> None:
        seed = 23
        hazard = 1.0
        expected_draw = random.Random(seed).random()
        expected_time_s = -math.log1p(-expected_draw) / hazard
        result = run_digital_race(
            circuit=self.reference,
            scenario=scenario(
                self.reference,
                sectors=sectors(
                    degradation_per_m=0.0,
                    damage_per_m=0.0,
                ),
            ),
            vehicle=vehicle(
                auxiliary_power_w=0.0,
                base_reliability_hazard_per_s=hazard,
            ),
            control=control(random_seed=seed),
        )
        self.assertEqual("failed", result.outcome)
        self.assertEqual("reliability", result.failure_mode)
        self.assertEqual(1, result.replay.stochastic_draw_count)
        self.assertAlmostEqual(expected_draw, result.telemetry[0].reliability_draw)
        self.assertAlmostEqual(expected_time_s, result.final_state.time_s)
        self.assertAlmostEqual(
            result.telemetry[0].average_progress_speed_mps * expected_time_s,
            result.final_state.distance_m,
        )

    def test_different_seeds_change_uncertain_failure_trace(self) -> None:
        results = tuple(
            run_digital_race(
                circuit=self.reference,
                scenario=scenario(self.reference),
                vehicle=vehicle(base_reliability_hazard_per_s=1.0),
                control=control(random_seed=seed),
            )
            for seed in (1, 2)
        )
        self.assertTrue(all(result.failure_mode == "reliability" for result in results))
        self.assertNotEqual(
            results[0].telemetry[0].reliability_draw,
            results[1].telemetry[0].reliability_draw,
        )
        self.assertNotEqual(results[0].final_state.time_s, results[1].final_state.time_s)

    def test_depletion_degradation_damage_and_timeout_are_localized(self) -> None:
        depleted = run_digital_race(
            circuit=self.reference,
            scenario=scenario(self.reference),
            vehicle=vehicle(initial_onboard_energy_j=1_000.0),
            control=control(),
        )
        degraded = run_digital_race(
            circuit=self.reference,
            scenario=scenario(
                self.reference,
                sectors=sectors(degradation_per_m=1.0e-3, damage_per_m=0.0),
            ),
            vehicle=vehicle(degradation_limit=0.1, auxiliary_power_w=0.0),
            control=control(),
        )
        damaged = run_digital_race(
            circuit=self.reference,
            scenario=scenario(
                self.reference,
                sectors=sectors(degradation_per_m=0.0, damage_per_m=1.0e-3),
            ),
            vehicle=vehicle(damage_limit=0.2, auxiliary_power_w=0.0),
            control=control(),
        )
        timed_out = run_digital_race(
            circuit=self.reference,
            scenario=scenario(self.reference),
            vehicle=vehicle(auxiliary_power_w=0.0),
            control=control(timeout_s=2.5),
        )
        self.assertEqual(("depleted", "energy"), (depleted.outcome, depleted.failure_mode))
        self.assertEqual(0.0, depleted.final_state.remaining_energy_j)
        self.assertEqual(("failed", "degradation"), (degraded.outcome, degraded.failure_mode))
        self.assertAlmostEqual(0.1, degraded.final_state.degradation)
        self.assertAlmostEqual(100.0, degraded.final_state.distance_m)
        self.assertEqual(("failed", "damage"), (damaged.outcome, damaged.failure_mode))
        self.assertAlmostEqual(0.2, damaged.final_state.damage)
        self.assertAlmostEqual(200.0, damaged.final_state.distance_m)
        self.assertEqual(("timeout", "timeout"), (timed_out.outcome, timed_out.failure_mode))
        self.assertEqual(2.5, timed_out.final_state.time_s)

    def test_energy_never_increases_and_finish_wins_exact_final_tie(self) -> None:
        race_sectors = sectors(
            degradation_per_m=0.0,
            damage_per_m=0.0,
            base_energy_j_per_m=1_000.0,
        )
        exact_energy_j = self.reference.race_distance_m * 1_000.0
        result = run_digital_race(
            circuit=self.reference,
            scenario=scenario(self.reference, sectors=race_sectors),
            vehicle=vehicle(
                initial_onboard_energy_j=exact_energy_j,
                auxiliary_power_w=0.0,
                degradation_speed_loss_per_unit=0.0,
            ),
            control=control(),
        )
        self.assertEqual("finished", result.outcome)
        energies = [exact_energy_j] + [
            item.end_remaining_energy_j for item in result.telemetry
        ]
        self.assertTrue(all(after <= before for before, after in zip(energies, energies[1:])))
        self.assertAlmostEqual(0.0, result.final_state.remaining_energy_j, places=6)
        self.assertAlmostEqual(0.0, result.total_energy_accounting_residual_j, places=6)
        self.assertTrue(
            all(abs(item.energy_accounting_residual_j) <= 1.0e-8 for item in result.telemetry)
        )

    def test_invalid_contracts_fail_before_execution(self) -> None:
        invalid = (
            lambda: DigitalRaceSector("", 1.0, 1.0, 0.0, 0.0, 0.0),
            lambda: DigitalRaceSector("s", 0.0, 1.0, 0.0, 0.0, 0.0),
            lambda: LapStrategyCommand("c", math.nan),
            lambda: WeatherCondition("wet", speed_multiplier=0.0),
            lambda: TrafficCondition("traffic", delay_s=-1.0),
            lambda: DigitalRaceScenario(
                "bad-fractions",
                (DigitalRaceSector("s", 0.5, 1.0, 0.0, 0.0, 0.0),),
                strategy(self.reference),
            ),
            lambda: scenario(
                self.reference,
                weather_events=(
                    WeatherEvent(0, 0, WeatherCondition("a")),
                    WeatherEvent(0, 0, WeatherCondition("b")),
                ),
            ),
            lambda: vehicle(initial_degradation=1.0),
            lambda: control(random_seed=True),
        )
        for constructor in invalid:
            with self.subTest(constructor=constructor):
                with self.assertRaises(DigitalRaceInputError):
                    constructor()

        wrong_lap_count = DigitalRaceScenario(
            "wrong-laps",
            sectors(),
            DigitalRaceStrategy("short", (LapStrategyCommand("only", 1.0),)),
        )
        with self.assertRaises(DigitalRaceInputError):
            run_digital_race(
                circuit=self.reference,
                scenario=wrong_lap_count,
                vehicle=vehicle(),
                control=control(),
            )
        with self.assertRaises(DigitalRaceInputError):
            run_digital_race(
                circuit=self.reference,
                scenario=scenario(
                    self.reference,
                    traffic_events=(
                        TrafficEvent(
                            self.reference.race_laps,
                            0,
                            TrafficCondition("outside"),
                        ),
                    ),
                ),
                vehicle=vehicle(),
                control=control(),
            )

    def test_runtime_numerical_failure_is_observable(self) -> None:
        result = run_digital_race(
            circuit=self.reference,
            scenario=scenario(self.reference),
            vehicle=vehicle(
                initial_degradation=0.5,
                degradation_speed_loss_per_unit=3.0,
            ),
            control=control(),
        )
        self.assertEqual("invalid", result.outcome)
        self.assertEqual("numerical", result.failure_mode)
        self.assertIn("non-positive speed", result.reason)
        self.assertFalse(result.telemetry)


if __name__ == "__main__":
    unittest.main()
