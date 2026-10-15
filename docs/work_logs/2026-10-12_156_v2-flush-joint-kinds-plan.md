# Work 156 Plan: v2 Flush-Contact Joint Kinds Without an Axis-Less `threaded`

Thai companion: `2026-10-12_156_v2-flush-joint-kinds-plan.th.md`

Date: 2026-10-12

Status: Completed

## Objective

Goal v2 requires every `threaded` interface to carry `axis_point_m` and a unit
`axis_dir` whose axis passes through a hole of one part and the material of
the other. The v1 layout joins leaves by flat cap or side-face contact, which
has no hole and no axis, yet the v1 decomposition draws `threaded` for about
a fifth of those joints (49 in seed 11). This fails `TierA0Interfaces` for the
v2 package. Make the v2 generator draw flush-contact joint kinds from the v1
kinds minus `threaded`, so that `threaded` is reserved for real hole-and-pin
fastener joints that a later work item realizes with geometry.

## Scope

- `src/formula_ultimate/hierarchy/functional.py`: add
  `FLUSH_JOINT_KINDS` (v1 `JOINT_KINDS` without `threaded`) and
  `V2_DECOMPOSITION_CONFIG = replace(DEFAULT_CONFIG, joint_kinds=FLUSH_JOINT_KINDS)`.
- `scripts/hierarchy/generate_functional_vehicle.py`: plan with
  `V2_DECOMPOSITION_CONFIG`, and hash it in `config_sha256`.
- New tests in a new file `tests/test_hierarchy_functional_joints.py`: the
  v2 config has no `threaded`, keeps the other v1 kinds, the v2 plan for
  several seeds lays out with no `threaded` interface, and the v1 default is
  unchanged.

## Planned files

- `src/formula_ultimate/hierarchy/functional.py`
- `scripts/hierarchy/generate_functional_vehicle.py`
- `tests/test_hierarchy_functional_joints.py` (new)
- this plan and result pair (English and Thai)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## Validation

1. `python -m unittest tests.test_hierarchy_functional_joints tests.test_hierarchy_functional -v`
2. Generator run for seed 11 under the CAD runtime into `artifacts/work156/`.
3. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gates 1 and 2 must pass;
   Gate 3 recorded per tier.

## Success criteria

- `TierA0Interfaces` passes for the v2 package; every other Tier A0 test and
  Tier A3 still pass; the v1 suite still passes.
- No v1 module or existing test changes.

## Risks

- Changing the joint-kind choice list changes the random draw sequence, so v2
  trees differ from v1 trees for the same seed. That is acceptable (v2 is a
  separate generator), but layout could fail more often; the declared v1
  fallback (next decomposition attempt) still applies.
- `TierB10ThreadedJoints` keeps failing (now on the count of 0 < 8 instead of
  a `KeyError`) until fastener joints exist.

## Non-goals

- No hole or pin geometry, no motions, no function evidence in this item.
- No special-casing of seeds 11, 23 or 37.
