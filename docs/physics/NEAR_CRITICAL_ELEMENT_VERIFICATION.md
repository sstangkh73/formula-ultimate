# Near-Critical Mesh and Element Verification

Thai companion: `NEAR_CRITICAL_ELEMENT_VERIFICATION.th.md`

## Claim and outcome

Work 041 completed a solver-backed, precritical verification experiment for the Work 037-039 imperfect cantilever column. The execution gates passed, but the combined convergence hypothesis was **rejected**. The last two C3D4 meshes agreed within the declared `5%` limit at all loads, while refined C3D4 and C3D10 differed by `9.213%` at the highest load. Therefore this evidence does not admit post-buckling capacity or whole-vehicle structural claims.

This is numerical-element verification for a synthetic elastic fixture. It is not material validation, component certification, fracture evidence, fatigue evidence, or a safety factor.

## Physics fixture

The controlled specimen is a fixed-free square column with `L=0.2 m`, `b=h=0.01 m`, `E=70 GPa`, `nu=0.3`, and a synthetic density of `2700 kg/m^3`. A transverse eigenmode imperfection is scaled to `e0=0.1 mm`. Every mesh receives the same absolute compression loads: `1857.580`, `2600.612`, and `3157.886 N`.

The analytical checks are

```text
I = b h^3 / 12
Pcr = pi^2 E I / (K L)^2, K = 2
amplification = 1 / (1 - P/Pcr)
```

The analytical Euler load is `3598.293 N`. The eigenmode secant relation is used only in the precritical region and is not a post-buckling constitutive model.

## Element definitions and frozen pilot

The implementation reads Gmsh MSH2 linear and quadratic tetrahedra and boundary triangles. Gmsh identifies type `4` as a four-node tetrahedron, type `11` as a ten-node second-order tetrahedron, type `2` as a three-node triangle, and type `9` as a six-node second-order triangle. CalculiX documents C3D10 as a ten-node quadratic tetrahedron with four integration points. The converter applies the verified Gmsh-to-CalculiX final edge-node swap and uses consistent quadratic face loads.

Before any C3D10 solver result was observed, a mesh-only pilot froze C3D10 at `1.4 mm`: C3D4 `0.65 mm` had `65,835` nodes and C3D10 `1.4 mm` had `57,426` nodes. The pilot's C3D4-denominator difference was `12.773%`; the admitted runner's symmetric comparison was `13.644%`. Both are below the declared `25%` compute-comparability limit. Comparable node count does not imply comparable truncation error.

## Experimental design

- Independent variables: element family/order, characteristic mesh size, and absolute compression load.
- Dependent variables: eigenvalue critical load, nonlinear amplification, stress, reactions, solver status, mesh size, wall time, and artifact hashes.
- Controls: geometry, material parameters, support, eigenmode imperfection, load distribution, absolute loads, Gmsh/CalculiX route, and parsing rules.
- Preferred hypothesis: the last two C3D4 meshes and the refined C3D4/C3D10 routes each differ by at most `5%` at every load.
- Falsification: retain the highest load, reject missing/non-finite results, do not replace absolute loads with per-mesh load fractions, and record a changed mode or failed solve.

## Results

| Mesh | Nodes | Tetrahedra | Eigenvalue `Pcr` (N) | Amplification at 1857.580 N | at 2600.612 N | at 3157.886 N |
|---|---:|---:|---:|---:|---:|---:|
| C3D4, 1.0 mm | 20,514 | 95,711 | 3715.160 | 1.9971 | 3.3269 | 6.6413 |
| C3D4, 0.8 mm | 36,927 | 182,285 | 3675.360 | 2.0201 | 3.4160 | 7.0795 |
| C3D4, 0.65 mm | 65,835 | 337,805 | 3649.524 | 2.0343 | 3.4744 | 7.3923 |
| C3D10, 1.4 mm | 57,426 | 35,460 | 3599.539 | 2.0641 | 3.5986 | 8.1062 |

The C3D4 `0.8 -> 0.65 mm` amplification changes were `0.702%`, `1.694%`, and `4.323%`; all passed the `5%` gate. Refined C3D4 versus C3D10 differences were `1.455%`, `3.512%`, and `9.213%`; the high-load case failed the `5%` gate. Maximum secant error was `0.539%`, maximum analytical eigenvalue error was `3.248%`, and all admitted reaction residuals were zero at the parser precision.

## Evidence assessment

Supporting evidence:

- all admitted meshes solved with finite results, preserved hashes, and the same global transverse-bending mode family;
- C3D4 refinement now passes its declared last-two-mesh gate;
- C3D10 predicts the analytical eigenvalue within `0.035%` and all nonlinear cases remain close to the secant reference;
- the C3D4/C3D10 node budgets pass the frozen comparability gate.

Contradicting evidence:

- element-family amplification differs by `9.213%` at `3157.886 N`, so the preferred combined convergence hypothesis is rejected;
- the disagreement grows with proximity to critical load, exactly where the intended claim is most sensitive.

Alternative explanations include differing interpolation error, imperfection transfer, surface-load discretization, and the inadequacy of node count as an equal-accuracy measure. Missing evidence includes an asymptotic C3D10 refinement series, a second verified solver or element formulation, independently validated strain-energy parsing, measured process peak memory, and any post-critical continuation.

Confidence is high that the recorded solver paths and declared gates reject element-family agreement for this fixture. Confidence is low for any post-buckling inference because that region was not tested and Gate A remains open. Work 042 plasticity work may proceed as an independent evidence stream, but post-buckling promotion remains blocked pending a new remedial mesh/element study.

## Reproduction

```powershell
.\scripts\run_work041.ps1
py -3.14 -m unittest tests.test_element_verification tests.test_eigenvalue_buckling_acceptance tests.test_nonlinear_imperfect_column -v
```

The machine-readable evidence is written to `artifacts/work041/experiment_summary.json` and is intentionally ignored by Git. A clean-tree replay is required after the implementation commit so the summary records that exact commit and `worktree_dirty_during_run=false`.
