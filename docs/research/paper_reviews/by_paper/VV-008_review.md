# VV-008: Verification, validation, and predictive capability in computational engineering and physics

Thai companion: `VV-008_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | William L Oberkampf, Timothy G Trucano, Charles Hirsch |
| Year | 2004 |
| Venue | Applied Mechanics Reviews |
| DOI | 10.1115/1.1767847 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1115/1.1767847](https://doi.org/10.1115/1.1767847) |
| Library topic | Verification, validation, uncertainty, statistics, and claims |
| Project relation | `direct` |
| Review depth | Decision-critical deep review |
| Source | [local PDF](../../../../papers/13_validation_statistics_claims/VV-008_Oberkampf2004_verification-validation-and-predictive-capability.pdf) |
| Source SHA-256 | `74df43945adc818c7718587e71058b31124b7d8255ee9b3e7f21e6bfaeaeca25` |
| Full-text coverage | 92/92 pages (100.00%); 42,720 extracted words |

## Research question

How should confidence in a computational prediction be built by separating code/solution verification from validation against experiments?

## Method and evidence

This 92-page engineering viewpoint synthesizes V&V practice: PIRT prioritization, code and calculation verification, grid convergence, validation hierarchies, experimental uncertainty, quantitative comparison, and inference from a validation domain to prediction (pp. 14, 21, 34, 48).

## Principal findings

- **Paper finding (conservative paraphrase):** Verification assesses accuracy in solving the computational model; validation assesses agreement with experimental reality for intended use. Validation requires numerical error, experimental uncertainty, and model discrepancy to remain distinct, and prediction outside the validation database requires weaker inference (pp. 3-4, 14, 21).
- **Reviewer interpretation:** A code can be verified while its model is invalid for the application; equally, experimental agreement at one tier does not automatically validate a complete-system prediction.
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** A code can be verified while its model is invalid for the application; equally, experimental agreement at one tier does not automatically validate a complete-system prediction. This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

This is a framework and viewpoint, not validation evidence for any Formula Ultimate solver. Its practices must be specialized into numerical thresholds, experiments, and intended-use domains for each physics evaluator. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **A code can be verified while its model is invalid for the application; equally, experimental agreement at one tier does not automatically validate a complete-system prediction.** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Validation Strategy, experiment registration schema, claim ledger, and independent evidence gates**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Validation Strategy, experiment registration schema, claim ledger, and independent evidence gates |
| Proposed change | Add an intended-use/V&V block to every evaluator identity: governing model, code-verification cases, refinement evidence, validation tier/data, discrepancy and uncertainty, applicability domain, and prohibited claim language. |
| Experiment and control | Apply the paper-derived check to a known-positive case, a falsifying negative control, repeated seeds/refinements, and a calibration-versus-holdout split; audit claim wording against outcomes. |
| Acceptance and failure evidence | Require predefined error/uncertainty bounds, correct rejection of invalid evidence, multiplicity-aware inference, deterministic provenance, and no retrospective repair. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 92 pages, 280,341 characters, 42,720 words.
- Pages with substantial extractable text: 92/92.
- High-information cue pages sampled from across the paper: 12, 14, 17, 21, 26, 29, 34, 35. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
