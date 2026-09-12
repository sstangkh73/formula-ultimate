# Work 117 Plan: Bidirectional Architecture-Part Feedback

Thai companion: `2026-09-12_117_architecture-part-feedback-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Implement a bounded feedback/regeneration loop that pins Work 112 terminal semantics, Work 114 motion/load history and Work 115 thermal coupling. Keep the external task immutable while versioned internal tasks receive assembly-derived load, heat, motion, envelope and unknown-model requirements.

Generate local free-parameter region geometry from each task, evaluate structural/thermal margins and mass, return changed requirements, and invalidate stale evidence after every causal task revision. Compare feedback-enabled and frozen-task controls with the same initial candidate, coefficients, seeds and evaluation cap.

## Variables, controls and files

- IV: feedback enabled/frozen, task version, geometry parameters, decomposition/merge and architecture-derived conditions.
- DV: task/geometry identities, load/heat margins, mass, missing-model blockers, invalidation events and evaluations per iteration.
- Controls: immutable external task, equal compute opportunity, changed assembly load requiring reevaluation, multifunctional region merge without duplicate mass, and missing-coefficient rejection.
- Success: at least one traced feedback/regeneration cycle changes both task and geometry evidence; ancestry and invalidations are complete; unresolved models cannot justify feasibility; replay is exact. Improvement is measured but not required.

Planned files: `src/formula_ultimate/experiments/architecture_part_feedback.py`, `config/development/architecture_part_feedback_v1.json`, `scripts/development/run_architecture_part_feedback.py`, `tests/test_architecture_part_feedback.py`, bilingual `docs/contracts/ARCHITECTURE_PART_FEEDBACK_V1*`, this bilingual plan/result and ignored `artifacts/work117/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_architecture_part_feedback tests.test_repository_contract -v
python scripts/development/run_architecture_part_feedback.py --config config/development/architecture_part_feedback_v1.json --output-root artifacts/work117/run_a
python scripts/development/run_architecture_part_feedback.py --config config/development/architecture_part_feedback_v1.json --output-root artifacts/work117/run_b --replay-reference artifacts/work117/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected regressions and explicit staged/cached diff checks; commit immediately only after all gates pass.

## Risks and non-goals

The bounded generator and reduced evaluators are not a complete optimizer. Non-goals: changing race rules, complete feasibility, isolated-survivor promotion, unrestricted search, vehicle readiness, physical validation, push or history rewrite.
