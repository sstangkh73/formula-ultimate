from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from formula_ultimate.experiments.discovery_audit import (
    compare_execution, proxy_audit, ranked_selection, stratified_sample,
)
from formula_ultimate.experiments.discovery_evidence import (
    apply_outcome, exploration_permission, legacy_annotation, promotion_decision,
)
from formula_ultimate.experiments.discovery_ledger import DiscoveryLedger, account_key, scientific_summary
from formula_ultimate.experiments.discovery_registration import (
    DiscoveryViolation, digest, freeze, strict_json, validate_registration,
)
from scripts.experiments.run_discovery_contract import (
    evaluate, fixture_candidate, fixture_cost, fixture_outcome, measured, reserve, run_fixture,
)

ROOT = Path(__file__).resolve().parents[1]


def registration():
    return strict_json((ROOT / "config/experiments/discovery_contract_fixture_v1.json").read_text(encoding="utf-8"))


class RegistrationTests(unittest.TestCase):
    def test_frozen_fixture_is_complete_and_explicitly_nonscientific(self):
        reg = registration()
        body = validate_registration(reg, expected_sha256=reg["registration_sha256"])
        self.assertEqual("software_fixture", body["evidence_class"])
        self.assertEqual(2, body["analysis"]["sample_size"])

    def test_missing_top_level_fields_never_admit(self):
        body = registration()["body"]
        for key in body:
            with self.subTest(key=key):
                changed = deepcopy(body)
                del changed[key]
                with self.assertRaises(DiscoveryViolation):
                    freeze(changed)

    def test_changed_registration_cannot_continue_old_identity(self):
        reg = registration()
        old = reg["registration_sha256"]
        reg["body"]["gates"][0]["threshold"] = 2.0
        with self.assertRaisesRegex(DiscoveryViolation, "identity changed"):
            validate_registration(reg)
        new = freeze(reg["body"])
        with self.assertRaisesRegex(DiscoveryViolation, "frozen registration"):
            validate_registration(new, expected_sha256=old)

    def test_numeric_thresholds_samples_and_units_cannot_be_blank_or_nonfinite(self):
        for key, bad in (("threshold", None), ("threshold", True), ("threshold", float("nan")),
                         ("error_limit", -1), ("unit", ""), ("minimum_refinements", 0)):
            with self.subTest(key=key, bad=bad):
                body = registration()["body"]
                body["gates"][0][key] = bad
                with self.assertRaises(DiscoveryViolation):
                    freeze(body)

    def test_fixture_evaluator_cannot_be_reclassified_by_campaign_label(self):
        body = registration()["body"]
        body["evidence_class"] = "admitted_simulation"
        with self.assertRaisesRegex(DiscoveryViolation, "class mismatch"):
            freeze(body)

    def test_partition_overlap_and_holdout_feedback_reject(self):
        body = registration()["body"]
        body["partitions"]["holdout"] = body["partitions"]["training"]
        with self.assertRaisesRegex(DiscoveryViolation, "leakage"):
            freeze(body)
        body = registration()["body"]
        body["execution"]["holdout_feedback"] = True
        with self.assertRaises(DiscoveryViolation):
            freeze(body)

    def test_missing_gates_independence_and_refinement_reject(self):
        for mutation in ("missing_safety", "same_solver", "two_levels", "unregistered_evaluator"):
            body = registration()["body"]
            if mutation == "missing_safety":
                body["promotion_gates"].remove("safety")
            elif mutation == "same_solver":
                body["evaluators"][1]["implementation_sha256"] = body["evaluators"][0]["implementation_sha256"]
            elif mutation == "two_levels":
                body["gates"][1]["minimum_refinements"] = 2
            else:
                body["gates"][0]["evaluator_id"] = "missing"
            with self.subTest(mutation=mutation), self.assertRaises(DiscoveryViolation):
                freeze(body)

    def test_independent_source_cannot_be_lower_fidelity_than_survivor(self):
        body = registration()["body"]
        body["gates"][-1]["fidelity_rank"] = 1
        with self.assertRaisesRegex(DiscoveryViolation, "source fidelity"):
            freeze(body)

    def test_empty_audit_budget_and_unsupported_cache_policy_reject(self):
        for mutation in ("audit_zero", "cache_free", "worker_boolean", "counter_boolean", "workers_two"):
            body = registration()["body"]
            if mutation == "audit_zero":
                body["budget"]["pools"]["audit"]["cpu_s"] = 0
            elif mutation == "cache_free":
                body["budget"]["cache_policy"] = "free"
            elif mutation == "counter_boolean":
                body["budget"]["pools"]["quality"]["attempts"] = True
            else:
                body["execution"]["workers"] = True if mutation == "worker_boolean" else 2
            with self.subTest(mutation=mutation), self.assertRaises(DiscoveryViolation):
                freeze(body)

    def test_malformed_types_have_protocol_error_not_scientific_failure(self):
        for key, value in (("evidence_class", []), ("seeds", [True]), ("evaluators", [None]), ("budget", None)):
            body = registration()["body"]
            body[key] = value
            with self.subTest(key=key), self.assertRaises(DiscoveryViolation):
                freeze(body)

    def test_duplicate_json_keys_and_nonfinite_json_reject(self):
        for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{'):
            with self.subTest(raw=raw), self.assertRaises(DiscoveryViolation):
                strict_json(raw)


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "ledger.jsonl"
        self.reg = registration()
        self.ledger = DiscoveryLedger(self.path, self.reg)

    def ready(self, cid="a", **kwargs):
        measured(self.ledger, cid, **kwargs)
        return cid

    def snapshot(self, cid="a"):
        return self.ledger.replay()["state"]["states"][cid]

    def reserve_start(self, cid="a", scope="structural_coarse", **kwargs):
        aid = reserve(self.ledger, cid, scope, **kwargs)
        self.ledger.append({"type": "start", "id": aid})
        return aid

    def settle(self, aid, result, **cost):
        return self.ledger.append({"type": "settle", "id": aid, "observed_cost": fixture_cost(**cost),
                                   "result": result, "diagnostics": {"test": True}})

    def promote(self, cid="a", target="candidate_survivor"):
        return self.ledger.append({"type": "promote", "candidate_id": cid, "target": target,
                                   "use": self.reg["body"]["promotion_scope"]})

    def test_unsealed_geometry_and_boundary_are_bound_once(self):
        self.ready(unsealed=True)
        self.assertIsNotNone(self.snapshot()["context"]["geometry_sha256"])
        self.assertIsNotNone(self.snapshot()["context"]["boundary_sha256"])
        self.assertIsNone(self.ledger.replay()["state"]["candidates"]["a"]["context"]["geometry_sha256"])

    def test_initial_promotion_is_explicitly_not_ready(self):
        self.ready()
        self.assertEqual("not_ready", self.snapshot()["promotion"][self.reg["body"]["promotion_scope"]]["status"])

    def test_physics_manufacturing_and_fidelity_states_coexist(self):
        self.ready()
        evaluate(self.ledger, "a", "structural_coarse")
        evaluate(self.ledger, "a", "structural_fine", status="numerically_unresolved", reason="mesh_failure")
        evaluate(self.ledger, "a", "additive", value=2)
        evaluate(self.ledger, "a", "machining")
        s = self.snapshot()
        self.assertEqual("physically_feasible", s["physics"]["structural_coarse"]["status"])
        self.assertEqual("numerically_unresolved", s["physics"]["structural_fine"]["status"])
        self.assertEqual("manufacturing_incompatible", s["manufacturing"]["additive"]["status"])
        self.assertEqual("manufacturing_compatible", s["manufacturing"]["machining"]["status"])

    def test_physical_failure_is_normal_settled_evidence_and_search_continues(self):
        self.ready()
        evaluate(self.ledger, "a", "structural_coarse", value=2)
        self.ready("b", parents=["a"])
        self.assertEqual("physically_failed", self.snapshot()["physics"]["structural_coarse"]["status"])
        self.assertFalse(self.ledger.replay()["state"]["stopped"])

    def test_numerical_failure_cannot_claim_physical_failure(self):
        self.ready()
        out = fixture_outcome(self.ledger, "a", "structural_coarse", status="numerically_unresolved", reason="solver_divergence")
        out["status"] = "physically_failed"
        with self.assertRaises(DiscoveryViolation):
            self.settle(self.reserve_start(), out)

    def test_all_causal_identity_changes_reject_even_with_rehashed_artifact(self):
        self.ready()
        original = fixture_outcome(self.ledger, "a", "structural_coarse")
        state = self.ledger.replay()["state"]
        for key in original["context"]:
            changed = deepcopy(original)
            changed["context"][key] = "other" if key == "candidate_id" else digest(["changed", key])
            changed["artifact"]["body"]["context_sha256"] = digest(changed["context"])
            changed["artifact"]["sha256"] = digest(changed["artifact"]["body"])
            with self.subTest(key=key), self.assertRaises(DiscoveryViolation):
                apply_outcome(state["states"]["a"], state["candidates"]["a"], changed, self.reg["body"])

    def test_tampered_evaluator_metric_unit_class_and_convergence_reject(self):
        self.ready()
        original = fixture_outcome(self.ledger, "a", "structural_fine")
        s = self.ledger.replay()["state"]
        changes = {"evaluator_id": "fake", "implementation_sha256": digest("fake"), "validation_sha256": digest("fake"),
                   "metric": "fake", "unit": "kg", "evidence_class": "admitted_simulation", "converged": False,
                   "error": 1.0, "refinements": [4, 4, 8], "evidence_type": "scalar", "dataset_id": "holdout_fixture"}
        for key, value in changes.items():
            out = deepcopy(original)
            out["artifact"]["body"][key] = value
            out["artifact"]["sha256"] = digest(out["artifact"]["body"])
            with self.subTest(key=key), self.assertRaises(DiscoveryViolation):
                apply_outcome(s["states"]["a"], s["candidates"]["a"], out, self.reg["body"])

    def test_wrong_threshold_label_rejects(self):
        self.ready()
        out = fixture_outcome(self.ledger, "a", "structural_coarse", value=2, status="physically_feasible")
        with self.assertRaisesRegex(DiscoveryViolation, "threshold"):
            self.settle(self.reserve_start(), out)

    def test_boundary_unresolved_and_representation_invalid_are_separate(self):
        for cid in ("bad", "unbound"):
            self.ledger.append({"type": "candidate", "candidate": fixture_candidate(self.reg, cid)})
        evaluate(self.ledger, "bad", "representation", status="representation_invalid")
        evaluate(self.ledger, "unbound", "representation")
        evaluate(self.ledger, "unbound", "boundary", status="boundary_unresolved")
        self.assertEqual("representation_invalid", self.snapshot("bad")["representation"])
        self.assertEqual("boundary_unresolved", self.snapshot("unbound")["boundary"])

    def test_unknown_physics_and_timeout_preserve_distinct_reason(self):
        self.ready()
        evaluate(self.ledger, "a", "structural_coarse", status="not_evaluated", reason="unsupported_physics")
        evaluate(self.ledger, "a", "structural_fine", status="numerically_unresolved", reason="timeout")
        s = self.snapshot()["physics"]
        self.assertEqual("not_evaluated", s["structural_coarse"]["status"])
        self.assertEqual("timeout", s["structural_fine"]["reason"])

    def test_exploratory_integration_without_full_physics_never_grants_promotion(self):
        self.ready()
        declaration = {"missing_domains": ["flow"], "approximations": ["bounded_proxy"],
                       "interfaces_sha256": digest("interfaces"), "scope": "trial"}
        permit = exploration_permission(self.snapshot(), declaration)
        self.assertTrue(permit["eligible"])
        self.assertFalse(permit["promotion_allowed"])
        with self.assertRaisesRegex(DiscoveryViolation, "promotion evidence"):
            self.promote()

    def test_unbound_exploratory_assembly_rejects(self):
        self.ledger.append({"type": "candidate", "candidate": fixture_candidate(self.reg, "a")})
        with self.assertRaises(DiscoveryViolation):
            exploration_permission(self.snapshot(), {"missing_domains": [], "approximations": [],
                "interfaces_sha256": digest("interfaces"), "scope": "trial"})

    def test_complete_fixture_promotion_never_counts_as_science(self):
        self.ready()
        for gate in self.reg["body"]["promotion_gates"]:
            evaluate(self.ledger, "a", gate, pool="finalist")
        self.promote()
        self.promote(target="promotion_ready")
        d = self.snapshot()["promotion"][self.reg["body"]["promotion_scope"]]
        self.assertEqual("promotion_ready", d["status"])
        self.assertFalse(d["scientific_survivor"])
        self.assertFalse(d["physical_validation"])

    def test_missing_each_survivor_gate_and_unregistered_use_reject(self):
        self.ready()
        for gate in self.reg["body"]["survivor_gates"]:
            evaluate(self.ledger, "a", gate, pool="finalist")
        state = self.snapshot()
        for dim, gate in (("physics", "structural_fine"), ("manufacturing", "additive"), ("gate", "holdout"), ("gate", "replay")):
            partial = deepcopy(state)
            del partial[dim][gate]
            with self.subTest(gate=gate), self.assertRaises(DiscoveryViolation):
                promotion_decision(partial, self.reg["body"], "candidate_survivor", self.reg["body"]["promotion_scope"])
        with self.assertRaisesRegex(DiscoveryViolation, "unregistered promotion use"):
            promotion_decision(state, self.reg["body"], "candidate_survivor", "whole_vehicle_certified")

    def test_holdout_evidence_cannot_feed_a_new_training_child(self):
        self.ready()
        evaluate(self.ledger, "a", "holdout", pool="finalist")
        with self.assertRaisesRegex(DiscoveryViolation, "holdout feedback"):
            self.ledger.append({"type": "candidate", "candidate": fixture_candidate(self.reg, "child", parents=["a"])})

    def test_descendant_cannot_cross_treatment_or_modify_parent(self):
        self.ready()
        before = self.snapshot()
        child = fixture_candidate(self.reg, "child", parents=["a"], treatment="CONVENTIONAL_CONTROL")
        with self.assertRaisesRegex(DiscoveryViolation, "cross-treatment"):
            self.ledger.append({"type": "candidate", "candidate": child})
        child["treatment"] = "OPEN_ARCHITECTURE"
        self.ledger.append({"type": "candidate", "candidate": child})
        self.assertEqual(before, self.snapshot())
        with self.assertRaisesRegex(DiscoveryViolation, "already exists"):
            self.ledger.append({"type": "candidate", "candidate": child})

    def test_genotype_change_requires_real_identity_and_mutation_trace(self):
        self.ready()
        child = fixture_candidate(self.reg, "child", parents=["a"])
        child["genotype"]["parameter"] += 1
        with self.assertRaisesRegex(DiscoveryViolation, "genotype identity"):
            self.ledger.append({"type": "candidate", "candidate": child})
        child["context"]["genotype_sha256"] = digest(child["genotype"])
        child["mutation_trace"] = []
        with self.assertRaisesRegex(DiscoveryViolation, "mutation trace"):
            self.ledger.append({"type": "candidate", "candidate": child})

    def test_reopen_exact_replay_and_caller_mutation_do_not_change_history(self):
        self.ready()
        expected = self.ledger.replay()
        reopened = DiscoveryLedger(self.path, self.reg, expected_head=expected["head_sha256"])
        self.assertEqual(expected, reopened.replay())
        expected["state"]["states"]["a"]["representation"] = "representation_invalid"
        self.assertEqual("geometry_measured", reopened.replay()["state"]["states"]["a"]["representation"])

    def test_changed_registration_on_reopen_rejects(self):
        self.ready()
        body = deepcopy(self.reg["body"])
        body["analysis"]["minimum_effect"] = 0.2
        with self.assertRaisesRegex(DiscoveryViolation, "registration changed"):
            DiscoveryLedger(self.path, freeze(body))

    def test_tampered_rehashed_illegal_state_still_rejects(self):
        self.ready()
        rows = [json.loads(line) for line in self.path.read_text().splitlines()]
        rows[-1]["event"]["result"]["status"] = "physically_feasible"
        rows[-1]["sha256"] = digest({k:v for k,v in rows[-1].items() if k != "sha256"})
        self.path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
        with self.assertRaisesRegex(DiscoveryViolation, "outcome state"):
            DiscoveryLedger(self.path, self.reg)

    def test_hash_tampering_and_partial_tail_fail_closed(self):
        self.ready()
        raw = self.path.read_bytes()
        self.path.write_bytes(raw[:-4])
        with self.assertRaisesRegex(DiscoveryViolation, "truncated"):
            DiscoveryLedger(self.path, self.reg)
        rows = raw.splitlines()
        first = json.loads(rows[0])
        first["event"]["candidate"]["representation"] = "shell"
        rows[0] = json.dumps(first).encode()
        self.path.write_bytes(b"\n".join(rows) + b"\n")
        with self.assertRaisesRegex(DiscoveryViolation, "hash mismatch"):
            DiscoveryLedger(self.path, self.reg)

    def test_trusted_head_detects_whole_record_rollback(self):
        self.ready()
        head = self.ledger.replay()["head_sha256"]
        lines = self.path.read_bytes().splitlines(keepends=True)
        self.path.write_bytes(b"".join(lines[:-1]))
        with self.assertRaisesRegex(DiscoveryViolation, "checkpoint"):
            DiscoveryLedger(self.path, self.reg, expected_head=head)

    def test_writer_lock_and_stale_reader_reject_concurrent_append(self):
        self.ready()
        stale = DiscoveryLedger(self.path, self.reg, expected_head=self.ledger.replay()["head_sha256"])
        reserve(self.ledger, "a", "structural_coarse")
        with self.assertRaisesRegex(DiscoveryViolation, "checkpoint"):
            stale.replay()
        lock = self.path.with_name(self.path.name + ".lock")
        lock.write_text("other writer")
        with self.assertRaisesRegex(DiscoveryViolation, "writer lock"):
            self.ledger.append({"type": "quarantine", "source_sha256": digest("bad"), "reason": "bad"})

    def test_duplicate_unreserved_and_unstarted_results_reject(self):
        self.ready()
        result = fixture_outcome(self.ledger, "a", "structural_coarse")
        with self.assertRaisesRegex(DiscoveryViolation, "unreserved"):
            self.settle("missing", result)
        aid = reserve(self.ledger, "a", "structural_coarse")
        with self.assertRaisesRegex(DiscoveryViolation, "before invocation"):
            self.settle(aid, result)
        self.ledger.append({"type": "start", "id": aid})
        self.settle(aid, result)
        with self.assertRaisesRegex(DiscoveryViolation, "duplicate settlement"):
            self.settle(aid, result)

    def test_serial_reservation_cannot_be_overbooked(self):
        self.ready()
        reserve(self.ledger, "a", "structural_coarse")
        with self.assertRaisesRegex(DiscoveryViolation, "pending attempt"):
            reserve(self.ledger, "a", "structural_fine")

    def test_recovery_before_start_is_not_evaluated_and_charges_one_attempt(self):
        self.ready()
        aid = reserve(self.ledger, "a", "structural_coarse")
        self.ledger = DiscoveryLedger(self.path, self.reg, expected_head=self.ledger.replay()["head_sha256"])
        self.ledger.append({"type": "recover", "id": aid})
        state = self.ledger.replay()["state"]
        a = state["attempts"][aid]
        self.assertEqual(1, a["charged"]["attempts"])
        self.assertEqual(0, a["charged"]["cpu_s"])
        self.assertEqual("not_evaluated", a["result"]["status"])
        self.assertTrue(state["accounting_complete"])

    def test_started_lost_output_remains_unknown_cost_and_unresolved(self):
        self.ready()
        aid = self.reserve_start()
        self.ledger = DiscoveryLedger(self.path, self.reg, expected_head=self.ledger.replay()["head_sha256"])
        self.ledger.append({"type": "recover", "id": aid})
        a = self.ledger.replay()["state"]["attempts"][aid]
        self.assertEqual(0.25, a["charged"]["cpu_s"])
        self.assertIsNone(a["observed_cost"])
        self.assertEqual("numerically_unresolved", a["result"]["status"])
        self.assertFalse(self.ledger.replay()["state"]["accounting_complete"])
        evaluate(self.ledger, "a", "structural_coarse", retry_of=aid)
        self.assertEqual("lost_output", self.snapshot()["history"][-2]["reason"])

    def test_current_scientific_summary_blocks_unknown_spending_even_for_prior_decisions(self):
        self.ready()
        aid = self.reserve_start()
        self.ledger.append({"type": "recover", "id": aid})
        state = self.ledger.replay()["state"]
        # Inject a previously admitted decision into a reporting fixture to falsify aggregation.
        state["states"]["a"]["promotion"][self.reg["body"]["promotion_scope"]]["scientific_survivor"] = True
        summary = scientific_summary(state)
        self.assertEqual(0, summary["scientific_survivors"])
        self.assertIn("unknown_actual_cost", summary["blocking_reasons"])

    def test_pending_work_blocks_promotion_and_current_scientific_count(self):
        self.ready()
        reserve(self.ledger, "a", "structural_coarse")
        with self.assertRaisesRegex(DiscoveryViolation, "unsettled cost"):
            self.promote()
        self.assertIn("pending_cost", scientific_summary(self.ledger.replay()["state"])["blocking_reasons"])

    def test_retry_limit_cannot_be_evaded_by_new_ids_or_old_parent(self):
        self.ready()
        first = evaluate(self.ledger, "a", "structural_coarse", status="numerically_unresolved", reason="timeout")
        with self.assertRaisesRegex(DiscoveryViolation, "explicit retry"):
            reserve(self.ledger, "a", "structural_coarse")
        second = evaluate(self.ledger, "a", "structural_coarse", retry_of=first, status="numerically_unresolved", reason="timeout")
        with self.assertRaisesRegex(DiscoveryViolation, "latest attempt"):
            reserve(self.ledger, "a", "structural_coarse", retry_of=first)
        third = evaluate(self.ledger, "a", "structural_coarse", retry_of=second, status="numerically_unresolved", reason="timeout")
        with self.assertRaisesRegex(DiscoveryViolation, "retry limit"):
            reserve(self.ledger, "a", "structural_coarse", retry_of=third)

    def test_repeat_failed_design_cannot_be_silently_repaired(self):
        self.ready()
        first = evaluate(self.ledger, "a", "structural_coarse", value=2)
        with self.assertRaisesRegex(DiscoveryViolation, "explicit retry"):
            reserve(self.ledger, "a", "structural_coarse")
        with self.assertRaisesRegex(DiscoveryViolation, "not unresolved"):
            reserve(self.ledger, "a", "structural_coarse", retry_of=first)

    def test_cache_reuse_charges_full_source_cost_and_preserves_observed_cost(self):
        self.ready()
        first = evaluate(self.ledger, "a", "structural_coarse")
        result = fixture_outcome(self.ledger, "a", "structural_coarse")
        aid = reserve(self.ledger, "a", "structural_coarse", cache_of=first, cost=fixture_cost(cache_hits=1))
        self.ledger.append({"type": "start", "id": aid})
        self.settle(aid, result, cpu_s=0.01, wall_s=0.01, cache_hits=1)
        a = self.ledger.replay()["state"]["attempts"][aid]
        self.assertEqual(0.25, a["charged"]["cpu_s"])
        self.assertEqual(0.01, a["observed_cost"]["cpu_s"])
        self.assertEqual(1, a["charged"]["cache_hits"])

    def test_cache_cannot_change_candidate_result_or_avoid_charge(self):
        self.ready()
        first = evaluate(self.ledger, "a", "structural_coarse")
        with self.assertRaisesRegex(DiscoveryViolation, "full registered charge"):
            reserve(self.ledger, "a", "structural_coarse", cache_of=first, cost=fixture_cost(cpu_s=0.01, cache_hits=1))
        self.ready("b")
        with self.assertRaisesRegex(DiscoveryViolation, "context mismatch"):
            reserve(self.ledger, "b", "structural_coarse", cache_of=first, cost=fixture_cost(cache_hits=1))
        aid = reserve(self.ledger, "a", "structural_coarse", cache_of=first, cost=fixture_cost(cache_hits=1))
        self.ledger.append({"type": "start", "id": aid})
        with self.assertRaisesRegex(DiscoveryViolation, "cache result changed"):
            self.settle(aid, fixture_outcome(self.ledger, "a", "structural_coarse", value=0.1), cache_hits=1)

    def test_overshoot_is_recorded_not_clamped_and_stops_next_operation(self):
        self.ready()
        result = fixture_outcome(self.ledger, "a", "structural_coarse")
        aid = self.reserve_start()
        self.settle(aid, result, cpu_s=2)
        state = self.ledger.replay()["state"]
        self.assertTrue(state["stopped"])
        self.assertEqual(2, state["attempts"][aid]["charged"]["cpu_s"])
        with self.assertRaisesRegex(DiscoveryViolation, "stopped"):
            reserve(self.ledger, "a", "structural_fine")

    def test_budget_exhaustion_is_visible_without_solver_invocation(self):
        body = deepcopy(self.reg["body"])
        body["budget"]["pools"]["exploration"]["cpu_s"] = 0.5
        self.reg = freeze(body)
        self.ledger = DiscoveryLedger(self.path, self.reg)
        self.ready()
        with self.assertRaisesRegex(DiscoveryViolation, "budget exhausted"):
            reserve(self.ledger, "a", "structural_coarse")
        self.ledger.append({"type": "defer", "candidate_id": "a", "pool": "exploration", "dimension": "physics",
                           "scope": "structural_coarse", "cost": fixture_cost(), "reason": "budget_exhausted"})
        state = self.ledger.replay()["state"]
        self.assertEqual("not_evaluated", self.snapshot()["physics"]["structural_coarse"]["status"])
        self.assertEqual("budget_exhausted", state["deferrals"][0]["disposition"])
        self.assertEqual(2, len(state["attempts"]))

    def test_resource_pools_and_treatment_opportunity_are_independent(self):
        body = deepcopy(self.reg["body"])
        body["budget"]["pools"]["exploration"]["cpu_s"] = 0.5
        self.reg = freeze(body)
        self.ledger = DiscoveryLedger(self.path, self.reg)
        self.ready()
        self.ready("b", treatment="CONVENTIONAL_CONTROL")
        aid = reserve(self.ledger, "a", "structural_fine", pool="finalist")
        self.assertEqual("pending", self.ledger.replay()["state"]["attempts"][aid]["disposition"])

    def test_peak_memory_is_not_summed_and_every_proposal_is_counted(self):
        self.ready()
        state = self.ledger.replay()["state"]
        cost = state["accounts"][account_key(state["candidates"]["a"], "exploration")]
        self.assertEqual(1024, cost["peak_memory_bytes"])
        self.assertEqual(1, cost["proposals"])
        self.assertEqual(2, cost["attempts"])
        self.assertEqual(0.5, cost["cpu_s"])

    def test_negative_unknown_and_boolean_costs_reject(self):
        self.ready()
        for change in ({"cpu_s": -1}, {"cpu_s": None}, {"attempts": True}, {"extra": 2}):
            with self.subTest(change=change), self.assertRaises(DiscoveryViolation):
                reserve(self.ledger, "a", "structural_coarse", cost=fixture_cost(**change))

    def test_audit_pool_cannot_be_spent_without_score_independent_selection(self):
        self.ready()
        evaluate(self.ledger, "a", "structural_coarse", value=2)
        with self.assertRaisesRegex(DiscoveryViolation, "missing selection"):
            reserve(self.ledger, "a", "structural_fine", pool="audit")
        self.ledger.append({"type": "select", "pool": "audit", "gate_id": "structural_coarse"})
        chosen = self.ledger.replay()["state"]["selections"][-1]
        evaluate(self.ledger, "a", "structural_fine", pool="audit", selection_sha256=chosen["selection_sha256"])
        report = self.ledger.audit_report(chosen["selection_sha256"], "structural_fine")
        stratum = next(iter(report["strata"].values()))
        self.assertEqual(1, stratum["false_negatives"])
        self.assertEqual(1, stratum["known_reference_fnr"])

    def test_audit_rejects_same_or_lower_fidelity_reference(self):
        self.ready()
        evaluate(self.ledger, "a", "structural_fine")
        self.ledger.append({"type": "select", "pool": "audit", "gate_id": "structural_fine"})
        chosen = self.ledger.replay()["state"]["selections"][-1]
        with self.assertRaisesRegex(DiscoveryViolation, "higher comparable fidelity"):
            self.ledger.audit_report(chosen["selection_sha256"], "structural_coarse")

    def test_relabeling_fixture_artifact_as_science_is_rejected(self):
        self.ready()
        state = self.ledger.replay()["state"]
        artifact = fixture_outcome(self.ledger, "a", "structural_fine")
        admitted = deepcopy(self.reg["body"])
        admitted["evidence_class"] = "admitted_simulation"
        for ev in admitted["evaluators"]:
            ev["evidence_class"] = "admitted_simulation"
        artifact["artifact"]["body"]["evidence_class"] = "admitted_simulation"
        artifact["artifact"]["sha256"] = digest(artifact["artifact"]["body"])
        with self.assertRaisesRegex(DiscoveryViolation, "synthetic fixture"):
            apply_outcome(state["states"]["a"], state["candidates"]["a"], artifact, admitted)

    def test_quality_and_unresolved_stepping_stone_selection_are_replayable(self):
        self.ready()
        evaluate(self.ledger, "a", "structural_coarse", status="numerically_unresolved", reason="timeout")
        self.ledger.append({"type": "select", "pool": "stepping_stone", "gate_id": "structural_coarse"})
        chosen = self.ledger.replay()["state"]["selections"][-1]
        self.assertEqual([{"candidate_id": "a"}], chosen["selection"]["selected"])
        self.assertEqual(self.ledger.replay(), DiscoveryLedger(self.path, self.reg).replay())

    def test_protocol_invalid_is_quarantined_not_a_physics_result(self):
        self.ledger.append({"type": "quarantine", "source_sha256": digest("bad"), "reason": "bad provenance"})
        state = self.ledger.replay()["state"]
        self.assertEqual("protocol_invalid", state["quarantines"][0]["disposition"])
        self.assertFalse(state["states"])


class AuditAndReplayTests(unittest.TestCase):
    def population(self):
        return [{"candidate_id": f"c{i}", "stratum": "free_form" if i < 4 else "primitive", "proxy_score": i}
                for i in range(6)]

    def test_stratified_selection_ignores_scores_and_input_order(self):
        population = self.population()
        first = stratified_sample(population, seed=7, per_stratum=2)
        for row in population:
            row["proxy_score"] = -10000 * row["proxy_score"]
        second = stratified_sample(list(reversed(population)), seed=7, per_stratum=2)
        self.assertEqual(first, second)
        self.assertEqual({0.5, 1.0}, {r["inclusion_probability"] for r in first["selected"]})

    def test_unknown_reference_does_not_become_negative_or_fake_rate(self):
        sample = stratified_sample(self.population(), seed=7, per_stratum=2)
        labels = [{"candidate_id": r["candidate_id"], "proxy_pass": False, "reference_pass": None}
                  for r in sample["selected"]]
        report = proxy_audit(sample, labels)
        self.assertIsNone(report["pooled_rate"])
        for s in report["strata"].values():
            self.assertEqual("not_estimable", s["status"])
            self.assertEqual(0, s["reference_negative"])
            self.assertIsNone(s["known_reference_fnr"])
            self.assertEqual([0, 1], s["fnr_unknown_bounds"])

    def test_fnr_and_fpr_use_reference_class_denominators(self):
        pop = [{"candidate_id": str(i), "stratum": "one", "proxy_score": i} for i in range(4)]
        sample = stratified_sample(pop, seed=7, per_stratum=4)
        labels = [{"candidate_id": "0", "proxy_pass": False, "reference_pass": True},
                  {"candidate_id": "1", "proxy_pass": True, "reference_pass": True},
                  {"candidate_id": "2", "proxy_pass": True, "reference_pass": False},
                  {"candidate_id": "3", "proxy_pass": False, "reference_pass": False}]
        s = proxy_audit(sample, labels)["strata"]["one"]
        self.assertEqual(0.5, s["known_reference_fnr"])
        self.assertEqual(0.5, s["known_reference_fpr"])

    def test_audit_rejects_duplicate_population_labels_and_forged_probability(self):
        population = self.population()
        with self.assertRaises(DiscoveryViolation):
            stratified_sample(population + population[:1], seed=1, per_stratum=1)
        sample = stratified_sample(population, seed=1, per_stratum=1)
        labels = [{"candidate_id": r["candidate_id"], "proxy_pass": True, "reference_pass": False} for r in sample["selected"]]
        with self.assertRaises(DiscoveryViolation):
            proxy_audit(sample, labels + labels[:1])
        sample["selected"][0]["inclusion_probability"] = 0.99
        with self.assertRaisesRegex(DiscoveryViolation, "probability"):
            proxy_audit(sample, labels)

    def test_score_ties_have_deterministic_candidate_order(self):
        p = [{"candidate_id": c, "stratum": "x", "proxy_score": 0.5} for c in ["c", "a", "b"]]
        self.assertEqual(["a", "b"], ranked_selection(p, count=2))

    def test_execution_replay_tolerates_registered_numerics_not_changed_identity_or_limits(self):
        tolerances = {"displacement_m": {"absolute": 1e-6, "relative": 0.0}}
        identity = {"registration_sha256": digest("registration"), "evaluator_sha256": digest("solver"),
                    "context_sha256": digest("context"), "tolerances_sha256": digest(tolerances)}
        a = {"identity": identity, "values": {"displacement_m": 0.01}, "wall_s": 1.0}
        b = deepcopy(a)
        b["wall_s"] = 2.0
        b["values"]["displacement_m"] += 0.5e-6
        self.assertTrue(compare_execution(a, b, tolerances)["passed"])
        b["values"]["displacement_m"] += 1e-3
        self.assertFalse(compare_execution(a, b, tolerances)["passed"])
        changed = deepcopy(tolerances)
        changed["displacement_m"]["absolute"] = 1
        with self.assertRaisesRegex(DiscoveryViolation, "tolerances changed"):
            compare_execution(a, b, changed)
        b["identity"]["evaluator_sha256"] = digest("other")
        with self.assertRaisesRegex(DiscoveryViolation, "identity mismatch"):
            compare_execution(a, b, tolerances)


class LegacyAndRunnerTests(unittest.TestCase):
    def test_legacy_labels_never_automatically_admit_physics(self):
        for status in ("accepted", "repaired", "rejected"):
            self.assertEqual("not_evaluated", legacy_annotation("095", {"status": status})["physics"])
        self.assertEqual("not_evaluated", legacy_annotation("097", {"status": "passed"})["physics"])
        self.assertEqual("numerically_unresolved", legacy_annotation("097", {"status": "invalid", "reason": "solver_divergence"})["physics"])
        with self.assertRaises(DiscoveryViolation):
            legacy_annotation("unknown", {"status": "passed"})

    def test_fixture_runner_replays_mixed_ledger_and_protects_existing_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = run_fixture(registration(), root / "a")
            second = run_fixture(registration(), root / "b")
            self.assertEqual(first, second)
            self.assertEqual((root / "a/ledger.jsonl").read_bytes(), (root / "b/ledger.jsonl").read_bytes())
            self.assertEqual(0, first["counts"]["scientific_survivors"])
            self.assertEqual("exact", first["decision_replay"])
            with self.assertRaisesRegex(DiscoveryViolation, "new or empty"):
                run_fixture(registration(), root / "a")


if __name__ == "__main__":
    unittest.main()
