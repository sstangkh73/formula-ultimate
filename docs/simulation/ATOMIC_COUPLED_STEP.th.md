# Atomic Coupled-Step Transaction

ต้นฉบับภาษาอังกฤษ: `ATOMIC_COUPLED_STEP.md`

## สถานะและขอบเขตคำกล่าวอ้าง

Work 022 สร้าง generic execution boundary ระหว่าง architecture จาก Work 021 กับ
domain adapter ในอนาคต สามารถ execute adapter ที่ register แปดตัวตาม causal
order และ publish complete next-state transaction หนึ่งชุด

Reference validator ใช้ placeholder payload และรายงาน
`domain_physics_adapter_count: 0` ดังนั้น committed reference step พิสูจน์เฉพาะ
transaction behavior ไม่ได้พิสูจน์ว่า circuit, aerodynamic, contact, motion,
energy, thermal, health หรือ race physics เชื่อมถูกต้อง

## Transaction flow

```text
compiled architecture + immutable start state
              + exact initial signals + exact adapter set
                               |
                           preflight
                               |
                    private candidate signal bus
                               |
       adapters execute in compiled stage/module order
                               |
        validate identity, version, reads, writes, evidence
                               |
              validate complete monotonic state.next
                    /                          \
          publish all outputs             publish none
          + committed state               + failure/evidence
```

Registration order ไม่ใช่ execution order แม้สลับ adapter tuple ก็ยัง execute
ตาม compiled architecture เสมอ

## Runtime signal และ read isolation

`RuntimeSignal` เก็บ deep-copied payload snapshot และคืน copy ใหม่จาก property
`value` กับ adapter `read()` ทำให้ adapter ปกติไม่แชร์ mutable reference กับ
caller หรือ candidate bus

`AdapterReadView` มีเฉพาะ signal ที่อยู่ใน `consumes` ของ module ปัจจุบัน การอ่าน
ID อื่นทำให้เกิด `CoupledTransactionError` และมี immutable
`SharedVehicleState` เป็น common start-state identity นี่คือ trusted-code contract
ไม่ใช่ hostile Python sandbox

## Preflight gate

ก่อน execute adapter ตัวแรก `execute_coupled_step` บังคับ:

- initial-signal coverage ตรงพอดี ไม่มี ID หาย เกิน หรือซ้ำ
- payload `manifest.current_state` เท่ากับ `start_state` ที่ระบุ
- adapter coverage ตรงพอดี ไม่มี module ID หาย เกิน หรือซ้ำ
- `model_version` ของทุก adapter ตรงกับ compiled module pin

Preflight fail คืน invalid result ที่มี trace ศูนย์และ published signal ศูนย์ โดย
ไม่เรียก adapter

## Adapter contract

แต่ละ adapter ประกาศ `module_id`, `model_version` และ `execute(view)` Successful
`AdapterOutput` ต้อง:

- ระบุ module ที่กำลัง execute
- ใช้ status `ok`
- เขียนทุก signal ใน `produces` อย่างละหนึ่งครั้งและไม่มี signal อื่น
- ใช้ residual/event ID ไม่ซ้ำ
- ไม่มี failure reason

Adapter เลือกคืน status `invalid`, nonblank reason, evidence และ candidate write
ศูนย์ได้ Invalid output หยุด step ทันที การคืน write พร้อม invalid status เป็น
protocol violation

Exception, ค่าที่ไม่ใช่ `AdapterOutput`, module identity ผิด และ write set ผิดรูป
กลายเป็น `adapter_exception` ที่สังเกตได้ และหยุดที่ module นั้น

## การเก็บ Evidence

`CoupledStepResult` เก็บ:

- `AdapterTrace` ตามลำดับ
- raw `ResidualEntry` รวม value, unit, scale และ tolerance
- raw `EventCandidate`

Evidence ที่เกิดจนถึง module ที่หยุดยังตรวจได้หลัง rollback Residual/event ID ต้อง
unique ทั้ง step Failed residual คืน `residual_failure` พร้อมค่าดิบจริงโดยไม่แก้
ค่า การเก็บ evidence แยกจาก state publication ดังนั้น invalid result ยังมี
`published_signals` ว่าง

## Atomic commit และ rollback

Successful adapter output ทั้งหมดอยู่ใน private candidate bus จน module สุดท้าย
เสร็จ `state.next` ต้องมีอยู่ เป็น `SharedVehicleState` และ `time_s` กับ
`race_distance_m` ห้ามถอยหลัง

เมื่อผ่านครบเท่านั้น result จึงเปิดเผย:

- status `committed`
- complete `committed_state` หนึ่งชุด
- reference produced signal ทั้ง 21 ตัว
- trace และ evidence ทั้งหมด

Invalid result ทุกตัวเปิดเผย:

- status `invalid`
- failure code/reason/module แบบมีโครงสร้าง
- `committed_state = None`
- `published_signals = ()`
- `rolled_back_state` เท่ากับ start state เดิม

ไม่มีการ mutate state ในที่เดิม และ candidate signal ก่อนหน้าไม่ถูก publish เมื่อ
เกิด failure ภายหลัง

## Failure code

Boundary ที่ implement แล้วรายงาน code ชัดเจน เช่น:

- `initial_signal_coverage`
- `current_state_signal_missing`
- `current_state_mismatch`
- `adapter_coverage`
- `adapter_version_mismatch`
- `adapter_exception`
- `adapter_invalid`
- `evidence_identity_duplicate`
- `residual_failure`
- `next_state_missing`
- `next_state_type`
- `time_regression`
- `distance_regression`

## หลักฐาน Validation

Deterministic reference execute:

```text
input_bridge -> aerodynamic_map -> normal_load_solver
-> contact_limit_solver -> vehicle_motion_solver
-> energy_graph_audit -> health_event_solver
-> race_progress_solver
```

Placeholder state เดินจาก `4.0 s` เป็น `4.01 s` และ `100.0 m` เป็น `100.3 m`,
publish 21 output หลัง trace แปดตัวผ่านเท่านั้น และ replay ตรงกันเมื่อกลับลำดับ
adapter กับ initial-signal registration

Falsification ครอบคลุม preflight failure, undeclared read, missing/extra write,
identity/version/return type ผิด, invalid adapter output, failed residual,
exception, invalid write ตอน fail, next-state type ผิด, time regression และ
distance regression ทุก invalidity เก็บ start state และ publish signal ศูนย์

## ข้อจำกัดและ Boundary ถัดไป

- บังคับ payload identity/atomicity แล้ว แต่ real adapter ยังไม่ให้ domain unit และ
  semantics
- Deep-copy isolation อาจไม่เหมาะกับ array ขนาดใหญ่มากในอนาคต; zero-copy ที่มา
  แทนต้องรักษา immutability evidence เท่าเดิม
- Monotonic time/distance จำเป็นแต่ไม่เพียงพอสำหรับ valid motion
- Work 023 ต้องสร้าง typed deterministic circuit, environment, weather, traffic
  และ strategy input สำหรับ profile สิบสนาม
- Level-0 transaction success ไม่ใช่ physical validation, safety,
  manufacturability, discovery หรือ race superiority
