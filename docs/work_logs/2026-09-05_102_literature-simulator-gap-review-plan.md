# Work 102 Plan: Literature and Simulator Gap Review

Thai companion: `2026-09-05_102_literature-simulator-gap-review-plan.th.md`

Status: Completed

## Objective and scope

Audit the current Formula Ultimate implementation and retained experimental evidence; find a broad, relevant body of primary research on autonomous morphology/design discovery, geometry, multi-fidelity optimization, vehicle/race simulation and validation; compare demonstrable capability with public evidence about professional F1 simulation.

Work 102 leaves roadmap numbers 098–101 available for their previously named implementation work. The inspected starting revision is `251ede5`.

## Planned files

- `docs/reports/LITERATURE_AND_SIMULATOR_GAP_REVIEW_2026-09-05.md` and `.th.md`.
- `docs/research/RELATED_WORK_CATALOG_2026-09-05.md` and `.th.md`.
- These two plans and matching bilingual result records.

## Sequence and validation

1. Read current source, tests, contracts, recent work results and available artifacts; distinguish code verification, cross-model agreement and physical validation.
2. Search and inspect primary academic and official industry sources; record exact titles, years, direct URLs, relevance, limitations and depth of access. Deduplicate publications and distinguish papers from industry evidence.
3. Produce an evidence-based gap matrix, prioritized reading list and falsifiable development recommendations without assuming conventional vehicle architecture.
4. Run `python -m unittest discover -s tests -q` to check the current baseline. This is software evidence, not physical validation. Record any skips or failures.
5. Check new Markdown companions, source IDs, URLs, repository evidence paths and numerical consistency with a scoped Python validation command; run `git diff --check` and `git diff --cached --check` before a scoped commit.

## Success and failure criteria

Success: a broad deduplicated primary-source catalog, current code-backed gap assessment, honest F1 comparison, equivalent bilingual deliverables and passing declared validation followed by a successful commit. No invented F1 accuracy, time-to-parity estimate, or unsupported discovery claim. Search breadth is bounded by retrievable public evidence; explicitly record inaccessible/full-text-unread items.

Failure: unsupported citations, stale-code assessment, missing companions, or failed validation unresolved at handoff. Keep status In progress or Stopped if a blocker prevents completion.

## Risks and controls

F1 model internals and calibration data are proprietary; use public capability evidence and label uncertainty. A source's abstract does not establish implementation detail. Passing unit tests does not validate a physical vehicle. Old artifact evidence is identified as retained rather than rerun. Search is broad but not a systematic-review claim.

## Non-goals

No physics/code/configuration changes, new simulation experiments, solver installation, spending, external publication, push, or claim of F1 regulatory compliance. This work recommends future experiments but does not execute them.
