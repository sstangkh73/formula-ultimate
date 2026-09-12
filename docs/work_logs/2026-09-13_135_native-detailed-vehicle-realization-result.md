# Work 135 Result: Native Detailed Vehicle Realization

Thai companion: `2026-09-13_135_native-detailed-vehicle-realization-result.th.md`

Date: 2026-09-13 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 135 realized new candidate `tri_contact_native_135_r1` as 48 native OCCT B-rep definitions and 83 uniquely owned occurrences: 77 material solids and 6 explicit zero-structural-mass void solids. The architecture is the selected three-contact open-body arrangement derived from the Work 118 contact tasks; Work 126 supplied only the function checklist, not geometry. The maintained implementation creates actual structure, three ground bodies with carriers/bushings/axles, an in-wheel actuation/transmission chain, energy containment and internals, controller/sensors/connectors, cooling hardware and flow voids, routed harnesses/tubes, external panels/opening, fasteners/nuts/washers/gasket and service voids.

CadQuery derived mass `1023.6476530495439 kg`. FreeCAD independently recomputed `1023.6476530421635 kg` from the exact occurrence STEP files. Maximum cross-application residuals were volume `3.338611945214137e-9` relative, mass `3.3386118825076423e-9` relative, center `1.8893996922564327e-9 m` absolute and inertia `4.176665888559849e-9` relative. All 48 definition STEP and 83 occurrence STEP files imported as one valid solid each; material/void assembly counts were `77/6`; all `754/754` semantic selector groups survived; non-contact penetration was `0.0 m^3`; motion used 101 samples with zero collisions and `0.0 m` refinement change.

Required occurrence coverage and physics-boundary coverage are both exactly `1.0`; unknown essential occurrences are zero. All 18 mandatory falsification-control groups were rejected. The independent SHA-256 selection audited `pack_washer_1` without proxy-score preference; no component-specific serviceability claim was invented. `run_a` and clean `run_b` match exactly at result SHA-256 `a9a3f55571bf5b5441c3ef3e8b2674623305d8c1fb02814dcf87cd4a1b9b7d3c`; the canonical FCStd SHA-256 is `3353e4266e4d119e19fb76477862749fb77fc2fe5e0a72bea432bf165b782ee6`.

The admitted status is `passed_native_detailed_geometry`. Promotion remains false. This is a native-geometry/assembly gate, not a claim that the `1023.65 kg` unoptimized candidate is competitive or physically valid.

## Files changed

- `src/formula_ultimate/assembly/native_detailed_vehicle.py`
- `config/development/native_detailed_vehicle_v1.json`
- `scripts/cad/build_native_detailed_vehicle.py`
- `scripts/cad/inspect_native_detailed_vehicle_freecad.py`
- `scripts/development/run_native_detailed_vehicle.py`
- `tests/test_native_detailed_vehicle.py`
- bilingual `docs/contracts/NATIVE_DETAILED_VEHICLE_V1.md` / `.th.md`
- this bilingual Work 135 plan/result pair

Generated evidence remains ignored under `artifacts/work135/{pilot,run_a,run_b}`. The admitted run contains 48 per-definition STEP files, 83 per-instance STEP files, material/void assembly STEP, non-evidence preview STL, exact-import FCStd, identity/semantic/interface/material-void/physics/property/collision/motion/tolerance/view reports, independent audit, controls and replay record.

## Decisions and pilot findings

- Kept the selected architecture open rather than introducing a conventional vehicle shape. New identity `tri_contact_native_135_r1` prevents Work 126 box geometry from being inherited.
- Regenerated the audited Work 83/84/87/108/113 geometry because none matched this candidate's exact placement and interfaces.
- Used valid one-solid OCCT topology plus exact FreeCAD re-import as the closed-solid witness because CadQuery 2.8.0's `Shape.Closed()` binding is unreliable.
- Matched curved STEP faces by stable physical properties. Parameter-seam bounds and seam-edge count remain diagnostic because STEP may reparameterize them; all selector groups still require one-to-one survival.
- Preserved pilot packaging failures: initial cross-subsystem overlaps were corrected through placement/feature changes until the Boolean non-contact report reached `0.0 m^3`; no penetration was silently waived.
- Did not optimize away the geometry-derived `1023.65 kg` mass. That contradicting result is retained for Work 136 rather than presented as benefit.

## Bug reports

1. **CadQuery closed flag false-negative.** Symptom: a valid one-solid definition, including a plain box and `active_stack`, was rejected because `Shape.Closed()` returned `False`. Root cause: the CadQuery 2.8.0 binding does not reliably expose the OCCT closed flag for these valid `TopoDS_Solid` objects. Fix: require `shape.isValid()` and exactly one `Solid`, then independently repeat validity/count checks after exact STEP import in FreeCAD. Regression: `test_cadquery_closed_flag_regression_uses_valid_single_solid` passes and all 131 definition/occurrence STEP files import as valid one-solid shapes.
2. **Fan definition split into three solids.** Symptom: the first six-blade fan construction fused into three disconnected solids. Root cause: the initial hub/blade radial placement did not provide sufficient intersection for one connected finished form. Fix: changed the fan hub radius to `0.05 m`, blade-center radius to `0.06 m`, and blade dimensions to `[0.018, 0.12, 0.025] m`. Regression: `test_fan_definition_regression_is_one_fused_solid` and both admitted builds pass.
3. **Semantic import gate could report a false pass.** Symptom: the early FreeCAD report said `passed` while raw semantic survival was only `0.9458333333333333`; signed zero and curved-face STEP seam changes also produced false signature loss. Root cause: report status originally considered invalid/null solids only, while raw exact hashes included nonphysical parameterization details. Fix: canonicalized signed zero, quantized declared numeric fields, matched selector records one-to-one with `1e-7 m` positional tolerance, kept planar bounds/edge count strict, treated curved seam bounds/count as diagnostic, and made every residual/count/hash/semantic threshold part of inspector status. Regression: the final report passes `754/754`, survival `1.0`; a reduced survival negative control is rejected.
4. **CadQuery test environment import failure.** Symptom: the first Work 135 unit command exited 1 with `ModuleNotFoundError: No module named 'formula_ultimate'`. Root cause: the pinned CadQuery virtual environment did not install the local package and the test imported it before registering `src`. Fix: deterministically prepend repository root and `src` in the test bootstrap. Regression: the exact command now exits 0 with 9 tests passing.
5. **FCStd replay drift and timestamped backups.** Symptom: the first clean `run_b` exited 1; equivalent FCStd files had different document timestamps, UUIDs and transient object IDs (`1df6ab...` versus `eadd3d...`) and repeated saves could create timestamped `.FCBak` files. Root cause: FreeCAD document metadata is nondeterministic even when `Shape.bin` is identical. Fix: save to a disposable FCStd, canonicalize only ZIP timestamps and non-geometric document metadata/object IDs, preserve native shape bytes unchanged, atomically replace the witness, and exclude backup/temp files from evidence. Regression: both admitted runs produce FCStd SHA-256 `3353e426...`, result SHA-256 `a9a3f555...`, and replay `exact: true`.

## Validation

```powershell
& 'C:\Formula Ultimate\.tools\cadquery-mcp\Scripts\python.exe' -m unittest tests.test_native_detailed_vehicle -v
# initial exit 1 before bug 4 fix; final exit 0; 9 tests passed
& 'C:\Formula Ultimate\.tools\cadquery-mcp\Scripts\python.exe' scripts/cad/build_native_detailed_vehicle.py --config config/development/native_detailed_vehicle_v1.json --output-root artifacts/work135/run_a/cad --manifest artifacts/work135/run_a/cadquery_manifest.json
# exit 0; 48 definitions, 83 instances, 77 material solids, 6 void solids, 0.0 m^3 non-contact penetration
& 'C:\Program Files\FreeCAD 1.1\bin\python.exe' scripts/cad/inspect_native_detailed_vehicle_freecad.py artifacts/work135/run_a/cadquery_manifest.json config/development/native_detailed_vehicle_v1.json artifacts/work135/run_a/freecad_report.json artifacts/work135/run_a/native_vehicle_tri_contact_native_135_r1.FCStd
# exit 0; exact no-repair import; 48 definitions and 83 instances valid; semantic survival 1.0
& 'C:\Formula Ultimate\.tools\cadquery-mcp\Scripts\python.exe' scripts/development/run_native_detailed_vehicle.py --config config/development/native_detailed_vehicle_v1.json --output-root artifacts/work135/run_a
# exit 0; passed_native_detailed_geometry; 18/18 controls rejected; result SHA-256 a9a3f55571bf5b5441c3ef3e8b2674623305d8c1fb02814dcf87cd4a1b9b7d3c
& 'C:\Formula Ultimate\.tools\cadquery-mcp\Scripts\python.exe' scripts/development/run_native_detailed_vehicle.py --config config/development/native_detailed_vehicle_v1.json --output-root artifacts/work135/run_b --replay-reference artifacts/work135/run_a/result.json
# first pre-fix exit 1 from FCStd drift; final exit 0; exact replay
python -m compileall -q src scripts tests
# exit 0
python -m unittest tests.test_spatial_material tests.test_geometry_mesh_bridge tests.test_physical_interface_graph tests.test_detailed_connection_contact tests.test_moving_contact_assembly tests.test_realized_actuation_chain tests.test_onboard_energy_realization tests.test_geometry_flow_heat_exchange tests.test_control_hardware_realization tests.test_repository_contract -v
# exit 0; 61 tests passed
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly 12 declared Work 135 maintained files
git diff --cached --check
# exit 0
```

## Limitations and follow-up

CadQuery and FreeCAD both use OCCT, so agreement is a cross-application witness rather than independent-kernel validation. Geometry materials include synthetic geometry-only densities, no supplier-certified purchased geometry, process qualification or physical correlation. The assembly gate does not establish component-specific serviceability for every part. The registered motion proves only the axisymmetric front-tire spin; non-axisymmetric steering remains unmodeled.

The very high unoptimized mass and all earlier structural, thermal, internal/external flow, ground, actuation, energy and controller conclusions must be challenged on the exact Work 135 solids. Work 136 is required before any performance, feasibility, promotion, manufacturing, safety or physical-validation claim.
