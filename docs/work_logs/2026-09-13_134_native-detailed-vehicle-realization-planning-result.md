# Work 134 Result: Native Detailed Vehicle Realization Planning

Thai companion: `2026-09-13_134_native-detailed-vehicle-realization-planning-result.th.md`

Date: 2026-09-13 (Asia/Bangkok)

Status: Completed

## Outcome

Authored the bilingual, execution-ready Work 135 plan for a native detailed vehicle. The plan explicitly corrects the implementation gap exposed after Work 126: the Work 126 bounding-box registry remains a function checklist and is not accepted as detailed vehicle geometry. The bilingual detailed-plan index now records Work 135 as a forward corrective extension without rewriting Work 126 history.

Work 135 requires a complete occurrence inventory, valid native OCCT B-rep solids, semantic face identities, material/void ownership, physical joints, tolerances, motion/clearance checks, per-part and assembly STEP, an exact-import FCStd witness, physics-boundary maps, eighteen falsification controls and exact clean replay. Passing it will mean only `passed_native_detailed_geometry`; downstream physics must be rerun in Work 136.

This work item changed planning evidence only. It did not implement CAD, select a conventional layout, establish performance, authorize fabrication or validate a physical vehicle.

## Files changed

- `docs/plans/detailed_part_to_vehicle_v1/work135-native_detailed_vehicle_realization.md`
- `docs/plans/detailed_part_to_vehicle_v1/work135-native_detailed_vehicle_realization.th.md`
- `docs/plans/detailed_part_to_vehicle_v1/README.md`
- `docs/plans/detailed_part_to_vehicle_v1/README.th.md`
- `docs/work_logs/2026-09-13_134_native-detailed-vehicle-realization-planning-plan.md`
- `docs/work_logs/2026-09-13_134_native-detailed-vehicle-realization-planning-plan.th.md`
- `docs/work_logs/2026-09-13_134_native-detailed-vehicle-realization-planning-result.md`
- `docs/work_logs/2026-09-13_134_native-detailed-vehicle-realization-planning-result.th.md`

## Decisions and inspected capability

- Work 134 is the completed planning record; Work 135 is the proposed implementation work so planning is not confused with CAD realization.
- The plan preserves architecture freedom but requires every physical occurrence applicable to the selected architecture. A shell, graph, label, bounding box, tessellation or render cannot substitute for the native part.
- Installed probes on 2026-09-13 returned CadQuery `2.8.0`, FreeCAD `1.1.3`, OCCT `7.8.1` and Gmsh `4.15.0`; `C:\Program Files\FreeCAD 1.1\bin\ccx.exe` exists. Work 135 must pin these identities again rather than inherit this probe.
- Direct `import Part` under the FreeCAD Python executable and `Standard_Version` from the CadQuery OCP binding were not valid version-probe paths. `FreeCAD.ConfigGet('OCC_VERSION')` returned `7.8.1`. This was a probe-interface limitation, not a repository product defect.
- CadQuery and FreeCAD both use OCCT, so their agreement is disclosed as a cross-application witness, not independent-kernel validation.
- No repository bug was encountered or fixed in Work 134. The historical scope regression is addressed by the new forward plan and is not rewritten as a newly discovered code bug.

## Validation evidence

The following commands were run separately with fail-fast exit handling:

```powershell
$en='docs/plans/detailed_part_to_vehicle_v1/work135-native_detailed_vehicle_realization.md'; $th='docs/plans/detailed_part_to_vehicle_v1/work135-native_detailed_vehicle_realization.th.md'; $required=@('passed_native_detailed_geometry','1e-12','0.00025','tests.test_native_detailed_vehicle','native_detailed_vehicle_v1.json','Work 136','semantic_faces.json','interface_graph.json','material_void_regions.json','physics_boundary_map.json'); foreach($f in @($en,$th)){ if(-not (Test-Path -LiteralPath $f)){throw "missing $f"}; $body=Get-Content -Raw -LiteralPath $f; foreach($token in $required){if(-not $body.Contains($token)){throw "$f missing $token"}}}; $enReadme=Get-Content -Raw -LiteralPath 'docs/plans/detailed_part_to_vehicle_v1/README.md'; $thReadme=Get-Content -Raw -LiteralPath 'docs/plans/detailed_part_to_vehicle_v1/README.th.md'; if(-not $enReadme.Contains('(work135-native_detailed_vehicle_realization.md)')){throw 'English index missing Work 135'}; if(-not $thReadme.Contains('(work135-native_detailed_vehicle_realization.th.md)')){throw 'Thai index missing Work 135'}; if(-not (Get-Content -Raw -LiteralPath $th).Contains('แหล่งภาษาอังกฤษ: `work135-native_detailed_vehicle_realization.md`')){throw 'Thai source reference missing'}; Write-Output 'work135_plan_contract: PASS'
python -m unittest tests.test_repository_contract -v
python -m compileall -q src scripts tests
git diff --check
```

Results before closing the log:

- Work 135 bilingual plan/index static contract: exit `0`, `work135_plan_contract: PASS`.
- `tests.test_repository_contract`: exit `0`, 6 tests passed.
- `compileall`: exit `0`.
- working-tree `git diff --check`: exit `0`; Git emitted only LF-to-CRLF working-copy notices for the two edited index files.

The completed-log contract, explicit staged scope and cached diff checks are rerun immediately before the required commit.

## Limitations and follow-up

The planned Work 135 commands were documented, not executed. No native detailed candidate, per-part STEP set, assembly FCStd, mass/inertia ledger or face-level physics map exists from this work item. The next execution item is Work 135. If exact supplier geometry or any essential occurrence remains unsupported, Work 135 must stop as `incomplete_part_realization` rather than replace it with a box. Work 136 is required before any downstream physics conclusion can apply to the new geometry.
