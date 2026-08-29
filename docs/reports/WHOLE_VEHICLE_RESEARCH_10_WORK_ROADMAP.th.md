# Roadmap สิบงานสู่การวิจัยรถทั้งคัน

ไฟล์ต้นฉบับภาษาอังกฤษ: `WHOLE_VEHICLE_RESEARCH_10_WORK_ROADMAP.md`

## จุดประสงค์และขอบเขตปัจจุบัน

Roadmap นี้กำหนด minimum ten validated work items ระหว่าง repository ปัจจุบันกับ bounded whole-vehicle design-search pilot ไม่ได้สัญญาว่าสิบงานจะเพียงพอเสมอ หาก hypothesis ถูก reject หรือ solver มีข้อจำกัด ต้องสร้าง remedial work item ใหม่แทนการผ่อน gate

หลักฐานปัจจุบันรองรับ deterministic coupled Level 0 reference, bounded component route `3D -> STEP -> FreeCAD -> Level 0`, solver acceptance สำหรับ tension, beam bending และ solid-shaft torsion, ideal eigenvalue buckling และ precritical nonlinear imperfection response Work 039 reject full-range near-critical mesh-convergence และ imperfection-shape-robustness hypothesis ส่วน loaded-interface transfer, nonlinear material failure, connection failure coupling และ arbitrary whole-vehicle geometry ยังไม่ validate

Execution dependency:

```text
041 numerical convergence
  -> 045 loaded interface
042 plasticity -> 043 fracture
              -> 044 fatigue
043 + 044 + 045 -> 046 failure coupling
046 -> 047 whole-vehicle grammar
047 + coupled Level 0 -> 048 vehicle load cases
048 -> 049 fixed-topology end-to-end baseline
049 -> 050 bounded search pilot and readiness review
```

ค่า SI และ numeric gate ด้านล่างเป็น preregistration proposal แต่ละ work ต้อง pin final config ก่อน admitted run แรกและห้ามผ่อน gate หลังเห็นผล

## Work 041 — ตรวจ Near-Critical Mesh และ Element

### วัตถุประสงค์และ dependency

แก้ numerical-convergence rejection จาก Work 039 ก่อนข้ออ้าง post-buckling หรือโครงสร้างรถใด ๆ ขึ้นกับ Work 037-039

### การทดลอง

- ตัวแปรอิสระ: C3D4 mesh size `1.0`, `0.8`, `0.65 mm`; C3D10 route ที่มี declared comparable degree-of-freedom budget; absolute compression `1857.580`, `2600.612`, `3157.886 N` (`0.50`, `0.70`, `0.85` ของ Work 037 fine-mesh `Pcr=3715.160 N`)
- ตัวแปรตาม: eigenvalue `Pcr`, nonlinear tip amplification, stress, strain energy, reaction closure, solver iteration, memory, wall time และ artifact hash
- ตัวแปรควบคุม: geometry/material/support จาก Work 039, `e0=0.1 mm`, cantilever eigenmode imperfection, fixed absolute load, solver version และ output parser
- falsification: เก็บ high-load case แม้ reject convergence และห้าม normalize แต่ละ mesh ด้วย `Pcr` ของตัวเองเมื่อคำนวณ primary mesh-change metric

### Implementation และ deliverable

เพิ่ม higher-order mesh/deck route, element-aware result contract, deterministic launcher, unit fixture, ignored solver evidence และ bilingual numerical-verification report

### Completion gate

- declared case ทุกตัวมี complete finite evidence และ reaction residual `<=1e-5`
- last-two C3D4 amplification change `<=5%` ทุก absolute load
- refined C3D4 กับ admitted C3D10 amplification difference `<=5%`
- eigenmode secant error `<=15%` และไม่มี mode-family change ที่อธิบายไม่ได้
- failure/non-convergence ต้องถูกบันทึกโดยไม่แทนที่ด้วย load ต่ำกว่า

### ข้ออ้างที่ห้าม

การผ่านยืนยัน precritical numerical adequacy เฉพาะ fixture นี้ ไม่ใช่ post-buckling capacity, safety factor หรือหลักฐานว่า C3D4 เหมาะกับชิ้นส่วนรถทุกแบบ

## Work 042 — Yield และ Plasticity Solver Acceptance

### วัตถุประสงค์และ dependency

ตรวจว่า stress ที่เกิน declared yield law ทำให้เกิด plastic strain, residual deformation และ plastic-work accounting แทน unlimited linear-elastic strength ขึ้นกับ Work 034 และทำคู่ขนาน Work 041 ได้ แต่ห้ามเข้า vehicle fitness ก่อน Work 041 ปิด

### การทดลอง

- ตัวแปรอิสระ: load/unload amplitude, hardening law, mesh และ monotonic/reversed loading
- ตัวแปรตาม: yield-onset load, tangent stiffness, plastic strain, residual displacement, elastic/plastic energy, reaction และ convergence
- ตัวแปรควบคุม: uniform tension coupon, SI geometry, temperature, strain rate, boundary surface และ synthetic material identity
- fixture: pinned synthetic bilinear law (`E=70 GPa`, proposed `sigma_y=250 MPa`, proposed tangent `Et=1 GPa`) สำหรับ solver verification และ material record ที่มีแหล่งอ้างอิงแยกก่อนใช้กับ design

### Implementation และ deliverable

Implement versioned elastic-plastic material record, CalculiX `*PLASTIC` deck generation, load/unload step, multi-step evidence parser, analytical bilinear reference, negative control และ bilingual report

### Completion gate

- yield-onset error `<=2%`, post-yield tangent error `<=5%`, residual-strain error `<=5%` เทียบ declared bilinear reference
- reaction residual `<=1e-5` และ energy-ledger residual `<=1e-4`
- below-yield control ต้องมี plastic strain เล็กจนละเลยได้; missing/unsourced design material เข้า fitness ไม่ได้
- mesh last-two change ของ nominal response `<=5%`

### ข้ออ้างที่ห้าม

Synthetic law ตรวจ implementation ไม่ใช่ real alloy allowable, temperature/rate effect, cyclic plasticity, fracture หรือ component safety

## Work 043 — หลักฐาน Fracture Initiation

### วัตถุประสงค์และ dependency

ตรวจ fracture initiation จาก declared flaw และ toughness record โดยไม่ถือ singular element peak เป็น physical proof ขึ้นกับ Work 042 และ tension/bending acceptance fixture

### การทดลอง

- ตัวแปรอิสระ: crack length, nominal tension, thickness regime, mesh ใกล้ flaw และ toughness
- ตัวแปรตาม: `K_I` หรือ fracture parameter ที่ preregister, initiation load, reaction/energy residual, mesh sensitivity และ failure classification
- analytical reference: `K_I = Y sigma sqrt(pi a)` ภายใน declared geometry-factor domain
- ตัวแปรควบคุม: flaw geometry, plane-stress/plane-strain assumption, material state, load surface, gauge definition และห้าม hidden crack healing

### Implementation และ deliverable

เพิ่ม fracture-material record พร้อม provenance, cracked-coupon grammar, fracture-parameter evaluator, initiation event contract, deliberate invalid-domain fixture และ bilingual report หาก solver ที่เลือกให้ admissible fracture evidence ไม่ได้ ต้องบันทึกข้อจำกัดและใช้ independently verified evaluator แทนการสั่ง element deletion โดยไม่มีฟิสิกส์

### Completion gate

- initiation-load error `<=5%` ใน analytical fixture domain
- last-two refinement change `<=5%` สำหรับ admitted fracture parameter ไม่ใช่ raw singular peak stress
- reject missing flaw/toughness/thickness-regime evidence แบบ exact
- reaction residual `<=1e-5`, energy residual `<=1e-4` และ deterministic event identity

### ข้ออ้างที่ห้าม

ตรวจเฉพาะ initiation เว้นแต่ stable/unstable crack propagation, path และ dissipated fracture energy จะ validate แยก และไม่พิสูจน์ crashworthiness

## Work 044 — Fatigue Damage และ Life Acceptance

### วัตถุประสงค์และ dependency

แปลง load history เป็น observable cumulative damage และ localized fatigue-failure event ขึ้นกับ Work 042 ส่วน fracture initiation จาก Work 043 เป็นกลไกแยก

### การทดลอง

- ตัวแปรอิสระ: constant/variable amplitude history, mean stress, cycle count, material curve และ sequence
- ตัวแปรตาม: counted cycle, alternating/mean stress, per-bin damage, cumulative `D`, predicted life, event cycle และ uncertainty
- ตัวแปรควบคุม: S-N หรือ strain-life record, correction rule, rainflow version, temperature, surface/notch factor และห้าม damage clipping
- analytical reference: constant-amplitude life และ Miner accumulation `D=sum(n_i/N_i)` ภายใน limitation ที่ประกาศ

### Implementation และ deliverable

Implement immutable fatigue record, deterministic rainflow counting, mean-stress correction, damage ledger, event localization, exact replay test, deliberate overload/underload control และ bilingual report

### Completion gate

- exact cycle-count fixture และ constant-amplitude damage error `<=1%`
- cumulative-damage arithmetic และ replay ต้อง exact สำหรับ input record เดิม
- emit failure ที่ admitted crossing แรก `D>=1` โดยไม่ reset หรือ clip damage เงียบ ๆ
- missing curve-domain หรือ extrapolated stress ต้อง reject/ระบุ unsupported และรายงาน uncertainty

### ข้ออ้างที่ห้าม

Miner/S-N acceptance ไม่ใช่ crack-growth validation, multiaxial fatigue proof หรือ real component service-life claim หากไม่มี sourced material/process/environment data

## Work 045 — Loaded Interface และ Joint Load Path

### วัตถุประสงค์และ dependency

พิสูจน์ว่า force/moment เข้าทาง finite interface หนึ่ง ไหลผ่าน material และปิดที่ declared interface อื่น ขึ้นกับ Work 041 และ tension/bending/torsion fixture

### การทดลอง

- ตัวแปรอิสระ: interface geometry, hole/fastener arrangement, load direction/eccentricity, mesh และ support compliance
- ตัวแปรตาม: interface resultant, compliance, strain energy, nominal ligament/bearing stress, load share, reaction closure และ field continuity
- ตัวแปรควบคุม: persistent CAD-to-mesh interface tag, material, load/support surface, non-singular gauge และ topology-neutral interface definition
- negative control: broken ligament, missing support, duplicated load tag, zero-area interface และ disconnected solid

### Implementation และ deliverable

สร้าง `loaded_interface_plate_v1`, constrained geometry grammar, FreeCAD interface verification, CalculiX surface mapping, resultant/energy parser, boundary-sensitivity matrix, negative control และ bilingual report

### Completion gate

- exact interface identity ต้องอยู่ครบผ่าน CAD, STEP, FreeCAD, mesh และ result
- force/moment residual `<=1e-5`, energy residual `<=1e-4`
- last-two mesh change `<=5%` สำหรับ compliance และ integrated interface resultant
- วัด boundary-condition sensitivity และ response change ที่ preregister `>10%` ต้อง reject transferability
- disconnected/malformed control ทุกตัว fail closed

### ข้ออ้างที่ห้าม

การผ่าน interface plate หนึ่งตัวไม่ validate arbitrary bolt, weld, adhesive, contact friction, preload, manufacturing tolerance หรือ vehicle chassis

## Work 046 — Structural Failure Coupling และ DNF

### วัตถุประสงค์และ dependency

Couple yield/fracture/fatigue/interface evidence เข้าสู่ typed connection state เพื่อให้ failed load path หยุดหรือ redistribute force และทำให้ subsystem failure หรือ `DNF` ได้ ขึ้นกับ Work 042-045 และ coupled transaction/failure system ถึง Work 030

### การทดลอง

- ตัวแปรอิสระ: failure mechanism, event time/load, redundant/critical connection topology, timestep และ arbitration tie
- ตัวแปรตาม: state `intact -> degraded -> failed`, transmitted wrench, redistribution, stored/dissipated energy, event time, subsystem state และ race outcome
- ตัวแปรควบคุม: identical pre-failure state, deterministic seed, connection graph, failure threshold และ energy policy
- falsification: critical connection failure ต้องไม่ปล่อย original force path ทำงานต่อ, ลบ elastic energy หรือให้รถ finish ผ่าน disconnected required path

### Implementation และ deliverable

เพิ่ม typed structural-health state, event localization, connection-wrench adapter, redistribution/no-path logic, energy ledger, `DNF` arbitration, replay metadata, negative test และ bilingual report

### Completion gate

- failed connection ห้ามส่ง forbidden wrench หลัง localized event
- redistributed force/moment residual `<=1e-5` และ energy residual `<=1e-4`
- event time converge ภายใน relative `1e-6` เมื่อ refine timestep
- critical failure ให้ deterministic `DNF`; redundant topology ต้อง re-equilibrate ใน gate หรือ fail แบบ observable
- input เดิม replay exact และ invalid evidence เขียน state เป็นศูนย์รายการ

### ข้ออ้างที่ห้าม

นี่เป็น verified coupling policy ไม่ใช่หลักฐาน real fracture dynamics, crash energy absorption, occupant safety หรือ repairability

## Work 047 — Topology-Neutral Whole-Vehicle CAD และ Assembly Grammar

### วัตถุประสงค์และ dependency

Represent complete 3D vehicle candidate โดยไม่บังคับ conventional car shape หรือ fixed component count และบังคับให้ mass, contact, connection, energy path ทุกอย่าง explicit ขึ้นกับ Work 046 contract และ CAD evidence route ที่มีอยู่

### การทดลอง

- ตัวแปรอิสระ: component count/type, geometry parameter, connection graph, contact arrangement, placement และ material assignment
- ตัวแปรตาม: valid-solid status, interface match, collision/keep-out violation, envelope, ground clearance, mass, center of mass, inertia, connectivity และ artifact identity
- ตัวแปรควบคุม: component library/version, global coordinate frame, SI unit, allowed operation, numerical resolution และห้าม hidden geometry repair
- negative control: floating component, overlapping protected volume, unmatched interface, disconnected required path, invalid solid และ massless energy component

### Implementation และ deliverable

สร้าง versioned vehicle/assembly schema, topology-neutral grammar, deterministic candidate manifest, multi-component STEP export, FreeCAD assembly measurement, connection/contact tag, mass/inertia aggregation, invalid-case corpus และ bilingual report

### Completion gate

- admitted candidate ทุกตัวมี complete typed path จาก energy source ถึง propulsion และจาก external load ถึง support/contact interface
- component ทุกตัวเป็น valid solid พร้อม persistent identity และ exact STEP hash
- FreeCAD กับ independent component-sum mass/center/inertia residual `<=1e-6` relative ในค่าที่เทียบกันทางคณิตศาสตร์ได้
- interface/envelope/keep-out/contact rule ต้อง fail closed โดยไม่ auto-repair
- candidate replay สร้าง declaration/evidence hash เดิมภายใต้ pinned tool

### ข้ออ้างที่ห้าม

Geometric admission ไม่พิสูจน์ structural feasibility, aerodynamics, cooling, manufacturability, safety, race completion, novelty หรือ superiority

## Work 048 — Whole-Vehicle Load Case และ Structural Coupling

### วัตถุประสงค์และ dependency

แปลง coupled Level 0 race state เป็น balanced traceable structural load case บน complete assembly ขึ้นกับ Work 047, Work 046 และ coupled vehicle ถึง Work 030

### การทดลอง

- ตัวแปรอิสระ: circuit profile/evidence class, speed, acceleration, braking, cornering, aero state, grade, contact state, energy mass state และ selected time
- ตัวแปรตาม: component/interface force/moment, inertial load, load combination, equilibrium residual, structural response, failure margin/event และ provenance
- ตัวแปรควบคุม: immutable race snapshot หนึ่งตัวต่อ case, coordinate transform, gravity, mass/inertia evidence, contact/aero adapter version และ training/holdout partition
- case: straight acceleration, braking, steady cornering, combined manoeuvre, bump/load-transfer extreme, aero-load extreme และ thermal/mass-state extreme ที่รองรับ

### Implementation และ deliverable

เพิ่ม critical-state extraction, immutable load-case manifest, body/component coordinate transform, inertia relief หรือ declared support, surface-load mapping, multi-case FEA orchestration, holdout partition, equilibrium audit และ bilingual report

### Completion gate

- applied structural wrench ทุกตัว trace ถึง immutable Level 0 snapshot และ exact geometry/material identity หนึ่งรายการ
- global/per-interface force/moment residual `<=1e-5`
- mapped mass/inertia ตรง FreeCAD evidence ภายใน `1e-6` relative
- freeze training/holdout case ก่อน candidate search
- unsupported dynamics/contact/aero evidence ต้อง reject promotion แทน neutral numeric default

### ข้ออ้างที่ห้าม

Quasi-static equivalent case แรกที่รับได้ไม่ใช่ transient crash, vibration, random road, CFD, tyre-test หรือ physical-track validation

## Work 049 — Fixed-Topology End-to-End Whole-Vehicle Baseline

### วัตถุประสงค์และ dependency

รัน reviewed fixed-topology vehicle หนึ่งคันผ่าน complete evidence chain ก่อนอนุญาต design search ขึ้นกับ Work 048 และ structural/failure gate ทั้งหมด

### การทดลอง

- ตัวแปรอิสระ: pinned baseline design, declared training/holdout load case, mesh level, timestep และ circuit/environment evidence class
- ตัวแปรตาม: CAD validity, mass/inertia, structural margin/event, energy/thermal state, race completion หรือ `DNF`, convergence, compute cost และ replay hash
- ตัวแปรควบคุม: ห้าม geometry mutation, fixed solver/settings, fixed seed, fixed component library และ explicit unsupported-evidence state
- falsification: deliberately weakened/disconnected variant ต้อง structural fail หรือ `DNF`; heavy but feasible control ตรวจว่า mass optimization ไม่ใช่ทางเดียวที่ผ่าน

### Implementation และ deliverable

สร้าง fixed baseline manifest, end-to-end orchestrator สำหรับ `3D -> STEP -> FreeCAD -> load cases -> structural/failure -> coupled Level 0`, refinement matrix, exploit fixture, complete telemetry bundle และ bilingual baseline report

### Completion gate

- reviewed baseline ให้ complete deterministic result ทุก declared training/holdout case ไม่ว่าจะ finish หรือ explicit failure
- ต้องมี baseline อย่างน้อยหนึ่งตัว structurally feasible สำหรับ declared training set ก่อนเปิด search
- deliberate weak/disconnected control ต้อง reject หรือเกิด expected `DNF`
- timestep/mesh change ผ่าน pinned convergence gate และ repeated run คง exact identity/provenance
- ห้ามเปลี่ยนชื่อ Level 0 outcome เป็น physical validation

### ข้ออ้างที่ห้าม

Fixed baseline ไม่ใช่ autonomous research, optimized car, real-circuit admission, safety certification หรือ discovery

## Work 050 — Bounded Whole-Vehicle Search Pilot และ Readiness Review

### วัตถุประสงค์และ dependency

ตรวจว่า whole-vehicle candidate สามารถถูก propose, evaluate, fail, compare และ replay อย่างยุติธรรมก่อนอนุญาต main research campaign ขึ้นกับ Work 049

### การทดลอง

- treatment: `GRID`, `RANDOM`, `EVOLUTION` ผ่าน evaluator API เดียว
- ตัวแปรอิสระ: treatment และ preregistered seed; candidate variable จำกัดใน Work 047 grammar
- ตัวแปรตาม: feasible rate, failure-code distribution, objective ใน candidate ที่ผ่าน gate, holdout survival, refined-evaluator survival, wall time, memory และ budget use
- ตัวแปรควบคุม: equal attempted-evaluation budget, component library, load, seed, compute cap, evaluator, tolerance, baseline และ immutable result ledger
- pilot budget proposal: attempted evaluation `32` ครั้งต่อ treatment ต่อ seed รวม `3` seeds โดย grammar/CAD/solver failure ถูกนับใน budget Final value ต้อง freeze ก่อน admitted pilot แรก

### Implementation และ deliverable

Implement `DesignSearchAgentV0`, candidate ancestry/RNG checkpoint, append-only result/budget ledger, equal-budget treatment adapter, holdout/refinement promotion, exploit test, pilot summary table/plot, falsification review และ bilingual readiness report

### Completion gate

- same-seed replay exact และ budget accounting exact รวม failed candidate ทุกตัว
- ทุก treatment ใช้ evaluator/opportunity set เดียวกัน; agent แก้ code, config, load, tolerance หรือ evidence ไม่ได้
- selected candidate ต้องผ่าน preregistered holdout และ independent refined evaluation มิฉะนั้นรายงานเป็น failure
- numerical exploit, hidden repair, missing evidence หรือ unequal compute opportunity ห้ามสร้าง winner
- readiness review ต้องคืน `ready_for_bounded_main_campaign` หรือ `not_ready` พร้อม blocker อย่างชัดเจน

### ข้ออ้างที่ห้าม

Pilot success อนุญาตเฉพาะ bounded main campaign ไม่พิสูจน์ superiority, novelty, manufacturability, safety, physical validity หรือ discovery การ promote เกิน Level 0 ยังต้องมี independent Level 1 evidence, real circuit admission, structural safety, cross-model aerodynamics, thermal reliability และ quantified uncertainty ตาม promotion gate ที่มีอยู่

## Program-level stop/go gate

### Gate A — Structural subsystem พร้อม

Work 041-046 ต้อง complete โดยไม่มี unresolved numerical, material, interface หรือ failure-coupling blocker ก่อนให้ structural fitness มีผลต่อ whole-vehicle candidate

### Gate B — Whole-vehicle evaluator พร้อม

Work 047-049 ต้อง complete พร้อม end-to-end fixed baseline หนึ่งคัน, deliberate failure control, frozen training/holdout load และ reproducible evidence ก่อนเริ่ม Work 050 search

### Gate C — Main research campaign พร้อม

Work 050 ต้องคืน `ready_for_bounded_main_campaign` นี่หมายถึง experimental apparatus พร้อม ไม่ใช่ physical validation หาก work ใด reject preferred hypothesis ให้หยุด dependency chain และสร้าง separately numbered remedial work item

## นิยามจุดปลายทาง

หลัง Work 050 Formula Ultimate อาจเริ่ม bounded evidence-constrained whole-vehicle research campaign ที่มี explicit 3D candidate, coupled physics, structural failure, fair baseline, holdout และ deterministic replay ข้ออ้างยังจำกัดเฉพาะ grammar, load, material, solver, evidence class และ fidelity level ที่ทดสอบจริง
