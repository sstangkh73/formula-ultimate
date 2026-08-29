from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from formula_ultimate.physics.circuit import load_circuit_catalog
from formula_ultimate.simulation import (
    CrossModelEvidence,
    IntegrationReleaseError,
    assess_refinement_samples,
    create_integration_release_review,
    evaluate_promotion_gate,
    load_baseline_campaign_protocol,
    load_coupling_architecture,
    load_integration_gate_protocol,
    run_baseline_campaign,
    run_baseline_refinement_matrix,
    run_transaction_falsification_suite,
    verify_baseline_campaign_result,
)


ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / "config/simulation/integration_promotion_gate_v1.json"
BASELINE_PATH = ROOT / "config/simulation/fixed_topology_baseline_protocol_v1.json"
ARCHITECTURE = load_coupling_architecture(
    ROOT / "config/simulation/coupled_level0_architecture_v4.json"
)
PROFILES = load_circuit_catalog(ROOT / "config/circuits/real_circuits_v1.json")


def complete_evidence(protocol):
    return tuple(
        CrossModelEvidence(
            f"fixture-{evidence_type}",
            evidence_type,
            "level1",
            True,
            True,
            hashlib.sha256(evidence_type.encode()).hexdigest(),
            "test-only independent fixture",
        )
        for evidence_type in protocol.promotion.required_evidence_types
    )


class IntegrationReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gate = load_integration_gate_protocol(GATE_PATH)
        cls.baseline_protocol = load_baseline_campaign_protocol(BASELINE_PATH)
        cls.campaign = run_baseline_campaign(
            protocol=cls.baseline_protocol,
            architecture=ARCHITECTURE,
            profiles=PROFILES,
        )
        cls.falsification = run_transaction_falsification_suite(
            protocol=cls.gate, architecture=ARCHITECTURE
        )
        cls.refinement = run_baseline_refinement_matrix(
            gate_protocol=cls.gate,
            baseline_protocol=cls.baseline_protocol,
            architecture=ARCHITECTURE,
            profiles=PROFILES,
        )
        cls.blocked_decision = evaluate_promotion_gate(
            candidate_id="fixed-four-steady-drag-v1",
            protocol=cls.gate,
            campaign=cls.campaign,
            falsification=cls.falsification,
            refinement=cls.refinement,
            cross_model_evidence=(),
        )

    def test_gate_protocol_forbids_automatic_discovery(self):
        self.assertEqual(6, len(self.gate.falsification_requirements))
        self.assertEqual((2000.0, 1000.0, 500.0), self.gate.refinement.timesteps_s)
        self.assertTrue(self.gate.promotion.require_real_circuit_admission)
        self.assertTrue(self.gate.promotion.require_independent_evidence)
        self.assertFalse(self.gate.promotion.automatic_discovery_claim)
        self.assertEqual(6, len(self.gate.promotion.required_evidence_types))

    def test_transaction_control_commits_and_all_faults_roll_back(self):
        suite = self.falsification
        self.assertEqual("committed", suite.control_status)
        self.assertTrue(suite.control_committed)
        self.assertEqual((6, 6), (suite.detected_case_count, suite.required_case_count))
        self.assertTrue(suite.all_required_faults_detected)
        self.assertTrue(all(case.detected and case.rolled_back for case in suite.cases))
        observed = {case.case_id: case.observed_failure_code for case in suite.cases}
        expected = {
            requirement.case_id: requirement.expected_failure_code
            for requirement in self.gate.falsification_requirements
        }
        self.assertEqual(expected, observed)

    def test_falsification_suite_replays_exactly(self):
        replay = run_transaction_falsification_suite(
            protocol=self.gate, architecture=ARCHITECTURE
        )
        self.assertEqual(self.falsification, replay)

    def test_refinement_matrix_passes_but_does_not_claim_order(self):
        result = self.refinement
        self.assertEqual("passed", result.status)
        self.assertEqual(6, len(result.samples))
        self.assertEqual(0.0, result.max_relative_time_variation)
        self.assertLessEqual(
            result.max_relative_energy_variation,
            self.gate.refinement.maximum_relative_energy_variation,
        )
        self.assertEqual(0.0, result.max_absolute_finish_residual_m)
        self.assertFalse(result.convergence_order_estimated)
        self.assertTrue(all(sample.outcome == "finished" for sample in result.samples))
        self.assertEqual({16, 31, 62}, {sample.attempted_steps for sample in result.samples})

    def test_divergent_refinement_sample_blocks(self):
        samples = list(self.refinement.samples)
        samples[0] = replace(samples[0], final_time_s=samples[0].final_time_s + 100.0)
        result = assess_refinement_samples(
            samples=tuple(samples), configuration=self.gate.refinement
        )
        self.assertEqual("blocked", result.status)
        self.assertGreater(
            result.max_relative_time_variation,
            self.gate.refinement.maximum_relative_time_variation,
        )

    def test_current_proxy_campaign_is_identity_valid_but_promotion_blocked(self):
        valid, reasons = verify_baseline_campaign_result(self.campaign)
        self.assertTrue(valid); self.assertEqual((), reasons)
        decision = self.blocked_decision
        self.assertEqual("blocked", decision.status)
        self.assertIn("real_circuit_admission_missing", decision.blocking_reasons)
        for evidence_type in self.gate.promotion.required_evidence_types:
            self.assertIn(
                f"missing_or_invalid_evidence:{evidence_type}",
                decision.blocking_reasons,
            )
        self.assertFalse(decision.discovery_claim_allowed)
        self.assertFalse(decision.automatic_promotion)

    def test_tampered_campaign_identity_is_rejected(self):
        tampered = replace(self.campaign, real_circuit_admitted=True)
        valid, reasons = verify_baseline_campaign_result(tampered)
        self.assertFalse(valid)
        self.assertIn("campaign_fingerprint_mismatch", reasons)
        decision = evaluate_promotion_gate(
            candidate_id="tampered",
            protocol=self.gate,
            campaign=tampered,
            falsification=self.falsification,
            refinement=self.refinement,
            cross_model_evidence=complete_evidence(self.gate),
        )
        self.assertEqual("blocked", decision.status)
        self.assertTrue(
            any(reason.startswith("campaign_evidence_invalid:") for reason in decision.blocking_reasons)
        )

    def test_complete_test_evidence_reaches_review_only_under_relaxed_test_admission(self):
        relaxed = replace(
            self.gate,
            promotion=replace(
                self.gate.promotion, require_real_circuit_admission=False
            ),
        )
        decision = evaluate_promotion_gate(
            candidate_id="review-fixture",
            protocol=relaxed,
            campaign=self.campaign,
            falsification=self.falsification,
            refinement=self.refinement,
            cross_model_evidence=complete_evidence(relaxed),
        )
        self.assertEqual("eligible_for_independent_review", decision.status)
        self.assertEqual((), decision.blocking_reasons)
        self.assertFalse(decision.discovery_claim_allowed)
        review = create_integration_release_review(
            protocol=relaxed,
            campaign=self.campaign,
            falsification=self.falsification,
            refinement=self.refinement,
            promotion=decision,
        )
        self.assertEqual(
            "level0_experimentation_ready_independent_review_required", review.status
        )
        self.assertFalse(review.discovery_claim_allowed)

    def test_release_review_authorizes_only_gated_level0_work(self):
        review = create_integration_release_review(
            protocol=self.gate,
            campaign=self.campaign,
            falsification=self.falsification,
            refinement=self.refinement,
            promotion=self.blocked_decision,
        )
        self.assertEqual(
            "level0_experimentation_ready_promotion_blocked", review.status
        )
        self.assertTrue(review.level0_infrastructure_ready)
        self.assertTrue(review.gated_level0_experimentation_authorized)
        self.assertFalse(review.real_circuit_claim_allowed)
        self.assertFalse(review.discovery_claim_allowed)
        self.assertFalse(review.safety_claim_allowed)
        self.assertFalse(review.manufacturability_claim_allowed)

    def test_loader_rejects_hidden_fields_and_auto_discovery(self):
        raw = json.loads(GATE_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "gate.json"
            hidden = dict(raw); hidden["hidden_override"] = True
            path.write_text(json.dumps(hidden), encoding="utf-8")
            with self.assertRaisesRegex(IntegrationReleaseError, "unexpected"):
                load_integration_gate_protocol(path)
            automatic = json.loads(json.dumps(raw))
            automatic["promotion"]["automatic_discovery_claim"] = True
            path.write_text(json.dumps(automatic), encoding="utf-8")
            with self.assertRaisesRegex(IntegrationReleaseError, "forbidden"):
                load_integration_gate_protocol(path)


if __name__ == "__main__":
    unittest.main()
