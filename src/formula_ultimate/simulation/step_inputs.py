"""Typed, evidence-explicit inputs for one coupled simulation step."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
import hashlib
import json
import math

from formula_ultimate.physics.circuit import CircuitProfile

from .coupling import SharedVehicleState
from .transaction import AdapterOutput, AdapterReadView, RuntimeSignal


class StepInputError(ValueError):
    """Raised when typed step input violates the Work 023 contract."""


def _json_ready(value: object) -> object:
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_ready(item) for item in value]
    return value


def _text(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise StepInputError(f"{name} must not be blank")


def _finite(name: str, value: float) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        raise StepInputError(f"{name} must be finite")


@dataclass(frozen=True, slots=True)
class SpatialStepEvidence:
    circuit_id: str
    status: str
    source_id: str | None = None
    segment_id: str | None = None
    curvature_1pm: float | None = None
    grade_rad: float | None = None
    bank_rad: float | None = None
    width_left_m: float | None = None
    width_right_m: float | None = None
    horizontal_uncertainty_m: float | None = None
    reason: str | None = None

    def __post_init__(self) -> None:
        _text("spatial circuit_id", self.circuit_id)
        if self.status not in {"available", "missing"}:
            raise StepInputError("spatial status must be available or missing")
        values = (self.curvature_1pm, self.grade_rad, self.bank_rad,
                  self.width_left_m, self.width_right_m, self.horizontal_uncertainty_m)
        if self.status == "missing":
            if not self.reason or any(value is not None for value in values):
                raise StepInputError("missing spatial evidence requires reason and no numeric defaults")
            return
        for name in ("source_id", "segment_id"):
            _text(f"spatial {name}", getattr(self, name))
        if any(value is None for value in values):
            raise StepInputError("available spatial evidence requires every SI field")
        for name in ("curvature_1pm", "grade_rad", "bank_rad", "width_left_m",
                     "width_right_m", "horizontal_uncertainty_m"):
            _finite(name, getattr(self, name))
        if self.width_left_m <= 0 or self.width_right_m <= 0 or self.horizontal_uncertainty_m < 0:
            raise StepInputError("spatial widths must be positive and uncertainty non-negative")
        if self.reason is not None:
            raise StepInputError("available spatial evidence cannot have missing reason")


@dataclass(frozen=True, slots=True)
class WeatherStepEvidence:
    circuit_id: str
    status: str
    source_id: str | None = None
    air_temperature_k: float | None = None
    pressure_pa: float | None = None
    relative_humidity: float | None = None
    wind_velocity_mps: tuple[float, float, float] | None = None
    precipitation_kg_per_m2_s: float | None = None
    track_temperature_k: float | None = None
    reason: str | None = None

    def __post_init__(self) -> None:
        _text("weather circuit_id", self.circuit_id)
        if self.status not in {"observed", "missing"}:
            raise StepInputError("weather status must be observed or missing")
        scalars = (self.air_temperature_k, self.pressure_pa, self.relative_humidity,
                   self.precipitation_kg_per_m2_s, self.track_temperature_k)
        if self.status == "missing":
            if not self.reason or any(value is not None for value in scalars) or self.wind_velocity_mps is not None:
                raise StepInputError("missing weather requires reason and no neutral defaults")
            return
        _text("weather source_id", self.source_id)
        if any(value is None for value in scalars) or self.wind_velocity_mps is None:
            raise StepInputError("observed weather requires every field")
        for name in ("air_temperature_k", "pressure_pa", "relative_humidity",
                     "precipitation_kg_per_m2_s", "track_temperature_k"):
            _finite(name, getattr(self, name))
        if self.air_temperature_k <= 0 or self.track_temperature_k <= 0 or self.pressure_pa <= 0:
            raise StepInputError("temperatures and pressure must be positive")
        if not 0 <= self.relative_humidity <= 1 or self.precipitation_kg_per_m2_s < 0:
            raise StepInputError("humidity must be [0,1] and precipitation non-negative")
        if len(self.wind_velocity_mps) != 3:
            raise StepInputError("wind velocity must have three components")
        for value in self.wind_velocity_mps:
            _finite("wind velocity", value)
        if self.reason is not None:
            raise StepInputError("observed weather cannot have missing reason")


@dataclass(frozen=True, slots=True)
class TrafficStepEvidence:
    circuit_id: str
    mode: str
    source_id: str
    nearby_vehicle_count: int | None
    reason: str | None = None

    def __post_init__(self) -> None:
        _text("traffic circuit_id", self.circuit_id)
        _text("traffic source_id", self.source_id)
        if self.mode not in {"isolated_control", "observed", "missing"}:
            raise StepInputError("unsupported traffic mode")
        if self.mode == "missing":
            if self.nearby_vehicle_count is not None or not self.reason:
                raise StepInputError("missing traffic requires reason and no count")
        elif not isinstance(self.nearby_vehicle_count, int) or isinstance(self.nearby_vehicle_count, bool) or self.nearby_vehicle_count < 0:
            raise StepInputError("declared traffic requires non-negative integer count")
        if self.mode == "isolated_control" and self.nearby_vehicle_count != 0:
            raise StepInputError("isolated control must declare zero nearby vehicles")


@dataclass(frozen=True, slots=True)
class StrategyStepCommand:
    throttle_fraction: float
    brake_fraction: float
    steering_request: float
    recovery_fraction: float

    def __post_init__(self) -> None:
        for name in ("throttle_fraction", "brake_fraction", "recovery_fraction"):
            value = getattr(self, name); _finite(name, value)
            if not 0 <= value <= 1: raise StepInputError(f"{name} must be in [0,1]")
        _finite("steering_request", self.steering_request)
        if not -1 <= self.steering_request <= 1:
            raise StepInputError("steering_request must be in [-1,1]")


@dataclass(frozen=True, slots=True)
class CircuitInputScenario:
    profile: CircuitProfile
    race_distance_m: float
    spatial: SpatialStepEvidence
    weather: WeatherStepEvidence
    traffic: TrafficStepEvidence

    def __post_init__(self) -> None:
        _finite("race_distance_m", self.race_distance_m)
        if not 0 <= self.race_distance_m <= self.profile.race_distance_m:
            raise StepInputError("race distance lies outside circuit race distance")
        for evidence in (self.spatial, self.weather, self.traffic):
            if evidence.circuit_id != self.profile.circuit_id:
                raise StepInputError("evidence circuit_id must match profile")


@dataclass(frozen=True, slots=True)
class EnvironmentStepInputs:
    weather: WeatherStepEvidence
    traffic: TrafficStepEvidence


@dataclass(frozen=True, slots=True)
class StepInputResolution:
    scenario: CircuitInputScenario
    strategy: StrategyStepCommand
    status: str
    missing_evidence: tuple[str, ...]
    fingerprint_sha256: str


def resolve_step_inputs(scenario: CircuitInputScenario, strategy: StrategyStepCommand) -> StepInputResolution:
    missing = []
    if scenario.spatial.status == "missing": missing.append("spatial")
    if scenario.weather.status == "missing": missing.append("weather")
    if scenario.traffic.mode == "missing": missing.append("traffic")
    payload = {
        "profile": _json_ready(asdict(scenario.profile)),
        "race_distance_m": scenario.race_distance_m,
        "spatial": asdict(scenario.spatial),
        "weather": asdict(scenario.weather),
        "traffic": asdict(scenario.traffic),
        "strategy": asdict(strategy),
    }
    fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()
    return StepInputResolution(scenario, strategy, "ready" if not missing else "incomplete", tuple(missing), fingerprint)


@dataclass(frozen=True, slots=True)
class CircuitEnvironmentInputAdapter:
    module_id: str = "input_bridge"
    model_version: str = "work021-input-contract-v1"

    def execute(self, view: AdapterReadView) -> AdapterOutput:
        scenario = view.read("manifest.circuit_profile")
        state = view.read("manifest.current_state")
        strategy = view.read("manifest.strategy_command")
        if not isinstance(scenario, CircuitInputScenario) or not isinstance(state, SharedVehicleState) or not isinstance(strategy, StrategyStepCommand):
            return AdapterOutput(self.module_id, "invalid", (), reason="input bridge payload types are invalid")
        resolution = resolve_step_inputs(scenario, strategy)
        if resolution.status != "ready":
            return AdapterOutput(self.module_id, "invalid", (), reason=f"missing evidence: {resolution.missing_evidence!r}")
        return AdapterOutput(self.module_id, "ok", (
            RuntimeSignal("circuit.segment_inputs", scenario.spatial),
            RuntimeSignal("control.step_command", strategy),
            RuntimeSignal("environment.step_inputs", EnvironmentStepInputs(scenario.weather, scenario.traffic)),
            RuntimeSignal("state.current", state),
        ))
