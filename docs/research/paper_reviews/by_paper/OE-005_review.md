# OE-005: Neural Graph Evolution: Towards Efficient Automatic Robot Design

Thai companion: `OE-005_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Tingwu Wang, Yuhao Zhou, S. Fidler, Jimmy Ba |
| Year | 2019 |
| Venue | International Conference on Learning Representations |
| DOI | Not recorded |
| arXiv | 1906.05370 |
| Canonical record | [https://arxiv.org/abs/1906.05370](https://arxiv.org/abs/1906.05370) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-005_Wang2019_neural-graph-evolution-towards-efficient-automatic.pdf) |
| Source SHA-256 | `267dbde264760f353cfb3d63d162a814f581a44a17896f7e9c4bcdb3dc1b2166` |
| Full-text coverage | 17/17 pages (100.00%); 9,300 extracted words |

## Research question

How does Neural Graph Evolution: Towards Efficient Automatic Robot Design search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, simulation/numerical evidence, optimization/search study, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, methods, and frequent technical terms were graph, species, search, model, policy, generation, neural, design. The paper-specific method or result selected for transfer review is: **Reuses graph-network controllers across morphology mutations to cut retraining cost**.

## Principal findings

- **Paper finding (conservative paraphrase):** Reuses graph-network controllers across morphology mutations to cut retraining cost
- **Reviewer interpretation:** relevant if every topology needs its own optimised driver
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant if every topology needs its own optimised driver This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Reuses graph-network controllers across morphology mutations to cut retraining cost** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Reuses graph-network controllers across morphology mutations to cut retraining cost' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 17 pages, 53,909 characters, 9,300 words.
- Pages with substantial extractable text: 17/17.
- High-information cue pages sampled from across the paper: 1, 2, 3, 6, 7, 8, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, methods.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
