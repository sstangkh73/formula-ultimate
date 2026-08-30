# Work 055 Plan: Bounded Main-Campaign Rules

Status: Completed

Thai companion: `2026-08-31_055_bounded-main-campaign-rules-plan.th.md`

## Objective

Preregister and machine-validate the rules for the first bounded whole-vehicle main research campaign. Freeze the hypotheses, evidence boundary, treatments, paired seeds, equal opportunity budget, candidate bounds, staged promotion route, statistical unit, outcome hierarchy, failure accounting, stop/go gates, and prohibited claims before implementing or running the campaign.

## Scope and planned files

- Add `config/experiments/bounded_whole_vehicle_main_campaign_v1.json` as the immutable campaign declaration.
- Add a strict protocol parser/validator under `src/formula_ultimate/experiments/` and package exports.
- Add `scripts/experiments/validate_main_campaign_protocol.py` and `scripts/run_work055.ps1`; validation writes ignored evidence under `artifacts/work055/` but performs no candidate evaluation.
- Add focused tests, bilingual campaign-protocol documentation, and matching bilingual result records.

## Planned rules

- Treatments remain `GRID`, `RANDOM`, and `EVOLUTION` with the same five Work 050 bounded variables and identical evaluator opportunity.
- Use 12 new paired seeds and 80 attempted evaluations per treatment/seed: `960` attempts per treatment and `2,880` total. Every invalid geometry, numerical failure, structural failure, exploit rejection, or DNF consumes one attempt.
- With four levels across five GRID variables, `4^5=1,024`; the planned `12 x 80=960` GRID opportunities must be unique and may not wrap or repeat.
- Promote exactly two training-feasible candidates per treatment/seed, or record an explicit shortfall. At most 72 promotions enter frozen holdout and Work 053 refined evaluation.
- The seed is the inferential unit. Candidate attempts within a seed are not independent replicates.
- Primary outcomes are seed-level refined-supported-finisher presence and seed-level best frozen-holdout time. Failures remain visible and are not discarded or assigned a hidden neutral score.
- A candidate is winner-eligible only after frozen holdout, Work 053 refined stress/deformation, provenance, exploit, and final `3D -> STEP -> FreeCAD` witness gates pass.

## Validation

1. Validate all identities, SI bounds, seed uniqueness/exclusion, budget arithmetic, GRID capacity, treatment symmetry, stage order, promotion cap, hypothesis/outcome definitions, analysis plan, failure policy, and claim boundary.
2. Deliberately reject duplicate/pilot/burn-in seeds, GRID overflow, unequal treatment budgets, missing failure consumption, attempt-level pseudo-replication, mutable thresholds, unavailable refined evaluator, and physical-validation claims.
3. Run focused/full unit tests, Python compilation, repository-contract checks, staged `git diff --cached --check`, an explicit scoped commit, and clean-tree protocol replay.

## Success criteria

- One bilingual, versioned, internally consistent protocol exists and validates deterministically without evaluating candidates.
- All campaign-changing fields are explicitly frozen and require a new protocol ID after this work.
- The protocol pins the current readiness/evaluator evidence identities and admits only the exact bounded grammar/load/material domain.
- Negative fixtures fail closed for every listed exploit or fairness violation.

## Failure criteria

Stop Work 055 if a fair non-repeating GRID budget cannot coexist with paired treatment budgets, if upstream identities cannot be pinned, if the outcome hierarchy silently drops DNF/failures, or if the validator cannot distinguish campaign readiness from physical validation.

## Risks and explicit non-goals

The seed count and opportunity budget bound this first campaign; they do not guarantee statistical power for small effects. GRID discretization differs from continuous RANDOM/EVOLUTION proposal distributions and must be reported as a treatment property. This work does not implement the campaign runner, perform burn-in, evaluate candidates, alter physics, expand topology/material/load domains, claim algorithm superiority, push, or publish.
