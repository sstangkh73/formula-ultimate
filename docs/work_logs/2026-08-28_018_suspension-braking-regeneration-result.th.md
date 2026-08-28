# ผล Work 018: Suspension, Mechanical Braking และ Regeneration

ต้นฉบับภาษาอังกฤษ: `2026-08-28_018_suspension-braking-regeneration-result.md`

สถานะ: Completed

## ผลลัพธ์

Work 018 เสร็จสมบูรณ์ `work018-suspension-braking-v1` ประเมิน ground-contact
interval แบบ topology-neutral หนึ่งตัวพร้อม upstream normal load ชัดเจน,
spring/damper travel, tyre-limited regen-first/mechanical braking,
recovered-energy storage/conversion loss, mechanical brake heat, thermal
derating จาก Work 014 และ earliest-event truncation สำหรับ suspension travel หรือ
brake overtemperature

สมมติฐานหลักได้รับการสนับสนุนใน model boundary: requested braking ถูกใช้เฉพาะ
ส่วนที่ contact load, component torque/power, storage, suspension travel และ
thermal survival รองรับ Recovered energy ปิด exact กับ removed wheel work และ
conversion loss ที่ประกาศ ไม่มี free energy หรือ primary energy ที่ไม่ได้ประกาศ

นี่เป็น Level-0 software/analytical evidence ไม่ใช่ whole-vehicle braking หรือ
safety validation

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/physics/suspension_braking.py`: module/state/input
  contract, suspension motion/event, torque limit/allocation, thermal coupling
  Work 014, event truncation, regen storage, energy/torque/force residual และ
  invalidity ที่สังเกตได้
- `src/formula_ultimate/physics/__init__.py`: export API Work 018
- `tests/test_suspension_braking.py`: 13 tests สำหรับ analytical, limit, failure,
  replay, invalid contract และ numerical failure
- `scripts/validate_suspension_braking.py`: validator ของ suspension, energy,
  thermal, tyre และ replay reference
- `docs/physics/SUSPENSION_BRAKING_REGEN_MODEL.md` และ `.th.md`: สมการ,
  event/energy semantics, evidence, integration boundary และ limitation
- `docs/problem_reports/2026-08-28_018_tyre-limit-fixture-suspension-failure.md`
  และ `.th.md`: coupled-fixture failure, root cause, correction และ rerun
- queue และคู่ plan/result Work 018 สองภาษานี้

## การตัดสินใจและหลักฐาน

1. Evaluator model contact module ใดก็ได้หนึ่งตัว ไม่กำหนด wheel count, axle pair,
   symmetry หรือ layout แบบเดิม
2. Normal load เป็น upstream evidence ชัดเจน; Work 018 ไม่ redistribute
3. Spring/damper force ต้น step ให้ travel acceleration คงที่ Travel bound สองด้าน
   ใช้ analytical outward-crossing localization โดยไม่ clip
4. Regen capacity เป็นค่าต่ำสุดของ component torque, generator-input power,
   storage charge power และ remaining storage energy ตลอด requested step
5. Allocate regen ก่อน mechanical torque ที่ thermal-derated Tyre scale เดียวเก็บ
   blend ขณะที่ torque ที่รองรับไม่ได้ยังสังเกตได้
6. Mechanical wheel work กลายเป็น brake heat Work 014 Regen wheel work กลายเป็น
   stored energy + conversion loss และ residual แยกปิดศูนย์
7. Travel/temperature failure ที่เร็วสุดตัด motion, heat และ energy พร้อมกัน Tie
   event exact คืน `simultaneous`; prior failure คืน `already_failed` โดยไม่ execute

## ปัญหาที่พบและแก้แล้ว

การรัน Work 018 ครั้งแรกผ่าน 12 tests และ fail tyre-limit reference Fixture ลด
normal load เป็น `100 N` แต่ยังใช้ suspension preload `1000 N` ทำให้ production
model สร้าง rebound acceleration และ travel failure ได้ถูกต้อง Independent
variable ที่ตั้งใจคือ tyre capacity ไม่ใช่ suspension imbalance Test/validator
จึงใช้ preload/load เท่ากัน `100 N` โดยไม่ผ่อน production solver การรันใหม่ผ่าน
13 tests และแสดง applied `30 N*m`, unserved `120 N*m` โดยไม่มี suspension event

## ทบทวนการทดลอง

- Independent variables: normal load, suspension mass/stiffness/damping/preload/
  travel, wheel speed, brake request, radius/friction, mechanical/regen torque,
  generator/charge power, efficiency, storage, thermal state/parameter, cooling,
  ambient และ interval duration
- Dependent variables: suspension force/acceleration/travel, event time/mode,
  torque limit/allocation/scale/unserved ทุกตัว, wheel/stored/loss/heat energy,
  brake temperature, end state, status และ residual สี่ตัว
- Controls: SI/sign convention, regen-first policy, tyre scaling ร่วม,
  start-of-step torque/speed/load คงที่, solver Work 014, earliest-event semantics,
  exact tie classification และ random draw ศูนย์
- Metrics: analytical travel/time error, torque/force/energy residual, storage
  capacity, regen limit value, temperature/failure time, replay equality และ
  invalid coverage
- Supporting evidence: equilibrium force residual ศูนย์; constant-acceleration
  motion ตรง analytical; ordinary braking ปิด `1500 J` เป็น stored `800 J`, regen
  loss `200 J` และ heat `500 J`; replay exact
- Falsifying evidence: travel crossing ที่ `5 s`; brake ถึง `400 K` ที่ `50 s`;
  tie travel/thermal simultaneous ที่ `50 s`; tyre limit ทิ้ง unserved torque;
  regen torque/power/charge/storage และ zero-speed limit bind ทุกตัว; prior failure
  และ extreme finite arithmetic ไม่ execute เงียบ
- Contradicting evidence: tyre fixture แรกคืน suspension failure ขัดกับ test
  expectation แต่เปิดเผย input imbalance แบบ coupled ได้ถูกต้องและเก็บใน report
- Alternative explanations: energy closure อย่างเดียวอาจผ่านแม้ torque เกิน จึง
  test tyre, component, power, capacity, derating, event และ unserved torque แยก
- Missing evidence: coupled chassis/road/link geometry, combined lateral tyre,
  wheel/vehicle deceleration, central shared storage, pressure/inverter/battery
  map, calibrated brake thermal data และ stopping distance
- Confidence: สูงสำหรับ deterministic interval contract/internal accounting;
  ต่ำหรือไม่มีสำหรับ braking performance หรือ safety จริง

## หลักฐาน Validation

ทุกคำสั่งรันจาก `C:\Formula Ultimate` แบบ fail-fast

```powershell
python -m unittest tests.test_suspension_braking -v
```

Exit status: `0`; `Ran 13 tests`; `OK`

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`; `Ran 145 tests`; `OK`

```powershell
python scripts/validate_suspension_braking.py
```

Exit status: `0` ผลสำคัญ:

```text
ordinary torque regen/mechanical: 100.0 / 50.0 N*m
wheel energy removed: 1500.0 J
stored/loss/heat: 800.0 / 200.0 / 500.0 J
end brake temperature: 300.5 K
force/torque/energy residuals: 0
suspension failure: 5.0 s, travel 0.1 m, unexecuted 5.0 s
thermal failure: 50.0 s, 400.0 K, heat 50000.0 J, unexecuted 50.0 s
tyre limit/scale/applied/unserved: 30.0 N*m / 0.2 / 30.0 / 120.0 N*m
replay_equal: true
```

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` ทุกคำสั่ง Full validation รันซ้ำหลัง result นี้ และตรวจ staged
scope/check ก่อน commit

## ข้อจำกัดและงานต่อ

- Suspension เป็น independent constant-acceleration contact coordinate ไม่ใช่
  coupled chassis heave/pitch/roll หรือ detailed linkage/road dynamics
- Wheel speed คงที่ในแต่ละ interval จึงยังไม่ update stopping speed/distance
- Tyre limit เป็น longitudinal เท่านั้น ยังไม่กิน lateral-force capacity
- Regen storage เป็น per module ไม่ใช่ central shared vehicle store
- Model ยังไม่ integrate เข้า race state Work 015 หรือ vehicle controller
- Work 019 รับผิดชอบ reliability, traffic, weather, degradation และ strategy โดย
  ยังไม่ได้เริ่มในงานนี้
- รายงาน commit hash ใน final handoff และไม่ push remote
