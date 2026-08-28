# รายงานปัญหา Work 022: การเก็บ Transaction Evidence

ต้นฉบับภาษาอังกฤษ: `2026-08-28_022_transaction-evidence-retention.md`

สถานะ: Resolved

## ปัญหา

การ review หลัง Work 022 validator ครั้งแรกผ่านพบว่า adapter residual และ event
candidate มีผลต่อ control flow และแสดง ID ใน trace แต่ raw `ResidualEntry` กับ
`EventCandidate` ไม่ถูกเก็บใน `CoupledStepResult` ดังนั้น failed residual หยุด
commit ถูกต้อง แต่ caller ตรวจค่าจริง, unit, tolerance และ event evidence หลัง
rollback ไม่ได้

## ผลกระทบ

Signal atomicity ยังถูกต้อง แต่ scientific auditability ไม่ครบ ซึ่งขัดกับกฎ
โครงการที่บังคับให้ conservation residual และ invalid state สังเกตได้ ไม่ถูกลด
เหลือ generic failure

## แผนการแก้

- เพิ่ม transaction-level residual/event collection แบบ immutable
- เก็บ evidence ทั้งหมดจนถึง module ที่ทำให้หยุดเมื่อ invalid
- `published_signals` ยังว่างสำหรับ invalid transaction ทุกกรณี; evidence ไม่ใช่
  partial state commit
- Reject residual/event ID ซ้ำข้าม module เพื่อให้ provenance ไม่กำกวม
- เพิ่ม regression test และ validator evidence ว่าเก็บ raw failed residual

## Validation

Result ที่แก้แล้วเก็บ residual `force-x` ค่าดิบ `2.0 N` และ tolerance `0.1 N`
ขณะที่ `published_signal_count` ยังเป็น `0` และ rollback คืน start state ตรงเดิม

```powershell
python -m unittest tests.test_coupled_transaction -v
# Ran 11 tests ... OK (exit 0)

python -m unittest discover -s tests -v
# Ran 177 tests ... OK (exit 0)

python scripts/validate_coupled_transaction.py
# residual retained; rollback true; published signals 0; exit 0

python -m compileall -q src scripts tests
# exit 0
```
