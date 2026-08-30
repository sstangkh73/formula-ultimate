# แผนงาน 047: Topology-Neutral Whole-Vehicle CAD และ Assembly Grammar

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_047_topology-neutral-vehicle-assembly-plan.md`

## วัตถุประสงค์

Represent และ verify complete multi-component 3D vehicle candidate หนึ่งตัวโดยไม่กำหนด conventional vehicle shape, จำนวนล้อ, จำนวน component หรือ layout พร้อมบังคับให้ solid, material, interface, connection, contact, energy path และ external-load path ทุกส่วน explicit

## ขอบเขตและขอบเขตการอ้างผล

สร้าง versioned assembly grammar จาก initial library ของ neutral solid primitive, deterministic placement, typed point interface, graph connection, contact, envelope/keep-out rule และ material-density record Export exact per-component STEP พร้อม multi-solid assembly STEP หนึ่งไฟล์ ตรวจอย่างอิสระด้วย FreeCAD และเปรียบเทียบ geometry-derived mass properties นี่คือ geometric admission เท่านั้น ไม่ใช่หลักฐาน structural, aerodynamic, thermal, manufacturing, safety, race, novelty หรือ superiority

## การออกแบบการทดลอง

- ตัวแปรอิสระ: component count, primitive type/parameter, placement, material, interface declaration, connection graph, contact count/arrangement, energy graph, load-support graph, envelope และ keep-out
- ตัวแปรตาม: solid validity/count, STEP identity, interface position residual, overlap/keep-out/envelope/ground-clearance status, mass, centre of mass, inertia tensor, graph connectivity และ replay hash
- ตัวแปรควบคุม: grammar/library version, SI global frame, translation-only v1 transform, material record, exact tolerance, tool path, ไม่มี hidden healing/repair และ exact Work 046 failure-contract identity
- สมมติฐานที่ต้องการ: admitted fixture regenerate declaration/STEP identity ตรงกัน, typed path ทุกเส้นครบ, solid ทุกชิ้น valid และ FreeCAD เทียบ independent component-sum mass/centre/inertia residual แต่ละค่า `<=1e-6` relative
- เกณฑ์ล้มเหลว: floating component, overlapping protected volume, unmatched interface, disconnected required energy/load path, invalid/duplicate identity, invalid solid, massless energy component, envelope violation หรือ undeclared ground contact ต้อง fail closed

## ไฟล์ที่วางแผน

- `config/vehicle/topology_neutral_vehicle_v1.json`
- `src/formula_ultimate/topology/vehicle_assembly.py` และ exports
- CadQuery generator และ FreeCAD inspector ใต้ `scripts/cad/`
- `scripts/topology/run_vehicle_assembly_acceptance.py`
- `scripts/run_work047.ps1`
- `tests/test_vehicle_assembly.py`
- `docs/physics/TOPOLOGY_NEUTRAL_VEHICLE_ASSEMBLY.md` และ `.th.md`
- result record สองภาษาของ Work 047
- ignored CAD/STEP/evidence ใต้ `artifacts/work047/`

## การตรวจสอบ

รัน focused grammar/negative-control tests, CAD export อิสระสองรอบ, FreeCAD inspection, deterministic Work 047 experiment, Work 046 regression, full repository tests, Python compilation, repository-contract checks, staged-diff checks, explicit scoped commit และ clean-tree replay

## เกณฑ์ความสำเร็จ

- Component/assembly STEP artifact deterministic และ solid ทุกชิ้น valid
- Interface residual และ forbidden-overlap residual ผ่าน declared tolerance โดยไม่มี repair
- Required source-to-propulsion และ external-load-to-contact path มีอยู่แบบ explicit
- FreeCAD และ analytical/component-sum mass, centre, inertia ตรงกันภายใน `1e-6` relative
- Negative control ทุกกรณี fail closed และ same-input replay identity ตรง exact

## ความเสี่ยง

STEP ไม่รักษา application label อย่างเชื่อถือได้ จึงต้องใช้งาน per-component hash พร้อม geometric signature Primitive-only v1 grammar เป็น expressive infrastructure ไม่ใช่ open-ended shape discovery Translation-only placement ยังไม่รองรับ arbitrary orientation ใน work item นี้

## สิ่งที่ไม่ทำอย่างชัดเจน

ไม่รวม conventional-car template, fixed wheel/contact count, FEA load case, aerodynamics, cooling, manufacturing, controls, race fitness, design search, push หรือ publication
