# Work 075 Plan: Geometry-Derived Linkage Motion Ratio

Status: In progress

Thai companion: `2026-09-02_075_geometry-linkage-motion-ratio-plan.th.md`

## Objective and scope

Replace Work 073's implicit one-to-one suspension displacement boundary with an explicit small-angle rocker/link geometry. Derive each contact's motion ratio from declared 3D pivot, rotation axis, wheel pickup, spring pickup, wheel direction, and spring axis. Transform spring stiffness, damping, and travel into wheel coordinates before Work 073 solves vertical loads.

This is geometry-causal Level-0 linkage evidence on synthetic declared points, not detailed CAD joint validation.

## Experiment design

- Independent variables: pivot/pickup coordinates, rotation axis, spring/wheel directions, spring stiffness/damping, and spring travel.
- Dependent variables: projected lever arms, motion ratio, wheel-coordinate stiffness/damping/travel, Work 073 load/body/energy response, and terminal failure.
- Controls: unit-ratio preservation, doubled spring arm, spatial mirror, zero projected wheel arm, collinear spring arm, axis scaling, permutation, and changed geometry identity.
- Preferred hypothesis: `r = d_spring/d_wheel` derived from geometry causes `k_wheel = k_spring r^2`, `c_wheel = c_spring r^2`, and wheel travel limit `s_limit/r`; changing geometry changes vehicle response while unit ratio preserves Work 073.
- Falsification: using declared ratio instead of deriving it, missing virtual-work scaling, sign ambiguity hidden by clipping, degenerate geometry accepted, energy drift, or geometry change not affecting response identity.

## Planned files

- `config/vehicle/geometry_linkage_motion_ratio_v1.json`
- `src/formula_ultimate/simulation/linkage_motion_ratio.py`
- simulation exports, runner, tests, bilingual research/result records
- ignored evidence under `artifacts/work075/`

## Validation and success criteria

Analytical lever cases and mirrored geometry must close within `1e-12`; degeneracies and non-finite geometry must fail closed. Unit ratio must retain the Work 073 result hash. Non-unit geometry must alter stiffness/travel and coupled response with bounded equation/energy residuals. Replay, geometry mutation identity, focused/full tests, compilation, bilingual contract, scoped commit, and post-commit replay must pass.

## Risks and explicit non-goals

The small-angle rigid-rocker model omits arcs at large travel, joint compliance/backlash/friction, pushrod geometry, anti-dive/squat, collision, bearing stress, fastener loads, and CAD assembly constraints. Declared points are not yet extracted from STEP/FreeCAD solids.
