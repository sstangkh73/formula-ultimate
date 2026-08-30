# แผนงาน 056: Campaign runner และ append-only ledgers

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_056_campaign-runner-ledger-plan.md`

## วัตถุประสงค์

implement deterministic resume-safe orchestration core ที่ Work 055 campaign ต้องใช้ โดยยังไม่รัน burn-in หรือ admitted main seed ตัวใด Runner ต้อง consume opportunity ก่อน evaluation, เก็บ candidate/RNG/ancestry identity, append budget/result records แบบตรวจการแก้ไขได้, reconstruct state หลัง interruption อย่าง exact, เลือก training promotions สูงสุดสองแบบต่อ treatment/seed และปฏิเสธ main execution จนกว่า work item ถัดไปจะให้ physical adapters และ burn-in authorization ที่ validate แล้ว

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม campaign-runner state, chained JSONL ledger, resume/replay, promotion และ stage-transition contracts ใต้ `src/formula_ultimate/experiments/`
- เพิ่มคำสั่ง preparation/verification ของ Work 056 และ `scripts/run_work056.ps1` ซึ่ง initialize/verify ignored workspace ว่างใต้ `artifacts/work056/` ได้ แต่ต้องรายงาน `candidate_evaluations=0`
- เพิ่ม focused tests ด้วย synthetic callback results และ temporary ledgers Fixture opportunities เป็น software tests ไม่ใช่ Work 055 campaign observations และเข้า campaign evidence ไม่ได้
- เพิ่มเอกสาร runner/ledger สองภาษา และ result records สองภาษา

## สัญญาของ runner

- `budget_ledger.jsonl` reserve และ consume attempt ก่อน evaluation พร้อมเก็บ full candidate declaration ที่ใช้ recovery แบบ deterministic
- `result_ledger.jsonl` เก็บ terminal training resultหนึ่งรายการต่อ reserved attempt การ crash หลัง reservation ทิ้ง pending attempt ที่มองเห็นได้ Resume ต้อง reconstruct candidate เดิมและ complete ได้เฉพาะ reservation เดิมหนึ่งครั้ง
- ทุก row มี protocol/campaign identity, monotonic sequence, previous-row SHA-256, payload และ record SHA-256 หาก truncate, mutate, duplicate result, skip attempt, treatment/seed drift หรือ cross-ledger mismatch ต้อง fail closed
- runner rebuild agent แต่ละตัวด้วย proposal/observation order เปรียบเทียบ candidate identity และ RNG checkpoint แล้ว resume จาก incomplete reservation แรก
- promotion selectionอ่านเฉพาะ terminal training-feasible records เรียง training objective แล้ว candidate ID จำกัดสองแบบต่อ treatment/seed และบันทึก shortfall โดยไม่ยืม
- Main seeds และ burn-in seed ถูก execution-lock ใน Work 056 นอก tests อนุญาตเฉพาะคำสั่ง `prepare`/`verify`

## การตรวจสอบ

1. พิสูจน์ chained-ledger replay, append, restart และ fingerprint แบบ exact
2. จำลอง interruption หลัง reservation และตรวจว่า candidate เดิม complete หนึ่งครั้งโดยไม่เพิ่ม budget
3. reject altered/truncated row, previous hash ผิด, duplicate/unreserved result, skipped attempt, RNG/candidate เปลี่ยน, seed/treatment drift และ cross-seed promotion borrowing
4. ตรวจ equal planned budget และ GRID mapping ไม่ซ้ำจาก Work 055 protocol โดยทำ campaign evaluations เป็นศูนย์
5. รัน focused/full tests, compilation, repository contract, staged checks แบบ fail-fast, explicit scoped commit และ clean-tree Work 056 replay

## เกณฑ์สำเร็จ

- runner mechanics และ append-only ledgers deterministic และ fail closedใน negative fixtures ทุกตัว
- คำสั่ง Work 056 คืน `runner_prepared_campaign_locked`, exact replay และ `candidate_evaluations=0`
- artifact จาก unit fixture ต้องไม่ถูกสับสนกับ `FU-BMC-001` campaign evidence
- ไม่มี admitted หรือ burn-in seedถูกประเมิน

## เกณฑ์ล้มเหลว

หยุดหาก interrupted attempt หายหรือ consume สองครั้ง, รับ ledger ที่ถูกแก้, resume สร้าง candidate ต่าง, promotion อ่าน holdout/refined data หรือคำสั่ง Work 056 ใดรัน main/burn-in seedได้

## ความเสี่ยงและสิ่งที่ไม่ทำ

filesystem append พร้อม `flush/fsync` ลดแต่ไม่กำจัด storage/hardware failure Hash chain ตรวจ corruption แต่ไม่ใช่ external signature Work 056 ไม่ implement CalculiX/STEP/FreeCAD campaign adapters, ไม่รัน burn-in, ไม่รัน main campaign, ไม่ทำ statistical analysis, ไม่เปลี่ยน Work 055 rules, ไม่ push หรือ publish
