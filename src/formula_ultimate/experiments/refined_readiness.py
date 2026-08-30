"""Deterministic adjudication of Work 050 readiness using Work 053 evidence."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping


class ReadinessAdjudicationError(ValueError):
    """Raised when retained experiment identities or records are inconsistent."""


def _fingerprint(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def adjudicate_refined_readiness(
    work050: Mapping[str, Any],
    work053: Mapping[str, Any],
    *,
    expected_treatments: tuple[str, ...] = ("GRID", "RANDOM", "EVOLUTION"),
    original_promotions_per_treatment: int = 3,
    minimum_supported_per_treatment: int = 2,
    expected_attempts_per_treatment: int = 96,
) -> dict[str, Any]:
    if work050.get("status") != "passed" or work053.get("status") != "passed":
        raise ReadinessAdjudicationError("upstream experiment status is not passed")
    readiness = work050.get("readiness")
    if not isinstance(readiness, Mapping):
        raise ReadinessAdjudicationError("Work 050 readiness record is missing")
    checks = dict(readiness.get("checks", {}))
    required_checks = {
        "complete_provenance", "equal_budget", "exact_replay", "holdout_pass",
        "independent_refined_evaluation", "no_exploit", "same_evaluator",
    }
    if set(checks) != required_checks:
        raise ReadinessAdjudicationError("Work 050 readiness check identity mismatch")
    if checks["independent_refined_evaluation"] is not False:
        raise ReadinessAdjudicationError("Work 050 refined-evaluation blocker was not retained")
    if any(not bool(checks[name]) for name in required_checks - {"independent_refined_evaluation"}):
        raise ReadinessAdjudicationError("Work 050 contains an additional readiness blocker")
    if readiness.get("blockers") != ["independent_refined_evaluation"]:
        raise ReadinessAdjudicationError("Work 050 blocker set changed")
    if work053.get("decision") != "independent_refined_evaluator_available":
        raise ReadinessAdjudicationError("Work 053 evaluator is unavailable")

    promotions = list(work050.get("promotions", ()))
    refined = list(work053.get("promotion_results", ()))
    if len(promotions) != len(refined):
        raise ReadinessAdjudicationError("promotion count mismatch")
    refined_by_id: dict[str, Mapping[str, Any]] = {}
    for item in refined:
        candidate_id = item.get("candidate_id")
        if not isinstance(candidate_id, str) or candidate_id in refined_by_id:
            raise ReadinessAdjudicationError("refined candidate identity is missing or duplicated")
        refined_by_id[candidate_id] = item

    attempt_counts = readiness.get("attempt_counts", {})
    if set(attempt_counts) != set(expected_treatments) or any(
        attempt_counts[name] != expected_attempts_per_treatment for name in expected_treatments
    ):
        raise ReadinessAdjudicationError("original treatment budget changed")

    joined: list[dict[str, Any]] = []
    seen: set[str] = set()
    for promotion in promotions:
        candidate_id = promotion.get("candidate_id")
        treatment = promotion.get("treatment")
        objective = promotion.get("holdout_objective")
        if candidate_id in seen or candidate_id not in refined_by_id:
            raise ReadinessAdjudicationError("promotion candidate identity mismatch")
        if treatment not in expected_treatments:
            raise ReadinessAdjudicationError("promotion treatment identity mismatch")
        if not isinstance(objective, (int, float)) or not math.isfinite(float(objective)):
            raise ReadinessAdjudicationError("promotion objective is invalid")
        if promotion.get("holdout_status") != "feasible":
            raise ReadinessAdjudicationError("Work 050 promoted an infeasible holdout")
        seen.add(candidate_id)
        evidence = refined_by_id[candidate_id]
        cases = list(evidence.get("holdout_cases", ()))
        if len(cases) != 2:
            raise ReadinessAdjudicationError("refined holdout evidence is incomplete")
        supported = evidence.get("status") == "passed" and all(case.get("status") == "passed" for case in cases)
        if (evidence.get("status") == "passed") != supported:
            raise ReadinessAdjudicationError("refined aggregate status contradicts holdouts")
        joined.append({
            "candidate_id": candidate_id,
            "treatment": treatment,
            "original_holdout_objective_s": float(objective),
            "refined_status": "supported" if supported else "rejected",
            "refined_holdout_statuses": {case["case_id"]: case["status"] for case in cases},
        })

    treatment_results: dict[str, dict[str, Any]] = {}
    supported_all: list[dict[str, Any]] = []
    for treatment in expected_treatments:
        original = [item for item in joined if item["treatment"] == treatment]
        if len(original) != original_promotions_per_treatment:
            raise ReadinessAdjudicationError("original promotion allocation changed")
        supported = sorted(
            (item for item in original if item["refined_status"] == "supported"),
            key=lambda item: (item["original_holdout_objective_s"], item["candidate_id"]),
        )
        supported_all.extend(supported)
        treatment_results[treatment] = {
            "original_promotions": len(original),
            "supported_promotions": len(supported),
            "rejected_candidate_ids": sorted(item["candidate_id"] for item in original if item["refined_status"] == "rejected"),
            "winner_candidate_id": supported[0]["candidate_id"] if supported else None,
            "winner_holdout_objective_s": supported[0]["original_holdout_objective_s"] if supported else None,
        }

    ranked = sorted(supported_all, key=lambda item: (item["original_holdout_objective_s"], item["candidate_id"]))
    global_winner = ranked[0] if ranked else None
    final_checks = {name: bool(value) for name, value in checks.items()}
    final_checks["independent_refined_evaluation"] = True
    final_checks.update({
        "minimum_supported_per_treatment": all(
            item["supported_promotions"] >= minimum_supported_per_treatment for item in treatment_results.values()
        ),
        "supported_global_winner": global_winner is not None,
        "refined_join_complete": len(joined) == len(promotions) == len(refined),
    })
    blockers = sorted(name for name, passed in final_checks.items() if not passed)
    decision = "ready_for_bounded_whole_vehicle_campaign" if not blockers else "not_ready"
    draft = {
        "decision": decision,
        "checks": final_checks,
        "blockers": blockers,
        "joined_promotions": joined,
        "treatment_results": treatment_results,
        "global_winner": global_winner,
        "supported_candidates": len(supported_all),
        "rejected_candidates": len(joined) - len(supported_all),
    }
    return {**draft, "adjudication_sha256": _fingerprint(draft)}
