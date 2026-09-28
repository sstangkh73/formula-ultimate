# Work 147 Result: Material Licensing and Publication Boundary

Thai companion: `2026-09-28_147_material-licensing-publication-boundary-result.th.md`

Date: 2026-09-28

Status: Completed

## Outcome

Formula Ultimate now applies a conservative, source-rights-based publication
boundary to material data. The repository grants CC BY 4.0 only over original
project-authored content that the project owner is authorized to license. It
does not grant rights over third-party material, restricted databases,
standards, handbooks, papers, supplier documents, or private records.

This is risk reduction and an auditable engineering control, not a guarantee
of legal clearance. Source-specific licences, contracts, permissions, and
applicable law remain controlling.

## Files changed

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
- `docs/work_logs/2026-09-28_147_material-licensing-publication-boundary-plan.md`
- `docs/work_logs/2026-09-28_147_material-licensing-publication-boundary-plan.th.md`
- this result and its Thai companion

## Decisions

- The publication decision is based on documented source rights, not on
  whether an individual value is described as a fact or is publicly viewable.
- `project_synthetic`, `public_domain`, `open_licensed`,
  `permission_granted`, and `restricted_private` are distinct rights classes.
- ASM and MatWeb are classified `restricted_private` under the official terms
  reviewed on 2026-09-28.
- MMPDS, CMH-17/SAE, and supplier datasheets default to private use until the
  exact edition or document has redistribution evidence.
- A sourced public material record must include a machine-readable
  `publication_rights` record with an admitted status, redistribution
  authority, evidence URI, evidence SHA-256, and verification date. Required
  class-specific evidence is also enforced.
- Existing synthetic verification fixtures remain public only because they are
  project-authored and retain `claim_boundary.design_use_allowed=false`.
- `/private/`, files under `/papers/`, and common material-source document
  formats fail the publication-boundary check when they enter the candidate
  Git file set.
- Human provenance review remains mandatory because automated checks cannot
  establish ownership, interpret all contracts, or detect deliberate false
  labels.

## Validation evidence

All commands were run from `C:\Formula Ultimate`.

1. `python scripts/validation/check_material_publication_boundary.py`
   - Exit status: `0`
   - Relevant output: `material publication boundary: PASS`
2. `python -m unittest tests.test_material_publication_boundary -v`
   - Exit status: `0`
   - Relevant output: `Ran 7 tests`; `OK`
3. `python -m unittest discover -s tests -v`
   - Exit status: `0`
   - Relevant output: `Ran 1042 tests in 400.308s`; `OK (skipped=11)`
   - This successful run was executed outside the filesystem sandbox after the
     sandbox run demonstrated a temporary-directory permission failure.
4. `python -m py_compile scripts/validation/check_material_publication_boundary.py tests/test_material_publication_boundary.py`
   - Exit status: `0`
5. English/Thai companion and cross-link checks
   - Exit status: `0`
   - Relevant output: all Work 147 policy, register, licence, plan, and result
     companions present; source-filename references present.
6. `git diff --check`
   - Exit status: `0`

The first complete-suite attempt inside the filesystem sandbox ran 1,042 tests
but ended with 115 `PermissionError` errors and 11 skips in 358.688 seconds.
A minimal temporary-directory probe reproduced the same write denial. This was
an execution-environment failure, not a product-test assertion failure. The
same complete suite then passed outside that sandbox as recorded above.

The final staged-scope inspection, `git diff --cached --check`, commit identity,
and post-commit publication-boundary result are recorded in the final handoff
because their evidence can exist only after this result file is written.

## Limitations

- No repository policy or scanner can guarantee that future publication will
  have no legal risk.
- The rights register is a dated engineering decision record, not legal
  advice. Terms can change and must be rechecked for each new source or edition.
- A valid hash proves which evidence was reviewed; it does not create rights or
  prove that the reviewer interpreted the controlling terms correctly.
- The validator inspects the current Git candidate file set and structured JSON
  material records. It cannot prove provenance of arbitrary prose or detect a
  source that has been intentionally misidentified.
- Historical commits were not rewritten or audited exhaustively in this work.

## Follow-up work

- Before admitting any sourced material record, obtain and archive the exact
  licence or written permission privately, then add only the permitted public
  notice and evidence metadata.
- Recheck source terms and the applicable jurisdiction when a source, edition,
  licence, or intended use changes.
- Obtain qualified legal review before public release if the project intends to
  include values derived from commercial databases, standards, handbooks, or
  supplier documents.
