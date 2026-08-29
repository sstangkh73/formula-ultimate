# Work 041 Plan: Near-Critical Mesh and Element Verification

Status: Completed

Thai companion: `2026-08-30_041_near-critical-mesh-element-verification-plan.th.md`

## Objective

Resolve or retain the Work 039 near-critical numerical-convergence rejection by extending C3D4 refinement below `1.0 mm` and comparing an independently declared C3D10 route at a comparable degree-of-freedom budget.

## Scope and claim boundary

- Reuse the Work 037-039 cantilever geometry, synthetic elastic material, fixed support, `e0=0.1 mm` eigenmode imperfection, and fixed absolute compression schedule.
- Evaluate C3D4 mesh sizes `1.0`, `0.8`, and `0.65 mm` and one C3D10 mesh chosen by a mesh-only resource pilot before the admitted solver config is frozen.
- Run ideal eigenvalue and precritical `NLGEOM` evidence while preserving exact mesh/deck/result hashes and solver confirmation.
- Separate experiment execution from the convergence hypothesis. A rejected hypothesis is a completed measured result and blocks promotion; it is not permission to relax a gate.

This work verifies numerical adequacy only for the declared precritical column fixture. It does not validate post-buckling capacity, plasticity, fracture, fatigue, safety, or any vehicle component.

## Experiment design

- independent variables: element family/order, characteristic mesh size, and absolute compressive load;
- dependent variables: eigenvalue `Pcr`, nonlinear amplification, stress, strain energy where available, reactions, solver iterations/status, nodes/DOFs, tetrahedra, wall time, memory proxy, and artifact hashes;
- controls: `L=0.2 m`, `b=h=0.01 m`, `E=70 GPa`, `nu=0.3`, fixed-free support, `e0=0.1 mm`, cantilever eigenmode shape, CalculiX/Gmsh versions, load distribution, parsing rules, and absolute loads `1857.580`, `2600.612`, `3157.886 N`;
- falsification: retain the highest load, use the same absolute loads for every mesh, reject missing/malformed/non-finite evidence, and record a changed mode family or non-convergence.

## Proposed gates

- complete finite evidence and reaction residual `<=1e-5` for every admitted static case;
- last-two C3D4 amplification change `<=5%` at every absolute load;
- refined C3D4 versus admitted C3D10 amplification difference `<=5%`;
- eigenmode secant error `<=15%` and the lowest physical eigenmode remains global transverse bending;
- C3D10 mesh node count must be declared after the mesh-only pilot and remain within `25%` of the finest admitted C3D4 node count unless the result is explicitly classified as not compute-comparable.

## Planned implementation and validation

Add an element-aware mesh/deck/parser contract, versioned frozen config, Work 041 runner and launcher, focused tests, bilingual physics report, ignored solver evidence, and matching bilingual result logs. Validate element connectivity/order, consistent quadratic-face loading, negative malformed-element fixtures, focused/full tests, Work 039 regression, compile checks, staged diff checks, explicit commit, and clean-tree replay.

## Risks and non-goals

Fine C3D4 eigenvalue extraction may be compute/memory intensive; the runner must fail observably rather than silently coarsen. Gmsh and CalculiX quadratic tetrahedral node ordering must be verified before admission. Comparable node/DOF count is not equal truncation error. No mass optimization, material nonlinearity, interface contact, arc-length continuation, whole vehicle, push, or publication is included.
