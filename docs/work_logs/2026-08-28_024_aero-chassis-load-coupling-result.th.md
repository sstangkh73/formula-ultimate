# ผลลัพธ์ Work 024: Aerodynamic Chassis และ Normal-Load Coupling

ต้นฉบับภาษาอังกฤษ: `2026-08-28_024_aero-chassis-load-coupling-result.md`

สถานะ: Completed

## ผลลัพธ์

Work 024 เปลี่ยน typed weather/motion เป็นผล Work 017 aerodynamic, translate
force/moment และ cooling evidence มาที่ chassis centre of mass และ balance normal
load บน contact topology ใดก็ได้ Adapter สองตัว emit signal ตรงและ fail-closed
เมื่อ map/load invalid

## ไฟล์และการตัดสินใจ

- เพิ่ม `aero_load_coupling.py`, export, focused test 10 รายการ, validator และ
  เอกสาร model/plan/result สองภาษา
- อัปเดต Work 023 weather contract/validator ให้บังคับ wind `local_enu`
- ใช้ body axis `x` หน้า, `y` ซ้าย, `z` ขึ้น และ `M_com=M_map+r x F`
- Generalize vertical/pitch/roll equilibrium โดยไม่ clip negative load
- เก็บ raw residual และ numerical node-snap evidence ที่ตรวจได้
- รักษา topology neutrality; analytical three/four-contact ผ่าน

## ปัญหาที่แก้

รายงานสองภาษาแยกครอบคลุม wind coordinate frame ที่หาย, exact-node roundoff หลัง
ENU rotation และ fixture สาม contact ที่ปัดเศษจนไม่สมดุล ทั้งหมดแก้ก่อนปิดงาน

## Validation

```powershell
python -m unittest tests.test_aero_load_coupling -v
# exit 0; Ran 10 tests in 0.003s; OK
python -m unittest discover -s tests -v
# exit 0; Ran 196 tests in 1.607s; OK
python scripts/validate_aero_load_coupling.py
# exit 0; drag -525.9915 N; downforce -1051.9830 N
# front 2978.4915 N ต่อจุด; rear 2452.5 N ต่อจุด
# residual ผ่าน; outside map invalid พร้อม 0 writes
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
```

## Review และข้อจำกัด

Evidence รองรับ sign, moment translation, load shift, conservation closure,
replay, topology neutrality และ invalid boundary แต่ synthetic map/weather เป็น
alternative explanation ของผลสะอาด จึงไม่อ้าง real aero accuracy ยังขาด
acceleration feedback, contact force, suspension/brake และ motion Work 025 ถัดไป
ไม่มีการ push
