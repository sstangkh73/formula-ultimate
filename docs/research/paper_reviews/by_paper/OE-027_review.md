# OE-027: Evolution and learning in differentiable robots

Thai companion: `OE-027_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Luke Strgar, David Matthews, Tyler M Hummer, S. Kriegman |
| Year | 2024 |
| Venue | Robotics: Science and Systems Conference |
| DOI | Not recorded |
| arXiv | 2405.14712 |
| Canonical record | [https://arxiv.org/abs/2405.14712](https://arxiv.org/abs/2405.14712) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-027_Strgar2024_evolution-and-learning-in-differentiable-robots.pdf) |
| Source SHA-256 | `694a0cf06a0fd059ba71e9d7cab050ab3aa7cce11967f419f0b47e1c3560004f` |
| Full-text coverage | 16/16 pages (100.00%); 10,913 extracted words |

## Research question

How does Evolution and learning in differentiable robots search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **simulation/numerical evidence, optimization/search study, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were robots, robot, design, single, learning, springs, evolution, soft. The paper-specific method or result selected for transfer review is: **Combines evolution of bodies with gradient learning of control at scale**.

## Principal findings

- **Paper finding (conservative paraphrase):** Combines evolution of bodies with gradient learning of control at scale
- **Reviewer interpretation:** informs the split between discrete search and continuous refinement
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** informs the split between discrete search and continuous refinement This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Combines evolution of bodies with gradient learning of control at scale** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Combines evolution of bodies with gradient learning of control at scale' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 16 pages, 68,658 characters, 10,913 words.
- Pages with substantial extractable text: 16/16.
- High-information cue pages sampled from across the paper: 1, 6, 7, 9, 10, 12, 13. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
