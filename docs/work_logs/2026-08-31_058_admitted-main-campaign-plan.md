# Work 058 Plan: Admitted Bounded Whole-Vehicle Main Campaign

Status: Stopped before execution — Work 057 did not issue burn-in admission; zero main-seed opportunities were reserved.

Thai companion: `2026-08-31_058_admitted-main-campaign-plan.th.md`

## Objective

Conditionally execute and analyze the preregistered `FU-BMC-001` main campaign with the exact code, protocol, adapters, tools, and thresholds accepted in Work 057. No main-seed reservation is allowed before a committed burn-in decision authorizes admission.

## Scope and planned files

- Reuse the Work 057 command and committed implementation without modification.
- Produce ignored append-only main ledgers, per-seed promotion/holdout/refinement/STEP-FreeCAD evidence, analysis, and replay manifests under `artifacts/work058/`.
- Add bilingual main-campaign research/result records and commit them after validation.
- If any post-admission implementation/config change becomes necessary, stop `FU-BMC-001`; do not repair and continue under the same campaign ID.

## Preregistered design

- Independent variable: proposal treatment (`GRID`, `RANDOM`, `EVOLUTION`).
- Inference unit: paired seed, not individual attempt.
- Paired main seeds: `55001` through `55012`.
- Opportunities: `80` per treatment/seed, `960` per treatment, `2,880` total.
- Promotion cap: two training-feasible candidates per treatment/seed, maximum `72`; shortfall remains explicit.
- Primary dependent outcome: presence of at least one refined-supported finisher per treatment/seed.
- Secondary paired outcome: best frozen-holdout time on common-success seeds.
- Other declared outputs: failure distribution, training feasible rate, refined survival, mass, energy, stress margin, displacement, and compute cost.
- Controls: common candidate bounds/component library/constraints/partitions/evaluators, equal attempted-opportunity budget, paired seeds, unique GRID opportunities, exact ledger/replay, no holdout leakage, and unchanged Work 057 tool identities.

## Preferred hypothesis and falsification

Primary `H1_EVOLUTION_SUPPORTED_FINISHER_RATE`: `EVOLUTION` has a higher paired-seed supported-finisher probability than `RANDOM`. A non-positive observed paired rate difference contradicts the preferred hypothesis. Attempt-level feasibility must not replace this endpoint.

For common-success seeds, lower EVOLUTION best holdout time supports the secondary hypothesis; zero or positive paired median difference does not. GRID comparisons remain descriptive. All preregistered outcomes and contradictory evidence must be reported.

## Admission, success, and failure criteria

Admission requires a committed Work 057 decision `burn_in_accepted_for_admitted_main_campaign`, exact burn-in replay, matching protocol/adapters/tool hashes, and a clean worktree.

Successful execution requires exactly `2,880` terminal attempts with equal per-treatment/seed budgets, terminal evidence for every promotion, no identity/partition/provenance violation, exact replay, and one declared final status. `completed_without_supported_finisher` is a valid scientific result.

Stop as `stopped_protocol_violation` on identity, leakage, fairness, mutation-after-burn-in, or replay violations. Stop as `stopped_infrastructure_failure` when required tools or durable outputs become unavailable. Never retry failed opportunities or change thresholds after seeing results.

## Analysis

Use analysis seed `551337`. Report paired supported-finisher rate difference, exact McNemar result, 95% paired bootstrap interval, common-success paired median best-time difference, exact sign-flip result, 95% paired bootstrap interval, descriptive GRID tables, complete failure counts, and winner selection by all gates then minimum holdout time then candidate ID.

## Validation and commit

Verify admitted authorization, immutable identities, ledger counts/fingerprints, GRID uniqueness, promotion caps/shortfalls, terminal downstream evidence, statistical replay, full tests, compilation, bilingual documentation, explicit staged scope, `git diff --cached --check`, commit, and clean-tree verify-only replay.

## Risks and non-goals

The campaign may take substantial solver time or finish with no supported candidate. It cannot establish physical validation, safety, manufacturability, real-race superiority, novelty, discovery, arbitrary-topology transfer, certified material allowables, or algorithm superiority from one campaign. Work 058 does not push or publish.
