# Work 124 Result: Multiscale Discovery and Fair Accounting

Thai companion: `2026-09-12_124_multiscale-discovery-search-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 124 implemented reserve-before-execute accounting for matched score-first and representation-balanced policies over the same eight-candidate library, paired seeds, hardware opportunity and partition budgets. Both policies retained unknown count `3`; candidate `c7` was explicitly `not_evaluated_budget_exhausted`. The failed `c4` solver attempt and retry were charged, and score-independent audits covered field and B-rep representations.

Admission SHA-256, dependency-aware cache invalidation, tamper rejection, inactive appendage zero effect and same-topology useful continuous shape all passed. Work 123 continues to block vehicle promotion. Result SHA-256 is `8b2cc7908fc4e33a7ab128d3e0e10bcabc3159304ab09ee8b81f6bda9888a887`; exact decision replay passed. No implementation bug was encountered.

Changed: implementation/config/runner/test files, bilingual `MULTISCALE_DISCOVERY_SEARCH_V1` contract and this bilingual plan/result. Ignored evidence is under `artifacts/work124/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_multiscale_discovery_search -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/search/multiscale_discovery_search.py scripts/development/run_multiscale_discovery_search.py
# exit 0
python scripts/development/run_multiscale_discovery_search.py --config config/development/multiscale_discovery_search_v1.json --output-root artifacts/work124/run_a
# exit 0; result SHA-256 above
python scripts/development/run_multiscale_discovery_search.py --config config/development/multiscale_discovery_search_v1.json --output-root artifacts/work124/run_b --replay-reference artifacts/work124/run_a/result.json
# exit 0; exact decision replay
python -m unittest tests.test_freeform_material_generator tests.test_architecture_part_feedback tests.test_coupled_vehicle_transient tests.test_multiscale_discovery_search tests.test_repository_contract -v
# exit 0; 30 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly 10 declared Work 124 files
git diff --cached --check
# exit 0
```

Candidate outcomes are bounded synthetic fixtures. Accounting/diversity does not establish novelty, discovery, vehicle benefit or physical validation. The verified commit hash is reported in the final handoff.
