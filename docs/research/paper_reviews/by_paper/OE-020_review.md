# OE-020: Efficient automatic design of robots

Thai companion: `OE-020_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | David Matthews, Andrew Spielberg, Daniela Rus, Sam Kriegman, Josh Bongard |
| Year | 2023 |
| Venue | Proceedings of the National Academy of Sciences |
| DOI | 10.1073/pnas.2305180120 |
| arXiv | 2306.03263 |
| Canonical record | [https://doi.org/10.1073/pnas.2305180120](https://doi.org/10.1073/pnas.2305180120) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-020_Matthews2023_efficient-automatic-design-of-robots.pdf) |
| Source SHA-256 | `8cd07643bc24af6e495e373a7edbe1734b7906a2075a24a5ea4d3afd0ac2b688` |
| Full-text coverage | 41/41 pages (100.00%); 7,933 extracted words |

## Research question

How does Efficient automatic design of robots search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were discussion, introduction, results, and frequent technical terms were robot, particle, design, voids, attempt, page, etal, initial. The paper-specific method or result selected for transfer review is: **Gradient-based whole-body design found in seconds and fabricated**.

## Principal findings

- **Paper finding (conservative paraphrase):** Gradient-based whole-body design found in seconds and fabricated
- **Reviewer interpretation:** a benchmark for how fast a topology search can be once differentiable physics exists
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a benchmark for how fast a topology search can be once differentiable physics exists This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Gradient-based whole-body design found in seconds and fabricated** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Gradient-based whole-body design found in seconds and fabricated' against the target below. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 41 pages, 65,315 characters, 7,933 words.
- Pages with substantial extractable text: 41/41.
- High-information cue pages sampled from across the paper: 18, 19, 20, 21, 22, 23, 24, 29. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: discussion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
