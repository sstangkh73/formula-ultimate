"""Validate Work 018 suspension, brake, regen, and failure references."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.suspension_braking import (  # noqa: E402
    BrakeParameters,
    RegenerationParameters,
    SuspensionBrakeModule,
    SuspensionBrakeState,
    SuspensionBrakeStepInput,
    SuspensionParameters,
    evaluate_suspension_brake_step,
)
from formula_ultimate.physics.thermal import ThermalParameters  # noqa: E402


SUSPENSION = SuspensionParameters(100.0, 10_000.0, 0.0, 1_000.0, 0.1, 0.1)
THERMAL = ThermalParameters(1_000.0, 0.0, 0.0, 370.0, 400.0)
REGEN = RegenerationParameters(100.0, 2_000.0, 1_600.0, 10_000.0, 0.8, 1.0)


def build_module(regeneration: RegenerationParameters = REGEN) -> SuspensionBrakeModule:
    return SuspensionBrakeModule(
        "work018-reference",
        SUSPENSION,
        BrakeParameters(0.3, 1.0, 200.0, THERMAL),
        regeneration,
    )


def state(*, velocity: float = 0.0, temperature: float = 300.0) -> SuspensionBrakeState:
    return SuspensionBrakeState(0.0, 0.0, velocity, temperature, 0.0)


def input_(duration: float, torque: float) -> SuspensionBrakeStepInput:
    return SuspensionBrakeStepInput(duration, 1_000.0, 10.0, torque, 300.0)


def main() -> int:
    ordinary = evaluate_suspension_brake_step(
        module=build_module(), state=state(), step_input=input_(1.0, 150.0)
    )
    travel_failure = evaluate_suspension_brake_step(
        module=build_module(),
        state=state(velocity=0.02),
        step_input=input_(10.0, 0.0),
    )
    no_regen = RegenerationParameters(0.0, 0.0, 0.0, 10_000.0, 0.8)
    thermal_failure = evaluate_suspension_brake_step(
        module=build_module(no_regen),
        state=state(temperature=350.0),
        step_input=input_(100.0, 100.0),
    )
    replay = evaluate_suspension_brake_step(
        module=build_module(), state=state(), step_input=input_(1.0, 150.0)
    )
    tyre_limit_module = SuspensionBrakeModule(
        "work018-tyre-limit-reference",
        SuspensionParameters(100.0, 10_000.0, 0.0, 100.0, 0.1, 0.1),
        BrakeParameters(0.3, 1.0, 200.0, THERMAL),
        REGEN,
    )
    tyre_limited = evaluate_suspension_brake_step(
        module=tyre_limit_module,
        state=state(),
        step_input=SuspensionBrakeStepInput(1.0, 100.0, 10.0, 150.0, 300.0),
    )

    if ordinary.status != "ok":
        raise RuntimeError(f"ordinary reference failed: {ordinary.reason}")
    if ordinary.residuals is None or ordinary.residuals.brake_energy_j != 0.0:
        raise RuntimeError("ordinary energy balance did not close")
    if travel_failure.failure_mode != "suspension_travel":
        raise RuntimeError("travel failure did not localize")
    if thermal_failure.failure_mode != "brake_overtemperature":
        raise RuntimeError("thermal failure did not localize")
    if ordinary != replay:
        raise RuntimeError("identical reference inputs did not replay exactly")
    if tyre_limited.applied_total_brake_torque_n_m != 30.0:
        raise RuntimeError("tyre-limited reference did not respect mu*Fz*R")

    print(
        json.dumps(
            {
                "ordinary_braking": {
                    "status": ordinary.status,
                    "applied_regen_torque_n_m": ordinary.applied_regen_torque_n_m,
                    "applied_mechanical_torque_n_m": ordinary.applied_mechanical_torque_n_m,
                    "wheel_energy_removed_j": ordinary.wheel_energy_removed_j,
                    "recovered_storage_energy_j": ordinary.recovered_storage_energy_j,
                    "regenerative_conversion_loss_j": ordinary.regenerative_conversion_loss_j,
                    "mechanical_brake_heat_j": ordinary.mechanical_brake_heat_j,
                    "end_brake_temperature_k": ordinary.end_state.brake_temperature_k,
                    "residuals": asdict(ordinary.residuals),
                },
                "suspension_failure": {
                    "failure_mode": travel_failure.failure_mode,
                    "executed_duration_s": travel_failure.executed_duration_s,
                    "unexecuted_duration_s": travel_failure.unexecuted_duration_s,
                    "end_travel_m": travel_failure.end_state.suspension_travel_m,
                },
                "thermal_failure": {
                    "failure_mode": thermal_failure.failure_mode,
                    "executed_duration_s": thermal_failure.executed_duration_s,
                    "unexecuted_duration_s": thermal_failure.unexecuted_duration_s,
                    "end_temperature_k": thermal_failure.end_state.brake_temperature_k,
                    "mechanical_brake_heat_j": thermal_failure.mechanical_brake_heat_j,
                    "energy_residual_j": thermal_failure.residuals.brake_energy_j,
                },
                "tyre_limit": {
                    "limit_n_m": tyre_limited.tyre_torque_limit_n_m,
                    "scale": tyre_limited.tyre_limit_scale,
                    "applied_total_n_m": tyre_limited.applied_total_brake_torque_n_m,
                    "unserved_n_m": tyre_limited.unserved_brake_torque_n_m,
                },
                "replay_equal": ordinary == replay,
                "claim_boundary": "Level-0 contact interval; not vehicle braking validation",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
