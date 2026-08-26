# ผลลัพธ์ Work 015: Deterministic Full-Race Completion Loop

ต้นฉบับภาษาอังกฤษ: `2026-08-26_015_deterministic-race-loop-result.md`

สถานะ: Completed

## ผลลัพธ์

Work 015 เสร็จสมบูรณ์ Level-0 loop ที่ทำซ้ำได้รัน candidate เทียบ published race
distance ของแต่ละ circuit profile และจบด้วย outcome หนึ่งค่า: `finished`,
`depleted`, `timeout`, `failed` หรือ `invalid` Onboard energy ถูกประกาศก่อน race
และไม่เติมระหว่างแข่ง

สมมติฐานได้รับการสนับสนุน: ความเร็วช่วงสั้นอย่างเดียวผ่าน gate ไม่ได้ Reference
energy ไม่พอ, force ศูนย์, overheating และ numerical failure หยุดก่อน finish
ส่วน reference budget ที่ตั้งให้พอจบและ replay exact บน profile ทั้งสิบ

Fixture time สิบสนาม (`228–248 s`) เป็น reduced-order software evidence ไม่ใช่
prediction race/lap จริงหรือ physical validation

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/physics/race.py`: race contract, replay metadata,
  motion/energy/thermal loop, event localization/priority, terminal outcome,
  numerical invalidity และ telemetry
- `src/formula_ultimate/physics/__init__.py`: public race API export
- `tests/test_race.py`: test 10 รายการครอบคลุม outcome, สิบสนาม, replay,
  energy, derating, event tie, invalid contract และ numerical failure
- `scripts/validate_race.py`: all-ten finish replay และ terminal reference
- `docs/physics/RACE_COMPLETION_LOOP.md` และ `.th.md`: model, evidence,
  event/energy semantics และข้อจำกัด
- `docs/problem_reports/2026-08-26_015_event-tie-energy-overspend.md` และ
  `.th.md`: ปัญหาแยก, root cause, fix และ verification
- queue และคู่ plan/result Work 015 สองภาษานี้

## การตัดสินใจและหลักฐาน

1. Target distance คือ `CircuitProfile.race_distance_m` ที่มีแหล่งข้อมูล
2. Motion ใช้ longitudinal solver deterministic และ reference air density
   Applied force คือ commanded force คูณ derating ต้น step
3. Source energy คือ wheel work + waste heat + auxiliary draw ที่ประกาศ
   remaining energy ไม่เพิ่มและไม่มี recovery/refueling API
4. Finish/depletion ใช้ bisection คงที่ default 64 iteration; Work 014 ให้
   analytical thermal failure time
5. Event เร็วสุดชนะ; exact-time priority คือ finish, failure, depletion, timeout
   และแยก requested/executed time
6. Runtime numerical failure เป็น `invalid` พร้อมเหตุผล ไม่แก้แบบเงียบ
7. Replay metadata เก็บ version, identity, control, seed, iteration, tolerance
   และ stochastic draw ศูนย์

## ปัญหาที่พบและแก้แล้ว

Falsification exact event tie ที่วางแผนไว้ล้มเหลวครั้งแรก: finish, depletion,
timeout ที่ `10 s` ให้ `invalid` เพราะ bisection bound ที่ติดกัน overspend
`0.000244140625 J` บน scale `1354976035920.0 J`

วิธีแก้เพิ่ม scaled energy-event tolerance ที่ประกาศและเก็บ raw signed boundary
residual ภายใน tolerance finish/failure priority สูงให้ remaining energy ศูนย์
แต่ยังเก็บ residual; เกิน tolerance ยัง invalid Exact tie ตอนนี้ให้ `finished`,
remaining `0 J`, residual `-0.000244140625 J`; tolerance ศูนย์ให้ `invalid`
ไม่มี replenishment

## การทบทวนการทดลอง

- Independent variables: circuit, vehicle/motion parameter, force, onboard
  energy, heat/auxiliary power, thermal setting, cooling, step, timeout และ seed
- Dependent variables: outcome, time, distance/speed, energy, temperature,
  derating, terminal/event residual และ telemetry
- Controls: SI, model/iteration/priority คงที่, ไม่เติม energy, random draw ศูนย์
  และ replay metadata เดียวกัน
- Metrics: outcome coverage, distance/depletion residual, thermal time, energy
  monotonicity, accounting residual และ exact replay
- หลักฐานสนับสนุน: profile ทั้งสิบให้ `finished` สองครั้งด้วย equality exact และ
  finish residual ศูนย์; energy/timeout/failure/invalid reference ให้ outcome ตาม
  ที่ประกาศ
- หลักฐานหักล้าง: `1000 J` deplete โดย energy ไม่ติดลบ; force ศูนย์ timeout ที่
  `5 s`; thermal fail ที่ `50 s/400 K`; equilibrium non-finite ให้ invalid;
  event overspend ที่ tolerance ศูนย์ให้ invalid
- หลักฐานขัดแย้ง: exact-tie implementation แรกล้มเหลวและเก็บไว้ใน problem
  report; implementation ที่แก้แล้วผ่าน
- คำอธิบายทางเลือก: terminal case เปลี่ยน parameter แยกและ assert state/residual
  ไม่ใช่ตรวจ outcome string อย่างเดียว
- หลักฐานที่ขาด: track geometry/dynamics, braking, tyre ใน loop, efficiency/heat
  calibrated, traffic, weather, degradation และ control strategy
- ความมั่นใจสูงต่อ software/event semantics; ต่ำ/ไม่มีต่อ race time หรือ
  feasibility รถจริง

## หลักฐาน Validation

ทุกคำสั่งรันจาก `C:\Formula Ultimate` พร้อม fail-fast

```powershell
python -m unittest tests.test_race -v
```

Exit status `0`; `Ran 10 tests`; `OK`

```powershell
python -m unittest discover -s tests -v
```

Exit status `0`; `Ran 110 tests`; `OK`

```powershell
python scripts/validate_race.py
```

Exit status `0`; ผลสำคัญ:

```text
ten circuit outcomes: finished
replay_equal: true
energy_replenishment_events: 0
depleted remaining_energy_j: 2.2737367544323206e-13
timeout time_s: 5.0
failed time_s/temperature_k: 50.0 / 400.0
invalid: thermal equilibrium is non-finite
exact tie: finished, remaining 0.0 J, residual -0.000244140625 J
```

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status `0` ทุกคำสั่ง รัน full validation ซ้ำหลัง result และ staged
scope/check ก่อน commit

## ข้อจำกัดและงานต่อเนื่อง

- Circuit เป็น total distance + reference density ไม่ใช่ 3D layout ที่วิ่งจริง
- ไม่มี lateral, braking, tyre, traffic, weather, recovery, pit หรือ strategy
- Force/heat/auxiliary power ที่ประกาศไม่ใช่ powertrain map calibrated
- `finished` ระดับ Level-0 ไม่ใช่ physical validation
- Work 016 จะเพิ่ม lateral/yaw/load transfer และยังไม่เริ่มในงานนี้
- รายงาน commit hash ใน final handoff และไม่ push remote
