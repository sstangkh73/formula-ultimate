# แผน Work 077: Geometry-Causal Part Contract V1

สถานะ: Completed

ต้นฉบับภาษาอังกฤษ: `2026-09-02_077_geometry-causal-part-contract-plan.md`

## วัตถุประสงค์และขอบเขต

กำหนด contract แบบ fail-closed รุ่นแรกของ repository สำหรับชิ้นส่วนทางกายภาพที่ geometry เป็นสาเหตุของผลฟิสิกส์ และบันทึก roadmap Work 077-086 ที่ผู้ใช้ให้มา ชิ้นส่วนที่รับเข้าได้ต้องประกาศ functional identity, feature history ตามลำดับ, material assignment, local frame, datums, interfaces, load/application regions และ load path, manufacturing process, tolerances, minimum feature size, parameter provenance และ claim boundary

งานนี้กำหนดและตรวจ declaration เท่านั้น ยังไม่สร้าง B-rep geometry, ตรวจ STEP, แก้ structural response, ยืนยันกระบวนการผลิต หรือพิสูจน์ว่าชิ้นส่วนที่ประกาศ feasible ทางกายภาพ

## แบบการทดลอง

- ตัวแปรอิสระ: การมีอยู่/ลำดับของ field, interface type, basis ของ coordinate frame, suffix หน่วยและค่าของ parameter, tolerance, minimum feature size, material evidence identity, การเชื่อมต่อของ load region และความครบถ้วนของ provenance
- ตัวแปรตาม: admission/rejection, failure reason ที่แน่นอน, canonical serialized bytes, declaration SHA-256 และ replay identity
- ตัวแปรควบคุม: canonical bracket declaration ที่ผ่านหนึ่งรายการ; การสลับลำดับ key; control สำหรับ unknown field, wrong unit, missing material, missing interface, missing load path, `NaN`, negative thickness, invalid tolerance, invalid frame และ unsupported interface
- สมมติฐานที่ต้องการ: declaration ที่มีความหมายเท่ากันให้ canonical bytes และ SHA-256 เดียวกัน ขณะที่ declaration ผิดรูปหรือไม่ครบทุกตัวต้อง fail ก่อนเข้า geometry หรือ physics downstream
- การหักล้าง: ลบ field แบบเงียบ, แปลงหน่วยโดยปริยาย, รับข้อมูล non-finite, เติม material/interface/load path โดย default, hash เปลี่ยนเมื่อสลับ key หรือยอมรับ interface ที่ไม่รองรับ

## ไฟล์ที่วางแผน

- `docs/reports/GEOMETRY_CAUSAL_WHOLE_VEHICLE_ROADMAP_V1.md` และคู่ภาษาไทย
- `docs/contracts/GEOMETRY_CAUSAL_PART_CONTRACT_V1.md` และคู่ภาษาไทย
- `config/components/geometry_causal_part_contract_v1.json`
- `src/formula_ultimate/components/part_contract.py` และ component exports
- `scripts/components/validate_part_contract.py`
- `tests/test_part_contract.py`
- plan นี้และ result record คู่สองภาษา
- หลักฐานที่ ignore ใต้ `artifacts/work077/`

## การตรวจและเกณฑ์สำเร็จ

ตัวอย่าง canonical และการสลับลำดับ key ต้องให้ serialization ที่เหมือนกันทุก byte และ SHA-256 เดียวกัน Unknown field หรือหน่วย, material/interface/load path ที่หายไป, ค่า non-finite, thickness หรือ minimum feature size ที่ไม่เป็นบวก, tolerance ผิด, frame ไม่ orthonormal/right-handed, identity ซ้ำ และ interface type ที่ไม่รองรับต้อง fail closed พร้อมเหตุผลที่มี test ครอบคลุม Focused tests, full regression, compilation, bilingual repository contract, runner replay, scoped staging, `git diff --cached --check`, commit เดียว และ post-commit verification ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำโดยชัดแจ้ง

Declaration ที่ซื่อตรงยังอาจบรรยาย geometry ที่ CAD kernel สร้างไม่ได้หรือโครงสร้างที่ล้มเหลวได้ Geometry signature ของ interface ยังเป็นเพียง declaration ใน Work 077 และยังไม่ถูกตรวจหลัง STEP exchange Material evidence ถูกอ้างอิงแต่ engineering-property/manufacturing contract จะทำใน Work 079 ห้ามใช้ Work 077 เพื่ออ้าง CAD validity, load capacity, manufacturability, assembly validity หรือ physical validation
