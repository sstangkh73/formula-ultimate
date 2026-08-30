from __future__ import annotations

from dataclasses import replace
import unittest

from formula_ultimate.simulation import (
    ConnectionDefinition,
    EventCandidate,
    FailureEvidence,
    GateAIdentity,
    StructuralFailureCouplingError,
    arbitrate_event_candidates,
    evaluate_structural_failure_step,
    initial_network_state,
    structural_result_fingerprint,
)


WRENCH = (1000.0, 50.0, -20.0, 10.0, 5.0, -3.0)
GATE = GateAIdentity(
    "gate_a_remediation_v1",
    "narrowly_bounded",
    "C3D10_precritical_v1",
    "7f4444a78af66157f04441b38e4d4bc3225a892b29f90ebf9840279694fb6258",
    "bonded_cylindrical_surface_zero_displacement_v1",
)
PROTOCOLS = {
    "yield": "yield_plasticity_acceptance_v1",
    "fracture": "fracture_initiation_acceptance_v1",
    "fatigue": "fatigue_damage_acceptance_v1",
}
DEFINITIONS = (
    ConnectionDefinition("joint_a", "primary_mount", 1.0),
    ConnectionDefinition("joint_b", "primary_mount", 1.0),
)
YIELD = FailureEvidence("yield_a", "joint_a", "yield", 0.2, PROTOCOLS["yield"], "a" * 64, 0.0)
FRACTURE = FailureEvidence("fracture_a", "joint_a", "fracture", 0.375, PROTOCOLS["fracture"], "b" * 64, 0.7)


def start(definitions=DEFINITIONS):
    energies = {item.connection_id: 12.0 if item.connection_id == "joint_a" else 8.0 for item in definitions}
    return initial_network_state(time_s=0.0, definitions=definitions, stored_energy_by_connection_j=energies, applied_wrench=WRENCH)


def step(state, definitions, evidence, duration=0.5, gate=GATE):
    return evaluate_structural_failure_step(
        state=state,
        duration_s=duration,
        definitions=definitions,
        applied_wrench=WRENCH,
        evidence=evidence,
        gate_identity=gate,
        expected_gate_identity=GATE,
        mechanism_protocols=PROTOCOLS,
    )


class StructuralFailureCouplingTests(unittest.TestCase):
    def test_yield_degrades_then_fracture_zeros_and_redistributes_wrench(self) -> None:
        yielded = step(start(), DEFINITIONS, (YIELD, FRACTURE))
        self.assertEqual(("degraded",), yielded.transition.target_states)
        self.assertIsNone(yielded.race_event)
        fractured = step(yielded.candidate_state, DEFINITIONS, (FRACTURE,))
        self.assertEqual("running", fractured.outcome)
        states = {item.connection_id: item for item in fractured.candidate_state.connections}
        self.assertEqual((0.0,) * 6, states["joint_a"].transmitted_wrench)
        self.assertEqual(WRENCH, states["joint_b"].transmitted_wrench)
        self.assertTrue(all(item.passed for item in fractured.residuals))
        self.assertEqual(12.0, fractured.energy_ledger.stored_energy_j)
        self.assertAlmostEqual(8.4, fractured.energy_ledger.dissipated_energy_j)
        self.assertAlmostEqual(3.6, fractured.energy_ledger.released_energy_j)
        self.assertLess(abs(fractured.energy_ledger.residual_j), 1.0e-12)
        self.assertEqual("structural_failure", fractured.race_event.event_type)

    def test_critical_path_failure_produces_dnf(self) -> None:
        definitions = DEFINITIONS[:1]
        yielded = step(start(definitions), definitions, (YIELD, FRACTURE))
        fractured = step(yielded.candidate_state, definitions, (FRACTURE,))
        self.assertEqual("DNF", fractured.outcome)
        self.assertEqual("DNF", fractured.candidate_state.status)
        self.assertEqual((0.0,) * 6, fractured.candidate_state.connections[0].transmitted_wrench)

    def test_replay_is_exact_and_structural_event_uses_race_arbitration(self) -> None:
        first = step(step(start(), DEFINITIONS, (YIELD, FRACTURE)).candidate_state, DEFINITIONS, (FRACTURE,))
        second = step(step(start(), DEFINITIONS, (YIELD, FRACTURE)).candidate_state, DEFINITIONS, (FRACTURE,))
        self.assertEqual(first, second)
        self.assertEqual(structural_result_fingerprint(first), structural_result_fingerprint(second))
        decision = arbitrate_event_candidates((
            EventCandidate("finish", "finished", 0.375, "race"),
            first.race_event,
        ))
        self.assertEqual("finish", decision.winner.event_id)

    def test_invalid_identity_and_protocol_return_no_state_write(self) -> None:
        state = start()
        bad_gate = replace(GATE, element_route_id="C3D4_near_critical")
        invalid = step(state, DEFINITIONS, (YIELD,), gate=bad_gate)
        self.assertEqual("invalid", invalid.status)
        self.assertIsNone(invalid.candidate_state)
        self.assertEqual(0.0, state.time_s)
        bad = replace(YIELD, upstream_protocol_id="unknown")
        mismatch = step(state, DEFINITIONS, (bad,))
        self.assertEqual("invalid", mismatch.status)
        self.assertIsNone(mismatch.candidate_state)

    def test_malformed_evidence_and_topology_fail_closed(self) -> None:
        with self.assertRaises(StructuralFailureCouplingError):
            FailureEvidence("bad", "joint_a", "fracture", 0.1, PROTOCOLS["fracture"], "b" * 64, 1.1)
        with self.assertRaises(StructuralFailureCouplingError):
            initial_network_state(
                time_s=0.0,
                definitions=(DEFINITIONS[0], DEFINITIONS[0]),
                stored_energy_by_connection_j={"joint_a": 1.0},
                applied_wrench=WRENCH,
            )
        unknown = replace(YIELD, connection_id="unknown")
        invalid = step(start(), DEFINITIONS, (unknown,))
        self.assertEqual("invalid", invalid.status)
        self.assertIsNone(invalid.candidate_state)


if __name__ == "__main__":
    unittest.main()
