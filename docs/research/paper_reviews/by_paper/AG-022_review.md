# AG-022: CADDesigner: Conceptual CAD Model Generation with a General-Purpose Agent

Thai companion: `AG-022_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Fengxiao Fan, Jingzhe Ni, Xiaolong Yin, Sirui Wang, Xingyu Lu, Qiang Zou, Ruo-Feng Tong, Min Tang, Peng Du |
| Year | 2025 |
| Venue | Comput. Aided Des. |
| DOI | Not recorded |
| arXiv | 2508.01031 |
| Canonical record | [https://arxiv.org/abs/2508.01031](https://arxiv.org/abs/2508.01031) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-022_Fan2025_caddesigner-conceptual-cad-model-generation-with-a.pdf) |
| Source SHA-256 | `07349fcf5aad7d9a67d6d5c2f5059ab6cc45e4bbf9cddf2c41a416c0e0d33be3` |
| Full-text coverage | 16/16 pages (100.00%); 9,954 extracted words |

## Research question

Can the agent or generative method in CADDesigner: Conceptual CAD Model Generation with a General-Purpose Agent produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, dataset/benchmark, empirical/experimental evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were generation, code, model, models, modeling, caddesigner, ecip, design. The paper-specific method or result selected for transfer review is: **General-purpose agent with structured diagnostics for failed CAD scripts**.

## Principal findings

- **Paper finding (conservative paraphrase):** General-purpose agent with structured diagnostics for failed CAD scripts
- **Reviewer interpretation:** relevant to turning kernel errors into repairable feedback
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to turning kernel errors into repairable feedback This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **General-purpose agent with structured diagnostics for failed CAD scripts** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a bounded diagnostic pilot from 'General-purpose agent with structured diagnostics for failed CAD scripts' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 16 pages, 72,539 characters, 9,954 words.
- Pages with substantial extractable text: 16/16.
- High-information cue pages sampled from across the paper: 1, 3, 8, 9, 10, 11, 12, 15. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
