# โมเดล Digital Race Reliability และ Strategy

ต้นฉบับภาษาอังกฤษ: `DIGITAL_RACE_RELIABILITY_STRATEGY_MODEL.md`

## สถานะและขอบเขตคำอ้าง

Work 019 สร้าง `digital-race-level0-v1` ซึ่งเป็น race gate หลาย lap/หลาย sector
แบบ deterministic ที่มี per-lap pace command, weather/traffic ราย event,
degradation, damage, onboard primary energy, seeded reliability และ terminal-
event localization ชัดเจน

นี่เป็น strategy และ failure-selection model ระดับ Level-0 ไม่ใช่ calibrated
reliability, การทำนาย lap time จริง, coupled vehicle physics, safety evidence
หรือ physical validation รถที่ผ่านยังต้องมี higher-fidelity coupling และหลักฐาน
เชิงประจักษ์

## Contract ที่ไม่ผูก Topology

Model ไม่กำหนด body shape, wheel count, axle layout, engine type, energy
technology, fastener type หรือ component topology Scenario ส่ง ordered abstract
sector ซึ่งค่า `lap_fraction` ต้องรวมเป็นหนึ่ง แต่ละ sector ประกาศ base speed ใน
SI, onboard energy ต่อระยะ, degradation ต่อระยะ และ damage ต่อระยะ

Abstraction นี้ให้ free-topology candidate ส่ง reduced-order sector evidence ของ
ตัวเองโดยเทียบภายใต้ circuit, sector contract, strategy schedule, environment
schedule, seed และ finish gate เดียวกัน

## ระยะสนามจริงและลำดับ Event

สำหรับ `CircuitProfile` จริงแต่ละสนาม Model เดิน:

```text
published race_laps * declared sectors_per_lap
```

ระยะ event ปกติคือ:

```text
d_nominal = published lap_length * sector lap_fraction
```

Published lap length ถูกปัดเศษและ race start อาจเยื้องจาก finish Circuit profile
เดิมแสดง:

```text
d_offset = published race_distance - lap_length * race_laps
```

Work 019 ไม่เปลี่ยนทุก lap เงียบ แต่กำหนดระยะ event สุดท้ายเท่ากับ published
race distance ที่เหลือ และบันทึกส่วนต่างจาก nominal final sector ใน
`official_distance_adjustment_m` Event ก่อนหน้าทั้งหมดมี adjustment ศูนย์ Final
state ตรง published target exact โดย adjustment ยัง audit ได้

## สมการ Strategy, Environment และ Degradation

สำหรับระยะ event `d`, degradation ต้น event `g`, base sector speed `v0`, lap
pace `p`, weather multiplier `w`, traffic multiplier `q` และ speed-loss
coefficient `k_v`:

```text
degradation_speed_factor = 1 - k_v*g
v_travel = v0 * p * w_speed * q_speed * degradation_speed_factor
t_request = d / v_travel + t_traffic

E_drive = d * e0 * p^2 * w_energy * q_energy
E_source = E_drive + P_aux * t_request

delta_g = d * r_g * p^2 * w_degradation * q_degradation
delta_D = d * r_D * p^3 * w_damage * q_damage
```

ต้องมี command หนึ่งตัวต่อ published lap ทุก lap Command ขาด/เกิน, schedule key
ซ้ำ, event index นอกขอบ, multiplier ไม่บวก หรือผลรวม sector fraction ผิด จะ fail
ก่อน execute

Traffic delay เป็น reduced-order event penalty ที่ประกาศ สำหรับ localization
progress, drive energy, degradation และ damage กระจายสม่ำเสมอตลอด combined
travel-plus-delay duration นี่ไม่ใช่ microscopic queue/overtaking model Weather
หรือ traffic event กระทบเฉพาะ zero-based `(lap_index, sector_index)` ที่ประกาศ
ส่วน key ที่ไม่ระบุใช้ neutral condition

## Seeded Reliability Uncertainty

Hazard rate ต้น event คือ:

```text
lambda = lambda0
       * w_reliability
       * q_reliability
       * p^n
       * (1 + k_g*g + k_D*D)
```

ใช้ pseudorandom draw หนึ่งค่าพอดีต่อ event ที่เข้า:

```text
u ~ Uniform[0, 1)
t_reliability = -ln(1 - u) / lambda
```

หาก hazard เป็นศูนย์จะไม่มี candidate time แต่ยังบันทึก draw เพื่อให้ event count
และตำแหน่ง random stream deterministic Replay metadata เก็บ model/circuit/layout/
scenario/vehicle/strategy identity, pace ทุก lap, weather/traffic key และ identity,
seed, จำนวน event ที่เข้า และ draw count

Hazard ที่ประกาศเป็น scenario parameter Seeded repeatability ทำให้ uncertainty
experiment audit ได้ แต่ไม่ได้ calibrate หรือ validate failure probability จริง

## Event Localization และ Priority

Rate ทุกตัวคงที่ภายในหนึ่ง event Candidate time คำนวณแบบ analytical สำหรับ:

- การจบ published distance ที่ final event
- seeded reliability failure
- damage limit
- degradation limit
- onboard-energy depletion
- global timeout

Candidate ที่เร็วสุดตัด time, distance, energy, degradation และ damage พร้อมกัน
ภายใน `event_time_tolerance_s` ที่ประกาศ final finish ชนะ tie แล้วตามด้วย
reliability, damage, degradation, depletion และ timeout ที่ non-final sector
terminal candidate ซึ่งเกิดที่หรือก่อน boundary ชนะ มิฉะนั้น event จบและเข้า
sector ถัดไป

Terminal outcome คือ:

- `finished`, `failure_mode=none`
- `failed`, `failure_mode=reliability|damage|degradation`
- `depleted`, `failure_mode=energy`
- `timeout`, `failure_mode=timeout`
- `invalid`, `failure_mode=numerical`

Hard-limit event เก็บ boundary ที่ localized แบบ analytical Runtime overflow,
rate ไม่ finite, effective speed ไม่บวก, event ordering ใช้ energy เกิน tolerance
และ residual failure กลายเป็น `invalid` ที่สังเกตได้ ไม่แก้เงียบ

## หลักฐาน Energy และ Residual

Model ไม่มี refuelling หรือ external primary-energy input Source energy ที่ใช้คือ:

```text
E_used = E_drive_requested * executed_fraction + P_aux * t_executed
E_remaining_next = E_remaining_start - E_used
```

ทุก event บันทึก:

```text
distance residual = d_end - d_start - d_executed
energy residual   = E_start - E_used - E_end
```

Energy ลดทางเดียว หาก event localization แบบ floating-point ทำให้ boundary ติดลบ
ต่ำกว่า tolerance จะตั้งเป็นศูนย์ได้เฉพาะเมื่อ raw value ยังอยู่ใน
`energy_boundary_residual_j` การ overspend มากกว่านั้นทำให้ race invalid Result
ยังเก็บ direct terminal reconciliation residual แทนการปัดทิ้ง

## หลักฐานอ้างอิง

`scripts/validate_digital_race.py` แสดงว่า:

- circuit profile จริงทั้งสิบจบด้วย distance residual ศูนย์ จำนวน lap/event exact
  และ final distance adjustment สังเกตได้
- run ซ้ำด้วย seed เดิมเท่ากัน exact
- onboard energy ไม่เพิ่มและไม่มี replenishment event
- pace `1.2` จบ Monaco reference ใน `2410.1454516951667 s` เร็วกว่า pace `0.8`
  ที่ `3615.1432624331906 s` แต่ใช้ energy และสะสม degradation/damage มากกว่า
- traffic penalty `7.5 s` เพิ่ม total time ประมาณ `7.5 s`
- wet event หนึ่งตัวเพิ่มเวลา `3.178249263393809 s` และ energy `133480 J` เทียบ
  neutral condition
- reliability seed `23`, draw `0.9248652516259452` และ hazard `1 /s` ให้
  analytical/simulated failure time `2.5884721324944864 s` ตรงกัน
- depletion, degradation, damage, timeout และ numerical invalidity คืน outcome/
  failure mode แยกตามที่คาด

Unit test ยังครอบคลุม seeded replay exact, uncertainty สอง seed, ตำแหน่ง official-
distance residual, final finish/depletion tie priority, scale-aware energy
closure, invalid contract และ localized hard limit

## Falsification และการตีความ

สมมติฐานหลักรองรับแบบมีเงื่อนไข: aggressive pace เร็วกว่าใน reference แต่จ่าย
energy, degradation, damage และ hazard มากขึ้น Test suite บังคับ non-finish outcome
ทุกแบบ จึงไม่จัด fast partial run เป็น successful race

ยังมี alternative explanation ผลลัพธ์อาจเปลี่ยนเมื่อใช้ sector rate จาก
aerodynamics, tyre, thermal, suspension, braking, energy-graph และ traffic model
ที่ fidelity สูงกว่า ดังนั้น Work 019 จัดอันดับเฉพาะ candidate ที่จบ Level-0
experiment ที่ประกาศ ไม่ได้พิสูจน์ว่า strategy/design ที่ชอบเหนือกว่าในโลกจริง

## ขอบเขต Integration ปัจจุบันและข้อจำกัด

- Work 019 ใช้ abstract sector coefficient; ยังไม่ time-step Work 011–018 tyre,
  energy, thermal, lateral, aerodynamic หรือ suspension model ร่วมกัน
- Degradation/damage เป็น scalar linear state ไม่ใช่ component-level failure,
  wear map, fatigue, corrosion หรือ collision physics
- Reliability hazard คงที่ในแต่ละ event และยังไม่ calibrate
- Weather ไม่มี spatial field, rainfall evolution, surface water, wind vector,
  temperature coupling หรือ forecast uncertainty
- Traffic เป็น event multiplier/delay ไม่ใช่รถหลายคันที่โต้ตอบกัน, overtaking,
  flag, safety car, pit lane หรือ race control
- Strategy ควบคุม pace เท่านั้น ไม่มี refuelling, pit repair, energy
  replenishment, tyre change หรือ tactical opponent AI
- Official-distance adjustment เป็น bookkeeping evidence ไม่ใช่ surveyed
  start/finish-line geometry
- การผ่าน model นี้เพียงอย่างเดียวไม่ใช่ physical validation, safety evidence,
  manufacturability evidence หรือหลักฐานความเหนือกว่าจริงในสนาม
