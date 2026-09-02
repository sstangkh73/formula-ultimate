# แผนดำเนินงานละเอียด: Work 080-086

ต้นฉบับภาษาอังกฤษ: `WORKS_080_086_DETAILED_EXECUTION_PLAN.md`

สถานะ: Program plan ที่ preregister แล้ว; Work 080 เป็น `In progress` ส่วน Work 081-086 ยังไม่เริ่ม

## 1. จุดประสงค์

แผนนี้ขยาย roadmap ที่เหลือเจ็ด Work เพื่อเดินจาก bounded B-rep test part แยกชิ้นไปสู่ Whole Mechanical Vehicle Candidate 001 เอกสารนี้เป็น execution contract ไม่ใช่หลักฐานว่าความสามารถที่ระบุถูกสร้างแล้ว

หลักฐานตั้งต้นที่ Completed:

- Work 077: geometry-causal part declaration แบบ fail-closed
- Work 078: B-rep/STEP fixture 5 ชิ้นแบบ one-solid deterministic และ feature operator ที่ execute จริง 15 ตัว
- Work 079: material, manufacturing-process, geometry-witness และ assignment contract

ข้อจำกัดตั้งต้นสำคัญ: material, process limit และ measurement array ของ Work 079 เป็น synthetic fixture และคืน `design_use_allowed=false` STEP hash เป็น toolchain evidence จริง แต่มิติยังไม่ถูกดึงอย่างอิสระโดย Work 081 และยังไม่มี sourced vehicle-design material/process record ที่รับเข้า

## 2. เป้าหมายหลัง Work 086

Candidate 001 จะเรียกว่า **รถเชิงกลทั้งคันที่พร้อมเริ่ม bounded whole-vehicle research** ได้เมื่อมี:

1. B-rep part แยกชิ้นและสร้างซ้ำได้พร้อม exact identity
2. sourced material/process record และ independently measured geometry เมื่อคำอ้าง design use บังคับ
3. assembly constraint พร้อม joint/DOF ที่คำนวณจริง
4. geometry-realized load, torque, energy, thermal และ ground-contact path ที่ต่อเนื่อง
5. mass, centre of mass, inertia, thickness, section, lever arm, clearance และ interface ที่ derive จาก geometry
6. mesh/solver evidence ที่ yield, fracture-domain, fatigue, torsion, buckling, connection และ numerical failure สังเกตได้
7. failure propagation เข้าสู่ subsystem state และ deterministic `DNF` เมื่อบังคับ
8. exact seed/config/toolchain replay โดยไม่มีการแก้ geometry ตามผลลัพธ์
9. whole-vehicle Level 0 admission case และ control ที่ประกาศครบ

ปลายทางนี้ยังไม่ใช่ physical validation, safety certification, manufacturing approval, novelty, superiority หรือรถจริงที่พร้อมแข่ง

## 3. Dependency และลำดับ batch

```text
Completed 077-079
      |
      v
080 Assembly and joint kernel
      |
      v
081 STEP -> FreeCAD geometry witness V2
      |
      +---- evidence remediation หาก material/process/measurement ยังใช้เพื่อ design ไม่ได้
      |
      v
082 Geometry -> structural physics coupling
      |
      v
083 Ground-interaction module Candidate 001
      |
      v
084 Energy conversion and torque-path Candidate 001
      |
      v
085 Load structure, packaging, and thermal integration
      |
      v
086 Whole Mechanical Vehicle Candidate 001
```

Cadence ยังคง `080-082`, `083-085` แล้ว `086` ภายในแต่ละ batch ต้องทำตามลำดับเพราะ Work หลังใช้ exact hash/evidence จาก Work ก่อน หาก dependency ถูก reject ให้สร้าง remedial work หมายเลขแยก ห้ามลด downstream gate

## 4. กติการ่วมทั้งโปรแกรม

### 4.1 ตัวควบคุมที่ต้อง freeze

ทุก admitted experiment ต้อง freeze ก่อน admitted run แรก:

- SI units และ coordinate-frame convention
- version ของ part/assembly/schema
- version ของ CadQuery, OCCT, FreeCAD, Gmsh, CalculiX, Python และ library
- material/process library version และ evidence hash
- random seed และ deterministic replay metadata
- solver tolerance, element family, mesh policy, load case และ timestep policy
- component library, baseline/control candidate และ compute budget
- training/holdout หรือ design/control partition เมื่อมี search

หากเปลี่ยนสิ่งเหล่านี้หลังเห็นผล admission จะเป็นโมฆะและต้องสร้าง config identity หรือ remedial work ใหม่

### 4.2 Numerical gate ร่วม

หาก Work ใดไม่ preregister gate เฉพาะที่เข้มกว่า ให้ใช้:

- artifact/config/schema identity แบบ exact: SHA-256 เหมือนกันทุก byte
- รับเฉพาะ finite value; `NaN`, infinity, invalid state และ solver divergence เป็น failure ที่ observable
- global/per-interface force/moment relative residual: `<=1e-5`
- energy-ledger relative residual: `<=1e-4`
- CAD/FreeCAD mass-property relative residual ที่เทียบกันได้: `<=1e-6`
- last-two mesh change ของ admitted response metric: `<=5%`
- event-time change ภายใต้ refinement ที่ประกาศ: relative `<=1e-6` เมื่ออ้าง failure localization
- penetration, clearance หรือ mate error ห้ามเกิน geometry/interface tolerance ที่ประกาศ
- ห้าม hidden repair, silent clipping, default material, default load path หรือแทนผลด้วย fidelity ต่ำกว่า

### 4.3 Evidence class

ทุก report ต้องระบุ evidence เป็นหนึ่งใน:

- `synthetic_verification`: validate implementation เท่านั้น
- `toolchain_cross_check`: เทียบ software path ที่อาจใช้ geometry technology ร่วมกัน
- `sourced_engineering`: source traceable พร้อม domain/condition/confidence
- `independent_measurement`: ดึงจาก exact artifact ผ่าน route อิสระที่ประกาศ
- `higher_fidelity_validation`: เทียบ solver, experiment หรือ real data ที่เข้มกว่า

เฉพาะ evidence class ที่ completion gate อนุญาตเท่านั้นจึงรองรับคำอ้างนั้นได้

### 4.4 Work log และ commit protocol

ก่อน implement Work 081-086 แต่ละตัว ต้องสร้าง work-log plan EN/TH แยกและ mark เฉพาะ Work นั้นเป็น `In progress` เมื่อ Completed ต้องสร้าง result EN/TH ที่บันทึก changed files, decisions, exact commands, exit codes, relevant output, supporting/contradicting evidence, alternative explanations, missing evidence, confidence และ limitations

ทุก Work ที่ Completed ต้องมี scoped commit หนึ่งรายการทันทีหลัง validation ห้าม blanket staging ต้องตรวจ `git diff --cached --name-status`, รัน `git diff --cached --check`, commit, ตรวจ hash และรัน post-commit replay ห้าม push อัตโนมัติ

## 5. Work 080 — Mechanical Assembly and Joint Kernel

### วัตถุประสงค์

แสดงตำแหน่งและ constraint ของ part จริง คำนวณ motion ที่ geometry/constraint อนุญาตจริง และ reject assembly ที่ misaligned, overconstrained, underconstrained, loose, interfering หรือชนตลอด motion ที่ประกาศ

### Entry gate

- part/interface declaration ของ Work 077 ผ่าน
- exact part geometry/STEP identity ของ Work 078 มีอยู่
- assembly part ทุกตัวมี local frame, persistent datum, typed interface และ tolerance
- code ของ Work 080 ห้ามสมมติ conventional wheel, suspension, steering หรือ powertrain layout

### Proposed implementation artifacts

- `config/assembly/mechanical_assembly_joint_kernel_v1.json`
- `src/formula_ultimate/assembly/joint_kernel.py` และ package exports
- `scripts/assembly/run_joint_kernel_acceptance.py`
- `tests/test_joint_kernel.py`
- contract/research record สองภาษา `MECHANICAL_ASSEMBLY_JOINT_KERNEL_V1`
- manifest, motion sample, collision report และ replay evidence ใต้ `artifacts/work080/`

ชื่อไฟล์สุดท้ายต้องยืนยันใน implementation review ของ Work 080 และบันทึกการเปลี่ยน ห้ามแทนแบบเงียบ

### ความสามารถบังคับ

1. assemble ด้วย datum point, axis, plane และ interface-surface signature
2. rigid, revolute, prismatic และ spherical joint constraint
3. joint limit และ home/reference state ที่ประกาศ
4. bearing-seat/shaft alignment, axial/radial clearance และ support spacing
5. interference, minimum gap และ continuous หรือ conservatively bounded swept-motion check
6. fastener-preload declaration โดยไม่อ้าง fastener capacity
7. connection translational/rotational stiffness และ compliance declaration
8. constraint Jacobian/rank และ realized six-DOF calculation
9. deterministic canonical assembly, joint และ motion-evidence hash

### การทดลองที่ preregister

- ตัวแปรอิสระ: mate type/count/order, part transform, datum/axis position, joint limit, bearing spacing, clearance, tolerance, compliance และ motion coordinate
- ตัวแปรตาม: constraint rank, null-space DOF, mate position/angular residual, coaxial error, clearance/gap, penetration, collision coordinate และ assembly hash
- reference: กลไกที่ neutral ต่อรูปแบบ conventional ประกอบด้วย fixture แยกของ rigid, revolute, prismatic, spherical และ combined mechanism หนึ่งตัว
- controls: key-order permutation, mirrored frame, shaft misalignment, redundant two-bearing lock, missing constraint, excessive clearance, negative clearance, collision ใน travel, declared DOF ผิด, duplicate interface, missing datum และ non-finite transform

### ลำดับ implementation

1. กำหนด exact assembly/joint schema และ canonical serialization
2. implement frame transform และ right-handed datum resolution
3. สร้าง constraint equation และ rank/null-space evidence
4. implement joint limit และ deterministic motion sampling/refinement
5. เพิ่ม clearance, interference และ swept-volume collision check
6. เพิ่ม compliance/preload declaration เป็น evidence เท่านั้น
7. รัน isolated fixture, combined reference, falsification control และ replay
8. บันทึก contradictory/missing evidence และ freeze admitted config

### Completion gates

- calculated DOF count/type ตรง reference declaration exact
- reference mate position residual `<=1e-6 m` และ angular residual `<=1e-6 rad` โดยยังต้องอยู่ใน declared tolerance ที่เข้มกว่า
- coaxial bearing/shaft error และ clearance อยู่ใน declared limit
- ไม่มี forbidden penetration เกิน geometry tolerance ตลอด motion envelope
- over/underconstraint, looseness, misalignment และ collision control reject ด้วย causal code แยก
- mapping-key permutation รักษา exact identity; การเปลี่ยน array/order/geometry ที่ causal ต้องเปลี่ยน identity
- invalid evidence ต้องเขียน downstream state เป็นศูนย์รายการ

### Proposed validation commands

```powershell
python -m unittest tests.test_joint_kernel -v
python scripts/assembly/run_joint_kernel_acceptance.py --config config/assembly/mechanical_assembly_joint_kernel_v1.json --output artifacts/work080/evidence.json
python -m unittest discover -s tests -q
python -m compileall -q src scripts tests
```

### ข้ออ้างที่ห้ามและ stop condition

ห้ามอ้าง bearing life, friction/wear, bolt/weld strength, dynamic vibration, crash response หรือ physical validation หยุด Work 080 หาก bound continuous collision ไม่ได้, constraint rank ambiguous ภายใต้ refinement หรือ reference mechanism ต้องใช้ auto-alignment/repair

## 6. Work 081 — STEP to FreeCAD Geometry Witness V2

### วัตถุประสงค์

Import exact canonical STEP อย่างอิสระและ derive physical input ที่ downstream assembly/physics ต้องใช้แทนค่าพิมพ์มือ

### Entry gate

- Work 080 Completed พร้อม stable assembly/interface/datum identity
- freeze exact per-part/assembly STEP hash
- semantic interface มี geometry signature และ datum witness ที่ไม่ขึ้นกับ face number ชั่วคราว

### Proposed implementation artifacts

- `config/cad/step_freecad_geometry_witness_v2.json`
- `src/formula_ultimate/components/geometry_witness.py`
- `scripts/cad/inspect_geometry_witness_v2_freecad.py`
- `scripts/cad/compare_geometry_witness_v2.py`
- `tests/test_geometry_witness_v2.py`
- report สองภาษา `STEP_FREECAD_GEOMETRY_WITNESS_V2`
- FreeCAD JSON, FCStd, comparison และ replay evidence ใต้ `artifacts/work081/`

### Measurement ที่บังคับ

- STEP SHA-256, part count, solid count, shape validity และ no-repair status
- volume, material-linked mass, centre of mass, full inertia tensor, principal axes และ bounding box
- hole/bore/shaft diameter, wall thickness sample/minimum, section area/centroid/second moment/torsion proxy เมื่อรองรับ
- interface position/orientation/signature, joint axis, load/support/contact surface
- clearance ระหว่าง part, minimum gap, interference volume/depth และ motion-envelope witness
- measurement method, resolution/tolerance, tool version, report hash และ unsupported measurement

### การทดลองที่ preregister

- ตัวแปรอิสระ: part family, STEP export/reimport, measurement resolution, interface signature, transformed placement และ deliberate geometry mutation
- ตัวแปรตาม: measurement value, CAD-to-FreeCAD residual, signature recovery, invalid/repair state และ report identity
- controls: Work 078 part ทั้ง 5, Work 080 reference assembly, key-order replay, STEP byte เปลี่ยน, solid เกิน/หาย, face rename/reorder, geometry-signature collision, thin-wall mutation และ deliberate interference

### ลำดับ implementation

1. freeze exact STEP/declaration hash
2. import ด้วย FreeCAD ใน read-only/no-heal mode เท่าที่ API เปิดให้
3. ดึง global mass property และ local feature measurement
4. recover datum/interface ด้วย geometry signature ร่วม spatial witness ไม่ใช้ `Face17`
5. วัด clearance/interference และ motion state ที่ประกาศ
6. เทียบ CadQuery/declaration evidence และจำแนกข้อจำกัด shared technology
7. bind measurement report hash เข้า geometry-witness contract ของ Work 079
8. รัน mutation/falsification corpus และ exact replay

### Completion gates

- imported STEP hash ตรง frozen exporter hash exact
- part/solid count และ valid-solid state ตรง declaration; repair flag ใด ๆ ต้อง reject
- volume/mass/COM/inertia residual `<=1e-6` relative เมื่อเทียบตรงได้
- interface/datum position และ axis อยู่ใน declared tolerance
- required semantic interface/load/contact region ทุกตัว recover ได้แบบ unique โดยไม่พึ่ง face number
- thickness/section measurement converge ภายใต้ resolution study; proposed last-two change `<=1%` สำหรับ smooth canonical fixture
- altered hash, solid count, signature ambiguity, missing region หรือ hidden repair ต้อง fail closed
- FreeCAD run ซ้ำให้ canonical measurement/report identity เดิม exact

### Proposed validation commands

```powershell
& "C:\Program Files\FreeCAD 1.1\bin\python.exe" scripts/cad/inspect_geometry_witness_v2_freecad.py --config config/cad/step_freecad_geometry_witness_v2.json --output-root artifacts/work081
python scripts/cad/compare_geometry_witness_v2.py --artifact-root artifacts/work081 --output artifacts/work081/comparison.json
python -m unittest tests.test_geometry_witness_v2 -v
python -m unittest discover -s tests -q
```

### ข้ออ้างที่ห้ามและ stop condition

CadQuery/FreeCAD อาจใช้ OCCT technology ร่วมกัน ดังนั้น agreement เป็น toolchain cross-check ไม่ใช่ independent physical validation หยุดหาก recover semantic region โดยไม่ใช้ face number ไม่ได้, measurement ต้อง hidden repair หรือ resolution sensitivity เกิน frozen gate

### Evidence-remediation gate บังคับก่อน Work 082 design use

Work 081 ต้องแทน synthetic measurement array ของ Work 079 ด้วย evidence `independently_measured` และ material/process record อย่างน้อยหนึ่งชุดที่ใช้กับ design-use structural claim ต้อง sourced พร้อม condition/domain/confidence หากไม่มี evidence ให้สร้าง remedial work Work 082 อาจทดสอบ software coupling ด้วย synthetic fixture แต่ห้าม complete คำอ้าง design-material หรือ real-part capacity จาก fixture นั้น

## 7. Work 082 — Geometry-to-Structural Physics Coupling

### วัตถุประสงค์

ส่ง exact geometry-witness region และ sourced engineering property เข้า meshed structural solve, จำแนก deformation/failure/numerical state และ propagate connection failure เข้า vehicle connection graph

### Entry gate

- exact independent measurement report ของ Work 081 ผ่าน
- support/load/contact surface recover ได้ unique
- material/process/measurement evidence ตรง claim class ที่จะทดสอบ
- solver-acceptance fixture เดิมสำหรับ tension, bending, torsion, yield, fracture initiation, fatigue, buckling และ failure coupling ยังผ่าน

### Proposed implementation artifacts

- `config/structural/geometry_structural_coupling_v1.json`
- `src/formula_ultimate/structural/geometry_coupling.py`
- `scripts/structural/run_geometry_structural_coupling.py`
- `tests/test_geometry_structural_coupling.py`
- report สองภาษา `GEOMETRY_STRUCTURAL_COUPLING_V1`
- mesh, deck, solver file, parsed field, convergence และ failure ledger ใต้ `artifacts/work082/`

### Pipeline ที่บังคับ

1. เลือก exact support/load region จาก Work 081 witness
2. สร้าง mesh refinement ที่ประกาศอย่างน้อยสามระดับโดยไม่เปลี่ยน geometry
3. assign exact material identity ของ Work 079 พร้อม domain
4. ใช้ immutable load case พร้อม force/moment provenance
5. solve และ parse displacement, strain, stress, plastic variable, reaction และ energy
6. ประเมิน elastic deformation, yield/plasticity, ultimate-domain violation, fracture-domain violation, fatigue state, torsion, local/global buckling และ numerical failure
7. map failure ไป typed connection state และถอด/redistribute forbidden wrench path
8. emit deterministic result/failure/replay identity

### การทดลองที่ preregister

- ตัวแปรอิสระ: exact part geometry, thickness/section mutation, material record, mesh level/element family, load/support region, load magnitude/direction, flaw/fatigue state และ connection topology
- ตัวแปรตาม: stiffness/compliance, stress/strain/displacement, reaction, energy, residual, convergence, failure mode/location/time, transmitted wrench และ `DNF`/subsystem state
- controls: analytical accepted fixture, thicker/thinner geometry, severed load path, missing surface, reversed load, below-yield load/unload, deliberate overload, fatigue crossing, buckling fixture, redundant/critical connection และ solver divergence injection

### Completion gates

- exact geometry/material/load identity trace ผ่าน mesh, deck, result และ failure ledger
- force/moment residual `<=1e-5`, energy residual `<=1e-4`
- last-two mesh change `<=5%` สำหรับ admitted compliance, displacement, integrated reaction และ non-singular stress/failure metric
- thicker control ห้ามอ่อนลงโดยไม่มี geometric/mode explanation ที่บันทึก
- severed path ห้ามส่ง forbidden wrench
- failure ต้องเปลี่ยน connection state/downstream response; critical path failure ให้ deterministic `DNF` เมื่อประกาศ
- unsupported fracture/fatigue/material domain ต้อง reject แทน neutral capacity
- solver divergence/invalid state เป็น experiment result โดยไม่มี silent correction
- exact replay ภายใต้ pinned tools/seeds

### Proposed validation commands

```powershell
python scripts/structural/run_geometry_structural_coupling.py --config config/structural/geometry_structural_coupling_v1.json --artifact-root artifacts/work082 --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
python -m unittest tests.test_geometry_structural_coupling -v
python -m unittest discover -s tests -q
```

### ข้ออ้างที่ห้ามและ stop condition

การผ่าน bounded part/load family หนึ่งตัวไม่ใช่ arbitrary-component strength, crashworthiness, fatigue life หรือ physical validation หยุดหาก convergence fail, reaction ไม่ปิด, material domain unsupported, critical region singular/unresolved หรือ failure ไม่เปลี่ยน connection graph แบบ causal

## 8. Work 083 — Ground-Interaction Module Candidate 001

### วัตถุประสงค์

สร้าง inspectable multi-part mechanical subsystem แรกที่ส่ง ground force/torque เข้า structural mount พร้อม motion, braking และ steering/force-direction behavior ที่ประกาศ โดยไม่บังคับ conventional suspension/wheel architecture

### Entry gate

- Work 080-082 Completed
- real-part claim ใช้ design-eligible material/process/measurement evidence
- freeze allowed topology/function requirement และ compute budget ก่อน candidate generation

### Proposed implementation artifacts

- `config/candidates/ground_interaction_candidate_001.json`
- per-part CadQuery config และ exact STEP artifact
- complete subsystem STEP และ FCStd
- `src/formula_ultimate/subsystems/ground_interaction.py`
- `scripts/candidates/build_ground_interaction_candidate_001.py`
- `tests/test_ground_interaction_candidate_001.py`
- candidate design/experiment report สองภาษา
- assembly, motion, load-path, structural และ replay evidence ใต้ `artifacts/work083/`

### Functional requirements

- ground contact และ positive/observable normal-force state
- longitudinal/lateral force transfer
- torque receipt/transmission และ braking path
- force-direction change เมื่อประกาศ
- vertical motion envelope
- structural-mount load path
- unwanted-DOF constraint
- failure state ที่เปลี่ยน subsystem behavior

### การทดลองที่ preregister

- ตัวแปรอิสระ: topology, part count, joint location/type, section geometry, wall thickness, material, bearing/support spacing, contact radius, motion ratio และ declared travel
- ตัวแปรตาม: mass/inertia, stiffness, stress/fatigue/buckling margin, steering/force-direction response, travel, torque efficiency, unsprung-equivalent inertia, clearance และ failure mode
- controls: mirrored candidate, rigid/no-travel control, disconnected mount, blocked joint, seized bearing/connection, broken torque path, undersized section, contact-loss case และ replay

### ลำดับ implementation

1. freeze functional requirement โดยไม่เลือก conventional layout
2. propose topology และ separate part contract
3. สร้าง B-rep, interface, material/process assignment และ exact STEP hash
4. assemble ด้วย Work 080 joint และสร้าง FCStd evidence
5. inspect ด้วย Work 081 และแก้ผ่าน config identity ใหม่ก่อน admission เท่านั้น
6. รัน kinematics, clearance, force/torque path และ structural case ของ Work 082
7. inject causal failure และ propagate subsystem state
8. รัน mirror/control/refinement/replay และสร้าง candidate report

### Completion gates

- FCStd/STEP แสดง separate physical part ไม่ใช่ functional solid เดียว
- calculated joint DOF/travel ตรง declaration ภายใน gate ของ Work 080
- มี unique continuous path จาก ground force ไป structural mount และจาก braking/drive torque ไป contact
- force/moment residual `<=1e-5`, energy residual `<=1e-4`
- ไม่มี forbidden interference ตลอด motion; ground clearance/service envelope ผ่าน tolerance
- structural case ที่บังคับ converge ตาม Work 082 gate
- break/seizure ที่ inject ทุกตัวเปลี่ยน measurable behavior และ critical failure ที่บังคับทำให้ subsystem failure/`DNF`
- mirror/control result ตรง symmetry ที่ประกาศหรือมี causal asymmetry ที่บันทึก
- exact seed/config replay สร้าง declaration, STEP, assembly และ evidence hash เดิม

### ข้ออ้างที่ห้ามและ stop condition

ห้ามเรียกว่า validated suspension, wheel, steering, brake, tyre หรือ production subsystem หยุดหาก solution ที่ผ่านต้องพึ่ง conventional topology ที่ evaluator hard-code, synthetic design evidence, hidden geometry edit หรือ load/torque path ที่ยังไม่ปิด

## 9. Work 084 — Energy Conversion and Torque-Path Candidate 001

### วัตถุประสงค์

แทน abstract energy-converter box และ scalar ratio ด้วย geometry, mount, support, torque-transfer interface, loss, braking-energy route และ thermal rejection จริง โดยรักษา technology neutrality

### Entry gate

- freeze torque/contact interface ของ Work 083
- candidate ประกาศ technology และ evidence domain เฉพาะโดย evaluator ไม่ prefer historical powertrain layout
- energy-equivalent race profile, onboard pre-race energy และ recovery accounting ยังบังคับ

### Proposed implementation artifacts

- `config/candidates/energy_torque_path_candidate_001.json`
- separate store/converter/shaft-or-equivalent/support/coupling/housing/cooling STEP
- assembly STEP และ FCStd
- `src/formula_ultimate/subsystems/energy_torque_path.py`
- `scripts/candidates/build_energy_torque_path_candidate_001.py`
- `tests/test_energy_torque_path_candidate_001.py`
- torque/energy/thermal experiment report สองภาษา
- torque, speed, bearing, structural, energy, thermal, failure และ replay ledger ใต้ `artifacts/work084/`

### Function ที่บังคับ

- energy-store interface และ mass/state identity
- converter geometry และ mounting load path จริง
- input/output shaft หรือ mechanically equivalent torque path
- torque multiplication/transformation mechanism และ support
- bearing หรือ alternative reaction support
- output coupling ไป Work 083
- housing พร้อม lubrication/cooling interface
- braking-energy path และ conserved recovery source
- explicit loss/thermal-rejection ledger

### การทดลองที่ preregister

- ตัวแปรอิสระ: declared technology, topology, ratio/mechanism geometry, shaft/equivalent section, support spacing, speed/torque schedule, efficiency/loss model, cooling interface และ failure injection
- ตัวแปรตาม: torque equilibrium, torsional stress/twist, bearing/support reaction, housing deformation, rotational limit, delivered power, energy residual, loss/heat rate, required rejection และ failure propagation
- controls: locked converter, seized support, broken coupling, zero-loss exploit, efficiency เกินหนึ่ง, reversed torque, overspeed, inadequate cooling, disconnected housing reaction และ equal-energy replay

### Completion gates

- continuous geometry/interface torque path จาก converter ถึง contact ของ Work 083
- torque/reaction residual `<=1e-5` และ energy residual `<=1e-4`
- efficiency อยู่ใน `[0,1]`; recovered energy มี conserved source/loss ที่ observable
- shaft/equivalent, support, housing case ผ่าน Work 082 gate หรือ fail observable
- speed, temperature, material domain ถูก enforce โดยไม่ clip
- heat generation/rejection requirement ปิดตลอด declared duration
- seized/broken control ถอดหรือเปลี่ยน torque และ propagate failure deterministic
- ใช้ energy-equivalent profile และ compute/evidence opportunity เท่ากับ control/baseline

### ข้ออ้างที่ห้ามและ stop condition

ห้ามอ้าง validated motor, engine, battery, fuel, transmission, cooling system หรือ technology superiority หยุดเมื่อมี undeclared energy, energy creation, unsupported property evidence, missing reaction path, heat ledger ไม่ปิด หรือ evaluator bias ไป conventional technology/layout

## 10. Work 085 — Load Structure, Packaging และ Thermal Integration

### วัตถุประสงค์

สร้าง geometry-causal load structure และ package Work 083/084 พร้อม control/routing/thermal interface โดยไม่มี interference แทน abstract `load_spine` ด้วย structure ที่ agent ออกแบบจาก load/spatial constraint

### Entry gate

- Work 083/084 Completed พร้อม frozen mount/interface/motion/heat identity
- preregister whole-system load case และ packaging envelope
- ประกาศ service/removal/routing requirement ก่อน topology generation

### Proposed implementation artifacts

- `config/candidates/load_structure_integration_001.json`
- separate structure/mount/routing/support STEP, complete integration STEP และ FCStd
- `src/formula_ultimate/subsystems/load_structure_integration.py`
- `scripts/candidates/build_load_structure_integration_001.py`
- `tests/test_load_structure_integration_001.py`
- packaging/load/thermal report สองภาษา
- interference, service path, routing, structural, thermal, failure และ replay evidence ใต้ `artifacts/work085/`

### Function/case ที่บังคับ

- mounting geometry จริงของทุก subsystem
- ไม่มี forbidden interference ทั้ง static และ motion envelope
- declared service/removal swept path
- power/control/fluid routing พร้อม bend/clearance limit
- heat-source/heat-rejection interface
- ground clearance และ external envelope
- acceleration, braking, cornering, combined, bump/vertical, aero เมื่อ admitted และ torque-reaction load
- bending, torsion, buckling, fatigue-domain และ mount-failure evaluation

### การทดลองที่ preregister

- ตัวแปรอิสระ: structural topology, member/skin section, material, mount position, subsystem placement, routing, thermal-interface location และ service path
- ตัวแปรตาม: total mass/COM/inertia, package volume, clearance/interference, service feasibility, route length/loss, temperature/heat rejection, stiffness, stress/fatigue/buckling margin, mount reaction และ failure mode
- controls: box-like placeholder baseline, disconnected mount, blocked service path, routing collision, inadequate thermal rejection, asymmetric load, weakened mount, thin/buckling structure และ mirror/replay

### Completion gates

- subsystem ทุกตัวมี unique inspectable geometry-realized mount/load/torque/thermal interface
- ไม่มี forbidden interference เกิน tolerance ตลอด motion/service envelope
- routing/service path ผ่าน clearance/bend/tool rule หรือ fail explicit
- mass/COM/inertia มาจาก Work 081 geometry evidence
- declared load case ทุกตัวปิด force/moment residual `<=1e-5`, energy residual `<=1e-4`
- structural mesh/convergence/failure ตรง Work 082
- heat generation/storage/transfer/rejection ปิดตลอด duration
- weakened/disconnected control ทำให้เกิด structural/subsystem consequence ที่คาด
- exact replay และไม่มี result-conditioned topology repair

### ข้ออ้างที่ห้ามและ stop condition

ห้ามเรียกว่า chassis, monocoque, crash structure, cooling package หรือ production assembly หากคำอ้าง exact นั้นยังไม่ validate อิสระ หยุดหาก packaging ผ่านด้วยการ suppress overlap, ลบ service requirement หลังเห็นผล, ทิ้ง heat โดยไม่มี sink หรือ structure เป็นกล่องรูปรถเพื่อประดับเท่านั้น

## 11. Work 086 — Whole Mechanical Vehicle Candidate 001

### วัตถุประสงค์

รวม admitted subsystem ทุกตัวเป็น deterministic candidate หนึ่งตัว และตัดสินว่าพร้อมเข้าสู่ bounded whole-vehicle research ภายใต้ Level 0/evidence gate ที่ประกาศหรือไม่

### Entry gate

- Work 080-085 Completed โดยไม่มี unresolved numerical, identity, material, interface, load-path, energy, packaging หรือ thermal blocker
- freeze final training/control/admission case
- ห้าม geometry/evidence mutation หลัง admitted whole-vehicle run แรก

### Artifact บังคับ

- individual STEP ทุก part พร้อม exact per-file hash
- complete assembly STEP และ FreeCAD FCStd
- assembly tree และ joint/DOF manifest
- material/process/measurement manifest
- mass/COM/full-inertia report
- clearance/interference/motion/service report
- structural load-case/convergence report
- torque/power/energy/thermal ledger
- failure-propagation/`DNF` report
- deterministic seed/config/toolchain/replay manifest
- integrated Level 0 result พร้อม mirrored/control candidate evidence

### Proposed implementation artifacts

- `config/candidates/whole_mechanical_vehicle_candidate_001.json`
- `src/formula_ultimate/experiments/whole_mechanical_vehicle_candidate.py`
- `scripts/candidates/run_whole_mechanical_vehicle_candidate_001.py`
- `tests/test_whole_mechanical_vehicle_candidate_001.py`
- admission/result report สองภาษา
- immutable evidence bundle ครบใต้ `artifacts/work086/`

### Admission case บังคับ

1. static support/stable contact
2. straight acceleration
3. braking
4. steady cornering
5. combined braking/cornering
6. bump/vertical event และ motion envelope
7. converter/drive torque reaction
8. declared thermal-duration case
9. single critical connection failure
10. redundant connection/control failure เมื่อประกาศ
11. mesh/timestep/refinement และ exact replay
12. mirrored/control candidate
13. integrated Level 0 lap/race gate ที่ใช้ geometry-derived input

### การทดลองที่ preregister

- ตัวแปรอิสระ: complete topology/config, seed, control/mirror identity, load/admission case, refinement level และ injected failure
- ตัวแปรตาม: artifact validity, mass property, contact/DOF, residual, structural/thermal/energy margin, failure, progress/lap/race outcome, `DNF`, compute use และ complete evidence identity
- controls: mirrored candidate, deliberate weak/disconnected connection, heavy feasible control, no-hidden-repair exploit control, energy exploit control, geometry-hash mutation, unsupported-evidence control และ replay

### Completion gates

- mandatory artifact ทุกตัวมีอยู่ cross-reference exact identity และ replay
- ไม่มี placeholder functional box แทน required physical part/path
- external load ทุกตัวปิดผ่าน geometry ไป contact/support และ drive/brake torque ปิดผ่าน interface จริง
- mass/COM/inertia, clearance, section, lever arm และ interface derive จาก geometry
- admitted case ทุกตัวผ่าน common numerical gate หรือให้ causal failure/`DNF` ที่ประกาศ
- deliberate weak/disconnected/exploit control reject/fail ด้วยสาเหตุที่คาด
- ห้ามเปลี่ยน training/control/admission case, solver tolerance, evidence class หรือ geometry หลังเห็น admitted result
- exact repeat สร้าง immutable evidence bundle hash เดิม
- final verdict ต้องเป็น `ready_for_bounded_whole_vehicle_research` หรือ `not_ready` พร้อม blocker เท่านั้น

### Proposed validation commands

```powershell
python scripts/candidates/run_whole_mechanical_vehicle_candidate_001.py --config config/candidates/whole_mechanical_vehicle_candidate_001.json --artifact-root artifacts/work086
python -m unittest tests.test_whole_mechanical_vehicle_candidate_001 -v
python -m unittest discover -s tests -q
python -m compileall -q src scripts tests
```

### ข้ออ้างที่ห้ามและ stop condition

แม้ verdict `ready` ก็อนุญาตเฉพาะ bounded research ไม่พิสูจน์ real race completion, safety, manufacturability, legality, novelty, optimized superiority หรือ physical validity ต้องหยุดและคืน `not_ready` เมื่อ artifact หาย, hash stale, evidence unsupported, non-convergence, force/energy/thermal path ไม่ปิด, hidden repair, unfair control หรือผลทำซ้ำไม่ได้

## 12. Program stop/go review

### Gate A — Real part mechanics

Work 080-082 ผ่านพร้อม calculated DOF, independent geometry measurement, design-eligible evidence สำหรับ capacity claim, converged structural response และ causal failure propagation การผ่าน Gate A เป็นจุดแรกที่ bounded tested item อาจเรียกว่า geometry/material/load-causal research part

### Gate B — Functional mechanical subsystems

Work 083-084 ผ่านพร้อม real multi-part ground และ torque/energy path การผ่าน Gate B อนุญาต integration work แต่ยังไม่ validate subsystem ทางกายภาพ

### Gate C — Vehicle-scale integration

Work 085 ผ่าน packaging, load structure, routing และ thermal integration โดยไม่มี hidden overlap หรือทิ้ง load/heat

### Gate D — Whole-vehicle research readiness

Work 086 คืน exact admission verdict หาก hypothesis reject, real evidence หาย หรือ solver limitation ต้องสร้าง remedial work ใหม่ ห้ามลด gate หลังเห็นผล

## 13. นิยามความคืบหน้าที่ผู้ใช้มองเห็น

- ตอนนี้: มี real B-rep/STEP test-part shape 5 ชิ้นที่เปิดดูได้ แต่ยังไม่ใช่ design-eligible vehicle part
- หลัง Work 080: เห็น part ประกอบกันพร้อม joint/DOF ที่คำนวณและยืนยัน
- หลัง Work 081: เห็น part ใน FreeCAD พร้อม independently extracted dimension, mass property, interface และ clearance
- หลัง Work 082: เห็น bounded part deform/fail จาก geometry/material/load evidence
- หลัง Work 083: ได้ ground-interaction subsystem หลายชิ้นจริงตัวแรกใน FCStd
- หลัง Work 084: ได้ geometry torque/energy path จริงเชื่อมกับ subsystem
- หลัง Work 085: ได้ integrated load structure/packaging ระดับรถ
- หลัง Work 086: ได้ Whole Mechanical Vehicle Candidate 001 evidence bundle และ research-readiness verdict
