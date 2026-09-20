# แผน Work 143: ซ่อมการข้ามเทสต์ที่ต้องใช้ artifact บน CI

แหล่งภาษาอังกฤษ: `2026-09-20_143_ci-artifact-skip-repair-plan.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: In progress

## วัตถุประสงค์

ทำให้ชุดทดสอบกลับมาเขียวบน checkout ที่สะอาด การรัน CI ครั้งแรกของประวัติที่ push ไป คือรัน `35523292349` ที่ commit `04e6421` ล้มเหลวด้วย `Ran 1022 tests ... FAILED (errors=6, skipped=38)`

## หลักฐานตั้งต้น

error ทั้งหกข้อมาจากความผิดพลาดเดียวกัน คือ `tests/test_independent_claim_validation.py` อ่าน `artifacts/work128/run_a/telemetry.json` ใน `setUp` ขณะที่ `.gitignore` ตัด `artifacts/` ออก ไฟล์จึงไม่มีบน CI traceback คือ `FileNotFoundError` ภายใน `setUp` ซึ่ง unittest รายงานเป็น error ไม่ใช่การข้าม

repository มีกลไกที่ถูกต้องอยู่แล้ว คือ `tests/artifact_requirements.py` ที่ให้ `requires_artifacts` และถูกใช้ใน `test_campaign_physics.py`, `test_refined_housing_mesh.py` และ `test_whole_mechanical_vehicle_candidate_001.py` แต่โมดูลทดสอบของ Work 129 เขียนขึ้นโดยไม่ได้ใช้

นี่คือข้อบกพร่องประเภทเดียวกับ Work 136 คือการทดสอบที่ต้องใช้อินพุตซึ่ง checkout ไม่มี ต้องข้ามพร้อมข้อความระบุชื่ออินพุต ไม่ใช่ล้มเหลว

## ขอบเขต

- `tests/test_independent_claim_validation.py`: ใส่ `requires_artifacts("artifacts/work128/run_a/telemetry.json")` ที่ระดับ class
- `EVIDENCE.md` และ `EVIDENCE.th.md`: บันทึกผล CI ที่วัดได้ของประวัติที่ push ไป ทั้งก่อนและหลังการซ่อมนี้
- แผนสองภาษานี้และผลลัพธ์สองภาษาที่ตรงกัน

## การตรวจสอบ

1. `python -m unittest tests.test_independent_claim_validation`: exit 0 ผ่าน 6 การทดสอบเมื่อมี artifact
2. คำสั่งเดิมโดยย้าย `artifacts/work128` ออก: exit 0 ข้าม 6 การทดสอบ
3. `python -m unittest discover -s tests`: exit 0
4. การรัน CI หลัง push ได้ข้อสรุปเป็น `success`

## เกณฑ์สำเร็จและล้มเหลว

สำเร็จ: การทดสอบรันที่ใดก็ตามที่มีหลักฐาน ข้ามที่ใดที่ไม่มี และ CI เขียวบน checkout ที่สะอาด

ล้มเหลว: มีการลบหรือลดความเข้มของการทดสอบเพื่อให้เขียว หรือการข้ามไปบังความล้มเหลวจริงของโค้ด

## ความเสี่ยงและสิ่งที่ไม่ทำ

- ความเสี่ยง: การข้ามอาจบัง regression ของ logic ใน Work 129 บน CI ยอมรับและระบุไว้ว่า การยืนยันเหล่านั้นใช้ได้เฉพาะกับหลักฐานที่บันทึกไว้ และยังรันอยู่ทุกที่ที่มีหลักฐานนั้น
- สิ่งที่ไม่ทำ: ไม่แก้ logic ของ Work 129 หรือหลักฐานที่บันทึกไว้, ไม่แตะการทดสอบอื่น และไม่เขียนประวัติใหม่
