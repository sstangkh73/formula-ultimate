from __future__ import annotations

import math
from dataclasses import replace
from pathlib import Path
import unittest

from formula_ultimate.physics.circuit import load_circuit_catalog
from formula_ultimate.simulation import (
    AdapterReadView, CircuitEnvironmentInputAdapter, CircuitInputScenario,
    ComponentHealthState, ContactRuntimeState, RuntimeSignal, SharedVehicleState,
    SpatialStepEvidence, StepInputError, StrategyStepCommand,
    TrafficStepEvidence, WeatherStepEvidence, resolve_step_inputs,
)

ROOT = Path(__file__).resolve().parents[1]
PROFILES = load_circuit_catalog(ROOT / "config/circuits/real_circuits_v1.json")

def state():
    return SharedVehicleState(0, 0, (0,0,0), (0,0,0), 0, 0, 1e6, 0, 0,
        (ContactRuntimeState("c", 1, 0, 0, 0, 0),),
        (ComponentHealthState("s", 300, 0, 0, False),))

def strategy(): return StrategyStepCommand(.5, 0, 0, 0)

def missing_scenario(profile):
    cid = profile.circuit_id
    return CircuitInputScenario(profile, 0,
        SpatialStepEvidence(cid, "missing", reason="no surveyed local corridor"),
        WeatherStepEvidence(cid, "missing", reason="no event-time observation"),
        TrafficStepEvidence(cid, "missing", "catalog-gap", None, "no traffic scenario"))

def ready_scenario(profile):
    cid = profile.circuit_id
    return CircuitInputScenario(profile, 10,
        SpatialStepEvidence(cid, "available", "fixture", "s1", .01, .02, .03, 5, 5, .1),
        WeatherStepEvidence(cid, "observed", "fixture", 300, 100000, .5, (1,2,0), 0, 310),
        TrafficStepEvidence(cid, "isolated_control", "fixture-control", 0))

class StepInputTests(unittest.TestCase):
    def test_all_ten_profiles_resolve_deterministically_with_explicit_gaps(self):
        self.assertEqual(10, len(PROFILES))
        first = [resolve_step_inputs(missing_scenario(p), strategy()) for p in PROFILES]
        second = [resolve_step_inputs(missing_scenario(p), strategy()) for p in reversed(PROFILES)]
        self.assertTrue(all(r.status == "incomplete" for r in first))
        self.assertTrue(all(r.missing_evidence == ("spatial","weather","traffic") for r in first))
        self.assertEqual({r.scenario.profile.circuit_id:r.fingerprint_sha256 for r in first},
                         {r.scenario.profile.circuit_id:r.fingerprint_sha256 for r in second})

    def test_complete_fixture_is_ready_and_replays(self):
        scenario = ready_scenario(PROFILES[0])
        a = resolve_step_inputs(scenario, strategy()); b = resolve_step_inputs(scenario, strategy())
        self.assertEqual("ready", a.status); self.assertEqual((), a.missing_evidence)
        self.assertEqual(a, b)

    def test_profile_content_change_under_same_id_changes_fingerprint(self):
        original = ready_scenario(PROFILES[0])
        changed_profile = replace(PROFILES[0], name=PROFILES[0].name + " revised")
        changed = CircuitInputScenario(
            changed_profile,
            original.race_distance_m,
            original.spatial,
            original.weather,
            original.traffic,
        )
        self.assertNotEqual(
            resolve_step_inputs(original, strategy()).fingerprint_sha256,
            resolve_step_inputs(changed, strategy()).fingerprint_sha256,
        )

    def test_ready_adapter_emits_exact_typed_four_signal_set(self):
        scenario = ready_scenario(PROFILES[0]); current = state()
        view = AdapterReadView("input_bridge", current, (
            RuntimeSignal("manifest.circuit_profile", scenario),
            RuntimeSignal("manifest.current_state", current),
            RuntimeSignal("manifest.strategy_command", strategy()),))
        output = CircuitEnvironmentInputAdapter().execute(view)
        self.assertEqual("ok", output.status)
        self.assertEqual({"circuit.segment_inputs","control.step_command","environment.step_inputs","state.current"},
                         {s.signal_id for s in output.signals})

    def test_incomplete_adapter_returns_no_writes(self):
        current = state(); scenario = missing_scenario(PROFILES[0])
        view = AdapterReadView("input_bridge", current, (
            RuntimeSignal("manifest.circuit_profile", scenario), RuntimeSignal("manifest.current_state", current),
            RuntimeSignal("manifest.strategy_command", strategy()),))
        output = CircuitEnvironmentInputAdapter().execute(view)
        self.assertEqual("invalid", output.status); self.assertEqual((), output.signals)
        self.assertIn("spatial", output.reason)

    def test_cross_circuit_evidence_is_rejected(self):
        with self.assertRaisesRegex(StepInputError, "must match"):
            CircuitInputScenario(PROFILES[0], 0, missing_scenario(PROFILES[1]).spatial,
                missing_scenario(PROFILES[0]).weather, missing_scenario(PROFILES[0]).traffic)

    def test_missing_records_forbid_neutral_numeric_defaults(self):
        with self.assertRaises(StepInputError):
            SpatialStepEvidence(PROFILES[0].circuit_id, "missing", curvature_1pm=0, reason="missing")
        with self.assertRaises(StepInputError):
            WeatherStepEvidence(PROFILES[0].circuit_id, "missing", air_temperature_k=288.15, reason="missing")

    def test_nonfinite_and_ranges_are_rejected(self):
        with self.assertRaises(StepInputError): StrategyStepCommand(math.nan,0,0,0)
        with self.assertRaises(StepInputError): StrategyStepCommand(0,0,2,0)
        with self.assertRaises(StepInputError): CircuitInputScenario(PROFILES[0], -1,
            missing_scenario(PROFILES[0]).spatial, missing_scenario(PROFILES[0]).weather,
            missing_scenario(PROFILES[0]).traffic)

    def test_unknown_traffic_differs_from_explicit_isolated_control(self):
        missing = missing_scenario(PROFILES[0]).traffic
        isolated = ready_scenario(PROFILES[0]).traffic
        self.assertEqual("missing", missing.mode); self.assertIsNone(missing.nearby_vehicle_count)
        self.assertEqual("isolated_control", isolated.mode); self.assertEqual(0, isolated.nearby_vehicle_count)

if __name__ == "__main__": unittest.main()
