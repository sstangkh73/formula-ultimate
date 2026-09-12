# Work 128 Result: Held-Out Race Robustness

Thai companion: `2026-09-12_128_heldout-race-robustness-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 128 sealed the fixed/open finalist, evaluator, rules and six unseen condition identities before executing all 12 registered trajectories. Both finalists completed every synthetic race within the `520000 J` energy cap and positive thermal/structural margins. The open finalist improved paired race time by `0.5 s`; after `0.1 s` numerical uncertainty this did not meet the preregistered `1.0 s` meaningful-improvement gate. Robust superiority and promotion remained false.

Controls rejected training/holdout reuse, changed source identity, hidden incomplete telemetry and post-exposure tuning. Result SHA-256 is `7ef6c7951abf5dbd3fd96941a10f8775164221ba82b9aceb6d349ac69630bcaa`; exact replay passed. No implementation bug was encountered.

Changed: implementation, configuration, runner, tests, bilingual `HELDOUT_RACE_ROBUSTNESS_V1` contract, and this bilingual plan/result. Ignored evidence is under `artifacts/work128/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_heldout_race_robustness -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/experiments/heldout_race_robustness.py scripts/development/run_heldout_race_robustness.py tests/test_heldout_race_robustness.py
# exit 0
python scripts/development/run_heldout_race_robustness.py --config config/development/heldout_race_robustness_v1.json --output-root artifacts/work128/run_a
# exit 0; completed_negative_result; result SHA-256 above
python scripts/development/run_heldout_race_robustness.py --config config/development/heldout_race_robustness_v1.json --output-root artifacts/work128/run_b --replay-reference artifacts/work128/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_optimized_vehicle_controls tests.test_heldout_race_robustness tests.test_repository_contract -v
# exit 0; 18 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly 10 declared Work 128 files
git diff --cached --check
# exit 0
```

The race/evaluator is synthetic, paired condition effects are deliberately bounded, and numerical completion cannot establish manufactured performance, physical robustness or novelty. Work 129 must independently reproduce the decision from locked artifacts rather than accepting this summary.
