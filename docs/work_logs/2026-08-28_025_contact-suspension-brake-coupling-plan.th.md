# แผน Work 025: Contact, Suspension, Brake และ Regeneration Coupling

ต้นฉบับภาษาอังกฤษ: `2026-08-28_025_contact-suspension-brake-coupling-plan.md`

สถานะ: Completed

## วัตถุประสงค์

Resolve ground contact รูปแบบใดก็ได้จาก normal load Work 024 ผ่าน explicit
drive/brake allocation, suspension travel, mechanical braking, regeneration และ
combined tyre ellipse พร้อมเก็บ requested, applied, unserved, heat และ energy โดย
ไม่ redistribute เงียบ

## ขอบเขต

- กำหนด topology-neutral contact coupling spec และ allocation weight ตรงจริง
- Reject contact-ID mismatch, state หาย/ซ้ำ, wheel speed ลบ, throttle/brake ชนกัน
  และ allocation sum ที่ไม่ปิด
- Evaluate Work 018 suspension/brake/regen model เดิมต่อ contact
- จำกัด regen ด้วย central recovery request ก่อน mechanical allocation
- Resolve combined longitudinal/lateral tyre capacity ต่อ contact
- Emit typed `contact.force_moment`, `contact.energy_transfers` และ
  `contact.health_inputs` พร้อม raw residual/failure evidence
- พิสูจน์ three/four-contact, saturation, zero recovery, storage/power limit,
  replay, no redistribution และ adapter failure
- เพิ่ม test, validator, เอกสาร/result สองภาษา, bug report, validation, commit

## นิยามการทดลอง

- สมมติฐาน: explicit per-contact allocation กับ independent capacity model ปิด
  torque/energy accounting ได้โดยไม่โยก unmet demand
- Independent variables: topology, load, command, wheel speed, subsystem
  state/parameter, allocation weight, recovery fraction และ tyre capacity
- Dependent variables: contact force/moment, travel/failure, recovered energy,
  heat/loss, unserved demand, saturation, residual และ adapter status
- Controls: Work 011 tyre ellipse, Work 018 suspension/brake model, Work 024
  contact load, immutable start state และ exact signal contract
- Success: per-contact/summed evidence ปิด; demand ที่ขาดยัง unserved;
  three-contact ผ่าน; invalidity ที่ inject มี write ศูนย์
- Failure: redistribute เงียบ, นับ braking/regen ซ้ำ, load mismatch, failure event
  หาย, residual ถูกแก้, บังคับ topology หรือ commit fail

## ความเสี่ยงและสิ่งที่ไม่ทำ

Adapter Level 0 นี้ใช้ control allocation และ subsystem state ที่ประกาศ ไม่ใช่
optimal controller หรือ calibrated tyre/suspension Work 026 เป็นเจ้าของ motion
integration ไม่มี whole race, optimizer, physical validation, README change หรือ
remote push

## Validation

```powershell
python -m unittest tests.test_contact_coupling -v
python -m unittest discover -s tests -v
python scripts/validate_contact_coupling.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```
