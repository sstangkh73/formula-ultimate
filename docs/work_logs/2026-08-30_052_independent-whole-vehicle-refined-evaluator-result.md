# Work 052 Result: Independent Whole-Vehicle Refined Evaluator

Status: Stopped

Thai companion: `2026-08-30_052_independent-whole-vehicle-refined-evaluator-result.th.md`

## Outcome

The preregistered `1/2/4` B31 protocol was falsified at the analytical benchmark and was not admitted. CalculiX `*EL PRINT` reports expanded-element integration-point stress, while the analytical and project-frame values are extreme-fiber root stress. At four subdivisions, CalculiX displacement error was `1.734%`, but the printed integration-point stress error was `49.56%`; these are not equivalent measurement locations. No candidate result or readiness decision was produced from this failed protocol.

## Files and evidence

- The stopped bilingual plan and this result are the only Work 052 files committed by this work item.
- Uncommitted prototype evaluator files were intentionally excluded from this stopped-work commit and may be revised only under a new preregistered work item.
- Ignored failed-run evidence remains under `artifacts/work052/`, including fresh `.inp`, `.dat`, `.frd`, process evidence, and `experiment_failure.json`.

## Exact validation and exit status

```powershell
py -3.14 -m unittest tests.test_vehicle_frame_refinement -q
# exit 0; Ran 4 tests; OK

powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work052.ps1
# exit 1; stage=benchmark
# message="fine cantilever analytical benchmark gate failed"
```

The original runs using `*EL PRINT` gave CalculiX displacement errors of approximately `24.97%`, `6.84%`, and `1.734%`, and printed-stress errors of approximately `71.1%`, `56.86%`, and `49.56%` at `1/2/4` subdivisions. A diagnostic output change to `*EL FILE,SECTION FORCES` confirmed that the reported six-component field contains beam section resultants at the original beam nodes; this diagnostic was not admitted as a Work 052 result.

## Decision and limitation

Work 052 cannot close `independent_refined_evaluation`. Changing the mesh series or substituting section-resultant-derived stress after seeing the failed result would violate the declared experiment. A successor must preregister the corrected observable, derive surface stress from section force/moment and section properties, retain external displacement corroboration, and rerun from the analytical benchmark.
