# Work 121 Result: Geometry-Derived Flow and Heat Exchange

Thai companion: `2026-09-12_121_geometry-flow-heat-exchange-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 121 implemented separately gated internal laminar-passage and external quadratic-drag references. The exact Work 110 mesh SHA-256 was checked; `503` mesh nodes produced extents `[0.08, 0.048, 0.104] m` and projected YZ area `0.004992 m2`. The Work 115 heat source remained `10 W`, and Work 116 material eligibility remained blocked.

The finest 40-segment internal case had Reynolds `891.4465070933691`, pressure drop `3.5411974837946705 Pa`, pumping power `1.7705987418973355e-5 W`, heat-capacity error `0.0003268634672523165`, rejected heat `10 W` and residual `-3.4283687000424834e-13 W`. The finest `2 m` far-field case produced drag `3.027798918144 N`, domain error `0.000256`, and zero force residual. Geometry/control mutations and three-level refinement passed independently.

Result SHA-256 is `6fbd7cd8562a7ec65d201dacaf05140194f144968c68cf9cebb6a5ad47398681`; replay is exact. No implementation bug was encountered. Changed: implementation/config/runner/test files, bilingual `GEOMETRY_FLOW_HEAT_EXCHANGE_V1` contract and this bilingual plan/result. Ignored evidence is under `artifacts/work121/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_geometry_flow_heat_exchange -v
# exit 0; 7 tests passed
python -m py_compile src/formula_ultimate/physics/geometry_flow_heat_exchange.py scripts/development/run_geometry_flow_heat_exchange.py
# exit 0
python scripts/development/run_geometry_flow_heat_exchange.py --config config/development/geometry_flow_heat_exchange_v1.json --output-root artifacts/work121/run_a
# exit 0; result SHA-256 above
python scripts/development/run_geometry_flow_heat_exchange.py --config config/development/geometry_flow_heat_exchange_v1.json --output-root artifacts/work121/run_b --replay-reference artifacts/work121/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_geometry_mesh_bridge tests.test_coupled_thermal_solid tests.test_material_failure_scope tests.test_geometry_flow_heat_exchange tests.test_repository_contract -v
# exit 0; 28 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly 10 declared Work 121 files
git diff --cached --check
# exit 0
```

Both scopes use reduced analytic laws and synthetic properties/closures. Internal success does not validate external flow or whole-car aerodynamics. Turbulence, cavitation, compressibility, conjugate CFD, validated cooling and physical validation remain unresolved. The verified commit hash is reported in the final handoff.
