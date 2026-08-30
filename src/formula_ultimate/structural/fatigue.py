"""Deterministic rainflow and Miner damage contracts for Work 044."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
import hashlib
import json
import math
from typing import Any, Iterable, Mapping

from .acceptance import StructuralEvidenceError


getcontext().prec = 34


@dataclass(frozen=True, slots=True)
class FatigueMaterialRecord:
    record_id: str
    reference_alternating_stress_pa: float
    reference_cycles: float
    basquin_exponent: float
    minimum_corrected_stress_pa: float
    maximum_corrected_stress_pa: float
    ultimate_stress_pa: float
    life_scatter_factor: float
    provenance: str
    design_use_permitted: bool

    def __post_init__(self) -> None:
        if not self.record_id.strip() or not self.provenance.strip():
            raise StructuralEvidenceError("fatigue curve identity and provenance are required")
        for name, value in (
            ("reference_alternating_stress_pa", self.reference_alternating_stress_pa),
            ("reference_cycles", self.reference_cycles), ("basquin_exponent", self.basquin_exponent),
            ("minimum_corrected_stress_pa", self.minimum_corrected_stress_pa),
            ("maximum_corrected_stress_pa", self.maximum_corrected_stress_pa),
            ("ultimate_stress_pa", self.ultimate_stress_pa), ("life_scatter_factor", self.life_scatter_factor),
        ):
            if not math.isfinite(value) or value <= 0.0:
                raise StructuralEvidenceError(f"{name} must be finite and > 0")
        if self.minimum_corrected_stress_pa >= self.maximum_corrected_stress_pa:
            raise StructuralEvidenceError("fatigue corrected-stress domain is empty")
        if self.maximum_corrected_stress_pa >= self.ultimate_stress_pa:
            raise StructuralEvidenceError("fatigue domain must remain below ultimate stress")
        if self.life_scatter_factor < 1.0:
            raise StructuralEvidenceError("life_scatter_factor must be >= 1")
        if self.design_use_permitted:
            raise StructuralEvidenceError("synthetic fatigue record cannot enter design fitness")


@dataclass(frozen=True, slots=True)
class RainflowCycle:
    range_pa: float
    mean_pa: float
    count: float

    @property
    def alternating_stress_pa(self) -> float:
        return self.range_pa / 2.0


@dataclass(frozen=True, slots=True)
class DamageLedgerEntry:
    block_id: str
    alternating_stress_pa: float
    mean_stress_pa: float
    corrected_alternating_stress_pa: float
    counted_cycles: float
    cycles_to_failure: float
    damage_increment: str
    cumulative_damage: str
    life_interval_cycles: tuple[float, float]


@dataclass(frozen=True, slots=True)
class FatigueDamageResult:
    ledger: tuple[DamageLedgerEntry, ...]
    cumulative_damage: str
    failed: bool
    event_cycle: float | None
    event_id: str | None


def fatigue_material_from_mapping(value: Mapping[str, Any]) -> FatigueMaterialRecord:
    try:
        if value["curve"] != "synthetic_basquin_stress_life" or value["mean_stress_rule"] != "goodman":
            raise StructuralEvidenceError("unsupported fatigue curve or mean-stress rule")
        return FatigueMaterialRecord(
            str(value["record_id"]), float(value["reference_alternating_stress_pa"]),
            float(value["reference_cycles"]), float(value["basquin_exponent"]),
            float(value["minimum_corrected_stress_pa"]), float(value["maximum_corrected_stress_pa"]),
            float(value["ultimate_stress_pa"]), float(value["life_scatter_factor"]),
            str(value["provenance"]), bool(value["design_use_permitted"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, StructuralEvidenceError):
            raise
        raise StructuralEvidenceError(f"malformed fatigue material record: {exc}") from exc


def reversal_history(low_pa: float, high_pa: float, cycles: int) -> tuple[float, ...]:
    if not (math.isfinite(low_pa) and math.isfinite(high_pa) and low_pa < high_pa):
        raise StructuralEvidenceError("fatigue reversal bounds must be finite and increasing")
    if cycles <= 0:
        raise StructuralEvidenceError("fatigue cycle count must be positive")
    values = [low_pa]
    for _ in range(cycles):
        values.extend((high_pa, low_pa))
    return tuple(values)


def rainflow_cycles(reversals_pa: Iterable[float]) -> tuple[RainflowCycle, ...]:
    points = tuple(float(value) for value in reversals_pa)
    if len(points) < 2 or not all(math.isfinite(value) for value in points):
        raise StructuralEvidenceError("rainflow history requires finite reversal points")
    if any(left == right for left, right in zip(points, points[1:])):
        raise StructuralEvidenceError("rainflow reversal history contains adjacent duplicates")
    stack: list[float] = []
    counted: list[RainflowCycle] = []
    for point in points:
        stack.append(point)
        while len(stack) >= 3:
            older_range = abs(stack[-2] - stack[-3])
            newer_range = abs(stack[-1] - stack[-2])
            if newer_range < older_range:
                break
            mean = 0.5 * (stack[-3] + stack[-2])
            if len(stack) == 3:
                counted.append(RainflowCycle(older_range, mean, 0.5))
                del stack[-3]
            else:
                counted.append(RainflowCycle(older_range, mean, 1.0))
                del stack[-3:-1]
    for left, right in zip(stack, stack[1:]):
        counted.append(RainflowCycle(abs(right - left), 0.5 * (left + right), 0.5))
    if not counted or any(cycle.range_pa <= 0.0 for cycle in counted):
        raise StructuralEvidenceError("rainflow counter produced no positive cycle range")
    return tuple(counted)


def aggregate_cycles(cycles: Iterable[RainflowCycle]) -> tuple[RainflowCycle, ...]:
    totals: dict[tuple[float, float], float] = {}
    order: list[tuple[float, float]] = []
    for cycle in cycles:
        key = (cycle.range_pa, cycle.mean_pa)
        if key not in totals:
            totals[key] = 0.0
            order.append(key)
        totals[key] += cycle.count
    return tuple(RainflowCycle(key[0], key[1], totals[key]) for key in order)


def corrected_amplitude_goodman(record: FatigueMaterialRecord, cycle: RainflowCycle) -> float:
    denominator = 1.0 - cycle.mean_pa / record.ultimate_stress_pa
    if denominator <= 0.0:
        raise StructuralEvidenceError("mean stress reaches or exceeds ultimate stress")
    corrected = cycle.alternating_stress_pa / denominator
    if corrected < record.minimum_corrected_stress_pa:
        raise StructuralEvidenceError("corrected alternating stress is below fatigue curve domain")
    if corrected > record.maximum_corrected_stress_pa:
        raise StructuralEvidenceError("corrected alternating stress is above fatigue curve domain")
    return corrected


def cycles_to_failure(record: FatigueMaterialRecord, corrected_stress_pa: float) -> float:
    life = record.reference_cycles * (corrected_stress_pa / record.reference_alternating_stress_pa) ** (-record.basquin_exponent)
    if not math.isfinite(life) or life <= 0.0:
        raise StructuralEvidenceError("fatigue life evaluation is non-finite")
    return life


def evaluate_damage_blocks(record: FatigueMaterialRecord, blocks: Iterable[tuple[str, tuple[RainflowCycle, ...]]]) -> FatigueDamageResult:
    cumulative = Decimal(0)
    elapsed_cycles = 0.0
    ledger: list[DamageLedgerEntry] = []
    event_cycle: float | None = None
    event_id: str | None = None
    for block_id, cycles in blocks:
        if not block_id.strip() or not cycles:
            raise StructuralEvidenceError("fatigue damage block identity and cycles are required")
        for cycle in aggregate_cycles(cycles):
            corrected = corrected_amplitude_goodman(record, cycle)
            life = cycles_to_failure(record, corrected)
            increment = Decimal(str(cycle.count)) / Decimal(str(life))
            before = cumulative
            cumulative += increment
            if event_cycle is None and cumulative >= Decimal(1):
                cycles_inside = float((Decimal(1) - before) * Decimal(str(life)))
                event_cycle = elapsed_cycles + cycles_inside
                identity = {"record_id": record.record_id, "block_id": block_id, "event_cycle": event_cycle, "mechanism": "miner_damage_crossing"}
                event_id = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            ledger.append(DamageLedgerEntry(block_id, cycle.alternating_stress_pa, cycle.mean_pa, corrected, cycle.count, life, str(increment), str(cumulative), (life / record.life_scatter_factor, life * record.life_scatter_factor)))
            elapsed_cycles += cycle.count
    return FatigueDamageResult(tuple(ledger), str(cumulative), cumulative >= Decimal(1), event_cycle, event_id)
