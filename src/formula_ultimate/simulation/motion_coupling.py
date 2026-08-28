"""Work 026 planar force, yaw, corridor, and race-progress integration."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
import math

from .aero_load_coupling import AerodynamicChassisWrench
from .contact_coupling import ContactForceMoment
from .coupling import ResidualEntry, SharedVehicleState
from .step_inputs import SpatialStepEvidence
from .transaction import AdapterOutput, AdapterReadView, RuntimeSignal


MOTION_ADAPTER_VERSION = "work026-coupled-motion-v1"


class MotionCouplingError(ValueError):
    """Raised when Work 026 motion inputs violate the declared contract."""


def _finite(name: str, value: float) -> None:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
    ):
        raise MotionCouplingError(f"{name} must be finite")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise MotionCouplingError(f"{name} must be positive")


def _vector3(name: str, value: tuple[float, float, float]) -> None:
    if not isinstance(value, tuple) or len(value) != 3:
        raise MotionCouplingError(f"{name} must be a three-value tuple")
    for item in value:
        _finite(name, item)


@dataclass(frozen=True, slots=True)
class MotionConfiguration:
    mass_kg: float
    yaw_inertia_kg_m2: float
    duration_s: float
    vehicle_width_m: float

    def __post_init__(self) -> None:
        for name in (
            "mass_kg",
            "yaw_inertia_kg_m2",
            "duration_s",
            "vehicle_width_m",
        ):
            _positive(name, getattr(self, name))


@dataclass(frozen=True, slots=True)
class MotionCorridorReference:
    """Local ENU centreline reference at the start state's race distance."""

    circuit_id: str
    segment_id: str
    race_distance_m: float
    centreline_position_m: tuple[float, float, float]
    centreline_heading_rad: float

    def __post_init__(self) -> None:
        if not self.circuit_id.strip() or not self.segment_id.strip():
            raise MotionCouplingError("corridor reference IDs must not be blank")
        _finite("race_distance_m", self.race_distance_m)
        if self.race_distance_m < 0.0:
            raise MotionCouplingError("race_distance_m must be non-negative")
        _vector3("centreline_position_m", self.centreline_position_m)
        _finite("centreline_heading_rad", self.centreline_heading_rad)


@dataclass(frozen=True, slots=True)
class MotionCorridorEvidence:
    circuit_id: str
    segment_id: str
    status: str
    start_lateral_offset_m: float
    candidate_lateral_offset_m: float
    left_clearance_m: float
    right_clearance_m: float
    minimum_clearance_m: float
    raw_tangent_progress_m: float
    credited_race_progress_m: float
    reverse_progress_m: float
    reference_heading_end_rad: float
    reason: str

    def __post_init__(self) -> None:
        if self.status not in {"inside", "departed", "invalid"}:
            raise MotionCouplingError("unsupported corridor evidence status")
        for name in (
            "start_lateral_offset_m",
            "candidate_lateral_offset_m",
            "left_clearance_m",
            "right_clearance_m",
            "minimum_clearance_m",
            "raw_tangent_progress_m",
            "credited_race_progress_m",
            "reverse_progress_m",
            "reference_heading_end_rad",
        ):
            _finite(name, getattr(self, name))
        if self.credited_race_progress_m < 0.0 or self.reverse_progress_m < 0.0:
            raise MotionCouplingError("race-progress evidence must be non-negative")


@dataclass(frozen=True, slots=True)
class MotionIntegrationEvidence:
    method: str
    duration_s: float
    total_body_longitudinal_force_n: float
    total_body_lateral_force_n: float
    total_yaw_moment_n_m: float
    midpoint_yaw_rad: float
    global_acceleration_mps2: tuple[float, float, float]
    corridor: MotionCorridorEvidence
    residuals: tuple[ResidualEntry, ...]


@dataclass(frozen=True, slots=True)
class MotionStepResult:
    status: str
    reason: str
    candidate_state: SharedVehicleState | None
    evidence: MotionIntegrationEvidence | None
    residuals: tuple[ResidualEntry, ...]

    def __post_init__(self) -> None:
        if self.status not in {"ok", "invalid"}:
            raise MotionCouplingError("unsupported motion result status")
        if self.status == "ok" and (
            self.candidate_state is None or self.evidence is None
        ):
            raise MotionCouplingError("successful motion result must be complete")


def _advance_centreline(
    reference: MotionCorridorReference,
    spatial: SpatialStepEvidence,
    progress_m: float,
) -> tuple[tuple[float, float, float], float]:
    heading = reference.centreline_heading_rad
    curvature = spatial.curvature_1pm
    if abs(curvature) < 1.0e-14:
        dx = progress_m * math.cos(heading)
        dy = progress_m * math.sin(heading)
        end_heading = heading
    else:
        end_heading = heading + curvature * progress_m
        dx = (math.sin(end_heading) - math.sin(heading)) / curvature
        dy = (-math.cos(end_heading) + math.cos(heading)) / curvature
    x, y, z = reference.centreline_position_m
    return (
        (x + dx, y + dy, z + progress_m * math.tan(spatial.grade_rad)),
        end_heading,
    )


def _lateral_offset(
    position_m: tuple[float, float, float],
    centreline_position_m: tuple[float, float, float],
    heading_rad: float,
) -> float:
    dx = position_m[0] - centreline_position_m[0]
    dy = position_m[1] - centreline_position_m[1]
    return -math.sin(heading_rad) * dx + math.cos(heading_rad) * dy


def _tangent_progress(
    displacement_m: tuple[float, float], heading_rad: float, curvature_1pm: float
) -> float:
    progress = (
        displacement_m[0] * math.cos(heading_rad)
        + displacement_m[1] * math.sin(heading_rad)
    )
    for _ in range(6):
        midpoint_heading = heading_rad + 0.5 * curvature_1pm * progress
        progress = (
            displacement_m[0] * math.cos(midpoint_heading)
            + displacement_m[1] * math.sin(midpoint_heading)
        )
    return progress


def integrate_coupled_motion(
    *,
    config: MotionConfiguration,
    reference: MotionCorridorReference,
    spatial: SpatialStepEvidence,
    aerodynamic_wrench: AerodynamicChassisWrench,
    contact_wrench: ContactForceMoment,
    state: SharedVehicleState,
) -> MotionStepResult:
    """Integrate one planar step with a midpoint force orientation."""

    if state.status != "running":
        raise MotionCouplingError("motion requires a running shared state")
    if spatial.status != "available":
        raise MotionCouplingError("available spatial evidence is required")
    if spatial.circuit_id != reference.circuit_id or spatial.segment_id != reference.segment_id:
        raise MotionCouplingError("spatial and corridor reference IDs differ")
    if not math.isclose(
        state.race_distance_m,
        reference.race_distance_m,
        rel_tol=0.0,
        abs_tol=1.0e-9,
    ):
        raise MotionCouplingError("corridor reference race distance differs from state")
    if not contact_wrench.contacts:
        raise MotionCouplingError("contact wrench must contain contacts")

    contact_fx_sum = math.fsum(
        item.applied_body_longitudinal_force_n for item in contact_wrench.contacts
    )
    contact_fy_sum = math.fsum(
        item.applied_body_lateral_force_n for item in contact_wrench.contacts
    )
    contact_mz_sum = math.fsum(
        item.applied_yaw_moment_n_m for item in contact_wrench.contacts
    )
    input_residuals = (
        ResidualEntry(
            "motion.input-contact-force-x",
            "force",
            contact_wrench.total_body_longitudinal_force_n - contact_fx_sum,
            "N",
            1.0e-9,
            1.0e-12,
            max(1.0, abs(contact_fx_sum)),
        ),
        ResidualEntry(
            "motion.input-contact-force-y",
            "force",
            contact_wrench.total_body_lateral_force_n - contact_fy_sum,
            "N",
            1.0e-9,
            1.0e-12,
            max(1.0, abs(contact_fy_sum)),
        ),
        ResidualEntry(
            "motion.input-contact-moment-z",
            "moment",
            contact_wrench.total_yaw_moment_n_m - contact_mz_sum,
            "N*m",
            1.0e-9,
            1.0e-12,
            max(1.0, abs(contact_mz_sum)),
        ),
    )
    if any(not item.passed for item in input_residuals):
        return MotionStepResult(
            "invalid", "contact wrench totals are inconsistent", None, None, input_residuals
        )

    aero_fx, aero_fy, _aero_fz = aerodynamic_wrench.force_body_n
    total_fx = aero_fx + contact_wrench.total_body_longitudinal_force_n
    total_fy = aero_fy + contact_wrench.total_body_lateral_force_n
    total_mz = (
        aerodynamic_wrench.moment_about_com_n_m[2]
        + contact_wrench.total_yaw_moment_n_m
    )
    dt = config.duration_s
    angular_acceleration = total_mz / config.yaw_inertia_kg_m2
    midpoint_yaw = (
        state.yaw_rad
        + 0.5 * state.yaw_rate_rad_per_s * dt
        + 0.125 * angular_acceleration * dt * dt
    )
    cosine = math.cos(midpoint_yaw)
    sine = math.sin(midpoint_yaw)
    ax = (cosine * total_fx - sine * total_fy) / config.mass_kg
    ay = (sine * total_fx + cosine * total_fy) / config.mass_kg
    vx0, vy0, vz0 = state.velocity_mps
    vx1 = vx0 + ax * dt
    vy1 = vy0 + ay * dt
    x0, y0, z0 = state.position_m
    x1 = x0 + 0.5 * (vx0 + vx1) * dt
    y1 = y0 + 0.5 * (vy0 + vy1) * dt
    yaw_rate_1 = state.yaw_rate_rad_per_s + angular_acceleration * dt
    yaw_1 = (
        state.yaw_rad
        + state.yaw_rate_rad_per_s * dt
        + 0.5 * angular_acceleration * dt * dt
    )

    displacement = (x1 - x0, y1 - y0)
    raw_progress = _tangent_progress(
        displacement, reference.centreline_heading_rad, spatial.curvature_1pm
    )
    credited_progress = max(0.0, raw_progress)
    reverse_progress = max(0.0, -raw_progress)
    centreline_end, reference_heading_end = _advance_centreline(
        reference, spatial, credited_progress
    )
    z1 = z0 + vz0 * dt
    candidate_position = (x1, y1, z1)
    start_offset = _lateral_offset(
        state.position_m,
        reference.centreline_position_m,
        reference.centreline_heading_rad,
    )
    candidate_offset = _lateral_offset(
        candidate_position, centreline_end, reference_heading_end
    )
    effective_left = spatial.width_left_m - spatial.horizontal_uncertainty_m
    effective_right = spatial.width_right_m - spatial.horizontal_uncertainty_m
    half_width = 0.5 * config.vehicle_width_m
    left_clearance = effective_left - half_width - candidate_offset
    right_clearance = effective_right - half_width + candidate_offset
    minimum_clearance = min(left_clearance, right_clearance)
    start_left = effective_left - half_width - start_offset
    start_right = effective_right - half_width + start_offset
    if min(start_left, start_right) < 0.0:
        corridor_status = "invalid"
        corridor_reason = "start state is outside the effective corridor"
    elif minimum_clearance < 0.0:
        corridor_status = "departed"
        corridor_reason = "candidate vehicle envelope crosses the effective corridor"
    else:
        corridor_status = "inside"
        corridor_reason = (
            "candidate vehicle envelope remains inside the effective corridor"
        )
    corridor = MotionCorridorEvidence(
        spatial.circuit_id,
        spatial.segment_id,
        corridor_status,
        start_offset,
        candidate_offset,
        left_clearance,
        right_clearance,
        minimum_clearance,
        raw_progress,
        credited_progress,
        reverse_progress,
        reference_heading_end,
        corridor_reason,
    )

    candidate = replace(
        state,
        time_s=state.time_s + dt,
        race_distance_m=state.race_distance_m + credited_progress,
        position_m=candidate_position,
        velocity_mps=(vx1, vy1, vz0),
        yaw_rad=yaw_1,
        yaw_rate_rad_per_s=yaw_rate_1,
    )
    dvx = vx1 - vx0
    dvy = vy1 - vy0
    residuals = input_residuals + (
        ResidualEntry(
            "motion.linear-force-x",
            "force",
            config.mass_kg * (cosine * dvx + sine * dvy) / dt - total_fx,
            "N",
            1.0e-8,
            1.0e-11,
            max(1.0, abs(total_fx)),
        ),
        ResidualEntry(
            "motion.linear-force-y",
            "force",
            config.mass_kg * (-sine * dvx + cosine * dvy) / dt - total_fy,
            "N",
            1.0e-8,
            1.0e-11,
            max(1.0, abs(total_fy)),
        ),
        ResidualEntry(
            "motion.yaw-moment",
            "moment",
            config.yaw_inertia_kg_m2
            * (yaw_rate_1 - state.yaw_rate_rad_per_s)
            / dt
            - total_mz,
            "N*m",
            1.0e-8,
            1.0e-11,
            max(1.0, abs(total_mz)),
        ),
        ResidualEntry(
            "motion.kinematic-x",
            "distance",
            x1 - x0 - 0.5 * (vx0 + vx1) * dt,
            "m",
            1.0e-12,
            1.0e-12,
            max(1.0, abs(x1 - x0)),
        ),
        ResidualEntry(
            "motion.kinematic-y",
            "distance",
            y1 - y0 - 0.5 * (vy0 + vy1) * dt,
            "m",
            1.0e-12,
            1.0e-12,
            max(1.0, abs(y1 - y0)),
        ),
        ResidualEntry(
            "motion.kinematic-z",
            "distance",
            z1 - z0 - vz0 * dt,
            "m",
            1.0e-12,
            1.0e-12,
            max(1.0, abs(z1 - z0)),
        ),
    )
    evidence = MotionIntegrationEvidence(
        "midpoint-force/trapezoidal-position",
        dt,
        total_fx,
        total_fy,
        total_mz,
        midpoint_yaw,
        (ax, ay, 0.0),
        corridor,
        residuals,
    )
    if any(not item.passed for item in residuals):
        return MotionStepResult(
            "invalid", "motion residual exceeded tolerance", candidate, evidence, residuals
        )
    if corridor.status != "inside":
        return MotionStepResult("invalid", corridor.reason, candidate, evidence, residuals)
    return MotionStepResult(
        "ok", "motion and corridor gates passed", candidate, evidence, residuals
    )


@dataclass(frozen=True, slots=True)
class VehicleMotionCouplingAdapter:
    config: MotionConfiguration
    corridor_reference: MotionCorridorReference
    module_id: str = field(default="vehicle_motion_solver", init=False)
    model_version: str = field(default=MOTION_ADAPTER_VERSION, init=False)

    def execute(self, view: AdapterReadView) -> AdapterOutput:
        aero = view.read("aero.force_moment")
        spatial = view.read("circuit.segment_inputs")
        contact = view.read("contact.force_moment")
        state = view.read("state.current")
        if (
            not isinstance(aero, AerodynamicChassisWrench)
            or not isinstance(spatial, SpatialStepEvidence)
            or not isinstance(contact, ContactForceMoment)
            or not isinstance(state, SharedVehicleState)
        ):
            return AdapterOutput(
                self.module_id,
                "invalid",
                (),
                reason="motion adapter payload types are invalid",
            )
        try:
            result = integrate_coupled_motion(
                config=self.config,
                reference=self.corridor_reference,
                spatial=spatial,
                aerodynamic_wrench=aero,
                contact_wrench=contact,
                state=state,
            )
        except (ArithmeticError, ValueError) as exc:
            return AdapterOutput(self.module_id, "invalid", (), reason=str(exc))
        if result.status != "ok":
            return AdapterOutput(
                self.module_id,
                "invalid",
                (),
                residuals=result.residuals,
                reason=result.reason,
            )
        return AdapterOutput(
            self.module_id,
            "ok",
            (
                RuntimeSignal("motion.residuals", result.evidence),
                RuntimeSignal("state.motion_candidate", result.candidate_state),
            ),
            residuals=result.residuals,
        )
