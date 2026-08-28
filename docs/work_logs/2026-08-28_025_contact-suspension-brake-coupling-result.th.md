# ผลลัพธ์ Work 025: Contact, Suspension, Brake และ Regeneration Coupling

ต้นฉบับภาษาอังกฤษ: `2026-08-28_025_contact-suspension-brake-coupling-result.md`

สถานะ: Completed

## ผลลัพธ์

Work 025 couple arbitrary contact load เข้ากับ explicit drive/brake allocation,
suspension, mechanical braking, regeneration, combined tyre capacity, body force
และ yaw moment โดย requested/applied/unserved, energy, heat, travel, failure และ
residual อยู่ราย contact และไม่ redistribute เงียบ

## ไฟล์และการตัดสินใจ

- เพิ่ม `contact_coupling.py`, public export, focused test 11 รายการ, validator
  และเอกสาร model/plan/result สองภาษา
- Allocation fraction ต้องปิดแยกสำหรับ drive และ brake
- Central recovery fraction cap regen ก่อน mechanical allocation
- Combined brake/steer saturation ใช้ subsystem evaluation สอง pass เพื่อให้
  thermal/energy evidence ตรง road-transmitted torque
- Physical contact failure เก็บเป็น health evidence; malformed/conservation-
  invalid input emit signal ศูนย์แบบ atomic
- Three/four-contact ผ่านโดยไม่บังคับ axle topology

## ปัญหาที่แก้

Implementation แรกนับ brake/regen energy เกินหลัง combined tyre ellipse ลด
longitudinal force รายงานสองภาษาแยกบันทึกและแก้ด้วย two-pass แล้ว Regression ปิด
applied force, torque, angular speed, duration และ wheel energy ต่อ contact

## Validation

```powershell
python -m unittest tests.test_contact_coupling -v
# exit 0; Ran 11 tests in 0.005s; OK
python -m unittest discover -s tests -v
# exit 0; Ran 207 tests in 0.368s; OK
python scripts/validate_contact_coupling.py
# exit 0; 3 contacts; replay equal; residual 9 ตัวผ่าน
# requested drive 3000 N; applied 2100 N; front unserved 900 N
# brake wheel energy 85.3178 J; recovered 68.2542 J
# energy/force consistency ต่อ contact true; redistribution false
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
```

## Review และข้อจำกัด

Evidence รองรับ explicit allocation, saturation, no redistribution, energy
closure, failure retention, replay และ topology neutrality แต่ยังเป็น
reduced-order tyre/suspension/brake fixture ไม่ใช่ calibration Subsystem state ยัง
ไม่ central commit และ summed force ยังไม่ advance motion Work 026 รับผิดชอบ
integration นี้ ไม่มีการ push
