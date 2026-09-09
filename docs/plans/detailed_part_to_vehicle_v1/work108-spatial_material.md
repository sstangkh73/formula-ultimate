# Work 108: Spatial material and void source of truth

Thai companion: `work108-spatial_material.th.md`

Status: Planned

Original Work 106 package: 107

Dependencies: Existing CAD evidence

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Create actual geometry whose material ownership, cavities, mass, center of mass and inertia remain consistent through export and placement.

Inputs: Work 092 B-rep corpus, CAD inspection adapters and Work 106 spatial contract proposal; recheck installed CAD runtimes.

## 2. Proposed files

- `src/formula_ultimate/components/spatial_material.py`
- `config/development/spatial_material_v1.json`
- `scripts/development/run_spatial_material.py`
- `tests/test_spatial_material.py`

## 3. Implementation sequence

1. Define SI frames, material/void regions, ownership and immutable revision references.
2. Adapt existing curved, branched, hollow and multi-body CAD cases; reject undeclared overlaps.
3. Compute mass properties from occupied geometry and reconcile independent CAD measurements.
4. Mutate cavities/materials and transform placements; invalidate dependent evidence and replay exports.

## 4. Experiment

- IV: Cavity geometry, region material and rigid placement.
- DV: Volume, mass, center-of-mass and inertia discrepancies.
- Controls: Identical geometry revision and known homogeneous reference cases.

## 5. Tests and falsification

Check cavity loss, duplicated ownership, overlapping materials, non-finite coordinates, stale hashes and frame/unit invariance. A removed cavity must not retain the old mass.

## 6. Registration and acceptance

Freeze feature scale and length/volume/mass/inertia tolerances after a disclosed CAD pilot, before admitted cases.

All positive invariants and intended negative rejections must pass. Actual CAD-dependent tests must run; skipped CAD tests block adapter completion.

## 7. Deliverables and handoff

Exported solids, region manifest, mass-property comparison, mutation report and replay identities.

Feeds Works 109, 110 and 112 with a trustworthy spatial contract.

## 8. Risks and non-goals

Blended junctions can double-count matter. Resolve ownership explicitly; no hidden fusion. No structural or whole-vehicle feasibility claim.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_spatial_material tests.test_repository_contract -v
python scripts/development/run_spatial_material.py --config config/development/spatial_material_v1.json --output-root artifacts/work108/run_a
python scripts/development/run_spatial_material.py --config config/development/spatial_material_v1.json --output-root artifacts/work108/run_b --replay-reference artifacts/work108/run_a/result.json
```
