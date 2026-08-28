"""Atomic execution boundary for one compiled coupled-vehicle step.

Work 022 deliberately executes generic adapters rather than domain physics.  It
guarantees declared reads/writes, deterministic order, private candidate state,
and all-or-nothing publication for later Work 023-027 adapters.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Callable, Protocol

from .coupling import (
    CompiledCouplingArchitecture,
    CoupledModuleSpec,
    EventCandidate,
    ResidualEntry,
    SharedVehicleState,
)


class CoupledTransactionError(ValueError):
    """Raised when a runtime adapter violates the Work 022 protocol."""


@dataclass(frozen=True, slots=True, init=False)
class RuntimeSignal:
    """A named payload copied on ingress and access.

    The private snapshot prevents ordinary adapter code from sharing mutable
    references across the transaction boundary.  This is a repository contract,
    not a sandbox for hostile Python code.
    """

    signal_id: str
    _payload_snapshot: object = field(repr=False)

    def __init__(self, signal_id: str, value: object) -> None:
        if not isinstance(signal_id, str) or not signal_id.strip():
            raise CoupledTransactionError("runtime signal_id must not be blank")
        object.__setattr__(self, "signal_id", signal_id)
        object.__setattr__(self, "_payload_snapshot", deepcopy(value))

    @property
    def value(self) -> object:
        return deepcopy(self._payload_snapshot)

    def _copy_payload(self) -> object:
        return deepcopy(self._payload_snapshot)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RuntimeSignal):
            return NotImplemented
        return (
            self.signal_id == other.signal_id
            and self._payload_snapshot == other._payload_snapshot
        )


@dataclass(frozen=True, slots=True)
class AdapterReadView:
    """Immutable, module-scoped view of declared input signals."""

    module_id: str
    start_state: SharedVehicleState
    _signals: tuple[RuntimeSignal, ...] = field(repr=False)

    def __post_init__(self) -> None:
        identities = tuple(signal.signal_id for signal in self._signals)
        if len(identities) != len(set(identities)):
            raise CoupledTransactionError("adapter read signal IDs must be unique")

    @property
    def signal_ids(self) -> tuple[str, ...]:
        return tuple(sorted(signal.signal_id for signal in self._signals))

    def read(self, signal_id: str) -> object:
        for signal in self._signals:
            if signal.signal_id == signal_id:
                return signal._copy_payload()
        raise CoupledTransactionError(
            f"module {self.module_id!r} attempted undeclared read {signal_id!r}"
        )


@dataclass(frozen=True, slots=True)
class AdapterOutput:
    """One adapter's complete candidate write set and evidence."""

    module_id: str
    status: str
    signals: tuple[RuntimeSignal, ...]
    residuals: tuple[ResidualEntry, ...] = ()
    events: tuple[EventCandidate, ...] = ()
    reason: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, str) or not self.module_id.strip():
            raise CoupledTransactionError("adapter output module_id must not be blank")
        if self.status not in {"ok", "invalid"}:
            raise CoupledTransactionError(
                f"unsupported adapter output status {self.status!r}"
            )
        if self.status == "invalid":
            if not isinstance(self.reason, str) or not self.reason.strip():
                raise CoupledTransactionError("invalid adapter output requires reason")
        elif self.reason is not None:
            raise CoupledTransactionError("successful adapter output cannot have reason")
        signal_ids = tuple(signal.signal_id for signal in self.signals)
        if len(signal_ids) != len(set(signal_ids)):
            raise CoupledTransactionError("adapter output signal IDs must be unique")
        residual_ids = tuple(item.residual_id for item in self.residuals)
        if len(residual_ids) != len(set(residual_ids)):
            raise CoupledTransactionError("adapter residual IDs must be unique")
        event_ids = tuple(item.event_id for item in self.events)
        if len(event_ids) != len(set(event_ids)):
            raise CoupledTransactionError("adapter event IDs must be unique")


class CoupledAdapter(Protocol):
    module_id: str
    model_version: str

    def execute(self, view: AdapterReadView) -> AdapterOutput:
        """Return one complete candidate output without external mutation."""


@dataclass(frozen=True, slots=True)
class FunctionCoupledAdapter:
    """Small deterministic adapter wrapper used by validators and domain bridges."""

    module_id: str
    model_version: str
    function: Callable[[AdapterReadView], AdapterOutput] = field(
        repr=False, compare=False
    )

    def __post_init__(self) -> None:
        for name, value in (
            ("module_id", self.module_id),
            ("model_version", self.model_version),
        ):
            if not isinstance(value, str) or not value.strip():
                raise CoupledTransactionError(f"adapter {name} must not be blank")
        if not callable(self.function):
            raise CoupledTransactionError("adapter function must be callable")

    def execute(self, view: AdapterReadView) -> AdapterOutput:
        return self.function(view)


@dataclass(frozen=True, slots=True)
class AdapterTrace:
    module_id: str
    stage: str
    status: str
    read_signal_ids: tuple[str, ...]
    written_signal_ids: tuple[str, ...]
    residual_ids: tuple[str, ...]
    event_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TransactionFailure:
    code: str
    reason: str
    module_id: str | None = None


@dataclass(frozen=True, slots=True)
class CoupledStepResult:
    status: str
    architecture_fingerprint_sha256: str
    start_state: SharedVehicleState
    committed_state: SharedVehicleState | None
    published_signals: tuple[RuntimeSignal, ...]
    traces: tuple[AdapterTrace, ...]
    residuals: tuple[ResidualEntry, ...]
    events: tuple[EventCandidate, ...]
    failure: TransactionFailure | None

    def __post_init__(self) -> None:
        if self.status not in {"committed", "invalid"}:
            raise CoupledTransactionError(f"unsupported step status {self.status!r}")
        residual_ids = tuple(item.residual_id for item in self.residuals)
        if len(residual_ids) != len(set(residual_ids)):
            raise CoupledTransactionError("step residual IDs must be unique")
        event_ids = tuple(item.event_id for item in self.events)
        if len(event_ids) != len(set(event_ids)):
            raise CoupledTransactionError("step event IDs must be unique")
        if self.status == "committed":
            if self.committed_state is None or self.failure is not None:
                raise CoupledTransactionError(
                    "committed result requires state and forbids failure"
                )
        else:
            if self.committed_state is not None or self.failure is None:
                raise CoupledTransactionError(
                    "invalid result requires failure and forbids committed state"
                )
            if self.published_signals:
                raise CoupledTransactionError(
                    "invalid result cannot publish candidate signals"
                )

    @property
    def rolled_back_state(self) -> SharedVehicleState:
        """The exact immutable start state retained on invalidity."""

        return self.start_state

    def read_published(self, signal_id: str) -> object:
        for signal in self.published_signals:
            if signal.signal_id == signal_id:
                return signal._copy_payload()
        raise CoupledTransactionError(f"published signal {signal_id!r} not found")


def _invalid_result(
    architecture: CompiledCouplingArchitecture,
    start_state: SharedVehicleState,
    *,
    code: str,
    reason: str,
    module_id: str | None = None,
    traces: tuple[AdapterTrace, ...] = (),
    residuals: tuple[ResidualEntry, ...] = (),
    events: tuple[EventCandidate, ...] = (),
) -> CoupledStepResult:
    return CoupledStepResult(
        status="invalid",
        architecture_fingerprint_sha256=architecture.fingerprint_sha256,
        start_state=start_state,
        committed_state=None,
        published_signals=(),
        traces=traces,
        residuals=residuals,
        events=events,
        failure=TransactionFailure(code=code, reason=reason, module_id=module_id),
    )


def _exact_coverage(name: str, actual: tuple[str, ...], expected: tuple[str, ...]) -> str | None:
    duplicates = sorted({item for item in actual if actual.count(item) > 1})
    if duplicates:
        return f"{name} contains duplicate IDs {duplicates!r}"
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    if missing or extra:
        return f"{name} coverage mismatch; missing={missing!r}, extra={extra!r}"
    return None


def execute_coupled_step(
    *,
    architecture: CompiledCouplingArchitecture,
    start_state: SharedVehicleState,
    initial_signals: tuple[RuntimeSignal, ...],
    adapters: tuple[CoupledAdapter, ...],
    current_state_signal_id: str = "manifest.current_state",
    next_state_signal_id: str = "state.next",
) -> CoupledStepResult:
    """Execute one architecture as an all-or-nothing transaction.

    Preflight faults and adapter faults are represented as invalid results.  No
    candidate output is published until every adapter and the final-state checks
    pass.
    """

    initial_ids = tuple(signal.signal_id for signal in initial_signals)
    coverage_error = _exact_coverage(
        "initial signal", initial_ids, architecture.initial_signals
    )
    if coverage_error:
        return _invalid_result(
            architecture, start_state, code="initial_signal_coverage", reason=coverage_error
        )

    initial_by_id = {signal.signal_id: signal for signal in initial_signals}
    if current_state_signal_id not in initial_by_id:
        return _invalid_result(
            architecture,
            start_state,
            code="current_state_signal_missing",
            reason=f"current state signal {current_state_signal_id!r} is absent",
        )
    declared_start = initial_by_id[current_state_signal_id]._copy_payload()
    if not isinstance(declared_start, SharedVehicleState) or declared_start != start_state:
        return _invalid_result(
            architecture,
            start_state,
            code="current_state_mismatch",
            reason="current state signal must equal the transaction start_state",
        )

    adapter_ids = tuple(getattr(adapter, "module_id", "") for adapter in adapters)
    expected_adapter_ids = tuple(
        module.module_id for module in architecture.ordered_modules
    )
    coverage_error = _exact_coverage("adapter", adapter_ids, expected_adapter_ids)
    if coverage_error:
        return _invalid_result(
            architecture, start_state, code="adapter_coverage", reason=coverage_error
        )
    adapter_by_id = {adapter.module_id: adapter for adapter in adapters}
    for module in architecture.ordered_modules:
        adapter = adapter_by_id[module.module_id]
        if getattr(adapter, "model_version", None) != module.model_version:
            return _invalid_result(
                architecture,
                start_state,
                code="adapter_version_mismatch",
                module_id=module.module_id,
                reason=(
                    f"adapter model_version {getattr(adapter, 'model_version', None)!r} "
                    f"does not match {module.model_version!r}"
                ),
            )

    candidate_bus = {
        signal.signal_id: RuntimeSignal(signal.signal_id, signal._copy_payload())
        for signal in initial_signals
    }
    candidate_outputs: dict[str, RuntimeSignal] = {}
    traces: list[AdapterTrace] = []
    retained_residuals: list[ResidualEntry] = []
    retained_events: list[EventCandidate] = []

    for module in architecture.ordered_modules:
        adapter = adapter_by_id[module.module_id]
        read_signals = tuple(candidate_bus[signal] for signal in module.consumes)
        view = AdapterReadView(
            module_id=module.module_id,
            start_state=start_state,
            _signals=read_signals,
        )
        try:
            output = adapter.execute(view)
            if not isinstance(output, AdapterOutput):
                raise CoupledTransactionError("adapter must return AdapterOutput")
            if output.module_id != module.module_id:
                raise CoupledTransactionError(
                    f"adapter returned module_id {output.module_id!r}; "
                    f"expected {module.module_id!r}"
                )
            output_ids = tuple(signal.signal_id for signal in output.signals)
            if output.status == "invalid":
                if output_ids:
                    raise CoupledTransactionError(
                        "invalid adapter output cannot contain candidate writes"
                    )
            else:
                output_error = _exact_coverage(
                    "adapter output", output_ids, module.produces
                )
                if output_error:
                    raise CoupledTransactionError(output_error)
        except Exception as exc:
            return _invalid_result(
                architecture,
                start_state,
                code="adapter_exception",
                module_id=module.module_id,
                reason=f"{type(exc).__name__}: {exc}",
                traces=tuple(traces),
                residuals=tuple(retained_residuals),
                events=tuple(retained_events),
            )

        trace = AdapterTrace(
            module_id=module.module_id,
            stage=module.stage,
            status=output.status,
            read_signal_ids=view.signal_ids,
            written_signal_ids=tuple(sorted(signal.signal_id for signal in output.signals)),
            residual_ids=tuple(sorted(item.residual_id for item in output.residuals)),
            event_ids=tuple(sorted(item.event_id for item in output.events)),
        )
        traces.append(trace)
        duplicate_residuals = sorted(
            {item.residual_id for item in retained_residuals}
            & {item.residual_id for item in output.residuals}
        )
        duplicate_events = sorted(
            {item.event_id for item in retained_events}
            & {item.event_id for item in output.events}
        )
        if duplicate_residuals or duplicate_events:
            return _invalid_result(
                architecture,
                start_state,
                code="evidence_identity_duplicate",
                module_id=module.module_id,
                reason=(
                    f"duplicate residual IDs={duplicate_residuals!r}; "
                    f"duplicate event IDs={duplicate_events!r}"
                ),
                traces=tuple(traces),
                residuals=tuple(retained_residuals),
                events=tuple(retained_events),
            )
        retained_residuals.extend(output.residuals)
        retained_events.extend(output.events)
        if output.status == "invalid":
            return _invalid_result(
                architecture,
                start_state,
                code="adapter_invalid",
                module_id=module.module_id,
                reason=output.reason or "adapter returned invalid",
                traces=tuple(traces),
                residuals=tuple(retained_residuals),
                events=tuple(retained_events),
            )
        failed_residuals = tuple(
            sorted(item.residual_id for item in output.residuals if not item.passed)
        )
        if failed_residuals:
            return _invalid_result(
                architecture,
                start_state,
                code="residual_failure",
                module_id=module.module_id,
                reason=f"failed residuals {failed_residuals!r}",
                traces=tuple(traces),
                residuals=tuple(retained_residuals),
                events=tuple(retained_events),
            )
        for signal in output.signals:
            stored = RuntimeSignal(signal.signal_id, signal._copy_payload())
            candidate_bus[signal.signal_id] = stored
            candidate_outputs[signal.signal_id] = stored

    if next_state_signal_id not in candidate_outputs:
        return _invalid_result(
            architecture,
            start_state,
            code="next_state_missing",
            reason=f"next state output {next_state_signal_id!r} is absent",
            traces=tuple(traces),
            residuals=tuple(retained_residuals),
            events=tuple(retained_events),
        )
    next_state = candidate_outputs[next_state_signal_id]._copy_payload()
    if not isinstance(next_state, SharedVehicleState):
        return _invalid_result(
            architecture,
            start_state,
            code="next_state_type",
            reason="state.next must contain SharedVehicleState",
            traces=tuple(traces),
            residuals=tuple(retained_residuals),
            events=tuple(retained_events),
        )
    if next_state.time_s < start_state.time_s:
        return _invalid_result(
            architecture,
            start_state,
            code="time_regression",
            reason="state.next time_s must not regress",
            traces=tuple(traces),
            residuals=tuple(retained_residuals),
            events=tuple(retained_events),
        )
    if next_state.race_distance_m < start_state.race_distance_m:
        return _invalid_result(
            architecture,
            start_state,
            code="distance_regression",
            reason="state.next race_distance_m must not regress",
            traces=tuple(traces),
            residuals=tuple(retained_residuals),
            events=tuple(retained_events),
        )

    published = tuple(
        RuntimeSignal(signal_id, signal._copy_payload())
        for signal_id, signal in sorted(candidate_outputs.items())
    )
    return CoupledStepResult(
        status="committed",
        architecture_fingerprint_sha256=architecture.fingerprint_sha256,
        start_state=start_state,
        committed_state=next_state,
        published_signals=published,
        traces=tuple(traces),
        residuals=tuple(retained_residuals),
        events=tuple(retained_events),
        failure=None,
    )
