"""Work 074 deterministic centreline feedback around the Work 073 plant."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
import math
from typing import Any, Mapping

from formula_ultimate.physics.corridor import (
    CircuitCorridor,
    CorridorStation,
    integrate_corridor,
)

from .coupled_planar_differential import (
    total_accounted_energy_j as total_coupled_accounted_energy_j,
)
from .powertrain_dynamics import (
    PowertrainConfig,
    total_accounted_energy_j as total_powertrain_accounted_energy_j,
)
from .sprung_body_vertical_coupling import (
    SprungBodyVerticalConfig,
    SprungBodyVerticalState,
    SprungBodyVerticalStepEvidence,
    conservation_accounted_energy_j,
    initial_sprung_body_vertical_state,
    step_sprung_body_vertical_coupling,
    with_vertical_steer,
)


MODEL_VERSION = "closed_loop_corridor_controller_v1"


class ClosedLoopControllerError(ValueError):
    """Raised when the Work 074 controller contract is invalid."""


def _finite(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ClosedLoopControllerError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ClosedLoopControllerError(f"{name} must be finite")
    return result


def _positive(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result <= 0.0:
        raise ClosedLoopControllerError(f"{name} must be positive")
    return result


def _nonnegative(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result < 0.0:
        raise ClosedLoopControllerError(f"{name} must be non-negative")
    return result


def _section(raw: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    result = raw.get(name)
    if not isinstance(result, Mapping):
        raise ClosedLoopControllerError(f"missing section {name}")
    return result


def _wrap(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


@dataclass(frozen=True, slots=True)
class ClosedLoopControllerConfig:
    protocol_id: str
    corridor_id: str
    heading_gain: float
    cross_track_gain_rad_per_m: float
    maximum_steer_angle_rad: float
    station_spacing_m: float
    vehicle_half_width_m: float
    duration_s: float
    time_step_s: float
    initial_lateral_error_m: float
    initial_heading_error_rad: float
    mirror_absolute_tolerance: float
    projection_distance_tolerance_m: float
    refinement_relative_tolerance: float


@dataclass(frozen=True, slots=True)
class CentrelineProjection:
    segment_id: str
    progress_m: float
    x_m: float
    y_m: float
    desired_heading_rad: float
    curvature_1pm: float
    cross_track_error_m: float
    distance_m: float
    width_left_m: float
    width_right_m: float


@dataclass(frozen=True, slots=True)
class SteeringCommandEvidence:
    projection: CentrelineProjection
    heading_error_rad: float
    feedforward_steer_rad: float
    heading_feedback_rad: float
    cross_track_feedback_rad: float
    unclipped_steer_rad: float
    applied_steer_rad: float
    saturated: bool


@dataclass(frozen=True, slots=True)
class ClosedLoopStepEvidence:
    step_index: int
    command: SteeringCommandEvidence
    vertical: SprungBodyVerticalStepEvidence
    end_projection: CentrelineProjection


@dataclass(frozen=True, slots=True)
class ClosedLoopRunResult:
    model_version: str
    protocol_id: str
    corridor_id: str
    status: str
    outcome: str
    terminal_reason: str
    requested_steps: int
    executed_steps: int
    initial_cross_track_error_m: float
    final_cross_track_error_m: float
    maximum_abs_cross_track_error_m: float
    final_heading_error_rad: float
    final_progress_m: float
    steering_saturation_count: int
    minimum_actual_normal_load_n: float
    maximum_abs_suspension_travel_m: float
    maximum_total_global_relative_energy_residual: float
    final_state: SprungBodyVerticalState
    trace: tuple[ClosedLoopStepEvidence, ...]
    result_sha256: str


def load_closed_loop_controller_config(
    raw: Mapping[str, Any], *, corridor_id: str | None = None
) -> ClosedLoopControllerConfig:
    if raw.get("model_version") != MODEL_VERSION:
        raise ClosedLoopControllerError("closed-loop controller model version mismatch")
    protocol = raw.get("protocol_id")
    if not isinstance(protocol, str) or not protocol:
        raise ClosedLoopControllerError("protocol_id must be non-empty")
    selected = raw.get("reference_corridor_id") if corridor_id is None else corridor_id
    if not isinstance(selected, str) or not selected:
        raise ClosedLoopControllerError("corridor_id must be non-empty")
    controller = _section(raw, "controller")
    numerical = _section(raw, "numerical")
    heading_gain = _finite("heading_gain", controller.get("heading_gain"))
    cross_gain = _finite(
        "cross_track_gain_rad_per_m", controller.get("cross_track_gain_rad_per_m")
    )
    if heading_gain < 0.0 or cross_gain < 0.0:
        raise ClosedLoopControllerError("reference feedback gains must be non-negative")
    maximum_steer = _positive(
        "maximum_steer_angle_rad", controller.get("maximum_steer_angle_rad")
    )
    if maximum_steer >= math.pi / 2.0:
        raise ClosedLoopControllerError("maximum steer must be below pi/2")
    mirror = _positive(
        "mirror_absolute_tolerance", numerical.get("mirror_absolute_tolerance")
    )
    projection = _positive(
        "projection_distance_tolerance_m",
        numerical.get("projection_distance_tolerance_m"),
    )
    refinement = _positive(
        "refinement_relative_tolerance", numerical.get("refinement_relative_tolerance")
    )
    if mirror > 1.0e-6 or projection > 0.01 or refinement > 0.02:
        raise ClosedLoopControllerError("controller numerical tolerance exceeds ceiling")
    return ClosedLoopControllerConfig(
        protocol,
        selected,
        heading_gain,
        cross_gain,
        maximum_steer,
        _positive("station_spacing_m", controller.get("station_spacing_m")),
        _positive("vehicle_half_width_m", controller.get("vehicle_half_width_m")),
        _positive("duration_s", controller.get("duration_s")),
        _positive("time_step_s", controller.get("time_step_s")),
        _finite("initial_lateral_error_m", controller.get("initial_lateral_error_m")),
        _finite("initial_heading_error_rad", controller.get("initial_heading_error_rad")),
        mirror,
        projection,
        refinement,
    )


def with_feedback_gains(
    config: ClosedLoopControllerConfig,
    *, heading_gain: float | None = None,
    cross_track_gain_rad_per_m: float | None = None,
) -> ClosedLoopControllerConfig:
    heading = config.heading_gain if heading_gain is None else _finite("heading_gain", heading_gain)
    cross = (
        config.cross_track_gain_rad_per_m
        if cross_track_gain_rad_per_m is None
        else _finite("cross_track_gain_rad_per_m", cross_track_gain_rad_per_m)
    )
    return replace(config, heading_gain=heading, cross_track_gain_rad_per_m=cross)


def project_to_corridor(
    corridor: CircuitCorridor,
    x_m: float,
    y_m: float,
    *,
    station_spacing_m: float,
) -> CentrelineProjection:
    x = _finite("x_m", x_m)
    y = _finite("y_m", y_m)
    spacing = _positive("station_spacing_m", station_spacing_m)
    stations = integrate_corridor(corridor, maximum_station_spacing_m=spacing)
    return project_to_corridor_stations(corridor, stations, x, y)


def project_to_corridor_stations(
    corridor: CircuitCorridor,
    stations: tuple[CorridorStation, ...],
    x: float,
    y: float,
) -> CentrelineProjection:
    segment_by_id = {item.segment_id: item for item in corridor.segments}
    best: tuple[float, float, int, float, float, float] | None = None
    for index, (start, end) in enumerate(zip(stations, stations[1:])):
        dx, dy = end.x_m - start.x_m, end.y_m - start.y_m
        length_squared = dx * dx + dy * dy
        if length_squared <= 0.0:
            raise ClosedLoopControllerError("corridor sampling produced a zero planar segment")
        fraction = max(0.0, min(1.0, ((x - start.x_m) * dx + (y - start.y_m) * dy) / length_squared))
        px, py = start.x_m + fraction * dx, start.y_m + fraction * dy
        distance_squared = (x - px) ** 2 + (y - py) ** 2
        progress = start.distance_m + fraction * (end.distance_m - start.distance_m)
        candidate = (distance_squared, progress, index, fraction, px, py)
        if best is None or candidate[:2] < best[:2]:
            best = candidate
    if best is None:
        raise ClosedLoopControllerError("corridor projection requires at least two stations")
    distance_squared, progress, index, _, px, py = best
    start, end = stations[index], stations[index + 1]
    heading = math.atan2(end.y_m - start.y_m, end.x_m - start.x_m)
    cross_track = (x - px) * -math.sin(heading) + (y - py) * math.cos(heading)
    segment = segment_by_id[start.segment_id]
    return CentrelineProjection(
        start.segment_id,
        progress,
        px,
        py,
        heading,
        segment.curvature_1pm,
        cross_track,
        math.sqrt(distance_squared),
        segment.width_left_m,
        segment.width_right_m,
    )


def steering_command(
    config: ClosedLoopControllerConfig,
    corridor: CircuitCorridor,
    *,
    wheelbase_m: float,
    x_m: float,
    y_m: float,
    heading_rad: float,
) -> SteeringCommandEvidence:
    projection = project_to_corridor(
        corridor, x_m, y_m, station_spacing_m=config.station_spacing_m
    )
    heading_error = _wrap(_finite("heading_rad", heading_rad) - projection.desired_heading_rad)
    feedforward = math.atan(_positive("wheelbase_m", wheelbase_m) * projection.curvature_1pm)
    heading_feedback = -config.heading_gain * heading_error
    cross_feedback = -config.cross_track_gain_rad_per_m * projection.cross_track_error_m
    raw = feedforward + heading_feedback + cross_feedback
    applied = max(-config.maximum_steer_angle_rad, min(config.maximum_steer_angle_rad, raw))
    return SteeringCommandEvidence(
        projection,
        heading_error,
        feedforward,
        heading_feedback,
        cross_feedback,
        raw,
        applied,
        applied != raw,
    )


def steering_command_from_stations(
    config: ClosedLoopControllerConfig,
    corridor: CircuitCorridor,
    stations: tuple[CorridorStation, ...],
    *,
    wheelbase_m: float,
    x_m: float,
    y_m: float,
    heading_rad: float,
) -> SteeringCommandEvidence:
    projection = project_to_corridor_stations(corridor, stations, x_m, y_m)
    heading_error = _wrap(_finite("heading_rad", heading_rad) - projection.desired_heading_rad)
    feedforward = math.atan(_positive("wheelbase_m", wheelbase_m) * projection.curvature_1pm)
    heading_feedback = -config.heading_gain * heading_error
    cross_feedback = -config.cross_track_gain_rad_per_m * projection.cross_track_error_m
    raw = feedforward + heading_feedback + cross_feedback
    applied = max(-config.maximum_steer_angle_rad, min(config.maximum_steer_angle_rad, raw))
    return SteeringCommandEvidence(
        projection, heading_error, feedforward, heading_feedback, cross_feedback,
        raw, applied, applied != raw,
    )


def _outside_corridor(config: ClosedLoopControllerConfig, projection: CentrelineProjection) -> bool:
    available = (
        projection.width_left_m - config.vehicle_half_width_m
        if projection.cross_track_error_m >= 0.0
        else projection.width_right_m - config.vehicle_half_width_m
    )
    return abs(projection.cross_track_error_m) > available


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def run_closed_loop_controller(
    config: ClosedLoopControllerConfig,
    vertical: SprungBodyVerticalConfig,
    powertrain: PowertrainConfig,
    corridor: CircuitCorridor,
    *,
    sample_stride: int = 10,
) -> ClosedLoopRunResult:
    if corridor.corridor_id != config.corridor_id:
        raise ClosedLoopControllerError("controller and corridor identity mismatch")
    if not isinstance(sample_stride, int) or isinstance(sample_stride, bool) or sample_stride <= 0:
        raise ClosedLoopControllerError("sample_stride must be a positive integer")
    count = config.duration_s / config.time_step_s
    requested_steps = round(count)
    if not math.isclose(count, requested_steps, rel_tol=0.0, abs_tol=1.0e-10):
        raise ClosedLoopControllerError("duration must be an integer multiple of time step")
    wheelbase = max(item.x_position_m for item in vertical.contacts) - min(
        item.x_position_m for item in vertical.contacts
    )
    if wheelbase <= 0.0:
        raise ClosedLoopControllerError("contact geometry has no positive wheelbase")
    stations = integrate_corridor(
        corridor, maximum_station_spacing_m=config.station_spacing_m
    )
    state = initial_sprung_body_vertical_state(vertical, powertrain)
    start_heading = corridor.start_heading_rad
    normal = (-math.sin(start_heading), math.cos(start_heading))
    planar = replace(
        state.coupled.planar,
        x_position_m=corridor.start_x_m + config.initial_lateral_error_m * normal[0],
        y_position_m=corridor.start_y_m + config.initial_lateral_error_m * normal[1],
        heading_rad=start_heading + config.initial_heading_error_rad,
    )
    state = replace(state, coupled=replace(state.coupled, planar=planar))
    initial_powertrain = total_powertrain_accounted_energy_j(powertrain, state.coupled.powertrain)
    initial_coupled = total_coupled_accounted_energy_j(vertical.transient.coupled, powertrain, state.coupled)
    zero_road = tuple(0.0 for _ in vertical.contacts)
    initial_total = conservation_accounted_energy_j(vertical, powertrain, state, zero_road)
    initial_projection = project_to_corridor_stations(
        corridor, stations, planar.x_position_m, planar.y_position_m
    )
    trace: list[ClosedLoopStepEvidence] = []
    maximum_error = abs(initial_projection.cross_track_error_m)
    minimum_load = min(item.static_preload_n for item in vertical.contacts)
    maximum_travel = maximum_residual = 0.0
    saturation_count = executed = 0
    outcome, terminal = "running", "running"
    final_projection = initial_projection
    if _outside_corridor(config, initial_projection):
        outcome, terminal = "DNF", "corridor_departure"
    for index in range(requested_steps if outcome == "running" else 0):
        planar = state.coupled.planar
        command = steering_command_from_stations(
            config,
            corridor,
            stations,
            wheelbase_m=wheelbase,
            x_m=planar.x_position_m,
            y_m=planar.y_position_m,
            heading_rad=planar.heading_rad,
        )
        saturation_count += int(command.saturated)
        steered = with_vertical_steer(vertical, command.applied_steer_rad)
        state, evidence = step_sprung_body_vertical_coupling(
            steered,
            powertrain,
            state,
            initial_powertrain_energy_j=initial_powertrain,
            initial_coupled_energy_j=initial_coupled,
            initial_total_energy_j=initial_total,
            time_step_s=config.time_step_s,
        )
        executed += 1
        final_projection = project_to_corridor_stations(
            corridor, stations,
            state.coupled.planar.x_position_m,
            state.coupled.planar.y_position_m,
        )
        maximum_error = max(maximum_error, abs(final_projection.cross_track_error_m))
        minimum_load = min(minimum_load, *(item.actual_normal_load_n for item in evidence.contacts))
        maximum_travel = max(
            maximum_travel, *(abs(item.suspension_end_m) for item in evidence.contacts)
        )
        maximum_residual = max(
            maximum_residual, evidence.total_global_relative_energy_residual
        )
        record = ClosedLoopStepEvidence(index + 1, command, evidence, final_projection)
        if index % sample_stride == 0 or index == requested_steps - 1 or state.outcome == "DNF":
            trace.append(record)
        if state.outcome == "DNF":
            outcome, terminal = "DNF", str(state.dnf_reason)
            break
        if _outside_corridor(config, final_projection):
            outcome, terminal = "DNF", "corridor_departure"
            if not trace or trace[-1] != record:
                trace.append(record)
            break
    if outcome == "running":
        outcome, terminal = "finished", "duration_complete"
    final_heading_error = _wrap(
        state.coupled.planar.heading_rad - final_projection.desired_heading_rad
    )
    status = "passed" if maximum_residual <= vertical.global_energy_relative_tolerance else "failed"
    body = {
        "model_version": MODEL_VERSION,
        "protocol_id": config.protocol_id,
        "corridor_id": corridor.corridor_id,
        "status": status,
        "outcome": outcome,
        "terminal_reason": terminal,
        "requested_steps": requested_steps,
        "executed_steps": executed,
        "initial_cross_track_error_m": initial_projection.cross_track_error_m,
        "final_cross_track_error_m": final_projection.cross_track_error_m,
        "maximum_abs_cross_track_error_m": maximum_error,
        "final_heading_error_rad": final_heading_error,
        "final_progress_m": final_projection.progress_m,
        "steering_saturation_count": saturation_count,
        "minimum_actual_normal_load_n": minimum_load,
        "maximum_abs_suspension_travel_m": maximum_travel,
        "maximum_total_global_relative_energy_residual": maximum_residual,
        "final_state": asdict(state),
        "trace": [asdict(item) for item in trace],
    }
    identity = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    return ClosedLoopRunResult(
        MODEL_VERSION,
        config.protocol_id,
        corridor.corridor_id,
        status,
        outcome,
        terminal,
        requested_steps,
        executed,
        initial_projection.cross_track_error_m,
        final_projection.cross_track_error_m,
        maximum_error,
        final_heading_error,
        final_projection.progress_m,
        saturation_count,
        minimum_load,
        maximum_travel,
        maximum_residual,
        state,
        tuple(trace),
        identity,
    )


def result_to_mapping(result: ClosedLoopRunResult) -> dict[str, Any]:
    return asdict(result)
