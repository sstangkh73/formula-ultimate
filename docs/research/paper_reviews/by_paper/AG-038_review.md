# AG-038: Large Language Models as Optimizers

Thai companion: `AG-038_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V. Le, Denny Zhou, Xin-Yun Chen |
| Year | 2023 |
| Venue | International Conference on Learning Representations |
| DOI | Not recorded |
| arXiv | 2309.03409 |
| Canonical record | [https://arxiv.org/abs/2309.03409](https://arxiv.org/abs/2309.03409) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-038_Yang2023_large-language-models-as-optimizers.pdf) |
| Source SHA-256 | `61c8493c964f6d4436f69ae63ff52d3a91540708e9387615f3a8f034bab081c0` |
| Full-text coverage | 42/42 pages (100.00%); 24,673 extracted words |

## Research question

Can the agent or generative method in Large Language Models as Optimizers produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, physical-test evidence, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, and frequent technical terms were optimization, palm, instructions, accuracy, step, training, prompt, text-bison. The paper-specific method or result selected for transfer review is: **OPRO: LLMs propose solutions from a scored history**.

## Principal findings

- **Paper finding (conservative paraphrase):** OPRO: LLMs propose solutions from a scored history
- **Reviewer interpretation:** a baseline for LLM-as-optimiser behaviour
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a baseline for LLM-as-optimiser behaviour This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **OPRO: LLMs propose solutions from a scored history** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a bounded diagnostic pilot from 'OPRO: LLMs propose solutions from a scored history' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 42 pages, 150,591 characters, 24,673 words.
- Pages with substantial extractable text: 42/42.
- High-information cue pages sampled from across the paper: 1, 2, 6, 10, 11, 13, 18, 21. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
