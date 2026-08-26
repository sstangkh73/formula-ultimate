# Work 014 Result: Lumped Thermal, Cooling, Derating, and Failure Physics

Status: Completed

Thai companion: `2026-08-26_014_lumped-thermal-physics-result.th.md`

## Outcome

Work 014 is complete. The repository now contains an exact constant-input
lumped thermal step with passive/active Newton cooling, linear temperature
derating, analytical first-failure event localization, latched failure, and
observable energy residuals. Temperature is not silently clipped.

The preferred hypothesis is supported inside the declared Level-0 boundary:
insufficient cooling causes a finite failure event and prevents the caller from
using the unexecuted remainder of the requested step as if it succeeded.

## Files changed

- `src/formula_ultimate/physics/thermal.py`: SI input/state contracts, exact
  temperature integration, derating, event localization, failure latch, signed
  passive/active exchange, and energy residual.
- `src/formula_ultimate/physics/__init__.py`: public thermal API exports.
- `tests/test_thermal.py`: 11 analytical, failure, energy, invalid-input,
  numerical-failure, and replay tests.
- `scripts/validate_thermal.py`: heating, cooldown, and failure references.
- `docs/physics/THERMAL_MODEL.md` and `.th.md`: equations, status semantics,
  evidence, boundary, and limitations.
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md` and `.th.md`: Work 014 status.
- this Work 014 plan/result pair in English and Thai.

No separate problem report was required. Numerical overflow, a state already
above threshold, and a previously failed state were declared cases in the plan
and are handled as explicit errors/statuses with tests.

## Decisions and physics evidence

1. The component is one uniform thermal mass with `C` in `J/K`.
2. Passive and commanded active cooling are conductances in `W/K`; active
   command is constrained to `[0,1]`.
3. Constant heat and conductance are integrated with the exact exponential
   solution, or the exact linear adiabatic solution when conductance is zero.
4. Heat rejected is signed and split by conductance fraction. Storage change
   and energy residual remain explicit.
5. Derating is linear from `T_derate` to zero at `T_fail`.
6. A threshold crossing terminates at the analytical event. Assigning the event
   temperature is event localization, not post-step clipping. Requested and
   executed durations remain separate.
7. Failure is irreversible in this model; later steps return `already_failed`.

## Experiment review

- Independent variables: `C`, passive/active conductance, cooling command, heat
  generation, ambient/initial temperature, thresholds, and duration.
- Dependent variables: temperature, rejected/storage energy, residual,
  derating, executed/unexecuted time, status, and failure time.
- Controls: SI units, constant step inputs, exact closed form, identical event
  rule, and no randomness.
- Metrics: temperature/failure-time error and energy residual.
- Supporting evidence: adiabatic `300 -> 301 K`; Newton cooldown equals
  `333.1091497054298 K`; equilibrium remains fixed; active conductance cools
  more and its energy is separately accounted.
- Falsifying evidence: with `C=1000 J/K`, `P=1000 W`, `350 K`, and no cooling,
  failure occurs at exactly `50 s / 400 K`; the remaining `50 s` of a `100 s`
  request is not executed, and a follow-up cannot recover.
- Contradicting evidence: none inside the analytical reference set.
- Alternative explanations: cooldown equality is checked against an
  independently written exponential reference, not against another call to the
  implementation.
- Missing evidence: geometry-driven gradients, calibrated parameters, coolant,
  radiation, auxiliary energy, material aging, and hardware tests.
- Confidence: high for the equations/software inside the constant-input
  one-node boundary; none for real hardware performance or safety.

## Validation evidence

All commands ran from `C:\Formula Ultimate` with fail-fast exit handling.

```powershell
python -m unittest tests.test_thermal -v
```

Exit status: `0`. Relevant output: `Ran 11 tests`; `OK`.

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`. Relevant output: `Ran 100 tests`; `OK`.

```powershell
python scripts/validate_thermal.py
```

Exit status: `0`. Relevant output:

```text
adiabatic end_temperature_k: 301.0
Newton analytical/end_temperature_k: 333.1091497054298
failure status: failed
failure_time_s/executed_duration_s: 50.0
unexecuted_duration_s: 50.0
latched: true
temperature_silently_clipped: false
```

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` for each command. The full fail-fast validation is rerun after
this result is added. `git diff --cached --check` is rerun after explicit
staging and before commit.

## Limitations and follow-up

- One node cannot resolve internal hotspots or thermal contact geometry.
- Inputs are constant during a step and are not calibrated evidence.
- Cooling auxiliary energy is not charged in Work 014.
- No radiation, coolant mass/flow, boiling, aging, or fire model exists.
- Work 015 must propagate derating, latched failure, and unexecuted time into a
  failed race outcome. Work 015 was not started in this work item.
- The verified commit hash is reported in the final handoff; no remote push is
  performed.
