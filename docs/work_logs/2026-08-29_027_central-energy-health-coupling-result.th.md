# ผลงาน 027: การ coupling พลังงานกลางและ health state

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_027_central-energy-health-coupling-result.md`

## ผลลัพธ์

สร้างการบัญชี propulsion/recovery energy ส่วนกลาง, independent audit, การอัปเดต component thermal/degradation/damage, deterministic reliability stream, persistent contact state และ earliest-event localization

## ไฟล์ที่เปลี่ยน

- เพิ่ม architecture v3, source ของ central energy/health, focused test 12 รายการ, validator และเอกสารโมเดลสองภาษา
- ขยาย shared contact state และ contract ด้าน energy/event ของ Work 025
- เพิ่ม problem report สองภาษาหกเรื่องสำหรับทุก defect ที่พบใน Work 027

## ปัญหาที่แก้

1. ขาด drive-wheel energy transfer
2. contact subsystem state ไม่คงอยู่
3. peer contact ไม่ถูกตัด ณ contact failure ที่เร็วสุด
4. health stage ขาด energy/motion input
5. ค่า thermal ambient `300 K` แบบซ่อน
6. validator สมมติว่า seed ต่างทุกครั้งต้องเปลี่ยนเวลาเหตุการณ์ที่ชนะ

## การตัดสินใจ

- เก็บ architecture v1/v2 และเพิ่ม v3
- ใช้ recovered energy ก่อน primary energy และปฏิเสธ capacity overflow
- audit drive, auxiliary และ recovery boundary แยกอิสระ
- เก็บ brake heat ใน contact model เพื่อป้องกันการนับซ้ำ
- สร้าง reliability stream จาก seed, step index และ component ID
- เมื่อ central terminal event เกิดก่อน ให้รักษา contact state เริ่มต้นแทนการ interpolate ที่สร้างขึ้นเอง

## คำสั่งและหลักฐาน validation

คำสั่งทั้งหมดคืน exit status `0`:

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_contact_coupling tests.test_energy_health_coupling
python -m unittest discover -s tests
python scripts/validate_energy_health_coupling.py
python -m compileall -q src scripts tests
git diff --check
```

- focused regression Work 025/027: ผ่าน 24 รายการใน `0.015 s`
- test suite ทั้ง repository: ผ่าน 232 รายการใน `0.622 s`
- validator exit `0`
- architecture fingerprint: `a3782a246e27997984ece4afc1c2f7b0924d8b9e67e602bb46889399ba565a38`
- primary จาก drive/aux: `2000 J -> 900 J` พร้อม residual ผ่านทั้งหมด
- recovery boundary: `1000 = 700 + 100 + 200 J`, residual `0 J`
- depletion time: `0.5 s`, primary สุดท้าย `0 J`
- thermal winner: `0.2 s`, `302 K`, localize `x = 2 m`
- same-seed replay ตรง exact และ seed ต่างเปลี่ยน reliability draw

## ข้อจำกัด

เป็น Level 0 เท่านั้น ไม่มี calibrated reliability, CFD cooling, battery chemistry, material fatigue, full 3D contact constraint หรือ physical validation Work 028 ต้องส่ง environment/configuration ชัดเจนและหยุด terminal state

## งานต่อเนื่อง

Work 028 จะสร้าง deterministic whole-race coupled transaction loop, final race-progress merge, terminal outcome และ replay/provenance telemetry
