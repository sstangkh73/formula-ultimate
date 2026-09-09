# Work 128: Held-out race and robustness

Thai companion: `work128-heldout_race_robustness.th.md`

Status: Planned

Original Work 106 package: 127

Dependencies: Work 127

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Evaluate frozen finalists on unseen declared task conditions without post-result repairs or training leakage.

Work 127 finalists, untouched holdout provenance and the governing race/energy task.

## 2. Proposed files

- `src/formula_ultimate/experiments/heldout_race_robustness.py`
- `config/development/heldout_race_robustness_v1.json`
- `scripts/development/run_heldout_race_robustness.py`
- `tests/test_heldout_race_robustness.py`

## 3. Implementation sequence

1. Seal candidate/controller/evaluator identities and held-out condition manifests before exposure.
2. Run complete registered trajectories and record every failure, stop and budget-limited attempt.
3. Propagate numerical/material/environment uncertainty and evaluate robustness metrics.
4. Compare paired finalist outcomes and retain full negative evidence and applicability bounds.

## 4. Experiment

- IV: Frozen candidate and held-out environment/load/initial-condition variations.
- DV: Race completion/time, primary energy, thermal/structural margins and uncertainty intervals.
- Controls: Same unseen conditions and rules for all arms; no additional tuning after exposure.

## 5. Tests and falsification

Holdout reuse, changed source hashes, incomplete races hidden from summaries and late threshold edits must be rejected.

## 6. Registration and acceptance

Freeze sample/condition design, statistical estimand, multiplicity treatment where needed, completion rules and acceptance thresholds.

An admitted comparison requires intact freeze/leakage and execution evidence. Claimed robust superiority additionally requires the preregistered effect/constraint gates.

## 7. Deliverables and handoff

Immutable holdout manifests, per-run telemetry, failure distribution, uncertainty analysis and comparative result.

Sends decisive outcomes and critical conditions to independent analysis Work 129.

## 8. Risks and non-goals

If finalists are changed, the observed set becomes exploratory and new holdout is needed. Numerical race completion is not physical validation.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_heldout_race_robustness tests.test_repository_contract -v
python scripts/development/run_heldout_race_robustness.py --config config/development/heldout_race_robustness_v1.json --output-root artifacts/work128/run_a
python scripts/development/run_heldout_race_robustness.py --config config/development/heldout_race_robustness_v1.json --output-root artifacts/work128/run_b --replay-reference artifacts/work128/run_a/result.json
```
