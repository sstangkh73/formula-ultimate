from dataclasses import asdict
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from tests.artifact_requirements import requires_artifacts

from formula_ultimate.experiments.campaign_physics import (
    CampaignPhysicsError,
    adjudicate_seed_outcomes,
    analyze_main_campaign,
    downstream_fingerprint,
    evaluate_level0,
    file_sha256,
    json_compatible,
    training_evaluator_identity,
    validate_campaign_environment,
    validate_campaign_admission,
)
from formula_ultimate.experiments.campaign_runner import execution_protocol_from_main
from formula_ultimate.experiments.campaign_runner import ChainedJsonlLedger
from formula_ultimate.experiments.whole_vehicle_search import CandidateEvaluation, DesignSearchAgentV0, canonical_sha256


ROOT = Path(__file__).resolve().parents[1]
CCX = Path(r"C:\Program Files\FreeCAD 1.1\bin\ccx.exe")
CADQUERY = ROOT / ".tools/cadquery-mcp/Scripts/python.exe"
FREECAD = Path(r"C:\Program Files\FreeCAD 1.1\bin\python.exe")


def load_protocol():
    return json.loads((ROOT / "config/experiments/bounded_whole_vehicle_main_campaign_v1.json").read_text(encoding="utf-8"))


def fixture_evaluation(candidate, objective=1.0):
    draft = {
        "candidate": asdict(candidate), "status": "feasible", "failure_code": None,
        "mass_kg": 1.0, "mass_ratio": 1.0, "capacity_factor": 1.0,
        "maximum_utilization": 0.5, "finish_time_s": objective, "energy_used_j": 2.0,
        "objective": objective, "partition": "training", "evaluator_sha256": "f" * 64,
    }
    return CandidateEvaluation(candidate, "feasible", None, 1.0, 1.0, 1.0, 0.5, objective, 2.0, objective, "training", "f" * 64, canonical_sha256(draft))


@requires_artifacts()
class CampaignPhysicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = load_protocol()
        cls.environment = validate_campaign_environment(ROOT, cls.protocol, ccx=CCX, cadquery_python=CADQUERY, freecad_python=FREECAD)

    def test_frozen_environment_and_training_adapter_are_exact(self):
        self.assertEqual(2880, self.environment["protocol_summary"]["total_attempts"])
        self.assertEqual(self.protocol["upstream_identity"], self.environment["upstream_identity"])
        first = training_evaluator_identity(self.protocol, self.environment)
        second = training_evaluator_identity(self.protocol, self.environment)
        self.assertEqual(first, second)
        self.assertEqual(64, len(first))

    def test_changed_upstream_identity_fails_closed(self):
        changed = copy.deepcopy(self.protocol)
        changed["upstream_identity"]["work047_assembly_config_sha256"] = "0" * 64
        with self.assertRaisesRegex(CampaignPhysicsError, "upstream identity"):
            validate_campaign_environment(ROOT, changed, ccx=CCX, cadquery_python=CADQUERY, freecad_python=FREECAD)

    def test_burn_in_level0_adapter_uses_frozen_training_partition(self):
        execution = execution_protocol_from_main(self.protocol, seeds=(55999,))
        candidate = DesignSearchAgentV0(execution, "GRID", 55999).propose(0)
        identity = training_evaluator_identity(self.protocol, self.environment)
        result = evaluate_level0(execution, candidate, self.environment, identity, partition="training")
        self.assertEqual("training", result.partition)
        self.assertEqual(identity, result.evaluator_sha256)
        self.assertIn(result.status, {"feasible", "failed"})

    def test_seed_outcomes_require_all_three_downstream_gates(self):
        agent_protocol = execution_protocol_from_main(self.protocol, seeds=(7,))
        agent = DesignSearchAgentV0(agent_protocol, "GRID", 7)
        first_candidate, second_candidate = agent.propose(0), agent.propose(1)
        first = fixture_evaluation(first_candidate, 2.0)
        second = fixture_evaluation(second_candidate, 1.0)
        selections = [{"treatment": "GRID", "seed": 7, "candidate_ids": [first_candidate.candidate_id, second_candidate.candidate_id]}]
        holdouts = {first_candidate.candidate_id: first, second_candidate.candidate_id: second}
        refinements = {first_candidate.candidate_id: {"status": "passed"}, second_candidate.candidate_id: {"status": "failed"}}
        witnesses = {first_candidate.candidate_id: {"status": "passed"}, second_candidate.candidate_id: {"status": "passed"}}
        outcomes = adjudicate_seed_outcomes(("GRID",), (7,), selections, holdouts, refinements, witnesses)
        self.assertTrue(outcomes[0]["supported_finisher_present"])
        self.assertEqual(first_candidate.candidate_id, outcomes[0]["best_candidate_id"])

    def test_preregistered_analysis_uses_paired_seed_not_attempts(self):
        outcomes = []
        support = {
            "GRID": [(True, 8.0), (False, None)],
            "RANDOM": [(False, None), (True, 12.0)],
            "EVOLUTION": [(True, 7.0), (True, 10.0)],
        }
        for treatment, rows in support.items():
            for seed, (present, value) in zip((1, 2), rows):
                outcomes.append({"treatment": treatment, "seed": seed, "supported_finisher_present": present, "best_frozen_holdout_time_s": value})
        execution = execution_protocol_from_main(self.protocol, seeds=(1, 2))
        candidate = DesignSearchAgentV0(execution, "GRID", 1).propose(0)
        result = analyze_main_campaign(outcomes, (fixture_evaluation(candidate),), analysis_seed=551337, bootstrap_samples=100)
        self.assertEqual(0.5, result["primary"]["evolution_minus_random_rate_difference"])
        self.assertEqual(1, result["primary"]["evolution_only_pairs"])
        self.assertEqual(-2.0, result["secondary"]["evolution_minus_random_paired_median_time_s"])
        self.assertTrue(result["primary"]["preferred_hypothesis_supported"])
        self.assertTrue(result["secondary"]["preferred_hypothesis_supported"])

    def test_downstream_fingerprint_is_order_and_content_sensitive(self):
        rows = ({"record_type": "a", "value": 1}, {"record_type": "b", "value": 2})
        self.assertEqual(downstream_fingerprint(rows), downstream_fingerprint(rows))
        self.assertNotEqual(downstream_fingerprint(rows), downstream_fingerprint(tuple(reversed(rows))))
        self.assertNotEqual(downstream_fingerprint(rows), downstream_fingerprint((rows[0], {**rows[1], "value": 3})))

    def test_promotion_selection_is_canonical_after_append_and_reload(self):
        selection = {"treatment": "GRID", "seed": 55999, "candidate_ids": ("candidate-a", "candidate-b"), "requested": 2, "selected": 2, "shortfall": 0, "selection_sha256": "f" * 64}
        expected = json_compatible(selection)
        with tempfile.TemporaryDirectory() as temporary:
            ledger = ChainedJsonlLedger(Path(temporary) / "stage.jsonl", protocol_id="p", campaign_id="c", evidence_class="test", ledger_kind="stage")
            ledger.initialize()
            ledger.append({"record_type": "promotion_selection", "selection": expected})
            stored = ledger.read_rows()[0].payload["selection"]
        self.assertEqual(expected, stored)
        self.assertNotEqual(stored, {**expected, "candidate_ids": ["candidate-a", "candidate-c"]})

    def test_successor_admission_uses_exact_active_protocol_path(self):
        protocol_path = ROOT / "config/experiments/bounded_whole_vehicle_main_campaign_v3.json"
        protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
        environment = validate_campaign_environment(ROOT, protocol, ccx=CCX, cadquery_python=CADQUERY, freecad_python=FREECAD)
        implementation = {
            "campaign_runner_sha256": file_sha256(ROOT / "src/formula_ultimate/experiments/campaign_runner.py"),
            "campaign_physics_sha256": file_sha256(ROOT / "src/formula_ultimate/experiments/campaign_physics.py"),
            "campaign_command_sha256": file_sha256(ROOT / "scripts/experiments/run_bounded_main_campaign.py"),
        }
        admission = {
            "decision": "burn_in_accepted_for_admitted_main_campaign",
            "protocol_id": protocol["protocol_id"], "campaign_id": protocol["campaign_id"] + "-BURNIN",
            "protocol_sha256": file_sha256(protocol_path),
            "protocol_fingerprint_sha256": environment["protocol_summary"]["protocol_fingerprint_sha256"],
            "upstream_identity": environment["upstream_identity"], "tool_identity": environment["tool_identity"],
            "implementation_identity": implementation,
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
        }
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "admission.json"
            path.write_text(json.dumps(admission), encoding="utf-8")
            accepted = validate_campaign_admission(ROOT, path, protocol_path, protocol, environment, implementation, require_clean_worktree=False)
            self.assertEqual(admission, accepted)
            with self.assertRaisesRegex(CampaignPhysicsError, "file identity"):
                validate_campaign_admission(ROOT, path, ROOT / "config/experiments/bounded_whole_vehicle_main_campaign_v2.json", protocol, environment, implementation, require_clean_worktree=False)


if __name__ == "__main__":
    unittest.main()
