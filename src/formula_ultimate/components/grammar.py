"""Versioned, constrained component grammar primitives.

Version 1 intentionally describes only one mounting-plate family.  It is a
geometry/interface gate, not evidence of strength or manufacturability.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any, Mapping


GRAMMAR_VERSION = "mounting_plate_v1"
MIN_EDGE_LIGAMENT_M = 0.006
MIN_INTERNAL_WEB_M = 0.006


class GrammarViolation(ValueError):
    """Raised when a component cannot be expressed by the declared grammar."""


def _finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise GrammarViolation(f"{name} must be finite; received {value!r}")


def _bounded(name: str, value: float, lower: float, upper: float) -> None:
    _finite(name, value)
    if not lower <= value <= upper:
        raise GrammarViolation(
            f"{name} must be in [{lower}, {upper}] m; received {value!r}"
        )


@dataclass(frozen=True, slots=True)
class Material:
    """A named constant-density material assumption in SI units."""

    name: str
    density_kg_per_m3: float

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise GrammarViolation("material name must not be empty")
        _finite("density_kg_per_m3", self.density_kg_per_m3)
        if self.density_kg_per_m3 <= 0.0:
            raise GrammarViolation("density_kg_per_m3 must be > 0")


@dataclass(frozen=True, slots=True)
class MountingPlateSpec:
    """A bounded rounded plate, four mounting holes, and optional centre cut.

    All dimensional inputs are metres.  Hole positions are symmetric about the
    plate centre and therefore form an immutable four-port mounting interface.
    """

    length_m: float
    width_m: float
    thickness_m: float
    corner_radius_m: float
    mounting_hole_diameter_m: float
    mounting_spacing_x_m: float
    mounting_spacing_y_m: float
    lightening_radius_m: float
    material: Material
    grammar_version: str = GRAMMAR_VERSION

    def __post_init__(self) -> None:
        if self.grammar_version != GRAMMAR_VERSION:
            raise GrammarViolation(
                f"grammar_version must be {GRAMMAR_VERSION!r}; "
                f"received {self.grammar_version!r}"
            )

        _bounded("length_m", self.length_m, 0.12, 0.30)
        _bounded("width_m", self.width_m, 0.08, 0.20)
        _bounded("thickness_m", self.thickness_m, 0.004, 0.015)
        _bounded("corner_radius_m", self.corner_radius_m, 0.002, 0.030)
        _bounded(
            "mounting_hole_diameter_m",
            self.mounting_hole_diameter_m,
            0.005,
            0.012,
        )
        _bounded("mounting_spacing_x_m", self.mounting_spacing_x_m, 0.012, 0.260)
        _bounded("mounting_spacing_y_m", self.mounting_spacing_y_m, 0.012, 0.160)
        _bounded("lightening_radius_m", self.lightening_radius_m, 0.0, 0.080)

        if self.corner_radius_m > min(self.length_m, self.width_m) / 4.0:
            raise GrammarViolation("corner_radius_m exceeds one quarter of the width")

        hole_radius_m = self.mounting_hole_diameter_m / 2.0
        edge_x_m = (self.length_m - self.mounting_spacing_x_m) / 2.0
        edge_y_m = (self.width_m - self.mounting_spacing_y_m) / 2.0
        required_edge_m = hole_radius_m + MIN_EDGE_LIGAMENT_M
        if edge_x_m < required_edge_m or edge_y_m < required_edge_m:
            raise GrammarViolation(
                "mounting holes violate the minimum outer-edge ligament"
            )

        # Axis-aligned margins alone are insufficient near a rounded corner.
        # Check the hole centre against the plate profile inset by the required
        # hole-edge ligament.  Rounded-rectangle corner centres do not move
        # under this inward offset.
        if self.corner_radius_m > required_edge_m:
            corner_centre_x_m = self.length_m / 2.0 - self.corner_radius_m
            corner_centre_y_m = self.width_m / 2.0 - self.corner_radius_m
            hole_x_m = self.mounting_spacing_x_m / 2.0
            hole_y_m = self.mounting_spacing_y_m / 2.0
            if hole_x_m > corner_centre_x_m and hole_y_m > corner_centre_y_m:
                inset_corner_radius_m = self.corner_radius_m - required_edge_m
                if math.hypot(
                    hole_x_m - corner_centre_x_m,
                    hole_y_m - corner_centre_y_m,
                ) > inset_corner_radius_m:
                    raise GrammarViolation(
                        "mounting holes violate the rounded-corner ligament"
                    )

        minimum_hole_pitch_m = self.mounting_hole_diameter_m + MIN_INTERNAL_WEB_M
        if (
            self.mounting_spacing_x_m < minimum_hole_pitch_m
            or self.mounting_spacing_y_m < minimum_hole_pitch_m
        ):
            raise GrammarViolation("mounting holes violate the minimum hole-to-hole web")

        if self.lightening_radius_m > 0.0:
            outer_clearance_m = (
                min(self.length_m, self.width_m) / 2.0
                - self.lightening_radius_m
            )
            if outer_clearance_m < MIN_EDGE_LIGAMENT_M:
                raise GrammarViolation(
                    "lightening cut violates the minimum outer-edge ligament"
                )

            nearest_hole_distance_m = math.hypot(
                self.mounting_spacing_x_m / 2.0,
                self.mounting_spacing_y_m / 2.0,
            )
            web_to_mounting_hole_m = (
                nearest_hole_distance_m
                - self.lightening_radius_m
                - hole_radius_m
            )
            if web_to_mounting_hole_m < MIN_INTERNAL_WEB_M:
                raise GrammarViolation(
                    "lightening cut violates the minimum web to a mounting hole"
                )

    @property
    def mounting_hole_centres_m(self) -> tuple[tuple[float, float], ...]:
        half_x_m = self.mounting_spacing_x_m / 2.0
        half_y_m = self.mounting_spacing_y_m / 2.0
        return (
            (-half_x_m, -half_y_m),
            (-half_x_m, half_y_m),
            (half_x_m, -half_y_m),
            (half_x_m, half_y_m),
        )

    @property
    def analytical_volume_m3(self) -> float:
        """Return the exact volume of the declared prismatic grammar shape."""

        rounded_area_m2 = (
            self.length_m * self.width_m
            - (4.0 - math.pi) * self.corner_radius_m**2
        )
        mounting_cut_area_m2 = 4.0 * math.pi * (
            self.mounting_hole_diameter_m / 2.0
        ) ** 2
        lightening_cut_area_m2 = math.pi * self.lightening_radius_m**2
        return (
            rounded_area_m2 - mounting_cut_area_m2 - lightening_cut_area_m2
        ) * self.thickness_m

    @property
    def analytical_mass_kg(self) -> float:
        return self.analytical_volume_m3 * self.material.density_kg_per_m3

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "MountingPlateSpec":
        expected = {
            "length_m",
            "width_m",
            "thickness_m",
            "corner_radius_m",
            "mounting_hole_diameter_m",
            "mounting_spacing_x_m",
            "mounting_spacing_y_m",
            "lightening_radius_m",
            "material",
            "grammar_version",
        }
        unknown = set(value) - expected
        missing = (expected - {"grammar_version"}) - set(value)
        if unknown or missing:
            raise GrammarViolation(
                f"spec keys mismatch; missing={sorted(missing)}, unknown={sorted(unknown)}"
            )
        material_value = value["material"]
        if not isinstance(material_value, Mapping):
            raise GrammarViolation("material must be an object")
        material_unknown = set(material_value) - {"name", "density_kg_per_m3"}
        material_missing = {"name", "density_kg_per_m3"} - set(material_value)
        if material_unknown or material_missing:
            raise GrammarViolation(
                "material keys mismatch; "
                f"missing={sorted(material_missing)}, unknown={sorted(material_unknown)}"
            )
        try:
            material = Material(
                name=str(material_value["name"]),
                density_kg_per_m3=float(material_value["density_kg_per_m3"]),
            )
            return cls(
                length_m=float(value["length_m"]),
                width_m=float(value["width_m"]),
                thickness_m=float(value["thickness_m"]),
                corner_radius_m=float(value["corner_radius_m"]),
                mounting_hole_diameter_m=float(value["mounting_hole_diameter_m"]),
                mounting_spacing_x_m=float(value["mounting_spacing_x_m"]),
                mounting_spacing_y_m=float(value["mounting_spacing_y_m"]),
                lightening_radius_m=float(value["lightening_radius_m"]),
                material=material,
                grammar_version=str(value.get("grammar_version", GRAMMAR_VERSION)),
            )
        except (TypeError, ValueError) as exc:
            if isinstance(exc, GrammarViolation):
                raise
            raise GrammarViolation(f"spec contains a non-numeric value: {exc}") from exc
