# Work 015 Plan: Deterministic Full-Race Completion Loop

Status: Completed

Thai companion: `2026-08-26_015_deterministic-race-loop-plan.th.md`

## Objective

Implement a deterministic Level-0 full-race loop that consumes the real race
distance from each Work 008 circuit profile and produces explicit `finished`,
`depleted`, `timeout`, `failed`, or `invalid` outcomes while coupling onboard
energy, longitudinal motion, Work 014 derating/failure, and replay metadata.

## Scope

- Define strict SI contracts for race vehicle, controls, state, step telemetry,
  replay metadata, and terminal outcome.
- Use the circuit profile's published `race_distance_m` as the finish target.
- Use Work 005 longitudinal physics for deterministic motion with start-of-step
  thermal derating applied to commanded tractive force.
- Permit only declared onboard primary energy at race start; never replenish it.
- Account source energy as tractive work plus declared waste heat and auxiliary
  energy. Preserve remaining energy and event residuals.
- Compete finish, energy depletion, thermal failure, and timeout within each
  step; localize finish/depletion deterministically and use Work 014's exact
  thermal failure time.
- Catch runtime numerical failures as an observable `invalid` outcome without
  silently repairing state.
- Preserve deterministic replay metadata including schema/model versions,
  circuit/layout identity, fixed step, and explicit random seed (the current
  loop uses no randomness).
- Test all ten real circuit profiles, every terminal outcome, event ordering,
  onboard-energy monotonicity, derating, invalidity, and exact replay.
- Add validator, bilingual model/result docs, validation, and one verified
  commit. Do not start Work 016.

## Planned files

- `src/formula_ultimate/physics/race.py`
- `src/formula_ultimate/physics/__init__.py`
- `tests/test_race.py`
- `scripts/validate_race.py`
- `docs/physics/RACE_COMPLETION_LOOP.md` and `.th.md`
- queue status and this bilingual plan/result pair
- a separate bilingual problem report only if a material problem occurs

## Physics and energy boundary

Within a race step, applied force is constant and equals commanded force times
the derating factor at the step start. Motion is delegated to the deterministic
longitudinal solver. For traveled distance `delta_x` and executed time `delta_t`:

```text
E_wheel = F_applied * delta_x
E_source = E_wheel + P_waste_heat * delta_t + P_auxiliary * delta_t
E_remaining_next = E_remaining - E_source
```

Declared waste heat is supplied to Work 014 and is charged to the onboard
source. `P_auxiliary` includes any declared cooling/support draw but is not
thermally resolved. Energy recovery and refueling are not implemented.

The circuit is reduced to total race distance and reference air density; it is
not a lap geometry or racing-line simulation.

## Event semantics

Each iteration proposes at most `time_step_s`, truncated at timeout. Candidate
event times are computed for finish, depletion, thermal failure, and timeout.
The earliest event wins. Exact-time ties use deterministic priority:

```text
finished -> failed -> depleted -> timeout
```

Finish and depletion use bounded deterministic bisection over the same motion
solver. Depletion chooses the last non-overspending bound, so energy never goes
negative; its small remaining numerical residual stays observable. Finish
distance overshoot stays observable. A thermal event executes only through its
analytical crossing and leaves the rest unexecuted.

## Experiment definition

- Preferred hypothesis: a candidate that is fast for a short interval is not a
  valid race design unless it completes the full published distance before
  energy, thermal, timeout, or numerical gates terminate it.
- Independent variables: circuit profile, mass/drag/rolling resistance,
  commanded force, onboard energy, heat/auxiliary power, thermal parameters,
  cooling command, time step, timeout, and seed.
- Dependent variables: outcome, total time/distance, speed, remaining/consumed
  energy, temperature/derating, terminal residuals, and telemetry.
- Controls: identical model version, SI/sign conventions, no replenishment,
  fixed solver/event iterations, no stochastic draws, and same event priority.
- Metrics: finish distance residual, depletion residual, thermal event time,
  monotonic energy, replay equality, and outcome counts.
- Success: all five terminal outcomes are independently produced and replayed;
  all ten profiles can complete under a deliberately sufficient reference
  budget; full tests and repository gates pass.
- Falsification: zero force must timeout; insufficient energy must deplete
  without negative energy; excessive heat must fail before the step ends;
  extreme finite runtime values must return invalid; a finished candidate must
  reach the declared distance.

## Risks

- A total-distance point-mass course omits cornering, braking, sector grades,
  traffic, tyre state, and strategy.
- Constant force and heat within a step are reduced-order assumptions.
- Bisection is numerical event localization; residuals and iteration count must
  remain explicit and deterministic.
- Declared heat/auxiliary power is not a calibrated powertrain efficiency map.

## Explicit non-goals

- No lateral/yaw/load-transfer physics, racing line, pit stop, refueling,
  recovery, traffic, weather, degradation, strategy, or real lap-time claim.
- No physical validation or claim that all ten real races are simulated at
  useful fidelity.
- No Work 016 implementation and no remote push.

## Validation

```powershell
python -m unittest tests.test_race -v
python -m unittest discover -s tests -v
python scripts/validate_race.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Every gate runs fail-fast. Completion requires bilingual results, explicit
staged scope, a successful commit, and post-commit clean-state/hash evidence.
