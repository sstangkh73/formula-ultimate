# Work 153 Plan: Hierarchical Vehicle Generator CLI

Thai companion: `2026-10-12_153_hierarchical-generator-cli-plan.th.md`

Date: 2026-10-12

Status: Completed

## Objective

Milestone 5 of `auto-loop/GOAL.md`: the entry point
`scripts/hierarchy/generate_hierarchical_vehicle.py --seed S --out DIR`
(CadQuery runtime) that chains Work 150 `decompose`, Work 152 `layout` and
Work 151 `realize_leaf`, and writes `DIR/manifest.json` plus one metre STL per
leaf with the exact contract fields, measured masses and an exact roll-up.

## Scope

- `src/formula_ultimate/hierarchy/decomposition.py`: add an optional
  `start_attempt` argument to `decompose` (default 0, existing behaviour
  unchanged) so a declared fallback can move to the next decomposition
  attempt.
- New pure-Python module `src/formula_ultimate/hierarchy/composition.py`:
  - `plan_vehicle(seed)`: decompose, then layout; on `LayoutFailure` move to
    the next decomposition attempt (`start_attempt = tree.attempt + 1`),
    bounded by `max_plan_attempts`. Every failure is recorded in the plan.
    Runs `layout_problems` and raises if any remain.
  - `composition_config_sha256(...)`: hash of the decomposition config and
    version, layout config and version, leaf grammar version, material
    records, contact tolerance, design language version.
  - `build_manifest(plan, measurements, materials, git_commit)`: builds the
    Work 149 `PartTree` (assembly functions from the abstract tree, parts from
    measured mass and centre of mass, interfaces `id, a, b, kind` from the
    layout) and serializes the exact contract fields with
    `to_manifest_nodes` / `to_manifest_interfaces`.
  - Material choice: a seed-driven draw per leaf from a declared catalogue
    file. v1 uses the existing synthetic record
    `synthetic_aluminium_like_verification_v1` in
    `config/materials/engineering_material_manufacturing_v1.json`
    (`evidence_status=synthetic`, `design_use_allowed=false`), read at run
    time. No new material values are written into tracked files.
- New CLI `scripts/hierarchy/generate_hierarchical_vehicle.py`: parse
  arguments, `git rev-parse HEAD`, plan, realize every leaf to
  `DIR/meshes/<leaf id>.stl`, write deterministic `manifest.json`
  (`sort_keys`, `allow_nan=False`).
- New tests `tests/test_hierarchy_composition.py` (pure parts plus one CAD
  subprocess run of the CLI).

## Planned files

- `src/formula_ultimate/hierarchy/decomposition.py` (edit)
- `src/formula_ultimate/hierarchy/composition.py` (new)
- `scripts/hierarchy/generate_hierarchical_vehicle.py` (new)
- `tests/test_hierarchy_composition.py` (new)
- this plan and result pair (English and Thai)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## Validation

1. `python -m unittest tests.test_hierarchy_composition tests.test_hierarchy_decomposition -v`
2. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gates 1 and 2 must pass.
   Gate 3 is run in full and its result is recorded; it may still fail.

## Success criteria

- The CLI exits 0 for seeds 11, 23 and 37, writes the contract fields and a
  byte-identical replay.
- Leaf masses come only from the re-read exported mesh times density.
- Gate 3 result recorded test by test.

## Risks

- A layout failure for some seed (seed 4 in Work 152) is handled by the
  declared fallback; if all plan attempts fail the CLI exits non-zero.
- `interference` joints carry no `interference_m` because the layout makes
  flush contact; the kind label is a representation label only.
- One synthetic material means masses are not design masses.

## Non-goals

- No physical validation, no sourced materials, no change to the acceptance
  suite, no special-casing of seeds 11, 23 or 37.
