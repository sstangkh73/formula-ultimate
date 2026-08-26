"""Validate Work 014 analytical thermal references and failure behavior."""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.thermal import (  # noqa: E402
    ThermalParameters,
    ThermalState,
    ThermalStepInput,
    step_thermal_state,
)


def run(params, temperature_k, **inputs):
    return step_thermal_state(
        parameters=params,
        state=ThermalState(0.0, temperature_k),
        step_input=ThermalStepInput(**inputs),
    )


def main() -> int:
    base = ThermalParameters(1_000.0, 0.0, 0.0, 370.0, 400.0)
    heating = run(base, 300.0, duration_s=10.0, heat_generation_w=100.0,
                  ambient_temperature_k=300.0, active_cooling_command=0.0)
    cooldown = run(ThermalParameters(1_000.0, 100.0, 0.0, 370.0, 400.0), 390.0,
                   duration_s=10.0, heat_generation_w=0.0,
                   ambient_temperature_k=300.0, active_cooling_command=0.0)
    failure = run(base, 350.0, duration_s=100.0, heat_generation_w=1_000.0,
                  ambient_temperature_k=300.0, active_cooling_command=0.0)
    expected_cooldown = 300.0 + 90.0 * math.exp(-1.0)
    if abs(heating.end_state.temperature_k - 301.0) > 1.0e-12:
        raise RuntimeError("adiabatic heating reference mismatch")
    if abs(cooldown.end_state.temperature_k - expected_cooldown) > 1.0e-12:
        raise RuntimeError("Newton cooldown reference mismatch")
    if failure.status != "failed" or failure.executed_duration_s != 50.0:
        raise RuntimeError("failure event reference mismatch")
    print(json.dumps({
        "adiabatic_heating": {
            "end_temperature_k": heating.end_state.temperature_k,
            "energy_residual_j": heating.energy_residual_j,
        },
        "newton_cooldown": {
            "end_temperature_k": cooldown.end_state.temperature_k,
            "analytical_temperature_k": expected_cooldown,
            "energy_residual_j": cooldown.energy_residual_j,
        },
        "failure_event": {
            "status": failure.status,
            "failure_time_s": failure.failure_time_s,
            "executed_duration_s": failure.executed_duration_s,
            "unexecuted_duration_s": failure.unexecuted_duration_s,
            "end_temperature_k": failure.end_state.temperature_k,
            "latched": failure.end_state.failed,
        },
        "temperature_silently_clipped": False,
        "claim_boundary": "Level-0 analytical verification only",
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
