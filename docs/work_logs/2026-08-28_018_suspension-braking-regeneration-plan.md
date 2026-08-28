# Work 018 Plan: Suspension, Mechanical Braking, and Regeneration

Status: Completed

Thai companion: `2026-08-28_018_suspension-braking-regeneration-plan.th.md`

## Objective

Implement a deterministic Level-0 ground-contact suspension/brake interval
model that accounts for normal load, suspension force/travel, tyre-limited
braking, mechanical brake heat, regenerative storage/loss, and localized travel
or overtemperature failure events without prescribing a conventional wheel
count or vehicle layout.

## Scope

- Define SI contracts for an independently placed ground-contact module,
  suspension parameters/state, mechanical/regen limits, storage state, brake
  thermal state, interval input, output telemetry, residuals, and failure mode.
- Accept normal load as explicit upstream evidence from Work 016 plus any later
  aerodynamic-load coupling; do not invent or silently redistribute wheel load.
- Use a start-of-step linear spring/damper force and constant-acceleration
  suspension update with analytical travel-limit event localization.
- Allocate requested brake torque regen-first, then mechanical, subject to
  generator torque/power, storage charge power/capacity, brake thermal derating,
  mechanical torque, and tyre friction limits.
- Apply a common tyre-limit scale to the declared regen/mechanical blend and
  preserve unserved torque rather than silently increasing another path.
- Convert mechanical wheel work to brake heat and regenerative wheel work to
  stored energy plus conversion loss; expose a zero-closing energy residual.
- Reuse Work 014 thermal integration and exact failure crossing for the
  mechanical brake. The earliest suspension/thermal event truncates the whole
  contact interval and leaves unexecuted time explicit.
- Latch failure state and return explicit `none`, `suspension_travel`,
  `brake_overtemperature`, `simultaneous`, or `already_failed` failure mode.
- Test equilibrium, analytical suspension motion, localized travel failure,
  mechanical heat, regen energy, every regen limit, tyre saturation, thermal
  failure, already-failed state, exact replay, invalid input, and numerical
  invalidity.
- Add validator, bilingual model/result documentation, separate bilingual
  problem reports for every issue encountered, and one verified commit. Do not
  start Work 019.

## Planned files

- `src/formula_ultimate/physics/suspension_braking.py`
- `src/formula_ultimate/physics/__init__.py`
- `tests/test_suspension_braking.py`
- `scripts/validate_suspension_braking.py`
- `docs/physics/SUSPENSION_BRAKING_REGEN_MODEL.md` and `.th.md`
- queue status and this bilingual plan/result pair
- separate bilingual problem reports for encountered issues

## Suspension boundary

Travel `x` is positive in compression. At the interval start:

```text
F_suspension = preload + k*x + c*v
a_travel     = (F_normal - F_suspension) / m_effective
x(t)         = x0 + v0*t + 0.5*a_travel*t^2
v(t)         = v0 + a_travel*t
```

The acceleration is held constant for one interval. Valid travel is
`[-maximum_rebound, maximum_compression]`. The earliest outward quadratic/linear
crossing is localized analytically. The failure boundary is retained exactly;
travel is never clipped and the remainder of the interval is not executed.

## Brake allocation and energy boundary

For non-negative requested torque `T_request`, wheel speed `omega`, effective
radius `R`, normal load `Fz`, and friction coefficient `mu`:

```text
T_tyre_limit = mu * Fz * R

T_regen_capacity = min(
    T_regen_max,
    P_generator_max / omega,
    P_charge_max / (eta_regen * omega),
    E_storage_remaining / (eta_regen * omega * dt)
)

T_regen_allocated = min(T_request, T_regen_capacity)
T_mech_allocated  = min(T_request - T_regen_allocated,
                        T_mech_max * thermal_derating)
tyre_scale        = min(1, T_tyre_limit /
                           (T_regen_allocated + T_mech_allocated))
```

At zero/below-minimum regen speed, regen capacity is zero. Allocated torques are
fixed at the interval start. If an event truncates the interval, unused storage
capacity remains; torque is not re-optimized after the event.

For executed duration `dt_exec`:

```text
E_regen_wheel = T_regen_applied * omega * dt_exec
E_stored      = eta_regen * E_regen_wheel
E_regen_loss  = E_regen_wheel - E_stored
E_mech_heat   = T_mech_applied * omega * dt_exec

E_removed - E_stored - E_regen_loss - E_mech_heat = residual
```

Recovered energy increases only the declared storage state, never above its
capacity. This is observable recovery of vehicle kinetic work, not primary
energy replenishment or free energy.

## Event semantics

The model first computes candidate suspension travel crossing and Work 014
brake-temperature crossing over the requested interval. The earliest event sets
the executed duration. Exact-time ties return `simultaneous`. State and energy
are recomputed only through that duration. A previously failed suspension or
brake returns `already_failed` at zero executed time.

## Experiment definition

- Preferred hypothesis: a braking command is physically admissible only to the
  extent supported by contact load, suspension travel, component limits,
  storage capacity, and thermal survival; recovered energy must close against
  removed wheel work.
- Independent variables: normal load, suspension state/parameters, wheel speed,
  requested torque, tyre friction/radius, mechanical/regen limits, efficiency,
  storage capacity/state, thermal parameters/state, cooling, ambient, and step.
- Dependent variables: suspension force/acceleration/travel, tyre/regen/mechanical
  limits and torques, unserved torque, wheel/brake/storage/loss energy, brake
  temperature, event time/mode, state, residuals, and status.
- Controls: SI/sign convention, regen-first allocation, common tyre scaling,
  start-of-step fixed inputs, Work 014 thermal solver, deterministic event
  priority, and zero random draws.
- Metrics: suspension force residual, travel/event-time error, torque residual,
  energy residual, storage monotonicity/capacity, temperature/failure time,
  replay equality, and invalid-case coverage.
- Success: equilibrium and constant-acceleration references match analytically;
  travel and thermal failures localize; all torque/power/energy limits hold;
  energy balance closes and repository gates pass.
- Failure criteria: travel outside limits, thermal failure, negative/non-finite
  declarations, storage above capacity, energy residual outside tolerance, or
  runtime numerical failure.
- Falsification: force travel crossing, brake overtemperature, tyre saturation,
  generator torque/power limit, charge-power limit, storage-capacity limit,
  zero-speed regen, already-failed state, and extreme finite arithmetic; none
  may be silently accepted or create energy.

## Risks

- Independent contact modules omit coupled chassis heave/pitch/roll and anti-
  geometry, link kinematics, compliance, unsprung tyre stiffness, and road input.
- Constant acceleration and constant wheel speed over one step are reduced-order
  assumptions; step size affects transient fidelity.
- Regen-first is a declared controller policy, not proof of an optimal strategy.
- Tyre braking uses a longitudinal `mu*Fz` ceiling and does not consume lateral
  capacity unless a future Work 011/016 coupling supplies that evidence.

## Explicit non-goals

- No conventional wheel-count/layout requirement, detailed linkage geometry,
  hydraulic pressure network, ABS controller, inverter map, battery chemistry,
  or full vehicle stopping-distance claim.
- No integration into the Work 015 race loop or claim of real braking safety.
- No Work 019 implementation and no remote push.

## Validation

```powershell
python -m unittest tests.test_suspension_braking -v
python -m unittest discover -s tests -v
python scripts/validate_suspension_braking.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Every gate runs fail-fast. Completion requires bilingual results, separate
problem reports for encountered issues, explicit staged scope, a successful
commit, and post-commit clean-state/hash evidence.
