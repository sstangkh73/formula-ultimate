"""Work 075 small-angle rocker geometry and virtual-work transformation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
import math
from typing import Any, Mapping, Sequence

from .sprung_body_vertical_coupling import SprungBodyVerticalConfig


MODEL_VERSION = "geometry_linkage_motion_ratio_v1"


class LinkageMotionRatioError(ValueError):
    """Raised when linkage geometry cannot define a physical motion ratio."""


def _finite(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise LinkageMotionRatioError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise LinkageMotionRatioError(f"{name} must be finite")
    return result


def _positive(name: str, value: Any) -> float:
    result = _finite(name, value)
    if result <= 0.0:
        raise LinkageMotionRatioError(f"{name} must be positive")
    return result


def _vector(name: str, value: Any) -> tuple[float, float, float]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 3:
        raise LinkageMotionRatioError(f"{name} must contain three coordinates")
    return tuple(_finite(f"{name}[{index}]", item) for index, item in enumerate(value))  # type: ignore[return-value]


def _subtract(left: tuple[float, ...], right: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(a - b for a, b in zip(left, right))


def _dot(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return math.fsum(a * b for a, b in zip(left, right))


def _cross(left: tuple[float, float, float], right: tuple[float, float, float]) -> tuple[float, float, float]:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def _normalize(name: str, vector: tuple[float, float, float]) -> tuple[float, float, float]:
    length = math.sqrt(_dot(vector, vector))
    if length <= 0.0:
        raise LinkageMotionRatioError(f"{name} must be non-zero")
    return tuple(item / length for item in vector)  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class RockerLinkageGeometry:
    contact_id: str
    pivot_m: tuple[float, float, float]
    rotation_axis: tuple[float, float, float]
    wheel_pickup_m: tuple[float, float, float]
    spring_pickup_m: tuple[float, float, float]
    wheel_direction: tuple[float, float, float]
    spring_direction: tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class LinkageMotionRatioConfig:
    protocol_id: str
    linkages: tuple[RockerLinkageGeometry, ...]
    geometry_absolute_tolerance_m: float
    ratio_absolute_tolerance: float
    energy_relative_tolerance: float


@dataclass(frozen=True, slots=True)
class MotionRatioEvidence:
    contact_id: str
    normalized_rotation_axis: tuple[float, float, float]
    normalized_wheel_direction: tuple[float, float, float]
    normalized_spring_direction: tuple[float, float, float]
    wheel_arm_m: tuple[float, float, float]
    spring_arm_m: tuple[float, float, float]
    projected_wheel_lever_m: float
    projected_spring_lever_m: float
    motion_ratio: float
    stiffness_scale: float
    damping_scale: float
    travel_scale: float


@dataclass(frozen=True, slots=True)
class LinkageApplication:
    model_version: str
    protocol_id: str
    evidence: tuple[MotionRatioEvidence, ...]
    transformed_vertical: SprungBodyVerticalConfig
    application_sha256: str


def _load_linkage(item: Mapping[str, Any]) -> RockerLinkageGeometry:
    contact_id = item.get("contact_id")
    if not isinstance(contact_id, str) or not contact_id:
        raise LinkageMotionRatioError("linkage contact_id must be non-empty")
    return RockerLinkageGeometry(
        contact_id,
        _vector(f"{contact_id}.pivot_m", item.get("pivot_m")),
        _vector(f"{contact_id}.rotation_axis", item.get("rotation_axis")),
        _vector(f"{contact_id}.wheel_pickup_m", item.get("wheel_pickup_m")),
        _vector(f"{contact_id}.spring_pickup_m", item.get("spring_pickup_m")),
        _vector(f"{contact_id}.wheel_direction", item.get("wheel_direction")),
        _vector(f"{contact_id}.spring_direction", item.get("spring_direction")),
    )


def load_linkage_motion_ratio_config(
    raw: Mapping[str, Any], *, geometry_section: str = "linkages"
) -> LinkageMotionRatioConfig:
    if raw.get("model_version") != MODEL_VERSION:
        raise LinkageMotionRatioError("linkage model version mismatch")
    protocol = raw.get("protocol_id")
    if not isinstance(protocol, str) or not protocol:
        raise LinkageMotionRatioError("protocol_id must be non-empty")
    values = raw.get(geometry_section)
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)) or not values:
        raise LinkageMotionRatioError(f"{geometry_section} must be a non-empty sequence")
    if not all(isinstance(item, Mapping) for item in values):
        raise LinkageMotionRatioError("each linkage must be a mapping")
    linkages = tuple(_load_linkage(item) for item in values)
    if len({item.contact_id for item in linkages}) != len(linkages):
        raise LinkageMotionRatioError("linkage contact_id values must be unique")
    numerical = raw.get("numerical")
    if not isinstance(numerical, Mapping):
        raise LinkageMotionRatioError("missing numerical section")
    geometry_tolerance = _positive(
        "geometry_absolute_tolerance_m", numerical.get("geometry_absolute_tolerance_m")
    )
    ratio_tolerance = _positive(
        "ratio_absolute_tolerance", numerical.get("ratio_absolute_tolerance")
    )
    energy_tolerance = _positive(
        "energy_relative_tolerance", numerical.get("energy_relative_tolerance")
    )
    if geometry_tolerance > 1.0e-9 or ratio_tolerance > 1.0e-9 or energy_tolerance > 1.0e-3:
        raise LinkageMotionRatioError("linkage tolerance exceeds protocol ceiling")
    return LinkageMotionRatioConfig(
        protocol, linkages, geometry_tolerance, ratio_tolerance, energy_tolerance
    )


def derive_motion_ratio(
    linkage: RockerLinkageGeometry, *, geometry_tolerance_m: float = 1.0e-12
) -> MotionRatioEvidence:
    tolerance = _positive("geometry_tolerance_m", geometry_tolerance_m)
    axis = _normalize("rotation_axis", linkage.rotation_axis)
    wheel_direction = _normalize("wheel_direction", linkage.wheel_direction)
    spring_direction = _normalize("spring_direction", linkage.spring_direction)
    wheel_arm = _subtract(linkage.wheel_pickup_m, linkage.pivot_m)
    spring_arm = _subtract(linkage.spring_pickup_m, linkage.pivot_m)
    wheel_lever = _dot(wheel_direction, _cross(axis, wheel_arm))
    spring_lever = _dot(spring_direction, _cross(axis, spring_arm))
    if abs(wheel_lever) <= tolerance:
        raise LinkageMotionRatioError("projected wheel lever is degenerate")
    if abs(spring_lever) <= tolerance:
        raise LinkageMotionRatioError("projected spring lever is degenerate")
    signed_ratio = spring_lever / wheel_lever
    if signed_ratio <= 0.0:
        raise LinkageMotionRatioError("wheel and spring compression directions disagree")
    ratio = _positive("motion_ratio", signed_ratio)
    return MotionRatioEvidence(
        linkage.contact_id,
        axis,
        wheel_direction,
        spring_direction,
        wheel_arm,  # type: ignore[arg-type]
        spring_arm,  # type: ignore[arg-type]
        wheel_lever,
        spring_lever,
        ratio,
        ratio * ratio,
        ratio * ratio,
        1.0 / ratio,
    )


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def apply_linkage_motion_ratios(
    config: LinkageMotionRatioConfig, vertical: SprungBodyVerticalConfig
) -> LinkageApplication:
    geometry = {item.contact_id: item for item in config.linkages}
    contact_ids = {item.contact_id for item in vertical.contacts}
    if set(geometry) != contact_ids:
        raise LinkageMotionRatioError("linkage identities do not exactly cover vertical contacts")
    evidence = tuple(
        derive_motion_ratio(
            geometry[item.contact_id],
            geometry_tolerance_m=config.geometry_absolute_tolerance_m,
        )
        for item in vertical.contacts
    )
    by_contact = {item.contact_id: item for item in evidence}
    transformed_contacts = tuple(
        replace(
            item,
            suspension_stiffness_n_per_m=(
                item.suspension_stiffness_n_per_m
                * by_contact[item.contact_id].stiffness_scale
            ),
            suspension_damping_n_s_per_m=(
                item.suspension_damping_n_s_per_m
                * by_contact[item.contact_id].damping_scale
            ),
            maximum_compression_m=(
                item.maximum_compression_m * by_contact[item.contact_id].travel_scale
            ),
            maximum_rebound_m=(
                item.maximum_rebound_m * by_contact[item.contact_id].travel_scale
            ),
        )
        for item in vertical.contacts
    )
    transformed = replace(vertical, contacts=transformed_contacts)
    body = {
        "model_version": MODEL_VERSION,
        "protocol_id": config.protocol_id,
        "evidence": [asdict(item) for item in evidence],
        "contacts": [asdict(item) for item in transformed_contacts],
    }
    identity = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    return LinkageApplication(MODEL_VERSION, config.protocol_id, evidence, transformed, identity)


def application_to_mapping(application: LinkageApplication) -> dict[str, Any]:
    return asdict(application)
