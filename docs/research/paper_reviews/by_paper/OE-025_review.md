# OE-025: An End-to-End Differentiable Framework for Contact-Aware Robot Design

Thai companion: `OE-025_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Jie Xu, Tao Chen, Lara Zlokapa, Michael Foshey, W. Matusik, S. Sueda, Pulkit Agrawal |
| Year | 2021 |
| Venue | Robotics: Science and Systems Conference |
| DOI | Not recorded |
| arXiv | 2107.07501 |
| Canonical record | [https://arxiv.org/abs/2107.07501](https://arxiv.org/abs/2107.07501) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-025_Xu2021_an-end-to-end-differentiable-framework-for-contact.pdf) |
| Source SHA-256 | `5b9024538e03cdd0106940c268378317bcf38a538569bb824ca5b66c47c28d50` |
| Full-text coverage | 15/15 pages (100.00%); 11,228 extracted words |

## Research question

How does An End-to-End Differentiable Framework for Contact-Aware Robot Design search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, optimization/search study, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were morphology, design, parameterization, control, parameters, task, optimization, method. The paper-specific method or result selected for transfer review is: **Differentiable contact-aware design with cage-based deformation**.

## Principal findings

- **Paper finding (conservative paraphrase):** Differentiable contact-aware design with cage-based deformation
- **Reviewer interpretation:** relevant to ground-interaction and contact-driven geometry
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to ground-interaction and contact-driven geometry This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Differentiable contact-aware design with cage-based deformation** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Differentiable contact-aware design with cage-based deformation' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 15 pages, 70,422 characters, 11,228 words.
- Pages with substantial extractable text: 15/15.
- High-information cue pages sampled from across the paper: 1, 2, 4, 5, 8, 15. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
