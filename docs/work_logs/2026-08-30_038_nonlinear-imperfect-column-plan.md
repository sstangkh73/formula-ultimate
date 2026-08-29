# Work 038 Plan: Nonlinear Imperfect Column

Status: Completed

Thai companion: `2026-08-30_038_nonlinear-imperfect-column-plan.th.md`

## Objective

Verify that a declared initial column crookedness couples axial compression into lateral displacement through CalculiX geometric nonlinearity, before any instability-sensitive result can affect candidate fitness.

## Scope and claim boundary

- Reuse the Work 037 cantilever solid-column physics and C3D4 route.
- Seed a deterministic cantilever first-mode-shaped imperfection at multiple amplitudes.
- Solve multiple subcritical load fractions with `NLGEOM`, then compare total tip offset and amplification against the elastic secant-column relation using the matched Work 037 mesh eigenvalue as the numerical reference.
- Gate force/reaction closure, solver completion, monotonic response, cross-amplitude consistency, analytical agreement, and artifact freshness.

This work verifies precritical geometric-nonlinearity and imperfection sensitivity only. It does not establish post-buckling capacity, collapse load, allowable load, yield, fracture, or fatigue.

## Experiment design

- independent variables: initial tip imperfection amplitude and compressive load fraction;
- dependent variables: incremental and total lateral tip offset, amplification factor, secant-reference error, axial shortening, stress, reaction closure, convergence status, and artifact hashes;
- controls: `L,b,h,E,nu`, cantilever support, C3D4 mesh, load distribution, solver version, imperfection shape, and parsing rules;
- falsification: a perfect symmetric control must not invent material lateral motion below critical load; a geometrically linear control must fail the required nonlinear amplification response; malformed or stale solver evidence must be rejected.

## Analytical reference and proposed gates

For a mode-shaped imperfect elastic column, use `A(P)=1/(1-P/Pcr)` as the precritical secant amplification reference, with total free-end offset `e(P)=e0*A(P)`. The numerical `Pcr` is pinned to the matching Work 037 mesh and the Euler value is retained as a separate comparison. Proposed gates include reaction residual `<=1e-5`, monotonic amplification with load, normalized response spread across admitted imperfection amplitudes `<=10%`, and secant-reference relative error `<=15%` over the declared subcritical range.

## Planned files and validation

Add a versioned config, nonlinear-imperfection contract/runner, launcher, focused tests, bilingual physics report, experiment artifact, and matching bilingual result logs. Run focused tests, live Work 038, Work 037 regression, full tests, compile checks, staged diff checks, explicit commit, and clean-tree replay.

## Risks and non-goals

Load-controlled static analysis may not continue through a limit point, tetrahedral bending stiffness may bias amplification, and large imperfections may leave the small-deflection secant regime. These are observable limitations, not values to silently correct. No arc-length continuation, plasticity, contact, local shell buckling, fracture, fatigue, whole vehicle, push, or publication is included.
