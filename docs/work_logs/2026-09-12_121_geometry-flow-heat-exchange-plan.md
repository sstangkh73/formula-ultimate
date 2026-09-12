# Work 121 Plan: Geometry-Derived Flow and Heat Exchange

Thai companion: `2026-09-12_121_geometry-flow-heat-exchange-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Implement separately gated internal-flow/heat and external-flow load references pinned to the exact Work 110 hollow B-rep mesh, Work 115 heat source and Work 116 applicability boundary. Make registered passage diameter/length and mesh-derived external projected bounds causally change pressure, heat-transfer capacity, pumping power and aerodynamic loads.

Verify a laminar circular-passage reference with Hagen-Poiseuille pressure drop and fully developed constant-wall-temperature heat transfer. Verify a separate incompressible subsonic quadratic-drag adapter with declared synthetic coefficients and far-field domain sensitivity. Return pressure/heat/drag loads without promoting either scope to whole-car aerodynamics.

## Variables, controls and files

- IV: passage diameter/length, segment refinement, flow/source, mesh projected geometry, external speed, surface/cavity mutation and far-field size.
- DV: pressure drop, outlet temperature, heat rejected/capacity, pumping power, drag/pressure/shear loads, moment and reference error.
- Controls: same source/ambient/task; blocked passage, zero flow/source, diameter and projected-area mutation, far-field sensitivity and conservation.
- Success: internal and external scopes independently pass analytic/refinement/conservation gates; geometry mutations are causal; exact replay passes.

Planned files: `src/formula_ultimate/physics/geometry_flow_heat_exchange.py`, `config/development/geometry_flow_heat_exchange_v1.json`, `scripts/development/run_geometry_flow_heat_exchange.py`, `tests/test_geometry_flow_heat_exchange.py`, bilingual `docs/contracts/GEOMETRY_FLOW_HEAT_EXCHANGE_V1*`, this bilingual plan/result and ignored `artifacts/work121/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_geometry_flow_heat_exchange tests.test_repository_contract -v
python scripts/development/run_geometry_flow_heat_exchange.py --config config/development/geometry_flow_heat_exchange_v1.json --output-root artifacts/work121/run_a
python scripts/development/run_geometry_flow_heat_exchange.py --config config/development/geometry_flow_heat_exchange_v1.json --output-root artifacts/work121/run_b --replay-reference artifacts/work121/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected Work 110/115/116 regressions and explicit staged/cached diff checks; commit immediately only after every gate passes.

## Risks and non-goals

Both adapters are bounded analytic/reduced references with synthetic properties. Non-goals: arbitrary cooling geometry, turbulence, cavitation, compressibility, conjugate 3D CFD, whole-car aerodynamics, validated cooling, physical validation, push or history rewrite.
