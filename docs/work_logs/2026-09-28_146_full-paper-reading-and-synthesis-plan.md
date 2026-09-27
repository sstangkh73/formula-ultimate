# Work 146 Plan: Full Paper Reading and Project Synthesis

Thai companion: `2026-09-28_146_full-paper-reading-and-synthesis-plan.th.md`

Date: 2026-09-28 (Asia/Bangkok)

Status: Completed

## Objective

Read every PDF currently present under `papers/`, produce an evidence-traceable report for each paper, and produce a cross-paper synthesis organized by the library's subject categories. The synthesis must identify what the literature establishes, what is especially interesting, how it connects to Formula Ultimate, and which concrete parts of the project should be improved.

## Scope

1. Inventory every local PDF and record its category, identifier, title, page count, and extraction status.
2. Read the complete extractable text of every PDF, including methods, results, limitations, and conclusions rather than relying only on titles or abstracts.
3. Create one separate bilingual Markdown report pair per paper.
4. Create one bilingual combined report pair organized by paper-library category, with cross-paper themes, disagreements, evidence gaps, and prioritized project actions.
5. Cross-check proposed actions against current Formula Ultimate architecture, validation boundaries, and existing research documentation.
6. Add reproducible tooling and machine-readable reading metadata where useful, without modifying the source PDFs.

## Planned files

- `docs/research/paper_reviews/FULL_LIBRARY_SYNTHESIS_2026-09-28.md` and `.th.md`.
- `docs/research/paper_reviews/by_paper/<paper-id>_review.md` and matching `.th.md` for every PDF.
- `docs/research/paper_reviews/reading_manifest.json` with source hash, pages, extraction coverage, and report paths.
- `scripts/research/extract_paper_corpus.py` and focused tests if extraction/validation automation is needed.
- This bilingual plan and the matching bilingual result record.

## Validation

1. The PDF inventory and reading manifest contain exactly the same set of local PDFs.
2. Every source PDF has exactly one English report and one Thai companion; every Thai report names its English source filename.
3. Every report includes bibliographic identity, research question, method/data, principal findings, limitations, Formula Ultimate connection, and actionable project changes, with page-level evidence references wherever extraction supports them.
4. The combined synthesis covers every library category and links every paper report.
5. Automated repository/document integrity tests pass, and a script verifies report counts, source hashes, bilingual pairing, required sections, and internal links.
6. `git diff --cached --check` passes for the explicit work-item staging set.

## Success criteria

- No local PDF is silently omitted.
- Per-paper reports distinguish author claims from our interpretation and do not imply that Level-0 results physically validate a design.
- Recommendations are tied to named Formula Ultimate modules, gates, protocols, or planned work rather than generic advice.
- The combined report explains both convergent evidence and contradictions or missing evidence across categories.
- Validation passes and the completed work item is committed as one scoped commit.

## Risks

- The library is large; complete-text extraction and synthesis may expose malformed, scanned, or encrypted PDFs. Such cases will be recorded explicitly and visually inspected where extraction is insufficient.
- Equations, tables, and figures can lose structure during text extraction. High-value or ambiguous evidence will be checked against rendered pages.
- A report can overstate evidence when a paper is conceptual, simulated, or benchmark-only. Each review will label evidence type and transfer limits.
- Existing unrelated working-tree changes must not enter this work item's commit.

## Explicit non-goals

- No change to physics, geometry, optimizer, controller, or experiment code in this work item.
- No claim that the literature search is exhaustive beyond the PDFs currently present in `papers/`.
- No redistribution, editing, or committing of source PDFs.
- No physical-validation claim based only on simulation or literature analogy.
