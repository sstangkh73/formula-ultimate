# ผล Work 117: การป้อนกลับสองทิศทางระหว่างสถาปัตยกรรมกับชิ้นส่วน

แหล่งภาษาอังกฤษ: `2026-09-12_117_architecture-part-feedback-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 117 สร้างวงรอบ feedback/regeneration ที่ทำซ้ำได้ โดยคงอัตลักษณ์งานภายนอก `203629bd848528f5a488f8564cf51d311f659a1af8d0bc81b31b2c13ed3120da` ไว้ วงรอบใช้ผลลัพธ์ Work 112, Work 114 และ Work 115 ที่ระบุแน่นอน และได้เงื่อนไขระดับ assembly `19196.837823792008 N`, `10 W` และ `7.099179394127206e-6 m`

Feedback แก้ไขงานภายใน สร้าง geometry ใหม่ และบันทึกการทำให้หลักฐานเก่าใช้ไม่ได้สองครั้ง ส่วน frozen control คงงานเริ่มต้นไว้ ทั้งสองโหมดใช้สาม evaluation พร้อม coefficient และ seed ชุดเดียวกัน การรวม cell ที่ทำหน้าที่หลายอย่างให้มวล `0.0081 kg` แทนการนับซ้ำ `0.0108 kg`; coefficient ที่ขาดถูกปฏิเสธ มวลที่สร้างเปลี่ยนจาก `0.005238 kg` เป็น `0.010573618273344638 kg` ซึ่งเป็นหลักฐานขัดแย้งที่เก็บไว้ เพราะไม่ได้กำหนดว่าต้องดีขึ้นจึงจะผ่าน

Result SHA-256 คือ `0d85d649eb8976e29bb08e6cb5815b06fba27b25428a8d3f5195281a52b004f1`; replay ตรงกันทุกบิต `measured_material` และ `ground_interaction` ยังไม่ถูกแก้ และ candidate ทุกตัวรายงาน feasibility ที่ไม่สมบูรณ์ ไม่พบบัคในการนำไปใช้ระหว่าง run ที่รับเข้า

ไฟล์ที่เปลี่ยน: implementation/config/runner/test, contract `ARCHITECTURE_PART_FEEDBACK_V1` สองภาษา และ plan/result สองภาษาชุดนี้ หลักฐานที่ไม่ติดตามใน Git อยู่ใต้ `artifacts/work117/run_a|run_b`

## การตรวจสอบและข้อจำกัด

```powershell
python -m unittest tests.test_architecture_part_feedback -v
# exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/experiments/architecture_part_feedback.py scripts/development/run_architecture_part_feedback.py
# exit 0
python scripts/development/run_architecture_part_feedback.py --config config/development/architecture_part_feedback_v1.json --output-root artifacts/work117/run_a
# exit 0; ได้ result SHA-256 ข้างต้น
python scripts/development/run_architecture_part_feedback.py --config config/development/architecture_part_feedback_v1.json --output-root artifacts/work117/run_b --replay-reference artifacts/work117/run_a/result.json
# exit 0; replay ตรงกันทุกบิต
```

```powershell
python -m unittest tests.test_physical_interface_graph tests.test_moving_contact_assembly tests.test_coupled_thermal_solid tests.test_architecture_part_feedback tests.test_repository_contract -v
# exit 0; ผ่าน 30 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; ตรงกับ 10 ไฟล์ที่ประกาศสำหรับ Work 117
git diff --cached --check
# exit 0
```

Generator ที่มีขอบเขตและตัวประเมินแบบลดรูปไม่ยืนยัน general topology optimization, ความถูกต้องของ material, ground interaction, feasibility ระดับยานพาหนะเต็มระบบ หรือ physical validation จะรายงาน commit hash ที่ตรวจแล้วในสรุปสุดท้าย
