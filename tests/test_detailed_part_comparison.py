from __future__ import annotations
import copy,json
from pathlib import Path
import unittest
from formula_ultimate.experiments.detailed_part_comparison import DetailedPartComparisonViolation,paired_study,utility,validate_protocol
ROOT=Path(__file__).resolve().parents[1]; CONFIG=ROOT/"config/development/detailed_part_comparison_v1.json"
class DetailedPartComparisonTests(unittest.TestCase):
    def setUp(self): self.raw=json.loads(CONFIG.read_text(encoding="utf-8"))
    def test_registration_holdout_and_budget(self): self.assertEqual(validate_protocol(self.raw)["holdout_count"],6)
    def test_all_arms_are_optimized_with_matched_cost(self): self.assertEqual(len(set(paired_study(self.raw)["total_evaluations_by_arm"].values())),1)
    def test_fine_fidelity_can_reverse_coarse_ranking(self): self.assertGreater(paired_study(self.raw,"coarse")["mean_effect"],0); self.assertLess(paired_study(self.raw,"fine")["mean_effect"],0)
    def test_active_ablation_is_causal_but_inactive_is_not(self):
        tuned=2; active=utility(self.raw,"open_material",tuned,"holdout_1",active=True)["utility"]; ablated=utility(self.raw,"open_material",tuned,"holdout_1",active=False)["utility"]; self.assertGreater(active,ablated); self.assertEqual(utility(self.raw,"fixed_family",tuned,"holdout_1",active=True)["utility"],utility(self.raw,"fixed_family",tuned,"holdout_1",active=False)["utility"])
    def test_omitted_hardware_invalidates(self): self.assertEqual(utility(self.raw,"open_material",2,"holdout_1",hardware_complete=False)["status"],"invalid_omitted_hardware")
    def test_holdout_leak_fails_closed(self):
        bad=copy.deepcopy(self.raw); bad["conditions"]["training"].append("holdout_1")
        with self.assertRaisesRegex(DetailedPartComparisonViolation,"leakage"): validate_protocol(bad)
if __name__=="__main__": unittest.main()
