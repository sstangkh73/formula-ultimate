# ผลลัพธ์ Work 143: ซ่อมการข้ามเทสต์ที่ต้องใช้ artifact บน CI

แหล่งภาษาอังกฤษ: `2026-09-20_143_ci-artifact-skip-repair-result.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์

CI เขียวแล้วบนประวัติที่ push ไป การรัน CI ครั้งแรกของ Works 108–142 แดงด้วยสาเหตุเดียว และสาเหตุนั้นถูกซ่อมแล้ว

| การรัน | Commit | ผล |
| --- | --- | --- |
| `35523292349` | `04e6421` (Work 141) | `Ran 1022 tests` — **FAILED (errors=6, skipped=38)** |
| `35524051329` | `6624a96` (Work 143) | `Ran 1022 tests` — **success** ใช้เวลา 7 นาที 34 วินาที |

## รายงานบั๊ก

- **อาการ:** error หกข้อ ทั้งหมดเกิดจาก `setUp` ใน `tests/test_independent_claim_validation.py` ด้วย `FileNotFoundError: .../artifacts/work128/run_a/telemetry.json`
- **สาเหตุ:** โมดูลนั้นอ่าน telemetry ของ Work 128 ที่บันทึกไว้ ขณะที่ `.gitignore` ตัด `artifacts/` ออกเพราะขนาดใหญ่ อินพุตจึงไม่มีบน checkout ที่สะอาดทุกครั้ง และข้อยกเว้นใน `setUp` ถูกรายงานเป็น error ไม่ใช่การข้าม ชุดทดสอบจึงเขียวไม่ได้เลยในที่ใดที่ยังไม่ได้สร้าง artifact ไว้เอง
- **การแก้:** ใส่ `requires_artifacts("artifacts/work128/run_a/telemetry.json")` ที่ระดับ class ซึ่งเป็น guard ที่ repository มีอยู่แล้วใน `tests/artifact_requirements.py` และถูกใช้โดย `test_campaign_physics.py`, `test_refined_housing_mesh.py` และ `test_whole_mechanical_vehicle_candidate_001.py` ไม่มีการลบสิ่งใดและไม่มี assertion ใดถูกลดความเข้ม
- **การทดสอบกำกับ:** เมื่อมี artifact ได้ `Ran 6 tests — OK` เมื่อย้าย `artifacts/work128` ออกได้ `Ran 6 tests — OK (skipped=6)` ชุดทดสอบทั้งหมด `Ran 1022 tests — OK (skipped=11)` และ CI success

นี่คือข้อบกพร่องประเภทเดียวกับ Work 136 ที่การทดสอบ import CadQuery โดยไม่มีเงื่อนไข ทั้งสองกรณีถูกพบโดยสภาพแวดล้อมแรกที่บังเอิญไม่มีอินพุตนั้น

## ไฟล์ที่เปลี่ยน

- `tests/test_independent_claim_validation.py`
- `EVIDENCE.md` และ `EVIDENCE.th.md`: หัวข้อ CI บันทึกทั้งสองการรัน ความผิดพลาด และการซ่อม พร้อมเพิ่มผลที่วัดบนเครื่องของ Work 143
- แผนและผลลัพธ์สองภาษานี้

## การตรวจสอบ

```text
Command: python -m unittest tests.test_independent_claim_validation
Exit code: 0
Result: Ran 6 tests — OK (มี artifact)

Command: คำสั่งเดิม โดยย้าย artifacts/work128 ออก
Exit code: 0
Result: Ran 6 tests — OK (skipped=6)

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 1022 tests in 379.509s — OK (skipped=11)

Command: git push origin main ; gh run watch 35524051329
Result: conclusion success
```

## ข้ออ้าง

- รองรับ: CI เขียวบน checkout ที่สะอาดที่ `6624a96` และการยืนยันของ Work 129 ยังทำงานทุกที่ที่มี telemetry ที่บันทึกไว้
- ไม่รองรับ: logic ของ Work 129 ถูกทดสอบบน CI เพราะบน CI มันถูกข้ามพร้อมระบุชื่อ และข้อนี้ระบุไว้ใน `EVIDENCE.md`

## ข้อจำกัดและงานถัดไป

การทดสอบที่ถูกข้ามไม่ได้พิสูจน์อะไรเกี่ยวกับโค้ดที่มันครอบคลุม การแก้ที่ทั่วถึงคือ commit fixture ขนาดเล็กของ telemetry ที่บันทึกไว้ เพื่อให้การยืนยันรันได้ทุกที่ หรือสร้างมันขึ้นใน CI ทั้งสองทางเป็นงานแยกต่างหาก
