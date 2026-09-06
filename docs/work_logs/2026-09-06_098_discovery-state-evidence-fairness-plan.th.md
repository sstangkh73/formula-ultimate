# แผน Work 098: Contract สถานะ หลักฐาน และความเป็นธรรมของการค้นหา

ต้นฉบับภาษาอังกฤษ: `2026-09-06_098_discovery-state-evidence-fairness-plan.md`

วันที่: 2026-09-06 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และหลักฐานเริ่มต้น

Implement software contract ของ Work 098 ตาม `WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md` โดยเริ่มจาก revision `7afb91e` ที่สะอาด เก็บ benchmarks ประวัติ Work 095/097 และ campaign runner เดิมโดยไม่เปลี่ยน เป็นงาน software contract ไม่ใช่ physical model ใหม่หรือ admitted discovery experiment

## ขอบเขตและไฟล์ที่วางแผน

- `src/formula_ultimate/experiments/discovery_registration.py`: ตรวจ registration ที่มี version, coverage และ budget แบบเข้มงวด immutable identity และ admission boundary
- `src/formula_ultimate/experiments/discovery_evidence.py`: candidate/context identity, orthogonal states, scoped evidence, exploratory/promotion admission และ legacy adapters ที่ไม่อ้างเกินหลักฐาน
- `src/formula_ultimate/experiments/discovery_ledger.py`: append-only event ledger, deterministic reduction/replay, candidate ancestry และกฎ reserve/settle/recovery/cache
- `src/formula_ultimate/experiments/discovery_audit.py`: deterministic stratified sampling, inclusion probabilities, proxy error accounting แยก strata, selection และ numerical replay comparison
- `config/experiments/discovery_contract_fixture_v1.json`: software registration ครบที่ประกาศชัดว่า synthetic ไม่ใช่ admitted campaign
- `scripts/experiments/run_discovery_contract.py`: mixed-ledger fixture ที่ execute ได้และ exact replay evidence พร้อมจัดการ output อย่างปลอดภัย
- `tests/test_discovery_contract.py`: adversarial acceptance cases และ integration/resume coverage
- `docs/contracts/DISCOVERY_STATE_EVIDENCE_FAIRNESS_V1.md` และ `.th.md`: interface ที่ implement คำสั่ง acceptance mapping และข้อจำกัด
- แผนสองภาษานี้และผลสองภาษาที่ตรงกัน เก็บ generated evidence ใต้ ignored `artifacts/work098/`

## ข้อตัดสินใจที่จะตรวจสอบ

- แยกสถานะตาม representation, boundary, physics domain/fidelity, manufacturing process และ intended use เก็บ attempts ก่อนหน้าแทนการเขียนทับ failures
- ผูกหลักฐานกับ causal identities ทั้งหมดและ frozen registration Fixtures ห้ามเข้า scientific survivor counts ระบุ trusted evaluator provenance ชัด hash ยืนยัน integrity ไม่ใช่ความจริงทางฟิสิกส์
- Implement แบบ single-writer และ serial scheduling ที่จำกัดขอบเขต แบ่งทรัพยากรตาม treatment/seed และ budget pool จองก่อน operation คิดต้นทุน retries/ผลที่หาย และเก็บ overshoot เป็นเงื่อนไขหยุด campaign ไม่อ้างว่ามี watchdog ฆ่า process หรือ distributed execution
- ระบุ numerical requirements ของ registration ชัด ตัวเลข synthetic fixture ใช้ทดสอบซอฟต์แวร์เท่านั้น Declaration ที่ไม่ครบหรือเปลี่ยนห้าม execute ภายใต้ registration identity เดิม
- แยก exact decision replay จาก numerical execution comparison ส่วน audit reference labels ที่ไม่ทราบยังคงไม่ทราบ รายงาน rates แยก strata พร้อม inclusion probabilities และข้อมูล uncertainty

## Validation และเกณฑ์สำเร็จ

1. รัน `python -m unittest tests.test_discovery_contract -v` ครอบคลุม acceptance requirements ทั้ง 10 ข้อใน governing protocol รวม negative promotion, stale identity, tampering, crash/retry, cache, budget, score-independent audit และ legacy semantics
2. รัน targeted regressions: `python -m unittest tests.test_constructive_validity tests.test_generalized_geometry_benchmarks tests.test_campaign_runner tests.test_repository_contract -q`
3. Execute fixture runner สองครั้งใน artifact directories แยกกัน และเทียบ deterministic ledger/report hashes เปิด ledger ใหม่และตรวจ replay/recovery ใน tests ข้อมูล fixture ไม่ใช่ admitted science
4. รัน `python -m compileall -q src scripts tests` และ `python -m unittest discover -s tests -q` เป็น final regression gates บันทึก failures และ environment-dependent skips ในผล
5. ตรวจไฟล์สองภาษา รัน `git diff --check` ตรวจ staged scope ที่ระบุชัด รัน `git diff --cached --check` commit เฉพาะงานนี้ และรายงาน hash ที่ตรวจแล้ว

สำเร็จเมื่อ state/accounting/admission execute ได้จริงพร้อม falsification tests และ replay artifacts ไม่ใช่เพียง schema labels หรือ ledger ที่เขียนมือ Gate ที่ล้มเหลวหยุด commit หากพบ blocker ที่ไม่คาดต้องคงงาน `In progress` หรือ `Stopped` พร้อมเหตุผลตรงจริง

## ความเสี่ยง การควบคุม และสิ่งที่ไม่ทำ

ความเสี่ยง: synthetic evidence ปลอมเป็นฟิสิกส์ metadata ผิดเปลี่ยน result class งาน retry/cache ไม่ถูกคิดต้นทุน admission ไม่ครบ และอ้าง hash-chain security เกินจริง ควบคุมด้วย evidence classes/causal identities เข้มงวด frozen rules, adversarial tests, cost recovery ชัด ตรวจ trusted checkpoints และอธิบาย provenance boundary

ไม่ทำ Works 099–101, morphology/CAD/field-solver implementation, physical laws ใหม่, statistical discovery conclusions, optimized race comparison, unrestricted concurrency, external publication หรือ push ไม่วางแผนแก้ governing protocol ลงวันที่หรือ backups ของมัน
