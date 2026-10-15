# OE-004: Evolution Gym: A Large-Scale Benchmark for Evolving Soft Robots

Thai companion: `OE-004_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Jagdeep Bhatia, Holly Jackson, Yunsheng Tian, Jie Xu, W. Matusik |
| Year | 2021 |
| Venue | Neural Information Processing Systems |
| DOI | Not recorded |
| arXiv | 2201.09863 |
| Canonical record | [https://arxiv.org/abs/2201.09863](https://arxiv.org/abs/2201.09863) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-004_Bhatia2021_evolution-gym-a-large-scale-benchmark-for-evolving.pdf) |
| Source SHA-256 | `dcc75b08a7fdb4e4e494ad76abfdb446596a48b9a321b4ba72adeac1b4872f09` |
| Full-text coverage | 39/39 pages (100.00%); 17,273 extracted words |

## Research question

How does Evolution Gym: A Large-Scale Benchmark for Evolving Soft Robots search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, optimization/search study, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, introduction, and frequent technical terms were uni00000013, robot, task, robots, uni00000048, uni00000055, algorithms, tasks. The paper-specific method or result selected for transfer review is: **Shared co-design benchmark with fixed tasks and budgets**.

## Principal findings

- **Paper finding (conservative paraphrase):** Shared co-design benchmark with fixed tasks and budgets
- **Reviewer interpretation:** borrow its benchmark discipline for fair GRID/RANDOM/EVOLUTION/QD comparisons
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** borrow its benchmark discipline for fair GRID/RANDOM/EVOLUTION/QD comparisons This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Shared co-design benchmark with fixed tasks and budgets** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Shared co-design benchmark with fixed tasks and budgets' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 39 pages, 112,727 characters, 17,273 words.
- Pages with substantial extractable text: 39/39.
- High-information cue pages sampled from across the paper: 1, 2, 3, 5, 7, 16, 36, 37. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
