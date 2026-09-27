# OE-039: Keep Rollin' - Whole-Body Motion Control and Planning for Wheeled Quadrupedal Robots

Thai companion: `OE-039_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Marko Bjelonic, C. D. Bellicoso, Yvain de Viragh, Dhionis V. Sako, F. Tresoldi, Fabian Jenelten, Marco Hutter, N. Tsagarakis |
| Year | 2019 |
| Venue | IEEE Robotics and Automation Letters |
| DOI | Not recorded |
| arXiv | 1809.03557 |
| Canonical record | [https://arxiv.org/abs/1809.03557](https://arxiv.org/abs/1809.03557) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-039_Bjelonic2019_keep-rollin-whole-body-motion-control-and-planning.pdf) |
| Source SHA-256 | `2ac803b5f1f703f801142cab55c57b2fc20ae206b4e594d920cafcceca1d85af` |
| Full-text coverage | 8/8 pages (100.00%); 7,403 extracted words |

## Research question

How does Keep Rollin' - Whole-Body Motion Control and Planning for Wheeled Quadrupedal Robots search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **physical-test evidence, empirical/experimental evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were motion, robot, robots, contact, optimization, control, wheels, wheel. The paper-specific method or result selected for transfer review is: **Hybrid wheel-leg locomotion control**.

## Principal findings

- **Paper finding (conservative paraphrase):** Hybrid wheel-leg locomotion control
- **Reviewer interpretation:** shows what a non-conventional ground-contact endpoint demands from control
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** shows what a non-conventional ground-contact endpoint demands from control This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Hybrid wheel-leg locomotion control** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Hybrid wheel-leg locomotion control' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 8 pages, 43,986 characters, 7,403 words.
- Pages with substantial extractable text: 8/8.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 7. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
