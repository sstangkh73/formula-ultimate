# Work 037 Plan: Eigenvalue Buckling Verification

Status: Completed

Thai companion: `2026-08-30_037_eigenvalue-buckling-plan.th.md`

## Objective

Verify the installed CalculiX linear-buckling route against an Euler column before any buckling result can affect candidate fitness.

## Scope and claim boundary

- Use a slender solid rectangular cantilever column with declared effective-length factor `K=2`; this avoids pretending that a solid-face constraint is an ideal pin.
- Generate three C3D4 meshes, apply a finite distributed compressive reference load, request the lowest four buckling factors, parse fresh eigenvalue/mode evidence, and compare `Pcr = pi^2*E*I/(K*L)^2`.
- Gate load/reaction identity, lowest positive global bending mode, orthogonal near-degenerate mode pair, analytical error, and mesh convergence.
- Preserve exact tools, decks, outputs, hashes, failures, and deterministic replay.

This verifies only ideal linear elastic eigenvalue buckling. It is not an allowable load or physical capacity. Nonlinear geometry with seeded imperfections and post-buckling response remains a separate required work item.

## Experiment design

- independent variable: mesh size at three declared levels;
- dependent variables: buckling factors/loads, mode ordering and transverse/axial mode content, reaction closure, volume, convergence, solver status, artifacts and time;
- controls: `L,b,h,E,nu`, fixed-free support, `K=2`, reference compression, element type/order, solver and parsing rules;
- falsification: reverse the load to tension and require no admitted positive compression mode; remove the clamp and require rejection; vary `L,E,I` in analytical unit tests.

## Analytical reference and gates

For bending about both equal section axes, `I=b*h^3/12` and `Pcr=pi^2*E*I/(2L)^2`. The first two physical modes should form a near-degenerate orthogonal bending pair. Proposed gates: first-mode load error `<=10%`, last-two change `<=5%`, pair split `<=5%`, reaction residual `<=1e-6`, and mode transverse-to-axial amplitude ratio `>=10`.

## Planned files and validation

Add a versioned config, buckling contract/parser/runner, launcher, tests, bilingual physics report and matching result logs. Run focused tests, live Work 037, Work 034-036 regressions, full tests, compileall, diff checks, explicit commit, and clean-tree replay.

## Risks and non-goals

C3D4 bending stiffness and faceted geometry may require refinement. Eigenvalue signs/order and `.dat/.frd` formats are solver-version specific and must fail closed. No imperfection, nonlinear collapse, local shell buckling, yield, fracture, fatigue, safety factor, whole vehicle, push, or publication is included.
