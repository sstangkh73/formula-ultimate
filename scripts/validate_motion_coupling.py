"""Generate deterministic Work 026 motion-coupling evidence."""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.tyre import (  # noqa: E402
    TyreContactParameters,
    TyreForceRequest,
    resolve_tyre_force,
)
from formula_ultimate.simulation import (  # noqa: E402
    AdapterReadView,
    AerodynamicChassisWrench,
    ComponentHealthState,
    ContactForceMoment,
    ContactRuntimeState,
    CoupledContactForce,
    MotionConfiguration,
    MotionCorridorReference,
    RuntimeSignal,
    SharedVehicleState,
    SpatialStepEvidence,
    VehicleMotionCouplingAdapter,
    integrate_coupled_motion,
    load_coupling_architecture,
)


def shared(*, velocity=(0.0, 0.0, 0.0), yaw_rate=0.0) -> SharedVehicleState:
    return SharedVehicleState(
        0.0, 0.0, (0.0, 0.0, 0.0), velocity, 0.0, yaw_rate,
        1.0e6, 0.0, 0,
        (ContactRuntimeState("c", 1000.0, 0.0, 0.0, 0.0, 0.0),),
        (ComponentHealthState("store", 300.0, 0.0, 0.0, False),),
    )


def aero(fx=0.0, fy=0.0, mz=0.0) -> AerodynamicChassisWrench:
    return AerodynamicChassisWrench((fx, fy, 0.0), (0.0, 0.0, mz), "map", "evidence")


def contact(fx=0.0, fy=0.0, mz=0.0) -> ContactForceMoment:
    tyre = resolve_tyre_force(
        parameters=TyreContactParameters(10.0, 10.0),
        normal_load_n=1000.0,
        request=TyreForceRequest(fx, fy),
    )
    item = CoupledContactForce(
        "c", 0.0, 0.0, 0.0, 1000.0, fx, fy, fx, fy, mz, 0.0, 0.0, tyre
    )
    return ContactForceMoment((item,), fx, fy, mz)


def spatial(width=100.0) -> SpatialStepEvidence:
    return SpatialStepEvidence(
        "fixture", "available", "analytical", "s1", 0.0, 0.0, 0.0,
        width, width, 0.0,
    )


def reference(current: SharedVehicleState) -> MotionCorridorReference:
    return MotionCorridorReference(
        "fixture", "s1", current.race_distance_m,
        (current.race_distance_m, 0.0, 0.0), 0.0,
    )


def step(current, *, duration, force_x=0.0, force_y=0.0, width=100.0):
    return integrate_coupled_motion(
        config=MotionConfiguration(1000.0, 2000.0, duration, 1.0),
        reference=reference(current),
        spatial=spatial(width),
        aerodynamic_wrench=aero(),
        contact_wrench=contact(force_x, force_y),
        state=current,
    )


def rotating_force(steps: int) -> SharedVehicleState:
    current = shared(yaw_rate=1.0)
    for _ in range(steps):
        result = step(current, duration=1.0 / steps, force_x=1000.0)
        if result.status != "ok":
            raise RuntimeError(result.reason)
        current = result.candidate_state
    return current


def main() -> int:
    architecture = load_coupling_architecture(
        ROOT / "config/simulation/coupled_level0_architecture_v2.json"
    )
    motion_spec = next(
        item for item in architecture.ordered_modules
        if item.module_id == "vehicle_motion_solver"
    )
    if "circuit.segment_inputs" not in motion_spec.consumes:
        raise RuntimeError("v2 motion module lacks corridor input")

    straight = step(
        shared(velocity=(10.0, 0.0, 0.0)), duration=1.0, force_x=2000.0
    )
    if straight.status != "ok" or not all(x.passed for x in straight.residuals):
        raise RuntimeError("straight analytical fixture failed")

    exact_position = (1.0 - math.cos(1.0), 1.0 - math.sin(1.0))
    coarse = rotating_force(1)
    refined = rotating_force(20)
    coarse_error = math.hypot(
        coarse.position_m[0] - exact_position[0],
        coarse.position_m[1] - exact_position[1],
    )
    refined_error = math.hypot(
        refined.position_m[0] - exact_position[0],
        refined.position_m[1] - exact_position[1],
    )
    if not refined_error < coarse_error:
        raise RuntimeError("timestep refinement did not reduce rotating-force error")

    lateral = step(shared(), duration=1.0, force_y=1000.0)
    reverse = step(shared(velocity=(-2.0, 0.0, 0.0)), duration=1.0)
    if lateral.candidate_state.race_distance_m != 0.0:
        raise RuntimeError("lateral motion advanced race distance")
    if reverse.evidence.corridor.reverse_progress_m <= 0.0:
        raise RuntimeError("reverse motion was not retained as evidence")

    departure_state = shared(velocity=(0.0, 3.0, 0.0))
    adapter = VehicleMotionCouplingAdapter(
        MotionConfiguration(1000.0, 2000.0, 1.0, 0.8),
        reference(departure_state),
    )
    departure = adapter.execute(AdapterReadView(
        "vehicle_motion_solver", departure_state, (
            RuntimeSignal("aero.force_moment", aero()),
            RuntimeSignal("circuit.segment_inputs", spatial(1.0)),
            RuntimeSignal("contact.force_moment", contact()),
            RuntimeSignal("state.current", departure_state),
        )
    ))
    missing = adapter.execute(AdapterReadView(
        "vehicle_motion_solver", departure_state, (
            RuntimeSignal("aero.force_moment", aero()),
            RuntimeSignal("circuit.segment_inputs", SpatialStepEvidence("fixture", "missing", reason="no local corridor")),
            RuntimeSignal("contact.force_moment", contact()),
            RuntimeSignal("state.current", departure_state),
        )
    ))
    if departure.status != "invalid" or departure.signals:
        raise RuntimeError("corridor departure emitted a candidate")
    if missing.status != "invalid" or missing.signals:
        raise RuntimeError("missing spatial evidence emitted a candidate")

    print(json.dumps({
        "schema_version": "1.0",
        "architecture": {
            "architecture_id": architecture.architecture_id,
            "fingerprint_sha256": architecture.fingerprint_sha256,
            "motion_model_version": motion_spec.model_version,
            "motion_consumes": motion_spec.consumes,
        },
        "straight_analytical_fixture": {
            "candidate_velocity_mps": straight.candidate_state.velocity_mps,
            "candidate_position_m": straight.candidate_state.position_m,
            "candidate_race_distance_m": straight.candidate_state.race_distance_m,
            "residual_count": len(straight.residuals),
            "all_residuals_passed": all(x.passed for x in straight.residuals),
        },
        "rotating_force_refinement": {
            "analytical_position_m": exact_position,
            "coarse_dt_s": 1.0,
            "coarse_position_error_m": coarse_error,
            "refined_dt_s": 0.05,
            "refined_position_error_m": refined_error,
            "error_reduction_ratio": coarse_error / refined_error,
        },
        "race_progress_falsification": {
            "lateral_only_credited_m": lateral.evidence.corridor.credited_race_progress_m,
            "reverse_raw_progress_m": reverse.evidence.corridor.raw_tangent_progress_m,
            "reverse_credited_m": reverse.evidence.corridor.credited_race_progress_m,
            "reverse_uncredited_m": reverse.evidence.corridor.reverse_progress_m,
        },
        "failure_observability": {
            "corridor_departure_status": departure.status,
            "corridor_departure_output_count": len(departure.signals),
            "missing_spatial_status": missing.status,
            "missing_spatial_output_count": len(missing.signals),
        },
        "deterministic_replay": straight == step(
            shared(velocity=(10.0, 0.0, 0.0)), duration=1.0, force_x=2000.0
        ),
        "claim_boundary": (
            "Level-0 planar integration and analytical verification only; "
            "not surveyed-circuit, calibrated, or physical validation"
        ),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
