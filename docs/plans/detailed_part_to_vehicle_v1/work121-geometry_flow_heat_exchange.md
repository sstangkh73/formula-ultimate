# Work 121: Geometry-derived flow and heat exchange

Thai companion: `work121-geometry_flow_heat_exchange.th.md`

Status: Planned

Original Work 106 package: 120

Dependencies: Work 110, Work 115, Work 116

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Make internal passages and exposed surfaces causally affect pressure loss, heat transfer and external aerodynamic loads.

Work 110 geometry meshes, Work 115 heat sources and material/data applicability. Internal and external flow require separate validation scopes.

## 2. Proposed files

- `src/formula_ultimate/physics/geometry_flow_heat_exchange.py`
- `config/development/geometry_flow_heat_exchange_v1.json`
- `scripts/development/run_geometry_flow_heat_exchange.py`
- `tests/test_geometry_flow_heat_exchange.py`

## 3. Implementation sequence

1. Separate solid/fluid domains and physical inlet/outlet/wall/far-field boundaries.
2. Verify an internal passage heat/pressure case before using arbitrary cooling geometry.
3. Build an external-flow adapter with independently validated reference cases and declared regime.
4. Return wall heat/pressure/shear loads to the coupled assembly; compare geometry mutations.

## 4. Experiment

- IV: Passage routing, surface shape, flow demand, speed and boundary assumptions.
- DV: Pressure drop, heat rejected, pumping power, aerodynamic forces/moments and error.
- Controls: Same source heat, ambient state, operating conditions and reference task.

## 5. Tests and falsification

Blocked passage, zero-flow/source limits, surface/cavity mutation, domain-size sensitivity and conservation. Include wall/mesh/time refinement where applicable.

## 6. Registration and acceptance

Freeze flow regime, constitutive/closure assumptions, boundary domain, refinement schedule and accepted errors.

Each admitted flow scope passes its own reference/convergence gates; internal-flow success does not establish whole-car aerodynamics.

## 7. Deliverables and handoff

Fluid/solid meshes, fields, heat/pressure loads, power costs and per-regime coverage reports.

Feeds transient coupling Work 123 and vehicle trade-offs Work 127.

## 8. Risks and non-goals

This is two substantial solver scopes: split internal and external implementations if needed. No arbitrary turbulence, cavitation or compressibility claim from one benchmark.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_geometry_flow_heat_exchange tests.test_repository_contract -v
python scripts/development/run_geometry_flow_heat_exchange.py --config config/development/geometry_flow_heat_exchange_v1.json --output-root artifacts/work121/run_a
python scripts/development/run_geometry_flow_heat_exchange.py --config config/development/geometry_flow_heat_exchange_v1.json --output-root artifacts/work121/run_b --replay-reference artifacts/work121/run_a/result.json
```
