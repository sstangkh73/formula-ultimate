# แผน Work 019: Digital Race Reliability และ Strategy

ต้นฉบับภาษาอังกฤษ: `2026-08-28_019_digital-race-reliability-strategy-plan.md`

สถานะ: Completed

## วัตถุประสงค์

สร้าง digital race model หลายรอบระดับ Level-0 แบบ deterministic ที่รวม strategy
control ชัดเจน, traffic, weather, degradation, onboard-energy depletion และ
seeded reliability failure โดยยึด published race distance ของสนามจริงแต่ละแห่ง
เป็น finish boundary

## ขอบเขต

- กำหนด SI contract เข้มงวดสำหรับ race sector ที่ไม่ผูก topology, per-lap
  strategy, weather/traffic event, vehicle/risk parameter, state, telemetry,
  residual, replay metadata และ terminal outcome
- วิ่งครบทุก lap/sector ที่ประกาศ ปรับ published-distance residual เฉพาะ event
  สุดท้าย และแสดง adjustment นั้นใน telemetry
- เก็บ primary energy ไว้ onboard และลดลงทางเดียว; ห้าม refuelling หรือเติม
  energy โดยไม่มีบัญชีระหว่างเรซ
- ให้ pace, weather, traffic และ degradation สะสมกระทบ sector time, energy use,
  degradation, damage และ reliability hazard ผ่านสมการ reduced-order ที่ประกาศ
- สุ่ม reliability uniform หนึ่งค่าต่อ event ที่เข้าโดยใช้ seed และหา exponential
  failure time ภายใน event แบบ analytical
- แข่งขันเวลา event ของ finish, reliability, degradation, damage, depletion และ
  timeout โดยไม่ clip invalid state หรือแก้ residual เงียบ
- ตรวจ neutral completion บนสนามจริงทั้งสิบ profile รวม deterministic replay,
  strategy comparison, weather, traffic และ forced failure mode
- เพิ่ม test, validator, เอกสาร model/result สองภาษา, ปิด queue, problem report
  สองภาษาแยกทุกปัญหาที่พบ และ commit ที่ตรวจยืนยันหนึ่งชุด

## ไฟล์ที่วางแผน

- `src/formula_ultimate/physics/digital_race.py`
- `src/formula_ultimate/physics/__init__.py`
- `tests/test_digital_race.py`
- `scripts/validate_digital_race.py`
- `docs/physics/DIGITAL_RACE_RELIABILITY_STRATEGY_MODEL.md` และ `.th.md`
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md` และ `.th.md`
- คู่ plan/result สองภาษานี้
- problem report สองภาษาแยกสำหรับปัญหาที่พบ

## ขอบเขต Model

สำหรับ event ระยะ `d`, degradation ต้น event `g`, base speed `v0`, pace `p`,
weather speed factor `w_v` และ traffic speed factor `q_v`:

```text
v = v0 * p * w_v * q_v * (1 - k_v*g)
t_event = d / v + t_traffic
E_event = d * e0 * p^2 * w_E * q_E + P_aux * t_event
delta_g = d * r_g * p^2 * w_g * q_g
delta_D = d * r_D * p^3 * w_D * q_D
```

Model ตรึง rate เหล่านี้ตลอด event และ integrate energy, degradation และ damage
เฉพาะสัดส่วนเวลาที่ execute พร้อมหา hard limit และ global timeout แบบ analytical

Reliability ใช้ hazard rate คงที่ใน event จาก state ต้น event และ condition ที่
ประกาศ:

```text
lambda = lambda0 * w_R * q_R * p^n *
         (1 + k_g*g + k_D*D)
t_reliability = -ln(1 - u) / lambda,  u ~ Uniform[0, 1)
```

สุ่ม `u` หนึ่งค่าพอดีสำหรับทุก event ที่เข้าจาก seed ที่ประกาศ บันทึก draw และ
candidate time แม้ไม่เกิด reliability failure ทำให้ replay uncertainty ได้ แต่
ไม่ได้พิสูจน์ real-world failure rate

## ความหมาย Event

Candidate ที่ valid และเร็วที่สุดตัด current event หาก tie exact ที่ final sector
ให้ completion มาก่อน แล้ว reliability, damage, degradation, depletion และ timeout
สำหรับ non-final sector จะ advance เมื่อไม่มี terminal candidate ที่เกิดไม่ช้ากว่า
ขอบ sector Final state เก็บ localized boundary และ conservation residual ทั้งหมด

## นิยามการทดลอง

- สมมติฐานหลัก: conservative strategy ที่ชัดเจนสามารถแลก lap time กับ energy,
  degradation, damage และ seeded reliability exposure ที่ต่ำลง ขณะที่ aggressive
  strategy อ้างชนะไม่ได้หากไม่จบ published race distance เดียวกันผ่าน evidence gate
- Independent variables: circuit, sector map, strategy pace, weather schedule,
  traffic schedule, energy budget, degradation/damage rate และ limit, reliability
  hazard parameter, timeout และ random seed
- Dependent variables: elapsed time, distance, energy, degradation, damage,
  hazard/draw/failure time, terminal outcome, residual และ replay metadata
- Controls: circuit/component library เดียวกัน, ไม่มี primary-energy addition
  กลางเรซ, schedule/สมการ/seed คงที่ และ tie priority deterministic
- Metrics: finish status/time, exact distance closure, energy residual, energy
  ลดทางเดียว, limit localization, replay equality, event count และ invalid coverage
- Success: neutral race สนามจริงทั้งสิบจบ exact; run seed เดิมเหมือนกัน; ผลของ
  strategy/weather/traffic ไปทิศที่ประกาศ; forced terminal event ทุกแบบ localized;
  repository gate ทั้งหมดผ่าน
- Failure criteria: declaration ไม่ finite/ติดลบ, schedule ไม่ครบ/ซ้ำ, effective
  speed ไม่บวก, conservation residual เกิน tolerance, energy เพิ่ม, limit crossing
  ไม่ localized, replay ไม่ deterministic หรือ repository gate ล้มเหลว
- Falsification: บังคับ depletion, timeout, degradation, damage, reliability,
  severe weather, traffic delay, official-distance residual และ numerical
  invalidity โดยห้ามรายงานกรณีเหล่านี้ว่า valid finish

## ความเสี่ยง

- Speed/rate คงที่ต่อ event ตัด transient vehicle dynamics, tyre state, coupled
  thermal system, pit-lane operation, driver behavior และ detailed multi-agent
  traffic interaction ออก
- Weather/reliability multiplier เป็น scenario ที่ประกาศ ไม่ใช่ forecast ที่
  calibrate หรือ empirical failure distribution
- Linear degradation และ scalar damage ยุบหลาย physical mechanism; ต้องแทนด้วย
  model fidelity สูงกว่าก่อน scientific validation
- การใส่ official-distance residual ที่ event สุดท้ายรักษา finish target จริง แต่
  เป็น bookkeeping boundary ไม่ใช่การ reconstruct timing-line geometry

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่กำหนด conventional car layout, tyre count, engine type, body shape หรือ
  component topology
- ไม่มี refuelling, external primary-energy transfer, pit repair, tactical
  opponent AI, CFD, multibody dynamics, real weather prediction หรือ safety
  certification
- ไม่อ้างว่า Level-0 completion ทำนายผลเรซจริงหรือ physical validity และไม่ push
  remote

## Validation

```powershell
python -m unittest tests.test_digital_race -v
python -m unittest discover -s tests -v
python scripts/validate_digital_race.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

ทุก gate รัน fail-fast การเสร็จต้องมี result สองภาษา, problem report ที่จำเป็น,
staged scope ที่ระบุ, commit สำเร็จ และหลักฐาน clean-state/hash หลัง commit
