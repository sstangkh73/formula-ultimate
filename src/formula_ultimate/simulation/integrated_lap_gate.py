"""Work 076 integrated synthetic closed-loop lap gate."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
import math
from typing import Any, Mapping

from formula_ultimate.physics.corridor import CircuitCorridor, integrate_corridor

from .closed_loop_corridor_controller import (
    ClosedLoopControllerConfig,
    CentrelineProjection,
    SteeringCommandEvidence,
    project_to_corridor_stations,
    steering_command_from_stations,
)
from .coupled_planar_differential import total_accounted_energy_j as total_coupled_accounted_energy_j
from .powertrain_dynamics import PowertrainConfig, total_accounted_energy_j as total_powertrain_accounted_energy_j
from .sprung_body_vertical_coupling import (
    RaisedCosineRoadProfile,
    SprungBodyVerticalConfig,
    SprungBodyVerticalState,
    SprungBodyVerticalStepEvidence,
    conservation_accounted_energy_j,
    initial_sprung_body_vertical_state,
    step_sprung_body_vertical_coupling,
    with_vertical_steer,
)


MODEL_VERSION = "integrated_level0_lap_gate_v1"


class IntegratedLapGateError(ValueError):
    """Raised when the integrated lap contract or evidence is invalid."""


def _finite(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise IntegratedLapGateError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise IntegratedLapGateError(f"{name} must be finite")
    return result


def _positive(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result <= 0.0:
        raise IntegratedLapGateError(f"{name} must be positive")
    return result


def _nonnegative(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result < 0.0:
        raise IntegratedLapGateError(f"{name} must be non-negative")
    return result


def _section(raw: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    result = raw.get(name)
    if not isinstance(result, Mapping):
        raise IntegratedLapGateError(f"missing section {name}")
    return result


def _wrap(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


@dataclass(frozen=True, slots=True)
class IntegratedLapGateConfig:
    protocol_id: str
    corridor_id: str
    time_step_s: float
    timeout_s: float
    throttle: float
    controller: ClosedLoopControllerConfig
    finish_position_tolerance_m: float
    finish_heading_tolerance_rad: float
    progress_spatial_residual_tolerance_m: float
    progress_reversal_tolerance_m: float
    mirror_absolute_tolerance: float
    refinement_relative_tolerance: float
    energy_relative_tolerance: float


@dataclass(frozen=True, slots=True)
class LapFinishEvidence:
    target_progress_m: float
    previous_progress_m: float
    candidate_progress_m: float
    localized_fraction: float
    localized_time_s: float
    localized_x_m: float
    localized_y_m: float
    localized_heading_rad: float
    position_closure_residual_m: float
    heading_closure_residual_rad: float


@dataclass(frozen=True, slots=True)
class IntegratedLapStepEvidence:
    step_index: int
    controller_enabled: bool
    command: SteeringCommandEvidence
    vertical: SprungBodyVerticalStepEvidence
    projection: CentrelineProjection
    unwrapped_progress_m: float
    spatial_distance_m: float
    progress_delta_m: float
    progress_spatial_residual_m: float


@dataclass(frozen=True, slots=True)
class IntegratedLapRunResult:
    model_version: str
    protocol_id: str
    corridor_id: str
    status: str
    outcome: str
    terminal_reason: str
    target_progress_m: float
    executed_steps: int
    elapsed_time_s: float
    credited_progress_m: float
    maximum_abs_cross_track_error_m: float
    maximum_abs_heading_error_rad: float
    steering_saturation_count: int
    minimum_actual_normal_load_n: float
    maximum_abs_suspension_travel_m: float
    maximum_total_global_relative_energy_residual: float
    maximum_abs_progress_spatial_residual_m: float
    finish: LapFinishEvidence | None
    final_state: SprungBodyVerticalState
    trace: tuple[IntegratedLapStepEvidence, ...]
    result_sha256: str


def load_integrated_lap_gate_config(
    raw: Mapping[str, Any],
    *,
    controller_source: ClosedLoopControllerConfig,
    corridor_id: str | None = None,
) -> IntegratedLapGateConfig:
    if raw.get("model_version") != MODEL_VERSION:
        raise IntegratedLapGateError("integrated lap model version mismatch")
    protocol = raw.get("protocol_id")
    if not isinstance(protocol, str) or not protocol:
        raise IntegratedLapGateError("protocol_id must be non-empty")
    selected = raw.get("reference_corridor_id") if corridor_id is None else corridor_id
    if not isinstance(selected, str) or not selected:
        raise IntegratedLapGateError("corridor_id must be non-empty")
    lap = _section(raw, "lap")
    numerical = _section(raw, "numerical")
    throttle = _finite("throttle", lap.get("throttle"))
    if not 0.0 <= throttle <= 1.0:
        raise IntegratedLapGateError("throttle must lie in [0, 1]")
    mirror = _positive("mirror_absolute_tolerance", numerical.get("mirror_absolute_tolerance"))
    refinement = _positive("refinement_relative_tolerance", numerical.get("refinement_relative_tolerance"))
    energy = _positive("energy_relative_tolerance", numerical.get("energy_relative_tolerance"))
    if mirror > 1.0e-6 or refinement > 0.02 or energy > 1.0e-3:
        raise IntegratedLapGateError("integrated lap tolerance exceeds protocol ceiling")
    controller = replace(
        controller_source,
        corridor_id=selected,
        heading_gain=_nonnegative("heading_gain", lap.get("heading_gain")),
        cross_track_gain_rad_per_m=_nonnegative(
            "cross_track_gain_rad_per_m", lap.get("cross_track_gain_rad_per_m")
        ),
        maximum_steer_angle_rad=_positive(
            "maximum_steer_angle_rad", lap.get("maximum_steer_angle_rad")
        ),
        station_spacing_m=_positive("station_spacing_m", lap.get("station_spacing_m")),
        vehicle_half_width_m=_positive("vehicle_half_width_m", lap.get("vehicle_half_width_m")),
        initial_lateral_error_m=_finite(
            "initial_lateral_error_m", lap.get("initial_lateral_error_m")
        ),
        initial_heading_error_rad=_finite(
            "initial_heading_error_rad", lap.get("initial_heading_error_rad")
        ),
    )
    return IntegratedLapGateConfig(
        protocol,
        selected,
        _positive("time_step_s", lap.get("time_step_s")),
        _positive("timeout_s", lap.get("timeout_s")),
        throttle,
        controller,
        _positive("finish_position_tolerance_m", lap.get("finish_position_tolerance_m")),
        _positive("finish_heading_tolerance_rad", lap.get("finish_heading_tolerance_rad")),
        _positive(
            "progress_spatial_residual_tolerance_m",
            lap.get("progress_spatial_residual_tolerance_m"),
        ),
        _nonnegative(
            "progress_reversal_tolerance_m", lap.get("progress_reversal_tolerance_m")
        ),
        mirror,
        refinement,
        energy,
    )


def _outside(config: IntegratedLapGateConfig, projection: CentrelineProjection) -> bool:
    available = (
        projection.width_left_m - config.controller.vehicle_half_width_m
        if projection.cross_track_error_m >= 0.0
        else projection.width_right_m - config.controller.vehicle_half_width_m
    )
    return available < 0.0 or abs(projection.cross_track_error_m) > available


def _unwrapped_progress(base_progress: float, previous: float, lap_length: float) -> float:
    return base_progress + round((previous - base_progress) / lap_length) * lap_length


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def run_integrated_lap_gate(
    config: IntegratedLapGateConfig,
    vertical: SprungBodyVerticalConfig,
    powertrain: PowertrainConfig,
    corridor: CircuitCorridor,
    *,
    controller_enabled: bool = True,
    road_profiles: tuple[RaisedCosineRoadProfile, ...] = (),
    target_progress_m: float | None = None,
    require_loop_closure: bool = True,
    sample_stride: int = 100,
) -> IntegratedLapRunResult:
    if corridor.corridor_id != config.corridor_id:
        raise IntegratedLapGateError("lap gate and corridor identity mismatch")
    if require_loop_closure and not corridor.closed_loop:
        raise IntegratedLapGateError("lap finish requires a closed-loop corridor")
    if not isinstance(controller_enabled, bool):
        raise IntegratedLapGateError("controller_enabled must be boolean")
    if not isinstance(sample_stride, int) or isinstance(sample_stride, bool) or sample_stride <= 0:
        raise IntegratedLapGateError("sample_stride must be a positive integer")
    lap_length = math.fsum(item.length_m for item in corridor.segments)
    target = lap_length if target_progress_m is None else _positive("target_progress_m", target_progress_m)
    if require_loop_closure and not math.isclose(target, lap_length, rel_tol=0.0, abs_tol=1.0e-9):
        raise IntegratedLapGateError("loop closure target must equal one corridor length")
    maximum_steps = math.ceil(config.timeout_s / config.time_step_s)
    wheelbase = max(item.x_position_m for item in vertical.contacts) - min(
        item.x_position_m for item in vertical.contacts
    )
    if wheelbase <= 0.0:
        raise IntegratedLapGateError("contact geometry has no positive wheelbase")
    coupled = replace(vertical.transient.coupled, throttle=config.throttle)
    plant = replace(vertical, transient=replace(vertical.transient, coupled=coupled))
    stations = integrate_corridor(
        corridor, maximum_station_spacing_m=config.controller.station_spacing_m
    )
    state = initial_sprung_body_vertical_state(plant, powertrain)
    normal = (-math.sin(corridor.start_heading_rad), math.cos(corridor.start_heading_rad))
    planar = replace(
        state.coupled.planar,
        x_position_m=corridor.start_x_m + config.controller.initial_lateral_error_m * normal[0],
        y_position_m=corridor.start_y_m + config.controller.initial_lateral_error_m * normal[1],
        heading_rad=corridor.start_heading_rad + config.controller.initial_heading_error_rad,
    )
    state = replace(state, coupled=replace(state.coupled, planar=planar))
    initial_planar = planar
    initial_powertrain = total_powertrain_accounted_energy_j(powertrain, state.coupled.powertrain)
    initial_coupled = total_coupled_accounted_energy_j(plant.transient.coupled, powertrain, state.coupled)
    initial_total = conservation_accounted_energy_j(
        plant, powertrain, state, tuple(0.0 for _ in plant.contacts)
    )
    projection = project_to_corridor_stations(
        corridor, stations, planar.x_position_m, planar.y_position_m
    )
    previous_progress = _unwrapped_progress(projection.progress_m, 0.0, lap_length)
    trace: list[IntegratedLapStepEvidence] = []
    maximum_cross = abs(projection.cross_track_error_m)
    maximum_heading = saturation_count = 0
    minimum_load = min(item.static_preload_n for item in plant.contacts)
    maximum_travel = maximum_energy = maximum_progress_residual = 0.0
    outcome, terminal = "running", "running"
    finish: LapFinishEvidence | None = None
    executed = 0
    if _outside(config, projection):
        outcome, terminal = "DNF", "corridor_departure"
    for index in range(maximum_steps if outcome == "running" else 0):
        start_planar = state.coupled.planar
        command = steering_command_from_stations(
            config.controller,
            corridor,
            stations,
            wheelbase_m=wheelbase,
            x_m=start_planar.x_position_m,
            y_m=start_planar.y_position_m,
            heading_rad=start_planar.heading_rad,
        )
        if not controller_enabled:
            command = replace(command, applied_steer_rad=0.0, saturated=False)
        saturation_count += int(command.saturated)
        state, vertical_evidence = step_sprung_body_vertical_coupling(
            with_vertical_steer(plant, command.applied_steer_rad),
            powertrain,
            state,
            initial_powertrain_energy_j=initial_powertrain,
            initial_coupled_energy_j=initial_coupled,
            initial_total_energy_j=initial_total,
            road_profiles=road_profiles,
            time_step_s=config.time_step_s,
        )
        executed += 1
        end_planar = state.coupled.planar
        projection = project_to_corridor_stations(
            corridor, stations, end_planar.x_position_m, end_planar.y_position_m
        )
        unwrapped = _unwrapped_progress(projection.progress_m, previous_progress, lap_length)
        progress_delta = unwrapped - previous_progress
        spatial_distance = math.hypot(
            end_planar.x_position_m - start_planar.x_position_m,
            end_planar.y_position_m - start_planar.y_position_m,
        )
        progress_residual = progress_delta - spatial_distance
        heading_error = _wrap(end_planar.heading_rad - projection.desired_heading_rad)
        record = IntegratedLapStepEvidence(
            index + 1,
            controller_enabled,
            command,
            vertical_evidence,
            projection,
            unwrapped,
            spatial_distance,
            progress_delta,
            progress_residual,
        )
        maximum_cross = max(maximum_cross, abs(projection.cross_track_error_m))
        maximum_heading = max(maximum_heading, abs(heading_error))
        minimum_load = min(
            minimum_load, *(item.actual_normal_load_n for item in vertical_evidence.contacts)
        )
        maximum_travel = max(
            maximum_travel,
            *(abs(item.suspension_end_m) for item in vertical_evidence.contacts),
        )
        maximum_energy = max(
            maximum_energy, vertical_evidence.total_global_relative_energy_residual
        )
        maximum_progress_residual = max(maximum_progress_residual, abs(progress_residual))
        if index % sample_stride == 0 or state.outcome == "DNF":
            trace.append(record)
        if state.outcome == "DNF":
            outcome, terminal = "DNF", str(state.dnf_reason)
            break
        if progress_delta < -config.progress_reversal_tolerance_m:
            outcome, terminal = "DNF", "progress_reversal"
            if not trace or trace[-1] != record:
                trace.append(record)
            break
        if progress_residual > config.progress_spatial_residual_tolerance_m:
            outcome, terminal = "invalid", "progress_spatial_residual"
            if not trace or trace[-1] != record:
                trace.append(record)
            break
        if _outside(config, projection):
            outcome, terminal = "DNF", "corridor_departure"
            if not trace or trace[-1] != record:
                trace.append(record)
            break
        if previous_progress < target <= unwrapped and progress_delta > 0.0:
            fraction = (target - previous_progress) / progress_delta
            localized_x = start_planar.x_position_m + fraction * (
                end_planar.x_position_m - start_planar.x_position_m
            )
            localized_y = start_planar.y_position_m + fraction * (
                end_planar.y_position_m - start_planar.y_position_m
            )
            heading_delta = _wrap(end_planar.heading_rad - start_planar.heading_rad)
            localized_heading = start_planar.heading_rad + fraction * heading_delta
            position_closure = math.hypot(
                localized_x - initial_planar.x_position_m,
                localized_y - initial_planar.y_position_m,
            )
            heading_closure = abs(_wrap(localized_heading - initial_planar.heading_rad))
            finish = LapFinishEvidence(
                target,
                previous_progress,
                unwrapped,
                fraction,
                start_planar.time_s + fraction * config.time_step_s,
                localized_x,
                localized_y,
                localized_heading,
                position_closure,
                heading_closure,
            )
            if require_loop_closure and (
                position_closure > config.finish_position_tolerance_m
                or heading_closure > config.finish_heading_tolerance_rad
            ):
                outcome, terminal = "DNF", "loop_closure_failure"
            else:
                outcome, terminal = "finished", (
                    "lap_complete" if require_loop_closure else "segment_complete"
                )
            if not trace or trace[-1] != record:
                trace.append(record)
            previous_progress = target
            break
        previous_progress = unwrapped
        if end_planar.time_s >= config.timeout_s - 1.0e-12:
            outcome, terminal = "DNF", "timeout"
            if not trace or trace[-1] != record:
                trace.append(record)
            break
    if outcome == "running":
        outcome, terminal = "DNF", "timeout"
    status = "failed" if outcome == "invalid" or maximum_energy > config.energy_relative_tolerance else "passed"
    elapsed = finish.localized_time_s if finish is not None and outcome == "finished" else state.coupled.planar.time_s
    credited = target if outcome == "finished" else previous_progress
    body = {
        "model_version": MODEL_VERSION,
        "protocol_id": config.protocol_id,
        "corridor_id": corridor.corridor_id,
        "status": status,
        "outcome": outcome,
        "terminal_reason": terminal,
        "target_progress_m": target,
        "executed_steps": executed,
        "elapsed_time_s": elapsed,
        "credited_progress_m": credited,
        "maximum_abs_cross_track_error_m": maximum_cross,
        "maximum_abs_heading_error_rad": maximum_heading,
        "steering_saturation_count": saturation_count,
        "minimum_actual_normal_load_n": minimum_load,
        "maximum_abs_suspension_travel_m": maximum_travel,
        "maximum_total_global_relative_energy_residual": maximum_energy,
        "maximum_abs_progress_spatial_residual_m": maximum_progress_residual,
        "finish": None if finish is None else asdict(finish),
        "final_state": asdict(state),
        "trace": [asdict(item) for item in trace],
    }
    identity = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    return IntegratedLapRunResult(
        MODEL_VERSION,
        config.protocol_id,
        corridor.corridor_id,
        status,
        outcome,
        terminal,
        target,
        executed,
        elapsed,
        credited,
        maximum_cross,
        maximum_heading,
        saturation_count,
        minimum_load,
        maximum_travel,
        maximum_energy,
        maximum_progress_residual,
        finish,
        state,
        tuple(trace),
        identity,
    )


def result_to_mapping(result: IntegratedLapRunResult) -> dict[str, Any]:
    return asdict(result)
