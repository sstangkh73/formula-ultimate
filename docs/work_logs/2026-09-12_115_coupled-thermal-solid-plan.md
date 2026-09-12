# Work 115 Plan: Coupled Thermal-Solid Response

Thai companion: `2026-09-12_115_coupled-thermal-solid-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Implement a bounded two-region transient thermal network derived from the Work 113 threaded-reference mating geometry and contact patches, then couple its temperatures to thermal expansion, temperature-dependent elastic stiffness, joint preload and preload-dependent contact conductance. Pin the exact Work 111 and Work 113 contracts.

Use explicit synthetic thermal properties and a prescribed boundary conductance. This is not validated convection, radiation or fluid cooling. Compare fully coupled, explicitly decoupled and reduced single-temperature models over three time steps, and invalidate properties/reductions outside their frozen temperature/load ranges.

## Variables, controls and files

- IV: heat input, prescribed boundary conductance, contact state/area, thermal properties and coupling time step.
- DV: regional temperature, interface heat transfer, energy residual, free/constrained expansion, modulus, preload shift, contact conductance and reduced-model error.
- Controls: insulated analytic energy rise, zero-source equilibrium, free versus constrained expansion, removed heat path, interface-area mutation and one-way decoupled response.
- Success: actual contact area is derived from Work 113 geometry parameters, energy and refinement gates pass, temperature changes mechanics and mechanics returns a changed conductance, controls are causal, invalid ranges fail closed and replay is exact.

Planned files: `src/formula_ultimate/physics/coupled_thermal_solid.py`, `config/development/coupled_thermal_solid_v1.json`, `scripts/development/run_coupled_thermal_solid.py`, `tests/test_coupled_thermal_solid.py`, bilingual `docs/contracts/COUPLED_THERMAL_SOLID_V1*`, this bilingual plan/result and ignored `artifacts/work115/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_coupled_thermal_solid tests.test_repository_contract -v
python scripts/development/run_coupled_thermal_solid.py --config config/development/coupled_thermal_solid_v1.json --output-root artifacts/work115/run_a
python scripts/development/run_coupled_thermal_solid.py --config config/development/coupled_thermal_solid_v1.json --output-root artifacts/work115/run_b --replay-reference artifacts/work115/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected regressions and explicit staged/cached diff checks; commit immediately only after every gate passes.

## Risks and non-goals

Lumped regions omit spatial gradients and contact conductance is unmeasured uncertainty. Non-goals: validated convection/radiation/fluid flow, thermal-stress FEA, certified properties, fatigue/loosening, vehicle cooling adequacy, physical validation, push or history rewrite.
