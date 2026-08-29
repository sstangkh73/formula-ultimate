# Work 039 Plan: Nonlinear Column Robustness

Status: Completed

Thai companion: `2026-08-30_039_nonlinear-column-robustness-plan.th.md`

## Objective

Test whether the Work 038 precritical nonlinear amplification result remains numerically convergent across mesh refinement and quantify how strongly it depends on the declared initial-imperfection shape.

## Scope and claim boundary

- Reuse the Work 037 cantilever column and the Work 038 CalculiX `NLGEOM` evidence route.
- Evaluate the same absolute compressive loads on the Work 037 coarse, medium, and fine meshes.
- Compare the admitted cantilever eigenmode-shaped imperfection with an independent smooth cubic crookedness having the same fixed-face offset, fixed-face slope, and free-end amplitude.
- Separate execution/evidence acceptance from the shape-robustness hypothesis outcome; a falsified hypothesis is a valid recorded experiment, not a solver failure.

This work remains precritical and linear elastic. It does not establish a limit point, post-buckling capacity, yield, fracture, fatigue, safety factor, or DNF coupling.

## Experiment design

- independent variables: mesh size, imperfection shape, and absolute compressive load;
- dependent variables: total tip offset, amplification, reaction closure, stress, axial shortening, secant-reference error, mesh-change metric, and shape-sensitivity metric;
- controls: `L,b,h,E,nu`, tip imperfection amplitude, fixed-free support, C3D4 formulation, load distribution, solver version, parsing rules, and absolute load schedule;
- execution success: all declared subcritical cases converge with fresh complete evidence, reaction closure passes, and each response is monotonic with load;
- numerical hypothesis: the eigenmode-shaped response has last-two-mesh change `<=5%` at every admitted load and matches each mesh's Work 037 secant reference within `15%`;
- robustness hypothesis: at the fine mesh, the two imperfection shapes differ in amplification by `<=10%`; a larger difference rejects robustness while retaining the measured evidence.

## Falsification and controls

The absolute load schedule is based on fractions of the fine-mesh Work 037 eigenvalue so mesh refinement is not hidden by renormalizing each load. Unit tests vary shape identity and reject unknown shapes, invalid coordinates, and supercritical secant requests. The Work 037 critical-load table and its source commit must match before execution.

## Planned files and validation

Add a versioned config, shape-aware mesh contract, Work 039 runner and launcher, focused tests, bilingual physics report, ignored experiment artifacts, and matching bilingual result logs. Run focused tests, live Work 039, Work 038 regression, full tests, compile checks, explicit staged checks, commit, and clean-tree replay.

## Risks and non-goals

The cubic imperfection is not an eigenfunction, so the single-mode secant equation is not an exact reference for it. C3D4 bending stiffness and mesh asymmetry remain possible explanations. No shell/local buckling, residual stress, manufacturing tolerance distribution, nonlinear material, contact, arc-length continuation, whole vehicle, push, or publication is included.
