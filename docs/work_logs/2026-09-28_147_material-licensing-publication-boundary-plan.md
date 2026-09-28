# Work 147 Plan: Material Licensing and Publication Boundary

Thai companion: `2026-09-28_147_material-licensing-publication-boundary-plan.th.md`

Date: 2026-09-28

Status: Completed

## Objective

Replace the uncommitted material-data policy draft with a conservative,
source-rights-based publication boundary. Reduce the risk that Formula Ultimate
publishes third-party material data, documents, or derived records under CC BY
4.0 without authority, and add an automated fail-closed check for future
commits.

This work does not promise that legal risk can be eliminated. It records the
evidence checked, defaults uncertain sources to private use, and leaves final
legal interpretation to qualified counsel and the controlling source licence.

## Scope

- Audit the existing uncommitted material-policy, repository-licence, README,
  and `.gitignore` changes without publishing any private source content.
- Distinguish project-authored synthetic fixtures, public-domain/open-licensed
  data, permission-granted data, and restricted or unverified sources.
- Record a public source-rights register for ASM, MatWeb, MMPDS, CMH-17/SAE,
  and supplier datasheets using official terms available on 2026-09-28.
- Narrow the CC BY 4.0 grant to rights controlled by the project owner and mark
  third-party exclusions explicitly.
- Add a deterministic publication-boundary validator and tests. A material
  record intended for public design use must carry machine-readable evidence
  of redistribution authority; unknown or restricted sources fail closed.
- Preserve the existing synthetic verification fixtures and their explicit
  `design_use_allowed=false` boundary.

## Planned files

- `.gitignore`
- `LICENSE-DATA.md`
- `LICENSE-DATA.th.md`
- `README.md`
- `README.th.md`
- `docs/MATERIAL_DATA_POLICY.md`
- `docs/MATERIAL_DATA_POLICY.th.md`
- `docs/MATERIAL_SOURCE_RIGHTS_REGISTER.md`
- `docs/MATERIAL_SOURCE_RIGHTS_REGISTER.th.md`
- `scripts/validation/check_material_publication_boundary.py`
- `tests/test_material_publication_boundary.py`
- this plan and its Thai companion
- matching Work 147 English/Thai result records

## Validation

1. Run the publication-boundary validator against the repository.
2. Run focused unit tests for allowed synthetic/open records and rejected
   restricted, unknown, malformed, and `/private/` cases.
3. Run the complete unittest suite.
4. Compile the new Python files.
5. Check English/Thai companion presence and policy-link integrity.
6. Stage only the declared Work 147 files, inspect staged names, run
   `git diff --cached --check`, commit once, verify the commit hash, and rerun
   the publication-boundary validator after the commit.

## Success criteria

- No policy statement claims that all material-property facts are copyrighted
  or that every named source has identical terms.
- CC BY 4.0 is granted only over material the project owner is authorized to
  license, with third-party and separately licensed material excluded.
- ASM and MatWeb are treated as restricted; MMPDS, CMH-17/SAE, and supplier
  datasheets remain private until source-specific redistribution evidence is
  recorded.
- Publicly committed sourced material records cannot be design-eligible unless
  they include an admitted publication-rights classification and evidence.
- Existing synthetic fixtures remain reproducible and explicitly ineligible
  for physical-design claims.
- All declared validation and commit gates pass.

## Risks

- Copyright, contract, database-right, and jurisdiction questions are distinct;
  repository automation cannot replace legal advice.
- Source terms can change, so the register is dated and must be rechecked before
  new sourced data is published.
- A content scanner cannot prove origin or detect deliberate relabelling; human
  provenance review remains mandatory.
- Repository history can contain information not discoverable by filename or
  source-name searches.

## Explicit non-goals

- Do not publish, quote, summarize, enumerate, or modify files under `/private/`.
- Do not decide ownership of an individual third-party value without its exact
  source record and controlling terms.
- Do not obtain permissions, purchase licences, or provide legal advice.
- Do not change physical models, material values, candidate geometry, search,
  or experiment results.
- Do not push, publish, rewrite history, or amend existing commits.
