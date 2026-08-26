"""Deterministic Level-0 planar lateral/yaw and load-transfer physics.

The model accepts an arbitrary ground-contact topology.  It is a reduced-order
selection gate, not a calibrated suspension, tyre, or vehicle validation model.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from .tyre import (
    TyreContactParameters,
    TyreForceRequest,
    TyreForceResult,
    TyreInputError,
    TyreNumericalError,
    resolve_tyre_force,
)


MODEL_VERSION = "work016-planar-v1"


class LateralInputError(ValueError):
    """Raised when a declared planar-model input violates its contract."""


def _finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise LateralInputError(f"{name} must be finite; received {value!r}")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise LateralInputError(f"{name} must be > 0; received {value!r}")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0.0:
        raise LateralInputError(f"{name} must be >= 0; received {value!r}")


def _within(value: float, *, absolute: float, relative: float, scale: float) -> bool:
    return abs(value) <= absolute + relative * max(1.0, abs(scale))


@dataclass(frozen=True, slots=True)
class PlanarContact:
    """One independently located and steered ground contact."""

    contact_id: str
    x_position_m: float
    y_position_m: float
    baseline_normal_load_n: float
    steer_angle_rad: float
    cornering_stiffness_n_per_rad: float
    requested_longitudinal_force_n: float
    tyre_parameters: TyreContactParameters

    def __post_init__(self) -> None:
        if not self.contact_id or not self.contact_id.strip():
            raise LateralInputError("contact_id must be non-empty")
        _finite("x_position_m", self.x_position_m)
        _finite("y_position_m", self.y_position_m)
        _positive("baseline_normal_load_n", self.baseline_normal_load_n)
        _finite("steer_angle_rad", self.steer_angle_rad)
        _nonnegative(
            "cornering_stiffness_n_per_rad",
            self.cornering_stiffness_n_per_rad,
        )
        _finite(
            "requested_longitudinal_force_n",
            self.requested_longitudinal_force_n,
        )
        if not isinstance(self.tyre_parameters, TyreContactParameters):
            raise LateralInputError(
                "tyre_parameters must be a TyreContactParameters instance"
            )


@dataclass(frozen=True, slots=True)
class PlanarVehicleParameters:
    mass_kg: float
    yaw_inertia_kg_m2: float
    centre_of_mass_height_m: float
    gravity_m_per_s2: float = 9.81

    def __post_init__(self) -> None:
        _positive("mass_kg", self.mass_kg)
        _positive("yaw_inertia_kg_m2", self.yaw_inertia_kg_m2)
        _nonnegative("centre_of_mass_height_m", self.centre_of_mass_height_m)
        _positive("gravity_m_per_s2", self.gravity_m_per_s2)


@dataclass(frozen=True, slots=True)
class PlanarVehicle:
    vehicle_id: str
    parameters: PlanarVehicleParameters
    contacts: tuple[PlanarContact, ...]

    def __post_init__(self) -> None:
        if not self.vehicle_id or not self.vehicle_id.strip():
            raise LateralInputError("vehicle_id must be non-empty")
        if not isinstance(self.parameters, PlanarVehicleParameters):
            raise LateralInputError(
                "parameters must be a PlanarVehicleParameters instance"
            )
        contacts = tuple(self.contacts)
        object.__setattr__(self, "contacts", contacts)
        if not contacts:
            raise LateralInputError("at least one contact must be declared")
        if not all(isinstance(contact, PlanarContact) for contact in contacts):
            raise LateralInputError("contacts must contain only PlanarContact values")
        identifiers = [contact.contact_id for contact in contacts]
        if len(set(identifiers)) != len(identifiers):
            raise LateralInputError("contact_id values must be unique")

        weight = self.parameters.mass_kg * self.parameters.gravity_m_per_s2
        vertical = math.fsum(c.baseline_normal_load_n for c in contacts)
        pitch = math.fsum(
            c.x_position_m * c.baseline_normal_load_n for c in contacts
        )
        roll = math.fsum(
            c.y_position_m * c.baseline_normal_load_n for c in contacts
        )
        length_scale = max(
            1.0,
            *(abs(c.x_position_m) for c in contacts),
            *(abs(c.y_position_m) for c in contacts),
        )
        if not math.isclose(vertical, weight, rel_tol=1.0e-9, abs_tol=1.0e-9):
            raise LateralInputError(
                "baseline normal loads must sum to vehicle weight; "
                f"residual={vertical - weight!r} N"
            )
        moment_tolerance = 1.0e-9 * max(1.0, weight * length_scale)
        if abs(pitch) > moment_tolerance or abs(roll) > moment_tolerance:
            raise LateralInputError(
                "baseline normal loads must have zero pitch and roll moment; "
                f"pitch_residual={pitch!r} N*m, roll_residual={roll!r} N*m"
            )


@dataclass(frozen=True, slots=True)
class PlanarState:
    time_s: float
    x_position_m: float
    y_position_m: float
    heading_rad: float
    longitudinal_velocity_m_per_s: float
    lateral_velocity_m_per_s: float
    yaw_rate_rad_per_s: float

    def __post_init__(self) -> None:
        _nonnegative("time_s", self.time_s)
        for name in (
            "x_position_m",
            "y_position_m",
            "heading_rad",
            "longitudinal_velocity_m_per_s",
            "lateral_velocity_m_per_s",
            "yaw_rate_rad_per_s",
        ):
            _finite(name, getattr(self, name))


@dataclass(frozen=True, slots=True)
class PlanarSolverControl:
    time_step_s: float
    max_load_iterations: int = 64
    acceleration_absolute_tolerance_m_per_s2: float = 1.0e-10
    acceleration_relative_tolerance: float = 1.0e-10
    relaxation_factor: float = 0.5
    speed_regularization_m_per_s: float = 0.1
    load_force_absolute_tolerance_n: float = 1.0e-6
    load_moment_absolute_tolerance_n_m: float = 1.0e-5
    balance_relative_tolerance: float = 1.0e-10

    def __post_init__(self) -> None:
        _positive("time_step_s", self.time_step_s)
        if (
            isinstance(self.max_load_iterations, bool)
            or not isinstance(self.max_load_iterations, int)
            or self.max_load_iterations < 1
            or self.max_load_iterations > 10_000
        ):
            raise LateralInputError(
                "max_load_iterations must be an integer in [1, 10000]"
            )
        _positive(
            "acceleration_absolute_tolerance_m_per_s2",
            self.acceleration_absolute_tolerance_m_per_s2,
        )
        _nonnegative(
            "acceleration_relative_tolerance",
            self.acceleration_relative_tolerance,
        )
        _positive("relaxation_factor", self.relaxation_factor)
        if self.relaxation_factor > 1.0:
            raise LateralInputError("relaxation_factor must be <= 1")
        _positive("speed_regularization_m_per_s", self.speed_regularization_m_per_s)
        _nonnegative(
            "load_force_absolute_tolerance_n",
            self.load_force_absolute_tolerance_n,
        )
        _nonnegative(
            "load_moment_absolute_tolerance_n_m",
            self.load_moment_absolute_tolerance_n_m,
        )
        _nonnegative("balance_relative_tolerance", self.balance_relative_tolerance)


@dataclass(frozen=True, slots=True)
class NormalLoadResiduals:
    vertical_force_n: float
    pitch_moment_n_m: float
    roll_moment_n_m: float


@dataclass(frozen=True, slots=True)
class NormalLoadSolution:
    status: str
    reason: str
    normal_loads_n: tuple[float, ...]
    residuals: NormalLoadResiduals | None


@dataclass(frozen=True, slots=True)
class PlanarContactResult:
    contact_id: str
    normal_load_n: float
    local_longitudinal_velocity_m_per_s: float
    local_lateral_velocity_m_per_s: float
    slip_angle_rad: float
    tyre_force: TyreForceResult
    applied_body_longitudinal_force_n: float
    applied_body_lateral_force_n: float
    applied_yaw_moment_n_m: float


@dataclass(frozen=True, slots=True)
class PlanarBalanceResiduals:
    vertical_force_n: float
    pitch_moment_n_m: float
    roll_moment_n_m: float
    longitudinal_force_n: float
    lateral_force_n: float
    yaw_moment_n_m: float


@dataclass(frozen=True, slots=True)
class PlanarStepResult:
    model_version: str
    status: str
    reason: str
    start_state: PlanarState
    end_state: PlanarState
    contact_results: tuple[PlanarContactResult, ...]
    normal_loads_n: tuple[float, ...]
    load_iterations: int
    converged: bool
    longitudinal_acceleration_m_per_s2: float | None
    lateral_acceleration_m_per_s2: float | None
    yaw_acceleration_rad_per_s2: float | None
    total_body_longitudinal_force_n: float | None
    total_body_lateral_force_n: float | None
    total_yaw_moment_n_m: float | None
    saturated_contact_count: int
    residuals: PlanarBalanceResiduals | None


def _solve_three_by_three(
    matrix: tuple[tuple[float, float, float], ...],
    vector: tuple[float, float, float],
) -> tuple[float, float, float] | None:
    augmented = [list(row) + [value] for row, value in zip(matrix, vector)]
    matrix_scale = max(abs(value) for row in matrix for value in row)
    singular_tolerance = 1.0e-12 * max(1.0, matrix_scale)
    for column in range(3):
        pivot = max(range(column, 3), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) <= singular_tolerance:
            return None
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        for index in range(column, 4):
            augmented[column][index] /= pivot_value
        for row in range(3):
            if row == column:
                continue
            factor = augmented[row][column]
            for index in range(column, 4):
                augmented[row][index] -= factor * augmented[column][index]
    result = tuple(augmented[row][3] for row in range(3))
    if not all(math.isfinite(value) for value in result):
        return None
    return result  # type: ignore[return-value]


def _normal_load_residuals(
    vehicle: PlanarVehicle,
    normal_loads_n: tuple[float, ...],
    longitudinal_acceleration_m_per_s2: float,
    lateral_acceleration_m_per_s2: float,
) -> NormalLoadResiduals:
    params = vehicle.parameters
    vertical = math.fsum(normal_loads_n) - params.mass_kg * params.gravity_m_per_s2
    pitch = math.fsum(
        contact.x_position_m * load
        for contact, load in zip(vehicle.contacts, normal_loads_n)
    ) + params.mass_kg * longitudinal_acceleration_m_per_s2 * params.centre_of_mass_height_m
    roll = math.fsum(
        contact.y_position_m * load
        for contact, load in zip(vehicle.contacts, normal_loads_n)
    ) + params.mass_kg * lateral_acceleration_m_per_s2 * params.centre_of_mass_height_m
    return NormalLoadResiduals(vertical, pitch, roll)


def solve_quasi_static_normal_loads(
    *,
    vehicle: PlanarVehicle,
    longitudinal_acceleration_m_per_s2: float,
    lateral_acceleration_m_per_s2: float,
) -> NormalLoadSolution:
    """Project baseline loads onto vertical, pitch, and roll equilibrium."""

    _finite(
        "longitudinal_acceleration_m_per_s2",
        longitudinal_acceleration_m_per_s2,
    )
    _finite("lateral_acceleration_m_per_s2", lateral_acceleration_m_per_s2)
    contacts = vehicle.contacts
    params = vehicle.parameters
    count = float(len(contacts))
    sum_x = math.fsum(contact.x_position_m for contact in contacts)
    sum_y = math.fsum(contact.y_position_m for contact in contacts)
    sum_xx = math.fsum(contact.x_position_m**2 for contact in contacts)
    sum_xy = math.fsum(
        contact.x_position_m * contact.y_position_m for contact in contacts
    )
    sum_yy = math.fsum(contact.y_position_m**2 for contact in contacts)
    gram = (
        (count, sum_x, sum_y),
        (sum_x, sum_xx, sum_xy),
        (sum_y, sum_xy, sum_yy),
    )
    baseline = tuple(contact.baseline_normal_load_n for contact in contacts)
    target = (
        params.mass_kg * params.gravity_m_per_s2,
        -params.mass_kg
        * longitudinal_acceleration_m_per_s2
        * params.centre_of_mass_height_m,
        -params.mass_kg
        * lateral_acceleration_m_per_s2
        * params.centre_of_mass_height_m,
    )
    baseline_projection = (
        math.fsum(baseline),
        math.fsum(
            contact.x_position_m * load
            for contact, load in zip(contacts, baseline)
        ),
        math.fsum(
            contact.y_position_m * load
            for contact, load in zip(contacts, baseline)
        ),
    )
    correction = _solve_three_by_three(
        gram,
        tuple(wanted - current for wanted, current in zip(target, baseline_projection)),
    )
    if correction is None:
        return NormalLoadSolution(
            status="invalid",
            reason="contact geometry is rank-deficient for vertical/pitch/roll balance",
            normal_loads_n=(),
            residuals=None,
        )
    normal_loads = tuple(
        load
        + correction[0]
        + correction[1] * contact.x_position_m
        + correction[2] * contact.y_position_m
        for contact, load in zip(contacts, baseline)
    )
    if not all(math.isfinite(load) for load in normal_loads):
        return NormalLoadSolution(
            status="invalid",
            reason="normal-load projection produced a non-finite load",
            normal_loads_n=normal_loads,
            residuals=None,
        )
    residuals = _normal_load_residuals(
        vehicle,
        normal_loads,
        longitudinal_acceleration_m_per_s2,
        lateral_acceleration_m_per_s2,
    )
    lifted = [
        contact.contact_id
        for contact, load in zip(contacts, normal_loads)
        if load < 0.0
    ]
    if lifted:
        return NormalLoadSolution(
            status="invalid",
            reason="contact lift produced negative normal load at " + ", ".join(lifted),
            normal_loads_n=normal_loads,
            residuals=residuals,
        )
    return NormalLoadSolution(
        status="ok",
        reason="normal loads satisfy the declared minimum-change equilibrium",
        normal_loads_n=normal_loads,
        residuals=residuals,
    )


def _resolve_contacts(
    *,
    vehicle: PlanarVehicle,
    state: PlanarState,
    normal_loads_n: tuple[float, ...],
    speed_regularization_m_per_s: float,
) -> tuple[PlanarContactResult, ...]:
    results: list[PlanarContactResult] = []
    for contact, normal_load in zip(vehicle.contacts, normal_loads_n):
        body_vx = (
            state.longitudinal_velocity_m_per_s
            - state.yaw_rate_rad_per_s * contact.y_position_m
        )
        body_vy = (
            state.lateral_velocity_m_per_s
            + state.yaw_rate_rad_per_s * contact.x_position_m
        )
        cosine = math.cos(contact.steer_angle_rad)
        sine = math.sin(contact.steer_angle_rad)
        local_vx = cosine * body_vx + sine * body_vy
        local_vy = -sine * body_vx + cosine * body_vy
        slip_angle = math.atan2(
            local_vy,
            max(abs(local_vx), speed_regularization_m_per_s),
        )
        requested_lateral = -contact.cornering_stiffness_n_per_rad * slip_angle
        tyre_force = resolve_tyre_force(
            parameters=contact.tyre_parameters,
            normal_load_n=normal_load,
            request=TyreForceRequest(
                contact.requested_longitudinal_force_n,
                requested_lateral,
            ),
        )
        body_fx = (
            cosine * tyre_force.applied_longitudinal_force_n
            - sine * tyre_force.applied_lateral_force_n
        )
        body_fy = (
            sine * tyre_force.applied_longitudinal_force_n
            + cosine * tyre_force.applied_lateral_force_n
        )
        yaw_moment = contact.x_position_m * body_fy - contact.y_position_m * body_fx
        values = (local_vx, local_vy, slip_angle, body_fx, body_fy, yaw_moment)
        if not all(math.isfinite(value) for value in values):
            raise TyreNumericalError(
                f"contact {contact.contact_id!r} produced non-finite kinematics"
            )
        results.append(
            PlanarContactResult(
                contact_id=contact.contact_id,
                normal_load_n=normal_load,
                local_longitudinal_velocity_m_per_s=local_vx,
                local_lateral_velocity_m_per_s=local_vy,
                slip_angle_rad=slip_angle,
                tyre_force=tyre_force,
                applied_body_longitudinal_force_n=body_fx,
                applied_body_lateral_force_n=body_fy,
                applied_yaw_moment_n_m=yaw_moment,
            )
        )
    return tuple(results)


def _invalid_step(
    *,
    state: PlanarState,
    reason: str,
    normal_loads_n: tuple[float, ...] = (),
    contact_results: tuple[PlanarContactResult, ...] = (),
    iterations: int = 0,
) -> PlanarStepResult:
    return PlanarStepResult(
        model_version=MODEL_VERSION,
        status="invalid",
        reason=reason,
        start_state=state,
        end_state=state,
        contact_results=contact_results,
        normal_loads_n=normal_loads_n,
        load_iterations=iterations,
        converged=False,
        longitudinal_acceleration_m_per_s2=None,
        lateral_acceleration_m_per_s2=None,
        yaw_acceleration_rad_per_s2=None,
        total_body_longitudinal_force_n=None,
        total_body_lateral_force_n=None,
        total_yaw_moment_n_m=None,
        saturated_contact_count=sum(
            result.tyre_force.saturated for result in contact_results
        ),
        residuals=None,
    )


def step_planar_dynamics(
    *,
    vehicle: PlanarVehicle,
    state: PlanarState,
    control: PlanarSolverControl,
) -> PlanarStepResult:
    """Advance one deterministic explicit planar-dynamics step."""

    guess_ax = 0.0
    guess_ay = 0.0
    contact_results: tuple[PlanarContactResult, ...] = ()
    normal_loads: tuple[float, ...] = ()
    total_fx = total_fy = total_mz = new_ax = new_ay = 0.0
    for iteration in range(1, control.max_load_iterations + 1):
        load_solution = solve_quasi_static_normal_loads(
            vehicle=vehicle,
            longitudinal_acceleration_m_per_s2=guess_ax,
            lateral_acceleration_m_per_s2=guess_ay,
        )
        normal_loads = load_solution.normal_loads_n
        if load_solution.status != "ok":
            return _invalid_step(
                state=state,
                reason=load_solution.reason,
                normal_loads_n=normal_loads,
                iterations=iteration,
            )
        try:
            contact_results = _resolve_contacts(
                vehicle=vehicle,
                state=state,
                normal_loads_n=normal_loads,
                speed_regularization_m_per_s=control.speed_regularization_m_per_s,
            )
        except (TyreInputError, TyreNumericalError, OverflowError, ValueError) as exc:
            return _invalid_step(
                state=state,
                reason=f"contact-force resolution failed: {exc}",
                normal_loads_n=normal_loads,
                iterations=iteration,
            )
        total_fx = math.fsum(
            result.applied_body_longitudinal_force_n for result in contact_results
        )
        total_fy = math.fsum(
            result.applied_body_lateral_force_n for result in contact_results
        )
        total_mz = math.fsum(
            result.applied_yaw_moment_n_m for result in contact_results
        )
        new_ax = total_fx / vehicle.parameters.mass_kg
        new_ay = total_fy / vehicle.parameters.mass_kg
        if not all(math.isfinite(value) for value in (new_ax, new_ay, total_mz)):
            return _invalid_step(
                state=state,
                reason="force summation produced a non-finite acceleration",
                normal_loads_n=normal_loads,
                contact_results=contact_results,
                iterations=iteration,
            )
        tolerance_x = (
            control.acceleration_absolute_tolerance_m_per_s2
            + control.acceleration_relative_tolerance
            * max(abs(guess_ax), abs(new_ax))
        )
        tolerance_y = (
            control.acceleration_absolute_tolerance_m_per_s2
            + control.acceleration_relative_tolerance
            * max(abs(guess_ay), abs(new_ay))
        )
        if abs(new_ax - guess_ax) <= tolerance_x and abs(new_ay - guess_ay) <= tolerance_y:
            break
        guess_ax += control.relaxation_factor * (new_ax - guess_ax)
        guess_ay += control.relaxation_factor * (new_ay - guess_ay)
    else:
        return _invalid_step(
            state=state,
            reason="load-transfer fixed-point solver did not converge",
            normal_loads_n=normal_loads,
            contact_results=contact_results,
            iterations=control.max_load_iterations,
        )

    yaw_acceleration = total_mz / vehicle.parameters.yaw_inertia_kg_m2
    load_residuals = _normal_load_residuals(vehicle, normal_loads, new_ax, new_ay)
    longitudinal_residual = vehicle.parameters.mass_kg * new_ax - total_fx
    lateral_residual = vehicle.parameters.mass_kg * new_ay - total_fy
    yaw_residual = vehicle.parameters.yaw_inertia_kg_m2 * yaw_acceleration - total_mz
    residuals = PlanarBalanceResiduals(
        vertical_force_n=load_residuals.vertical_force_n,
        pitch_moment_n_m=load_residuals.pitch_moment_n_m,
        roll_moment_n_m=load_residuals.roll_moment_n_m,
        longitudinal_force_n=longitudinal_residual,
        lateral_force_n=lateral_residual,
        yaw_moment_n_m=yaw_residual,
    )
    weight = vehicle.parameters.mass_kg * vehicle.parameters.gravity_m_per_s2
    length_scale = max(
        1.0,
        *(abs(contact.x_position_m) for contact in vehicle.contacts),
        *(abs(contact.y_position_m) for contact in vehicle.contacts),
    )
    checks = (
        _within(
            residuals.vertical_force_n,
            absolute=control.load_force_absolute_tolerance_n,
            relative=control.balance_relative_tolerance,
            scale=weight,
        ),
        _within(
            residuals.pitch_moment_n_m,
            absolute=control.load_moment_absolute_tolerance_n_m,
            relative=control.balance_relative_tolerance,
            scale=weight * length_scale,
        ),
        _within(
            residuals.roll_moment_n_m,
            absolute=control.load_moment_absolute_tolerance_n_m,
            relative=control.balance_relative_tolerance,
            scale=weight * length_scale,
        ),
        _within(
            residuals.longitudinal_force_n,
            absolute=control.load_force_absolute_tolerance_n,
            relative=control.balance_relative_tolerance,
            scale=total_fx,
        ),
        _within(
            residuals.lateral_force_n,
            absolute=control.load_force_absolute_tolerance_n,
            relative=control.balance_relative_tolerance,
            scale=total_fy,
        ),
        _within(
            residuals.yaw_moment_n_m,
            absolute=control.load_moment_absolute_tolerance_n_m,
            relative=control.balance_relative_tolerance,
            scale=total_mz,
        ),
    )
    if not all(checks):
        return _invalid_step(
            state=state,
            reason=f"declared balance residual exceeded tolerance: {residuals!r}",
            normal_loads_n=normal_loads,
            contact_results=contact_results,
            iterations=iteration,
        )

    dt = control.time_step_s
    u_dot = new_ax + state.yaw_rate_rad_per_s * state.lateral_velocity_m_per_s
    v_dot = new_ay - state.yaw_rate_rad_per_s * state.longitudinal_velocity_m_per_s
    cosine_heading = math.cos(state.heading_rad)
    sine_heading = math.sin(state.heading_rad)
    x_dot = (
        cosine_heading * state.longitudinal_velocity_m_per_s
        - sine_heading * state.lateral_velocity_m_per_s
    )
    y_dot = (
        sine_heading * state.longitudinal_velocity_m_per_s
        + cosine_heading * state.lateral_velocity_m_per_s
    )
    values = (
        state.time_s + dt,
        state.x_position_m + x_dot * dt,
        state.y_position_m + y_dot * dt,
        state.heading_rad + state.yaw_rate_rad_per_s * dt,
        state.longitudinal_velocity_m_per_s + u_dot * dt,
        state.lateral_velocity_m_per_s + v_dot * dt,
        state.yaw_rate_rad_per_s + yaw_acceleration * dt,
    )
    if not all(math.isfinite(value) for value in values):
        return _invalid_step(
            state=state,
            reason="state integration produced a non-finite result",
            normal_loads_n=normal_loads,
            contact_results=contact_results,
            iterations=iteration,
        )
    end_state = PlanarState(*values)
    return PlanarStepResult(
        model_version=MODEL_VERSION,
        status="ok",
        reason="planar step converged and all declared balances closed",
        start_state=state,
        end_state=end_state,
        contact_results=contact_results,
        normal_loads_n=normal_loads,
        load_iterations=iteration,
        converged=True,
        longitudinal_acceleration_m_per_s2=new_ax,
        lateral_acceleration_m_per_s2=new_ay,
        yaw_acceleration_rad_per_s2=yaw_acceleration,
        total_body_longitudinal_force_n=total_fx,
        total_body_lateral_force_n=total_fy,
        total_yaw_moment_n_m=total_mz,
        saturated_contact_count=sum(
            result.tyre_force.saturated for result in contact_results
        ),
        residuals=residuals,
    )
