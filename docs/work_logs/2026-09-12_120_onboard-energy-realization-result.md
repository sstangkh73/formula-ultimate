# Work 120 Result: Detailed Onboard Energy Realization

Thai companion: `2026-09-12_120_onboard-energy-realization-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 120 realized one synthetic stored-electric/DC route with active storage, enclosure, insulation, connectors, mounts and converter. Geometry/count-derived complete mass is `58.1820224 kg`; nominal active energy is `28.8 MJ`, usable capacity `23.04 MJ`, and registered initial energy `18.432 MJ`.

The nominal `8000 W` case delivered `4.8 MJ` over `600 s`, modeled `257950.13850415577 J` loss, reached `304.93957447302887 K`, and closed the ledger with residual `-7.8580342233181e-10 J`. Work 115 temperature, Work 116 blocked material claim and Work 119 available actuation output `11465 W` were preserved. Empty, rate-limited, thermal-limited, disconnected, omitted-containment, hidden-replenishment and boundary controls passed.

Result SHA-256 is `607140da3cdbb4346fdcbccce030b0e767d54872cc21bccbe966be8f1def3979`; replay is exact. No implementation bug was encountered. Changed: implementation/config/runner/test files, bilingual `ONBOARD_ENERGY_REALIZATION_V1` contract and this bilingual plan/result. Ignored evidence is under `artifacts/work120/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_onboard_energy_realization -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/subsystems/onboard_energy_realization.py scripts/development/run_onboard_energy_realization.py
# exit 0
python scripts/development/run_onboard_energy_realization.py --config config/development/onboard_energy_realization_v1.json --output-root artifacts/work120/run_a
# exit 0; result SHA-256 above
python scripts/development/run_onboard_energy_realization.py --config config/development/onboard_energy_realization_v1.json --output-root artifacts/work120/run_b --replay-reference artifacts/work120/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_coupled_thermal_solid tests.test_material_failure_scope tests.test_realized_actuation_chain tests.test_onboard_energy_realization tests.test_repository_contract -v
# exit 0; 29 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly 10 declared Work 120 files
git diff --cached --check
# exit 0
```

All storage/conversion/thermal properties are synthetic. Chemistry safety, measured capacity/rate/life, alternative routes, aging/faults and physical validation remain unresolved. This is not build or energization authorization. The verified commit hash is reported in the final handoff.
