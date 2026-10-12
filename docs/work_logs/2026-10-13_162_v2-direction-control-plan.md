# Work 162 Plan: v2 direction control (steering post and arm)

Thai companion: `2026-10-13_162_v2-direction-control-plan.th.md`

Status: Completed

## Objective

Add a direction-control mechanism to the v2 mechanism layer so the package
carries real `direction_control` evidence: a revolute motion about a vertical
axis (>= 30 deg from every ground-propulsion axis, which are along y), range
>= 0.2 rad, with a `bearing` interface to a fixed part, sweeping without
collision and attached to the structural deck.

## Design

- New pure-Python module `src/formula_ultimate/hierarchy/direction_control.py`
  with `add_direction_control(layer, seed, catalogue, config)` (extends the
  layer from `add_ground_contacts`) and `direction_control_problems(layer)`.
- One root-level assembly `m<k>-direction_control` tagged
  `[direction_control]` in the deck bay (`bay_x0..core_x1`) on the deck top,
  three `func-leaf-mechanism-v2` prisms extruded along +z:
  - boss: regular N_b-gon plate on the deck top (`bonded` to the deck);
  - post: regular N_p-gon prism on the boss top (`bonded` to the boss);
  - arm: convex lever plate (hub polygon plus a tip polygon, convex hull)
    with a 96-gon bore of apothem `r_p + c` (c = 2.5e-5 m, a bore vertex at
    every post vertex direction), floating `c` above the boss top; `bearing`
    to the post.
- Motion `<assembly>.steer` = {arm}, revolute about +z through the post axis,
  range drawn in [0.3, 0.8] rad.
- The post sits at the +x end of the bay, centred in y, so the arm's full
  sweep circle stays inside the bay and the deck footprint (keeps clear of the
  cluster and the wheels) and leaves the -x part of the bay free for later
  modules.
- Evidence: `direction_control: {motion: <steer id>}`.
- Generator calls it after `add_ground_contacts` and hashes its config.

## Planned files

- `src/formula_ultimate/hierarchy/direction_control.py` (new)
- `scripts/hierarchy/generate_functional_vehicle.py`
- `tests/test_hierarchy_direction_control.py` (new)
- Work log plan/result (EN + TH), `auto-loop/progress.md` (+ `.th.md`)

## Validation

- `python -m unittest tests.test_hierarchy_direction_control tests.test_hierarchy_ground_contacts tests.test_hierarchy_mechanisms -v`
- Generate seed 11 (and 23, 37) into `artifacts/work162/`; run the acceptance
  classes with the nine-key check relaxed locally (gitignored script) for
  A0 interfaces, A2 motions, B4, B5, B6; run the Level-0 evaluator on seed 11.
- `pwsh -NoProfile -File auto-loop/verify.ps1`: Gates 1 and 2 must pass; no
  previously passing Gate 3 test may regress.

## Success criteria

Focused tests pass, the local B5 and A2 checks pass on 11/23/37, Gates 1-2
pass, Tier A, B10 and C1 stay green.

## Risks

- Bay space is shared with later modules; this item reserves only the +x end.
- The arm floats `c` above the boss (thrust clearance); nothing models axial
  retention.

## Non-goals

No linkage from the steering arm to the wheels, no steering geometry, no
vehicle dynamics. Not physical validation.
