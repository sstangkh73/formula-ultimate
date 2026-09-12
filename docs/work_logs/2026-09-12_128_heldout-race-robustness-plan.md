# Work 128 Plan: Held-Out Race Robustness

Thai companion: `2026-09-12_128_heldout-race-robustness-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Evaluate the frozen Work 127 finalists and controllers on a sealed set of unseen synthetic race conditions without tuning, repair or threshold changes after exposure. Pin finalist, evaluator, rules and holdout hashes; execute every registered paired trajectory; retain failures and propagate environment/numerical uncertainty into the registered comparison.

The experiment can complete with a negative result. Robust superiority additionally requires the preregistered paired time effect, complete-race rate, energy, thermal and structural gates. Numerical completion is not physical validation.

## Variables, controls and files

- IV: frozen finalist and sealed held-out environment/load/initial-condition case.
- DV: completion, race time in `s`, primary energy in `J`, thermal/structural margin, paired interval and failure distribution.
- Controls: reject reused training conditions, changed source hashes, hidden incomplete races, post-exposure tuning and late threshold edits.
- Success: immutable identities, complete telemetry for all registered pairs, uncertainty analysis, exact replay and bounded decision.

Planned files: `src/formula_ultimate/experiments/heldout_race_robustness.py`, `config/development/heldout_race_robustness_v1.json`, `scripts/development/run_heldout_race_robustness.py`, `tests/test_heldout_race_robustness.py`, bilingual `docs/contracts/HELDOUT_RACE_ROBUSTNESS_V1*`, this bilingual plan/result, and ignored `artifacts/work128/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_heldout_race_robustness tests.test_repository_contract -v
python scripts/development/run_heldout_race_robustness.py --config config/development/heldout_race_robustness_v1.json --output-root artifacts/work128/run_a
python scripts/development/run_heldout_race_robustness.py --config config/development/heldout_race_robustness_v1.json --output-root artifacts/work128/run_b --replay-reference artifacts/work128/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected Work 127 regressions and explicit staged/cached diff checks; commit immediately only after all gates pass.

## Risks and non-goals

Synthetic race telemetry may expose model assumptions rather than manufactured behavior. Changed finalists invalidate admission and require a new holdout. Non-goals: post-result repair, external novelty, physical validation, promotion from Level 0, push or history rewrite.
