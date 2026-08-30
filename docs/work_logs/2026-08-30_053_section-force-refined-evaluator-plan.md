# Work 053 Plan: Section-Force Refined Whole-Vehicle Evaluator

Status: Completed

Thai companion: `2026-08-30_053_section-force-refined-evaluator-plan.th.md`

## Objective

Replace the falsified Work 052 stress observable with a preregistered, dimensionally consistent external check: CalculiX B31 section force/moment resultants converted to extreme-fiber equivalent stress using the declared section properties. Establish an independent bounded stress/deformation evaluator only if analytical, equilibrium, refinement, cross-model, identity, and negative-control gates pass.

## Scope and planned files

- Repair the trailing-blank-line defect that `git diff --cached --check` reported in the stopped Work 052 result. Commit `37359db` is retained and will not be amended or rewritten.
- Add versioned Work 053 structural configuration with corrected output semantics and frozen upstream identities.
- Finish the project 6-DOF frame model, CalculiX deck/FRD section-resultant parser, candidate-geometry adapter, runner, PowerShell entry point, tests, bilingual physics report, and bilingual result record.
- Preserve ignored raw evidence beneath `artifacts/work053/`.

## Experiment definition

- Independent variables: nine frozen Work 050 promoted geometries, two frozen Work 048 holdout load cases, and `4/8/16` B31 subdivisions per branch.
- Dependent variables: project-frame and CalculiX maximum displacement, section force/moment, derived extreme-fiber equivalent stress, reaction residual, last-two refinement change, yield margin, solver status, and evidence hashes.
- Controls: fixed Work 050 candidate identities and ancestry; fixed Work 048 wrenches; SI units; CalculiX 2.22; synthetic isotropic `E=70 GPa`, `nu=0.3`, yield stress `250 MPa`; fixed support; square equivalent sections; and no Work 050 capacity-factor input.
- External-solver isolation: because shared nodes can average section output across unlike sections, each full coupled state is rerun once per section output set. All three decks retain the full structure and loads; only the requested result set differs. Displacements must replay consistently across those decks.
- Falsification controls: analytical cantilever, reversed load, zero stiffness, missing restraint, altered identity, incomplete DAT/FRD evidence, section-output mismatch, and deliberately undersized section.

## Validation and gates

1. Derive surface stress from CalculiX resultants `N`, `V1`, `V2`, `T`, `M1`, and `M2`; never compare integration-point material stress to root surface stress.
2. At the finest cantilever mesh, require project and CalculiX displacement/stress within `5%` of `F L^3/(3 E I)` and `6 F L/b^3`; require monotonically reduced CalculiX error.
3. Evaluate `9 x 2 x 3 = 54` structural states and three section-output decks per state, for `162` candidate CalculiX processes plus three benchmark processes.
4. Require reaction residual `<=1e-5`, last-two displacement/stress change `<=5%`, fine project/CalculiX difference `<=8%`, yield margin `>=1.1`, and displacement `<=0.02 m`.
5. Require fresh `.inp/.dat/.frd` hashes, exact replay identity, focused/full tests, compilation, repository-contract checks, fail-fast staged-diff checks, an explicit scoped commit, and clean-tree replay.

## Success criteria

- The corrected observable passes without relaxing the declared `5%`/`8%` thresholds after observation.
- Every promoted candidate/holdout either has complete converged evidence or fails explicitly.
- The final decision states only bounded linear-elastic beam-network evidence and does not imply solid/contact, nonlinear, crash, or hardware validation.

## Risks and explicit non-goals

B31, rigid joints, square equivalent sections, fixed ground, synthetic material, and quasi-static wrenches omit local solid stress concentrations, real fasteners, contact, preload, plasticity, fracture propagation, buckling, vibration, crash, fatigue life, manufacturing variation, and physical calibration. No arbitrary topology, main research campaign, push, or publication is included.
