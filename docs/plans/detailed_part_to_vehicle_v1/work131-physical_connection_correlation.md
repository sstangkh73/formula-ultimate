# Work 131: Authorized material and connection measurement

Thai companion: `work131-physical_connection_correlation.th.md`

Status: Planned

Original Work 106 package: 130

Dependencies: Work 113, Work 116, Work 130

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Compare safe, authorized material/connection measurements with frozen model predictions and quantify discrepancy.

Requires explicit authority, suitable facility, qualified safety review, inspected specimens and calibrated instruments before testing.

## 2. Proposed files

- `src/formula_ultimate/experiments/physical_connection_correlation.py`
- `config/development/physical_connection_correlation_v1.json`
- `scripts/development/run_physical_connection_correlation.py`
- `tests/test_physical_connection_correlation.py`

## 3. Implementation sequence

1. Prepare a bounded test protocol, hazard review, stop conditions and measurement uncertainty budget.
2. Freeze predictions and specimen/fixture identities; separate calibration and validation specimens/conditions.
3. Have authorized personnel perform the approved test and preserve unedited raw observations.
4. Analyze offline, compare predictions and register any model update before new validation.

## 4. Experiment

- IV: Approved specimen/joint geometry, material batch and bounded test condition.
- DV: Measured load/displacement/temperature or other approved quantities, repeatability and model discrepancy.
- Controls: Reference specimen, calibrated measurement chain, fixture compliance and environmental records.

## 5. Tests and falsification

Offline analysis rejects missing calibration, swapped specimen IDs, sensor saturation and edited raw data. Test stop logic without energizing hazardous hardware.

## 6. Registration and acceptance

Freeze safe bounds approved by qualified reviewers, sample design, measurement uncertainty and discrepancy acceptance before data collection.

No physical execution without all entry permissions. Valid measurements support only tested scope; unexplained discrepancy blocks extrapolation.

## 7. Deliverables and handoff

Approval references, specimen/measurement manifests, raw data, uncertainty and correlation report; analysis runner is offline only.

Provides measured material/joint applicability for subsystem Work 132.

## 8. Risks and non-goals

Stop for unsafe conditions or missing authorization. No autonomous equipment operation, unsupervised destructive tests or whole-vehicle certification.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_physical_connection_correlation tests.test_repository_contract -v
python scripts/development/run_physical_connection_correlation.py --config config/development/physical_connection_correlation_v1.json --output-root artifacts/work131/run_a
python scripts/development/run_physical_connection_correlation.py --config config/development/physical_connection_correlation_v1.json --output-root artifacts/work131/run_b --replay-reference artifacts/work131/run_a/result.json
```
