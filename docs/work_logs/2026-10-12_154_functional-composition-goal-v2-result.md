# Work 154 Result: Functional Composition Goal v2 for the Auto-Loop

Thai companion: `2026-10-12_154_functional-composition-goal-v2-result.th.md`

Date: 2026-10-12

Plan: `2026-10-12_154_functional-composition-goal-v2-plan.md`

Status: Completed

## Outcome

Goal v2 is prepared and sized for an 8-hour unattended run. The v2 acceptance
suite (28 tests in tiers A, B and C) can be satisfied, as a synthetic package
passes all of it. It is also discriminating: every one of 8 deliberate defects
fails its intended test. On the real repository, verify gives exactly the
loop's intended starting state. The loop was not run, and goal v1's branch was
not merged into `main`, because the session's permission policy refused that
merge.

## Files changed

- `auto-loop/acceptance/test_functional_composition.py` (new). It re-applies
  the v1 checks to the v2 package by subclassing them (`TierA0*`), and adds
  the geometry language (`TierA1`), motions with bearings and collision sweeps
  (`TierA2`), inertia (`TierA3`), nine function-evidence checks plus
  threaded through-holes and ground stability (`TierB1`–`TierB10`), and the
  Level-0 evaluator with a mass-sensitivity falsification check (`TierC1`).
- `auto-loop/GOAL.md`, `GOAL.th.md`: the goal v2 contract, the time box, the
  tiers and the limitations.
- `auto-loop/verify.ps1`: clears all three fixture hooks, and Gate 3 runs
  both suites.
- `auto-loop/run-loop.ps1`: defaults are now branch
  `loop/functional-composition-v2`, 150 turns per iteration, 20 iterations
  and 8 hours.
- `auto-loop/README.md`, `README.th.md`: the branch name.
- `auto-loop/progress.md`, `progress.th.md`: the v2 starting state and the
  lessons from v1.

## Sizing evidence

- v1 run: 5 iterations from about 22:30 to 00:37. The `iter-*.log` timestamps
  were 22:56, 23:11, 23:30, 00:00 and 00:27.
- One verify now takes about 10.3 min (Gate 2 `533.585s`, Gate 3 `82.014s`),
  and runs at least twice per iteration. So the estimate is about 30 min per
  iteration, or about 16 in 8 h, against 15–20 estimated work items.

## Validation

1. The v2 suite was run with a valid synthetic fixture (`fixture_v2.py`)
   and a toy evaluator, both in the scratchpad and not committed.
   `python -m unittest discover -s auto-loop/acceptance -p "test_functional*.py"`
   gave `Ran 28 tests`, `OK`. The first run exposed two issues, both fixed:
   - The fixture's cross members were disconnected. That was a fixture bug.
   - The test's "surrounds the axis" check sampled vertices only, so it
     rejected a valid square nut. It now casts 8 radial rays from the axis,
     which also fits the intent better.
2. Defect matrix. Each variant fails exactly its intended test:

   | Variant | Failing test |
   |---|---|
   | no_void | `test_vessel_holds_declared_volume` |
   | piston_blocked | `test_motions_sweep_without_collision` |
   | no_fins | `test_surfaces_are_extended` |
   | threaded_no_hole | `test_threaded_joints_pass_through_a_hole` |
   | unstable | `test_rotating_ground_contacts_carry_the_vehicle_stably` |
   | wrong_inertia | `test_vehicle_inertia_matches_meshes` |
   | no_bearing | `test_every_motion_has_a_bearing_or_guide` |
   | evaluator ignores mass | `test_level0_race_uses_the_generated_vehicle` |

3. Analytic checks of the measurement functions:
   - Box 2 x 1 x 0.5 m with density 3: mass `3.0`, centre of mass
     `[1, 0.5, 0.25]`, inertia diagonal `[0.3125, 1.0625, 1.25]`, exactly the
     analytic values, with off-diagonal terms `0.0`.
   - Square ring: genus `1`, closed, volume `3.0` (expected 3).
   - Hollow box: void `1.0` (expected 1).
   - The frustum is classified non-prismatic. The box and the 64-gon disc are
     classified prismatic.
4. `pwsh -NoProfile -File auto-loop/verify.ps1` was run with all three hooks
   set to a bogus command. It exited 3. Gate 1 passed. Gate 2:
   `Ran 1094 tests in 533.585s`, `OK (skipped=11)`. Gate 3: `Ran 41 tests`,
   `FAILED (failures=28)`. The 13 v1 tests passed, and all 28 v2 failures
   were `missing: ...generate_functional_vehicle.py`, which proves the hooks
   were cleared.
5. The PowerShell parser reported 0 errors in `run-loop.ps1` and
   `verify.ps1`.
6. Commit gates: `python -m unittest tests.test_repository_contract`,
   `git diff --cached --check`, explicit staging.

## Limitations

- The contract's function evidence is a design-language bias toward
  recognisable mechanisms (cavity storage, rotating ground contacts).
- Threads are checked as through-holes only, and the drag area is bounded,
  not derived. Mesh checks are sampled.
- The 8 h estimate rests on one 5-iteration run.
- `main` still points at `56412d6`. Works 149–154 are on
  `loop/hierarchical-composition` until the owner fast-forwards `main`.

## Follow-up work

- Fast-forward `main` to `loop/hierarchical-composition`, then start the v2
  loop from `main`.
- After the run, audit for gaming and for depth, as was done after v1.
