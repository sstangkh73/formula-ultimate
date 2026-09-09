# Work 133: Authorized whole-vehicle validation program

Thai companion: `work133-physical_vehicle_validation.th.md`

Status: Planned

Original Work 106 package: 132

Dependencies: Work 128, Work 129, Work 130, Work 131, Work 132

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Build measured evidence for an exact vehicle configuration through a professionally reviewed staged test envelope.

Independent digital claims, manufacturing/assembly inspection and relevant physical subsystem evidence; explicit authority and facility readiness mandatory.

## 2. Proposed files

- `src/formula_ultimate/experiments/physical_vehicle_validation.py`
- `config/development/physical_vehicle_validation_v1.json`
- `scripts/development/run_physical_vehicle_validation.py`
- `tests/test_physical_vehicle_validation.py`

## 3. Implementation sequence

1. Review unresolved hazards, instrumentation and abort/recovery arrangements with qualified reviewers.
2. Freeze configuration and predictions; define staged expansion criteria before operating.
3. Have authorized personnel execute only approved stages, recording all incidents and configuration changes.
4. Compare measured whole-system behavior and limits with predictions; issue scope-bounded conclusions.

## 4. Experiment

- IV: Approved vehicle configuration and staged environmental/operating conditions.
- DV: Measured completion/time, energy, thermal/structural response, controllability and model discrepancy.
- Controls: Traceable conditions and measurement uncertainty; any comparison vehicle requires equivalent approved opportunity.

## 5. Tests and falsification

Offline audit detects unapproved stage expansion, changed hardware/control, missing failures, incomplete energy records and improper extrapolation.

## 6. Registration and acceptance

Freeze qualified-review safety bounds, staged entry/exit rules, measurement plan and exact scope of any performance/safety claim.

Only approved stages with valid measured evidence support conclusions. Incidents, missing data or unresolved discrepancy can stop promotion even when the vehicle moves.

## 7. Deliverables and handoff

Configuration/test dossiers, immutable telemetry, incident reports, uncertainty analysis and tested-scope validation statement.

Defines achieved physical scope and new research gaps; further claims require new numbered work and authority.

## 8. Risks and non-goals

This is a program requiring smaller approved test works, not one unattended run. No automatic racing, road use, safety certification or guaranteed superiority.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_physical_vehicle_validation tests.test_repository_contract -v
python scripts/development/run_physical_vehicle_validation.py --config config/development/physical_vehicle_validation_v1.json --output-root artifacts/work133/run_a
python scripts/development/run_physical_vehicle_validation.py --config config/development/physical_vehicle_validation_v1.json --output-root artifacts/work133/run_b --replay-reference artifacts/work133/run_a/result.json
```
