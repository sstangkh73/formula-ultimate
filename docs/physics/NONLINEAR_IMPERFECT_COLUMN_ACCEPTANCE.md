# Nonlinear Imperfect Column Acceptance

Thai companion: `NONLINEAR_IMPERFECT_COLUMN_ACCEPTANCE.th.md`

## Question and claim boundary

Work 038 asks whether axial compression actually couples through an initial geometric imperfection into increasing lateral displacement. It verifies a precritical, linear-elastic, geometrically nonlinear CalculiX route. It does **not** measure post-buckling capacity, collapse, allowable load, yield, fracture, or fatigue.

The solver deck uses `*STEP, NLGEOM`. CalculiX documents that `NLGEOM` on `*STEP` activates the geometrically nonlinear static formulation and recommends checking solver output for the nonlinear-geometric confirmation message: <https://www.feacluster.com/CalculiX/ccx_2.18/doc/ccx/node332.html>.

## Specimen and reference

The specimen is the Work 037 solid cantilever column: `L=0.2 m`, `b=h=0.01 m`, `E=70 GPa`, `nu=0.3`, C3D4 mesh size `1.25 mm`, fixed at `x=0`, and compressed by a tributary-area-weighted end-face load. Work 037 measured the matching mesh eigenvalue as `Pcr=3776.375 N`; the separate Euler reference is `3598.293271 N`.

The initial cross-section translation is

```text
z0(x) = e0 [1 - cos(pi x / (2L))]
```

so the fixed face is unshifted and the free-end offset is exactly `e0`. For a mode-shaped imperfect elastic column below `Pcr`, the comparison is

```text
A(P) = 1 / (1 - P/Pcr)
e(P) = e0 A(P)
```

Two amplitudes, `e0=0.1 mm` and `0.2 mm`, are evaluated at `P/Pcr={0.25,0.50,0.70,0.85}`.

## Experiment variables and gates

- independent variables: `e0` and `P/Pcr`;
- dependent variables: incremental and total lateral tip displacement, amplification, axial shortening, maximum computed von Mises stress, reaction closure, solver status, and evidence hashes;
- controls: geometry, elastic properties, mesh, support, load distribution, imperfection function, solver, and parser;
- success: every nonlinear case converges, reaction error is `<=1e-5`, response is strictly monotonic, secant-reference error is `<=15%`, and cross-amplitude normalized spread is `<=10%`;
- failure: missing/malformed evidence, missing NLGEOM confirmation, non-monotonic response, or any exceeded gate fails the experiment.

The perfect-column control must keep lateral drift below `2e-6 m`, which is 2% of the smallest admitted imperfection. This threshold was calibrated after an initial pilot exposed mesh-asymmetry drift, then pinned before the reported replay. Therefore Work 038 is solver acceptance evidence, not an independently preregistered confirmatory study.

## Results

| `P/Pcr` | Secant `A` | `A`, `e0=0.1 mm` | error | `A`, `e0=0.2 mm` | error |
|---:|---:|---:|---:|---:|---:|
| 0.25 | 1.3333 | 1.3327 | 0.044% | 1.3326 | 0.055% |
| 0.50 | 2.0000 | 1.9982 | 0.089% | 1.9978 | 0.109% |
| 0.70 | 3.3333 | 3.3292 | 0.123% | 3.3273 | 0.180% |
| 0.85 | 6.6667 | 6.6457 | 0.314% | 6.5724 | 1.414% |

At `0.85 Pcr`, total tip offsets are `0.664571 mm` and `1.314475 mm`. The largest cross-amplitude spread is `1.110%`; the largest reaction error is `2.648e-7`. The perfect NLGEOM control drifts `0.000426 mm`, below its `0.002 mm` gate. The imperfect geometrically linear control reaches only `A=1.8485` and misses the secant response by `72.27%`, falsifying the explanation that initial geometry alone is sufficient without geometric stiffness.

## Interpretation and limitations

Supporting evidence is the monotonic, amplitude-consistent nonlinear response and close secant match. Contradicting evidence is the growing departure at the larger imperfection and highest load; this is compatible with leaving the ideal small-deflection secant approximation. Mesh asymmetry, C3D4 bending stiffness, and the pinned numerical eigenvalue are alternative contributors. No independent mesh-convergence study of nonlinear amplification was performed.

Confidence is high that the implemented route transmits axial load into precritical P-delta displacement for this fixture, moderate for quantitative transfer to other solid columns, and absent for post-buckling or material failure. A later work item needs imperfection-shape variation, nonlinear mesh convergence, arc-length or another validated continuation method, and material nonlinearity before collapse or DNF coupling can be claimed.
