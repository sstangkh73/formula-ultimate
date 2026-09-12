# ผล Work 125: การเปรียบเทียบชิ้นส่วนละเอียดที่ลงทะเบียนล่วงหน้า

แหล่งภาษาอังกฤษ: `2026-09-12_125_detailed-part-comparison-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

แขนทั้งสี่ที่ลงทะเบียนถูก optimize บนเงื่อนไข training เดียวกัน 4 เงื่อนไข และประเมินบน paired holdout 6 เงื่อนไขที่ไม่ทับกัน แต่ละแขนใช้ 10 evaluations เท่ากัน แขน open-material เหนือกว่า control ที่ optimize แล้วและดีที่สุด `+0.05` ณ coarse fidelity แต่ด้อยกว่า `-0.01` ณ fine fidelity ดังนั้นด่าน discovery-benefit ที่ลงทะเบียนยังเป็น false การเอา active coupling ที่อ้างออกลด utility ตรง `0.05` ขณะที่ inactive appendage ของ fixed-family ไม่เปลี่ยน การละเว้น hardware เป็น invalid, holdout leakage ถูกปฏิเสธ และ audit subject ที่ไม่ขึ้นกับ score ทั้งสองรายการถูกเก็บไว้

ผลนี้คือ negative result ที่ทำงานสำเร็จ ไม่ใช่งานล้มเหลว ข้อจำกัด material survival จาก Work 116 และ promotion จาก Work 124 ยังมีผล Result SHA-256 คือ `7f5889940e6bf6cb5f24523f9443aa73b705b3510b6ba2244c400d6eae4b79a6`; exact replay ผ่าน ไม่พบบั๊ก implementation

ไฟล์ที่เปลี่ยน: implementation, configuration, runner, tests, สัญญาสองภาษา `DETAILED_PART_COMPARISON_V1` และ plan/result สองภาษานี้ หลักฐานที่ ignore อยู่ใต้ `artifacts/work125/run_a|run_b`

## การตรวจสอบและข้อจำกัด

```powershell
python -m unittest tests.test_detailed_part_comparison -v
# exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/experiments/detailed_part_comparison.py tests/test_detailed_part_comparison.py
# exit 0
python scripts/development/run_detailed_part_comparison.py --config config/development/detailed_part_comparison_v1.json --output-root artifacts/work125/run_a
# exit 0; completed_negative_result; result SHA-256 ตามข้างต้น
python scripts/development/run_detailed_part_comparison.py --config config/development/detailed_part_comparison_v1.json --output-root artifacts/work125/run_b --replay-reference artifacts/work125/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_detailed_connection_contact tests.test_moving_contact_assembly tests.test_coupled_thermal_solid tests.test_material_failure_scope tests.test_multiscale_discovery_search tests.test_detailed_part_comparison tests.test_repository_contract -v
# exit 0; ผ่าน 41 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; มีไฟล์ Work 125 ที่ประกาศไว้ 10 ไฟล์พอดี
git diff --cached --check
# exit 0
```

fixture การตอบสนองเป็นข้อมูลสังเคราะห์และยืนยัน external novelty, measured material survival, พฤติกรรมเมื่อผลิตจริง, whole-vehicle benefit หรือ physical validation ไม่ได้ งานถัดไป: Work 126 ต้องปิด geometry ของ detailed candidate ทั้งคันและทุกเส้นทาง hardware/function ที่จำเป็น โดยไม่ผ่อนข้อจำกัดหลักฐานที่ยังไม่คลี่คลายเหล่านี้
