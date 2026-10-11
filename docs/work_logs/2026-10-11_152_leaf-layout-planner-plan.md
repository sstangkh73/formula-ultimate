# Work 152 Plan: Leaf Layout Planner

Thai companion: `2026-10-11_152_leaf-layout-planner-plan.th.md`

Date: 2026-10-11

Status: Completed

## Objective

Milestone 4 of `auto-loop/GOAL.md`: place every leaf of a Work 150 abstract
tree in vehicle coordinates and turn every Work 150 attachment into a planned
interface with measurable flat cap-to-cap contact and no interpenetration.
This is pure-Python planning. CAD realization of the planned programs is the
next work item.

## Scope

- New module `src/formula_ultimate/hierarchy/layout.py`:
  - `layout(tree, config)` returns per-leaf placed programs (Work 151
    `leaf_program` + `placement_transforms`) and planned interfaces.
  - Procedure (declared, seed-driven, no part catalogue): place the root
    anchor leaf at the origin, then recurse depth-first: lay out an
    assembly's anchor child first, then for each satellite child place the
    satellite's anchor leaf on a flat cap of a leaf already placed in the
    anchor child's subtree, and recurse into the satellite. The attachment
    target is re-chosen at layout time (the decomposition's target is a
    random leaf of the same anchor subtree, so connectivity is unchanged).
  - Contact rule: the two leaves are coaxial on the shared cap axis, their
    caps lie in the same plane, and the smaller cap disk
    (`outer_radius + |offset|`) fits inside the larger cap's
    `inscribed_radius` minus its linear tessellation tolerance. If neither
    order fits, the source leaf is scaled down (same per-leaf random draw,
    smaller length) but never below `min_leaf_length_m`.
  - Collision rule: the conservative axis-aligned box of every leaf
    (`outer_radius` across the axis, `[0, h]` along it) is interior-disjoint
    from every other leaf box. Touching is allowed. Measured mesh boxes lie
    inside these boxes, so the acceptance penetration test has no
    overlapping pairs to examine.
  - `layout_problems(result)` re-checks box disjointness, cap contact and
    containment from the placed programs with `transform_points`.
- New tests `tests/test_hierarchy_layout.py`.

## Planned files

- `src/formula_ultimate/hierarchy/layout.py` (new)
- `tests/test_hierarchy_layout.py` (new)
- this plan and result pair (English and Thai)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## Validation

1. `python -m unittest tests.test_hierarchy_layout -v`
2. `pwsh -NoProfile -File auto-loop/verify.ps1` (Gates 1 and 2 must pass;
   Gate 3 still fails because the generator does not exist yet).

## Success criteria

- Seeds 11, 23, 37 and a sweep of further seeds lay out every leaf with no
  failure, deterministically.
- `layout_problems` is empty: boxes pairwise interior-disjoint, every
  interface coaxial with coplanar caps and the smaller cap inside the larger
  cap's inscribed disk.
- Every assembly's children are connected by the planned interfaces.
- A deliberately overlapping or separated layout is reported by
  `layout_problems` (falsification test).

## Risks

- Crowding: a growing subtree may find no free cap, causing failures. These
  are raised as `LayoutFailure`, never hidden.
- Scaling down sources lowers some leaf sizes; the measured size span still
  has to be checked after CAD realization.
- Box disjointness is conservative and makes the vehicle sparse; that is a
  representation choice, not a design claim.

## Non-goals

- No CAD execution, STL, manifest, generator CLI or materials.
- No physical validation, no load paths, no packaging optimisation.
