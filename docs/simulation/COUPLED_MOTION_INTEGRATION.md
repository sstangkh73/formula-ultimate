# Coupled Motion Integration

Thai companion: `COUPLED_MOTION_INTEGRATION.th.md`

## Purpose and Boundary

Work 026 advances one topology-neutral `SharedVehicleState` from the Work 024 aerodynamic wrench and Work 025 aggregate contact wrench. It is a deterministic planar Level-0 selection model, not physical validation.

The module solves global horizontal translation and yaw. It does not solve heave, pitch, roll, suspension constraint impulses, surveyed racing-line selection, barrier contact, or tyre relaxation.

## Inputs and Frame Contract

- `aero.force_moment`: force and moment expressed in the vehicle body frame about the centre of mass.
- `contact.force_moment`: per-contact forces plus declared body-frame totals.
- `circuit.segment_inputs`: an available `SpatialStepEvidence` sample with local curvature, grade, bank, widths, and uncertainty.
- `state.current`: global local-ENU position/velocity plus yaw and yaw rate.
- `MotionCorridorReference`: local-ENU centreline position and heading at exactly the start state's race distance.
- `MotionConfiguration`: mass, yaw inertia, duration, and vehicle width in SI units.

Architecture `coupled-level0-reference-v2` routes the corridor signal into `vehicle_motion_solver`. Version 1 remains unchanged as historical evidence.

## Equations

The declared body-frame horizontal wrench is:

`F_x = F_x,aero + F_x,contact`

`F_y = F_y,aero + F_y,contact`

`M_z = M_z,aero + M_z,contact`

With constant wrench over `dt`, midpoint orientation is:

`psi_mid = psi_0 + 0.5*r_0*dt + 0.125*(M_z/I_z)*dt^2`

The body force is rotated to global local-ENU at `psi_mid`, velocity is advanced once, and position uses trapezoidal velocity:

`v_1 = v_0 + R(psi_mid) * [F_x/m, F_y/m] * dt`

`p_1 = p_0 + 0.5*(v_0 + v_1)*dt`

`r_1 = r_0 + (M_z/I_z)*dt`

`psi_1 = psi_0 + r_0*dt + 0.5*(M_z/I_z)*dt^2`

The vertical axis is not projected onto the road. Work 026 preserves `v_z` and applies `z_1 = z_0 + v_z*dt`; `motion.kinematic-z` exposes its consistency. Grade is retained as evidence for later constrained 3D motion work.

## Race Progress and Corridor Gate

Horizontal displacement is projected onto the local corridor tangent. For non-zero curvature, six deterministic fixed-point iterations evaluate the tangent at the estimated midpoint. Positive tangent progress is credited; negative progress is recorded as `reverse_progress_m` and receives zero race-distance credit. Pure lateral motion therefore cannot increase race distance.

The centreline advances by the credited progress. Candidate lateral offset is measured against its end tangent. Effective left and right widths subtract horizontal evidence uncertainty and half the declared vehicle width. A negative clearance marks `departed`; the adapter returns `invalid` with zero output signals. The state is never projected back into the corridor.

This is a local body-width screen. It does not yet sweep vehicle length, yawed corners, overhang, barriers, or kerbs. Work 010 remains the separate static swept-envelope feasibility screen.

## Observable Residuals

Nine residuals are retained:

- three input aggregation checks for contact `F_x`, `F_y`, and `M_z`;
- two horizontal force balances;
- one yaw-moment balance;
- three position-kinematic checks for `x`, `y`, and `z`.

An inconsistent contact total, failed balance, missing spatial record, mismatched corridor reference, off-corridor start, or departed candidate makes the adapter invalid. No motion candidate is written.

## Analytical Evidence

The standalone validator demonstrates:

- constant straight force: `v_x = 12 m/s`, `x = 11 m`, and race distance `= 11 m` after `1 s` from `v_x = 10 m/s` with `F_x = 2000 N`, `m = 1000 kg`;
- all nine residuals pass;
- rotating constant body force: reducing `dt` from `1.0 s` to `0.05 s` reduces one-second position error from `0.08383245221108916 m` to `0.00019773501705859235 m`;
- lateral-only credited progress is `0 m`;
- reverse raw progress is `-2 m`, credited progress is `0 m`, and uncredited reverse evidence is `2 m`;
- corridor departure and missing spatial evidence both return `invalid` with zero outputs;
- identical inputs replay exactly.

## Limitations and Promotion Boundary

The corridor fixtures are analytical and local. No current ten-circuit profile is promoted to surveyed 3D admission by this work. Bank and grade do not yet contribute constraint forces. Force inputs are held constant within a step. Level 0 may reject or rank candidates, but cannot establish real-world performance or safety.
