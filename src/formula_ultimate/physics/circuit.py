"""Auditable Level-0 circuit inputs and pre-design envelope screening.

The circuit catalogue deliberately separates published facts from derived
design-pressure scores.  A profile is an early feasibility input, not a
surveyed racing line or a physically validated vehicle-dynamics model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import json
import math
from pathlib import Path
from typing import Any, Mapping


class CircuitInputError(ValueError):
    """Raised when circuit data violate the declared Level-0 boundary."""


PRESSURE_AXES = (
    "straight_speed",
    "low_speed_agility",
    "high_speed_cornering",
    "braking",
    "traction",
    "elevation",
    "thermal_cooling",
    "confinement",
)

_VALID_DIRECTIONS = {"clockwise", "counterclockwise", "unknown"}
_VALID_EVIDENCE_QUALITIES = {
    "official-championship",
    "official-circuit-operator",
    "official-event-organizer",
}


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise CircuitInputError(f"{name} must be finite; received {value!r}")


def _require_positive(name: str, value: float) -> None:
    _require_finite(name, value)
    if value <= 0.0:
        raise CircuitInputError(f"{name} must be > 0; received {value!r}")


@dataclass(frozen=True, slots=True)
class SourceEvidence:
    source_id: str
    publisher: str
    title: str
    url: str
    accessed_on: date
    quality: str
    supports: tuple[str, ...]

    def __post_init__(self) -> None:
        for name, value in (
            ("source_id", self.source_id),
            ("publisher", self.publisher),
            ("title", self.title),
            ("url", self.url),
        ):
            if not value.strip():
                raise CircuitInputError(f"{name} must not be blank")
        if not self.url.startswith("https://"):
            raise CircuitInputError("source URL must use https://")
        if self.quality not in _VALID_EVIDENCE_QUALITIES:
            raise CircuitInputError(
                f"unsupported evidence quality {self.quality!r}"
            )
        if not self.supports:
            raise CircuitInputError("source evidence must declare supported fields")


@dataclass(frozen=True, slots=True)
class PublishedWidth:
    minimum_m: float
    maximum_m: float | None
    source_id: str

    def __post_init__(self) -> None:
        _require_positive("minimum_m", self.minimum_m)
        if self.maximum_m is not None:
            _require_positive("maximum_m", self.maximum_m)
            if self.maximum_m < self.minimum_m:
                raise CircuitInputError("maximum_m must be >= minimum_m")
        if not self.source_id.strip():
            raise CircuitInputError("width source_id must not be blank")


@dataclass(frozen=True, slots=True)
class DesignPressure:
    """Ordinal screening scores on a closed 0..1 scale, not measurements."""

    straight_speed: float
    low_speed_agility: float
    high_speed_cornering: float
    braking: float
    traction: float
    elevation: float
    thermal_cooling: float
    confinement: float

    def __post_init__(self) -> None:
        for axis in PRESSURE_AXES:
            value = getattr(self, axis)
            _require_finite(axis, value)
            if not 0.0 <= value <= 1.0:
                raise CircuitInputError(f"{axis} must be in [0, 1]")

    def as_tuple(self) -> tuple[float, ...]:
        return tuple(getattr(self, axis) for axis in PRESSURE_AXES)


@dataclass(frozen=True, slots=True)
class EnvelopeAssessment:
    circuit_id: str
    status: str
    vehicle_width_m: float
    required_static_corridor_m: float
    available_published_width_m: float | None
    reason: str


@dataclass(frozen=True, slots=True)
class CircuitProfile:
    circuit_id: str
    name: str
    country: str
    layout_reference: str
    circuit_type: str
    direction: str
    lap_length_m: float
    race_laps: int
    race_distance_m: float
    turns: int
    reference_altitude_m: float | None
    published_width: PublishedWidth | None
    unresolved_width_reason: str | None
    design_pressure: DesignPressure
    design_strengths: tuple[str, ...]
    design_weaknesses: tuple[str, ...]
    sources: tuple[SourceEvidence, ...]

    def __post_init__(self) -> None:
        for name, value in (
            ("circuit_id", self.circuit_id),
            ("name", self.name),
            ("country", self.country),
            ("layout_reference", self.layout_reference),
            ("circuit_type", self.circuit_type),
        ):
            if not value.strip():
                raise CircuitInputError(f"{name} must not be blank")
        if self.direction not in _VALID_DIRECTIONS:
            raise CircuitInputError(f"invalid direction {self.direction!r}")
        _require_positive("lap_length_m", self.lap_length_m)
        _require_positive("race_distance_m", self.race_distance_m)
        if self.race_laps <= 0:
            raise CircuitInputError("race_laps must be > 0")
        if self.turns <= 0:
            raise CircuitInputError("turns must be > 0")
        if self.reference_altitude_m is not None:
            _require_finite("reference_altitude_m", self.reference_altitude_m)
            if not -500.0 <= self.reference_altitude_m <= 11_000.0:
                raise CircuitInputError(
                    "reference_altitude_m must be in [-500, 11000]"
                )
        if not self.sources:
            raise CircuitInputError("circuit must provide source evidence")
        source_ids = {source.source_id for source in self.sources}
        if len(source_ids) != len(self.sources):
            raise CircuitInputError("source_id values must be unique per circuit")
        if self.published_width is None:
            if not self.unresolved_width_reason:
                raise CircuitInputError(
                    "missing width must include unresolved_width_reason"
                )
        elif self.published_width.source_id not in source_ids:
            raise CircuitInputError("published width references an unknown source_id")
        if not self.design_strengths or not self.design_weaknesses:
            raise CircuitInputError(
                "each circuit must declare derived strengths and weaknesses"
            )
        nominal_distance_m = self.lap_length_m * self.race_laps
        if abs(self.race_distance_m - nominal_distance_m) >= self.lap_length_m:
            raise CircuitInputError(
                "race distance residual must be smaller than one lap"
            )

    @property
    def nominal_lap_product_m(self) -> float:
        return self.lap_length_m * self.race_laps

    @property
    def race_start_offset_m(self) -> float:
        """Official distance minus rounded lap length times lap count.

        This is observable metadata, not an error correction.  Published lap
        lengths are rounded and the start line may be offset from the finish.
        """

        return self.race_distance_m - self.nominal_lap_product_m

    @property
    def isa_air_density_kg_per_m3(self) -> float | None:
        if self.reference_altitude_m is None:
            return None
        return isa_air_density_kg_per_m3(self.reference_altitude_m)

    def assess_static_width(
        self,
        *,
        vehicle_width_m: float,
        clearance_per_side_m: float = 0.5,
        evidence_allowance_m: float = 0.0,
    ) -> EnvelopeAssessment:
        """Apply a necessary static-width screen before any vehicle simulation.

        The screen does not prove cornering feasibility.  Steering geometry,
        wheelbase, swept path, barriers, kerbs and a surveyed 3D corridor are
        intentionally deferred to a higher validation level.
        """

        _require_positive("vehicle_width_m", vehicle_width_m)
        for name, value in (
            ("clearance_per_side_m", clearance_per_side_m),
            ("evidence_allowance_m", evidence_allowance_m),
        ):
            _require_finite(name, value)
            if value < 0.0:
                raise CircuitInputError(f"{name} must be >= 0")
        required_m = (
            vehicle_width_m + 2.0 * clearance_per_side_m + evidence_allowance_m
        )
        if self.published_width is None:
            return EnvelopeAssessment(
                circuit_id=self.circuit_id,
                status="indeterminate",
                vehicle_width_m=vehicle_width_m,
                required_static_corridor_m=required_m,
                available_published_width_m=None,
                reason=self.unresolved_width_reason or "width evidence unavailable",
            )
        available_m = self.published_width.minimum_m
        if required_m > available_m:
            status = "rejected"
            reason = "required static corridor exceeds published minimum width"
        else:
            status = "screen_passed"
            reason = (
                "static width screen passed; swept-path and 3D corridor evidence "
                "are still required"
            )
        return EnvelopeAssessment(
            circuit_id=self.circuit_id,
            status=status,
            vehicle_width_m=vehicle_width_m,
            required_static_corridor_m=required_m,
            available_published_width_m=available_m,
            reason=reason,
        )


def isa_air_density_kg_per_m3(altitude_m: float) -> float:
    """Return dry-air density in the ISA troposphere for -500..11000 m.

    Constants use SI units: T0=288.15 K, p0=101325 Pa, lapse rate
    L=0.0065 K/m, g0=9.80665 m/s^2, and specific gas constant
    R=287.05287 J/(kg*K).
    """

    _require_finite("altitude_m", altitude_m)
    if not -500.0 <= altitude_m <= 11_000.0:
        raise CircuitInputError("altitude_m must be in [-500, 11000]")
    sea_level_temperature_k = 288.15
    sea_level_pressure_pa = 101_325.0
    lapse_rate_k_per_m = 0.0065
    gravity_mps2 = 9.80665
    gas_constant_j_per_kg_k = 287.05287
    temperature_k = sea_level_temperature_k - lapse_rate_k_per_m * altitude_m
    exponent = gravity_mps2 / (gas_constant_j_per_kg_k * lapse_rate_k_per_m)
    pressure_pa = sea_level_pressure_pa * (
        temperature_k / sea_level_temperature_k
    ) ** exponent
    density = pressure_pa / (gas_constant_j_per_kg_k * temperature_k)
    if not math.isfinite(density) or density <= 0.0:
        raise CircuitInputError("ISA calculation produced an invalid density")
    return density


def _source_from_dict(raw: Mapping[str, Any]) -> SourceEvidence:
    return SourceEvidence(
        source_id=str(raw["source_id"]),
        publisher=str(raw["publisher"]),
        title=str(raw["title"]),
        url=str(raw["url"]),
        accessed_on=date.fromisoformat(str(raw["accessed_on"])),
        quality=str(raw["quality"]),
        supports=tuple(str(item) for item in raw["supports"]),
    )


def _profile_from_dict(raw: Mapping[str, Any]) -> CircuitProfile:
    width_raw = raw.get("published_width")
    published_width = None
    if width_raw is not None:
        published_width = PublishedWidth(
            minimum_m=float(width_raw["minimum_m"]),
            maximum_m=(
                None
                if width_raw.get("maximum_m") is None
                else float(width_raw["maximum_m"])
            ),
            source_id=str(width_raw["source_id"]),
        )
    pressure_raw = raw["design_pressure"]
    return CircuitProfile(
        circuit_id=str(raw["circuit_id"]),
        name=str(raw["name"]),
        country=str(raw["country"]),
        layout_reference=str(raw["layout_reference"]),
        circuit_type=str(raw["circuit_type"]),
        direction=str(raw["direction"]),
        lap_length_m=float(raw["lap_length_m"]),
        race_laps=int(raw["race_laps"]),
        race_distance_m=float(raw["race_distance_m"]),
        turns=int(raw["turns"]),
        reference_altitude_m=(
            None
            if raw.get("reference_altitude_m") is None
            else float(raw["reference_altitude_m"])
        ),
        published_width=published_width,
        unresolved_width_reason=(
            None
            if raw.get("unresolved_width_reason") is None
            else str(raw["unresolved_width_reason"])
        ),
        design_pressure=DesignPressure(
            **{axis: float(pressure_raw[axis]) for axis in PRESSURE_AXES}
        ),
        design_strengths=tuple(str(item) for item in raw["design_strengths"]),
        design_weaknesses=tuple(str(item) for item in raw["design_weaknesses"]),
        sources=tuple(_source_from_dict(item) for item in raw["sources"]),
    )


def load_circuit_catalog(path: str | Path) -> tuple[CircuitProfile, ...]:
    """Load and validate a deterministic circuit catalogue from JSON."""

    catalog_path = Path(path)
    try:
        raw = json.loads(catalog_path.read_text(encoding="utf-8"))
        if raw["schema_version"] != "1.0":
            raise CircuitInputError(
                f"unsupported schema_version {raw['schema_version']!r}"
            )
        profiles = tuple(_profile_from_dict(item) for item in raw["circuits"])
    except CircuitInputError:
        raise
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise CircuitInputError(f"invalid circuit catalogue: {exc}") from exc
    ids = [profile.circuit_id for profile in profiles]
    if len(ids) != len(set(ids)):
        raise CircuitInputError("circuit_id values must be unique")
    return profiles
