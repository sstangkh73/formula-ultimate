# OE-022: Jointly Learning to Construct and Control Agents using Deep Reinforcement Learning

Thai companion: `OE-022_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Charles B. Schaff, David Yunis, Ayan Chakrabarti, Matthew R. Walter |
| Year | 2019 |
| Venue | IEEE International Conference on Robotics and Automation |
| DOI | Not recorded |
| arXiv | 1801.01432 |
| Canonical record | [https://arxiv.org/abs/1801.01432](https://arxiv.org/abs/1801.01432) |
| Library topic | Open-ended morphology/control co-design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/01_open_ended_codesign/OE-022_Schaff2019_jointly-learning-to-construct-and-control-agents-u.pdf) |
| Source SHA-256 | `7906ca5f1bee5fc8fdb22fac96deeb8088a8118b188fdc283bf5044a6c13d554` |
| Full-text coverage | 8/8 pages (100.00%); 6,914 extracted words |

## Research question

How does Jointly Learning to Construct and Control Agents using Deep Reinforcement Learning search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, simulation/numerical evidence, optimization/search study, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were no reliable heading match, and frequent technical terms were design, policy, control, designs, distribution, optimization, robot, training. The paper-specific method or result selected for transfer review is: **Design-conditioned policy shared across a design distribution**.

## Principal findings

- **Paper finding (conservative paraphrase):** Design-conditioned policy shared across a design distribution
- **Reviewer interpretation:** a way to amortise driver optimisation over many candidate vehicles
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a way to amortise driver optimisation over many candidate vehicles This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Design-conditioned policy shared across a design distribution** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 124 multiscale search scheduler and morphology/controller evidence ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 124 multiscale search scheduler and morphology/controller evidence ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Design-conditioned policy shared across a design distribution' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments. |
| Acceptance and failure evidence | Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 8 pages, 43,224 characters, 6,914 words.
- Pages with substantial extractable text: 8/8.
- High-information cue pages sampled from across the paper: 1, 3, 5, 6. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: no reliable heading match.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
