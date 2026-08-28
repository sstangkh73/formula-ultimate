# แผน Work 021: Coupling Contract และ Architecture Compiler

ต้นฉบับภาษาอังกฤษ: `2026-08-28_021_coupling-contract-architecture-plan.md`

สถานะ: Completed

## วัตถุประสงค์

สร้าง central contract ตัวแรกที่ execute ได้สำหรับ coupled-vehicle program:
versioned experiment manifest, shared vehicle state แบบ topology-neutral,
deterministic physics-stage architecture compiler, residual ledger และ event
arbitration พร้อมสร้างคิว integration Work 021–030 ตามลำดับ งานนี้กำหนดและ
validate coupling boundary; ยังไม่ execute physics solver อิสระ Work 011–019
เป็นรถคันเดียว

## ขอบเขต

- ลิสต์ Work 021–030 ใน sequential implementation queue สองภาษา พร้อม completion
  gate ต่อรายการ
- กำหนด causal stage order กลางจาก environment input ผ่าน aero, load balance,
  contact, motion, energy, health จน race progress
- กำหนด module declaration ที่มี version, consumed signal และ produced signal;
  compile input order ใดๆ เป็น execution order deterministic
- Reject missing producer, duplicate output, same/later-stage dependency,
  duplicate identity, required stage ที่หาย และ JSON ผิดรูป
- กำหนด immutable experiment manifest ที่ pin candidate/design language,
  geometry hash, catalog, circuit/regulatory/energy/solver profile, architecture
  fingerprint, source commit, seed, timestep และ evaluation budget พร้อมสร้าง
  deterministic SHA-256 identity
- กำหนด shared vehicle state แบบ topology-neutral ที่มี contact/component-health
  collection จำนวนใดก็ได้ พร้อม SI/numerical contract เข้มงวด
- กำหนด residual entry/ledger โดยไม่แก้เงียบ และ deterministic event arbitration
  ที่มี tie priority/tolerance ประกาศ
- เพิ่ม versioned reference architecture configuration ที่ map Level-0
  capability เดิมเข้าสู่ coupling order ในอนาคต
- เพิ่ม test, validator, เอกสาร model/result สองภาษา, problem report สองภาษาแยก
  ทุกปัญหาที่พบ และ commit ที่ยืนยันแล้วหนึ่งชุด

## ไฟล์ที่วางแผน

- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.md` และ `.th.md`
- `docs/simulation/COUPLING_CONTRACT_AND_ARCHITECTURE.md` และ `.th.md`
- `config/simulation/coupled_level0_architecture_v1.json`
- `src/formula_ultimate/simulation/coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_coupling_contracts.py`
- `scripts/validate_coupling_contracts.py`
- คู่ plan/result สองภาษานี้
- problem report สองภาษาแยกสำหรับปัญหาที่พบ

## ขอบเขต Work 021

Compiler ตรวจ explicit signal provenance และ stage ordering แต่ไม่เรียก physics
module หรืออ้างว่า unit/interface ถูก adapt แล้ว Reference architecture เป็น
coupling specification ไม่ใช่ integrated simulation result

Shared state รองรับ contact state set ที่ไม่ว่างและมี unique ID จำนวนใดก็ได้ รวม
component-health set ที่มี unique ID โดยไม่บังคับสี่ล้อ, paired axle, conventional
body หรือ powertrain type

## นิยามการทดลอง

- สมมติฐานหลัก: central typed contract ทำให้ physics dependency ที่หาย, ซ้ำ หรือ
  กลับ causal order fail ก่อนเรซ ขณะที่ declaration เดิม compile/fingerprint ตรงกัน
  ไม่ว่า input order เป็นอย่างไร
- Independent variables: module declaration/order, signal dependency, manifest
  identity/hash/profile/seed/budget/timestep, shared state, residual value/
  tolerance และ event candidate time
- Dependent variables: compiled module order/fingerprint, manifest fingerprint,
  contract acceptance/rejection, residual status/failed ID และ event decision
- Controls: canonical eight-stage order, dependency ต้องมาจาก stage ก่อนหน้า,
  SI state field, SHA-256 canonical serialization, event priority คงที่ และไม่รัน
  physics solver หรือ stochastic draw
- Metrics: replay equality, permutation invariance, stage coverage ของ reference,
  invalid dependency coverage, state validation, residual visibility, event-time/
  priority correctness, repository gate และ commit
- Success: reference architecture load/compile deterministic; invalid case ทุก
  ตัว fail; arbitrary three-contact state ผ่าน; residual เกิน tolerance สังเกตได้;
  event tie deterministic; repository gate ทั้งหมดผ่าน
- Failure criteria: hidden producer, duplicate signal, causal reversal,
  architecture/manifest nondeterminism, รับ invalid state, แก้ residual, event
  winner กำกวม, bilingual mismatch หรือ commit fail
- Falsification: permute module, ลบ producer/stage, output ซ้ำ, consume จาก same/
  later stage, hash เสีย, contact ซ้ำ, บังคับ residual fail และ exact event tie

## ความเสี่ยง

- Central schema อาจกลายเป็นข้อบังคับ conventional car หาก encode wheel count,
  axle layout หรือ powertrain component แบบตายตัว
- Signal name อย่างเดียวไม่พิสูจน์ unit/semantic compatibility งาน adapter ถัดไป
  ต้องกำหนด executable typed payload
- Architecture graph deterministic ยังเชื่อมสมการผิดทางฟิสิกส์ได้ Work 022–030
  ต้องทดสอบ transaction, conservation, integration, numerical refinement และ
  higher-fidelity promotion

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่มี coupled physics step, complete vehicle, whole-race integrated result,
  autonomous search, optimizer, CAD generation, CFD, FEA, calibration, README
  rewrite, remote push หรือ physical-validation claim
- ไม่อ้างว่า reference architecture ทำให้ Work 011–019 แลก real state/energy แล้ว

## Validation

```powershell
python -m unittest tests.test_coupling_contracts -v
python -m unittest discover -s tests -v
python scripts/validate_coupling_contracts.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

ทุก gate รัน fail-fast การเสร็จต้องมี queue/model/result สองภาษาตรงกัน, problem
report ที่จำเป็น, stage แบบ explicit, commit สำเร็จ และหลักฐาน hash/clean-state
หลัง commit
