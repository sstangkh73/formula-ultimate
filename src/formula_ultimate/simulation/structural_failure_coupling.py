"""Work 046 deterministic structural connection failure coupling policy."""

from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json
import math
import re
from typing import Any, Mapping, Sequence

from .coupling import EventCandidate, ResidualEntry


class StructuralFailureCouplingError(ValueError):
    """Raised when bounded structural-coupling evidence is inadmissible."""


_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ZERO_WRENCH = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
_MECHANISM_PRIORITY = {"fracture": 0, "fatigue": 1, "yield": 2}


def _text(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise StructuralFailureCouplingError(f"{name} must not be blank")


def _finite(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise StructuralFailureCouplingError(f"{name} must be finite")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise StructuralFailureCouplingError(f"{name} must be non-negative")


def _wrench(name: str, value: tuple[float, ...]) -> None:
    if not isinstance(value, tuple) or len(value) != 6:
        raise StructuralFailureCouplingError(f"{name} must contain six components")
    for index, component in enumerate(value):
        _finite(f"{name}[{index}]", component)


@dataclass(frozen=True, slots=True)
class GateAIdentity:
    remediation_protocol_id: str
    decision: str
    element_route_id: str
    support_topology_sha256: str
    boundary_model_id: str

    def __post_init__(self) -> None:
        for name in ("remediation_protocol_id", "decision", "element_route_id", "boundary_model_id"):
            _text(name, getattr(self, name))
        if not _SHA256.fullmatch(self.support_topology_sha256):
            raise StructuralFailureCouplingError("support topology SHA-256 is invalid")


@dataclass(frozen=True, slots=True)
class ConnectionDefinition:
    connection_id: str
    load_path_id: str
    share_weight: float

    def __post_init__(self) -> None:
        _text("connection_id", self.connection_id)
        _text("load_path_id", self.load_path_id)
        _finite("share_weight", self.share_weight)
        if self.share_weight <= 0.0:
            raise StructuralFailureCouplingError("share_weight must be positive")


@dataclass(frozen=True, slots=True)
class ConnectionState:
    connection_id: str
    health_state: str
    transmitted_wrench: tuple[float, float, float, float, float, float]
    stored_elastic_energy_j: float

    def __post_init__(self) -> None:
        _text("connection_id", self.connection_id)
        if self.health_state not in {"intact", "degraded", "failed"}:
            raise StructuralFailureCouplingError("connection health state is invalid")
        _wrench("transmitted_wrench", self.transmitted_wrench)
        _nonnegative("stored_elastic_energy_j", self.stored_elastic_energy_j)
        if self.health_state == "failed" and self.transmitted_wrench != _ZERO_WRENCH:
            raise StructuralFailureCouplingError("failed connection must transmit a zero wrench")


@dataclass(frozen=True, slots=True)
class StructuralNetworkState:
    time_s: float
    load_path_id: str
    connections: tuple[ConnectionState, ...]
    status: str = "running"

    def __post_init__(self) -> None:
        _nonnegative("time_s", self.time_s)
        _text("load_path_id", self.load_path_id)
        if not self.connections:
            raise StructuralFailureCouplingError("network must contain connections")
        ids = tuple(item.connection_id for item in self.connections)
        if len(ids) != len(set(ids)):
            raise StructuralFailureCouplingError("connection state IDs are duplicated")
        if self.status not in {"running", "DNF"}:
            raise StructuralFailureCouplingError("network status is invalid")


@dataclass(frozen=True, slots=True)
class FailureEvidence:
    evidence_id: str
    connection_id: str
    mechanism: str
    crossing_time_s: float
    upstream_protocol_id: str
    artifact_sha256: str
    dissipated_fraction: float

    def __post_init__(self) -> None:
        _text("evidence_id", self.evidence_id)
        _text("connection_id", self.connection_id)
        if self.mechanism not in _MECHANISM_PRIORITY:
            raise StructuralFailureCouplingError("unsupported structural failure mechanism")
        _nonnegative("crossing_time_s", self.crossing_time_s)
        _text("upstream_protocol_id", self.upstream_protocol_id)
        if not _SHA256.fullmatch(self.artifact_sha256):
            raise StructuralFailureCouplingError("failure evidence SHA-256 is invalid")
        _finite("dissipated_fraction", self.dissipated_fraction)
        if not 0.0 <= self.dissipated_fraction <= 1.0:
            raise StructuralFailureCouplingError("dissipated_fraction must lie in [0,1]")
        if self.mechanism == "yield" and self.dissipated_fraction != 0.0:
            raise StructuralFailureCouplingError("yield transition does not admit failure-energy partition")


@dataclass(frozen=True, slots=True)
class FailureEnergyLedger:
    stored_energy_j: float
    dissipated_energy_j: float
    released_energy_j: float
    residual_j: float


@dataclass(frozen=True, slots=True)
class StructuralTransition:
    time_s: float
    evidence_ids: tuple[str, ...]
    connection_ids: tuple[str, ...]
    mechanisms: tuple[str, ...]
    target_states: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class StructuralCouplingResult:
    status: str
    reason: str
    outcome: str
    candidate_state: StructuralNetworkState | None
    transition: StructuralTransition | None
    race_event: EventCandidate | None
    energy_ledger: FailureEnergyLedger | None
    residuals: tuple[ResidualEntry, ...]


def initial_network_state(
    *,
    time_s: float,
    definitions: Sequence[ConnectionDefinition],
    stored_energy_by_connection_j: Mapping[str, float],
    applied_wrench: tuple[float, float, float, float, float, float],
) -> StructuralNetworkState:
    if not definitions:
        raise StructuralFailureCouplingError("connection definitions must not be empty")
    ids = tuple(item.connection_id for item in definitions)
    if len(ids) != len(set(ids)):
        raise StructuralFailureCouplingError("connection definition IDs are duplicated")
    paths = {item.load_path_id for item in definitions}
    if len(paths) != 1:
        raise StructuralFailureCouplingError("Work 046 admits exactly one load-path group")
    if set(stored_energy_by_connection_j) != set(ids):
        raise StructuralFailureCouplingError("stored-energy identities differ from connection definitions")
    _wrench("applied_wrench", applied_wrench)
    total_weight = math.fsum(item.share_weight for item in definitions)
    states = tuple(
        ConnectionState(
            item.connection_id,
            "intact",
            tuple(component * item.share_weight / total_weight for component in applied_wrench),  # type: ignore[arg-type]
            float(stored_energy_by_connection_j[item.connection_id]),
        )
        for item in definitions
    )
    return StructuralNetworkState(time_s, next(iter(paths)), states)


def _invalid(reason: str) -> StructuralCouplingResult:
    return StructuralCouplingResult("invalid", reason, "invalid", None, None, None, None, ())


def evaluate_structural_failure_step(
    *,
    state: StructuralNetworkState,
    duration_s: float,
    definitions: Sequence[ConnectionDefinition],
    applied_wrench: tuple[float, float, float, float, float, float],
    evidence: Sequence[FailureEvidence],
    gate_identity: GateAIdentity,
    expected_gate_identity: GateAIdentity,
    mechanism_protocols: Mapping[str, str],
    residual_relative_tolerance: float = 1.0e-6,
    event_time_absolute_tolerance_s: float = 1.0e-12,
) -> StructuralCouplingResult:
    """Advance to the earliest typed transition or to the requested step end."""

    try:
        _finite("duration_s", duration_s)
        if duration_s <= 0.0:
            raise StructuralFailureCouplingError("duration_s must be positive")
        _wrench("applied_wrench", applied_wrench)
        if gate_identity != expected_gate_identity or gate_identity.decision != "narrowly_bounded":
            raise StructuralFailureCouplingError("Gate A identity is outside the admitted Work 051 domain")
        if set(mechanism_protocols) != set(_MECHANISM_PRIORITY):
            raise StructuralFailureCouplingError("mechanism protocol mapping is incomplete")
        ids = tuple(item.connection_id for item in definitions)
        if len(ids) != len(set(ids)):
            raise StructuralFailureCouplingError("connection definition IDs are duplicated")
        if set(ids) != {item.connection_id for item in state.connections}:
            raise StructuralFailureCouplingError("definition/state connection identities differ")
        if {item.load_path_id for item in definitions} != {state.load_path_id}:
            raise StructuralFailureCouplingError("connection load-path identity differs from state")
        evidence_ids = tuple(item.evidence_id for item in evidence)
        if len(evidence_ids) != len(set(evidence_ids)):
            raise StructuralFailureCouplingError("failure evidence IDs are duplicated")
        for item in evidence:
            if item.connection_id not in set(ids):
                raise StructuralFailureCouplingError("failure evidence references an unknown connection")
            if mechanism_protocols[item.mechanism] != item.upstream_protocol_id:
                raise StructuralFailureCouplingError("failure evidence protocol identity is not admitted")
            if item.crossing_time_s < state.time_s - event_time_absolute_tolerance_s:
                raise StructuralFailureCouplingError("failure evidence crossing precedes the current state")
        end_time = state.time_s + duration_s
        admitted = tuple(
            item for item in evidence
            if item.crossing_time_s <= end_time + event_time_absolute_tolerance_s
        )
        transition_time = min((item.crossing_time_s for item in admitted), default=end_time)
        tied = tuple(
            item for item in admitted
            if abs(item.crossing_time_s - transition_time) <= event_time_absolute_tolerance_s
        )
        by_connection: dict[str, FailureEvidence] = {}
        for item in sorted(tied, key=lambda row: (_MECHANISM_PRIORITY[row.mechanism], row.evidence_id)):
            by_connection.setdefault(item.connection_id, item)
        chosen = tuple(sorted(by_connection.values(), key=lambda item: item.connection_id))
        definitions_by_id = {item.connection_id: item for item in definitions}
        states_by_id = {item.connection_id: item for item in state.connections}
        failed_energy: list[tuple[ConnectionState, FailureEvidence]] = []
        targets: list[str] = []
        for item in chosen:
            current = states_by_id[item.connection_id]
            target = "degraded" if item.mechanism == "yield" else "failed"
            if current.health_state == "failed":
                raise StructuralFailureCouplingError("failure evidence targets an already failed connection")
            if target == "degraded" and current.health_state == "degraded":
                raise StructuralFailureCouplingError("yield evidence targets an already degraded connection")
            targets.append(target)
            if target == "failed":
                failed_energy.append((current, item))
                states_by_id[item.connection_id] = replace(current, health_state="failed", transmitted_wrench=_ZERO_WRENCH)
            else:
                states_by_id[item.connection_id] = replace(current, health_state="degraded")

        active_ids = tuple(sorted(item for item, value in states_by_id.items() if value.health_state != "failed"))
        outcome = "running" if active_ids else "DNF"
        if active_ids:
            total_weight = math.fsum(definitions_by_id[item].share_weight for item in active_ids)
            for connection_id in active_ids:
                fraction = definitions_by_id[connection_id].share_weight / total_weight
                states_by_id[connection_id] = replace(
                    states_by_id[connection_id],
                    transmitted_wrench=tuple(component * fraction for component in applied_wrench),  # type: ignore[arg-type]
                )
        candidate = StructuralNetworkState(
            transition_time,
            state.load_path_id,
            tuple(states_by_id[item] for item in sorted(states_by_id)),
            outcome,
        )
        residuals: list[ResidualEntry] = [
            ResidualEntry(
                "structural.event-time", "time", candidate.time_s - transition_time, "s",
                event_time_absolute_tolerance_s, 0.0, max(1.0, transition_time),
            )
        ]
        if active_ids:
            summed = tuple(math.fsum(item.transmitted_wrench[index] for item in candidate.connections) for index in range(6))
            for index in range(3):
                residuals.append(ResidualEntry(
                    f"structural.force-{index}", "force", summed[index] - applied_wrench[index], "N",
                    1.0e-12, residual_relative_tolerance,
                    max(1.0, abs(applied_wrench[index])),
                ))
            for index in range(3, 6):
                residuals.append(ResidualEntry(
                    f"structural.moment-{index - 3}", "moment", summed[index] - applied_wrench[index], "N*m",
                    1.0e-12, residual_relative_tolerance,
                    max(1.0, abs(applied_wrench[index])),
                ))
        stored = math.fsum(item.stored_elastic_energy_j for item, _ in failed_energy)
        dissipated = math.fsum(item.stored_elastic_energy_j * event.dissipated_fraction for item, event in failed_energy)
        released = math.fsum(item.stored_elastic_energy_j * (1.0 - event.dissipated_fraction) for item, event in failed_energy)
        energy_residual = stored - dissipated - released
        ledger = FailureEnergyLedger(stored, dissipated, released, energy_residual)
        residuals.append(ResidualEntry(
            "structural.failure-energy", "energy", energy_residual, "J",
            1.0e-12, residual_relative_tolerance, max(1.0, stored),
        ))
        if any(not item.passed for item in residuals):
            return StructuralCouplingResult("invalid", "structural residual failed", "invalid", None, None, None, ledger, tuple(residuals))
        transition = None if not chosen else StructuralTransition(
            transition_time,
            tuple(item.evidence_id for item in chosen),
            tuple(item.connection_id for item in chosen),
            tuple(item.mechanism for item in chosen),
            tuple(targets),
        )
        race_event = None
        if failed_energy:
            race_event = EventCandidate(
                "structural." + "+".join(item.evidence_id for _, item in failed_energy),
                "structural_failure",
                transition_time,
                "structural_failure_coupling",
            )
        reason = "step completed without transition" if transition is None else "structural transition localized and coupled"
        return StructuralCouplingResult("ok", reason, outcome, candidate, transition, race_event, ledger, tuple(residuals))
    except (ArithmeticError, StructuralFailureCouplingError, ValueError) as exc:
        return _invalid(str(exc))


def structural_result_fingerprint(result: StructuralCouplingResult) -> str:
    def ready(value: Any) -> Any:
        if hasattr(value, "__dataclass_fields__"):
            return {name: ready(getattr(value, name)) for name in value.__dataclass_fields__}
        if isinstance(value, tuple):
            return [ready(item) for item in value]
        if isinstance(value, dict):
            return {str(key): ready(item) for key, item in value.items()}
        return value

    encoded = json.dumps(ready(result), sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
