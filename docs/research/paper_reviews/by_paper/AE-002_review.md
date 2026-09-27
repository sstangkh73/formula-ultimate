# AE-002: Spectral/hp element simulation of flow past a Formula One front wing: validation against experiments

Thai companion: `AE-002_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | F. Buscariolo, Julien Hoessler, D. Moxey, Ayad Jassim, Kevin Gouder, J. Basley, Yushi Murai, G. Assi, S. Sherwin |
| Year | 2019 |
| Venue | Journal of Wind Engineering and Industrial Aerodynamics |
| DOI | Not recorded |
| arXiv | 1909.06701 |
| Canonical record | [https://arxiv.org/abs/1909.06701](https://arxiv.org/abs/1909.06701) |
| Library topic | Aerodynamics and aerodynamic data |
| Project relation | `data` |
| Review depth | Decision-critical deep review |
| Source | [local PDF](../../../../papers/10_aerodynamics/AE-002_Buscariolo2019_spectral-hp-element-simulation-of-flow-past-a-form.pdf) |
| Source SHA-256 | `8d241b76654c21b2d35d3b5a37fb92e92b71a9c254e30a76d8401d68370ef078` |
| Full-text coverage | 18/18 pages (100.00%); 5,545 extracted words |

## Research question

What spatial and temporal resolution is required for high-fidelity CFD to reproduce measured ground-effect front-wing flow structures?

## Method and evidence

The Imperial Front Wing supplies CAD and experimental oil-flow/PIV data. Under-resolved DNS/implicit LES with third-, fourth-, and fifth-order spectral/hp discretizations is compared against measured vortex locations, intensities, wall features, lift, and drag (pp. 1, 7-16).

## Principal findings

- **Paper finding (conservative paraphrase):** The third-order case is under-resolved. The fifth-order case best matches experimental reattachment and flow features; its downforce is 4.5% above the fourth-order case, and its lift stabilizes only late in the averaging window (pp. 8, 16).
- **Reviewer interpretation:** A visually plausible lower-resolution field gives the wrong load trend, so aero validation must include resolution and averaging-time sensitivity, not only one coefficient snapshot.
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** A visually plausible lower-resolution field gives the wrong load trend, so aero validation must include resolution and averaging-time sensitivity, not only one coefficient snapshot. This is a `data` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

This is one front-wing geometry and high-fidelity setup, not a complete car or broad turbulence-model validation. The highest-order lift was still evolving for much of the run, so averaging convergence remains material. An explicit `Limitations` heading was **not detected as a standalone heading** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **A visually plausible lower-resolution field gives the wrong load trend, so aero validation must include resolution and averaging-time sensitivity, not only one coefficient snapshot.** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit |
| Proposed change | Use the IFW CAD/PIV case as the first independent aero gate: reproduce vortex location and reattachment plus lift/drag under at least three resolution levels and a preregistered averaging-convergence rule. |
| Experiment and control | Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments. |
| Acceptance and failure evidence | Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms. |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: 18 pages, 40,766 characters, 5,545 words.
- Pages with substantial extractable text: 18/18.
- High-information cue pages sampled from across the paper: 1, 2, 3, 4, 5, 6, 8, 10. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: abstract, conclusion, introduction, results.
- Extraction errors: 0; likely scanned: `false`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
