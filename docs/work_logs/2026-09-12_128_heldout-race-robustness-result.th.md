# ผล Work 128: ความทนทานในการแข่งแบบ Held-Out

แหล่งภาษาอังกฤษ: `2026-09-12_128_heldout-race-robustness-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 128 seal identity ของ fixed/open finalist, evaluator, rules และ condition ที่ไม่เคยเห็น 6 รายการก่อนรัน trajectory ที่ลงทะเบียนครบ 12 รายการ finalist ทั้งคู่จบ synthetic race ทุกครั้งภายใน energy cap `520000 J` และมี thermal/structural margin เป็นบวก open finalist ทำเวลา paired race ดีขึ้น `0.5 s`; หลังรวม numerical uncertainty `0.1 s` ยังไม่ถึง meaningful-improvement gate `1.0 s` ที่ลงทะเบียน Robust superiority และ promotion ยังคง false

Controls ปฏิเสธ training/holdout reuse, source identity ที่เปลี่ยน, incomplete telemetry ที่ซ่อน และ tuning หลัง exposure Result SHA-256 คือ `7ef6c7951abf5dbd3fd96941a10f8775164221ba82b9aceb6d349ac69630bcaa`; exact replay ผ่าน ไม่พบบั๊ก implementation

ไฟล์ที่เปลี่ยน: implementation, configuration, runner, tests, สัญญาสองภาษา `HELDOUT_RACE_ROBUSTNESS_V1` และ plan/result สองภาษานี้ หลักฐานที่ ignore อยู่ใต้ `artifacts/work128/run_a|run_b`

## การตรวจสอบและข้อจำกัด

```powershell
python -m unittest tests.test_heldout_race_robustness -v
# exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/experiments/heldout_race_robustness.py scripts/development/run_heldout_race_robustness.py tests/test_heldout_race_robustness.py
# exit 0
python scripts/development/run_heldout_race_robustness.py --config config/development/heldout_race_robustness_v1.json --output-root artifacts/work128/run_a
# exit 0; completed_negative_result; result SHA-256 ตามข้างต้น
python scripts/development/run_heldout_race_robustness.py --config config/development/heldout_race_robustness_v1.json --output-root artifacts/work128/run_b --replay-reference artifacts/work128/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_optimized_vehicle_controls tests.test_heldout_race_robustness tests.test_repository_contract -v
# exit 0; ผ่าน 18 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; มีไฟล์ Work 128 ที่ประกาศไว้ 10 ไฟล์พอดี
git diff --cached --check
# exit 0
```

race/evaluator เป็นข้อมูลสังเคราะห์, paired condition effects ถูกจำกัดไว้โดยตั้งใจ และ numerical completion ยืนยัน manufactured performance, physical robustness หรือ novelty ไม่ได้ Work 129 ต้องสร้าง decision ซ้ำอย่างอิสระจาก artifact ที่ล็อกไว้ ไม่รับ summary นี้โดยตรง
