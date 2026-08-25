# Work 011 Plan: Tyre-Road Combined-Force Saturation

Status: Completed

Thai companion: `2026-08-26_011_tyre-road-saturation-plan.th.md`

## Objective

Implement a deterministic Level-0 tyre-road contact law that accepts requested
longitudinal and lateral force, applies an auditable friction circle or ellipse,
and exposes both requested and applied force, utilization, saturation scale,
residual, normal load, and limiting reason.

## Scope

- Define strict SI contracts for contact parameters, force requests, and force
  results.
- Support isotropic friction circles and anisotropic friction ellipses through
  independent longitudinal and lateral friction coefficients.
- Project an over-limit request radially onto the normalized ellipse without
  silently overwriting the requested force.
- Treat zero normal load as a distinct observable no-contact state.
- Preserve deterministic symmetry for all force quadrants.
- Add analytical boundary, saturated, unsaturated, zero-load, invalid-input,
  monotonicity, and replay tests.
- Add a validator and bilingual model/result documentation.
- Validate and commit Work 011 separately before Work 012 begins.

## Planned files

- `src/formula_ultimate/physics/tyre.py`
- `src/formula_ultimate/physics/__init__.py`
- `scripts/validate_tyre.py`
- `tests/test_tyre.py`
- `docs/physics/TYRE_ROAD_MODEL.md`
- `docs/physics/TYRE_ROAD_MODEL.th.md`
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md`
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.th.md`
- this Work 011 plan/result pair in English and Thai
- a separate bilingual problem report only if a material problem is found

## Model boundary and equations

For normal load `Fz >= 0`, longitudinal coefficient `mu_x > 0`, lateral
coefficient `mu_y > 0`, and request `(Fx_req, Fy_req)`, define axes:

```text
Fx_limit = mu_x Fz
Fy_limit = mu_y Fz
q = (Fx_req / Fx_limit)^2 + (Fy_req / Fy_limit)^2
```

For `Fz > 0`, requests with `q <= 1` pass unchanged. Requests with `q > 1`
receive scale `1 / sqrt(q)` on both components. Requested utilization is
`sqrt(q)` and applied utilization cannot exceed one except for declared floating
point tolerance. For `Fz = 0`, zero request returns `no_contact_zero_request`;
nonzero request returns zero applied force with an explicit `no_normal_load`
reason and no undefined numeric utilization.

This is a force-capacity boundary, not a slip-ratio/angle tyre curve. It cannot
predict relaxation, transients, heat, wear, surface variation, aquaplaning,
camber, aligning torque, or optimum slip.

## Experiment definition

### Preferred hypothesis

A combined force boundary prevents an agent from independently consuming full
longitudinal and lateral grip at the same contact patch while retaining exact
evidence of what the design requested.

### Independent variables

- requested longitudinal and lateral force;
- normal load;
- longitudinal and lateral friction coefficients.

### Dependent variables

- requested and applied utilization;
- saturation scale and boolean;
- applied force and force residual;
- contact status/reason.

### Controls

- SI units and fixed sign convention;
- radial projection in normalized force space;
- zero numerical randomness;
- same coefficients and normal load for compared requests.

### Falsification and failure criteria

- A request exactly on the ellipse must remain unchanged and unsaturated.
- A diagonal request outside a friction circle must be scaled to its analytical
  boundary, not clipped independently per axis.
- Increasing only normal load at fixed request and coefficients must never
  increase requested utilization.
- Negative/non-finite load, coefficient, or request is rejected where invalid;
  signed finite force requests remain valid.
- Zero normal load cannot transmit nonzero force and must not generate NaN.
- Identical inputs must replay identically.

## Validation

```powershell
python -m unittest tests.test_tyre -v
python -m unittest discover -s tests -v
python scripts/validate_tyre.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Commands will use fail-fast exit handling.

## Success criteria

- Circle and ellipse analytical references pass.
- Applied utilization remains within the declared boundary.
- Requested force, applied force, residual, saturation, and no-contact state are
  observable.
- Full tests, validator, compilation, bilingual Markdown contract, whitespace,
  explicit staged scope, commit, and post-commit verification pass.

## Risks

- A friction ellipse is deliberately simpler than a physical tyre curve and may
  encourage false confidence if exposed without its model boundary.
- Floating-point equality at the boundary needs a documented numerical
  tolerance while retaining raw utilization.
- A single contact patch does not determine axle load transfer or vehicle yaw.

## Explicit non-goals

- No Pacejka/Fiala calibration or empirical tyre claim.
- No slip ratio, slip angle, aligning torque, load transfer, thermal, wear,
  wet-surface, or aquaplaning physics.
- No direct integration into a lap-time/race loop in this work item.
- No Work 012 energy graph before Work 011 is committed.
- No remote push.
