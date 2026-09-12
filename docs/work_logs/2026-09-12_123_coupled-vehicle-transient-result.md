# Work 123 Result: Coupled Whole-Candidate Transient Harness

Thai companion: `2026-09-12_123_coupled-vehicle-transient-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 123 coupled exact Work 117–122 evidence through an owned-state and signed-exchange schema. The finest `0.005 s` run ended at `33.97591865087971 m`, `9.964358996108553 m/s`, `18416105.011570092 J` stored energy and `299.6451530112513 K`. Maximum step residual was `4.157563182616286e-12 J`; global residual was `-9.645725640439196e-8 J`. Three-level convergence and sign, double-count, event, depletion, validity and decoupling controls passed.

Result SHA-256 is `66abf81b6f49179cb881e70d594e856b5042c4ef0f6fcc0fa813ef2acad2a14c`; replay is exact. Status remains `passed_exploratory_only`, with `promotion_allowed: false` because complete geometry and validated material/ground/aero/structural domains remain unresolved.

## Bug record

- Symptom: pre-run interface review found the runner derived the configured drag coefficient from Work 121 `unbounded_reference_drag_n`, while the harness configuration represented the admitted far-field-corrected `drag_force_n`.
- Root cause: the two neighboring Work 121 fields have the same units but different boundary-domain meaning.
- Fix: derive `work121_drag_coefficient_n_per_m_s2` from admitted finest `drag_force_n / 30^2`.
- Retest: unit tests, run A, exact replay run B and the 51-test affected regression all passed. No further implementation bug was encountered.

Changed: implementation/config/runner/test files, bilingual `COUPLED_VEHICLE_TRANSIENT_V1` contract and this bilingual plan/result. Ignored histories/results are under `artifacts/work123/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_coupled_vehicle_transient -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/simulation/coupled_vehicle_transient.py scripts/development/run_coupled_vehicle_transient.py
# exit 0
python scripts/development/run_coupled_vehicle_transient.py --config config/development/coupled_vehicle_transient_v1.json --output-root artifacts/work123/run_a
# exit 0; result SHA-256 above
python scripts/development/run_coupled_vehicle_transient.py --config config/development/coupled_vehicle_transient_v1.json --output-root artifacts/work123/run_b --replay-reference artifacts/work123/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_architecture_part_feedback tests.test_ground_interaction_tasks tests.test_realized_actuation_chain tests.test_onboard_energy_realization tests.test_geometry_flow_heat_exchange tests.test_control_hardware_realization tests.test_coupled_vehicle_transient tests.test_repository_contract -v
# exit 0; 51 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly 10 declared Work 123 files
git diff --cached --check
# exit 0
```

This reduced short trajectory does not establish a complete vehicle, race completion, readiness or physical validation. The verified commit hash is reported in the final handoff.
