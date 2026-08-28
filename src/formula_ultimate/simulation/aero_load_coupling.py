"""Work 024 aerodynamic wrench and arbitrary-contact load coupling."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
import math

from formula_ultimate.physics.aerodynamics import (
    MODEL_VERSION as AERO_MODEL_VERSION,
    AerodynamicCoefficientMap,
    AerodynamicOperatingPoint,
    AerodynamicReference,
    AerodynamicResult,
    evaluate_aerodynamics,
)
from formula_ultimate.physics.lateral import (
    MODEL_VERSION as LOAD_MODEL_VERSION,
    PlanarVehicle,
)

from .coupling import ResidualEntry, SharedVehicleState
from .step_inputs import EnvironmentStepInputs
from .transaction import AdapterOutput, AdapterReadView, RuntimeSignal


class AeroLoadCouplingError(ValueError):
    """Raised for malformed Work 024 declarations."""


def _finite(name: str, value: float) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        raise AeroLoadCouplingError(f"{name} must be finite")


@dataclass(frozen=True, slots=True)
class AerodynamicReferenceOrigin:
    position_from_com_m: tuple[float, float, float]

    def __post_init__(self) -> None:
        if len(self.position_from_com_m) != 3:
            raise AeroLoadCouplingError("reference origin must be a three-vector")
        for value in self.position_from_com_m:
            _finite("reference origin", value)


@dataclass(frozen=True, slots=True)
class AerodynamicQueryEvidence:
    raw_airspeed_m_per_s: float
    queried_airspeed_m_per_s: float
    raw_yaw_angle_rad: float
    queried_yaw_angle_rad: float
    numerically_snapped_axes: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("raw_airspeed_m_per_s", "queried_airspeed_m_per_s",
                     "raw_yaw_angle_rad", "queried_yaw_angle_rad"):
            _finite(name, getattr(self, name))
        if self.raw_airspeed_m_per_s < 0 or self.queried_airspeed_m_per_s < 0:
            raise AeroLoadCouplingError("airspeed evidence must be non-negative")
        allowed = {"airspeed", "ride_height", "yaw_angle"}
        if len(set(self.numerically_snapped_axes)) != len(self.numerically_snapped_axes) or not set(self.numerically_snapped_axes) <= allowed:
            raise AeroLoadCouplingError("invalid numerical snap axis evidence")


@dataclass(frozen=True, slots=True)
class AerodynamicChassisWrench:
    force_body_n: tuple[float, float, float]
    moment_about_com_n_m: tuple[float, float, float]
    map_id: str
    evidence_id: str
    query_evidence: AerodynamicQueryEvidence | None = None

    def __post_init__(self) -> None:
        for name, vector in (("force_body_n", self.force_body_n), ("moment_about_com_n_m", self.moment_about_com_n_m)):
            if len(vector) != 3:
                raise AeroLoadCouplingError(f"{name} must be a three-vector")
            for value in vector: _finite(name, value)
        if not self.map_id.strip() or not self.evidence_id.strip():
            raise AeroLoadCouplingError("wrench map/evidence IDs must not be blank")


@dataclass(frozen=True, slots=True)
class AerodynamicCoolingEvidence:
    mass_flow_kg_per_s: float
    conductance_w_per_k: float
    heat_rejection_w: float
    map_id: str
    evidence_id: str

    def __post_init__(self) -> None:
        for name in ("mass_flow_kg_per_s", "conductance_w_per_k", "heat_rejection_w"):
            _finite(name, getattr(self, name))
        if self.mass_flow_kg_per_s < 0 or self.conductance_w_per_k < 0:
            raise AeroLoadCouplingError("cooling flow/conductance must be non-negative")


@dataclass(frozen=True, slots=True)
class ContactNormalLoad:
    contact_id: str
    normal_load_n: float

    def __post_init__(self) -> None:
        if not self.contact_id.strip(): raise AeroLoadCouplingError("contact_id must not be blank")
        _finite("normal_load_n", self.normal_load_n)


@dataclass(frozen=True, slots=True)
class AeroLoadBalanceResiduals:
    vertical_force_n: float
    pitch_moment_n_m: float
    roll_moment_n_m: float

    def __post_init__(self) -> None:
        for name in ("vertical_force_n", "pitch_moment_n_m", "roll_moment_n_m"):
            _finite(name, getattr(self, name))

    def entries(self) -> tuple[ResidualEntry, ...]:
        return (
            ResidualEntry("aero-load.vertical", "force", self.vertical_force_n, "N", 1e-6, 1e-10, 1.0),
            ResidualEntry("aero-load.pitch", "moment", self.pitch_moment_n_m, "N*m", 1e-5, 1e-10, 1.0),
            ResidualEntry("aero-load.roll", "moment", self.roll_moment_n_m, "N*m", 1e-5, 1e-10, 1.0),
        )


@dataclass(frozen=True, slots=True)
class AeroLoadCouplingResult:
    status: str
    reason: str
    wrench: AerodynamicChassisWrench | None
    cooling: AerodynamicCoolingEvidence | None
    contact_loads: tuple[ContactNormalLoad, ...]
    residuals: AeroLoadBalanceResiduals | None


def moist_air_density_kg_per_m3(temperature_k: float, pressure_pa: float, relative_humidity: float) -> float:
    """Moist-air density using Tetens saturation pressure and ideal-gas mixture."""
    for name, value in (("temperature_k", temperature_k), ("pressure_pa", pressure_pa), ("relative_humidity", relative_humidity)):
        _finite(name, value)
    if temperature_k <= 0 or pressure_pa <= 0 or not 0 <= relative_humidity <= 1:
        raise AeroLoadCouplingError("invalid atmospheric state")
    temperature_c = temperature_k - 273.15
    saturation_pa = 610.94 * math.exp(17.625 * temperature_c / (temperature_c + 243.04))
    vapor_pa = relative_humidity * saturation_pa
    if vapor_pa >= pressure_pa:
        raise AeroLoadCouplingError("water-vapor pressure must be below total pressure")
    density = (pressure_pa - vapor_pa) / (287.05287 * temperature_k) + vapor_pa / (461.5 * temperature_k)
    if not math.isfinite(density) or density <= 0:
        raise AeroLoadCouplingError("air density calculation failed")
    return density


def _snap_to_declared_node(value: float, axis: tuple[float, ...]) -> tuple[float, bool]:
    nearest = min(axis, key=lambda node: abs(node - value))
    tolerance = 1e-12 * max(1.0, abs(nearest), abs(value))
    return (nearest, True) if abs(nearest - value) <= tolerance else (value, False)


def translate_aerodynamic_result(result: AerodynamicResult, origin: AerodynamicReferenceOrigin) -> tuple[AerodynamicChassisWrench, AerodynamicCoolingEvidence]:
    if result.status != "ok":
        raise AeroLoadCouplingError(f"aerodynamic map result is invalid: {result.reason}")
    required = (result.drag_force_n, result.side_force_n, result.downforce_n,
                result.pitching_moment_n_m, result.yawing_moment_n_m,
                result.cooling_air_mass_flow_kg_per_s,
                result.cooling_effective_conductance_w_per_k,
                result.cooling_heat_rejection_w)
    if any(value is None for value in required):
        raise AeroLoadCouplingError("successful aerodynamic result is incomplete")
    drag, side, down, pitch, yaw, flow, conductance, heat = required
    force = (-drag, side, -down)
    rx, ry, rz = origin.position_from_com_m
    fx, fy, fz = force
    translated = (
        ry * fz - rz * fy,
        rz * fx - rx * fz,
        rx * fy - ry * fx,
    )
    moment = (translated[0], pitch + translated[1], yaw + translated[2])
    if not all(math.isfinite(value) for value in (*force, *moment, flow, conductance, heat)):
        raise AeroLoadCouplingError("translated aerodynamic output is non-finite")
    return (
        AerodynamicChassisWrench(force, moment, result.map_id, result.evidence.evidence_id),
        AerodynamicCoolingEvidence(flow, conductance, heat, result.map_id, result.evidence.evidence_id),
    )


def _solve3(matrix, rhs):
    a = [list(row) + [rhs[index]] for index, row in enumerate(matrix)]
    for column in range(3):
        pivot = max(range(column, 3), key=lambda row: abs(a[row][column]))
        if abs(a[pivot][column]) <= 1e-12:
            return None
        a[column], a[pivot] = a[pivot], a[column]
        divisor = a[column][column]
        for index in range(column, 4): a[column][index] /= divisor
        for row in range(3):
            if row == column: continue
            factor = a[row][column]
            for index in range(column, 4): a[row][index] -= factor * a[column][index]
    result = tuple(a[row][3] for row in range(3))
    return result if all(math.isfinite(value) for value in result) else None


def couple_wrench_to_normal_loads(*, vehicle: PlanarVehicle, wrench: AerodynamicChassisWrench,
        longitudinal_acceleration_m_per_s2: float = 0.0,
        lateral_acceleration_m_per_s2: float = 0.0) -> AeroLoadCouplingResult:
    _finite("longitudinal acceleration", longitudinal_acceleration_m_per_s2)
    _finite("lateral acceleration", lateral_acceleration_m_per_s2)
    contacts = vehicle.contacts; params = vehicle.parameters
    xs = tuple(c.x_position_m for c in contacts); ys = tuple(c.y_position_m for c in contacts)
    matrix = ((len(contacts), math.fsum(xs), math.fsum(ys)),
              (math.fsum(xs), math.fsum(x*x for x in xs), math.fsum(x*y for x,y in zip(xs,ys))),
              (math.fsum(ys), math.fsum(x*y for x,y in zip(xs,ys)), math.fsum(y*y for y in ys)))
    fx, fy, fz = wrench.force_body_n; mx, my, _mz = wrench.moment_about_com_n_m
    target = (params.mass_kg * params.gravity_m_per_s2 - fz,
              my - params.mass_kg * longitudinal_acceleration_m_per_s2 * params.centre_of_mass_height_m,
              -mx - params.mass_kg * lateral_acceleration_m_per_s2 * params.centre_of_mass_height_m)
    baseline = tuple(c.baseline_normal_load_n for c in contacts)
    current = (math.fsum(baseline), math.fsum(x*n for x,n in zip(xs,baseline)), math.fsum(y*n for y,n in zip(ys,baseline)))
    correction = _solve3(matrix, tuple(wanted-have for wanted,have in zip(target,current)))
    if correction is None:
        return AeroLoadCouplingResult("invalid", "contact geometry is rank-deficient", wrench, None, (), None)
    loads = tuple(n + correction[0] + correction[1]*x + correction[2]*y for n,x,y in zip(baseline,xs,ys))
    contact_loads = tuple(ContactNormalLoad(c.contact_id, n) for c,n in zip(contacts,loads))
    residuals = AeroLoadBalanceResiduals(
        math.fsum(loads) + fz - params.mass_kg * params.gravity_m_per_s2,
        math.fsum(x*n for x,n in zip(xs,loads)) + params.mass_kg*longitudinal_acceleration_m_per_s2*params.centre_of_mass_height_m - my,
        math.fsum(y*n for y,n in zip(ys,loads)) + params.mass_kg*lateral_acceleration_m_per_s2*params.centre_of_mass_height_m + mx,
    )
    if any(n < 0 for n in loads):
        return AeroLoadCouplingResult("invalid", "aerodynamic/load transfer caused contact lift", wrench, None, contact_loads, residuals)
    if any(not entry.passed for entry in residuals.entries()):
        return AeroLoadCouplingResult("invalid", "normal-load balance residual exceeded tolerance", wrench, None, contact_loads, residuals)
    return AeroLoadCouplingResult("ok", "aerodynamic wrench and contact loads balance", wrench, None, contact_loads, residuals)


@dataclass(frozen=True, slots=True)
class AerodynamicMapAdapter:
    coefficient_map: AerodynamicCoefficientMap
    reference: AerodynamicReference
    reference_origin: AerodynamicReferenceOrigin
    ride_height_m: float
    active_state: str
    component_temperature_k: float
    module_id: str = field(default="aerodynamic_map", init=False)
    model_version: str = field(default=AERO_MODEL_VERSION, init=False)

    def execute(self, view: AdapterReadView) -> AdapterOutput:
        environment = view.read("environment.step_inputs"); state = view.read("state.current")
        if not isinstance(environment, EnvironmentStepInputs) or not isinstance(state, SharedVehicleState):
            return AdapterOutput(self.module_id, "invalid", (), reason="aerodynamic adapter payload types are invalid")
        weather = environment.weather
        if weather.status != "observed" or weather.wind_coordinate_frame != "local_enu":
            return AdapterOutput(self.module_id, "invalid", (), reason="observed local_enu weather is required")
        vx = state.velocity_mps[0] - weather.wind_velocity_mps[0]
        vy = state.velocity_mps[1] - weather.wind_velocity_mps[1]
        vz = state.velocity_mps[2] - weather.wind_velocity_mps[2]
        cosine, sine = math.cos(state.yaw_rad), math.sin(state.yaw_rad)
        body_x = cosine*vx + sine*vy; body_y = -sine*vx + cosine*vy
        speed = math.sqrt(body_x*body_x + body_y*body_y + vz*vz)
        yaw = math.atan2(body_y, max(1e-15, body_x))
        query_speed, speed_snapped = _snap_to_declared_node(speed, self.coefficient_map.airspeeds_m_per_s)
        query_yaw, yaw_snapped = _snap_to_declared_node(yaw, self.coefficient_map.yaw_angles_rad)
        query_height, height_snapped = _snap_to_declared_node(self.ride_height_m, self.coefficient_map.ride_heights_m)
        raw = {"airspeed": speed, "ride_height": self.ride_height_m, "yaw_angle": yaw}
        queried = {"airspeed": query_speed, "ride_height": query_height, "yaw_angle": query_yaw}
        query_evidence = AerodynamicQueryEvidence(
            speed, query_speed, yaw, query_yaw,
            tuple(name for name, snapped in (("airspeed", speed_snapped), ("ride_height", height_snapped), ("yaw_angle", yaw_snapped)) if snapped and raw[name] != queried[name]),
        )
        try:
            density = moist_air_density_kg_per_m3(weather.air_temperature_k, weather.pressure_pa, weather.relative_humidity)
            result = evaluate_aerodynamics(coefficient_map=self.coefficient_map, reference=self.reference,
                operating_point=AerodynamicOperatingPoint(query_speed, density, query_height, query_yaw,
                    self.active_state, weather.air_temperature_k, self.component_temperature_k))
            wrench, cooling = translate_aerodynamic_result(result, self.reference_origin)
            wrench = replace(wrench, query_evidence=query_evidence)
        except (AeroLoadCouplingError, ValueError) as exc:
            return AdapterOutput(self.module_id, "invalid", (), reason=str(exc))
        return AdapterOutput(self.module_id, "ok", (
            RuntimeSignal("aero.cooling_evidence", cooling),
            RuntimeSignal("aero.force_moment", wrench),
        ))


@dataclass(frozen=True, slots=True)
class NormalLoadCouplingAdapter:
    vehicle: PlanarVehicle
    longitudinal_acceleration_m_per_s2: float = 0.0
    lateral_acceleration_m_per_s2: float = 0.0
    module_id: str = field(default="normal_load_solver", init=False)
    model_version: str = field(default=LOAD_MODEL_VERSION, init=False)

    def execute(self, view: AdapterReadView) -> AdapterOutput:
        wrench = view.read("aero.force_moment"); state = view.read("state.current")
        if not isinstance(wrench, AerodynamicChassisWrench) or not isinstance(state, SharedVehicleState):
            return AdapterOutput(self.module_id, "invalid", (), reason="normal-load adapter payload types are invalid")
        if {c.contact_id for c in self.vehicle.contacts} != {c.contact_id for c in state.contacts}:
            return AdapterOutput(self.module_id, "invalid", (), reason="vehicle and shared-state contact IDs differ")
        result = couple_wrench_to_normal_loads(vehicle=self.vehicle, wrench=wrench,
            longitudinal_acceleration_m_per_s2=self.longitudinal_acceleration_m_per_s2,
            lateral_acceleration_m_per_s2=self.lateral_acceleration_m_per_s2)
        if result.status != "ok":
            return AdapterOutput(self.module_id, "invalid", (), reason=result.reason,
                residuals=() if result.residuals is None else result.residuals.entries())
        return AdapterOutput(self.module_id, "ok", (
            RuntimeSignal("chassis.balance_residuals", result.residuals),
            RuntimeSignal("chassis.normal_loads", result.contact_loads),
        ), residuals=result.residuals.entries())
