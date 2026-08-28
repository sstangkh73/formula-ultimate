# Coupling Contract และ Architecture

ต้นฉบับภาษาอังกฤษ: `COUPLING_CONTRACT_AND_ARCHITECTURE.md`

## สถานะและขอบเขตคำอ้าง

Work 021 สร้าง central contract ตัวแรกที่ execute ได้สำหรับ coupled-vehicle
program ประกอบด้วย:

- deterministic coupling architecture compiler แปด stage
- signal producer/consumer provenance ชัดเจน
- versioned experiment manifest ที่มี fingerprint
- shared vehicle state แบบ topology-neutral
- residual ledger ที่รู้ unit
- deterministic terminal-event arbitration

Reference architecture ประกาศว่า Level-0 capability group เดิมต้องแลก evidence
อย่างไรในอนาคต แต่ **ยังไม่** เรียก physics solver Work 011–019, advance coupled
vehicle, สร้าง race time หรือพิสูจน์ physical validation Validator Work 021
รายงาน `physics_execution_count: 0`

## เหตุผลที่ต้องมี Contract นี้

Physics module อิสระอาจผ่าน test ทุกตัวแต่ยัง coupling ผิด ตัวอย่าง integration
failure ได้แก่ ใช้ aerodynamic result ผิด timestep, ใช้ normal load หลัง resolve
tyre force แล้ว, นับ regenerative energy สองครั้ง, ให้ module เขียนทับ signal ของ
อีก module หรือ update shared state เพียงบางส่วนก่อน failure

Work 021 ย้าย error เหล่านี้มาเป็น fail-closed architecture boundary ก่อนมี
adapter execution จริง Work 022 เป็นเจ้าของ atomic execution และ state
commit/rollback semantics

## Canonical Causal Stage

ลำดับ stage ตายตัวคือ:

| Index | Stage | หน้าที่ที่ตั้งใจ |
|---:|---|---|
| 0 | `inputs` | Pin current state, circuit/environment evidence และ strategy/control command |
| 1 | `aerodynamics` | สร้าง aerodynamic force/moment และ cooling evidence |
| 2 | `load_balance` | Resolve chassis balance และ contact normal load |
| 3 | `contact_limits` | Resolve tyre, suspension, braking และ recovery limit ราย contact |
| 4 | `motion` | สร้าง candidate longitudinal/lateral/yaw motion state เดียว |
| 5 | `energy_audit` | สร้าง candidate energy state และ conservation evidence |
| 6 | `health` | สร้าง thermal/degradation/damage state และ failure candidate |
| 7 | `race_progress` | Reconcile candidate/residual และสร้าง next shared state/race event |

Module consume ได้เฉพาะ initial signal หรือ signal จาก stage ที่ก่อนหน้าอย่าง
เคร่งครัด Dependency จาก same/later stage ถูก reject อนาคตมีหลาย module ใน stage
เดียวได้ แต่ signal หนึ่งตัวยังมี producer เดียว

## Module และ Signal Contract

`CoupledModuleSpec` แต่ละตัวประกาศ:

```text
module_id
stage
model_version
consumes[]
produces[]
```

Compiler reject:

- module ID ว่างหรือซ้ำ
- stage ไม่รู้จักหรือ required stage หาย
- signal ว่างหรือซ้ำภายใน declaration หนึ่งตัว
- module consume/produce signal เดียวกัน
- initial/produced signal ที่มี producer หลายตัว
- consumed signal ที่ไม่มี producer
- dependency จาก same/later stage

Input module order ไม่ใช่ execution order Compiler sort ตาม canonical stage และ
module ID, sort signal set ที่ไม่มี semantics ด้านลำดับเพื่อ hash และสร้าง SHA-256
architecture fingerprint การ reverse module declaration/initial signal ทั้งหมด
ยังให้ compiled architecture เท่ากัน exact

## Reference Architecture

`config/simulation/coupled_level0_architecture_v1.json` ประกาศ:

```text
input_bridge
  -> aerodynamic_map
  -> normal_load_solver
  -> contact_limit_solver
  -> vehicle_motion_solver
  -> energy_graph_audit
  -> health_event_solver
  -> race_progress_solver
```

มี required stage ครบแปดและ initial/produced signal identity 24 ตัว Compiled
fingerprint คือ:

```text
51ca53e9d4c6058f67f61dc57f3ece7e8c24176d915e74069f27d0aa6999f8a6
```

JSON loader บังคับ root/module key set exact และชนิด JSON string/string-array จริง
ไม่แปลง number, boolean หรือ object เป็น signal/module name Unknown/missing field,
JSON ผิด และ type ผิด fail ด้วย `CouplingContractError`

ชื่อเหล่านี้ map capability boundary ปัจจุบัน ยังไม่ใช่ executable adapter
`model_version` pin ระบุ source evidence ที่ตั้งใจ แต่ไม่พิสูจน์ว่าสอง module ใช้
payload compatible แล้ว

## Experiment Manifest

`ExperimentManifest` pin identity ทั้งหมดก่อน coupled evaluation:

- `experiment_id` และ `candidate_id`
- design-language version
- geometry artifact ID และ lowercase SHA-256 hash อย่างน้อยหนึ่งรายการ
- component-catalog version
- circuit-profile ID
- regulatory, energy และ solver profile version
- model-version pin
- compiled architecture fingerprint
- source commit
- random seed
- evaluation budget
- timestep หน่วยวินาที

Artifact/model pin มี unique ID บังคับ syntax ของ commit/hash, budget บวก, seed
integer และ timestep finite/บวก Canonical manifest fingerprint sort artifact และ
model-pin identity จึงไม่เปลี่ยนเมื่อสลับ declaration แต่เปลี่ยนเมื่อ field สำคัญ
เช่น seed เปลี่ยน

Reference manifest Work 021 ใช้ seed `17`, budget `1000`, timestep `0.01 s` และ
fingerprint:

```text
7f40394bf539ef230870a758cfba81c093268d38f52c7efac359fdd9ec5fb416
```

Manifest เป็น identity contract ไม่ใช่สิทธิ์ให้ self-report physical property
Geometry hash ต้องชี้ artifact ที่ evaluate อิสระในงานหลัง

## Shared State แบบ Topology-Neutral

`SharedVehicleState` มี common runtime boundary ขั้นต่ำ:

- time และ race distance
- position/velocity 3D
- yaw และ yaw rate
- primary/recovered energy ที่เหลือ
- completed laps
- tuple ของ unique contact state จำนวนใดก็ได้แต่ต้องไม่ว่าง
- tuple ของ unique component-health state จำนวนใดก็ได้
- running/terminal status ชัดเจน

Contact แต่ละตัวมี ID, normal load, longitudinal/lateral force, suspension travel
และ angular speed Component-health state แต่ละตัวมี ID, temperature, degradation,
damage และ failure latch Input ต้อง finite และมี constraint ตามที่ physics ต้องการ

Contract รับ arrangement สาม contact `front/left/right` จาก validator ไม่บังคับสี่
ล้อ, left/right pair, axle, symmetry, conventional body หรือ powertrain technology
Field เหล่านี้เป็น shared evidence boundary งาน Work 022 ต้องรับประกันว่า adapter
เขียนเฉพาะ candidate output ที่ประกาศและ commit แบบ atomic

## Residual Ledger

`ResidualEntry` รองรับ quantity/unit exact:

| Quantity | Unit |
|---|---|
| `force` | `N` |
| `moment` | `N*m` |
| `energy` | `J` |
| `distance` | `m` |
| `time` | `s` |
| `state` | `1` |

Acceptance boundary คือ:

```text
tolerance = absolute_tolerance + relative_tolerance * scale
passed = abs(raw_residual) <= tolerance
```

เก็บ raw value ไว้ `ResidualLedger.status` เป็น `invalid` เมื่อ unique entry ใด fail
และลิสต์ failed residual ID exact Reference validator เก็บ `-2.0 J` และรายงาน ID
`energy` โดยไม่แก้เป็นศูนย์

## Event Arbitration

`EventCandidate` แต่ละตัวประกาศ unique ID, type, candidate time ไม่ติดลบ และ
source module Tie priority กลางคือ:

```text
finished
thermal_failure
reliability_failure
damage_failure
degradation_failure
energy_depletion
timeout
step_complete
```

หาเวลาที่เร็วสุดก่อน Candidate ภายใน `time_tolerance_s` ที่ประกาศถือเป็น tie แล้ว
ใช้ priority ข้างบน ตามด้วย event ID เป็น deterministic final key Decision เก็บ
true earliest time, tied candidate ID ทั้งหมด, winner และ tolerance

ใน reference tie exact ที่ `10.0 s`, `finished` ชนะ `thermal_failure` เมื่อ thermal
failure เกิด `9.9 s` มันชนะเพราะไม่ใช่ tie นี่คือ event semantics ที่ประกาศสำหรับ
Level-0 integration program ไม่ใช่ sporting/safety regulation จริง

## หลักฐาน Falsification

Test และ validator แสดง:

- replay reference architecture ที่ load แบบ exact
- stage coverage ครบแปด
- architecture/manifest permutation invariance
- deterministic SHA-256 identity
- reject missing producer, duplicate producer/ID, missing stage และ same/later-
  stage dependency
- reject extra/missing JSON key, malformed JSON, JSON type ผิด, hash/commit/
  budget/timestep ผิด และ version/artifact ID ซ้ำ
- รับและ replay shared state สาม contact แบบ arbitrary exact
- reject contact ว่าง/ซ้ำและ numeric/status ผิด
- residual pass/fail สังเกตได้พร้อม strict unit
- event localization/tie priority deterministic และ reject ID ซ้ำ

## ข้อจำกัดและ Boundary ถัดไป

- ยังไม่มี physics solver รันผ่าน architecture นี้
- Signal ตอนนี้มี identity/provenance name ไม่ใช่ typed runtime payload
- ยังไม่มี atomic start-state/output/next-state transaction
- ยังไม่มี adapter ยืนยันว่า unit/timing semantics Work 011–019 ตรง contract นี้
- ยังไม่วัด coupled force, moment, energy, thermal หรือ race residual
- Reference topology เป็น integration control ไม่ใช่ mandatory design
- Work 022 ต้องสร้าง adapter protocol, declared read/write set, atomic step
  transaction, rollback เมื่อ invalid และ reject partial write
- Level-0 contract success ไม่ใช่ physical validation, safety, manufacturability,
  technology discovery หรือ real-race evidence
