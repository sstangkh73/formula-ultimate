# Work 127 Result: Optimized Vehicle Controls

Thai companion: `2026-09-12_127_optimized-vehicle-controls-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

The fixed-topology, reference, random-control and open-candidate arms each received four vehicle-search and four controller-tuning evaluations over the same paired conditions and `1,000,000 J` source energy. Every arm was optimized, evaluated with the common controller, then retuned with matched opportunity. Installed base, cooling, containment and support mass, energy use and manufacturing penalty were included.

After complete transferred burdens, the open candidate's paired effect against the best optimized control was `-0.003`; the registered meaningful system effect was `+0.02`. The system-benefit gate and promotion therefore remained false. Untuned baseline, free controller effort, omitted cooling mass and unequal source energy controls were rejected. Result SHA-256 is `d19548b5d45cfcd382ff248aa554e7c96c3043d201d02ee11398d95dd0366f1a`; exact replay passed. No implementation bug was encountered.

Changed: implementation, configuration, runner, tests, bilingual `OPTIMIZED_VEHICLE_CONTROLS_V1` contract, and this bilingual plan/result. Ignored evidence is under `artifacts/work127/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_optimized_vehicle_controls -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/experiments/optimized_vehicle_controls.py scripts/development/run_optimized_vehicle_controls.py tests/test_optimized_vehicle_controls.py
# exit 0
python scripts/development/run_optimized_vehicle_controls.py --config config/development/optimized_vehicle_controls_v1.json --output-root artifacts/work127/run_a
# exit 0; completed_negative_result; result SHA-256 above
python scripts/development/run_optimized_vehicle_controls.py --config config/development/optimized_vehicle_controls_v1.json --output-root artifacts/work127/run_b --replay-reference artifacts/work127/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_coupled_vehicle_transient tests.test_multiscale_discovery_search tests.test_detailed_vehicle_closure tests.test_optimized_vehicle_controls tests.test_repository_contract -v
# exit 0; 30 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly 10 declared Work 127 files
git diff --cached --check
# exit 0
```

The scores and burden weights are deterministic synthetic fixtures. They do not establish held-out race performance, manufacturing behavior, physical reliability, external novelty or vehicle superiority. Work 128 must evaluate the frozen finalists on its separately held-out race without changing this negative result or its threshold.
