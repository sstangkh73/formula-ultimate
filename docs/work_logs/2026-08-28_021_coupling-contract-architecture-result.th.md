# ผลลัพธ์ Work 021: Coupling Contract และ Architecture Compiler

ต้นฉบับภาษาอังกฤษ: `2026-08-28_021_coupling-contract-architecture-result.md`

สถานะ: Completed

## ผลลัพธ์

Work 021 สร้าง boundary กลางตัวแรกที่ execute ได้สำหรับ coupled vehicle
simulation ในอนาคต ประกอบด้วย deterministic architecture compiler, experiment
manifest ที่ pin ค่า, shared runtime state แบบ topology-neutral, residual ledger
ที่สังเกตได้ และ deterministic event arbitration พร้อมบันทึกคิว Work 021–030
ตามลำดับ

นี่คือผลลัพธ์ระดับ contract และ architecture เท่านั้น รัน vehicle-physics module
จำนวนศูนย์ และไม่ใช่หลักฐานว่ามี coupled vehicle หรือ physical validation แล้ว

## ไฟล์ที่เปลี่ยน

- `config/simulation/coupled_level0_architecture_v1.json`: reference architecture
  แปด stage แบบ versioned
- `src/formula_ultimate/simulation/coupling.py`: contract, compiler, manifest,
  shared state, residual ledger และ event arbitration
- `src/formula_ultimate/simulation/__init__.py`: public coupling export
- `tests/test_coupling_contracts.py`: focused contract/falsification test 12 รายการ
- `scripts/validate_coupling_contracts.py`: ตัวสร้าง deterministic evidence
- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.md` และ `.th.md`:
  คิว Work 021–030 ตามลำดับ
- `docs/simulation/COUPLING_CONTRACT_AND_ARCHITECTURE.md` และ `.th.md`:
  เอกสาร architecture และ claim boundary
- คู่ plan/result สองภาษานี้
- `docs/problem_reports/2026-08-28_021_json-loader-type-coercion.md` และ
  `.th.md`: ปัญหา loader ที่แก้แล้วและหลักฐาน

## การตัดสินใจ

- ใช้ causal stage แปดลำดับ: `inputs`, `aerodynamics`, `load_balance`,
  `contact_limits`, `motion`, `energy_audit`, `health` และ `race_progress`
- ทุก consumed signal ต้องเป็น initial signal หรือมี producer เดียวใน stage ที่
  ก่อนหน้าอย่างเคร่งครัด
- Canonicalize declaration ก่อน SHA-256 hashing เพื่อไม่ให้ input order ของ
  module เปลี่ยน architecture/experiment identity
- เก็บ contact และ component-health record เป็น collection ที่มี unique ID จำนวน
  ใดก็ได้ โดยไม่ encode โครงรถสี่ล้อ, axle, body หรือ powertrain
- เก็บ residual value ตรงตามจริงและแสดง invalidity แทนการแก้ conservation error
  อย่างเงียบ
- ตัดสิน simultaneous event ด้วย priority ที่ประกาศ หลังหา earliest time ภายใน
  tolerance คงที่
- JSON schema/type error ทุกตัวเป็น invalid declaration ไม่ใช่ค่าที่ควร coerce

## ปัญหาที่พบและการแก้

Implementation แรกที่ผ่าน test ใช้ `str(...)` coerce ค่า JSON หลายจุด การ review
พบว่า `architecture_id` แบบตัวเลขอาจถูกยอมรับเป็น string รายงานปัญหาแยกบันทึก
ข้อบกพร่องนี้แล้ว เปลี่ยนเป็นตัวอ่าน JSON string/string-array แบบ strict และเพิ่ม
regression test ที่บังคับ numeric ID ให้เกิด `CouplingContractError` ทุก gate ผ่าน
หลังการแก้

## หลักฐานและ Validation

รันคำสั่งจาก `C:\Formula Ultimate` เมื่อ 2026-08-28 พร้อม fail-fast exit handling

```powershell
python -m unittest tests.test_coupling_contracts -v
# exit 0; Ran 12 tests in 0.030s; OK

python -m unittest discover -s tests -v
# exit 0; Ran 166 tests in 0.445s; OK

python scripts/validate_coupling_contracts.py
# exit 0
# architecture fingerprint:
# 51ca53e9d4c6058f67f61dc57f3ece7e8c24176d915e74069f27d0aa6999f8a6
# manifest fingerprint:
# 7f40394bf539ef230870a758cfba81c093268d38f52c7efac359fdd9ec5fb416
# input_permutation_equal: true
# contact_count: 3
# residual status: invalid; raw_energy_residual_j: -2.0
# exact event tie winner: finished
# physics_execution_count: 0

python -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

ตรวจ staged scope ขั้นสุดท้ายและ commit verification หลัง stage result record นี้
ตาม repository protocol

## การทบทวนการทดลอง

- Supporting evidence: architecture/manifest fingerprint ไม่เปลี่ยนตาม declaration
  order; reference ครบแปด stage; รับ arbitrary three-contact state; invalid
  dependency, hash, contact, residual, event และ JSON type แสดงชัดเจน
- Contradicting evidence: ไม่พบภายในสมมติฐานระดับ contract ที่ประกาศ
- Alternative explanation: ผล deterministic มาจาก schema canonicalization และ
  ไม่ได้แสดงว่าสมการฟิสิกส์ถูกต้อง
- Missing evidence: adapter, atomic state transition, การแลก force/energy ข้าม
  domain, numerical convergence, integrated race สิบสนาม และ higher-fidelity
  validation
- Confidence: สูงว่า central contract ทำงานตาม test; ไม่เพิ่มความมั่นใจด้าน
  whole-vehicle physical accuracy

## ข้อจำกัดและงานถัดไป

Signal name ยังไม่มี executable unit/semantic adapter ดังนั้น Work 022 เป็นงาน
ถัดไป: สร้าง atomic coupled-step transaction ให้ module อ่าน immutable start
state ชุดเดียว แล้ว commit complete next state หนึ่งชุด หรือคืน observable invalid
result โดยไม่มี partial mutation

ไม่มีการ push หรือเผยแพร่ remote
