# Work 135: Native Detailed Vehicle Realization

แหล่งภาษาอังกฤษ: `work135-native_detailed_vehicle_realization.md`

Status: Planned

แหล่งการวางแผน: Work 134 จริงหลัง scope regression ของ Work 126

Dependencies: Work 108, 110, 112–123, 125, 126, 129 และ 130; ตรวจ CadQuery และ FreeCAD/OCCT ใหม่ตอน execution

ข้อกำหนดร่วมบังคับ: [ดัชนีและกติกา](README.th.md) แผนนี้ยังไม่ใช่ implementation และไม่ทำให้ Work 126 สมบูรณ์ย้อนหลัง

## 1. ผลลัพธ์แก้ไขและขอบเขต

สร้าง candidate หนึ่ง revision ที่แน่นอนและเชื่อมต่อทางกายภาพ เป็น native OCCT B-rep part solids พร้อม assembly ที่ตรวจได้ แทน axis-aligned boxes ของ Work 126 ในฐานะแหล่ง geometry โดยเก็บกล่องเดิมเป็นเพียง function/hardware checklist

Artifact ต้องแสดง manufactured หรือ purchased-part geometry ที่มีหลักฐาน, internal hardware, connection features, material/void ownership, assembly relationships, motion และ face-level physics boundaries Bounding box, role label, graph edge, tessellation หรือ render ใช้แทน part solidไม่ได้

Work 135 เป็น geometry-realization gate ไม่จำเป็นต้องแสดง benefit และยืนยัน manufacturing readiness, safety, physical validation หรือ promotion ไม่ได้

## 2. Entry evidence และ frozen identity

Work 135 log ต้องตรึง commit/result/contract hashes ของ upstream, identities ของ CadQuery/FreeCAD/OCCT/Gmsh/CalculiX, candidate ID ใหม่, task/energy/safety/function checklist, part/instance inventory, material/process eligibility, purchased sources และ unresolved entries แยก `pilot`, admitted `run_a` และ clean replay `run_b`

Work 134 probe พบ CadQuery `2.8.0`, FreeCAD `1.1.3`, OCCT `7.8.1`, Gmsh และ CalculiX เมื่อ 2026-09-13 แต่ execution ต้องตรวจใหม่ ห้ามใช้ `final_126_r1` ซ้ำ

Reuse upstream STEP ได้ราย part เมื่อ exact hash, material/use envelope และ interfaces ยังใช้ได้ ให้ audit Work 083, 084, 087, 108 และ 113 ห้ามรับ old whole candidate โดยอัตโนมัติ

## 3. Maintained files

- `src/formula_ultimate/assembly/native_detailed_vehicle.py`
- `config/development/native_detailed_vehicle_v1.json`
- `scripts/cad/build_native_detailed_vehicle.py`
- `scripts/cad/inspect_native_detailed_vehicle_freecad.py`
- `scripts/development/run_native_detailed_vehicle.py`
- `tests/test_native_detailed_vehicle.py`
- สัญญาสองภาษา `NATIVE_DETAILED_VEHICLE_V1` และ Work 135 logs

Generated artifacts ถูก ignore ใต้ `artifacts/work135/{pilot,run_a,run_b,negative_controls}`

## 4. Physical occurrences บังคับ

ไม่บังคับจำนวนล้อ, symmetry, body style หรือ powertrain แต่ architecture ที่เลือกต้องแสดง structure/reinforcement, ground bodies และ supports/bearings/axles, actuation/shafts/couplings/transmission/housings, energy source/containment/terminals/conductors, controller/sensors/connectors/supports, cooling/voids/ducts/pumps/fans, external wetted geometry/openings, fasteners พร้อม engagement, seals และ compression faces, harnesses พร้อม swept section/bend radius และ service/removal paths

Repeated hardware instance จาก definition hash เดียวได้ แต่ทุก occurrence ต้องมี ID/placement/ownership/mass ห้าม outer shell ซ่อน internals Purchased part ต้องมี supplier/source geometry ตรง Surrogate ต้องติด label และปิด completion จน interface/envelope/mass/inertia match หลักฐาน

## 5. Native representation และ semantic identity

Manufactured part เป็น valid closed B-rep solid หนึ่งก้อน เว้นแต่ประกาศ multi-solid ตาม process Fluid/air cavities เป็น zero-structural-mass void solids Flexible tube/harness ต้องมี native swept solid และ semantic centerline

Declaration ใช้ metres/SI และแปลงเป็น CAD millimetres ที่ adapter Part record ต้องมี definition/instance/revision/provenance, feature inventory, material/process, STEP hash/topology, volume/center/full inertia, semantic face signatures/adjacency, minimum-feature evidence, access และ physics roles

ห้าม persistent raw `FaceN`/`EdgeN` Face signature ใช้ surface type, area, centroid, orientation/axis, bounds และ adjacency และต้องรอด STEP export/import Hidden repair ทำให้ fail Primitive ใช้ได้เฉพาะเมื่อเป็น finished form จริงพร้อม holes/seats/passages/interfaces; same-envelope primitive substitution ต้องตก

## 6. Assembly/interface/tolerance/motion gates

ทุก instance ต้องเชื่อมถึง assembly root ผ่าน explicit joint/non-contact relation พร้อม mating faces, axes, DOF, stops, gap/interference, fit, fastening/sealing และ load/energy/signal/heat ownership

ต้องไม่มี floating/unowned region; mating residual `<=1e-6 m`; non-contact penetration `<=1e-12 m^3`; ใช้ worst-case tolerance; fastener engagement และ seal compression ชัด; harness/tube ต่อ endpoints, ผ่าน bend radius และ clearance; assembly order acyclic พร้อม access

Motion ใช้ endpoints/events, อย่างน้อย 101 samples และ adaptive refinement จน minimum-clearance change `<=1e-5 m`; ใช้ analytic swept envelope เมื่อทำได้และเปิดเผย between-sample risk

## 7. Geometry ledgers และ physics maps

คำนวณ material/void volume, mass, center และ full inertia ใหม่จาก exact solids/densities ห้าม aggregate กรอกมือ override geometry CadQuery-to-FreeCAD limits: relative volume/mass `<=1e-8`, center residual `<=1e-7 m`, inertia residual `<=1e-7`, solid counts ตรง, invalid/null/hidden repair เป็นศูนย์

Map semantic faces/regions สำหรับ structural, thermal, internal flow, external aero, ground/motion, energy และ control/sensor endpoints Signature ที่เปลี่ยนหรือหายต้อง fail Work 136 ต้อง rerun physics; ห้าม inherit Work 123–130 จาก box registry

## 8. Artifacts และ replay

ต้องมี artifact อย่างน้อยดังนี้

- `parts/<definition_id>.step` และ hash manifest
- separate-solid assembly STEP `native_vehicle_<candidate_id>.step`
- exact-import witness `native_vehicle_<candidate_id>.FCStd`
- `cadquery_manifest.json` และ `freecad_report.json`
- `semantic_faces.json`, `interface_graph.json`, `material_void_regions.json` และ `physics_boundary_map.json`
- mass/inertia, collision/clearance, swept-motion และ tolerance reports
- native-derived exploded/section manifests
- `result.json`, negative-control records และ `replay.json`

Canonicalize STEP timestamp/order `run_a` กับ clean `run_b` ต้องได้ hashes ตรง Preview tessellation chord `<=0.00025 m` เป็น visualization เท่านั้น

## 9. Negative controls บังคับ

ต้องปฏิเสธ same-bbox substitution; missing bearing/support/fastener/seal/connector/harness; floating component; duplicate mass; invalid/open topology; changed STEP; hidden repair; lost semantic face; wrong mate/engagement; nominal-only tolerance; swept collision; trapped/cyclic assembly; cable/tube failure; void with density; missing aero opening; unsupported purchased proxy; changed upstream identity; และ render ที่ไม่มี native manifest

เลือกอย่างน้อยหนึ่ง component แบบไม่ขึ้นกับ proxy score แล้ว audit feature tree, sections, interfaces, ownership และ access

## 10. Experiment และ acceptance

IV คือ candidate/features/placement/joint/tolerance/motion/representation DV คือ native/topology/semantic validity, occurrence coverage, ledgers, interface, collision/motion และ boundary coverage Primary estimand คือสัดส่วน required occurrences ที่เป็น valid native solids ต้องเท่ากับ `1.0` และไม่มี unknown essential occurrence

สถานะมี `invalid_native_geometry`, `incomplete_part_realization`, `assembly_unresolved`, `physics_mapping_unresolved`, `passed_native_detailed_geometry` เฉพาะตัวสุดท้ายทำให้ Work 135 complete และยังหมายถึง geometry เท่านั้น ไม่ใช่ physics benefit/manufacturing/safety/validation

## 11. ลำดับทำงาน

1. เปิด Work 135 logs และตรึง inputs/runtimes/inventory/thresholds
2. Audit upstream STEP ราย part
3. สร้าง strict schema/semantic signatures
4. Build native parts ตาม function โดยเปิด architecture
5. เพิ่ม connection/seal/routing/support/service features จริง
6. Assemble instances และตรวจ tolerance/motion/collision
7. สร้าง material/void และ physics-face maps
8. FreeCAD exact import โดยไม่ repair และ cross-check
9. รัน controls และ clean exact replay
10. รัน regressions ที่ได้รับผล
11. สร้าง bilingual result และ commit explicit maintained files

## 12. Validation commands

รันคำสั่งต่อไปนี้แบบ fail-fast:

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

CadQuery/FreeCAD ไม่ได้รัน, cross-import ถูกข้าม, negative control fail หรือ replay ไม่ exact ต้อง block completion

## 13. ความเสี่ยงและ handoff

CadQuery/FreeCAD ใช้ OCCT ร่วมกันจึงไม่ใช่ independent-kernel validation STEP อาจ reorder topology จึงใช้ semantic signatures Detailed geometry อาจเปิดเผย packaging ที่ทำไม่ได้หรือ performance ติดลบ ให้เก็บหลักฐาน Supplier geometry ที่ขาดต้องหยุดด้วย exact part ID ไม่แทนด้วยกล่อง ถ้าต้องเพิ่ม solver/supplier program ให้แยก numbered work

เมื่อสำเร็จ ส่ง exact native candidate ให้ Work 136 revalidate structural, thermal, flow, ground, actuation, energy และ control บน geometry นี้
