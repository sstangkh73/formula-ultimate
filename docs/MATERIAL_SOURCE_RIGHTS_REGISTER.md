# Material Source Rights Register

Thai companion: `MATERIAL_SOURCE_RIGHTS_REGISTER.th.md`

Reviewed: 2026-09-28

Status: Conservative repository admission record; not legal advice or source-owner permission

## Purpose

This register records the official public terms located for source families
named in the Formula Ultimate material-data policy. It decides only whether a
source is admitted to the public repository. It does not decide whether a
particular fact is copyrightable, whether an exception applies, or whether a
private use is lawful.

`restricted_private` is the default whenever exact redistribution authority is
missing or ambiguous. Source terms can change; recheck the controlling terms
before admitting a new record.

## Register

| Source family | Official evidence reviewed | Public-repository class | Repository decision |
|---|---|---|---|
| ASM International website and digital resources | [Website Terms of Use](https://www.asminternational.org/about-asm/legal-policies/terms-of-use-website/); [Digital Resources License Agreement](https://www.asminternational.org/about-asm/legal-policies/asm-digital-resources-license-agreement/); [permission process](https://www.asminternational.org/about-asm/contact/permission/) | `restricted_private` | Do not commit ASM content, exports, extracts, transformed records, or derived material unless exact written permission covering this repository use is obtained and recorded. |
| MatWeb database | [MatWeb License Agreement](https://www.matweb.com/reference/terms.aspx) | `restricted_private` | Do not commit MatWeb records or use them in AI/ML workflows. The public terms prohibit redistribution and public database release and impose specific AI/ML restrictions. |
| MMPDS handbook | [official purchase page](https://www.mmpds.org/purchase-handbook/); [official programme site](https://www.mmpds.org/) | `restricted_private` pending exact licence | The public pages establish handbook distribution/purchase but were insufficient to establish repository redistribution authority. Keep all MMPDS-derived records private until the exact edition and controlling licence grant public redistribution. |
| CMH-17 handbook distributed by SAE International | [CMH-17 purchase page](https://www.cmh17.org/RESOURCES/Purchase-Handbook); [SAE product record](https://saemobilus.sae.org/books/composite-materials-handbook-volume-3-revision-h-r-640) | `restricted_private` pending exact licence | Purchase availability and a product citation are not redistribution permission. Keep handbook data private until the exact volume/edition and controlling SAE terms or written permission are reviewed. |
| Supplier or manufacturer datasheets | Exact document and issuing site required | `restricted_private` by default | Review each document separately. A publicly viewable PDF or factual value is not, by itself, evidence that the repository may redistribute its text, tables, graphics, compilation, or contract-restricted content. |
| Government/open data or openly licensed source | Exact official legal source or licence required | Not admitted generically | May become `public_domain` or `open_licensed` only after record-level review identifies jurisdiction, licence/version, attribution/notice duties, and redistribution scope. |
| Direct written permission | Exact non-secret permission reference and scope required | Not admitted generically | May become `permission_granted` only when the permission covers the exact content, public Git redistribution, transformations/derived records if applicable, duration, territory, and intended use. |

## Legal distinctions used by the policy

- The U.S. Copyright Office states that facts are not protected by copyright,
  while original selection or arrangement of a factual database can be
  protected. See [Copyright FAQ](https://www.copyright.gov/help/faq/faq-protect.html)
  and [Automated Databases](https://www.copyright.gov/register/tx-databases.html).
- Thailand's Copyright Act recognizes protection for qualifying compilations or
  compositions of data. See the [WIPO Lex record and Act](https://www.wipo.int/wipolex/en/legislation/details/3801).
- Contract, confidentiality, database rights, and access terms can matter even
  where an individual fact is not copyrightable.
- Creative Commons advises licensors to secure the rights necessary for the
  permissions they grant and to mark material not subject to the licence. See
  the [CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode).

## Admission procedure for a new public source

1. Identify the exact document, database edition, URL, supplier, and access
   route used; do not rely on a source-family name alone.
2. Save the controlling terms privately, hash the exact evidence, and record
   the official public evidence URI when available.
3. Determine whether public redistribution, transformations, derived records,
   and the intended computational or AI use are expressly allowed.
4. Record attribution, notice, share-alike, non-commercial, no-derivatives,
   jurisdiction, duration, and revocation constraints as applicable.
5. If any required right is uncertain, classify the source
   `restricted_private` and stop public admission.
6. If admitted, add the machine-readable `publication_rights` block required by
   `MATERIAL_DATA_POLICY.md`, run the validator, and obtain human review.

## Current audit limits

- This review examined official public terms, not the contents or purchase
  contracts of files under `/private/`.
- No permission was requested or obtained in Work 147.
- No current public material record is admitted from ASM, MatWeb, MMPDS,
  CMH-17/SAE, or an unspecified supplier datasheet.
- This register is a repository control and cannot replace advice from a
  qualified lawyer familiar with the exact source contract and jurisdictions.
