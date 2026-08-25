"""Deterministic Level-0 tyre-road combined-force capacity boundary.

This is a friction circle/ellipse, not a slip-based physical tyre model.
Requested and applied forces remain separate so saturation is never hidden.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


class TyreInputError(ValueError):
    """Raised when tyre contact inputs violate the declared model boundary."""


class TyreNumericalError(ArithmeticError):
    """Raised when finite inputs cannot produce a finite normalized state."""


def _finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise TyreInputError(f"{name} must be finite; received {value!r}")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise TyreInputError(f"{name} must be > 0; received {value!r}")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise TyreInputError(f"{name} must be >= 0; received {value!r}")


@dataclass(frozen=True, slots=True)
class TyreContactParameters:
    """Fixed contact capacity parameters in SI-compatible form."""

    friction_coefficient_longitudinal: float
    friction_coefficient_lateral: float
    boundary_tolerance: float = 1.0e-12

    def __post_init__(self) -> None:
        _positive(
            "friction_coefficient_longitudinal",
            self.friction_coefficient_longitudinal,
        )
        _positive(
            "friction_coefficient_lateral", self.friction_coefficient_lateral
        )
        _nonnegative("boundary_tolerance", self.boundary_tolerance)
        if self.boundary_tolerance > 1.0e-6:
            raise TyreInputError("boundary_tolerance must be <= 1e-6")


@dataclass(frozen=True, slots=True)
class TyreForceRequest:
    longitudinal_force_n: float
    lateral_force_n: float

    def __post_init__(self) -> None:
        _finite("longitudinal_force_n", self.longitudinal_force_n)
        _finite("lateral_force_n", self.lateral_force_n)


@dataclass(frozen=True, slots=True)
class TyreForceResult:
    status: str
    reason: str
    normal_load_n: float
    longitudinal_limit_n: float
    lateral_limit_n: float
    requested_longitudinal_force_n: float
    requested_lateral_force_n: float
    applied_longitudinal_force_n: float
    applied_lateral_force_n: float
    residual_longitudinal_force_n: float
    residual_lateral_force_n: float
    requested_utilization: float | None
    applied_utilization: float | None
    saturation_scale: float
    saturated: bool


def resolve_tyre_force(
    *,
    parameters: TyreContactParameters,
    normal_load_n: float,
    request: TyreForceRequest,
) -> TyreForceResult:
    """Apply one friction ellipse while preserving the original force request."""

    _nonnegative("normal_load_n", normal_load_n)
    fx_requested = request.longitudinal_force_n
    fy_requested = request.lateral_force_n
    fx_limit = parameters.friction_coefficient_longitudinal * normal_load_n
    fy_limit = parameters.friction_coefficient_lateral * normal_load_n

    if normal_load_n == 0.0:
        zero_request = fx_requested == 0.0 and fy_requested == 0.0
        return TyreForceResult(
            status=(
                "no_contact_zero_request" if zero_request else "no_normal_load"
            ),
            reason=(
                "zero normal load and zero requested force"
                if zero_request
                else "zero normal load cannot transmit requested tyre force"
            ),
            normal_load_n=normal_load_n,
            longitudinal_limit_n=0.0,
            lateral_limit_n=0.0,
            requested_longitudinal_force_n=fx_requested,
            requested_lateral_force_n=fy_requested,
            applied_longitudinal_force_n=0.0,
            applied_lateral_force_n=0.0,
            residual_longitudinal_force_n=fx_requested,
            residual_lateral_force_n=fy_requested,
            requested_utilization=0.0 if zero_request else None,
            applied_utilization=0.0,
            saturation_scale=1.0 if zero_request else 0.0,
            saturated=not zero_request,
        )

    if not all(
        math.isfinite(limit) and limit > 0.0 for limit in (fx_limit, fy_limit)
    ):
        raise TyreNumericalError(
            "positive inputs produced a non-finite or zero force-capacity axis"
        )

    normalized_fx = fx_requested / fx_limit
    normalized_fy = fy_requested / fy_limit
    requested_utilization = math.hypot(normalized_fx, normalized_fy)
    if not math.isfinite(requested_utilization):
        raise TyreNumericalError(
            "normalized requested utilization is non-finite for finite inputs"
        )

    if requested_utilization <= 1.0 + parameters.boundary_tolerance:
        scale = 1.0
        saturated = False
        status = "within_limit"
        reason = "requested force is within the friction ellipse"
    else:
        scale = 1.0 / requested_utilization
        saturated = True
        status = "saturated"
        reason = "requested force was radially projected onto the friction ellipse"

    fx_applied = fx_requested * scale
    fy_applied = fy_requested * scale
    applied_utilization = math.hypot(fx_applied / fx_limit, fy_applied / fy_limit)
    values = (scale, fx_applied, fy_applied, applied_utilization)
    if not all(math.isfinite(value) for value in values):
        raise TyreNumericalError("tyre force resolution produced a non-finite state")

    return TyreForceResult(
        status=status,
        reason=reason,
        normal_load_n=normal_load_n,
        longitudinal_limit_n=fx_limit,
        lateral_limit_n=fy_limit,
        requested_longitudinal_force_n=fx_requested,
        requested_lateral_force_n=fy_requested,
        applied_longitudinal_force_n=fx_applied,
        applied_lateral_force_n=fy_applied,
        residual_longitudinal_force_n=fx_requested - fx_applied,
        residual_lateral_force_n=fy_requested - fy_applied,
        requested_utilization=requested_utilization,
        applied_utilization=applied_utilization,
        saturation_scale=scale,
        saturated=saturated,
    )
