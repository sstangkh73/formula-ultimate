# AG-023: Towards High-Fidelity CAD Generation via LLM-Driven Program Generation and Text-Based B-Rep Primitive Grounding

Thai companion: `AG-023_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Jiahao Li, Qingwang Zhang, Qiuyue Chen, Guozhan Qiu, Yunzhong Lou, Xiangdong Zhou |
| Year | 2026 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2603.11831 |
| Canonical record | [https://arxiv.org/abs/2603.11831](https://arxiv.org/abs/2603.11831) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-023_Li2026_towards-high-fidelity-cad-generation-via-llm-drive.pdf) |
| Source SHA-256 | `07bcd526f6e1729b22caa70e6207a9c93db5b046f47ef4775a4ce30bd1288736` |
| Full-text coverage | 13/13 pages (100.00%); 9,152 extracted words |

## Research question

Can the agent or generative method in Towards High-Fidelity CAD Generation via LLM-Driven Program Generation and Text-Based B-Rep Primitive Grounding produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, methods, and frequent technical terms were b-rep, generation, models, primitive, primitives, dataset, geometric, model. The paper-specific method or result selected for transfer review is: **FutureCAD: LLM writes CadQuery and grounds references to B-rep primitives**.

## Principal findings

- **Paper finding (conservative paraphrase):** FutureCAD: LLM writes CadQuery and grounds references to B-rep primitives
- **Reviewer interpretation:** addresses the fragile face/edge selection problem in generated CAD
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** addresses the fragile face/edge selection problem in generated CAD This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **FutureCAD: LLM writes CadQuery and grounds references to B-rep primitives** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a bounded diagnostic pilot from 'FutureCAD: LLM writes CadQuery and grounds references to B-rep primitives' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 13 pages, 58,971 characters, 9,152 words.
- Pages with substantial extractable text: 13/13.
- High-information cue pages sampled from across the paper: 1, 2, 3, 6, 7, 8, 11, 13. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, methods.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
