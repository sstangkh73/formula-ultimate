# แผน Work 087: Load Structure, Packaging และ Thermal Integration

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_087_load-structure-packaging-thermal-integration-plan.md`

## สถานะ

สถานะ: Partial

## วัตถุประสงค์

ทำขอบเขต integration ที่เดิมเป็น Work 085 หลังงานแก้โครงสร้างสองงานที่บันทึกไว้ จัดวางชิ้นส่วน exact ของ Work 083 ground interaction และ Work 084 energy/torque ภายใน load frame ที่เกิดจากรูปทรงจริง พร้อม mount, coolant route, control route, service envelope, บัญชี load/energy/thermal, failure controls และ STEP/FCStd ครบชุด

นี่คือ integration candidate แบบ topology-neutral หนึ่งแบบ ไม่ใช่รูป chassis ที่บังคับ เนื่องจากหลักฐานวัสดุ/กระบวนการยัง synthetic และ integration frame ใหม่ยังไม่อยู่ใน component mesh ของ Work 086 คาดว่างานจะปิดเป็น `Partial` เว้นแต่ blocker เหล่านี้ได้รับการแก้แยกต่างหาก

## ขอบเขตที่ตรึงไว้

- นำเข้า STEP exact ห้าชิ้นจาก Work 083 และเจ็ดชิ้นจาก Work 084 โดยไม่แก้
- สร้าง integration solid ห้าชิ้นจากพารามิเตอร์ SI ที่ตรึง: `upper_load_bridge`, `ground_mount_adapter`, `energy_mount_adapter`, `coolant_inlet_route` และ `coolant_outlet_route`
- ส่งออก STEP identity แยกสิบเจ็ดชิ้น, integration STEP สิบเจ็ด solid และ FreeCAD FCStd ที่มี named object สิบเจ็ดชิ้น
- คำนวณมวล จุดศูนย์กลางมวล และ geometry inertia เต็มจาก B-rep exact กับความหนาแน่น synthetic ที่ประกาศ
- ตรวจทุกคู่สำหรับ overlap และแยก contact/coupling interface ที่ประกาศออกจาก forbidden pair
- ตรวจ motion envelope ของ Work 083, เส้นทางถอด energy store, routing clearance, bend-radius declaration, ground clearance และ external envelope
- ปิด force/moment ledger ของ acceleration, braking, cornering, combined, bump และ torque reaction ที่ `1e-5`; ปิด energy/thermal ledger ที่ `1e-4`
- ผูก component structural case กับผล Work 086 `ec818c21ea45f4a129f762bac3130e06628c7b560bb1d74dff8a8c9555cdf827`
- รัน disconnected mount, blocked service path, routing collision, inadequate rejection, asymmetric load, weakened mount, thin-frame, mirror และ replay controls

## ไฟล์ที่วางแผนแก้ไข

- `config/candidates/load_structure_integration_001.json`
- `src/formula_ultimate/subsystems/load_structure_integration.py`
- `scripts/candidates/build_load_structure_integration_001.py`
- `scripts/candidates/inspect_load_structure_integration_freecad.py`
- `tests/test_load_structure_integration_001.py`
- `docs/contracts/LOAD_STRUCTURE_INTEGRATION_001.md` และไฟล์คู่ภาษาไทย
- plan/result นี้และไฟล์คู่ภาษาไทย
- หลักฐานที่ ignore ภายใต้ `artifacts/work087/`

## Validation และ gate

- Upstream hash exact, valid solid แยกสิบเจ็ดชิ้น, ไม่มี forbidden overlap เกิน `1e-12 m3`, forbidden clearance `>=0.5 mm`, routing/service clearance `>=2 mm` และ ground clearance `>=5 mm`
- มวล/COM/inertia จากรูปทรงและ exact replay
- force/moment residual `<=1e-5`; energy/thermal residual `<=1e-4`
- Control ทุกตัวทำให้เกิดผล rejection/degraded/`DNF` ตาม preregistration
- Focused, repository-contract, compilation และ full regression test ผ่าน

## สิ่งที่ไม่ทำและเงื่อนไขหยุด

ไม่อ้าง chassis, monocoque, crashworthiness, fatigue, physical thermal, production, safety หรือ physical validation ห้ามเรียก Gate C ว่า complete หากไม่มี meshed convergence evidence ของ load frame ใหม่หรือ design-eligible material/process evidence หยุดหรือคืน `Partial` เมื่อ identity หาย, มีการปิดบัง overlap, service path ถูกบล็อก, ทิ้ง heat/load, control ไม่เกิดผลเชิงสาเหตุ หรือ replay ไม่ตรง
