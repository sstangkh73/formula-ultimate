"""Transient, energy-audited functional powertrain specimen for Work 067."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from typing import Any, Mapping, Sequence


MODEL_VERSION = "functional_powertrain_dynamics_v1"


class PowertrainDynamicsError(ValueError):
    """Raised when a powertrain declaration or runtime input is invalid."""


def _finite(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PowertrainDynamicsError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise PowertrainDynamicsError(f"{name} must be finite")
    return result


def _positive(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result <= 0.0:
        raise PowertrainDynamicsError(f"{name} must be positive")
    return result


def _nonnegative(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result < 0.0:
        raise PowertrainDynamicsError(f"{name} must be non-negative")
    return result


def _unit_interval(name: str, value: Any, *, allow_zero: bool = False) -> float:
    result = _nonnegative(name, value)
    if result > 1.0 or (not allow_zero and result == 0.0):
        boundary = "[0, 1]" if allow_zero else "(0, 1]"
        raise PowertrainDynamicsError(f"{name} must be in {boundary}")
    return result


def _curve(name: str, raw: Any, *, y_unit_interval: bool = False) -> tuple[tuple[float, float], ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)) or len(raw) < 2:
        raise PowertrainDynamicsError(f"{name} must contain at least two points")
    points: list[tuple[float, float]] = []
    for index, item in enumerate(raw):
        if not isinstance(item, Sequence) or isinstance(item, (str, bytes)) or len(item) != 2:
            raise PowertrainDynamicsError(f"{name}[{index}] must contain x and y")
        x = _nonnegative(f"{name}[{index}].x", item[0])
        y = _unit_interval(f"{name}[{index}].y", item[1]) if y_unit_interval else _nonnegative(f"{name}[{index}].y", item[1])
        points.append((x, y))
    if any(points[index][0] >= points[index + 1][0] for index in range(len(points) - 1)):
        raise PowertrainDynamicsError(f"{name} x values must be strictly increasing")
    return tuple(points)


def interpolate_curve(points: Sequence[tuple[float, float]], x: float) -> float:
    """Piecewise-linear interpolation with endpoint hold."""

    value = _nonnegative("curve query", x)
    if value <= points[0][0]:
        return points[0][1]
    if value >= points[-1][0]:
        return points[-1][1]
    for left, right in zip(points, points[1:]):
        if left[0] <= value <= right[0]:
            fraction = (value - left[0]) / (right[0] - left[0])
            return left[1] + fraction * (right[1] - left[1])
    raise AssertionError("validated curve interval was not found")


@dataclass(frozen=True, slots=True)
class PowertrainConfig:
    protocol_id: str
    initial_storage_energy_j: float
    maximum_storage_power_w: float
    electrical_connection_efficiency: float
    torque_speed_curve_nm: tuple[tuple[float, float], ...]
    converter_efficiency_curve: tuple[tuple[float, float], ...]
    converter_maximum_input_power_w: float
    converter_maximum_output_power_w: float
    converter_inertia_kg_m2: float
    converter_viscous_coefficient_nm_per_rad_s: float
    shaft_stiffness_nm_per_rad: float
    shaft_damping_nm_s_per_rad: float
    shaft_efficiency: float
    shaft_maximum_torque_nm: float
    shaft_maximum_twist_rad: float
    transmission_ratio: float
    transmission_efficiency: float
    transmission_maximum_input_torque_nm: float
    transmission_maximum_output_torque_nm: float
    transmission_maximum_input_speed_rad_s: float
    transmission_maximum_output_speed_rad_s: float
    output_inertia_kg_m2: float
    output_viscous_coefficient_nm_per_rad_s: float
    ambient_temperature_k: float
    converter_heat_capacity_j_per_k: float
    converter_cooling_w_per_k: float
    converter_maximum_temperature_k: float
    transmission_heat_capacity_j_per_k: float
    transmission_cooling_w_per_k: float
    transmission_maximum_temperature_k: float
    energy_relative_tolerance: float
    refinement_relative_tolerance: float


@dataclass(frozen=True, slots=True)
class PowertrainState:
    time_s: float
    storage_energy_j: float
    converter_angle_rad: float
    converter_speed_rad_s: float
    output_angle_rad: float
    output_speed_rad_s: float
    converter_temperature_k: float
    transmission_temperature_k: float
    connection_failed: bool
    failure_code: str | None
    failure_time_s: float | None
    useful_work_j: float
    rejected_heat_j: float
    source_energy_used_j: float
    electrical_connection_heat_j: float
    converter_conversion_heat_j: float
    converter_viscous_heat_j: float
    shaft_damping_heat_j: float
    shaft_efficiency_heat_j: float
    transmission_efficiency_heat_j: float
    output_viscous_heat_j: float
    fracture_heat_j: float


@dataclass(frozen=True, slots=True)
class StepEvidence:
    time_s: float
    throttle: float
    requested_load_torque_nm: float
    applied_load_torque_nm: float
    converter_torque_nm: float
    connection_demand_torque_nm: float
    shaft_torque_nm: float
    output_drive_torque_nm: float
    shaft_twist_rad: float
    storage_power_w: float
    converter_mechanical_power_w: float
    generated_heat_w: float
    rejected_heat_w: float
    energy_residual_j: float
    relative_energy_residual: float
    failure_code: str | None


@dataclass(frozen=True, slots=True)
class PowertrainRunResult:
    model_version: str
    protocol_id: str
    status: str
    terminal_reason: str
    duration_s: float
    step_s: float
    requested_steps: int
    executed_steps: int
    initial_energy_j: float
    final_state: PowertrainState
    maximum_abs_energy_residual_j: float
    maximum_relative_energy_residual: float
    maximum_abs_connection_demand_torque_nm: float
    maximum_abs_shaft_torque_nm: float
    maximum_abs_shaft_twist_rad: float
    maximum_output_drive_torque_nm: float
    trace: tuple[StepEvidence, ...]
    result_sha256: str


def _section(raw: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    value = raw.get(name)
    if not isinstance(value, Mapping):
        raise PowertrainDynamicsError(f"missing section {name}")
    return value


def load_powertrain_config(raw: Mapping[str, Any]) -> PowertrainConfig:
    if raw.get("model_version") != MODEL_VERSION:
        raise PowertrainDynamicsError("powertrain model version mismatch")
    storage = _section(raw, "energy_storage")
    electrical = _section(raw, "electrical_connection")
    converter = _section(raw, "energy_converter")
    shaft = _section(raw, "compliant_connection")
    transmission = _section(raw, "transmission")
    thermal = _section(raw, "thermal")
    numerical = _section(raw, "numerical")
    converter_thermal = _section(thermal, "converter")
    transmission_thermal = _section(thermal, "transmission")
    config = PowertrainConfig(
        protocol_id=str(raw.get("protocol_id", "")),
        initial_storage_energy_j=_nonnegative("initial_storage_energy_j", storage.get("initial_energy_j")),
        maximum_storage_power_w=_positive("maximum_storage_power_w", storage.get("maximum_output_power_w")),
        electrical_connection_efficiency=_unit_interval("electrical_connection_efficiency", electrical.get("efficiency")),
        torque_speed_curve_nm=_curve("torque_speed_curve_nm", converter.get("torque_speed_curve_nm")),
        converter_efficiency_curve=_curve("converter_efficiency_curve", converter.get("efficiency_curve"), y_unit_interval=True),
        converter_maximum_input_power_w=_positive("converter_maximum_input_power_w", converter.get("maximum_input_power_w")),
        converter_maximum_output_power_w=_positive("converter_maximum_output_power_w", converter.get("maximum_output_power_w")),
        converter_inertia_kg_m2=_positive("converter_inertia_kg_m2", converter.get("inertia_kg_m2")),
        converter_viscous_coefficient_nm_per_rad_s=_nonnegative("converter_viscous_coefficient", converter.get("viscous_coefficient_nm_per_rad_s")),
        shaft_stiffness_nm_per_rad=_positive("shaft_stiffness_nm_per_rad", shaft.get("stiffness_nm_per_rad")),
        shaft_damping_nm_s_per_rad=_nonnegative("shaft_damping_nm_s_per_rad", shaft.get("damping_nm_s_per_rad")),
        shaft_efficiency=_unit_interval("shaft_efficiency", shaft.get("efficiency")),
        shaft_maximum_torque_nm=_positive("shaft_maximum_torque_nm", shaft.get("maximum_torque_nm")),
        shaft_maximum_twist_rad=_positive("shaft_maximum_twist_rad", shaft.get("maximum_twist_rad")),
        transmission_ratio=_positive("transmission_ratio", transmission.get("ratio")),
        transmission_efficiency=_unit_interval("transmission_efficiency", transmission.get("efficiency")),
        transmission_maximum_input_torque_nm=_positive("transmission_maximum_input_torque_nm", transmission.get("maximum_input_torque_nm")),
        transmission_maximum_output_torque_nm=_positive("transmission_maximum_output_torque_nm", transmission.get("maximum_output_torque_nm")),
        transmission_maximum_input_speed_rad_s=_positive("transmission_maximum_input_speed_rad_s", transmission.get("maximum_input_speed_rad_s")),
        transmission_maximum_output_speed_rad_s=_positive("transmission_maximum_output_speed_rad_s", transmission.get("maximum_output_speed_rad_s")),
        output_inertia_kg_m2=_positive("output_inertia_kg_m2", transmission.get("output_inertia_kg_m2")),
        output_viscous_coefficient_nm_per_rad_s=_nonnegative("output_viscous_coefficient", transmission.get("output_viscous_coefficient_nm_per_rad_s")),
        ambient_temperature_k=_positive("ambient_temperature_k", thermal.get("ambient_temperature_k")),
        converter_heat_capacity_j_per_k=_positive("converter_heat_capacity_j_per_k", converter_thermal.get("heat_capacity_j_per_k")),
        converter_cooling_w_per_k=_nonnegative("converter_cooling_w_per_k", converter_thermal.get("cooling_w_per_k")),
        converter_maximum_temperature_k=_positive("converter_maximum_temperature_k", converter_thermal.get("maximum_temperature_k")),
        transmission_heat_capacity_j_per_k=_positive("transmission_heat_capacity_j_per_k", transmission_thermal.get("heat_capacity_j_per_k")),
        transmission_cooling_w_per_k=_nonnegative("transmission_cooling_w_per_k", transmission_thermal.get("cooling_w_per_k")),
        transmission_maximum_temperature_k=_positive("transmission_maximum_temperature_k", transmission_thermal.get("maximum_temperature_k")),
        energy_relative_tolerance=_positive("energy_relative_tolerance", numerical.get("energy_relative_tolerance")),
        refinement_relative_tolerance=_positive("refinement_relative_tolerance", numerical.get("refinement_relative_tolerance")),
    )
    if not config.protocol_id.strip():
        raise PowertrainDynamicsError("protocol_id must be nonblank")
    if config.torque_speed_curve_nm[0][0] != 0.0:
        raise PowertrainDynamicsError("torque-speed curve must begin at zero speed")
    if config.torque_speed_curve_nm[-1][1] != 0.0:
        raise PowertrainDynamicsError("torque-speed curve must end at zero torque")
    if config.converter_efficiency_curve[0][0] != 0.0 or config.converter_efficiency_curve[-1][0] != 1.0:
        raise PowertrainDynamicsError("efficiency curve must cover load fraction [0, 1]")
    if config.converter_maximum_output_power_w > config.converter_maximum_input_power_w:
        raise PowertrainDynamicsError("converter creates undeclared power")
    if config.transmission_maximum_output_torque_nm > config.transmission_ratio * config.transmission_maximum_input_torque_nm:
        raise PowertrainDynamicsError("transmission creates undeclared torque")
    if config.converter_maximum_input_power_w > config.maximum_storage_power_w * config.electrical_connection_efficiency + 1.0e-12:
        raise PowertrainDynamicsError("converter input exceeds connected storage power")
    if config.converter_maximum_temperature_k <= config.ambient_temperature_k or config.transmission_maximum_temperature_k <= config.ambient_temperature_k:
        raise PowertrainDynamicsError("maximum temperatures must exceed ambient")
    if config.energy_relative_tolerance > 1.0e-3 or config.refinement_relative_tolerance > 0.02:
        raise PowertrainDynamicsError("numerical tolerance exceeds protocol ceiling")
    return config


def initial_powertrain_state(config: PowertrainConfig, *, storage_energy_j: float | None = None) -> PowertrainState:
    energy = config.initial_storage_energy_j if storage_energy_j is None else _nonnegative("storage_energy_j", storage_energy_j)
    return PowertrainState(
        0.0, energy, 0.0, 0.0, 0.0, 0.0,
        config.ambient_temperature_k, config.ambient_temperature_k,
        False, None, None, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    )


def shaft_twist_rad(config: PowertrainConfig, state: PowertrainState) -> float:
    return state.converter_angle_rad - config.transmission_ratio * state.output_angle_rad


def _stored_mechanical_energy(config: PowertrainConfig, state: PowertrainState) -> float:
    elastic = 0.0 if state.connection_failed else 0.5 * config.shaft_stiffness_nm_per_rad * shaft_twist_rad(config, state) ** 2
    return (
        0.5 * config.converter_inertia_kg_m2 * state.converter_speed_rad_s ** 2
        + 0.5 * config.output_inertia_kg_m2 * state.output_speed_rad_s ** 2
        + elastic
    )


def _stored_thermal_energy(config: PowertrainConfig, state: PowertrainState) -> float:
    return (
        config.converter_heat_capacity_j_per_k * (state.converter_temperature_k - config.ambient_temperature_k)
        + config.transmission_heat_capacity_j_per_k * (state.transmission_temperature_k - config.ambient_temperature_k)
    )


def total_accounted_energy_j(config: PowertrainConfig, state: PowertrainState) -> float:
    return (
        state.storage_energy_j + _stored_mechanical_energy(config, state)
        + _stored_thermal_energy(config, state) + state.useful_work_j + state.rejected_heat_j
    )


def energy_residual_j(config: PowertrainConfig, state: PowertrainState, initial_energy_j: float) -> float:
    return initial_energy_j - total_accounted_energy_j(config, state)


def analytical_power_partition(config: PowertrainConfig, *, throttle: float, converter_speed_rad_s: float) -> dict[str, float]:
    command = _unit_interval("throttle", throttle, allow_zero=True)
    speed = _nonnegative("converter_speed_rad_s", converter_speed_rad_s)
    available_torque = interpolate_curve(config.torque_speed_curve_nm, speed)
    requested_torque = command * available_torque
    load_fraction = 0.0 if available_torque == 0.0 else requested_torque / available_torque
    converter_efficiency = interpolate_curve(config.converter_efficiency_curve, load_fraction)
    maximum_mechanical_power = min(
        config.converter_maximum_output_power_w,
        config.converter_maximum_input_power_w * converter_efficiency,
        config.maximum_storage_power_w * config.electrical_connection_efficiency * converter_efficiency,
    )
    mechanical_power = min(requested_torque * speed, maximum_mechanical_power)
    converter_torque = 0.0 if speed == 0.0 else mechanical_power / speed
    converter_input_power = mechanical_power / converter_efficiency if converter_efficiency > 0.0 else 0.0
    storage_power = converter_input_power / config.electrical_connection_efficiency if converter_input_power > 0.0 else 0.0
    electrical_heat = storage_power - converter_input_power
    converter_heat = converter_input_power - mechanical_power
    shaft_output_power = mechanical_power * config.shaft_efficiency
    shaft_heat = mechanical_power - shaft_output_power
    output_power = shaft_output_power * config.transmission_efficiency
    transmission_heat = shaft_output_power - output_power
    residual = storage_power - output_power - electrical_heat - converter_heat - shaft_heat - transmission_heat
    return {
        "converter_torque_nm": converter_torque,
        "storage_power_w": storage_power,
        "converter_input_power_w": converter_input_power,
        "converter_mechanical_power_w": mechanical_power,
        "output_speed_rad_s": speed / config.transmission_ratio,
        "output_torque_nm": converter_torque * config.transmission_ratio * config.shaft_efficiency * config.transmission_efficiency,
        "electrical_connection_heat_w": electrical_heat,
        "converter_heat_w": converter_heat,
        "shaft_efficiency_heat_w": shaft_heat,
        "transmission_heat_w": transmission_heat,
        "power_residual_w": residual,
    }


def _terminal_failure(config: PowertrainConfig, state: PowertrainState) -> str | None:
    if state.converter_speed_rad_s > config.transmission_maximum_input_speed_rad_s:
        return "converter_overspeed"
    if state.output_speed_rad_s > config.transmission_maximum_output_speed_rad_s:
        return "transmission_output_overspeed"
    if state.converter_temperature_k > config.converter_maximum_temperature_k:
        return "converter_overtemperature"
    if state.transmission_temperature_k > config.transmission_maximum_temperature_k:
        return "transmission_overtemperature"
    return None


def step_powertrain(
    config: PowertrainConfig,
    state: PowertrainState,
    *,
    throttle: float,
    requested_load_torque_nm: float,
    step_s: float,
    initial_energy_j: float,
) -> tuple[PowertrainState, StepEvidence]:
    command = _unit_interval("throttle", throttle, allow_zero=True)
    requested_load = _nonnegative("requested_load_torque_nm", requested_load_torque_nm)
    dt = _positive("step_s", step_s)
    for name, value in asdict(state).items():
        if isinstance(value, float) and not math.isfinite(value):
            raise PowertrainDynamicsError(f"state {name} must be finite")
    if state.converter_speed_rad_s < 0.0 or state.output_speed_rad_s < 0.0:
        raise PowertrainDynamicsError("reverse rotation is outside Work 067 scope")

    old_twist = shaft_twist_rad(config, state)
    relative_speed = state.converter_speed_rad_s - config.transmission_ratio * state.output_speed_rad_s
    raw_shaft_torque = 0.0 if state.connection_failed else (
        config.shaft_stiffness_nm_per_rad * old_twist + config.shaft_damping_nm_s_per_rad * relative_speed
    )
    breaks_now = (
        not state.connection_failed
        and (abs(raw_shaft_torque) > config.shaft_maximum_torque_nm or abs(old_twist) > config.shaft_maximum_twist_rad)
    )
    new_failure_code = "shaft_connection_failure" if breaks_now else None
    failed = state.connection_failed or breaks_now
    shaft_torque = 0.0 if failed else raw_shaft_torque
    fracture_heat = 0.0
    if breaks_now:
        fracture_heat = 0.5 * config.shaft_stiffness_nm_per_rad * old_twist * old_twist

    available_torque = interpolate_curve(config.torque_speed_curve_nm, state.converter_speed_rad_s)
    converter_torque = 0.0 if state.storage_energy_j <= 0.0 else command * available_torque
    load_fraction = 0.0 if available_torque <= 0.0 else converter_torque / available_torque
    converter_efficiency = interpolate_curve(config.converter_efficiency_curve, load_fraction)
    mechanical_power_limit = min(
        config.converter_maximum_output_power_w,
        config.converter_maximum_input_power_w * converter_efficiency,
        config.maximum_storage_power_w * config.electrical_connection_efficiency * converter_efficiency,
    )
    converter_torque = min(converter_torque, mechanical_power_limit / max(state.converter_speed_rad_s, 1.0))

    motor_resistance = shaft_torque + config.converter_viscous_coefficient_nm_per_rad_s * state.converter_speed_rad_s
    maximum_source_energy = min(state.storage_energy_j, config.maximum_storage_power_w * dt)

    def motor_trial(torque: float) -> tuple[float, float]:
        acceleration = (torque - motor_resistance) / config.converter_inertia_kg_m2
        new_speed = max(0.0, state.converter_speed_rad_s + acceleration * dt)
        work = max(0.0, torque * 0.5 * (state.converter_speed_rad_s + new_speed) * dt)
        source = work / (config.electrical_connection_efficiency * converter_efficiency) if work > 0.0 else 0.0
        return new_speed, source

    _, trial_source = motor_trial(converter_torque)
    if trial_source > maximum_source_energy + 1.0e-15:
        low, high = 0.0, converter_torque
        for _ in range(60):
            middle = 0.5 * (low + high)
            if motor_trial(middle)[1] <= maximum_source_energy:
                low = middle
            else:
                high = middle
        converter_torque = low
    new_converter_speed, source_energy = motor_trial(converter_torque)
    source_energy = min(source_energy, state.storage_energy_j)
    converter_mechanical_work = source_energy * config.electrical_connection_efficiency * converter_efficiency
    converter_input_energy = source_energy * config.electrical_connection_efficiency
    electrical_heat = source_energy - converter_input_energy
    converter_conversion_heat = converter_input_energy - converter_mechanical_work

    ideal_output_torque = config.transmission_ratio * shaft_torque
    output_drive_torque = ideal_output_torque * config.shaft_efficiency * config.transmission_efficiency
    if abs(shaft_torque) > config.transmission_maximum_input_torque_nm or abs(output_drive_torque) > config.transmission_maximum_output_torque_nm:
        failed = True
        breaks_now = True
        new_failure_code = "transmission_overtorque"
        fracture_heat += 0.5 * config.shaft_stiffness_nm_per_rad * old_twist * old_twist
        shaft_torque = 0.0
        output_drive_torque = 0.0
    output_resistance = config.output_viscous_coefficient_nm_per_rad_s * state.output_speed_rad_s
    maximum_nonreversing_load = max(0.0, output_drive_torque - output_resistance + config.output_inertia_kg_m2 * state.output_speed_rad_s / dt)
    applied_load = min(requested_load, maximum_nonreversing_load)
    output_acceleration = (output_drive_torque - applied_load - output_resistance) / config.output_inertia_kg_m2
    new_output_speed = max(0.0, state.output_speed_rad_s + output_acceleration * dt)
    new_converter_angle = state.converter_angle_rad + 0.5 * (state.converter_speed_rad_s + new_converter_speed) * dt
    new_output_angle = state.output_angle_rad + 0.5 * (state.output_speed_rad_s + new_output_speed) * dt

    mean_converter_speed = 0.5 * (state.converter_speed_rad_s + new_converter_speed)
    mean_output_speed = 0.5 * (state.output_speed_rad_s + new_output_speed)
    mean_relative_speed = mean_converter_speed - config.transmission_ratio * mean_output_speed
    useful_work = applied_load * mean_output_speed * dt
    converter_viscous_heat = config.converter_viscous_coefficient_nm_per_rad_s * mean_converter_speed ** 2 * dt
    shaft_damping_heat = 0.0 if failed else config.shaft_damping_nm_s_per_rad * mean_relative_speed ** 2 * dt
    ideal_forward_energy = max(0.0, shaft_torque * config.transmission_ratio * mean_output_speed * dt)
    shaft_efficiency_heat = ideal_forward_energy * (1.0 - config.shaft_efficiency)
    transmission_input_energy = ideal_forward_energy * config.shaft_efficiency
    transmission_efficiency_heat = transmission_input_energy * (1.0 - config.transmission_efficiency)
    output_viscous_heat = config.output_viscous_coefficient_nm_per_rad_s * mean_output_speed ** 2 * dt

    converter_generated_heat = electrical_heat + converter_conversion_heat + converter_viscous_heat
    transmission_generated_heat = (
        shaft_damping_heat + shaft_efficiency_heat + transmission_efficiency_heat + output_viscous_heat + fracture_heat
    )
    converter_rejected = min(
        config.converter_cooling_w_per_k * max(0.0, state.converter_temperature_k - config.ambient_temperature_k) * dt,
        config.converter_heat_capacity_j_per_k * max(0.0, state.converter_temperature_k - config.ambient_temperature_k) + converter_generated_heat,
    )
    transmission_rejected = min(
        config.transmission_cooling_w_per_k * max(0.0, state.transmission_temperature_k - config.ambient_temperature_k) * dt,
        config.transmission_heat_capacity_j_per_k * max(0.0, state.transmission_temperature_k - config.ambient_temperature_k) + transmission_generated_heat,
    )
    converter_temperature = state.converter_temperature_k + (converter_generated_heat - converter_rejected) / config.converter_heat_capacity_j_per_k
    transmission_temperature = state.transmission_temperature_k + (transmission_generated_heat - transmission_rejected) / config.transmission_heat_capacity_j_per_k

    failure_code = state.failure_code
    failure_time = state.failure_time_s
    if breaks_now and failure_code is None:
        failure_code, failure_time = new_failure_code, state.time_s + dt
    provisional = PowertrainState(
        time_s=state.time_s + dt,
        storage_energy_j=state.storage_energy_j - source_energy,
        converter_angle_rad=new_converter_angle,
        converter_speed_rad_s=new_converter_speed,
        output_angle_rad=new_output_angle,
        output_speed_rad_s=new_output_speed,
        converter_temperature_k=converter_temperature,
        transmission_temperature_k=transmission_temperature,
        connection_failed=failed,
        failure_code=failure_code,
        failure_time_s=failure_time,
        useful_work_j=state.useful_work_j + useful_work,
        rejected_heat_j=state.rejected_heat_j + converter_rejected + transmission_rejected,
        source_energy_used_j=state.source_energy_used_j + source_energy,
        electrical_connection_heat_j=state.electrical_connection_heat_j + electrical_heat,
        converter_conversion_heat_j=state.converter_conversion_heat_j + converter_conversion_heat,
        converter_viscous_heat_j=state.converter_viscous_heat_j + converter_viscous_heat,
        shaft_damping_heat_j=state.shaft_damping_heat_j + shaft_damping_heat,
        shaft_efficiency_heat_j=state.shaft_efficiency_heat_j + shaft_efficiency_heat,
        transmission_efficiency_heat_j=state.transmission_efficiency_heat_j + transmission_efficiency_heat,
        output_viscous_heat_j=state.output_viscous_heat_j + output_viscous_heat,
        fracture_heat_j=state.fracture_heat_j + fracture_heat,
    )
    terminal = _terminal_failure(config, provisional)
    if terminal is not None and provisional.failure_code is None:
        provisional = PowertrainState(**{
            **asdict(provisional), "failure_code": terminal, "failure_time_s": provisional.time_s,
        })
    residual = energy_residual_j(config, provisional, initial_energy_j)
    relative = abs(residual) / max(abs(initial_energy_j), provisional.source_energy_used_j, 1.0)
    evidence = StepEvidence(
        provisional.time_s, command, requested_load, applied_load, converter_torque, raw_shaft_torque, shaft_torque,
        output_drive_torque, shaft_twist_rad(config, provisional), source_energy / dt,
        converter_mechanical_work / dt, (converter_generated_heat + transmission_generated_heat) / dt,
        (converter_rejected + transmission_rejected) / dt, residual, relative, provisional.failure_code,
    )
    return provisional, evidence


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def run_powertrain(
    config: PowertrainConfig,
    *,
    throttle: float,
    requested_load_torque_nm: float,
    duration_s: float,
    step_s: float,
    initial_storage_energy_j: float | None = None,
    sample_stride: int = 1,
    stop_on_failure: bool = True,
) -> PowertrainRunResult:
    duration = _positive("duration_s", duration_s)
    dt = _positive("step_s", step_s)
    if not isinstance(sample_stride, int) or isinstance(sample_stride, bool) or sample_stride <= 0:
        raise PowertrainDynamicsError("sample_stride must be a positive integer")
    step_count_float = duration / dt
    requested_steps = round(step_count_float)
    if requested_steps <= 0 or not math.isclose(step_count_float, requested_steps, rel_tol=0.0, abs_tol=1.0e-10):
        raise PowertrainDynamicsError("duration_s must be an integer multiple of step_s")
    state = initial_powertrain_state(config, storage_energy_j=initial_storage_energy_j)
    initial_energy = total_accounted_energy_j(config, state)
    trace: list[StepEvidence] = []
    max_residual = max_relative = max_demand = max_torque = max_twist = max_output = 0.0
    for index in range(requested_steps):
        state, evidence = step_powertrain(
            config, state, throttle=throttle, requested_load_torque_nm=requested_load_torque_nm,
            step_s=dt, initial_energy_j=initial_energy,
        )
        max_residual = max(max_residual, abs(evidence.energy_residual_j))
        max_relative = max(max_relative, evidence.relative_energy_residual)
        max_demand = max(max_demand, abs(evidence.connection_demand_torque_nm))
        max_torque = max(max_torque, abs(evidence.shaft_torque_nm))
        max_twist = max(max_twist, abs(evidence.shaft_twist_rad))
        max_output = max(max_output, abs(evidence.output_drive_torque_nm))
        if index % sample_stride == 0 or index == requested_steps - 1 or state.failure_code is not None:
            trace.append(evidence)
        if stop_on_failure and state.failure_code is not None:
            break
    status = "passed"
    reason = "completed"
    if state.failure_code is not None:
        status, reason = "failed", state.failure_code
    elif max_relative > config.energy_relative_tolerance:
        status, reason = "failed", "energy_conservation_residual"
    body = {
        "model_version": MODEL_VERSION,
        "protocol_id": config.protocol_id,
        "status": status,
        "terminal_reason": reason,
        "duration_s": duration,
        "step_s": dt,
        "requested_steps": requested_steps,
        "executed_steps": round(state.time_s / dt),
        "initial_energy_j": initial_energy,
        "final_state": asdict(state),
        "maximum_abs_energy_residual_j": max_residual,
        "maximum_relative_energy_residual": max_relative,
        "maximum_abs_connection_demand_torque_nm": max_demand,
        "maximum_abs_shaft_torque_nm": max_torque,
        "maximum_abs_shaft_twist_rad": max_twist,
        "maximum_output_drive_torque_nm": max_output,
        "trace": [asdict(item) for item in trace],
    }
    identity = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    return PowertrainRunResult(
        MODEL_VERSION, config.protocol_id, status, reason, duration, dt, requested_steps,
        body["executed_steps"], initial_energy, state, max_residual, max_relative,
        max_demand, max_torque, max_twist, max_output, tuple(trace), identity,
    )


def result_to_mapping(result: PowertrainRunResult) -> dict[str, Any]:
    return asdict(result)
