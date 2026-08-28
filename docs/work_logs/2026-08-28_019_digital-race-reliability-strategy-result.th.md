# ผล Work 019: Digital Race Reliability และ Strategy

ต้นฉบับภาษาอังกฤษ: `2026-08-28_019_digital-race-reliability-strategy-result.md`

สถานะ: Completed

## ผลลัพธ์

Work 019 และ physics queue Work 010–019 เสร็จแล้ว `digital-race-level0-v1`
execute ทุก published lap ผ่าน sector ที่ประกาศ โดยมี per-lap pace control แบบ
deterministic, weather/traffic ราย event, onboard primary energy ลดทางเดียว,
degradation, damage, seeded reliability uncertainty และ terminal-event
localization แบบ analytical

Circuit profile จริงทั้งสิบจบที่ published race distance exact ใน neutral
reference Run seed เดิม replay ตรงกัน Forced reliability, damage, degradation,
depletion, timeout และ numerical-invalid case จบด้วย mode ที่แยกและสังเกตได้
ไม่มี energy replenishment

สมมติฐานหลักรองรับแบบมีเงื่อนไขภายใน model ที่ประกาศ: aggressive reference เร็ว
กว่าแต่ใช้ energy และสะสม degradation, damage และ hazard มากกว่า นี่ยังเป็น Level-
0 selection evidence ไม่ใช่ lap-time, reliability, safety หรือ physical
validation จริง

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/physics/digital_race.py`: scenario/vehicle/control
  contract เข้มงวด, multi-lap event loop, published-distance closure, ผลจาก pace/
  weather/traffic, energy/degradation/damage rate, seeded exponential hazard,
  event competition, telemetry, residual, replay และ observable invalidity
- `src/formula_ultimate/physics/__init__.py`: public Work 019 API export
- `tests/test_digital_race.py`: test แบบ grouped เก้าข้อ ครอบคลุมสิบสนาม,
  strategy/environment effect, seeded uncertainty, terminal mode ทั้งหมด,
  conservation, tie priority, replay, invalid contract และ numerical failure
- `scripts/validate_digital_race.py`: validator สิบสนามและ falsification
- `docs/physics/DIGITAL_RACE_RELIABILITY_STRATEGY_MODEL.md` และ `.th.md`:
  contract, สมการ, priority, evidence, interpretation และ limitation
- `docs/problem_reports/2026-08-28_019_global-energy-residual-scale.md` และ
  `.th.md`: วินิจฉัย terminal residual แบบ scale-aware และแก้ไขที่ยืนยันแล้ว
- `docs/problem_reports/2026-08-28_019-lookup-command-path-assumptions.md` และ
  `.th.md`: แก้ read-only discovery-command path assumption แล้ว
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md` และ `.th.md`: ทำเครื่องหมาย Work
  019 และ sequential queue เป็น `Completed`
- คู่ plan/result สองภาษานี้

## การตัดสินใจและหลักฐาน

1. Sector/command เป็น abstract และ ordered; ไม่บังคับ conventional vehicle
   layout, energy technology, component topology หรือ fastener form
2. Strategy ต้องมี pace command หนึ่งตัวต่อ published lap Weather/traffic เป็น
   override ตาม event key ชัดเจน; key ที่ไม่มีเป็น neutral และ reject key ซ้ำ/นอกขอบ
3. Sector ปกติใช้ published lap length กับ fraction ที่ประกาศ Final event ใช้
   published race distance ที่เหลือ exact โดยยังแสดงส่วนต่าง nominal เป็น official-
   distance adjustment
4. Pace เปลี่ยน speed เชิงเส้น, drive energy/degradation กำลังสอง และ damage กับ
   default hazard exposure กำลังสาม Multiplier ทุกตัวเป็น scenario input ที่ประกาศ
5. Source energy มีเฉพาะ drive energy และ auxiliary power ที่ประกาศ Energy ลดทาง
   เดียว ไม่มี refuelling หรือ primary-energy input ที่ไม่ประกาศ
6. ใช้และบันทึก seeded uniform draw หนึ่งค่าต่อ entered event Constant start-of-
   event exponential hazard หา reliability failure แบบ localized
7. Finish, reliability, damage, degradation, depletion และ timeout แข่งขันด้วยเวลา
   analytical Terminal state integrate เฉพาะสัดส่วนที่ execute
8. ทุก event แสดง distance/energy residual และ sub-tolerance energy-boundary
   correction หาก overspend มากกว่า tolerance, rate ไม่ finite หรือ effective
   speed ไม่บวก run จะ invalid

## ปัญหาที่พบและแก้แล้ว

### สมมติฐาน Path ของ Read-only Lookup

Discovery probe แรกสมมติชื่อไฟล์ Work 015 สองไฟล์และใช้ PowerShell wildcard เป็น
path ของ `rg` จึง fail โดยไม่เปลี่ยนไฟล์ Repository search พบชื่อจริงและ probe
ถัดมาใช้ explicit path สำเร็จ รายงานปัญหาแยกเก็บ scope และ resolution exact

### Terminal Energy Assertion ที่ไม่คิดสเกล

Focused test แรกผ่าน behavioral case ทั้งหมด แต่ real-circuit subtest เก้าตัว
เปรียบเทียบ terminal reconciliation ระดับ `1e10 J` กับศูนย์ถึงทศนิยมเจ็ดตำแหน่ง
Floating-point residual ที่สังเกตได้มีเพียง `1.9073486328125e-06` ถึง
`1.1444091796875e-05 J` หรือประมาณ `1e-15` แบบ relative ขณะที่ทุก event ยังอยู่
ภายใน `1e-8 J`

ไม่ได้ปัดหรือซ่อน production residual Test เก็บ per-event absolute gate และเพิ่ม
terminal gate แบบ scale-aware `2e-15` ที่เข้มงวด Rerun ผ่าน รายงานปัญหาสองภาษา
บันทึก failure, impact, fix และ verification

## ทบทวนการทดลอง

- Independent variables: สนามจริง, sector coefficient/fraction, per-lap pace,
  weather/traffic schedule, onboard energy/auxiliary power, degradation/damage
  parameter/limit, reliability hazard coefficient, timeout และ seed
- Dependent variables: elapsed time/distance, energy used/remaining,
  degradation, damage, hazard/draw/failure time, event/outcome/failure mode,
  residual, completed lap/event และ replay metadata
- Controls: circuit/sector contract เดียวกัน, schedule/สมการคงที่, หนึ่ง command
  ต่อ lap, ไม่มี primary-energy addition, seed คงที่ และ event priority deterministic
- Metrics: published-distance finish exact, time, energy monotonicity/residual,
  degradation/damage, analytical failure time, event/draw count, replay equality
  และ invalid coverage
- Supporting evidence: reference ทั้งสิบจบ exact; same-seed result เหมือนกัน;
  aggressive pace เร็วกว่าแต่แพงกว่า; traffic/wet-weather เปลี่ยนตามทิศที่ประกาศ;
  seeded analytical failure ตรงกัน
- Falsifying evidence: forced reliability, damage, degradation, depletion,
  timeout, schedule นอกขอบ, fraction ผิด, input ไม่ finite และ runtime speed ไม่
  บวก ไม่สามารถรายงานเป็น valid finish
- Contradicting evidence: exact-style energy assertion แรก fail จาก terminal
  round-off ระดับ microjoule ขัดกับความคาดหวัง residual ศูนย์ literal และสนับสนุน
  การเก็บ raw numerical evidence แบบคิดสเกล
- Alternative explanations: high-fidelity sector model หรือ calibrated failure/
  weather/traffic input อื่นอาจกลับลำดับ strategy
- Missing evidence: coupled Work 011–018 time stepping, surveyed racing line,
  transient tyre/aerodynamics/thermal/storage, component wear/fatigue, รถคู่แข่ง
  ที่โต้ตอบกัน, pit/flag logic, empirical reliability และ weather จริง
- Confidence: สูงสำหรับ deterministic contract, event accounting และ replay;
  ต่ำหรือไม่มีสำหรับการทำนายเรซจริง, calibrated failure risk, safety หรือ physical
  superiority

## หลักฐาน Validation

ทุกคำสั่งรันจาก `C:\Formula Ultimate` ด้วย fail-fast handling

```powershell
python -m unittest tests.test_digital_race -v
```

Exit status: `0`; `Ran 9 tests`; `OK`

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`; `Ran 154 tests`; `OK`

```powershell
python scripts/validate_digital_race.py
```

Exit status: `0` หลักฐานสำคัญ:

```text
ten real-circuit outcomes: finished
distance residuals: 0 m
replay_equal: true
energy_monotonic: true
energy_replenishment_events: 0
aggressive/conservative time: 2410.1454516951667 / 3615.1432624331906 s
aggressive/conservative energy: 376016912.72584754 / 168390611.63121662 J
traffic delay delta: 7.499999999999545 s
wet time/energy delta: 3.178249263393809 s / 133480 J
seed 23 failure expected/actual: 2.5884721324944864 s
terminal modes: depleted, degradation, damage, timeout, invalid
```

```powershell
python -m compileall -q src scripts tests
git diff --check
```

ทุกคำสั่ง exit status `0` Validation ทั้งหมดรันซ้ำหลัง result นี้ จากนั้น stage
explicit และรัน `git diff --cached --check` ก่อน commit

## ข้อจำกัดและงานต่อ

- Sector rate เป็น reduced-order scenario evidence และยังไม่ได้มาจาก coupled
  simulation ของ Work 011–018
- Traffic, weather, degradation, damage และ reliability จงใจ simplify และยังไม่
  calibrate
- Strategy ควบคุม pace เท่านั้น ไม่มี pit service, repair, refuelling, tyre
  change, competitor tactics, flag state หรือ safety-car logic
- ต้องมี higher-fidelity physics และ empirical validation ก่อนคำอ้างด้าน design,
  performance, reliability, manufacturability หรือ safety จริง
- Work 010–019 เป็น staged Level-0 physics foundation ที่ครบ ไม่ใช่ Formula
  Ultimate vehicle ที่เสร็จหรือผลสรุปงานวิจัยขั้นสุดท้าย
- Commit hash รายงานใน final handoff และไม่ push remote
