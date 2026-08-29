# Work 038 Result: Nonlinear Imperfect Column

Status: Passed and ready for the required validated commit

Thai companion: `2026-08-30_038_nonlinear-imperfect-column-result.th.md`

## Files changed

- Added the versioned Work 038 config, nonlinear-column analytical contracts, runner, PowerShell launcher, and focused tests.
- Added `NONLINEAR_IMPERFECT_COLUMN_ACCEPTANCE.md` and its Thai companion.
- Updated the shared CalculiX solid-node coordinate format from 17 to 12 significant digits because CalculiX 2.22 rejected long scientific-notation node fields; all prior structural experiments were replayed.
- Generated ignored evidence under `artifacts/work038/`, including exact decks, solver outputs, `.dat`, `.frd`, hashes, failure record from the pilot, and final `experiment_summary.json`.

## Decisions and observed evidence

The admitted study is precritical geometric-nonlinearity only. The matched Work 037 mesh value `Pcr=3776.375 N` is the numerical secant reference; Euler `Pcr=3598.293271 N` remains separately visible. At `0.85 Pcr`, measured amplification was `6.645706` for `e0=0.1 mm` and `6.572374` for `e0=0.2 mm`, versus `6.666667`. Maximum secant error was `1.4144%`, cross-amplitude spread `1.1096%`, and reaction error `2.6481e-7`.

The perfect-control threshold was changed from the exploratory `1e-8 m` to `2e-6 m` after the first pilot exposed tetrahedral mesh-asymmetry drift of `1.11569e-6 m`. After the coordinate-format correction and pinned replay, drift was `4.26212e-7 m`. This calibration is disclosed; the result is not represented as independently confirmatory. The geometrically linear negative control missed secant amplification by `72.27%`.

## Validation

All commands exited `0` unless the explicitly recorded pilot falsification is described above.

```powershell
py -3.14 -m unittest tests.test_nonlinear_imperfect_column -v
& .\scripts\run_work038.ps1
py -3.14 -m unittest discover -s tests -v
py -3.14 -m compileall -q src scripts
& .\scripts\run_work034.ps1
& .\scripts\run_work035.ps1
& .\scripts\run_work036.ps1
& .\scripts\run_work037.ps1
```

Focused tests: `4/4` passed. Full suite: `290/290` passed in `25.685 s`. Work 034 tension, Work 035 bending, Work 036 torsion, and Work 037 eigenvalue buckling all replayed with `status=passed`. Work 037 retained medium `Pcr=3776.375 N`, fine `Pcr=3715.160 N`, and last-two change `1.6477%`.

## Limitations and follow-up

No nonlinear mesh-convergence matrix, independent imperfection shape, limit-point continuation, plasticity, collapse, fracture, fatigue, safety factor, or DNF coupling was tested. The next structural study should vary mesh and imperfection shape before evaluating an arc-length or otherwise validated post-buckling route. Commit identity is reported in the final handoff after the required explicit staged-scope checks and commit succeed.
