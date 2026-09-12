# Work 135: Native Detailed Vehicle Realization

Thai companion: `work135-native_detailed_vehicle_realization.th.md`

Status: Planned

Planning source: actual Work 134 corrective planning after the Work 126 scope regression.

Dependencies: Works 108, 110, 112–123, 125, 126, 129 and 130; CadQuery and FreeCAD/OCCT runtimes reverified at execution.

Mandatory common requirements: [index and execution rules](README.md). This plan is not implementation and does not make Work 126 retroactively complete.

## 1. Corrective outcome and boundary

Realize one exact, physically connected candidate as native OCCT B-rep part solids and an inspectable assembly. Replace the Work 126 axis-aligned boxes as geometry source; retain them only as a function/hardware checklist.

The artifact must expose manufactured or evidence-bound purchased-part geometry, internal hardware, connection features, material/void ownership, assembly relationships, motion and face-level physics boundaries. A bounding box, role label, graph edge, tessellation or render cannot substitute for a part solid.

Work 135 is a geometry-realization gate. It need not show benefit and cannot establish manufacturing readiness, safety, physical validation or promotion.

## 2. Entry evidence and frozen identity

Before implementation, the Work 135 log must pin:

1. Exact commit and result/contract SHA-256 for every consumed work.
2. CadQuery Python, CadQuery, FreeCAD, OCCT, Gmsh and CalculiX identities. The Work 134 probe found CadQuery `2.8.0`, FreeCAD `1.1.3`, OCCT `7.8.1`, Gmsh and CalculiX on 2026-09-13; execution must recheck.
3. A new candidate ID/revision. `final_126_r1` may not be reused.
4. External task, primary-energy boundary, safety scope and architecture-neutral function checklist.
5. Complete part/instance inventory, material/process eligibility, purchased sources and unresolved entries before admitted build.
6. Separate `pilot`, admitted `run_a` and clean replay `run_b` directories. Pilot output cannot be relabelled as admitted evidence.

Upstream STEP is reusable only per part when exact hash, material/use envelope and interfaces remain applicable. Audit Work 083 ground-interaction, Work 084 energy/torque, Work 087 integrated parts, Work 108 spatial/free-form solids and Work 113 detailed connection solids. Never accept an old whole candidate by inheritance.

## 3. Proposed maintained files

- `src/formula_ultimate/assembly/native_detailed_vehicle.py`: strict schema, semantic signatures, part/instance/port/joint parsing and closure checks.
- `config/development/native_detailed_vehicle_v1.json`: frozen candidate, evidence and thresholds.
- `scripts/cad/build_native_detailed_vehicle.py`: deterministic CadQuery construction and canonical STEP export.
- `scripts/cad/inspect_native_detailed_vehicle_freecad.py`: exact no-repair FreeCAD import, FCStd witness and cross-check.
- `scripts/development/run_native_detailed_vehicle.py`: orchestration, pins, controls, artifact hashes and replay.
- `tests/test_native_detailed_vehicle.py`.
- Bilingual `NATIVE_DETAILED_VEHICLE_V1` contract and dated Work 135 logs.

Generated artifacts remain ignored under `artifacts/work135/{pilot,run_a,run_b,negative_controls}`.

## 4. Mandatory physical-occurrence decomposition

Do not prescribe conventional wheel count, symmetry, body style or powertrain. Do require every occurrence applicable to the selected architecture:

- load-bearing structure and reinforcement;
- every ground-interaction body, carrier, bearing/bushing, axle or equivalent support;
- actuators/converters, shafts, couplings, transmission elements and housings;
- onboard energy source, containment, retention, terminals, switching and conductors;
- controller enclosure/modules, sensors, connectors and supports;
- heat-rejection hardware, fluid/air voids, ducts/tubes and pumps/fans when applicable;
- external wetted geometry and every opening changing the flow domain;
- fasteners, nuts/inserts/washers or justified captive equivalents, with axes and engagement;
- seals/gaskets and mating/compression surfaces;
- signal/power harnesses with endpoints, swept sections and bend radii;
- service/removal paths and retained hardware.

Repeated hardware may instance one definition hash, but each occurrence needs a unique instance ID, placement, ownership and mass. An outer shell cannot hide unmodelled internals. Purchased parts need exact supplier/source geometry. A surrogate must be labelled and blocks completion until interface, envelope, mass and inertia match eligible evidence.

## 5. Native representation and semantic identity

Each manufactured part is one valid closed B-rep solid unless a declared process requires multi-solid construction. Fluid/air cavities are separate zero-structural-mass void solids. Flexible tubes/harnesses require a native swept solid plus semantic centerline.

The declaration uses metres/SI; adapters convert explicitly to CAD millimetres. Each part record carries definition/instance/revision/provenance, construction-feature inventory, material/process IDs, STEP hash, validity and topology counts, volume/center/full inertia, semantic face signatures/adjacency, minimum-feature evidence, access and physics roles.

Persistent raw `FaceN`/`EdgeN` identity is forbidden. Face signatures combine surface type, area, centroid, orientation/axis where defined, bounds and local adjacency, and must survive STEP export/import. Hidden healing or topology repair fails.

A box/cylinder is allowed only when it is the intended finished form with all required holes, seats, passages and end features. Replacing a detailed part with a same-envelope primitive must fail.

## 6. Assembly, interface, tolerance and motion gates

Every instance must reach one assembly root through an explicit joint or approved non-contact relation. Record mating semantic faces, axes, DOF, stops, nominal gap/interference, fit, fastening/sealing hardware and load/energy/signal/heat ownership.

Acceptance requires:

1. no floating instance or unowned material/void;
2. mating face/axis residual `<= 1e-6 m` unless a tighter allocation is registered;
3. non-contact penetration volume `<= 1e-12 m^3`;
4. worst-case, not nominal-only, clearance/preload/seal propagation;
5. fastener axes intersect both retained interfaces and engagement is explicit;
6. seals lie between registered faces within their compression evidence range;
7. harness/tube routes meet endpoints, bend radius and solid-clearance constraints;
8. acyclic assembly order and tool/inspection/removal access or explicit non-serviceable justification.

Motion uses endpoints/events, at least 101 path samples and adaptive refinement until successive minimum-clearance change is `<= 1e-5 m`. Prefer analytic swept envelopes. Disclose between-sample risk when only sampling is available.

## 7. Geometry ledgers and face-level physics maps

Recompute material/void volume, mass, center and full inertia tensor from imported solids and densities; hand-entered aggregates cannot override geometry. CadQuery-to-FreeCAD limits:

- relative volume/mass residual `<= 1e-8`;
- absolute center residual `<= 1e-7 m`;
- componentwise inertia residual `<= 1e-7` relative to registered scale;
- exact definition, instance and assembly solid counts;
- zero invalid/null solids and hidden repairs.

Map exact semantic faces/regions for structural loads/support/contact, thermal sources/sinks/surfaces, internal-flow inlet/outlet/walls, external aerodynamic wetted surfaces/openings, ground contact/motion, energy terminals and controller/sensor endpoints. A changed or missing signature fails.

Work 135 verifies boundary existence/ownership. Downstream Work 136 must rerun the physics; Work 123–130 conclusions cannot be inherited from the box registry.

## 8. Required artifacts and replay

- `parts/<definition_id>.step` and hash manifest;
- separate-solid `native_vehicle_<candidate_id>.step`;
- exact-import `native_vehicle_<candidate_id>.FCStd`;
- `cadquery_manifest.json`, `freecad_report.json`;
- `semantic_faces.json`, `interface_graph.json`, `material_void_regions.json`, `physics_boundary_map.json`;
- mass/inertia, collision/clearance, swept-motion and tolerance reports;
- native-derived exploded/section manifests;
- `result.json`, negative-control records and `replay.json`.

Canonicalize STEP `FILE_NAME` time and deterministic ordering. Clean `run_a`/`run_b` must have identical declaration, per-part/assembly STEP, semantic map, FCStd witness and result hashes. Preview tessellation chord tolerance is `<= 0.00025 m`, but preview is never evidence source.

## 9. Mandatory falsification controls

Prove rejection of:

1. same-bounding-box primitive substitution;
2. missing bearing/support/fastener/seal/connector/harness occurrence;
3. labelled but floating component;
4. duplicate material ownership/mass;
5. open/non-manifold/invalid or undeclared multi-solid part;
6. swapped/edited STEP bytes;
7. hidden FreeCAD repair;
8. lost semantic face/boundary after regeneration;
9. mismatched mating axes or missing engagement;
10. nominal pass but worst-case clearance/preload/seal failure;
11. static pass with swept collision;
12. trapped part or cyclic assembly;
13. route endpoint/bend-radius/intersection failure;
14. void assigned structural density;
15. external opening missing from flow domain;
16. purchased proxy missing source/mass/interface evidence;
17. changed upstream identity; and
18. attractive mesh/render without matching native-solid manifest.

Independently select at least one component without proxy-score preference and audit its feature tree, sections, interfaces, ownership and access.

## 10. Experiment and acceptance

- IV: candidate revision, part features, placement, joint/tolerance state, motion coordinate and representation path.
- DV: native/topology/semantic validity, occurrence coverage, ledger residuals, interface closure, penetration/clearance, motion and boundary coverage.
- Controls: same task/function/energy requirements and authoritative material ownership; layout stays open.
- Primary estimand: fraction of required physical occurrences represented by valid evidence-bound native solids; acceptance requires exactly `1.0` with zero unknown essential occurrence.
- Secondary estimands: interface residual, minimum clearance, cross-import residual and boundary survival rate.

Statuses: `invalid_native_geometry`, `incomplete_part_realization`, `assembly_unresolved`, `physics_mapping_unresolved`, or `passed_native_detailed_geometry`. Only the last completes Work 135, and it means geometry only—not physics benefit, manufacturability, safety or validation.

## 11. Ordered implementation

1. Create Work 135 logs; freeze dependencies, candidate, runtimes, schema, inventory and thresholds.
2. Audit upstream STEP per part; accept/regenerate/reject with reasons.
3. Implement strict schema and semantic signatures before candidate construction.
4. Build native parts by functional subsystem while leaving architecture open.
5. Add real connection, sealing, routing, support and service features.
6. Assemble instances; generate joints/tolerances/motion and reject collision/floating parts.
7. Generate material/void and physics-face maps from exact solids.
8. Import exact STEP in FreeCAD without repair; save FCStd and cross-check.
9. Run all negative controls and clean exact replay.
10. Run affected CAD/material/interface/motion/energy/flow/control/repository regressions.
11. Create bilingual result and explicitly stage/commit maintained Work 135 files only.

## 12. Proposed validation commands

```powershell
& 'C:\Formula Ultimate\.tools\cadquery-mcp\Scripts\python.exe' -m unittest tests.test_native_detailed_vehicle -v
& 'C:\Formula Ultimate\.tools\cadquery-mcp\Scripts\python.exe' scripts/cad/build_native_detailed_vehicle.py --config config/development/native_detailed_vehicle_v1.json --output-root artifacts/work135/run_a/cad --manifest artifacts/work135/run_a/cadquery_manifest.json
& 'C:\Program Files\FreeCAD 1.1\bin\python.exe' scripts/cad/inspect_native_detailed_vehicle_freecad.py artifacts/work135/run_a/cadquery_manifest.json config/development/native_detailed_vehicle_v1.json artifacts/work135/run_a/freecad_report.json artifacts/work135/run_a/native_vehicle.FCStd
& 'C:\Formula Ultimate\.tools\cadquery-mcp\Scripts\python.exe' scripts/development/run_native_detailed_vehicle.py --config config/development/native_detailed_vehicle_v1.json --output-root artifacts/work135/run_a
& 'C:\Formula Ultimate\.tools\cadquery-mcp\Scripts\python.exe' scripts/development/run_native_detailed_vehicle.py --config config/development/native_detailed_vehicle_v1.json --output-root artifacts/work135/run_b --replay-reference artifacts/work135/run_a/result.json
python -m compileall -q src scripts tests
python -m unittest tests.test_spatial_material tests.test_geometry_mesh_bridge tests.test_physical_interface_graph tests.test_detailed_connection_contact tests.test_moving_contact_assembly tests.test_realized_actuation_chain tests.test_onboard_energy_realization tests.test_geometry_flow_heat_exchange tests.test_control_hardware_realization tests.test_repository_contract -v
git diff --check
git diff --cached --name-status
git diff --cached --check
```

All gates are fail-fast. Missing CadQuery/FreeCAD execution, skipped exact cross-import, failed negative control or non-exact replay blocks completion.

## 13. Risks and handoff

CadQuery and FreeCAD share OCCT, so agreement is a cross-application witness, not independent-kernel validation. STEP may reorder topology; use semantic signatures, never raw face indices. Detailed geometry may reveal infeasible packaging or negative performance—preserve it. Missing supplier geometry must stop with an exact part ID, not trigger a box substitution. Split new numbered work before adding new solver or supplier-program scope.

Successful handoff supplies one exact native candidate to Work 136 for structural, thermal, internal/external flow, ground, actuation, energy and controller revalidation on this geometry.
