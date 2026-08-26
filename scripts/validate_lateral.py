"""Validate Work 016 planar dynamics, load transfer, and falsification cases."""

from __future__ import annotations

from dataclasses import asdict, replace
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.lateral import (  # noqa: E402
    PlanarContact,
    PlanarSolverControl,
    PlanarState,
    PlanarVehicle,
    PlanarVehicleParameters,
    solve_quasi_static_normal_loads,
    step_planar_dynamics,
)
from formula_ultimate.physics.tyre import TyreContactParameters  # noqa: E402


def build_vehicle(*, steer_rad: float = 0.0, fx_n: float = 0.0) -> PlanarVehicle:
    mass = 1_200.0
    load = mass * 9.81 / 4.0
    tyre = TyreContactParameters(1.2, 1.1)

    def make(contact_id: str, x_m: float, y_m: float, steer: float) -> PlanarContact:
        return PlanarContact(
            contact_id,
            x_m,
            y_m,
            load,
            steer,
            20_000.0,
            fx_n,
            tyre,
        )

    return PlanarVehicle(
        "work016-reference",
        PlanarVehicleParameters(mass, 1_800.0, 0.5),
        (
            make("front-left", 1.5, 0.8, steer_rad),
            make("front-right", 1.5, -0.8, steer_rad),
            make("rear-left", -1.5, 0.8, 0.0),
            make("rear-right", -1.5, -0.8, 0.0),
        ),
    )


def initial_state() -> PlanarState:
    return PlanarState(0.0, 0.0, 0.0, 0.0, 20.0, 0.0, 0.0)


def main() -> int:
    control = PlanarSolverControl(time_step_s=0.01)
    steady = step_planar_dynamics(
        vehicle=build_vehicle(), state=initial_state(), control=control
    )
    transient = step_planar_dynamics(
        vehicle=build_vehicle(steer_rad=0.02),
        state=initial_state(),
        control=control,
    )
    replay = step_planar_dynamics(
        vehicle=build_vehicle(steer_rad=0.02),
        state=initial_state(),
        control=control,
    )
    transfer = solve_quasi_static_normal_loads(
        vehicle=build_vehicle(),
        longitudinal_acceleration_m_per_s2=2.0,
        lateral_acceleration_m_per_s2=3.0,
    )
    saturated = step_planar_dynamics(
        vehicle=build_vehicle(steer_rad=0.2, fx_n=5_000.0),
        state=replace(initial_state(), longitudinal_velocity_m_per_s=25.0),
        control=PlanarSolverControl(
            time_step_s=0.01,
            max_load_iterations=256,
            relaxation_factor=0.25,
        ),
    )
    no_convergence = step_planar_dynamics(
        vehicle=build_vehicle(steer_rad=0.03),
        state=initial_state(),
        control=PlanarSolverControl(time_step_s=0.01, max_load_iterations=1),
    )

    if steady.status != "ok" or steady.load_iterations != 1:
        raise RuntimeError("steady reference did not converge in one iteration")
    if transient.status != "ok":
        raise RuntimeError(f"transient reference failed: {transient.reason}")
    if transient.lateral_acceleration_m_per_s2 <= 0.0:  # type: ignore[operator]
        raise RuntimeError("positive steer did not produce positive lateral response")
    if transient.yaw_acceleration_rad_per_s2 <= 0.0:  # type: ignore[operator]
        raise RuntimeError("positive steer did not produce positive yaw response")
    if transient != replay:
        raise RuntimeError("identical transient inputs did not replay exactly")
    if transfer.status != "ok" or transfer.residuals is None:
        raise RuntimeError("analytical load-transfer reference failed")
    if saturated.status != "ok" or saturated.saturated_contact_count == 0:
        raise RuntimeError("combined-force saturation reference failed")
    if no_convergence.status != "invalid":
        raise RuntimeError("insufficient iteration budget was silently accepted")

    front_load = sum(transfer.normal_loads_n[:2])
    rear_load = sum(transfer.normal_loads_n[2:])
    left_load = transfer.normal_loads_n[0] + transfer.normal_loads_n[2]
    right_load = transfer.normal_loads_n[1] + transfer.normal_loads_n[3]
    print(
        json.dumps(
            {
                "steady_reference": {
                    "status": steady.status,
                    "iterations": steady.load_iterations,
                    "longitudinal_acceleration_m_per_s2": steady.longitudinal_acceleration_m_per_s2,
                    "lateral_acceleration_m_per_s2": steady.lateral_acceleration_m_per_s2,
                    "yaw_acceleration_rad_per_s2": steady.yaw_acceleration_rad_per_s2,
                    "residuals": asdict(steady.residuals) if steady.residuals else None,
                },
                "steering_transient": {
                    "status": transient.status,
                    "iterations": transient.load_iterations,
                    "lateral_acceleration_m_per_s2": transient.lateral_acceleration_m_per_s2,
                    "yaw_acceleration_rad_per_s2": transient.yaw_acceleration_rad_per_s2,
                    "saturated_contacts": transient.saturated_contact_count,
                    "replay_equal": transient == replay,
                    "residuals": asdict(transient.residuals) if transient.residuals else None,
                },
                "load_transfer": {
                    "status": transfer.status,
                    "front_load_n": front_load,
                    "rear_load_n": rear_load,
                    "left_load_n": left_load,
                    "right_load_n": right_load,
                    "residuals": asdict(transfer.residuals),
                },
                "combined_force": {
                    "status": saturated.status,
                    "saturated_contacts": saturated.saturated_contact_count,
                    "maximum_applied_utilization": max(
                        item.tyre_force.applied_utilization or 0.0
                        for item in saturated.contact_results
                    ),
                },
                "falsification": {
                    "one_iteration_status": no_convergence.status,
                    "one_iteration_reason": no_convergence.reason,
                },
                "claim_boundary": "Level-0 analytical and deterministic verification only",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
