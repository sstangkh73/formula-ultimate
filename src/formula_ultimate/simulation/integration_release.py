"""Work 030 integration falsification, refinement, and promotion gates."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass, replace
from datetime import date
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any, Mapping

from formula_ultimate.physics.circuit import CircuitProfile

from .baseline_campaign import (
    BaselineCampaignProtocol,
    BaselineCampaignResult,
    run_baseline_campaign,
    verify_baseline_campaign_result,
)
from .coupling import (
    CompiledCouplingArchitecture,
    ComponentHealthState,
    ContactRuntimeState,
    ResidualEntry,
    SharedVehicleState,
)
from .transaction import (
    AdapterOutput,
    FunctionCoupledAdapter,
    RuntimeSignal,
    execute_coupled_step,
)


INTEGRATION_RELEASE_MODEL_VERSION = "work030-integration-release-v1"
_SHA256 = re.compile(r"[0-9a-f]{64}")
_FIDELITY_RANK = {"level0": 0, "level1": 1, "level2": 2, "physical": 3}


class IntegrationReleaseError(ValueError):
    """Raised when a Work 030 gate or evidence record is invalid."""


def _text(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise IntegrationReleaseError(f"{name} must not be blank")


def _finite(name: str, value: float) -> None:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
    ):
        raise IntegrationReleaseError(f"{name} must be finite")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise IntegrationReleaseError(f"{name} must be positive")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise IntegrationReleaseError(f"{name} must be non-negative")


def _json_ready(value: object) -> object:
    if isinstance(value, date):
        return value.isoformat()
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_ready(item) for item in value]
    return value


def _fingerprint(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            _json_ready(value),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def _expect_keys(label: str, raw: Mapping[str, Any], keys: set[str]) -> None:
    actual = set(raw)
    if actual != keys:
        raise IntegrationReleaseError(
            f"{label} keys differ: missing={sorted(keys-actual)!r}, "
            f"unexpected={sorted(actual-keys)!r}"
        )


@dataclass(frozen=True, slots=True)
class FalsificationRequirement:
    case_id: str
    expected_failure_code: str

    def __post_init__(self) -> None:
        _text("case_id", self.case_id)
        _text("expected_failure_code", self.expected_failure_code)


@dataclass(frozen=True, slots=True)
class RefinementGateConfiguration:
    timesteps_s: tuple[float, ...]
    random_seed: int
    evaluation_budget_per_run: int
    maximum_relative_time_variation: float
    maximum_relative_energy_variation: float
    maximum_finish_residual_m: float

    def __post_init__(self) -> None:
        if len(self.timesteps_s) < 3:
            raise IntegrationReleaseError("refinement requires at least three timesteps")
        for value in self.timesteps_s:
            _positive("refinement timestep", value)
        if len(self.timesteps_s) != len(set(self.timesteps_s)):
            raise IntegrationReleaseError("refinement timesteps must be unique")
        object.__setattr__(self, "timesteps_s", tuple(sorted(self.timesteps_s, reverse=True)))
        if not isinstance(self.random_seed, int) or isinstance(self.random_seed, bool):
            raise IntegrationReleaseError("refinement random_seed must be integer")
        if (
            not isinstance(self.evaluation_budget_per_run, int)
            or isinstance(self.evaluation_budget_per_run, bool)
            or self.evaluation_budget_per_run <= 0
        ):
            raise IntegrationReleaseError(
                "refinement evaluation_budget_per_run must be positive integer"
            )
        for name in (
            "maximum_relative_time_variation",
            "maximum_relative_energy_variation",
            "maximum_finish_residual_m",
        ):
            _nonnegative(name, getattr(self, name))


@dataclass(frozen=True, slots=True)
class PromotionGateConfiguration:
    minimum_completed_profiles: int
    require_real_circuit_admission: bool
    require_independent_evidence: bool
    minimum_fidelity_level: str
    required_evidence_types: tuple[str, ...]
    automatic_discovery_claim: bool

    def __post_init__(self) -> None:
        if (
            not isinstance(self.minimum_completed_profiles, int)
            or isinstance(self.minimum_completed_profiles, bool)
            or self.minimum_completed_profiles <= 0
        ):
            raise IntegrationReleaseError("minimum_completed_profiles must be positive integer")
        for name in (
            "require_real_circuit_admission",
            "require_independent_evidence",
            "automatic_discovery_claim",
        ):
            if not isinstance(getattr(self, name), bool):
                raise IntegrationReleaseError(f"{name} must be boolean")
        if self.minimum_fidelity_level not in _FIDELITY_RANK:
            raise IntegrationReleaseError("unsupported minimum fidelity level")
        if not self.required_evidence_types:
            raise IntegrationReleaseError("required evidence types must not be empty")
        for item in self.required_evidence_types:
            _text("required evidence type", item)
        if len(self.required_evidence_types) != len(set(self.required_evidence_types)):
            raise IntegrationReleaseError("required evidence types must be unique")
        object.__setattr__(
            self, "required_evidence_types", tuple(sorted(self.required_evidence_types))
        )
        if self.automatic_discovery_claim:
            raise IntegrationReleaseError("automatic discovery claims are forbidden")


@dataclass(frozen=True, slots=True)
class IntegrationGateProtocol:
    schema_version: str
    gate_id: str
    falsification_requirements: tuple[FalsificationRequirement, ...]
    refinement: RefinementGateConfiguration
    promotion: PromotionGateConfiguration

    def __post_init__(self) -> None:
        if self.schema_version != "1.0":
            raise IntegrationReleaseError("unsupported integration gate schema")
        _text("gate_id", self.gate_id)
        if not self.falsification_requirements:
            raise IntegrationReleaseError("falsification requirements must not be empty")
        ids = tuple(item.case_id for item in self.falsification_requirements)
        if len(ids) != len(set(ids)):
            raise IntegrationReleaseError("falsification case IDs must be unique")
        object.__setattr__(
            self,
            "falsification_requirements",
            tuple(sorted(self.falsification_requirements, key=lambda item: item.case_id)),
        )

    @property
    def fingerprint_sha256(self) -> str:
        return _fingerprint(self)


@dataclass(frozen=True, slots=True)
class FalsificationCaseResult:
    case_id: str
    expected_failure_code: str
    observed_status: str
    observed_failure_code: str | None
    detected: bool
    rolled_back: bool
    reason: str


@dataclass(frozen=True, slots=True)
class FalsificationSuiteResult:
    control_status: str
    control_committed: bool
    required_case_count: int
    detected_case_count: int
    all_required_faults_detected: bool
    cases: tuple[FalsificationCaseResult, ...]
    fingerprint_sha256: str


@dataclass(frozen=True, slots=True)
class RefinementSample:
    circuit_id: str
    partition: str
    timestep_s: float
    outcome: str
    final_time_s: float
    final_distance_m: float
    primary_energy_used_j: float
    finish_distance_residual_m: float
    attempted_steps: int
    all_residuals_passed: bool
    race_replay_fingerprint_sha256: str


@dataclass(frozen=True, slots=True)
class RefinementAssessment:
    status: str
    reason: str
    max_relative_time_variation: float
    max_relative_energy_variation: float
    max_absolute_finish_residual_m: float
    exact_step_invariant_control: bool
    convergence_order_estimated: bool
    samples: tuple[RefinementSample, ...]
    fingerprint_sha256: str
    claim_boundary: str


@dataclass(frozen=True, slots=True)
class CrossModelEvidence:
    evidence_id: str
    evidence_type: str
    fidelity_level: str
    independent: bool
    passed: bool
    artifact_fingerprint_sha256: str
    source_reference: str

    def __post_init__(self) -> None:
        for name in ("evidence_id", "evidence_type", "source_reference"):
            _text(name, getattr(self, name))
        if self.fidelity_level not in _FIDELITY_RANK:
            raise IntegrationReleaseError("unsupported evidence fidelity level")
        if not isinstance(self.independent, bool) or not isinstance(self.passed, bool):
            raise IntegrationReleaseError("evidence independent/passed must be boolean")
        if not _SHA256.fullmatch(self.artifact_fingerprint_sha256):
            raise IntegrationReleaseError("evidence artifact fingerprint must be SHA-256")


@dataclass(frozen=True, slots=True)
class PromotionDecision:
    candidate_id: str
    status: str
    blocking_reasons: tuple[str, ...]
    accepted_evidence_ids: tuple[str, ...]
    discovery_claim_allowed: bool
    automatic_promotion: bool
    fingerprint_sha256: str


@dataclass(frozen=True, slots=True)
class IntegrationReleaseReview:
    model_version: str
    gate_id: str
    status: str
    level0_infrastructure_ready: bool
    gated_level0_experimentation_authorized: bool
    promotion_status: str
    real_circuit_claim_allowed: bool
    discovery_claim_allowed: bool
    safety_claim_allowed: bool
    manufacturability_claim_allowed: bool
    open_blockers: tuple[str, ...]
    fingerprint_sha256: str
    claim_boundary: str


def load_integration_gate_protocol(path: str | Path) -> IntegrationGateProtocol:
    """Load the strict Work 030 gate protocol."""

    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise IntegrationReleaseError("gate root must be an object")
        _expect_keys(
            "gate",
            raw,
            {"schema_version", "gate_id", "falsification", "refinement", "promotion"},
        )
        falsification = raw["falsification"]
        refinement = raw["refinement"]
        promotion = raw["promotion"]
        if not all(isinstance(item, dict) for item in (falsification, refinement, promotion)):
            raise IntegrationReleaseError("gate sections must be objects")
        _expect_keys("falsification", falsification, {"required_cases"})
        cases = falsification["required_cases"]
        if not isinstance(cases, dict):
            raise IntegrationReleaseError("required_cases must be an object")
        _expect_keys(
            "refinement",
            refinement,
            {
                "timesteps_s",
                "random_seed",
                "evaluation_budget_per_run",
                "maximum_relative_time_variation",
                "maximum_relative_energy_variation",
                "maximum_finish_residual_m",
            },
        )
        _expect_keys(
            "promotion",
            promotion,
            {
                "minimum_completed_profiles",
                "require_real_circuit_admission",
                "require_independent_evidence",
                "minimum_fidelity_level",
                "required_evidence_types",
                "automatic_discovery_claim",
            },
        )
        if not isinstance(refinement["timesteps_s"], list):
            raise IntegrationReleaseError("timesteps_s must be a JSON array")
        if not isinstance(promotion["required_evidence_types"], list):
            raise IntegrationReleaseError("required_evidence_types must be a JSON array")
        return IntegrationGateProtocol(
            str(raw["schema_version"]),
            str(raw["gate_id"]),
            tuple(
                FalsificationRequirement(str(case_id), str(code))
                for case_id, code in cases.items()
            ),
            RefinementGateConfiguration(
                tuple(refinement["timesteps_s"]),
                refinement["random_seed"],
                refinement["evaluation_budget_per_run"],
                refinement["maximum_relative_time_variation"],
                refinement["maximum_relative_energy_variation"],
                refinement["maximum_finish_residual_m"],
            ),
            PromotionGateConfiguration(
                promotion["minimum_completed_profiles"],
                promotion["require_real_circuit_admission"],
                promotion["require_independent_evidence"],
                str(promotion["minimum_fidelity_level"]),
                tuple(str(item) for item in promotion["required_evidence_types"]),
                promotion["automatic_discovery_claim"],
            ),
        )
    except IntegrationReleaseError:
        raise
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise IntegrationReleaseError(f"invalid integration gate protocol: {exc}") from exc


def _falsification_start_state() -> SharedVehicleState:
    return SharedVehicleState(
        1.0,
        1.0,
        (1.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        0.0,
        0.0,
        1000.0,
        0.0,
        0,
        (ContactRuntimeState("contact", 1000.0, 0.0, 0.0, 0.0, 1.0),),
        (ComponentHealthState("component", 300.0, 0.0, 0.0, False),),
    )


def _transaction_fixture(
    architecture: CompiledCouplingArchitecture,
    fault_case: str | None,
):
    start = _falsification_start_state()
    initial = tuple(
        RuntimeSignal(
            signal_id,
            start if signal_id == "manifest.current_state" else {"fixture": signal_id},
        )
        for signal_id in architecture.initial_signals
    )
    adapters = []
    for index, module in enumerate(architecture.ordered_modules):
        is_first = index == 0
        is_second = index == 1
        is_last = index == len(architecture.ordered_modules) - 1

        def function(
            view,
            module=module,
            is_first=is_first,
            is_second=is_second,
            is_last=is_last,
        ):
            for signal_id in module.consumes:
                view.read(signal_id)
            outputs = []
            for signal_id in module.produces:
                if signal_id == "state.current":
                    value = start
                elif signal_id == "state.next":
                    value = replace(
                        start,
                        time_s=(0.0 if fault_case == "time_regression" else 2.0),
                        race_distance_m=2.0,
                    )
                else:
                    value = {"producer": module.module_id, "signal": signal_id}
                outputs.append(RuntimeSignal(signal_id, value))
            if fault_case == "undeclared_output" and is_first:
                outputs.append(RuntimeSignal("fault.undeclared", True))
            residuals = ()
            if fault_case == "duplicate_residual" and (is_first or is_second):
                residuals = (
                    ResidualEntry("fault.duplicate", "energy", 0.0, "J", 0.0, 0.0, 1.0),
                )
            elif fault_case == "failed_residual" and is_first:
                residuals = (
                    ResidualEntry("fault.failed", "energy", 1.0, "J", 0.0, 0.0, 1.0),
                )
            return AdapterOutput(module.module_id, "ok", tuple(outputs), residuals=residuals)

        version = (
            "fault-version"
            if fault_case == "version_mismatch" and is_first
            else module.model_version
        )
        adapters.append(FunctionCoupledAdapter(module.module_id, version, function))
    if fault_case == "missing_adapter":
        adapters.pop()
    return start, initial, tuple(adapters)


def run_transaction_falsification_suite(
    *,
    protocol: IntegrationGateProtocol,
    architecture: CompiledCouplingArchitecture,
) -> FalsificationSuiteResult:
    """Run the declared faults against the real atomic v4 transaction."""

    control_fixture = _transaction_fixture(architecture, None)
    control = execute_coupled_step(
        architecture=architecture,
        start_state=control_fixture[0],
        initial_signals=control_fixture[1],
        adapters=control_fixture[2],
    )
    case_results = []
    for requirement in protocol.falsification_requirements:
        fixture = _transaction_fixture(architecture, requirement.case_id)
        result = execute_coupled_step(
            architecture=architecture,
            start_state=fixture[0],
            initial_signals=fixture[1],
            adapters=fixture[2],
        )
        observed = None if result.failure is None else result.failure.code
        detected = result.status == "invalid" and observed == requirement.expected_failure_code
        rolled_back = result.committed_state is None
        case_results.append(
            FalsificationCaseResult(
                requirement.case_id,
                requirement.expected_failure_code,
                result.status,
                observed,
                detected,
                rolled_back,
                "" if result.failure is None else result.failure.reason,
            )
        )
    cases = tuple(sorted(case_results, key=lambda item: item.case_id))
    all_detected = all(item.detected and item.rolled_back for item in cases)
    payload = {
        "control_status": control.status,
        "control_committed": control.committed_state is not None,
        "cases": cases,
    }
    return FalsificationSuiteResult(
        control.status,
        control.committed_state is not None,
        len(protocol.falsification_requirements),
        sum(item.detected and item.rolled_back for item in cases),
        all_detected and control.status == "committed",
        cases,
        _fingerprint(payload),
    )


def assess_refinement_samples(
    *,
    samples: tuple[RefinementSample, ...],
    configuration: RefinementGateConfiguration,
) -> RefinementAssessment:
    """Assess bounded sensitivity without inventing a convergence order."""

    if not samples:
        raise IntegrationReleaseError("refinement samples must not be empty")
    ordered = tuple(sorted(samples, key=lambda item: (item.circuit_id, -item.timestep_s)))
    circuit_ids = tuple(sorted({item.circuit_id for item in ordered}))
    time_variations = []
    energy_variations = []
    for circuit_id in circuit_ids:
        group = tuple(item for item in ordered if item.circuit_id == circuit_id)
        if {item.timestep_s for item in group} != set(configuration.timesteps_s):
            raise IntegrationReleaseError(
                f"refinement timesteps are incomplete for {circuit_id}"
            )
        finest = min(group, key=lambda item: item.timestep_s)
        for item in group:
            time_variations.append(
                abs(item.final_time_s - finest.final_time_s)
                / max(1.0, abs(finest.final_time_s))
            )
            energy_variations.append(
                abs(item.primary_energy_used_j - finest.primary_energy_used_j)
                / max(1.0, abs(finest.primary_energy_used_j))
            )
    max_time = max(time_variations, default=0.0)
    max_energy = max(energy_variations, default=0.0)
    max_finish = max(abs(item.finish_distance_residual_m) for item in ordered)
    basic = all(
        item.outcome == "finished" and item.all_residuals_passed for item in ordered
    )
    passed = (
        basic
        and max_time <= configuration.maximum_relative_time_variation
        and max_energy <= configuration.maximum_relative_energy_variation
        and max_finish <= configuration.maximum_finish_residual_m
    )
    exact = max_time == 0.0 and max_energy == 0.0 and max_finish == 0.0
    reason = (
        "analytical steady reference is within declared timestep sensitivity bounds"
        if passed
        else "refinement sensitivity or run validity exceeded the declared gate"
    )
    payload = {
        "status": "passed" if passed else "blocked",
        "max_time": max_time,
        "max_energy": max_energy,
        "max_finish": max_finish,
        "samples": ordered,
    }
    return RefinementAssessment(
        "passed" if passed else "blocked",
        reason,
        max_time,
        max_energy,
        max_finish,
        exact,
        False,
        ordered,
        _fingerprint(payload),
        (
            "Timestep sensitivity of one steady Level-0 analytical control only; "
            "no convergence order, uncertainty closure, or higher-fidelity validation"
        ),
    )


def run_baseline_refinement_matrix(
    *,
    gate_protocol: IntegrationGateProtocol,
    baseline_protocol: BaselineCampaignProtocol,
    architecture: CompiledCouplingArchitecture,
    profiles: tuple[CircuitProfile, ...],
) -> RefinementAssessment:
    """Run one calibration and one holdout profile at all declared timesteps."""

    controls = baseline_protocol.controls
    selected_ids = (
        controls.calibration_circuit_ids[0],
        controls.holdout_circuit_ids[0],
    )
    by_id = {profile.circuit_id: profile for profile in profiles}
    if any(circuit_id not in by_id for circuit_id in selected_ids):
        raise IntegrationReleaseError("refinement profile is absent from catalog")
    selected = tuple(by_id[circuit_id] for circuit_id in selected_ids)
    samples = []
    for timestep_s in gate_protocol.refinement.timesteps_s:
        reduced_controls = replace(
            controls,
            time_step_s=timestep_s,
            evaluation_budget_per_run=gate_protocol.refinement.evaluation_budget_per_run,
            random_seeds=(gate_protocol.refinement.random_seed,),
            calibration_circuit_ids=(selected_ids[0],),
            holdout_circuit_ids=(selected_ids[1],),
        )
        result = run_baseline_campaign(
            protocol=replace(baseline_protocol, controls=reduced_controls),
            architecture=architecture,
            profiles=selected,
        )
        for run in result.runs:
            samples.append(
                RefinementSample(
                    run.circuit_id,
                    run.partition,
                    timestep_s,
                    run.outcome,
                    run.final_time_s,
                    run.final_distance_m,
                    run.primary_energy_used_j,
                    run.finish_distance_residual_m,
                    run.attempted_steps,
                    run.all_residuals_passed,
                    run.race_replay_fingerprint_sha256,
                )
            )
    return assess_refinement_samples(
        samples=tuple(samples), configuration=gate_protocol.refinement
    )


def evaluate_promotion_gate(
    *,
    candidate_id: str,
    protocol: IntegrationGateProtocol,
    campaign: BaselineCampaignResult,
    falsification: FalsificationSuiteResult,
    refinement: RefinementAssessment,
    cross_model_evidence: tuple[CrossModelEvidence, ...],
) -> PromotionDecision:
    """Return review eligibility; never automatically declare a discovery."""

    _text("candidate_id", candidate_id)
    evidence_ids = tuple(item.evidence_id for item in cross_model_evidence)
    if len(evidence_ids) != len(set(evidence_ids)):
        raise IntegrationReleaseError("cross-model evidence IDs must be unique")
    reasons = []
    gate = protocol.promotion
    campaign_identity_valid, campaign_identity_reasons = (
        verify_baseline_campaign_result(campaign)
    )
    if not campaign_identity_valid:
        reasons.extend(
            f"campaign_evidence_invalid:{reason}"
            for reason in campaign_identity_reasons
        )
    if not campaign.all_runs_finished:
        reasons.append("baseline_campaign_not_finished")
    if not campaign.all_residuals_passed:
        reasons.append("baseline_residuals_failed")
    if not campaign.all_runs_within_budget:
        reasons.append("baseline_compute_budget_failed")
    if campaign.completed_profile_count < gate.minimum_completed_profiles:
        reasons.append("minimum_profile_coverage_missing")
    if gate.require_real_circuit_admission and not campaign.real_circuit_admitted:
        reasons.append("real_circuit_admission_missing")
    if not falsification.all_required_faults_detected:
        reasons.append("integration_falsification_incomplete")
    if refinement.status != "passed":
        reasons.append("numerical_refinement_blocked")

    accepted = []
    minimum_rank = _FIDELITY_RANK[gate.minimum_fidelity_level]
    for evidence_type in gate.required_evidence_types:
        candidates = tuple(
            item for item in cross_model_evidence if item.evidence_type == evidence_type
        )
        valid = tuple(
            item
            for item in candidates
            if item.passed
            and _FIDELITY_RANK[item.fidelity_level] >= minimum_rank
            and (item.independent or not gate.require_independent_evidence)
        )
        if not valid:
            reasons.append(f"missing_or_invalid_evidence:{evidence_type}")
        else:
            accepted.extend(item.evidence_id for item in valid)
    blocking = tuple(sorted(set(reasons)))
    status = "blocked" if blocking else "eligible_for_independent_review"
    payload = {
        "candidate_id": candidate_id,
        "gate": protocol.fingerprint_sha256,
        "campaign": campaign.result_fingerprint_sha256,
        "falsification": falsification.fingerprint_sha256,
        "refinement": refinement.fingerprint_sha256,
        "status": status,
        "blocking": blocking,
        "accepted": tuple(sorted(accepted)),
    }
    return PromotionDecision(
        candidate_id,
        status,
        blocking,
        tuple(sorted(accepted)),
        False,
        False,
        _fingerprint(payload),
    )


def create_integration_release_review(
    *,
    protocol: IntegrationGateProtocol,
    campaign: BaselineCampaignResult,
    falsification: FalsificationSuiteResult,
    refinement: RefinementAssessment,
    promotion: PromotionDecision,
) -> IntegrationReleaseReview:
    """Separate Level-0 experimentation readiness from promotion claims."""

    ready = (
        campaign.all_runs_finished
        and campaign.all_residuals_passed
        and campaign.all_runs_within_budget
        and falsification.all_required_faults_detected
        and refinement.status == "passed"
    )
    if ready and promotion.status == "blocked":
        status = "level0_experimentation_ready_promotion_blocked"
    elif ready:
        status = "level0_experimentation_ready_independent_review_required"
    else:
        status = "integration_release_blocked"
    blockers = promotion.blocking_reasons
    payload = {
        "model_version": INTEGRATION_RELEASE_MODEL_VERSION,
        "gate": protocol.fingerprint_sha256,
        "campaign": campaign.result_fingerprint_sha256,
        "falsification": falsification.fingerprint_sha256,
        "refinement": refinement.fingerprint_sha256,
        "promotion": promotion.fingerprint_sha256,
        "status": status,
        "ready": ready,
        "blockers": blockers,
    }
    return IntegrationReleaseReview(
        INTEGRATION_RELEASE_MODEL_VERSION,
        protocol.gate_id,
        status,
        ready,
        ready,
        promotion.status,
        False,
        False,
        False,
        False,
        blockers,
        _fingerprint(payload),
        (
            "Coupled Level-0 research infrastructure only; promotion, discovery, "
            "real-circuit, safety, and manufacturability claims require independent "
            "higher-fidelity and physical evidence"
        ),
    )
