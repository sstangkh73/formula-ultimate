from __future__ import annotations

from dataclasses import replace
import math
from pathlib import Path
import unittest

from formula_ultimate.physics.tyre import (
    TyreContactParameters,
    TyreForceRequest,
    resolve_tyre_force,
)
from formula_ultimate.simulation import (
    AdapterReadView,
    AerodynamicChassisWrench,
    ComponentHealthState,
    ContactForceMoment,
    ContactRuntimeState,
    CoupledContactForce,
    MotionConfiguration,
    MotionCorridorReference,
    MotionCouplingError,
    RuntimeSignal,
    SharedVehicleState,
    SpatialStepEvidence,
    VehicleMotionCouplingAdapter,
    integrate_coupled_motion,
    load_coupling_architecture,
)


ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE_V2 = ROOT / "config/simulation/coupled_level0_architecture_v2.json"


def state(**overrides) -> SharedVehicleState:
    values = dict(
        time_s=0.0,
        race_distance_m=0.0,
        position_m=(0.0, 0.0, 0.0),
        velocity_mps=(0.0, 0.0, 0.0),
        yaw_rad=0.0,
        yaw_rate_rad_per_s=0.0,
        primary_energy_j=1.0e6,
        recovered_energy_j=0.0,
        completed_laps=0,
        contacts=(ContactRuntimeState("c", 1000.0, 0.0, 0.0, 0.0, 0.0),),
        components=(ComponentHealthState("store", 300.0, 0.0, 0.0, False),),
    )
    values.update(overrides)
    return SharedVehicleState(**values)


def spatial(**overrides) -> SpatialStepEvidence:
    values = dict(
        circuit_id="fixture",
        status="available",
        source_id="analytical",
        segment_id="s1",
        curvature_1pm=0.0,
        grade_rad=0.0,
        bank_rad=0.0,
        width_left_m=100.0,
        width_right_m=100.0,
        horizontal_uncertainty_m=0.0,
    )
    values.update(overrides)
    return SpatialStepEvidence(**values)


def reference(current: SharedVehicleState, **overrides) -> MotionCorridorReference:
    values = dict(
        circuit_id="fixture",
        segment_id="s1",
        race_distance_m=current.race_distance_m,
        centreline_position_m=(current.race_distance_m, 0.0, 0.0),
        centreline_heading_rad=0.0,
    )
    values.update(overrides)
    return MotionCorridorReference(**values)


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


def run(
    current: SharedVehicleState,
    *,
    duration=1.0,
    aerodynamic=None,
    contacts=None,
    segment=None,
    corridor=None,
    width=1.0,
):
    return integrate_coupled_motion(
        config=MotionConfiguration(1000.0, 2000.0, duration, width),
        reference=corridor or reference(current),
        spatial=segment or spatial(),
        aerodynamic_wrench=aerodynamic or aero(),
        contact_wrench=contacts or contact(),
        state=current,
    )


class MotionCouplingTests(unittest.TestCase):
    def test_v2_architecture_routes_corridor_to_motion_exactly(self):
        architecture = load_coupling_architecture(ARCHITECTURE_V2)
        motion = next(x for x in architecture.ordered_modules if x.module_id == "vehicle_motion_solver")
        self.assertEqual("coupled-level0-reference-v2", architecture.architecture_id)
        self.assertEqual("work026-coupled-motion-v1", motion.model_version)
        self.assertEqual(
            ("aero.force_moment", "circuit.segment_inputs", "contact.force_moment", "state.current"),
            motion.consumes,
        )
        self.assertEqual(architecture, load_coupling_architecture(ARCHITECTURE_V2))

    def test_constant_straight_force_matches_analytical_solution(self):
        current = state(velocity_mps=(10.0, 0.0, 0.0))
        result = run(current, contacts=contact(2000.0))
        self.assertEqual("ok", result.status)
        self.assertEqual((12.0, 0.0, 0.0), result.candidate_state.velocity_mps)
        self.assertEqual((11.0, 0.0, 0.0), result.candidate_state.position_m)
        self.assertEqual(11.0, result.candidate_state.race_distance_m)
        self.assertTrue(all(item.passed for item in result.residuals))

    def test_aero_contact_force_and_yaw_moment_are_summed(self):
        result = run(state(), duration=0.5, aerodynamic=aero(1000.0, 200.0, 100.0), contacts=contact(500.0, 300.0, 300.0))
        self.assertEqual("ok", result.status)
        self.assertEqual(1500.0, result.evidence.total_body_longitudinal_force_n)
        self.assertEqual(500.0, result.evidence.total_body_lateral_force_n)
        self.assertEqual(400.0, result.evidence.total_yaw_moment_n_m)
        self.assertAlmostEqual(0.1, result.candidate_state.yaw_rate_rad_per_s)
        self.assertAlmostEqual(0.025, result.candidate_state.yaw_rad)

    def test_lateral_only_motion_does_not_advance_race_distance(self):
        result = run(state(), contacts=contact(0.0, 1000.0))
        self.assertEqual("ok", result.status)
        self.assertEqual(0.0, result.candidate_state.race_distance_m)
        self.assertGreater(result.candidate_state.position_m[1], 0.0)

    def test_reverse_motion_is_observable_and_not_credited(self):
        current = state(velocity_mps=(-2.0, 0.0, 0.0))
        result = run(current)
        self.assertEqual("ok", result.status)
        self.assertEqual(0.0, result.candidate_state.race_distance_m)
        self.assertEqual(2.0, result.evidence.corridor.reverse_progress_m)
        self.assertEqual(-2.0, result.evidence.corridor.raw_tangent_progress_m)

    def test_corridor_departure_invalidates_adapter_with_zero_writes(self):
        current = state(velocity_mps=(0.0, 3.0, 0.0))
        adapter = VehicleMotionCouplingAdapter(
            MotionConfiguration(1000.0, 2000.0, 1.0, 0.8), reference(current)
        )
        view = AdapterReadView("vehicle_motion_solver", current, (
            RuntimeSignal("aero.force_moment", aero()),
            RuntimeSignal("circuit.segment_inputs", spatial(width_left_m=1.0, width_right_m=1.0)),
            RuntimeSignal("contact.force_moment", contact()),
            RuntimeSignal("state.current", current),
        ))
        output = adapter.execute(view)
        self.assertEqual("invalid", output.status)
        self.assertEqual((), output.signals)
        self.assertIn("crosses", output.reason)

    def test_missing_spatial_evidence_invalidates_adapter_with_zero_writes(self):
        current = state()
        missing = SpatialStepEvidence("fixture", "missing", reason="no local corridor")
        adapter = VehicleMotionCouplingAdapter(
            MotionConfiguration(1000.0, 2000.0, 0.1, 1.0), reference(current)
        )
        view = AdapterReadView("vehicle_motion_solver", current, (
            RuntimeSignal("aero.force_moment", aero()),
            RuntimeSignal("circuit.segment_inputs", missing),
            RuntimeSignal("contact.force_moment", contact()),
            RuntimeSignal("state.current", current),
        ))
        output = adapter.execute(view)
        self.assertEqual("invalid", output.status)
        self.assertEqual((), output.signals)
        self.assertIn("available spatial", output.reason)

    def test_inconsistent_contact_totals_remain_observable(self):
        bad = replace(contact(100.0), total_body_longitudinal_force_n=101.0)
        result = run(state(), contacts=bad)
        self.assertEqual("invalid", result.status)
        self.assertIsNone(result.candidate_state)
        self.assertFalse(result.residuals[0].passed)

    def test_vertical_offset_uses_constant_velocity_kinematics(self):
        current = state(position_m=(0.0, 0.0, 2.5), velocity_mps=(1.0, 0.0, 0.4))
        result = run(current, corridor=reference(current, centreline_position_m=(0.0, 0.0, 0.0)))
        self.assertEqual("ok", result.status)
        self.assertEqual(2.9, result.candidate_state.position_m[2])
        self.assertEqual(0.4, result.candidate_state.velocity_mps[2])
        self.assertTrue(next(x for x in result.residuals if x.residual_id == "motion.kinematic-z").passed)

    def test_timestep_refinement_reduces_rotating_force_error(self):
        def integrate(steps):
            current = state(yaw_rate_rad_per_s=1.0)
            for _ in range(steps):
                result = run(current, duration=1.0 / steps, contacts=contact(1000.0), width=1.0)
                self.assertEqual("ok", result.status)
                current = result.candidate_state
            return current

        exact_position = (1.0 - math.cos(1.0), 1.0 - math.sin(1.0))
        coarse = integrate(1)
        refined = integrate(20)
        coarse_error = math.hypot(coarse.position_m[0] - exact_position[0], coarse.position_m[1] - exact_position[1])
        refined_error = math.hypot(refined.position_m[0] - exact_position[0], refined.position_m[1] - exact_position[1])
        self.assertLess(refined_error, coarse_error)
        self.assertLess(refined_error, 0.001)

    def test_replay_and_adapter_exact_output_contract(self):
        current = state(velocity_mps=(5.0, 0.0, 0.0))
        adapter = VehicleMotionCouplingAdapter(
            MotionConfiguration(1000.0, 2000.0, 0.1, 1.0), reference(current)
        )
        signals = (
            RuntimeSignal("aero.force_moment", aero(100.0)),
            RuntimeSignal("circuit.segment_inputs", spatial()),
            RuntimeSignal("contact.force_moment", contact(200.0)),
            RuntimeSignal("state.current", current),
        )
        first = adapter.execute(AdapterReadView("vehicle_motion_solver", current, signals))
        second = adapter.execute(AdapterReadView("vehicle_motion_solver", current, tuple(reversed(signals))))
        self.assertEqual(first, second)
        self.assertEqual("ok", first.status)
        self.assertEqual({"motion.residuals", "state.motion_candidate"}, {x.signal_id for x in first.signals})

    def test_invalid_configuration_and_reference_mismatch_are_rejected(self):
        with self.assertRaises(MotionCouplingError):
            MotionConfiguration(0.0, 1.0, 1.0, 1.0)
        current = state(race_distance_m=1.0)
        with self.assertRaisesRegex(MotionCouplingError, "race distance"):
            run(current, corridor=reference(current, race_distance_m=0.0))


if __name__ == "__main__":
    unittest.main()
