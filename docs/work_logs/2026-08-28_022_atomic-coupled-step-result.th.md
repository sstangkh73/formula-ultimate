# ผลลัพธ์ Work 022: Atomic Coupled-Step Transaction

ต้นฉบับภาษาอังกฤษ: `2026-08-28_022_atomic-coupled-step-result.md`

สถานะ: Completed

## ผลลัพธ์

Work 022 สร้าง atomic adapter transaction ระหว่าง architecture จาก Work 021 กับ
domain physics ในอนาคต Adapter execute ตาม compiled order, รับเฉพาะ copied input
ที่ประกาศ, เขียน output ตรงตาม declaration และ publish complete state หนึ่งชุด
หลัง module แปดตัวกับ final-state check ผ่านทั้งหมด ทุก failure rollback ไปยัง
immutable start state เดิมและ publish candidate signal ศูนย์

นี่คือ generic transaction boundary Validator execute domain physics adapter
ศูนย์ตัว และไม่อ้าง whole-vehicle หรือ physical validation

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/simulation/transaction.py`: runtime signal isolation,
  adapter protocol, trace/evidence, preflight, atomic execution และ rollback
- `src/formula_ultimate/simulation/__init__.py`: public Work 022 export
- `tests/test_coupled_transaction.py`: focused success/falsification test 11 รายการ
- `scripts/validate_coupled_transaction.py`: deterministic reference/fault evidence
- `docs/simulation/ATOMIC_COUPLED_STEP.md` และ `.th.md`: model contract
- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.md` และ `.th.md`: ปิด
  Work 022
- คู่ plan/result สองภาษานี้
- `docs/problem_reports/2026-08-28_022_transaction-evidence-retention.md` และ
  `.th.md`: ปัญหาการเก็บ evidence ที่แก้แล้ว

## การตัดสินใจ

- Copy runtime payload ตอน ingress และทุก declared read
- Preflight signal/adapter coverage และ model-version pin ให้ตรงก่อนเรียก adapter
- ให้ compiled architecture order เหนือ registration order
- Successful adapter เขียน complete declared set ตรงพอดี; invalid adapter เขียน
  ศูนย์และให้ nonblank reason
- Buffer signal ภายในตลอดทั้ง step
- เก็บ raw residual/event แยกจาก state publication รวม evidence จนถึง stopping
  module หลัง rollback
- บังคับ evidence ID unique ทั้ง step และ `state.next` typed/ไม่ถอยหลัง

## ปัญหาที่พบและการแก้

Implementation แรกใช้ residual/event evidence คุม flow แต่ไม่เก็บ raw record ใน
step result รายงานปัญหาแยกบันทึก auditability defect นี้แล้ว ปัจจุบัน
`CoupledStepResult` เก็บ raw evidence ทั้ง success/failure, reject ID ซ้ำข้าม
module และยัง publish signal ศูนย์เมื่อ invalid Regression evidence เก็บ
`force-x = 2.0 N` พร้อม tolerance `0.1 N`

## Validation

รันคำสั่งจาก `C:\Formula Ultimate` เมื่อ 2026-08-28 พร้อม fail-fast handling

```powershell
python -m unittest tests.test_coupled_transaction -v
# exit 0; Ran 11 tests in 0.023s; OK

python -m unittest discover -s tests -v
# exit 0; Ran 177 tests in 0.528s; OK

python scripts/validate_coupled_transaction.py
# exit 0
# architecture fingerprint:
# 51ca53e9d4c6058f67f61dc57f3ece7e8c24176d915e74069f27d0aa6999f8a6
# reference status: committed; trace count: 8; published signals: 21
# state: 4.0 -> 4.01 s; 100.0 -> 100.3 m
# reversed registration replay: equal
# injected preflight/adapter/residual/time faults: rollback true, outputs 0
# retained failed residual: force-x = 2.0 N; tolerance = 0.1 N
# domain_physics_adapter_count: 0

python -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

ตรวจ staged scope และ commit ขั้นสุดท้ายหลัง stage result record นี้

## การทบทวนการทดลอง

- Supporting evidence: replay ตรงเมื่อกลับ registration; trace แปดตัวตาม compiled
  order; publish 21 output เฉพาะ success; fault ด้าน preflight, undeclared read,
  write set, exception, invalid output, residual และ final state fail-closed
- Contradicting evidence: ไม่พบภายในสมมติฐาน generic atomicity
- Alternative explanation: state advance ที่ผ่านเกิดจาก placeholder adapter โดย
  ตั้งใจ ไม่ใช่สมการฟิสิกส์
- Missing evidence: typed circuit/environment input และ physical transfer ข้าม
  domain ทั้งหมด
- Confidence: สูงสำหรับ transaction contract ที่ test; ไม่เปลี่ยนสำหรับ physical
  vehicle accuracy

## ข้อจำกัดและงานถัดไป

งานนี้ยังไม่ couple domain solver Work 023 เป็นงานถัดไป ต้องสร้าง typed,
deterministic circuit/environment/weather/traffic/strategy input สำหรับ real-circuit
profile สิบสนาม โดย missing evidence ต้องแสดงชัด

ไม่มีการ push หรือเผยแพร่ remote
