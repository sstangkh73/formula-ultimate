# รายงานปัญหา Work 016: Slotted Dataclass Serialization

ต้นฉบับภาษาอังกฤษ: `2026-08-26_016_slotted-dataclass-serialization.md`

สถานะ: Resolved

## ปัญหา

การรัน test Work 016 ครั้งแรกผ่าน 10 และ error 1 รายการ Test steady-state พยายาม
อ่าน `PlanarBalanceResiduals.__dict__` แต่ evidence dataclass ทุกตัวของ Work 016
ใช้ `slots=True` จึงไม่มี `__dict__`

```text
AttributeError: 'PlanarBalanceResiduals' object has no attribute '__dict__'
Ran 11 tests
FAILED (errors=1)
```

Validator มีสมมติฐาน serialization ที่ไม่รองรับแบบเดียวกัน นี่เป็น defect ของ
test/evidence formatting; การคำนวณฟิสิกส์ในอีกสิบ test ผ่านแล้ว

## สาเหตุราก

Test และ validator ปฏิบัติต่อ slotted dataclass เหมือน object ปกติที่มี instance
dictionary ทั้งที่ `slots=True` ตั้งใจตัด dictionary นั้นออก

## การแก้ไข

- Test ใช้ `dataclasses.astuple` เพื่อไล่ residual value
- JSON validator ใช้ `dataclasses.asdict` เพื่อเก็บ residual field พร้อมชื่อ
- ไม่มีการเปลี่ยนสมการฟิสิกส์, tolerance, solver branch หรือ output value

## การยืนยันผล

```powershell
python -m unittest tests.test_lateral -v
python scripts/validate_lateral.py
```

ผล:

```text
Ran 11 tests
OK
validator exit status: 0
```

การรัน repository ทั้งหมดถัดมายังผ่าน 121 tests ปัญหาถูกแก้แล้วและไม่มีการอ่าน
`__dict__` ที่ไม่รองรับเหลือใน test หรือ validator ของ Work 016
