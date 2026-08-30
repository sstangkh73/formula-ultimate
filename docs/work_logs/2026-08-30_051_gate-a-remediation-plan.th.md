# แผนงาน 051: การแก้ Gate A ด้าน Element และ Boundary

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_051_gate-a-remediation-plan.md`

## วัตถุประสงค์

แก้หรือกำหนดขอบเขต blocker ของ Gate A ที่เก็บไว้สองรายการก่อน Work 046 ได้แก่ disagreement ระหว่าง C3D4/C3D10 ใกล้ critical ของ Work 041 และการ reject support-boundary transferability ของ Work 045

## ขอบเขตและขอบเขตการอ้างผล

งานนี้จะรัน remediation study ที่มี solver รองรับสองชุดบน synthetic fixture เดิม อาจ admit evaluation domain ที่แคบลงเมื่อหลักฐานรองรับ แต่จะไม่เขียนทับผล reject ของ Work 041 หรือ Work 045 งานนี้ไม่ validate post-buckling response, joint จริง, contact, material allowable, รถทั้งคัน หรือ hardware จริง

## การออกแบบการทดลอง

### การแก้ element family

- ตัวแปรอิสระ: characteristic mesh size ของ C3D10 และ absolute precritical load
- ตัวแปรตาม: eigenvalue load, nonlinear amplification, last-two refinement change, analytical secant error, reaction, solver status, mesh size และ evidence hash
- ตัวแปรควบคุม: geometry, material, imperfection field, load schedule, end-face loading, solver และ parser จาก Work 041
- สมมติฐานที่ต้องการ: C3D10 refinement series ที่ preregister ไว้ converge ไม่เกิน `5%` ในทุก admitted load และต่างจาก analytical precritical secant reference ไม่เกิน `5%`
- เกณฑ์ล้มเหลว: solve หาย/non-finite, mode family เปลี่ยน, last-two change เกิน `5%` หรือ secant error เกิน `5%` ให้ reject เส้นทาง C3D10
- กฎกำหนดขอบเขต: C3D4 ยังห้ามใช้ promote near-critical ในช่วงที่ Work 041 พบ cross-family difference เกิน `5%`; ห้ามเฉลี่ยหรือแก้เงียบ

### การแก้ boundary domain

- ตัวแปรอิสระ: support topology identity และ support representation identity
- ตัวแปรตาม: topology signature, admitted-comparison status, compliance change, force/moment/energy residual, และ load share
- ตัวแปรควบคุม: STEP geometry, material, load interface, load, fine mesh, solver และ result parser จาก Work 045
- สมมติฐานที่ต้องการ: encoding ที่เทียบเท่ากันของ two-support topology เดิม replay ตรงกันภายใน numerical tolerance ส่วนการลบ support ต้องถูกจัดเป็น topology mutation และห้ามใช้เป็นหลักฐาน representation transferability
- เกณฑ์ล้มเหลว: representation-only mutation เปลี่ยน topology signature หรือ response เกิน tolerance หรือ support set ที่เปลี่ยนถูก admit เงียบว่าเป็น topology เดิม
- กฎกำหนดขอบเขต: ผล one-support ของ Work 045 ยังคงเป็นหลักฐานขัดแย้งต่อการ transfer ไป support topology อื่น การใช้กับ structural fitness ที่ admit ได้ต้องจำกัดอยู่ที่ support topology และ boundary-model identity ที่ประกาศตรงกัน

## ไฟล์ที่วางแผน

- `config/structural/gate_a_remediation_v1.json`
- `src/formula_ultimate/structural/gate_a_remediation.py` และ package exports
- `scripts/structural/run_gate_a_remediation.py`
- `scripts/run_work051.ps1`
- `tests/test_gate_a_remediation.py`
- `docs/physics/GATE_A_ELEMENT_BOUNDARY_REMEDIATION.md` และ `.th.md`
- result record สองภาษาของ Work 051
- ignored evidence ใต้ `artifacts/work051/`

## การตรวจสอบ

รัน focused unit tests, การทดลอง Work 051 แบบ deterministic, regression ของ Work 041 และ Work 045, full repository suite, Python compilation, repository-contract checks, staged-diff checks, explicit scoped commit และ clean-tree replay

## เกณฑ์ความสำเร็จ

- Experiment และ negative control ทุกกรณี fail closed เมื่อ identity หรือ evidence ไม่ถูกต้อง
- Element study ต้องรองรับ C3D10 convergence หรือคง Gate A เป็น blocked พร้อมหลักฐานที่ชัดเจน
- Boundary study ต้องแยก representation change ออกจาก topology change และรายงานทั้งคู่โดยไม่ลบผล reject ของ Work 045
- Machine-readable decision ต้องระบุว่า Gate A ปิด, ถูกกำหนดขอบเขตแบบแคบ หรือยัง blocked และ Work 046 เริ่มได้หรือไม่

## ความเสี่ยง

Refined quadratic mesh อาจเกิน practical compute budget การใช้ exact support-topology identity contract กำหนดขอบเขตหลักฐานได้ แต่พิสูจน์ contact, preload, friction หรือ arbitrary-joint transfer ไม่ได้ Analytical secant agreement ไม่ใช่ independent physical validation

## สิ่งที่ไม่ทำอย่างชัดเจน

ไม่รวม Work 046 failure coupling, whole-vehicle CAD, whole-vehicle load case, design search, post-buckling capacity, real-material certification, push หรือ publication
