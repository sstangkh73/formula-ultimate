# Work 086 Plan: Refined Housing Mesh Convergence

Thai companion: `2026-09-04_086_refined-housing-mesh-convergence-plan.th.md`

## Status

Status: Completed

## Objective

Resolve or confirm the single Work 085 convergence failure through a new frozen experiment. Preserve the `12%` gate and all Work 084 loads, geometry, material, solver, and evidence identities; change only the `converter_housing_mount` mesh sequence to a finer range.

Because this is another remedial item, the original roadmap integration and whole-candidate scopes move to Works 087 and 088 respectively. Historical plans/results remain unchanged.

## Scope

- Verify the exact Work 085 failed evidence SHA-256 `71244cf626bc593f953dc5c37329541eb55462340a6c28885601b4d733f2c247` and reproduce its `13.187908211258156%` housing displacement change.
- Derive a new solver config from Work 085 config identity `f23b487f5f053325a4e349f686f4a2e24af3281fe8de3e1caf8e83fb7a5aec11`.
- Preserve shaft/support meshes and all physical declarations.
- Replace only housing mesh lengths `8/6/4.5 mm` with `4.5/3.5/2.75 mm`.
- Execute all cases again so the new result remains self-contained, then replay under a second clean root.
- Keep `design_use_allowed=false` and the `synthetic_meshed_verification_only` verdict.

## Planned files

- `config/structural/refined_housing_mesh_convergence_v1.json`
- `src/formula_ultimate/structural/refined_mesh.py`
- `scripts/structural/run_refined_housing_mesh.py`
- `tests/test_refined_housing_mesh.py`
- this plan and Thai companion
- matching result and Thai companion
- ignored evidence under `artifacts/work086/`

## Validation and success criteria

- Prior failure and base-config identities match exactly.
- The derived config differs only at the declared housing mesh path.
- All nine solves converge and retain force/moment `<=1e-5`, energy `<=1e-4`, and every last-two metric `<=12%`.
- Fine p90 stress remains below synthetic yield or fails observably.
- Two clean runs reproduce derived-config, solver-result, and refinement-result identities.
- Focused, repository-contract, compilation, and full regression tests pass before commit.

## Risks and explicit non-goals

Finer meshes can still remain outside the asymptotic range or increase compute. Passing is not physical validation and does not create material/process, contact, fatigue, fastener, bearing-life, manufacturing, or safety evidence. No integration or whole-vehicle work is included.
