# Aerodynamic Force, Balance, and Cooling-Flow Model

Thai companion: `AERODYNAMIC_FORCE_BALANCE_COOLING_MODEL.th.md`

## Status and claim boundary

Work 017 implements `work017-aerodynamic-map-v1`, a deterministic Level-0
coefficient-map evaluator. It resolves quasi-steady aerodynamic forces,
pitch/yaw moments, longitudinal centre of pressure, and ram-air cooling flow at
one operating point inside a declared speed, ride-height, yaw, and active-state
envelope.

It is not a CFD solver, wind-tunnel result, geometry mesher, calibrated vehicle
model, safety case, or physical validation. The repository's included reference
map is explicitly synthetic.

## Topology and geometry boundary

The model uses reference area and length rather than prescribing wings, body
shape, wheel count, or conventional Formula One architecture. Any candidate
topology may supply a coefficient map if its evidence contract is satisfied.

`AerodynamicEvidence.basis` must be one of:

- `synthetic_reference`: analytical/software fixture only;
- `geometry_derived`: derived from identified geometry and therefore requires a
  64-character lowercase SHA-256 geometry digest;
- `cfd`: externally generated computational-flow evidence; or
- `measured`: externally generated test evidence.

The evaluator records the evidence but does not independently verify CFD or
measurement quality. A digest links data to geometry; it does not prove mesh
quality, convergence, uncertainty, or experimental validity.

## Map contract and ordering

`AerodynamicCoefficientMap` declares strictly increasing axes:

```text
airspeeds_m_per_s >= 0
ride_heights_m   >= 0
yaw_angles_rad    finite and signed
```

Each unique active state owns one complete sample tuple. The deterministic
flattened order is speed-major, then ride-height, then yaw:

```text
index = (speed_index * height_count + height_index) * yaw_count + yaw_index
```

Each sample stores:

- non-negative drag coefficient `C_D`;
- signed side-force coefficient `C_Y`;
- signed downforce coefficient `C_L_down` (positive means body `-z` force);
- signed pitching-moment coefficient `C_m` about body `+y`;
- signed yawing-moment coefficient `C_n` about body `+z`; and
- non-negative cooling-flow coefficient `C_flow`.

Negative `C_L_down` is permitted and represents lift under this sign contract.
Active states are discrete; the evaluator never invents a fractional state.

## Envelope and interpolation

The evaluator finds an exact node or two brackets on each continuous axis and
performs tensor-product linear interpolation. The result preserves lower/upper
indices, values, fractions, active-state identity, and whether all three axes
were exact nodes.

Points below or above any continuous axis and unknown active states return
`invalid`. No extrapolation or boundary clamping occurs. Decimal bracket
fractions retain normal binary floating-point representation; for example, the
mathematical midpoint of `0.04` and `0.08` is recorded as
`0.4999999999999999` on the tested runtime.

## Force, moment, and balance equations

For airspeed `V`, air density `rho`, reference area `A`, and reference length
`L`:

```text
q       = 0.5 * rho * V^2
drag    = q * A * C_D
side    = q * A * C_Y
down    = q * A * C_L_down
pitch   = q * A * L * C_m
yaw     = q * A * L * C_n
x_cp    = pitch / down, when down != 0
```

`drag` is a positive magnitude opposing the relative airflow. `side`, `down`,
`pitch`, and `yaw` retain their declared signs. `x_cp` is signed relative to the
reference origin and is omitted when downforce is zero. Pitch moment is always
retained, so omitting `x_cp` never hides moment evidence.

The result independently recomputes and exposes residuals for all five
force/moment equations. A non-finite result or residual magnitude above
`1e-9` in its SI unit returns `invalid`.

## Ram-air cooling equations

For cooling inlet area `A_inlet`, air specific heat `cp_air`, effectiveness
`epsilon`, component temperature `T_component`, and air temperature `T_air`:

```text
m_dot_air = rho * V * A_inlet * C_flow
C_dot_air = m_dot_air * cp_air
G_cooling = epsilon * C_dot_air
Q_reject  = G_cooling * (T_component - T_air)
```

`Q_reject > 0` means heat leaves a hotter component. `Q_reject < 0` means the
air adds heat to a colder component. Zero airspeed produces zero ram flow,
conductance, and heat transfer even if the map coefficient is non-zero.

Mass-flow, conductance, and heat-flow residuals are explicit. The model does
not include pressure loss, a fan or pump curve, heat-exchanger UA limits,
recirculation, compressibility, or active-device energy. Any actuation/fan/pump
energy must be declared in Work 012/013-compatible accounting.

## Reference evidence

`scripts/validate_aerodynamics.py` evaluates a synthetic two-state map and
checks:

- an interior operating point with all eight algebraic residuals zero;
- `40/20 m/s` drag ratio `4.0` from `V^2` scaling;
- `40/20 m/s` ram-air mass-flow ratio `2.0` from linear `V` scaling;
- cooling-open state raises both drag and cooling mass flow;
- exact replay equality; and
- `41 m/s` outside a `0–40 m/s` map returns `invalid`.

The unit suite additionally checks exact nodes, tensor interpolation,
yaw-symmetric drag/downforce, yaw-antisymmetric side force/moment, signed heat
flow, zero speed, geometry-digest provenance, malformed grids, every envelope
dimension, unknown active state, and runtime non-finite output.

## Current integration boundary

Work 017 returns forces, moments, centre of pressure, and cooling conductance as
typed evidence. It does not yet inject those values into Work 015 race motion,
Work 016 contact loads, or Work 014 thermal integration. That coupling needs a
later explicitly planned experiment with event ordering and conservation checks.

## Limitations and follow-up

- Tensor-linear interpolation can miss nonlinear separation, stall, hysteresis,
  ground-effect transitions, and wake interactions between sparse nodes.
- Coefficients are quasi-steady and omit gusts, transient device motion,
  compressibility, fluid-structure interaction, and turbulence uncertainty.
- Synthetic tests validate software semantics only. Real candidate evaluation
  requires geometry-linked CFD or measurement with uncertainty and independent
  higher-fidelity checks.
- Work 018 owns suspension, mechanical braking, and regenerative braking and is
  not implemented here.
