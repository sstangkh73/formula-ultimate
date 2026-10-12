# Work 158 Plan: v2 Hex-Socket Fasteners as Threaded Joints

Thai companion: `2026-10-12_158_v2-hex-socket-fasteners-plan.th.md`

Date: 2026-10-12

Status: Completed

## Objective

Goal v2 Tier B10 requires at least 8 `threaded` interfaces per seed. Each one
carries `axis_point_m` and a unit `axis_dir`; the axis line must miss all
material of one part (a through-hole, genus >= 1, with material in all 8
radial directions around the axis point) and cross the material of the other
part (at least 2 triangle hits). Since Work 156 the v2 generator emits no
`threaded` interface (seed 11: 0 < 8).

Add a post-refinement fastener step. For a seed-chosen subset of leaves that
Work 157 left unbored, cut an axial regular-hexagon socket through the leaf
(a `hole` loop in the extruded profile) and add a new pin leaf: a hexagonal
prism seated in the socket with a declared clearance. The pin and the holed
leaf are joined by a `threaded` interface whose axis is the socket axis.

## Geometry rules (SI units, local leaf frame of the holed leaf)

- Holed leaf extrudes along local +z from `z = 0` to `z = h`;
  `rho = inscribed_radius_m - linear_tolerance_m`.
- Socket: regular hexagon, apothem `a`, phase `phi`, centre `(ox, oy)`,
  circumradius `R = a / cos(pi/6)`. Rule `|(ox, oy)| + R <= (1 - wall) rho`
  keeps it inside the inscribed circle (so inside the outer loop).
  `a >= min_apothem_m`.
- Cap exits: centres `(ox, oy, 0)` and `(ox, oy, h)` in world coordinates must
  be at least `patch radius + R + linear tolerance` from every contact patch
  the cap receives (Work 157 `contact_patches`).
- Pin: hexagonal prism with the same phase, apothem `a - c`, height `h - 2c`,
  local translation `(ox, oy, c)` followed by the holed leaf's placement.
  Clearance `c = 2.5e-5 m` (a quarter of the 1e-4 m contact tolerance), so the
  flat pin faces are parallel to the socket faces at distance `c`: measured
  contact gap `c <= tolerance`, no interpenetration. Planar faces tessellate
  exactly, so this holds on the meshes (up to float32 rounding, ~1e-7 m).
- Threaded axis: `axis_point_m` = world image of `(ox, oy, h/2)` (inside the
  holed part's thickness), `axis_dir` = world image of local +z.
- The pin leaf is a new child of the holed leaf's parent assembly (so it lies
  in the same capability subtree), with a material drawn per pin from the
  declared catalogue. Assembly masses roll up from measured meshes as before.

## Scope

- New `src/formula_ultimate/hierarchy/fasteners.py` (pure Python): config,
  socketed grammar version, `socket_program`, `pin_program`,
  `validate_v2_program`, `add_fasteners`, `fastener_problems`.
- `scripts/hierarchy/functional_realization.py`: validate with
  `validate_v2_program` so socketed programs realize.
- `src/formula_ultimate/hierarchy/functional.py`: `with_threaded_axes`.
- `scripts/hierarchy/generate_functional_vehicle.py`: run the fastener step
  after refinement, add axes, hash the fastener config.
- New tests `tests/test_hierarchy_fasteners.py`.

## Planned files

- `src/formula_ultimate/hierarchy/fasteners.py` (new)
- `scripts/hierarchy/functional_realization.py`
- `src/formula_ultimate/hierarchy/functional.py`
- `scripts/hierarchy/generate_functional_vehicle.py`
- `tests/test_hierarchy_fasteners.py` (new)
- this plan and result pair (English and Thai)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## Validation

1. `python -m unittest tests.test_hierarchy_fasteners tests.test_hierarchy_leaf_refinement tests.test_hierarchy_functional -v`
2. Generator run for seed 11 under the CAD runtime into `artifacts/work158/`
   and a spot check with the acceptance helpers (B10 condition, interface
   gaps, penetration of pins).
3. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gates 1 and 2 must pass;
   Gate 3 recorded per tier.

## Success criteria

- Gates 1 and 2 pass. Every Tier A test still passes. TierB10 passes for seeds
  11, 23 and 37.

## Failure criteria

- Fewer than 8 sockets fit on some seed, a pin interpenetrates or loses
  contact, or any Tier A test regresses.

## Risks

- Too few unbored leaves with room clear of contact patches. Mitigation:
  declared probability and draw count; record per-seed counts.
- CAD hole-loop orientation or nesting fails. Mitigation: CAD test.

## Non-goals

- No helical thread geometry (the contract checks through-holes only), no
  preload or load-path claim, no change to v1 modules or existing tests.
