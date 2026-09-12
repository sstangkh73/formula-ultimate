# Work 129 Result: Independent Claim Validation

Thai companion: `2026-09-12_129_independent-claim-validation-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 129 reconstructed paired time, energy and margin evidence from the locked Work 128 telemetry through a separately declared code path before comparing the upstream decision. The conservative boundary interpretation reduced the mean time improvement from `0.5 s` to `0.22 s`. The `0.28 s` disagreement exceeded the registered `0.2 s` discrepancy trigger and was classified `explained_model_boundary`; ranking remained positive, but the `1.0 s` superiority threshold was not reached.

Energy, thermal and structural constraints remained positive. A shared-function wrapper was rejected, and the known omitted-boundary injection was detected at `0.28 s`; disabling its correction caused the detector control to fail as intended. Selected superiority claims did not survive and promotion remained false. Result SHA-256 is `082158788a300b5ab7e91b7a4cc038e56314f139f21b5b5361c591aa61471b7c`; exact replay passed. No implementation bug was encountered.

Changed: implementation, configuration, runner, tests, bilingual `INDEPENDENT_CLAIM_VALIDATION_V1` contract, and this bilingual plan/result. Ignored evidence is under `artifacts/work129/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_independent_claim_validation -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/experiments/independent_claim_validation.py scripts/development/run_independent_claim_validation.py tests/test_independent_claim_validation.py
# exit 0
python scripts/development/run_independent_claim_validation.py --config config/development/independent_claim_validation_v1.json --output-root artifacts/work129/run_a
# exit 0; completed_claim_downgrade; result SHA-256 above
python scripts/development/run_independent_claim_validation.py --config config/development/independent_claim_validation_v1.json --output-root artifacts/work129/run_b --replay-reference artifacts/work129/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_detailed_part_comparison tests.test_detailed_vehicle_closure tests.test_optimized_vehicle_controls tests.test_heldout_race_robustness tests.test_independent_claim_validation tests.test_repository_contract -v
# exit 0; 36 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly 10 declared Work 129 files
git diff --cached --check
# exit 0
```

Both analyses share synthetic telemetry, candidate identities and physical assumptions. The independent code path is not institutional independence and cannot replace measured boundary histories or physical tests. Work 130 must carry the downgraded evidence envelope and unresolved assumptions into manufacturing tolerances.
