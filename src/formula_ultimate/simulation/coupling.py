"""Versioned contracts for deterministic coupled-vehicle orchestration.

Work 021 defines signal provenance, shared state, experiment identity, residual
evidence, and event priority.  It deliberately does not execute the independent
physics solvers as one vehicle yet.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any, Mapping


class CouplingContractError(ValueError):
    """Raised when a coupling declaration violates the Work 021 contract."""


COUPLING_STAGES = (
    "inputs",
    "aerodynamics",
    "load_balance",
    "contact_limits",
    "motion",
    "energy_audit",
    "health",
    "race_progress",
)

EVENT_PRIORITY = {
    "finished": 0,
    "thermal_failure": 1,
    "reliability_failure": 2,
    "structural_failure": 3,
    "damage_failure": 4,
    "degradation_failure": 5,
    "energy_depletion": 6,
    "timeout": 7,
    "step_complete": 8,
}

RESIDUAL_UNITS = {
    "force": "N",
    "moment": "N*m",
    "energy": "J",
    "distance": "m",
    "time": "s",
    "state": "1",
}

_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_COMMIT_PATTERN = re.compile(r"^[0-9a-f]{7,40}$")


def _nonblank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise CouplingContractError(f"{name} must not be blank")


def _finite(name: str, value: float) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise CouplingContractError(f"{name} must be a real number")
    if not math.isfinite(value):
        raise CouplingContractError(f"{name} must be finite; received {value!r}")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise CouplingContractError(f"{name} must be > 0; received {value!r}")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise CouplingContractError(f"{name} must be >= 0; received {value!r}")


def _vector3(name: str, value: tuple[float, float, float]) -> None:
    if not isinstance(value, tuple) or len(value) != 3:
        raise CouplingContractError(f"{name} must be a three-value tuple")
    for index, item in enumerate(value):
        _finite(f"{name}[{index}]", item)


def _unique_nonblank(name: str, values: tuple[str, ...]) -> None:
    for value in values:
        _nonblank(name, value)
    if len(values) != len(set(values)):
        raise CouplingContractError(f"{name} values must be unique")


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class CoupledModuleSpec:
    module_id: str
    stage: str
    model_version: str
    consumes: tuple[str, ...]
    produces: tuple[str, ...]

    def __post_init__(self) -> None:
        _nonblank("module_id", self.module_id)
        if self.stage not in COUPLING_STAGES:
            raise CouplingContractError(f"unsupported coupling stage {self.stage!r}")
        _nonblank("model_version", self.model_version)
        _unique_nonblank("consumed signal", self.consumes)
        _unique_nonblank("produced signal", self.produces)
        if not self.produces:
            raise CouplingContractError("each module must produce at least one signal")
        overlap = set(self.consumes) & set(self.produces)
        if overlap:
            raise CouplingContractError(
                f"module cannot consume and produce the same signal: {sorted(overlap)!r}"
            )


@dataclass(frozen=True, slots=True)
class CompiledCouplingArchitecture:
    schema_version: str
    architecture_id: str
    initial_signals: tuple[str, ...]
    ordered_modules: tuple[CoupledModuleSpec, ...]
    signal_producers: tuple[tuple[str, str], ...]
    fingerprint_sha256: str


def compile_coupling_architecture(
    *,
    architecture_id: str,
    modules: tuple[CoupledModuleSpec, ...],
    initial_signals: tuple[str, ...],
    schema_version: str = "1.0",
    required_stages: tuple[str, ...] = COUPLING_STAGES,
) -> CompiledCouplingArchitecture:
    """Validate provenance/causality and return deterministic execution order."""

    if schema_version != "1.0":
        raise CouplingContractError(
            f"unsupported coupling schema_version {schema_version!r}"
        )
    _nonblank("architecture_id", architecture_id)
    if not modules:
        raise CouplingContractError("coupling architecture must contain modules")
    _unique_nonblank("initial signal", initial_signals)
    _unique_nonblank("required stage", required_stages)
    unknown_required = set(required_stages) - set(COUPLING_STAGES)
    if unknown_required:
        raise CouplingContractError(
            f"unsupported required stages: {sorted(unknown_required)!r}"
        )

    module_ids = tuple(module.module_id for module in modules)
    if len(module_ids) != len(set(module_ids)):
        raise CouplingContractError("module_id values must be unique")
    present_stages = {module.stage for module in modules}
    missing_stages = set(required_stages) - present_stages
    if missing_stages:
        raise CouplingContractError(
            f"required coupling stages are missing: {sorted(missing_stages)!r}"
        )

    stage_index = {stage: index for index, stage in enumerate(COUPLING_STAGES)}
    producer_by_signal: dict[str, str] = {
        signal: "__initial__" for signal in initial_signals
    }
    producer_stage: dict[str, int] = {signal: -1 for signal in initial_signals}
    for module in modules:
        module_stage = stage_index[module.stage]
        for signal in module.produces:
            if signal in producer_by_signal:
                raise CouplingContractError(
                    f"signal {signal!r} has multiple producers: "
                    f"{producer_by_signal[signal]!r} and {module.module_id!r}"
                )
            producer_by_signal[signal] = module.module_id
            producer_stage[signal] = module_stage

    for module in modules:
        consumer_stage = stage_index[module.stage]
        for signal in module.consumes:
            if signal not in producer_by_signal:
                raise CouplingContractError(
                    f"module {module.module_id!r} consumes signal {signal!r} "
                    "without a producer"
                )
            if producer_stage[signal] >= consumer_stage:
                raise CouplingContractError(
                    f"module {module.module_id!r} consumes {signal!r} from the "
                    "same or a later stage"
                )

    ordered = tuple(
        sorted(modules, key=lambda module: (stage_index[module.stage], module.module_id))
    )
    canonical_initial = tuple(sorted(initial_signals))
    canonical_producers = tuple(sorted(producer_by_signal.items()))
    payload = {
        "schema_version": schema_version,
        "architecture_id": architecture_id,
        "initial_signals": canonical_initial,
        "modules": [
            {
                "module_id": module.module_id,
                "stage": module.stage,
                "model_version": module.model_version,
                "consumes": sorted(module.consumes),
                "produces": sorted(module.produces),
            }
            for module in ordered
        ],
    }
    return CompiledCouplingArchitecture(
        schema_version=schema_version,
        architecture_id=architecture_id,
        initial_signals=canonical_initial,
        ordered_modules=ordered,
        signal_producers=canonical_producers,
        fingerprint_sha256=_canonical_sha256(payload),
    )


def _require_exact_keys(
    name: str, raw: Mapping[str, Any], required: set[str]
) -> None:
    actual = set(raw)
    missing = required - actual
    extra = actual - required
    if missing or extra:
        raise CouplingContractError(
            f"{name} keys mismatch; missing={sorted(missing)!r}, "
            f"extra={sorted(extra)!r}"
        )


def _json_string(name: str, value: Any) -> str:
    if not isinstance(value, str):
        raise CouplingContractError(f"{name} must be a string")
    return value


def _json_string_array(name: str, value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise CouplingContractError(f"{name} must be an array")
    if any(not isinstance(item, str) for item in value):
        raise CouplingContractError(f"{name} items must be strings")
    return tuple(value)


def load_coupling_architecture(
    path: str | Path,
) -> CompiledCouplingArchitecture:
    """Load a fail-closed JSON declaration and compile it."""

    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise CouplingContractError("architecture JSON root must be an object")
        _require_exact_keys(
            "architecture",
            raw,
            {"schema_version", "architecture_id", "initial_signals", "modules"},
        )
        initial_signals = _json_string_array(
            "initial_signals", raw["initial_signals"]
        )
        if not isinstance(raw["modules"], list):
            raise CouplingContractError("modules must be an array")
        modules: list[CoupledModuleSpec] = []
        required_module_keys = {
            "module_id",
            "stage",
            "model_version",
            "consumes",
            "produces",
        }
        for index, item in enumerate(raw["modules"]):
            if not isinstance(item, dict):
                raise CouplingContractError(f"module[{index}] must be an object")
            _require_exact_keys(f"module[{index}]", item, required_module_keys)
            modules.append(
                CoupledModuleSpec(
                    module_id=_json_string(
                        f"module[{index}].module_id", item["module_id"]
                    ),
                    stage=_json_string(f"module[{index}].stage", item["stage"]),
                    model_version=_json_string(
                        f"module[{index}].model_version", item["model_version"]
                    ),
                    consumes=_json_string_array(
                        f"module[{index}].consumes", item["consumes"]
                    ),
                    produces=_json_string_array(
                        f"module[{index}].produces", item["produces"]
                    ),
                )
            )
        return compile_coupling_architecture(
            schema_version=_json_string("schema_version", raw["schema_version"]),
            architecture_id=_json_string("architecture_id", raw["architecture_id"]),
            initial_signals=initial_signals,
            modules=tuple(modules),
        )
    except CouplingContractError:
        raise
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise CouplingContractError(f"invalid coupling architecture: {exc}") from exc


@dataclass(frozen=True, slots=True)
class ArtifactReference:
    artifact_id: str
    sha256: str

    def __post_init__(self) -> None:
        _nonblank("artifact_id", self.artifact_id)
        if not _SHA256_PATTERN.fullmatch(self.sha256):
            raise CouplingContractError(
                "artifact sha256 must be 64 lowercase hexadecimal characters"
            )


@dataclass(frozen=True, slots=True)
class VersionPin:
    pin_id: str
    version: str

    def __post_init__(self) -> None:
        _nonblank("pin_id", self.pin_id)
        _nonblank("version", self.version)


@dataclass(frozen=True, slots=True)
class ExperimentManifest:
    schema_version: str
    experiment_id: str
    candidate_id: str
    design_language_version: str
    geometry_artifacts: tuple[ArtifactReference, ...]
    component_catalog_version: str
    circuit_profile_id: str
    regulatory_profile_version: str
    energy_profile_version: str
    solver_profile_version: str
    model_versions: tuple[VersionPin, ...]
    architecture_fingerprint_sha256: str
    source_commit: str
    random_seed: int
    evaluation_budget: int
    time_step_s: float

    def __post_init__(self) -> None:
        if self.schema_version != "1.0":
            raise CouplingContractError(
                f"unsupported manifest schema_version {self.schema_version!r}"
            )
        for name in (
            "experiment_id",
            "candidate_id",
            "design_language_version",
            "component_catalog_version",
            "circuit_profile_id",
            "regulatory_profile_version",
            "energy_profile_version",
            "solver_profile_version",
        ):
            _nonblank(name, getattr(self, name))
        if not self.geometry_artifacts:
            raise CouplingContractError("geometry_artifacts must not be empty")
        artifact_ids = tuple(item.artifact_id for item in self.geometry_artifacts)
        if len(artifact_ids) != len(set(artifact_ids)):
            raise CouplingContractError("geometry artifact IDs must be unique")
        if not self.model_versions:
            raise CouplingContractError("model_versions must not be empty")
        pin_ids = tuple(item.pin_id for item in self.model_versions)
        if len(pin_ids) != len(set(pin_ids)):
            raise CouplingContractError("model version pin IDs must be unique")
        if not _SHA256_PATTERN.fullmatch(self.architecture_fingerprint_sha256):
            raise CouplingContractError(
                "architecture fingerprint must be 64 lowercase hexadecimal characters"
            )
        if not _COMMIT_PATTERN.fullmatch(self.source_commit):
            raise CouplingContractError(
                "source_commit must be 7 to 40 lowercase hexadecimal characters"
            )
        if not isinstance(self.random_seed, int) or isinstance(self.random_seed, bool):
            raise CouplingContractError("random_seed must be an integer")
        if (
            not isinstance(self.evaluation_budget, int)
            or isinstance(self.evaluation_budget, bool)
            or self.evaluation_budget <= 0
        ):
            raise CouplingContractError("evaluation_budget must be a positive integer")
        _positive("time_step_s", self.time_step_s)

    @property
    def fingerprint_sha256(self) -> str:
        payload = {
            "schema_version": self.schema_version,
            "experiment_id": self.experiment_id,
            "candidate_id": self.candidate_id,
            "design_language_version": self.design_language_version,
            "geometry_artifacts": [
                {"artifact_id": item.artifact_id, "sha256": item.sha256}
                for item in sorted(
                    self.geometry_artifacts, key=lambda item: item.artifact_id
                )
            ],
            "component_catalog_version": self.component_catalog_version,
            "circuit_profile_id": self.circuit_profile_id,
            "regulatory_profile_version": self.regulatory_profile_version,
            "energy_profile_version": self.energy_profile_version,
            "solver_profile_version": self.solver_profile_version,
            "model_versions": [
                {"pin_id": item.pin_id, "version": item.version}
                for item in sorted(self.model_versions, key=lambda item: item.pin_id)
            ],
            "architecture_fingerprint_sha256": (
                self.architecture_fingerprint_sha256
            ),
            "source_commit": self.source_commit,
            "random_seed": self.random_seed,
            "evaluation_budget": self.evaluation_budget,
            "time_step_s": self.time_step_s,
        }
        return _canonical_sha256(payload)


@dataclass(frozen=True, slots=True)
class ContactRuntimeState:
    contact_id: str
    normal_load_n: float
    longitudinal_force_n: float
    lateral_force_n: float
    suspension_travel_m: float
    angular_speed_rad_per_s: float
    suspension_velocity_m_per_s: float = 0.0
    brake_temperature_k: float = 300.0
    stored_recovered_energy_j: float = 0.0
    suspension_failed: bool = False
    brake_failed: bool = False

    def __post_init__(self) -> None:
        _nonblank("contact_id", self.contact_id)
        _nonnegative("normal_load_n", self.normal_load_n)
        for name in (
            "longitudinal_force_n",
            "lateral_force_n",
            "suspension_travel_m",
            "angular_speed_rad_per_s",
            "suspension_velocity_m_per_s",
        ):
            _finite(name, getattr(self, name))
        _positive("brake_temperature_k", self.brake_temperature_k)
        _nonnegative("stored_recovered_energy_j", self.stored_recovered_energy_j)
        if not isinstance(self.suspension_failed, bool) or not isinstance(
            self.brake_failed, bool
        ):
            raise CouplingContractError("contact failure flags must be boolean")


@dataclass(frozen=True, slots=True)
class ComponentHealthState:
    component_id: str
    temperature_k: float
    degradation: float
    damage: float
    failed: bool

    def __post_init__(self) -> None:
        _nonblank("component_id", self.component_id)
        _positive("temperature_k", self.temperature_k)
        _nonnegative("degradation", self.degradation)
        _nonnegative("damage", self.damage)
        if not isinstance(self.failed, bool):
            raise CouplingContractError("failed must be boolean")


@dataclass(frozen=True, slots=True)
class SharedVehicleState:
    time_s: float
    race_distance_m: float
    position_m: tuple[float, float, float]
    velocity_mps: tuple[float, float, float]
    yaw_rad: float
    yaw_rate_rad_per_s: float
    primary_energy_j: float
    recovered_energy_j: float
    completed_laps: int
    contacts: tuple[ContactRuntimeState, ...]
    components: tuple[ComponentHealthState, ...]
    status: str = "running"

    def __post_init__(self) -> None:
        _nonnegative("time_s", self.time_s)
        _nonnegative("race_distance_m", self.race_distance_m)
        _vector3("position_m", self.position_m)
        _vector3("velocity_mps", self.velocity_mps)
        _finite("yaw_rad", self.yaw_rad)
        _finite("yaw_rate_rad_per_s", self.yaw_rate_rad_per_s)
        _nonnegative("primary_energy_j", self.primary_energy_j)
        _nonnegative("recovered_energy_j", self.recovered_energy_j)
        if (
            not isinstance(self.completed_laps, int)
            or isinstance(self.completed_laps, bool)
            or self.completed_laps < 0
        ):
            raise CouplingContractError(
                "completed_laps must be a non-negative integer"
            )
        if not self.contacts:
            raise CouplingContractError("shared state must contain at least one contact")
        contact_ids = tuple(item.contact_id for item in self.contacts)
        if len(contact_ids) != len(set(contact_ids)):
            raise CouplingContractError("contact state IDs must be unique")
        component_ids = tuple(item.component_id for item in self.components)
        if len(component_ids) != len(set(component_ids)):
            raise CouplingContractError("component state IDs must be unique")
        allowed_status = {
            "running",
            "finished",
            "failed",
            "depleted",
            "timeout",
            "invalid",
        }
        if self.status not in allowed_status:
            raise CouplingContractError(f"unsupported shared-state status {self.status!r}")


@dataclass(frozen=True, slots=True)
class ResidualEntry:
    residual_id: str
    quantity: str
    value: float
    unit: str
    absolute_tolerance: float
    relative_tolerance: float
    scale: float

    def __post_init__(self) -> None:
        _nonblank("residual_id", self.residual_id)
        if self.quantity not in RESIDUAL_UNITS:
            raise CouplingContractError(
                f"unsupported residual quantity {self.quantity!r}"
            )
        expected_unit = RESIDUAL_UNITS[self.quantity]
        if self.unit != expected_unit:
            raise CouplingContractError(
                f"{self.quantity} residual unit must be {expected_unit!r}"
            )
        _finite("residual value", self.value)
        _nonnegative("absolute_tolerance", self.absolute_tolerance)
        _nonnegative("relative_tolerance", self.relative_tolerance)
        _nonnegative("residual scale", self.scale)
        if self.relative_tolerance > 1.0e-6:
            raise CouplingContractError("relative_tolerance must be <= 1e-6")

    @property
    def tolerance(self) -> float:
        return self.absolute_tolerance + self.relative_tolerance * self.scale

    @property
    def passed(self) -> bool:
        return abs(self.value) <= self.tolerance


@dataclass(frozen=True, slots=True)
class ResidualLedger:
    entries: tuple[ResidualEntry, ...]

    def __post_init__(self) -> None:
        if not self.entries:
            raise CouplingContractError("residual ledger must not be empty")
        identities = tuple(entry.residual_id for entry in self.entries)
        if len(identities) != len(set(identities)):
            raise CouplingContractError("residual IDs must be unique")

    @property
    def failed_residual_ids(self) -> tuple[str, ...]:
        return tuple(
            sorted(entry.residual_id for entry in self.entries if not entry.passed)
        )

    @property
    def status(self) -> str:
        return "passed" if not self.failed_residual_ids else "invalid"


@dataclass(frozen=True, slots=True)
class EventCandidate:
    event_id: str
    event_type: str
    time_s: float
    source_module_id: str

    def __post_init__(self) -> None:
        _nonblank("event_id", self.event_id)
        if self.event_type not in EVENT_PRIORITY:
            raise CouplingContractError(f"unsupported event_type {self.event_type!r}")
        _nonnegative("event time_s", self.time_s)
        _nonblank("source_module_id", self.source_module_id)


@dataclass(frozen=True, slots=True)
class EventDecision:
    winner: EventCandidate
    earliest_time_s: float
    tied_candidate_ids: tuple[str, ...]
    time_tolerance_s: float


def arbitrate_event_candidates(
    candidates: tuple[EventCandidate, ...], *, time_tolerance_s: float = 1.0e-12
) -> EventDecision:
    """Select the earliest event and use declared priority for tolerance ties."""

    if not candidates:
        raise CouplingContractError("event candidates must not be empty")
    _nonnegative("time_tolerance_s", time_tolerance_s)
    event_ids = tuple(candidate.event_id for candidate in candidates)
    if len(event_ids) != len(set(event_ids)):
        raise CouplingContractError("event candidate IDs must be unique")
    earliest_time_s = min(candidate.time_s for candidate in candidates)
    tied = tuple(
        candidate
        for candidate in candidates
        if abs(candidate.time_s - earliest_time_s) <= time_tolerance_s
    )
    winner = min(
        tied,
        key=lambda candidate: (
            EVENT_PRIORITY[candidate.event_type],
            candidate.event_id,
        ),
    )
    return EventDecision(
        winner=winner,
        earliest_time_s=earliest_time_s,
        tied_candidate_ids=tuple(sorted(candidate.event_id for candidate in tied)),
        time_tolerance_s=time_tolerance_s,
    )
