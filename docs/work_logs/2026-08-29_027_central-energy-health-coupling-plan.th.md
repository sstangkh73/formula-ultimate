# แผนงาน 027: การ coupling พลังงานกลางและ health state

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_027_central-energy-health-coupling-plan.md`

## วัตถุประสงค์

เชื่อม contact energy transfer และ health input จาก Work 025 กับ aerodynamic cooling จาก Work 024 ให้เป็นการอัปเดต central energy, thermal, degradation, damage และ seeded reliability แบบ deterministic หนึ่งชุด โดยเหตุการณ์ทางฟิสิกส์ที่เกิดก่อนสุดต้องตัดปริมาณที่เกี่ยวข้องทั้งหมด ณ executed duration เดียวกัน

## ขอบเขต

- นิยาม central-energy และ component-health configuration/evidence แบบ typed
- audit primary use, recovered energy, conversion loss, mechanical heat, thermal storage และ heat rejection โดยไม่แก้แบบซ่อน
- อัปเดต `SharedVehicleState.primary_energy_j`, `recovered_energy_j` และ component health
- ใช้ thermal derating, degradation, damage และ seeded reliability hazard พร้อม event candidate ที่ชัดเจน
- เลือกเหตุการณ์ energy, thermal, degradation, damage, suspension หรือ reliability ที่เกิดก่อนสุดด้วย tie handling แบบ deterministic
- ตัด transfer และ state increment ทั้งหมดให้ใช้ event time เดียวกัน
- เพิ่ม adapter contract สำหรับ `energy_graph_audit` และ `health_event_solver` พร้อม health candidate ที่ merge แล้ว
- version coupling architecture หาก signal dependency ที่ประกาศอยู่ไม่พอสำหรับ merge state ที่สอดคล้อง
- เขียนรายงานปัญหาสองภาษาแยกทุกบั๊กที่พบและแก้ให้เสร็จก่อนปิดงาน

## ไฟล์ที่วางแผน

- `src/formula_ultimate/simulation/energy_health_coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_energy_health_coupling.py`
- `scripts/validate_energy_health_coupling.py`
- `docs/simulation/CENTRAL_ENERGY_HEALTH_COUPLING.md`
- `docs/simulation/CENTRAL_ENERGY_HEALTH_COUPLING.th.md`
- coupling architecture แบบมี version หากจำเป็น
- problem report ของ Work 027 หากจำเป็น
- implementation queue, แผนนี้ และบันทึกผลสองภาษาที่เข้าคู่

## นิยามการทดลอง

- ตัวแปรอิสระ: primary draw, regenerative return, brake heat, aerodynamic cooling, heat generation ของ component, อัตรา degradation/damage, reliability hazard, seed และ duration
- ตัวแปรตาม: executed duration, energy store, อุณหภูมิ component, degradation, damage, failure flag, derating, residual และ event candidate
- ตัวควบคุม: start state, component ID, thermal parameter, hazard law, random seed, draw index, event priority และ tolerance
- เมตริก: central energy residual, thermal residual, ความสอดคล้องของ event time, scaling ของ state increment, replay equality และจำนวน output เมื่อ invalid
- เกณฑ์สำเร็จ: typed transfer ปิดสมดุล; same-seed replay ตรง exact; recovery ไม่เกินค่าที่ประกาศ; cooling ไม่ถูกนับซ้ำ; earliest event ตัด candidate ทุกชุดสอดคล้องกัน; audit invalid เขียน candidate signal ศูนย์
- เกณฑ์ล้มเหลว: พลังงานเกิดหรือหายโดยไม่มี evidence; failure ที่ช้ากว่าแทนที่เหตุการณ์ก่อนหน้า; thermal/degradation/damage เดินเกิน event; stochastic draw ขึ้นกับ registration order; หรือ evidence ที่ fail ถูกแก้แบบซ่อน
- การพยายามหักล้าง: ใส่ hidden energy, recovery เกิน, cooling over-credit, component ID/time ไม่ตรง, exact event tie, seed ต่างกัน และ failure ก่อนปลาย step

## การตรวจสอบ

1. test เฉพาะ Work 027
2. test suite ทั้ง repository
3. validator แยกของ Work 027
4. compile Python bytecode
5. `git diff --check` และ `git diff --cached --check`
6. ตรวจ staged scope แบบระบุไฟล์ก่อน commit

## เกณฑ์สำเร็จ

- central energy และ component ทุกตัวที่ configure อัปเดตจาก typed evidence ที่ประกาศเท่านั้น
- conservation residual ผ่านและสังเกตได้
- recovery, heat, cooling, derating, degradation, damage และ seeded reliability ถูกแทนค่า
- earliest-event truncation ใช้ร่วมกันกับ state change ทุกส่วนที่เกี่ยวข้อง
- บันทึกอังกฤษและไทยตรงกันด้านสมการ หน่วย คำสั่ง หลักฐาน และข้อจำกัด
- commit Work 027 เป็น validated commit หนึ่งรายการก่อนเริ่ม Work 028

## ความเสี่ยง

- architecture ปัจจุบันแยก energy กับ health candidate และอาจขาด signal ที่จำเป็นสำหรับ merge ที่สอดคล้อง
- brake thermal state ราย contact กับ central component thermal stateอาจนับ heat เดียวกันซ้ำหาก ownership ไม่ชัด
- seeded reliability draw อาจขึ้นกับลำดับ component หากไม่มี stream deterministic ราย component
- cooling evidence เป็น capacity และห้ามถือเป็น heat rejection ที่รับประกันเกิน thermal law

## สิ่งที่ไม่ทำโดยชัดแจ้ง

- ไม่ทำ whole-race loop หรือ telemetry orchestration ของ Work 028
- ไม่อ้าง calibrated reliability, material fatigue, CFD cooling, battery chemistry หรือ physical validation
- ไม่ clip energy/temperature, ล้าง failure หรือแก้ event time แบบซ่อน
- ไม่ optimize รถหรือทำ campaign สิบสนาม
