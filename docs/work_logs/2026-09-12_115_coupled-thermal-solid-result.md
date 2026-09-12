# Work 115 Result: Coupled Thermal-Solid Response

Thai companion: `2026-09-12_115_coupled-thermal-solid-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 115 implemented two-way transient coupling on two detailed joint regions. Work 113 result identity, STEP hashes, volumes and helix-derived contact area were rechecked before solving. Heat changed temperatures, expansion, modulus and preload; the changed preload returned a changed contact conductance. The decoupled control produced an observable difference and therefore could not substitute for the coupled run.

Result SHA-256 is `764f1c22774b3c3321cea384053ba079f8671b587fe1059d12b8910d51bcc5fa`; replay is exact. At `0.005 s`, male/female temperatures were `299.6262800251348/296.18422109463023 K`, preload `4027.010508986209 N`, and contact conductance `2.422791168670161 W/K`. The coupled/decoupled return change was `0.008846767995635219`. Reduced temperature-rise error was `0.026501053417395667`.

Across `0.02/0.01/0.005 s`, energy residuals were `4.405364961712621e-15`, `8.057554623519536e-14`, `1.0544454198679887e-13`. All last-two changes were below `1.45e-6`. The insulated male ended at `314.1379777108881 K` versus analytic `314.1379777108996 K`, absolute error `1.1482370609883219e-11 K`. Zero-source equilibrium, free/constrained expansion, removed heat path, doubled area and property-range rejection passed.

Changed: proposed implementation/config/runner/test files, bilingual `COUPLED_THERMAL_SOLID_V1` contract and this bilingual plan/result. Ignored histories are under `artifacts/work115/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_coupled_thermal_solid -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/physics/coupled_thermal_solid.py scripts/development/run_coupled_thermal_solid.py
# exit 0
python scripts/development/run_coupled_thermal_solid.py --config config/development/coupled_thermal_solid_v1.json --output-root artifacts/work115/run_a
# exit 0; result SHA-256 above
python scripts/development/run_coupled_thermal_solid.py --config config/development/coupled_thermal_solid_v1.json --output-root artifacts/work115/run_b --replay-reference artifacts/work115/run_a/result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_vector_solid_fields tests.test_detailed_connection_contact tests.test_coupled_thermal_solid tests.test_repository_contract -v
# exit 0; 23 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly the 10 declared Work 115 files
git diff --cached --check
# exit 0
```

Thermal properties and conductances are synthetic, regions are lumped, and no spatial thermal stress, validated convection/radiation/fluid flow, fatigue, cooling adequacy or physical-validation claim is made. The verified commit hash is reported in the final handoff.
