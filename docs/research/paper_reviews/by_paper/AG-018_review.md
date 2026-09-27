# AG-018: Drag-guided diffusion models for vehicle image generation

Thai companion: `AG-018_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Nikos Aréchiga, F. Permenter, B. Song, Chenyang Yuan |
| Year | 2023 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2306.09935 |
| Canonical record | [https://arxiv.org/abs/2306.09935](https://arxiv.org/abs/2306.09935) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-018_Arechiga2023_drag-guided-diffusion-models-for-vehicle-image-gen.pdf) |
| Source SHA-256 | `a9085ac47e28e29e0db04394cf5f2234c7fb241001981b1f619a58344f896294` |
| Full-text coverage | 16/16 pages (100.00%); 4,631 extracted words |

## Research question

Can the agent or generative method in Drag-guided diffusion models for vehicle image generation produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence, mathematical/formal evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, introduction, and frequent technical terms were drag, diffusion, image, arxiv, model, figure, guidance, models. The paper-specific method or result selected for transfer review is: **Guides a generative model with a drag surrogate**.

## Principal findings

- **Paper finding (conservative paraphrase):** Guides a generative model with a drag surrogate
- **Reviewer interpretation:** illustrates the risk that surrogate guidance rewards surrogate errors
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** illustrates the risk that surrogate guidance rewards surrogate errors This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Guides a generative model with a drag surrogate** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Guides a generative model with a drag surrogate' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 16 pages, 28,488 characters, 4,631 words.
- Pages with substantial extractable text: 16/16.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 7, 8, 10. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, introduction.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
