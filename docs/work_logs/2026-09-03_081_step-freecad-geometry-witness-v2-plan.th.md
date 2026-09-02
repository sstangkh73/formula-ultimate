# แผน Work 081: STEP to FreeCAD Geometry Witness V2

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-03_081_step-freecad-geometry-witness-v2-plan.md`

## วัตถุประสงค์และขอบเขต

นำ canonical STEP ที่แน่นอนทั้งห้าชิ้นจาก Work 078 เข้า FreeCAD 1.1 อย่างอิสระโดยไม่ heal หรือแทนเรขาคณิต แล้วสร้าง geometry witness หน่วย SI แบบ deterministic สำหรับ topology, volume, bounding box, centre of mass, full inertia tensor, principal moments/axes, circular-feature signature และ semantic interface ที่ค้นได้แบบ unique เปรียบเทียบค่าที่ FreeCAD วัดกับบันทึก exporter ของ CadQuery ที่ freeze และผูกผลทุกตัวกับไบต์ STEP ที่แน่นอน

Work 081 จะสร้าง artifact Work 078 ที่ freeze ซ้ำด้วย pinned CadQuery environment ลงใน `artifacts/work081/source_step/` ซึ่งถูก ignore ตรวจ SHA-256 กับค่าที่ preregister จากนั้นเรียก FreeCAD เป็น process แยก นี่เป็นเส้นทาง import/measurement อิสระ แต่ยังจัดเป็น `toolchain_cross_check` เพราะ CadQuery และ FreeCAD อาจใช้เทคโนโลยี OCCT ร่วมกัน

## การออกแบบการทดลอง

- ตัวแปรอิสระ: canonical part family, ไบต์ STEP ที่แน่นอน, เส้นทางวัด, geometric signature ของ interface, ลำดับ mapping key และการกลายพันธุ์ hash/topology/signature/ค่าคาดหมายโดยเจตนา
- ตัวแปรตาม: STEP SHA-256, จำนวน shape/solid, validity, volume, bounding box, centre of mass, inertia tensor, principal properties, จำนวน/ตำแหน่ง/แกน/เส้นผ่านศูนย์กลาง interface วงกลมที่ค้นได้, residual เทียบ exporter ที่ freeze และ canonical report identity
- ตัวควบคุม: ชิ้นส่วน Work 078 ทั้งห้า; key-order replay; ไบต์ STEP เปลี่ยน; expected hash ผิด; solid เกิน/หาย; circular signature กำกวมหรือหาย; expected volume เปลี่ยน; invalid/no-repair flag; และการรัน FreeCAD ซ้ำ
- สมมติฐานที่ต้องการ: artifact ที่แน่นอนให้ valid solid ที่ไม่ repair หนึ่งก้อนต่อชิ้น, global properties ที่เทียบตรงกันเห็นพ้องภายใน relative `1e-6`, interface signature ที่จำเป็นถูกค้นแบบ unique โดยไม่ใช้ face number และการรันซ้ำให้ canonical report identity ตรงกัน
- การหักล้าง: ยอมรับไบต์ที่เปลี่ยน, ซ่อม geometry ผิด, ใช้ face index, คัดลอก expected value แทนการวัด, ซ่อนการวัดที่ไม่รองรับ หรือ result identity เปลี่ยนเมื่อสลับ mapping key

## ไฟล์ที่วางแผน

- `config/cad/step_freecad_geometry_witness_v2.json`
- `src/formula_ultimate/components/geometry_witness.py`
- `scripts/cad/inspect_geometry_witness_v2_freecad.py`
- `scripts/cad/compare_geometry_witness_v2.py`
- `tests/test_geometry_witness_v2.py`
- `docs/contracts/STEP_FREECAD_GEOMETRY_WITNESS_V2.md` และไฟล์ภาษาไทย
- ไฟล์ผล Work 081 ที่เข้าคู่กัน
- หลักฐานที่ ignore ใต้ `artifacts/work081/`

fixture material/process ของ Work 079 จะยังเป็น synthetic เว้นแต่ค่าที่วัดจริงของ bracket จะตอบ schema witness ได้ครบ Work 081 จะไม่เปลี่ยนชื่อ measurement ที่ไม่รองรับให้เป็นหลักฐานอิสระ

## การตรวจสอบและเกณฑ์สำเร็จ

- exact STEP hash ตรงกับ hash ที่ freeze จาก Work 078 ครบห้าชิ้น;
- FreeCAD รายงาน valid solid หนึ่งก้อน, positive finite SI volume, bounds/centre/inertia finite และ `hidden_geometry_repair=false` ทุกชิ้น;
- relative residual ของ FreeCAD/CadQuery volume และ bounding box ที่เทียบโดยตรง `<=1e-6`;
- circular interface signature ที่ตั้งค่าถูกค้นแบบ unique ด้วยชนิด geometry, radius, centre และ axis tolerance ไม่ใช้ face number;
- config ผิดและ mutation ของ hash/value/signature/topology fail closed ด้วย causal code;
- FreeCAD report สองรอบและ comparison สองรอบ replay ตรงกันแบบ exact;
- focused tests, repository-contract tests, compilation และ full regression ผ่านก่อน commit ที่จำกัด scope

## ความเสี่ยงและสิ่งที่ไม่อ้าง

FreeCAD และ CadQuery อาจใช้ OCCT ร่วมกัน ดังนั้นความตรงกันไม่ใช่ physical validation STEP ไม่เก็บชื่อ causal feature; V2 จึงรองรับเฉพาะ geometric signature ที่วัดได้และรายงาน wall/section/clearance ที่ไม่รองรับอย่างชัดเจน ค่า minimum wall thickness แบบ arbitrary, torsion constant, exact part-to-part interference, clearance ของ assembly ที่เคลื่อนที่, manufacturing capability, material allowable, strength, fatigue, safety และ production approval ไม่อยู่ในขอบเขต หาก interface ใดค้นแบบ unique โดยไม่ใช้ face index ไม่ได้ หรือ exact bytes replay ไม่ได้ Work 081 จะหยุดแทนการผ่อน gate
