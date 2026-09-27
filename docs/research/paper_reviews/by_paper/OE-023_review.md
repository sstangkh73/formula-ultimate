# OE-023: Data-efficient Co-Adaptation of Morphology and Behaviour with Deep Reinforcement Learning

Thai companion: `OE-023_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | K. Luck, Heni Ben Amor, R. Calandra |
| Year | 2019 |
| Venue | Conference on Robot Learning |
| DOI | Not recorded |
| arXiv | 1911.06832 |
| Canonical record | [https://arxiv.org/abs/1911.06832](https://arxiv.org/abs/1911.06832) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-023_Luck2019_data-efficient-co-adaptation-of-morphology-and-beh.pdf) |
| Source SHA-256 | `405f01a876001de4ab176c2a54a9729ef199ee7acd93c4f4aaf405ed4959ff15` |
| Full-text coverage | 16/16 pages (100.00%); 9,554 extracted words |

## Research question

How does Data-efficient Co-Adaptation of Morphology and Behaviour with Deep Reinforcement Learning search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **physical-test evidence, empirical/experimental evidence, simulation/numerical evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were conclusion, introduction, and frequent technical terms were design, designs, learning, optimization, reward, reinforcement, function, simulation. The paper-specific method or result selected for transfer review is: **Uses learned value functions to evaluate new designs without full rollouts**.

## Principal findings

- **Paper finding (conservative paraphrase):** Uses learned value functions to evaluate new designs without full rollouts
- **Reviewer interpretation:** relevant to cheap pre-screening before Level-0 races
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to cheap pre-screening before Level-0 races This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Uses learned value functions to evaluate new designs without full rollouts** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Uses learned value functions to evaluate new designs without full rollouts' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 16 pages, 52,307 characters, 9,554 words.
- Pages with substantial extractable text: 16/16.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 8, 14. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
