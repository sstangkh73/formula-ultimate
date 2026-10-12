# Work 163 Plan: v2 power transmission (rolling roller chain)

Thai companion: `2026-10-13_163_v2-power-transmission-plan.th.md`

Status: Completed

## Objective

Add a power-transmission mechanism to the v2 mechanism layer so the package
carries real `power_transmission` evidence: a chain of >= 2 full-turn
revolute members, consecutive members joined by an interface, each member
with a `bearing` to a fixed part, sweeping without collision and attached to
the structural deck.

## Design

- New pure-Python module `src/formula_ultimate/hierarchy/power_transmission.py`
  with `add_power_transmission(layer, seed, catalogue, config)` (extends the
  layer from `add_direction_control`) and `power_transmission_problems(layer)`.
- One root-level assembly `m<k>-power_transmission` tagged
  `[power_transmission]` in the free -x part of the deck bay, from
  `bay_x0 + m` to the steering sweep circle minus `m` (m = 0.02 m).
- 2 or 3 stations laid along y through the free strip's centre line. Each
  station: boss (regular N_b-gon plate on the deck top, `bonded` to the deck),
  post (regular N_p-gon on the boss, `bonded`), roller (regular N_r-gon disc,
  N_r even, with a 96-gon bore of apothem `r_p + c`, c = 2.5e-5 m, floating
  `c` above the boss top, `bearing` to the post).
- Rolling contact: neighbouring roller centres are `R_i + R_j + c` apart
  (circumradii) and each roller has a vertex pointing at each neighbour, so
  the sampled vertex gap is `c` and since each full-turn sweep stays inside
  its circumcircle no rotation brings one roller into the other. Interface
  kind `rolling` between consecutive rollers.
- Motions `<assembly>.r<i>` = {roller i}, revolute about +z, range 2 pi.
- Evidence: `power_transmission: {chain: [motion ids in order]}`.
- Generator calls it after `add_direction_control` and hashes its config.

## Planned files

- `src/formula_ultimate/hierarchy/power_transmission.py` (new)
- `scripts/hierarchy/generate_functional_vehicle.py`
- `tests/test_hierarchy_power_transmission.py` (new)
- Work log plan/result (EN + TH), `auto-loop/progress.md` (+ `.th.md`)

## Validation

- `python -m unittest tests.test_hierarchy_power_transmission tests.test_hierarchy_direction_control -v`
- Generate seeds 11, 23, 37 into `artifacts/work163/`; run the acceptance
  classes with the nine-key check relaxed locally (gitignored script) for
  A0 interfaces, A2 motions, B3, B4, B5, B6; Level-0 evaluator on seed 11.
- `pwsh -NoProfile -File auto-loop/verify.ps1`: Gates 1 and 2 must pass; no
  previously passing Gate 3 test may regress.

## Success criteria

Focused tests pass, the local B3 and A2 checks pass on 11/23/37, Gates 1-2
pass, Tier A, B10 and C1 stay green.

## Risks

- The free strip can be as narrow as about 0.12 m; roller radii are clamped
  to fit, and planning raises if even the minimum does not fit.
- Rollers touch at one vertex pair only (line contact proxy); no torque or
  slip model.

## Non-goals

No link from the rollers to the wheels or a converter, no gear teeth, no
torque, efficiency or slip. Not physical validation.
