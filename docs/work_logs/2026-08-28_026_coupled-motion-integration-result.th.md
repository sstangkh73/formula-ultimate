# ผลงาน 026: การอินทิเกรตการเคลื่อนที่แบบ coupled

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-28_026_coupled-motion-integration-result.md`

## ผลลัพธ์

สร้าง motion adapter บนระนาบระดับ Level 0 แบบ deterministic ซึ่งรวม aerodynamic/contact wrench, อัปเดต horizontal velocity, yaw, ตำแหน่ง เวลา และ race distance ตามแนวสัมผัส corridor พร้อม fail closed เมื่อ residual หรือ corridor ผิดพลาด

## ไฟล์ที่เปลี่ยน

- เพิ่ม architecture v2 แบบมี version พร้อม dependency จาก corridor ไป motion
- เพิ่ม `motion_coupling.py`, public export, unit test 12 รายการ และ validator แยก
- เพิ่มเอกสารโมเดล รายงานปัญหาสองเรื่อง แผน/ผล และสถานะคิวแบบสองภาษา

## การตัดสินใจ

- เก็บ architecture v1 เดิมและเพิ่ม v2 แทนการแก้หลักฐานประวัติย้อนหลัง
- ใช้ force orientation ที่ midpoint, ตำแหน่งแบบ trapezoidal และการอินทิเกรต yaw acceleration คงที่แบบ exact
- ให้ race-distance credit เฉพาะ displacement บวกตามแนวสัมผัส corridor และเก็บ reverse displacement เป็น uncredited evidence
- ปฏิเสธ corridor departure แทนการ project รถกลับเข้าด้านใน
- รักษาการเคลื่อนที่แนวดิ่งแบบ constant velocity ที่สังเกตได้ และไม่บังคับ grade constraint แบบซ่อนโดยไม่มีโมเดลแรง/constraint แนวดิ่ง

## ปัญหาที่แก้

1. `2026-08-28_026_motion-missing-corridor-signal.md`: architecture v1 route typed corridor evidence ไป motion ไม่ได้ แก้ใน v2
2. `2026-08-28_026_motion-vertical-projection.md`: ร่างแรกอาจลบ vertical offset และภายหลังพบ `z`/`v_z` ไม่สอดคล้อง แก้ด้วย constant-velocity vertical kinematics และ residual `motion.kinematic-z`

## คำสั่งตรวจสอบและหลักฐาน

คำสั่งทั้งหมดด้านล่างคืน exit status `0`:

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_motion_coupling
python -m unittest discover -s tests
python scripts/validate_motion_coupling.py
python -m compileall -q src scripts tests
git diff --check
```

หลักฐาน:

- focused tests: ผ่าน 12 รายการใน `0.005 s`
- full suite: ผ่าน 219 รายการในการรันสุดท้าย `0.373 s`
- validator: exit `0`
- bytecode compilation: exit `0`
- unstaged diff check: exit `0`
- architecture fingerprint: `a989fa92bc9eb1bcf83127b572cb2c33b99a802458211dbe4442fa9046c0f5fe`
- straight fixture: `(12, 0, 0) m/s`, `(11, 0, 0) m`, race distance `11 m`, residual เก้ารายการผ่าน
- refinement: error `0.08383245221108916 m` เมื่อ `dt = 1.0 s`, `0.00019773501705859235 m` เมื่อ `dt = 0.05 s`, reduction ratio `423.96361280940005`
- lateral-only credited progress `0 m`; reverse raw/credited/uncredited เท่ากับ `-2/0/2 m`
- corridor departure และ spatial evidence ที่หาย: `invalid`, output ศูนย์
- deterministic replay: `true`

## ข้อจำกัด

- เป็น analytical verification ระดับ Level 0 เท่านั้น ไม่ใช่ calibrated หรือ physical validation
- local body-width corridor gate ยังไม่ sweep corner ของรถเมื่อ yaw, ความยาว, overhang, barrier หรือ kerb
- profile จริงทั้งสิบสนามยังไม่มี surveyed local 3D corridor evidence สำหรับ admission
- grade และ bank ยังไม่สร้าง constraint force; vertical dynamics อยู่นอก Work 026
- energy, thermal, damage, degradation, reliability และ final state arbitration เป็นงาน Work 027 เป็นต้นไป

## งานต่อเนื่อง

Work 027 ควรรวม contact energy transfer, aerodynamic cooling, component thermal/degradation/damage state และ deterministic reliability/event evidence ก่อน transaction เผยแพร่ final next state
