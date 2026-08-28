# Formula Ultimate: รายงานสถานะ ความพร้อม และทิศทางโครงการ

ต้นฉบับภาษาอังกฤษ: `PROJECT_STATUS_AND_DIRECTION_2026-08-28.md`

## Snapshot ของรายงาน

| หัวข้อ | ค่า |
|---|---|
| วันที่รายงาน | 2026-08-28 |
| Local branch | `main` |
| Evidence baseline | `0992f5c` — `feat(physics): complete digital race strategy model` |
| ลำดับงานที่เสร็จ | Work 001–019 |
| Physics queue | Work 010–019 เสร็จครบ |
| Automated suite ปัจจุบัน | 154 tests ผ่านก่อนสร้างรายงานนี้ |
| คำอ้างกว้างที่สุดที่รองรับ | ฐาน software/analytical ระดับ Level-0 แบบ deterministic |
| คำอ้างที่ยังไม่รองรับ | รถทั้งคัน, autonomous discovery, physical validation, ความเหนือกว่าในสนามจริง, safety หรือ manufacturability |
| สถานะ Remote | ก่อน Work 020 local `main` นำ `origin/main` 14 commits; หลัง commit รายงานนี้จะนำ 15 commits และงานนี้ไม่ push |

รายงานนี้คือสถานะปัจจุบัน ข้อความ “current phase” เก่าใน README และ research
charter ถูกเขียนก่อน Work 010–019 จึงบอก inventory ของ Level-0 module ต่ำกว่า
ปัจจุบัน เอกสารเหล่านั้นยังเป็น input ทางประวัติศาสตร์ของโครงการ แต่ควร reconcile
ใน documentation work item แยกก่อน experimental phase ถัดไป

## บทสรุปผู้บริหาร

Formula Ultimate มีเป้าหมายทดสอบว่า autonomous agent สามารถค้นพบสถาปัตยกรรม
รถแข่ง 3D ทั้งคันและเทคโนโลยี component โดยไม่ถูกบังคับให้ใช้ layout รถแบบเดิม
ได้หรือไม่ Design domain ในอนาคตอาจรวม body topology, ground-contact
arrangement, energy system, cooling path, structure, joint, fastener และ
geometry ภายใน component ที่ไม่คุ้นเคย

โปรเจกต์ไม่ได้ตัด physics, race discipline, energy accounting, resource,
safety, evidence หรือ reproducibility ออก “เร็วที่สุด” หมายถึงเวลาแข่งขันรวมต่ำ
ที่สุดในกลุ่ม candidate ที่จบเรซเดียวกันและผ่าน evidence gate เดียวกัน Primary
propulsion energy ทั้งหมดต้องอยู่บนรถก่อนแข่ง ห้ามเพิ่ม primary energy ที่ไม่
ประกาศระหว่างแข่ง Internal recovery ทำได้เมื่อแหล่งทางฟิสิกส์, conversion loss
และ conservation residual ยังสังเกตได้

Repository ก้าวพ้น bootstrap ไปมากแล้ว ปัจจุบันมี:

- workflow วิจัยสองภาษาที่มี governance และ commit รองรับ
- constrained geometry evidence loop
  `CadQuery -> STEP -> FreeCAD -> Level 0`
- profile สนามจริงสิบสนามที่ audit แหล่งข้อมูลได้
- Level-0 model อิสระสำหรับ longitudinal motion, track corridor, tyre-force
  saturation, energy topology, energy conservation, thermal state, race
  completion, lateral/yaw/load transfer, aerodynamics/cooling,
  suspension/braking/regeneration และ multi-event race strategy/reliability
- deterministic replay, invalid state ชัดเจน, localized failure event และ
  conservation residual
- automated test ผ่าน 154 tests ที่ Work 019 baseline

สิ่งที่ยังไม่มีสำคัญไม่แพ้กัน: ยังไม่มี autonomous design agent, topology
evolution engine, complete-vehicle 3D grammar, integrated time-stepping vehicle
simulator, optimized baseline campaign, higher-fidelity promotion pipeline,
empirical calibration หรือ technology discovery ที่ validate แล้ว

ดังนั้นทิศทางถัดไปที่ถูกต้องคือ **integration before evolution**: สร้าง version
ของ experiment/candidate/state contract กลาง เชื่อม Level-0 module ที่มีเข้าเป็น
fixed-topology reference vehicle หนึ่งคัน สร้าง fair optimized baseline แล้วจึง
เปิด free-topology agent search วิธีนี้ป้องกัน novelty ที่อาศัย physics ซึ่งยังไม่
เชื่อมกันหรือ evidence ที่ไม่เท่ากัน

## 1. ทิศทางวิจัยที่กำหนดแล้ว

### 1.1 คำถามวิจัยระยะยาว

Autonomous agent สามารถสร้างรถแข่ง 3D ทั้งคันและเทคโนโลยี component ที่ไม่เคยมี
ซึ่งทำเวลาแข่งขันรวมดีกว่า conventional baseline ที่ optimize อย่างยุติธรรมใน
race environment จริงหลายแบบ และยังรอดผ่าน physics/evidence gate ที่มี fidelity
สูงขึ้นตามลำดับได้หรือไม่

สำหรับ race environment `r` objective ที่ประกาศคือ:

```text
d*_r = arg min_d T_race(d, r)
```

ภายใต้เงื่อนไขอย่างน้อย:

```text
RaceCompleted(d, r) = true
initial primary energy <= declared race energy budget
external primary-energy addition during race = 0
conservation residuals <= declared tolerances
complete 3D geometry is valid and physically accounted
required structural, thermal, aerodynamic, tyre, material,
manufacturing, numerical, and uncertainty gates pass
```

Peak speed, ระยะบางส่วนก่อนพัง, solver instability, hidden energy หรือ invalid
geometry ไม่ใช่ผลชนะ

### 1.2 สิ่งที่ตั้งใจเปิดกว้าง

ในอนาคต agent อาจเปลี่ยน:

- whole-vehicle topology, ขนาด, packaging, external surface และ aerodynamic
  architecture
- จำนวน ตำแหน่ง และหน้าที่ของ ground-contact endpoint ที่อนุญาต
- topology ของ source/store/converter/transmission/propulsor/cooling
- structure, housing, duct, rotor, joint, coupling และ fastener
- material distribution และ geometry ภายใน component
- race-specific strategy และ controller parameter

ชิ้นส่วนหน้าตาใหม่ไม่เป็น discovery อัตโนมัติ ต้องมี typed interface,
material/manufacturing assumption ที่ประกาศ, property ที่ derive จาก geometry,
load/failure ที่ evaluate อิสระ และ whole-race advantage ที่วัดได้ภายใต้ control
ยุติธรรม

### 1.3 สิ่งที่ยังเป็นข้อจำกัด

- SI-unit physics และ conservation
- ระยะเรซจริงและ environment เฉพาะสนาม
- primary-energy budget ที่ประกาศล่วงหน้าโดยไม่เติมกลางเรซ
- material, resource, compute และ evaluation budget ที่จำกัด
- numerical validity และ deterministic replay metadata
- safety และ failure observability
- fair fixed-topology baseline และ random seed ที่ตรงกัน
- promotion ผ่าน fidelity สูงกว่าก่อนคำอ้าง discovery

Open-ended design หมายถึงไม่บังคับ conventional architecture **ภายในขอบเขตการ
ทดลองที่ประกาศ** ไม่ได้หมายถึงไม่มีขอบเขต

## 2. งานที่เสร็จ: Work 001–019

| Work | Commit | ผลที่เสร็จ | ขอบเขตหลักฐาน |
|---:|---|---|---|
| 001 | `6b2d4cd` | Bootstrap physics-first repository, governance, package boundary, research charter, design language, validation ladder และ work-log protocol | Structure และ methodology เท่านั้น |
| 002 | `96e8db4` | เพิ่ม one-dimensional longitudinal motion แบบ deterministic พร้อม traction, drag, rolling resistance, grade, stop localization, telemetry, replay และ analytical test | Point-mass Level 0 แบบแคบ |
| 003 | `50af600` | เพิ่มไฟล์ไทยแยกและ automated bilingual Markdown coverage | Documentation contract ไม่ใช่ physics |
| 004 | `840f2b6` | วิจัย MCP-compatible engineering CAD tool และเลือกเส้นทาง CadQuery/FreeCAD/Fusion แบบหลายชั้น | Tooling research ณ 2026-08-23 |
| 005 | `f598799` | ยืนยัน Fusion MCP handshake, pinned CadQuery MCP, FreeCAD headless STEP flow, launcher และ environment evidence | Tool/environment proof; ยังไม่มี vehicle design |
| 006 | `455a9d0` | สร้าง `mounting_plate_v1` และ constrained `CadQuery -> STEP -> FreeCAD -> Level 0` loop Candidate valid สามตัวผ่านและ invalid หนึ่งตัวถูก reject ก่อน CAD | Pipeline coherence สำหรับ component grammar แบบ bounded หนึ่งชนิด |
| 007 | `a4ef20f` | กำหนดภารกิจ whole-vehicle แบบเปิด, technology-neutral energy comparison, finish-gated objective และกฎคำอ้าง discovery | Research framing |
| 008 | `774c66e` | เพิ่ม profile สนาม Formula One จริงสิบสนามแบบ deterministic/audited พร้อม conflicting design pressure และ width screening | Circuit evidence ระดับ profile ไม่ใช่ surveyed racing line |
| 009 | `da9cc4c` | บังคับ validated commit และ explicit scope ต่อ completed work ทุกงาน | Governance และ traceability |
| 010 | `37188b1` | เพิ่ม 3D piecewise corridor integrator และ static/swept/steering vehicle-envelope gate | Synthetic corridor validation; สนามจริงยัง indeterminate หากไม่มี surveyed geometry |
| 011 | `609329f` | เพิ่ม tyre friction circle/ellipse แบบ deterministic พร้อม requested/applied force, saturation, utilization และ residual | Capacity law ไม่ใช่ calibrated slip/transient tyre physics |
| 012 | `d1a9c54` | เพิ่ม typed source/converter/transmission/tyre/sink component graph และ fail-closed connection rule | Topology/interface validity เท่านั้น |
| 013 | `f1b4b90` | เพิ่ม independent energy audit ที่จับ hidden energy, double-counted loss, missing evidence และ interface imbalance | Audit algebra/conservation ที่ประกาศ ไม่ได้พิสูจน์ upstream physics |
| 014 | `f3c3fce` | เพิ่ม lumped heating/cooling, thermal derating, analytical overtemperature localization, latched failure และ thermal residual | Lumped thermal ระดับ Level-0 |
| 015 | `19fd7bc` | เพิ่ม deterministic whole-race distance completion พร้อม finish, depletion, timeout, thermal failure และ invalid outcome บนสิบสนาม | Reduced-order completion gate ไม่ใช่ lap-time prediction |
| 016 | `abce996` | เพิ่ม ground-contact layout แบบ arbitrary full-rank, quasi-static normal load, lateral/yaw dynamics, load transfer, combined tyre limit และ balance residual | Planar rigid-body step ระดับ Level-0 |
| 017 | `435750e` | เพิ่ม aerodynamic coefficient map ที่มี provenance ข้าม speed, ride height, yaw และ active state พร้อม force/moment/cooling output และ envelope rejection | Synthetic/declared map ไม่ใช่ CFD หรือ measurement |
| 018 | `f77d9c3` | เพิ่ม contact suspension แบบ topology-neutral, tyre-limited mechanical/regen braking, storage/loss accounting, brake heat, derating และ failure localization | Independent contact interval ไม่ใช่ whole-vehicle braking safety |
| 019 | `0992f5c` | เพิ่ม multi-lap/multi-sector strategy, traffic, weather, degradation, damage, onboard-energy depletion, seeded reliability, deterministic replay และ localized terminal outcome | Level-0 strategy/failure selection ไม่ใช่ reliability หรือ race prediction จริง |

## 3. แผนที่ Capability ปัจจุบันของ Repository

```text
research constraints and experiment controls
  -> constrained candidate/geometry declarations
  -> CadQuery B-rep generation
  -> STEP artifact and hash
  -> independent FreeCAD geometry measurement
  -> typed component/power interfaces
  -> independent Level-0 physics evaluators
  -> conservation, failure, numerical, and replay evidence
  -> real-circuit distance and scenario gates
```

ลูกศรข้างบนอธิบาย stage ที่มี ไม่ใช่ production pipeline ที่เชื่อมครบหนึ่งเส้น
Work 006 เชื่อม mounting plate แบบ constrained หนึ่งชนิดเข้ากับ geometry-derived
mass และ longitudinal kernel รุ่นต้น Work 011–019 ส่วนใหญ่เปิด model/validator
อิสระ Causal link กลางจาก whole-vehicle CAD ใดๆ ผ่าน physics module ทั้งหมดไปยัง
race fitness ยังไม่มี

### 3.1 Governance และ Reproducibility

| Capability | สถานะ | หลักฐาน |
|---|---|---|
| Plan ก่อน implementation | พร้อม | บังคับ record Work 001–020 สองภาษา |
| Result และ limitation record | พร้อม | Completed plan ทุกตัวต้องมี matching result |
| Explicit validated commit | พร้อม | Selective staging, fail-fast validation, cached diff check, commit hash และ clean-tree check |
| Maintained Markdown สองภาษา | พร้อม | Repository test บังคับ companion `.md` และ `.th.md` |
| Deterministic replay | พร้อมระดับ module | Immutable input/result และ fixed seed ใน physics test/digital race |
| Reproducible research run manifest | พร้อมบางส่วน | แต่ละ model มี metadata แต่ยังไม่มี schema เดียวครอบคลุม CAD, component graph, solver, circuit, seed และ artifact hash |

### 3.2 CAD และ Geometry

| Capability | สถานะ | หลักฐานและข้อจำกัด |
|---|---|---|
| CadQuery code-first solid generation | พร้อมสำหรับ controlled local experiment | Work 005 ยืนยัน CadQuery 2.8.0 และ pinned MCP; ควร recheck environment ก่อน CAD campaign ใหม่ |
| STEP export และ hashing | พร้อม | Work 005/006 เก็บ identity ของ exchange artifact |
| Independent FreeCAD import/measurement | พร้อมสำหรับ bounded loop ปัจจุบัน | FreeCAD 1.1.3 วัด solid count, bounds และ volume อิสระใน environment ที่บันทึก |
| Constrained component grammar | พร้อมบางส่วน | มีเพียง `mounting_plate_v1`; พิสูจน์ grammar enforcement ไม่ใช่ general component invention |
| Complete vehicle assembly/B-rep | ยังไม่พร้อม | ไม่มี vehicle grammar, assembly interface solver, collision/packaging system หรือ complete CAD candidate |
| Geometry-derived inertia/structure/flow | ยังไม่พร้อมแบบ end-to-end gate | พิสูจน์ mass/volume แล้ว แต่ general inertia, FEA, CFD, manufacturing และ material-failure promotion ยังไม่มี |

### 3.3 Circuit และ Race Environment

มีสิบ profile:

1. Monaco
2. Monza
3. Spa-Francorchamps
4. Singapore
5. Suzuka
6. Silverstone
7. Hungaroring
8. Mexico City
9. São Paulo
10. Bahrain

แต่ละ profile มี published lap length, race laps, race distance, circuit
metadata, design-pressure score, strengths/weaknesses, source evidence และ
width/altitude input ที่หาได้ Work 019 เก็บ published race-distance residual
อย่างชัดเจนใน final event

สิ่งที่พร้อม: pre-design diversity, published-distance race gate, air-density
reference ที่คิด altitude และ sourced static-width screening เมื่อ evidence ใช้ได้

สิ่งที่ไม่พร้อม: surveyed 3D centerline/corridor, local width, kerb, barrier,
surface/friction map, bump, drainage, wind field, racing line, pit lane, flag
zone หรือ empirical weather ดังนั้น real-circuit swept-envelope admission ยังเป็น
`indeterminate` ไม่ใช่ passed

### 3.4 Physics และ Race Module

| Module | พร้อมตอนนี้ | ขอบเขตสำคัญ |
|---|---|---|
| Longitudinal | Analytical Level-0 reference และ deterministic telemetry | Force command มาจากภายนอก; ยังไม่เชื่อม complete drivetrain |
| Corridor | Synthetic 3D path integration และ rigid swept-envelope rejection | ไม่มี surveyed real geometry ที่ admission-capable |
| Tyre | Combined longitudinal/lateral force capacity และ saturation | ไม่มี slip ratio/angle, load sensitivity, temperature, wear หรือ transient contact model |
| Energy graph | Typed topology/interface compiler | ไม่สร้างหรือ validate ค่า energy |
| Energy audit | Independent balance/transfer evidence | ขึ้นกับ upstream energy evidence ที่ถูกต้อง |
| Thermal | Lumped heating/cooling/derating/failure | ไม่มี calibrated distributed thermal network |
| Race completion | Deterministic distance/energy/thermal outcome gate | Reduced-order และไม่ใช่ lap-time model |
| Lateral/yaw | Planar step, arbitrary contact, load projection และ combined tyre use | Quasi-static load transfer และไม่มี full multibody suspension |
| Aerodynamics | Interpolated coefficient map, force/moment และ cooling flow | Map evidence อาจ synthetic; ไม่มี CFD หรือ wind-tunnel validation |
| Suspension/braking/regen | Independent contact travel, torque limit, heat, storage และ localized failure | ไม่มี centrally coupled chassis, wheel-speed dynamics, ABS หรือ stopping-distance validation |
| Digital race | Multi-lap strategy, traffic/weather event, wear/damage และ seeded reliability | Abstract sector coefficient และ scenario multiplier ที่ยังไม่ calibrate |

## 4. สิ่งที่พร้อมตอนนี้

งานต่อไปนี้ทำได้อย่างมีหลักฐาน **ภายใน Level-0 boundary ที่ประกาศ**:

1. สร้าง versioned deterministic unit/reference experiment ใน SI units
2. สร้างและวัด constrained CadQuery component อิสระที่อยู่ใน grammar ที่อนุมัติ
   เช่น `mounting_plate_v1`
3. Reject invalid geometry parameter ก่อน CAD และ reject measurement ของ
   CadQuery/FreeCAD ที่ไม่ตรงกันหลัง STEP exchange
4. Screen candidate กับ design pressure ของสิบสนามก่อนออกแบบ และ exact
   published race distance หลังออกแบบ
5. Compile power/energy component graph ที่ประกาศและ reject carrier, direction,
   fan-out, cycle, endpoint หรือ required-port topology ที่ผิด
6. Audit energy flow ที่ประกาศแบบอิสระและแสดง hidden/double-counted energy
7. Evaluate Level-0 law แยกสำหรับ tyre capacity, thermal failure,
   lateral/yaw/load transfer, aerodynamic map, suspension/braking/regen และ
   event-level race strategy
8. บังคับและแยก finish, depletion, reliability, damage, degradation, thermal
   failure, timeout, saturation, non-convergence และ invalid numerical outcome
9. Replay module/scenario ที่ประกาศแบบ exact ด้วย input และ seed เดิม
10. ใช้ suite ปัจจุบันเป็น regression foundation; Work 019 baseline ผ่าน 154 tests

Capability เหล่านี้พร้อมสำหรับ software research, interface design,
falsification fixture และ selection-gate development แต่ยังไม่พร้อมสำหรับคำอ้าง
รถแข่งจริง

## 5. สิ่งที่พร้อมบางส่วน

### 5.1 CAD Pipeline

Generation/exchange/measurement loop ในเครื่องพิสูจน์แล้ว แต่เฉพาะ mounting plate
แบบ bounded ต้องเพิ่ม assembly semantics, component family, material, load,
contact interface, manufacturing rule และ solver promotion ก่อน agent จะคิดค้น
เทคโนโลยีระดับรถ

### 5.2 ชุดสนาม

สิบ profile สร้าง conflicting objective และข้อจำกัดขนาด/ระยะจริงที่มีคุณค่า แต่
ไม่ใช่ digital twin ที่ครบ Geometry-dependent admission หรือ realistic lap
optimization ต้องยังไม่เปิดจนกว่าจะ version circuit evidence ที่ดีกว่า

### 5.3 Physics Stack

Module แต่ละตัวมีประโยชน์และ test ดี แต่ repository ยังไม่ส่ง shared state เดียว
ผ่านทั้งหมด เช่น aerodynamic load ยังไม่กระจายสู่ contact อัตโนมัติ, tyre force
ยังไม่ update common multibody state, brake recovery ยังไม่เป็น central energy-
graph transaction และ component degradation ยังไม่ derive จาก geometry/material
stress history

### 5.4 Race Strategy

Work 019 ทดสอบ pace/weather/traffic/failure scenario ที่ประกาศและ replay seeded
uncertainty ได้ แต่ sector rate เป็น input ไม่ใช่ output ของ detailed vehicle
module จึงเหมาะกับ contract/event test ไม่ใช่คำแนะนำ strategy จริง

## 6. สิ่งที่ยังไม่พร้อม

- Autonomous agent ที่ generate, mutate, repair และ select design
- Topology-evolution algorithm หรือ experiment runner ใน topology/simulation
  orchestration package ซึ่งปัจจุบันยังว่าง
- Complete 3D vehicle representation และ assembly/interface grammar
- Automatic extraction ของ full mass distribution, inertia tensor, stiffness,
  stress, fatigue, cooling, flow หรือ electromagnetic behavior จาก candidate
  geometry ใดๆ
- Unified vehicle state และ causal solver ที่เชื่อม Work 011–019
- Conventional fixed-topology baseline ที่ optimize ด้วย effort เทียบเท่า
- Fair free-topology เทียบ fixed-topology experimental campaign
- Multi-seed statistics, holdout circuit, ablation, uncertainty calibration หรือ
  surrogate auditing
- CFD, FEA, multibody, detailed tyre, crash หรือ empirical cross-validation
- Manufacturing feasibility, cost model, supply/material constraint, safety
  certification หรือ FIA eligibility จริง
- หลักฐานว่าค้นพบเทคโนโลยีใหม่แล้ว
- หลักฐานว่าดีไซน์ใดเร็วกว่า Formula One จริง

## 7. การตีความ Evidence และ Readiness

| คำอ้าง | สถานะปัจจุบัน |
|---|---|
| Repository structure มี governance และ reproduce ได้ | รองรับในเครื่อง |
| Individual Level-0 law ที่ประกาศตรง test/reference | รองรับสำหรับ case ที่ implement |
| Profile สิบสนามและ distance gate execute deterministic | รองรับ |
| Constrained CAD ผ่าน independent STEP measurement | รองรับสำหรับ fixture `mounting_plate_v1` |
| Independent module รวมเป็น coherent vehicle simulation หนึ่งระบบ | ยังไม่รองรับ |
| Level 0 converge ทาง numerical สำหรับ integrated vehicle ในอนาคต | ยังไม่รองรับ |
| Candidate ordering รอด independent model ที่แรงกว่า | ยังไม่ทดสอบ |
| Free topology ชนะ optimized conventional baseline | ยังไม่ทดสอบ |
| ค้นพบเทคโนโลยีใหม่ | ไม่รองรับ |
| Design ผลิตได้หรือปลอดภัย | ไม่รองรับ |
| ทำนาย real race performance แม่นยำ | ไม่รองรับ |

ปัจจุบันมี confidence สูงต่อ deterministic contract, analytical reference,
invalid-state handling, event localization และ internal accounting ที่ implement
แล้ว แต่ confidence ต่ำหรือไม่มีต่อ integrated-vehicle accuracy, calibrated
uncertainty, real performance, manufacturability และ safety

## 8. ช่องว่างและความเสี่ยงวิจัยหลัก

### 8.1 Integration Gap

ความเสี่ยงทางเทคนิคใหญ่ที่สุดคือ module ที่ถูกแยกกันอาจทำงานผิดเมื่อเชื่อม ต้องมี
causal contract และ residual aggregation policy เดียวสำหรับ load, energy,
thermal state, timestep และ failure ordering

### 8.2 Design-Language Bias

ถ้า grammar อนาคตมีแต่ conventional component agent จะค้นพบ non-conventional
architecture ไม่ได้ ถ้าเปิดเกินไป candidate ส่วนมากจะ invalid หรือ exploit
physics ที่หาย Grammar ต้องเปิด topology แต่เข้มงวดกับ typed physical interface
และ evidence requirement

### 8.3 Baseline Fairness

ผลที่ดูใหม่ไม่มีความหมายหาก conventional baseline ได้ optimization น้อยกว่า,
evaluation น้อยกว่า, component opportunity อ่อนกว่า, energy/seed ต่างกัน หรือ
failure gate ง่ายกว่า

### 8.4 Fidelity และ Calibration Gap

Synthetic coefficient map และ reduced-order failure multiplier อาจจัดอันดับ
candidate ผิด ต้อง promote สู่ independent solver และข้อมูลจริงในอนาคตเพื่อตรวจ
ว่า ordering ยังอยู่หรือไม่

### 8.5 Objective Exploitation

Agent อาจ exploit race completion ที่ไม่ครบ, numerical tolerance, hidden energy,
material ที่หาย, dimension ที่ไม่จำกัด หรือ failure mode ที่ไม่มี Fail-closed และ
residual discipline ปัจจุบันต้องเป็นส่วนหนึ่งของ fitness ไม่ใช่ post-process

### 8.6 Documentation Drift

ส่วน “current phase/status” ใน README และ charter ยังอธิบายสถานะเก่า ควรอัปเดตใน
work item แยกที่ audit ได้ เพื่อไม่ให้ project entry point บอก module ที่เสร็จต่ำ
กว่าจริงหรือทำให้ narrow Phase-1 เดิมสับสนกับ Level-0 foundation ที่กว้างขึ้นแล้ว

## 9. ทิศทางแนะนำ: Integration Before Evolution

### Stage A — Reconcile Experiment Contract

สร้าง versioned experiment manifest เดียวที่ pin:

- candidate/design-language version และ immutable geometry hash
- material/component catalog และ typed interface
- circuit profile และ regulatory/energy profile
- initial energy และ recovery path ที่อนุญาต
- solver/model version, timestep/tolerance, event priority และ failure policy
- random seed, evaluation/compute budget, artifact path และ code commit
- claim level และ promotion gate ที่ต้องผ่าน

พร้อม reconcile สถานะ README/research charter กับ Work 019 baseline โดยไม่เปลี่ยน
ภารกิจ open-ended ระยะยาว

### Stage B — สร้าง Coupled Fixed-Topology Level-0 Reference Vehicle

กำหนด common state และ deterministic execution order เช่น:

```text
circuit/environment/strategy command
  -> aerodynamic forces and cooling
  -> chassis force/moment and normal-load solution
  -> per-contact tyre/suspension/brake limits
  -> longitudinal/lateral/yaw state update
  -> typed energy transfer and conservation audit
  -> thermal/degradation/damage/reliability events
  -> race progress, finish, failure, telemetry, and replay
```

Integrated vehicle แรกควร fixed topology ไม่ใช่เพราะโปรเจกต์ชอบ conventional
car แต่เพราะต้องแยก integration error ออกจาก topology-search error ทุก step ต้อง
รวม force, moment, energy, distance และ state residual พร้อมบอก module ที่ทำให้
invalid

### Stage C — ขยาย Geometry-to-Physics Coverage

ขยายจาก mounting plate หนึ่งตัวเป็น library เล็กของ **functional interface** ที่
ประกอบกันได้ ไม่ใช่ catalog รูปทรง conventional ที่บังคับ Candidate family ควร
เปิด mounting/load surface, port, material region, clearance volume และ failure
evidence เพิ่ม:

- assembly และ collision/packaging rule
- mass, centre of mass และ inertia ที่ derive จาก FreeCAD
- material และ manufacturing declaration
- load-case export และ independent structural/thermal check
- provenance จาก geometry artifact ถึง derived property ทุกตัว

### Stage D — สร้าง Fair Optimized Baseline

สร้าง fixed-topology EV, ICE, hybrid หรือ reference family อื่นที่ประกาศล่วงหน้า
เป็น comparison treatment เท่านั้น ให้ energy opportunity, component library,
circuit set, constraint gate, compute/evaluation budget, seed และ promotion
criteria เท่ากัน ปรับ baseline ให้แข่งขันได้ก่อนเทียบ free topology

### Stage E — เปิด Autonomous Search ทีละชั้น

ลำดับแนะนำ:

1. Parameter optimization บน fixed topology หนึ่งแบบ
2. Component selection และ sizing บน topology เดิม
3. Typed connection/topology mutation โดย fixed vehicle envelope
4. Component-geometry mutation ผ่าน constrained grammar
5. เปลี่ยน packaging และ ground-contact arrangement
6. Whole-vehicle topology/geometry co-design

ทุกชั้นต้องเทียบกับชั้นก่อนหน้าภายใต้ matched budget และหลาย seed Invalid
candidate ต้องคืน structured failure evidence ให้ agent ไม่ใช่หายจาก dataset

### Stage F — Promote และพยายามหักล้าง Discovery

Promote เฉพาะ candidate ที่จบเรซและ non-dominated ตรวจซ้ำด้วย independent
geometry/physics solver, timestep ละเอียดขึ้น, uncertainty sweep, holdout circuit,
ablation ของ feature ที่อ้างว่าใหม่ และ known alternative ที่ optimize แล้ว
Candidate เป็น discovery เมื่อ functional advantage ยังรอดจากความพยายามอธิบาย
ด้วยสาเหตุอื่น

## 10. งานถัดไปที่แนะนำทันที

Implementation ถัดไปควรเป็น:

> **Unified Level-0 Experiment Contract and Coupled-Vehicle Architecture**

งานนี้ควรสร้าง schema และ executable fixed-topology integration reference ก่อน
สร้าง free-topology evolution

Minimum completion gate:

1. Immutable manifest หนึ่งตัวระบุ candidate, geometry, component, circuit,
   energy profile, solver, tolerance, seed และ commit
2. Fixed-topology vehicle หนึ่งคันเดิน deterministic coupled pipeline เดียวกัน
   บน circuit profile ทั้งสิบ
3. Aerodynamic load, contact load, tyre force, brake/regen energy, thermal state,
   degradation, damage และ race progress กระทบ shared state เดียว ไม่ใช่ fixture
   อิสระ
4. Force, moment, energy, distance และ event residual สังเกตได้
5. Finish และ failure mode หลักทุกตัว replay exact
6. Coupling ที่จงใจไม่สอดคล้องถูก reject ด้วย test
7. Result ยังระบุชัดว่า Level 0 และไม่อ้าง real performance

นี่คือสะพานสั้นที่สุดที่น่าเชื่อถือระหว่าง foundation ปัจจุบันกับ autonomous
discovery research ที่ต้องการ

## 11. การตัดสินใจที่แนะนำตอนนี้

1. ถือ Work 001–019 เป็น **foundation phase ที่เสร็จ** ไม่ใช่ simulator หรือรถที่
   เสร็จแล้ว
2. ยังไม่เริ่ม whole-vehicle agent evolution ก่อน coupled fixed-topology
   reference ผ่าน residual/failure gate ทั้งหมด
3. รักษา open topology ด้วยการนิยาม function และ typed interface แทนการบังคับ
   human component shape
4. ทำ experiment manifest และ fair-baseline policy เป็นส่วนของ evaluator ไม่ใช่
   informal lab note
5. เก็บ primary energy ทั้งหมดบนรถก่อน start; recovered energy ต้องมี source/loss
   evidence
6. ใช้สิบสนามสร้าง environmental diversity แต่ไม่อ้าง surveyed geometry เมื่อ
   evidence ไม่มี
7. Revalidate CAD tool environment ก่อน geometry campaign ถัดไป
8. อัปเดต top-level status ที่เก่าใน validated work item แยก
9. เก็บ repository เป็น private และไม่ push local history Work 006–020 จนกว่าผู้ใช้
   อนุญาต publication/synchronization ชัดเจน

## 12. ข้อสรุปปัจจุบัน

Formula Ultimate มีฐานวิจัย Level-0 ที่จริงจังและ audit ได้แล้ว ระบบสามารถแสดง
constrained CAD, วัด bounded component แบบอิสระ, represent typed energy topology,
evaluate physical boundary อิสระหลายตัว, รัน circuit/race scenario deterministic,
แสดง failure และเก็บ evidence นี่เพียงพอสำหรับเริ่ม **integration research**

แต่ยังไม่เพียงพอให้ปล่อย agent แล้วตีความ output ว่าเป็นรถที่คิดค้นหรือเทคโนโลยี
ใหม่ Milestone วิทยาศาสตร์ถัดไปไม่ใช่ “สร้างรถที่แปลกขึ้น” แต่คือพิสูจน์ว่า
ordinary reference candidate หนึ่งตัวผ่าน coupled, conserved, replayable,
race-completing pipeline เดียวได้ เมื่อ reference นั้นเสถียรและมี fair baseline
แล้ว โปรเจกต์จึงค่อยเปิด topology/geometry ทีละขั้นและถามคำถาม discovery จริงด้วย
หลักฐานที่ป้องกันได้
