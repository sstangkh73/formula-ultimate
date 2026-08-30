# Work 052 Plan: Independent Whole-Vehicle Refined Stress/Deformation Evaluator

Status: Stopped

Thai companion: `2026-08-30_052_independent-whole-vehicle-refined-evaluator-plan.th.md`

## Objective

Implement and falsify an independent CalculiX beam-network finite-element evaluator that derives stiffness, displacement, stress, and reactions from selected Work 050 candidate geometry and frozen Work 048 wrenches. Close the exact `independent_refined_evaluation` blocker only if analytical benchmark, equilibrium, refinement, identity, and negative-control gates pass.

## Scope and planned files

- Add a versioned structural protocol under `config/structural/` with material evidence class, B31 formulation, refinement levels, analytical benchmark, stress/deflection limits, and exact upstream identities.
- Add a project-owned beam-network deck builder and strict CalculiX parser under `src/formula_ultimate/structural/`.
- Add an acceptance runner and `scripts/run_work052.ps1` that consume the preserved Work 050 ledgers, solve all promoted candidates on frozen holdouts, and write ignored evidence under `artifacts/work052/`.
- Add focused tests, bilingual physics report, and matching bilingual result records.

## Experiment definition

- Independent variables: promoted candidate geometry, frozen holdout load case, B31 subdivisions per branch, and analytical benchmark load.
- Dependent variables: nodal displacement field, element stress field, support reactions, maximum displacement, maximum equivalent stress, utilization/yield margin, force/moment residual, refinement change, solver status, and hashes.
- Controls: exact candidate variables and ancestry from the immutable Work 050 ledger; fixed Work 048 wrenches; SI units; CalculiX 2.22; isotropic synthetic `E`, `nu`, and yield stress; fixed support; element orientation; and no capacity-factor input from Work 050.
- Falsification controls: analytical cantilever, reversed-load sign, zero stiffness, missing restraint, altered candidate identity, incomplete solver output, and deliberately undersized section.

## Validation

1. Verify the B31 deck/parser against cantilever reaction, tip deflection `F L^3/(3 E I)`, and bending stress `6 F L/b^3` within declared tolerances.
2. Solve each of nine promoted candidates for both frozen holdout cases at `1/2/4` elements per branch.
3. Require fresh `.inp/.dat/.frd` evidence and exact solver/tool/config/candidate hashes.
4. Require force and moment reaction residual `<=1e-5` relative and last-two displacement/stress change `<=5%`.
5. Require finite stress/deformation, positive stiffness, and declared yield margin `>=1.1` for promotion.
6. Run repository-contract, focused/full unit, compile, staged-diff, and clean-tree replay gates.

## Success criteria

- The analytical benchmark passes without changing thresholds after solver observation.
- Every promoted candidate/holdout produces complete converged stress/deformation evidence or an explicit failure.
- Same-input runs preserve result identities; malformed or singular models fail closed.
- The evaluator never reads Work 050 capacity factors and therefore supplies an independent structural evidence path.

## Risks

B31 is a one-dimensional beam idealization of the primitive assembly. Section selection, rigid joints, fixed ground support, linear elasticity, and scaled quasi-static wrenches omit solid stress concentrations, contact, preload, local plate behavior, nonlinear material response, buckling, and transient dynamics. Passing Work 052 can support only the bounded grammar/load/material/beam domain.

## Explicit non-goals

No solid whole-vehicle C3D10 model, nonlinear contact, fracture propagation, crash, vibration, CFD, real material certification, physical test, arbitrary topology, main campaign, push, or publication is included.
