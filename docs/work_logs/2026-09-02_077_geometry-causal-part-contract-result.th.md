# ผล Work 077: Geometry-Causal Part Contract V1

สถานะ: Completed

ต้นฉบับภาษาอังกฤษ: `2026-09-02_077_geometry-causal-part-contract-result.md`

## ผลลัพธ์และไฟล์ที่เปลี่ยน

Implement declaration แบบ fail-closed `geometry_causal_part_v1`, ตัวอย่าง canonical, validator, component exports, focused tests 8 รายการ, เอกสาร executable contract สองภาษา และ roadmap รถทั้งคันที่ geometry เป็นสาเหตุ Work 077-086 Roadmap บันทึก cadence ทีละสาม Work ตามคำขอเป็น `077-079`, `080-082`, `083-085` แล้ว `086` โดยยัง commit แยกตาม validation ของทุก Work ที่ Completed

ไฟล์ที่เปลี่ยนคือคู่ plan/result ของ Work 077; `docs/contracts/GEOMETRY_CAUSAL_PART_CONTRACT_V1.md` และคู่ภาษาไทย; `docs/reports/GEOMETRY_CAUSAL_WHOLE_VEHICLE_ROADMAP_V1.md` และคู่ภาษาไทย; `config/components/geometry_causal_part_contract_v1.json`; `src/formula_ultimate/components/part_contract.py`; component exports; `scripts/components/validate_part_contract.py`; และ `tests/test_part_contract.py`

## การตัดสินใจและหลักฐานการทดลอง

- Unknown/missing field ต้อง fail; implementation ไม่ลบหรือเติม default
- Feature parameter ต้องมี suffix SI ที่รับได้และค่า finite ส่วน thickness, minimum feature size และ tolerance ต้องเป็นบวก
- Frame ต้อง orthonormal/right-handed ส่วน feature ancestry, identity, datum/interface reference และ load-region path ต้อง explicit
- Feature/tolerance parameter ทุกตัวต้องมี provenance record แบบ exact หนึ่งรายการ Material และ geometry-region evidence ใช้ hash identity
- Canonical JSON เรียง object key แต่รักษาลำดับ array ที่เป็น causal Reference declaration และ control ที่กลับลำดับ key ทุกชั้นให้ SHA-256 เดียวกัน
- การผ่านยอมรับเฉพาะ contract completeness และ deterministic declaration ส่วน CAD validity, manufacturability, structural capacity และ physical validation ยังเป็นคำอ้างที่ห้าม

Reference มี canonical byte count `4319`; declaration SHA-256 คือ `8336bb69762d3263286db84e7e5435c7676a8df56fa73638c8f7839b930b0396` Evidence จาก runner สองไฟล์เหมือนกันทุก byteด้วย SHA-256 `825597A81E4E2DF37A1A7C49B6A7D37206752B7C2E0F38DEA387CDE709FFE03B`

## บันทึก validation แบบ exact

```text
python -m unittest tests.test_part_contract -v
Exit: 0
Ran 8 tests in 0.005s — OK

python scripts\components\validate_part_contract.py --config config\components\geometry_causal_part_contract_v1.json --output artifacts\work077\part_contract_evidence.json
Exit: 0
status=passed; canonical_byte_count=4319
declaration_sha256=8336bb69762d3263286db84e7e5435c7676a8df56fa73638c8f7839b930b0396

python -m unittest tests.test_part_contract tests.test_repository_contract -q
Exit: 0
Ran 14 tests in 3.275s — OK

python -m compileall -q src scripts\components tests\test_part_contract.py
Exit: 0

runner replay plus SHA-256 byte-identity comparison
Exit: 0
evidence_sha256=825597A81E4E2DF37A1A7C49B6A7D37206752B7C2E0F38DEA387CDE709FFE03B

python -m unittest discover -s tests -q
Exit: 0
Ran 487 tests in 333.822s — OK
```

หลัง record นี้จะตรวจ scoped staging, `git diff --cached --check`, สร้าง commit และ post-commit verification แล้วรายงานใน final handoff

## หลักฐานสนับสนุนและขัดแย้ง

หลักฐานสนับสนุน: negative control ทุกตัว reject ด้วยสาเหตุที่ตั้งใจ; key-order replay exact; bilingual repository contract และ test เดิมทั้งหมดผ่าน

หลักฐานขัดแย้ง: ไม่พบภายในสมมติฐาน declaration-only การผ่าน declaration ไม่ให้หลักฐานว่า CadQuery สร้าง feature history ได้หรือ FreeCAD หา semantic region กลับมาได้

Alternative explanation: deterministic identity ตรงนี้อาจเกิดจาก JSON canonicalization เท่านั้นและทำนาย STEP determinism ไม่ได้ Missing evidence รวม B-rep execution, self-intersection/solid validity, independent STEP inspection, material-property provenance จริง, manufacturing-domain validation, mesh/solver evidence และ physical correlation ระดับความเชื่อมั่นสูงสำหรับ Python declaration boundary ที่ทดสอบ และจงใจไม่กำหนดความเชื่อมั่นสำหรับ downstream physical claim

## ข้อจำกัดและงานถัดไป

Work 078 ต้อง execute bounded feature operator และพิสูจน์ deterministic valid-solid/STEP behavior กับ canonical part family 5 แบบ Work 079 ต้องแทน minimal material/manufacturing reference ด้วย engineering-property และ process-domain contract Artifact ของ Work 077 ไม่มีรายการใดเป็นผล load capacity, manufacturing, safety หรือ physical validation
