# Work 024 Plan: Aerodynamic Chassis and Normal-Load Coupling

Status: Completed

Thai companion: `2026-08-28_024_aero-chassis-load-coupling-plan.th.md`

## Objective

Couple the existing aerodynamic map result into an explicit chassis force/moment
wrench and arbitrary-contact normal-load equilibrium, with cooling evidence and
force/moment residuals retained. Unsupported aerodynamic queries and infeasible
contact loads must invalidate the adapter step.

## Scope

- Define body-axis force/moment and aerodynamic reference-origin contracts.
- Translate map forces/moments to the vehicle centre of mass with `r x F`.
- Generalize the minimum-change normal-load projection to include aerodynamic
  vertical force, pitch moment, and roll moment for arbitrary contact topology.
- Retain vertical/pitch/roll equilibrium residuals without correction.
- Implement `aerodynamic_map` and `normal_load_solver` adapters with exact Work
  021 signal sets and Work 022 fail-closed behavior.
- Prove drag/downforce/cooling signs, centre-of-pressure load shift, three-contact
  support, replay, map-envelope rejection, contact lift, and rank deficiency.
- Add validator, bilingual model/result documentation, queue updates, any bug
  reports, validation, and one commit.

## Planned files

- `src/formula_ultimate/simulation/aero_load_coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_aero_load_coupling.py`
- `scripts/validate_aero_load_coupling.py`
- `docs/simulation/AERO_CHASSIS_LOAD_COUPLING.md` and `.th.md`
- bilingual queue and Work 024 plan/result; problem reports if needed

## Experiment definition

- Hypothesis: an aerodynamic wrench translated about the centre of mass changes
  total/contact normal loads with closed force/moment balances, independent of
  a conventional four-wheel layout.
- Independent variables: map operating point, reference-origin offset, contact
  coordinates, acceleration estimate, and map validity.
- Dependent variables: body wrench, cooling evidence, per-contact loads,
  equilibrium residuals, adapter status, and candidate writes.
- Controls: existing Work 017 map evaluator, SI body axes (`x` forward, `y` left,
  `z` up), immutable Work 016 contact geometry, exact signal contracts.
- Success: analytical symmetric and offset cases close within declared
  tolerance; three-contact layout passes; invalid map/lift/rank cases emit no
  successful coupling output; full repository passes.
- Failure: sign reversal, lost moment translation, hidden clipping, residual
  correction, topology prescription, unsupported query accepted, or commit fail.

## Risks and non-goals

Aerodynamic coefficient sign conventions and reference origin must be explicit.
The Level-0 map is synthetic unless stronger evidence says otherwise. This work
does not resolve tyres, suspension, braking, motion, a whole race, CFD/FEA, or
physical validation; it does not change README or push remote history.

## Validation

```powershell
python -m unittest tests.test_aero_load_coupling -v
python -m unittest discover -s tests -v
python scripts/validate_aero_load_coupling.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```
