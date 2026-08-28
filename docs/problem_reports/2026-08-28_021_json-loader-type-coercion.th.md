# รายงานปัญหา Work 021: JSON Loader แปลง Type เงียบ

ต้นฉบับภาษาอังกฤษ: `2026-08-28_021_json-loader-type-coercion.md`

สถานะ: Resolved

## ปัญหา

Code review หลัง focused suite Work 021 ครั้งแรกผ่าน พบว่า JSON architecture
loader เรียก `str(...)` กับ `schema_version`, `architecture_id`, module identity/
stage/version และ signal ทุกตัว Declaration ที่ผิด เช่น `"architecture_id": 123`
จึงอาจกลายเป็น string `"123"` ที่ดู valid แทนการ fail-closed

## ผลกระทบ

Reference JSON ที่ใช้อยู่ประกาศ string type ถูกต้อง จึงไม่กระทบ fingerprint หรือ
stage evidence ของมัน แต่การรับ JSON type ผิดจะทำให้ central configuration
contract อ่อนลงและอาจทำให้ producer/consumer identity ต่างจากสิ่งที่ผู้เขียน
ประกาศจริง

## การแก้ไข

เพิ่มตัวอ่าน JSON string และ string-array แบบ strict Root/module string field
ต้องเป็น JSON string อยู่แล้ว และ list item ต้องเป็น string อยู่แล้ว ห้าม coerce
type เพิ่ม regression fixture ที่ `architecture_id` เป็นตัวเลขและบังคับให้เกิด
`CouplingContractError`

## Validation

Loader ที่แก้แล้วและ regression case ผ่าน gate ของ Work 021 และ repository
ทั้งหมดเมื่อ 2026-08-28:

```powershell
python -m unittest tests.test_coupling_contracts -v
# Ran 12 tests ... OK (exit 0)

python -m unittest discover -s tests -v
# Ran 166 tests ... OK (exit 0)

python scripts/validate_coupling_contracts.py
# reject JSON type ที่ผิด; exit 0

python -m compileall -q src scripts tests
# exit 0
```

Loader รักษาเจตนาของ declaration โดย reject JSON type ที่ผิด ไม่แก้หรือ
ตีความ type ใหม่อย่างเงียบ
