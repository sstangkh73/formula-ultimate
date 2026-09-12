# Work 120 Plan: Detailed Onboard Energy Realization

Thai companion: `2026-09-12_120_onboard-energy-realization-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Close one disclosed synthetic stored-electric/DC conversion reference route, pinned to Work 115 thermal evidence, Work 116 material scope and Work 119 realized actuation ports. Represent active storage volume, enclosure, insulation, connectors and mounts; derive complete mass and usable initial energy from registered geometry/properties.

Track stored-energy decrease, delivered output, conversion/conductor losses and temperature rise with no external replenishment. Enforce capacity, power-rate and temperature applicability while keeping unsupported chemistry/field/conversion routes open through explicit blocked extension slots.

## Variables, controls and files

- IV: active volume/allocation, initial state fraction, requested rate/duration, ambient/initial temperature, converter connection and containment coverage.
- DV: usable energy, delivered power/energy, stored-energy change, loss/heat, final temperature, complete mass and limiting state.
- Controls: same energy opportunity; empty storage, excessive demand, disconnected converter, omitted containment, hidden replenishment and unit/boundary inconsistency.
- Success: energy residual closes, mass includes every registered hardware class, limits are causal, unsupported physics remains blocked and exact replay passes.

Planned files: `src/formula_ultimate/subsystems/onboard_energy_realization.py`, `config/development/onboard_energy_realization_v1.json`, `scripts/development/run_onboard_energy_realization.py`, `tests/test_onboard_energy_realization.py`, bilingual `docs/contracts/ONBOARD_ENERGY_REALIZATION_V1*`, this bilingual plan/result and ignored `artifacts/work120/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_onboard_energy_realization tests.test_repository_contract -v
python scripts/development/run_onboard_energy_realization.py --config config/development/onboard_energy_realization_v1.json --output-root artifacts/work120/run_a
python scripts/development/run_onboard_energy_realization.py --config config/development/onboard_energy_realization_v1.json --output-root artifacts/work120/run_b --replay-reference artifacts/work120/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected Work 115/116/119 regressions and explicit staged/cached diff checks; commit immediately only after every gate passes.

## Risks and non-goals

All storage/conversion properties are synthetic. Non-goals: chemistry safety, build/energization authorization, validated capacity/rate/life, fault propagation, technology superiority/neutrality beyond this controlled opportunity, physical validation, push or history rewrite.
