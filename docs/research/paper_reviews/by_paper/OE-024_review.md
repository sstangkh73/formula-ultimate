# OE-024: Transform2Act: Learning a Transform-and-Control Policy for Efficient Agent Design

Thai companion: `OE-024_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Ye Yuan, Yuda Song, Zhengyi Luo, Wen Sun, Kris M. Kitani |
| Year | 2022 |
| Venue | International Conference on Learning Representations |
| DOI | Not recorded |
| arXiv | 2110.03659 |
| Canonical record | [https://arxiv.org/abs/2110.03659](https://arxiv.org/abs/2110.03659) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-024_Yuan2022_transform2act-learning-a-transform-and-control-pol.pdf) |
| Source SHA-256 | `900a2230a2eb0618d54564cc9273bd27596f0f8dc10db169f4011332eb84308f` |
| Full-text coverage | 17/17 pages (100.00%); 9,709 extracted words |

## Research question

How does Transform2Act: Learning a Transform-and-Control Policy for Efficient Agent Design search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, optimization/search study, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were design, transform, agent, joint, policy, designs, environment, stage. The paper-specific method or result selected for transfer review is: **Policy that first edits the body graph then controls it**.

## Principal findings

- **Paper finding (conservative paraphrase):** Policy that first edits the body graph then controls it
- **Reviewer interpretation:** an alternative to evolutionary topology mutation worth comparing at equal budget
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** an alternative to evolutionary topology mutation worth comparing at equal budget This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Policy that first edits the body graph then controls it** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Policy that first edits the body graph then controls it' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 17 pages, 57,834 characters, 9,709 words.
- Pages with substantial extractable text: 17/17.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 7, 8, 12. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
