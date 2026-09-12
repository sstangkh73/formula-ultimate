# Work 117 Result: Bidirectional Architecture-Part Feedback

Thai companion: `2026-09-12_117_architecture-part-feedback-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 117 implemented a deterministic feedback/regeneration loop while preserving the immutable external-task identity `203629bd848528f5a488f8564cf51d311f659a1af8d0bc81b31b2c13ed3120da`. The loop consumed exact Work 112, Work 114 and Work 115 result identities and derived assembly conditions of `19196.837823792008 N`, `10 W` and `7.099179394127206e-6 m`.

Feedback revised the internal task, regenerated geometry and emitted two explicit stale-evidence invalidations. Its frozen control retained the original task. Both modes used three evaluations, identical coefficients and seeds. Multifunctional-cell merging produced `0.0081 kg` rather than the duplicate-counted `0.0108 kg`; a missing coefficient failed closed. The generated mass changed from `0.005238 kg` to `0.010573618273344638 kg`, a contradicting result retained because improvement was not an admission gate.

Result SHA-256 is `0d85d649eb8976e29bb08e6cb5815b06fba27b25428a8d3f5195281a52b004f1`; replay is exact. `measured_material` and `ground_interaction` remain unresolved and every candidate reports incomplete feasibility. No implementation bug was encountered during the admitted runs.

Changed: implementation/config/runner/test files, bilingual `ARCHITECTURE_PART_FEEDBACK_V1` contract and this bilingual plan/result. Ignored evidence is under `artifacts/work117/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_architecture_part_feedback -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/experiments/architecture_part_feedback.py scripts/development/run_architecture_part_feedback.py
# exit 0
python scripts/development/run_architecture_part_feedback.py --config config/development/architecture_part_feedback_v1.json --output-root artifacts/work117/run_a
# exit 0; result SHA-256 above
python scripts/development/run_architecture_part_feedback.py --config config/development/architecture_part_feedback_v1.json --output-root artifacts/work117/run_b --replay-reference artifacts/work117/run_a/result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_physical_interface_graph tests.test_moving_contact_assembly tests.test_coupled_thermal_solid tests.test_architecture_part_feedback tests.test_repository_contract -v
# exit 0; 30 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly the 10 declared Work 117 files
git diff --cached --check
# exit 0
```

The bounded generator and reduced evaluators do not establish general topology optimization, material validity, ground interaction, full-vehicle feasibility or physical validation. The verified commit hash is reported in the final handoff.
