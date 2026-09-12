from __future__ import annotations
import copy,json
from pathlib import Path
import unittest
from formula_ultimate.search.multiscale_discovery_search import BudgetLedger,DiscoverySearchViolation,cache_key,cache_valid,candidate_admission,classify,run_policy,validate_protocol,verify_candidate
ROOT=Path(__file__).resolve().parents[1]; CONFIG=ROOT/"config/development/multiscale_discovery_search_v1.json"
class MultiscaleDiscoverySearchTests(unittest.TestCase):
    def setUp(self):
        self.raw=json.loads(CONFIG.read_text(encoding="utf-8"))
        for candidate in self.raw["candidates"]: candidate["admission_sha256"]=candidate_admission(candidate)
    def test_protocol_and_matched_opportunity(self): self.assertEqual(validate_protocol(self.raw)["candidate_count"],8)
    def test_budget_exhaustion_occurs_before_execution(self):
        ledger=BudgetLedger({"solver":1}); first=ledger.reserve("solver",1,"a",1); ledger.complete(first,"executed_charged"); second=ledger.reserve("solver",1,"b",1); self.assertEqual(second["status"],"not_evaluated_budget_exhausted"); self.assertEqual(ledger.used["solver"],1)
    def test_failed_attempt_is_charged(self):
        result=run_policy(self.raw,"score_first","deps"); self.assertTrue(any(x["status"]=="failed_charged" for x in result["ledger"]["records"])); self.assertGreater(result["unknown_count"],0)
    def test_cache_invalidation_and_tamper(self):
        candidate=self.raw["candidates"][0]; entry={"key":cache_key(candidate,"old")}; self.assertFalse(cache_valid(entry,candidate,"new")); bad=copy.deepcopy(candidate); bad["claimed_effect"]=99
        with self.assertRaisesRegex(DiscoverySearchViolation,"tampered"): verify_candidate(bad)
    def test_inactive_appendage_has_zero_effect(self):
        candidate=next(x for x in self.raw["candidates"] if x["candidate_id"]=="c3"); self.assertEqual(classify(candidate,.03,.05)["signed_effect"],0)
    def test_same_topology_useful_shape_is_eligible(self):
        base=self.raw["candidates"][0]; changed=self.raw["candidates"][1]; decision=classify(changed,.03,.05); self.assertEqual(base["topology_id"],changed["topology_id"]); self.assertTrue(decision["useful_shape"]); self.assertFalse(decision["graph_novelty_required"])
if __name__=="__main__": unittest.main()
