# Work 054 Plan: Refined-Gate Whole-Vehicle Readiness Adjudication

Status: Completed

Thai companion: `2026-08-30_054_refined-gate-readiness-adjudication-plan.th.md`

## Objective

Resolve the sole retained Work 050 blocker by consuming the completed Work 053 independent evaluator evidence, rejecting unsupported promotions without rewriting them, and issuing a deterministic readiness decision for a bounded whole-vehicle research campaign.

## Scope and planned files

- Add a versioned adjudication configuration that pins Work 050 ledgers/protocol and Work 053 evaluator implementation/config/replay identities.
- Add a pure adjudicator plus a fail-closed runner and `scripts/run_work054.ps1`.
- Add focused tests, a bilingual readiness report, and matching bilingual result records.
- Write ignored evidence under `artifacts/work054/`.

## Experiment and decision definition

- Independent variables: retained/refined gate status of the nine frozen Work 050 promotions and their original treatment/objective records.
- Dependent variables: supported count by treatment, treatment winner, global winner, readiness checks, blockers, decision, and deterministic record hash.
- Controls: original `96/96/96` GRID/RANDOM/EVOLUTION attempt budgets, all Work 050 provenance/exploit/holdout checks, the exact Work 053 evaluator identity, unchanged Work 053 pass/fail outcomes, and original objective values.
- Preferred hypothesis: removing only the two candidates rejected by Work 053 leaves at least two refined-supported promotions in every treatment and a refined-supported global winner while all other readiness checks remain true.
- Falsification: fail closed for any identity drift, extra Work 050 blocker, unsupported winner, missing treatment, fewer than two supported candidates in a treatment, changed objective, changed refined status, or non-exact replay.

## Validation and success criteria

1. Rerun Work 053, which itself reruns and verifies Work 050, before adjudication.
2. Require exactly nine frozen promotions with three original promotions per treatment and exact candidate identities.
3. Join Work 053 by candidate ID; retain only candidates with both holdouts passed and preserve rejected candidates as explicit contradictory evidence.
4. Require at least two supported candidates per treatment. Select each treatment winner and the global winner by original holdout objective with candidate ID as deterministic tie-break.
5. Change only `independent_refined_evaluation` from false to true; all other Work 050 readiness checks must already be true.
6. Decision may be only `ready_for_bounded_whole_vehicle_campaign`, never `physically_validated` or an engineering-discovery claim.
7. Run focused/full tests, compilation, repository contract, fail-fast staged checks, explicit scoped commit, and clean-tree replay.

## Risks and explicit non-goals

This adjudication can close research-process readiness only. It cannot validate the vehicle physically, repair rejected candidates, prove one search treatment superior, expand topology, add solid/contact/nonlinear/crash/fatigue evidence, run the main campaign, push, or publish.
