"""Work 029 fair fixed-topology baseline campaign across ten profiles."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass, replace
from datetime import date
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping

from formula_ultimate.physics.aerodynamics import (
    AerodynamicCoefficientMap,
    AerodynamicCoefficientSample,
    AerodynamicEvidence,
    AerodynamicReference,
    AerodynamicStateGrid,
)
from formula_ultimate.physics.circuit import CircuitProfile
from formula_ultimate.physics.lateral import (
    PlanarContact,
    PlanarVehicle,
    PlanarVehicleParameters,
)
from formula_ultimate.physics.suspension_braking import (
    BrakeParameters,
    RegenerationParameters,
    SuspensionBrakeModule,
    SuspensionParameters,
)
from formula_ultimate.physics.thermal import ThermalParameters
from formula_ultimate.physics.tyre import TyreContactParameters

from .aero_load_coupling import (
    AerodynamicMapAdapter,
    AerodynamicReferenceOrigin,
    NormalLoadCouplingAdapter,
    moist_air_density_kg_per_m3,
)
from .contact_coupling import (
    ContactCouplingConfig,
    ContactCouplingSpec,
    ContactLimitCouplingAdapter,
)
from .coupling import (
    CompiledCouplingArchitecture,
    ComponentHealthState,
    ContactRuntimeState,
    SharedVehicleState,
)
from .energy_health_coupling import (
    CentralEnergyAuditAdapter,
    CentralEnergyConfiguration,
    CentralHealthConfiguration,
    CentralHealthEventAdapter,
    ComponentHealthConfiguration,
)
from .motion_coupling import (
    MotionConfiguration,
    MotionCorridorReference,
    VehicleMotionCouplingAdapter,
)
from .step_inputs import (
    CircuitEnvironmentInputAdapter,
    CircuitInputScenario,
    SpatialStepEvidence,
    StrategyStepCommand,
    TrafficStepEvidence,
    WeatherStepEvidence,
)
from .whole_race import (
    RaceProgressAdapter,
    RaceProgressConfiguration,
    WholeRaceConfiguration,
    run_whole_race,
)


BASELINE_CAMPAIGN_MODEL_VERSION = "work029-baseline-campaign-v2"


class BaselineCampaignError(ValueError):
    """Raised when the fair-compute campaign contract is invalid."""


def _finite(name: str, value: float) -> None:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
    ):
        raise BaselineCampaignError(f"{name} must be finite")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise BaselineCampaignError(f"{name} must be positive")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise BaselineCampaignError(f"{name} must be non-negative")


def _text(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise BaselineCampaignError(f"{name} must not be blank")


def _json_ready(value: object) -> object:
    if isinstance(value, date):
        return value.isoformat()
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_ready(item) for item in value]
    return value


def _fingerprint(value: object) -> str:
    encoded = json.dumps(
        _json_ready(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _expect_keys(label: str, raw: Mapping[str, Any], keys: set[str]) -> None:
    actual = set(raw)
    if actual != keys:
        raise BaselineCampaignError(
            f"{label} keys differ: missing={sorted(keys-actual)!r}, "
            f"unexpected={sorted(actual-keys)!r}"
        )


@dataclass(frozen=True, slots=True)
class ProxyEnvironmentControl:
    source_id: str
    air_temperature_k: float
    pressure_pa: float
    relative_humidity: float
    track_temperature_k: float
    wind_velocity_mps: tuple[float, float, float]
    precipitation_kg_per_m2_s: float
    corridor_half_width_m: float
    horizontal_uncertainty_m: float

    def __post_init__(self) -> None:
        _text("proxy source_id", self.source_id)
        for name in (
            "air_temperature_k",
            "pressure_pa",
            "track_temperature_k",
            "corridor_half_width_m",
        ):
            _positive(name, getattr(self, name))
        for name in ("precipitation_kg_per_m2_s", "horizontal_uncertainty_m"):
            _nonnegative(name, getattr(self, name))
        _finite("relative_humidity", self.relative_humidity)
        if not 0.0 <= self.relative_humidity <= 1.0:
            raise BaselineCampaignError("relative_humidity must be in [0,1]")
        if len(self.wind_velocity_mps) != 3:
            raise BaselineCampaignError("wind_velocity_mps must have three values")
        for value in self.wind_velocity_mps:
            _finite("wind_velocity_mps", value)
        if self.horizontal_uncertainty_m >= self.corridor_half_width_m:
            raise BaselineCampaignError(
                "proxy corridor uncertainty must be smaller than half width"
            )


@dataclass(frozen=True, slots=True)
class BaselineContactDefinition:
    contact_id: str
    x_m: float
    y_m: float
    drive_fraction: float
    brake_fraction: float

    def __post_init__(self) -> None:
        _text("contact_id", self.contact_id)
        for name in ("x_m", "y_m"):
            _finite(name, getattr(self, name))
        for name in ("drive_fraction", "brake_fraction"):
            _nonnegative(name, getattr(self, name))


@dataclass(frozen=True, slots=True)
class BaselineReferenceFamily:
    family_id: str
    model_version: str
    topology_id: str
    component_library_version: str
    strategy_id: str
    mass_kg: float
    yaw_inertia_kg_m2: float
    vehicle_width_m: float
    centre_of_mass_height_m: float
    initial_speed_mps: float
    initial_primary_energy_j: float
    recovered_capacity_j: float
    drive_efficiency: float
    auxiliary_power_w: float
    maximum_drive_force_n: float
    maximum_brake_torque_n_m: float
    ride_height_m: float
    aerodynamic_reference_area_m2: float
    aerodynamic_reference_length_m: float
    drag_coefficient: float
    contacts: tuple[BaselineContactDefinition, ...]

    def __post_init__(self) -> None:
        for name in (
            "family_id",
            "model_version",
            "topology_id",
            "component_library_version",
            "strategy_id",
        ):
            _text(name, getattr(self, name))
        for name in (
            "mass_kg",
            "yaw_inertia_kg_m2",
            "vehicle_width_m",
            "initial_speed_mps",
            "initial_primary_energy_j",
            "recovered_capacity_j",
            "drive_efficiency",
            "maximum_drive_force_n",
            "ride_height_m",
            "aerodynamic_reference_area_m2",
            "aerodynamic_reference_length_m",
        ):
            _positive(name, getattr(self, name))
        for name in (
            "centre_of_mass_height_m",
            "auxiliary_power_w",
            "maximum_brake_torque_n_m",
            "drag_coefficient",
        ):
            _nonnegative(name, getattr(self, name))
        if self.drive_efficiency > 1.0:
            raise BaselineCampaignError("drive_efficiency must be <= 1")
        if len(self.contacts) < 3:
            raise BaselineCampaignError("reference family requires at least three contacts")
        ids = tuple(item.contact_id for item in self.contacts)
        if len(ids) != len(set(ids)):
            raise BaselineCampaignError("contact IDs must be unique")
        for name in ("drive_fraction", "brake_fraction"):
            total = math.fsum(getattr(item, name) for item in self.contacts)
            if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1.0e-12):
                raise BaselineCampaignError(f"{name} values must sum to 1")
        if self.strategy_id != "steady-drag-balance-v1":
            raise BaselineCampaignError("unsupported baseline strategy_id")

    @property
    def opportunity_fingerprint_sha256(self) -> str:
        return _fingerprint(self)


@dataclass(frozen=True, slots=True)
class BaselineCampaignControls:
    time_step_s: float
    timeout_s: float
    evaluation_budget_per_run: int
    design_evaluation_budget: int
    random_seeds: tuple[int, ...]
    calibration_circuit_ids: tuple[str, ...]
    holdout_circuit_ids: tuple[str, ...]
    proxy_environment: ProxyEnvironmentControl

    def __post_init__(self) -> None:
        _positive("time_step_s", self.time_step_s)
        _positive("timeout_s", self.timeout_s)
        if self.time_step_s > self.timeout_s:
            raise BaselineCampaignError("time step cannot exceed timeout")
        for name in ("evaluation_budget_per_run", "design_evaluation_budget"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise BaselineCampaignError(f"{name} must be a positive integer")
        if not self.random_seeds:
            raise BaselineCampaignError("at least one random seed is required")
        if any(not isinstance(seed, int) or isinstance(seed, bool) for seed in self.random_seeds):
            raise BaselineCampaignError("random seeds must be integers")
        if len(self.random_seeds) != len(set(self.random_seeds)):
            raise BaselineCampaignError("random seeds must be unique")
        calibration = tuple(sorted(self.calibration_circuit_ids))
        holdout = tuple(sorted(self.holdout_circuit_ids))
        if not calibration or not holdout:
            raise BaselineCampaignError("calibration and holdout partitions are required")
        if len(calibration) != len(set(calibration)) or len(holdout) != len(set(holdout)):
            raise BaselineCampaignError("partition circuit IDs must be unique")
        if set(calibration) & set(holdout):
            raise BaselineCampaignError("calibration and holdout partitions overlap")
        object.__setattr__(self, "random_seeds", tuple(sorted(self.random_seeds)))
        object.__setattr__(self, "calibration_circuit_ids", calibration)
        object.__setattr__(self, "holdout_circuit_ids", holdout)

    @property
    def fingerprint_sha256(self) -> str:
        return _fingerprint(self)


@dataclass(frozen=True, slots=True)
class BaselineCampaignProtocol:
    schema_version: str
    campaign_id: str
    architecture_id: str
    evidence_grade: str
    real_circuit_admission: bool
    controls: BaselineCampaignControls
    reference_families: tuple[BaselineReferenceFamily, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "1.0":
            raise BaselineCampaignError("unsupported baseline protocol schema")
        for name in ("campaign_id", "architecture_id", "evidence_grade"):
            _text(name, getattr(self, name))
        if not isinstance(self.real_circuit_admission, bool):
            raise BaselineCampaignError("real_circuit_admission must be boolean")
        if self.real_circuit_admission:
            raise BaselineCampaignError(
                "analytical proxy campaign cannot declare real-circuit admission"
            )
        if self.evidence_grade != "profile-distance-analytical-proxy":
            raise BaselineCampaignError("unsupported evidence grade")
        if not self.reference_families:
            raise BaselineCampaignError("at least one reference family is required")
        ids = tuple(item.family_id for item in self.reference_families)
        if len(ids) != len(set(ids)):
            raise BaselineCampaignError("reference family IDs must be unique")
        object.__setattr__(
            self,
            "reference_families",
            tuple(sorted(self.reference_families, key=lambda item: item.family_id)),
        )

    @property
    def fingerprint_sha256(self) -> str:
        return _fingerprint(self)


@dataclass(frozen=True, slots=True)
class BaselineRunRecord:
    campaign_id: str
    protocol_fingerprint_sha256: str
    controls_fingerprint_sha256: str
    architecture_fingerprint_sha256: str
    family_id: str
    family_opportunity_fingerprint_sha256: str
    circuit_id: str
    partition: str
    random_seed: int
    evidence_grade: str
    real_circuit_admitted: bool
    static_width_status: str
    outcome: str
    reason: str
    final_time_s: float
    final_distance_m: float
    finish_distance_residual_m: float
    primary_energy_used_j: float
    attempted_steps: int
    committed_steps: int
    evaluation_budget_per_run: int
    all_residuals_passed: bool
    scenario_fingerprint_count: int
    race_replay_fingerprint_sha256: str
    record_fingerprint_sha256: str = field(default="", compare=True)


@dataclass(frozen=True, slots=True)
class BaselineCampaignResult:
    model_version: str
    campaign_id: str
    protocol_fingerprint_sha256: str
    controls_fingerprint_sha256: str
    architecture_fingerprint_sha256: str
    expected_run_count: int
    completed_run_count: int
    completed_profile_count: int
    total_profile_count: int
    all_runs_finished: bool
    all_residuals_passed: bool
    all_runs_within_budget: bool
    partition_complete: bool
    real_circuit_admitted: bool
    runs: tuple[BaselineRunRecord, ...]
    result_fingerprint_sha256: str
    claim_boundary: str


def _run_record_identity_payload(record: BaselineRunRecord) -> dict[str, object]:
    payload = asdict(record)
    payload.pop("record_fingerprint_sha256")
    return payload


def _campaign_result_identity_payload(
    result: BaselineCampaignResult,
) -> dict[str, object]:
    payload = asdict(result)
    payload.pop("result_fingerprint_sha256")
    return payload


def verify_baseline_campaign_result(
    result: BaselineCampaignResult,
) -> tuple[bool, tuple[str, ...]]:
    """Recompute run/result identities and aggregate invariants."""

    reasons: list[str] = []
    if any(
        run.record_fingerprint_sha256 != _fingerprint(_run_record_identity_payload(run))
        for run in result.runs
    ):
        reasons.append("run_fingerprint_mismatch")
    if result.result_fingerprint_sha256 != _fingerprint(
        _campaign_result_identity_payload(result)
    ):
        reasons.append("campaign_fingerprint_mismatch")
    if result.expected_run_count != len(result.runs):
        reasons.append("expected_run_count_mismatch")
    run_keys = tuple(
        (run.family_id, run.circuit_id, run.random_seed) for run in result.runs
    )
    if len(run_keys) != len(set(run_keys)):
        reasons.append("duplicate_run_identity")
    completed = sum(run.outcome == "finished" for run in result.runs)
    if result.completed_run_count != completed:
        reasons.append("completed_run_count_mismatch")
    profile_ids = {run.circuit_id for run in result.runs}
    if result.total_profile_count != len(profile_ids):
        reasons.append("total_profile_count_mismatch")
    completed_profiles = {
        circuit_id
        for circuit_id in profile_ids
        if all(run.outcome == "finished" for run in result.runs if run.circuit_id == circuit_id)
    }
    if result.completed_profile_count != len(completed_profiles):
        reasons.append("completed_profile_count_mismatch")
    if profile_ids:
        first_profile = min(profile_ids)
        expected_family_seed = {
            (run.family_id, run.random_seed)
            for run in result.runs
            if run.circuit_id == first_profile
        }
        if any(
            {
                (run.family_id, run.random_seed)
                for run in result.runs
                if run.circuit_id == circuit_id
            }
            != expected_family_seed
            for circuit_id in profile_ids
        ):
            reasons.append("family_seed_matrix_incomplete")
    if result.all_runs_finished != all(run.outcome == "finished" for run in result.runs):
        reasons.append("all_runs_finished_mismatch")
    if result.all_residuals_passed != all(run.all_residuals_passed for run in result.runs):
        reasons.append("all_residuals_passed_mismatch")
    if result.all_runs_within_budget != all(
        run.attempted_steps <= run.evaluation_budget_per_run for run in result.runs
    ):
        reasons.append("all_runs_within_budget_mismatch")
    partition_by_profile = {
        circuit_id: {
            run.partition for run in result.runs if run.circuit_id == circuit_id
        }
        for circuit_id in profile_ids
    }
    partition_complete = (
        bool(profile_ids)
        and all(len(values) == 1 for values in partition_by_profile.values())
        and {next(iter(values)) for values in partition_by_profile.values()}
        == {"calibration", "holdout"}
    )
    if result.partition_complete != partition_complete:
        reasons.append("partition_complete_mismatch")
    if result.real_circuit_admitted != all(
        run.real_circuit_admitted for run in result.runs
    ):
        reasons.append("real_circuit_admission_mismatch")
    for field_name in (
        "campaign_id",
        "protocol_fingerprint_sha256",
        "controls_fingerprint_sha256",
        "architecture_fingerprint_sha256",
    ):
        if any(getattr(run, field_name) != getattr(result, field_name) for run in result.runs):
            reasons.append(f"run_{field_name}_mismatch")
    unique = tuple(sorted(set(reasons)))
    return not unique, unique


def _parse_proxy_environment(raw: Mapping[str, Any]) -> ProxyEnvironmentControl:
    _expect_keys(
        "proxy_environment",
        raw,
        {
            "source_id",
            "air_temperature_k",
            "pressure_pa",
            "relative_humidity",
            "track_temperature_k",
            "wind_velocity_mps",
            "precipitation_kg_per_m2_s",
            "corridor_half_width_m",
            "horizontal_uncertainty_m",
        },
    )
    wind = raw["wind_velocity_mps"]
    if not isinstance(wind, list):
        raise BaselineCampaignError("wind_velocity_mps must be a JSON array")
    return ProxyEnvironmentControl(
        str(raw["source_id"]),
        raw["air_temperature_k"],
        raw["pressure_pa"],
        raw["relative_humidity"],
        raw["track_temperature_k"],
        tuple(wind),
        raw["precipitation_kg_per_m2_s"],
        raw["corridor_half_width_m"],
        raw["horizontal_uncertainty_m"],
    )


def _parse_contact(raw: Mapping[str, Any]) -> BaselineContactDefinition:
    _expect_keys(
        "contact",
        raw,
        {"contact_id", "x_m", "y_m", "drive_fraction", "brake_fraction"},
    )
    return BaselineContactDefinition(
        str(raw["contact_id"]),
        raw["x_m"],
        raw["y_m"],
        raw["drive_fraction"],
        raw["brake_fraction"],
    )


def _parse_family(raw: Mapping[str, Any]) -> BaselineReferenceFamily:
    keys = {
        "family_id",
        "model_version",
        "topology_id",
        "component_library_version",
        "strategy_id",
        "mass_kg",
        "yaw_inertia_kg_m2",
        "vehicle_width_m",
        "centre_of_mass_height_m",
        "initial_speed_mps",
        "initial_primary_energy_j",
        "recovered_capacity_j",
        "drive_efficiency",
        "auxiliary_power_w",
        "maximum_drive_force_n",
        "maximum_brake_torque_n_m",
        "ride_height_m",
        "aerodynamic_reference_area_m2",
        "aerodynamic_reference_length_m",
        "drag_coefficient",
        "contacts",
    }
    _expect_keys("reference family", raw, keys)
    contacts = raw["contacts"]
    if not isinstance(contacts, list):
        raise BaselineCampaignError("contacts must be a JSON array")
    return BaselineReferenceFamily(
        family_id=str(raw["family_id"]),
        model_version=str(raw["model_version"]),
        topology_id=str(raw["topology_id"]),
        component_library_version=str(raw["component_library_version"]),
        strategy_id=str(raw["strategy_id"]),
        mass_kg=raw["mass_kg"],
        yaw_inertia_kg_m2=raw["yaw_inertia_kg_m2"],
        vehicle_width_m=raw["vehicle_width_m"],
        centre_of_mass_height_m=raw["centre_of_mass_height_m"],
        initial_speed_mps=raw["initial_speed_mps"],
        initial_primary_energy_j=raw["initial_primary_energy_j"],
        recovered_capacity_j=raw["recovered_capacity_j"],
        drive_efficiency=raw["drive_efficiency"],
        auxiliary_power_w=raw["auxiliary_power_w"],
        maximum_drive_force_n=raw["maximum_drive_force_n"],
        maximum_brake_torque_n_m=raw["maximum_brake_torque_n_m"],
        ride_height_m=raw["ride_height_m"],
        aerodynamic_reference_area_m2=raw["aerodynamic_reference_area_m2"],
        aerodynamic_reference_length_m=raw["aerodynamic_reference_length_m"],
        drag_coefficient=raw["drag_coefficient"],
        contacts=tuple(_parse_contact(item) for item in contacts),
    )


def load_baseline_campaign_protocol(path: str | Path) -> BaselineCampaignProtocol:
    """Load a strict Work 029 protocol without implicit type coercion."""

    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise BaselineCampaignError("protocol root must be an object")
        _expect_keys(
            "protocol",
            raw,
            {
                "schema_version",
                "campaign_id",
                "architecture_id",
                "evidence_grade",
                "real_circuit_admission",
                "controls",
                "reference_families",
            },
        )
        controls_raw = raw["controls"]
        if not isinstance(controls_raw, dict):
            raise BaselineCampaignError("controls must be an object")
        _expect_keys(
            "controls",
            controls_raw,
            {
                "time_step_s",
                "timeout_s",
                "evaluation_budget_per_run",
                "design_evaluation_budget",
                "random_seeds",
                "calibration_circuit_ids",
                "holdout_circuit_ids",
                "proxy_environment",
            },
        )
        for name in (
            "random_seeds",
            "calibration_circuit_ids",
            "holdout_circuit_ids",
        ):
            if not isinstance(controls_raw[name], list):
                raise BaselineCampaignError(f"{name} must be a JSON array")
        families_raw = raw["reference_families"]
        if not isinstance(families_raw, list):
            raise BaselineCampaignError("reference_families must be a JSON array")
        controls = BaselineCampaignControls(
            controls_raw["time_step_s"],
            controls_raw["timeout_s"],
            controls_raw["evaluation_budget_per_run"],
            controls_raw["design_evaluation_budget"],
            tuple(controls_raw["random_seeds"]),
            tuple(str(item) for item in controls_raw["calibration_circuit_ids"]),
            tuple(str(item) for item in controls_raw["holdout_circuit_ids"]),
            _parse_proxy_environment(controls_raw["proxy_environment"]),
        )
        return BaselineCampaignProtocol(
            str(raw["schema_version"]),
            str(raw["campaign_id"]),
            str(raw["architecture_id"]),
            str(raw["evidence_grade"]),
            raw["real_circuit_admission"],
            controls,
            tuple(_parse_family(item) for item in families_raw),
        )
    except BaselineCampaignError:
        raise
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise BaselineCampaignError(f"invalid baseline protocol: {exc}") from exc


def _vehicle(family: BaselineReferenceFamily) -> PlanarVehicle:
    load_n = family.mass_kg * 9.81 / len(family.contacts)
    tyre = TyreContactParameters(2.0, 2.0)
    contacts = tuple(
        PlanarContact(
            item.contact_id,
            item.x_m,
            item.y_m,
            load_n,
            0.0,
            20000.0,
            0.0,
            tyre,
        )
        for item in family.contacts
    )
    return PlanarVehicle(
        family.topology_id,
        PlanarVehicleParameters(
            family.mass_kg,
            family.yaw_inertia_kg_m2,
            family.centre_of_mass_height_m,
        ),
        contacts,
    )


def _aero_map(family: BaselineReferenceFamily) -> AerodynamicCoefficientMap:
    sample = AerodynamicCoefficientSample(
        family.drag_coefficient, 0.0, 0.0, 0.0, 0.0, 0.0
    )
    speeds = (0.0, family.initial_speed_mps, family.initial_speed_mps * 4.0)
    return AerodynamicCoefficientMap(
        f"{family.family_id}-analytical-aero",
        speeds,
        (family.ride_height_m,),
        (0.0,),
        (AerodynamicStateGrid("nominal", (sample, sample, sample)),),
        AerodynamicEvidence(
            f"{family.family_id}-declared-aero",
            "synthetic_reference",
            "Work 029 fixed-topology analytical coefficient control",
        ),
    )


def _brake_module(
    contact_id: str,
    preload_n: float,
    recovered_capacity_j: float,
) -> SuspensionBrakeModule:
    return SuspensionBrakeModule(
        contact_id,
        SuspensionParameters(100.0, 10000.0, 10.0, preload_n, 0.2, 0.2),
        BrakeParameters(
            0.3,
            2.0,
            0.0,
            ThermalParameters(1.0e6, 0.0, 0.0, 500.0, 600.0),
        ),
        RegenerationParameters(
            0.0,
            0.0,
            0.0,
            recovered_capacity_j,
            0.9,
            0.0,
        ),
    )


def _initial_state(
    family: BaselineReferenceFamily, vehicle: PlanarVehicle
) -> SharedVehicleState:
    load_n = family.mass_kg * 9.81 / len(family.contacts)
    return SharedVehicleState(
        0.0,
        0.0,
        (0.0, 0.0, 0.0),
        (family.initial_speed_mps, 0.0, 0.0),
        0.0,
        0.0,
        family.initial_primary_energy_j,
        0.0,
        0,
        tuple(
            ContactRuntimeState(
                contact_id=contact.contact_id,
                normal_load_n=load_n,
                longitudinal_force_n=0.0,
                lateral_force_n=0.0,
                suspension_travel_m=0.0,
                angular_speed_rad_per_s=family.initial_speed_mps / 0.3,
                suspension_velocity_m_per_s=0.0,
                brake_temperature_k=300.0,
            )
            for contact in vehicle.contacts
        ),
        (ComponentHealthState("central-store", 300.0, 0.0, 0.0, False),),
    )


def _run_reference(
    *,
    protocol: BaselineCampaignProtocol,
    architecture: CompiledCouplingArchitecture,
    family: BaselineReferenceFamily,
    profile: CircuitProfile,
    random_seed: int,
):
    controls = protocol.controls
    environment = controls.proxy_environment
    vehicle = _vehicle(family)
    initial_state = _initial_state(family, vehicle)
    energy = CentralEnergyConfiguration(
        family.drive_efficiency,
        family.auxiliary_power_w,
        family.recovered_capacity_j,
    )
    coefficient_map = _aero_map(family)
    aero_reference = AerodynamicReference(
        family.aerodynamic_reference_area_m2,
        family.aerodynamic_reference_length_m,
        0.0,
        1005.0,
        0.0,
    )
    density = moist_air_density_kg_per_m3(
        environment.air_temperature_k,
        environment.pressure_pa,
        environment.relative_humidity,
    )

    def scenario_factory(
        _step_index: int, state: SharedVehicleState
    ) -> CircuitInputScenario:
        circuit_id = profile.circuit_id
        return CircuitInputScenario(
            profile,
            state.race_distance_m,
            SpatialStepEvidence(
                circuit_id,
                "available",
                environment.source_id,
                "analytical-straight-proxy",
                0.0,
                0.0,
                0.0,
                environment.corridor_half_width_m,
                environment.corridor_half_width_m,
                environment.horizontal_uncertainty_m,
            ),
            WeatherStepEvidence(
                circuit_id,
                "synthetic_control",
                environment.source_id,
                environment.air_temperature_k,
                environment.pressure_pa,
                environment.relative_humidity,
                environment.wind_velocity_mps,
                "local_enu",
                environment.precipitation_kg_per_m2_s,
                environment.track_temperature_k,
            ),
            TrafficStepEvidence(
                circuit_id, "isolated_control", environment.source_id, 0
            ),
        )

    def strategy_factory(
        _step_index: int, state: SharedVehicleState
    ) -> StrategyStepCommand:
        speed_mps = math.sqrt(math.fsum(value * value for value in state.velocity_mps))
        drag_n = (
            0.5
            * density
            * speed_mps**2
            * family.aerodynamic_reference_area_m2
            * family.drag_coefficient
        )
        throttle = drag_n / family.maximum_drive_force_n
        if not 0.0 <= throttle <= 1.0:
            raise BaselineCampaignError("steady-drag strategy exceeds drive opportunity")
        return StrategyStepCommand(throttle, 0.0, 0.0, 0.0)

    def adapter_factory(
        step_index: int, state: SharedVehicleState, duration_s: float
    ):
        load_n = family.mass_kg * 9.81 / len(family.contacts)
        tyre = TyreContactParameters(2.0, 2.0)
        definitions = {item.contact_id: item for item in family.contacts}
        specs = tuple(
            ContactCouplingSpec(
                contact.contact_id,
                contact.x_position_m,
                contact.y_position_m,
                0.0,
                0.0,
                definitions[contact.contact_id].drive_fraction,
                definitions[contact.contact_id].brake_fraction,
                tyre,
                _brake_module(
                    contact.contact_id, load_n, family.recovered_capacity_j
                ),
            )
            for contact in vehicle.contacts
        )
        health_component = ComponentHealthConfiguration(
            "central-store",
            ThermalParameters(1.0e6, 0.0, 0.0, 500.0, 600.0),
            0.0,
            1.0,
            1.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            1.0,
            0.0,
        )
        return (
            CircuitEnvironmentInputAdapter(),
            AerodynamicMapAdapter(
                coefficient_map,
                aero_reference,
                AerodynamicReferenceOrigin((0.0, 0.0, 0.0)),
                family.ride_height_m,
                "nominal",
                state.components[0].temperature_k,
            ),
            NormalLoadCouplingAdapter(vehicle),
            ContactLimitCouplingAdapter(
                ContactCouplingConfig(
                    specs,
                    family.maximum_drive_force_n,
                    family.maximum_brake_torque_n_m,
                    duration_s,
                    environment.air_temperature_k,
                )
            ),
            VehicleMotionCouplingAdapter(
                MotionConfiguration(
                    family.mass_kg,
                    family.yaw_inertia_kg_m2,
                    duration_s,
                    family.vehicle_width_m,
                ),
                MotionCorridorReference(
                    profile.circuit_id,
                    "analytical-straight-proxy",
                    state.race_distance_m,
                    state.position_m,
                    0.0,
                ),
            ),
            CentralEnergyAuditAdapter(energy),
            CentralHealthEventAdapter(
                CentralHealthConfiguration(
                    (health_component,),
                    random_seed,
                    step_index,
                    environment.air_temperature_k,
                ),
                energy,
            ),
            RaceProgressAdapter(
                RaceProgressConfiguration(
                    profile.race_distance_m,
                    profile.lap_length_m,
                    controls.timeout_s,
                )
            ),
        )

    configuration = WholeRaceConfiguration(
        architecture,
        initial_state,
        controls.time_step_s,
        profile.race_distance_m,
        controls.timeout_s,
        controls.evaluation_budget_per_run,
        random_seed,
        scenario_factory,
        strategy_factory,
        adapter_factory,
    )
    return run_whole_race(configuration)


def _validate_campaign_inputs(
    protocol: BaselineCampaignProtocol,
    architecture: CompiledCouplingArchitecture,
    profiles: tuple[CircuitProfile, ...],
) -> dict[str, str]:
    if architecture.architecture_id != protocol.architecture_id:
        raise BaselineCampaignError("architecture ID differs from protocol")
    profile_ids = tuple(profile.circuit_id for profile in profiles)
    if len(profile_ids) != len(set(profile_ids)):
        raise BaselineCampaignError("catalog circuit IDs must be unique")
    declared = set(protocol.controls.calibration_circuit_ids) | set(
        protocol.controls.holdout_circuit_ids
    )
    actual = set(profile_ids)
    if declared != actual:
        raise BaselineCampaignError(
            f"partition/catalog mismatch: missing={sorted(actual-declared)!r}, "
            f"unknown={sorted(declared-actual)!r}"
        )
    return {
        circuit_id: (
            "calibration"
            if circuit_id in protocol.controls.calibration_circuit_ids
            else "holdout"
        )
        for circuit_id in profile_ids
    }


def run_baseline_campaign(
    *,
    protocol: BaselineCampaignProtocol,
    architecture: CompiledCouplingArchitecture,
    profiles: tuple[CircuitProfile, ...],
) -> BaselineCampaignResult:
    """Execute every family/profile/seed pair under one immutable protocol."""

    partitions = _validate_campaign_inputs(protocol, architecture, profiles)
    controls = protocol.controls
    ordered_profiles = tuple(sorted(profiles, key=lambda item: item.circuit_id))
    runs: list[BaselineRunRecord] = []
    for family in protocol.reference_families:
        for profile in ordered_profiles:
            width = profile.assess_static_width(vehicle_width_m=family.vehicle_width_m)
            if width.status == "rejected":
                raise BaselineCampaignError(
                    f"reference family fails static width screen at {profile.circuit_id}"
                )
            for seed in controls.random_seeds:
                race = _run_reference(
                    protocol=protocol,
                    architecture=architecture,
                    family=family,
                    profile=profile,
                    random_seed=seed,
                )
                all_residuals = all(
                    residual.passed
                    for step in race.telemetry
                    for residual in step.residuals
                )
                record = BaselineRunRecord(
                        protocol.campaign_id,
                        protocol.fingerprint_sha256,
                        controls.fingerprint_sha256,
                        architecture.fingerprint_sha256,
                        family.family_id,
                        family.opportunity_fingerprint_sha256,
                        profile.circuit_id,
                        partitions[profile.circuit_id],
                        seed,
                        protocol.evidence_grade,
                        False,
                        width.status,
                        race.outcome,
                        race.reason,
                        race.final_state.time_s,
                        race.final_state.race_distance_m,
                        race.finish_distance_residual_m,
                        family.initial_primary_energy_j
                        - race.final_state.primary_energy_j,
                        race.replay.attempted_step_count,
                        race.replay.committed_step_count,
                        controls.evaluation_budget_per_run,
                        all_residuals,
                        len(race.replay.scenario_fingerprints),
                        race.replay_fingerprint_sha256,
                        "",
                    )
                runs.append(
                    replace(
                        record,
                        record_fingerprint_sha256=_fingerprint(
                            _run_record_identity_payload(record)
                        ),
                    )
                )
    ordered_runs = tuple(
        sorted(runs, key=lambda item: (item.family_id, item.circuit_id, item.random_seed))
    )
    expected = (
        len(protocol.reference_families)
        * len(ordered_profiles)
        * len(controls.random_seeds)
    )
    completed_profiles = {
        profile.circuit_id
        for profile in ordered_profiles
        if all(
            run.outcome == "finished"
            for run in ordered_runs
            if run.circuit_id == profile.circuit_id
        )
        and sum(run.circuit_id == profile.circuit_id for run in ordered_runs)
        == len(protocol.reference_families) * len(controls.random_seeds)
    }
    all_finished = len(ordered_runs) == expected and all(
        run.outcome == "finished" for run in ordered_runs
    )
    residuals_passed = all(run.all_residuals_passed for run in ordered_runs)
    within_budget = all(
        run.attempted_steps <= controls.evaluation_budget_per_run
        for run in ordered_runs
    )
    partition_complete = set(partitions) == {
        profile.circuit_id for profile in ordered_profiles
    }
    claim_boundary = (
        "Level-0 profile-distance analytical proxy only; synthetic local "
        "environment is not measured circuit evidence or physical validation"
    )
    result = BaselineCampaignResult(
        BASELINE_CAMPAIGN_MODEL_VERSION,
        protocol.campaign_id,
        protocol.fingerprint_sha256,
        controls.fingerprint_sha256,
        architecture.fingerprint_sha256,
        expected,
        sum(run.outcome == "finished" for run in ordered_runs),
        len(completed_profiles),
        len(ordered_profiles),
        all_finished,
        residuals_passed,
        within_budget,
        partition_complete,
        False,
        ordered_runs,
        "",
        claim_boundary,
    )
    return replace(
        result,
        result_fingerprint_sha256=_fingerprint(
            _campaign_result_identity_payload(result)
        ),
    )
