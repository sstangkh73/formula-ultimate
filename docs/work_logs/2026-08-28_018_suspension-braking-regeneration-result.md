# Work 018 Result: Suspension, Mechanical Braking, and Regeneration

Status: Completed

Thai companion: `2026-08-28_018_suspension-braking-regeneration-result.th.md`

## Outcome

Work 018 is complete. `work018-suspension-braking-v1` now evaluates one
topology-neutral ground-contact interval with explicit upstream normal load,
spring/damper travel, tyre-limited regen-first/mechanical braking, recovered-
energy storage and conversion loss, mechanical brake heat, Work 014 thermal
derating, and earliest-event truncation for suspension travel or brake
overtemperature.

The preferred hypothesis is supported inside the model boundary: requested
braking is only applied to the extent supported by contact load, component
torque/power, storage, suspension travel, and thermal survival. Recovered energy
closes exactly against removed wheel work and declared conversion loss; no free
or undeclared primary energy is created.

This is Level-0 software/analytical evidence, not whole-vehicle braking or
safety validation.

## Files changed

- `src/formula_ultimate/physics/suspension_braking.py`: module/state/input
  contracts, suspension motion/events, torque limits/allocation, Work 014 thermal
  coupling, event truncation, regen storage, energy/torque/force residuals, and
  observable invalidity.
- `src/formula_ultimate/physics/__init__.py`: public Work 018 API exports.
- `tests/test_suspension_braking.py`: 13 analytical, limit, failure, replay,
  invalid-contract, and numerical-failure tests.
- `scripts/validate_suspension_braking.py`: suspension, energy, thermal, tyre,
  and replay reference validator.
- `docs/physics/SUSPENSION_BRAKING_REGEN_MODEL.md` and `.th.md`: equations,
  event/energy semantics, evidence, integration boundary, and limitations.
- `docs/problem_reports/2026-08-28_018_tyre-limit-fixture-suspension-failure.md`
  and `.th.md`: coupled-fixture failure, root cause, correction, and rerun.
- queue and this bilingual Work 018 plan/result pair.

## Decisions and evidence

1. The evaluator models one arbitrary contact module and does not prescribe
   wheel count, axle pairing, symmetry, or conventional layout.
2. Normal load is explicit upstream evidence; Work 018 does not redistribute it.
3. Start-of-step spring/damper force produces constant travel acceleration. Both
   travel bounds use analytical outward-crossing localization without clipping.
4. Regen capacity is the minimum of component torque, generator-input power,
   storage charge power, and remaining storage energy over the requested step.
5. Regen is allocated before thermal-derated mechanical torque. One tyre scale
   preserves that blend, while all unsupported torque remains observable.
6. Mechanical wheel work becomes Work 014 brake heat. Regen wheel work becomes
   stored energy plus conversion loss; their independent residual closes zero.
7. The earliest travel/temperature failure truncates motion, heat, and energy
   together. Exact event-time ties return `simultaneous`; prior failures return
   `already_failed` with zero execution.

## Problem encountered and resolved

The first Work 018 run passed 12 tests and failed the tyre-limit reference. The
fixture reduced normal load to `100 N` but retained `1000 N` suspension preload,
so the production model correctly generated rebound acceleration and a travel
failure. The intended independent variable was tyre capacity, not suspension
imbalance. The test and validator now use matched `100 N` preload/load. The
production solver was not weakened. The rerun passed all 13 tests and exposed
`30 N*m` applied, `120 N*m` unserved, with no suspension event.

## Experiment review

- Independent variables: normal load, suspension mass/stiffness/damping/preload/
  travel, wheel speed, brake request, radius/friction, mechanical/regen torque,
  generator/charge power, efficiency, storage, thermal state/parameters,
  cooling, ambient, and interval duration.
- Dependent variables: suspension force/acceleration/travel, event time/mode,
  all torque limits/allocation/scale/unserved torque, wheel/stored/loss/heat
  energy, brake temperature, end state, status, and four residuals.
- Controls: SI/sign conventions, regen-first policy, common tyre scaling,
  start-of-step fixed torque/speed/load, Work 014 solver, earliest-event
  semantics, exact tie classification, and zero random draws.
- Metrics: analytical travel/time error, torque/force/energy residual, storage
  capacity, regen limit values, temperature/failure time, replay equality, and
  invalid coverage.
- Supporting evidence: equilibrium force residual is zero; constant-acceleration
  motion matches analytically; ordinary braking closes `1500 J` into `800 J`
  stored, `200 J` regen loss, and `500 J` heat; exact replay passes.
- Falsifying evidence: travel crosses at `5 s`; brake reaches `400 K` at `50 s`;
  exact travel/thermal tie is simultaneous at `50 s`; tyre limit leaves torque
  unserved; regen torque/power/charge/storage and zero-speed limits all bind;
  prior failure and extreme finite arithmetic cannot silently execute.
- Contradicting evidence: the initial tyre fixture returned suspension failure,
  contradicting the test expectation but correctly revealing coupled input
  imbalance. It is retained in the separate report.
- Alternative explanations: energy closure alone could pass with excessive
  torque, so tyre, component, power, capacity, derating, event, and unserved-
  torque evidence are tested independently.
- Missing evidence: coupled chassis/road/link geometry, combined lateral tyre
  use, wheel/vehicle deceleration, central shared storage allocation, pressure/
  inverter/battery maps, calibrated brake thermal data, and stopping distance.
- Confidence: high for deterministic interval contracts and internal accounting;
  low or none for real braking performance or safety.

## Validation evidence

All commands ran from `C:\Formula Ultimate` with fail-fast handling.

```powershell
python -m unittest tests.test_suspension_braking -v
```

Exit status: `0`; `Ran 13 tests`; `OK`.

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`; `Ran 145 tests`; `OK`.

```powershell
python scripts/validate_suspension_braking.py
```

Exit status: `0`. Relevant output:

```text
ordinary torque regen/mechanical: 100.0 / 50.0 N*m
wheel energy removed: 1500.0 J
stored/loss/heat: 800.0 / 200.0 / 500.0 J
end brake temperature: 300.5 K
force/torque/energy residuals: 0
suspension failure: 5.0 s, travel 0.1 m, unexecuted 5.0 s
thermal failure: 50.0 s, 400.0 K, heat 50000.0 J, unexecuted 50.0 s
tyre limit/scale/applied/unserved: 30.0 N*m / 0.2 / 30.0 / 120.0 N*m
replay_equal: true
```

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` for each. Full validation is rerun after this result; staged
scope/check runs before commit.

## Limitations and follow-up

- Suspension is an independent constant-acceleration contact coordinate, not
  coupled chassis heave/pitch/roll or detailed linkage/road dynamics.
- Wheel speed is fixed inside each interval, so torque does not yet update
  stopping speed/distance.
- Tyre limit is longitudinal only; lateral-force capacity is not consumed.
- Regen storage is per module, not a centrally shared vehicle store.
- The model is not integrated into Work 015 race state or a vehicle controller.
- Work 019 owns reliability, traffic, weather, degradation, and strategy and was
  not started here.
- Commit hash is reported in final handoff; no remote push is performed.
