# AG-033: BIKED: A Dataset for Computational Bicycle Design with Machine Learning Benchmarks

Thai companion: `AG-033_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Lyle Regenwetter, Brent Curry, Faez Ahmed |
| Year | 2022 |
| Venue | Journal of Mechanical Design |
| DOI | 10.1115/1.4052585 |
| arXiv | 2103.05844 |
| Canonical record | [https://doi.org/10.1115/1.4052585](https://doi.org/10.1115/1.4052585) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `data` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-033_Regenwetter2022_biked-a-dataset-for-computational-bicycle-design-w.pdf) |
| Source SHA-256 | `30e74068c8027a485f02b4c9aca6d90448be043835cd19f0efce0f8e40c7cc8c` |
| Full-text coverage | 19/19 pages (100.00%); 12,459 extracted words |

## Research question

Can the agent or generative method in BIKED: A Dataset for Computational Bicycle Design with Machine Learning Benchmarks produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were conclusion, introduction, limitations, methods, and frequent technical terms were design, data, designs, bicycle, classi, parametric, bike, space. The paper-specific method or result selected for transfer review is: **Parametric vehicle-design dataset with structural and performance labels**.

## Principal findings

- **Paper finding (conservative paraphrase):** Parametric vehicle-design dataset with structural and performance labels
- **Reviewer interpretation:** a public example of vehicle design data with validity checks
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** a public example of vehicle design data with validity checks This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **present** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Parametric vehicle-design dataset with structural and performance labels** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Register the dataset or benchmark behind 'Parametric vehicle-design dataset with structural and performance labels' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 19 pages, 75,664 characters, 12,459 words.
- Pages with substantial extractable text: 19/19.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 7, 8. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: conclusion, introduction, limitations, methods.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
