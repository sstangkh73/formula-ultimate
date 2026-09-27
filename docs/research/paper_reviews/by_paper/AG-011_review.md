# AG-011: Self-Improving CAD Generation Agents with Finite Element Analysis as Feedback

Thai companion: `AG-011_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Guijin Son, Jehyun Park, Seyeon Park, Sunghee Ahn, Youngjae Yu |
| Year | 2026 |
| Venue | arXiv.org |
| DOI | Not recorded |
| arXiv | 2605.17448 |
| Canonical record | [https://arxiv.org/abs/2605.17448](https://arxiv.org/abs/2605.17448) |
| Library topic | AI agents for engineering and scientific design |
| Project relation | `direct` |
| Review depth | Full-text transfer record |
| Source | [local PDF](../../../../papers/02_ai_agents_engineering/AG-011_Son2026_self-improving-cad-generation-agents-with-finite-e.pdf) |
| Source SHA-256 | `b793a594ff8ad1bee86b1b37e964d4f572f2953e124bbbbd24650238bbc58eba` |
| Full-text coverage | 33/33 pages (100.00%); 14,144 extracted words |

## Research question

Can the agent or generative method in Self-Improving CAD Generation Agents with Finite Element Analysis as Feedback produce engineering artifacts that pass executable geometric and physical verification?

## Method and evidence

The complete PDF was processed page by page. Its heuristic evidence profile is **dataset/benchmark, empirical/experimental evidence, simulation/numerical evidence**; this label is a navigation aid, not an evidence grade. Located sections were abstract, conclusion, introduction, results, and frequent technical terms were pass, design, feedback, engineering, https, gpt-5, page, brief. The paper-specific method or result selected for transfer review is: **Uses FEA results as the feedback signal for a CAD-writing agent**.

## Principal findings

- **Paper finding (conservative paraphrase):** Uses FEA results as the feedback signal for a CAD-writing agent
- **Reviewer interpretation:** directly relevant to geometry-structural coupling (Works 082, 138)
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** directly relevant to geometry-structural coupling (Works 082, 138) This is a `direct` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **Uses FEA results as the feedback signal for a CAD-writing agent** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger |
| Proposed change | Build a matched-control pilot that directly tests the mechanism in 'Uses FEA results as the feedback signal for a CAD-writing agent' against the target below. |
| Experiment and control | Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline. |
| Acceptance and failure evidence | Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 33 pages, 88,556 characters, 14,144 words.
- Pages with substantial extractable text: 33/33.
- High-information cue pages sampled from across the paper: 1, 6, 8, 9, 13, 14, 16, 23. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
