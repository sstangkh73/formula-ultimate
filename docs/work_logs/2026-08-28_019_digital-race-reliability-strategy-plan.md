# Work 019 Plan: Digital Race Reliability and Strategy

Status: Completed

Thai companion: `2026-08-28_019_digital-race-reliability-strategy-plan.th.md`

## Objective

Implement a deterministic Level-0 multi-lap digital race model that combines
explicit strategy controls, traffic, weather, degradation, onboard-energy
depletion, and seeded reliability failures while retaining the published race
distance of each real circuit as the finish boundary.

## Scope

- Define strict SI contracts for topology-neutral race sectors, per-lap strategy,
  weather and traffic events, vehicle/risk parameters, state, telemetry,
  residuals, replay metadata, and terminal outcome.
- Traverse every declared lap and sector, apply any published-distance residual
  only to the final event, and expose that adjustment in telemetry.
- Keep primary energy onboard and monotonically non-increasing; no refuelling or
  unaccounted replenishment is permitted during the race.
- Make pace, weather, traffic, and accumulated degradation affect sector time,
  energy use, degradation, damage, and reliability hazard through declared
  reduced-order equations.
- Draw one seeded uniform reliability sample per entered event and analytically
  localize exponential failure time within the event.
- Compete finish, reliability, degradation, damage, depletion, and timeout event
  times without clipping invalid states or silently correcting residuals.
- Validate neutral completion on all ten real circuit profiles plus deterministic
  replay, strategy comparisons, weather, traffic, and forced failure modes.
- Add tests, validator, bilingual model/result documentation, queue completion,
  separate bilingual problem reports for issues encountered, and one verified
  commit.

## Planned files

- `src/formula_ultimate/physics/digital_race.py`
- `src/formula_ultimate/physics/__init__.py`
- `tests/test_digital_race.py`
- `scripts/validate_digital_race.py`
- `docs/physics/DIGITAL_RACE_RELIABILITY_STRATEGY_MODEL.md` and `.th.md`
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md` and `.th.md`
- this bilingual plan/result pair
- separate bilingual problem reports for encountered issues

## Model boundary

For an event of distance `d`, start-of-event degradation `g`, base speed `v0`,
pace `p`, weather speed factor `w_v`, and traffic speed factor `q_v`:

```text
v = v0 * p * w_v * q_v * (1 - k_v*g)
t_event = d / v + t_traffic
E_event = d * e0 * p^2 * w_E * q_E + P_aux * t_event
delta_g = d * r_g * p^2 * w_g * q_g
delta_D = d * r_D * p^3 * w_D * q_D
```

The event holds these rates constant. Energy, degradation, and damage are
integrated only through the executed fraction. Their hard limits and the global
timeout are analytically localized.

Reliability uses a constant event hazard rate based on start state and declared
conditions:

```text
lambda = lambda0 * w_R * q_R * p^n *
         (1 + k_g*g + k_D*D)
t_reliability = -ln(1 - u) / lambda,  u ~ Uniform[0, 1)
```

Exactly one `u` is drawn for every entered event from the declared seed. The
draw and candidate time are recorded even when no reliability failure occurs.
This makes uncertainty replayable; it does not establish real-world failure
rates.

## Event semantics

The earliest admissible candidate truncates the current event. A final-sector
completion has first priority on an exact tie, followed by reliability, damage,
degradation, depletion, and timeout. A non-final sector boundary advances the
race only when no terminal candidate occurs at or before it. Final states retain
the localized boundary and all conservation residuals.

## Experiment definition

- Preferred hypothesis: explicit conservative strategy can trade lap time for
  lower energy, degradation, damage, and seeded reliability exposure, while an
  aggressive strategy cannot claim a win unless it finishes the same published
  race distance within all evidence gates.
- Independent variables: circuit, sector map, strategy pace, weather schedule,
  traffic schedule, energy budget, degradation/damage rates and limits,
  reliability hazard parameters, timeout, and random seed.
- Dependent variables: elapsed time, distance, energy, degradation, damage,
  hazard/draw/failure time, terminal outcome, residuals, and replay metadata.
- Controls: identical circuit and sector library, no mid-race primary-energy
  addition, fixed schedules, fixed equations, fixed seed, and deterministic tie
  priority.
- Metrics: finish status/time, exact distance closure, energy residual,
  monotonic energy, limit localization, replay equality, event count, and
  invalid-case coverage.
- Success: all ten neutral real-circuit races finish exactly; repeated seeded
  runs are identical; strategy/weather/traffic effects have the declared
  direction; all forced terminal events localize; full repository gates pass.
- Failure criteria: non-finite or negative declarations, incomplete/duplicate
  schedules, non-positive effective speed, conservation residual outside
  tolerance, energy increase, unlocalized limit crossing, nondeterministic
  replay, or repository gate failure.
- Falsification: force depletion, timeout, degradation, damage, reliability,
  severe weather, traffic delay, official-distance residual, and numerical
  invalidity; none may be reported as a valid finish.

## Risks

- Event-constant speed and rates omit transient vehicle dynamics, tyre state,
  coupled thermal systems, pit-lane operations, driver behavior, and detailed
  multi-agent traffic interaction.
- Weather and reliability multipliers are declared scenarios, not calibrated
  forecasts or empirical failure distributions.
- Linear degradation state and scalar damage compress many physical mechanisms;
  higher-fidelity models must replace them before scientific validation.
- Applying the official-distance residual to the final event preserves the real
  finish target but is a bookkeeping boundary, not a reconstruction of timing
  line geometry.

## Explicit non-goals

- No conventional car layout, tyre count, engine type, body shape, or component
  topology is prescribed.
- No refuelling, external primary-energy transfer, pit repair, tactical opponent
  AI, CFD, multibody dynamics, real weather prediction, or safety certification.
- No claim that Level-0 completion predicts a real race result or physical
  validity, and no remote push.

## Validation

```powershell
python -m unittest tests.test_digital_race -v
python -m unittest discover -s tests -v
python scripts/validate_digital_race.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Every gate runs fail-fast. Completion requires bilingual results, any necessary
problem reports, explicit staged scope, a successful commit, and post-commit
clean-state/hash evidence.
