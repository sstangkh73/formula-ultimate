"""Validate Work 015 race outcomes and ten-circuit deterministic replay."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.circuit import load_circuit_catalog  # noqa: E402
from formula_ultimate.physics.longitudinal import VehicleParameters  # noqa: E402
from formula_ultimate.physics.race import RaceControl, RaceVehicle, run_full_race  # noqa: E402
from formula_ultimate.physics.thermal import ThermalParameters  # noqa: E402


def vehicle(**overrides):
    values = dict(
        vehicle_id="validator-reference",
        longitudinal=VehicleParameters(1_000.0),
        commanded_tractive_force_n=10_000.0,
        initial_onboard_energy_j=4.0e9,
        waste_heat_power_w=0.0,
        auxiliary_power_w=0.0,
        thermal_parameters=ThermalParameters(1.0e9, 0.0, 0.0, 1_000.0, 2_000.0),
        initial_temperature_k=300.0,
    )
    values.update(overrides)
    return RaceVehicle(**values)


def control(**overrides):
    values = dict(time_step_s=10.0, timeout_s=1_000.0,
                  ambient_temperature_k=300.0, active_cooling_command=0.0,
                  random_seed=17, event_bisection_iterations=64)
    values.update(overrides)
    return RaceControl(**values)


def main() -> int:
    circuits = load_circuit_catalog(ROOT / "config" / "circuits" / "real_circuits_v1.json")
    finishes = {}
    replay_equal = True
    for circuit in circuits:
        first = run_full_race(circuit=circuit, vehicle=vehicle(), control=control())
        second = run_full_race(circuit=circuit, vehicle=vehicle(), control=control())
        replay_equal = replay_equal and first == second
        finishes[circuit.circuit_id] = {
            "outcome": first.outcome,
            "time_s": first.final_state.time_s,
            "finish_residual_m": first.finish_distance_residual_m,
        }
    reference = circuits[0]
    depleted = run_full_race(circuit=reference, vehicle=vehicle(
        commanded_tractive_force_n=1_000.0, initial_onboard_energy_j=1_000.0),
        control=control(timeout_s=100.0))
    timeout = run_full_race(circuit=reference, vehicle=vehicle(commanded_tractive_force_n=0.0),
                            control=control(time_step_s=2.0, timeout_s=5.0))
    failed = run_full_race(circuit=reference, vehicle=vehicle(
        commanded_tractive_force_n=0.0, initial_onboard_energy_j=100_000.0,
        waste_heat_power_w=1_000.0,
        thermal_parameters=ThermalParameters(1_000.0, 0.0, 0.0, 370.0, 400.0),
        initial_temperature_k=350.0), control=control(time_step_s=100.0, timeout_s=200.0))
    invalid = run_full_race(circuit=reference, vehicle=vehicle(
        commanded_tractive_force_n=0.0, initial_onboard_energy_j=1.0e308,
        waste_heat_power_w=1.0e300,
        thermal_parameters=ThermalParameters(1_000.0, 1.0e-300, 0.0, 370.0, 400.0)),
        control=control(time_step_s=1.0, timeout_s=2.0))
    tie_time_s = 10.0
    tie_force_n = 2.0 * reference.race_distance_m * 1_000.0 / tie_time_s**2
    tie = run_full_race(
        circuit=reference,
        vehicle=vehicle(
            commanded_tractive_force_n=tie_force_n,
            initial_onboard_energy_j=tie_force_n * reference.race_distance_m,
        ),
        control=control(time_step_s=tie_time_s, timeout_s=tie_time_s),
    )
    expected = ("depleted", "timeout", "failed", "invalid")
    actual = (depleted.outcome, timeout.outcome, failed.outcome, invalid.outcome)
    if len(circuits) != 10 or any(item["outcome"] != "finished" for item in finishes.values()):
        raise RuntimeError("not all ten reference circuits finished")
    if not replay_equal or actual != expected or tie.outcome != "finished":
        raise RuntimeError(f"race outcome reference mismatch: {actual!r}")
    print(json.dumps({
        "schema_version": "1.0",
        "ten_circuit_finishes": finishes,
        "replay_equal": replay_equal,
        "terminal_references": {
            "depleted": {"outcome": depleted.outcome, "remaining_energy_j": depleted.final_state.remaining_energy_j},
            "timeout": {"outcome": timeout.outcome, "time_s": timeout.final_state.time_s},
            "failed": {"outcome": failed.outcome, "time_s": failed.final_state.time_s, "temperature_k": failed.final_state.thermal_state.temperature_k},
            "invalid": {"outcome": invalid.outcome, "reason": invalid.reason},
            "exact_finish_depletion_timeout_tie": {
                "outcome": tie.outcome,
                "remaining_energy_j": tie.final_state.remaining_energy_j,
                "energy_boundary_residual_j": tie.terminal_energy_boundary_residual_j,
            },
        },
        "energy_replenishment_events": 0,
        "claim_boundary": "Level-0 total-distance completion evidence only",
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
