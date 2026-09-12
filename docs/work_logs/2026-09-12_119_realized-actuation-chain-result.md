# Work 119 Result: Realized Transmission and Actuation Chain

Thai companion: `2026-09-12_119_realized-actuation-chain-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 119 realized one synthetic coaxial rotary reference route with two geometry-defined transfer members, four supports, containment and a coupler. Hardware mass is `7.676329657702542 kg`. An 18-point response map closed input-output-loss accounting and returned maximum output torque `200.6375 N*m`, loss `542.37 W`, output-member diagnostic stress `37845866.54174833 Pa` and radial reaction `1003.1875 N` per support.

Exact Work 114/115/116 identities were checked. The admitted upstream temperature is `299.6262800251348 K`, dynamic contact load is `19196.837823792008 N`, and the material claim remains `blocked_no_measured_process-qualified_material`. Disconnect, lock, reverse, saturation, removed-support and missing-hardware controls passed. Result SHA-256 is `fe9492419f0b52f3cd781bdca8425a13064361eab81a1de304b6e6a48b409089`; replay is exact. No implementation bug was encountered.

Changed: implementation/config/runner/test files, bilingual `REALIZED_ACTUATION_CHAIN_V1` contract and this bilingual plan/result. Ignored evidence is under `artifacts/work119/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_realized_actuation_chain -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/subsystems/realized_actuation_chain.py scripts/development/run_realized_actuation_chain.py
# exit 0
python scripts/development/run_realized_actuation_chain.py --config config/development/realized_actuation_chain_v1.json --output-root artifacts/work119/run_a
# exit 0; result SHA-256 above
python scripts/development/run_realized_actuation_chain.py --config config/development/realized_actuation_chain_v1.json --output-root artifacts/work119/run_b --replay-reference artifacts/work119/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_moving_contact_assembly tests.test_coupled_thermal_solid tests.test_material_failure_scope tests.test_realized_actuation_chain tests.test_repository_contract -v
# exit 0; 29 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly 10 declared Work 119 files
git diff --cached --check
# exit 0
```

Geometry and bookkeeping are deterministic, but losses and properties are synthetic. This does not validate hardware performance, materials, fatigue/wear, a preferred actuation technology or physical behavior. The verified commit hash is reported in the final handoff.
