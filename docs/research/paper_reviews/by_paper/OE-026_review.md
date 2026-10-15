# OE-026: SoftZoo: A Soft Robot Co-design Benchmark For Locomotion In Diverse Environments

Thai companion: `OE-026_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Tsun-Hsuan Wang, Ping-Chuan Ma, A. Spielberg, Zhou Xian, Hao Zhang, J. Tenenbaum, D. Rus, Chuang Gan |
| Year | 2023 |
| Venue | International Conference on Learning Representations |
| DOI | Not recorded |
| arXiv | 2303.09555 |
| Canonical record | [https://arxiv.org/abs/2303.09555](https://arxiv.org/abs/2303.09555) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-026_Wang2023_softzoo-a-soft-robot-co-design-benchmark-for-locom.pdf) |
| Source SHA-256 | `7e317aa800315ec4a2cd32e5fdef8877118c2340af07d230e2959d74a32bd166` |
| Full-text coverage | 20/20 pages (100.00%); 11,369 extracted words |

## Research question

How does SoftZoo: A Soft Robot Co-design Benchmark For Locomotion In Diverse Environments search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, simulation/numerical evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were design, robot, muscle, soft, optimization, differentiable, co-design, robots. The paper-specific method or result selected for transfer review is: **Co-design benchmark across diverse environments**.

## Principal findings

- **Paper finding (conservative paraphrase):** Co-design benchmark across diverse environments
- **Reviewer interpretation:** a pattern for running one search across several race environments and comparing specialisation
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a pattern for running one search across several race environments and comparing specialisation This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Co-design benchmark across diverse environments** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Co-design benchmark across diverse environments' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 20 pages, 70,063 characters, 11,369 words.
- Pages with substantial extractable text: 20/20.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 7, 19. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
