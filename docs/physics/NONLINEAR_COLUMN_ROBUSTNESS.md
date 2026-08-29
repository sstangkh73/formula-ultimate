# Nonlinear Column Mesh and Shape Robustness

Thai companion: `NONLINEAR_COLUMN_ROBUSTNESS.th.md`

## Research question and claim boundary

Work 039 tests two possible weaknesses in the Work 038 precritical result: mesh dependence and dependence on the assumed initial crookedness shape. All evidence remains linear elastic and below the matched Work 037 eigenvalue loads. It cannot support post-buckling, collapse, yield, fracture, fatigue, safety-factor, or vehicle-capacity claims.

## Method

The fixed-free solid column retains `L=0.2 m`, `b=h=0.01 m`, `E=70 GPa`, `nu=0.3`, C3D4 elements, and tip imperfection `e0=0.1 mm`. Three Work 037 meshes are used without renormalizing the applied loads:

| Mesh | Size | Nodes | Tetrahedra | Work 037 `Pcr` |
|---|---:|---:|---:|---:|
| coarse | 1.50 mm | 7,052 | 29,098 | 3852.795 N |
| medium | 1.25 mm | 11,702 | 51,221 | 3776.375 N |
| fine | 1.00 mm | 20,514 | 95,711 | 3715.160 N |

Absolute loads are `0.50`, `0.70`, and `0.85` times the fine-mesh `Pcr`. Two normalized shapes have identical root offset, root slope, and tip amplitude:

```text
cantilever_eigenmode:  phi(x) = 1 - cos(pi x/(2L))
smoothstep_cubic:      phi(x) = 3(x/L)^2 - 2(x/L)^3
```

Execution acceptance requires all 18 cases to converge with complete evidence, reaction closure `<=1e-5`, and monotonic response. The numerical-convergence hypothesis requires eigenmode secant error `<=15%` and medium-to-fine amplification change `<=5%`. The shape-robustness hypothesis requires fine-mesh amplification difference `<=10%`.

## Results

All 18 cases converged, all response sequences were monotonic, and maximum reaction error was `1.749e-16`. Therefore the experiment execution passed.

| Fine-load fraction | Medium-to-fine eigenmode change | Shape difference on fine mesh |
|---:|---:|---:|
| 0.50 | 1.548% | 7.523% |
| 0.70 | 3.639% | 10.980% |
| 0.85 | 8.653% | 13.697% |

The eigenmode response continued to match each mesh's own secant reference closely; maximum error across all meshes was `0.912%`. However, the absolute-load medium-to-fine change exceeded the `5%` gate at `0.85` fine `Pcr`. The numerical-convergence hypothesis is therefore **rejected** for the full declared load range.

Fine-mesh amplification was:

| Fine-load fraction | Eigenmode amplification | Cubic amplification |
|---:|---:|---:|
| 0.50 | 1.9971 | 1.8523 |
| 0.70 | 3.3269 | 2.9806 |
| 0.85 | 6.6413 | 5.7900 |

Shape difference exceeded `10%` at `0.70` and `0.85`; the shape-robustness hypothesis is therefore **rejected**.

## Interpretation

Supporting evidence: the solver route is stable, force closure is excellent, monotonicity is preserved, and the eigenmode-shaped cases follow their matched secant references. Contradicting evidence: response at high load has not converged between the two finest current meshes, and equal tip-amplitude imperfections do not produce shape-independent amplification.

Alternative explanations include C3D4 bending stiffness, the large condition sensitivity near `Pcr`, different first-mode projection of the two imperfection shapes, and mesh-asymmetry seeds. Missing evidence includes meshes finer than `1.0 mm`, quadratic elements, a measured/manufacturing imperfection distribution, and an independently validated nonlinear continuation procedure.

Confidence is high that mesh and imperfection-shape choices materially affect this near-critical fixture. Consequently, Work 039 blocks promotion to a post-buckling capacity claim. The next experiment should extend the eigenmode study below `1.0 mm` at the same absolute loads and compare a higher-order element route before selecting a continuation method.
