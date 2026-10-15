# AG-032: Constraining Generative Models for Engineering Design with Negative Data

Thai companion: `AG-032_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Giorgio Giannone, Lyle Regenwetter, Akash Srivastava, D. Gutfreund, Faez Ahmed |
| Year | 2023 |
| Venue | Trans. Mach. Learn. Res. |
| DOI | Not recorded |
| arXiv | 2306.15166 |
| Canonical record | [https://arxiv.org/abs/2306.15166](https://arxiv.org/abs/2306.15166) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-032_Giannone2023_constraining-generative-models-for-engineering-des.pdf) |
| Source SHA-256 | `6f829566eba3823d227d5d333e92b85e6cb51c1dc6ee8e65d7103d8da6dcad4e` |
| Full-text coverage | 38/38 pages (100.00%); 16,417 extracted words |

## Research question

Can the agent or generative method in Constraining Generative Models for Engineering Design with Negative Data produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence, mathematical/formal evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, methods, and frequent technical terms were models, data, generative, negative, design, model, engineering, gan-mdd. The paper-specific method or result selected for transfer review is: **Trains on infeasible examples to keep generators inside constraints**.

## Principal findings

- **Paper finding (conservative paraphrase):** Trains on infeasible examples to keep generators inside constraints
- **Reviewer interpretation:** our rejection ledgers are exactly such negative data
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** our rejection ledgers are exactly such negative data This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Trains on infeasible examples to keep generators inside constraints** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Trains on infeasible examples to keep generators inside constraints' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 38 pages, 103,782 characters, 16,417 words.
- Pages with substantial extractable text: 38/38.
- High-information cue pages sampled from across the paper: 2, 3, 4, 5, 6, 8, 11, 12. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, methods.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
