"""Independent interval-energy audit for a compiled component graph."""

from __future__ import annotations

from dataclasses import dataclass
import math

from .energy_graph import CompiledEnergyGraph


class EnergyAuditInputError(ValueError):
    """Raised when audit evidence values violate the SI contract."""


def _finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise EnergyAuditInputError(f"{name} must be finite; received {value!r}")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise EnergyAuditInputError(f"{name} must be >= 0; received {value!r}")


@dataclass(frozen=True, slots=True)
class EnergyAuditTolerance:
    absolute_j: float = 1.0e-9
    relative: float = 1.0e-12

    def __post_init__(self) -> None:
        _nonnegative("absolute_j", self.absolute_j)
        _nonnegative("relative", self.relative)
        if self.relative > 1.0e-3:
            raise EnergyAuditInputError("relative tolerance must be <= 1e-3")


@dataclass(frozen=True, slots=True)
class ComponentEnergyBalance:
    component_id: str
    energy_in_j: float
    energy_out_j: float
    declared_loss_j: float
    stored_energy_change_j: float

    def __post_init__(self) -> None:
        if not self.component_id.strip():
            raise EnergyAuditInputError("component_id must not be blank")
        _nonnegative("energy_in_j", self.energy_in_j)
        _nonnegative("energy_out_j", self.energy_out_j)
        _nonnegative("declared_loss_j", self.declared_loss_j)
        _finite("stored_energy_change_j", self.stored_energy_change_j)


@dataclass(frozen=True, slots=True)
class ConnectionEnergyTransfer:
    connection_id: str
    source_component_id: str
    target_component_id: str
    energy_j: float

    def __post_init__(self) -> None:
        for name, value in (
            ("connection_id", self.connection_id),
            ("source_component_id", self.source_component_id),
            ("target_component_id", self.target_component_id),
        ):
            if not value.strip():
                raise EnergyAuditInputError(f"{name} must not be blank")
        _nonnegative("energy_j", self.energy_j)


@dataclass(frozen=True, slots=True)
class ComponentEnergyAudit:
    component_id: str
    balance_residual_j: float
    input_interface_residual_j: float
    output_interface_residual_j: float
    tolerance_j: float
    status: str


@dataclass(frozen=True, slots=True)
class EnergyAuditResult:
    graph_id: str
    status: str
    total_balance_residual_j: float
    component_audits: tuple[ComponentEnergyAudit, ...]
    violations: tuple[str, ...]


def audit_energy_conservation(
    *,
    graph: CompiledEnergyGraph,
    balances: tuple[ComponentEnergyBalance, ...],
    transfers: tuple[ConnectionEnergyTransfer, ...],
    tolerance: EnergyAuditTolerance = EnergyAuditTolerance(),
) -> EnergyAuditResult:
    """Audit declared energy without correcting residuals or missing evidence."""

    violations: list[str] = []
    balance_by_id: dict[str, ComponentEnergyBalance] = {}
    for balance in balances:
        if balance.component_id in balance_by_id:
            violations.append(f"duplicate balance for component {balance.component_id!r}")
        else:
            balance_by_id[balance.component_id] = balance
    transfer_by_id: dict[str, ConnectionEnergyTransfer] = {}
    for transfer in transfers:
        if transfer.connection_id in transfer_by_id:
            violations.append(f"duplicate transfer for connection {transfer.connection_id!r}")
        else:
            transfer_by_id[transfer.connection_id] = transfer

    expected_components = set(graph.component_order)
    supplied_components = set(balance_by_id)
    for component_id in sorted(expected_components - supplied_components):
        violations.append(f"missing balance for component {component_id!r}")
    for component_id in sorted(supplied_components - expected_components):
        violations.append(f"extra balance for component {component_id!r}")

    expected_connections = {item.connection_id: item for item in graph.connections}
    supplied_connections = set(transfer_by_id)
    for connection_id in sorted(set(expected_connections) - supplied_connections):
        violations.append(f"missing transfer for connection {connection_id!r}")
    for connection_id in sorted(supplied_connections - set(expected_connections)):
        violations.append(f"extra transfer for connection {connection_id!r}")

    incoming = {component_id: 0.0 for component_id in expected_components}
    outgoing = {component_id: 0.0 for component_id in expected_components}
    for connection_id, expected in sorted(expected_connections.items()):
        transfer = transfer_by_id.get(connection_id)
        if transfer is None:
            continue
        if (
            transfer.source_component_id != expected.source_component_id
            or transfer.target_component_id != expected.target_component_id
        ):
            violations.append(
                f"endpoint mismatch for connection {connection_id!r}: "
                f"{transfer.source_component_id!r}->{transfer.target_component_id!r}"
            )
            continue
        outgoing[expected.source_component_id] += transfer.energy_j
        incoming[expected.target_component_id] += transfer.energy_j

    component_audits: list[ComponentEnergyAudit] = []
    total_residual_j = 0.0
    for component_id in graph.component_order:
        balance = balance_by_id.get(component_id)
        if balance is None:
            continue
        balance_residual_j = (
            balance.energy_in_j
            - balance.energy_out_j
            - balance.declared_loss_j
            - balance.stored_energy_change_j
        )
        input_residual_j = balance.energy_in_j - incoming[component_id]
        output_residual_j = balance.energy_out_j - outgoing[component_id]
        scale_j = max(
            balance.energy_in_j,
            balance.energy_out_j,
            balance.declared_loss_j,
            abs(balance.stored_energy_change_j),
            incoming[component_id],
            outgoing[component_id],
        )
        tolerance_j = tolerance.absolute_j + tolerance.relative * scale_j
        residuals = (balance_residual_j, input_residual_j, output_residual_j)
        valid = all(abs(value) <= tolerance_j for value in residuals)
        if not valid:
            if abs(balance_residual_j) > tolerance_j:
                violations.append(
                    f"component {component_id!r} balance residual {balance_residual_j!r} J exceeds {tolerance_j!r} J"
                )
            if abs(input_residual_j) > tolerance_j:
                violations.append(
                    f"component {component_id!r} input interface residual {input_residual_j!r} J exceeds {tolerance_j!r} J"
                )
            if abs(output_residual_j) > tolerance_j:
                violations.append(
                    f"component {component_id!r} output interface residual {output_residual_j!r} J exceeds {tolerance_j!r} J"
                )
        component_audits.append(
            ComponentEnergyAudit(
                component_id,
                balance_residual_j,
                input_residual_j,
                output_residual_j,
                tolerance_j,
                "valid" if valid else "invalid",
            )
        )
        total_residual_j += balance_residual_j

    return EnergyAuditResult(
        graph_id=graph.graph_id,
        status="valid" if not violations else "invalid",
        total_balance_residual_j=total_residual_j,
        component_audits=tuple(component_audits),
        violations=tuple(violations),
    )
