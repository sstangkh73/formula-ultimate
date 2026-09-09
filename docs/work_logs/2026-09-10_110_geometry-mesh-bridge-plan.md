# Work 110 Plan: Actual Geometry-to-Mesh Bridge

Thai companion: `2026-09-10_110_geometry-mesh-bridge-plan.th.md`

Date: 2026-09-10 (Asia/Bangkok)

Status: Completed

## Objective and scope

Implement solver-readable tetrahedral volume meshes and triangular surface/semantic sets from both admitted upstream representations: Work 109 labelled cells and an exact Work 108 hollow B-rep. Preserve cavities, material labels, source identities and observable approximation/quality errors across three registered levels.

The field adapter tetrahedralizes every occupied Cartesian cell without geometry substitution. The B-rep adapter samples the actual curved hollow solid at registered resolutions, marks unresolved boundary cells as approximation, and tetrahedralizes only admitted occupied cells. Both emit deterministic Gmsh 2.2 ASCII plus manifests.

## Experiment and planned files

- IV: source representation/family and resolution.
- DV: nodes/elements, signed Jacobian, aspect proxy, volume/mass discrepancy, material coverage, boundary-set coverage, cavity/topology preservation and deterministic cost.
- Controls: identical upstream SHA-256/material semantics and named boundary meanings at each level.
- Failures: inverted/zero elements, missing sets, filled cavity, wrong units, stale source identity, label loss, over-budget mesh or substituted geometry.

Planned files:

- `src/formula_ultimate/structural/geometry_mesh_bridge.py`
- `config/development/geometry_mesh_bridge_v1.json`
- `scripts/development/run_geometry_mesh_bridge.py`
- `tests/test_geometry_mesh_bridge.py`
- `docs/contracts/GEOMETRY_MESH_BRIDGE_V1.md` and Thai companion
- this plan/result and Thai companions
- ignored meshes/evidence under `artifacts/work110/`

## Validation and success

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_geometry_mesh_bridge tests.test_repository_contract -v
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_geometry_mesh_bridge.py --config config\development\geometry_mesh_bridge_v1.json --output-root artifacts\work110\run_a
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_geometry_mesh_bridge.py --config config\development\geometry_mesh_bridge_v1.json --output-root artifacts\work110\run_b --replay-reference artifacts\work110\run_a\result.json
python -m compileall -q src scripts tests
```

All three levels on both routes must contain only positive-volume tetrahedra, complete materials and required semantic surface sets; field mesh volume must be exact, B-rep volume/mass errors must remain within frozen approximation limits, the hollow centreline must remain void, negative controls must reject, and replay must be exact. Then run affected regressions, diff/staged checks and one immediate scoped commit.

## Risks and non-goals

Voxel sampling can lose thin/curved features and is not an unstructured conforming B-rep mesher. Record this bias and any unresolved conversion; never replace a failed candidate with a box. Non-goals: solver accuracy, stress convergence, constitutive physics, universal meshing, manufacturing, whole-vehicle or physical validation, installation, push or history rewrite.
