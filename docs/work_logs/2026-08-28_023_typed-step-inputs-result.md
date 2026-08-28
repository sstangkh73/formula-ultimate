# Work 023 Result: Typed Circuit and Environment Step Inputs

Status: Completed

Thai companion: `2026-08-28_023_typed-step-inputs-result.th.md`

## Outcome

Work 023 implemented deterministic SI-typed spatial, weather, traffic, and
strategy inputs and a real `input_bridge` adapter. All ten catalog profiles
resolve reproducibly. Because the catalog has no surveyed local corridor,
event-time weather, or traffic scenario, all ten remain explicitly incomplete
and cannot enter later physics as silent neutral values.

An analytical complete fixture resolves ready and emits exactly the four
declared signals. It validates the input contract only.

## Files changed

- `src/formula_ultimate/simulation/step_inputs.py` and simulation exports
- `tests/test_step_inputs.py` (9 focused tests)
- `scripts/validate_step_inputs.py`
- `docs/simulation/TYPED_STEP_INPUTS.md` and `.th.md`
- bilingual queue, plan/result, and fingerprint problem report

## Decisions and evidence

- Missing spatial/weather records carry a reason and forbid numeric defaults.
- Unknown traffic differs from an explicit zero-traffic isolated control.
- Cross-circuit evidence, non-finite/range-invalid SI values, and race-distance
  overflow fail closed.
- Fingerprints pin the complete profile, sources/dates, local evidence, and
  strategy—not only the circuit ID.
- Incomplete adapter result: `invalid`, reason lists spatial/weather/traffic,
  emitted signal count `0`.
- Complete fixture: `ready`, four declared typed signals, fingerprint
  `beaf971760985ac4218b2f4d708a3f1b61fef1af3eae5b591328d74470050d7e`.
- Real physics-ready profiles: `0/10`; no evidence was fabricated.

## Problem and resolution

The first fingerprint pinned only `circuit_id`. The separate problem report
records this. Canonical hashing now includes the complete nested profile and a
regression proves same-ID content changes alter the hash.

## Validation

```powershell
python -m unittest tests.test_step_inputs -v
# exit 0; Ran 9 tests in 0.007s; OK
python -m unittest discover -s tests -v
# exit 0; Ran 186 tests in 1.305s; OK
python scripts/validate_step_inputs.py
# exit 0; ten deterministic incomplete profiles; complete fixture emits 4
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
```

## Review and limitations

Supporting evidence covers deterministic replay, exact missing fields, strict
typing, fingerprint sensitivity, and zero writes on incomplete input. The ready
fixture is an alternative explanation for adapter success: it is analytical,
not real-circuit evidence. Missing evidence remains surveyed local geometry,
event weather, and traffic. Confidence is high for the input contract and
unchanged for vehicle physics.

Work 024 is next: couple aerodynamic force/cooling into chassis force/moment and
normal loads, accepting only ready typed input. No push was performed.
