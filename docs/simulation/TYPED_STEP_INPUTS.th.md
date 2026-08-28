# Typed Circuit และ Environment Step Inputs

ต้นฉบับภาษาอังกฤษ: `TYPED_STEP_INPUTS.md`

## สถานะและขอบเขตคำกล่าวอ้าง

Work 023 กำหนด typed evidence ที่เข้าสู่ stage `inputs` แรกของ coupled
architecture โดย resolve real-circuit catalog สิบสนามแบบ deterministic และเชื่อม
complete scenario กับ atomic adapter protocol จาก Work 022

Catalog ไม่มี surveyed local corridor geometry, event-time weather หรือ traffic
scenario ดังนั้น catalog-only resolution ทั้งสิบเป็น `incomplete`; validator
รายงาน `real_physics_ready_profile_count: 0` นี่คือ evidence ที่ตั้งใจเก็บ ไม่ใช่
การเติม neutral condition ขึ้นเอง

## Typed record

`SpatialStepEvidence` ประกาศ circuit/segment identity, source, curvature หน่วย
`1/m`, grade/bank หน่วย radian, width ซ้าย/ขวาหน่วย metre และ horizontal
uncertainty หน่วย metre Status เป็น `available` พร้อม SI field ครบ หรือ `missing`
พร้อมเหตุผลและไม่มี numeric value

`WeatherStepEvidence` ประกาศ source, อุณหภูมิอากาศ/ผิวสนามหน่วย kelvin, pressure
หน่วย pascal, relative humidity ใน `[0,1]`, 3D wind velocity หน่วย `m/s` และ
precipitation mass flux หน่วย `kg/(m^2*s)` Status เป็น `observed` พร้อม field ครบ
หรือ `missing` โดยไม่มี numeric default

`TrafficStepEvidence` แยก:

- `isolated_control`: ทดลองที่ประกาศชัดว่ารถใกล้เคียงเป็นศูนย์
- `observed`: จำนวนรถใกล้เคียง non-negative ที่มี source
- `missing`: ไม่ทราบ traffic และห้ามตีความเป็นศูนย์

`StrategyStepCommand` มี throttle, brake, recovery fraction ใน `[0,1]` และ
normalized steering request ใน `[-1,1]`

## Scenario resolution และ Identity

`CircuitInputScenario` ผูก immutable `CircuitProfile`, race distance และ spatial/
weather/traffic evidence ที่ circuit ตรงกัน Cross-circuit evidence และ distance
นอก `[0, race_distance_m]` ถูก reject

`resolve_step_inputs` คืน `ready` เมื่อมี spatial/weather evidence และ traffic ถูก
ประกาศ observed หรือ isolated เท่านั้น กรณีอื่นคืน `incomplete` พร้อม ordered
`missing_evidence`

SHA-256 fingerprint รวม circuit profile ทั้งชุด, nested source evidence/access
date, race distance, evidence สามชุด และ strategy command การสลับลำดับสิบ profile
ไม่เปลี่ยน fingerprint รายสนาม แต่การแก้ profile content ภายใต้ ID เดิมทำให้ hash
เปลี่ยน

## Input adapter

`CircuitEnvironmentInputAdapter` ใช้ identity `input_bridge` จาก compiled
architecture และอ่าน:

```text
manifest.circuit_profile   -> CircuitInputScenario
manifest.current_state     -> SharedVehicleState
manifest.strategy_command  -> StrategyStepCommand
```

Ready scenario emit ตรงสี่ signal:

```text
circuit.segment_inputs     -> SpatialStepEvidence
control.step_command       -> StrategyStepCommand
environment.step_inputs    -> EnvironmentStepInputs(weather, traffic)
state.current              -> SharedVehicleState
```

Incomplete หรือ wrong-typed scenario คืน `AdapterOutput(status="invalid")` พร้อม
reason และ write ศูนย์ จากนั้น Work 022 rollback ทั้ง step

## ผล Evidence สิบสนาม

Versioned catalog มี Monaco, Monza, Spa, Singapore, Suzuka, Silverstone,
Hungaroring, Mexico City, Bahrain และ Sao Paulo ทุกสนาม resolve deterministic แต่
ปัจจุบันรายงานตรงกันว่า:

```text
missing_evidence = ("spatial", "weather", "traffic")
status = "incomplete"
```

ข้อมูลระดับ circuit เช่น lap length, race distance, turns, width evidence,
altitude และ design pressure ใช้แทน local segment corridor หรือ event-time
condition ไม่ได้

## Analytical fixture

Complete analytical fixture หนึ่งชุดให้ geometry, observed weather และ traffic
แบบ `isolated_control` อย่างชัดเจน จึง resolve `ready` และ emit typed signal สี่ตัว
Fixture นี้ validate contract เท่านั้น ไม่ถูกนำไปอ้างเป็น geometry/weather ของ
สนามจริง

## Falsification และข้อจำกัด

Test reject cross-circuit evidence, non-finite/out-of-range value, missing record
ที่แฝง neutral zero, unknown traffic ที่ตีความเป็น isolated, distance นอกเรซ และ
adapter payload type ผิด พร้อมพิสูจน์ replay, fingerprint เปลี่ยนเมื่อ profile
content เปลี่ยน และ incomplete input มี write ศูนย์

Work 024 รับได้เฉพาะ ready typed input เพื่อ couple aerodynamic force/cooling
evidence เข้ากับ chassis force/moment และ normal load Work 023 ไม่ execute aero
หรือ vehicle physics และไม่ใช่ physical validation, safety, manufacturability,
discovery หรือ race-performance evidence
