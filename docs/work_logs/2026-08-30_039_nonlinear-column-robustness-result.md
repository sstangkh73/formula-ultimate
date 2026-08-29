# Work 039 Result: Nonlinear Column Robustness

Status: Completed; execution passed and both preferred hypotheses were rejected

Thai companion: `2026-08-30_039_nonlinear-column-robustness-result.th.md`

## Files changed

- Added the Work 039 versioned config, runner, PowerShell launcher, bilingual physics report, plan/result logs, and ignored solver artifacts.
- Extended the nonlinear-column contract with the declared `smoothstep_cubic` imperfection and fail-closed shape dispatch.
- Extended focused unit coverage for the independent shape and unknown-shape rejection.

## Decisions and evidence

Execution acceptance and hypothesis outcomes are separate. All 18 C3D4 `NLGEOM` cases completed with monotonic response and maximum reaction error `1.749e-16`, so the evidence-generating experiment passed. The fixed absolute-load schedule exposed medium-to-fine eigenmode changes of `1.548%`, `3.639%`, and `8.653%`; the final value exceeds the declared `5%` convergence limit. Fine-mesh shape differences were `7.523%`, `10.980%`, and `13.697%`, exceeding the `10%` robustness limit at the last two loads. Both preferred hypotheses were rejected and no tolerance was changed after observing these results.

## Validation

The initial launcher attempt exited `1` before solver execution because the repository root was absent from the runner import path. The path was fixed, focused tests were replayed, and no physical result from that attempt was admitted. Final commands exited `0`:

```powershell
py -3.14 -m unittest tests.test_nonlinear_imperfect_column -v
& .\scripts\run_work039.ps1
& .\scripts\run_work038.ps1
py -3.14 -m unittest discover -s tests -v
py -3.14 -m compileall -q src scripts
```

Focused tests passed `5/5`. Work 039 produced `18/18` complete cases. Work 038 regression returned `status=passed`. The full suite passed `291/291` in `23.895 s`; compileall exited `0`.

## Limitations and follow-up

The current three-mesh C3D4 series is insufficient at the highest load, and equal tip amplitude does not make different imperfection shapes equivalent. No post-buckling promotion is allowed. The next work item should add sub-`1.0 mm` refinement and a higher-order element comparison at fixed absolute loads. Commit identity will be reported in the final handoff after explicit staged-scope validation and commit.
