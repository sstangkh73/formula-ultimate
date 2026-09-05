# Roadmap V1 แบบสร้างก่อน แล้วใช้ฟิสิกส์ประเมิน

ต้นฉบับภาษาอังกฤษ: `GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.md`

## ข้อตัดสินใจ

Formula Ultimate ไม่ควรใช้รูปทรงรถที่รู้จัก, component family ที่ตรึง, heuristic การผลิต หรือขอบเขต solver ปัจจุบันเป็นตัวตัดสินว่าอะไรมีสิทธิ์ถือกำเนิด ระบบค้นหาควรสร้าง candidate ที่ไม่คุ้นเคยแต่มีค่าจำกัดและตามที่มาได้ก่อน แล้วใช้ฟิสิกส์ที่ derive จาก geometry ตอบว่ามันทำอะไร แรงและพลังงานไหลทางไหน พังอย่างไร รับได้เท่าไร และดีกว่าหรือไม่ภายใต้งานที่ประกาศ

ฟิสิกส์ยังเป็นข้อบังคับ แต่เปลี่ยนบทบาทจาก **การอนุญาตรูปทรง** เป็น **การวัด อธิบาย เปรียบเทียบ และให้หลักฐานเพื่อ promotion** Candidate ที่พังทางฟิสิกส์เป็นผลวัดที่ถูกต้อง Candidate ที่แก้เชิงตัวเลขไม่ได้ไม่ใช่ physical failure และ candidate ที่ยังผลิตด้วยกระบวนการเป้าหมายไม่ได้อาจเป็น stepping stone ทางวิจัย แต่ห้าม promote เป็นแบบที่สร้างได้

เอกสารนี้บันทึกสภาพก่อนหน้าและสถาปัตยกรรมที่เสนอ ยังไม่ได้อ้างว่าสถาปัตยกรรมใหม่ถูก implement แล้ว

## 1. สภาพก่อนหน้า: repository ทำอะไรได้จริง

| ชั้น | สภาพที่มีหลักฐาน | ผลตามมา |
| --- | --- | --- |
| Whole-vehicle search Work 050/090 | ตัวแปร scale จำกัด 5 ค่าแก้ assembly รูปทรงพื้นฐานที่ตายตัว Census 288 candidates วัด primitive fraction `1.0`, topology signature 1 แบบ และ functional-path signature 1 แบบ | มีมิติหลายชุด แต่ยังไม่มีการค้นหา architecture หรือ functional morphology |
| Wire grammar Work 091 | Profiles ที่ประกาศ 12 แบบทดสอบ polygon, arc, conic, Bézier, B-spline, hole, trim, offset และ transform | สร้างเส้นโค้งได้ แต่ control points และ profiles เป็น test corpus ที่ตรึง ไม่ใช่ genes ที่วิวัฒน์ได้ |
| Solid grammar Work 092 | Candidates ที่เขียนด้วยมือ 10 แบบทดสอบ sweep, loft, shell, ribs, booleans, fillets, patterns และ multi-solid | CAD ที่ไม่ใช่ primitive ทำได้ แต่ระบบค้นหาไม่ได้ประดิษฐ์ feature graph หรือค่าพารามิเตอร์ใหม่ |
| Topology genome Work 093 | Typed graphs 6 แบบแทนโครงสร้าง part/interface/path ต่างกัน จำกัดสูงสุด 8 parts และแต่ละ part อ้าง source-solid identity จาก Work 092 | แทน graph diversity ได้ แต่ geometry ยังเลือกจากคลัง |
| Mutation Work 094 | Operators ตายตัว 8 แบบทำกับ typed graphs การเปลี่ยน solid เลือก source candidate อื่นที่ตรึง ส่วน feature insertion เพิ่มเพียง `transform` ที่ไม่มี parameter ผลระบุ `cad_executed: false` และปิด crossover | Mutation ที่รับได้เป็นข้อเสนอ graph ไม่ใช่ physical geometry ที่สร้างใหม่ |
| Constructive/manufacturing gate Work 095 | Gate ก่อน performance สาธิตบัญชีการ reject บน synthetic scalar fixtures ที่จับคู่กัน โดยไม่ได้วัด STEP ที่อ้างถึง | พฤติกรรม gate ถูกทดสอบ แต่ถ้าใช้เป็น early search filter ทันทีจะฝังสมมติฐานกระบวนการก่อนรู้คุณค่าการทำงาน |
| Semantic witness Work 096 | FreeCAD วัด STEP ตายตัว 10 แบบและกำหนด selector support/load/contact/thermal/fluid ที่ตรึง | มี geometry measurement แต่ semantic boundary regions ยังไม่ได้สืบจาก functional genotype ของ candidate อิสระ |
| Structural benchmark Work 097 | Source candidates 7 ตัวถูกผูกกับ response models 7 แบบและ expected beam/shell/solid/contact ที่ตรึง | Reduced-order verification ทำงานกับ adapters เหล่านั้น ไม่ใช่ unseen candidate และ baseline state ที่ไม่ตรงจะ raise แทนการเป็น search outcome ปกติ |

หลักฐาน: [ผล Work 090](../work_logs/2026-09-04_090_search-space-bias-diversity-contract-result.th.md), [ผล Work 094](../work_logs/2026-09-04_094_reproducible-topology-mutation-recombination-result.th.md), [ผล Work 095](../work_logs/2026-09-04_095_constructive-validity-manufacturing-gate-result.th.md), [ผล Work 097](../work_logs/2026-09-05_097_generalized-meshing-contact-failure-evaluation-result.th.md) และ [การตรวจช่องว่างซิม Work 102](LITERATURE_AND_SIMULATOR_GAP_REVIEW_2026-09-05.th.md) ที่เป็นอิสระ

วงจรเหตุผลกลางที่ยังขาดคือ:

```text
evolvable morphology parameters
  -> executable new geometry
  -> geometry-derived boundary conditions and fields
  -> measured outcome returned to search
  -> next morphology proposal
```

ยังไม่มี runner ปัจจุบันที่เชื่อมทั้ง 5 ขั้น Work 094 จบก่อน CAD; Work 095 เป็น synthetic fixture; Work 097 เริ่มจากหลักฐาน Work 096 ที่ตรึง

## 2. ต้นเหตุ ไม่ใช่อาการ

ชิ้นส่วนที่เหลี่ยมหรือดูคุ้นเคยเกิดจากปัญหา representation เป็นหลัก ไม่ใช่หลักฐานว่ากฎฟิสิกส์ชอบกล่อง

1. Active search เดิมเปลี่ยนเพียงมิติของ primitive ที่รู้จักใน [`whole_vehicle_search.py`](../../src/formula_ultimate/experiments/whole_vehicle_search.py)
2. ความสามารถ free-form ใหม่เป็น corpus ใน JSON ไม่ใช่ distribution ของ generator ที่ agent เรียนรู้หรือ mutate
3. [`topology_mutation.py`](../../src/formula_ultimate/search/topology_mutation.py) mutate โครงสร้าง graph แต่ยังถือ source-solid IDs โดยไม่ mutate section control points, path fields, wall fields, voids, branch radii หรือ material distribution
4. [`generalized_geometry_benchmarks.py`](../../src/formula_ultimate/structural/generalized_geometry_benchmarks.py) เลือกฟิสิกส์ด้วย case identity ที่ตรึงและคาดผล intact ที่ตรึง จึงเป็น benchmark ไม่ใช่ search evaluator
5. Semantic selector ปัจจุบันเลือก extreme ทางเรขาคณิตและหน้าที่ใหญ่ที่สุด กฎเหล่านี้อาจระบุหน้าที่ผิดบนกลไกที่ไม่คุ้นเคย

การเพิ่ม template โค้งให้มากขึ้นจะเพิ่มความหลากหลายของรูปลักษณ์ แต่ยังคงกรงเดิม การแก้ที่ต้องการคือทำให้ morphology และ functional topology เป็น executable genes ไม่ใช่เพิ่มรายการรูปทรงที่มีชื่อ

## 3. การจัดประเภท constraint ใหม่

Constraint ทุกตัวต้องระบุว่าทำงานเมื่อใดและสร้างสถานะอะไร

| Constraint | วิธีใหม่ | เหตุผล |
| --- | --- | --- |
| ค่าตัวเลข finite, SI units, ขอบเขต memory/time/evaluations | Hard ก่อน execute | จำเป็นต่อ computation ที่นิยามและทำซ้ำได้ |
| Seed, genotype, operator trace, code/tool identities | Hard ก่อน execute | จำเป็นต่อ exact replay และการเปรียบเทียบยุติธรรม |
| ห้าม undeclared energy/source, hidden repair และ result leakage | Hard ตลอดทาง | ป้องกัน simulator exploitation และการเปรียบเทียบวิทยาศาสตร์ที่ผิด |
| External task terminals และ environment | Hard task contract | นิยามงานโดยไม่กำหนดรูปทรงภายใน |
| จำนวนล้อแบบเดิม, chassis layout, symmetry, named part family | ไม่เป็น constraint เว้นแต่งานกำหนดโดยตรง | เป็น historical priors ไม่ใช่ฟิสิกส์สากล |
| ข้อกำหนด B-rep ต้องเป็น single solid | แทนด้วยสถานะตาม representation | Shell, lattice, multi-body mechanism และ implicit field อาจถูกต้อง ต้องการเพียงให้ representation ที่ประกาศ instantiate ได้ ไม่ใช่ทุกแบบต้องเป็น solid เดียว |
| Minimum wall/radius/feature, tool access, overhang, enclosed void | วัดหลังมี geometry; hard เฉพาะ promotion route การผลิตที่ประกาศ | ขึ้นกับกระบวนการและอาจลบ stepping stone ที่มีคุณค่าก่อนวัดหน้าที่ |
| Stress, displacement, buckling, fracture, fatigue, contact, heat, flow | Physics outputs | คืนค่า fields, uncertainty, ตำแหน่งพัง และ thresholds โดยไม่ห้าม candidate ถือกำเนิด |
| Solver convergence และ meshability | Numerical evidence state | `numerically_unresolved` ต่างจาก `physically_failed` |
| Safety, buildability, calibrated material evidence, holdout validation | Hard promotion requirements | จำเป็นก่อนอ้างสร้าง/ใช้งาน ไม่ใช่ก่อนสำรวจ |
| Novelty | Archive/selection objective เท่านั้น | Novelty ห้ามชดเชย energy violation, physical failure หรือหลักฐานหาย |

## 4. วงจรชีวิต candidate เป้าหมาย

### Stage 0 — ตรึงโจทย์ ไม่ตรึงคำตอบ

ประกาศเพียง external functional terminals, ประวัติ load/energy/environment, envelope หรือ interaction domain ที่ใช้ได้, ทรัพยากรจำกัด, material evidence classes ที่มี, evaluation budget และ success metrics Trial ground interaction อาจกำหนด ground contact กับ body load terminals แต่ต้องไม่กำหนดล้อ จำนวนล้อ axle layout หรือ suspension geometry ที่รู้จัก

### Stage 1 — เสนอ evolvable causal genotype

Genotype มี geometry/assembly program ความยาวแปรผัน, typed functional terminals, สมมติฐาน material/process, controller genes เมื่อมี active motion และ provenance อ้าง generic operators ได้แต่ไม่บังคับ source candidate จาก frozen Work 092 catalog

### Stage 2 — สร้าง geometry

Execute genotype เป็น representation ที่ประกาศหนึ่งหรือหลายแบบ เช่น B-rep solids/shells, beam/shell networks, lattice/field structures และอนาคต implicit/voxel fields บันทึก kernel call และ failure ทุกครั้ง ห้าม hidden healing หากสร้างไม่สำเร็จให้เป็น `representation_invalid` ใช้งบตามประกาศและยังอยู่ใน ledger

### Stage 3 — วัด geometry โดยไม่ตัดสิน performance

กู้ volume, area, mass จาก material distribution, centre of mass, inertia, bounds, connected components, thickness samples, curvature, section fields, clearances, intersections และ semantic terminal geometry ค่า measurement และ sampling uncertainty เป็น output ห้ามสรุปว่าผนังบางพังทางฟิสิกส์ก่อนใส่ load

### Stage 4 — ผูกหน้าที่กับ geometry

Support, load, contact, fluid, thermal, electrical และ control regions ต้องสืบจาก typed terminal ancestry ใน genotype และรอดการแลกเปลี่ยน geometry ด้วย signatures กฎเช่น largest face เป็นได้เพียง fallback hypothesis ไม่ใช่ความจริงเงียบ ๆ หากผูกไม่ได้หรือกำกวมให้เป็น `boundary_unresolved`

### Stage 5 — ทดลองฟิสิกส์

รัน multi-fidelity ladder ที่ประกาศกับ representation-valid candidate ทุกตัวภายใน budget เริ่มจาก conservation และ analytical bounds ตามด้วย geometry-derived mesh/field solutions, contact/motion/thermal/flow solves และ coupled evaluation เมื่อเกี่ยวข้อง การเลือก model ต้องพึ่ง geometry ที่วัดกับ error estimate ไม่ใช่ชื่อ candidate

### Stage 6 — คืน outcome ไม่ใช่หายไปแบบ binary

บันทึก force, reaction, moment, energy transfer, displacement/stress/temperature/flow fields, contact states, eigenmodes, margins, failure initiation, failed paths, residual histories, mesh convergence, uncertainty, compute และ limitations Evaluator คืนหนึ่งใน state classes ด้านล่าง ไม่ raise เพียงเพราะ candidate อ่อน

### Stage 7 — ประเมิน manufacturing แยกต่างหาก

ประเมินทุก process ที่ประกาศว่า compatible เท่าที่งบพอ คืนผล wall/access/support/tolerance/cost แยกตาม process แบบหนึ่งอาจ machining ไม่ได้แต่ additive ได้หรืออาจต้องใช้ process อนาคตที่ยังไม่มี model Manufacturing status ห้ามเขียนทับ physics status

### Stage 8 — Archive และเลือก

ใช้ quality-diversity selection บน descriptor เชิงหน้าที่และเหตุผล รักษา archive แยกสำหรับ feasible, physically failed, manufacturing-incompatible และ numerically unresolved สุ่มข้าม archive เพื่อให้กลไกแปลกที่เกือบ feasible เป็น stepping stone แทนที่จะหาย

### Stage 9 — Promote ด้วยหลักฐานที่แรงขึ้น

เฉพาะ promotion เท่านั้นที่บังคับผ่าน physical, numerical, manufacturing, safety, holdout, replay และ independent-validation gates ทั้งหมด Candidate ที่ promote เรียก survivor ได้เฉพาะ fidelity ที่ผ่านจริง

## 5. State taxonomy ที่ต้องมี

| State | ความหมาย | การใช้ใน search | Promotion |
| --- | --- | --- | --- |
| `generated` | Serialize genotype พร้อม provenance ครบ | รอ execute | ไม่ได้ |
| `representation_invalid` | สร้าง representation ที่ประกาศไม่ได้ | เก็บสาเหตุ อาจใช้ชี้ mutation | ไม่ได้ |
| `geometry_measured` | Geometry มีจริงและวัดรายการบังคับแล้ว | ไปต่อ | ไม่ได้ |
| `boundary_unresolved` | การผูก function-to-geometry terminal หายหรือกำกวม | เก็บแยก ทดลอง binding refinement ตามประกาศ | ไม่ได้ |
| `numerically_unresolved` | Mesh/solver/error gates ให้ผลน่าเชื่อถือไม่ได้ภายใน budget | เก็บแยก ห้ามเรียก physical failure | ไม่ได้ |
| `physically_failed` | Solve ที่ converge/ผ่านหลักฐานข้าม physical limit ที่ประกาศ | เก็บ fields, margins และ failure path เป็นข้อมูลวิวัฒนาการ | ไม่ได้ |
| `physically_feasible` | ผ่านเฉพาะ physical fidelity ปัจจุบัน | เข้า manufacturing และ fidelity ต่อไปได้ | ยังไม่อัตโนมัติ |
| `manufacturing_incompatible` | ไม่มี process ที่ทดสอบผ่าน production target | เก็บเป็น research stepping stone | ไม่ได้ |
| `candidate_survivor` | ผ่าน physics, process, holdout และ replay gates ของ trial ที่ preregister | เข้า subsystem comparison ได้ | เฉพาะ scope ของ trial |
| `promotion_ready` | ผ่าน independent higher-fidelity และ safety evidence ตามการใช้งาน | เข้าการ integrate ภายหลังได้ | ได้เฉพาะ scope ที่ประกาศ |

สถานะเหล่านี้ต้องแยกกันในข้อมูลและรายงาน ห้ามรวม `invalid`, `failed` และ `not ready` เป็น Boolean เดียว

## 6. การออกแบบ genotype และ operator ใหม่

### Geometry genes

- Variable-length feature DAGs ที่มี executable parameters
- Curve/surface control points, knots, degree, continuity และ local refinement
- Paths, sections, taper/twist fields และ wall-thickness fields ตาม normalized material coordinates
- Branch/merge/split พร้อม junction blending ที่กำหนดด้วย genes แทน named family
- Constructive void และ material-add/remove regions
- Beam/shell/lattice graphs พร้อม continuous node positions และ section fields
- Optional implicit scalar fields และ material occupancy หลังมี independent extractor
- Multi-body และ moving-pair declarations
- Spatially varying material hypotheses ภายใน material evidence classes ที่ประกาศ

### Functional genes

- External terminal identity และ domain
- Source/sink/bidirectional role
- Allowed motion และ contact hypothesis
- Load/energy/fluid/thermal/control path ancestry
- Sensor/actuator/controller parameters เมื่อพฤติกรรมขึ้นกับ control
- Failure propagation edges ที่ derive จาก candidate graph ไม่เติมด้วยมือหลังเห็นผล

### Mutation/recombination operators

- Perturb, insert, delete, split, merge, rewire และ duplicate control points หรือ field regions
- Grow/prune branches โดยไม่บังคับ part ใหม่ทุกชิ้นให้ถือทุก domain
- เปลี่ยน representation เฉพาะที่พร้อมรักษา terminal mapping
- เพิ่ม/ลด voids, ribs, shells, lattices, compliant regions และ moving pairs โดยไม่เลือก named vehicle part
- เปลี่ยนสมมติฐาน material/process เฉพาะที่โดยไม่เลือก manufacturing winner ล่วงหน้า
- Recombine typed cut boundaries หลังพิสูจน์ compatibility
- Co-mutate geometry กับ controller genes สำหรับ active mechanisms

ทุก operator ต้องสร้าง executable parameter trace Morphology operator ที่เปลี่ยนเพียง ID, label หรือ rigid transform ไม่นับเป็น geometry ใหม่

## 7. ฟิสิกส์ในฐานะผู้สังเกต

Search-facing evaluator ต้องรับ unseen geometry record และคืนหลักฐานโดยไม่ต้องมี case name ใน frozen list

1. เลือก analysis representations จาก geometry/error criteria อาจทดลองหลาย model และถือความไม่ตรงกันเป็นหลักฐาน
2. สร้าง mesh จาก candidate geometry จริง เก็บ node/element sets ที่ผูก terminal signatures
3. ใส่ loads และ constraints จาก terminal ancestry
4. กู้ reactions จาก solve อย่างอิสระ ห้ามสร้าง residual เป็นศูนย์ด้วยการบวก load กับค่าติดลบที่ใส่เอง
5. เก็บ displacement, stress/strain, contact traction/penetration, temperature/flux, flow/pressure และ state histories เมื่อเกี่ยวข้อง
6. ผล structural ที่จะ promote ต้องมี refinement อย่างน้อย 3 ระดับตามที่ประกาศ พร้อมบันทึก non-monotonicity และ solver failures
7. แยก model-form disagreement, discretization error, material uncertainty และ numerical failure
8. คืน continuous margins และ localized failure evidence แม้ candidate พัง

ฟิสิกส์ตัดสินว่า candidate รอดงานที่ประกาศหรือไม่ แต่ไม่ตัดสินว่ารูปทรงใดมีสิทธิ์ถูกเสนอ

## 8. Quality-diversity และการเก็บ stepping stone

Archive ควร index สิ่งที่ candidate ทำเชิงเหตุผล ไม่ใช่ดูเพียงว่าโค้งแค่ไหน Descriptor อาจรวม typed topology, terminal-to-terminal path structure, branch/cycle rank, deformation mode, load-path redundancy, motion class, energy conversion path, heat-rejection route, mass/inertia distribution, section-field variation, material occupancy และ failure mode/location

ในแต่ละ niche เก็บอย่างน้อย:

- คุณภาพ physically feasible ที่ดีที่สุด
- Physical margin ที่ใกล้ feasibility ที่สุด
- คุณภาพ manufacturing-compatible ที่ดีที่สุด
- Unresolved candidate ที่คุ้มค่า escalation มากที่สุด
- Novelty และ ancestry โดยไม่ให้ novelty ลบ failure

Infeasible candidate อาจมีสิทธิ์ reproduce ภายใต้ stepping-stone policy ที่จำกัด เมื่อปรับ continuous margin, เปิด functional niche ใหม่ หรือแก้ path ที่เคยหาย สิทธิ์ reproduce และ compute ต้องชัดเพื่อไม่ให้ infeasible archive ใช้งบเงียบ ๆ

## 9. Multi-fidelity และ compute ที่ยุติธรรม

Primitive geometry มัก mesh เร็วกว่า free-form, multi-body หรือ contact-rich geometry จำนวน candidate เท่ากันจึงยังไม่ยุติธรรม ต้องบันทึกและควบคุม attempted proposals, CAD-kernel calls, meshing attempts, elements/DOF, nonlinear iterations, wall time, memory และ fidelity promotions

ใช้ staged budget:

1. Representation/measurement ราคาถูกสำหรับ generated candidates ทั้งหมด
2. Physics proxy สำหรับ representation-valid candidates ทั้งหมด
3. Stratified promotion ที่ไม่อิง proxy score เพื่อวัด false negatives
4. Score-based และ novelty-based promotion ภายใต้งบแยกที่รายงาน
5. Refined/independent solves สำหรับ finalists

Cheap proxy ใช้จัดคิว compute ได้แต่ห้ามนิยาม physical truth ต้องวัด proxy false-negative และ false-positive rate บน promoted samples

## 10. การทำ Works 098–101 แบบแก้ลำดับ

### Work 098 — Generation-First State and Fairness Protocol

- แทน linear pass/reject ladder ด้วย state taxonomy ในเอกสารนี้
- กำหนดว่า check ใดเป็น pre-execution invariant, measured outcome และ promotion gate
- ระบุ budget accounting สำหรับ CAD, meshing, solver, unresolved และ stepping-stone paths
- เพิ่ม ablation เปรียบเทียบ pre-manufacturing rejection กับ evaluate-first manufacturing annotation
- รักษาเป้าหมาย multi-fidelity/fairness เดิม พร้อมป้องกัน cheap proxy ลบ unfamiliar candidates ทั้งหมด

เงื่อนไขจบ: Protocol ที่ตรึง replay mixed ledger ซึ่งมีทุก state class ได้ โดยไม่รวมสถานะและไม่มี post-result hidden repair

### Work 099 — Executable Morphology and Quality-Diversity Agent V1

- ขยาย genome ด้วย numerical geometry parameters และ terminal ancestry
- Implement morphology-changing CAD operators ไม่ใช่ library replacement เท่านั้น
- เชื่อม proposal ไป CAD execution และ geometry measurement
- Implement feasible/infeasible/unresolved quality-diversity archives
- พิสูจน์ว่า morphology operator เปลี่ยน executable geometry hash และ measured fields พร้อมรักษา replay

เงื่อนไขจบ: หลาย seeds สร้าง geometry identities ที่ไม่เคยประกาศและ functional graphs แบบ non-isomorphic โดย failure ยังเป็น measured ledger entries งานนี้ยังไม่พิสูจน์ useful physics

### Work 100 — Isolated Functional Discovery Trials

- ตรึงเพียง external terminals, loads/environment, resources, evaluator identities และ budget ของแต่ละ subsystem trial
- รัน generation-first search ด้วย geometry-derived field solvers จริง
- เปรียบเทียบ conventional, random, graph-only, morphology-only และ joint morphology/controller controls
- เก็บ rejected/unresolved archives และ promote stratified samples เพื่อตรวจ proxy bias

เงื่อนไขจบ: Previously undeclared, non-primitive, non-isomorphic candidate อย่างน้อยหนึ่งตัวถึง `candidate_survivor` ภายใต้ converged physics, replay และ manufacturing route ที่ประกาศ ยังไม่จำเป็นต้องชนะ optimized baseline

### Work 101 — Free-Topology Integration and Evidence Promotion

- Integrate เฉพาะ subsystem survivors ผ่าน typed terminals
- ให้ integration failure ไหลกลับเป็น interface/load/control evidence แทนการบังคับ chassis แบบเดิม
- รัน coupled transient, energy, thermal, contact, failure, holdout และ independent higher-fidelity gates
- เปรียบเทียบ optimized fixed-topology baselines อย่างยุติธรรม

เงื่อนไขจบ: Whole candidate ทำงานที่ประกาศจบและผ่าน promotion gates ทั้งหมด โดยยังเป็น simulation evidence จนกว่าจะมี independent physical validation

## 11. การทดลองที่หักล้างได้

| การทดลอง | ตัวแปรต้นและ controls | หลักฐานตาม | สำเร็จ / ล้มเหลว |
| --- | --- | --- | --- |
| Representation freedom | Old five-scalar search, frozen-library topology mutation และ executable morphology mutation; matched seeds/compute | New geometry hashes, topology/path signatures, control-point/field changes, CAD success, duplicate rate | สำเร็จเมื่อมี executable geometry ที่ไม่อยู่ใน source corpus และ causal descriptor diversity ล้มเหลวหาก diversity เป็นเพียง scale, transform, rename หรือ cached-library substitution |
| Gate-order ablation | Pre-performance manufacturing rejection เทียบ evaluate-first annotation; ใช้ proposals/physics budget เดียวกัน | Candidates ที่ถึง physics, functional niche coverage, physical margins, process compatibility ภายหลัง, compute | สำเร็จเมื่อวิธีใหม่กู้ functional stepping stones ที่น่าเชื่อถือโดยไม่เพิ่ม unsupported promotions ล้มเหลวหากได้แต่ invalid/exploitative candidates หรือ compute ไร้ขอบเขต |
| Boundary binding | Fixed geometric selectors เทียบ genotype-terminal ancestry; geometry/load cases เดียวกัน | Region correspondence, reactions, path continuity, ambiguity rate | สำเร็จเมื่อ terminal-derived binding รอด transformations และตรง independent fixtures ล้มเหลวหาก largest/extreme faces เปลี่ยนหน้าที่เงียบ ๆ |
| Physics outcome integrity | Current reduced adapter เทียบ geometry mesh/solver จริงที่ 3 refinements | Fields, recovered reactions, residual histories, convergence, failure location, disagreement | สำเร็จเมื่อมี independent residual/reaction evidence และ refinement disagreement จำกัด ล้มเหลวหาก residual จริงเพราะสร้างสูตร, ไม่มี fields หรือเรียก solver error ว่า physical failure |
| Stepping-stone archive | Feasible-only selection เทียบ bounded feasible/infeasible/unresolved archive | Feasible niche coverage, time to survivor, lineage จาก failed states, compute share | สำเร็จเมื่อมี improvement ที่ preregister ข้าม paired seeds ล้มเหลวหาก unresolved candidates ครอง compute หรือไม่มี survivor ใช้ retained stepping stones |
| Manufacturing timing | Single early process gate เทียบ post-physics multi-process evaluation | Functionally valuable candidates ที่หายก่อนเวลา, process-specific feasibility, final promotion rate | สำเร็จเมื่อ early annotation รักษาทางเลือกที่มีประโยชน์และ final promotion ยังเข้มเท่าเดิม ล้มเหลวหาก buildability claim อ่อนลง |

Thresholds และ statistical tests ต้องถูกตรึงใน Work 098 ก่อนเห็น admitted experiment Candidate สวยแปลกหนึ่งตัวไม่ใช่หลักฐานว่าระบบใหม่ดีกว่า

## 12. เกณฑ์สำเร็จระดับระบบ

สถาปัตยกรรมใหม่ทำงานต่อเมื่อมีหลักฐานครบทุกข้อ:

1. Search child มี executable geometry parameters ที่ไม่อยู่ใน source candidate ใด
2. Proposal, CAD, measurement, boundary binding, physics, outcome, archive และ next proposal ทำงานใน replayable loop เดียว
3. ประเมิน unseen geometry ได้โดยไม่ต้องมี frozen case/candidate ID
4. Physical failure คืน measured margins, fields และ affected paths แทน evaluator exception
5. ความสามารถเชิงตัวเลขไม่พอไม่ถูกเรียกเป็น physical failure
6. Manufacturing incompatibility แยกตาม process และ block promotion โดยไม่ลบ early evidence
7. Physics และ energy constraints เหมือนกันสำหรับ conventional กับ unfamiliar candidates
8. Free-form representations ได้ audited compute opportunity ไม่แพ้อัตโนมัติเพราะแพงกว่า
9. Candidate ผ่าน holdout และ independent higher fidelity ก่อนอ้าง performance/discovery
10. Optimized fixed-topology baselines เป็นตัวเปรียบเทียบ ไม่ใช่คำตอบบังคับ

## 13. ความเสี่ยงและการควบคุม

- **Search explosion:** Variable-length geometry มีมิติสูงมาก ควบคุมด้วย staged budgets, developmental encodings, lineage-aware archives และ multi-fidelity promotion ไม่ใช่ named-shape restriction
- **Kernel fragility:** B-rep operations อาจพังบ่อย เก็บสาเหตุ exact และเพิ่ม alternative representation routes โดยไม่ heal เงียบ
- **Proxy exploitation:** Audit conservation, boundary work, contact energy, mesh dependence และ out-of-distribution promotion samples
- **Unresolved archive โตเกิน:** จำกัด reproduction กับ escalation budget แยกกัน แต่เก็บ metadata เพื่อวิเคราะห์
- **เลื่อน manufacturing ไกลเกิน:** วัดเร็วเมื่อราคาถูก แต่ destructive เฉพาะ promotion stage ที่ประกาศ
- **Novelty theater:** ต้องต่างด้าน function/topology/field และเทียบ fair baseline ไม่ใช่แค่ดูแปลก
- **Physics coverage bias:** เผย unsupported domains และ solver applicability Unsupported physics block promotion แต่ห้ามย้อนกลับไปห้าม genotype language

## 14. สิ่งที่ไม่ทำ

แผนนี้ไม่ตัด conservation, finite resources, race rules, safety, manufacturing, evidence, holdouts หรือ independent validation ไม่สัญญารูปคณิตศาสตร์ไร้ขอบเขต, จำนวน part อนันต์, magic materials, compute ฟรี หรือการรับ solver output ที่ invalid และไม่เรียก simulation survivor ว่าเป็นชิ้นส่วนที่ validate ในโลกจริง

สิ่งที่เปลี่ยนมีขอบเขตแคบแต่สำคัญ: **อนุญาตให้ unfamiliar candidate มีตัวตนเป็น computational object ที่ตามที่มาได้ก่อน แล้วให้ฟิสิกส์ที่วัดจริงตัดสินความหมายและระดับที่มันมีสิทธิ์ถูก promote**
