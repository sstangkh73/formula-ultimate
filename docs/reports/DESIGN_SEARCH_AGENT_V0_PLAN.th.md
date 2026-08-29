# Design Search Agent v0: แผนวิจัยและการพัฒนา

ไฟล์ต้นฉบับภาษาอังกฤษ: `DESIGN_SEARCH_AGENT_V0_PLAN.md`

วันที่รายงาน: 2026-08-29

สถานะ: วางแผนแล้ว ยังไม่ได้ implement

Evidence baseline: commit `3398459`, Research Experiment Protocol v1 และการรัน
`FU-C0001` ผ่าน geometry-to-Level-0 ที่เสร็จแล้ว

## ข้อสรุปหลัก

Formula Ultimate ควรใช้ **search agent แบบ deterministic ที่ repo เป็นเจ้าของ**
ชื่อ `DesignSearchAgentV0` สำหรับ campaign ออกแบบแรก ไม่ควรใช้ LLM เป็น
numerical optimizer และไม่ให้อำนาจ agent แก้ evaluator, tolerance, energy
limit, load case, budget หรือ promotion rule ของตัวเอง

Codex ยังคงเป็น **Research Orchestrator**: ช่วยตั้ง hypothesis, สร้าง protocol
ที่ review แล้ว, เริ่ม bounded run, ตรวจ failure และเขียน falsification review
ส่วน CadQuery, STEP, FreeCAD, Level 0 และ independent solver ในอนาคตเป็น
evaluator ที่ไม่ใช่ agent มนุษย์ยังเป็น gate สำหรับเปลี่ยนคำถามวิจัย, promote
candidate ที่มีค่าใช้จ่ายสูง หรือสร้างข้ออ้างภายนอก

งานออกแบบที่มีความหมายชุดแรกควรเป็น **loaded interface plate** แทนรถทั้งคัน
งานนี้เพิ่มหน้าที่ทางกลที่ประกาศไว้เข้าสู่ CAD route ที่พิสูจน์แล้ว และยังเล็ก
พอที่จะ falsify/debug ได้ `FU-C0001` เดิมเป็นหลักฐาน pipeline เท่านั้น ไม่ใช่
performance baseline

## 1. คำถามวิจัย

ภายใต้ interface, load, material assumption, geometry limit, evidence gate และ
candidate-evaluation budget ชุดเดียวกัน seeded evolutionary search สามารถหา
interface-plate geometry ที่ feasible และ mass ต่ำกว่า matched random กับ
fixed-grid search treatment ได้สม่ำเสมอกว่าหรือไม่?

คำถามนี้ทดสอบว่า search procedure เพิ่มคุณค่าภายใน functional boundary แบบแคบ
หรือไม่ ไม่ได้ถามว่า agent สร้างรถทั้งคันหรือเทคโนโลยีใหม่ได้หรือไม่

### Preferred hypothesis H1

เมื่อใช้ seed ที่ประกาศและ evaluation budget เท่ากัน `DesignSearchAgentV0`
ให้ median best-feasible mass ต่ำกว่า matched baseline ทั้งสอง โดยยังผ่าน
geometry, interface, structural และ replay gate ชุดเดียวกัน

### H0

Evolutionary treatment ไม่เหนือ baseline ที่ดีกว่าตาม practical threshold ที่
ประกาศ หรือข้อได้เปรียบหายไปเมื่อทดสอบ holdout load case หรือ independent
re-evaluation

### คำอธิบายทางเลือกที่ต้องทดสอบ

- Grammar ฝัง winning family แทนที่ agent จะค้นพบ
- Candidate invalid ถูกตัดออกและทำให้ treatment หนึ่งได้ budget ไม่ยุติธรรม
- ผลเกิดจาก wall time, solver call, retry หรือการใช้ seed ไม่เท่ากัน
- Level-0 structural model ให้รางวัล geometry บาง/ขาดที่ solver แรงกว่าปฏิเสธ
- STEP healing, meshing หรือ numerical tolerance เปลี่ยนลำดับ candidate
- Mass ดีขึ้นเพราะ parameter effect เท่านั้น ไม่ใช่ geometric discovery ที่มี
  ประโยชน์

## 2. หน้าที่ของ Agent และเครื่องมือ

| บทบาท | ระบบ | ทำได้ | ห้ามทำ |
|---|---|---|---|
| Research Orchestrator | Codex พร้อม human review | ร่าง protocol, ตรวจ evidence, เริ่ม bounded campaign, วินิจฉัย failure, เขียน review | เปลี่ยน preregistration ของ run ที่จบแล้ว หรือประกาศ discovery จาก Level 0 |
| Design search | seeded Python process `DesignSearchAgentV0` | เสนอ candidate declaration, อัปเดต population ภายในจาก result ที่รับแล้ว | แก้ evaluator/config/budget/tolerance, ซ่อม artifact, รัน arbitrary CAD code หรือซ่อน failure |
| Geometry generator | constrained CadQuery adapter | สร้าง geometry ที่ grammar รับเท่านั้นและ export STEP | เลือก fitness, เปลี่ยน load หรืออ้าง feasibility |
| Geometry evaluator | FreeCAD adapter | Import exact STEP hash และรายงาน topology/mass properties | ซ่อม geometry แบบเงียบหรือแทน evidence ที่หาย |
| Functional evaluator | Level-0 structural contract ที่ต้องสร้าง | ประเมิน load case ที่ประกาศและแสดง residual/failure | เปลี่ยน geometry หรือซ่อน non-convergence |
| Downstream evaluator | coupled Level 0 ที่มีอยู่ | รายงานผล mass ต่อ vehicle/race | ถือ mass ของ component อย่างเดียวเป็นหลักฐาน race advantage |
| Promotion evaluator | independent FEA/mesh route ในงานอนาคต | ประเมิน candidate ที่เลือกใหม่และตรวจ convergence/holdout | train หรือ tune search treatment ด้วยผล holdout |

Evaluator deterministic เป็นเจ้าของ pass/fail Agent รับ structured record แต่
ไม่มี mutable evaluator handle

## 3. งานออกแบบเชิงหน้าที่ชุดแรก

Working task ID: `loaded_interface_plate_v1`

Component ส่งผ่าน bearing load ที่ประกาศจาก bolt-hole pair หนึ่งไปอีก pair
ภายใน envelope ที่กำหนด งานนี้เป็น synthetic research fixture ไม่ใช่ vehicle
component ที่รับรองแล้ว

### Interface และ control ที่แก้ไม่ได้

- cylindrical bolt-interface region สี่จุดที่ centre/diameter ตายตัว
- interface pair ซ้ายเป็น support boundary ที่ประกาศ
- interface pair ขวาเป็น distributed bearing-load boundary ที่ประกาศ
- maximum outer envelope และ thickness bound คงที่ในหน่วย SI
- protected interface ligament และ central keep-out region ที่ประกาศ
- material record มีเวอร์ชัน พร้อม density, elastic constant, allowable policy,
  provenance และ uncertainty
- training load, holdout load, mesh policy, solver tolerance และ failure policy
  เหมือนกันทุก treatment
- ไม่มี geometry หรือ material นอก envelope/library ที่ประกาศ
- ห้ามแก้ contact, thickness หรือ material แบบเงียบ

Load และ allowable ตัวเลขต้องมี source หรือระบุว่า synthetic ก่อน experiment
implementation รายงานแผนนี้ยังไม่กำหนดตัวเลข เพราะต้องมี work item แยกสำหรับ
load/interface และ validation review

### Design variable ที่ agent เปลี่ยนได้ใน v0

- outer contour control point แบบ bounded หรือ profile parameter ที่รับ
- thickness ภายใน manufacturing และ solver bound ที่ประกาศ
- จำนวน ตำแหน่ง และขนาด relief feature ที่รับและอยู่นอก protected
  interface/keep-out
- web width และ fillet radius ภายใน minimum-feature rule ที่มีเวอร์ชัน

ตำแหน่ง bolt/load, material identity, envelope, keep-out, failure threshold,
solver setting และ budget ไม่ใช่ searchable variable

Grammar v0 จงใจเป็น fixed-topology หรือ variable-topology แบบแคบเพื่อแยก
search/evaluator error นี่ไม่ใช่หลักฐานเรื่อง open-ended vehicle topology
Grammar รุ่นหลังควรสื่อ functional interface แทนการบังคับรูปทรง component แบบ
conventional

## 4. Candidate Evidence Contract

Candidate declaration ที่ immutable ทุกตัวอย่างน้อยต้องมี:

```text
protocol_id
campaign_id
treatment_id
candidate_id
parent_candidate_ids
generation_index
grammar_version
operator_id
seed and RNG state/fingerprint
geometry parameters in SI units
material_id
interface/load_case_set IDs
evaluation-budget counters
source/config/commit identity
```

ทุก attempted evaluation ใช้ budget รวม grammar rejection, CAD failure, STEP
failure, FreeCAD failure, meshing failure, numerical failure และ constraint
failure Candidate ที่ล้มเหลวยังคงเป็น append-only observation

Output record ต้องเก็บ:

- exact stage และ failure code
- CAD validity, solid count, bounds, volume, centre of mass และ inertia เมื่อมี
- STEP hash และ source hash ของ generator/evaluator
- interface และ keep-out residual
- structural output, solver residual, mesh evidence และ convergence status
- mass, feasible/infeasible status และ objective value
- wall time, CPU time เมื่อวัดได้, peak memory เมื่อวัดได้ และจำนวน solver call
- downstream Level-0 output เป็น evidence ไม่ใช่ตัวแทน structural function
- supporting/contradicting/missing evidence และ claim level

## 5. Search Algorithm v0

ใช้ seeded `(mu + lambda)` evolutionary strategy ที่ implement ด้วย Python
ปกติ มี selection/serialization แบบ deterministic รุ่นแรกยังไม่ต้องใช้ LLM,
neural surrogate, novelty model หรือ self-modifying code

กลไกที่เสนอ:

1. Initialize population จาก declaration ที่ grammar รับด้วย RNG stream ที่
   บันทึกหนึ่งชุด
2. ประเมิน attempted candidate ทุกตัวหนึ่งครั้งผ่าน bounded pipeline เดียวกัน
3. จัดอันดับ candidate ที่ feasible แบบ lexicographic: hard gate ต้องผ่านก่อน
   แล้วจึง mass ต่ำกว่า เก็บ diversity เป็น tie-break รองหรือ metric แยก
4. เลือก parent แบบ deterministic จาก record ที่รับ
5. ใช้ parameter/feature mutation operator ที่มีเวอร์ชัน
6. ห้าม retry failed geometry ฟรี Retry คือ candidate ใหม่และใช้ budget
7. Checkpoint population, RNG state, budget ledger และ artifact reference หลัง
   ทุก generation
8. Replay campaign จาก manifest และเทียบลำดับ semantic result แบบ exact หรือ
   ตาม numerical tolerance ที่ประกาศ

ห้าม optimize mass จนกว่าจะมี structural feasibility contract การใช้เส้นทาง
mass-only ของ `FU-C0001` ปัจจุบันเป็น fitness จะให้รางวัลการตัด material โดยไม่
พิสูจน์ว่า component ส่งผ่าน load ได้

## 6. Experimental Treatment และ Fair Budget

Scientific campaign ควรเทียบสาม treatment บน grammar เดียวกัน:

| Treatment | วิธี | วัตถุประสงค์ |
|---|---|---|
| `GRID` | deterministic space-filling/fixed grid บน parameter ที่รับ | tuned fixed-search baseline ที่โปร่งใส |
| `RANDOM` | seeded uniform หรือ prior sampling ที่ประกาศ | unguided search baseline |
| `EVOLUTION` | `(mu + lambda)` search ของ `DesignSearchAgentV0` | agent treatment ที่ทดสอบ |

Development smoke run ใช้ `8–16` evaluation และหนึ่ง seed ได้ แต่รองรับเพียง
software debugging Preregistered comparison ควรเริ่มจาก budget ชั่วคราวนี้และ
เปลี่ยนได้เฉพาะในแผนของตัวเองก่อนเห็นผล:

- attempted candidate `64` ตัวต่อ treatment ต่อ seed
- independent seed ที่ประกาศล่วงหน้า `10` ชุด
- grammar, initialization domain, candidate directory limit, CAD/solver
  version, training load, holdout และ promotion gate ชุดเดียวกัน
- ไม่มี retry ฟรี attempted evaluation ทุกครั้งนับ budget
- รายงาน evaluation count และ measured compute เพราะ solver failure เปลี่ยน
  cost ได้
- cap wall time/memory ต่อ candidate เท่ากัน
- tune baseline operator ก่อน freeze campaign โดยไม่อ่าน holdout result

รวม attempted evaluation `1,920` ครั้งในสาม treatment Pilot ต้องวัด wall time
และ failure rate จริงก่อนยืนยัน budget

## 7. ตัวแปร Metric และกฎตัดสิน

### ตัวแปรอิสระ

- search treatment: `GRID`, `RANDOM` หรือ `EVOLUTION`

### ตัวแปรควบคุม

- grammar และ candidate domain
- interface, material, envelope, keep-out, load, constraint และหน่วย
- evaluator version, mesh policy, tolerance, failure policy และ promotion rule
- candidate-attempt budget, seed, machine class และ resource limit

### ตัวแปรตาม

- best feasible mass ในแต่ละ attempted-evaluation count
- feasible-candidate rate และการกระจาย failure code
- จำนวน evaluation/wall time เพื่อถึง mass target ที่ประกาศ
- final best feasible mass ต่อ seed
- holdout survival และ independent-evaluator promotion survival
- geometry/interface/structural residual
- diversity หลังตัดผล parameter-identical และ geometry-equivalent
- deterministic replay agreement

### Primary metric

Median final best-feasible mass ข้าม seed เทียบเป็นคู่ที่ attempt เท่ากับ 64
Lower is better เฉพาะเมื่อ geometry, interface, structural, numerical และ
evidence gate ทุกตัวผ่าน

### เกณฑ์สำเร็จชั่วคราว

ก่อน campaign ต้อง freeze practical-effect threshold ข้อเสนอเริ่มต้นคือ
`EVOLUTION` ต้องลด median best-feasible mass อย่างน้อย `2%` เทียบ baseline ที่
ดีกว่าระหว่าง `GRID` และ `RANDOM` โดย paired bootstrap `95%` confidence interval
ของ improvement ยังสูงกว่า `0%` และ candidate ที่เลือกผ่าน holdout กับ
independent promotion check ทั้งหมด

หากไม่ถึงเกณฑ์ ให้รายงานว่า H1 ไม่ได้รับการสนับสนุน ห้ามเปลี่ยน visual
difference, lucky seed หนึ่งชุด หรือ winner ที่ผ่านแค่ Level 0 เป็น success

### เกณฑ์ล้มเหลว

- Search process แก้ evaluator หรือ budget
- candidate identity หาย/ซ้ำ หรือ ledger ไม่ครบ
- replay ไม่ deterministic เกิน tolerance
- จำนวน attempt, seed, load case, solver setting หรือ promotion rule ไม่เท่ากัน
- มี hidden retry เป็นระบบหรือ candidate invalid หาย
- treatment/seed ใดไม่มี feasible candidate
- winner ไม่ผ่าน preregistered holdout หรือ independent solver
- mesh ไม่ converge, geometry invalid, interface violation หรือ numerical
  residual เกิน tolerance
- หลักฐานว่า grammar bias หรือ evaluator exploit อธิบายข้อได้เปรียบได้

## 8. แผน Falsification

Campaign ต้องพยายามล้ม preferred result ด้วย:

1. **Replay:** ทำ candidate order, ancestry, budget ledger และ admitted metric
   ซ้ำจาก manifest เดิม
2. **Operator ablation:** ตัด selection pressure หรือ geometry-feature mutation
   โดยรักษา budget
3. **Grammar ablation:** เทียบ parameter-only grammar กับ feature-mutation
   grammar ภายใต้โอกาสเท่ากัน
4. **Holdout loads:** ประเมิน promoted candidate บน load ที่ไม่ได้ใช้ search
5. **Mesh/timestep refinement:** ทดสอบลำดับ candidate ด้วย numerical setting
   ที่ละเอียดขึ้น
6. **Independent solver route:** ประเมิน candidate ที่เลือกใหม่โดยไม่ใช้ cached
   output จาก search evaluator
7. **Known alternative:** tune solid/webbed baseline ที่ดีที่สุดอย่างแข่งขัน
   แทนการเทียบ default plate ตามอำเภอใจ
8. **Exploit audit:** ตรวจว่า win พึ่ง minimum-feature boundary, topology healing,
   tolerance edge, failure localization หรือ omitted physics หรือไม่

Final review ต้องบันทึก supporting evidence, contradicting evidence,
alternative explanation, missing evidence และ confidence

## 9. ขอบเขต Security และ Authority

`DesignSearchAgentV0` ควรรันเป็น process สร้าง candidate declaration แบบแคบ:

- เขียนได้เฉพาะ fresh candidate/campaign artifact root
- ใช้ allowlisted schema/operator แทน arbitrary generated Python
- ไม่มี network access หรือ project secret
- รับ evaluator result เป็น immutable record
- read-only protocol/config hash ที่ freeze แล้ว
- ไม่มีอำนาจ Git, shell, evaluator-source, tolerance, load หรือ promotion mutation
- หยุดเมื่อ budget/resource หมดและเก็บ checkpoint
- ขอ human approval ก่อนใช้ cloud tool, expensive solver, publication หรือข้ออ้าง
  เกิน registered level

Codex implement/operate harness ได้ใน work item ที่ review แล้ว แต่ pass/fail
ทางวิทยาศาสตร์ต้อง execute ใน deterministic code

## 10. Implementation Roadmap

แต่ละ milestone ต้องเป็น bilingual validated committed work item แยกกัน

### Milestone 1 — Functional task และ load contract

- version interface, keep-out, material record, training/holdout load,
  synthetic/source label และ failure policy ของ `loaded_interface_plate_v1`
- เพิ่ม analytical fixture และ invalid case
- ห้ามเริ่ม search ก่อน freeze contract นี้

Completion gate: interface/load/unit/schema test ผ่านทั้งหมดและไม่มี numerical
allowable ที่ไม่มีเอกสาร

### Milestone 2 — Geometry grammar และ independent measurement

- implement constrained grammar และ candidate manifest
- export STEP และตรวจ exact interface, bounds, volume, mass properties,
  protected region และ topology แยกใน FreeCAD
- บันทึก rejection ทั้งหมดและไม่มี hidden repair

Completion gate: controlled valid/invalid specimen ผ่าน evidence route ซ้ำได้

### Milestone 3 — Structural Level-0 feasibility gate

- implement conservative structural model ที่ประกาศหรือ project-owned solver
  adapter พร้อม load, boundary condition, mesh evidence, residual และ convergence
  test
- ทดสอบ analytical reference และ deliberate failure fixture
- แยก solver validity จาก physical pass/fail

Completion gate: mass ปรับ fitness ดีขึ้นไม่ได้หาก load transfer และ
structural/numerical gate ไม่ผ่านทั้งหมด

### Milestone 4 — Search harness และ budget ledger

- implement candidate ID, ancestry, operator, RNG checkpoint, append-only
  result ledger, equal-budget enforcement และ structured failure
- เพิ่ม treatment `GRID`, `RANDOM`, `EVOLUTION` หลัง evaluator API เดียวกัน
- รันเฉพาะ smoke fixture

Completion gate: treatment replay และ budget accounting ตรง exact รวม candidate
ที่ล้มเหลว

### Milestone 5 — Pilot และ protocol freeze

- วัด candidate wall time, memory, failure distribution และ feasible rate
- tune resource cap และยืนยัน/แก้ campaign ชั่วคราว `64 x 10 x 3` ก่อนเห็น
  holdout comparison
- freeze hypothesis, metric, seed, baseline tuning และ statistical rule

Completion gate: มี signed/versioned campaign manifest ก่อนสร้าง main result

### Milestone 6 — Main campaign และ falsification

- execute ทุก treatment ภายใต้โอกาสเท่ากัน
- promote เฉพาะ candidate ที่เลือกตาม preregistration
- รัน holdout, refinement, independent-solver และ ablation check
- รายงาน failure และ contradicting evidence

Completion gate: สรุปเฉพาะว่า H1 ได้รับการสนับสนุนภายใน
`loaded_interface_plate_v1` หรือไม่ ห้าม generalize เป็น complete-vehicle
discovery

### Milestone 7 — ขยายขอบเขตแบบควบคุม

หลัง Milestone 6 เท่านั้นจึงพิจารณาเพิ่ม component selection, typed connection
mutation, variable topology, packaging, ground-contact arrangement และ
whole-vehicle co-design ทุกการขยายต้องมี matched baseline และหลักฐาน
geometry-to-physics ที่แรงขึ้น

## 11. Deliverable สำหรับ Implementation ในอนาคต

ระบบที่ implement แล้วควรมี:

- protocol, task, grammar, material, load และ campaign schema ที่มีเวอร์ชัน
- `DesignSearchAgentV0` พร้อม deterministic checkpoint/replay
- evaluator interface เดียวที่ทุก treatment ใช้
- immutable candidate/result/budget ledger
- constrained CadQuery และ FreeCAD adapter
- structural Level-0 และ independent-promotion adapter
- unit, invariant, integration, numerical, replay, exploit และ negative test
- campaign summary table/plot ที่สร้างจาก admitted result record
- bilingual plan/result พร้อม exact command, hash, commit, seed, limitation และ
  claim level

## 12. สิ่งที่รายงานนี้ยังไม่พิสูจน์

- `DesignSearchAgentV0` ยังไม่มีใน code
- ยังไม่ได้รัน loaded-interface grammar, load case, structural solver, baseline
  campaign หรือ autonomous candidate
- Budget และ effect threshold `2%` เป็นตัวเลือกในแผนที่ต้อง review/freeze ก่อน
  experiment ไม่ใช่ผลที่สังเกตแล้ว
- `FU-C0001` พิสูจน์เพียง geometry evidence route ไม่ใช่ structural baseline
- ไม่มีสิ่งใดรองรับ complete-vehicle feasibility, safety, manufacturability,
  race superiority, novelty หรือ discovery

## คำแนะนำ

งานถัดไปควรเป็น **Milestone 1: Functional Task and Load Contract** ห้าม implement
evolutionary loop ก่อน Search agent ที่ไม่มี load-bearing feasibility evaluator
จะ optimize ฟิสิกส์ที่หายไปและสร้าง geometry ที่ดูน่าเชื่อแต่ไม่มีความหมายทาง
วิทยาศาสตร์
