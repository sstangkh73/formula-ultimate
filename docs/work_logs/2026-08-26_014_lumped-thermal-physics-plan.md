# Work 014 Plan: Lumped Thermal, Cooling, Derating, and Failure Physics

Status: Completed

Thai companion: `2026-08-26_014_lumped-thermal-physics-plan.th.md`

## Objective

Implement a deterministic lumped-capacitance thermal model that converts
declared heat generation, ambient exchange, and commanded active conductance
into temperature, derating, energy accounting, and an irreversible over-
temperature failure event without silently clipping temperature.

## Scope

- Define strict SI contracts for thermal parameters, state, step input,
  derating, failure state, and telemetry.
- Integrate constant heat generation with Newton cooling exactly over each step.
- Separate passive and active heat exchange energy and expose signed values.
- Apply a linear derating factor from a declared start temperature to zero at
  the failure temperature.
- Locate the first over-temperature crossing analytically, shorten the executed
  interval to that event, latch failure, and expose unexecuted requested time.
- Preserve a per-step energy residual; never silently correct invalid or
  non-finite states.
- Add heating, cooldown, equilibrium, derating, failure-crossing, already-
  failed, invalid-input, conservation, and deterministic-replay tests.
- Add a validator, bilingual model/result documents, queue update, validation,
  and one verified commit before Work 015.

## Planned files

- `src/formula_ultimate/physics/thermal.py`
- `src/formula_ultimate/physics/__init__.py`
- `tests/test_thermal.py`
- `scripts/validate_thermal.py`
- `docs/physics/THERMAL_MODEL.md` and `THERMAL_MODEL.th.md`
- queue status and this bilingual plan/result pair
- a separate bilingual problem report only if a material problem occurs

## Assumptions and equations

The component is one spatially uniform thermal mass with heat capacity `C`
(`J/K`). Ambient temperature and heat generation are constant within a step.
Passive and commanded active cooling are conductances:

```text
G = G_passive + command * G_active
C dT/dt = P_heat - G (T - T_ambient)
```

For `G > 0`:

```text
T_eq = T_ambient + P_heat / G
T(t) = T_eq + (T0 - T_eq) exp(-G t / C)
```

For `G = 0`, `T(t) = T0 + P_heat t / C`. Total exchange energy is derived from
`P_heat*t - C*(T1-T0)` and divided between passive/active conductances. Signed
negative exchange means the ambient heats a colder component.

Derating equals one at or below `T_derate`, decreases linearly, and equals zero
at `T_fail`. Failure is latched and later steps do not resume automatically.

## Experiment definition

- Preferred hypothesis: explicit cooling and failure-event physics prevent an
  agent from using unlimited heat-producing power while keeping energy and
  derating consequences observable.
- Independent variables: heat capacity, passive/active conductance, command,
  heat generation, ambient/initial temperature, thresholds, and duration.
- Dependent variables: end temperature, exchange energies, storage change,
  residual, derating factor, executed time, status, and failure time.
- Controls: SI units, constant inputs per step, exact closed-form integration,
  identical event rule, and no random inputs.
- Metrics: analytical temperature error, energy residual, failure-time error,
  and deterministic equality.
- Success: analytical references match within floating-point tolerance,
  residual remains scaled-small, and event/status behavior is exact.
- Failure/falsification: adiabatic heating and Newton cooldown must match closed
  forms; equilibrium must remain fixed; insufficient cooling must cross and
  latch failure; a failed state must not silently recover; invalid values fail.

## Risks

- A one-node model omits internal gradients and hotspots.
- Conductance inputs are declared parameters, not evidence from CFD or tests.
- Exact integration is exact only for constant within-step inputs.
- Event termination leaves requested time unexecuted; downstream loops must
  treat that as failure, not as successful completion.

## Explicit non-goals

- No spatial mesh, coolant inventory, phase change, radiation, fan/pump energy,
  material aging, fire, thermal contact network, or empirical calibration.
- No claim of physical validation from Level 0.
- No Work 015 implementation and no remote push.

## Validation

```powershell
python -m unittest tests.test_thermal -v
python -m unittest discover -s tests -v
python scripts/validate_thermal.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Every gate runs fail-fast. Completion requires the result pair, explicit staged
scope, successful commit, and post-commit clean-state/hash verification.
