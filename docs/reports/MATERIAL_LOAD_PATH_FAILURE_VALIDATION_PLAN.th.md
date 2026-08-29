# แผนตรวจสอบ Material Load Path และ Failure

ไฟล์ต้นฉบับภาษาอังกฤษ: `MATERIAL_LOAD_PATH_FAILURE_VALIDATION_PLAN.md`

วันที่รายงาน: 2026-08-29

สถานะ: วางแผนแล้ว ยังไม่ได้ implement หรือรันการทดลอง

## ข้อสรุปหลัก

Formula Ultimate ต้องตรวจการส่งแรงและ torque ผ่าน geometry/material ก่อนเริ่ม
ใช้ structural fitness หรือค้นหา geometry ของรถทั้งคัน ระยะวิจัยถัดไปใช้
หลักฐานหกกลุ่ม:

1. axial tension
2. beam bending
3. shaft torsion
4. column buckling
5. loaded-interface plate load transfer
6. deterministic structural-failure coupling สู่ subsystem failure หรือ `DNF`

Design agent ทำ material บางหรือรูปทรงแปลกได้ตามต้องการ Evaluator ห้ามใช้
minimum thickness ที่มนุษย์ชอบแทน physics Candidate บางอาจ yield, deform,
buckle, fracture, สะสม fatigue, ทำหน้าที่ล้มเหลว หรือ numerically unresolved
ผลเหล่านี้ต้องแยกและสังเกตได้

รายงานนี้แทนที่ถ้อยคำวางแผนใน Work 032 ที่ถือ minimum feature/thickness เป็น
general feasibility constraint ขีดจำกัดดังกล่าวมีได้เฉพาะ CAD/solver resolution
boundary ที่ประกาศ หรือ optional manufacturing treatment ที่ติดป้ายแยก ไม่ใช่
hidden physical law

## 1. ขอบเขตข้ออ้าง

การผ่าน suite ที่วางแผนจะรองรับเพียงว่า structural route ที่ implement ทำ
analytical/numerical reference case ที่เลือกซ้ำได้ภายในช่วงที่ประกาศ ไม่พิสูจน์:

- arbitrary vehicle geometry ปลอดภัยทางโครงสร้าง
- material data แทน batch วัสดุจริงที่ซื้อ
- fracture, fatigue, joint, composite, impact หรือ post-buckling behavior
  ถูกต้องทั่วไป
- solver หนึ่งเป็น independent validation ของตัวเอง
- component ผลิตได้ รับรองแล้ว หรือ race-ready

Evidence ladder คือ:

```text
equation/unit contract
  -> analytical reference
  -> mesh and boundary-condition verification
  -> solver-to-reference agreement
  -> loaded 3D interface evidence
  -> coupled failure event and replay
  -> independent solver/model promotion
  -> physical coupon/component testing
```

ห้ามเปลี่ยนชื่อหลักฐานระดับล่างเป็นระดับสูง

## 2. Tool Inventory Local ที่ตรวจแล้ว

Read-only probe วันที่ 2026-08-29 พบ:

| เครื่องมือ | หลักฐานที่สังเกต | ขอบเขต |
|---|---|---|
| FreeCAD | `1.1.3`; bundled Python import `FreeCAD`, `Part`, `Fem` ได้ | พิสูจน์ import เท่านั้น ยังไม่ได้รัน FEM solve |
| CalculiX | `ccx.exe` รายงาน `2.22` | `-v` คืน exit code `201`; ยังไม่รับ runtime/artifact behavior |
| Gmsh | version probe รายงาน `4.15.0` | invocation ที่สังเกตคืน exit code `201`; ยังไม่รับการ meshing |
| CadQuery/STEP | geometry/STEP route deterministic พิสูจน์แล้ว | structural boundary condition และ mesh tag ยังไม่มี |

Launcher ในอนาคตต้องตรวจทั้งหมดนี้:

- exact executable และ version identity
- input-deck/mesh hash
- expected output file ใหม่กว่าเวลาเริ่ม run
- parsed solver completion/status marker
- requested step/increment coverage
- reaction/displacement/stress/energy field finite
- ตรวจ non-convergence/fatal message ชัดเจน
- process exit behavior ของ command mode จริง

Exit code `0` อย่างเดียวพิสูจน์ evidence ไม่ได้ และ exit code `201` จาก version
command ที่พบอย่างเดียวถือเป็น physics failure ไม่ได้

## 3. ขอบเขต Physics และ Material

### 3.1 Material law เริ่มต้น

เริ่มด้วย small-strain, homogeneous, isotropic, linear elasticity:

```text
sigma = C(E, nu) : epsilon
```

Material record ทุกตัวต้องประกาศ:

- density `rho` หน่วย `kg/m^3`
- Young's modulus `E` หน่วย `Pa`
- Poisson ratio `nu`
- shear modulus `G` ที่ประกาศหรือ derive อย่างสอดคล้อง
- yield policy พร้อม source/uncertainty
- valid temperature และ strain-rate range
- provenance, revision และ claim level

Linear suite แรกใช้ yield เป็น screening threshold ที่สังเกตได้เท่านั้น ไม่แกล้ง
คำนวณ plastic redistribution ต้องมี phase material law แยกที่ validate
elastoplastic ก่อนให้เครดิต plastic reserve

### 3.2 ลำดับ Failure Law

- **Yield:** รายงานครั้งแรกที่ข้าม yield criterion การรัน linear เกิน yield อยู่
  นอก constitutive validity
- **Plastic collapse:** ต้องมี elastoplastic law ที่ implement และตรวจแยก ห้าม
  สรุปจากการรัน linear ต่อ
- **Fracture:** เกิน ultimate value เป็น screening failure ไม่ใช่ crack-path
  prediction การเริ่ม/โตของ crack ต้องใช้ calibrated damage/fracture model
- **Fatigue:** screening แรกอาจใช้ versioned S-N curve และ cumulative damage
  rule พร้อม uncertainty แต่ห้ามเรียก general fatigue validation ต้องเก็บ load
  history/cycle counting เป็น evidence
- **Buckling:** eigenvalue buckling ระบุ ideal elastic instability mode/load
  factor Physical capacity ต้องมี imperfection sensitivity และ nonlinear
  post-buckling analysis

### 3.3 นโยบาย Geometry บาง

ไม่มี arbitrary physical minimum thickness Candidate บางได้ตราบใดที่ยังเป็น
finite valid 3D solid Evaluator คืนสถานะแยก:

- `physically_admissible` — ผ่าน law/functional gate ที่ประกาศทั้งหมด
- `yielded`, `buckled`, `fractured`, `fatigue_failed` หรือ physical failure อื่น
- `numerically_unresolved` — mesh/solver resolve geometry ไม่ได้ภายใน common
  resource budget
- `invalid_geometry` — ไม่มี finite valid solid/interface
- `unsupported_physics` — material/joint/load behavior ที่ต้องใช้ยังไม่มี model

ห้ามแปลง `numerically_unresolved` เป็นรอดหรือพังแบบเงียบ ผลนี้ใช้ evaluation
budget และ block promotion

## 4. Common Experiment Contract

ทุก specimen run ต้อง pin:

- `protocol_id`, `experiment_id`, `specimen_id` และ geometry hash
- material-law ID และ property provenance ครบ
- load-case/boundary-condition ID
- coordinate frame, units, load surface, support surface และ reference point
- mesher/solver/adapter พร้อม exact version/source hash
- element family/order, mesh size, quality metric และ degrees of freedom
- nonlinear/eigenvalue/static step control ตามกรณี
- tolerance และ common resource budget
- analytical reference implementation/hash
- random seed เมื่อใช้ imperfection/sampling
- result/failure status และ claim level

### Common output ที่บังคับ

- nodal displacement และ reaction evidence
- strain/stress field และ named gauge value
- total reaction force/moment รอบ declared origin
- strain energy/external work เมื่อมี
- mass/volume และ dimensional identity
- mesh count/quality, solver iterations, residual/status และ wall time
- analytical/mesh-sequence residual
- singular/excluded region และ averaging/extrapolation policy
- exact artifact และ hash

### Common equilibrium gate

สำหรับ applied force `F_app`, applied moment `M_app`, reaction `R_i` ที่ตำแหน่ง
`r_i` และ declared origin `O`:

```text
force residual  = F_app + sum(R_i)
moment residual = M_app + sum((r_i - O) cross R_i) + sum(M_reaction_i)
```

Residual ต้องสังเกตได้แม้อยู่ใน tolerance ห้ามรับ solver result หาก reaction
หรือ load identity ที่บังคับหาย

### Common energy gate

สำหรับ linear static ramp จาก load ศูนย์:

```text
external work ~= strain energy ~= 0.5 * generalized_load * generalized_displacement
```

Energy agreement เป็น consistency check ไม่ใช่ independent material theory

## 5. Numerical Verification Policy

Canonical specimen ทุกตัวใช้ mesh level ที่ประกาศล่วงหน้าอย่างน้อยสามระดับ
Implementation สุดท้ายต้อง freeze mesh size จริงหลัง pilot และก่อนอ่านผล
comparison

Numerical gate เริ่มต้นที่แนะนำ:

- relative force/moment closure `<= 1e-6` เมื่อ solver precision รองรับ
- analytical displacement/twist/strain-energy error `<= 1%` ใน linear range
- analytical non-singular stress-gauge error `<= 2%`
- relative change ระหว่าง admitted mesh สองระดับสุดท้าย `<= 1%` สำหรับ global
  displacement/strain energy และ `<= 2%` สำหรับ named non-singular stress gauge
- ทุกค่า finite, output step ครบ และ solver converge

เปอร์เซ็นต์เหล่านี้เป็น numerical evidence threshold ที่เสนอ ไม่ใช่ physical
thickness rule Pilot เปลี่ยนได้เฉพาะก่อน main campaign และในแผนใหม่

Peak stress ที่ ideal fixed edge/point load ไม่ใช่ convergence metric ต้องใส่
load บน finite surface และประกาศ stress gauge ห่าง singular boundary ทดสอบทั้ง
structured canonical mesh และ Gmsh unstructured route เพื่อไม่ให้ element/mesher
artifact ปลอมเป็น material behavior

## 6. Experiment A — Axial Tension Specimen

### Preferred hypothesis

ใน small-strain elastic range Solver ทำ axial displacement, strain, stress,
reaction และ strain energy ของ prismatic bar ตรง reference

### Geometry และ boundary condition

- prismatic bar มี `L` และ cross-section `A` ที่ประกาศ
- constrain ปลายหนึ่งเท่าที่จำเป็นเพื่อตัด rigid-body motion
- uniform traction ที่ปลายตรงข้าม มี resultant `F`
- finite load surface ไม่มี point force
- named mid-span gauge region ห่าง end effect

### Analytical reference

```text
sigma = F / A
epsilon = sigma / E
delta = F * L / (A * E)
U = F * delta / 2
```

### ตัวแปรอิสระ

- load magnitude ภายในและเข้าใกล้ elastic-validity range
- mesh level
- aspect ratio ในช่วงที่ประกาศ
- optional material-property fixture

### ตัวแปรตาม

- end displacement, gauge strain/stress, reaction force, strain energy
- analytical residual, mesh sensitivity และ solver status
- first yield-screen crossing

### Falsification case

- กลับทิศ load และบังคับ signed symmetry
- เพิ่ม `F` สองเท่าและต้องได้ elastic displacement/stress สองเท่า
- เพิ่ม `E` สองเท่าและต้องได้ displacement ครึ่งหนึ่งโดย axial stress เท่าเดิม
- จงใจขาด restraint และต้องเกิด rigid-body/singularity failure
- เกิน linear-law validity และต้องได้ `outside_constitutive_validity` ไม่ใช่
  elastic pass ปลอม

## 7. Experiment B — Beam Bending Specimen

### Preferred hypothesis

Cantilever เรียวยาวที่รับ finite end traction ทำ displacement/bending stress ตรง
Euler-Bernoulli reference ในช่วง slender/small-deflection ที่ประกาศ

### Analytical reference สำหรับหน้าตัดสี่เหลี่ยม

เมื่อ width `b`, bending depth `h`, length `L`, end resultant `P` และ
`I = b*h^3/12`:

```text
tip deflection = P * L^3 / (3 * E * I)
root moment = P * L
nominal outer-fibre stress = P * L * (h/2) / I
U = P * tip_deflection / 2
```

### Control และการวัด

- finite traction patch ที่ free end
- displacement/stress gauge ห่าง ideal clamp singularity
- beam slenderness ที่ประกาศซึ่ง reference ใช้ได้
- load resultant/moment สอดคล้อง

### Falsification case

- กลับ `P` และบังคับ displacement/stress กลับ sign
- เพิ่ม `P` สองเท่าใน linear range และบังคับ linear response
- เปลี่ยน `h` และทดสอบ scaling ของ `I`
- เทียบ beam สั้น/ลึกเกินช่วงและต้องระบุ Euler-Bernoulli out of range ไม่บังคับ
  ให้ผ่าน
- perturb clamp representation และรายงาน boundary sensitivity

## 8. Experiment C — Solid Circular Shaft Torsion

### Preferred hypothesis

Applied torque ไหลผ่าน shaft แล้วสร้าง reaction torque, shear-stress
distribution, twist angle และ strain energy ถูกต้องใน linear elastic range

### Analytical reference

เมื่อ radius `R`, length `L`, torque `T`, shear modulus `G` และ
`J = pi*R^4/2`:

```text
tau(r) = T * r / J
tau_max = T * R / J
theta = T * L / (J * G)
U = T * theta / 2
```

### Boundary condition

- constrain ปลายหนึ่งต่อ rigid rotation โดยไม่ over-constrain local เกินจำเป็น
- distributed tangential traction หรือ kinematic coupling ที่หน้าตรงข้าม พร้อม
  exact resultant `T`
- named radial shear-stress gauge ห่าง end effect

### Falsification case

- กลับ `T` และบังคับ shear/twist กลับ sign
- เพิ่ม `T` สองเท่าและบังคับ linear response
- เปลี่ยน `R` และทดสอบ `R^4` twist sensitivity
- เปลี่ยน `G` และบังคับ inverse twist scaling
- ใส่ force pair ที่ให้ moment เท่ากันแล้วเทียบนอก load-introduction region
- ตัด rotational restraint และต้อง solver invalid

การผ่าน specimen นี้พิสูจน์เพียง continuum shaft torsion สำหรับ law ที่ประกาศ
ยังไม่พิสูจน์ gear tooth, spline, bearing, joint, wheel inertia หรือ drivetrain
ทั้งระบบ

## 9. Experiment D — Column Buckling

### Preferred hypothesis

Ideal slender-column eigenvalue analysis ทำ Euler critical load/mode family ตรง
ภายใน slenderness/support model ที่ประกาศ

### Analytical reference

```text
P_cr = pi^2 * E * I / (K * L)^2
```

Canonical case แรกใช้ pinned-pinned representation ที่ประกาศและ `K = 1`
Support อื่นเป็น fixture แยก ไม่ใช่ hidden change

### Evidence ที่บังคับ

- pre-stress/load identity
- eigenvalue/load factor และ normalized mode shape
- reaction closure ใน pre-buckling state
- mesh convergence ของ relevant lowest eigenvalue
- support/imperfection sensitivity

### Falsification และ limitation case

- เปลี่ยน `L`, `E`, `I` และทดสอบ analytical scaling
- เทียบ support model และบังคับ declared `K` case ที่ถูกต้อง
- ใส่ imperfection เล็กที่ประกาศและรัน nonlinear study ภายหลัง
- ห้ามใช้ ideal eigenvalue อย่างเดียวเป็น allowable physical load
- แยก local element/constraint mode จาก global column mode ที่ต้องการ

## 10. Experiment E — Loaded Interface Plate

### วัตถุประสงค์

ตรวจว่า load ที่ใส่บน component interface ที่ประกาศไหลผ่าน arbitrary admitted
3D solid และปิด force, moment, deformation, stress, energy evidence นี่เป็นสะพาน
จาก canonical specimen ไป agent geometry

### นิยาม Interface

- exact tagged support/load-bearing surface คงอยู่จาก source geometry ผ่าน STEP
  และ mesh
- finite bearing/contact traction distribution แทน point load
- declared load origin และ coordinate frame
- central keep-out/outer envelope เฉพาะเมื่อ component task ต้องใช้
- ไม่มี arbitrary minimum thickness หรือ conventional web shape

### Preferred hypothesis

สำหรับ reference plate applied force/moment resultant ทั้งหมดถูกกู้ที่ declared
support, global displacement/strain energy converge และ field ของ stress,
deformation, failure ตอบสนองต่อ load/material change อย่างสอดคล้อง

### ตัวแปรอิสระ

- load direction/magnitude
- geometry candidate
- material-law record
- mesh level/local-refinement policy
- boundary-condition fixture variant

### ตัวแปรตาม

- reaction force/moment closure
- load-path stress/strain field และ named gauge
- displacement, strain energy, mass และ stiffness-to-mass evidence
- yield/buckling/failure indicator
- mesh/boundary sensitivity และ solver status

### Falsification case

- ตัด load path และต้องได้ invalid/disconnected หรือ failed evidence
- ทำ ligament บางลงเรื่อย ๆ และให้ physics/numerics ไม่ใช่ fixed thickness rule
  ตัดสิน outcome
- กลับ/สลับ load พร้อมตรวจ signed reaction
- เลื่อน load introduction บน finite region ที่เทียบเท่าและวัด sensitivity
- เทียบ reaction/energy closure ก่อนเชื่อ local stress
- promote case ที่เลือกไป independent solver/model route

ไม่มี analytical stress formula เดียวสำหรับ arbitrary plate geometry Admission
จึงต้องให้ canonical-solver verification ผ่านก่อน พร้อม mesh, equilibrium,
energy, boundary และ independent-promotion evidence

## 11. Experiment F — Failure Coupling เข้ารถ

### Connection state ของ Component

ทุก load-carrying connection มี state ชัดเจน:

```text
intact -> degraded -> failed
```

Transition ต้องระบุ:

- component/connection ID
- governing failure law และ evidence record
- load history และ event time
- capacity ก่อน/หลัง event
- force/moment path ที่ถูกตัดหรือเปลี่ยน
- stored elastic energy และ release/dissipation policy
- downstream signal และ terminal outcome
- replay fingerprint

### Policy Implementation แรก

Coupling แรกที่ปลอดภัยที่สุดคือหยุด race ณ critical structural failure แรกที่
localize แล้วรายงาน `DNF` ไม่จำลอง post-break debris หรือ redistribute load โดย
ไม่มี transient failure model ที่ validate วิธีนี้ป้องกัน force/stored energy
หายผ่านการลบ connection ที่ไม่มี model

ระบบ redundant ในอนาคตจะวิ่งต่อได้หลัง implement ชัดเจน:

- connection removal และ load redistribution
- partition released elastic energy ไป kinetic, fracture, heat และ sink อื่น
- transient dynamics และ contact/collision state ใหม่
- cascading structural/subsystem failure

### Coupling test

1. Fixture ต่ำกว่า threshold ยัง intact และ replay exact
2. Known threshold crossing localize failure time ภายใน tolerance
3. Critical connection failure ทำ `DNF` และไม่มี race progress หลังจากนั้น
4. Non-critical/degraded fixture เปลี่ยน capacity ตามที่ประกาศเท่านั้น
5. Structural evidence หายต้อง block step ไม่ใช่สรุปว่ารอด
6. Structural/energy/thermal/finish event ที่เสมอกันใช้ deterministic arbitration
   priority ที่ประกาศ
7. stale hash, connection ID ผิด และ hidden energy release ถูก reject พร้อม zero
   committed state

## 12. Experiment Matrix และลำดับ

| Phase | Specimen | Model level | Promotion gate |
|---:|---|---|---|
| 0 | unit/equation fixture | pure Python analytical reference | equation, unit, sign, invalid input ผ่าน |
| 1 | tension, bending, torsion | linear elastic CalculiX route | analytical, equilibrium, energy, mesh gate ผ่าน |
| 2 | buckling | eigenvalue แล้ว nonlinear imperfection study | mode/eigenvalue/refinement และ scope limit ผ่าน |
| 3 | loaded interface plate | arbitrary admitted solid, linear range ก่อน | tag, load path, equilibrium, energy, mesh/boundary gate ผ่าน |
| 4 | material nonlinearity/failure | plastic/damage/fatigue model ที่ตรวจแยก | dedicated reference/provenance ผ่าน |
| 5 | failure coupling | coupled Level-0 event | rollback, localization, DNF, conservation, replay ผ่าน |
| 6 | independent promotion | second solver/model และ physical coupon ภายหลัง | ordering/failure classification ยังรอด |

ห้าม implement Phase 5 จาก output Phase 1–4 ที่ยังไม่ verify

## 13. Implementation Roadmap

ทุก milestone ต้องเป็น bilingual validated committed work item แยก

### Milestone 1 — Solver acceptance harness

- pin/probe invocation behavior ของ FreeCAD, Gmsh, CalculiX
- สร้าง bounded artifact directory และ fail-closed parser
- reject stale/missing/incomplete output แม้ process ดูสำเร็จ
- เก็บ tool/config/source/input/output hash และ resource use

### Milestone 2 — Material และ load-case contract

- implement typed SI material, geometry-interface, boundary-condition, mesh,
  solver และ structural-result schema
- เก็บ property provenance, validity range, uncertainty และ unsupported behavior
- เพิ่ม malformed/non-finite/unknown-field test

### Milestone 3 — Linear canonical specimen

- implement analytical reference และ CAD/mesh/solver adapter สำหรับ tension,
  bending, torsion
- รัน mesh sequence และ boundary-condition audit
- เก็บ failed attempt/solver evidence ทั้งหมด

### Milestone 4 — Buckling verification

- เพิ่ม Euler fixture, mode classification, mesh refinement, support sensitivity
- แยก nonlinear imperfect-column work ก่อนใช้ buckling capacity ใน fitness

### Milestone 5 — Loaded-interface plate

- เพิ่ม persistent interface tag จาก geometry ถึง mesh
- รัน reference และ deliberate broken/thin load path
- audit reaction, moment, strain energy, stress gauge, mesh/boundary sensitivity
  และ independent promotion

### Milestone 6 — Nonlinear material และ fatigue staging

- validate elastoplastic response ก่อนให้เครดิต post-yield capacity
- แยก fracture screening กับ fracture prediction ชัดเจน
- เพิ่ม versioned fatigue history/S-N evidence และ uncertainty ก่อน fatigue มีผล
  ต่อ fitness

### Milestone 7 — Failure coupling

- แปลง admitted structural failure evidence เป็น typed connection event
- เริ่มด้วย terminate ณ critical first failure
- ทดสอบ event arbitration, rollback, energy policy, `DNF`, replay

### Milestone 8 — Search release gate

- ให้ `DesignSearchAgentV0` ใช้ structural fitness หลัง specimen/replay/promotion
  gate ที่บังคับผ่านทั้งหมดเท่านั้น
- เก็บ unresolved/failed candidate ใน budget ledger
- ต้องมี independent review ที่แรงกว่าก่อน discovery claim

## 14. Falsification Review ที่บังคับ

ทุก milestone result ต้องบันทึก:

- supporting evidence
- contradicting evidence
- alternative explanation
- missing evidence
- confidence และ exact claim level

ต้องท้าทาย preferred hypothesis ด้วย sign/scaling test, deliberate missing
constraint, disconnected geometry, mesh/order change, boundary variant, solver
disagreement, stale artifact, non-convergence และ failure-event inconsistency

## 15. งานถัดไปทันที

Implement **Milestone 1: Solver Acceptance Harness** ก่อน เครื่องมือที่ติดตั้งมี
อยู่จริงแต่ยังไม่มี structural solve ที่รับเป็นหลักฐาน Implementation แรกควร
สร้าง disposable analytical tension specimen ที่ง่าย แล้วพิสูจน์ exact process
และ artifact contract ของ Gmsh/CalculiX/FreeCAD ก่อนสร้าง specimen suite เต็ม
