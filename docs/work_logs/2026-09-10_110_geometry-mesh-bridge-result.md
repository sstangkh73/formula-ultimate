# Work 110 Result: Actual Geometry-to-Mesh Bridge

Thai companion: `2026-09-10_110_geometry-mesh-bridge-result.th.md`

Date: 2026-09-10 (Asia/Bangkok)

Status: Completed

## Outcome and files

Work 110 generated six deterministic solver-readable Gmsh meshes: three levels from the Work 109 labelled field and three voxel approximations of the exact Work 108 hollow B-rep. All tetrahedra had positive Jacobians, material and required boundary sets were complete, the cavity centreline stayed void, controls failed closed and replay was exact.

Changed: `src/formula_ultimate/structural/geometry_mesh_bridge.py`, `config/development/geometry_mesh_bridge_v1.json`, `scripts/development/run_geometry_mesh_bridge.py`, `tests/test_geometry_mesh_bridge.py`, bilingual `docs/contracts/GEOMETRY_MESH_BRIDGE_V1*`, this bilingual plan/result, and ignored `artifacts/work110/run_a|run_b`.

## Decisions, failures and falsification

- A fixed six-tetra cell split gives deterministic positive orientation, material groups and Gmsh 2.2 output. It is not a conforming unstructured B-rep mesh.
- Semantic sets are `external_surface`, `load_surface`, `contact_surface` and, where labels meet, `material_interface`.
- The first runner wrongly replayed Work 109's mutation chain at every Work 110 resolution; at `0.02 m` an edit became a no-op and the run exited `1`. The corrected experiment meshes the same Work 109 source field at every level, without extending mutation validity beyond its registered `0.01 m`.
- The next run exposed the actual CadQuery `isInside(point, tolerance)` signature; removing an unsupported fourth argument corrected the adapter without changing geometry or thresholds.
- Controls rejected inverted elements, missing boundary sets, wrong units, filled cavity, stale reference and geometry substitution.

## Evidence

Result SHA-256: `46a4d7a0a7f168c0bbb879b186751397cf4127347cd27bd495979153eb82c0fd`. Artifact manifest: `e50a30b1338a350a8151ff5e95d7b9c65a007cf485f398c7aab49c6b0085bd2a`. `run_b/replay.json` is `exact: true`.

| Route / resolution (`m`) | Nodes | Tets | Triangles | Volume error | Min Jacobian (`m3`) |
|---|---:|---:|---:|---:|---:|
| field / `0.02` | `289` | `984` | `434` | `1.801494463428658e-14` | `7.999999999999988e-6` |
| field / `0.01` | `1865` | `8100` | `2008` | `1.1596947681993097e-13` | `9.999999999999944e-7` |
| field / `0.008` | `3220` | `14880` | `2936` | `1.6428340630214454e-13` | `5.11999999999996e-7` |
| hollow B-rep / `0.02` | `62` | `78` | `120` | `0.07909779256191748` | `7.999999999999991e-6` |
| hollow B-rep / `0.01` | `334` | `732` | `728` | `0.26586471819763147` | `9.99999999999998e-7` |
| hollow B-rep / `0.008` | `503` | `1062` | `1092` | `0.05969078506606261` | `5.119999999999991e-7` |

Maximum edge ratio was `1.7320508075688812`, below `1.8`. B-rep errors are non-monotonic and therefore contradict convergence; all are below the registered `0.35` approximation gate.

## Validation

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_geometry_mesh_bridge tests.test_repository_contract -v
# exit 0; 10 tests passed
python -m compileall -q src scripts tests
# exit 0
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_geometry_mesh_bridge.py --config config\development\geometry_mesh_bridge_v1.json --output-root artifacts\work110\run_a
# exit 0; six meshes; status passed
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_geometry_mesh_bridge.py --config config\development\geometry_mesh_bridge_v1.json --output-root artifacts\work110\run_b --replay-reference artifacts\work110\run_a\result.json
# exit 0; exact replay
git diff --check
# exit 0
```

Final affected regression and staged checks remain before commit; the verified hash is reported in the final handoff.

## Limitations and follow-up

The B-rep route uses centre-sampled voxels and a permissive disclosed `35%` bound; it is suitable as a bounded bridge, not high-fidelity curved meshing. Error aliasing, thin-feature loss outside the selected case, and absent solver-field convergence remain. Work 111 must solve and verify vector fields on these exact meshes without treating mesh quality as physics validation.
