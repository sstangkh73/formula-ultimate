# Work 132 Result: Physical Subsystem Correlation

Thai companion: `2026-09-12_132_physical-subsystem-correlation-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Stopped

The offline integrity pipeline rejects missing boundary power, undocumented replacement, calibration leakage, censored aborts and sensor disagreement. Unit fixtures remain software tests only. Physical subsystem work stopped with 7 blockers: valid Work 131 measured applicability, subsystem safety/facility/operator references, frozen configuration, instrument manifest and measured subsystem records are absent. No equipment was operated and no endurance/lifetime claim was made.

Result SHA-256 is `0393b2cf2c3fe295496bbaa357ad928ad8f716b8cb580a48b46f447a68047797`; exact stopped-decision replay passed. No implementation bug was encountered.

```powershell
python -m unittest tests.test_physical_subsystem_correlation -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/experiments/physical_subsystem_correlation.py scripts/development/run_physical_subsystem_correlation.py tests/test_physical_subsystem_correlation.py
# exit 0
python scripts/development/run_physical_subsystem_correlation.py --config config/development/physical_subsystem_correlation_v1.json --output-root artifacts/work132/run_a
# exit 0; stopped; 7 blockers
python scripts/development/run_physical_subsystem_correlation.py --config config/development/physical_subsystem_correlation_v1.json --output-root artifacts/work132/run_b --replay-reference artifacts/work132/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_physical_connection_correlation tests.test_physical_subsystem_correlation tests.test_repository_contract -v
# exit 0; 18 tests passed
```

Resume requires a new authorized measured program after Work 131 is satisfied.
