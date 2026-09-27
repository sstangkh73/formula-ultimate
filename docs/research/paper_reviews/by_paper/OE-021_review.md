# OE-021: Reinforcement Learning for Improving Agent Design

Thai companion: `OE-021_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | David R Ha |
| Year | 2019 |
| Venue | Artificial Life |
| DOI | Not recorded |
| arXiv | 1810.03779 |
| Canonical record | [https://arxiv.org/abs/1810.03779](https://arxiv.org/abs/1810.03779) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-021_Ha2019_reinforcement-learning-for-improving-agent-design.pdf) |
| Source SHA-256 | `25f796db97134d059661fe4c365cdbeab3c1d11a56fab98bab9b655918679f86` |
| Full-text coverage | 12/12 pages (100.00%); 7,090 extracted words |

## Research question

How does Reinforcement Learning for Improving Agent Design search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, optimization/search study, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, introduction, methods, results, and frequent technical terms were agent, design, learning, policy, body, morphology, environment, task. The paper-specific method or result selected for transfer review is: **Joint learning of body parameters and policy**.

## Principal findings

- **Paper finding (conservative paraphrase):** Joint learning of body parameters and policy
- **Reviewer interpretation:** shows the optimiser exploits body freedom in unexpected ways, a warning for our objective checks
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** shows the optimiser exploits body freedom in unexpected ways, a warning for our objective checks This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Joint learning of body parameters and policy** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Joint learning of body parameters and policy' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 12 pages, 42,932 characters, 7,090 words.
- Pages with substantial extractable text: 12/12.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 6, 7. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, introduction, methods, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
