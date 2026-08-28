# แผน Work 022: Atomic Coupled-Step Transaction

ต้นฉบับภาษาอังกฤษ: `2026-08-28_022_atomic-coupled-step-plan.md`

สถานะ: Completed

## วัตถุประสงค์

สร้าง adapter execution และ transaction boundary สำหรับรัน compiled coupling
architecture หนึ่ง step แบบ atomic ทุก adapter ต้องเห็นเฉพาะ immutable input ที่
ประกาศ คืน output ตรงกับที่ประกาศ และสร้าง committed `state.next` ที่สมบูรณ์หนึ่ง
ชุด หรือคง start state เดิมพร้อม invalidity evidence ที่ชัดเจน

## ขอบเขต

- กำหนด immutable runtime signal value และ read view ที่จำกัดตาม `consumes`
  ของแต่ละ module
- กำหนด adapter output, trace, failure และ step-result record
- Validate initial-signal และ adapter coverage ให้ตรงพอดีก่อน execute
- Execute adapter ตาม compiled architecture order เท่านั้น
- Reject write ที่หาย, เกิน, ซ้ำ หรือผิดรูป; adapter identity ไม่ตรง; exception;
  adapter status ผิด; และ final state ผิด
- Buffer candidate output ทั้งหมดภายในและเปิดเผยหลัง step สำเร็จครบเท่านั้น
- บังคับ `state.next` เป็น `SharedVehicleState` ที่ time/race distance ไม่ถอยหลัง
- เพิ่ม focused falsification test, deterministic validator, เอกสาร model/result
  สองภาษา, อัปเดต queue และ verified commit หนึ่งชุด

## ไฟล์ที่วางแผน

- `src/formula_ultimate/simulation/transaction.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_coupled_transaction.py`
- `scripts/validate_coupled_transaction.py`
- `docs/simulation/ATOMIC_COUPLED_STEP.md` และ `.th.md`
- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.md` และ `.th.md`
- คู่ plan/result สองภาษานี้
- problem report สองภาษาแยก หากพบปัญหาสำคัญ

## นิยามการทดลอง

- สมมติฐานหลัก: ordered transaction ทำให้ partial/undeclared adapter update ทุก
  ตัวสังเกตได้ และ commit complete next state เพียงหนึ่งครั้งเมื่อทุก module ผ่าน
- Independent variables: adapter order, identity, read/write declaration,
  returned output/status, exception, initial signal coverage และ final state
- Dependent variables: transaction status, committed state, failure module/reason,
  trace length/order และ published output set
- Controls: compiled architecture จาก Work 021, immutable start state, private
  candidate signal buffer, declared output equality และ deterministic module order
- Success criteria: reference transaction แปด adapter deterministic commit หนึ่ง
  ครั้ง; adapter เห็นเฉพาะ input ที่ประกาศ; fault ที่ inject ทุกตัว rollback โดย
  คืน state เดิมและไม่ publish candidate output
- Failure criteria: partial output มองเห็นได้, start state เปลี่ยน, undeclared/
  missing write ผ่าน, execute ต่อหลัง fail, adapter order เปลี่ยน หรือ commit next
  state ที่ผิด/ถอยหลัง
- Falsification: permute adapter registration, ลบ/เพิ่ม adapter หรือ initial
  signal, คืน output หาย/เกิน/ซ้ำ, throw exception, invalidity กลาง pipeline และ
  คืน `state.next` ผิด type หรือถอยหลัง

## ความเสี่ยง

- Immutability ของ Python เป็น contract boundary ไม่ใช่ hostile-code sandbox;
  adapter ยังเป็น trusted repository code
- Generic payload สร้าง atomicity/provenance แต่ยังไม่พิสูจน์ physical unit หรือ
  semantics; Work 023–027 เป็นเจ้าของ typed domain adapter
- Reference pipeline แบบ no-op ที่ผ่านพิสูจน์ transaction behavior เท่านั้น ไม่ใช่
  vehicle physics

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่มี circuit, aero, contact, motion, energy, thermal, health หรือ race physics
  coupling; ไม่มี whole-race loop; optimizer/CAD/CFD/FEA; physical-validation
  claim; README change หรือ remote push

## Validation

```powershell
python -m unittest tests.test_coupled_transaction -v
python -m unittest discover -s tests -v
python scripts/validate_coupled_transaction.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

การเสร็จต้องผ่านทุก gate, เอกสารสองภาษาตรงกัน, staged scope ชัดเจน, commit สำเร็จ
และยืนยัน clean state/hash หลัง commit
