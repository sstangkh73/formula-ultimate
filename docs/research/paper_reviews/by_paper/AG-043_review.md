# AG-043: Physical Design using Differentiable Learned Simulators

Thai companion: `AG-043_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Kelsey R. Allen, Tatiana Lopez-Guevara, Kimberly L. Stachenfeld, Alvaro Sanchez-Gonzalez, P. Battaglia, Jessica B. Hamrick, T. Pfaff |
| Year | 2022 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2202.00728 |
| Canonical record | [https://arxiv.org/abs/2202.00728](https://arxiv.org/abs/2202.00728) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-043_Allen2022_physical-design-using-differentiable-learned-simul.pdf) |
| Source SHA-256 | `d2939f57fce3a3ba92e58ddf31237c32d03611d8c20256168db4dd94c5701138` |
| Full-text coverage | 24/24 pages (100.00%); 13,192 extracted words |

## Research question

Can the agent or generative method in Physical Design using Differentiable Learned Simulators produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, dataset/benchmark, empirical/experimental evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were design, learned, page, cited, simulators, model, figure, optimization. The paper-specific method or result selected for transfer review is: **Optimises designs through learned graph-network simulators (airfoils, fluid tools)**.

## Principal findings

- **Paper finding (conservative paraphrase):** Optimises designs through learned graph-network simulators (airfoils, fluid tools)
- **Reviewer interpretation:** shows both the speed and the surrogate-exploitation risk
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** shows both the speed and the surrogate-exploitation risk This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Optimises designs through learned graph-network simulators (airfoils, fluid tools)** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Optimises designs through learned graph-network simulators (airfoils, fluid tools)' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 24 pages, 84,497 characters, 13,192 words.
- Pages with substantial extractable text: 24/24.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 6, 7, 8, 9. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
