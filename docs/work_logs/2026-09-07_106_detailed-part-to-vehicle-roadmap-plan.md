# Work 106 Plan: Detailed Part-to-Vehicle Discovery Roadmap

Thai companion: `2026-09-07_106_detailed-part-to-vehicle-roadmap-plan.th.md`

Date: 2026-09-07 (Asia/Bangkok)

Status: Completed

## Objective

Read the latest implementation and evidence, then define an actionable route to complete vehicle geometry, including internal parts and fastening details, without restricting discovery to familiar component shapes or conventional vehicle architectures. Shape freedom remains subject to explicit physics, task constraints, and evidence limits.

## Scope and inputs

This is a planning/documentation work item, not implementation of future solvers or a new vehicle experiment. Review Work 105 at commit `ea70f5f`, the Work 104 governing protocol, earlier CAD and assembly evidence, and the current morphology/network/intake code. Preserve all historical records. Use primary technical documentation only to bound possible infrastructure choices; do not install or select a production backend without benchmarks.

## Planned files

- `docs/reports/DETAILED_PART_TO_VEHICLE_DISCOVERY_ROADMAP_V1_2026-09-07.md` and its Thai companion.
- This plan and its Thai companion.
- Matching result log and its Thai companion.

No source, test, configuration, historical report, generated experiment output, or dependency changes are planned.

## Detailed approach

1. Separate currently demonstrated geometry, reduced-order physics, causal novelty, and vehicle readiness.
2. Define complete geometric detail independently from simulation resolution; specify material regions, voids, joints, internals, tolerances, ownership and multiscale model transfer.
3. Define an extensible representation and evaluator architecture, coupled component/vehicle search, accounting, falsification and promotion gates.
4. Break delivery into bounded work packages with dependencies, artifacts, tests, exit criteria, and an executable next-work specification.
5. Identify research uncertainty, computational bottlenecks, unsupported physics, hardware validation, and explicit non-goals.
6. Validate bilingual completeness and local links, review consistency with the governing protocol, and immediately commit only this work item's files after validation.

## Validation

- `python -m unittest tests.test_repository_contract -v` must exit `0`.
- Read-only document checks: paired files, Thai source identifiers, local Markdown links, matching roadmap section numbers, planned work identifiers and technical literals; command and results must be recorded in the result log.
- Manual review: each future package has dependencies and measurable exit evidence; unsupported geometry/physics is not relabeled physically impossible; continuous shape improvements are not excluded by graph novelty; exploratory integration is not restricted to isolated survivors.
- `git diff --check` and `git diff --cached --check` must exit `0`; inspect explicit staged paths before commit and verify the new commit afterward.

## Success criteria

The bilingual roadmap gives a reader a specific path from present bounded demonstrations to detailed parts and a coupled whole-vehicle candidate, including how to falsify each milestone. It identifies the immediate implementation step and does not claim that documentation, CAD success, or Level-0 simulation validates a physical vehicle. All six files are committed together.

## Risks and non-goals

Risks: overpromising arbitrary geometry, treating software limits as physical laws, becoming trapped in audit-only work, substituting visual detail for causal geometry, and confusing historical validation with newly executed tests. Mitigations are explicit coverage maps, an early geometry-to-field milestone, orthogonal evidence states, and attributed historical results.

Non-goals: implement the roadmap this turn; prescribe wheel count, body silhouette, powertrain or standard fasteners; prove novelty over external prior art; purchase/install tools; conduct physical tests; push or rewrite Git history; rewrite old plans to match new priorities.
