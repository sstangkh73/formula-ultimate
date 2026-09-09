# Work 123: Coupled whole-candidate transient harness

Thai companion: `work123-coupled_vehicle_transient.th.md`

Status: Planned

Original Work 106 package: 122

Dependencies: Work 117, Work 118, Work 119, Work 120, Work 121, Work 122

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Couple actual subsystem states and energy exchanges through time on one candidate revision, including incomplete exploratory models.

Use applicable subsystem response models and physical interfaces; unresolved domains remain explicit, never favorable invented coefficients.

## 2. Proposed files

- `src/formula_ultimate/simulation/coupled_vehicle_transient.py`
- `config/development/coupled_vehicle_transient_v1.json`
- `scripts/development/run_coupled_vehicle_transient.py`
- `tests/test_coupled_vehicle_transient.py`

## 3. Implementation sequence

1. Define state ownership, time bases, initialization and interface variable exchange.
2. Implement coupling iterations/events and conservative work/heat transfer accounting.
3. Integrate controller, ground, actuation, energy, structure and cooling with validity checks.
4. Run bounded trajectories with time/coupling refinement and replay complete input identities.

## 4. Experiment

- IV: Architecture, subsystem variants, coupling step and controller adaptation mode.
- DV: Trajectory, completion, energy/heat residuals, failure margins and integration error.
- Controls: Same external task/environment and consistent initial physical state.

## 5. Tests and falsification

Mismatched frames/signs, double-counted power, delayed events, depleted energy and out-of-range reduced models. Repeat decoupled tests to localize errors.

## 6. Registration and acceptance

Freeze exchange schema, time-step ladder, coupling tolerance, stop/failure rules and trial envelope.

Coupled reference and numerical gates pass; required unresolved domains block promotion but can remain in clearly typed exploratory runs.

## 7. Deliverables and handoff

State histories, interface energy ledger, validity excursions, convergence and exact decision replay.

Enables Work 124 vehicle-search mode and Works 126–128 candidate comparisons.

## 8. Risks and non-goals

A coupled harness is not a complete detailed vehicle. Do not infer readiness from successful integration or a short path; no physical-validation claim.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_coupled_vehicle_transient tests.test_repository_contract -v
python scripts/development/run_coupled_vehicle_transient.py --config config/development/coupled_vehicle_transient_v1.json --output-root artifacts/work123/run_a
python scripts/development/run_coupled_vehicle_transient.py --config config/development/coupled_vehicle_transient_v1.json --output-root artifacts/work123/run_b --replay-reference artifacts/work123/run_a/result.json
```
