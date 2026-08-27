# ผล Work 017: Aerodynamic Force, Balance และ Cooling Flow

ต้นฉบับภาษาอังกฤษ: `2026-08-28_017_aerodynamic-force-balance-cooling-result.md`

สถานะ: Completed

## ผลลัพธ์

Work 017 เสร็จสมบูรณ์ `work017-aerodynamic-map-v1` ประเมิน coefficient grid ที่มี
provenance ข้าม envelope ของ airspeed, ride height, yaw และ discrete active state
ที่ประกาศ Result คืน drag, side force, downforce, pitch/yaw moment, signed
longitudinal centre of pressure, ram-air mass flow, cooling conductance, signed
heat flow, interpolation evidence และ algebraic residual แปดตัว

สมมติฐานหลักได้รับการสนับสนุนภายใน software boundary ที่ประกาศ: synthetic
reference แสดง trade-off ตาม speed, ride height, yaw และ active state แบบ
deterministic ขณะที่ query นอก envelope ทุกแบบยังเป็น `invalid` และ synthetic
evidence ยังแยกชัดจาก geometry-derived evidence

นี่เป็น Level-0 software/analytical evidence ไม่ใช่ CFD, measurement หรือ
physical validation

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/physics/aerodynamics.py`: evidence contract, coefficient
  grid ครบ, tensor interpolation, สมการ force/moment/cooling, residual และ
  invalidity ที่สังเกตได้
- `src/formula_ultimate/physics/__init__.py`: export API Work 017
- `tests/test_aerodynamics.py`: 11 tests สำหรับ analytical, envelope, provenance,
  replay, cooling, malformed grid และ numerical failure
- `scripts/validate_aerodynamics.py`: synthetic reference validator สอง state
- `docs/physics/AERODYNAMIC_FORCE_BALANCE_COOLING_MODEL.md` และ `.th.md`: model,
  sign/evidence contract, สมการ, integration boundary และ limitation
- `docs/problem_reports/2026-08-28_017_aerodynamic-speed-scaling-wording.md` และ
  `.th.md`: แก้ถ้อยคำ `inverse-square` เป็น `speed-squared` ก่อนเขียน code
- `docs/problem_reports/2026-08-28_017_interpolation-fraction-exact-assertion.md`
  และ `.th.md`: floating-point assertion failure, fix และการรันใหม่ที่ผ่าน
- queue และคู่ plan/result Work 017 สองภาษานี้

## การตัดสินใจและหลักฐาน

1. Map เป็น topology-neutral ไม่กำหนด wing, body shape, wheel count หรือ vehicle
   architecture แบบเดิม
2. Provenance basis คือ `synthetic_reference`, `geometry_derived`, `cfd` และ
   `measured` Map geometry-derived ต้องมี geometry digest SHA-256 lowercase
3. Axis เพิ่มอย่างเคร่งครัด และ active state ทุกตัวต้องมี grid ครบตามลำดับ
   speed-major, height, yaw โดย active state เป็น discrete
4. Tensor-linear interpolation แสดง bracket/fraction ทุกตัว Exact node ยังคง
   exact; จุดนอกขอบและ state ที่ไม่รู้จักไม่ถูก clamp
5. Dynamic pressure สร้าง drag, side/down force และ pitch/yaw moment Centre of
   pressure หาเฉพาะเมื่อ signed downforce ไม่เป็นศูนย์
6. Ram-air flow สร้าง mass flow, air heat-capacity rate, effective cooling
   conductance และ signed heat rejection พลังงาน active device ไม่ถูกซ่อนใน
   airflow model
7. Residual แปดตัวปิดสมการ force, moment, mass flow, conductance และ heat flow
   แยกกัน; runtime output ไม่ finite คืน `invalid`

## ปัญหาที่พบและแก้แล้ว

1. แผนรุ่นแรกเขียน `inverse-square force scaling` ผิด แม้สมการใช้ `V^2` ถูกต้อง
   แผนสองภาษาถูกแก้เป็น `speed-squared` ก่อน implementation และเก็บปัญหาใน
   bilingual report แยก
2. Test รอบแรกผ่าน 10 และ fail exact equality หนึ่งข้อ: binary floating point
   แทน ride-height midpoint fraction เป็น `0.4999999999999999` ไม่ใช่ decimal
   `0.5` Test fraction เปลี่ยนเป็น `assertAlmostEqual`; exact-node identity และ
   replay เต็มยัง exact การรันใหม่ผ่าน 11 tests และ raw fraction ยังแสดงอยู่
3. คำสั่ง patch เอกสารหนึ่งครั้งถูก reject ก่อนเขียน เพราะ code block ไม่มี patch
   line prefix จากนั้นเพิ่มไฟล์แยกกันสำเร็จ ไม่มี partial file หรือ repository
   state เกิดขึ้น

## ทบทวนการทดลอง

- Independent variables: map/provenance, continuous axis, active state,
  airspeed/density, ride height, yaw, reference area/length, inlet area, air heat
  capacity, effectiveness และอุณหภูมิ air/component
- Dependent variables: coefficient, interpolation bracket/fraction, dynamic
  pressure, force/moment ห้าค่า, centre of pressure, cooling-path output สามค่า,
  heat flow, residual แปดตัว, status และ reason
- Controls: SI/sign contract, grid order คงที่, tensor-linear interpolation,
  ไม่ extrapolate, discrete active state, input เดียวกัน และ random draw ศูนย์
- Metrics: exact-node/interior error, residual ทั้งหมด, force ratio `V^2`,
  mass-flow ratio `V`, yaw symmetry/antisymmetry, drag/cooling delta จาก active
  state, replay exact และ invalid-case coverage
- Supporting evidence: residual แปดตัวศูนย์ที่ validator point; drag ratio
  `40/20 m/s` เท่ากับ `4.0`; mass-flow ratio `2.0`; cooling-open เพิ่ม drag/flow;
  replay exact
- Falsifying evidence: continuous axis ทุกตัวนอกขอบ, unknown active state,
  incomplete/duplicate grid, coefficient/provenance invalid และ runtime output
  ไม่ finite ถูก reject `41 m/s` กับ map `0–40 m/s` คืน `invalid` ไม่ clamp
- Contradicting evidence: exact fraction assertion แรกล้มและถูกเก็บใน report;
  สิ่งที่ขัดแย้งคือวิธี assertion ไม่ใช่ coefficient output
- Alternative explanations: speed ratio อย่างเดียวอาจผ่านแม้ index map ผิด จึง
  test exact node, interior interpolation, yaw symmetry, active state, provenance
  และ bracket evidence แยก
- Missing evidence: CFD/measurement ที่เชื่อม geometry, uncertainty, mesh/
  convergence study, pressure-drop/UA/fan work, transient flow และ coupling เข้า
  dynamics Work 014–016
- Confidence: สูงสำหรับ deterministic map/interpolation/algebra contract; ต่ำ
  หรือไม่มีสำหรับ aerodynamic ของ candidate จริงเพราะ reference เป็น synthetic

## หลักฐาน Validation

ทุกคำสั่งรันจาก `C:\Formula Ultimate` แบบ fail-fast

```powershell
python -m unittest tests.test_aerodynamics -v
```

Exit status: `0`; `Ran 11 tests`; `OK`

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`; `Ran 132 tests`; `OK`

```powershell
python scripts/validate_aerodynamics.py
```

Exit status: `0` ผลสำคัญ:

```text
evidence basis: synthetic_reference; geometry_sha256: null
dynamic pressure: 240.0 Pa
coefficients: Cd 0.63, Cy 0.035, Cdown 1.22, Cm 0.05, Cn 0.01, Cflow 0.389
drag/downforce/pitch: 226.8 N / 439.2 N / 54.0 N*m
centre of pressure x: 0.12295081967213115 m
mass flow: 0.74688 kg/s
cooling conductance: 525.43008 W/K
heat rejection: 31525.804799999998 W
all eight residuals: 0
drag 40/20 ratio: 4.0
mass-flow 40/20 ratio: 2.0
cooling-open drag: 270.0 N; flow: 1.51488 kg/s
replay_equal: true
41 m/s query: invalid, outside declared airspeed envelope
```

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` ทุกคำสั่ง Full validation รันซ้ำหลัง result นี้ และตรวจ staged
scope/check ก่อน commit

## ข้อจำกัดและงานต่อ

- Linear quasi-steady coefficient interpolation ขึ้นกับความหนาแน่นของ map และ
  ไม่มี separation hysteresis, gust, transient device, compressibility หรือ
  fluid-structure interaction
- Cooling ไม่มี duct pressure loss, heat-exchanger UA, fan/pump curve/energy,
  recirculation และ thermal mass
- Output ยังไม่ coupling เข้า race motion Work 015, load transfer Work 016 หรือ
  thermal state Work 014
- Work 018 จะรับผิดชอบ suspension, mechanical braking และ regenerative braking
  โดยยังไม่ได้เริ่มในงานนี้
- รายงาน commit hash ใน final handoff และไม่ push remote
