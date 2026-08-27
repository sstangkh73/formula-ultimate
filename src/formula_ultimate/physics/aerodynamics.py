"""Deterministic Level-0 aerodynamic map and ram-air cooling evaluator.

Coefficient provenance and envelope limits remain explicit.  This module does
not run CFD or turn a synthetic coefficient grid into physical validation.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import re


MODEL_VERSION = "work017-aerodynamic-map-v1"
EVIDENCE_BASES = frozenset(
    {"synthetic_reference", "geometry_derived", "cfd", "measured"}
)
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class AerodynamicInputError(ValueError):
    """Raised when an aerodynamic declaration violates the model contract."""


def _finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise AerodynamicInputError(f"{name} must be finite; received {value!r}")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise AerodynamicInputError(f"{name} must be > 0; received {value!r}")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise AerodynamicInputError(f"{name} must be >= 0; received {value!r}")


def _nonempty(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise AerodynamicInputError(f"{name} must be a non-empty string")


def _axis(name: str, values: tuple[float, ...], *, positive: bool) -> None:
    if not values:
        raise AerodynamicInputError(f"{name} must contain at least one node")
    for index, value in enumerate(values):
        (_positive if positive else _nonnegative)(f"{name}[{index}]", value)
    if any(current >= following for current, following in zip(values, values[1:])):
        raise AerodynamicInputError(f"{name} must be strictly increasing")


@dataclass(frozen=True, slots=True)
class AerodynamicEvidence:
    evidence_id: str
    basis: str
    source_reference: str
    geometry_sha256: str | None = None

    def __post_init__(self) -> None:
        _nonempty("evidence_id", self.evidence_id)
        _nonempty("basis", self.basis)
        _nonempty("source_reference", self.source_reference)
        if self.basis not in EVIDENCE_BASES:
            raise AerodynamicInputError(
                f"basis must be one of {sorted(EVIDENCE_BASES)!r}"
            )
        if self.geometry_sha256 is not None and not _SHA256_PATTERN.fullmatch(
            self.geometry_sha256
        ):
            raise AerodynamicInputError(
                "geometry_sha256 must be 64 lowercase hexadecimal characters"
            )
        if self.basis == "geometry_derived" and self.geometry_sha256 is None:
            raise AerodynamicInputError(
                "geometry_derived evidence requires geometry_sha256"
            )


@dataclass(frozen=True, slots=True)
class AerodynamicReference:
    reference_area_m2: float
    reference_length_m: float
    cooling_inlet_area_m2: float
    air_specific_heat_j_per_kg_k: float
    cooling_effectiveness: float

    def __post_init__(self) -> None:
        _positive("reference_area_m2", self.reference_area_m2)
        _positive("reference_length_m", self.reference_length_m)
        _nonnegative("cooling_inlet_area_m2", self.cooling_inlet_area_m2)
        _positive(
            "air_specific_heat_j_per_kg_k",
            self.air_specific_heat_j_per_kg_k,
        )
        _nonnegative("cooling_effectiveness", self.cooling_effectiveness)
        if self.cooling_effectiveness > 1.0:
            raise AerodynamicInputError("cooling_effectiveness must be <= 1")


@dataclass(frozen=True, slots=True)
class AerodynamicCoefficientSample:
    drag_coefficient: float
    side_force_coefficient: float
    downforce_coefficient: float
    pitching_moment_coefficient: float
    yawing_moment_coefficient: float
    cooling_flow_coefficient: float

    def __post_init__(self) -> None:
        _nonnegative("drag_coefficient", self.drag_coefficient)
        _finite("side_force_coefficient", self.side_force_coefficient)
        _finite("downforce_coefficient", self.downforce_coefficient)
        _finite(
            "pitching_moment_coefficient",
            self.pitching_moment_coefficient,
        )
        _finite("yawing_moment_coefficient", self.yawing_moment_coefficient)
        _nonnegative("cooling_flow_coefficient", self.cooling_flow_coefficient)


@dataclass(frozen=True, slots=True)
class AerodynamicStateGrid:
    active_state: str
    samples: tuple[AerodynamicCoefficientSample, ...]

    def __post_init__(self) -> None:
        _nonempty("active_state", self.active_state)
        samples = tuple(self.samples)
        object.__setattr__(self, "samples", samples)
        if not all(isinstance(sample, AerodynamicCoefficientSample) for sample in samples):
            raise AerodynamicInputError(
                "samples must contain only AerodynamicCoefficientSample values"
            )


@dataclass(frozen=True, slots=True)
class AerodynamicCoefficientMap:
    map_id: str
    airspeeds_m_per_s: tuple[float, ...]
    ride_heights_m: tuple[float, ...]
    yaw_angles_rad: tuple[float, ...]
    state_grids: tuple[AerodynamicStateGrid, ...]
    evidence: AerodynamicEvidence

    def __post_init__(self) -> None:
        _nonempty("map_id", self.map_id)
        airspeeds = tuple(self.airspeeds_m_per_s)
        ride_heights = tuple(self.ride_heights_m)
        yaw_angles = tuple(self.yaw_angles_rad)
        state_grids = tuple(self.state_grids)
        object.__setattr__(self, "airspeeds_m_per_s", airspeeds)
        object.__setattr__(self, "ride_heights_m", ride_heights)
        object.__setattr__(self, "yaw_angles_rad", yaw_angles)
        object.__setattr__(self, "state_grids", state_grids)
        _axis("airspeeds_m_per_s", airspeeds, positive=False)
        _axis("ride_heights_m", ride_heights, positive=False)
        if not yaw_angles:
            raise AerodynamicInputError(
                "yaw_angles_rad must contain at least one node"
            )
        for index, yaw in enumerate(yaw_angles):
            _finite(f"yaw_angles_rad[{index}]", yaw)
        if any(
            current >= following
            for current, following in zip(yaw_angles, yaw_angles[1:])
        ):
            raise AerodynamicInputError("yaw_angles_rad must be strictly increasing")
        if not state_grids:
            raise AerodynamicInputError("at least one active-state grid is required")
        if not all(isinstance(grid, AerodynamicStateGrid) for grid in state_grids):
            raise AerodynamicInputError(
                "state_grids must contain only AerodynamicStateGrid values"
            )
        state_names = [grid.active_state for grid in state_grids]
        if len(set(state_names)) != len(state_names):
            raise AerodynamicInputError("active_state values must be unique")
        expected_samples = len(airspeeds) * len(ride_heights) * len(yaw_angles)
        for grid in state_grids:
            if len(grid.samples) != expected_samples:
                raise AerodynamicInputError(
                    f"active state {grid.active_state!r} requires exactly "
                    f"{expected_samples} samples; received {len(grid.samples)}"
                )
        if not isinstance(self.evidence, AerodynamicEvidence):
            raise AerodynamicInputError(
                "evidence must be an AerodynamicEvidence instance"
            )


@dataclass(frozen=True, slots=True)
class AerodynamicOperatingPoint:
    airspeed_m_per_s: float
    air_density_kg_per_m3: float
    ride_height_m: float
    yaw_angle_rad: float
    active_state: str
    air_temperature_k: float
    component_temperature_k: float

    def __post_init__(self) -> None:
        _nonnegative("airspeed_m_per_s", self.airspeed_m_per_s)
        _positive("air_density_kg_per_m3", self.air_density_kg_per_m3)
        _nonnegative("ride_height_m", self.ride_height_m)
        _finite("yaw_angle_rad", self.yaw_angle_rad)
        _nonempty("active_state", self.active_state)
        _positive("air_temperature_k", self.air_temperature_k)
        _positive("component_temperature_k", self.component_temperature_k)


@dataclass(frozen=True, slots=True)
class AxisBracket:
    lower_index: int
    upper_index: int
    lower_value: float
    upper_value: float
    fraction: float


@dataclass(frozen=True, slots=True)
class AerodynamicInterpolationEvidence:
    active_state: str
    airspeed: AxisBracket
    ride_height: AxisBracket
    yaw_angle: AxisBracket
    exact_grid_node: bool


@dataclass(frozen=True, slots=True)
class AerodynamicResiduals:
    drag_force_n: float
    side_force_n: float
    downforce_n: float
    pitching_moment_n_m: float
    yawing_moment_n_m: float
    cooling_mass_flow_kg_per_s: float
    cooling_conductance_w_per_k: float
    heat_rejection_w: float


@dataclass(frozen=True, slots=True)
class AerodynamicResult:
    model_version: str
    status: str
    reason: str
    map_id: str
    evidence: AerodynamicEvidence
    operating_point: AerodynamicOperatingPoint
    interpolation: AerodynamicInterpolationEvidence | None
    coefficients: AerodynamicCoefficientSample | None
    dynamic_pressure_pa: float | None
    drag_force_n: float | None
    side_force_n: float | None
    downforce_n: float | None
    pitching_moment_n_m: float | None
    yawing_moment_n_m: float | None
    longitudinal_centre_of_pressure_m: float | None
    cooling_air_mass_flow_kg_per_s: float | None
    cooling_air_heat_capacity_rate_w_per_k: float | None
    cooling_effective_conductance_w_per_k: float | None
    cooling_heat_rejection_w: float | None
    residuals: AerodynamicResiduals | None


def _invalid_result(
    coefficient_map: AerodynamicCoefficientMap,
    operating_point: AerodynamicOperatingPoint,
    reason: str,
) -> AerodynamicResult:
    return AerodynamicResult(
        model_version=MODEL_VERSION,
        status="invalid",
        reason=reason,
        map_id=coefficient_map.map_id,
        evidence=coefficient_map.evidence,
        operating_point=operating_point,
        interpolation=None,
        coefficients=None,
        dynamic_pressure_pa=None,
        drag_force_n=None,
        side_force_n=None,
        downforce_n=None,
        pitching_moment_n_m=None,
        yawing_moment_n_m=None,
        longitudinal_centre_of_pressure_m=None,
        cooling_air_mass_flow_kg_per_s=None,
        cooling_air_heat_capacity_rate_w_per_k=None,
        cooling_effective_conductance_w_per_k=None,
        cooling_heat_rejection_w=None,
        residuals=None,
    )


def _bracket(axis: tuple[float, ...], value: float) -> AxisBracket | None:
    if value < axis[0] or value > axis[-1]:
        return None
    for index, node in enumerate(axis):
        if value == node:
            return AxisBracket(index, index, node, node, 0.0)
    for lower_index, (lower, upper) in enumerate(zip(axis, axis[1:])):
        if lower < value < upper:
            fraction = (value - lower) / (upper - lower)
            return AxisBracket(
                lower_index,
                lower_index + 1,
                lower,
                upper,
                fraction,
            )
    return None


def _weighted_indices(bracket: AxisBracket) -> tuple[tuple[int, float], ...]:
    if bracket.lower_index == bracket.upper_index:
        return ((bracket.lower_index, 1.0),)
    return (
        (bracket.lower_index, 1.0 - bracket.fraction),
        (bracket.upper_index, bracket.fraction),
    )


def _sample_index(
    speed_index: int,
    height_index: int,
    yaw_index: int,
    height_count: int,
    yaw_count: int,
) -> int:
    return (speed_index * height_count + height_index) * yaw_count + yaw_index


def _interpolate_sample(
    *,
    coefficient_map: AerodynamicCoefficientMap,
    grid: AerodynamicStateGrid,
    speed: AxisBracket,
    height: AxisBracket,
    yaw: AxisBracket,
) -> AerodynamicCoefficientSample:
    fields = (
        "drag_coefficient",
        "side_force_coefficient",
        "downforce_coefficient",
        "pitching_moment_coefficient",
        "yawing_moment_coefficient",
        "cooling_flow_coefficient",
    )
    weighted_values: dict[str, list[float]] = {field: [] for field in fields}
    height_count = len(coefficient_map.ride_heights_m)
    yaw_count = len(coefficient_map.yaw_angles_rad)
    for speed_index, speed_weight in _weighted_indices(speed):
        for height_index, height_weight in _weighted_indices(height):
            for yaw_index, yaw_weight in _weighted_indices(yaw):
                weight = speed_weight * height_weight * yaw_weight
                sample = grid.samples[
                    _sample_index(
                        speed_index,
                        height_index,
                        yaw_index,
                        height_count,
                        yaw_count,
                    )
                ]
                for field in fields:
                    weighted_values[field].append(weight * getattr(sample, field))
    return AerodynamicCoefficientSample(
        *(math.fsum(weighted_values[field]) for field in fields)
    )


def evaluate_aerodynamics(
    *,
    coefficient_map: AerodynamicCoefficientMap,
    reference: AerodynamicReference,
    operating_point: AerodynamicOperatingPoint,
) -> AerodynamicResult:
    """Interpolate one declared map point and resolve force/cooling outputs."""

    state_by_name = {
        grid.active_state: grid for grid in coefficient_map.state_grids
    }
    grid = state_by_name.get(operating_point.active_state)
    if grid is None:
        return _invalid_result(
            coefficient_map,
            operating_point,
            f"unknown active state {operating_point.active_state!r}",
        )
    speed = _bracket(
        coefficient_map.airspeeds_m_per_s,
        operating_point.airspeed_m_per_s,
    )
    height = _bracket(
        coefficient_map.ride_heights_m,
        operating_point.ride_height_m,
    )
    yaw = _bracket(
        coefficient_map.yaw_angles_rad,
        operating_point.yaw_angle_rad,
    )
    outside = [
        name
        for name, bracket in (
            ("airspeed", speed),
            ("ride height", height),
            ("yaw angle", yaw),
        )
        if bracket is None
    ]
    if outside:
        return _invalid_result(
            coefficient_map,
            operating_point,
            "operating point is outside the declared " + ", ".join(outside) + " envelope",
        )
    assert speed is not None and height is not None and yaw is not None
    interpolation = AerodynamicInterpolationEvidence(
        active_state=grid.active_state,
        airspeed=speed,
        ride_height=height,
        yaw_angle=yaw,
        exact_grid_node=all(
            bracket.lower_index == bracket.upper_index
            for bracket in (speed, height, yaw)
        ),
    )
    try:
        coefficients = _interpolate_sample(
            coefficient_map=coefficient_map,
            grid=grid,
            speed=speed,
            height=height,
            yaw=yaw,
        )
        dynamic_pressure = (
            0.5
            * operating_point.air_density_kg_per_m3
            * operating_point.airspeed_m_per_s**2
        )
        force_scale = dynamic_pressure * reference.reference_area_m2
        moment_scale = force_scale * reference.reference_length_m
        drag = force_scale * coefficients.drag_coefficient
        side = force_scale * coefficients.side_force_coefficient
        downforce = force_scale * coefficients.downforce_coefficient
        pitching_moment = moment_scale * coefficients.pitching_moment_coefficient
        yawing_moment = moment_scale * coefficients.yawing_moment_coefficient
        centre_of_pressure = (
            pitching_moment / downforce if downforce != 0.0 else None
        )
        mass_flow = (
            operating_point.air_density_kg_per_m3
            * operating_point.airspeed_m_per_s
            * reference.cooling_inlet_area_m2
            * coefficients.cooling_flow_coefficient
        )
        heat_capacity_rate = mass_flow * reference.air_specific_heat_j_per_kg_k
        cooling_conductance = (
            reference.cooling_effectiveness * heat_capacity_rate
        )
        heat_rejection = cooling_conductance * (
            operating_point.component_temperature_k
            - operating_point.air_temperature_k
        )
    except (OverflowError, ValueError, AerodynamicInputError) as exc:
        return _invalid_result(
            coefficient_map,
            operating_point,
            f"aerodynamic evaluation failed: {exc}",
        )
    values = (
        dynamic_pressure,
        drag,
        side,
        downforce,
        pitching_moment,
        yawing_moment,
        mass_flow,
        heat_capacity_rate,
        cooling_conductance,
        heat_rejection,
    )
    if centre_of_pressure is not None:
        values += (centre_of_pressure,)
    if not all(math.isfinite(value) for value in values):
        return _invalid_result(
            coefficient_map,
            operating_point,
            "aerodynamic evaluation produced a non-finite output",
        )

    residuals = AerodynamicResiduals(
        drag_force_n=drag - force_scale * coefficients.drag_coefficient,
        side_force_n=side - force_scale * coefficients.side_force_coefficient,
        downforce_n=downforce - force_scale * coefficients.downforce_coefficient,
        pitching_moment_n_m=(
            pitching_moment
            - moment_scale * coefficients.pitching_moment_coefficient
        ),
        yawing_moment_n_m=(
            yawing_moment - moment_scale * coefficients.yawing_moment_coefficient
        ),
        cooling_mass_flow_kg_per_s=(
            mass_flow
            - operating_point.air_density_kg_per_m3
            * operating_point.airspeed_m_per_s
            * reference.cooling_inlet_area_m2
            * coefficients.cooling_flow_coefficient
        ),
        cooling_conductance_w_per_k=(
            cooling_conductance
            - reference.cooling_effectiveness * heat_capacity_rate
        ),
        heat_rejection_w=(
            heat_rejection
            - cooling_conductance
            * (
                operating_point.component_temperature_k
                - operating_point.air_temperature_k
            )
        ),
    )
    if not all(
        math.isfinite(value) and abs(value) <= 1.0e-9
        for value in (
            residuals.drag_force_n,
            residuals.side_force_n,
            residuals.downforce_n,
            residuals.pitching_moment_n_m,
            residuals.yawing_moment_n_m,
            residuals.cooling_mass_flow_kg_per_s,
            residuals.cooling_conductance_w_per_k,
            residuals.heat_rejection_w,
        )
    ):
        return _invalid_result(
            coefficient_map,
            operating_point,
            f"declared aerodynamic residual exceeded tolerance: {residuals!r}",
        )
    return AerodynamicResult(
        model_version=MODEL_VERSION,
        status="ok",
        reason="operating point is inside the declared map and balances close",
        map_id=coefficient_map.map_id,
        evidence=coefficient_map.evidence,
        operating_point=operating_point,
        interpolation=interpolation,
        coefficients=coefficients,
        dynamic_pressure_pa=dynamic_pressure,
        drag_force_n=drag,
        side_force_n=side,
        downforce_n=downforce,
        pitching_moment_n_m=pitching_moment,
        yawing_moment_n_m=yawing_moment,
        longitudinal_centre_of_pressure_m=centre_of_pressure,
        cooling_air_mass_flow_kg_per_s=mass_flow,
        cooling_air_heat_capacity_rate_w_per_k=heat_capacity_rate,
        cooling_effective_conductance_w_per_k=cooling_conductance,
        cooling_heat_rejection_w=heat_rejection,
        residuals=residuals,
    )
