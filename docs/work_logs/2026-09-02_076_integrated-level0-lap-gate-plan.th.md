# แผน Work 076: Gate หนึ่งรอบแบบ Closed Loop ระดับ Level 0 ที่รวมระบบ

สถานะ: กำลังดำเนินการ (In progress)

แปลจากไฟล์ภาษาอังกฤษ: `2026-09-02_076_integrated-level0-lap-gate-plan.md`

## วัตถุประสงค์และขอบเขต

รวม controller Work 074, linkage transform Work 075, vertical tyre/road dynamics Work 073 และ drivetrain/planar plant เดิมเป็นการทดลองหนึ่งรอบสังเคราะห์แบบ deterministic Gate ต้องบังคับ centreline progress, corridor containment, contact เป็นบวก, suspension travel อยู่ในขอบเขต, energy closure และ finish event ที่ตรงพอดี

นี่เป็น integration gate หนึ่งรอบสังเคราะห์ระดับ Level 0 ไม่ใช่รอบสนามจริง การ optimize lap time, safety validation หรือหลักฐานว่ารถจริงครบถ้วน

## การออกแบบการทดลอง

- ตัวแปรอิสระ: controller gains, linkage geometry, curvature/direction/width, time step, energy/throttle และ fault ของ steering/contact
- ตัวแปรตาม: finish time/progress, tracking error สูงสุด/สุดท้าย, steering saturation, tyre load, travel/body mode, energy/residual สูงสุด, เหตุหยุด และ hash deterministic
- ตัวควบคุม: exact replay, mirror lap ทิศตรงข้าม, open-loop departure, corridor แคบ, contact-loss road input, linkage degeneracy, energy depletion/timeout เมื่อทำได้ และ half-step refinement บนช่วงสั้นที่จับคู่กัน
- สมมติฐานหลัก: candidate ที่เลือกจบ analytical closed loop หนึ่งรอบพอดี โดยอยู่ใน corridor และ physical gates; control ต้องล้มเหลวด้วยสาเหตุที่ประกาศ
- การหักล้าง: ให้ progress โดยไม่มี spatial motion, จบด้วยระยะอย่างเดียว, จบนอก corridor, clip contact/travel, ซ่อน saturation, สร้างพลังงาน, identity drift, first failure ผิด หรือ replay ไม่ตรง

## ไฟล์ที่วางแผน

- `config/vehicle/integrated_level0_lap_gate_v1.json`
- `src/formula_ultimate/simulation/integrated_lap_gate.py`
- simulation exports, runner, tests และเอกสารวิจัย/ผลสองภาษา
- หลักฐานที่ ignore ใต้ `artifacts/work076/`

## การตรวจสอบและเกณฑ์สำเร็จ

Reference ต้องถึงความยาว corridor หนึ่งรอบด้วย finish distance ที่ localize ตรง อยู่ภายในความกว้างหลังหัก vehicle-envelope allowance รักษา normal load เป็นบวกและ travel ต่ำกว่าขีดจำกัด พร้อมผ่าน equation/energy tolerance ทั้งหมด Mirror/replay identities, DNF controls ที่มีเหตุ, upstream hashes Work 074/075, focused/full tests, compilation, bilingual contract, scoped commit และ post-commit replay ต้องผ่าน Numerical หรือ physical failure ใดต้องห้าม finish claim

## ความเสี่ยงและสิ่งที่ไม่ทำ

วงกลม analytical และถนนสังเคราะห์ไม่ใช่ข้อมูลสนามจริง แบบจำลองไม่รวม braking zone, variable speed, aerodynamic load, thermal limit ระยะการแข่งขัน, tyre relaxation/contact แบบละเอียด, driver/traffic, barrier, weather, structural-load coupling และ linkage CAD จริง Gate ที่ผ่านอนุญาตเพียง fidelity ขั้นถัดไป
