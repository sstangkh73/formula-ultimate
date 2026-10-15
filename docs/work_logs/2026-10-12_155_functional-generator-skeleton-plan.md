# Work 155 Plan: Functional (v2) Generator Skeleton with Measured Inertia

Thai companion: `2026-10-12_155_functional-generator-skeleton-plan.th.md`

Date: 2026-10-12

Status: Completed

## Objective

First step of goal v2 (`auto-loop/GOAL.md`, Tier A): add the v2 entry point
`scripts/hierarchy/generate_functional_vehicle.py --seed S --out DIR`
(CadQuery runtime) that reuses the v1 plan and realization unchanged and
writes the v2 top-level fields: `up_axis = "z"`, `motions`,
`function_evidence` and `vehicle_inertia_kg_m2` (3x3 about the vehicle centre
of mass, computed from the re-read exported meshes).

## Scope

- New pure-Python module `src/formula_ultimate/hierarchy/functional.py`:
  - `DESIGN_LANGUAGE_VERSION_V2 = "func-composition-v2"`.
  - `mesh_inertia(meshes_and_density)`: mass, centre of mass and inertia
    tensor about the centre of mass of a set of closed triangle meshes with
    uniform density each (divergence-theorem tetrahedron integrals, SI units).
  - `build_functional_manifest(v1_manifest, motions, function_evidence,
    inertia)`: the v1 manifest plus the four v2 fields and the v2 design
    language version.
- New CLI `scripts/hierarchy/generate_functional_vehicle.py`: plan with the v1
  `plan_vehicle`, realize leaves, re-read every STL, compute the inertia,
  write the manifest. In this skeleton `motions` is `[]` and
  `function_evidence` is `{}`: no motion or capability evidence is claimed
  yet. Later work items add them.
- `config_sha256` covers the v1 composition config plus the v2 design
  language version.
- New tests `tests/test_hierarchy_functional.py`: inertia of analytic boxes
  (with an offset and a rotation) against closed-form values, the parallel
  axis theorem for two separated bodies, and the manifest field set.

## Planned files

- `src/formula_ultimate/hierarchy/functional.py` (new)
- `scripts/hierarchy/generate_functional_vehicle.py` (new)
- `tests/test_hierarchy_functional.py` (new)
- this plan and result pair (English and Thai)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## Validation

1. `python -m unittest tests.test_hierarchy_functional -v`
2. One generator run for seed 11 under the CAD runtime into `artifacts/work155/`.
3. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gates 1 and 2 must pass.
   Gate 3 is recorded tier by tier; it is expected to still fail in Tier A1
   and Tier B/C.

## Success criteria

- Tier A0 (v1 contract on the v2 package) and Tier A3 (inertia) pass.
- Tier A2 passes only vacuously (no motions yet); this is recorded as not
  yet meaningful.
- The v1 suite and all existing tests still pass.

## Risks

- Inertia tolerance is 1e-5 relative to the largest entry; computing from the
  re-read float32 meshes in float64 should match the acceptance formula.
- Empty `motions` / `function_evidence` must not be presented as function
  evidence; they are placeholders that fail Tier B by design.

## Non-goals

- No functional geometry, no motions, no Level-0 evaluator in this item.
- No edit of v1 modules, no special-casing of seeds 11, 23 or 37.
