# Work 145 Result: Local Paper Library

Thai companion: `2026-09-27_145_paper-library-result.th.md`

Date: 2026-09-27 to 2026-09-28 (Asia/Bangkok)

Status: Completed

## Outcome

The library catalogues **411 papers** in 15 categories: 143 direct, 234 indirect and 34 data/findings. **261 PDFs are stored locally** in `papers/<category>/` (2.0 GB, git-ignored). Every one was identity-checked and matches its recorded SHA-256. The other 150 have an explicit status:

| Status | Papers | Meaning |
| --- | ---: | --- |
| `downloaded` | 261 | Local PDF; resolver identity confirmed and title words found on the first pages |
| `download_failed` | 60 | A source asserts a free copy, but the host refused scripted access; listed for browser download |
| `no_open_access_copy` | 90 | No source asserted a free copy; obtain through a library |
| `identity_unconfirmed` | 0 | — |

All 62 Work 102 papers (P01–P62) are included under their P-numbers, and 44 of them now have local copies. The catalog is [`PAPER_LIBRARY_2026-09-27.md`](../research/paper_library/PAPER_LIBRARY_2026-09-27.md).

| Category | Papers | Local PDF |
| --- | ---: | ---: |
| OE Open-ended, evolutionary and co-design discovery | 43 | 33 |
| AG LLM/AI agents for engineering, CAD code and simulation | 43 | 43 |
| QD Quality diversity, search, surrogates, multifidelity | 36 | 31 |
| CAD CAD, B-rep and assembly | 34 | 30 |
| ST Topology optimisation, meshing, FE, contact, failure | 24 | 9 |
| SI Simulation, optimal-control and MDO infrastructure | 21 | 12 |
| LT Minimum-lap-time control, vehicle dynamics, co-design | 32 | 11 |
| EN Race energy, powertrain and energy storage | 31 | 15 |
| TY Tyres and friction | 17 | 5 |
| AE Aerodynamics, CFD, datasets, surrogates | 33 | 22 |
| TH Thermal and cooling | 6 | 2 |
| MA Materials, joints, crash, manufacturing, tolerances | 15 | 2 |
| VV Verification, validation, statistics, claim discipline | 32 | 20 |
| AR Autonomous racing, telemetry, strategy | 27 | 23 |
| DS Design synthesis, functional representation, novelty | 17 | 3 |

Of the 261 downloads, 213 came from arXiv. The rest came from publisher open-access pages (Nature, Springer, IOP, PLOS, Frontiers), university repositories (Southampton, KU Leuven, Oxford ORA, HAL, Lund, Zenodo), author pages and NASA NTRS.

## Files changed

- `scripts/research/build_paper_library.py`: resolver, downloader, catalog generator, `--verify` and `--ingest`.
- `docs/research/paper_library/sources/01…15_*.json`: the curated list with bilingual relevance notes.
- `docs/research/paper_library/intro.json`: catalog introduction, bilingual. This file was not named in the plan.
- `docs/research/paper_library/manifest_v1.json`: generated identities, URLs, SHA-256, sizes and attempts.
- `docs/research/paper_library/PAPER_LIBRARY_2026-09-27.md` and `.th.md`: generated catalog.
- `tests/test_paper_library.py`: catalog integrity.
- `papers/.gitignore`: keeps every PDF out of version control.
- This bilingual plan and result.

No physics code, configuration, gate or claim changed. The user's uncommitted edits (`.gitignore`, `LICENSE-DATA.md`, `README*.md`, `docs/MATERIAL_DATA_POLICY*.md`) were left untouched and unstaged.

## Decisions

- **PDFs stay local.** The repository is public under CC BY 4.0, and most papers, including many open-access ones, may not be redistributed under that licence. Only metadata is committed. `papers/` ignores itself through its own `.gitignore`, so the root `.gitignore` with the user's pending edits was not touched.
- **Identity before storage.** Remembered arXiv IDs and DOIs were treated as hints. A file is saved only when:
  1. arXiv, Crossref or Semantic Scholar metadata matches the curated title, with similarity at least 0.86 (a DOI record may also match when its title is a subset of the curated one);
  2. at least 60 % of the significant title words appear on the PDF's first two pages.

  No DOI or arXiv hint was rejected in the final run. Wrong remembered titles were corrected against the source instead: AG-022, AG-042, SI-021, EN-018, LT-010 and LT-032, whose current titles differ from the ones first recorded.
- **Resolver chain changed during the work.** OpenAlex was planned, but its anonymous daily budget ran out after about 100 searches (HTTP 429, "Insufficient budget"; a key is now required). The chain became arXiv, then Crossref (with subtitles), then one batched Semantic Scholar call that supplies open-access PDF locations. OpenAlex remains available behind `--openalex`.
- **No bot check was bypassed.** Many open-access hosts answer scripts with a Cloudflare-style 403: MDPI, ACM (whose library is open access), PNAS, Royal Society, IEEE, T&F, Europe PMC, Cranfield, UniTN, Padova and TU/e. PMC and some repositories (DTU, mediaTUM) served interstitial or landing pages rather than PDFs. These were recorded, not circumvented. The client identifies itself honestly as a non-browser tool. That is also why HAL, which challenges browser-like clients, served its PDFs directly.
- **Untrusted mirrors not used.** Copies of MA-006 and MA-008 exist only on fan websites of unknown provenance, so they were not downloaded. Scribd, ResearchGate and similar hosts were not used either.
- **Manual completion path.** The 60 `download_failed` papers are listed in a table at the end of the catalog with their links. `--ingest <folder>` files hand-downloaded PDFs under the same identity rules.

## Validation

```text
Command: python scripts/research/build_paper_library.py --download
Exit code: 0
Result: {"papers": 411, "downloaded": 242, "no_open_access_copy": 102, "identity_unconfirmed": 0, "download_failed": 67}

Command: python scripts/research/build_paper_library.py --download --only <169 non-downloaded or corrected ids>
Exit code: 1 (crash at item 153/169)
Result: OSError: [Errno 22] Invalid argument writing manifest_v1.json (Windows transient lock while another process read it).
Fix: manifest writes go to a temporary file and are replaced atomically with retries (write_manifest).

Command: python scripts/research/build_paper_library.py --download --only AR-016,AR-024,DS-001,…,DS-016   (the 16 not reached)
Exit code: 0
Result: {"papers": 411, "downloaded": 258, "no_open_access_copy": 94, "identity_unconfirmed": 0, "download_failed": 59}

Command: python scripts/research/build_paper_library.py --download --only SI-007,LT-010,TY-010,DS-008,LT-018,AE-032
Exit code: 0
Result: {"papers": 411, "downloaded": 261, "no_open_access_copy": 90, "identity_unconfirmed": 0, "download_failed": 60}

Command: --ingest negative test (the OE-001 PDF copied in as "OE-003.pdf" and as "unnamed.pdf")
First result: "OE-003.pdf" refused; "unnamed.pdf" WRONGLY filed as DS-007 ("Development of a Functional Basis for Design"),
              because that short generic title's words all occur in the Sims paper.
Fix: an unnamed file must contain exactly one pending catalog title as a contiguous phrase on its first pages;
     an ID-named file needs the phrase or word coverage >= 0.8. The wrong file was deleted and DS-007 restored
     (--download --only DS-007: no_open_access_copy).
Re-test: both negatives refused; a correct unnamed PDF (ST-003) is filed. Run in a scratch copy, not the real manifest.

Command: python scripts/research/build_paper_library.py --verify
Exit code: 0
Result: {"downloaded_checked": 261, "problems": 0}   (exists, starts with %PDF, SHA-256 and size match)

Command: title-phrase audit of all 261 local PDFs (first two pages)
Result: 254 contain the curated title as a phrase. 7 were inspected by hand and are the right papers:
  OE-040 (scanned NASA title), ST-011 ("3-D" vs "three-dimensional"), LT-005 ("Optimising"),
  VV-024 ("ML-based"), AR-005 (preprint template header), AR-023 ("physics-constrained" preprint title),
  DS-012 (the authors' KU Leuven working-paper version, "Identifying ex ante characteristics of radical
  inventions through patent-based indicators", of the Research Policy article).

Command: python -m unittest tests.test_paper_library tests.test_repository_contract
Exit code: 0
Result: Ran 12 tests — OK

Command: python -m compileall -q scripts src tests ; git diff --cached --check
Exit code: 0

Command: git status --short --ignored papers
Result: only papers/.gitignore is untracked; every category folder is ignored (!!). No PDF is staged.
```

## Claims

- Supported: 411 related papers are catalogued with bilingual notes. 261 identity-checked PDFs are on disk, and each matches its recorded hash. Every paper has an explicit acquisition status.
- Not supported:
  - that the search is exhaustive;
  - that the relevance notes come from reading each paper in full (most come from abstracts and known content);
  - that any listed method works for this project;
  - that finding no direct competitor shows novelty.

## Limitations and follow-up

- 60 open-access papers still need a browser download. The table at the end of the catalog lists them. Save them into a folder and run `python scripts/research/build_paper_library.py --ingest <folder>`; naming files `<ID>.pdf` makes the match explicit.
- 90 papers have no free copy, including closed classics (for example Bendsøe & Kikuchi 1988, NSGA-II, Katz 2006, the Pacejka papers, Junker 1969) and several Taylor & Francis VSD papers. They need institutional access.
- osti.gov is unreachable from this network (TCP connect failure). VV-001 and VV-004 have OSTI copies that may download from another network.
- OpenAlex needs an API key for anonymous-scale use. Rerunning with `--openalex` and a key may find more repository copies.
- The library is large (2.0 GB). Graphics papers are the biggest files, up to 75 MB each.
- Suggested next work: re-rank the Work 102 gap review against the new categories, especially CAD-013 to CAD-016, DS-013 to DS-015 (assembly and joint synthesis for part resolution), LT-011, LT-012 and LT-022 to LT-025 (co-design lap solvers), and AE-022 to AE-024 (surrogates outside their training distribution).
