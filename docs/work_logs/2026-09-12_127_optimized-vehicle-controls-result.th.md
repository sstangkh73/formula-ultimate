# ผล Work 127: Optimized Vehicle Controls

แหล่งภาษาอังกฤษ: `2026-09-12_127_optimized-vehicle-controls-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

แขน fixed-topology, reference, random-control และ open-candidate แต่ละแขนได้รับ vehicle-search 4 evaluations และ controller-tuning 4 evaluations บน paired conditions เดียวกันและ source energy `1,000,000 J` ทุกแขนถูก optimize, ประเมินด้วย common controller แล้ว retune ด้วย opportunity เท่ากัน มีการรวม installed base, cooling, containment และ support mass, energy use และ manufacturing penalty

หลังรวม transferred burden ครบ paired effect ของ open candidate เทียบกับ control ที่ optimize แล้วและดีที่สุดคือ `-0.003`; meaningful system effect ที่ลงทะเบียนคือ `+0.02` ดังนั้น system-benefit gate และ promotion ยังคง false controls แบบ untuned baseline, free controller effort, omitted cooling mass และ unequal source energy ถูกปฏิเสธ Result SHA-256 คือ `d19548b5d45cfcd382ff248aa554e7c96c3043d201d02ee11398d95dd0366f1a`; exact replay ผ่าน ไม่พบบั๊ก implementation

ไฟล์ที่เปลี่ยน: implementation, configuration, runner, tests, สัญญาสองภาษา `OPTIMIZED_VEHICLE_CONTROLS_V1` และ plan/result สองภาษานี้ หลักฐานที่ ignore อยู่ใต้ `artifacts/work127/run_a|run_b`

## การตรวจสอบและข้อจำกัด

```powershell
python -m unittest tests.test_optimized_vehicle_controls -v
# exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/experiments/optimized_vehicle_controls.py scripts/development/run_optimized_vehicle_controls.py tests/test_optimized_vehicle_controls.py
# exit 0
python scripts/development/run_optimized_vehicle_controls.py --config config/development/optimized_vehicle_controls_v1.json --output-root artifacts/work127/run_a
# exit 0; completed_negative_result; result SHA-256 ตามข้างต้น
python scripts/development/run_optimized_vehicle_controls.py --config config/development/optimized_vehicle_controls_v1.json --output-root artifacts/work127/run_b --replay-reference artifacts/work127/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_coupled_vehicle_transient tests.test_multiscale_discovery_search tests.test_detailed_vehicle_closure tests.test_optimized_vehicle_controls tests.test_repository_contract -v
# exit 0; ผ่าน 30 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; มีไฟล์ Work 127 ที่ประกาศไว้ 10 ไฟล์พอดี
git diff --cached --check
# exit 0
```

คะแนนและ burden weights เป็น deterministic synthetic fixtures ไม่ยืนยัน held-out race performance, manufacturing behavior, physical reliability, external novelty หรือ vehicle superiority Work 128 ต้องประเมิน finalist ที่ตรึงไว้บน race แบบ held-out แยก โดยไม่เปลี่ยน negative result หรือ threshold นี้
