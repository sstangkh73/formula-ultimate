# Material Data Rights and Publication Policy

Thai companion: `MATERIAL_DATA_POLICY.th.md`

Policy date: 2026-09-28

Status: Active repository policy; not legal advice

## Decision

Formula Ultimate publishes a material record only when the project has recorded
source-specific authority to redistribute that record. Whether a number is
"real" is not the legal test. Copyright in expression or compilation,
contractual access terms, database rights, confidentiality, and the law of the
relevant jurisdiction can impose different obligations.

Uncertain, restricted, purchased, account-gated, confidential, or
permission-pending material data stays under the gitignored `/private/`
boundary. Uncertainty fails closed: absence of a prohibition is not evidence of
permission.

The dated source review is in
[`MATERIAL_SOURCE_RIGHTS_REGISTER.md`](MATERIAL_SOURCE_RIGHTS_REGISTER.md).

## Publication-rights classes

| Class | Public repository treatment |
|---|---|
| `project_synthetic` | Allowed only when authored for this project, labelled synthetic, and prohibited from design or physical-validation claims. |
| `public_domain` | Allowed only with evidence identifying the public-domain basis and jurisdiction. |
| `open_licensed` | Allowed only within the exact licence terms, with source, licence, attribution, modification, and notice requirements preserved. |
| `permission_granted` | Allowed only within written permission whose scope covers repository redistribution and the intended record. |
| `restricted_private` | Never committed. This is also the default for unknown, unverified, purchased, account-gated, or source-specific terms not yet reviewed. |

An identifier, citation, or public URL does not by itself establish a right to
copy or redistribute the underlying content.

## Public material records

A public record with `evidence_status: "sourced"` must include a
`publication_rights` object containing:

- `status`: `public_domain`, `open_licensed`, or `permission_granted`;
- `redistribution_allowed: true`;
- `evidence_uri`: the controlling official licence, permission, or legal source;
- `evidence_sha256`: SHA-256 of the exact rights evidence reviewed;
- `verified_on`: an ISO `YYYY-MM-DD` date;
- `license_id` and required attribution/notice when an open licence applies, or
  a non-secret permission reference and scope when written permission applies.

The record must also retain the material source identity, conditions, units,
uncertainty, and property-to-source mapping required by its engineering
contract. Publication authority does not make a property technically suitable,
and technical evidence does not create publication authority.

## What must remain private

- source PDFs, handbook extracts, screenshots, tables, graphs, database exports,
  scraped records, account-gated content, and purchased electronic content;
- values or compilations obtained under terms that prohibit public
  redistribution or whose redistribution status has not been verified;
- permission correspondence containing confidential or personal information;
- derived tables, fitted models, or reports when the controlling terms restrict
  derivatives, or when the output reproduces or permits recovery of restricted
  source content;
- any record classified `restricted_private`.

Private records may be used only within their controlling terms. Keeping a file
out of Git does not itself grant permission to use it.

## What may remain public

- project-authored synthetic verification fixtures with
  `design_use_allowed=false`;
- analytic reference cases authored to verify equations, when they do not copy
  a protected source presentation or restricted dataset;
- source identifiers, official links, bibliographic citations, rights classes,
  and cryptographic hashes that do not disclose restricted content;
- project-authored code, schemas, validators, and solver logic that do not embed
  restricted source values;
- public-domain, open-licensed, or permission-granted records whose
  machine-readable rights evidence passes this policy;
- non-reversible public outcomes only after the source-specific terms have been
  checked to allow them. A pass/fail label is not automatically safe merely
  because it omits the input values.

The existing aluminium-like and other numerical fixtures are declared
project-authored synthetic verification inputs. Their familiar-looking values
are not sourced design allowables and cannot support material selection,
structural safety, fatigue life, manufacturing, or physical-validation claims.

## Private boundary and publication controls

1. Restricted records and source documents stay below `/private/`; never use
   `git add -f` on that path.
2. Code reading private records must fail closed when records or rights evidence
   are missing. It must never substitute a synthetic or built-in value silently.
3. Public results that depend on private data must disclose that dependency and
   must not expose restricted values or reversible derivatives.
4. Public references to private records use stable non-secret IDs and hashes.
   A recorded hash proves only identity for a person who lawfully possesses the
   same source bytes; the public cannot verify unseen private content.
5. Run `python scripts/validation/check_material_publication_boundary.py`
   before staging a material-policy or material-record change. The full test
   suite also runs this boundary check.
6. Human review remains mandatory. The validator cannot prove origin, interpret
   every licence, or detect a falsely labelled record.
7. Recheck controlling terms before each new source family is admitted and
   update the dated rights register in a separate bilingual work item.

## CC BY 4.0 interaction

[`LICENSE-DATA.md`](../LICENSE-DATA.md) licenses only original material over
which the project owner has authority to grant CC BY 4.0. It does not relicense
third-party content, restricted private data, or separately licensed material.
When a file contains separately licensed material, the file-specific notice and
source terms control that material.

## Engineering and reproducibility consequences

- A private sourced record can support only the claims permitted by its
  technical evidence and controlling terms; it does not become public merely
  because its hash is recorded.
- Public replay of a private-data result is unavailable unless an independently
  redistributable dataset is also supplied. Report this as a reproducibility
  limitation, not as public verification.
- A source marked `restricted_private` may not be used to train, fine-tune,
  evaluate, index, embed, or otherwise supply an AI/ML workflow unless its exact
  controlling terms expressly allow that use.
- If the rights evidence is ambiguous, stop publication and seek source-owner
  permission or qualified legal review.
