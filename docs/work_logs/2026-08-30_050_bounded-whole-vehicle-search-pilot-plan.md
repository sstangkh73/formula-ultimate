# Work 050 Plan: Bounded Whole-Vehicle Search Pilot and Readiness Review

Status: Completed

Thai companion: `2026-08-30_050_bounded-whole-vehicle-search-pilot-plan.th.md`

## Objective

Test whether `GRID`, `RANDOM`, and `EVOLUTION` can propose, evaluate, fail, compare, and replay whole-vehicle candidates fairly through one immutable bounded evaluator. Run the preregistered equal attempted-evaluation budget, promote selected candidates to frozen holdouts, audit refined-evaluator availability, and return either `ready_for_bounded_main_campaign` or `not_ready` without weakening gates.

## Scope and planned files

- Add a frozen pilot manifest under `config/experiments/` with candidate bounds, three seeds, `32` attempts per treatment/seed, immutable upstream identities, promotion rules, and readiness blockers.
- Implement `DesignSearchAgentV0`, shared evaluator, treatment adapters, ancestry/RNG checkpoints, exact budget accounting, immutable ledgers, holdout promotion, exploit controls, and readiness decision under `src/formula_ultimate/experiments/`.
- Add an acceptance runner, `scripts/run_work050.ps1`, focused tests, bilingual pilot/readiness report, and matching bilingual result records.
- Write ignored ledgers and summaries under `artifacts/work050/`.

## Experiment definition

- Treatments: `GRID`, `RANDOM`, and `EVOLUTION` through the same evaluator API.
- Independent variables: treatment, preregistered seed, and bounded Work 047 grammar variables for core length/width, ground-contact radius, source primitive size, and propulsor primitive size. Material densities remain fixed because no density-strength law is admitted.
- Dependent variables: grammar validity, mass and inertia-derived mass ratio, structural-capacity proxy, training feasibility, failure code, Level 0 time/energy objective, holdout survival, refined-evaluator status, wall time, attempted budget, ancestry, and replay hashes.
- Controls: `32` attempts per treatment per seed across seeds `101/202/303`; identical variable bounds, loads, evaluator, tolerances, component library, opportunity set, and failure accounting.
- Falsification controls: hidden evaluator/load/tolerance mutation, out-of-range/NaN variable, unknown variable, skipped failed attempt, changed seed, and ledger mutation.

## Validation

1. Unit-test all treatment adapters, exact same-seed replay, candidate schema, budget accounting, ancestry, and fail-closed exploit controls.
2. Run exactly `288` attempted evaluations; every invalid or failed candidate consumes one attempt.
3. Require equal attempted budgets and one evaluator/opportunity identity across treatments.
4. Promote preregistered best training-feasible candidates to Work 048 holdouts.
5. Require an independent refined structural evaluator for readiness; if absent, report promotions as unverified and return `not_ready`.
6. Run repository-contract, full unit, compile, staged-diff, and clean-tree replay gates.

## Success criteria

- Same-seed rerun reproduces every candidate, failure, ancestry link, objective, and ledger fingerprint exactly.
- All treatments consume exactly equal budgets including failures and cannot edit evaluator inputs outside candidate variables.
- Holdout results are explicit for every selected candidate; unavailable refined evaluation cannot create a winner.
- Readiness returns one explicit allowed decision with evidence-backed blockers.

## Risks

The geometry-to-capacity relation is a declared Level 0 proxy, not stress FEA. A treatment may appear better because of the bounded parameterization. Material density is deliberately not mutable because changing density without strength evidence would create an exploit. Equal attempts do not prove equal wall-clock opportunity at higher fidelity. The correct result may be `not_ready` even if search mechanics pass.

## Explicit non-goals

No main research campaign, superiority/novelty/discovery claim, arbitrary topology, whole-vehicle stress FEA, real-circuit result, physical validation, safety/manufacturing certification, push, or publication is included.
