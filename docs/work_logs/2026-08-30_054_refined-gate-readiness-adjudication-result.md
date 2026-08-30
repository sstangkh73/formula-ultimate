# Work 054 Result: Refined-Gate Whole-Vehicle Readiness Adjudication

Status: Completed

Thai companion: `2026-08-30_054_refined-gate-readiness-adjudication-result.th.md`

## Outcome

Decision: `ready_for_bounded_whole_vehicle_campaign`. The sole Work 050 blocker is closed by the Work 053 independent refined evaluator. All ten final readiness checks are true, blockers are empty, seven candidates are supported, and two remain rejected. Every treatment retains at least two supported promotions.

The global pilot winner remains GRID `candidate-12b30a0606bccf88` with original holdout objective `34.1204253544251 s`; it passed both Work 053 holdouts. This is research-campaign readiness, not physical vehicle validation or a treatment-superiority claim.

## Files changed

- `config/experiments/refined_gate_readiness_adjudication_v1.json`
- `src/formula_ultimate/experiments/refined_readiness.py` and experiment package exports
- `scripts/experiments/adjudicate_refined_readiness.py` and `scripts/run_work054.ps1`
- `tests/test_refined_readiness.py`
- `docs/research/BOUNDED_WHOLE_VEHICLE_CAMPAIGN_READINESS.md` and `.th.md`
- matching Work 054 bilingual plan/result records

Ignored evidence is under `artifacts/work054/`.

## Decisions and evidence

- Original Work 050 budgets remained GRID/RANDOM/EVOLUTION `96/96/96`, with three original promotions per treatment.
- GRID retained `2/3`, RANDOM `3/3`, and EVOLUTION `2/3` refined-supported promotions.
- Treatment winners are GRID `candidate-12b30a0606bccf88` (`34.1204253544251 s`), RANDOM `candidate-58b6c6238b708e6a` (`35.42349737959053 s`), and EVOLUTION `candidate-333486cb11b2f603` (`34.16703235066346 s`).
- Rejected candidates `candidate-9b03158dc541df18` and `candidate-372db49a7cbceba5` remain explicit and ineligible.
- Work 054 changed only `independent_refined_evaluation` from false to true; all other Work 050 readiness checks were required to be true before adjudication.
- Deterministic adjudication SHA-256 is `c8a5e89fba6d96be5a5cfa063a51a1d2b0eb597c25f24784dbe85a4c062da953`; config SHA-256 is `927b7c9fa9194ba1ae6967297d011d07e23f0acb28489b42f85ff6954eac67d4`.

## Exact validation

```powershell
py -3.14 -m unittest tests.test_refined_readiness -q
# exit 0; Ran 4 tests; OK

powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work054.ps1
# exit 0; status=passed
# decision=ready_for_bounded_whole_vehicle_campaign
# supported_candidates=7; rejected_candidates=2
# global_winner=candidate-12b30a0606bccf88
# blockers=[]; replay=exact

py -3.14 -m unittest tests.test_refined_readiness tests.test_vehicle_frame_refinement tests.test_repository_contract -q
# exit 0; Ran 15 tests; OK

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 343 tests in 29.853s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0
```

Repository-contract checks, staged `git diff --cached --check`, the explicit scoped commit, and clean-tree Work 054 replay are verified after this result exists and are reported in the final handoff.

## Limitations and follow-up

The readiness scope remains the exact bounded grammar, loads, synthetic material, quasi-static beam evaluator, fixed baselines, and equal-attempt pilot controls. It does not validate solid/contact behavior, nonlinear materials, local buckling, fatigue, vibration, crash, physical calibration, manufacturing, safety, or race performance. The main campaign itself has not been run.
