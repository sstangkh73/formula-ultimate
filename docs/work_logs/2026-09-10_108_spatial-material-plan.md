# Work 108 Plan: Spatial Material and Void Source of Truth

Thai companion: `2026-09-10_108_spatial-material-plan.th.md`

Date: 2026-09-10 (Asia/Bangkok)

Status: Completed

## Objective

Implement the first package in `docs/plans/detailed_part_to_vehicle_v1`: a bounded, replayable spatial contract in which occupied B-rep regions, declared voids, material ownership, rigid placement, volume, mass, centre of mass and inertia share immutable geometry and material identities.

## Scope and inputs

The admitted scope uses the verified Work 092 free-form B-rep grammar and exact upstream configuration identities. It covers curved, hollow and multi-body CAD cases, one homogeneous analytic reference, explicit single ownership of every occupied solid, explicit cavity evidence where the source feature DAG contains a subtraction, and rigid placement in SI units. CadQuery performs generation and first measurement; FreeCAD independently imports the exact STEP exports and measures them without healing.

The experiment freezes:

- independent variables: cavity-bearing source revision, region density and rigid placement;
- dependent variables: occupied volume, mass, centre-of-mass and inertia discrepancies;
- controls: a known homogeneous reference and unchanged upstream geometry revision;
- failure criteria: undeclared overlap, duplicate ownership, non-finite coordinates, stale hashes, invalid CAD, unit/frame inconsistency, mass retained after cavity removal, or any tolerance breach.

## Planned files

- `src/formula_ultimate/components/spatial_material.py`
- `src/formula_ultimate/components/__init__.py` if a public export is needed
- `config/development/spatial_material_v1.json`
- `scripts/development/run_spatial_material.py`
- `scripts/cad/inspect_spatial_material_freecad.py`
- `tests/test_spatial_material.py`
- `docs/contracts/SPATIAL_MATERIAL_VOID_V1.md` and Thai companion
- this plan and Thai companion
- matching result log and Thai companion
- ignored generated evidence under `artifacts/work108/`

Path additions relative to the proposed card are limited to the independent FreeCAD inspector and mandatory bilingual contract/evidence logs.

## Implementation approach

1. Validate an exact-schema declaration with finite SI coordinates, positive densities, unique region ownership, disjoint ownership declarations, source SHA-256 identities and bounded placement transforms.
2. Regenerate the selected Work 092 solids from the frozen upstream configurations; retain source and placed STEP files plus canonical manifests.
3. Derive volume, centre and unit-density inertia from actual occupied B-rep solids. Apply density, rigid rotation, translation and the parallel-axis theorem to obtain system mass properties.
4. Represent cavity evidence using the actual subtractive feature ancestry and verify that occupied volume equals outer volume minus declared cavity volume for the admitted hollow case.
5. Independently import exact STEP artifacts in FreeCAD, measure each solid, reconstruct material-weighted mass properties and compare within frozen tolerances.
6. Exercise material, cavity/source and placement mutations. Require changed dependent evidence identities and reject replay against stale evidence.
7. Produce deterministic `result.json`, artifact manifest, mutation report and exact replay result. Preserve all negative outcomes and limitations.

## Validation

The resolved CadQuery and FreeCAD Python executables must be recorded in the result log. Planned gates are:

```powershell
$env:PYTHONPATH='src'
& .\.tools\cadquery-mcp\Scripts\python.exe -m unittest tests.test_spatial_material tests.test_repository_contract -v
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_spatial_material.py --config config\development\spatial_material_v1.json --output-root artifacts\work108\run_a --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe'
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_spatial_material.py --config config\development\spatial_material_v1.json --output-root artifacts\work108\run_b --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe' --replay-reference artifacts\work108\run_a\result.json
python -m compileall -q src scripts tests
python -m unittest tests.test_spatial_material tests.test_repository_contract -v
```

Run affected or full regression tests if implementation risk warrants it. Before commit, run `git diff --check`, stage only Work 108 files, inspect `git diff --cached --name-only`, and run `git diff --cached --check`.

## Success criteria

- All positive invariants and intended negative controls pass without skipped CAD-dependent tests.
- At least curved, hollow and multi-body Work 092 geometries retain immutable source and export identities.
- The hollow case demonstrates geometry-derived cavity removal; no removed cavity retains old mass.
- CadQuery and FreeCAD independently agree on volume, mass, centre and inertia within registered tolerances.
- A rigid placement changes world-frame centre/inertia consistently while preserving volume and centroidal invariants.
- A clean replay is exact and stale source/material/placement evidence is rejected.
- The bilingual contract, tests, implementation, configuration and result evidence are committed as one scoped Work 108 commit.

## Risks and explicit non-goals

Risks include OCCT body ordering, inconsistent inertia tensor conventions, double counting at blended junctions, volatile CAD metadata and confusing a declared cavity with the occupied solid complement. Mitigations are geometric identities, per-solid ownership, canonical ordering, symmetric tensor checks, independent CAD measurement and fail-closed comparisons.

Non-goals: structural stress, thermal/flow behaviour, manufacturing feasibility, arbitrary material fields, whole-vehicle feasibility, physical validation, dependency installation, physical testing, pushing or rewriting Git history, or prescribing any conventional vehicle layout or component shape.
