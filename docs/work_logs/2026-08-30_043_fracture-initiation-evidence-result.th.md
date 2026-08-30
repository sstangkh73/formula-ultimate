# ผลงาน 043: หลักฐาน Fracture Initiation

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_043_fracture-initiation-evidence-result.md`

สถานะ: เสร็จสมบูรณ์

## ผลลัพธ์

Ideal LEFM evaluator ผ่าน arithmetic, representation, ledger, identity และ invalid-domain gate ทั้งหมดสำหรับ crack สามขนาด ผลนี้ตั้งใจไม่อ้าง solver crack-tip field หรือ propagation

## ไฟล์ที่เปลี่ยน

- `config/structural/fracture_initiation_acceptance_v1.json`
- `src/formula_ultimate/structural/fracture.py` และ structural exports
- `scripts/structural/run_fracture_initiation_acceptance.py`
- `scripts/run_work043.ps1`
- `tests/test_fracture_initiation.py`
- `docs/physics/FRACTURE_INITIATION_ACCEPTANCE.md` และ `.th.md`
- matching Work 043 plan/result pair

Ignored evidence อยู่ใต้ `artifacts/work043/`

## การตัดสินใจและผล

- เลือก independently verified evaluator route ตาม roadmap เพราะยังไม่มี admitted CalculiX contour-integral parser
- ใช้ `K_I=sigma sqrt(pi a)` เฉพาะใน narrow `Y=1` infinite-plate domain
- บังคับ finite-width, plane-strain thickness, small-scale-yielding และ yield-before-fracture screen
- รักษา exact crack-tip tag ผ่าน representation `8/16/32` segments และไม่ใช้ singular peak stress
- Initiation load สามค่าถูก localize ด้วย relative error ศูนย์; last-two `K_I`, reaction และ work-ledger residual เป็นศูนย์
- Invalid control หกแบบ fail closed พร้อม exact classified reason

## การตรวจสอบ

```powershell
py -3.14 -m unittest tests.test_fracture_initiation -v
# exit 0; Ran 4 tests; OK

.\scripts\run_work043.ps1
# exit 0; status=passed; case_count=3; negative_controls=6

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 303 tests in 19.264s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

## ข้อจำกัดและงานต่อ

Gross elastic work ledger ไม่ใช่ crack energy ไม่มี solver field, J integral, propagation, path, dissipated fracture energy, uncertainty distribution หรือ physical toughness record Work 044 fatigue เป็น Miner/S-N evidence mechanism แยกต่างหากและห้ามนำเสนอเป็น crack-growth validation
