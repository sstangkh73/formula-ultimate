# AG-024: Clarify Before You Draw: Proactive Agents for Robust Text-to-CAD Generation

Thai companion: `AG-024_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Bo Yuan, Zelin Zhao, Petr Molodyk, Bin Hu, Yong-Xin Chen |
| Year | 2026 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2602.03045 |
| Canonical record | [https://arxiv.org/abs/2602.03045](https://arxiv.org/abs/2602.03045) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-024_Yuan2026_clarify-before-you-draw-proactive-agents-for-robus.pdf) |
| Source SHA-256 | `d4783c128a3caf321a85c34c544d821e5da1a33a04c3e15b9e1e8dd24963cbf0` |
| Full-text coverage | 28/28 pages (100.00%); 16,199 extracted words |

## Research question

Can the agent or generative method in Clarify Before You Draw: Proactive Agents for Robust Text-to-CAD Generation produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, control/learning study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were cadquery, generation, code, prompt, agent, prompts, arxiv, user. The paper-specific method or result selected for transfer review is: **Agents that resolve underspecified CAD requests before drawing**.

## Principal findings

- **Paper finding (conservative paraphrase):** Agents that resolve underspecified CAD requests before drawing
- **Reviewer interpretation:** relevant to typed interface specifications for generated parts
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** relevant to typed interface specifications for generated parts This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Agents that resolve underspecified CAD requests before drawing** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Agents that resolve underspecified CAD requests before drawing' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 28 pages, 102,028 characters, 16,199 words.
- Pages with substantial extractable text: 28/28.
- High-information cue pages sampled from across the paper: 2, 3, 4, 6, 9, 13, 14, 21. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
