# Work 127 Plan: Optimized Vehicle Controls

Thai companion: `2026-09-12_127_optimized-vehicle-controls-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Test whether the Work 126 candidate's bounded system score survives optimized fixed-topology, reference and random-control baselines, common-controller substitution, matched-budget retuning and complete transferred-burden accounting. Pin Work 123 transient evidence, Work 124 reserve-before-execute accounting and the exact Work 126 exploratory assembly.

All arms receive the same external task, component library opportunity, source energy, safety boundary, paired seeds and separate search/tuning budgets. A completed negative result is acceptable; a system-benefit claim requires a registered effect beyond uncertainty with no hidden mass, energy, cooling, containment, support or manufacturing burden.

## Variables, controls and files

- IV: vehicle/search arm, mechanism substitution, controller treatment and tuned parameter.
- DV: paired system score, completion/time proxy, energy, installed mass, failure state, uncertainty and charged search/tuning cost.
- Controls: untuned baseline, free controller effort, omitted cooling mass and unequal source energy must invalidate fairness.
- Success: every arm optimized at equal cost, common controller evaluated then equally retuned, complete burden ledger, exact replay and evidence-bound promotion decision.

Planned files: `src/formula_ultimate/experiments/optimized_vehicle_controls.py`, `config/development/optimized_vehicle_controls_v1.json`, `scripts/development/run_optimized_vehicle_controls.py`, `tests/test_optimized_vehicle_controls.py`, bilingual `docs/contracts/OPTIMIZED_VEHICLE_CONTROLS_V1*`, this bilingual plan/result, and ignored `artifacts/work127/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_optimized_vehicle_controls tests.test_repository_contract -v
python scripts/development/run_optimized_vehicle_controls.py --config config/development/optimized_vehicle_controls_v1.json --output-root artifacts/work127/run_a
python scripts/development/run_optimized_vehicle_controls.py --config config/development/optimized_vehicle_controls_v1.json --output-root artifacts/work127/run_b --replay-reference artifacts/work127/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected Work 123/124/126 regressions and explicit staged/cached diff checks; commit immediately only after every gate passes.

## Risks and non-goals

The registered response model is synthetic and cannot establish race performance or physical superiority. A fixed topology is only a fair control and does not prescribe the open arm's layout. Non-goals: external novelty, post-result threshold changes, physical validation, promotion from an exploratory assembly, push or history rewrite.
