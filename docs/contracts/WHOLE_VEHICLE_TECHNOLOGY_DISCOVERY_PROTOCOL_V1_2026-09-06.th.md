# Protocol V1 การค้นพบรถทั้งคันและเทคโนโลยี

ต้นฉบับภาษาอังกฤษ: `WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md`

วันที่: 2026-09-06 (Asia/Bangkok)

Protocol ID: `FU-WHOLE-VEHICLE-DISCOVERY-V1-2026-09-06`

Status: Normative design protocol; implementation pending

งานเอกสาร: Work 104; ลำดับ implementation: Works 098–101

## 1. อำนาจอ้างอิง วัตถุประสงค์ และเอกสารเดิมที่เก็บรักษา

Protocol นี้กำกับ implementation ถัดไปของ Works 098–101 โดยแทนที่แนวทางดำเนินงานของเลขงานเหล่านี้ใน [generation-first roadmap](../reports/GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.th.md) รวมถึงข้อกำหนดที่ให้เฉพาะ subsystem survivors จากการทดสอบแยกเข้าสู่การทดลองประกอบใด ๆ ข้อจำกัดนั้นเปลี่ยนเป็นกติกาแยกสำหรับ exploratory integration และ evidence promotion ส่วน work logs และหลักฐานการทดลองเดิมยังเป็นบันทึกประวัติ เอกสารนี้ไม่เปลี่ยนผลย้อนหลัง

ภารกิจคือสร้างรถแข่งสามมิติทั้งคัน และค้นพบรูปทรงชิ้นส่วน กลไก โครงสร้างหลายหน้าที่ และสถาปัตยกรรมระบบที่มีประโยชน์โดยไม่ได้กำหนดคำตอบไว้ล่วงหน้า แบบสามารถเปลี่ยนวิธีแบ่งรถเป็นชิ้นส่วนและวิธีที่ชิ้นส่วนทำงานร่วมกัน ชื่อชิ้นส่วนที่มนุษย์ใช้และรูปแบบรถทั่วไปเป็น baseline ที่เลือกใช้ได้ ไม่ใช่ grammar บังคับในการสร้าง

เก็บ backup ก่อนแก้แบบตรงทุก byte ลงวันที่ 2026-09-06 ไว้ใน [ภาษาอังกฤษ](../reports/backups/2026-09-06_104/GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.md) และ [ภาษาไทย](../reports/backups/2026-09-06_104/GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.th.md) โดยมี SHA-256 ดังนี้:

| ไฟล์ | SHA-256 |
| --- | --- |
| `GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.md` | `686b81df2f98b566775010aabcf225ae32a8552f9ec1818d43b1457070dbc449` |
| `GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.th.md` | `f86ee5472f5afe02f18ac14685dcf755de7a56bd82c5ade960cc2b51d71338c3` |

เนื้อหา backup เป็นสำเนา byte ที่ไม่เปลี่ยนแปลง ลิงก์ relative ภายในยังอ้างบริบท `docs/reports/` เดิม ดูหลักฐานการเปลี่ยนแปลงใน [แผน Work 104](../work_logs/2026-09-06_104_whole-vehicle-discovery-protocol-plan.th.md) และ [ผลลัพธ์](../work_logs/2026-09-06_104_whole-vehicle-discovery-protocol-result.th.md)

## 2. เป้าหมายสูงสุดและขอบเขตการกล่าวอ้าง

สำหรับสภาพแวดล้อมการแข่งขัน `r` ที่ลงทะเบียน ให้ optimize:

```text
d*_r = arg min_d T_race(d, r)
subject to RaceCompleted(d, r) = true
initial primary energy <= registered energy budget
external primary-energy addition during the race = 0
all required physical, numerical, safety, manufacturing and evidence gates pass
```

พลังงานปฐมภูมิสำหรับขับเคลื่อนทั้งหมดต้องอยู่บนรถก่อนแข่ง การนำพลังงานกลับมาใช้ต้องตามกลับไปถึง physical flows ที่ประกาศและมีการสูญเสียที่สังเกตได้ ห้ามนับซ้ำหรือรับพลังงานภายนอกที่ไม่ประกาศ ใช้หน่วย SI และตรึง race/energy profile การเปรียบเทียบที่เป็นกลางต่อเทคโนโลยีต้องคิดมวลตัวพาพลังงาน ภาชนะกักเก็บ อุปกรณ์แปลงพลังงาน การสูญเสีย และผลทางความร้อน การให้งบเป็น joule เท่ากันอย่างเดียวไม่ใช่โมเดลรถที่ครบถ้วน

เวลาการแข่งขันคือเป้าหมายสุดท้าย ส่วน metric งานย่อยและความหลากหลายช่วยรักษาทิศทางค้นหาที่อาจมีประโยชน์ แต่ไม่ยกเว้น feasibility สุดท้าย รูปทรงแปลกไม่ใช่กลไกใหม่โดยตัวมันเอง survivor ใน simulation ไม่ใช่ผลิตภัณฑ์ที่ผ่าน physical validation และแบบที่ไม่มีใน repository นี้ไม่ได้แปลว่าใหม่ในโลกภายนอกโดยอัตโนมัติ

เอกสารนี้กำหนดข้อกำหนดเท่านั้น ไม่ได้ implement generator, arbitrary-geometry solver, vehicle discovery loop, scheduler หรือเทคโนโลยีที่ผ่าน validation การทำ software protocol fixture สำเร็จยืนยันได้เฉพาะพฤติกรรมซอฟต์แวร์

## 3. ตรึงโจทย์ภายนอก ให้คำตอบภายในวิวัฒนาการได้

| สิ่งที่ตรึงสำหรับ admitted comparison | สิ่งที่วิวัฒนาการได้ภายในภาษาและทรัพยากรที่ลงทะเบียน |
| --- | --- |
| สนาม สภาพแวดล้อม ประวัติภารกิจ เกณฑ์จบการแข่งขัน และความปลอดภัย | สถาปัตยกรรม รูปทรง การจัดวาง และมิติรถทั้งคัน |
| โอกาสพลังงานตั้งต้น ขีดจำกัดทรัพยากร และ material evidence classes | การจัดระบบเก็บ/แปลง/นำพลังงานกลับมาใช้ และเส้นทางกายภาพ |
| ข้อกำหนดปฏิสัมพันธ์ภายนอกและการแลกเปลี่ยนกับสิ่งแวดล้อมที่อนุญาต | กลไกปฏิสัมพันธ์กับพื้น จำนวน/ตำแหน่งสัมผัส และการเคลื่อนที่ภายใน |
| Evaluator versions, applicability rules, evidence gates และงบ | จำนวนชิ้นส่วน ขอบเขตชิ้นส่วน interfaces และการกระจายวัสดุ |
| แผนวิเคราะห์ โอกาสของ baseline และ holdout policy | Controller, sensors, actuators และการทำงานร่วมของ geometry/control |

ห้ามบังคับว่าต้องมีล้อ จำนวนเพลา การจัด chassis ความสมมาตร powertrain ที่มีชื่อ หรือ part family ที่มีชื่อ เว้นแต่งานที่ลงทะเบียนนั้นกำหนดโดยชัดแจ้ง ข้อจำกัดดังกล่าวต้องรายงานว่าเป็นขอบเขตการศึกษา ไม่ใช่กฎฟิสิกส์สากล

การทดลองเฉพาะส่วนอาจตรึง external functional terminals เพื่อแยกคำถาม แต่ในระดับรถ การเลือกโจทย์ย่อยและ terminals ภายในอาจวิวัฒนาการผ่าน task proposals ที่มี version การเปลี่ยนการแบ่งระบบภายในไม่อนุญาตให้เปลี่ยนข้อกำหนดการแข่งขัน พลังงาน หรือความปลอดภัยภายนอก โหลดเฉพาะ candidate ต้อง derive ภายใต้กติกาประเมินรถ/สิ่งแวดล้อมเดียวกัน ไม่เลือกด้วยมือเพื่อเอื้อแบบใด

ทุก proposal ที่สร้างต้องมีค่าจำกัด ความซับซ้อน representation ที่มีขอบเขต seed/lineage พารามิเตอร์ที่ execute ได้ และ code/tool identities สิ่งเหล่านี้เป็น execution invariants ส่วนความชอบด้านการผลิตและขอบเขต evaluator ไม่ใช่สิทธิ์กำหนดให้มีได้เฉพาะรูปทรงทั่วไป

## 4. Representation ที่วิวัฒนาการได้และการจัดระบบหลายหน้าที่

Genome เป็นโปรแกรม geometry/assembly ความยาวเปลี่ยนได้ที่ execute ได้ พร้อมสมมติฐานวัสดุ functional terminal ancestry คำประกาศ motion/contact และ controller genes เมื่อเกี่ยวข้อง อาจสร้าง solids, shells, beam/lattice networks, multi-body systems หรือ representation อื่นที่ประกาศรองรับ ห้ามใช้เงื่อนไข single-solid ครอบคลุมทุก representation

Operators ต้องเปลี่ยน numerical geometry เพิ่ม/ลบวัสดุและช่องว่าง grow/prune/rewire เส้นทาง split/merge ชิ้นส่วน และย้ายหรือนิยาม interfaces ภายในใหม่ได้ โดยคงความหมายกายภาพแบบมีชนิด พารามิเตอร์ควบคุมและ geometry อาจวิวัฒนาการร่วมกัน การเปลี่ยน source-catalog identity ชื่อ หรือทำเพียง transform ไม่ใช่หลักฐานรูปทรงใหม่ แต่การจัดวางที่เปลี่ยนอาจมีความหมายเชิงหน้าที่และต้องประเมินเป็นหลักฐานการจัดวาง

บริเวณกายภาพเดียวอาจทำหลายหน้าที่ และหน้าที่เดียวอาจกระจายหลายบริเวณ ห้ามบังคับหนึ่งชิ้นส่วนต่อหนึ่งหน้าที่ หรือให้ทุกชิ้นส่วนรองรับทุก physical domain ตัวอย่างเช่นบริเวณรับแรงที่เสนออาจมีทางระบายความร้อนด้วย แต่ stiffness, heat transfer, pressure loss และ mass ต้องมาจากการวัด ไม่ใช่ค่าที่ genome อ้างเอง ตัวอย่างนี้เป็นสมมติฐานที่อนุญาต ไม่ใช่แบบบังคับหรือการค้นพบที่สาธิตแล้ว

การนับมวล พลังงาน ปริมาตร และความเป็นเจ้าของวัสดุต้องสอดคล้องกันเมื่อคำอธิบายหน้าที่ทับซ้อน บริเวณหลายหน้าที่ไม่ถูกนับเป็นสำเนากายภาพหลายชุด ต้องแยก multi-body contact และการเคลื่อนที่ที่อนุญาตออกจาก overlap ที่ไม่ตั้งใจ ส่วน shell/network validity ใช้กติกาของ representation ที่ประกาศ

## 5. วงจรค้นหาร่วมและสิทธิ์ประกอบสองระดับ

```text
whole-vehicle architecture and controller proposal
  -> task and interface hypotheses derived from vehicle behavior
  -> executable geometry, material and mechanism proposals
  -> measured local evidence and applicability limits
  -> exploratory coupled vehicle evaluation
  -> race/task effects, failure paths and uncertainties
  -> revised architecture, decomposition, geometry and controller
  -> stronger evidence and eventual promotion
```

**Exploratory integration** อาจรวม candidates ที่หลักฐานเฉพาะส่วนยังไม่ครบเพื่อทดสอบผลการทำงานร่วม ต้องมี geometry/model inputs ที่ตามที่มาได้ typed interfaces ประกาศ domains ที่ขาด วิธีประมาณที่ชัดเจน บัญชีทรัพยากร และไม่มี hidden repairs ถ้าหลักฐานที่ขาดทำให้แก้ระบบร่วมอย่างมีความหมายไม่ได้ ให้บันทึก unresolved result ห้ามใส่ coefficient ที่แต่งขึ้น ผลนี้ห้ามอ้าง complete physical feasibility หรือ promotion ข้อผิดกฎที่พิสูจน์แล้วปิดกั้นการกล่าวอ้าง แต่ใช้เป็นข้อมูลสร้าง descendant ใหม่ได้

**Evidence promotion** ต้องผ่านทุก gate ของขอบเขตที่ประกาศ Local verification ยังจำเป็นต่อการตรวจ physical laws และหาสาเหตุ แต่ไม่บังคับให้ทุกชิ้นส่วนเหนือกว่าเมื่อทดสอบแยก ชิ้นส่วนที่มีประโยชน์จาก coupling อาจ validate ภายใน assembly ที่ประกาศ โดยหลักฐานต้องครอบคลุมเงื่อนไข assembly จริง การผ่านแบบแยกไม่ถ่ายโอนไปยังรถอีกแบบโดยอัตโนมัติ

Search ต้องแก้ architecture และ controller หลังได้รับ integration feedback ได้ ไม่ถูกจำกัดให้ประกอบรถขั้นสุดท้ายจาก catalog ตรึงของผู้ชนะที่ optimize แยกกัน Integration failure ต้องส่ง interfaces ที่ได้รับผล โหลด control states การสูญเสีย และ uncertainty กลับสู่ proposal ถัดไป

## 6. Evidence identity และสถานะผลลัพธ์ที่แยกหลายมิติ

หลักฐานผูกกับ evaluation attempt ไม่ใช่ชื่อ candidate อย่างเดียว Identity ประกอบด้วย `candidate_id`, `genotype_sha256`, geometry/material identities, boundary/load history, controller, environment, evaluator/configuration versions, fidelity, seed, evidence class และ artifact hashes การแลกเปลี่ยน geometry ต้องบันทึก terminal signatures และสมมติฐาน binding การผูกที่ขาดหรือกำกวมเป็นผลลัพธ์ชัดเจน

เก็บ event history แบบ append-only โดยแยกมิติ:

| มิติ | ความแตกต่างที่ต้องเก็บ |
| --- | --- |
| Lifecycle/representation | `generated`, `representation_invalid`, `geometry_measured` |
| Boundary binding | `not_evaluated`, `boundary_resolved`, `boundary_unresolved` |
| Physics แยกตาม domain/fidelity/load scope | `not_evaluated`, `numerically_unresolved`, `physically_failed`, `physically_feasible` |
| Manufacturing แยกตาม process ที่ประกาศ | `not_evaluated`, `manufacturing_unresolved`, `manufacturing_compatible`, `manufacturing_incompatible` |
| Promotion แยกตามการใช้งานที่ประกาศ | `not_ready`, `candidate_survivor`, `promotion_ready` |
| Execution disposition | `pending`, `completed`, `budget_exhausted`, `cancelled`, `protocol_invalid` |

ทั้งหมดเป็น fields ที่แยกกัน ไม่ใช่ candidate enum เดียวที่เลือกได้สถานะเดียว Candidate อาจผ่านฟิสิกส์ที่ fidelity หนึ่ง ยังแก้เชิงตัวเลขไม่ได้ที่อีก fidelity และผลิตไม่ได้ด้วย process หนึ่ง Manufacturing status ไม่เขียนทับ physics status การไม่มี process ที่ทดสอบแล้วผ่าน ไม่ได้แปลว่าทุก process ที่เป็นไปได้เป็นไปไม่ได้ เส้นทางที่ไม่ทดสอบหรือยัง unresolved ยังคงไม่ทราบ

`physically_failed` ต้องมีหลักฐานที่รับเข้าได้ว่าข้ามขีดจำกัดกายภาพในขอบเขตที่ประกาศ Divergence, unsupported physics หรือ timeout ไม่ใช่หลักฐาน physical failure ส่วน mesh/solve attempt ที่ไม่สำเร็จเป็น `numerically_unresolved` พร้อมเหตุผลและ execution disposition หากงบหมดก่อนเรียก solver ฟิสิกส์ยังเป็น `not_evaluated` ขอบเขตประมาณที่รับเป็นหลักฐานได้อาจยืนยัน failure เฉพาะขอบเขตได้ เมื่อ preregister applicability ไว้แล้วเท่านั้น

หลักฐานที่ขาดไม่ใช่ error เป็นศูนย์ Protocol/schema/hash/provenance ที่ผิดต้องไม่ผ่าน admission และเก็บบริบทวินิจฉัยไว้ ไม่แปลงเงียบ ๆ เป็น scientific outcome Campaign policy อาจกัก record เสียเฉพาะ candidate แต่ความเสียหายของ protocol ร่วมหรือ ledger integrity ต้องหยุด campaign ที่ได้รับผล ส่วน candidate failures ที่คาดหมายต้องเป็น ledger results ไม่ใช่ assertions ที่ทำ campaign ล่ม

## 7. ขอบเขตฟิสิกส์และหน้าที่ evaluator

ดูแล coverage registry ที่มี version เชื่อม representation, physical domain, constitutive assumptions, boundary types, geometry applicability, solver, validation fixtures, error estimates และระดับหลักฐานสูงสุด พฤติกรรมที่ไม่รองรับรายงานเป็น `unsupported_physics` หรือ `unsupported_representation` ภายใต้ unresolved/not-evaluated outcome ตามกรณี โดยไม่ย้อนกลับไปห้าม genotype language

Evaluators ต้อง derive mass properties, interfaces และ response ที่ใช้ได้จาก geometry วัสดุ และเงื่อนไขงานจริง การเลือก solver ห้ามขึ้นกับชื่อ candidate ที่ตรึงเพียงอย่างเดียว Terminal ancestry ต้องคงอยู่หลัง exchange ส่วน geometric selectors เป็น fallback hypotheses ที่ประกาศและตรวจความกำกวม โมเดลหยาบต้องมีหลักฐาน applicability และ discrepancy ไม่ใช่มีเพียงชื่อ fidelity

แต่ละ domain ที่เกี่ยวข้องต้องเก็บ fields หรือ response quantities ตามขอบเขต reactions/fluxes, residual histories, margins, failure locations, numerical errors, model-form uncertainty และข้อจำกัดวัสดุ ต้อง recover conservation evidence อย่างอิสระเมื่อโมเดลรองรับ การสร้าง balance ด้วยการใส่ค่าติดลบของ input ด้วยมือไม่ใช่ independent validation และ scalar constitutive check ไม่ใช่ full field-equilibrium check

Promoted structural field results ต้องมี refinement อย่างน้อยสามระดับที่ประกาศ บันทึก failures/non-monotonicity และ preregister error gates ส่วน exact analytical หรือ reduced-model checks ต้องระบุแยก และใช้แทน spatial convergence evidence ที่ขาดไม่ได้ Domains อื่นต้องมีกติกา verification และ convergence ที่ลงทะเบียนเฉพาะตัว

Search อาจค้นพบการจัดวางและกลไกใหม่ภายในฟิสิกส์ที่แทนได้ แต่การเสนอรูปทรงไม่สามารถยืนยันกฎฟิสิกส์ที่ยังไม่ได้ model การเพิ่ม physical law, constitutive model หรือ solver capability ต้องเป็น work item ที่ validate แยก มี tests และ evaluator identity ใหม่ Admitted comparison ที่ใช้การเปลี่ยนนั้นต้องเริ่มใหม่ภายใต้ registration ใหม่ และให้ทุก treatment เข้าถึงได้เท่ากัน

## 8. คุณค่าชิ้นส่วน คุณค่ารถ และความเป็นธรรมด้านการควบคุม

บันทึก local quality ต้นทุนปฏิสัมพันธ์ และผลต่อรถทั้งคันแยกกัน Local evidence รวม mass, loss, capacity, response range และ failure margins ที่เกี่ยวข้อง ส่วน vehicle evidence รวมการจบการแข่งขัน เวลารวม พลังงาน thermal/structural margins และภาระที่ย้ายไปให้ระบบอื่น ชิ้นส่วนที่ดูดีขึ้นไม่ใช่รถดีขึ้น หากย้ายต้นทุนไปอยู่ที่ cooling, containment, supports หรือ control

ใช้การเปรียบเทียบที่ลงทะเบียนทั้งสองชนิดเมื่อเกี่ยวข้อง:

- **Controlled substitution:** เปลี่ยนแบบเป้าหมายโดยตรึงสภาพแวดล้อมรอบข้างที่ประกาศและตรวจ interface feasibility เพื่อแยก causal effect ภายในบริบทนั้น
- **Matched adaptation:** ให้แต่ละ treatment ปรับรถและ controller ได้ภายใต้งบ optimization รวม โอกาสใช้ชิ้นส่วน และข้อกำหนดหลักฐานเดียวกัน รายงานงบ design กับ controller แยกกัน เพื่อเทียบประโยชน์ระบบที่ทำได้ ไม่ใช่เพียงความเข้ากันได้กับ controller เดิมตัวหนึ่ง

ไม่บังคับให้ exploratory child ทุกตัวลดเวลาการแข่งขันทันที เก็บ archives ที่จำกัดงบสำหรับ feasible quality, near-feasible margins, functional behavior ที่ต่างกัน และ unresolved hypotheses ที่ให้ข้อมูล Reproduction privileges, escalation caps และ diversity descriptors ต้องตรึงโดย registration การอยู่ใน archive ไม่ให้สิทธิ์ promotion

## 9. บัญชีทรัพยากร การจัดคิว และการตรวจ proxy

รายงาน proposal attempts, geometry executions, CAD calls, meshing attempts, elements/DOF, solver iterations, CPU/GPU time เมื่อมี, wall time, peak memory, retries, cache hits และ fidelity promotions โดย peak memory เป็นค่าสูงสุด ไม่ใช่ค่าใช้จ่ายสะสม บันทึก hardware, worker count และ concurrency Counter ที่ไม่ทราบต้องคงไม่ทราบ หากขาด counter ที่ประกาศว่าบังคับ ห้ามกล่าวอ้าง fairness

แต่ละ experiment กำหนด primary compute constraint และ resource vector พร้อมกติกาบังคับ การนับ candidate เท่ากันอย่างเดียวไม่พอ ต้อง reserve ทรัพยากรก่อนเริ่ม operation และ settle ต้นทุนที่สังเกตได้ภายหลัง กำหนดวิธีจัดการ timeout/overshoot, retries, duplicate work, reservation recovery หลัง crash และเงื่อนไขหยุด campaign ทุก failed/unresolved attempt ใช้งบตามต้นทุนที่ประกาศ Retry มี attempt identity ของตัวเองและห้ามลบต้นทุนครั้งก่อน

แบ่งงบชัดเจนสำหรับการประเมินหยาบวงกว้าง score-independent stratified audits, quality/novelty promotion, unresolved/stepping-stone escalation และ finalist validation ลงทะเบียนสัดส่วนและกฎย้ายงบก่อนทดลอง จองโอกาส audit มากกว่าศูนย์ให้ representation ไม่คุ้นเคยที่อยู่ในขอบเขตประเมิน ห้ามใช้งบ audit เฉพาะแบบคะแนน proxy สูง Candidate ที่ยังไม่ได้รับการประเมินก่อนงบหมดต้องคงมองเห็นเป็น `not_evaluated`

Cache policy ต้องเปิดเผยต้นทุนสร้าง ขอบเขตใช้ซ้ำ และ amortization Shared caches และโมเดลที่คำนวณไว้ต้องเข้าถึงเท่ากัน หรือรายงานโอกาสที่ไม่เท่ากันและคิดต้นทุนตามกฎตรึง Logical scheduling ที่ deterministic ใช้ลำดับและ tie-breaking ที่ลงทะเบียน การ execute แบบ asynchronous ห้ามเอื้อ representation ที่เสร็จเร็วโดยไม่เปิดเผย

ตรวจ proxy false negatives และ false positives เทียบหลักฐานที่เข้มกว่าและรับเข้าได้ ด้วย score-independent stratified samples บันทึก strata, inclusion probabilities, denominators, unresolved reference outcomes และ uncertainty แก้ aggregate estimates ตามการสุ่มที่ไม่เท่ากัน หรือรายงานเฉพาะภายใน strata ผล higher-fidelity ที่ไม่ทราบห้ามติดป้าย negative และหลักฐานไม่พอต้องเป็น `not_estimable` ไม่ใช่อัตราที่แต่งขึ้น

## 10. Replay การเรียนรู้ และการห้ามซ่อมย้อนหลัง

แยก replay claims สองชนิด:

- **Decision replay:** ใช้ immutable events, random streams, protocol และ tie-break rules เดิม เพื่อสร้าง proposal identities, budget decisions, state transitions และ promotion decisions กลับมาตรงเดิม
- **Execution replay:** รัน geometry/physics ใหม่ด้วย tools และ environment ที่ตรึง เทียบตาม numerical tolerances ที่ลงทะเบียน และรายงาน timing กับ nondeterminism แยกกัน ห้ามสัญญา wall time เท่ากันหรือ field values ตรงทุก bit โดยไม่มีหลักฐาน

อนุญาตให้เรียนรู้จากผล การเปลี่ยน geometry, material, architecture, controller, interfaces หรือ task decomposition ต้องสร้าง candidate/task identity ใหม่ มี parent links, mutation trace และต้นทุนประเมินใหม่ Parent ที่ล้มเหลวคงเดิม Refinement ของ candidate เดิมสร้าง evaluation attempt ใหม่พร้อม fidelity/tool identity การ healing geometry แบบเปิดเผยที่เปลี่ยนแบบก็ต้องเป็น descendant ใหม่ ห้ามเขียนทับ geometry ของ parent เงียบ ๆ

Retrospective repair ที่ห้ามรวมการแก้ผล เกณฑ์ โหลด identity หรือ accounting record เดิมเพื่อให้ผ่าน ผลใหม่ append โดยไม่เขียนทับประวัติ การเปลี่ยน external task, evidence gates, evaluator หรือ statistical plan ต้องใช้ experiment registration ใหม่ ข้อมูลที่เห็นแล้วใช้เป็น exploratory/calibration evidence ได้ แต่ห้ามเปลี่ยนป้ายให้เป็น holdout evidence ที่ยังไม่เคยเห็น

## 11. การลงทะเบียนและออกแบบการทดลอง

แยก exploratory/calibration runs, software fixtures และ admitted comparisons โดย Work 098 ตรึง protocol schema, transition rules และ registration requirements แต่ละ study ต้องใส่และตรึงค่าตัวเลขของตัวเองก่อนเห็น admitted outcomes หากมีค่าที่ขาดต้องปิดกั้น admitted execution เอกสารนี้ไม่แต่ง universal tolerances หรือ sample sizes สำหรับ physical domains ที่ยังไม่ได้ implement

ทุก registration ประกอบด้วย:

- hypothesis คำอธิบายคู่แข่ง independent variables และ controlled factors
- task/energy/material profile, representations, operators, evaluators และ applicability
- treatment/baseline identities, seeds, optimization opportunity และ controller policy
- primary metric, direction, minimum meaningful effect, secondary metrics และ units
- physical/numerical/promotion thresholds และวิธีจัดการ failure/unresolved
- เหตุผล sample size หรือ power/precision target, statistical test, uncertainty intervals และ multiplicity policy
- budget partition, stopping rule, audit sampling, cache/retry และ scheduling policy
- exploratory/training/holdout split, leakage controls และ immutable registration hash
- supporting evidence, contradicting evidence, alternative explanations, missing evidence และ confidence ใน result record

การเปรียบเทียบขั้นต่ำที่ต้องวางแผน:

| Experiment | Independent variable / controls | Dependent evidence และการหักล้าง |
| --- | --- | --- |
| Gate-order diagnostic | Proposals ตรึงชุดเดียวกัน; early manufacturing rejection เทียบ evaluate-first annotation; task/evaluator ตรงกันและประกาศ diagnostic budget | หน้าที่ที่มีหลักฐานน่าเชื่อถือแต่ถูกทิ้งเร็ว process outcomes และ compute หักล้างหากสิ่งที่กู้คืนได้มีแต่ invalid/exploitative หรือ unsupported promotions เพิ่ม |
| Gate-order search | Adaptive searches ภายใต้ seeds และงบรวมที่จับคู่; proposal streams อาจแยกจากกัน | Feasible niches, time/cost to survivor และ vehicle utility ห้ามอ้าง same-proposal เมื่อ feedback ที่ต่างทำให้ search เปลี่ยนแล้ว |
| Coupled discovery | ประกอบเฉพาะ isolated survivors เทียบ exploratory architecture/component/controller co-design โดยให้โอกาสเท่ากัน | Vehicle benefit, กลไกหลายหน้าที่ที่มีประโยชน์ และ interaction effects ที่ validate แล้ว หักล้างหากประโยชน์หายเมื่อคิดต้นทุนครบหรือใช้ฟิสิกส์เข้มขึ้น |
| Representation and morphology | Frozen-library, graph-only, morphology-only และ joint search controls เมื่อเกี่ยวข้อง | Executed geometry change, functional behavior, duplication และ causal diversity การเปลี่ยนชื่อหรือ hash อย่างเดียวไม่พอ |
| Archive retention | Feasible-only เทียบการเก็บ feasible/failed/unresolved แบบจำกัดงบ | Survivor utility แบบ paired-seed, ancestry และ compute share ความล้มเหลวรวมไม่มีประโยชน์ที่น่าเชื่อถือหรือ escalation ควบคุมไม่ได้ |
| Controller fairness | Controlled substitution และ matched adaptation | Local/vehicle effects พร้อมต้นทุน design/controller; รายงานเมื่อประโยชน์ขึ้นกับ controller |

ใช้ conventional/fixed-topology baselines ที่ optimize อย่างยุติธรรมและ random controls เมื่อเกี่ยวข้อง โอกาสเท่าเทียมไม่บังคับให้ผลกายภาพเหมือนกัน Threshold ที่เลือกจาก calibration ต้องเปิดเผย calibration set และล็อกก่อน admitted run ที่แยกต่างหาก

## 12. Promotion และหลักฐานการค้นพบ

`candidate_survivor` หมายถึง candidate หรือ coupled assembly ที่ประกาศผ่านข้อกำหนด physical, numerical, manufacturing, holdout และ replay ของ trial ที่ลงทะเบียนภายในขอบเขตที่ระบุ สิทธิ์ exploratory integration ไม่ต้องมีสถานะนี้ ส่วน `promotion_ready` ต้องมีหลักฐาน independent stronger-fidelity และความปลอดภัยเพิ่มเติมสำหรับการใช้งานเป้าหมาย ไม่ใช่คุณสมบัติสากลของชิ้นส่วน

Whole-vehicle promotion ต้องมี geometry สามมิติที่คิดบัญชีครบ หรือ representations ที่มีเหตุผลรองรับชัดเจนครอบคลุมรถ interfaces, mass/inertia, energy carriers, motion/contact, structure, thermal behavior, flow/aerodynamics, controls และทุก domain อื่นที่เกี่ยวข้อง พฤติกรรมเกี่ยวข้องที่ยังไม่ทดสอบปิดกั้น complete-vehicle claim หลักฐานเฉพาะส่วนถ่ายโอนได้เฉพาะภายใน applicability envelope ที่ลงทะเบียน การเปลี่ยน interfaces หรือ loads ต้องตรวจ applicability และประเมินใหม่ตามที่จำเป็น

Alternative representation ใด ๆ ยังต้อง instantiate แบบกายภาพสามมิติที่ครบในส่วนที่เกี่ยวข้อง การ execute รถแบบ reduced-order อาจใช้ response models ที่ validate แล้วและ derive จากแบบนั้น แต่ไม่ยกเว้น hardware ภายใน containment หรือ interfaces จาก geometry และบัญชีกายภาพ

รายงาน novelty และ evidence strength แยกกัน:

| คำถามความใหม่ | หลักฐานที่ต้องมี |
| --- | --- |
| Geometry หรือ arrangement ใหม่หรือไม่? | ความต่างที่ execute ได้เกินกว่าการเปลี่ยน identity; ขอบเขต corpus ที่เทียบ |
| Functional behavior หรือ mechanism ใหม่หรือไม่? | Causal load/energy/motion/field evidence และ controlled removal/substitution tests |
| Component หรือ system ดีขึ้นอย่างมีประโยชน์หรือไม่? | Local/vehicle metric ที่ลงทะเบียน optimized baselines, uncertainty และ matched adaptation เมื่อเกี่ยวข้อง |
| เป็น technology-discovery candidate ในบริบทกว้างหรือไม่? | เทียบ prior art/literature และ independent validation; แยก corpus novelty จาก external novelty |

Graph non-isomorphism เป็น diversity descriptor ไม่ใช่เงื่อนไขบังคับของทุกการค้นพบ Continuous geometry หรือ material distribution ที่เปลี่ยนอาจทำให้หน้าที่เปลี่ยนแม้ connection graph เหมือนเดิม ในทางกลับกันกราฟต่างไม่พิสูจน์ว่ามีกลไกต่างที่มีประโยชน์ เก็บ labels แยกสำหรับ software fixture, exploratory simulation, admitted simulation, independently corroborated simulation และ physical validation การอ้างเทคโนโลยีที่ validate ในโลกจริงต้องมี physical evidence ที่สอดคล้องกัน

## 13. ขอบเขต implementation ใหม่ของ Works 098–101

| Work | สิ่งที่ต้องส่งมอบ | Exit gate และข้อจำกัดชัดเจน |
| --- | --- | --- |
| 098 — Whole-Vehicle Discovery State, Evidence and Fairness Contract | Schemas/validators ที่มี version, orthogonal states, evidence identity/applicability, การแยก exploratory/promotion, append-only ledger/replay, กฎ budget/scheduling/audit, registration validator และ legacy adapters ขั้นต่ำ | Mixed-ledger decision replay; ปฏิเสธ tamper/invalid-promotion; budget/resume ถูกต้อง; registration ครบ; evidence classes ปลอมเป็น physical survivors ไม่ได้ เป็น software contract เท่านั้น |
| 099 — Executable Morphology, Architecture and Archive Search | Numerical geometry execution, part/interface split/merge, typed ancestry, controller genes ที่ลงทะเบียนเมื่อใช้ และ bounded feasible/failed/unresolved archives | หลาย seeds สร้างการเปลี่ยนที่ execute แล้วพร้อม geometry ที่วัดและ lineage ที่ทำซ้ำได้ สาธิตการเปลี่ยน decomposition และการวัด descriptor ที่มีประโยชน์ ไม่อ้าง useful new physics จาก geometry อย่างเดียว |
| 100 — Functional and Coupled Discovery Trials | Geometry-derived local/assembly solvers แบบจำกัดขอบเขต task-derived loads, isolated/coupled contrasts ที่ลงทะเบียน proxy audits และ vehicle feedback ที่ fidelity ประกาศ | Functional candidate หรือ coupled assembly ที่ไม่เคยประกาศอย่างน้อยหนึ่งตัวผ่าน `candidate_survivor` gates พร้อม causal evidence และ ledger integrity ถ้าไม่มี survivor ให้บันทึกผล negative/partial ห้ามลด gate ไม่บังคับทุกชิ้นส่วนชนะเมื่อแยกหรือมี non-isomorphic graph |
| 101 — Whole-Vehicle Co-Design and Evidence Promotion | ปรับ architecture/geometry/controller integration วนซ้ำ coupled transient evaluation, full accounting, holdouts, independent stronger evidence และ optimized vehicle baselines | Candidate ครบทั้งคันจบงานที่ลงทะเบียนและผ่าน vehicle promotion gates ทั้งหมด Performance superiority และ technology novelty ต้องมีหลักฐานที่ลงทะเบียนแยก Simulation ยังคงเป็น simulation จนกว่าจะ physically validated |

Exploratory integration เริ่มใน Work 100 ด้วยขอบเขตจำกัดที่ประกาศ ไม่รอ Work 101 ส่วน Work 101 เป็น milestone ระดับโปรแกรม ไม่ใช่คำสัญญาว่าการค้นหารถทั้งคันทั่วไปจะจบใน implementation task เดียว แบ่ง implementation ใหญ่เป็น work items สองภาษาที่มีเลขใหม่ dependencies ชัด validation และ commit ห้ามนับการทำเอกสารนี้เสร็จเป็นการทำ Work 098 เสร็จ

## 14. Acceptance cases ที่ต้องมี ก่อน admitted execution

Work 098 ต้อง implement tests ที่สาธิตทุกข้อต่อไปนี้ด้วย fixtures ที่ติดป้ายชัดเจน:

1. แยกทุกสถานะจาก roadmap เดิมได้ โดยเก็บ physics/manufacturing states ที่เกิดพร้อมกันและ uncertainty แยกตาม fidelity
2. ห้ามรวม physics ที่ยังไม่ถูกเรียก timeout, divergence, unsupported domain, physical failure และ corrupt provenance เป็นอย่างเดียวกัน
3. Exploratory assembly รับหลักฐานที่ประกาศว่ายังไม่ครบได้เฉพาะขอบเขตที่อนุญาต ส่วน promotion ต้องปฏิเสธหลักฐานบังคับที่ขาด แม้ proxy quality ดีมาก
4. Geometry/material/controller/boundary/evaluator identities ที่เปลี่ยนต้องใช้หลักฐานนอก applicability ซ้ำหรือปลอมเป็น survivor ไม่ได้
5. Descendant ใหม่เรียนรู้จาก failure ได้ แต่ parent และเกณฑ์เดิมต้องเปลี่ยนย้อนหลังไม่ได้
6. Interruption/resume, retry, duplicate results, cache reuse และ budget exhaustion ต้องไม่ทำให้เกิดงานฟรี double settlement หรือ hidden deletion; งานภายนอกที่ใช้ทรัพยากรแล้วแต่ผลสูญหายบันทึกตาม recovery rule ที่ลงทะเบียน
7. Decision replay สร้าง selection และ accounting ตรงเดิม ส่วน execution replay รายงาน numerical tolerance และข้อจำกัด timing แยกกัน
8. Audit selection ไม่ใช้คะแนนภายใน strata ที่ลงทะเบียน เก็บ inclusion probabilities และจัดการ reference labels ที่ไม่ทราบโดยไม่แต่ง false-negative rate
9. Registration ที่ไม่ครบหรือถูกแก้เริ่มหรือทำ admitted run ต่อภายใต้ identity เดิมไม่ได้ และ software promotion fixtures เข้า scientific result counts ไม่ได้
10. Regression tests ของ benchmark เดิมยังคงอยู่ Labels เดิม `accepted`, `intact`, `passed` หรือ `invalid` ต้องตีความจาก evidence scope ไม่แปลงเป็น physical feasibility/failure โดยอัตโนมัติ

การผ่าน cases นี้ยืนยัน contract readiness การค้นพบจริงต้องอาศัยการทดลองและหลักฐานขั้นถัดไปข้างต้น

## 15. สิ่งที่ไม่ทำและข้อจำกัดที่คงอยู่

Protocol นี้ไม่รับประกันการค้นพบ ไม่อนุญาต infinite search หรือ magic materials ไม่ลด conservation/safety และไม่บังคับให้ implement ทุก physics domain ทันที ไม่กำหนดให้รถทั่วไปเป็นคำตอบที่ถูกต้องเพียงแบบเดียว Manufacturing อาจ annotate เร็วเมื่อราคาถูก แต่เฉพาะ promotion requirements ที่ประกาศเท่านั้นที่ใช้คัดออกจากการกล่าวอ้างได้ Unresolved research hypotheses คงอยู่ภายใต้งบจำกัดได้โดยไม่โฆษณาว่าเป็นเทคโนโลยีที่ทำงานแล้ว

ผลที่ต้องการคือวงจรเรียนรู้ที่ตามหลักฐานได้ ซึ่งความต้องการของรถทั้งคันและกลไกชิ้นส่วนปรับเปลี่ยนกันและกันได้ ขณะที่ทุก promoted claim ยังผูกกับฟิสิกส์ ทรัพยากร และหลักฐานที่สาธิตจริง
