# Work 122 Result: Controller, Sensor and Support Hardware

Thai companion: `2026-09-12_122_control-hardware-realization-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 122 realized a synthetic sampled sensor-controller-actuator path with `1.19 kg` counted hardware. Work 119 bounded authority to `200 N*m` below its `200.6375 N*m` evidence, and Work 120 bounded charged supply to `100000 J` below `18.432 MJ` available initial energy.

Common and adapted modes each consumed four tuning evaluations. Adapted best gain `140` produced RMSE `0.44575617787699745`. Dropout, disconnection, exhausted supply, saturation and increased-delay controls were observable; a noncausal parameter preserved the trace SHA and was not useful. Result SHA-256 is `3dad312ce2cc6f044be5df73fbe6323d4cbc4ffb09d6b5dd07cde7dc4a630810`; replay is exact. No implementation bug was encountered.

Changed: implementation/config/runner/test files, bilingual `CONTROL_HARDWARE_REALIZATION_V1` contract and this bilingual plan/result. Ignored evidence is under `artifacts/work122/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_control_hardware_realization -v
# exit 0; 7 tests passed
python -m py_compile src/formula_ultimate/subsystems/control_hardware_realization.py scripts/development/run_control_hardware_realization.py
# exit 0
python scripts/development/run_control_hardware_realization.py --config config/development/control_hardware_realization_v1.json --output-root artifacts/work122/run_a
# exit 0; result SHA-256 above
python scripts/development/run_control_hardware_realization.py --config config/development/control_hardware_realization_v1.json --output-root artifacts/work122/run_b --replay-reference artifacts/work122/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_realized_actuation_chain tests.test_onboard_energy_realization tests.test_control_hardware_realization tests.test_repository_contract -v
# exit 0; 25 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly 10 declared Work 122 files
git diff --cached --check
# exit 0
```

Plant, noise, delay and hardware are synthetic. This does not establish real stability, electronics, EMI/fault safety, certification or physical validation. The verified commit hash is reported in the final handoff.
