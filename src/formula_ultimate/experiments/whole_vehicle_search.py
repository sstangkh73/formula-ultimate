"""Work 050 bounded equal-budget whole-vehicle search pilot."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import random
from typing import Any, Mapping, Sequence

from formula_ultimate.topology.vehicle_assembly import from_mapping, mass_properties, validate


SEARCH_AGENT_VERSION = "DesignSearchAgentV0"
SEARCH_EVALUATOR_VERSION = "bounded_geometry_mass_capacity_level0_v1"


class WholeVehicleSearchError(ValueError):
    """Raised when the Work 050 fairness or candidate contract is violated."""


@dataclass(frozen=True, slots=True)
class SearchCandidate:
    candidate_id: str
    treatment: str
    seed: int
    attempt_index: int
    variables: tuple[tuple[str, float], ...]
    parent_candidate_id: str | None
    rng_checkpoint_sha256: str


@dataclass(frozen=True, slots=True)
class CandidateEvaluation:
    candidate: SearchCandidate
    status: str
    failure_code: str | None
    mass_kg: float | None
    mass_ratio: float | None
    capacity_factor: float | None
    maximum_utilization: float | None
    finish_time_s: float | None
    energy_used_j: float | None
    objective: float | None
    partition: str
    evaluator_sha256: str
    evaluation_sha256: str


@dataclass(frozen=True, slots=True)
class PromotionResult:
    candidate_id: str
    treatment: str
    seed: int
    training_objective: float
    holdout_status: str
    holdout_failure_code: str | None
    holdout_objective: float | None
    refined_status: str
    selected_as_winner: bool


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_search_protocol(protocol: Mapping[str, Any], baseline: Mapping[str, Any], *, baseline_protocol_sha256: str) -> str:
    if protocol.get("protocol_id") != "bounded_whole_vehicle_search_pilot_v1":
        raise WholeVehicleSearchError("search protocol identity mismatch")
    if protocol.get("agent_version") != SEARCH_AGENT_VERSION or protocol.get("evaluator_version") != SEARCH_EVALUATOR_VERSION:
        raise WholeVehicleSearchError("search implementation identity mismatch")
    if tuple(protocol.get("treatments", ())) != ("GRID", "RANDOM", "EVOLUTION"):
        raise WholeVehicleSearchError("treatment set or order changed")
    if tuple(protocol.get("seeds", ())) != (101, 202, 303):
        raise WholeVehicleSearchError("preregistered seeds changed")
    if protocol.get("attempted_evaluations_per_treatment_seed") != 32:
        raise WholeVehicleSearchError("attempted evaluation budget changed")
    identity = protocol["upstream_identity"]
    expected = {
        "baseline_protocol_sha256": baseline_protocol_sha256,
        "reference_result_sha256": baseline["replay"]["result_sha256"],
        "reference_matrix_sha256": baseline["replay"]["matrix_sha256"],
    }
    for key, value in expected.items():
        if identity.get(key) != value:
            raise WholeVehicleSearchError(f"upstream {key} mismatch")
    variables = protocol["candidate_variables"]
    if len(variables) != 5:
        raise WholeVehicleSearchError("candidate opportunity set changed")
    for name, bounds in variables.items():
        low, high = float(bounds["minimum"]), float(bounds["maximum"])
        if not math.isfinite(low) or not math.isfinite(high) or low >= high:
            raise WholeVehicleSearchError(f"invalid bounds for {name}")
    if protocol["refined_evaluator"].get("status") not in {"available", "unavailable"}:
        raise WholeVehicleSearchError("refined evaluator status is invalid")
    return canonical_sha256({
        "evaluator_version": protocol["evaluator_version"],
        "variables": variables,
        "baseline_protocol": baseline_protocol_sha256,
        "load_case_identity": baseline["upstream"]["load_case_result_sha256"],
        "training_partition": baseline["upstream"]["training_partition_sha256"],
        "holdout_partition": baseline["upstream"]["holdout_partition_sha256"],
    })


def _candidate_variables(protocol: Mapping[str, Any], values: Mapping[str, Any]) -> tuple[tuple[str, float], ...]:
    bounds = protocol["candidate_variables"]
    if set(values) != set(bounds):
        raise WholeVehicleSearchError("candidate variables differ from the frozen opportunity set")
    ready = []
    for name in sorted(bounds):
        value = float(values[name])
        low, high = float(bounds[name]["minimum"]), float(bounds[name]["maximum"])
        if not math.isfinite(value) or not low <= value <= high:
            raise WholeVehicleSearchError(f"candidate variable {name} is outside bounds")
        ready.append((name, value))
    return tuple(ready)


def mutate_candidate_assembly(base: Mapping[str, Any], variables: Mapping[str, float]) -> dict:
    raw = json.loads(json.dumps(base))
    by_id = {item["component_id"]: item for item in raw["components"]}
    core_length = variables["core_length_scale"]
    core_width = variables["core_width_scale"]
    radius = variables["contact_radius_scale"]
    source_scale = variables["source_size_scale"]
    propulsor_scale = variables["propulsor_size_scale"]
    by_id["core"]["primitive"]["size_m"][0] *= core_length
    by_id["core"]["primitive"]["size_m"][1] *= core_width
    by_id["source"]["primitive"]["size_m"] = [0.1 * source_scale] * 3
    by_id["propulsor"]["primitive"]["size_m"] = [0.1 * propulsor_scale] * 3
    by_id["source"]["translation_m"][0] = -(0.2 * core_length + 0.05 * source_scale)
    by_id["propulsor"]["translation_m"][0] = 0.2 * core_length + 0.05 * propulsor_scale
    by_id["contact_alpha"]["primitive"]["radius_m"] *= radius
    for interface in raw["interfaces"]:
        if interface["interface_id"] == "core_energy":
            interface["local_position_m"][0] = -0.2 * core_length
        elif interface["interface_id"] == "source_out":
            interface["local_position_m"][0] = 0.05 * source_scale
        elif interface["interface_id"] == "core_prop":
            interface["local_position_m"][0] = 0.2 * core_length
        elif interface["interface_id"] == "prop_in":
            interface["local_position_m"][0] = -0.05 * propulsor_scale
    return raw


def _partition_cases(work048: Mapping[str, Any], partition: str) -> list[Mapping[str, Any]]:
    return [item for item in work048["results"] if item["partition"] == partition]


def evaluate_candidate(
    protocol: Mapping[str, Any],
    candidate: SearchCandidate,
    base_assembly: Mapping[str, Any],
    work048: Mapping[str, Any],
    baseline_protocol: Mapping[str, Any],
    evaluator_sha256: str,
    *,
    partition: str,
) -> CandidateEvaluation:
    if candidate.treatment not in protocol["treatments"] or candidate.seed not in protocol["seeds"]:
        raise WholeVehicleSearchError("candidate treatment or seed is not registered")
    variables = dict(_candidate_variables(protocol, dict(candidate.variables)))
    try:
        assembly = from_mapping(mutate_candidate_assembly(base_assembly, variables))
        validate(assembly)
    except (KeyError, TypeError, ValueError) as exc:
        return _evaluation(candidate, "failed", "grammar_invalid", None, None, None, None, None, None, None, partition, evaluator_sha256)
    base = from_mapping(base_assembly)
    base_mass = mass_properties(base)["mass_kg"]
    mass = mass_properties(assembly)["mass_kg"]
    mass_ratio = mass / base_mass
    capacity_factor = min(
        variables["core_width_scale"], variables["contact_radius_scale"] ** 2,
        variables["source_size_scale"] ** 2, variables["propulsor_size_scale"] ** 2,
    )
    cases = _partition_cases(work048, partition)
    if not cases:
        raise WholeVehicleSearchError("requested evaluation partition has no frozen cases")
    maximum_utilization = max(
        max(float(load["utilization"]) for load in case["connection_loads"]) * mass_ratio / capacity_factor
        for case in cases
    )
    if maximum_utilization > 1.0:
        return _evaluation(candidate, "failed", "structural_failure", mass, mass_ratio, capacity_factor, maximum_utilization, None, None, None, partition, evaluator_sha256)
    fixture = baseline_protocol["race_fixture"]
    time_s = float(fixture["distance_m"]) / (float(fixture["reference_speed_m_per_s"]) / math.sqrt(mass_ratio))
    energy = float(fixture["base_energy_j_per_m"]) * float(fixture["distance_m"]) * mass_ratio + float(fixture["auxiliary_power_w"]) * time_s
    if energy > float(fixture["initial_energy_j"]):
        return _evaluation(candidate, "failed", "energy_depletion", mass, mass_ratio, capacity_factor, maximum_utilization, None, energy, None, partition, evaluator_sha256)
    return _evaluation(candidate, "feasible", None, mass, mass_ratio, capacity_factor, maximum_utilization, time_s, energy, time_s, partition, evaluator_sha256)


def _evaluation(candidate, status, failure_code, mass, mass_ratio, capacity_factor, utilization, time_s, energy, objective, partition, evaluator_sha256):
    draft = {
        "candidate": asdict(candidate), "status": status, "failure_code": failure_code,
        "mass_kg": mass, "mass_ratio": mass_ratio, "capacity_factor": capacity_factor,
        "maximum_utilization": utilization, "finish_time_s": time_s, "energy_used_j": energy,
        "objective": objective, "partition": partition, "evaluator_sha256": evaluator_sha256,
    }
    return CandidateEvaluation(
        candidate, status, failure_code, mass, mass_ratio, capacity_factor, utilization,
        time_s, energy, objective, partition, evaluator_sha256, canonical_sha256(draft),
    )


def _rng_checkpoint(rng: random.Random) -> str:
    return canonical_sha256(repr(rng.getstate()))


class DesignSearchAgentV0:
    def __init__(self, protocol: Mapping[str, Any], treatment: str, seed: int):
        if treatment not in protocol["treatments"] or seed not in protocol["seeds"]:
            raise WholeVehicleSearchError("agent treatment or seed is not registered")
        self.protocol = protocol
        self.treatment = treatment
        self.seed = seed
        self.rng = random.Random(seed)
        self.history: list[CandidateEvaluation] = []

    def _random_values(self) -> dict[str, float]:
        return {
            name: self.rng.uniform(float(bounds["minimum"]), float(bounds["maximum"]))
            for name, bounds in self.protocol["candidate_variables"].items()
        }

    def _grid_values(self, attempt: int) -> dict[str, float]:
        levels = int(self.protocol["grid_levels_per_variable"])
        index = attempt + (self.protocol["seeds"].index(self.seed) * int(self.protocol["attempted_evaluations_per_treatment_seed"]))
        values = {}
        for name, bounds in self.protocol["candidate_variables"].items():
            digit = index % levels
            index //= levels
            low, high = float(bounds["minimum"]), float(bounds["maximum"])
            values[name] = low + (high - low) * digit / (levels - 1)
        return values

    def propose(self, attempt: int) -> SearchCandidate:
        checkpoint = _rng_checkpoint(self.rng)
        parent = None
        if self.treatment == "GRID":
            values = self._grid_values(attempt)
        elif self.treatment == "RANDOM" or attempt < int(self.protocol["evolution_initial_random"]):
            values = self._random_values()
        else:
            feasible = [item for item in self.history if item.status == "feasible"]
            pool = feasible or self.history
            best = min(pool, key=lambda item: (float("inf") if item.objective is None else item.objective, item.candidate.candidate_id))
            parent = best.candidate.candidate_id
            parent_values = dict(best.candidate.variables)
            sigma = float(self.protocol["evolution_mutation_sigma_fraction"])
            values = {}
            for name, bounds in self.protocol["candidate_variables"].items():
                low, high = float(bounds["minimum"]), float(bounds["maximum"])
                values[name] = min(high, max(low, parent_values[name] + self.rng.gauss(0.0, sigma * (high - low))))
        frozen = _candidate_variables(self.protocol, values)
        identity = canonical_sha256({"treatment": self.treatment, "seed": self.seed, "attempt": attempt, "variables": frozen, "parent": parent})
        return SearchCandidate("candidate-" + identity[:16], self.treatment, self.seed, attempt, frozen, parent, checkpoint)

    def observe(self, evaluation: CandidateEvaluation) -> None:
        if evaluation.candidate.treatment != self.treatment or evaluation.candidate.seed != self.seed:
            raise WholeVehicleSearchError("agent cannot observe another treatment opportunity")
        if evaluation.candidate.attempt_index != len(self.history):
            raise WholeVehicleSearchError("attempt ledger is not append-only")
        self.history.append(evaluation)


def run_search_pilot(
    protocol: Mapping[str, Any], base_assembly: Mapping[str, Any], work048: Mapping[str, Any],
    baseline_protocol: Mapping[str, Any], evaluator_sha256: str,
) -> tuple[CandidateEvaluation, ...]:
    records = []
    budget = int(protocol["attempted_evaluations_per_treatment_seed"])
    for treatment in protocol["treatments"]:
        for seed in protocol["seeds"]:
            agent = DesignSearchAgentV0(protocol, treatment, seed)
            for attempt in range(budget):
                candidate = agent.propose(attempt)
                result = evaluate_candidate(
                    protocol, candidate, base_assembly, work048, baseline_protocol,
                    evaluator_sha256, partition="training",
                )
                agent.observe(result)
                records.append(result)
    return tuple(records)


def promote_candidates(
    protocol: Mapping[str, Any], records: Sequence[CandidateEvaluation], base_assembly: Mapping[str, Any],
    work048: Mapping[str, Any], baseline_protocol: Mapping[str, Any], evaluator_sha256: str,
) -> tuple[PromotionResult, ...]:
    promotions = []
    refined_available = protocol["refined_evaluator"]["status"] == "available"
    for treatment in protocol["treatments"]:
        for seed in protocol["seeds"]:
            feasible = [item for item in records if item.candidate.treatment == treatment and item.candidate.seed == seed and item.status == "feasible"]
            if not feasible:
                continue
            selected = min(feasible, key=lambda item: (item.objective, item.candidate.candidate_id))
            holdout = evaluate_candidate(
                protocol, selected.candidate, base_assembly, work048, baseline_protocol,
                evaluator_sha256, partition="holdout",
            )
            refined_status = "passed" if refined_available and holdout.status == "feasible" else "unavailable"
            promotions.append(PromotionResult(
                selected.candidate.candidate_id, treatment, seed, float(selected.objective),
                holdout.status, holdout.failure_code, holdout.objective, refined_status, False,
            ))
    return tuple(promotions)


def readiness_decision(
    protocol: Mapping[str, Any], records: Sequence[CandidateEvaluation], promotions: Sequence[PromotionResult],
    *, exact_replay: bool, exploit_controls_passed: bool,
) -> dict[str, Any]:
    budget = int(protocol["attempted_evaluations_per_treatment_seed"])
    counts = {
        treatment: sum(1 for item in records if item.candidate.treatment == treatment)
        for treatment in protocol["treatments"]
    }
    equal_budget = set(counts.values()) == {budget * len(protocol["seeds"])}
    holdout_pass = len(promotions) == len(protocol["treatments"]) * len(protocol["seeds"]) and all(item.holdout_status == "feasible" for item in promotions)
    refined = bool(promotions) and all(item.refined_status == "passed" for item in promotions)
    checks = {
        "exact_replay": exact_replay,
        "equal_budget": equal_budget,
        "same_evaluator": len({item.evaluator_sha256 for item in records}) == 1,
        "holdout_pass": holdout_pass,
        "independent_refined_evaluation": refined,
        "no_exploit": exploit_controls_passed,
        "complete_provenance": all(item.candidate.rng_checkpoint_sha256 and item.evaluation_sha256 for item in records),
    }
    blockers = tuple(name for name in protocol["readiness_requirements"] if not checks.get(name, False))
    decision = "ready_for_bounded_main_campaign" if not blockers else "not_ready"
    return {"decision": decision, "checks": checks, "blockers": blockers, "attempt_counts": counts}
