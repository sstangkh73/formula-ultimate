# AG-021: Generating CAD Code with Vision-Language Models for 3D Designs

Thai companion: `AG-021_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Kamel Alrashedy, Pradyumna Tambwekar, Z. Zaidi, Megan Langwasser, Wei Xu, Matthew C. Gombolay |
| Year | 2024 |
| Venue | International Conference on Learning Representations |
| DOI | Not recorded |
| arXiv | 2410.05340 |
| Canonical record | [https://arxiv.org/abs/2410.05340](https://arxiv.org/abs/2410.05340) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-021_Alrashedy2024_generating-cad-code-with-vision-language-models-fo.pdf) |
| Source SHA-256 | `f3e88746a0739c925efde8dbc80e20f947bb4a88bfdeab08f1e3a7cdbac6e056` |
| Full-text coverage | 27/27 pages (100.00%); 12,303 extracted words |

## Research question

Can the agent or generative method in Generating CAD Code with Vision-Language Models for 3D Designs produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were code, object, generated, cadcodeverify, feedback, objects, geometric, generation. The paper-specific method or result selected for transfer review is: **CADCodeVerify: the model renders its own CAD output and self-verifies**.

## Principal findings

- **Paper finding (conservative paraphrase):** CADCodeVerify: the model renders its own CAD output and self-verifies
- **Reviewer interpretation:** a cheap pre-check before our independent geometry witnesses
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a cheap pre-check before our independent geometry witnesses This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **CADCodeVerify: the model renders its own CAD output and self-verifies** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a bounded diagnostic pilot from 'CADCodeVerify: the model renders its own CAD output and self-verifies' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 27 pages, 72,751 characters, 12,303 words.
- Pages with substantial extractable text: 27/27.
- High-information cue pages sampled from across the paper: 1, 2, 3, 6, 8, 9, 10, 16. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
