# Deterministic Full-Race Completion Loop

สถานะ: ดำเนินการแล้วสำหรับ Work 015

ต้นฉบับภาษาอังกฤษ: `RACE_COMPLETION_LOOP.md`

## จุดประสงค์และขอบเขตหลักฐาน

Work 015 ตอบคำถามจำเป็นว่า candidate จบ published race distance ก่อน onboard
energy, thermal failure, timeout หรือ numerical invalidity หยุดหรือไม่ ไม่ได้
คำนวณ lap time ที่น่าเชื่อถือ สนามจริงแต่ละแห่งถูกลดเป็น total race distance และ
reference air density โดยไม่มี geometry, cornering, braking, traffic, weather
และ strategy

Fixture finish สิบสนามจงใจใช้ vehicle budget แบบง่ายที่เพียงพอเพื่อ verify
พฤติกรรม loop ผลประมาณ `228–248 s` เป็น analytical software fixture ไม่ใช่
prediction หรือ performance claim

## Contract state และ onboard energy

State มี elapsed time (`s`), distance (`m`), speed (`m/s`), remaining onboard
energy (`J`) และ thermal state จาก Work 014 ไม่มี API เติม energy ระหว่าง race
อุณหภูมิต้น step กำหนด derating factor และ applied force:

```text
F_applied = F_commanded * thermal_derating_factor
E_wheel = F_applied * delta_x
E_source = E_wheel + P_waste_heat*delta_t + P_auxiliary*delta_t
E_remaining_next = E_remaining - E_source
```

Waste heat ถูกคิดจาก source และส่งเข้า Work 014 Auxiliary power ถูกคิดแต่ยังไม่
resolve ทาง thermal โดย source term และ accounting residual ต่อ step แสดงอยู่

## Terminal outcomes

| Outcome | ความหมาย |
|---|---|
| `finished` | ข้าม `race_distance_m` ที่เผยแพร่ |
| `depleted` | Onboard energy ไม่พอ complete interval ถัดไป |
| `timeout` | ถึง time limit ก่อน finish |
| `failed` | เกิด thermal failure หรือถูก latch แล้ว |
| `invalid` | Runtime numerical physics สร้าง finite valid state ไม่ได้ |

Finish/depletion ใช้ fixed-iteration bisection บน motion solver เดียวกัน Thermal
failure ใช้ analytical event time จาก Work 014 Event ที่เร็วสุดชนะ โดย exact
time priority คือ `finished`, `failed`, `depleted`, `timeout`

## หลักฐาน Numerical Event Boundary

Work 015 พบและแก้ปัญหา numerical จริง บันทึกใน
`docs/problem_reports/2026-08-26_015_event-tie-energy-overspend.th.md` Exact tie
ของ finish/depletion/timeout ทำให้ upper-bound energy deficit
`-0.000244140625 J` บน scale `1354976035920.0 J`

Race control ตอนนี้ประกาศ absolute/relative energy-event tolerance (default
`1e-6 J` และ `1e-12`) และเก็บใน replay metadata หาก finish/failure priority สูง
มี raw boundary residual ติดลบภายใน scaled tolerance จะให้ usable remaining
energy เป็นศูนย์ แต่เก็บ signed residual ใน step/terminal output หากเกิน tolerance
run เป็น `invalid` วิธีนี้ไม่ใช่ energy replenishment

## Deterministic Replay

Replay metadata เก็บ schema/model version, circuit/layout, vehicle ID, fixed
time step, timeout, seed, bisection iteration และ energy tolerance Loop ปัจจุบัน
มี stochastic draw ศูนย์ การรัน profile ทั้งสิบซ้ำให้ dataclass equality exact

ใช้คำสั่ง:

```powershell
python scripts/validate_race.py
python -m unittest tests.test_race -v
```

## ข้อจำกัดและงานต่อเนื่อง

- Total-distance point mass ไม่มี circuit corridor, sector, curvature, braking,
  grade distribution, tyre capacity และ driver/controller decision
- Force/heat คงที่ภายใน step
- Waste/auxiliary power เป็น input ที่ประกาศ ไม่ใช่ efficiency map calibrated
- ไม่มี recovery, refueling, pit operation, reliability stochasticity/strategy
- `finished` หมายถึงผ่านเฉพาะ Level-0 gate นี้ ไม่ใช่ physical validation
- Work 016 ต้องเพิ่ม lateral/yaw/load-transfer constraint โดยไม่ตีความ fixture
  time เหล่านี้เป็น performance จริง
