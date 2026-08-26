# แผน Work 015: Deterministic Full-Race Completion Loop

ต้นฉบับภาษาอังกฤษ: `2026-08-26_015_deterministic-race-loop-plan.md`

สถานะ: Completed

## วัตถุประสงค์

Implement full-race loop ระดับ Level-0 ที่ทำซ้ำได้ ใช้ race distance จริงจาก
profile สนาม Work 008 และให้ผล `finished`, `depleted`, `timeout`, `failed` หรือ
`invalid` อย่างชัดเจน โดย coupling onboard energy, longitudinal motion,
derating/failure จาก Work 014 และ replay metadata

## ขอบเขต

- กำหนด contract SI เข้มงวดสำหรับ race vehicle, control, state, step
  telemetry, replay metadata และ terminal outcome
- ใช้ `race_distance_m` ที่เผยแพร่ใน circuit profile เป็น finish target
- ใช้ longitudinal physics Work 005 และใช้ thermal derating ต้น step กับ
  commanded tractive force
- อนุญาตเฉพาะ primary energy onboard ที่ประกาศตอนเริ่ม race; ไม่เติมระหว่างแข่ง
- คิด source energy เป็น tractive work + waste heat + auxiliary energy ที่
  ประกาศ พร้อมเก็บ remaining energy และ event residual
- แข่งขัน event finish, depletion, thermal failure และ timeout ในแต่ละ step;
  localize finish/depletion แบบ deterministic และใช้ failure time exact จาก
  Work 014
- จับ runtime numerical failure เป็น `invalid` ที่สังเกตได้โดยไม่ซ่อม state
- เก็บ replay metadata: schema/model version, circuit/layout, fixed step และ
  random seed ชัดเจน (loop ปัจจุบันไม่มี randomness)
- Test สนามจริงทั้งสิบ, terminal outcome ทุกแบบ, event ordering, energy ลดลง
  เท่านั้น, derating, invalidity และ replay exact
- เพิ่ม validator, เอกสาร model/result สองภาษา, validation และ commit แยก โดย
  ไม่เริ่ม Work 016

## ไฟล์ที่วางแผน

- `src/formula_ultimate/physics/race.py`
- `src/formula_ultimate/physics/__init__.py`
- `tests/test_race.py`
- `scripts/validate_race.py`
- `docs/physics/RACE_COMPLETION_LOOP.md` และ `.th.md`
- สถานะ queue และคู่ plan/result สองภาษานี้
- problem report แยกสองภาษาเฉพาะเมื่อพบปัญหาที่มีสาระ

## ขอบเขตฟิสิกส์และพลังงาน

ภายใน race step applied force คงที่และเท่ากับ commanded force คูณ derating
factor ที่ต้น step Motion ใช้ deterministic longitudinal solver สำหรับระยะ
`delta_x` และเวลาที่ execute `delta_t`:

```text
E_wheel = F_applied * delta_x
E_source = E_wheel + P_waste_heat * delta_t + P_auxiliary * delta_t
E_remaining_next = E_remaining - E_source
```

Waste heat ที่ประกาศส่งเข้า Work 014 และคิดจาก onboard source ด้วย
`P_auxiliary` รวม cooling/support draw ที่ประกาศ แต่ยังไม่ resolve ทาง thermal
ไม่มี energy recovery หรือ refueling

สนามถูกลดรูปเป็น total race distance และ reference air density ไม่ใช่ lap
geometry หรือ racing-line simulation

## ความหมาย Event

แต่ละ iteration เสนอเวลาไม่เกิน `time_step_s` และตัดที่ timeout คำนวณ candidate
event time สำหรับ finish, depletion, thermal failure และ timeout Event ที่เร็ว
สุดชนะ Tie เวลา exact ใช้ priority deterministic:

```text
finished -> failed -> depleted -> timeout
```

Finish/depletion ใช้ bounded deterministic bisection บน motion solver เดียวกัน
Depletion เลือก bound สุดท้ายที่ไม่ใช้เกิน จึงไม่ทำให้ energy ติดลบ และเก็บ
remaining numerical residual เล็กไว้ Finish distance overshoot ยังแสดง Thermal
event execute ถึง analytical crossing เท่านั้นและเหลือเวลาที่ไม่ execute

## นิยามการทดลอง

- สมมติฐาน: candidate ที่เร็วช่วงสั้นไม่ใช่ race design ที่ valid หากไม่จบระยะ
  ที่เผยแพร่ก่อน energy, thermal, timeout หรือ numerical gate หยุด
- Independent variables: circuit profile, mass/drag/rolling resistance,
  commanded force, onboard energy, heat/auxiliary power, thermal parameter,
  cooling command, time step, timeout และ seed
- Dependent variables: outcome, total time/distance, speed, remaining/consumed
  energy, temperature/derating, terminal residual และ telemetry
- Controls: model version/convention SI เดียว, ไม่เติม energy, solver/event
  iteration คงที่, ไม่มี stochastic draw และ event priority เดียว
- Metrics: finish distance residual, depletion residual, thermal event time,
  energy monotonic, replay equality และจำนวน outcome
- Success: สร้าง/replay terminal outcome ทั้งห้าแยกกัน; profile ทั้งสิบจบได้ด้วย
  reference budget ที่ตั้งให้พอ; test/repository gate ทั้งหมดผ่าน
- Falsification: force ศูนย์ต้อง timeout; energy ไม่พอต้อง deplete โดยไม่ติดลบ;
  heat สูงต้อง fail ก่อนจบ step; runtime value finite สุดขั้วต้อง invalid;
  candidate finished ต้องถึง declared distance

## ความเสี่ยง

- สนาม point-mass ตาม total distance ไม่มี cornering, braking, sector grade,
  traffic, tyre state และ strategy
- Force/heat คงที่ใน step เป็น reduced-order assumption
- Bisection เป็น numerical event localization; ต้องแสดง residual และ iteration
  countแบบ deterministic
- Heat/auxiliary power ที่ประกาศไม่ใช่ powertrain efficiency map calibrated

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่มี lateral/yaw/load-transfer physics, racing line, pit stop, refueling,
  recovery, traffic, weather, degradation, strategy หรือข้ออ้าง lap time จริง
- ไม่มี physical validation หรืออ้างว่าสนามจริงสิบแห่งถูก simulate ด้วย fidelity
  ที่นำไปใช้จริงได้
- ไม่ทำ Work 016 และไม่ push remote

## Validation

```powershell
python -m unittest tests.test_race -v
python -m unittest discover -s tests -v
python scripts/validate_race.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

ทุก gate รัน fail-fast การเสร็จต้องมี result สองภาษา, staged scope ที่ระบุ,
commit สำเร็จ และหลักฐาน clean-state/hash หลัง commit
