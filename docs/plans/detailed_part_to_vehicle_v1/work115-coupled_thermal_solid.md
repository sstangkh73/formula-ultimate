# Work 115: Transient thermal and solid coupling

Thai companion: `work115-coupled_thermal_solid.th.md`

Status: Planned

Original Work 106 package: 114

Dependencies: Work 111, Work 113

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Make heat, temperature, deformation and joint preload causally interact on the same detailed geometry.

Work 111 fields, Work 113 joints, shared material regions and explicit thermal properties/source assumptions.

## 2. Proposed files

- `src/formula_ultimate/physics/coupled_thermal_solid.py`
- `config/development/coupled_thermal_solid_v1.json`
- `scripts/development/run_coupled_thermal_solid.py`
- `tests/test_coupled_thermal_solid.py`

## 3. Implementation sequence

1. Derive thermal mesh regions, heat sources and boundary/contact conductances from declared geometry/laws.
2. Solve transient heat balance with actual interface areas and material capacities.
3. Transfer temperatures to expansion/material response and return geometry/contact-dependent changes.
4. Compare coupled, decoupled and reduced models; invalidate reductions outside their envelopes.

## 4. Experiment

- IV: Heat input, cooling boundary, contact state, temperature-dependent properties and coupling step.
- DV: Temperature, heat residual, expansion, preload shift and coupling/reduction error.
- Controls: Same geometry, initial thermal state and energy input; independently specified decoupled control.

## 5. Tests and falsification

Insulated energy rise, equilibrium with no sources, free versus constrained expansion, heat-path removal and interface-area mutation.

## 6. Registration and acceptance

Freeze spatial/time refinement, heat/contact laws, property range and thermal/mechanical error tolerances.

Heat balance and both coupling directions pass registered tests; merely solving independent heat and load fields does not pass.

## 7. Deliverables and handoff

Temperature/deformation histories, interface heat transfers, preload response, convergence and reduced-model bounds.

Feeds Work 116 material limits, Work 117 co-design and Work 121 cooling.

## 8. Risks and non-goals

Unmeasured contact conductance must remain an uncertainty. No validated convection, radiation or fluid claim unless separately implemented and tested.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_coupled_thermal_solid tests.test_repository_contract -v
python scripts/development/run_coupled_thermal_solid.py --config config/development/coupled_thermal_solid_v1.json --output-root artifacts/work115/run_a
python scripts/development/run_coupled_thermal_solid.py --config config/development/coupled_thermal_solid_v1.json --output-root artifacts/work115/run_b --replay-reference artifacts/work115/run_a/result.json
```
