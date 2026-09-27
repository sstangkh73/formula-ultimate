# MA-003: Exploration of data science techniques to predict fatigue strength of steel from composition and processing parameters

Thai companion: `MA-003_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | Ankit Agrawal, Parijat D Deshpande, Ahmet Cecen, Gautham P Basavarsu, Alok N Choudhary, Surya R Kalidindi |
| Year | 2014 |
| Venue | Integrating Materials and Manufacturing Innovation |
| DOI | 10.1186/2193-9772-3-8 |
| arXiv | Not recorded |
| Canonical record | [https://doi.org/10.1186/2193-9772-3-8](https://doi.org/10.1186/2193-9772-3-8) |
| Library topic | Materials, joints, fatigue, and manufacturing |
| Project relation | `data` |
| Review depth | Decision-critical deep review |
| Source | [local PDF](../../../../papers/12_materials_joints_manufacturing/MA-003_Agrawal2014_exploration-of-data-science-techniques-to-predict.pdf) |
| Source SHA-256 | `390cc476d0f097cfd8b1b216a72cff89c1e371b36fb40e385e802ca4d1bbf204` |
| Full-text coverage | 19/19 pages (100.00%); 8,896 extracted words |

## Research question

Can steel fatigue strength be predicted from composition and processing variables using open materials data, and which inputs matter most?

## Method and evidence

The study cleans NIMS steel records, ranks composition/process features, fits multiple regressors including neural networks, trees, and polynomial models, and evaluates with leave-one-out cross-validation for rotating-bending fatigue at 10^7 cycles (pp. 5-10).

## Principal findings

- **Paper finding (conservative paraphrase):** Several models reach R2 around 0.98 with reported error below 4%, improving earlier efforts and ranking predictive composition/process variables (pp. 1, 13-15).
- **Reviewer interpretation:** The paper models process-structure-property linkage rather than composition alone, which matches the project's rule that material values depend on manufacturing history.
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** The paper models process-structure-property linkage rather than composition alone, which matches the project's rule that material values depend on manufacturing history. This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

The authors call the dataset small for data mining and recommend more heterogeneous data (p. 16). LOOCV within one database does not prove cross-source, new-alloy, multiaxial, thermal, or variable-amplitude fatigue transfer, and prediction is not causation. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **The paper models process-structure-property linkage rather than composition alone, which matches the project's rule that material values depend on manufacturing history.** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **material-data policy and Works 113/114/116/130 joint, failure, and tolerance evidence**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | material-data policy and Works 113/114/116/130 joint, failure, and tolerance evidence |
| Proposed change | Register NIMS provenance and reproduce the model with alloy-family/source holdouts; use predictions only to prioritize tests, then validate candidate-specific S-N/failure data before Work 116 admission. |
| Experiment and control | Validate paper-derived properties or mechanisms with held-out specimen and joint/assembly cases spanning process, orientation, temperature, tolerance, preload, surface, and cyclic loading. |
| Acceptance and failure evidence | Require provenance-complete properties, calibrated uncertainty, correct failure mode/location, and bounded transfer from specimen to assembly; unsupported conditions remain unknown. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 19 pages, 55,665 characters, 8,896 words.
- Pages with substantial extractable text: 19/19.
- High-information cue pages sampled from across the paper: 1, 2, 7, 8, 9, 10, 11, 13. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, methods, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
