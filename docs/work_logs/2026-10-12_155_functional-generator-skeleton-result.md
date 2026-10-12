# Work 155 Result: Functional (v2) Generator Skeleton with Measured Inertia

Thai companion: `2026-10-12_155_functional-generator-skeleton-result.th.md`

Date: 2026-10-12

Plan: `2026-10-12_155_functional-generator-skeleton-plan.md`

Status: Completed

## Files changed

- `src/formula_ultimate/hierarchy/functional.py` (new): `mesh_inertia`
  (mass, centre of mass and inertia tensor about the centre of mass from
  closed triangle meshes, signed-tetrahedron integrals), `config_sha256_v2`,
  `build_functional_manifest`, `DESIGN_LANGUAGE_VERSION_V2 = "func-composition-v2"`.
- `scripts/hierarchy/generate_functional_vehicle.py` (new): v2 entry point.
  Uses the v1 `plan_vehicle` and `realize_leaf` unchanged, re-reads every
  exported STL and writes the v2 fields.
- `tests/test_hierarchy_functional.py` (new, 6 tests).
- `auto-loop/progress.md`, `auto-loop/progress.th.md`.

## Decisions

- Skeleton only: `motions = []` and `function_evidence = {}`. No motion or
  capability evidence is claimed; Tier B fails by design until later items.
- The inertia is computed in float64 from the re-read float32 STL triangles,
  the same data the acceptance suite reads.
- The v1 modules are not edited; the v2 generator wraps the v1 manifest.

## Validation

1. `python -m unittest tests.test_hierarchy_functional -v`: exit 0,
   `Ran 6 tests`, `OK`.
2. `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed 11 --out artifacts/work155/seed11`:
   exit 0, `seed 11: 226 leaves, 225 interfaces, 0 motions`.
3. `pwsh -NoProfile -File auto-loop/verify.ps1`:
   - Gate 1 PASS.
   - Gate 2 `Ran 1100 tests in 452.108s`, `OK (skipped=11)`.
   - Gate 3 `Ran 41 tests`, `FAILED (failures=13, errors=1)`. All 13 v1
     tests pass. v2 passing: TierA0 Replay (2), Hierarchy (2), Capabilities,
     GeometryAndMass (2), FreeForm (2), NoFixedTemplate (2), TierA2 (2, only
     vacuously: no motions), TierA3 inertia.
   - v2 failing: TierA0Interfaces (2): the v1 layout emits `threaded`
     interfaces (49 in seed 11) without `axis_point_m`/`axis_dir`; TierA1
     (non-prismatic and through-hole shares); TierB1..B9 (no evidence);
     TierB10 error (threaded joints without an axis); TierC1 (no evaluator).

## Limitations

- Tier A2 passing is not meaningful while `motions` is empty.
- Geometry is still the v1 straight-extrusion language.

## Follow-up

- Next: threaded joints with a real hole and pin (fixes TierA0Interfaces and
  TierB10) or re-label v1 threaded contacts that cannot carry an axis, and
  add non-prismatic and holed leaves (TierA1).
