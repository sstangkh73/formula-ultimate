# Work 107 Plan: Detailed Work-Package Plans

Thai companion: `2026-09-07_107_detailed-work-package-plans-plan.th.md`

Date: 2026-09-07 (Asia/Bangkok)

Continued: 2026-09-09 (Asia/Bangkok); original start date and scope preserved.

Status: Completed

## Objective and scope

Expand the Work 106 roadmap into individual executable planning specifications for all 26 proposed packages. This documentation work consumes actual Work 107; map the previously tentative 107–132 packages to proposed implementation Works 108–133 without rewriting Work 106 history. Future numbers remain provisional until execution starts.

## Planned files

- `docs/plans/detailed_part_to_vehicle_v1/README.md` and Thai companion: numbering, dependencies, common registration requirements and index.
- 26 individual `workNNN-<slug>.md` plans in that directory, each with a separate Thai companion.
- This bilingual plan and matching bilingual result: 58 Markdown files in total.

No runtime code, configuration, dependency, historical roadmap, experiment artifact or future work-log status changes are planned. Proposed source paths and commands must be labeled unimplemented.

## Approach

For each package specify objective, entry conditions, source inputs, proposed files, ordered implementation steps, variables/controls, targeted tests and negative controls, numerical registration fields, acceptance/failure conditions, evidence products, risks, non-goals and handoff. Keep unfamiliar shape freedom, real internal hardware, multiscale evidence, fair accounting and early exploratory integration. Distinguish documentary completion from engineering and scientific success.

## Validation and success criteria

- `python -m unittest tests.test_repository_contract -v` exits `0`.
- Read-only checks verify 26 contiguous plans and companions, links, matching technical literals/commands, required sections, old-to-new numbering, dependency validity and absence of cycles.
- Manual review verifies all work packages have actionable steps and falsification tests, no unapproved physical testing, no claimed backend implementation, and no unsupported numerical tolerance disguised as a law.
- Stage exactly 58 paths; inspect scope and run `git diff --cached --check` before a descriptive commit. Verify hash and clean status; do not push.

## Risks and non-goals

Number shifts may confuse execution: preserve explicit mapping and treat dependencies as capability requirements. Large packages may need subdivision: define boundaries and stop rules before implementation rather than claim a whole domain from one fixture. This work does not execute any proposed implementation, install solvers, choose a vehicle architecture, reserve resources, fabricate hardware or prove discovery. No calendar estimate is promised without cost pilots.
