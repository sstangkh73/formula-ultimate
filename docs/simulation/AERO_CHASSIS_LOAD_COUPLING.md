# Aerodynamic Chassis and Normal-Load Coupling

Thai companion: `AERO_CHASSIS_LOAD_COUPLING.th.md`

## Boundary

Work 024 connects declared `local_enu` weather and shared motion state to the
Work 017 aerodynamic map, translates its wrench to the centre of mass, and
projects normal loads across any non-rank-deficient contact topology. It emits
the exact `aerodynamic_map` and `normal_load_solver` signal sets.

Declared weather may be `observed` or `synthetic_control`. The numerical path
is shared, but the typed status and scenario fingerprint preserve the evidence
class; a synthetic control never becomes real-circuit evidence.

This remains Level 0. Synthetic coefficients and analytical weather are not CFD,
measurement, calibration, safety, or physical validation.

## Axes and wrench translation

Body axes are `x` forward, `y` left, `z` up. Positive map drag/downforce become
body forces `(-drag, side, -downforce)`. The map intrinsic moment is
`(0, pitching_moment, yawing_moment)`. A declared reference origin `r` from the
centre of mass is translated using:

```text
M_com = M_map + r x F
```

The raw/queried airspeed and yaw, plus any numerical node snap, remain in
`AerodynamicQueryEvidence`.

## Atmosphere and relative wind

Observed pressure, temperature, and relative humidity produce moist-air density
from an ideal dry-air/water-vapour mixture with Tetens saturation pressure.
Vehicle velocity minus `local_enu` wind is rotated into body axes using yaw.
The resulting magnitude and yaw query the map.

Coordinate-transform roundoff may snap to a declared node only within `1e-12`.
The snap is recorded. Larger out-of-envelope values remain invalid with zero
writes; there is no physical clamp.

## Normal-load equilibrium

The solver makes the minimum Euclidean change from declared baseline loads while
satisfying three equations. With aero force `(Fx,Fy,Fz)`, COM moment
`(Mx,My,Mz)`, accelerations `(ax,ay)`, mass `m`, COM height `h`, and contact
coordinates `(xi,yi)`:

```text
sum(Ni)      + Fz - m*g       = 0
sum(xi*Ni)   + m*ax*h - My    = 0
sum(yi*Ni)   + m*ay*h + Mx    = 0
```

The raw vertical, pitch, and roll residuals are emitted as SI `ResidualEntry`
records. Rank-deficient geometry, negative contact load, or failed residual
invalidates the adapter; loads are never clipped or redistributed secretly.

## Evidence

The analytical validator produces drag `-525.9915 N`, downforce `-1051.9830 N`,
cooling heat rejection `17620.7160 W`, and a forward-origin pitch moment
`1051.9830 N*m`. Front loads rise to `2978.4915 N` each while rear loads remain
`2452.5 N`; vertical/roll residuals are zero and pitch residual is
`-9.09e-13 N*m`. An outside-speed query is invalid and emits zero signals.

Tests also cover humidity density direction, ENU rotation, exact replay,
symmetric downforce, forward load shift, arbitrary three-contact topology,
contact-ID mismatch, rank deficiency, lift, and invalid declarations.

## Limitations and next work

The acceleration estimate is an explicit adapter configuration until Work 026
closes motion feedback. No tyre/suspension/brake force is resolved here. Work 025
must consume these contact loads without hidden redistribution. A successful
Level-0 balance is not proof of real aerodynamics or structural feasibility.
