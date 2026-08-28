# Work 020 Plan: Project Status and Direction Report

Status: Completed

Thai companion: `2026-08-28_020_project-status-direction-report-plan.th.md`

## Objective

Create a current, evidence-backed Markdown report that summarizes Formula
Ultimate from repository bootstrap through Work 019, distinguishes what is
implemented from what is only planned, identifies what is ready for use now,
and defines the recommended next research direction without weakening the
open-ended design mission or Level-0 claim boundary.

## Scope

- Reconstruct the completed work sequence from Git history and Work 001–019
  result records.
- Summarize the research objective, race/energy constraints, open 3D design
  boundary, governance, CAD evidence loop, ten real circuits, and physics stack.
- Classify capabilities as ready, partially ready, or not yet ready.
- State the current evidence level and explicitly prevent Level-0 results from
  being presented as physical validation or a complete race vehicle.
- Recommend a staged next direction that connects the existing independent
  models before opening autonomous whole-vehicle discovery.
- Produce separate English and Thai reports with equivalent technical facts,
  identifiers, commands, hashes, units, limitations, and recommendations.
- Add the matching bilingual result record, validate repository contracts, and
  create one verified commit.

## Planned files

- `docs/reports/PROJECT_STATUS_AND_DIRECTION_2026-08-28.md`
- `docs/reports/PROJECT_STATUS_AND_DIRECTION_2026-08-28.th.md`
- this bilingual plan/result pair
- separate bilingual problem reports if any issue is encountered

## Evidence inputs

- Current Git history through commit `0992f5c`.
- Bilingual Work 001–019 plan/result records.
- Research charter, design-language boundary, validation strategy, physics
  system plan, CAD documentation, circuit documentation, physics model
  documentation, queue status, source tree, validators, and tests.
- Fresh repository test and validator evidence collected during Work 020.

## Success criteria

- The report covers all major completed work without claiming absent coupling,
  autonomous search, complete-vehicle CAD, higher-fidelity validation, or real
  performance evidence.
- “Ready now,” “partially ready,” and “not ready” categories are unambiguous.
- The next direction is actionable, ordered, and compatible with fair baseline,
  conservation, reproducibility, and multi-fidelity requirements.
- English and Thai reports remain factually synchronized.
- Repository Markdown-contract tests, full unit tests, compilation, whitespace,
  staged-scope, commit, hash, and clean-tree checks pass.

## Risks

- Older README status text predates Work 010–019 and can understate the current
  Level-0 foundation; the new report must use current evidence without silently
  rewriting historical work records.
- A broad summary can blur the difference between independent component models
  and an integrated vehicle simulator.
- A roadmap can accidentally prescribe conventional vehicle architecture or
  imply empirical validity that the repository does not possess.

## Explicit non-goals

- No new physics law, model coupling, CAD component, autonomous optimizer,
  experiment, benchmark result, README rewrite, external research, or remote
  push.
- No claim that a complete vehicle, race-winning strategy, discovered
  technology, safety case, manufacturability case, or physical validation is
  ready.

## Review definition

- Independent variable: the evidence snapshot at commit `0992f5c`.
- Dependent output: report coverage, classification accuracy, limitations, and
  roadmap clarity.
- Controls: repository evidence only, explicit claim levels, bilingual parity,
  and no inference of unimplemented capability.
- Failure criteria: missing completed work, stale facts presented as current,
  undocumented extrapolation, Level-0 overclaim, language mismatch, repository
  gate failure, or failed commit.
- Falsification: search the report for claims of integration, optimization,
  discovery, complete-vehicle readiness, or physical validation and require a
  repository artifact or reclassify the claim.

## Validation

```powershell
python -m unittest tests.test_repository_contract -v
python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Every gate runs fail-fast. Completion requires synchronized bilingual reports
and results, explicit staging, a successful commit, and post-commit clean-state
and hash evidence.
