# Work 156 Result: v2 Flush-Contact Joint Kinds Without an Axis-Less `threaded`

Thai companion: `2026-10-12_156_v2-flush-joint-kinds-result.th.md`

Plan: `2026-10-12_156_v2-flush-joint-kinds-plan.md`

Date: 2026-10-12

Status: Completed

## Files changed

- `src/formula_ultimate/hierarchy/functional.py`: `FLUSH_JOINT_KINDS` (v1
  `JOINT_KINDS` without `threaded`) and `V2_DECOMPOSITION_CONFIG`
  (`DEFAULT_CONFIG` with only `joint_kinds` replaced).
- `scripts/hierarchy/generate_functional_vehicle.py`: plans with
  `V2_DECOMPOSITION_CONFIG` and hashes it into `config_sha256`.
- `tests/test_hierarchy_functional_joints.py` (new, 4 tests).
- this result pair, the plan pair, `auto-loop/progress.md` and
  `auto-loop/progress.th.md`.

## Decisions

- A flat cap or side-face contact has no hole and no axis, so labelling it
  `threaded` cannot satisfy the v2 contract. Instead of relabelling after the
  draw, the v2 generator draws flush-contact kinds from the axis-free v1
  kinds (`welded`, `bonded`, `interference`, `integral`). `threaded` is
  reserved for hole-and-pin fastener joints that a later item realizes with
  geometry and an axis.
- The v1 generator, its default config and all v1 tests are unchanged.
- The changed choice list changes the random draw sequence, so v2 trees
  differ from v1 trees for the same seed. This is acceptable: v2 is a separate
  generator with its own `config_sha256`.

## Validation

1. `python -m unittest tests.test_hierarchy_functional_joints tests.test_hierarchy_functional -v`
   -> `Ran 10 tests in 24.035s`, `OK` (exit 0).
2. `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed 11 --out artifacts/work156/seed11`
   -> `seed 11: 226 leaves, 225 interfaces, 0 motions` (exit 0).
3. `pwsh -NoProfile -File auto-loop/verify.ps1`:
   - Gate 1: `material publication boundary: PASS`.
   - Gate 2: `Ran 1104 tests in 503.882s`, `OK (skipped=11)`.
   - Gate 3: `Ran 41 tests`, `FAILED (failures=12)`. The v1 suite passes
     13/13. In v2, all of Tier A0 now passes (including both
     `TierA0Interfaces` tests, which failed before), plus Tier A2 (still
     vacuous, no motions) and Tier A3. Still failing: Tier A1 (0 holed
     leaves), Tier B1–B10 (no evidence; B10 now fails on the count 0 < 8
     instead of a `KeyError`) and Tier C1 (no evaluator).

## Limitations

- No threaded joints exist in the v2 package now; `TierB10ThreadedJoints`
  needs real hole-and-pin fasteners (at least 8 per seed).
- Tier A2 passing is vacuous until motions exist.

## Follow-up

- Tier A1 geometry language: non-prismatic leaves (>= 25 %) and leaves with a
  through-hole (>= 5 %), then threaded fasteners through those holes.
