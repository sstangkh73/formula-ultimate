# Work 118 Result: Ground Interaction, Stopping and Direction Control

Thai companion: `2026-09-12_118_ground-interaction-tasks-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 118 implemented architecture-neutral ground-contact ports and a bounded synthetic rigid/dry Coulomb reference. It pinned exact Work 114 and Work 116 evidence, preserved Work 114 load `19196.837823792008 N`, and retained material claim `blocked_no_measured_process-qualified_material`.

The `300 kg`, `20 m/s`, `3000 N` normal-load stopping fixture used coefficient `0.8` and stopped in `2.5 s` over `25.00000000000007 m`, matching the constant-force analytic reference across time steps `0.1`, `0.05` and `0.025 s`. Energy residual and last-two refinement gates passed. Contact placement changed yaw moment from `0` to `960 N*m`; force-circle saturation and zero-friction, lift-off, reverse-motion, disconnection, absent-interaction and unsupported-surface controls behaved causally.

Maximum admitted ground resultant was `960 N` at `contact_alpha`. This is a part-load handoff, not a material-survival claim. Result SHA-256 is `e843d60deda1d892c38331e3f51b6f27479954660acbcfafdf6394956f9d0a85`; replay is exact. No implementation bug was encountered during the admitted runs.

Changed: implementation/config/runner/test files, bilingual `GROUND_INTERACTION_TASKS_V1` contract and this bilingual plan/result. Ignored histories/results are under `artifacts/work118/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_ground_interaction_tasks -v
# exit 0; 7 tests passed
python -m py_compile src/formula_ultimate/simulation/ground_interaction_tasks.py scripts/development/run_ground_interaction_tasks.py
# exit 0
python scripts/development/run_ground_interaction_tasks.py --config config/development/ground_interaction_tasks_v1.json --output-root artifacts/work118/run_a
# exit 0; result SHA-256 above
python scripts/development/run_ground_interaction_tasks.py --config config/development/ground_interaction_tasks_v1.json --output-root artifacts/work118/run_b --replay-reference artifacts/work118/run_a/result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_moving_contact_assembly tests.test_material_failure_scope tests.test_ground_interaction_tasks tests.test_repository_contract -v
# exit 0; 24 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly the 10 declared Work 118 files
git diff --cached --check
# exit 0
```

The coefficient, surface, constant normal loads and rigid contact are synthetic. Tire, soft-soil, non-tire adapters, load transfer, compliant contact, control stability, wear/thermal evolution and physical validation remain unresolved. The verified commit hash is reported in the final handoff.
