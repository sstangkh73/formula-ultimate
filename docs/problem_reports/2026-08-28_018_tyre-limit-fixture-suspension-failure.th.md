# รายงานปัญหา Work 018: Tyre-Limit Fixture ทำให้ Suspension Failure

ต้นฉบับภาษาอังกฤษ: `2026-08-28_018_tyre-limit-fixture-suspension-failure.md`

สถานะ: Resolved

## ปัญหา

การรัน Work 018 ครั้งแรกผ่าน 12 tests และ fail tyre-limit test เพราะ result เป็น
`failed` ไม่ใช่ `ok` ที่คาด:

```text
Ran 13 tests
FAILED (failures=1)
AssertionError: 'ok' != 'failed'
```

Test ลด normal load จาก `1000 N` เป็น `100 N` เพื่อสร้าง tyre torque ceiling
`mu*Fz*R = 30 N*m` แต่ยังใช้ suspension preload `1000 N` Model จึงคำนวณ rebound
acceleration สูงและหา suspension-travel failure ภายใน interval หนึ่งวินาทีได้ถูกต้อง

## สาเหตุราก

Fixture เปลี่ยน physical condition ที่ coupled สองตัวโดยไม่ตั้งใจ คือ tyre load
และ suspension force imbalance Test ต้องการแยก tyre saturation แต่ suspension ไม่
อยู่ equilibrium แล้ว

## การแก้ไข

Test และ validator ใช้ tyre-limit fixture แยกที่ preload `100 N` และ normal load
`100 N` Suspension
จึงอยู่ equilibrium ขณะที่ tyre torque limit ยังเป็น `30 N*m` และแก้ validator
แบบเดียวกัน

ห้ามแก้ production solver เพื่อซ่อน suspension failure ที่สังเกตได้

## Validation

```powershell
python -m unittest tests.test_suspension_braking -v
python scripts/validate_suspension_braking.py
```

ทั้งสองคำสั่ง exit status `0`; `Ran 13 tests`; `OK` Validator รายงาน tyre limit
`30 N*m`, tyre scale `0.2`, applied torque `30 N*m` และ unserved torque
`120 N*m` โดยไม่มี suspension event ปัญหาถูกแก้แล้ว
