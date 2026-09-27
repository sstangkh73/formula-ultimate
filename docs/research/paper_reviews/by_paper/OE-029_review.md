# OE-029: An Empirical Study on the Computation Budget of Co-Optimization of Robot Design and Control in Simulation

Thai companion: `OE-029_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Etor Arza, Frank Veenstra, T. Nygaard, Kyrre Glette |
| Year | 2024 |
| Venue | arXiv |
| DOI | Not recorded |
| arXiv | 2409.08621 |
| Canonical record | [https://arxiv.org/abs/2409.08621](https://arxiv.org/abs/2409.08621) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-029_Arza2024_an-empirical-study-on-the-computation-budget-of-co.pdf) |
| Source SHA-256 | `692767090d0cbbae61219741368aa1b0080916189498a1aa0225de9f39665765` |
| Full-text coverage | 14/14 pages (100.00%); 7,113 extracted words |

## Research question

How does An Empirical Study on the Computation Budget of Co-Optimization of Robot Design and Control in Simulation search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **physical-test evidence, empirical/experimental evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, and frequent technical terms were design, budget, controller, co-optimization, control, computation, best, complexity. The paper-specific method or result selected for transfer review is: **Quantifies how the split of compute between design and control changes co-optimisation outcomes**.

## Principal findings

- **Paper finding (conservative paraphrase):** Quantifies how the split of compute between design and control changes co-optimisation outcomes
- **Reviewer interpretation:** directly relevant to budget-matched fairness rules
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** directly relevant to budget-matched fairness rules This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Quantifies how the split of compute between design and control changes co-optimisation outcomes** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Quantifies how the split of compute between design and control changes co-optimisation outcomes' against the target below. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 14 pages, 44,420 characters, 7,113 words.
- Pages with substantial extractable text: 14/14.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 7, 9, 11. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
