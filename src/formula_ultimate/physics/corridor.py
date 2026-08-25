"""Level-0 3D circuit-corridor and planar swept-envelope screening.

The module integrates piecewise-constant horizontal curvature, grade and bank.
It is deliberately a feasibility screen: it does not model tyres, suspension,
transients, barriers, kerbs or a racing line.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Any, Mapping


class CorridorInputError(ValueError):
    """Raised when corridor inputs violate the declared contract."""


_EVIDENCE_CLASSES = {
    "surveyed",
    "operator_engineering",
    "digitized_approximate",
    "synthetic_validation",
    "unavailable",
}
_ADMISSION_EVIDENCE = {"surveyed", "operator_engineering"}


def _finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise CorridorInputError(f"{name} must be finite; received {value!r}")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise CorridorInputError(f"{name} must be > 0; received {value!r}")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise CorridorInputError(f"{name} must be >= 0; received {value!r}")


def _heading_residual(angle_rad: float) -> float:
    return math.atan2(math.sin(angle_rad), math.cos(angle_rad))


@dataclass(frozen=True, slots=True)
class CorridorEvidence:
    evidence_class: str
    source_id: str
    source_title: str
    source_url: str | None
    coordinate_reference_system: str
    horizontal_uncertainty_m: float
    vertical_uncertainty_m: float

    def __post_init__(self) -> None:
        if self.evidence_class not in _EVIDENCE_CLASSES:
            raise CorridorInputError(
                f"unsupported evidence_class {self.evidence_class!r}"
            )
        for name, value in (
            ("source_id", self.source_id),
            ("source_title", self.source_title),
            ("coordinate_reference_system", self.coordinate_reference_system),
        ):
            if not value.strip():
                raise CorridorInputError(f"{name} must not be blank")
        if self.source_url is not None and not (
            self.source_url.startswith("https://")
            or self.source_url.startswith("urn:")
        ):
            raise CorridorInputError("source_url must use https:// or urn:")
        _nonnegative("horizontal_uncertainty_m", self.horizontal_uncertainty_m)
        _nonnegative("vertical_uncertainty_m", self.vertical_uncertainty_m)

    @property
    def admission_capable(self) -> bool:
        return self.evidence_class in _ADMISSION_EVIDENCE


@dataclass(frozen=True, slots=True)
class CorridorSegment:
    segment_id: str
    length_m: float
    curvature_1pm: float
    grade_rad: float
    bank_rad: float
    width_left_m: float
    width_right_m: float

    def __post_init__(self) -> None:
        if not self.segment_id.strip():
            raise CorridorInputError("segment_id must not be blank")
        _positive("length_m", self.length_m)
        _finite("curvature_1pm", self.curvature_1pm)
        _finite("grade_rad", self.grade_rad)
        _finite("bank_rad", self.bank_rad)
        _positive("width_left_m", self.width_left_m)
        _positive("width_right_m", self.width_right_m)
        if abs(self.grade_rad) >= math.pi / 2.0:
            raise CorridorInputError("abs(grade_rad) must be < pi/2")
        if abs(self.bank_rad) >= math.pi / 2.0:
            raise CorridorInputError("abs(bank_rad) must be < pi/2")


@dataclass(frozen=True, slots=True)
class CircuitCorridor:
    schema_version: str
    corridor_id: str
    circuit_id: str
    layout_reference: str
    start_x_m: float
    start_y_m: float
    start_z_m: float
    start_heading_rad: float
    closed_loop: bool
    evidence: CorridorEvidence
    segments: tuple[CorridorSegment, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "1.0":
            raise CorridorInputError(
                f"unsupported corridor schema_version {self.schema_version!r}"
            )
        for name, value in (
            ("corridor_id", self.corridor_id),
            ("circuit_id", self.circuit_id),
            ("layout_reference", self.layout_reference),
        ):
            if not value.strip():
                raise CorridorInputError(f"{name} must not be blank")
        for name, value in (
            ("start_x_m", self.start_x_m),
            ("start_y_m", self.start_y_m),
            ("start_z_m", self.start_z_m),
            ("start_heading_rad", self.start_heading_rad),
        ):
            _finite(name, value)
        if not self.segments:
            raise CorridorInputError("corridor must contain at least one segment")
        ids = [segment.segment_id for segment in self.segments]
        if len(set(ids)) != len(ids):
            raise CorridorInputError("segment_id values must be unique")


@dataclass(frozen=True, slots=True)
class VehicleEnvelope:
    width_m: float
    wheelbase_m: float
    front_overhang_m: float
    rear_overhang_m: float
    max_steering_angle_rad: float

    def __post_init__(self) -> None:
        _positive("width_m", self.width_m)
        _positive("wheelbase_m", self.wheelbase_m)
        _nonnegative("front_overhang_m", self.front_overhang_m)
        _nonnegative("rear_overhang_m", self.rear_overhang_m)
        _positive("max_steering_angle_rad", self.max_steering_angle_rad)
        if self.max_steering_angle_rad >= math.pi / 2.0:
            raise CorridorInputError("max_steering_angle_rad must be < pi/2")


@dataclass(frozen=True, slots=True)
class CorridorStation:
    segment_id: str
    distance_m: float
    x_m: float
    y_m: float
    z_m: float
    heading_rad: float
    grade_rad: float
    bank_rad: float
    width_left_m: float
    width_right_m: float


@dataclass(frozen=True, slots=True)
class SegmentEnvelopeAssessment:
    segment_id: str
    status: str
    required_steering_angle_rad: float
    inside_margin_m: float
    outside_margin_m: float
    reason: str


@dataclass(frozen=True, slots=True)
class CorridorAssessment:
    circuit_id: str
    corridor_id: str | None
    status: str
    minimum_margin_m: float | None
    first_failing_segment_id: str | None
    reason: str
    segment_assessments: tuple[SegmentEnvelopeAssessment, ...]


@dataclass(frozen=True, slots=True)
class ClosureResidual:
    horizontal_m: float
    vertical_m: float
    heading_rad: float


def _advance(
    x_m: float,
    y_m: float,
    z_m: float,
    heading_rad: float,
    segment: CorridorSegment,
    distance_m: float,
) -> tuple[float, float, float, float]:
    k = segment.curvature_1pm
    if abs(k) < 1.0e-14:
        x_m += distance_m * math.cos(heading_rad)
        y_m += distance_m * math.sin(heading_rad)
    else:
        end_heading = heading_rad + k * distance_m
        x_m += (math.sin(end_heading) - math.sin(heading_rad)) / k
        y_m += (-math.cos(end_heading) + math.cos(heading_rad)) / k
    z_m += distance_m * math.tan(segment.grade_rad)
    return x_m, y_m, z_m, heading_rad + k * distance_m


def integrate_corridor(
    corridor: CircuitCorridor, *, maximum_station_spacing_m: float = 10.0
) -> tuple[CorridorStation, ...]:
    """Return deterministic stations, including the start and every segment end."""

    _positive("maximum_station_spacing_m", maximum_station_spacing_m)
    x_m = corridor.start_x_m
    y_m = corridor.start_y_m
    z_m = corridor.start_z_m
    heading_rad = corridor.start_heading_rad
    distance_m = 0.0
    first = corridor.segments[0]
    stations = [
        CorridorStation(
            first.segment_id,
            distance_m,
            x_m,
            y_m,
            z_m,
            heading_rad,
            first.grade_rad,
            first.bank_rad,
            first.width_left_m,
            first.width_right_m,
        )
    ]
    for segment in corridor.segments:
        steps = max(1, math.ceil(segment.length_m / maximum_station_spacing_m))
        step_m = segment.length_m / steps
        for _ in range(steps):
            x_m, y_m, z_m, heading_rad = _advance(
                x_m, y_m, z_m, heading_rad, segment, step_m
            )
            distance_m += step_m
            stations.append(
                CorridorStation(
                    segment.segment_id,
                    distance_m,
                    x_m,
                    y_m,
                    z_m,
                    heading_rad,
                    segment.grade_rad,
                    segment.bank_rad,
                    segment.width_left_m,
                    segment.width_right_m,
                )
            )
    return tuple(stations)


def closure_residual(corridor: CircuitCorridor) -> ClosureResidual:
    end = integrate_corridor(
        corridor,
        maximum_station_spacing_m=max(segment.length_m for segment in corridor.segments),
    )[-1]
    return ClosureResidual(
        horizontal_m=math.hypot(
            end.x_m - corridor.start_x_m, end.y_m - corridor.start_y_m
        ),
        vertical_m=abs(end.z_m - corridor.start_z_m),
        heading_rad=abs(
            _heading_residual(end.heading_rad - corridor.start_heading_rad)
        ),
    )


def _assess_segment(
    segment: CorridorSegment,
    vehicle: VehicleEnvelope,
    uncertainty_m: float,
) -> SegmentEnvelopeAssessment:
    half_width_m = vehicle.width_m / 2.0
    left_m = segment.width_left_m - uncertainty_m
    right_m = segment.width_right_m - uncertainty_m
    static_left_margin_m = left_m - half_width_m
    static_right_margin_m = right_m - half_width_m
    required_steering = math.atan(vehicle.wheelbase_m * abs(segment.curvature_1pm))

    if left_m <= 0.0 or right_m <= 0.0:
        return SegmentEnvelopeAssessment(
            segment.segment_id,
            "rejected",
            required_steering,
            min(static_left_margin_m, static_right_margin_m),
            min(static_left_margin_m, static_right_margin_m),
            "horizontal uncertainty consumes an available corridor side",
        )
    if required_steering > vehicle.max_steering_angle_rad:
        return SegmentEnvelopeAssessment(
            segment.segment_id,
            "rejected",
            required_steering,
            static_left_margin_m,
            static_right_margin_m,
            "required bicycle-model steering exceeds the vehicle limit",
        )
    if abs(segment.curvature_1pm) < 1.0e-14:
        inside_margin_m = min(static_left_margin_m, static_right_margin_m)
        outside_margin_m = max(static_left_margin_m, static_right_margin_m)
    else:
        radius_m = 1.0 / abs(segment.curvature_1pm)
        inside_available_m, outside_available_m = (
            (left_m, right_m)
            if segment.curvature_1pm > 0.0
            else (right_m, left_m)
        )
        inside_boundary_radius_m = max(0.0, radius_m - inside_available_m)
        vehicle_inside_radius_m = max(0.0, radius_m - half_width_m)
        inside_margin_m = vehicle_inside_radius_m - inside_boundary_radius_m
        longitudinal_extent_m = max(
            vehicle.wheelbase_m + vehicle.front_overhang_m,
            vehicle.rear_overhang_m,
        )
        vehicle_outside_radius_m = math.hypot(
            longitudinal_extent_m, radius_m + half_width_m
        )
        outside_boundary_radius_m = radius_m + outside_available_m
        outside_margin_m = outside_boundary_radius_m - vehicle_outside_radius_m

    minimum_margin_m = min(inside_margin_m, outside_margin_m)
    status = "passed" if minimum_margin_m >= 0.0 else "rejected"
    reason = (
        "planar constant-radius swept envelope fits"
        if status == "passed"
        else "planar swept envelope crosses the effective corridor boundary"
    )
    return SegmentEnvelopeAssessment(
        segment.segment_id,
        status,
        required_steering,
        inside_margin_m,
        outside_margin_m,
        reason,
    )


def assess_vehicle_corridor(
    corridor: CircuitCorridor | None,
    vehicle: VehicleEnvelope,
    *,
    circuit_id: str | None = None,
) -> CorridorAssessment:
    """Assess feasibility without promoting synthetic or weak data to admission."""

    if corridor is None:
        if circuit_id is None or not circuit_id.strip():
            raise CorridorInputError("circuit_id is required when corridor is absent")
        return CorridorAssessment(
            circuit_id,
            None,
            "indeterminate",
            None,
            None,
            "no surveyed 3D corridor is available",
            (),
        )
    assessments = tuple(
        _assess_segment(
            segment, vehicle, corridor.evidence.horizontal_uncertainty_m
        )
        for segment in corridor.segments
    )
    failure = next((item for item in assessments if item.status == "rejected"), None)
    minimum_margin_m = min(
        min(item.inside_margin_m, item.outside_margin_m) for item in assessments
    )
    if failure is not None:
        return CorridorAssessment(
            corridor.circuit_id,
            corridor.corridor_id,
            "rejected",
            minimum_margin_m,
            failure.segment_id,
            failure.reason,
            assessments,
        )
    if corridor.evidence.admission_capable:
        status = "admitted"
        reason = "geometry screen passed with admission-capable evidence"
    elif corridor.evidence.evidence_class == "synthetic_validation":
        status = "verification_passed"
        reason = "analytical fixture passed; this is not real-circuit admission"
    else:
        status = "indeterminate"
        reason = "geometry passes, but evidence is not admission-capable"
    return CorridorAssessment(
        corridor.circuit_id,
        corridor.corridor_id,
        status,
        minimum_margin_m,
        None,
        reason,
        assessments,
    )


def _required(mapping: Mapping[str, Any], key: str) -> Any:
    if key not in mapping:
        raise CorridorInputError(f"missing required field {key!r}")
    return mapping[key]


def corridor_from_mapping(data: Mapping[str, Any]) -> CircuitCorridor:
    """Parse one strict corridor mapping from the versioned JSON contract."""

    evidence_data = _required(data, "evidence")
    segment_data = _required(data, "segments")
    if not isinstance(evidence_data, Mapping):
        raise CorridorInputError("evidence must be an object")
    if not isinstance(segment_data, list):
        raise CorridorInputError("segments must be an array")
    closed_loop = _required(data, "closed_loop")
    if not isinstance(closed_loop, bool):
        raise CorridorInputError("closed_loop must be a boolean")
    if not all(isinstance(item, Mapping) for item in segment_data):
        raise CorridorInputError("each segment must be an object")
    try:
        evidence = CorridorEvidence(
            evidence_class=str(_required(evidence_data, "evidence_class")),
            source_id=str(_required(evidence_data, "source_id")),
            source_title=str(_required(evidence_data, "source_title")),
            source_url=(
                None
                if evidence_data.get("source_url") is None
                else str(evidence_data["source_url"])
            ),
            coordinate_reference_system=str(
                _required(evidence_data, "coordinate_reference_system")
            ),
            horizontal_uncertainty_m=float(
                _required(evidence_data, "horizontal_uncertainty_m")
            ),
            vertical_uncertainty_m=float(
                _required(evidence_data, "vertical_uncertainty_m")
            ),
        )
        segments = tuple(
            CorridorSegment(
                segment_id=str(_required(item, "segment_id")),
                length_m=float(_required(item, "length_m")),
                curvature_1pm=float(_required(item, "curvature_1pm")),
                grade_rad=float(_required(item, "grade_rad")),
                bank_rad=float(_required(item, "bank_rad")),
                width_left_m=float(_required(item, "width_left_m")),
                width_right_m=float(_required(item, "width_right_m")),
            )
            for item in segment_data
        )
        return CircuitCorridor(
            schema_version=str(_required(data, "schema_version")),
            corridor_id=str(_required(data, "corridor_id")),
            circuit_id=str(_required(data, "circuit_id")),
            layout_reference=str(_required(data, "layout_reference")),
            start_x_m=float(_required(data, "start_x_m")),
            start_y_m=float(_required(data, "start_y_m")),
            start_z_m=float(_required(data, "start_z_m")),
            start_heading_rad=float(_required(data, "start_heading_rad")),
            closed_loop=closed_loop,
            evidence=evidence,
            segments=segments,
        )
    except (TypeError, ValueError) as exc:
        if isinstance(exc, CorridorInputError):
            raise
        raise CorridorInputError(f"invalid corridor field type: {exc}") from exc


def load_corridors(path: str | Path) -> tuple[CircuitCorridor, ...]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, Mapping):
        raise CorridorInputError("corridor document root must be an object")
    if data.get("schema_version") != "1.0":
        raise CorridorInputError("corridor document schema_version must be '1.0'")
    rows = data.get("corridors")
    if not isinstance(rows, list) or not rows:
        raise CorridorInputError("corridors must be a non-empty array")
    corridors = tuple(corridor_from_mapping(row) for row in rows)
    ids = [corridor.corridor_id for corridor in corridors]
    if len(ids) != len(set(ids)):
        raise CorridorInputError("corridor_id values must be unique")
    return corridors
