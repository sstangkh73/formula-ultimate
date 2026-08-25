# Tyre-Road Combined-Force Model

Status: Implemented for Work 011

Thai companion: `TYRE_ROAD_MODEL.th.md`

## Purpose and claim boundary

The Work 011 model is a deterministic force-capacity gate for one tyre contact
patch. It prevents simultaneous independent use of full longitudinal and full
lateral grip, while preserving the exact force requested by an agent and the
force actually applied.

It is an analytical friction circle/ellipse. It is not a calibrated tyre model
and does not establish real tyre performance, physical validation, safety, or
lap-time accuracy.

## Unit and sign contract

- Forces and normal load use newtons (`N`).
- Friction coefficients and utilization are dimensionless.
- Positive/negative longitudinal and lateral request signs are both valid. The
  capacity is symmetric in all four force quadrants.
- Normal load must be nonnegative. Friction coefficients must be positive.
- Requested force is never overwritten; applied force and residual are separate
  output fields.

## Friction ellipse

For normal load `Fz > 0`, longitudinal coefficient `mu_x`, lateral coefficient
`mu_y`, and requested forces `Fx_req`, `Fy_req`:

```text
Fx_limit = mu_x Fz
Fy_limit = mu_y Fz

u_requested = sqrt(
    (Fx_req / Fx_limit)^2 +
    (Fy_req / Fy_limit)^2
)
```

When `mu_x = mu_y`, this is a friction circle. Otherwise it is an ellipse.

```text
if u_requested <= 1 + boundary_tolerance:
    scale = 1
else:
    scale = 1 / u_requested

Fx_applied = scale Fx_req
Fy_applied = scale Fy_req
residual   = requested - applied
```

Radial projection in normalized coordinates preserves the force direction and
places an over-limit request on the combined-force boundary. It does not clip
each axis independently.

The default `boundary_tolerance` is `1e-12` and cannot exceed `1e-6`. Raw
requested and applied utilization remain visible, including a within-tolerance
value slightly above one.

## Observable states

| Status | Meaning |
|---|---|
| `within_limit` | Request is unchanged within the declared tolerance |
| `saturated` | Request is radially projected to the ellipse |
| `no_contact_zero_request` | Zero load and zero request; no transmitted force |
| `no_normal_load` | Zero load with nonzero request; applied force is zero and the complete request remains residual |

For a nonzero request at zero normal load, requested utilization is undefined
and represented as `None`, not infinity or NaN. Capacity-axis underflow or
overflow raises `TyreNumericalError`; invalid inputs raise `TyreInputError`.

## Analytical references

With `mu_x = mu_y = 1`, `Fz = 4000 N`, and request `(3000, 4000) N`:

```text
u_requested = 1.25
scale = 0.8
applied = (2400, 3200) N
residual = (600, 800) N
u_applied = 1.0
```

The anisotropic boundary test uses `mu_x = 1.5`, `mu_y = 1.0`, `Fz = 4000 N`,
`Fx = 3000 N`, and `Fy = 4000 sqrt(0.75) N`; its utilization is exactly one
within floating-point precision and the force remains unchanged.

Run:

```powershell
python scripts/validate_tyre.py
python -m unittest tests.test_tyre -v
```

## Limitations and next work

- No slip ratio, slip angle, stiffness, relaxation length, aligning moment,
  camber, pneumatic trail, load sensitivity, temperature, wear, degradation,
  surface texture, water depth, or aquaplaning.
- The coefficients are declared inputs, not measured data in this work item.
- One contact patch does not compute normal-load transfer, axle balance, yaw,
  or suspension behavior.
- Work 016 may consume this capacity law inside lateral/yaw dynamics, but must
  retain requested/applied force and saturation evidence.
- Work 012 next implements typed energy/powertrain flow; it must not infer
  energy consumption from force without an explicit velocity and loss contract.
