# ผลงาน 028: Whole-Race Coupled Orchestrator

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_028_whole-race-coupled-orchestrator-result.md`

## ผลลัพธ์

สร้าง deterministic whole-race Level-0 orchestrator ที่ execute coupled architecture ครบแปด stage ผ่าน atomic transaction จน finish, energy depletion, physical failure, timeout, invalidity หรือ evaluation budget หมด โดย attempted step ทุกครั้งเก็บ replay identity, numerical evidence, transaction trace และ terminal provenance

## ไฟล์ที่เปลี่ยน

- เพิ่ม `config/simulation/coupled_level0_architecture_v4.json`
- เพิ่ม `src/formula_ultimate/simulation/whole_race.py` และ export public contract จาก `src/formula_ultimate/simulation/__init__.py`
- เพิ่ม `tests/test_whole_race.py` และ `scripts/validate_whole_race.py`
- เพิ่ม invariant ระยะ state/scenario ใน `src/formula_ultimate/simulation/step_inputs.py`, test และ validator
- แก้ exact-end depletion และ residual publication ownership ใน `src/formula_ultimate/simulation/energy_health_coupling.py`
- เพิ่มเอกสารโมเดล whole-race สองภาษา, plan/result คู่นี้, problem report สองภาษาห้าเรื่อง และอัปเดต coupled implementation queue

## ปัญหาที่แก้

1. ระยะ scenario อาจไม่ตรงกับ shared start state
2. race-progress stage ขาด `state.current` ใน compiled signal graph
3. energy depletion ที่ปลาย requested step แบบ exact ไม่สร้าง depletion event
4. health adapter ส่ง energy residual ID ที่ energy adapter เป็นเจ้าของซ้ำ
5. standalone validator ใช้ floating-point `0.0` แทน integer traffic count

ทุกปัญหามีรายงานภาษาอังกฤษและไทยแยกใน `docs/problem_reports`

## การตัดสินใจ

- เก็บ architecture v1-v3 และเพิ่ม v4 ที่ใช้ `work028-race-progress-v1`
- ให้ adapter registration เป็นอิสระจาก compiled execution order
- สร้าง adapter ที่ขึ้นกับ duration ใหม่จาก committed state ล่าสุดทุก step
- merge motion, energy, health, finish, timeout และ step-complete candidate ผ่าน deterministic event arbitrator ร่วม
- เก็บ exact-time tie ให้สังเกตได้พร้อม commit สถานะเดียวแบบ deterministic
- publish residual ID เฉพาะจาก adapter ที่เป็นเจ้าของ
- ถือว่า evaluation budget หมดเป็น timeout outcome พร้อมเหตุผล `evaluation budget exhausted` ที่ชัดเจน
- เก็บ telemetry ของ attempted step ที่ invalid โดยไม่มี end-state identity หรือ partial state advance

## ผลการทดลองและการพยายามหักล้าง

- ตัวแปรอิสระที่ทดลอง: initial energy, auxiliary draw, central heat, timeout, evaluation budget, corridor width, seed และลำดับ adapter registration
- หลักฐานตัวแปรตาม: outcome, terminal time/state, จำนวน committed step, residual, event ledger, state/input fingerprint, trace และ replay fingerprint
- ตัวควบคุม: architecture fingerprint, model version แปดชุด, fixed four-contact topology, zero-aero analytical map, straight corridor, timestep `1 s`, start speed `10 m/s` และ seed คงที่
- การหักล้างสมมติฐานที่ต้องการ: depletion, thermal failure, timeout, invalid corridor, adapter หาย, budget หมด, exact finish/depletion tie และ reversed registration ให้ผลที่ประกาศและสังเกตได้ทั้งหมด
- หลักฐานขัดแย้ง: ไม่พบภายใน analytical fixture
- คำอธิบายทางเลือก: exact replay พิสูจน์ deterministic implementation ไม่ใช่ความแม่นยำต่อโลกจริง
- หลักฐานที่ขาด: measured ten-circuit local geometry/weather, calibrated model, numerical refinement, uncertainty และ higher-fidelity validation
- ความมั่นใจ: สูงสำหรับ deterministic software contract ที่ประกาศ; ต่ำสำหรับ real-race prediction เพราะอยู่นอกหลักฐาน Work 028

## คำสั่งและหลักฐาน validation

คำสั่งทั้งหมดคืน exit status `0`:

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_step_inputs tests.test_energy_health_coupling tests.test_whole_race -v
python -m unittest discover -s tests
python scripts/validate_step_inputs.py
python scripts/validate_energy_health_coupling.py
python scripts/validate_whole_race.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

- focused regression Work 023/027/028: ผ่าน 29 รายการใน `0.291 s`
- test suite ทั้ง repository: ผ่าน 240 รายการใน `0.742 s`
- architecture v4 fingerprint: `abf3148cfba2063f8fdba23951239b2b0a4a899c391503d3e46db69fd203618d`
- reference outcome: `finished`, committed สาม step, `3.0 s`, `30.0 m`, finish residual `0.0 m`
- whole-race replay fingerprint: `419b25773df7982aebb606d5a834b84f95a6c6a0fdc32735c063cb8e10793163`
- same-seed replay และ reversed registration: เท่ากัน exact
- depletion: `0.5 s`, primary energy `0.0 J`
- thermal failure: `0.2 s`
- timeout: `1.5 s`
- invalid corridor: ไม่มี committed state identity
- reference residual ผ่านทั้งหมดและบันทึก adapter trace ครบแปดรายการต่อ committed step

## ข้อจำกัด

เป็น Level 0 เท่านั้น run ที่สำเร็จเป็น controlled analytical integration fixture ไม่ใช่ real-circuit prediction หรือ physical validation ยังขาด measured per-segment evidence, strategy optimization, calibrated tyre/aero/thermal/reliability model, full 3D contact, uncertainty quantification และ cross-model validation

## งานต่อเนื่อง

Work 029 สามารถสร้าง fair fixed-topology campaign บน circuit profile ที่ประกาศสิบสนามต่อได้ ส่วน Work 030 ยังต้องปิด numerical refinement, deliberate integration-defect falsification และ promotion/release gate ก่อนถือ autonomous candidate เป็น discovery
