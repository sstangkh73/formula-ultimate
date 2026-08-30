# แผนงาน 058: Admitted Bounded Whole-Vehicle Main Campaign

สถานะ: หยุดก่อน execution — Work 057 ไม่ออก burn-in admission และไม่มีการ reserve main-seed opportunity

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_058_admitted-main-campaign-plan.md`

## วัตถุประสงค์

รันและวิเคราะห์ preregistered main campaign `FU-BMC-001` แบบมีเงื่อนไข โดยใช้ code, protocol, adapters, tools และ thresholds exact ชุดเดียวกับที่ Work 057 รับรอง ห้าม reserve main seed ก่อน committed burn-in decision อนุญาต admission

## ขอบเขตและไฟล์ที่วางแผน

- reuse คำสั่งและ committed implementation ของ Work 057 โดยไม่แก้ไข
- สร้าง ignored append-only main ledgers, per-seed promotion/holdout/refinement/STEP-FreeCAD evidence, analysis และ replay manifests ใต้ `artifacts/work058/`
- เพิ่ม main-campaign research/result records สองภาษาและ commit หลัง validation
- หากหลัง admission จำเป็นต้องแก้ implementation/config ให้หยุด `FU-BMC-001` ห้ามซ่อมแล้วทำต่อด้วย campaign ID เดิม

## แบบการทดลองที่ preregister

- Independent variable: proposal treatment (`GRID`, `RANDOM`, `EVOLUTION`)
- Inference unit: paired seed ไม่ใช่ individual attempt
- Paired main seeds: `55001` ถึง `55012`
- Opportunities: `80` ต่อ treatment/seed, `960` ต่อ treatment, รวม `2,880`
- Promotion cap: training-feasible candidates สองตัวต่อ treatment/seed สูงสุด `72`; shortfall ต้องแสดง
- Primary dependent outcome: มี refined-supported finisher อย่างน้อยหนึ่งตัวต่อ treatment/seedหรือไม่
- Secondary paired outcome: best frozen-holdout time บน common-success seeds
- Declared outputs อื่น: failure distribution, training feasible rate, refined survival, mass, energy, stress margin, displacement และ compute cost
- Controls: candidate bounds/component library/constraints/partitions/evaluators ร่วมกัน, attempted-opportunity budget เท่ากัน, paired seeds, GRID opportunities ไม่ซ้ำ, exact ledger/replay, ไม่มี holdout leakage และ Work 057 tool identities ไม่เปลี่ยน

## Preferred hypothesis และ falsification

Primary `H1_EVOLUTION_SUPPORTED_FINISHER_RATE`: `EVOLUTION` มี paired-seed supported-finisher probability สูงกว่า `RANDOM` หาก observed paired rate difference ไม่เป็นบวก ถือว่าขัดแย้ง preferred hypothesis ห้ามแทน endpoint นี้ด้วย attempt-level feasibility

สำหรับ common-success seeds EVOLUTION best holdout time ที่ต่ำกว่าสนับสนุน secondary hypothesis หาก paired median difference เป็นศูนย์หรือบวกจะไม่สนับสนุน GRID comparisons เป็น descriptive และต้องรายงาน preregistered outcomes กับ contradictory evidenceทั้งหมด

## เกณฑ์ admission, สำเร็จ และล้มเหลว

Admission ต้องมี committed Work 057 decision `burn_in_accepted_for_admitted_main_campaign`, exact burn-in replay, protocol/adapters/tool hashes ตรง และ worktree สะอาด

Execution สำเร็จเมื่อมี exactly `2,880` terminal attempts พร้อม equal budgets ต่อ treatment/seed, terminal evidence สำหรับทุก promotion, ไม่มี identity/partition/provenance violation, replay exact และมี final status ที่ประกาศ `completed_without_supported_finisher` เป็นผลวิจัยที่ถูกต้อง

หยุดเป็น `stopped_protocol_violation` เมื่อ identity, leakage, fairness, mutation-after-burn-in หรือ replay ผิด หยุดเป็น `stopped_infrastructure_failure` เมื่อ tools หรือ durable outputs ที่ต้องใช้ unavailable ห้าม retry failed opportunities หรือเปลี่ยน threshold หลังเห็นผล

## การวิเคราะห์

ใช้ analysis seed `551337` รายงาน paired supported-finisher rate difference, exact McNemar result, 95% paired bootstrap interval, common-success paired median best-time difference, exact sign-flip result, 95% paired bootstrap interval, descriptive GRID tables, failure counts ครบ และเลือก winner ด้วย all gates แล้ว minimum holdout time แล้ว candidate ID

## การตรวจสอบและ commit

ตรวจ admitted authorization, immutable identities, ledger counts/fingerprints, GRID uniqueness, promotion caps/shortfalls, terminal downstream evidence, statistical replay, full tests, compilation, เอกสารสองภาษา, explicit staged scope, `git diff --cached --check`, commit และ clean-tree verify-only replay

## ความเสี่ยงและสิ่งที่ไม่ทำ

Campaign อาจใช้ solver time มากหรือจบโดยไม่มี supported candidate งานนี้พิสูจน์ physical validation, safety, manufacturability, real-race superiority, novelty, discovery, arbitrary-topology transfer, certified material allowables หรือ algorithm superiority จาก campaign เดียวไม่ได้ Work 058 ไม่ push และไม่ publish
