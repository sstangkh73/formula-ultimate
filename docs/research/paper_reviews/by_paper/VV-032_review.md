# VV-032: SALib: An open-source Python library for Sensitivity Analysis

Thai companion: `VV-032_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Jon Herman, Will Usher |
| Year | 2017 |
| Venue | The Journal of Open Source Software |
| DOI | 10.21105/joss.00097 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.21105/joss.00097](https://doi.org/10.21105/joss.00097) |
| Library topic | Verification, validation, uncertainty, statistics, and claims |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/13_validation_statistics_claims/VV-032_Herman2017_salib-an-open-source-python-library-for-sensitivit.pdf) |
| Source SHA-256 | `702455103000c4988ffa5b80079a40011a5edaaee90785df8ee598ace2741d2a` |
| Full-text coverage | 2/2 pages (100.00%); 638 extracted words |

## Research question

Which verification, validation, uncertainty, statistical, or claim failure does SALib: An open-source Python library for Sensitivity Analysis address, and what evidence discipline follows?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **technical/methodological study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were sensitivity, analysis, saltelli, global, andrea, salib, model, sobol. The paper-specific method or result selected for transfer review is: **Global sensitivity analysis tooling (Sobol, Morris)**.

## Principal findings

- **Paper finding (conservative paraphrase):** Global sensitivity analysis tooling (Sobol, Morris)
- **Reviewer interpretation:** for finding which parameters drive race-time rankings
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** for finding which parameters drive race-time rankings This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

These methods improve claim discipline but do not supply missing physical data or model validity; statistical correctness cannot rescue an inapplicable evaluator. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Global sensitivity analysis tooling (Sobol, Morris)** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Validation Strategy, experiment registration schema, claim ledger, and independent evidence gates**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Validation Strategy, experiment registration schema, claim ledger, and independent evidence gates |
| Proposed change | Build a bounded diagnostic pilot from 'Global sensitivity analysis tooling (Sobol, Morris)' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Apply the paper-derived check to a known-positive case, a falsifying negative control, repeated seeds/refinements, and a calibration-versus-holdout split; audit claim wording against outcomes. |
| Acceptance and failure evidence | Require predefined error/uncertainty bounds, correct rejection of invalid evidence, multiplicity-aware inference, deterministic provenance, and no retrospective repair. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 2 pages, 4,125 characters, 638 words.
- Pages with substantial extractable text: 2/2.
- High-information cue pages sampled from across the paper: 1. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
