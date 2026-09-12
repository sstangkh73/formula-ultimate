# ผล Work 129: การตรวจสอบ Claim แบบอิสระ

แหล่งภาษาอังกฤษ: `2026-09-12_129_independent-claim-validation-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 129 สร้าง paired time, energy และ margin evidence ใหม่จาก Work 128 telemetry ที่ล็อกไว้ผ่าน code path ที่ประกาศแยก ก่อนเปรียบเทียบ upstream decision conservative boundary interpretation ลด mean time improvement จาก `0.5 s` เป็น `0.22 s` ความต่าง `0.28 s` เกิน discrepancy trigger `0.2 s` ที่ลงทะเบียนและถูกจำแนก `explained_model_boundary`; ranking ยังเป็นบวก แต่ไม่ถึง superiority threshold `1.0 s`

constraint ด้าน energy, thermal และ structural ยังเป็นบวก shared-function wrapper ถูกปฏิเสธ และ known omitted-boundary injection ถูกตรวจพบที่ `0.28 s`; เมื่อปิด correction detector control ล้มตามที่ตั้งใจ selected superiority claims ไม่รอดและ promotion ยังคง false Result SHA-256 คือ `082158788a300b5ab7e91b7a4cc038e56314f139f21b5b5361c591aa61471b7c`; exact replay ผ่าน ไม่พบบั๊ก implementation

ไฟล์ที่เปลี่ยน: implementation, configuration, runner, tests, สัญญาสองภาษา `INDEPENDENT_CLAIM_VALIDATION_V1` และ plan/result สองภาษานี้ หลักฐานที่ ignore อยู่ใต้ `artifacts/work129/run_a|run_b`

## การตรวจสอบและข้อจำกัด

```powershell
python -m unittest tests.test_independent_claim_validation -v
# exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/experiments/independent_claim_validation.py scripts/development/run_independent_claim_validation.py tests/test_independent_claim_validation.py
# exit 0
python scripts/development/run_independent_claim_validation.py --config config/development/independent_claim_validation_v1.json --output-root artifacts/work129/run_a
# exit 0; completed_claim_downgrade; result SHA-256 ตามข้างต้น
python scripts/development/run_independent_claim_validation.py --config config/development/independent_claim_validation_v1.json --output-root artifacts/work129/run_b --replay-reference artifacts/work129/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_detailed_part_comparison tests.test_detailed_vehicle_closure tests.test_optimized_vehicle_controls tests.test_heldout_race_robustness tests.test_independent_claim_validation tests.test_repository_contract -v
# exit 0; ผ่าน 36 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; มีไฟล์ Work 129 ที่ประกาศไว้ 10 ไฟล์พอดี
git diff --cached --check
# exit 0
```

การวิเคราะห์ทั้งสองยังใช้ synthetic telemetry, candidate identities และ physical assumptions ร่วมกัน independent code path ไม่ใช่ institutional independence และแทน measured boundary histories หรือ physical tests ไม่ได้ Work 130 ต้องส่งต่อ downgraded evidence envelope และ unresolved assumptions เข้า manufacturing tolerances
