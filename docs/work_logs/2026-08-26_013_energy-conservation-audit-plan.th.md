# แผน Work 013: Independent Energy-Conservation Audit

ต้นฉบับภาษาอังกฤษ: `2026-08-26_013_energy-conservation-audit-plan.md`

สถานะ: Completed

## วัตถุประสงค์

เพิ่ม audit โดเมน joule ที่เป็นอิสระบน graph ที่ compile จาก Work 012 โดยเทียบ
connection transfer ทุกเส้น, input/output ของทุก component, loss ที่ประกาศ และ
การเปลี่ยน stored energy แสดง residual ทั้งหมด และทำให้ hidden/double-counted
energy เป็น invalid

## ขอบเขตและสมการ

สำหรับแต่ละ component ในหนึ่งช่วงเวลา:

```text
r = E_in - E_out - E_loss - delta_E_stored
tolerance = absolute_tolerance_j + relative_tolerance * scale
```

`E_in`, `E_out`, `E_loss` เป็น joule ที่ไม่ติดลบ `delta_E_stored` มีเครื่องหมาย:
บวกคือเก็บพลังงานและลบคือปล่อย Scale คือขนาดที่มากที่สุดของเทอมที่ประกาศ Audit
ยังกำหนดให้ input/output ของ component เท่ากับผลรวม connection transfer ที่ตรง
กันภายใน scaled tolerance

- กำหนด contract เข้มงวดสำหรับ component balance, connection transfer,
  tolerance, violation และ audit result
- ต้องมีหลักฐานครบตรงกับ component/connection ของ compiled graph
- ตรวจ endpoint mismatch, hidden source/sink energy, transfer mismatch,
  component residual, duplicated loss, ค่า invalid และ replay drift
- Validate chain lossless/lossy และกรณีหักล้าง hidden-energy/double-loss
- เพิ่ม tests, validator, เอกสาร model/result สองภาษา และ commit แยก

## ไฟล์ที่วางแผน

- `src/formula_ultimate/physics/energy_audit.py`
- `src/formula_ultimate/physics/__init__.py`
- `scripts/validate_energy_audit.py`
- `tests/test_energy_audit.py`
- `docs/physics/ENERGY_CONSERVATION_AUDIT.md` และ `.th.md`
- สถานะ queue และคู่ plan/result สองภาษานี้
- problem report แยกสองภาษาเฉพาะเมื่อพบปัญหาที่มีสาระ

## นิยามการทดลอง

- สมมติฐาน: audit อิสระตรวจ energy creation หรือ loss ซ้ำที่ graph ถูก type แต่
  ตรวจเองไม่ได้
- Independent variables: joule ของ transfer, input/output/loss/storage change
  ที่ประกาศ และ tolerance
- Dependent variables: residual balance/interface ต่อ component, tolerance,
  violation, total residual และสถานะ valid/invalid
- Controls: compiled graph เดียวกัน, หน่วย SI joule, signed-storage convention,
  ลำดับ deterministic และ scaled tolerance
- การหักล้าง: chain lossless และ lossy ที่ประกาศต้องผ่าน; เพิ่ม output โดยไม่มี
  source/storage release และนับ loss ซ้ำต้องล้มเหลว; หลักฐานขาด/เกินต้องล้มเหลว;
  residual ต้องยังแสดง

## Validation

```powershell
python -m unittest tests.test_energy_audit -v
python -m unittest discover -s tests -v
python scripts/validate_energy_audit.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

## เกณฑ์สำเร็จ

Reference balance ปิดภายใน scaled tolerance; กรณีหักล้าง invalid; residual และ
violation ทั้งหมดสังเกตได้; validation ทั้งหมด, contract สองภาษา, staging แบบ
ระบุ, commit และ post-commit verification ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

Audit พีชคณิตพิสูจน์ไม่ได้ว่าสมการ component ต้นทางถูกต้อง ตรวจเฉพาะ energy ใน
ช่วงที่ประกาศ ไม่ใช่ instantaneous power integration, thermal state,
uncertainty propagation หรือ physical validation Work 014 ต้อง model thermal
state แยก ไม่มี implementation Work 014 หรือ remote push
