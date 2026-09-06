# แผน Work 100: Functional and Coupled Discovery Trial V1

ต้นฉบับภาษาอังกฤษ: `2026-09-06_100_functional-coupled-discovery-trial-plan.md`

วันที่: 2026-09-06 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และหลักฐานเริ่มต้น

Implement trial Work 100 แบบจำกัดตาม `WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md` โดยเริ่มจาก Work 099 commit `e6f3196` ที่สะอาด Work 099 execute numerical swept-solid morphology, วัด CAD geometry และรักษา architecture/archive lineage แต่ระบุชัดว่าไม่มี field solver Work 100 จะเพิ่ม geometry-derived coupled axial-load/thermal-network evaluator, closed-form reference implementation ที่ต่างกัน, preregistered treatment contrasts, proxy audit, bounded vehicle-feedback metrics และ Work 098 ledger admission

Scope ที่ประกาศคือ multifunctional load/heat path ระหว่าง terminals ไม่ใช่รถแข่งทั้งคัน ผล `candidate_survivor` จะหมายถึง candidate ผ่านเฉพาะ simulated subsystem task fidelity ต่ำ, process-envelope check, untouched holdout load case และ replay gate ที่ลงทะเบียน ไม่ได้หมายถึง race superiority, technology novelty, complete-vehicle feasibility, independent promotion หรือ physical validation

## ขอบเขตและไฟล์ที่วางแผน

- `src/formula_ultimate/physics/functional_network_solver.py`: ประกอบ geometry-derived variable-radius axial/thermal conductance; multi-refinement field solve; reactions, conservation/energy residuals, stresses, temperatures, margins, failure locations, numerical applicability และ bounded component-to-vehicle burden feedback
- `src/formula_ultimate/physics/functional_network_reference.py`: exact linear-radius resistance integration และ network solution แยกสำหรับ cross-method validation โดยไม่ reuse numerical subdivision results
- `src/formula_ultimate/experiments/functional_discovery.py`: ตรวจ trial config แบบเข้มงวด, สร้าง treatments ที่ลงทะเบียนห้าแบบ, bind task/material/process, สร้าง outcome/admission artifacts และ deterministic analysis
- `config/experiments/functional_discovery_trial_v1.json`: ตรึง physical assumptions หน่วย SI, seeds, treatments, task loads, training/holdout conditions, material model, refinement/error/physics/process thresholds, analysis และ claim boundary
- `config/experiments/functional_discovery_registration_v1.json`: final Work 098 `admitted_simulation` registration ซึ่งสร้างหลังรู้ implementation/validation identities และก่อน admitted observation แรกเท่านั้น
- `scripts/experiments/run_functional_discovery.py`: execute CAD, task-derived proxy/refined/holdout fields, ledger costs, score-independent audits, process/replay gates, survivor decision, archives/results และ cross-run comparison
- `tests/test_functional_discovery.py`: analytical chain/parallel checks, conservation/energy, refinement/reference agreement, task/boundary/material tampering, physical failure เทียบ numerical failure, treatment determinism, process และ promotion/admission negatives
- `docs/contracts/FUNCTIONAL_COUPLED_DISCOVERY_TRIAL_V1.md` และ `.th.md`: equations, assumptions, registration, evidence, commands, outcomes และ limitations
- แผนสองภาษานี้และผลสองภาษาที่ตรงกัน Generated calibration/fixture/admitted evidence เก็บใต้ ignored `artifacts/work100/`

## ตัวแปรการทดลอง controls และการหักล้าง

- Independent variable: treatment ระหว่าง `FIXED_TOPOLOGY`, `RANDOM_CONTROL`, `GRAPH_ONLY`, `MORPHOLOGY_ONLY` และ `JOINT_MORPHOLOGY_CONTROLLER` โดยจับคู่ registered seeds Controller gene ยังมองเห็นได้ แต่ไม่ให้เครดิตหาก task model ที่ประกาศไม่มี causal path
- Dependent evidence: coupled utilization, maximum axial stress/displacement/temperature, nodal fields, edge forces/heat flux, recovered reactions, force/heat/energy residuals, refinement/reference disagreement, process-envelope result, CAD/mass burden, survivor count, proxy false-negative/positive accounting และ compute
- Controls: external terminal ancestry/roles, load/heat histories, material law, process envelope, evaluator identities, numerical levels, training/holdout split, optimization opportunity, thresholds, archive rules, random streams, hardware/concurrency declaration และ total treatment/seed budgets
- Preferred hypothesis: generation-first treatments สร้าง previously undeclared multifunctional candidate อย่างน้อยหนึ่งตัวที่ผ่าน registered subsystem task โดยไม่ละเมิด conservation, numerical, process, holdout หรือ replay
- Competing explanations: gain ที่เห็นมาจาก radius/mass advantage, task/controller loophole, singular network, proxy error, unequal compute, CAD/field identity mismatch หรือ threshold ที่เลือกหลังเห็นผล
- Falsification: sever paths และเปลี่ยน boundary/material/evaluator identities; ตรวจ analytical series/parallel networks; บังคับ independently recovered reactions และ energy; promote score-independent proxy samples; เก็บ failures/unresolved results; ห้ามเปลี่ยน frozen thresholds หลัง admitted outcomes

## Registration และ observation boundary

จะคำนวณ implementation/validation hashes หลัง code/tests มีอยู่ ก่อน admitted run ต้องตรึง final registration พร้อม hashes เหล่านั้น รวม task, material, representation, operator และ environment identities Development tests และ threshold calibration ใด ๆ เป็น software/calibration evidence เท่านั้น ห้าม relabel เป็น untouched training/holdout evidence เมื่อ freeze admitted registration แล้ว numerical thresholds, paired seeds, treatment rules และ holdout conditions เปลี่ยนไม่ได้ใน work item นี้

Primary numerical evaluator ใช้ subdivision levels ที่เพิ่มขึ้นและรายงาน full scalar-network fields ส่วน reference evaluator ใช้ exact resistance integration สำหรับ linear radius variation ทั้งสองอาจใช้ linear-algebra library เดียวกัน จึงเป็น cross-method corroboration ไม่ใช่ independent software stack หรือ physical experiment Stronger independent promotion ยังคงเป็น Work 101

## Validation และเกณฑ์สำเร็จ

1. รัน `python -m unittest tests.test_functional_discovery -v`; ตรวจ equations เทียบ closed-form series/parallel cases, fields/reactions/residuals, three refinements, exact-reference disagreement, treatment replay, process envelope, identity binding และ negative admission
2. รัน targeted regressions สำหรับ Works 098–100 และ morphology/topology/geometry behavior
3. Freeze และ validate final `admitted_simulation` registration ก่อน execute `artifacts/work100/run_a`; บันทึก SHA-256 และยืนยัน implementation/validation source hashes ตรงกับไฟล์ที่ execute
4. Execute admitted runs A/B แยกกันด้วย pinned CadQuery environment เทียบ deterministic CAD/field/selection/survivor evidence ภายใต้ registered tolerances โดยรายงาน timing แยก เปิด ledger แต่ละชุดใหม่ที่ trusted head
5. รัน `python -m compileall -q src scripts tests` และ `python -m unittest discover -s tests -q` พร้อม durable exit evidence
6. ตรวจ bilingual files/local links/technical tokens, รัน `git diff --check`, stage เฉพาะไฟล์ที่ประกาศ ตรวจ exact cached scope รัน `git diff --cached --check`, commit ทันที และ verify commit hash

Success ต้องมี previously undeclared candidate อย่างน้อยหนึ่งตัวผ่าน preregistered subsystem survivor gates ทั้งหมด พร้อม causal geometry/field evidence และ accounting ที่ admissible หากไม่มี survivor Work 100 ยัง complete เป็น negative trial ได้เฉพาะเมื่อ implementation, registration, falsification และ evidence gates ผ่านโดยไม่ลด criteria Validation/commit ที่ล้มเหลวทำให้งานคง `In progress` หรือเป็น `Stopped` พร้อม blocker ตรงจริง

## ความเสี่ยง การควบคุม และสิ่งที่ไม่ทำ

ความเสี่ยงคือเรียก scalar network ว่า full 3D mechanics, ใช้ synthetic material assumptions เป็น real validation, ปรับ threshold หลังเห็นผล, singular/disconnected graphs, proxy exploitation, controller สร้าง energy, hidden CAD repair และ admitted label หลุด scope ควบคุมด้วย one-dimensional axial/conduction equations ที่ระบุชัด, material-model scope, frozen registration, terminal ancestry, conservation/energy residuals, exact-reference comparison, score-independent audit, immutable ledger identities, no hidden repair และ survivor wording ที่แคบ

ไม่ทำ full 3D elasticity/contact/CFD, nonlinear failure, fatigue/fracture, arbitrary material distribution, manufacturing proof, race completion/time, optimized conventional vehicle baselines, whole-vehicle energy/race integration, `promotion_ready`, real-world novelty, physical validation, distributed scheduling, external publication หรือ push Work 101 ยังรับผิดชอบ whole-vehicle co-design และ stronger evidence promotion

## ภาคผนวกการรันล่วงหน้าหลัง V1 ที่ freeze แล้วหยุด

Registration V1 (`aa5012d3b0a85b9f6c42b1ede5561681713cb9c9832577f6d2bf88e09d96a871`) ถูก freeze ก่อนการรัน admitted ครั้งแรก การรันนั้นหยุดหลังประเมิน proxy และ refined เพราะผล proxy 8 จาก 10 แบบเป็น `numerically_unresolved` ตามขีดจำกัด refinement change `0.005` ที่ freeze ไว้อย่างตรงไปตรงมา ขณะที่ตัวรายงาน proxy audit ของ Work 098 ต้องการป้าย proxy แบบ Boolean จึงยังไม่มี survivor, contrast หรือผล holdout ใดถูกสร้าง ledger บางส่วนคงอยู่ที่ `artifacts/work100/run_a/` และจะไม่ถูกทำต่อหรือเปลี่ยนป้ายหลักฐาน

ก่อนสังเกต admitted ครั้งใหม่ ให้สร้าง registration V2 แยกต่างหากและใช้โฟลเดอร์ผลลัพธ์ใหม่ V2 ต้องคงเกณฑ์ทางกายภาพ งานทดสอบ seed treatment กฎเลือก audit และขอบเขตคำกล่าวอ้างทุกค่าจาก V1 การเปลี่ยนเฉพาะส่วน execution แบบล่วงหน้าคือ หากป้าย proxy ที่ถูกเลือก unresolved ให้รายงาน `not_estimable_due_to_unresolved_proxy_labels` แบบ deterministic พร้อมจำนวน known/unresolved แทนการแต่งค่า FNR/FPR โดย V2 ต้องมี hash ใหม่ของ runner/test/operator/registration และไม่ใช้หลักฐานจาก V1 ซ้ำ

การควบคุม portability ขั้นสุดท้าย: evaluator identities ใช้ raw file SHA-256 และ Windows checkout นี้เปิด `core.autocrlf` จึงเพิ่มกฎ `.gitattributes` ที่จำกัด path เฉพาะ byte-addressed Work 099/100 sources และ Work 100 records เพื่อป้องกัน clean checkout แปลง committed LF bytes เป็น CRLF แล้วทำให้ frozen registration invalid ทั้งที่เนื้อหาไม่เปลี่ยน
