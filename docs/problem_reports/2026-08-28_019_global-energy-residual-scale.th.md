# รายงานปัญหา Work 019: สเกลของ Global Energy Residual

ต้นฉบับภาษาอังกฤษ: `2026-08-28_019_global-energy-residual-scale.md`

สถานะ: Resolved

## ปัญหา

การรัน test Work 019 ครั้งแรกผ่าน behavioral case ทั้งหมด แต่ fail 9 ใน 10
real-circuit subtest เพราะ test ถือว่าการลบ terminal value ระดับประมาณ `1e10 J`
ต้องเป็นศูนย์ถึงทศนิยมเจ็ดตำแหน่ง Residual ที่พบมีขนาดตั้งแต่
`1.9073486328125e-06 J` ถึง `1.1444091796875e-05 J`:

```text
Ran 9 tests
FAILED (failures=9)
```

รถจบที่ published distance exact และ per-event energy balance ยังอยู่ภายใน
`1e-8 J` ค่า terminal เป็น binary floating-point accumulation/cancellation
ธรรมดาที่สเกลสัมพัทธ์ประมาณ `1e-15` ไม่ใช่หลักฐานการสร้างหรือทำลายพลังงาน

## ผลกระทบ

Assertion แบบ exact-zero เข้มกว่าขีดจำกัด numerical representation และบดบัง
residual ไม่เป็นศูนย์ที่มีประโยชน์ Model จงใจเก็บ terminal residual นี้เป็น
หลักฐานที่สังเกตได้

## การแก้ไข

เก็บ raw terminal residual ไว้ไม่เปลี่ยน Test per-event residual แต่ละตัวกับ
absolute bound `1e-8 J` ที่ประกาศ และ test terminal reconciliation ด้วย
scale-aware relative bound `2e-15` เทียบกับ initial onboard energy

## Validation

```powershell
python -m unittest tests.test_digital_race -v
python -m unittest discover -s tests -v
python scripts/validate_digital_race.py
```

ทุกคำสั่ง exit status `0` Focused suite รายงาน `Ran 9 tests`; repository suite
รายงาน `Ran 154 tests`; ทั้งคู่รายงาน `OK` Validator เก็บ raw terminal residual
สูงสุด `1.1444091796875e-05 J`, รายงานทั้งสิบสนามจบด้วย distance residual ศูนย์
และยืนยัน onboard energy ลดทางเดียว ปัญหาจบโดยไม่เปลี่ยนหรือซ่อน production
residual
