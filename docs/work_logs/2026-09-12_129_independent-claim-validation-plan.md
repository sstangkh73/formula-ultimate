# Work 129 Plan: Independent Claim Validation

Thai companion: `2026-09-12_129_independent-claim-validation-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Challenge the highest-impact Work 125–128 claims using a separately declared analysis formulation over locked raw candidate telemetry, without copying upstream conclusions into the calculation. Recompute paired time, energy and margin evidence, apply a stronger conservative boundary interpretation, register shared assumptions, and classify discrepancies before inspecting the upstream decision.

The validation must reject shared-function wrappers as independent and demonstrate detection of a known omitted-boundary effect. Surviving claims remain bounded numerical evidence; unexplained discrepancies or unresolved common-mode assumptions block promotion.

## Variables, controls and files

- IV: independent formulation, conservative boundary correction, fidelity and critical condition.
- DV: response disagreement, ranking stability, minimum margins, discrepancy class and revised evidence scope.
- Controls: reject identical backend/source module; inject a known modeling omission and require detection; reject changed candidate or telemetry identity.
- Success: independently recomputed claims, explicit shared assumptions, classified discrepancies, exact replay and no rewrite of upstream outcomes.

Planned files: `src/formula_ultimate/experiments/independent_claim_validation.py`, `config/development/independent_claim_validation_v1.json`, `scripts/development/run_independent_claim_validation.py`, `tests/test_independent_claim_validation.py`, bilingual `docs/contracts/INDEPENDENT_CLAIM_VALIDATION_V1*`, this bilingual plan/result, and ignored `artifacts/work129/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_independent_claim_validation tests.test_repository_contract -v
python scripts/development/run_independent_claim_validation.py --config config/development/independent_claim_validation_v1.json --output-root artifacts/work129/run_a
python scripts/development/run_independent_claim_validation.py --config config/development/independent_claim_validation_v1.json --output-root artifacts/work129/run_b --replay-reference artifacts/work129/run_a/result.json
python -m compileall -q src scripts tests
```

Then run affected Work 125–128 regressions and explicit staged/cached diff checks; commit immediately only after every gate passes.

## Risks and non-goals

Separate code can retain shared telemetry and physical assumptions. This is an independent numerical interpretation, not institutional independence or physical measurement. Non-goals: rewriting prior results, external novelty, vehicle promotion, physical validation, push or history rewrite.
