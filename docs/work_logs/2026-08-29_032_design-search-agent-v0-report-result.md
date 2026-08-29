# Work 032 Result: Design Search Agent v0 Research Report

Status: Completed

Thai companion: `2026-08-29_032_design-search-agent-v0-report-result.th.md`

## Outcome

Created a bilingual, implementation-ready research plan for
`DesignSearchAgentV0`. The report separates Codex research orchestration from a
future deterministic search process and from non-agentic CAD/physics
evaluators. It recommends beginning with a functional loaded-interface-plate
experiment rather than whole-vehicle generation.

This work item created documentation only. No search agent, component grammar,
structural solver, candidate, or campaign was implemented or executed.

## Files Changed

- `docs/reports/DESIGN_SEARCH_AGENT_V0_PLAN.md`
- `docs/reports/DESIGN_SEARCH_AGENT_V0_PLAN.th.md`
- matching Work 032 plan/result records in English and Thai

## Decisions Recorded

1. Use a repository-owned seeded `(mu + lambda)` Python search process rather
   than an LLM as the numerical optimizer.
2. Keep Codex as a reviewed Research Orchestrator; deterministic code owns
   scientific pass/fail.
3. Prevent the search process from editing evaluators, budgets, tolerances,
   loads, promotion rules, Git, or arbitrary CAD code.
4. Make `loaded_interface_plate_v1` the first proposed functional task, with
   immutable interfaces, loads, keep-outs, material policy, and evidence gates.
5. Do not optimize mass until a load-transfer/structural feasibility gate
   exists.
6. Compare `GRID`, `RANDOM`, and `EVOLUTION` under equal attempted-evaluation
   counts, seeds, resources, solvers, and promotion rules.
7. Treat `64` attempts per treatment per seed, `10` seeds, and a `2%` practical
   effect threshold as provisional choices requiring a pilot and preregistration
   before results are observed.
8. Require replay, ablations, holdout loads, numerical refinement, independent
   promotion, optimized known alternatives, and exploit audit.

## Experiment Definition Recorded

- Independent variable: search treatment.
- Dependent variables: best feasible mass versus attempted evaluations,
  feasibility/failure distribution, time to target, holdout/promotion survival,
  residuals, diversity, compute, and replay agreement.
- Controls: grammar, interfaces, material, envelope, loads, constraints,
  evaluator versions, tolerances, resource caps, budget, seeds, and promotion
  rules.
- Preferred hypothesis: the evolutionary treatment lowers median
  best-feasible mass relative to both matched baselines while passing the same
  evidence and holdout gates.
- Failure criteria: unequal opportunity, missing failures, evaluator mutation,
  replay disagreement, no feasible treatment result, solver/geometry/interface
  failure, holdout rejection, or evidence of grammar/evaluator exploitation.

## Exact Validation

### Repository contract

Command:

```powershell
py -3.14 -m unittest tests.test_repository_contract -v
```

Exit code: `0`

Result: `Ran 6 tests in 2.173s ... OK` before the result records were added; a
final rerun after adding them also passed.

### Full regression

Command:

```powershell
py -3.14 -m unittest discover -s tests -q
```

Exit code: `0`

Result: `Ran 268 tests in 29.163s ... OK`.

### Whitespace and staged scope

Commands:

```powershell
git diff --check
git diff --cached --check
```

Exit codes: `0`, `0` in the final validation/staging sequence.

Result: no whitespace errors; only the six explicit Work 032 Markdown files
were staged.

## Claims Supported

- The project now has a concrete and falsifiable Design Search Agent v0 plan.
- The report defines roles, authority, first task, algorithm, evidence contract,
  fair treatments/budget, variables, metrics, decision rules, risks, and a
  seven-milestone implementation roadmap.

## Claims Explicitly Unsupported

- `DesignSearchAgentV0` is not implemented.
- No loaded component or autonomous candidate has been generated.
- No structural result, search advantage, physical validation, complete
  vehicle, novelty, or discovery is established.
- The provisional campaign budget and effect threshold are not final
  preregistration decisions or observed findings.

## Deviations from Plan

None. The work remained documentation-only and did not alter implementation or
experiment artifacts.

## Recommended Next Work

Implement Milestone 1 as a separate work item: define and validate the
`loaded_interface_plate_v1` functional interface, load, keep-out, material, and
failure contract before building the search loop.
