# Work 120: Detailed onboard energy realization

Thai companion: `work120-onboard_energy_realization.th.md`

Status: Planned

Original Work 106 package: 119

Dependencies: Work 115, Work 116, Work 119

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Close one explicitly scoped onboard storage/conversion route, including internal geometry, containment, loss and usable energy limits.

Work 119 ports and existing external primary-energy rules; material and thermal evidence from Works 115/116.

## 2. Proposed files

- `src/formula_ultimate/subsystems/onboard_energy_realization.py`
- `config/development/onboard_energy_realization_v1.json`
- `scripts/development/run_onboard_energy_realization.py`
- `tests/test_onboard_energy_realization.py`

## 3. Implementation sequence

1. Freeze energy boundary, initial stored state, capacity/rate conditions and a supported reference technology.
2. Represent storage/conversion internals, enclosure, insulation, connectors and mounting.
3. Track input, output, stored energy change and all modeled losses without external replenishment.
4. Propagate temperature/rate limits and containment loads into geometry and assembly models.

## 4. Experiment

- IV: Internal geometry, storage allocation, rate demand and thermal environment.
- DV: Usable primary energy, delivered power, heat, complete mass and limiting states.
- Controls: Same external energy opportunity, task and initial-state accounting across routes.

## 5. Tests and falsification

Empty storage, excessive demand, disconnected converter, omitted containment mass and hidden replenishment. Reject unit/energy-boundary inconsistencies.

## 6. Registration and acceptance

Freeze constitutive/data validity, energy budget, capacity/rate/temperature limits and residual tolerances.

Energy and hardware coverage close for the selected route. Unsupported chemistry/field/conversion physics blocks stronger claims, not other technology proposals.

## 7. Deliverables and handoff

Detailed energy assembly, state/loss ledger, geometry-derived mass and safe applicability limits.

Feeds Work 122 hardware supply and Work 123 coupled energy integration.

## 8. Risks and non-goals

Containment/chemistry hazards require specialized evidence. This is simulation planning, not permission to build or energize hardware; no technology-neutrality claim beyond tested opportunity.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_onboard_energy_realization tests.test_repository_contract -v
python scripts/development/run_onboard_energy_realization.py --config config/development/onboard_energy_realization_v1.json --output-root artifacts/work120/run_a
python scripts/development/run_onboard_energy_realization.py --config config/development/onboard_energy_realization_v1.json --output-root artifacts/work120/run_b --replay-reference artifacts/work120/run_a/result.json
```
