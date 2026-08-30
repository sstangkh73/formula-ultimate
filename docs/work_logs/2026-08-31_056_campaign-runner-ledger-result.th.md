# ผลงาน 056: Campaign Runner และ Append-Only Ledgers

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_056_campaign-runner-ledger-result.md`

## ผลลัพธ์

implement deterministic resume-safe campaign runner พร้อม opportunity-budget ledger และ terminal-result ledger แบบ hash chain แยกกัน คำสั่ง preparation ของ Work 056 คืน `runner_prepared_campaign_locked` และทำ candidate, burn-in, main-seed evaluations เป็นศูนย์ ดังนั้นงานนี้เป็นหลักฐานด้าน runner mechanics เท่านั้น ไม่ใช่ campaign outcome หรือ physical validation

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/experiments/campaign_runner.py`: chained JSONL ledger, cross-ledger validation, candidate/evaluation identity verification, deterministic agent reconstruction, interruption resume, explicit execution authorization และ training-only promotion selection
- `src/formula_ultimate/experiments/__init__.py`: public runner exports
- `scripts/experiments/prepare_main_campaign_runner.py` และ `scripts/run_work056.ps1`: preparation-only state initialization, exact replay และ execution-lock control
- `tests/test_campaign_runner.py`: positive/adversarial runner-ledger tests สิบกรณี
- `docs/research/BOUNDED_MAIN_CAMPAIGN_RUNNER_LEDGER.md` และคู่ภาษาไทย: maintained contract และ evidence boundary
- แผนและผล Work 056 สองภาษา

หลักฐาน ignored ที่สร้าง: `artifacts/work056/runner_preparation.json` และ empty ledgers `artifacts/work056/preparation_only/*.jsonl`

## การตัดสินใจ

- consume opportunity ด้วย durable reservation ก่อน evaluator invocation หากสะดุด latest reservation จะค้างเป็น pending และ resume ต้อง complete candidate เดิมโดยไม่จัด attempt ใหม่
- ตรวจ candidate ID, RNG checkpoint, ancestry, evaluation SHA-256, sequence และ previous-row hash แยกจาก row hash
- Execution ต้องมี authorization ID ที่ไม่ว่างและตรงกับ campaign ID, evidence class และ seed ส่วน admitted main execution ต้องมี explicit flag ของมันด้วย
- Promotion อ่านเฉพาะ training evidence เลือก feasible candidates สูงสุดสองตัวต่อ treatment/seed และบันทึก shortfall โดยไม่ยืม
- Preparation ใช้ campaign ID `PREP-FU-BMC-001` และ evidence class `preparation_only` ทำให้ rows ไม่สับสนกับ admitted evidence ของ `FU-BMC-001`

## บันทึกการตรวจสอบ

ทุกคำสั่งรันจาก `C:\Formula Ultimate` ด้วย Python 3.14

1. Focused runner tests หลัง harden identity/authorization:

   ```powershell
   py -3.14 -m unittest tests.test_campaign_runner -q
   ```

   Exit status: `0` ผลสำคัญ: `Ran 10 tests in 0.188s` และ `OK`

2. คำสั่ง preparation-only:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work056.ps1
   ```

   Exit status: `0` ผลสำคัญ: `status=passed`, `decision=runner_prepared_campaign_locked`, `execution_lock=rejected_as_expected`, `replay=exact`, `reservations=0`, `results=0`, `pending=0` และ `candidate_evaluations=0`

3. Focused integration และ repository-contract tests:

   ```powershell
   py -3.14 -m unittest tests.test_campaign_runner tests.test_main_campaign_protocol tests.test_whole_vehicle_search tests.test_repository_contract -q
   ```

   Exit status: `0` ผลสำคัญ: `Ran 27 tests in 0.868s` และ `OK`

4. Full test suite:

   ```powershell
   py -3.14 -m unittest discover -s tests -q
   ```

   Exit status: `0` ผลสำคัญ: `Ran 360 tests in 28.745s` และ `OK`

5. Python compilation:

   ```powershell
   py -3.14 -m compileall -q src scripts tests
   ```

   Exit status: `0` และไม่มี error output

Staged-scope checks, commit identity และ clean-tree replay บันทึกใน final handoff เพราะ commit hash ยังไม่เกิดจนกว่า result file นี้จะถูก stage

## Review discipline

หลักฐานสนับสนุน: tests ครอบคลุม exact ledger replay, one-time recovery ของ pending reservation, authorization lock ก่อน evaluator invocation, การ reject mutated/truncated/rehashed-invalid evidence, monotonic budget enforcement และ training-only per-stream promotion

หลักฐานที่ขัดแย้ง: ยังไม่ได้ใช้ external solver หรือจำลอง real process interruption Hash chain ไม่ใช่ external signature และ fixture behavior ยืนยัน storage durability ต่อ filesystem/hardware failure ทุกแบบไม่ได้

คำอธิบายทางเลือก: unit fixtures อาจไม่ครอบคลุม timing, process หรือ adapter failures ที่เกิดระหว่าง CalculiX/FreeCAD run ระยะยาว

หลักฐานที่ยังขาด: CalculiX evaluation adapter, STEP/FreeCAD finalist adapter, real interruption recovery, burn-in seed `55999`, burn-in acceptance, admitted main seeds, statistical analysis และ higher-fidelity physical validation

ความเชื่อมั่น: สูงว่า software contract ที่ implement เป็น deterministic และ fail closed ในกรณีที่ทดสอบ แต่ผลิต campaign-outcome evidence เป็นศูนย์

## งานถัดไป

Work 057 ควร implement และทดสอบ physical adapter boundary แล้วรันเฉพาะ excluded burn-in seed `55999` ภายใต้ explicit authorization แยกต่างหาก Admitted paired seeds ต้องล็อกต่อไปจนมีการ review และบันทึก burn-in acceptance
