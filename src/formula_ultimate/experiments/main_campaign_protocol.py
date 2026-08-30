"""Strict rules for the first bounded whole-vehicle main campaign."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import re
from typing import Any, Mapping


class MainCampaignProtocolError(ValueError):
    """Raised when a campaign declaration violates a frozen rule."""


@dataclass(frozen=True, slots=True)
class MainCampaignProtocolSummary:
    protocol_id: str
    campaign_id: str
    treatments: tuple[str, ...]
    paired_seeds: tuple[int, ...]
    attempts_per_treatment_seed: int
    attempts_per_treatment: int
    total_attempts: int
    grid_capacity: int
    grid_unique_opportunities: int
    maximum_promotions: int
    inferential_unit: str
    refined_evaluator_identity: str
    protocol_fingerprint_sha256: str


TREATMENTS = ("GRID", "RANDOM", "EVOLUTION")
VARIABLE_BOUNDS = {
    "core_length_scale": (0.9, 1.1),
    "core_width_scale": (0.9, 1.1),
    "contact_radius_scale": (0.8, 1.2),
    "source_size_scale": (0.8, 1.2),
    "propulsor_size_scale": (0.8, 1.2),
}
STAGES = (
    "declaration_and_identity",
    "candidate_proposal",
    "grammar_geometry_and_training_level0",
    "seed_level_training_selection",
    "frozen_holdout_level0",
    "work053_refined_stress_deformation",
    "finalist_step_freecad_witness",
    "eligibility_and_analysis",
)
REQUIRED_FAILURES = {
    "invalid_declaration", "invalid_geometry", "numerical_failure",
    "structural_failure", "energy_failure", "exploit_rejection",
    "holdout_failure", "refined_disagreement", "DNF",
}
PROHIBITED_CLAIMS = {
    "physical_validation", "real_world_safety", "manufacturability",
    "race_superiority", "algorithm_superiority_from_this_campaign_alone",
    "novelty", "engineering_discovery", "arbitrary_topology_transfer",
    "certified_material_allowable",
}


def _canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise MainCampaignProtocolError(message)


def _require_sha256(value: Any, name: str) -> None:
    _require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None, f"{name} must be a lowercase SHA-256")


def _require_commit(value: Any, name: str) -> None:
    _require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None, f"{name} must be a full lowercase Git commit ID")


def validate_main_campaign_protocol(protocol: Mapping[str, Any]) -> MainCampaignProtocolSummary:
    protocol_id = protocol.get("protocol_id")
    _require(protocol_id in {"bounded_whole_vehicle_main_campaign_v1", "bounded_whole_vehicle_main_campaign_v2"}, "protocol identity mismatch")
    expected_campaign_id = "FU-BMC-001" if protocol_id.endswith("_v1") else "FU-BMC-002"
    _require(protocol.get("campaign_id") == expected_campaign_id, "campaign identity mismatch")
    if protocol_id.endswith("_v1"):
        _require("supersedes" not in protocol, "v1 cannot carry successor remediation evidence")
    else:
        remediation = protocol.get("supersedes", {})
        _require(remediation.get("protocol_id") == "bounded_whole_vehicle_main_campaign_v1" and remediation.get("campaign_id") == "FU-BMC-001", "v2 predecessor identity mismatch")
        _require(remediation.get("stopped_work") == "057", "v2 stopped-work provenance mismatch")
        _require(remediation.get("reason") == "canonicalize semantically equal tuple/list promotion selections after JSON append and replay", "v2 remediation scope mismatch")
        for name in ("v1_budget_ledger_sha256", "v1_result_ledger_sha256", "v1_stage_ledger_sha256", "v1_failure_record_sha256"):
            _require_sha256(remediation.get(name), name)
        _require(remediation.get("scientific_rules_changed") is False and remediation.get("v1_observations_reused") is False, "v2 scientific or observation boundary mismatch")
    _require(protocol.get("status") == "preregistered_not_run", "campaign status must remain preregistered_not_run")
    _require_commit(protocol.get("frozen_source_commit"), "frozen_source_commit")
    claim = protocol.get("claim_level")
    _require(isinstance(claim, str) and "no physical validation" in claim and "bounded" in claim, "claim boundary is not explicit")

    upstream = protocol.get("upstream_identity")
    _require(isinstance(upstream, Mapping) and len(upstream) == 13, "upstream identity set mismatch")
    for name, value in upstream.items():
        if name.endswith("_identity"):
            _require(value == "project_frame6dof_plus_calculix_b31_section_force_v2", "refined evaluator identity mismatch")
        else:
            _require_sha256(value, name)

    hypotheses = protocol.get("hypotheses", {})
    primary = hypotheses.get("primary", {})
    _require(primary.get("id") == "H1_EVOLUTION_SUPPORTED_FINISHER_RATE", "primary hypothesis identity mismatch")
    _require("EVOLUTION" in primary.get("preferred", "") and "RANDOM" in primary.get("preferred", ""), "primary comparison is incomplete")
    _require("paired-seed" in primary.get("null", ""), "primary null must use paired seeds")
    _require("non-positive" in primary.get("falsification", ""), "primary falsification rule is missing")
    secondary = hypotheses.get("secondary")
    _require(isinstance(secondary, list) and {item.get("id") for item in secondary} == {"H2_EVOLUTION_BEST_TIME", "H3_GRID_CALIBRATION"}, "secondary hypotheses mismatch")

    design = protocol.get("design", {})
    _require(tuple(design.get("treatments", ())) == TREATMENTS, "treatment order or identity mismatch")
    seeds = tuple(design.get("paired_seeds", ()))
    _require(len(seeds) == 12 and all(isinstance(seed, int) and seed > 0 for seed in seeds), "exactly 12 positive paired seeds are required")
    _require(len(set(seeds)) == len(seeds), "paired seeds must be unique")
    excluded = design.get("excluded_seeds", {})
    excluded_values = tuple(excluded.get("pilot", ())) + tuple(excluded.get("burn_in", ()))
    _require(set(excluded.get("pilot", ())) == {101, 202, 303}, "pilot seed exclusions mismatch")
    _require(set(excluded.get("burn_in", ())) == {55999}, "burn-in seed exclusion mismatch")
    _require(set(seeds).isdisjoint(excluded_values), "paired seeds overlap pilot or burn-in seeds")

    budget = design.get("attempted_evaluations_per_treatment_seed")
    _require(budget == 80, "attempt budget per treatment/seed must be 80")
    attempts_per_treatment = budget * len(seeds)
    total_attempts = attempts_per_treatment * len(TREATMENTS)
    _require(design.get("attempts_per_treatment") == attempts_per_treatment, "attempts_per_treatment arithmetic mismatch")
    _require(design.get("total_attempted_evaluations") == total_attempts, "total attempt arithmetic mismatch")
    for rule in ("failure_consumes_attempt", "same_candidate_bounds", "same_training_evaluator", "same_frozen_partitions"):
        _require(design.get(rule) is True, f"fairness rule {rule} must be true")

    variables = design.get("candidate_variables", {})
    _require(set(variables) == set(VARIABLE_BOUNDS), "candidate variable identity mismatch")
    for name, expected in VARIABLE_BOUNDS.items():
        bounds = variables[name]
        actual = (bounds.get("minimum"), bounds.get("maximum"))
        _require(actual == expected and all(math.isfinite(float(value)) for value in actual), f"candidate bounds mismatch for {name}")

    grid = design.get("grid", {})
    levels = grid.get("levels_per_variable")
    _require(levels == 4, "GRID levels must remain four")
    capacity = levels ** len(VARIABLE_BOUNDS)
    _require(grid.get("combination_capacity") == capacity, "GRID capacity arithmetic mismatch")
    _require(grid.get("planned_unique_opportunities") == attempts_per_treatment, "GRID opportunity count mismatch")
    _require(grid.get("wrap_or_repeat_allowed") is False, "GRID wrap or repeat must be prohibited")
    _require(attempts_per_treatment <= capacity, "GRID opportunity budget exceeds non-repeating capacity")
    grid_codes = {
        tuple((index // (levels ** position)) % levels for position in range(len(VARIABLE_BOUNDS)))
        for index in range(attempts_per_treatment)
    }
    _require(len(grid_codes) == attempts_per_treatment, "GRID opportunities are not unique")
    _require(design.get("random", {}).get("distribution") == "independent_uniform_within_declared_bounds", "RANDOM distribution mismatch")
    evolution = design.get("evolution", {})
    _require(evolution.get("initial_random_attempts_per_seed") == 20, "EVOLUTION initial random budget mismatch")
    _require(evolution.get("mutation_sigma_fraction_of_range") == 0.12, "EVOLUTION mutation scale mismatch")
    _require(evolution.get("parent_rule") == "best_training_feasible_else_best_observed", "EVOLUTION parent rule mismatch")
    _require(evolution.get("bound_handling") == "declared_bound_clamp_and_record", "EVOLUTION bound handling mismatch")

    _require(tuple(protocol.get("stage_order", ())) == STAGES, "campaign stage order mismatch")
    promotion = protocol.get("promotion", {})
    promoted_per_seed = promotion.get("training_feasible_candidates_per_treatment_seed")
    _require(promoted_per_seed == 2, "promotion count per treatment/seed must be two")
    maximum_promotions = promoted_per_seed * len(seeds) * len(TREATMENTS)
    _require(promotion.get("maximum_promotions") == maximum_promotions, "maximum promotion arithmetic mismatch")
    _require(promotion.get("shortfall_policy") == "record_zero_or_one_without_replacement_or_cross_seed_borrowing", "promotion shortfall policy mismatch")
    _require(promotion.get("ranking") == ["minimum_training_finish_time", "candidate_id_ascending"], "training promotion ranking mismatch")
    _require(promotion.get("holdout_is_never_used_for_training_or_parent_selection") is True, "holdout leakage is not prohibited")
    refined = promotion.get("refined_evaluator", {})
    evaluator_identity = upstream.get("work053_evaluator_identity")
    _require(refined.get("required_identity") == evaluator_identity, "promotion evaluator identity mismatch")
    _require(refined.get("required_status") == "passed_on_both_frozen_holdouts", "refined pass rule mismatch")
    _require(refined.get("thresholds_mutable_during_campaign") is False, "refined thresholds must be immutable")
    witness = promotion.get("final_witness", {})
    _require(witness == {"route": "3D_to_STEP_to_FreeCAD", "required_for_winner": True, "hidden_geometry_repair_allowed": False}, "final witness rules mismatch")

    outcomes = protocol.get("outcomes", {})
    _require(outcomes.get("inferential_unit") == "paired_seed", "inferential unit must be paired_seed")
    _require(outcomes.get("attempts_are_independent_replicates") is False, "attempt-level pseudo-replication must be prohibited")
    _require(outcomes.get("primary") == ["refined_supported_finisher_present_per_treatment_seed", "best_frozen_holdout_time_s_per_treatment_seed"], "primary outcomes mismatch")
    missing = outcomes.get("no_supported_finisher", {})
    _require(missing.get("presence") is False and missing.get("best_time_s") is None, "no-finisher outcome encoding mismatch")
    _require(missing.get("drop_from_rate_analysis") is False and missing.get("drop_from_time_availability_report") is False, "no-finisher outcomes cannot be silently dropped")

    analysis = protocol.get("analysis", {})
    _require(analysis.get("primary_comparison") == "EVOLUTION_minus_RANDOM", "primary analysis comparison mismatch")
    _require(analysis.get("analysis_seed") == 551337, "analysis seed mismatch")
    _require("paired" in analysis.get("supported_finisher_rate", "") and "95_percent" in analysis.get("supported_finisher_rate", ""), "supported-finisher analysis is incomplete")
    _require("paired" in analysis.get("common_success_best_time", "") and "95_percent" in analysis.get("common_success_best_time", ""), "best-time analysis is incomplete")
    _require(analysis.get("multiple_outcomes") == "report_all_preregistered_outcomes_without_selective_suppression", "selective outcome reporting is not prohibited")
    _require(analysis.get("winner_rule") == ["all_eligibility_gates_passed", "minimum_frozen_holdout_time_s", "candidate_id_ascending"], "winner rule mismatch")
    _require("independent_replication_under_a_new_protocol" in analysis.get("algorithm_superiority_requires_both", ()), "algorithm-superiority replication rule is missing")

    failure = protocol.get("failure_policy", {})
    _require(set(failure.get("counted_outcomes", ())) == REQUIRED_FAILURES, "counted failure outcomes mismatch")
    for rule in ("silent_repair_allowed", "neutral_numeric_substitution_allowed", "cross_seed_budget_borrowing_allowed", "failed_attempt_retry_allowed"):
        _require(failure.get(rule) is False, f"failure exploit {rule} must be false")
    stop_go = protocol.get("stop_go", {})
    _require(set(stop_go.get("campaign_result_statuses", ())) == {"completed_with_supported_finishers", "completed_without_supported_finisher", "stopped_protocol_violation", "stopped_infrastructure_failure"}, "result status set mismatch")
    _require("GRID_opportunities_repeat" in stop_go.get("stop_before_admitted_run_if", ()), "GRID repeat stop rule is missing")
    _require("holdout_information_reaches_training" in stop_go.get("stop_before_admitted_run_if", ()), "holdout leakage stop rule is missing")
    immutability = protocol.get("immutability", {})
    _require(all(immutability.get(name) is True for name in ("changes_after_burn_in_require_new_protocol_id", "changes_after_admitted_start_require_new_campaign_id", "append_only_result_and_budget_ledgers", "record_rng_checkpoint_and_ancestry")), "immutability rules must all be true")
    _require(set(protocol.get("prohibited_claims", ())) == PROHIBITED_CLAIMS, "prohibited claim set mismatch")

    draft = {
        "protocol_id": protocol["protocol_id"], "campaign_id": protocol["campaign_id"],
        "treatments": TREATMENTS, "paired_seeds": seeds,
        "attempts_per_treatment_seed": budget, "attempts_per_treatment": attempts_per_treatment,
        "total_attempts": total_attempts, "grid_capacity": capacity,
        "grid_unique_opportunities": len(grid_codes), "maximum_promotions": maximum_promotions,
        "inferential_unit": outcomes["inferential_unit"], "refined_evaluator_identity": evaluator_identity,
    }
    return MainCampaignProtocolSummary(**draft, protocol_fingerprint_sha256=_canonical_sha256(protocol))


def summary_as_dict(summary: MainCampaignProtocolSummary) -> dict[str, Any]:
    return asdict(summary)
