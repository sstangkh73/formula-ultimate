# Work 132: Authorized subsystem correlation and endurance

Thai companion: `work132-physical_subsystem_correlation.th.md`

Status: Planned

Original Work 106 package: 131

Dependencies: Work 131

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Validate selected coupled subsystem behavior and relevant endurance within an approved physical test envelope.

Work 131 calibrated local applicability plus all relevant subsystem packages; requires new subsystem-specific safety/authorization review.

## 2. Proposed files

- `src/formula_ultimate/experiments/physical_subsystem_correlation.py`
- `config/development/physical_subsystem_correlation_v1.json`
- `scripts/development/run_physical_subsystem_correlation.py`
- `tests/test_physical_subsystem_correlation.py`

## 3. Implementation sequence

1. Select a subsystem/claim and assemble its geometry, model, instrument and safety dossier.
2. Freeze coupled predictions, test sequence, approved duration/cycles and failure observations.
3. Acquire authorized measurements with complete boundary/energy records and abort reporting.
4. Analyze losses, degradation and uncertainty; recalibrate only on designated data and validate anew.

## 4. Experiment

- IV: Approved load/thermal/control histories and inspected subsystem configuration.
- DV: Coupled response, efficiency/loss, degradation, failure onset and prediction error.
- Controls: Same approved fixture/environment and traceable instrumentation; separate untouched validation runs.

## 5. Tests and falsification

Offline pipeline detects missing boundary power, undocumented replacement, calibration leakage, censored aborts and sensor disagreement.

## 6. Registration and acceptance

Freeze approved loads/cycles, material/model ranges, endurance claim, uncertainty and stop criteria; no universal lifetime extrapolation.

Traceable measurements meet registered claim criteria or produce a bounded negative result. Local calibration alone cannot establish subsystem validation.

## 7. Deliverables and handoff

Subsystem raw data, energy/loss/degradation histories, discrepancy analysis and revised applicability dossier.

Supplies qualified subsystem evidence and unresolved risks to whole-vehicle Work 133.

## 8. Risks and non-goals

One subsystem test cannot certify other architectures or full service life. Separate authorization is required for hazardous operating changes; offline analysis only.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_physical_subsystem_correlation tests.test_repository_contract -v
python scripts/development/run_physical_subsystem_correlation.py --config config/development/physical_subsystem_correlation_v1.json --output-root artifacts/work132/run_a
python scripts/development/run_physical_subsystem_correlation.py --config config/development/physical_subsystem_correlation_v1.json --output-root artifacts/work132/run_b --replay-reference artifacts/work132/run_a/result.json
```
