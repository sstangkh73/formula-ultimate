# Work 011 Result: Tyre-Road Combined-Force Saturation

Status: Completed

Thai companion: `2026-08-26_011_tyre-road-saturation-result.th.md`

## Outcome

Work 011 is complete. A deterministic single-contact-patch friction
circle/ellipse now preserves requested longitudinal/lateral force separately
from applied force, residual, utilization, saturation scale, and status.

The preferred hypothesis was supported: a `(3000, 4000) N` request against a
`4000 N` isotropic capacity has utilization `1.25` and is radially scaled by
`0.8` to `(2400, 3200) N`. This prevents simultaneous independent full-axis
grip without hiding the agent's impossible request.

This is a Level-0 capacity law, not a calibrated slip-based tyre model or a
physical-validation claim.

## Files changed

- `src/formula_ultimate/physics/tyre.py`: input contracts, result telemetry,
  friction ellipse, zero-load states, and observable numerical failures.
- `src/formula_ultimate/physics/__init__.py`: public tyre API exports.
- `tests/test_tyre.py`: 11 analytical, symmetry, monotonicity, tolerance,
  zero-load, invalid-input, numerical-failure, and replay tests.
- `scripts/validate_tyre.py`: deterministic circle, ellipse, and zero-load
  references.
- `docs/physics/TYRE_ROAD_MODEL.md` and `.th.md`: equations, state meanings,
  numerical behavior, limitations, and follow-up.
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md` and `.th.md`: Work 011 status.
- this Work 011 plan/result pair in English and Thai.

## Decisions and observable behavior

1. Longitudinal/lateral capacity axes are `mu_x Fz` and `mu_y Fz`.
2. Utilization is Euclidean radius in normalized force space. An over-limit
   request receives one common scale `1 / utilization`, preserving direction.
3. Requests within `1 + boundary_tolerance` pass unchanged; the default
   tolerance is `1e-12` and cannot exceed `1e-6`.
4. Requested, applied, and residual force components remain separately visible.
5. Zero load plus zero request is `no_contact_zero_request`. Zero load plus a
   nonzero request is `no_normal_load`, applies zero force, retains the entire
   request as residual, and uses `None` for undefined requested utilization.
6. Invalid inputs raise `TyreInputError`. Floating-point capacity-axis
   underflow/overflow raises `TyreNumericalError`, never a silent force result.

## Experiment review

- Independent variables: requested force, normal load, and longitudinal/lateral
  friction coefficients.
- Dependent variables: utilization, scale, applied force, residual, saturation,
  and status.
- Controls: SI/sign convention, normalized radial projection, no randomness,
  identical parameters for compared cases.
- Supporting evidence: exact circle reference produces scale `0.8` and applied
  utilization `1.0`; anisotropic ellipse boundary remains unchanged; all force
  quadrants preserve sign/direction.
- Falsifying evidence attempted: static per-axis feasibility does not authorize
  diagonal combined force; zero load cannot transmit a force; capacity
  underflow is an explicit numerical error.
- Alternative explanation excluded: output is not independent axis clipping,
  because both components receive the same analytical scale.
- Missing evidence: empirical tyre coefficients and curves, slip behavior,
  load sensitivity, temperature, wear, wet track, and transient response.
- Confidence: high for the declared ellipse equation and software behavior;
  none for real tyre performance until calibrated evidence exists.

## Problems encountered

No material problem requiring a separate problem report was found. The
zero-load singularity and floating-point capacity underflow were anticipated in
the plan/model boundary and implemented as explicit states/errors with tests.

## Validation evidence

All commands ran from `C:\Formula Ultimate` with fail-fast exit handling.

### Work-specific tests

```powershell
python -m unittest tests.test_tyre -v
```

Exit status: `0`. Relevant output: `Ran 11 tests`; `OK`.

### Full repository tests

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`. Relevant output: `Ran 68 tests`; `OK`.

### Validator

```powershell
python scripts/validate_tyre.py
```

Exit status: `0`. Relevant output:

```text
outside circle: status=saturated, utilization=1.25, scale=0.8
outside circle applied force: [2400.0, 3200.0] N
inside ellipse: status=within_limit, utilization=0.7071067811865476
zero normal load: status=no_normal_load, scale=0.0
```

### Compilation and whitespace

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` for each command. The staged check is rerun after explicit
staging and before commit.

## Limitations and follow-up

- The law contains no slip curve, relaxation, torque, thermal, wear, surface,
  or wet-weather physics.
- Coefficients are inputs, not measured claims.
- Normal-load transfer and yaw remain outside this work item.
- Work 012 may connect applied longitudinal force to a typed energy graph only
  through explicit power, velocity, direction, and efficiency contracts.
