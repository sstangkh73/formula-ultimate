# VV-013: Deep Reinforcement Learning that Matters

Thai companion: `VV-013_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Peter Henderson, Riashat Islam, Philip Bachman, Joelle Pineau, Doina Precup, D. Meger |
| Year | 2018 |
| Venue | AAAI Conference on Artificial Intelligence |
| DOI | Not recorded |
| arXiv | 1709.06560 |
| Canonical record | [https://arxiv.org/abs/1709.06560](https://arxiv.org/abs/1709.06560) |
| Library topic | Verification, validation, uncertainty, statistics, and claims |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/13_validation_statistics_claims/VV-013_Henderson2018_deep-reinforcement-learning-that-matters.pdf) |
| Source SHA-256 | `0fc34bc1fb56746be58c2a4aa3d65b4b6fd7c732886edff368898ea00273e917` |
| Full-text coverage | 26/26 pages (100.00%); 12,917 extracted words |

## Research question

Which verification, validation, uncertainty, statistical, or claim failure does Deep Reinforcement Learning that Matters address, and what evidence discipline follows?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence, mathematical/formal evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, and frequent technical terms were network, policy, ddpg, trpo, average, timesteps, return, halfcheetah-v1. The paper-specific method or result selected for transfer review is: **Shows seeds, implementations and hyperparameters can flip conclusions**.

## Principal findings

- **Paper finding (conservative paraphrase):** Shows seeds, implementations and hyperparameters can flip conclusions
- **Reviewer interpretation:** motivates full replay metadata
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** motivates full replay metadata This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

These methods improve claim discipline but do not supply missing physical data or model validity; statistical correctness cannot rescue an inapplicable evaluator. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Shows seeds, implementations and hyperparameters can flip conclusions** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Validation Strategy, experiment registration schema, claim ledger, and independent evidence gates**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Validation Strategy, experiment registration schema, claim ledger, and independent evidence gates |
| Proposed change | Build a bounded diagnostic pilot from 'Shows seeds, implementations and hyperparameters can flip conclusions' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Apply the paper-derived check to a known-positive case, a falsifying negative control, repeated seeds/refinements, and a calibration-versus-holdout split; audit claim wording against outcomes. |
| Acceptance and failure evidence | Require predefined error/uncertainty bounds, correct rejection of invalid evidence, multiplicity-aware inference, deterministic provenance, and no retrospective repair. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 26 pages, 76,492 characters, 12,917 words.
- Pages with substantial extractable text: 26/26.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 7, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
