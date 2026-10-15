# OE-008: Multi-Objective Graph Heuristic Search for Terrestrial Robot Design

Thai companion: `OE-008_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Jie Xu, A. Spielberg, Allan Zhao, D. Rus, W. Matusik |
| Year | 2021 |
| Venue | IEEE International Conference on Robotics and Automation |
| DOI | Not recorded |
| arXiv | 2107.05858 |
| Canonical record | [https://arxiv.org/abs/2107.05858](https://arxiv.org/abs/2107.05858) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-008_Xu2021_multi-objective-graph-heuristic-search-for-terrest.pdf) |
| Source SHA-256 | `0a1205adabbd27dca4822c262b99157dfab9f743749e55a84f501c17d4524f3f` |
| Full-text coverage | 7/7 pages (100.00%); 7,080 extracted words |

## Research question

How does Multi-Objective Graph Heuristic Search for Terrestrial Robot Design search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **optimization/search study, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were design, robot, pareto, multi-objective, designs, heuristic, search, algorithm. The paper-specific method or result selected for transfer review is: **Discrete graph design search under competing objectives**.

## Principal findings

- **Paper finding (conservative paraphrase):** Discrete graph design search under competing objectives
- **Reviewer interpretation:** a comparator for multi-objective race time, energy, mass and reliability (H2)
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a comparator for multi-objective race time, energy, mass and reliability (H2) This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Discrete graph design search under competing objectives** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Discrete graph design search under competing objectives' against the target below. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 7 pages, 43,134 characters, 7,080 words.
- Pages with substantial extractable text: 7/7.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 6. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
