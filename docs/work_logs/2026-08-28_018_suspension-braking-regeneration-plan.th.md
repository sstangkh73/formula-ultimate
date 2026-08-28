# แผน Work 018: Suspension, Mechanical Braking และ Regeneration

ต้นฉบับภาษาอังกฤษ: `2026-08-28_018_suspension-braking-regeneration-plan.md`

สถานะ: Completed

## วัตถุประสงค์

สร้าง ground-contact suspension/brake interval model ระดับ Level-0 ที่
deterministic ซึ่งคิด normal load, suspension force/travel, tyre-limited braking,
mechanical brake heat, regenerative storage/loss และ localized travel หรือ
overtemperature failure event โดยไม่กำหนด wheel count หรือ vehicle layout แบบเดิม

## ขอบเขต

- กำหนด SI contract สำหรับ ground-contact module อิสระ, suspension parameter/
  state, mechanical/regen limit, storage state, brake thermal state, interval
  input, output telemetry, residual และ failure mode
- รับ normal load เป็น upstream evidence ชัดเจนจาก Work 016 รวม aerodynamic-load
  coupling ในอนาคต; ไม่สร้างหรือ redistribute wheel load เงียบ
- ใช้ linear spring/damper force ต้น step และ constant-acceleration suspension
  update พร้อมหา travel-limit event แบบ analytical
- แบ่ง requested brake torque แบบ regen-first แล้ว mechanical ภายใต้ generator
  torque/power, storage charge power/capacity, brake thermal derating, mechanical
  torque และ tyre friction limit
- ใช้ tyre-limit scale ร่วมกับ regen/mechanical blend ที่ประกาศและเก็บ unserved
  torque แทนการเพิ่มอีก path เงียบ
- แปลง mechanical wheel work เป็น brake heat และ regenerative wheel work เป็น
  stored energy + conversion loss พร้อม energy residual ที่ปิดศูนย์
- ใช้ thermal integration และ exact failure crossing จาก Work 014 Event
  suspension/thermal ที่เร็วที่สุดตัด interval ทั้ง contact และแสดงเวลาที่ไม่ทำ
- Latch failure state และคืน failure mode `none`, `suspension_travel`,
  `brake_overtemperature`, `simultaneous` หรือ `already_failed`
- Test equilibrium, analytical suspension motion, localized travel failure,
  mechanical heat, regen energy, regen limit ทุกตัว, tyre saturation, thermal
  failure, already-failed state, replay exact, invalid input และ numerical
  invalidity
- เพิ่ม validator, เอกสาร model/result สองภาษา, problem report สองภาษาแยกทุก
  ปัญหาที่พบ และ commit แยก โดยไม่เริ่ม Work 019

## ไฟล์ที่วางแผน

- `src/formula_ultimate/physics/suspension_braking.py`
- `src/formula_ultimate/physics/__init__.py`
- `tests/test_suspension_braking.py`
- `scripts/validate_suspension_braking.py`
- `docs/physics/SUSPENSION_BRAKING_REGEN_MODEL.md` และ `.th.md`
- สถานะ queue และคู่ plan/result สองภาษานี้
- problem report สองภาษาแยกสำหรับปัญหาที่พบ

## ขอบเขต Suspension

Travel `x` เป็นบวกเมื่อ compression ที่ต้น interval:

```text
F_suspension = preload + k*x + c*v
a_travel     = (F_normal - F_suspension) / m_effective
x(t)         = x0 + v0*t + 0.5*a_travel*t^2
v(t)         = v0 + a_travel*t
```

Acceleration คงที่หนึ่ง interval ช่วง travel valid คือ
`[-maximum_rebound, maximum_compression]` จุด crossing ออกนอกขอบที่เร็วสุดจาก
quadratic/linear ถูกหาแบบ analytical เก็บ failure boundary exact โดยไม่ clip
travel และไม่ execute เวลาที่เหลือ

## ขอบเขต Brake Allocation และ Energy

สำหรับ requested torque `T_request` ไม่ติดลบ, wheel speed `omega`, effective
radius `R`, normal load `Fz` และ friction coefficient `mu`:

```text
T_tyre_limit = mu * Fz * R

T_regen_capacity = min(
    T_regen_max,
    P_generator_max / omega,
    P_charge_max / (eta_regen * omega),
    E_storage_remaining / (eta_regen * omega * dt)
)

T_regen_allocated = min(T_request, T_regen_capacity)
T_mech_allocated  = min(T_request - T_regen_allocated,
                        T_mech_max * thermal_derating)
tyre_scale        = min(1, T_tyre_limit /
                           (T_regen_allocated + T_mech_allocated))
```

ที่ speed ศูนย์/ต่ำกว่า minimum regen speed regen capacity เป็นศูนย์ Allocated
torque ถูกล็อกต้น interval หาก event ตัด interval storage capacity ที่ไม่ได้ใช้ยัง
เหลือและไม่ optimize torque ใหม่หลัง event

สำหรับเวลาที่ execute `dt_exec`:

```text
E_regen_wheel = T_regen_applied * omega * dt_exec
E_stored      = eta_regen * E_regen_wheel
E_regen_loss  = E_regen_wheel - E_stored
E_mech_heat   = T_mech_applied * omega * dt_exec

E_removed - E_stored - E_regen_loss - E_mech_heat = residual
```

Recovered energy เพิ่มเฉพาะ storage state ที่ประกาศและไม่เกิน capacity นี่คือ
recovery ของ vehicle kinetic work ที่สังเกตได้ ไม่ใช่การเติม primary energy หรือ
free energy

## ความหมาย Event

Model คำนวณ candidate suspension travel crossing และ brake-temperature crossing
จาก Work 014 ตลอด requested interval ก่อน Event ที่เร็วที่สุดกำหนดเวลาที่ execute
Tie เวลา exact คืน `simultaneous` State และ energy คำนวณถึงเวลานั้นเท่านั้น
Suspension หรือ brake ที่ fail มาก่อนคืน `already_failed` ที่ execute time ศูนย์

## นิยามการทดลอง

- สมมติฐานหลัก: braking command admissible ทางฟิสิกส์เฉพาะส่วนที่ contact load,
  suspension travel, component limit, storage capacity และ thermal survival
  รองรับ; recovered energy ต้องปิดกับ removed wheel work
- Independent variables: normal load, suspension state/parameter, wheel speed,
  requested torque, tyre friction/radius, mechanical/regen limit, efficiency,
  storage capacity/state, thermal parameter/state, cooling, ambient และ step
- Dependent variables: suspension force/acceleration/travel, tyre/regen/mechanical
  limit/torque, unserved torque, wheel/brake/storage/loss energy, brake
  temperature, event time/mode, state, residual และ status
- Controls: SI/sign convention, regen-first allocation, tyre scaling ร่วม,
  start-of-step input คงที่, thermal solver Work 014, event priority deterministic
  และ random draw ศูนย์
- Metrics: suspension force residual, travel/event-time error, torque residual,
  energy residual, storage monotonicity/capacity, temperature/failure time,
  replay equality และ invalid-case coverage
- Success: equilibrium/constant-acceleration reference ตรง analytical; travel/
  thermal failure localized; torque/power/energy limit ทั้งหมดผ่าน; energy balance
  ปิดและ repository gate ผ่าน
- Failure criteria: travel นอก limit, thermal failure, declaration ติดลบ/ไม่ finite,
  storage เกิน capacity, energy residual เกิน tolerance หรือ runtime numerical
  failure
- Falsification: บังคับ travel crossing, brake overtemperature, tyre saturation,
  generator torque/power limit, charge-power limit, storage-capacity limit,
  zero-speed regen, already-failed state และ extreme finite arithmetic โดยห้าม
  accept หรือสร้าง energy เงียบ

## ความเสี่ยง

- Contact module อิสระไม่มี coupled chassis heave/pitch/roll, anti-geometry,
  link kinematics, compliance, unsprung tyre stiffness และ road input
- Constant acceleration และ constant wheel speed ในหนึ่ง step เป็น reduced-order
  assumption; transient fidelity ขึ้นกับ step size
- Regen-first เป็น controller policy ที่ประกาศ ไม่ใช่หลักฐานว่า strategy optimal
- Tyre braking ใช้ longitudinal ceiling `mu*Fz` และไม่กิน lateral capacity จนกว่า
  coupling Work 011/016 ในอนาคตจะส่ง evidence นั้น

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่บังคับ wheel count/layout แบบเดิม ไม่มี detailed linkage geometry, hydraulic
  pressure network, ABS controller, inverter map, battery chemistry หรือ full
  vehicle stopping-distance claim
- ไม่ integrate เข้า race loop Work 015 หรืออ้าง braking safety จริง
- ไม่ทำ Work 019 และไม่ push remote

## Validation

```powershell
python -m unittest tests.test_suspension_braking -v
python -m unittest discover -s tests -v
python scripts/validate_suspension_braking.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

ทุก gate รัน fail-fast การเสร็จต้องมี result สองภาษา, problem report แยกสำหรับ
ปัญหาที่พบ, staged scope ที่ระบุ, commit สำเร็จ และหลักฐาน clean-state/hash หลัง
commit
