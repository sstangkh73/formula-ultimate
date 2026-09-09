# Work 110: Actual geometry-to-mesh bridge

Thai companion: `work110-geometry_mesh_bridge.th.md`

Status: Planned

Original Work 106 package: 109

Dependencies: Work 108, Work 109

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Generate solver-ready volume/surface meshes from candidate geometry while preserving cavities, materials and semantic boundaries.

Use Work 108 solids and Work 109 surfaces. Existing B-rep meshing can start before the new representation adapter finishes.

## 2. Proposed files

- `src/formula_ultimate/structural/geometry_mesh_bridge.py`
- `config/development/geometry_mesh_bridge_v1.json`
- `scripts/development/run_geometry_mesh_bridge.py`
- `tests/test_geometry_mesh_bridge.py`

## 3. Implementation sequence

1. Benchmark candidate mesh adapters on the frozen corpus; record versions and failures before selection.
2. Map material regions and load/contact surfaces to persistent semantic mesh sets.
3. Generate at least 3 spatial refinement levels and inspect Jacobians, cavities and interfaces.
4. Reconcile mesh/CAD mass and boundary geometry; retain deterministic manifests and diagnostics.

## 4. Experiment

- IV: Geometry family, representation, mesh density and curvature/feature refinement.
- DV: Element quality, geometric error, material coverage, mass discrepancy and meshing cost.
- Controls: Same source geometry/material hash and boundary meanings at every refinement.

## 5. Tests and falsification

Inject inverted elements, missing boundary sets, filled cavities, wrong units and stale mesh references. Never substitute a box mesh for a failed candidate mesh.

## 6. Registration and acceptance

Freeze 3-level refinement schedule, quality criteria, coverage requirements and geometry/mass tolerances.

Every admitted positive case preserves required regions and boundaries within frozen tolerances. Unsupported cases remain unresolved, not physically failed.

## 7. Deliverables and handoff

Actual meshes, semantic maps, quality/error tables, build metadata and repeatability report.

Feeds vector mechanics Work 111 and thermal/flow Work 115/121.

## 8. Risks and non-goals

Thin features may disappear while global volume looks correct. Inspect local geometry too. No solver accuracy or stress-convergence claim yet.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_geometry_mesh_bridge tests.test_repository_contract -v
python scripts/development/run_geometry_mesh_bridge.py --config config/development/geometry_mesh_bridge_v1.json --output-root artifacts/work110/run_a
python scripts/development/run_geometry_mesh_bridge.py --config config/development/geometry_mesh_bridge_v1.json --output-root artifacts/work110/run_b --replay-reference artifacts/work110/run_a/result.json
```
