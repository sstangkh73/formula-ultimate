# VV-029: Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World

Thai companion: `VV-029_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Joshua Tobin, Rachel Fong, Alex Ray, Jonas Schneider, Wojciech Zaremba, P. Abbeel |
| Year | 2017 |
| Venue | IEEE/RJS International Conference on Intelligent RObots and Systems |
| DOI | Not recorded |
| arXiv | 1703.06907 |
| Canonical record | [https://arxiv.org/abs/1703.06907](https://arxiv.org/abs/1703.06907) |
| Library topic | Verification, validation, uncertainty, statistics, and claims |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/13_validation_statistics_claims/VV-029_Tobin2017_domain-randomization-for-transferring-deep-neural.pdf) |
| Source SHA-256 | `3fc98c5f4cea050686d45858e647e1b704492121fdae80f8fcd5d560c107f11f` |
| Full-text coverage | 8/8 pages (100.00%); 6,579 extracted words |

## Research question

Which verification, validation, uncertainty, statistical, or claim failure does Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World address, and what evidence discipline follows?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were object, training, learning, real, data, arxiv, domain, images. The paper-specific method or result selected for transfer review is: **Randomising simulator parameters to transfer to reality**.

## Principal findings

- **Paper finding (conservative paraphrase):** Randomising simulator parameters to transfer to reality
- **Reviewer interpretation:** a robustness tactic for held-out conditions
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a robustness tactic for held-out conditions This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

These methods improve claim discipline but do not supply missing physical data or model validity; statistical correctness cannot rescue an inapplicable evaluator. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Randomising simulator parameters to transfer to reality** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Validation Strategy, experiment registration schema, claim ledger, and independent evidence gates**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Validation Strategy, experiment registration schema, claim ledger, and independent evidence gates |
| Proposed change | Build a bounded diagnostic pilot from 'Randomising simulator parameters to transfer to reality' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Apply the paper-derived check to a known-positive case, a falsifying negative control, repeated seeds/refinements, and a calibration-versus-holdout split; audit claim wording against outcomes. |
| Acceptance and failure evidence | Require predefined error/uncertainty bounds, correct rejection of invalid evidence, multiplicity-aware inference, deterministic provenance, and no retrospective repair. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 8 pages, 41,081 characters, 6,579 words.
- Pages with substantial extractable text: 8/8.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
