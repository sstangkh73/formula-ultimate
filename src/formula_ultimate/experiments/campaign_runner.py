"""Resume-safe campaign orchestration and tamper-evident append-only ledgers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from .whole_vehicle_search import (
    CandidateEvaluation,
    DesignSearchAgentV0,
    SearchCandidate,
    WholeVehicleSearchError,
    canonical_sha256,
)


ZERO_SHA256 = "0" * 64
LEDGER_SCHEMA = "chained_campaign_jsonl_v1"


class CampaignRunnerError(ValueError):
    """Raised when campaign execution, replay, or ledger evidence is invalid."""


@dataclass(frozen=True, slots=True)
class LedgerRow:
    schema: str
    protocol_id: str
    campaign_id: str
    evidence_class: str
    ledger_kind: str
    sequence: int
    previous_record_sha256: str
    payload: Mapping[str, Any]
    record_sha256: str


@dataclass(frozen=True, slots=True)
class CampaignExecutionAuthorization:
    authorization_id: str
    campaign_id: str
    evidence_class: str
    allowed_seeds: tuple[int, ...]
    admitted_main_execution: bool


@dataclass(frozen=True, slots=True)
class PromotionSelection:
    treatment: str
    seed: int
    candidate_ids: tuple[str, ...]
    requested: int
    selected: int
    shortfall: int
    selection_sha256: str


def _row_without_hash(
    protocol_id: str,
    campaign_id: str,
    evidence_class: str,
    ledger_kind: str,
    sequence: int,
    previous_record_sha256: str,
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema": LEDGER_SCHEMA,
        "protocol_id": protocol_id,
        "campaign_id": campaign_id,
        "evidence_class": evidence_class,
        "ledger_kind": ledger_kind,
        "sequence": sequence,
        "previous_record_sha256": previous_record_sha256,
        "payload": payload,
    }


class ChainedJsonlLedger:
    """A deterministic JSONL hash chain with fail-closed replay."""

    def __init__(self, path: Path, *, protocol_id: str, campaign_id: str, evidence_class: str, ledger_kind: str):
        self.path = Path(path)
        self.protocol_id = protocol_id
        self.campaign_id = campaign_id
        self.evidence_class = evidence_class
        self.ledger_kind = ledger_kind
        if not all(isinstance(value, str) and value for value in (protocol_id, campaign_id, evidence_class, ledger_kind)):
            raise CampaignRunnerError("ledger identities must be non-empty strings")

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
        self.read_rows()

    def read_rows(self) -> tuple[LedgerRow, ...]:
        if not self.path.exists():
            return ()
        rows: list[LedgerRow] = []
        expected_previous = ZERO_SHA256
        text = self.path.read_text(encoding="utf-8")
        for index, line in enumerate(text.splitlines()):
            if not line.strip():
                raise CampaignRunnerError("ledger contains a blank or truncated row")
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                raise CampaignRunnerError("ledger contains malformed JSON") from exc
            expected_keys = {
                "schema", "protocol_id", "campaign_id", "evidence_class", "ledger_kind",
                "sequence", "previous_record_sha256", "payload", "record_sha256",
            }
            if set(raw) != expected_keys:
                raise CampaignRunnerError("ledger row schema mismatch")
            if raw["schema"] != LEDGER_SCHEMA or raw["protocol_id"] != self.protocol_id or raw["campaign_id"] != self.campaign_id:
                raise CampaignRunnerError("ledger protocol or campaign identity mismatch")
            if raw["evidence_class"] != self.evidence_class or raw["ledger_kind"] != self.ledger_kind:
                raise CampaignRunnerError("ledger evidence class or kind mismatch")
            if raw["sequence"] != index:
                raise CampaignRunnerError("ledger sequence is not append-only")
            if raw["previous_record_sha256"] != expected_previous:
                raise CampaignRunnerError("ledger previous-record hash mismatch")
            without_hash = {key: raw[key] for key in raw if key != "record_sha256"}
            calculated = canonical_sha256(without_hash)
            if raw["record_sha256"] != calculated:
                raise CampaignRunnerError("ledger record hash mismatch")
            if not isinstance(raw["payload"], dict):
                raise CampaignRunnerError("ledger payload must be an object")
            rows.append(LedgerRow(**raw))
            expected_previous = calculated
        return tuple(rows)

    def append(self, payload: Mapping[str, Any]) -> LedgerRow:
        if not isinstance(payload, Mapping):
            raise CampaignRunnerError("ledger append payload must be a mapping")
        rows = self.read_rows()
        previous = rows[-1].record_sha256 if rows else ZERO_SHA256
        base = _row_without_hash(
            self.protocol_id, self.campaign_id, self.evidence_class, self.ledger_kind,
            len(rows), previous, dict(payload),
        )
        row = {**base, "record_sha256": canonical_sha256(base)}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(row, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        replayed = self.read_rows()
        if replayed[-1].record_sha256 != row["record_sha256"]:
            raise CampaignRunnerError("ledger append replay mismatch")
        return replayed[-1]

    def fingerprint(self) -> str:
        rows = self.read_rows()
        return rows[-1].record_sha256 if rows else ZERO_SHA256


def _candidate_from_mapping(raw: Mapping[str, Any]) -> SearchCandidate:
    variables = raw.get("variables")
    if not isinstance(variables, list):
        raise CampaignRunnerError("candidate variables are malformed")
    candidate = SearchCandidate(
        str(raw["candidate_id"]), str(raw["treatment"]), int(raw["seed"]), int(raw["attempt_index"]),
        tuple((str(item[0]), float(item[1])) for item in variables),
        None if raw.get("parent_candidate_id") is None else str(raw["parent_candidate_id"]),
        str(raw["rng_checkpoint_sha256"]),
    )
    expected_id = "candidate-" + canonical_sha256({
        "treatment": candidate.treatment,
        "seed": candidate.seed,
        "attempt": candidate.attempt_index,
        "variables": candidate.variables,
        "parent": candidate.parent_candidate_id,
    })[:16]
    if candidate.candidate_id != expected_id:
        raise CampaignRunnerError("candidate identity hash mismatch")
    if len(candidate.rng_checkpoint_sha256) != 64:
        raise CampaignRunnerError("candidate RNG checkpoint is malformed")
    return candidate


def _evaluation_from_mapping(raw: Mapping[str, Any]) -> CandidateEvaluation:
    candidate = _candidate_from_mapping(raw["candidate"])
    numeric_names = (
        "mass_kg", "mass_ratio", "capacity_factor", "maximum_utilization",
        "finish_time_s", "energy_used_j", "objective",
    )
    values = {name: None if raw.get(name) is None else float(raw[name]) for name in numeric_names}
    if any(value is not None and not math.isfinite(value) for value in values.values()):
        raise CampaignRunnerError("evaluation contains non-finite numeric evidence")
    evaluation = CandidateEvaluation(
        candidate, str(raw["status"]), None if raw.get("failure_code") is None else str(raw["failure_code"]),
        values["mass_kg"], values["mass_ratio"], values["capacity_factor"], values["maximum_utilization"],
        values["finish_time_s"], values["energy_used_j"], values["objective"], str(raw["partition"]),
        str(raw["evaluator_sha256"]), str(raw["evaluation_sha256"]),
    )
    draft = {
        "candidate": asdict(candidate), "status": evaluation.status, "failure_code": evaluation.failure_code,
        "mass_kg": evaluation.mass_kg, "mass_ratio": evaluation.mass_ratio,
        "capacity_factor": evaluation.capacity_factor, "maximum_utilization": evaluation.maximum_utilization,
        "finish_time_s": evaluation.finish_time_s, "energy_used_j": evaluation.energy_used_j,
        "objective": evaluation.objective, "partition": evaluation.partition,
        "evaluator_sha256": evaluation.evaluator_sha256,
    }
    if evaluation.evaluation_sha256 != canonical_sha256(draft):
        raise CampaignRunnerError("evaluation identity hash mismatch")
    return evaluation


class CampaignLedgerStore:
    """Cross-validates consumed opportunity and terminal result ledgers."""

    def __init__(self, budget: ChainedJsonlLedger, result: ChainedJsonlLedger):
        if (budget.protocol_id, budget.campaign_id, budget.evidence_class) != (result.protocol_id, result.campaign_id, result.evidence_class):
            raise CampaignRunnerError("budget and result ledger identities differ")
        if budget.ledger_kind != "budget" or result.ledger_kind != "result":
            raise CampaignRunnerError("campaign ledger kinds must be budget and result")
        self.budget = budget
        self.result = result

    def initialize(self) -> None:
        self.budget.initialize()
        self.result.initialize()
        self.validate()

    def validate(self) -> dict[str, Any]:
        reservations: dict[str, Mapping[str, Any]] = {}
        stream_attempts: dict[tuple[str, int], list[int]] = {}
        for row in self.budget.read_rows():
            payload = row.payload
            if payload.get("record_type") != "attempt_reserved" or payload.get("consumed_attempts") != 1:
                raise CampaignRunnerError("budget ledger row is not a consumed reservation")
            candidate = _candidate_from_mapping(payload["candidate"])
            if candidate.candidate_id in reservations:
                raise CampaignRunnerError("candidate opportunity was reserved twice")
            reservations[candidate.candidate_id] = payload
            stream_attempts.setdefault((candidate.treatment, candidate.seed), []).append(candidate.attempt_index)
        for attempts in stream_attempts.values():
            if attempts != list(range(len(attempts))):
                raise CampaignRunnerError("campaign attempt stream skipped or reordered an opportunity")

        results: dict[str, CandidateEvaluation] = {}
        for row in self.result.read_rows():
            payload = row.payload
            if payload.get("record_type") != "training_result":
                raise CampaignRunnerError("result ledger row has an unsupported record type")
            evaluation = _evaluation_from_mapping(payload["evaluation"])
            candidate_id = evaluation.candidate.candidate_id
            if candidate_id not in reservations:
                raise CampaignRunnerError("result references an unreserved opportunity")
            if candidate_id in results:
                raise CampaignRunnerError("reserved opportunity has duplicate results")
            reserved_candidate = _candidate_from_mapping(reservations[candidate_id]["candidate"])
            if evaluation.candidate != reserved_candidate:
                raise CampaignRunnerError("result candidate differs from reserved candidate")
            if evaluation.partition != "training":
                raise CampaignRunnerError("training result ledger contains non-training evidence")
            results[candidate_id] = evaluation

        pending = [candidate_id for candidate_id in reservations if candidate_id not in results]
        for treatment_seed, attempts in stream_attempts.items():
            stream_pending = [candidate_id for candidate_id, payload in reservations.items() if (_candidate_from_mapping(payload["candidate"]).treatment, _candidate_from_mapping(payload["candidate"]).seed) == treatment_seed and candidate_id not in results]
            if len(stream_pending) > 1:
                raise CampaignRunnerError("attempt stream has more than one pending reservation")
            if stream_pending:
                candidate = _candidate_from_mapping(reservations[stream_pending[0]]["candidate"])
                if candidate.attempt_index != attempts[-1]:
                    raise CampaignRunnerError("pending reservation is not the latest stream attempt")
        return {
            "reservations": reservations,
            "results": results,
            "pending_candidate_ids": tuple(sorted(pending)),
            "budget_fingerprint_sha256": self.budget.fingerprint(),
            "result_fingerprint_sha256": self.result.fingerprint(),
        }

    def reserve_attempt(self, candidate: SearchCandidate) -> LedgerRow:
        state = self.validate()
        if candidate.candidate_id in state["reservations"]:
            raise CampaignRunnerError("candidate opportunity is already reserved")
        stream = [
            _candidate_from_mapping(payload["candidate"])
            for payload in state["reservations"].values()
            if payload["candidate"]["treatment"] == candidate.treatment and int(payload["candidate"]["seed"]) == candidate.seed
        ]
        if candidate.attempt_index != len(stream):
            raise CampaignRunnerError("campaign attempt reservation skipped an opportunity")
        if any(item.candidate_id not in state["results"] for item in stream):
            raise CampaignRunnerError("cannot reserve after a pending opportunity")
        return self.budget.append({"record_type": "attempt_reserved", "consumed_attempts": 1, "candidate": asdict(candidate)})

    def append_training_result(self, evaluation: CandidateEvaluation) -> LedgerRow:
        state = self.validate()
        candidate_id = evaluation.candidate.candidate_id
        if candidate_id not in state["reservations"]:
            raise CampaignRunnerError("cannot append a result for an unreserved opportunity")
        if candidate_id in state["results"]:
            raise CampaignRunnerError("cannot append a duplicate result")
        reserved = _candidate_from_mapping(state["reservations"][candidate_id]["candidate"])
        if evaluation.candidate != reserved:
            raise CampaignRunnerError("evaluation candidate does not match reservation")
        if evaluation.partition != "training":
            raise CampaignRunnerError("only training results belong in this ledger")
        row = self.result.append({"record_type": "training_result", "evaluation": asdict(evaluation)})
        self.validate()
        return row

    def fingerprint(self) -> str:
        state = self.validate()
        return canonical_sha256({
            "protocol_id": self.budget.protocol_id,
            "campaign_id": self.budget.campaign_id,
            "evidence_class": self.budget.evidence_class,
            "budget": state["budget_fingerprint_sha256"],
            "result": state["result_fingerprint_sha256"],
        })


def reconstruct_training_agent(
    store: CampaignLedgerStore,
    protocol: Mapping[str, Any],
    treatment: str,
    seed: int,
) -> tuple[DesignSearchAgentV0, SearchCandidate | None]:
    state = store.validate()
    reservations = [
        _candidate_from_mapping(payload["candidate"])
        for payload in state["reservations"].values()
        if payload["candidate"]["treatment"] == treatment and int(payload["candidate"]["seed"]) == seed
    ]
    reservations.sort(key=lambda candidate: candidate.attempt_index)
    agent = DesignSearchAgentV0(protocol, treatment, seed)
    pending = None
    for candidate in reservations:
        proposed = agent.propose(candidate.attempt_index)
        if proposed != candidate:
            raise CampaignRunnerError("reconstructed candidate or RNG checkpoint differs")
        evaluation = state["results"].get(candidate.candidate_id)
        if evaluation is None:
            pending = candidate
            continue
        if pending is not None:
            raise CampaignRunnerError("completed result exists after a pending reservation")
        agent.observe(evaluation)
    return agent, pending


def execute_training_opportunities(
    store: CampaignLedgerStore,
    protocol: Mapping[str, Any],
    treatment: str,
    seed: int,
    evaluator: Callable[[SearchCandidate], CandidateEvaluation],
    *,
    target_attempts: int,
    authorization: CampaignExecutionAuthorization | None,
) -> tuple[CandidateEvaluation, ...]:
    if authorization is None:
        raise CampaignRunnerError("campaign execution is locked without authorization")
    if authorization.campaign_id != store.budget.campaign_id or seed not in authorization.allowed_seeds:
        raise CampaignRunnerError("execution authorization does not cover campaign or seed")
    if authorization.evidence_class != store.budget.evidence_class or not authorization.authorization_id:
        raise CampaignRunnerError("execution authorization evidence class or identity mismatch")
    if store.budget.evidence_class == "admitted_campaign" and not authorization.admitted_main_execution:
        raise CampaignRunnerError("admitted main execution is not authorized")
    if target_attempts < 0 or target_attempts > int(protocol["attempted_evaluations_per_treatment_seed"]):
        raise CampaignRunnerError("target attempt count exceeds the frozen budget")
    agent, pending = reconstruct_training_agent(store, protocol, treatment, seed)
    consumed = len(agent.history) + (1 if pending is not None else 0)
    if target_attempts < consumed:
        raise CampaignRunnerError("target attempt count is below already consumed budget")
    completed: list[CandidateEvaluation] = []
    if pending is not None:
        evaluation = evaluator(pending)
        store.append_training_result(evaluation)
        agent.observe(evaluation)
        completed.append(evaluation)
    while len(agent.history) < target_attempts:
        candidate = agent.propose(len(agent.history))
        store.reserve_attempt(candidate)
        evaluation = evaluator(candidate)
        store.append_training_result(evaluation)
        agent.observe(evaluation)
        completed.append(evaluation)
    return tuple(completed)


def select_training_promotions(
    evaluations: Sequence[CandidateEvaluation],
    treatments: Sequence[str],
    seeds: Sequence[int],
    *,
    per_treatment_seed: int,
) -> tuple[PromotionSelection, ...]:
    if per_treatment_seed <= 0:
        raise CampaignRunnerError("promotion cap must be positive")
    allowed = {(treatment, seed) for treatment in treatments for seed in seeds}
    seen_candidates: set[str] = set()
    for evaluation in evaluations:
        key = (evaluation.candidate.treatment, evaluation.candidate.seed)
        if key not in allowed:
            raise CampaignRunnerError("training result belongs to an unregistered treatment/seed")
        if evaluation.candidate.candidate_id in seen_candidates:
            raise CampaignRunnerError("training result candidate is duplicated")
        if evaluation.partition != "training":
            raise CampaignRunnerError("promotion selection cannot read holdout or refined data")
        seen_candidates.add(evaluation.candidate.candidate_id)
    selections = []
    for treatment in treatments:
        for seed in seeds:
            feasible = [
                evaluation for evaluation in evaluations
                if evaluation.candidate.treatment == treatment and evaluation.candidate.seed == seed
                and evaluation.status == "feasible" and evaluation.objective is not None
            ]
            feasible.sort(key=lambda item: (float(item.objective), item.candidate.candidate_id))
            selected = tuple(item.candidate.candidate_id for item in feasible[:per_treatment_seed])
            draft = {"treatment": treatment, "seed": seed, "candidate_ids": selected, "requested": per_treatment_seed, "selected": len(selected), "shortfall": per_treatment_seed-len(selected)}
            selections.append(PromotionSelection(**draft, selection_sha256=canonical_sha256(draft)))
    return tuple(selections)


def execution_protocol_from_main(main_protocol: Mapping[str, Any], *, seeds: Sequence[int] | None = None) -> dict[str, Any]:
    design = main_protocol["design"]
    selected_seeds = tuple(design["paired_seeds"] if seeds is None else seeds)
    return {
        "protocol_id": main_protocol["protocol_id"],
        "campaign_id": main_protocol["campaign_id"],
        "treatments": list(design["treatments"]),
        "seeds": list(selected_seeds),
        "attempted_evaluations_per_treatment_seed": int(design["attempted_evaluations_per_treatment_seed"]),
        "candidate_variables": design["candidate_variables"],
        "grid_levels_per_variable": int(design["grid"]["levels_per_variable"]),
        "evolution_initial_random": int(design["evolution"]["initial_random_attempts_per_seed"]),
        "evolution_mutation_sigma_fraction": float(design["evolution"]["mutation_sigma_fraction_of_range"]),
    }
