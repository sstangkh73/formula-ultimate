# รายงานปัญหา Work 023: Fingerprint Pin Circuit Profile ไม่ครบ

ต้นฉบับภาษาอังกฤษ: `2026-08-28_023_profile-fingerprint-underpinning.md`

สถานะ: Resolved

## ปัญหา

การ review focused suite แรกของ Work 023 พบว่า step-input fingerprint ใส่เพียง
`profile.circuit_id` แต่ไม่ใส่ circuit profile ทั้งชุด หากแก้ lap fact, evidence
หรือ design-pressure โดยคง ID เดิม fingerprint จะไม่เปลี่ยน

## ผลกระทบ

Typed input และ missing-evidence behavior ถูกต้อง แต่ replay identity pin ข้อมูล
ไม่ครบ จึงพิสูจน์ไม่ได้ว่า evaluate catalog content รุ่นใด

## การแก้

Canonicalize immutable `CircuitProfile` ทั้งชุด รวม nested source evidence และ
วันที่แบบ ISO เข้า step-input fingerprint พร้อม regression test ว่า profile
content เปลี่ยนภายใต้ ID เดิมต้องทำให้ fingerprint เปลี่ยน

## Validation

Regression เปลี่ยนชื่อ profile ภายใต้ circuit ID เดิมและได้ SHA-256 fingerprint
ต่างกัน ขณะที่ catalog permutation ยัง replay ตรง

```powershell
python -m unittest tests.test_step_inputs -v
# Ran 9 tests ... OK (exit 0)
python -m unittest discover -s tests -v
# Ran 186 tests ... OK (exit 0)
python scripts/validate_step_inputs.py
# catalog_permutation_replay_equal: true; exit 0
```
