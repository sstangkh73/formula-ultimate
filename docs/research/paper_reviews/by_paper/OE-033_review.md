# OE-033: Shape Your Body: Value Gradients for Multi-Embodiment Robot Design

Thai companion: `OE-033_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Nico Bohlinger, Jan Peters |
| Year | 2026 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2606.00702 |
| Canonical record | [https://arxiv.org/abs/2606.00702](https://arxiv.org/abs/2606.00702) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-033_Bohlinger2026_shape-your-body-value-gradients-for-multi-embodime.pdf) |
| Source SHA-256 | `00e8f5b45b88da847c66c97bd2a506b39c7cc697b74a77fb9dbab3d8f3cb3cb1` |
| Full-text coverage | 27/27 pages (100.00%); 11,760 extracted words |

## Research question

How does Shape Your Body: Value Gradients for Multi-Embodiment Robot Design search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, optimization/search study, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were conclusion, introduction, limitations, results, and frequent technical terms were design, robot, value, policy, learning, training, critic, designs. The paper-specific method or result selected for transfer review is: **Uses value gradients of a multi-embodiment policy to improve body design**.

## Principal findings

- **Paper finding (conservative paraphrase):** Uses value gradients of a multi-embodiment policy to improve body design
- **Reviewer interpretation:** a continuous-design comparator
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a continuous-design comparator This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **present** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Uses value gradients of a multi-embodiment policy to improve body design** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Uses value gradients of a multi-embodiment policy to improve body design' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 27 pages, 71,539 characters, 11,760 words.
- Pages with substantial extractable text: 27/27.
- High-information cue pages sampled from across the paper: 1, 2, 3, 6, 7, 8, 19, 22. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion, introduction, limitations, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
