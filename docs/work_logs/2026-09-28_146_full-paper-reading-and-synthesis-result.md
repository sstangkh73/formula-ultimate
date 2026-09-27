# Work 146 Result: Full Paper Reading and Project Synthesis

Thai companion: `2026-09-28_146_full-paper-reading-and-synthesis-result.th.md`

Date: 2026-09-28 (Asia/Bangkok)

Status: Completed

## Outcome

The complete local library of 261 PDFs was inventoried, extracted page by page, and represented by 261 English/Thai report pairs. A bilingual cross-library synthesis now organizes the findings, notable results, Formula Ultimate connections, evidence gaps, and prioritized project changes across all 15 library topics.

The corpus contains 6,280 pages and 3,503,351 extracted words. Fifteen decision-critical papers received deeper method/result/limitation reviews with pinpoint page references. The remaining 246 reports are explicitly labeled full-text transfer records rather than equivalent replications or deep critical reviews.

## Files changed

- `docs/research/paper_reviews/FULL_LIBRARY_SYNTHESIS_2026-09-28.md`
- `docs/research/paper_reviews/FULL_LIBRARY_SYNTHESIS_2026-09-28.th.md`
- `docs/research/paper_reviews/by_paper/`: 261 English reports and 261 Thai companions.
- `docs/research/paper_reviews/reading_manifest.json`: source identity, hash, coverage, section/evidence-page locators, bibliography, and report paths for all 261 PDFs.
- `scripts/research/extract_paper_corpus.py`: deterministic inventory, extraction, metadata generation, and report validation.
- `scripts/research/generate_paper_review_reports.py`: reproducible bilingual report and synthesis generation.
- `tests/test_paper_reviews.py`: inventory, coverage, privacy/size boundary, bilingual parity, links, depth, and schema regression checks.
- This bilingual plan/result record.

The source PDFs were not modified or staged. Pre-existing changes to `.gitignore`, `LICENSE-DATA.md`, `README.md`, `README.th.md`, `docs/MATERIAL_DATA_POLICY.md`, and `docs/MATERIAL_DATA_POLICY.th.md` were preserved outside this work item.

## Decisions and evidence handling

1. Separate paper findings, reviewer interpretation, and project proposals in every report.
2. Use two disclosed review depths: 15 decision-critical deep reviews and 246 full-text transfer records. Extraction completion is not presented as independent replication.
3. Give every paper a distinct transfer proposal with target artifact/module, proposed change, experiment/control, and acceptance/failure evidence.
4. Keep verbatim extracted text in ignored local artifacts; publish only compact provenance and page locators in `reading_manifest.json`.
5. Treat automatic cue-page and evidence-profile labels as navigation aids, never as evidence grades.
6. Visually inspect representative low-text pages. The six sources below 95% substantial-text coverage contained figure-only CFD/geometry/diagram/dataset pages or a blank trailing page; no unreadable scanned source was found.
7. Correct the EN-012 interpretation: the paper supports a sizing-versus-control fidelity distinction and does not establish a generic architecture-ranking reversal.
8. Preserve the project boundary that literature and Level-0 simulation can support selection and falsification, but cannot by themselves physically validate a vehicle.

## Fresh-reader review

An independent fresh-reader pass found that the initial per-paper output was too templated, project changes were insufficiently paper-derived, important claims lacked auditability, the synthesis's interesting sections were generic, bibliography was incomplete, and one Thai agent-authority sentence was ambiguous. The reports were regenerated to address those findings with distinct questions/proposals, bibliographic records, explicit claim roles, transfer tables, named synthesis anchors, 15 deep reviews, and corrected Thai wording.

A requested second fresh-reader pass could not complete because the reviewing agent hit the service usage limit. Final automated and manual content audits were therefore performed in the primary task.

## Validation

All commands were run from `C:\Formula Ultimate`.

### Python syntax

Command:

```powershell
python -m py_compile scripts/research/extract_paper_corpus.py scripts/research/generate_paper_review_reports.py tests/test_paper_reviews.py
```

Exit status: `0`. Output: none.

### Corpus and report validation

Command:

```powershell
python scripts/research/extract_paper_corpus.py --validate-reports
```

Exit status: `0`.

```text
Validated 261 PDFs; pages=6280; words=3503351
```

### Repository tests

Command:

```powershell
python -m unittest tests.test_paper_library tests.test_paper_reviews tests.test_repository_contract
```

Exit status: `0`.

```text
...................
----------------------------------------------------------------------
Ran 19 tests in 0.892s

OK
```

### Content audit

PowerShell count/search audit exit status: `0`.

```text
EN_REPORTS=261
TH_REPORTS=261
DEEP_REVIEWS=15
PROPOSALS=261
UNIQUE_PROPOSALS=261
OVERCLAIM_PHRASE=absent
PAPER_TREE_CHANGES=none
```

The staged-scope check and `git diff --cached --check` are recorded by the commit workflow immediately after this result record.

## Limitations

- The reports cover every PDF currently in the local library, not all literature in the field.
- Full-text extraction does not preserve every equation, table, or figure layout. Decision-critical claims should still be checked against the cited source pages before implementation.
- Only 15 papers received deep critical reviews in this work item. The other 246 reports are traceable transfer records intended for triage and project planning, not substitutes for independent replication.
- No proposed model, controller, geometry, material law, or experiment was implemented or physically validated here.
- Bibliographic fields are limited to identifiers recoverable from the local sources and library metadata; unavailable DOI or venue fields are marked accordingly.

## Follow-up work

1. Deepen additional per-paper reviews when a paper becomes decision-critical for a specific work item.
2. Convert the prioritized synthesis actions into separately planned experiments with fixed controls, metrics, falsification criteria, and deterministic replay metadata.
3. Begin with transient tyre/contact evidence, aerodynamic field validation, energy/thermal endurance closure, independent structural evidence, tolerance/fatigue, and coupled whole-vehicle replay.
4. Record implementation evidence separately; do not promote a design from literature analogy or Level-0 simulation alone.
