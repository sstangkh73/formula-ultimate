# แผน Work 105: Survivor Causality และ Whole-Vehicle Integration Intake V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-07_105_survivor-causality-integration-intake-plan.md`

วันที่: 2026-09-07 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต milestone

เดินหน้า roadmap milestone Work 101 ด้วย implementation phase แรกแบบมีขอบเขต Work 100 สร้าง axial/thermal subsystem survivors สิบรายการ แต่ graph-only และ joint candidates ต่างจาก fixed topology หลัก ๆ ด้วยกิ่งที่แทบไม่มี source-to-sink flow Work 105 จะแยก declared graph diversity ออกจาก task-relevant functional causality รับเฉพาะ typed subsystem evidence เข้า whole-vehicle intake registry และ fail closed เมื่อขาดหน้าที่ของรถหรือ stronger promotion evidence

งานนี้จะไม่ประกอบหรืออ้าง complete vehicle Roadmap Work 101 exit condition ยังคงไม่ผ่านจนกว่า candidate ครบทั้งคันในอนาคตจะมีทุก required functional domain, causal path, geometry/material applicability, transient/energy/contact/failure evidence, holdout, independent higher fidelity, safety และ fair optimized-baseline comparison

## ขอบเขตและไฟล์ที่วางแผน

- `src/formula_ultimate/experiments/integration_intake.py`: validate intake config/result แบบเข้ม, รวม mechanical/thermal edge flow, ตัด inactive branches, สร้าง active-path identities, เปรียบเทียบ candidate แบบ paired กับ fixed control, รักษา survivor evidence พร้อมจำแนก functional-mechanism, shape-response และ inactive-topology cases และคำนวณ technology-neutral vehicle capability coverage/blockers
- `config/experiments/work101_integration_intake_v1.json`: freeze Work 100 registration/result identities, flow/activity tolerances, meaningful-effect threshold, capability vocabulary, evidence requirements และ claim boundary
- `scripts/experiments/run_integration_intake.py`: อ่าน ignored Work 100 admitted result ตรวจ identities สร้าง deterministic intake evidence ปฏิเสธ overwrite และรองรับ exact replay
- `tests/test_integration_intake.py`: ทดสอบ nonzero-flow aggregation, dangling-branch pruning, paired fixed comparison, tampering, incomplete capability coverage, missing stronger evidence, false whole-vehicle admission และ deterministic replay
- `docs/contracts/WHOLE_VEHICLE_INTEGRATION_INTAKE_V1.md` และ `.th.md`: definitions, decision rules, evidence result และ limitations
- แผนสองภาษานี้และผลสองภาษาที่เข้าคู่ Generated reports ยังถูก ignore ใต้ `artifacts/work105/`

## ตัวแปร การควบคุม และการหักล้าง

- Independent evidence: treatment และ paired seed จาก Work 100; declared เทียบกับ active edge topology; candidate capability declarations; การมี survivor, independent, safety, transient, energy, contact, failure, holdout และ optimized-baseline evidence
- Dependent evidence: edge flow fractions, active mechanical/thermal/coupled edge sets, active-path identity, response difference จาก paired fixed control, mechanism classification, capability coverage, missing evidence classes, integration status และ Work 101 milestone readiness
- Controls: exact Work 100 V2 registration/deterministic identities, ไม่ mutate source candidates, ใช้ registered load/heat tasks เดิม, fixed activity tolerance, fixed minimum meaningful effect, technology-neutral `REQUIRED_CAPABILITIES` เดิม, ไม่มี holdout feedback และ deterministic ordering
- Preferred hypothesis: Work 100 survivor อย่างน้อยหนึ่งรายการมี task-relevant active-path change และเข้า whole-vehicle integration เป็น supported typed subsystem ได้
- Competing explanations: novelty ที่เห็นเป็น zero-flow appendage, identifier-only graph change, continuous-radius response variationต่ำกว่า meaningful-effect threshold, numerical noise หรือ vehicle capability/evidence coverage ไม่ครบ
- Falsification: ใส่ added edge ที่ high-flow แล้ว active identity ต้องเปลี่ยน; ใส่เฉพาะ zero-flow branch แล้วต้องถูกตัด; เปลี่ยน source identityแล้วต้อง reject; ลบ required capability/evidence class แล้ว integration ต้องยัง blocked; ห้ามเปลี่ยน subsystem survivor เป็น `promotion_ready` หรือ whole-vehicle admission

## กฎการตัดสินใจที่ freeze

Original edge active ในหนึ่ง domain เฉพาะเมื่อ maximum absolute segment flow หารด้วย registered applied input มากกว่า relative activity tolerance ที่ freeze Coupled active edgeต้อง active ทั้ง mechanical และ thermal Active-path identity ไม่รวม refinement node labelsและ zero-flow appendages Graph-diverse survivorเป็น functional-mechanism candidate เฉพาะเมื่อ active coupled topology ต่างจาก paired fixed control และ registered response difference มากกว่า meaningful-effect threshold Same-active-topology geometry ที่ response วัดได้แต่ต่ำกว่า threshold คงเป็น shape-response variant ไม่ใช่ mechanism ใหม่

Whole-vehicle intake ใช้ functional capabilities ไม่ใช้ชื่อ component หรือ layout รถที่กำหนดล่วงหน้า Work 100 subsystem ให้ได้เฉพาะ `load_structure`; axial conduction อย่างเดียวไม่ได้พิสูจน์ `heat_rejection` การขาด energy storage/conversion/transmission, ground propulsion, direction control, braking, heat rejection และ controller ทำให้ assembly ถูก block การขาด independent, safety, transient, energy, contact, failure และ optimized-baseline evidence ยัง block stronger promotion แม้ local survivor gates ผ่าน

## Validation และ success criteria

1. รัน focused unit tests สำหรับ causality, identity, tamper rejection, coverage และ replay
2. รัน Work 105 reports A/B จาก exact Work 100 V2 admitted result และบังคับ byte-identical deterministic evidence
3. รัน targeted regressions สำหรับ Works 098-100, functional vehicle architecture และ integration/promotion contracts
4. รัน `python -m compileall -q src scripts tests` และ full repository suite
5. ตรวจ bilingual companions, Markdown links, JSON/config identities, `git diff --check`, exact staged scope และ `git diff --cached --check`

Work 105 สำเร็จเมื่อ gate แสดง causal distinction และ integration blockers จาก Work 100 อย่างชัดเจน ทำซ้ำได้ และ fail closed Negative intake result เป็นผลที่คาดและยอมรับได้หากหลักฐานไม่พบ active-topology mechanism หรือ complete capability set ห้ามลด threshold เพื่อสร้าง integration-ready candidateเทียม

## ความเสี่ยงและสิ่งที่ไม่ทำ

ความเสี่ยงคือถือ floating-point flow เล็กมากว่าเป็น function, สับสน geometry response กับ mechanism novelty, กำหนด conventional hardware ผ่าน capability labels, ใช้ local artifact ซ้ำโดยไม่ตรวจ identity หรือเรียก coverage audit ว่า whole-vehicle physics ควบคุมด้วย relative flow thresholds, paired fixed controls, technology-neutral functional roles, content-addressed input evidence และ missing-evidence output ที่ชัดเจน

ไม่ทำ new CAD generation, candidate mutation, whole-vehicle assembly, transient lap execution, FEA/contact/CFD, material/process certification, performance optimization, baseline superiority, prior-art novelty, `promotion_ready`, complete-vehicle research admission, physical validation, external publication หรือ push
