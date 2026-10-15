# OE-038: Design Mining Interacting Wind Turbines

Thai companion: `OE-038_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | R. Preen, L. Bull |
| Year | 2016 |
| Venue | Evolutionary Computation |
| DOI | Not recorded |
| arXiv | 1410.0547 |
| Canonical record | [https://arxiv.org/abs/1410.0547](https://arxiv.org/abs/1410.0547) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-038_Preen2016_design-mining-interacting-wind-turbines.pdf) |
| Source SHA-256 | `a521beb06472d09093b8045844c5872fe7c7ea5195a3427051c9d931f8ca4a48` |
| Full-text coverage | 24/24 pages (100.00%); 10,885 extracted words |

## Research question

How does Design Mining Interacting Wind Turbines search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **physical-test evidence, empirical/experimental evidence, simulation/numerical evidence, mathematical/formal evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, methods, results, and frequent technical terms were wind, tness, species, used, evolutionary, design, evaluated, individual. The paper-specific method or result selected for transfer review is: **Evolves physical designs evaluated by 3D printing and wind-tunnel tests with surrogates**.

## Principal findings

- **Paper finding (conservative paraphrase):** Evolves physical designs evaluated by 3D printing and wind-tunnel tests with surrogates
- **Reviewer interpretation:** an example of physical evaluation in the loop
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** an example of physical evaluation in the loop This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Evolves physical designs evaluated by 3D printing and wind-tunnel tests with surrogates** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Evolves physical designs evaluated by 3D printing and wind-tunnel tests with surrogates' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 24 pages, 67,431 characters, 10,885 words.
- Pages with substantial extractable text: 24/24.
- High-information cue pages sampled from across the paper: 1, 2, 4, 6, 7, 8, 10, 11. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, methods, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
