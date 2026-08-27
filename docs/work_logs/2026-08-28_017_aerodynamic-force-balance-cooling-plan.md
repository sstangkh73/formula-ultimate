# Work 017 Plan: Aerodynamic Force, Balance, and Cooling Flow

Status: Completed

Thai companion: `2026-08-28_017_aerodynamic-force-balance-cooling-plan.th.md`

## Objective

Implement a deterministic Level-0 aerodynamic coefficient-map evaluator that
interpolates drag, side force, downforce, pitch/yaw moment, and ram-air cooling
flow across declared speed, ride-height, yaw, and discrete active-state
envelopes while preserving provenance, interpolation evidence, residuals, and
invalid/out-of-envelope states.

## Scope

- Define SI contracts for a topology-neutral aerodynamic reference, map
  provenance, grid axes, active-state grids, coefficient samples, operating
  points, interpolation evidence, force/moment/cooling outputs, and residuals.
- Do not prescribe wings, body shape, wheel count, conventional aero devices,
  or a current Formula One layout.
- Require complete deterministic coefficient grids and reject duplicate active
  states, unordered axes, missing samples, and unsupported evidence contracts.
- Use tensor-product linear interpolation over airspeed, ride height, and yaw;
  active state is discrete and never interpolated.
- Reject points outside the declared envelope rather than clamp or extrapolate.
- Convert coefficients to drag, side force, downforce, pitch moment, and yaw
  moment using dynamic pressure and declared reference dimensions.
- Derive a signed longitudinal centre of pressure only when downforce is
  non-zero, keeping pitch-moment evidence independently observable.
- Convert cooling-flow coefficient to air mass flow, heat-capacity rate,
  effective conductance, and signed heat rejection/absorption at declared air
  and component temperatures.
- Test exact nodes, interpolation, symmetry reference behavior, speed-squared
  force scaling, ride-height/yaw effects, active-state trade-off, zero-speed
  behavior, provenance, exact replay, malformed grids, and out-of-envelope
  rejection.
- Add a validator, bilingual model/result documentation, validation evidence,
  and one verified commit. Do not start Work 018.

## Planned files

- `src/formula_ultimate/physics/aerodynamics.py`
- `src/formula_ultimate/physics/__init__.py`
- `tests/test_aerodynamics.py`
- `scripts/validate_aerodynamics.py`
- `docs/physics/AERODYNAMIC_FORCE_BALANCE_COOLING_MODEL.md` and `.th.md`
- queue status and this bilingual plan/result pair
- a separate bilingual problem report for every issue encountered and resolved

## Physics boundary

At airspeed `V`, density `rho`, reference area `A`, and reference length `L`:

```text
q       = 0.5 * rho * V^2
drag    = q * A * C_D                 (positive magnitude opposing flow)
side    = q * A * C_Y                 (signed body +y)
down    = q * A * C_L_down            (signed positive body -z)
pitch   = q * A * L * C_m             (signed body +y moment)
yaw     = q * A * L * C_n             (signed body +z moment)
x_cp    = pitch / down                 (only when down != 0)
```

Cooling is a reduced-order ram-air path:

```text
m_dot_air = rho * V * A_inlet * C_flow
C_dot_air = m_dot_air * cp_air
G_cooling = effectiveness * C_dot_air
Q_reject  = G_cooling * (T_component - T_air)
```

Positive `Q_reject` means heat leaves a hotter component; negative means the
air heats a colder component. Active actuation energy and fan/pump work are not
included and must be accounted separately by energy models.

## Map and evidence semantics

Each map has strictly increasing axes and one complete ordered sample tuple per
active state. Sample order is speed-major, then ride-height, then yaw. Allowed
evidence bases are `synthetic_reference`, `geometry_derived`, `cfd`, and
`measured`. Geometry-derived evidence requires a SHA-256 geometry digest;
synthetic maps cannot be presented as geometry evidence.

Interpolation returns the two bracket indices and fraction on every continuous
axis. Exact nodes remain exact. A point outside any axis or with an unknown
active state returns observable `invalid` without boundary clamping.

## Experiment definition

- Preferred hypothesis: a declared aerodynamic map can deterministically expose
  force, balance, and cooling trade-offs across the full control envelope, while
  unsupported points and weak provenance remain distinguishable from validated
  geometry-derived evidence.
- Independent variables: coefficient grid, evidence basis, active state,
  airspeed, density, ride height, yaw, reference area/length, cooling inlet,
  air heat capacity, effectiveness, and temperatures.
- Dependent variables: interpolated coefficients, brackets/weights, dynamic
  pressure, forces, moments, centre of pressure, air mass flow, cooling
  conductance, heat flow, residuals, status, and reason.
- Controls: SI/sign convention, identical grid ordering, no extrapolation,
  tensor-linear interpolation, discrete active states, and zero random draws.
- Metrics: exact-node error, interpolation error, force/moment/cooling
  residuals, speed-squared force ratio, mass-flow speed ratio, symmetry signs,
  active-state drag/cooling delta, replay equality, and invalid-case coverage.
- Success: all node/interior/envelope reference cases match analytical values;
  the active-state trade-off is observable; malformed/outside cases fail; full
  repository gates pass.
- Failure criteria: silent extrapolation/clamping, incomplete grids, non-finite
  values, negative drag or cooling-flow coefficients, invalid provenance, or a
  declared algebraic residual outside tolerance.
- Falsification: query below/above every continuous envelope, request an unknown
  active state, provide an incomplete grid, and provide geometry-derived
  evidence without a digest; none may be accepted.

## Risks

- Linear interpolation cannot reproduce nonlinear separated-flow transitions
  between sparse nodes.
- Coefficient maps are only as credible as their geometry/CFD/test provenance;
  a synthetic map is software evidence only.
- The cooling model omits pressure-drop curves, duct losses, heat-exchanger UA,
  fan work, recirculation, and compressibility.
- Quasi-steady coefficients omit gusts, wake history, transient active-device
  motion, and fluid-structure interaction.

## Explicit non-goals

- No CFD solver, wind-tunnel calibration, geometry meshing, automatic
  coefficient extraction, or claim of real aerodynamic performance.
- No prescribed vehicle shape or conventional aerodynamic component library.
- No suspension/braking/regen implementation, Work 018, or remote push.

## Validation

```powershell
python -m unittest tests.test_aerodynamics -v
python -m unittest discover -s tests -v
python scripts/validate_aerodynamics.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Every gate runs fail-fast. Completion requires bilingual results, separate
problem reports for encountered issues, explicit staged scope, a successful
commit, and post-commit clean-state/hash evidence.
