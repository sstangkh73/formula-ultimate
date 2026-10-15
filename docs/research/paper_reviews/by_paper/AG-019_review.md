# AG-019: Text-to-CadQuery: A New Paradigm for CAD Generation with Scalable Large Model Capabilities

Thai companion: `AG-019_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Haoyang Xie, Feng Ju |
| Year | 2025 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2505.06507 |
| Canonical record | [https://arxiv.org/abs/2505.06507](https://arxiv.org/abs/2505.06507) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-019_Xie2025_text-to-cadquery-a-new-paradigm-for-cad-generation.pdf) |
| Source SHA-256 | `b78f5a28edb4fc9468c0605bd90863b59094d4598d6a1daad273151b62639acc` |
| Full-text coverage | 18/18 pages (100.00%); 9,072 extracted words |

## Research question

Can the agent or generative method in Text-to-CadQuery: A New Paradigm for CAD Generation with Scalable Large Model Capabilities produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, dataset/benchmark, physical-test evidence, empirical/experimental evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, limitations, methods, and frequent technical terms were models, cadquery, model, arxiv, language, command, code, point. The paper-specific method or result selected for transfer review is: **Trains LLMs to emit CadQuery directly**.

## Principal findings

- **Paper finding (conservative paraphrase):** Trains LLMs to emit CadQuery directly
- **Reviewer interpretation:** the same CAD language our agents write, with a dataset and error statistics we can reuse
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** the same CAD language our agents write, with a dataset and error statistics we can reuse This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **present** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Trains LLMs to emit CadQuery directly** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Trains LLMs to emit CadQuery directly' against the target below. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 18 pages, 56,342 characters, 9,072 words.
- Pages with substantial extractable text: 18/18.
- High-information cue pages sampled from across the paper: 2, 3, 4, 5, 6, 7, 9, 17. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, limitations, methods.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
