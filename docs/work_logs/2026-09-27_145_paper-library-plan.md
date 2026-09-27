# Work 145 Plan: Local Paper Library

Thai companion: `2026-09-27_145_paper-library-plan.th.md`

Date: 2026-09-27 (Asia/Bangkok)

Status: Completed

## Objective

Find papers that bear on Formula Ultimate directly (the same kind of objective or method) and indirectly (a method, dataset or measurement the project could adopt), with no fixed upper limit on count. Download every paper that has a lawful open-access copy into a separate local project folder, and record, for every paper found, why it matters and whether a local copy exists.

## Entry evidence

- Work 102 produced `docs/research/RELATED_WORK_CATALOG_2026-09-05.md`: 62 academic works (P01–P62), each with links but no local copies, and states that "no external research code or large dataset was run/downloaded".
- Works 103–144 moved the project into areas that catalog covers thinly or not at all: B-rep and CAD-code generation, assembly joints and fasteners, onboard energy realization, flow and heat exchange, material failure, manufacturing tolerance, part resolution and physical correlation.
- The user asked on 2026-09-27 for an unlimited related-paper search, including papers whose findings or data the project can use, downloaded into a separate folder.

## Scope

1. A curated source list covering the topics the project actually works on: open-ended and automated design, morphology/control co-design, quality diversity and multifidelity search, CAD/B-rep/assembly generation, topology optimization, meshing and contact, minimum-lap-time optimal control and design/control co-optimization, race energy management, tyres, aerodynamics and aero datasets, energy storage and powertrain, thermal and cooling, materials, fatigue, joints and tolerances, verification/validation/UQ, statistics and reproducibility, specification gaming, and autonomous racing data.
2. The existing P01–P62 are included so that the library is complete in one place.
3. A resolver/downloader that confirms each paper's identity against arXiv or OpenAlex metadata before accepting a file, downloads only from the resolved open-access location, checks that the file is a PDF, and records SHA-256, size, URL and status.
4. A bilingual human-readable catalog generated from the same source list.

## Planned files

- `docs/research/paper_library/sources_v1.json` — curated list: id, category, title, authors, year, venue, identifiers, relation (direct/indirect/data), English and Thai relevance notes.
- `docs/research/paper_library/manifest_v1.json` — generated: resolved identity, download URL, SHA-256, bytes, local path, status.
- `docs/research/paper_library/PAPER_LIBRARY_2026-09-27.md` and `.th.md` — generated catalog.
- `scripts/research/build_paper_library.py` — resolver, downloader and catalog generator.
- `tests/test_paper_library.py` — catalog integrity (unique ids, required fields, categories, manifest/source agreement).
- `papers/.gitignore` — keeps the downloaded PDFs local.
- `papers/<category>/*.pdf` — local only, not committed.
- This bilingual plan and the matching bilingual result.

## Storage and licensing decision

The repository is pushed publicly and its documents are licensed CC BY 4.0. Most papers, including many open-access ones, are not redistributable under that licence. The PDFs therefore stay in `papers/`, which is git-ignored by its own `papers/.gitignore`; only metadata (titles, identifiers, URLs, hashes, notes) is committed. The root `.gitignore`, which has uncommitted user changes, is not touched.

## Validation

1. `python scripts/research/build_paper_library.py --download` completes; every entry ends in a recorded status (`downloaded`, `no_open_access_copy`, `identity_unconfirmed`, or `download_failed`) and none is silently dropped.
2. Every `downloaded` file starts with `%PDF`, its SHA-256 matches the manifest, and its resolved title matches the curated title.
3. `python -m unittest tests.test_paper_library tests.test_repository_contract`: exit 0.
4. `git status --short papers` shows no PDF; `git diff --cached --check`: exit 0.

## Success and failure criteria

Success: a catalog substantially larger than the 62 Work 102 papers, covering every topic in scope; every catalogued paper either has a verified local PDF or an explicit reason why not; PDFs are not staged.

Failure: a file is saved under the wrong paper's name (identity not checked), a download comes from an unlawful mirror, a PDF is committed, or a paper is claimed as downloaded without a hash.

## Risks

- Remembered arXiv identifiers or DOIs can be wrong. Mitigation: identity is confirmed against resolver metadata by title similarity; mismatches are recorded, not saved under the curated name.
- Some publisher PDFs sit behind bot checks. Those are recorded as `download_failed` or `no_open_access_copy` with the landing link; no CAPTCHA or access control is bypassed.
- A related-work search is never exhaustive. The result will say so.
- Relevance notes are informed judgement from abstracts and known content, not a full reading of every paper.

## Non-goals

- No sci-hub or other unlicensed mirrors; no paywalled download.
- No change to physics code, configurations, gates or claims.
- No re-rating of the Work 102 catalog; P01–P62 keep their own entries and the new library references them by P-number.
- No statement that the project is novel because a search did not find a competitor.
