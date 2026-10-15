# AG-014: What Do CAE Simulation Agents Really Need Beyond a Generic Harness?

Thai companion: `AG-014_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Jiasheng Shi, Tian-Han Zhang |
| Year | 2026 |
| Venue | arXiv |
| DOI | Not recorded |
| arXiv | 2609.03718 |
| Canonical record | [https://arxiv.org/abs/2609.03718](https://arxiv.org/abs/2609.03718) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `indirect` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-014_Shi2026_what-do-cae-simulation-agents-really-need-beyond-a.pdf) |
| Source SHA-256 | `becf60f94a42bb7be106a2e55057b80ebf35ff773ebf0415971f529077bbfcc0` |
| Full-text coverage | 14/14 pages (100.00%); 9,213 extracted words |

## Research question

Can the agent or generative method in What Do CAE Simulation Agents Really Need Beyond a Generic Harness? produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, limitations, and frequent technical terms were tutorial, openfoam, solver, case, simulation, specialized, harness, agent. The paper-specific method or result selected for transfer review is: **Analyses what tooling CAE agents need beyond a generic coding harness**.

## Principal findings

- **Paper finding (conservative paraphrase):** Analyses what tooling CAE agents need beyond a generic coding harness
- **Reviewer interpretation:** informs the CAD/solver tool interface design
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** informs the CAD/solver tool interface design This is a `indirect` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **present** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Analyses what tooling CAE agents need beyond a generic coding harness** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a bounded diagnostic pilot from 'Analyses what tooling CAE agents need beyond a generic coding harness' and do not change an admitted evaluator until applicability testing passes. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 14 pages, 61,330 characters, 9,213 words.
- Pages with substantial extractable text: 14/14.
- High-information cue pages sampled from across the paper: 2, 4, 5, 6, 7, 9, 11. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, limitations.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
