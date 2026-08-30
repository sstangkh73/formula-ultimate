from dataclasses import asdict, replace
import json
from pathlib import Path
import tempfile
import unittest

from formula_ultimate.experiments.campaign_runner import (
    CampaignExecutionAuthorization,
    CampaignLedgerStore,
    CampaignRunnerError,
    ChainedJsonlLedger,
    execute_training_opportunities,
    reconstruct_training_agent,
    select_training_promotions,
)
from formula_ultimate.experiments.whole_vehicle_search import (
    CandidateEvaluation,
    DesignSearchAgentV0,
    SearchCandidate,
    canonical_sha256,
)


def protocol_fixture():
    variables = {
        "core_length_scale": {"minimum": 0.9, "maximum": 1.1},
        "core_width_scale": {"minimum": 0.9, "maximum": 1.1},
        "contact_radius_scale": {"minimum": 0.8, "maximum": 1.2},
        "source_size_scale": {"minimum": 0.8, "maximum": 1.2},
        "propulsor_size_scale": {"minimum": 0.8, "maximum": 1.2},
    }
    return {
        "protocol_id": "TEST-PROTOCOL",
        "campaign_id": "TEST-CAMPAIGN",
        "treatments": ["GRID", "RANDOM", "EVOLUTION"],
        "seeds": [7],
        "attempted_evaluations_per_treatment_seed": 4,
        "candidate_variables": variables,
        "grid_levels_per_variable": 4,
        "evolution_initial_random": 2,
        "evolution_mutation_sigma_fraction": 0.12,
    }


def evaluation(candidate: SearchCandidate, *, feasible=True, objective=None, partition="training"):
    objective = float(candidate.attempt_index + 1 if objective is None else objective)
    draft = {
        "candidate": asdict(candidate), "status": "feasible" if feasible else "failed",
        "failure_code": None if feasible else "fixture_failure", "mass_kg": 1.0,
        "mass_ratio": 1.0, "capacity_factor": 1.0, "maximum_utilization": 0.5,
        "finish_time_s": objective if feasible else None, "energy_used_j": 10.0,
        "objective": objective if feasible else None, "partition": partition,
        "evaluator_sha256": "f" * 64,
    }
    return CandidateEvaluation(
        candidate, draft["status"], draft["failure_code"], 1.0, 1.0, 1.0, 0.5,
        draft["finish_time_s"], 10.0, draft["objective"], partition, "f" * 64,
        canonical_sha256(draft),
    )


class CampaignRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        budget = ChainedJsonlLedger(root / "budget.jsonl", protocol_id="TEST-PROTOCOL", campaign_id="TEST-CAMPAIGN", evidence_class="unit_test_only", ledger_kind="budget")
        result = ChainedJsonlLedger(root / "result.jsonl", protocol_id="TEST-PROTOCOL", campaign_id="TEST-CAMPAIGN", evidence_class="unit_test_only", ledger_kind="result")
        self.store = CampaignLedgerStore(budget, result)
        self.store.initialize()
        self.protocol = protocol_fixture()
        self.auth = CampaignExecutionAuthorization("TEST-AUTH", "TEST-CAMPAIGN", "unit_test_only", (7,), False)

    def tearDown(self):
        self.temp.cleanup()

    def test_exact_append_restart_and_resume(self):
        first = execute_training_opportunities(self.store, self.protocol, "RANDOM", 7, evaluation, target_attempts=2, authorization=self.auth)
        self.assertEqual(2, len(first))
        before = self.store.fingerprint()
        second = execute_training_opportunities(self.store, self.protocol, "RANDOM", 7, evaluation, target_attempts=4, authorization=self.auth)
        self.assertEqual(2, len(second))
        state = self.store.validate()
        self.assertEqual(4, len(state["reservations"]))
        self.assertEqual(4, len(state["results"]))
        self.assertEqual((), state["pending_candidate_ids"])
        self.assertNotEqual(before, self.store.fingerprint())
        agent, pending = reconstruct_training_agent(self.store, self.protocol, "RANDOM", 7)
        self.assertEqual(4, len(agent.history))
        self.assertIsNone(pending)

    def test_interruption_after_reservation_completes_exact_candidate_once(self):
        agent = DesignSearchAgentV0(self.protocol, "EVOLUTION", 7)
        candidate = agent.propose(0)
        self.store.reserve_attempt(candidate)
        seen = []

        def callback(value):
            seen.append(value)
            return evaluation(value)

        completed = execute_training_opportunities(self.store, self.protocol, "EVOLUTION", 7, callback, target_attempts=1, authorization=self.auth)
        self.assertEqual((candidate,), tuple(seen))
        self.assertEqual(candidate.candidate_id, completed[0].candidate.candidate_id)
        state = self.store.validate()
        self.assertEqual(1, len(state["reservations"]))
        self.assertEqual(1, len(state["results"]))
        with self.assertRaisesRegex(CampaignRunnerError, "duplicate"):
            self.store.append_training_result(completed[0])

    def test_unreserved_result_and_skipped_attempt_fail_closed(self):
        agent = DesignSearchAgentV0(self.protocol, "GRID", 7)
        candidate = agent.propose(0)
        with self.assertRaisesRegex(CampaignRunnerError, "unreserved"):
            self.store.append_training_result(evaluation(candidate))
        skipped = replace(agent.propose(0), attempt_index=1)
        with self.assertRaisesRegex(CampaignRunnerError, "skipped"):
            self.store.reserve_attempt(skipped)

    def test_mutated_and_truncated_ledger_fail_closed(self):
        agent = DesignSearchAgentV0(self.protocol, "GRID", 7)
        self.store.reserve_attempt(agent.propose(0))
        path = self.store.budget.path
        raw = json.loads(path.read_text(encoding="utf-8").strip())
        raw["payload"]["consumed_attempts"] = 2
        path.write_text(json.dumps(raw, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(CampaignRunnerError, "record hash"):
            self.store.validate()
        path.write_text('{"schema":', encoding="utf-8")
        with self.assertRaisesRegex(CampaignRunnerError, "malformed"):
            self.store.validate()

    def test_changed_candidate_or_rng_checkpoint_breaks_reconstruction(self):
        agent = DesignSearchAgentV0(self.protocol, "RANDOM", 7)
        candidate = replace(agent.propose(0), rng_checkpoint_sha256="0" * 64)
        self.store.reserve_attempt(candidate)
        with self.assertRaisesRegex(CampaignRunnerError, "RNG"):
            reconstruct_training_agent(self.store, self.protocol, "RANDOM", 7)

    def test_execution_requires_explicit_matching_authorization(self):
        with self.assertRaisesRegex(CampaignRunnerError, "locked"):
            execute_training_opportunities(self.store, self.protocol, "GRID", 7, evaluation, target_attempts=1, authorization=None)
        wrong = CampaignExecutionAuthorization("WRONG", "OTHER", "unit_test_only", (7,), False)
        with self.assertRaisesRegex(CampaignRunnerError, "does not cover"):
            execute_training_opportunities(self.store, self.protocol, "GRID", 7, evaluation, target_attempts=1, authorization=wrong)
        wrong_evidence = CampaignExecutionAuthorization("TEST-AUTH", "TEST-CAMPAIGN", "admitted_campaign", (7,), True)
        with self.assertRaisesRegex(CampaignRunnerError, "evidence class"):
            execute_training_opportunities(self.store, self.protocol, "GRID", 7, evaluation, target_attempts=1, authorization=wrong_evidence)

    def test_execution_cannot_rewind_consumed_budget(self):
        execute_training_opportunities(self.store, self.protocol, "RANDOM", 7, evaluation, target_attempts=2, authorization=self.auth)
        with self.assertRaisesRegex(CampaignRunnerError, "below already consumed"):
            execute_training_opportunities(self.store, self.protocol, "RANDOM", 7, evaluation, target_attempts=1, authorization=self.auth)

    def test_rehashed_rows_with_invalid_domain_identities_fail_closed(self):
        agent = DesignSearchAgentV0(self.protocol, "GRID", 7)
        candidate = agent.propose(0)
        invalid_candidate = replace(candidate, candidate_id="candidate-" + "0" * 16)
        self.store.budget.append({"record_type": "attempt_reserved", "consumed_attempts": 1, "candidate": asdict(invalid_candidate)})
        with self.assertRaisesRegex(CampaignRunnerError, "candidate identity"):
            self.store.validate()

        root = Path(self.temp.name) / "evaluation-identity"
        budget = ChainedJsonlLedger(root / "budget.jsonl", protocol_id="TEST-PROTOCOL", campaign_id="TEST-CAMPAIGN", evidence_class="unit_test_only", ledger_kind="budget")
        result = ChainedJsonlLedger(root / "result.jsonl", protocol_id="TEST-PROTOCOL", campaign_id="TEST-CAMPAIGN", evidence_class="unit_test_only", ledger_kind="result")
        store = CampaignLedgerStore(budget, result)
        store.initialize()
        store.reserve_attempt(candidate)
        invalid_evaluation = replace(evaluation(candidate), evaluation_sha256="0" * 64)
        result.append({"record_type": "training_result", "evaluation": asdict(invalid_evaluation)})
        with self.assertRaisesRegex(CampaignRunnerError, "evaluation identity"):
            store.validate()

    def test_promotion_uses_training_only_and_records_shortfall(self):
        agents = {name: DesignSearchAgentV0(self.protocol, name, 7) for name in self.protocol["treatments"]}
        records = []
        for name, agent in agents.items():
            for index in range(3):
                candidate = agent.propose(index)
                item = evaluation(candidate, feasible=not (name == "GRID" and index > 0), objective=3-index)
                agent.observe(item)
                records.append(item)
        selections = select_training_promotions(records, self.protocol["treatments"], [7], per_treatment_seed=2)
        by_name = {item.treatment: item for item in selections}
        self.assertEqual(1, by_name["GRID"].selected)
        self.assertEqual(1, by_name["GRID"].shortfall)
        self.assertEqual(2, by_name["RANDOM"].selected)
        self.assertEqual(2, by_name["EVOLUTION"].selected)
        self.assertEqual(records[5].candidate.candidate_id, by_name["RANDOM"].candidate_ids[0])
        holdout = replace(records[0], partition="holdout")
        with self.assertRaisesRegex(CampaignRunnerError, "holdout"):
            select_training_promotions([holdout], self.protocol["treatments"], [7], per_treatment_seed=2)

    def test_cross_ledger_identity_mismatch_fails_closed(self):
        other = ChainedJsonlLedger(Path(self.temp.name) / "other.jsonl", protocol_id="TEST-PROTOCOL", campaign_id="OTHER", evidence_class="unit_test_only", ledger_kind="result")
        with self.assertRaisesRegex(CampaignRunnerError, "identities differ"):
            CampaignLedgerStore(self.store.budget, other)


if __name__ == "__main__":
    unittest.main()
