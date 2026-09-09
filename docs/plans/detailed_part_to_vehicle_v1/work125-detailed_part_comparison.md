# Work 125: Registered detailed-part discovery comparison

Thai companion: `work125-detailed_part_comparison.th.md`

Status: Planned

Original Work 106 package: 124

Dependencies: Work 113, Work 114, Work 115, Work 116, Work 124

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Test whether freely generated detailed parts provide task-relevant benefit beyond numerical uncertainty and fair optimized controls.

Verified detailed connection/field models and Work 124 engine; use untouched admitted conditions separate from pilots.

## 2. Proposed files

- `src/formula_ultimate/experiments/detailed_part_comparison.py`
- `config/development/detailed_part_comparison_v1.json`
- `scripts/development/run_detailed_part_comparison.py`
- `tests/test_detailed_part_comparison.py`

## 3. Implementation sequence

1. Select a bounded functional task and freeze training/holdout plus meaningful effect before comparison.
2. Optimize fixed-family, existing-grammar, open-material and random-control arms with matched budgets.
3. Run paired studies and audit rejected/unresolved geometry independent of proxy score.
4. Ablate proposed active geometry/coupling and evaluate finalists at stronger fidelity.

## 4. Experiment

- IV: Representation/search arm, geometry/coupling intervention and held-out operating condition.
- DV: Verified task utility, material/energy burden, failure margins and total cost.
- Controls: Identical task, material/process evidence, budget and seed pairing; optimized controls, not untuned defaults.

## 5. Tests and falsification

Inactive appendage, same-graph response change, omitted hardware, ranking reversal at finer mesh and leaked holdout detection.

## 6. Registration and acceptance

Freeze sample size from a separate pilot, outcome estimand, uncertainty method, effect threshold and stopping rules.

Experiment execution can complete with a negative result. A discovery-benefit claim additionally requires constraints, signed effect and uncertainty gates to pass.

## 7. Deliverables and handoff

Registration, all-arm results, ablation evidence, holdout report and supporting/contradicting/alternative/missing evidence.

Passes scoped useful parts and negative findings to detailed vehicle Work 126.

## 8. Risks and non-goals

Do not tune thresholds after results or demand visible strangeness. External prior-art novelty and whole-vehicle benefit remain separate studies.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_detailed_part_comparison tests.test_repository_contract -v
python scripts/development/run_detailed_part_comparison.py --config config/development/detailed_part_comparison_v1.json --output-root artifacts/work125/run_a
python scripts/development/run_detailed_part_comparison.py --config config/development/detailed_part_comparison_v1.json --output-root artifacts/work125/run_b --replay-reference artifacts/work125/run_a/result.json
```
