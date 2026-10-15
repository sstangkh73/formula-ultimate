# AG-035: Eureka: Human-Level Reward Design via Coding Large Language Models

Thai companion: `AG-035_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Y. Ma, William Liang, Guanzhi Wang, De-An Huang, O. Bastani, D. Jayaraman, Yu-Ke Zhu, Linxi Fan, Anima Anandkumar |
| Year | 2023 |
| Venue | International Conference on Learning Representations |
| DOI | Not recorded |
| arXiv | 2310.12931 |
| Canonical record | [https://arxiv.org/abs/2310.12931](https://arxiv.org/abs/2310.12931) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-035_Ma2023_eureka-human-level-reward-design-via-coding-large.pdf) |
| Source SHA-256 | `aa3b6350a92e4e8b1d894d0879d0af72df2fe76b3fe5d9341151924cb5884f74` |
| Full-text coverage | 45/45 pages (100.00%); 21,010 extracted words |

## Research question

Can the agent or generative method in Eureka: Human-Level Reward Design via Coding Large Language Models produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, physical-test evidence, empirical/experimental evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were reward, torch, eureka, tensor, function, human, task, environment. The paper-specific method or result selected for transfer review is: **LLM writes reward code for control tasks**.

## Principal findings

- **Paper finding (conservative paraphrase):** LLM writes reward code for control tasks
- **Reviewer interpretation:** a caution that agent-written objectives must be frozen and audited before search
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a caution that agent-written objectives must be frozen and audited before search This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **LLM writes reward code for control tasks** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a bounded diagnostic pilot from 'LLM writes reward code for control tasks' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 45 pages, 142,656 characters, 21,010 words.
- Pages with substantial extractable text: 45/45.
- High-information cue pages sampled from across the paper: 1, 2, 3, 7, 23, 24, 28, 29. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
