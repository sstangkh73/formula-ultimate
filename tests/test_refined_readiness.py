import copy
import unittest

from formula_ultimate.experiments.refined_readiness import (
    ReadinessAdjudicationError,
    adjudicate_refined_readiness,
)


def fixtures():
    treatments = ("GRID", "RANDOM", "EVOLUTION")
    promotions = []
    refined = []
    rejected = {"GRID-2", "EVOLUTION-3"}
    objective = 10.0
    for treatment in treatments:
        for index in range(1, 4):
            candidate_id = f"{treatment}-{index}"
            promotions.append({
                "candidate_id": candidate_id,
                "treatment": treatment,
                "holdout_objective": objective,
                "holdout_status": "feasible",
            })
            passed = candidate_id not in rejected
            refined.append({
                "candidate_id": candidate_id,
                "status": "passed" if passed else "failed",
                "holdout_cases": [
                    {"case_id": "a", "status": "passed" if passed else "failed"},
                    {"case_id": "b", "status": "passed" if passed else "failed"},
                ],
            })
            objective += 1.0
    work050 = {
        "status": "passed",
        "promotions": promotions,
        "readiness": {
            "checks": {
                "complete_provenance": True,
                "equal_budget": True,
                "exact_replay": True,
                "holdout_pass": True,
                "independent_refined_evaluation": False,
                "no_exploit": True,
                "same_evaluator": True,
            },
            "attempt_counts": {name: 96 for name in treatments},
            "blockers": ["independent_refined_evaluation"],
        },
    }
    work053 = {
        "status": "passed",
        "decision": "independent_refined_evaluator_available",
        "promotion_results": refined,
    }
    return work050, work053


class RefinedReadinessTests(unittest.TestCase):
    def test_ready_result_reranks_only_supported_candidates(self):
        work050, work053 = fixtures()
        result = adjudicate_refined_readiness(work050, work053)
        self.assertEqual("ready_for_bounded_whole_vehicle_campaign", result["decision"])
        self.assertEqual(7, result["supported_candidates"])
        self.assertEqual("GRID-1", result["global_winner"]["candidate_id"])
        self.assertEqual("GRID-1", result["treatment_results"]["GRID"]["winner_candidate_id"])
        self.assertEqual([], result["blockers"])
        self.assertEqual(result, adjudicate_refined_readiness(work050, work053))

    def test_insufficient_supported_candidates_stays_not_ready(self):
        work050, work053 = fixtures()
        random_two = next(item for item in work053["promotion_results"] if item["candidate_id"] == "RANDOM-2")
        random_two["status"] = "failed"
        for case in random_two["holdout_cases"]:
            case["status"] = "failed"
        random_three = next(item for item in work053["promotion_results"] if item["candidate_id"] == "RANDOM-3")
        random_three["status"] = "failed"
        for case in random_three["holdout_cases"]:
            case["status"] = "failed"
        result = adjudicate_refined_readiness(work050, work053)
        self.assertEqual("not_ready", result["decision"])
        self.assertIn("minimum_supported_per_treatment", result["blockers"])

    def test_extra_original_blocker_fails_closed(self):
        work050, work053 = fixtures()
        work050["readiness"]["checks"]["no_exploit"] = False
        with self.assertRaisesRegex(ReadinessAdjudicationError, "additional"):
            adjudicate_refined_readiness(work050, work053)

    def test_identity_and_aggregate_contradictions_fail_closed(self):
        work050, work053 = fixtures()
        duplicate = copy.deepcopy(work053["promotion_results"][0])
        work053["promotion_results"][1] = duplicate
        with self.assertRaisesRegex(ReadinessAdjudicationError, "duplicated"):
            adjudicate_refined_readiness(work050, work053)
        work050, work053 = fixtures()
        item = work053["promotion_results"][0]
        item["status"] = "passed"
        item["holdout_cases"][0]["status"] = "failed"
        with self.assertRaisesRegex(ReadinessAdjudicationError, "contradicts"):
            adjudicate_refined_readiness(work050, work053)


if __name__ == "__main__":
    unittest.main()
