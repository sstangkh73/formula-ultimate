# Roadmap ความหลากหลายในการออกแบบเชิงเรขาคณิต V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `GEOMETRIC_DESIGN_DIVERSITY_ROADMAP_V1.md`

## เป้าหมาย

Formula Ultimate ต้องการมากกว่าแค่ขอบมน เป้าหมายคือระบบค้นหาที่คิด **functional topology** ที่ไม่คุ้นเคย แปลงเป็น parametric B-rep ที่ valid ประเมินด้วยฟิสิกส์ที่เกิดจาก geometry และเก็บไว้เฉพาะเมื่อผ่าน evidence gate เดียวกับ candidate ที่ดูธรรมดา

รูปลักษณ์แปลกไม่เท่ากับ discovery Candidate จะเริ่มมีโอกาสเป็นของใหม่เมื่อ topology หรือเส้นทางแรง/พลังงาน/การเคลื่อนที่แตกต่างจากคลังเปรียบเทียบอย่างวัดได้ ฟังก์ชันเกิดขึ้นเชิงสาเหตุ ไม่มี hidden geometry repair ทำ replay exact ได้ และรอดจากการประเมินฟิสิกส์ที่ยุติธรรม

## ขอบเขตปัจจุบัน

CadQuery `2.8.0` ที่ติดตั้งมี spline, arc, sweep, loft, fillet และ chamfer ดังนั้น CAD kernel ไม่ใช่ต้นเหตุหลักของความเหลี่ยม Bias เกิดจากสามชั้นที่แคบกว่า:

1. Functional vehicle grammar ยอมรับเฉพาะ box และ cylinder ตามแกน
2. B-rep Grammar V1 เริ่มจาก profile แบบ rectangle, circle, annulus หรือ shaft section และยังไม่มี declaration สำหรับ general wire, spline control point, 3D path, sweep หรือ loft
3. `DesignSearchAgentV0` เปลี่ยน scalar scale factor ห้าค่าบน component graph ที่ตายตัว ส่วน Work 083, 084 และ 087 ใช้ procedural builder ที่เขียนด้วยมือและประกอบจาก box/cylinder เป็นหลัก แทนการใช้ feature grammar ที่ agent เขียนได้

ดังนั้นระบบปัจจุบันมีชิ้นส่วนจริงที่ตรวจดูได้ แต่ยังไม่มี generative design แบบ free topology

## นิยามความหลากหลายที่มีประโยชน์และห้ามลดทอน

การอ้าง design diversity ต้องมีครบทุกข้อ:

- **Representational reach:** grammar เขียน solid แบบโค้ง เรียว แตกแขนง กลวง มี rib เป็น shell และ hybrid ได้โดยไม่ import opaque mesh
- **Topological reach:** mutation เพิ่ม ลบ แยก รวม แตกแขนง และเชื่อม part/feature/interface ใหม่ได้ ไม่ใช่เพียงปรับขนาด
- **Functional closure:** terminal ด้านแรง torque motion thermal fluid electrical และ control ที่บังคับเชื่อมต่อเชิงสาเหตุ
- **Physical consequence:** geometry กำหนด mass, centre of mass, inertia, clearance, section property, mesh, stress, deformation, ปริมาณ heat/flow และ failure
- **Manufacturing consequence:** constraint ของกระบวนการผลิตมีผลต่อ admission ไม่ใช่ metadata ประดับ
- **Search diversity:** archive รักษา feasible niche หลายชนิดแทนการยุบไปหา primitive ครอบครัวเดียวที่ง่ายที่สุด
- **Evidence discipline:** exact replay, immutable source identity, numerical failure และหลักฐานที่ขาดต้องมองเห็นได้

ห้ามให้งานใดให้รางวัลกับ novelty เพียงอย่างเดียว บังคับรูปทรงรถตามประเพณี หรือนับรูปทรงที่ดูแปลกแต่ประเมินฟิสิกส์ไม่ได้เป็น discovery

## ลำดับภาพรวม

| ชุด | Work | ความสามารถที่ได้ |
|---|---|---|
| 1 | 090–091 | วัด bias เดิม; ประกาศ constrained 2D profile แบบ arbitrary |
| 2 | 092–093 | สร้าง free-form solid; เขียน topology ของ part/feature/interface ที่ mutate ได้ |
| 3 | 094–095 | Mutate topology แบบทำซ้ำได้; บังคับ validity/manufacturing โดยไม่มี hidden repair |
| 4 | 096–097 | กู้ semantic จาก arbitrary geometry; mesh และประเมินฟิสิกส์ได้ |
| 5 | 098–099 | จัดสรร compute อย่างยุติธรรม; ค้นหา quality และ diversity พร้อมกัน |
| 6 | 100–101 | ทดลองค้นพบ subsystem; integrate และ promote เฉพาะ candidate ที่รอด |

โอกาสแรกที่ป้องกันได้ด้วยหลักฐานว่าจะเห็นชิ้นส่วนทำงานที่ไม่คุ้นเคยจริงอยู่หลัง Work 097 และการค้นพบจริงเริ่มใน Work 100 ชิ้นส่วนโค้งอาจเห็นหลัง Work 092 แต่ตอนนั้นยังไม่ใช่ discovery ที่มีหลักฐานรองรับ

## Work 090 — Search-Space Bias and Diversity Contract

### วัตถุประสงค์

วัด primitive/topology bias ปัจจุบันก่อนขยาย grammar และตรึง metric ที่ห้ามเปลี่ยนหลังเห็นผล

### Deliverable

- Contract descriptor/distance ชื่อ `design_diversity_v1`
- Census แบบ deterministic ของ reference candidate เดิมและ generated sample ที่มีขอบเขต
- Canonical topology signature ที่ไม่เปลี่ยนเมื่อ translate, rotate, เปลี่ยนชื่อ part หรือ uniform scale ทั้งระบบ
- Baseline report สำหรับ primitive fraction, profile/operator entropy, curvature distribution, ความหลากหลายของ part/interface graph, phenotype duplication, load-path diversity, failure-mode diversity และสาเหตุ invalid candidate

### Metric ที่บังคับ

- `unique_topology_signatures / attempted_candidates`
- `unique_geometry_signatures / valid_candidates`
- duplicate phenotype rate
- Shannon entropy ของ feature operator และ interface type
- curved-surface-area fraction และ curvature-spectrum histogram
- graph-edit distance บน typed part/interface graph
- ระยะห่างของ load/energy/motion path signature
- feasible archive coverage และ failure-mode coverage

### การหักล้างและเกณฑ์สำเร็จ

Metric ต้องจัด translation, rotation, renaming และ uniform rescaling เป็น control ที่ไม่ใหม่ แต่ตรวจพบการเพิ่ม branch, reroute path, เปลี่ยน profile family และเปลี่ยน interface topology ได้ ผลผ่านเพียงทำให้ bias วัดได้ ยังไม่พิสูจน์ว่า search สร้าง diversity ได้

## Work 091 — Constrained Free-Form Sketch and Wire Grammar V2

### วัตถุประสงค์

แทนคอขวด profile สี่แบบด้วยภาษา 2D profile แบบ typed, bounded และ replay ได้

### Operator

- line segment, tangent arc, three-point arc, circle, ellipse
- quadratic/cubic Bezier และ B-spline ที่จำกัด degree
- polyline และ closed wire แบบ mixed segment
- หลาย loop สำหรับ hole/island
- mirror, rotate, translate, offset, trim และ bounded constraint solve
- constraint แบบ dimensional, coincident, tangent, concentric, parallel, perpendicular และ symmetry

### ขอบเขตความปลอดภัย

ทุก wire ต้องประกาศ local coordinate, หน่วย, ขอบเขต control point, degree, นโยบาย knot/weight, closure tolerance, minimum radius และ provenance ปฏิเสธ open loop, self-intersection, duplicate edge, zero-length segment, feature ต่ำกว่า tolerance, hole nesting ผิด และ constraint solution ที่ไม่ deterministic

### เกณฑ์สำเร็จ

Corpus อย่างน้อยสิบสอง profile จากอย่างน้อยหก family ต้อง export canonical wire identity เหมือนกันสองรอบ Metamorphic test ต้องคง identity เมื่อสลับลำดับ key ใน declaration และเปลี่ยน identity เมื่อ geometry mutation งานนี้พิสูจน์ profile expressivity ไม่ใช่ solid validity หรือประโยชน์เชิงฟิสิกส์

## Work 092 — Free-Form B-rep Solid Grammar V2

### วัตถุประสงค์

แปลง wire จาก Work 091 และ bounded 3D path เป็น solid แบบ single/multi-feature ที่ valid โดยไม่ใช้ opaque mesh แทน

### Operator

- extrude/revolve ด้วย local axis อิสระ
- straight/curved sweep หรือ pipe ตาม 3D path ที่ประกาศ
- multi-section loft พร้อมการควบคุม correspondence/orientation
- taper/draft, shell, variable section, rib/web, gusset, pocket, bore และ local pattern
- bounded fillet/chamfer ที่เลือกด้วย geometry signature แทน edge number ที่ไม่เสถียร
- boolean union/subtract/intersect และ multi-body output ที่ประกาศชัดเมื่อ part contract อนุญาต
- deterministic local transform และ datum creation

### เกณฑ์สำเร็จ

Non-primitive solid อย่างน้อยสิบแบบ—รวม curved branch, tapered hollow duct, lofted rotary member, organic-like load bridge และ variable-section shell—ต้อง valid ทั้ง CadQuery/FreeCAD รักษา semantic datum ผ่าน STEP และ replay ได้ geometry identity เดิม รูปทรงโค้งอย่างเดียวยังไม่พิสูจน์ topology mutation

## Work 093 — Typed Morphology and Topology Genome V1

### วัตถุประสงค์

แทน candidate จากรายการ component ที่เลือกไว้ล่วงหน้าด้วย typed graph ที่ mutate ได้

### ชั้นของ Genome

1. Functional terminal และ domain ที่บังคับ
2. Part graph และ parent/child containment
3. Interface/joint graph พร้อม DOF ที่อนุญาต
4. Feature DAG ต่อ part พร้อม material/process declaration
5. เส้นทาง load, energy, motion, fluid, thermal และ control
6. Symmetry เป็น gene ทางเลือก ไม่ใช่ prior รูปรถที่บังคับ

### Topology operation

เพิ่ม/ลบ part, แยก/รวม part, เพิ่ม/ลบ branch, reroute typed path, เปลี่ยน solid family, เพิ่ม/ลบ rib หรือ shell, เปลี่ยน section family, เพิ่ม/ลบ interface และเปลี่ยน joint type ภายในกฎ functional domain

### เกณฑ์สำเร็จ

Generator ต้องสร้าง genome valid ที่มีจำนวน part และ typed graph non-isomorphic แตกต่างกัน ซึ่งตัวแปร scalar ห้าค่าเดิมเข้าถึงไม่ได้ Functional terminal ทุกตัวต้อง trace ได้ มิฉะนั้นปฏิเสธก่อน CAD งานนี้พิสูจน์ topology representation แต่ยังไม่พิสูจน์ว่า CAD/physics execute genome ทุกแบบได้

## Work 094 — Reproducible Topology Mutation and Recombination

### วัตถุประสงค์

ให้ agent สำรวจ Work 093 โดยไม่ใช้ geometry candidate ที่เขียนด้วยมือ

### กลุ่ม Mutation

- parametric perturbation
- feature insertion/removal/reordering เมื่อ dependency อนุญาต
- branch growth/pruning
- part split/fusion
- interface creation/deletion/rerouting
- material/process mutation ภายใน evidence class
- graph crossover ทางเลือกที่จำกัดบน typed boundary ที่เข้ากันได้

ทุก proposal ต้องบันทึก parent identity, random seed/checkpoint, operator ที่เลือก, proposal probability, bounded retry และ genotype identity สุดท้าย Initializer แบบ primitive, skeletal, shell, rotary, branching และ hybrid ต้องได้รับ opportunity budget ที่ประกาศและสมดุล

### เกณฑ์สำเร็จ

เมื่อ parent, seed และ operator budget เดิม ลำดับ proposal ต้อง replay exact Negative control ต้องปฏิเสธ cycle, mandatory terminal ที่หลุด, joint domain ที่เป็นไปไม่ได้, material/process ที่เข้ากันไม่ได้ และ mutation หลังเห็นผล อย่างน้อยสี่ topology-changing operator family ต้องสร้าง genome ที่ execute ได้ใน bounded pilot

## Work 095 — Constructive Validity and Manufacturing Gate

### วัตถุประสงค์

ป้องกันไม่ให้ geometry ซับซ้อนกลายเป็น exploit หรือกระแส CAD failure ที่ใช้ไม่ได้

### กติกา

- เลือก grammar-preserving construction ก่อน post-hoc repair
- Deterministic repair ทำได้เฉพาะก่อน evaluation ภายในรายการ operation/budget ที่ preregister และต้องเข้า genotype/provenance identity
- ห้ามเปลี่ยน geometry หลังเห็น performance, collision, stress หรือ failure
- บันทึก proposal ที่ถูกปฏิเสธหรือซ่อมทุกตัวพร้อมสาเหตุ exact
- ใช้ข้อจำกัดเฉพาะกระบวนการ: minimum wall/ligament/radius, tool access, overhang/support, enclosed void, tolerance, joining access และ material/process compatibility

### เกณฑ์สำเร็จ

Control ที่ฉีด self-intersection, sliver, zero thickness, inaccessible feature, unsupported wall และ hidden repair ต้อง fail อย่างเห็นได้ชัด ต้องรายงาน validity yield และสาเหตุ reject แยกตาม representation family เพื่อไม่ให้ primitive ได้เปรียบแบบมองไม่เห็น

## Work 096 — Semantic Geometry Witness V3

### วัตถุประสงค์

กู้ semantic ที่ฟิสิกส์ต้องใช้จาก STEP geometry แบบโค้งและแตกแขนงโดยไม่พึ่ง face number ที่ไม่เสถียร

### การวัดที่บังคับ

- จำนวน solid/shell/body, volume, mass, centre of mass, full inertia
- oriented bounds, curvature class/spectrum, thickness field, minimum radius, section property ตาม path
- datum axis/plane/point และ interface surface จาก signature
- บริเวณ load/support/contact/thermal/fluid
- path length, bend radius, การเปลี่ยน cross-section, clearance, interference และ swept motion envelope
- semantic correspondence ระหว่าง declaration กับ geometry ที่ตรวจอิสระ

### เกณฑ์สำเร็จ

FreeCAD ต้องกู้ semantic บังคับทั้งหมดของ Work 092 corpus ได้อย่างอิสระหลัง export STEP การสลับ face order และ export change ที่ไม่มีผลต้องรักษา semantic match ส่วน interface ที่เปลี่ยนหรือ region ที่หายต้อง fail closed งานนี้พิสูจน์ inspection ไม่ใช่ structural validity

## Work 097 — Generalized Meshing, Contact, and Failure Evaluation

### วัตถุประสงค์

ทำให้ geometry ที่ไม่คุ้นเคยประเมินได้ แทนการเลือก primitive เพียงเพราะ solver เข้าใจ

### ความสามารถ

- เลือก model solid/shell/beam อัตโนมัติพร้อมเหตุผลที่ประกาศ
- Mesh ที่คำนึงถึง curvature, thickness, interface และ stress gradient
- บริเวณ load/support/contact arbitrary ที่เลือกด้วย signature
- bonded, sliding, bearing, preload และ friction/contact law ที่ประกาศ
- bending, torsion, buckling, yield/plasticity, fracture-domain, fatigue, thermal stress และ solver-invalid state
- Mesh convergence ตาม geometry family พร้อม equilibrium/energy residual อิสระ
- ส่ง failure กลับ typed connection graph

### Benchmark และเกณฑ์สำเร็จ

ใช้ analytical/cross-solver benchmark สำหรับ curved cantilever, tapered beam, hollow shell, branched joint, lattice/rib junction, bearing seat และ contact pair Benchmark ที่ admit ทุกตัวต้องผ่าน convergence/residual gate และ divergence ต้องเป็น output ผลผ่านไม่ validate arbitrary topology ในอนาคตหรือวัสดุจริง

## Work 098 — Multi-Fidelity Compute and Fairness Protocol

### วัตถุประสงค์

ป้องกันไม่ให้ box ได้รางวัลเพียงเพราะสร้าง mesh และ solve ถูกกว่า

### บันได Evaluation

1. ตรวจ grammar/connectivity/identity
2. ตรวจ B-rep validity และ coarse collision/manufacturing
3. analytical bound จาก geometry
4. coarse mesh/contact/thermal evaluation
5. refined convergence สำหรับ survivor
6. holdout และ independent higher-fidelity evaluation

Budget ต้องรายงานจำนวน attempt, CAD-kernel call, mesh element, nonlinear iteration, solver time และ total compute แต่ละ representation family ต้องได้ matched opportunity หรือ cost-normalized budget ที่ประกาศ ต้อง audit false negative ของ cheap proxy โดย promote stratified sample บางส่วนโดยไม่ดู proxy score

### เกณฑ์สำเร็จ

Primitive และ free-form family ต้องเจอ functional case และ evidence threshold เดียวกัน Protocol ต้องแสดง deterministic promotion, fail-fast และอัตรา proxy false-negative/false-positive ที่วัดได้ Compute ยุติธรรมไม่แปลว่าผลต้องเท่ากัน

## Work 099 — Quality-Diversity Search Agent V1

### วัตถุประสงค์

ค้นหา design ที่ feasible และคุณภาพดีในหลาย niche แทนการยุบไปหารูปทรงง่ายที่สุดเพียงแบบเดียว

### วิธี

สร้าง deterministic MAP-Elites หรือ quality-diversity archive เทียบเท่า Descriptor รวม typed topology, part count, interface graph, curvature spectrum, section variation, load-path branching, mass distribution, motion strategy, heat-rejection strategy และ failure mode ประเมิน objective quality เฉพาะ candidate ที่ผ่าน mandatory gate

เปรียบเทียบ GRID/RANDOM/scalar EVOLUTION/free-form QD ด้วย budget, seed, operator, case และ evaluator identity ที่ตรึงเหมือนกัน Novelty ห้ามชดเชย failure, undeclared energy, missing evidence หรือ numerical invalidity

### เกณฑ์สำเร็จ

QD ต้องเพิ่ม feasible niche coverage หรือ topology diversity เหนือ control ตาม analysis ที่ preregister Candidate สวยแปลกหนึ่งตัว seed โชคดีหนึ่งตัว หรือ diversity ที่เป็นเพียง duplicate เปลี่ยน scale ถือว่าล้มเหลว

## Work 100 — Isolated Functional Subsystem Discovery Trials

### วัตถุประสงค์

ให้ geometry แปลกมีพื้นที่ที่จัดการได้เพื่อถือกำเนิดก่อน whole-vehicle integration

### Trial domain

- ground interaction และ vertical compliance
- torque transfer และ speed conversion
- branching load bridge หรือ structural mount
- heat collection/rejection และ fluid routing
- energy containment/interface support

แต่ละ trial ตรึงเฉพาะ external functional terminal, load, envelope, energy/resource, evidence class, evaluator และ compute budget—not รูปทรงหรือการจัดวาง component ที่มนุษย์รู้จัก ใช้ training, holdout, mirror, disconnected-path, weakened-material, blocked-motion และ replay control

### เกณฑ์สำเร็จ

ต้องมี non-primitive, non-isomorphic candidate อย่างน้อยหนึ่งตัวรอดจาก CAD/FreeCAD identity, manufacturing, motion/clearance, converged physics, failure control และ exact replay ยังไม่จำเป็นต้องชนะ optimized baseline เพราะการรอดคือหลักฐานแรกของชิ้นส่วนทำงานที่ไม่คุ้นเคยอย่างน่าเชื่อถือ การอ้าง performance ยังต้องเปรียบเทียบ fair optimized baseline และ holdout

## Work 101 — Free-Topology Integration and Evidence Promotion

### วัตถุประสงค์

Integrate subsystem genome ที่รอดโดยไม่ย้อนกลับไปใช้ rectangular frame ที่บังคับ แล้วตัดสินว่ามี complete candidate ใดสมควรเข้าสู่ whole-vehicle Level-0 research หรือไม่

### Gate ที่บังคับ

- part/interface ทุกตัวมี exact STEP/FCStd geometry
- ไม่มี forbidden interference ตลอด motion/thermal/service envelope
- มีเส้นทาง force, torque, energy, control, fluid และ heat แบบ causal
- mass/COM/inertia มาจาก geometry พร้อม structural/thermal ledger ครบ
- integrated mesh/contact convergence และ failure propagation ถึง DNF
- static, acceleration, braking, cornering, combined, bump, torque, duration, single-failure, mirror และ replay case
- เปรียบเทียบ fixed-topology/free-topology baseline ที่ optimize ด้วย budget เท่ากัน
- holdout และ independent higher-fidelity review ก่อนอ้าง discovery

### เกณฑ์สำเร็จ

เฉพาะ candidate ที่ผ่าน admission gate ทุกตัวจึงเข้า whole-vehicle Level 0 ได้ Novel candidate จะเป็น discovery candidate เมื่อชนะ fair optimized baseline และรอด higher-fidelity challenge แล้วเท่านั้น และยังไม่ physically validated จนกว่าจะมี material/process evidence จริงและ physical testing

## สถาปัตยกรรม Artifact

Implementation ในอนาคตควรแยก identity สี่ชนิด:

1. `genotype_sha256`: typed topology และ feature declaration
2. `geometry_sha256`: canonical STEP/FCStd witness
3. `evaluation_sha256`: evaluator, case, material, mesh, solver และ output ที่ตรึง
4. `lineage_sha256`: parent, seed/checkpoint, mutation trace, repair trace และ archive insertion

Identity ที่เกี่ยวข้องไม่ตรงกันต้อง fail closed Cache ใช้ซ้ำได้เฉพาะเมื่อ identity ที่เกี่ยวข้องทั้งสี่ตรง

## กฎการตัดสิน

- โค้งแต่ topology เดิม: **shape variation** ไม่ใช่ topology discovery
- Graph ต่างแต่ functional path ขาด: **invalid proposal** ไม่ใช่ novelty
- Valid และแปลกแต่มีเพียง analytical evaluation: **promising candidate** ยังไม่ admitted
- ผ่าน converged component physics: **subsystem survivor** ยังไม่ใช่ทั้งคัน
- ผ่าน integrated Level 0: **whole-candidate research admission** ไม่ใช่ physical validation
- ชนะ fair baseline และรอด independent higher fidelity: **discovery candidate** โดยยังจำกัดตาม evidence class

## ความเสี่ยงหลักและการลดความเสี่ยง

| ความเสี่ยง | การลดความเสี่ยงที่บังคับ |
|---|---|
| เพิ่มผิวโค้งแต่ search ยังเปลี่ยนเพียง scale | Work 093–094 ต้อง mutate typed topology และ feature DAG |
| Novelty reward สร้างประติมากรรมที่ใช้ไม่ได้ | Mandatory functional gate ต้องมาก่อน quality/novelty ranking |
| Free-form CAD fail มากกว่าและแพ้อย่างไม่ยุติธรรม | บัญชี rejection Work 095 และ matched compute Work 098 |
| Hidden repair รั่วข้อมูลผลลัพธ์ | Repair ก่อน evaluation ตาม preregistration เท่านั้น และ repair trace เข้า identity |
| Semantic face reference พังหลัง STEP | Signature/datum และการกู้อิสระใน Work 096 |
| Solver รองรับเฉพาะ primitive ง่าย | Benchmark coverage ของ Work 097 ก่อน discovery trial |
| Exotic candidate หนึ่งตัวถูกอ้างเกินจริง | หลาย seed, optimized baseline, holdout, higher fidelity และ evidence boundary |
| Complexity ระเบิด | จำกัด graph/feature budget และขยายหลัง validity/solver audit เท่านั้น |

## จังหวะดำเนินงานที่แนะนำ

ทำครั้งละสอง Work และ commit แยกแต่ละงาน: `090–091`, `092–093`, `094–095`, `096–097`, `098–099` แล้ว `100–101` ห้ามเริ่ม Work 100 จน Work 097 ประเมิน non-primitive benchmark geometry ได้ และห้ามเริ่ม whole-vehicle integration จนมี subsystem survivor
