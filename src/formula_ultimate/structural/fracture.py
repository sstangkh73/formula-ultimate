"""Narrow LEFM fracture-initiation evaluator for Work 043."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Any, Mapping

from .acceptance import StructuralEvidenceError


@dataclass(frozen=True, slots=True)
class FractureMaterialRecord:
    material_id: str
    toughness_pa_sqrt_m: float
    yield_stress_pa: float
    youngs_modulus_pa: float
    provenance: str
    design_use_permitted: bool

    def __post_init__(self) -> None:
        if not self.material_id.strip() or not self.provenance.strip():
            raise StructuralEvidenceError("fracture material identity and provenance are required")
        for name, value in (("toughness_pa_sqrt_m", self.toughness_pa_sqrt_m), ("yield_stress_pa", self.yield_stress_pa), ("youngs_modulus_pa", self.youngs_modulus_pa)):
            if not math.isfinite(value) or value <= 0.0:
                raise StructuralEvidenceError(f"{name} must be finite and > 0")
        if self.design_use_permitted:
            raise StructuralEvidenceError("synthetic Work 043 material cannot be enabled for design use")


@dataclass(frozen=True, slots=True)
class CrackedCoupon:
    coupon_id: str
    length_m: float
    width_m: float
    thickness_m: float
    crack_half_length_m: float
    crack_model: str
    thickness_regime: str

    def __post_init__(self) -> None:
        if not self.coupon_id.strip():
            raise StructuralEvidenceError("coupon identity is required")
        for name, value in (("length_m", self.length_m), ("width_m", self.width_m), ("thickness_m", self.thickness_m), ("crack_half_length_m", self.crack_half_length_m)):
            if not math.isfinite(value) or value <= 0.0:
                raise StructuralEvidenceError(f"{name} must be finite and > 0")
        if self.crack_model != "ideal_infinite_plate_center_crack_Y1":
            raise StructuralEvidenceError("unsupported crack geometry-factor model")
        if self.thickness_regime != "plane_strain_screened":
            raise StructuralEvidenceError("thickness regime must be plane_strain_screened")

    @property
    def gross_area_m2(self) -> float:
        return self.width_m * self.thickness_m


@dataclass(frozen=True, slots=True)
class FractureEvaluation:
    applied_force_n: float
    nominal_stress_pa: float
    stress_intensity_pa_sqrt_m: float
    utilization: float
    initiated: bool
    reaction_force_n: float
    reaction_residual_relative: float
    external_work_j: float
    internal_energy_j: float
    energy_residual_relative: float
    event_id: str | None


def material_from_mapping(value: Mapping[str, Any]) -> FractureMaterialRecord:
    try:
        return FractureMaterialRecord(str(value["material_id"]), float(value["toughness_pa_sqrt_m"]), float(value["yield_stress_pa"]), float(value["youngs_modulus_pa"]), str(value["provenance"]), bool(value["design_use_permitted"]))
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, StructuralEvidenceError):
            raise
        raise StructuralEvidenceError(f"malformed fracture material: {exc}") from exc


def coupon_from_mapping(value: Mapping[str, Any], *, crack_half_length_m: float) -> CrackedCoupon:
    try:
        return CrackedCoupon(str(value["coupon_id"]), float(value["length_m"]), float(value["width_m"]), float(value["thickness_m"]), crack_half_length_m, str(value["crack_model"]), str(value["thickness_regime"]))
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, StructuralEvidenceError):
            raise
        raise StructuralEvidenceError(f"malformed cracked coupon: {exc}") from exc


def validate_lefm_domain(material: FractureMaterialRecord, coupon: CrackedCoupon, *, maximum_full_crack_width_ratio: float, maximum_plastic_zone_crack_ratio: float) -> dict[str, float]:
    if not (0.0 < maximum_full_crack_width_ratio <= 0.2):
        raise StructuralEvidenceError("finite-width domain limit must lie in (0, 0.2]")
    if not (0.0 < maximum_plastic_zone_crack_ratio <= 0.1):
        raise StructuralEvidenceError("plastic-zone domain limit must lie in (0, 0.1]")
    crack_width_ratio = 2.0 * coupon.crack_half_length_m / coupon.width_m
    if crack_width_ratio > maximum_full_crack_width_ratio:
        raise StructuralEvidenceError("crack exceeds ideal infinite-plate finite-width domain")
    required_thickness = 2.5 * (material.toughness_pa_sqrt_m / material.yield_stress_pa) ** 2
    if coupon.thickness_m < required_thickness:
        raise StructuralEvidenceError("coupon fails declared plane-strain thickness screen")
    initiation_stress = material.toughness_pa_sqrt_m / math.sqrt(math.pi * coupon.crack_half_length_m)
    if initiation_stress >= material.yield_stress_pa:
        raise StructuralEvidenceError("material yield precedes declared LEFM initiation")
    plastic_zone_m = (material.toughness_pa_sqrt_m / material.yield_stress_pa) ** 2 / (6.0 * math.pi)
    plastic_zone_ratio = plastic_zone_m / coupon.crack_half_length_m
    if plastic_zone_ratio > maximum_plastic_zone_crack_ratio:
        raise StructuralEvidenceError("coupon fails small-scale-yielding screen")
    return {"full_crack_width_ratio": crack_width_ratio, "required_plane_strain_thickness_m": required_thickness, "plane_strain_thickness_margin_m": coupon.thickness_m - required_thickness, "plastic_zone_m": plastic_zone_m, "plastic_zone_crack_ratio": plastic_zone_ratio, "initiation_stress_pa": initiation_stress, "initiation_force_n": initiation_stress * coupon.gross_area_m2}


def crack_representation(coupon: CrackedCoupon, *, segments_per_half_crack: int) -> dict[str, Any]:
    if segments_per_half_crack <= 0:
        raise StructuralEvidenceError("crack representation resolution must be positive")
    points = [(-coupon.crack_half_length_m + 2.0 * coupon.crack_half_length_m * index / (2 * segments_per_half_crack), 0.0) for index in range(2 * segments_per_half_crack + 1)]
    payload = {"coupon_id": coupon.coupon_id, "crack_model": coupon.crack_model, "left_tip_m": [-coupon.crack_half_length_m, 0.0], "right_tip_m": [coupon.crack_half_length_m, 0.0], "points_m": points}
    payload["sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return payload


def evaluate_fracture(material: FractureMaterialRecord, coupon: CrackedCoupon, *, applied_force_n: float, maximum_full_crack_width_ratio: float, maximum_plastic_zone_crack_ratio: float) -> FractureEvaluation:
    if not math.isfinite(applied_force_n) or applied_force_n < 0.0:
        raise StructuralEvidenceError("fracture applied force must be finite and >= 0")
    validate_lefm_domain(material, coupon, maximum_full_crack_width_ratio=maximum_full_crack_width_ratio, maximum_plastic_zone_crack_ratio=maximum_plastic_zone_crack_ratio)
    stress = applied_force_n / coupon.gross_area_m2
    intensity = stress * math.sqrt(math.pi * coupon.crack_half_length_m)
    utilization = intensity / material.toughness_pa_sqrt_m
    reaction = -applied_force_n
    displacement = applied_force_n * coupon.length_m / (material.youngs_modulus_pa * coupon.gross_area_m2)
    work = 0.5 * applied_force_n * displacement
    initiated = utilization >= 1.0 - 1.0e-12
    event_id = None
    if initiated:
        identity = {"material_id": material.material_id, "coupon_id": coupon.coupon_id, "a_m": coupon.crack_half_length_m, "force_n": applied_force_n, "mechanism": "LEFM_mode_I_initiation"}
        event_id = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return FractureEvaluation(applied_force_n, stress, intensity, utilization, initiated, reaction, abs(applied_force_n + reaction) / max(applied_force_n, 1.0), work, work, 0.0, event_id)
