# Work 104 Plan: Whole-Vehicle and Technology Discovery Protocol

Thai companion: `2026-09-06_104_whole-vehicle-discovery-protocol-plan.th.md`

Date: 2026-09-06 (Asia/Bangkok)

Status: Completed

## Objective and scope

Write a dated, bilingual replacement execution protocol that connects open whole-vehicle architecture, executable morphology, multifunctional components, control, exploratory integration, and evidence promotion. Preserve exact backups of the previous generation-first roadmap before adding a supersession notice. Starting revision: `9889daf`; the inspected worktree is clean. Work 104 is documentation work; Works 098–101 remain reserved for implementation.

## Planned files

- `docs/contracts/WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md` and its `.th.md` companion.
- `docs/reports/GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.md` and its `.th.md` companion: add a dated link to the new protocol; preserve the historical body.
- `docs/reports/backups/2026-09-06_104/GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.md` and its `.th.md` companion: byte-identical pre-change copies.
- This bilingual plan and the matching bilingual result.

## Sequence

1. Create both plans with status `In progress`.
2. Copy and hash-check both old documents before modifying either source.
3. Write the new protocol and Thai translation; add supersession links to the old documents.
4. Validate backup identity, local links, companion coverage, contract content, and staged whitespace/scope.
5. Write results, mark plans `Completed` only after validation passes, stage only these files, commit, and verify the commit.

## Validation and success criteria

- Compare both backup byte streams against `git show 9889daf:<original-path>` using SHA-256 and byte equality.
- Verify that removing the new supersession notice recovers each original document exactly.
- Check the new protocol's date, version, English-source identification, matching numbered sections, technical identifiers, and equivalent equations/commands/numeric decisions in Thai.
- Resolve all relative Markdown links in the new protocol and new supersession notices. Byte-preserved backup links retain their original report-directory context and are not rewritten.
- Run `python -m unittest tests.test_repository_contract -q` and `git diff --check`.
- Inspect explicit staged file scope; run `git diff --cached --check`; create and verify one descriptive commit.
- Success means a reviewable bilingual protocol with preserved originals, explicit implementation boundaries, and no claim that documentation establishes a working vehicle or new technology.

## Risks and controls

- A replacement protocol could be confused with an implemented capability: distinguish normative target, software fixtures, exploratory evidence, and admitted physical evidence.
- Early component boundaries could prohibit useful coupled mechanisms: allow evolving internal boundaries and exploratory integration while retaining strict claim gates.
- Unfrozen science could permit result leakage: define immutable experiment registration, exploratory/admitted separation, and new identities for post-result design changes.
- Translation or archive drift: compare content and hashes, preserve exact backups, and keep both languages in one commit.

## Explicit non-goals

No simulator, physical law, CAD operator, scheduler, or search implementation; no admitted experiment; no hardware or novelty claim; no live regulatory update; no rewrite of older work logs; no push or publication.
