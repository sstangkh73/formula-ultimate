# AG-031: Beyond Statistical Similarity: Rethinking Metrics for Deep Generative Models in Engineering Design

Thai companion: `AG-031_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Lyle Regenwetter, Akash Srivastava, D. Gutfreund, Faez Ahmed |
| Year | 2023 |
| Venue | Comput. Aided Des. |
| DOI | Not recorded |
| arXiv | 2302.02913 |
| Canonical record | [https://arxiv.org/abs/2302.02913](https://arxiv.org/abs/2302.02913) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-031_Regenwetter2023_beyond-statistical-similarity-rethinking-metrics-f.pdf) |
| Source SHA-256 | `0c9941d6186f288cd5c0195fad18b819120ec1d2f253514dbba3cdba8fa7f57f` |
| Full-text coverage | 51/51 pages (100.00%); 20,371 extracted words |

## Research question

Can the agent or generative method in Beyond Statistical Similarity: Rethinking Metrics for Deep Generative Models in Engineering Design produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **review/synthesis, dataset/benchmark, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, discussion, introduction, results, and frequent technical terms were design, metrics, generated, performance, designs, distance, models, metric. The paper-specific method or result selected for transfer review is: **Argues generated designs must be scored on constraint satisfaction, performance and novelty rather than similarity to data**.

## Principal findings

- **Paper finding (conservative paraphrase):** Argues generated designs must be scored on constraint satisfaction, performance and novelty rather than similarity to data
- **Reviewer interpretation:** aligned with our discovery criteria
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** aligned with our discovery criteria This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Argues generated designs must be scored on constraint satisfaction, performance and novelty rather than similarity to data** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Argues generated designs must be scored on constraint satisfaction, performance and novelty rather than similarity to data' against the target below. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 51 pages, 133,692 characters, 20,371 words.
- Pages with substantial extractable text: 51/51.
- High-information cue pages sampled from across the paper: 4, 6, 12, 13, 17, 18, 19, 27. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, discussion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
