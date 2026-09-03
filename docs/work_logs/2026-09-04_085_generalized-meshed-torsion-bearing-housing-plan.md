# Work 085 Plan: Generalized Meshed Torsion, Bearing, and Housing Route

Thai companion: `2026-09-04_085_generalized-meshed-torsion-bearing-housing-plan.th.md`

## Status

Status: Stopped

## Objective

Close the explicit meshed-structural blocker recorded by Work 084 without modifying Work 082 or rewriting Work 084. Add a new exact-geometry Gmsh/CalculiX route that supports arbitrary principal-axis end faces, cylindrical bearing surfaces, combined force/torque loads, and arbitrary support planes, then apply it to the exact Work 084 `output_shaft`, `support_block`, and `converter_housing` STEP artifacts.

This remedial work is inserted before the original integration scope. Consequently, the former roadmap Work 085 integration becomes Work 086 and the former Work 086 whole-mechanical candidate becomes Work 087. The historical roadmap remains unchanged as append-oriented evidence.

## Scope and frozen experiment

- Identity-couple all cases to Work 084 result `c87fa43572efc0a8bc6ef67e375589943d73ecc4ca3b3a3d7a51df4ddb3edb66`, its canonical FreeCAD report, and each exact STEP hash.
- Mesh three exact parts independently with three preregistered characteristic lengths each.
- `output_shaft_combined`: apply the declared `415.3846153846154 N` radial Work 083 interface reaction plus `22.8 Nm` output torque at the `y=0.019 m` end; constrain the `y=0.086 m` end.
- `support_block_bearing`: apply the declared `384.6153846153847 N` support reaction over its `y`-axis bore; constrain its `x=-0.100 m` mounting plane.
- `converter_housing_mount`: apply the declared `8 Nm` converter reaction torque over its `y`-axis bore; constrain its `x=-0.080 m` mounting plane.
- Build surface-consistent nodal forces and couples, report reactions, displacement, compliance, p90 von Mises stress, external/internal work, and force/moment residuals.
- Run mesh convergence independently per case; do not hide non-convergence or failed/invalid states.
- Keep Work 079 material identity and `design_use_allowed=false`; meshed software evidence is not physical validation.
- Inject a severed-support control for every case and require zero transmitted load plus subsystem rejection/`DNF`.
- Run two clean solver roots and compare canonical identities.

Independent variables are exact part, load-region type, support plane, force, torque, mesh length, and connection state. Dependent variables are node/element counts, mapped surface nodes/area, displacement, compliance, p90 stress, force/moment/energy residuals, convergence, elastic/yield state, and failure propagation. Controls are exact replay, identity mutation, missing surface, non-finite load, mesh non-convergence, and severed support.

## Planned files

- `config/structural/generalized_meshed_torsion_bearing_housing_v1.json`
- `src/formula_ultimate/structural/generalized_coupling.py`
- `scripts/structural/run_generalized_structural_coupling.py`
- `tests/test_generalized_structural_coupling.py`
- `docs/contracts/GENERALIZED_MESHED_STRUCTURAL_COUPLING_V1.md` and Thai companion
- this plan and Thai companion
- matching result and Thai companion after validation
- ignored evidence under `artifacts/work085/`

## Validation

1. Run all nine exact-geometry Gmsh/CalculiX solves under a clean output root.
2. Check surface mapping, solver freshness/convergence, force/moment/energy closure, and per-case last-two-mesh changes.
3. Run a second clean root and compare result plus canonical solver-artifact identities.
4. Run focused tests, repository-contract tests, Python compilation, and the full repository suite.
5. Stage only Work 085 files, run `git diff --cached --check`, commit, and repeat focused post-commit validation.

## Success criteria

- All exact STEP and upstream result/report identities match before meshing.
- Each declared load and support region maps uniquely and does not overlap.
- All nine solver cases converge without hidden geometry repair or silent state correction.
- Force and moment residuals are each `<=1e-5`; energy residual is `<=1e-4`.
- For every case, each of maximum displacement, compliance, and p90 stress changes by `<=12%` between the last two mesh levels.
- Elastic cases remain below the synthetic yield value or fail observably; no stress clipping is permitted.
- Every severed-support control removes transmitted load and causes rejection/`DNF`.
- Two runs reproduce the config/result and canonical mesh/deck/DAT/FRD identities.
- Verdict remains `synthetic_meshed_verification_only` and `design_use_allowed=false`.

## Risks

- Curved-surface node mapping can fail on generated mesh tolerances.
- Local stress concentration or coarse tetrahedra can prevent p90 convergence.
- The housing geometry may require coarser levels to keep compute bounded.
- Algebraic nodal couples can close global equilibrium while remaining a simplified bearing/contact representation.

## Explicit non-goals

- No physical validation, fatigue, fracture, nonlinear contact, fastener, bearing-life, lubrication, manufacturing, or safety claim.
- No change to Work 082 identities or retroactive change of Work 084 status.
- No design admission from synthetic material/process evidence.
- No load-structure integration or whole-vehicle candidate in this work item.
