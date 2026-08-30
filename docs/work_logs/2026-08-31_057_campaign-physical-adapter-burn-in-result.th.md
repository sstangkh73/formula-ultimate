# ผลงาน 057: Campaign Physical Adapter และ Burn-In

สถานะ: หยุด (Stopped)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_057_campaign-physical-adapter-burn-in-result.md`

## ผลลัพธ์

Control การ recover pending reservation ข้าม process ผ่านแบบ exact จากนั้น excluded burn-in seed `55999` consume และบันทึก frozen training opportunities ครบ `240` รายการ (`80` ต่อ treatment) โดยไม่มี pending record แต่ downstream replay หยุดก่อน holdout evaluation เพราะ serialized promotion `candidate_ids` เป็น JSON lists ขณะที่ dataclass representation ที่คำนวณใหม่ยังเป็น tuples แม้ค่าตรงกัน strict structural comparison จึง fail closed ด้วย `CampaignPhysicsError: stored promotion selection differs from training-only replay`

ไม่มี main seed ถูก reserve หรือ evaluate และไม่มี burn-in admission ตาม v1 immutability rule ห้ามซ่อม implementation แล้วทำต่อด้วย protocol เดิมหลังมี burn-in observations การแก้ต้องใช้ protocol ID ใหม่

## ไฟล์ที่เปลี่ยน

- Initial campaign adapter และ analysis implementation ใน `src/formula_ultimate/experiments/campaign_physics.py`
- Public evidence decoding ใน `campaign_runner.py` และ exports ใน `experiments/__init__.py`
- Generic campaign command, process-resume probe และ Work 057/058 wrappers ใต้ `scripts/`
- Focused campaign-physics tests
- แผนสองภาษา Work 057/058 และ stopped-result records

ไฟล์เหล่านี้เก็บ exact failed implementation เพื่อ reproducibility โดยตั้งใจไม่แก้ serialization defect ใน work item นี้

## บันทึก validation และ execution ที่ exact

1. Compilation:

   ```powershell
   py -3.14 -m compileall -q src scripts
   ```

   Exit status: `0`

2. Focused tests:

   ```powershell
   py -3.14 -m unittest tests.test_campaign_physics tests.test_campaign_runner -q
   ```

   Exit status: `0`; `Ran 16 tests in 0.413s`; `OK`

3. Separate-process reservation phase:

   ```powershell
   py -3.14 scripts/experiments/probe_campaign_process_resume.py --action reserve --artifact-root artifacts/work057/process_resume_probe
   ```

   Intentional exit status: `75` Candidate `candidate-52a6df50771f058c`; reservations/results/pending = `1/0/1`

4. Separate-process resume phase:

   ```powershell
   py -3.14 scripts/experiments/probe_campaign_process_resume.py --action resume --artifact-root artifacts/work057/process_resume_probe
   ```

   Exit status: `0`; decision `separate_process_resume_exact`; reservations/results/pending = `1/1/0` และไม่จัด opportunity ที่สอง

5. Burn-in:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work057.ps1
   ```

   Exit status: `1` Failed stage: `downstream` Exact message: `stored promotion selection differs from training-only replay`

## Ignored evidence ที่เก็บไว้

- Training budget/result rows: `240/240`; stage rows: `4` (passed refinement benchmark หนึ่งรายการและ treatment/seed promotion declarations สามรายการ); holdout rows: `0`; main-seed rows: `0`
- Budget-ledger file SHA-256: `53874fdfc878d0a23b0868797cf59556a08e5106d06fd5a3bfe339ccc8abf005`
- Result-ledger file SHA-256: `0c79ae667631a93c95f6872b8e79e65c0337636e2a3316dc31b3c0fd036bfeb9`
- Stage-ledger file SHA-256: `dcb6b2fd5918800402d3c01d4a5d5b060fc7bf03f16bc711f22d3b2b8aac8f0f`
- Failure-record SHA-256: `faa7b387b33003c3f4321aabd50d631ad4186ec95898f400847cd4e8ccb31b41`

## Review discipline

หลักฐานสนับสนุน: opportunity accounting, candidate reconstruction, process-boundary resume, physical input identity และ CalculiX refinement benchmark ทำงานก่อนจุดหยุด

หลักฐานที่ขัดแย้ง: downstream replay ไม่ representation-canonical ข้าม JSON boundary และ unit tests เดิมไม่ได้ exercise การ append/reload แล้วเปรียบเทียบ promotion selection tuples กับ lists

คำอธิบายทางเลือกที่ตัดออก: นี่ไม่ใช่ scientific treatment outcome หรือ candidate physics failure แต่เป็น infrastructure serialization-contract defect

หลักฐานที่ยังขาด: holdout, candidate refinement, STEP/FreeCAD finalist witnesses, burn-in acceptance, main-seed evidence ทั้งหมด และ statistical analysis

ความเชื่อมั่น: สูงต่อสาเหตุที่หยุดและขอบเขต zero-main-seed แต่ยังไม่ให้ confidence claim ต่อ downstream campaign completion

## งานถัดไป

สร้าง numbered work item ใหม่และ protocol/campaign identity ใหม่ Canonicalize promotion selection representations ที่ serialization boundary เพิ่ม regression test ที่ append/reload stage evidence freeze corrected implementation identity รัน excluded burn-in ใหม่จาก empty ledgers และอนุญาต main executionหลัง acceptanceเท่านั้น
