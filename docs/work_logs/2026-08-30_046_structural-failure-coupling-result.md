# Work 046 Result: Structural Failure Coupling and DNF

Status: Completed

Thai companion: `2026-08-30_046_structural-failure-coupling-result.th.md`

## Outcome

Implemented and validated the bounded deterministic structural failure-coupling policy. The fixture supported `intact -> degraded -> failed`, exact post-failure zero wrench, redundant redistribution, critical `DNF`, event-time refinement, retained energy residuals, race arbitration, exact replay, and fail-closed invalid evidence.

## Files changed

- `config/simulation/structural_failure_coupling_v1.json`
- `src/formula_ultimate/simulation/structural_failure_coupling.py`
- simulation exports, central event typing, and whole-race structural-failure mapping
- `scripts/simulation/run_structural_failure_coupling.py`
- `scripts/run_work046.ps1`
- `tests/test_structural_failure_coupling.py`
- `docs/physics/STRUCTURAL_FAILURE_COUPLING_DNF.md` and `.th.md`
- `docs/simulation/COUPLING_CONTRACT_AND_ARCHITECTURE.md` and `.th.md`
- matching Work 046 bilingual plan/result records

Ignored evidence is under `artifacts/work046/`.

## Decisions and evidence

- Yield degrades; fracture/fatigue fail and force exact six-axis zero wrench.
- Event time was `0.375 s` for `0.5/0.25/0.125 s` timesteps; relative change was `0`.
- Redundant topology remained `running`; the survivor carried `(1000,50,-20,10,5,-3)` in `N` and `N*m` components.
- Critical topology produced `DNF` for every timestep.
- The `12 J` failure ledger produced `8.399999999999999 J` dissipated, `3.6000000000000005 J` released, and residual `8.881784197001252e-16 J`.
- Same-input replay was exact; five malformed/out-of-domain controls failed closed with no candidate state.
- The first focused run rejected only an exact-decimal test expectation for `12*0.7`; the implementation already retained and passed the nonzero floating residual. The test and runner were corrected to use the declared residual tolerance while keeping the failed wrench bitwise zero.

## Exact validation

```powershell
py -3.14 -m unittest tests.test_structural_failure_coupling tests.test_coupling_contracts tests.test_whole_race -q
# exit 0; Ran 24 tests; OK

.\scripts\run_work046.ps1
# exit 0; status=passed; event_time_s=0.375
# redundant_outcome=running; critical_outcome=DNF
# event_time_refinement_relative=0; replay=exact; negative_controls=5
# wrench_residual=8.881784197001252e-16
# energy_residual_j=8.881784197001252e-16

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 319 tests in 28.572s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0
```

Repository-contract checks, staged `git diff --cached --check`, the explicit scoped commit, and clean-tree Work 046 replay are verified after this result exists and reported in the final handoff.

## Limitations and follow-up

This validates coupling policy only. Redistribution is instantaneous; released-energy destination is not modeled; the fixture has one bounded load-path group and exact Work 051 identities. There is no transient fracture, stress-wave, contact/preload/friction, physical joint calibration, post-critical response, impact, or crash evidence. Work 047 may consume the typed contract but must not enlarge these claims.
