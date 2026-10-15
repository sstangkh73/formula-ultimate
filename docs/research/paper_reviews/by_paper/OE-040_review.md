# OE-040: Automated Antenna Design with Evolutionary Algorithms

Thai companion: `OE-040_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Gregory Hornby, Al Globus, Derek Linden, Jason Lohn |
| Year | 2006 |
| Venue | Space 2006 |
| DOI | 10.2514/6.2006-7242 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.2514/6.2006-7242](https://doi.org/10.2514/6.2006-7242) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-040_Hornby2006_automated-antenna-design-with-evolutionary-algorit.pdf) |
| Source SHA-256 | `f3012a5aa26dd280f654061f8d868f63d684adc20fffb531b17a73757656199a` |
| Full-text coverage | 11/11 pages (100.00%); 5,064 extracted words |

## Research question

How does Automated Antenna Design with Evolutionary Algorithms search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were antenna, design, gain, mission, antennas, evolutionary, evolved, nasa. The paper-specific method or result selected for transfer review is: **NASA ST5 evolved antenna that flew**.

## Principal findings

- **Paper finding (conservative paraphrase):** NASA ST5 evolved antenna that flew
- **Reviewer interpretation:** a rare case of an evolved, non-intuitive hardware design passing real qualification
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a rare case of an evolved, non-intuitive hardware design passing real qualification This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **NASA ST5 evolved antenna that flew** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'NASA ST5 evolved antenna that flew' against the target below. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 11 pages, 30,868 characters, 5,064 words.
- Pages with substantial extractable text: 11/11.
- High-information cue pages sampled from across the paper: 1, 4, 5, 6, 7, 11. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
