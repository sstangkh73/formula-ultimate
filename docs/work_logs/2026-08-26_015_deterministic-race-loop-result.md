# Work 015 Result: Deterministic Full-Race Completion Loop

Status: Completed

Thai companion: `2026-08-26_015_deterministic-race-loop-result.th.md`

## Outcome

Work 015 is complete. A deterministic Level-0 loop now runs a candidate against
each circuit profile's published race distance and terminates with exactly one
observable outcome: `finished`, `depleted`, `timeout`, `failed`, or `invalid`.
Onboard energy is declared before the race and is never replenished.

The preferred hypothesis is supported: short-interval speed alone cannot pass
the gate. Deliberate insufficient-energy, zero-force, overheating, and numerical
failure references terminate before finish, while a deliberately sufficient
reference completes and exactly replays on all ten profiles.

The ten-circuit fixture times (`228–248 s`) are reduced-order software evidence,
not real lap/race predictions or physical validation.

## Files changed

- `src/formula_ultimate/physics/race.py`: race contracts, replay metadata,
  coupled motion/energy/thermal loop, event localization/priority, terminal
  outcomes, numerical invalidity, and telemetry.
- `src/formula_ultimate/physics/__init__.py`: public race API exports.
- `tests/test_race.py`: 10 outcome, ten-circuit, replay, energy, derating,
  event-tie, invalid-contract, and numerical-failure tests.
- `scripts/validate_race.py`: all-ten finish replay and terminal references.
- `docs/physics/RACE_COMPLETION_LOOP.md` and `.th.md`: model, evidence,
  event/energy semantics, and limitations.
- `docs/problem_reports/2026-08-26_015_event-tie-energy-overspend.md` and
  `.th.md`: separate problem, root cause, fix, and verification.
- queue and this bilingual Work 015 plan/result pair.

## Decisions and evidence

1. Target distance is the sourced `CircuitProfile.race_distance_m`.
2. Motion uses the existing deterministic longitudinal solver and reference air
   density. Applied force is commanded force times start-of-step derating.
3. Source energy equals wheel work plus declared waste heat and auxiliary draw.
   Remaining energy never increases and no recovery/refueling API exists.
4. Finish/depletion are localized with 64 fixed bisection iterations by
   default; Work 014 supplies the analytical thermal failure time.
5. Earliest event wins; exact-time priority is finish, failure, depletion,
   timeout. Requested and executed time remain distinct.
6. Runtime numerical failures become `invalid` with their reason; they are not
   silently corrected.
7. Replay metadata records versions, identities, controls, seed, iterations,
   tolerances, and zero stochastic draws.

## Problem encountered and resolved

The planned exact event-tie falsification initially failed: analytical finish,
depletion, and timeout at `10 s` returned `invalid` because adjacent bisection
bounds overspent `0.000244140625 J` on a `1354976035920.0 J` scale.

The fix adds declared scaled energy-event tolerance and preserves the raw signed
boundary residual. Within tolerance, the higher-priority finish/failure uses
zero remaining energy while retaining the residual; beyond tolerance remains
invalid. The exact tie now returns `finished`, `0 J` remaining, and
`-0.000244140625 J`; zero tolerance returns `invalid`. No replenishment occurs.

## Experiment review

- Independent variables: circuit, vehicle/motion parameters, force, onboard
  energy, heat/auxiliary power, thermal settings, cooling, step, timeout, seed.
- Dependent variables: outcome, time, distance/speed, energy, temperature,
  derating, terminal/event residuals, and telemetry.
- Controls: SI, fixed models/iterations/priority, no replenishment, zero random
  draws, identical replay metadata.
- Metrics: outcome coverage, distance/depletion residual, thermal time, energy
  monotonicity, accounting residual, and exact replay.
- Supporting evidence: all ten profiles return `finished` twice with exact
  equality and zero finish residual; energy, timeout, failure, and invalid
  references return their declared outcomes.
- Falsifying evidence: `1000 J` depletes without negative energy; zero force
  times out at `5 s`; thermal case fails at `50 s/400 K`; non-finite thermal
  equilibrium returns invalid; zero-tolerance event overspend returns invalid.
- Contradicting evidence: the first exact-tie implementation failed and is
  retained in the problem report; the resolved implementation passes.
- Alternative explanations: terminal cases use separate parameter changes and
  assert state/residual evidence, not only outcome strings.
- Missing evidence: track geometry/dynamics, braking, tyres in loop, calibrated
  efficiency/heat, traffic, weather, degradation, and control strategy.
- Confidence: high for declared software/event semantics; low/none for actual
  race time or real vehicle feasibility.

## Validation evidence

All commands ran from `C:\Formula Ultimate` with fail-fast handling.

```powershell
python -m unittest tests.test_race -v
```

Exit status: `0`; `Ran 10 tests`; `OK`.

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`; `Ran 110 tests`; `OK`.

```powershell
python scripts/validate_race.py
```

Exit status: `0`. Relevant output:

```text
ten circuit outcomes: finished
replay_equal: true
energy_replenishment_events: 0
depleted remaining_energy_j: 2.2737367544323206e-13
timeout time_s: 5.0
failed time_s/temperature_k: 50.0 / 400.0
invalid: thermal equilibrium is non-finite
exact tie: finished, remaining 0.0 J, residual -0.000244140625 J
```

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` for each. Full validation is rerun after this result; staged
scope/check runs before commit.

## Limitations and follow-up

- Circuit is total distance plus reference density, not a traversed 3D layout.
- No lateral, braking, tyre, traffic, weather, recovery, pit, or strategy loop.
- Declared force/heat/auxiliary power are not calibrated powertrain maps.
- A Level-0 `finished` result is not physical validation.
- Work 016 will add lateral/yaw/load transfer and was not started here.
- Commit hash is reported in final handoff; no remote push is performed.
