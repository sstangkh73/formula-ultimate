# AG-002: Mathematical discoveries from program search with large language models

Thai companion: `AG-002_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M. Pawan Kumar, Emilien Dupont, Francisco J. R. Ruiz, Jordan S. Ellenberg, Pengming Wang, Omar Fawzi, Pushmeet Kohli, Alhussein Fawzi |
| Year | 2024 |
| Venue | Nature |
| DOI | 10.1038/s41586-023-06924-6 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1038/s41586-023-06924-6](https://doi.org/10.1038/s41586-023-06924-6) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-002_Paredes2024_mathematical-discoveries-from-program-search-with.pdf) |
| Source SHA-256 | `65d1e915a0813ab39592d9ffa0a94b2645c7f470a4be9219257317a87e9e29d2` |
| Full-text coverage | 30/33 pages (90.91%); 12,803 extracted words |

## Research question

Can the agent or generative method in Mathematical discoveries from program search with large language models produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **empirical/experimental evidence, mathematical/formal evidence, optimization/search study**; this label is a navigation aid, not an evidence grade. Located sections were results, and frequent technical terms were programs, funsearch, program, problem, arxiv, problems, packing, code. The paper-specific method or result selected for transfer review is: **FunSearch pairs an LLM proposer with an automatic, trusted evaluator**.

## Principal findings

- **Paper finding (conservative paraphrase):** FunSearch pairs an LLM proposer with an automatic, trusted evaluator
- **Reviewer interpretation:** its separation of generation from evaluation mirrors our independent-evaluator rule
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** its separation of generation from evaluation mirrors our independent-evaluator rule This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **FunSearch pairs an LLM proposer with an automatic, trusted evaluator** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'FunSearch pairs an LLM proposer with an automatic, trusted evaluator' against the target below. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 33 pages, 78,595 characters, 12,803 words.
- Pages with substantial extractable text: 30/33.
- High-information cue pages sampled from across the paper: 2, 3, 4, 6, 7, 9, 16, 31. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
