# รายงานปัญหา Work 017: Exact Assertion ของ Interpolation Fraction

ต้นฉบับภาษาอังกฤษ: `2026-08-28_017_interpolation-fraction-exact-assertion.md`

สถานะ: Resolved

## ปัญหา

การรัน test Work 017 ครั้งแรกผ่าน 10 และ fail interior interpolation test เพราะ
เปรียบเทียบ fraction แบบ binary floating-point ที่คำนวณกับเลขทศนิยม `0.5` ด้วย
exact equality:

```text
AssertionError: 0.5 != 0.4999999999999999
Ran 11 tests
FAILED (failures=1)
```

ช่วง ride height คือ `[0.04, 0.08]` และ query คือ `0.06`; fraction ทางคณิตศาสตร์
เท่ากับครึ่งหนึ่ง exact แต่ decimal input แทนใน binary floating-point ไม่ได้ exact
จึงต่างจากค่าคาดประมาณ `1.11e-16`

## ผลกระทบ

Assertion ของ coefficient interpolation ผ่าน นี่เป็น defect ของ test assertion
ไม่ใช่หลักฐานว่า bracket, coefficient, force, moment หรือ cooling result ผิด

## การแก้ไข

Test ใช้ `assertAlmostEqual` กับ interpolation fraction ทั้งสาม โดยยังคง exact
equality สำหรับ grid-node identity และ deterministic replay

## Validation

```powershell
python -m unittest tests.test_aerodynamics -v
python scripts/validate_aerodynamics.py
```

ทั้งสองคำสั่ง exit status `0`; `Ran 11 tests`; `OK`; validator รายงาน
`replay_equal: true`, drag ratio `4.0`, mass-flow ratio `2.0` และ raw ride-height
fraction `0.4999999999999999` ปัญหาถูกแก้แล้ว
