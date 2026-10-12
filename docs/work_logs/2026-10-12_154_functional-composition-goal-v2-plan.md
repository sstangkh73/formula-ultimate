# Work 154 Plan: Functional Composition Goal v2 for the Auto-Loop

Thai companion: `2026-10-12_154_functional-composition-goal-v2-plan.th.md`

Date: 2026-10-12

Status: Completed

## Objective

Goal v1 (Works 149–153) passed, but its parts were straight extrusions of
star-shaped profiles, and its capability labels did not change any geometry.
Goal v2 makes function drive geometry and motion, and couples the vehicle to
the Level-0 race kernel. It is sized for one unattended run of about 8 hours.

## Sizing (from the v1 run)

The v1 run took 5 iterations in about 2 h 07 min. Each iteration took 15–30
min, about half of it verification. Gate 2 now takes about 9 min and Gate 3
about 1.5 min, and every iteration runs `verify.ps1` at least twice. So the
estimate is about 30 min per iteration, or about 16 iterations in 8 h. The v2
contract is estimated at 15–20 work items. It is split into three tiers, so
partial progress stays usable and shows plainly in `last-verify.txt`:

- Tier A, about 5–6 items: richer geometry language (through-holes, voids,
  non-prismatic solids), declared motions with collision-free sweeps, and the
  inertia tensor.
- Tier B, about 8–10 items: evidence for each function (vessel volume,
  chamber with a moving member, transmission chain, ground propulsion,
  steering, brake, structural backbone, heat rejection, controller housing),
  through-hole threaded joints, and static ground stability.
- Tier C, about 2–3 items: the Level-0 evaluator on the existing race kernel,
  with a mass-sensitivity falsification check.

Expected outcome in 8 h: Tier A almost certainly, most of Tier B, and Tier C
possibly. Full completion is roughly a coin flip.

## Scope

- Add `auto-loop/acceptance/test_functional_composition.py`, the v2
  acceptance suite. It runs the v1 checks on the v2 package through
  subclassing, plus the A/B/C checks. It reuses the v1 mesh helpers.
- Keep the v1 acceptance suite unchanged as a regression gate for the v1
  generator.
- Rewrite `auto-loop/GOAL.md` and `GOAL.th.md` for v2. Append a v2 starting
  section to `progress.md` and `progress.th.md`. Set the runner's default
  branch to `loop/functional-composition-v2`, its default budget to 8 h and
  20 iterations, and its turn budget to 150. Update the README files to match.
- Self-check the v2 suite with a synthetic fixture generator and evaluator in
  the scratchpad. Neither is committed.

## Planned files

- `auto-loop/acceptance/test_functional_composition.py` (new)
- `auto-loop/GOAL.md`, `auto-loop/GOAL.th.md`
- `auto-loop/progress.md`, `auto-loop/progress.th.md`
- `auto-loop/run-loop.ps1`, `auto-loop/README.md`, `auto-loop/README.th.md`
- this plan, its Thai companion, and the Work 154 result records

## Validation

1. Run the v2 suite against a valid synthetic fixture. Every test must pass.
2. Run broken variants. Each must fail its intended test: no void, piston
   blocked, heat fins removed, threaded joint without a hole, unstable
   support, wrong inertia, an evaluator that ignores mass, and a missing motion
   bearing.
3. Run `verify.ps1` on the real repository. The expected result is that Gates
   1 and 2 pass, the v1 acceptance passes, and the v2 acceptance fails because
   the v2 generator is missing.
4. Run the PowerShell parse check, then make one commit with explicit staging.

## Success criteria

- The v2 suite can be satisfied (the valid fixture passes) and is
  discriminating (every broken variant fails its intended test).
- The goal records the estimate, the tiers and the limitations honestly.

## Risks

- The contract prescribes function evidence, such as a cavity for storage
  and a revolute member touching the ground. That is a bias toward
  recognisable mechanisms, and it is recorded as a design-language boundary.
- Mesh checks are sampled. Thread helices are not checked; only through-holes
  are.
- The 8 h estimate rests on one 5-iteration sample.

## Explicit non-goals

- Do not implement the v2 generator or the evaluator.
- Do not run the loop.
- Do not merge into `main`. That merge was refused by the session's
  permission policy and is left to the owner.
- Do not touch `/private/`.
