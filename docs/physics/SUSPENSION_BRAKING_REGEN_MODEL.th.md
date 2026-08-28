# โมเดล Suspension, Mechanical Braking และ Regeneration

ต้นฉบับภาษาอังกฤษ: `SUSPENSION_BRAKING_REGEN_MODEL.md`

## สถานะและขอบเขตคำอ้าง

Work 018 สร้าง `work018-suspension-braking-v1` ซึ่งเป็น interval evaluator ระดับ
Level-0 ที่ deterministic สำหรับ ground-contact suspension/brake module อิสระ
หนึ่งตัว โดย coupling normal load, reduced-order suspension travel,
tyre-limited regen/mechanical brake torque, recovered-energy storage, brake heat,
thermal derating/failure จาก Work 014 และ event truncation

นี่ไม่ใช่ detailed linkage, tyre, hydraulic, inverter, battery, ABS,
whole-vehicle stopping-distance, safety หรือ physical-validation model

## ขอบเขต Topology และ Upstream Load

API ประเมิน module ที่ระบุหนึ่งตัวและไม่กำหนด wheel count, paired axle,
left/right symmetry หรือ vehicle layout แบบเดิม Candidate สร้าง module จำนวนและ
arrangement ใดก็ได้

`normal_load_n` เป็น interval input ชัดเจน อาจมาจาก Work 016 รวม aerodynamic-load
coupling Work 017 ในอนาคต แต่ Work 018 ไม่สร้าง, redistribute หรือแก้ load นั้น
เงียบ Tyre ceiling ปัจจุบันเป็น longitudinal `mu*Fz` เท่านั้นและยังไม่ coupling
lateral force consumption

## Suspension State และ Force

Suspension travel `x` เป็นบวกใน compression และลบใน rebound Envelope valid คือ:

```text
-maximum_rebound <= x <= maximum_compression
```

ที่ต้น interval:

```text
F_suspension = preload + k*x0 + c*v0
a_travel     = (F_normal - F_suspension) / m_effective
x(t)         = x0 + v0*t + 0.5*a_travel*t^2
v(t)         = v0 + a_travel*t
```

Force และ acceleration คงที่หนึ่ง interval Result แสดง force residual:

```text
m_effective*a_travel - (F_normal - F_suspension)
```

Evaluator แก้ linear/quadratic root ของ travel boundary สองด้านและรับเฉพาะ
outward crossing จุด crossing valid ที่เร็วสุดหยุด interval ที่ analytical time,
latch suspension failure, เก็บ travel ที่ boundary และปล่อย requested time ที่
เหลือเป็น unexecuted โดยไม่ clip travel กลับเข้า envelope เงียบ

## Brake Torque Allocation

Requested torque ทุกค่าเป็น braking magnitude ไม่ติดลบ Contact ceiling คือ:

```text
T_tyre_limit = mu * F_normal * effective_radius
```

ที่ wheel speed `omega` สูงกว่า minimum ที่ประกาศ regen capacity เป็นค่าต่ำสุดของ:

```text
T_regen_component = maximum_regen_torque
T_regen_generator = maximum_generator_input_power / omega
T_regen_charge    = maximum_storage_charge_power /
                    (conversion_efficiency * omega)
T_regen_storage   = remaining_storage_energy /
                    (conversion_efficiency * omega * requested_duration)
```

ที่ speed ศูนย์หรือต่ำกว่า minimum regen capacity เป็นศูนย์ Control policy ที่
ประกาศ allocate regen ก่อนแล้ว mechanical Mechanical capacity เท่ากับ
`maximum_mechanical_torque * Work014_start_derating`

Tyre ceiling ใช้ scale ร่วมกับ allocated path ทั้งสอง จึงเก็บ blend ที่ขอแทนการ
แทน path ที่ saturated ด้วยอีก path เงียบ Requested torque ที่ใช้ไม่ได้แสดงเป็น
`unserved_brake_torque_n_m` Torque residual แยกตรวจ:

```text
T_requested - T_applied_total - T_unserved = 0
```

## Energy และ Storage Accounting

Allocated torque ถูกล็อกต้น interval หาก event ตัด interval จะ integrate energy
ถึงเวลาที่ execute `dt_exec` เท่านั้น:

```text
E_regen_wheel = T_regen_applied * omega * dt_exec
E_stored      = efficiency * E_regen_wheel
E_regen_loss  = E_regen_wheel - E_stored
E_mech_heat   = T_mechanical_applied * omega * dt_exec
E_removed     = (T_regen_applied + T_mechanical_applied) * omega * dt_exec
```

Energy residual ที่สังเกตแยกคือ:

```text
E_removed - E_stored - E_regen_loss - E_mech_heat
```

Recovered energy เพิ่มเฉพาะ `stored_recovered_energy_j` และไม่เกิน capacity ที่
ประกาศ เป็น vehicle wheel work ที่ conserve พร้อม loss ชัดเจน ไม่ใช่ free energy
หรือการเติม primary propulsion energy ที่ไม่ได้ประกาศ

Storage-capacity torque limit คำนวณตลอด requested interval เมื่อ failure ตัด
interval model ไม่ optimize torque ใหม่เพื่อเติม storage capacity ที่ว่างเพิ่ม;
start-of-step command ยังคงเดิม

## Brake Heat และ Failure

Mechanical braking power คือ:

```text
P_mechanical_heat = T_mechanical_applied * omega
```

Power นี้เข้า lumped thermal model Work 014 พร้อม ambient/cooling command ที่
ประกาศ Work 014 ให้ temperature integration, derating, energy residual,
overtemperature crossing exact และ latched failure

Evaluator หา candidate event time ของ suspension และ brake temperature ตลอด
requested interval ก่อน Event ที่เร็วสุดกำหนด `dt_exec` Tie exact คืน
`simultaneous` Final suspension, brake temperature, storage และ energy term ทุกตัว
ประเมินถึง `dt_exec` เท่านั้น Failure suspension/brake ที่ latch ก่อนเข้า interval
คืน `already_failed` โดยไม่ execute

## Result State

- `status=ok`, `failure_mode=none`: requested interval จบ
- `status=failed`, `failure_mode=suspension_travel`: travel limit crossing ก่อน
- `status=failed`, `failure_mode=brake_overtemperature`: thermal limit crossing ก่อน
- `status=failed`, `failure_mode=simultaneous`: candidate time tie exact
- `status=failed`, `failure_mode=already_failed`: failure latch ก่อนเข้า
- `status=invalid`: cross-contract, runtime ไม่ finite, capacity หรือ energy
  residual fail โดย state ไม่เปลี่ยน

## หลักฐานอ้างอิง

`scripts/validate_suspension_braking.py` ตรวจ:

- request `150 N*m` allocate regen `100 N*m` และ mechanical `50 N*m`;
- ที่ `10 rad/s` เป็น `1 s`, wheel energy `1500 J` กลายเป็น stored `800 J`,
  conversion loss `200 J` และ brake heat `500 J` พร้อม residual ศูนย์;
- suspension ถึง `0.1 m` ที่ `5 s` exact และเหลือ `5 s` unexecuted;
- adiabatic brake heating ถึง `400 K` ที่ `50 s` exact สร้าง mechanical heat
  `50000 J` และเหลือ `50 s` unexecuted;
- `mu=1`, `Fz=100 N`, `R=0.3 m` จำกัด torque `30 N*m`, เก็บ scale `0.2` และ
  แสดง unserved `120 N*m`; และ
- input เดียว replay exact

Unit suite ยังตรวจ constant-acceleration suspension motion, regen torque/power/
charge/storage limit ทุกตัว, zero-speed regen, thermal derating, simultaneous
travel/thermal failure, already-failed state, invalid contract และ runtime output
ไม่ finite

## ขอบเขต Integration ปัจจุบัน

Work 018 แสดง typed per-contact load, torque, energy, thermal และ failure evidence
แต่ยังไม่ integrate เข้า race state Work 015 หรือ multi-contact vehicle controller
Shared central storage allocation, combined lateral tyre capacity, wheel-speed
dynamics และ stopping distance ต้องเป็น coupling experiment ที่วางแผนแยก

## ข้อจำกัดและงานต่อ

- Suspension เป็น contact coordinate แบบ constant acceleration ไม่ใช่ coupled
  heave/pitch/roll, linkage kinematics, anti-geometry, compliance หรือ road input
- Wheel speed คงที่ใน interval; brake torque ยังไม่ update vehicle/wheel speed
- Regen-first เป็น policy ที่ประกาศ ไม่ใช่ optimized race strategy
- Thermal behavior เป็น lumped และไม่ calibrated; brake temperature ที่ผ่านไม่ใช่
  braking-safety evidence
- Work 019 รับผิดชอบ reliability, traffic, weather, degradation และ race strategy
