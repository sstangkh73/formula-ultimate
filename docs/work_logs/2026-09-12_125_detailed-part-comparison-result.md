# Work 125 Result: Registered Detailed-Part Comparison

Thai companion: `2026-09-12_125_detailed-part-comparison-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

All four registered arms were optimized over the same four training conditions and evaluated on six disjoint paired holdout conditions. Each arm consumed 10 evaluations. The open-material arm exceeded the best optimized control by `+0.05` at coarse fidelity but fell behind by `-0.01` at fine fidelity; the registered discovery-benefit gate therefore remained false. Removing the claimed active coupling removed exactly `0.05` utility, while the inactive fixed-family appendage was unchanged. Omitted hardware was invalid, holdout leakage was rejected, and both score-independent audit subjects were retained.

The result is a completed negative result, not a failed work item. Work 116 material-survival limitations and Work 124 promotion limits remain active. Result SHA-256 is `7f5889940e6bf6cb5f24523f9443aa73b705b3510b6ba2244c400d6eae4b79a6`; exact replay passed. No implementation bug was encountered.

Changed: implementation, configuration, runner, tests, bilingual `DETAILED_PART_COMPARISON_V1` contract, and this bilingual plan/result. Ignored evidence is under `artifacts/work125/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_detailed_part_comparison -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/experiments/detailed_part_comparison.py tests/test_detailed_part_comparison.py
# exit 0
python scripts/development/run_detailed_part_comparison.py --config config/development/detailed_part_comparison_v1.json --output-root artifacts/work125/run_a
# exit 0; completed_negative_result; result SHA-256 above
python scripts/development/run_detailed_part_comparison.py --config config/development/detailed_part_comparison_v1.json --output-root artifacts/work125/run_b --replay-reference artifacts/work125/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_detailed_connection_contact tests.test_moving_contact_assembly tests.test_coupled_thermal_solid tests.test_material_failure_scope tests.test_multiscale_discovery_search tests.test_detailed_part_comparison tests.test_repository_contract -v
# exit 0; 41 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly 10 declared Work 125 files
git diff --cached --check
# exit 0
```

The response fixtures are synthetic and cannot establish external novelty, measured material survival, manufactured behavior, whole-vehicle benefit or physical validation. Follow-up: Work 126 must close the whole detailed candidate geometry and every essential hardware/function path without relaxing these unresolved-evidence boundaries.
