import copy
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import unittest

from formula_ultimate.experiments.whole_vehicle_search import (
    DesignSearchAgentV0,
    WholeVehicleSearchError,
    evaluate_candidate,
    promote_candidates,
    readiness_decision,
    run_search_pilot,
    validate_search_protocol,
)
from formula_ultimate.simulation.vehicle_load_cases import (
    canonical_sha256,
    evaluate_all_load_cases,
    validate_protocol as validate_load_protocol,
)


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


class WholeVehicleSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = read("config/experiments/bounded_whole_vehicle_search_pilot_v1.json")
        cls.base_assembly = read("config/vehicle/topology_neutral_vehicle_v1.json")
        cls.load_protocol = read("config/vehicle/whole_vehicle_load_cases_v1.json")
        failure = read("config/simulation/structural_failure_coupling_v1.json")
        assembly = validate_load_protocol(
            cls.load_protocol, cls.base_assembly,
            assembly_config_sha256=sha("config/vehicle/topology_neutral_vehicle_v1.json"),
            assembly_step_sha256=cls.load_protocol["assembly_identity"]["assembly_step_sha256"],
            failure_config_sha256=sha("config/simulation/structural_failure_coupling_v1.json"),
        )
        ready = [asdict(item) for item in evaluate_all_load_cases(cls.load_protocol, assembly, failure)]
        cls.work048 = {
            "results": ready,
            "partitions": {
                "training": cls.load_protocol["partitions"]["training"],
                "holdout": cls.load_protocol["partitions"]["holdout"],
            },
        }
        cls.baseline_protocol = read("config/vehicle/fixed_topology_end_to_end_baseline_v1.json")
        cls.baseline = {
            "replay": {
                "result_sha256": cls.protocol["upstream_identity"]["reference_result_sha256"],
                "matrix_sha256": cls.protocol["upstream_identity"]["reference_matrix_sha256"],
            },
            "upstream": {
                "load_case_result_sha256": canonical_sha256(ready),
                "training_partition_sha256": cls.load_protocol["partitions"]["training"],
                "holdout_partition_sha256": cls.load_protocol["partitions"]["holdout"],
            },
        }
        cls.evaluator = validate_search_protocol(
            cls.protocol, cls.baseline,
            baseline_protocol_sha256=sha("config/vehicle/fixed_topology_end_to_end_baseline_v1.json"),
        )
        cls.records = run_search_pilot(
            cls.protocol, cls.base_assembly, cls.work048, cls.baseline_protocol, cls.evaluator,
        )

    def test_equal_budget_and_exact_replay(self):
        self.assertEqual(288, len(self.records))
        counts = {t: sum(item.candidate.treatment == t for item in self.records) for t in self.protocol["treatments"]}
        self.assertEqual({96}, set(counts.values()))
        replay = run_search_pilot(
            self.protocol, self.base_assembly, self.work048, self.baseline_protocol, self.evaluator,
        )
        self.assertEqual(self.records, replay)
        self.assertEqual({self.evaluator}, {item.evaluator_sha256 for item in self.records})

    def test_evolution_ancestry_is_recorded(self):
        evolved = [item for item in self.records if item.candidate.treatment == "EVOLUTION" and item.candidate.attempt_index >= 8]
        self.assertTrue(evolved)
        self.assertTrue(all(item.candidate.parent_candidate_id for item in evolved))
        candidate_ids = {item.candidate.candidate_id for item in self.records}
        self.assertTrue(all(item.candidate.parent_candidate_id in candidate_ids for item in evolved))

    def test_holdout_and_readiness_block_on_refined_evaluator(self):
        promotions = promote_candidates(
            self.protocol, self.records, self.base_assembly, self.work048,
            self.baseline_protocol, self.evaluator,
        )
        self.assertEqual(9, len(promotions))
        self.assertEqual({"feasible"}, {item.holdout_status for item in promotions})
        self.assertEqual({"unavailable"}, {item.refined_status for item in promotions})
        review = readiness_decision(self.protocol, self.records, promotions, exact_replay=True, exploit_controls_passed=True)
        self.assertEqual("not_ready", review["decision"])
        self.assertEqual(("independent_refined_evaluation",), review["blockers"])

    def test_candidate_and_ledger_exploits_fail_closed(self):
        agent = DesignSearchAgentV0(self.protocol, "RANDOM", 101)
        candidate = agent.propose(0)
        unknown = replace(candidate, variables=candidate.variables + (("hidden_tolerance", 0.0),))
        with self.assertRaisesRegex(WholeVehicleSearchError, "opportunity"):
            evaluate_candidate(self.protocol, unknown, self.base_assembly, self.work048, self.baseline_protocol, self.evaluator, partition="training")
        bad = list(candidate.variables); bad[0] = (bad[0][0], float("nan"))
        with self.assertRaisesRegex(WholeVehicleSearchError, "outside"):
            evaluate_candidate(self.protocol, replace(candidate, variables=tuple(bad)), self.base_assembly, self.work048, self.baseline_protocol, self.evaluator, partition="training")
        skipped = agent.propose(1)
        result = evaluate_candidate(self.protocol, skipped, self.base_assembly, self.work048, self.baseline_protocol, self.evaluator, partition="training")
        with self.assertRaisesRegex(WholeVehicleSearchError, "append-only"):
            agent.observe(result)
        changed = copy.deepcopy(self.protocol); changed["seeds"] = [101, 202, 304]
        with self.assertRaisesRegex(WholeVehicleSearchError, "seeds"):
            validate_search_protocol(changed, self.baseline, baseline_protocol_sha256=sha("config/vehicle/fixed_topology_end_to_end_baseline_v1.json"))


if __name__ == "__main__":
    unittest.main()
