# Circuit Corridor and Swept-Envelope Model

Status: Implemented for Work 010

Thai companion: `CIRCUIT_CORRIDOR_MODEL.th.md`

## Purpose and claim boundary

This model is an auditable early feasibility gate between the real-circuit
catalogue and later vehicle dynamics. It can reject a rigid vehicle whose
width, steering lock, wheelbase, or overhang cannot fit an analytical corridor.
It does not establish physical validation, collision safety, lap time, or race
completion.

The repository contains analytical fixtures, not survey geometry for the ten
real circuits. Those ten profiles therefore remain `indeterminate` at this
gate. The evidence limitation and resolution are recorded in
`docs/problem_reports/2026-08-25_010_survey-geometry-evidence-gap.md`.

## Coordinate, unit, and sign contract

- All distances use metres; curvature uses `1/m`; angles use radians.
- The reference point is the vehicle rear-axle center.
- Local `x-y` is a right-handed horizontal Cartesian plane and `z` is up.
- Heading zero points along positive `x`; positive curvature turns left.
- Positive grade increases `z`; positive bank is stored as a corridor property.
- `width_left_m` and `width_right_m` are perpendicular horizontal distances
  from the centerline. Horizontal evidence uncertainty is conservatively
  subtracted from both sides.
- Segment `length_m` is horizontal plan distance. Curvature, grade, bank, and
  widths are piecewise constant within one segment.

## Reference-line integration

For start pose `(x0, y0, z0, psi0)`, signed horizontal curvature `k`, plan
distance `s`, and grade `g`:

```text
psi1 = psi0 + k s

if k = 0:
    x1 = x0 + s cos(psi0)
    y1 = y0 + s sin(psi0)
else:
    x1 = x0 + [sin(psi1) - sin(psi0)] / k
    y1 = y0 + [-cos(psi1) + cos(psi0)] / k

z1 = z0 + s tan(g)
```

The exact constant-curvature update is applied at deterministic station
spacing. Closure residual reports horizontal position, vertical position, and
wrapped heading error; it is never silently corrected.

## Steering and swept-envelope screen

The necessary bicycle-model steering angle for wheelbase `L` is:

```text
delta_required = atan(L |k|)
```

For a curved segment, centerline radius is `R = 1 / |k|`, vehicle half-width is
`w/2`, and longitudinal extent from the rear axle is:

```text
a = max(wheelbase + front_overhang, rear_overhang)
```

The rigid-body radial extrema are:

```text
r_inside_vehicle  = max(0, R - w/2)
r_outside_vehicle = sqrt(a^2 + (R + w/2)^2)
```

The evidence-adjusted inside/outside corridor radii depend on turn direction.
Both radial margins must be nonnegative and required steering must not exceed
the declared steering limit. A straight uses left/right static margins.

This construction deliberately tests a falsifying case: a vehicle can pass the
static width check but fail because its front outside corner sweeps beyond a
tight curved boundary.

## Evidence and outcome states

| Evidence or geometry result | Status | Meaning |
|---|---|---|
| Any steering or boundary failure | `rejected` | Necessary geometry condition failed |
| Passing `surveyed` or `operator_engineering` evidence | `admitted` | May proceed past this gate only |
| Passing `synthetic_validation` fixture | `verification_passed` | Equation fixture passed; no real-race authority |
| Passing approximate/digitized evidence | `indeterminate` | Evidence cannot authorize admission |
| No real-circuit corridor | `indeterminate` | Required geometry is absent |

Admission means only that this reduced-order geometry gate passed. It is not a
claim of physical validation.

## Deterministic fixture and validator

`config/circuits/corridor_schema_v1.json` contains three transparent analytical
fixtures: a 20 m-radius full circle, a static-fit/overhang-fail tight arc, and a
steering-limit failure. Run:

```powershell
python scripts/validate_corridor.py
python -m unittest tests.test_corridor -v
```

The validator also loads all ten Work 008 profiles and requires each to remain
`indeterminate` because no admission-capable corridor is present.

## Limitations and next evidence

- Rigid planar sweep omits tyre slip, compliance, yaw transient, roll, pitch,
  suspension motion, aero deformation, kerbs, walls, and collision dynamics.
- Grade and bank are integrated/stored but do not yet alter the planar swept
  envelope or force capacity.
- Piecewise-constant inputs can approximate a surveyed path only after a
  separately audited import and discretization study.
- A real layout requires a licensed survey or circuit-operator engineering
  export with coordinate reference system, boundaries, timestamp, uncertainty,
  and closure audit before it can produce `admitted`.
- Work 011 adds tyre-road force saturation; it must not reinterpret Work 010 as
  dynamic proof.
