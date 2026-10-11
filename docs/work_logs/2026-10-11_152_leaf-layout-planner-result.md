# Work 152 Result: Leaf Layout Planner

Thai companion: `2026-10-11_152_leaf-layout-planner-result.th.md`

Date: 2026-10-11

Status: Completed

Plan: `2026-10-11_152_leaf-layout-planner-plan.md`

## Files changed

- `src/formula_ultimate/hierarchy/layout.py` (new): `layout(tree, config)`,
  `leaf_faces(program)`, `contact_problem(cap, face)`,
  `layout_problems(result, tree)`, and the `LayoutConfig`, `PlacedLeaf`,
  `PlannedInterface` and `LayoutResult` dataclasses.
- `tests/test_hierarchy_layout.py` (new, 8 tests).
- This result pair, the plan pair (status), and `auto-loop/progress.md` /
  `auto-loop/progress.th.md`.

## What was built

- Each leaf is placed with its extrusion axis on a vehicle axis. Its box is
  exact for polyline profiles (the transformed prism vertices) and
  conservative for B-spline profiles (`outer_radius_m` across the axis).
- Contact faces: the two flat caps (disks) and, for polyline profiles, one
  convex-hull side face whose outward normal the planner puts on a vehicle
  axis by choosing the spin. That face is an exact planar rectangle lying in
  the box face.
- Growth: root anchor leaf at the origin; each assembly grows its anchor
  child, then attaches each satellite's anchor leaf (cap first) to a face of
  a leaf already placed inside the same assembly, then grows the satellite.
- Fit rule: "inside" (source cap disk plus offset inside the target's
  inscribed disk or rectangle) or "around" (the target face inside the
  source's inscribed disk). A fresh source leaf keeps its per-leaf random
  shape and may be resized between 0.004 m and 4x its planned length.
- Collision rule: leaf boxes are pairwise interior-disjoint (touching is
  allowed), so touching leaves are separated by their shared plane.
- Room keeping: a first pass also requires a claim box (the satellite
  assembly's planned length beyond and across the face) to be free; a second
  pass drops it. Up to 16 deterministic layout attempts with a fresh
  placement random stream (per-leaf shapes unchanged).

## Decisions and deviations from the plan

- The plan said targets come from the anchor child's subtree. In practice an
  anchor child that is a single leaf has only two caps, so the third
  satellite had no room. Targets are any leaf already placed in the same
  assembly. Connectivity is preserved: each satellite joins the connected
  set.
- The plan only had cap-to-cap contact. With caps only, every leaf inherits
  the root axis and the vehicle grows as a single column that crowds itself
  (every seed failed). The flush polyline side faces were added to change
  axis.
- The plan only had shrinking. Shrinking cascaded (a shrunk anchor forced its
  satellites smaller), so "around" fits that enlarge the fresh source were
  added, plus the room-keeping pass and the deterministic attempts.

## Validation

1. `python -m unittest tests.test_hierarchy_layout -v`: exit 0,
   `Ran 8 tests in 19.173s`, `OK`.
2. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 PASS. Gate 2
   `Ran 1082 tests in 369.096s`, `OK (skipped=11)`. Gate 3 `FAILED
   (failures=13)` because `scripts/hierarchy/generate_hierarchical_vehicle.py`
   does not exist yet (expected).

## Evidence (scratch scripts under gitignored `artifacts/work152/`)

- Pure layout sweep, seeds 0..62: 62 of 63 seeds lay out with
  `layout_problems == []` (attempts used 0..3, 2.0..9.6 s each). Seed 4 fails
  all 16 attempts with `LayoutFailure` (crowding). Leaves use all three axes.
  Per seed, interfaces are about 45 % inside-cap, 33 % around-cap, 18 %
  inside-side and 2 % around-side. The ratio of largest to smallest
  characteristic length is 110..431.
- CAD spot check (`.tools/cadquery-mcp/Scripts/python.exe
  artifacts/work152/cad_spot_check.py SEED 1e-4`): every leaf of seeds 11,
  23 and 37 realized with `realize_leaf` (226/229/229 leaves, 9.3..13.9 s).
  Measured with the acceptance suite's own functions:
  - interface gap at most 8.5e-18 m on all 225/228/228 interfaces;
  - 0 mesh-box pairs overlapping by more than 1e-4 m, so the maximum
    penetration depth is 0;
  - box-like leaf fraction 0.0;
  - bounding-box diagonal ratio 139.3, 178.7 and 266.5.
  This is not Gate 3 evidence: no manifest or generator exists yet.

## Limitations

- Seed 4 has no layout under this config. The generator will need a declared
  fallback (for example the next decomposition attempt), or the failure must
  be reported.
- Box disjointness is conservative. The vehicle is sparse and its shape has no
  packaging meaning. Interfaces are geometric contact only, with no load,
  thermal or functional meaning. None of this is physical validation.
- `interference_m` is never used. Interference joints are planned as touching
  contact.
- Contact faces are limited to caps and at most one side face per polyline
  leaf.

## Follow-up

- Next work item: the generator CLI
  `scripts/hierarchy/generate_hierarchical_vehicle.py`. Decompose, lay out,
  realize every leaf, write the manifest (catalog-only material ids with
  synthetic, labelled densities, or a declared density source that stays out
  of tracked files), roll up mass and centre of mass from the meshes, and
  ensure deterministic replay.
