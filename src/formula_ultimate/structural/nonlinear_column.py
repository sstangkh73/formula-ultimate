"""Contracts and analytical references for Work 038 imperfect columns."""

from __future__ import annotations

from dataclasses import dataclass
import math

from .acceptance import MeshData, StructuralEvidenceError


def cantilever_first_mode(x_m: float, length_m: float) -> float:
    """Return the normalized Euler cantilever first-mode ordinate."""

    if not math.isfinite(x_m) or not math.isfinite(length_m) or length_m <= 0.0:
        raise StructuralEvidenceError("mode coordinates must be finite and length positive")
    if x_m < 0.0 or x_m > length_m:
        raise StructuralEvidenceError("mode coordinate lies outside the column")
    return 1.0 - math.cos(math.pi * x_m / (2.0 * length_m))


def secant_amplification(load_n: float, critical_load_n: float) -> float:
    """Return the elastic precritical secant amplification 1/(1-P/Pcr)."""

    if not (math.isfinite(load_n) and math.isfinite(critical_load_n)):
        raise StructuralEvidenceError("secant inputs must be finite")
    if critical_load_n <= 0.0 or load_n < 0.0 or load_n >= critical_load_n:
        raise StructuralEvidenceError("secant relation requires 0 <= P < Pcr")
    return 1.0 / (1.0 - load_n / critical_load_n)


def imperfect_mesh(
    mesh: MeshData, *, length_m: float, tip_amplitude_m: float
) -> MeshData:
    """Translate each cross-section in z by a deterministic mode-shaped offset."""

    if not math.isfinite(tip_amplitude_m) or tip_amplitude_m < 0.0:
        raise StructuralEvidenceError("tip imperfection must be finite and non-negative")
    nodes = {
        node: (
            xyz[0],
            xyz[1],
            xyz[2] + tip_amplitude_m * cantilever_first_mode(xyz[0], length_m),
        )
        for node, xyz in mesh.nodes.items()
    }
    return MeshData(nodes=nodes, tetrahedra=mesh.tetrahedra, triangles=mesh.triangles)


@dataclass(frozen=True, slots=True)
class ResponsePoint:
    load_fraction: float
    total_tip_offset_m: float
    measured_amplification: float
    reference_amplification: float

    @property
    def reference_error_relative(self) -> float:
        return abs(self.measured_amplification - self.reference_amplification) / self.reference_amplification


def response_is_strictly_monotonic(points: list[ResponsePoint]) -> bool:
    ordered = sorted(points, key=lambda point: point.load_fraction)
    return all(
        current.measured_amplification > previous.measured_amplification
        for previous, current in zip(ordered, ordered[1:], strict=False)
    )
