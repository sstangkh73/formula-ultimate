# แผนงาน 045: Loaded Interface และ Joint Load Path

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_045_loaded-interface-joint-load-path-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

แสดงว่า finite resultant force ที่เข้าทาง declared cylindrical interface หนึ่งไหลผ่าน connected plate solid หนึ่งชิ้นและปิดที่ declared support interfaces สองตัว โดย interface identity คงอยู่ตลอด CAD, STEP, FreeCAD, mesh, solver input และ parsed result

## ขอบเขตและข้ออ้าง

- สร้าง `loaded_interface_plate_v1`: rectangular prismatic plate ที่มี loaded through-hole หนึ่งรูและ support through-holes สองรูซึ่งนิยามด้วย topology-neutral geometric signature
- Generate CAD solid หนึ่งชิ้นด้วย CadQuery, export hashed STEP หนึ่งไฟล์, import/identify cylindrical interface ทั้งหมดอย่างอิสระใน FreeCAD, mesh exact STEP ด้วย Gmsh และ solve linear elasticity ด้วย CalculiX
- ใช้ constant-direction consistent traction resultant บน loaded cylindrical surface และ rigid bonded support constraint บน declared support cylindrical surfaces
- วัด compliance, nominal bearing/net-section stress, support load share, force/moment closure, solver internal energy, field evidence, mesh convergence และ one-support boundary-sensitivity case

งานนี้ validate เฉพาะ declared bonded-interface plate fixture ไม่ validate bolt, pin/contact, bearing failure, weld, adhesive, friction, preload, manufacturing tolerance, nonlinear material failure, arbitrary joint หรือ vehicle chassis

## การออกแบบการทดลอง

- ตัวแปรอิสระ: mesh size, support interface set (`both_supports` เทียบ `lower_support_only`), interface geometry และ load eccentricity ที่ fixed ด้วย loaded-hole center
- ตัวแปรตาม: interface area/resultant/moment, compliance, reaction load share, nominal bearing/net-section stress, internal/external energy, stress field, mesh identity และ wall time
- ตัวแปรควบคุม: exact STEP hash หนึ่งค่า, material, coordinate frame, geometric interface signature, load resultant/direction, mesh family, solver/parser และ SI unit
- สมมติฐานที่ต้องการพิสูจน์: last-two compliance change `<=5%`; force/moment residual `<=1e-5`; energy residual `<=1e-4`; interface identity อยู่ครบ และ boundary sensitivity `<=10%` สำหรับ transferability
- การพยายามหักล้าง: เก็บ one-support result แม้ reject transferability; reject broken ligament, missing support, duplicated load ID, zero-area interface และ disconnected solid

## Implementation และไฟล์ที่วางแผน

- `config/structural/loaded_interface_plate_v1.json`
- interface grammar, mesh mapping, consistent load, deck และ result parser ใต้ `src/formula_ultimate/structural/`
- CadQuery generator และ FreeCAD independent interface inspector
- Work 045 orchestrator/launcher และ ignored evidence ใต้ `artifacts/work045/`
- focused identity/load/negative-control test
- bilingual physics report และ matching result records

Proposed mesh size `6`, `4`, `3 mm` ถูก freeze ก่อน solver result Mesh-only count อาจ reject compute infeasibility แต่ห้าม tune ระดับด้วย structural response

## Validation และเกณฑ์สำเร็จ

- exact interface ID และ STEP hash อยู่ครบทุก declared stage
- force/moment residual `<=1e-5` และ internal/external energy residual `<=1e-4` ทุก admitted solve
- last-two compliance และ integrated-resultant change `<=5%`
- measured boundary-response change `>10%` ต้อง mark transferability `rejected` โดยไม่ลบ completed execution evidence
- malformed/disconnected control ทุกตัว fail closed
- focused/live/full test, compile/static check, staged-diff check, explicit commit และ clean-tree replay ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

STEP ไม่รับประกัน application-level face label ดังนั้น identity ใช้ immutable center/radius/axis/area signature ที่ตรวจอิสระทุก stage Linear tetrahedra อาจ reject convergence hypothesis ใกล้รู Rigid bonded cylindrical support อาจไวต่อ stiffness และถูกทดสอบโดยตั้งใจ ไม่มี contact, bolt preload, plastic bearing, fracture, fatigue coupling, whole vehicle, push หรือ publication
