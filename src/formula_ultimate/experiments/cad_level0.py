"""Evidence contract connecting independent CAD measurements to Level 0."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any, Mapping

from formula_ultimate.components.grammar import MountingPlateSpec
from formula_ultimate.physics.longitudinal import (
    EnvironmentParameters,
    SimulationConfig,
    VehicleParameters,
    simulate_constant_traction,
)


class EvidenceViolation(ValueError):
    """Raised when CAD evidence cannot be admitted to Level 0."""


@dataclass(frozen=True, slots=True)
class CadMeasurement:
    source: str
    volume_m3: float
    solid_count: int
    is_valid: bool
    bounds_m: tuple[float, float, float]
    centre_of_mass_m: tuple[float, float, float]

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise EvidenceViolation("CAD measurement source must not be empty")
        if len(self.bounds_m) != 3 or len(self.centre_of_mass_m) != 3:
            raise EvidenceViolation("CAD bounds and centre of mass must have 3 values")
        if type(self.solid_count) is not int:
            raise EvidenceViolation("CAD solid_count must be an integer")
        if type(self.is_valid) is not bool:
            raise EvidenceViolation("CAD is_valid must be a boolean")
        values = (self.volume_m3, *self.bounds_m, *self.centre_of_mass_m)
        if not all(math.isfinite(value) for value in values):
            raise EvidenceViolation("CAD measurement contains a non-finite value")
        if self.volume_m3 <= 0.0:
            raise EvidenceViolation("CAD volume must be > 0")
        if self.solid_count != 1:
            raise EvidenceViolation(
                f"expected exactly one solid; received {self.solid_count}"
            )
        if not self.is_valid:
            raise EvidenceViolation("CAD system reported an invalid shape")
        if any(length <= 0.0 for length in self.bounds_m):
            raise EvidenceViolation("all CAD bounding-box lengths must be > 0")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CadMeasurement":
        try:
            if type(value["solid_count"]) is not int:
                raise EvidenceViolation("CAD solid_count must be an integer")
            if type(value["is_valid"]) is not bool:
                raise EvidenceViolation("CAD is_valid must be a boolean")
            return cls(
                source=str(value["source"]),
                volume_m3=float(value["volume_m3"]),
                solid_count=value["solid_count"],
                is_valid=value["is_valid"],
                bounds_m=tuple(float(v) for v in value["bounds_m"]),  # type: ignore[arg-type]
                centre_of_mass_m=tuple(  # type: ignore[arg-type]
                    float(v) for v in value["centre_of_mass_m"]
                ),
            )
        except (KeyError, TypeError, ValueError) as exc:
            if isinstance(exc, EvidenceViolation):
                raise
            raise EvidenceViolation(f"malformed CAD measurement: {exc}") from exc


@dataclass(frozen=True, slots=True)
class Level0Controls:
    base_vehicle_mass_kg: float
    tractive_force_n: float
    duration_s: float
    time_step_s: float

    def __post_init__(self) -> None:
        values = (
            self.base_vehicle_mass_kg,
            self.tractive_force_n,
            self.duration_s,
            self.time_step_s,
        )
        if not all(math.isfinite(value) for value in values):
            raise EvidenceViolation("Level 0 controls must be finite")
        if self.base_vehicle_mass_kg <= 0.0:
            raise EvidenceViolation("base_vehicle_mass_kg must be > 0")
        if self.tractive_force_n < 0.0 or self.duration_s < 0.0:
            raise EvidenceViolation("force and duration must be >= 0")
        if self.time_step_s <= 0.0:
            raise EvidenceViolation("time_step_s must be > 0")


@dataclass(frozen=True, slots=True)
class CadLevel0Result:
    component_mass_kg: float
    total_vehicle_mass_kg: float
    final_speed_mps: float
    final_distance_m: float
    analytical_volume_m3: float
    measured_volume_m3: float
    volume_residual_m3: float
    volume_relative_residual: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def evaluate_cad_measurement(
    *,
    spec: MountingPlateSpec,
    measurement: CadMeasurement,
    controls: Level0Controls,
    volume_absolute_tolerance_m3: float = 1.0e-10,
    volume_relative_tolerance: float = 1.0e-6,
    bounds_absolute_tolerance_m: float = 1.0e-7,
) -> CadLevel0Result:
    """Gate a CAD measurement and use only its volume for Level 0 mass."""

    expected_bounds_m = (spec.length_m, spec.width_m, spec.thickness_m)
    for actual, expected in zip(measurement.bounds_m, expected_bounds_m, strict=True):
        if not math.isclose(actual, expected, abs_tol=bounds_absolute_tolerance_m):
            raise EvidenceViolation(
                f"CAD bound {actual} m disagrees with expected {expected} m"
            )

    residual_m3 = measurement.volume_m3 - spec.analytical_volume_m3
    relative_residual = abs(residual_m3) / spec.analytical_volume_m3
    if not math.isclose(
        measurement.volume_m3,
        spec.analytical_volume_m3,
        rel_tol=volume_relative_tolerance,
        abs_tol=volume_absolute_tolerance_m3,
    ):
        raise EvidenceViolation(
            "measured and analytical volumes disagree: "
            f"residual={residual_m3} m^3, relative={relative_residual}"
        )

    component_mass_kg = (
        measurement.volume_m3 * spec.material.density_kg_per_m3
    )
    total_vehicle_mass_kg = controls.base_vehicle_mass_kg + component_mass_kg
    simulation = simulate_constant_traction(
        vehicle=VehicleParameters(mass_kg=total_vehicle_mass_kg),
        environment=EnvironmentParameters(),
        config=SimulationConfig(
            duration_s=controls.duration_s,
            time_step_s=controls.time_step_s,
        ),
        tractive_force_n=controls.tractive_force_n,
    )
    return CadLevel0Result(
        component_mass_kg=component_mass_kg,
        total_vehicle_mass_kg=total_vehicle_mass_kg,
        final_speed_mps=simulation.final_state.speed_mps,
        final_distance_m=simulation.final_state.position_m,
        analytical_volume_m3=spec.analytical_volume_m3,
        measured_volume_m3=measurement.volume_m3,
        volume_residual_m3=residual_m3,
        volume_relative_residual=relative_residual,
    )
