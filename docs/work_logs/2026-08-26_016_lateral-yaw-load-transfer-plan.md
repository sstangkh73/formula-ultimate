# Work 016 Plan: Lateral/Yaw Dynamics and Load Transfer

Status: Completed

Thai companion: `2026-08-26_016_lateral-yaw-load-transfer-plan.th.md`

## Objective

Implement a deterministic Level-0 planar rigid-body model that couples lateral
and yaw dynamics, quasi-static longitudinal/lateral load transfer, and Work 011
combined tyre-force saturation while keeping force, moment, load, convergence,
and invalid-state evidence observable.

## Scope

- Define strict SI contracts for an arbitrary set of ground contact patches;
  do not require a conventional four-wheel or two-axle topology.
- Represent each contact by its body-frame position, steer angle, cornering
  stiffness, friction parameters, requested longitudinal force, and declared
  baseline normal load.
- Compute contact slip kinematics from body longitudinal/lateral velocity and
  yaw rate, then request lateral force from a documented linear slip-angle law.
- Pass every requested longitudinal/lateral pair through Work 011 combined-force
  saturation and expose requested, applied, utilization, and saturation state.
- Solve quasi-static normal loads from declared vertical, pitch, and roll
  equilibrium with a deterministic minimum-change projection from baseline
  loads. Report residuals and reject contact lift instead of clipping loads.
- Iterate force-dependent load transfer with a fixed deterministic limit and
  explicit convergence outcome.
- Advance planar body velocity, yaw rate, heading, and position with declared
  integration semantics and expose force/moment balance residuals.
- Test a non-conventional contact layout, steady straight equilibrium,
  transient steering response, saturation, longitudinal and lateral load
  transfer, exact replay, non-convergence, singular layout, contact lift, and
  invalid numerical inputs.
- Add a validator, bilingual model/result documentation, validation evidence,
  and one verified commit. Do not start Work 017.

## Planned files

- `src/formula_ultimate/physics/lateral.py`
- `src/formula_ultimate/physics/__init__.py`
- `tests/test_lateral.py`
- `scripts/validate_lateral.py`
- `docs/physics/LATERAL_YAW_LOAD_TRANSFER_MODEL.md` and `.th.md`
- queue status and this bilingual plan/result pair
- a separate bilingual problem report only if a material problem occurs

## Physics boundary

The vehicle is one planar rigid body with body-frame velocity `(u, v)`, yaw
rate `r`, mass `m`, yaw inertia `I_z`, and centre-of-mass height `h`. For contact
position `(x_i, y_i)` and steer angle `delta_i`, the contact velocity is rotated
into its local tyre frame. The requested lateral force is:

```text
alpha_i = atan2(v_local_y, max(abs(v_local_x), v_regularization))
Fy_requested_i = -C_alpha_i * alpha_i
```

The pair `(Fx_requested_i, Fy_requested_i)` is then resolved by the existing
Work 011 friction-circle/ellipse model at the current normal load.

Normal loads satisfy the declared quasi-static constraints:

```text
sum(Fz_i)       = m * g
sum(x_i Fz_i)   = -m * a_x * h
sum(y_i Fz_i)   = -m * a_y * h
```

The solver selects the unique minimum Euclidean change from declared baseline
loads subject to these constraints. A rank-deficient contact layout, negative
normal load, non-finite state, or failed fixed-point convergence is observable
as invalid; no hidden clipping or silent repair is allowed.

Planar force and yaw-moment balances are:

```text
m * (du/dt - r*v) = sum(Fx_body_i)
m * (dv/dt + r*u) = sum(Fy_body_i)
I_z * dr/dt       = sum(x_i*Fy_body_i - y_i*Fx_body_i)
```

## Experiment definition

- Preferred hypothesis: adding explicit load transfer and yaw dynamics changes
  available combined tyre force in a deterministic, balance-closing way; a
  force request that ignores these couplings should be falsifiable by
  saturation, lift, convergence, or residual evidence.
- Independent variables: contact topology and locations, baseline loads,
  steering, cornering stiffness, friction limits, longitudinal requests, mass,
  yaw inertia, centre-of-mass height, state, time step, and solver tolerance.
- Dependent variables: normal loads, slip angles, requested/applied contact
  forces, utilization, body force/moment, accelerations, state, convergence,
  iterations, residuals, and validity.
- Controls: SI/sign conventions, Work 011 saturation law, deterministic contact
  order, fixed solver limit/tolerance, identical initial state, and no random
  draws.
- Metrics: vertical/pitch/roll residuals, longitudinal/lateral/yaw balance
  residuals, solver iterations, replay equality, saturation count, and state
  response.
- Success: a steady zero-slip case converges; a steering transient produces the
  expected lateral/yaw signs; load-transfer direction and all declared balances
  pass analytical checks; exact replay and repository gates pass.
- Failure criteria: singular contact geometry, contact lift, non-convergence,
  non-finite arithmetic, or a residual outside declared tolerance is invalid.
- Falsification: force an over-limit combined request, an excessive-CG-height
  lift case, a rank-deficient layout, and a deliberately insufficient iteration
  budget; none may be silently accepted.

## Risks

- The planar rigid body omits heave, pitch, roll rates, suspension travel,
  compliance, camber, relaxation length, tyre temperature, and aero loads.
- Linear cornering stiffness is a Level-0 request law, not a calibrated tyre
  model; Work 011 only bounds the resulting force.
- Quasi-static load transfer assumes instantaneous vertical equilibrium and can
  overstate response during fast transients.
- Explicit time integration is deterministic but step-size dependent; residuals
  prove internal accounting, not real-world accuracy.

## Explicit non-goals

- No conventional wheel-count/layout requirement and no claim that this model
  covers every open-ended locomotion architecture.
- No aerodynamic, suspension, braking-system, regenerative, degradation,
  traffic, weather, strategy, lap-time, safety, or physical-validation claim.
- No Work 017 implementation and no remote push.

## Validation

```powershell
python -m unittest tests.test_lateral -v
python -m unittest discover -s tests -v
python scripts/validate_lateral.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Every gate runs fail-fast. Completion requires bilingual results, explicit
staged scope, a successful commit, and post-commit clean-state/hash evidence.
