# OE-007: DiffAqua: A Differentiable Computational Design Pipeline for Soft Underwater Swimmers with Shape Interpolation

Thai companion: `OE-007_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Ping-Chuan Ma, Tao Du, John Z. Zhang, Kui Wu, A. Spielberg, Robert K. Katzschmann, W. Matusik |
| Year | 2021 |
| Venue | ACM Transactions on Graphics |
| DOI | Not recorded |
| arXiv | 2104.00837 |
| Canonical record | [https://arxiv.org/abs/2104.00837](https://arxiv.org/abs/2104.00837) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-007_Ma2021_diffaqua-a-differentiable-computational-design-pip.pdf) |
| Source SHA-256 | `0e5d75ef7ae0c0bbeacc81d03e3902e07474963d5a233c85a91cccb37e15e779` |
| Full-text coverage | 14/14 pages (100.00%); 12,520 extracted words |

## Research question

How does DiffAqua: A Differentiable Computational Design Pipeline for Soft Underwater Swimmers with Shape Interpolation search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were introduction, results, and frequent technical terms were shape, design, control, soft, swimmer, differentiable, controller, swimmers. The paper-specific method or result selected for transfer review is: **Differentiable shape-and-control co-design**.

## Principal findings

- **Paper finding (conservative paraphrase):** Differentiable shape-and-control co-design
- **Reviewer interpretation:** a model for gradient refinement inside an admitted topology, not for topology change itself
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a model for gradient refinement inside an admitted topology, not for topology change itself This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Differentiable shape-and-control co-design** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Differentiable shape-and-control co-design' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 14 pages, 79,310 characters, 12,520 words.
- Pages with substantial extractable text: 14/14.
- High-information cue pages sampled from across the paper: 1, 2, 7, 8, 9, 10, 11, 12. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
