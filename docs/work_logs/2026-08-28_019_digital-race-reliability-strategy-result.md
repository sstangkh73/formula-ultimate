# Work 019 Result: Digital Race Reliability and Strategy

Status: Completed

Thai companion: `2026-08-28_019_digital-race-reliability-strategy-result.th.md`

## Outcome

Work 019 and the Work 010–019 physics queue are complete.
`digital-race-level0-v1` now executes every published lap across explicit
sectors with deterministic per-lap pace controls, event-local weather and
traffic, monotonic onboard primary energy, degradation, damage, seeded
reliability uncertainty, and analytically localized terminal events.

All ten real circuit profiles finish at their exact published race distance in
the neutral reference. Same-seed runs replay exactly. Forced reliability,
damage, degradation, depletion, timeout, and numerical-invalid cases terminate
with distinct observable modes. No energy replenishment occurs.

The preferred hypothesis is conditionally supported within this declared model:
the aggressive reference is faster but consumes more energy and accumulates
more degradation, damage, and hazard. This remains Level-0 selection evidence,
not real lap-time, reliability, safety, or physical validation.

## Files changed

- `src/formula_ultimate/physics/digital_race.py`: strict scenario/vehicle/control
  contracts, multi-lap event loop, published-distance closure, pace/weather/
  traffic effects, energy/degradation/damage rates, seeded exponential hazard,
  event competition, telemetry, residuals, replay, and observable invalidity.
- `src/formula_ultimate/physics/__init__.py`: public Work 019 API exports.
- `tests/test_digital_race.py`: nine grouped tests covering ten circuits,
  strategy/environment effects, seeded uncertainty, all terminal modes,
  conservation, tie priority, replay, invalid contracts, and numerical failure.
- `scripts/validate_digital_race.py`: ten-circuit and falsification validator.
- `docs/physics/DIGITAL_RACE_RELIABILITY_STRATEGY_MODEL.md` and `.th.md`:
  contracts, equations, priority, evidence, interpretation, and limitations.
- `docs/problem_reports/2026-08-28_019_global-energy-residual-scale.md` and
  `.th.md`: scale-aware terminal residual diagnosis and verified correction.
- `docs/problem_reports/2026-08-28_019-lookup-command-path-assumptions.md` and
  `.th.md`: resolved read-only discovery-command path assumptions.
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md` and `.th.md`: Work 019 and the
  sequential queue marked `Completed`.
- this bilingual plan/result pair.

## Decisions and evidence

1. Sectors and commands are abstract and ordered; no conventional vehicle
   layout, energy technology, component topology, or fastener form is required.
2. A strategy supplies exactly one pace command per published lap. Weather and
   traffic are explicit event-keyed overrides; missing keys are neutral and
   duplicate/out-of-range keys are rejected.
3. Ordinary sectors use published lap length and declared fractions. The final
   event consumes exactly the remaining published race distance, while its
   nominal difference remains observable as official-distance adjustment.
4. Pace modifies speed linearly, drive energy/degradation quadratically, and
   damage plus default hazard exposure cubically. All multipliers are declared
   scenario inputs rather than hidden tuning.
5. Source energy consists only of declared drive energy and auxiliary power.
   It decreases monotonically; no refuelling or undeclared primary-energy input
   exists.
6. One seeded uniform draw is consumed and recorded per entered event. A
   constant start-of-event exponential hazard localizes reliability failure.
7. Finish, reliability, damage, degradation, depletion, and timeout compete by
   analytical time. Terminal state integrates only the executed fraction.
8. Every event exposes distance/energy residuals and any sub-tolerance energy
   boundary correction. Larger overspend, non-finite rates, or non-positive
   effective speed invalidates the run.

## Problems encountered and resolved

### Read-only lookup path assumptions

The first discovery probe assumed two Work 015 filenames and used a PowerShell
wildcard as an `rg` path. It failed without changing files. Repository search
found the actual filenames and later probes used explicit paths successfully.
The separate problem report preserves the exact scope and resolution.

### Scale-insensitive terminal energy assertion

The first focused test passed all behavioral cases but nine real-circuit
subtests compared terminal reconciliation around `1e10 J` to zero at seven
decimal places. Observable floating-point residuals were only
`1.9073486328125e-06` to `1.1444091796875e-05 J`, approximately `1e-15`
relative, while every event remained within `1e-8 J`.

Production residuals were not rounded or hidden. The test now keeps the
per-event absolute gate and adds a stringent `2e-15` scale-aware terminal gate.
The rerun passed. The bilingual problem report records failure, impact, fix, and
verification.

## Experiment review

- Independent variables: real circuit, sector coefficients/fractions, per-lap
  pace, weather and traffic schedules, onboard energy/auxiliary power,
  degradation/damage parameters and limits, reliability hazard coefficients,
  timeout, and seed.
- Dependent variables: elapsed time/distance, energy consumed/remaining,
  degradation, damage, hazard/draw/failure time, event/outcome/failure mode,
  residuals, completed laps/events, and replay metadata.
- Controls: identical circuit/sector contracts, fixed schedules and equations,
  one command per lap, no primary-energy addition, fixed seed, and deterministic
  event priority.
- Metrics: exact published-distance finish, time, energy monotonicity and
  residual, degradation/damage, analytical failure time, event/draw count,
  replay equality, and invalid coverage.
- Supporting evidence: all ten references finish exactly; same-seed results are
  identical; aggressive pace is faster but costlier; traffic and wet-weather
  changes follow their declared directions; seeded analytical failure matches.
- Falsifying evidence: forced reliability, damage, degradation, depletion,
  timeout, out-of-range schedules, malformed fractions, non-finite input, and
  non-positive runtime speed cannot be reported as a valid finish.
- Contradicting evidence: the initial exact-style energy assertion failed on
  microjoule terminal round-off, contradicting a literal zero-residual
  expectation. It supports retaining scale-aware raw numerical evidence.
- Alternative explanations: different high-fidelity sector models or calibrated
  failure/weather/traffic inputs may reverse the strategy ordering.
- Missing evidence: coupled Work 011–018 time stepping, surveyed racing line,
  transient tyres/aerodynamics/thermal/storage, component wear/fatigue,
  interacting competitors, pit/flag logic, empirical reliability, and real
  weather.
- Confidence: high for deterministic contracts, event accounting, and replay;
  low or none for real race prediction, calibrated failure risk, safety, or
  physical superiority.

## Validation evidence

All commands ran from `C:\Formula Ultimate` with fail-fast handling.

```powershell
python -m unittest tests.test_digital_race -v
```

Exit status: `0`; `Ran 9 tests`; `OK`.

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`; `Ran 154 tests`; `OK`.

```powershell
python scripts/validate_digital_race.py
```

Exit status: `0`. Relevant evidence:

```text
ten real-circuit outcomes: finished
distance residuals: 0 m
replay_equal: true
energy_monotonic: true
energy_replenishment_events: 0
aggressive/conservative time: 2410.1454516951667 / 3615.1432624331906 s
aggressive/conservative energy: 376016912.72584754 / 168390611.63121662 J
traffic delay delta: 7.499999999999545 s
wet time/energy delta: 3.178249263393809 s / 133480 J
seed 23 failure expected/actual: 2.5884721324944864 s
terminal modes: depleted, degradation, damage, timeout, invalid
```

```powershell
python -m compileall -q src scripts tests
git diff --check
```

Exit status: `0` for each. The complete validation is rerun after this result,
then explicit staging and `git diff --cached --check` run before commit.

## Limitations and follow-up

- Sector rates are reduced-order scenario evidence and are not yet generated by
  a coupled simulation of Work 011–018.
- Traffic, weather, degradation, damage, and reliability are intentionally
  simplified and uncalibrated.
- Strategy controls pace only; no pit service, repair, refuelling, tyre change,
  competitor tactics, flag state, or safety-car logic is modeled.
- Higher-fidelity physics and empirical validation are required before any real
  design, performance, reliability, manufacturability, or safety claim.
- Work 010–019 establishes a complete staged Level-0 physics foundation, not a
  completed Formula Ultimate vehicle or final research conclusion.
- Commit hash is reported in the final handoff; no remote push is performed.
