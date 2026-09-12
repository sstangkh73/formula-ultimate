# Work 116 Result: Material Provenance and Scoped Failure

Thai companion: `2026-09-12_116_material-failure-scope-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 116 implemented provenance/range/process eligibility gates plus bounded first-yield and Euler-column references. It consumed exact Work 111 p90 stress `8631.834378747026 Pa`, Work 114 maximum dynamic contact force `19196.837823792008 N`, and Work 115 male temperature `299.6262800251348 K` after checking their result identities.

Result SHA-256 is `ea418059c16fdddc6f7205b0d13b35b2d0623a17e9a930d474c9133137e708aa`; replay is exact. Safe/failed yield and buckling fixtures passed, while increasing imperfection reduced capacity. Temperature/rate/process/relabel/mixture controls were rejected. The candidate numerical margin remains diagnostic and its claim is `blocked_no_measured_process-qualified_material`. Fatigue, fracture and wear remain unresolved blockers.

Changed: proposed implementation/config/runner/test files, bilingual `MATERIAL_FAILURE_SCOPE_V1` contract and this bilingual plan/result. Ignored evidence is under `artifacts/work116/run_a|run_b`. No implementation bug was encountered during the admitted runs.

## Validation and limitations

```powershell
python -m unittest tests.test_material_failure_scope -v
# exit 0; 5 tests passed
python -m py_compile src/formula_ultimate/structural/material_failure_scope.py scripts/development/run_material_failure_scope.py
# exit 0
python scripts/development/run_material_failure_scope.py --config config/development/material_failure_scope_v1.json --output-root artifacts/work116/run_a
# exit 0; result SHA-256 above
python scripts/development/run_material_failure_scope.py --config config/development/material_failure_scope_v1.json --output-root artifacts/work116/run_b --replay-reference artifacts/work116/run_a/result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_vector_solid_fields tests.test_moving_contact_assembly tests.test_coupled_thermal_solid tests.test_material_failure_scope tests.test_repository_contract -v
# exit 0; 28 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly the 10 declared Work 116 files
git diff --cached --check
# exit 0
```

Analytic references and synthetic margins do not establish physical survival. The verified commit hash is reported in the final handoff.
