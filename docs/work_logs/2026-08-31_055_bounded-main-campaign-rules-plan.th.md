# แผนงาน 055: กติกา bounded main campaign

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_055_bounded-main-campaign-rules-plan.md`

## วัตถุประสงค์

preregister และตรวจด้วยเครื่องกติกาของ bounded whole-vehicle main research campaign แรก โดยตรึง hypothesis, evidence boundary, treatment, paired seed, equal opportunity budget, candidate bound, staged promotion route, statistical unit, outcome hierarchy, failure accounting, stop/go gate และข้ออ้างที่ห้าม ก่อน implement หรือรัน campaign

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม `config/experiments/bounded_whole_vehicle_main_campaign_v1.json` เป็น campaign declaration ที่แก้ไม่ได้ภายในการรัน
- เพิ่ม strict protocol parser/validator ใต้ `src/formula_ultimate/experiments/` และ package exports
- เพิ่ม `scripts/experiments/validate_main_campaign_protocol.py` และ `scripts/run_work055.ps1`; validation เขียน ignored evidenceใต้ `artifacts/work055/` แต่ไม่ประเมิน candidate
- เพิ่ม focused tests, เอกสาร campaign protocol สองภาษา และ result records สองภาษา

## กติกาที่วางแผน

- treatment ยังคงเป็น `GRID`, `RANDOM`, `EVOLUTION` ด้วยตัวแปรแบบ bounded ห้าค่าของ Work 050 และ evaluator opportunity เท่ากัน
- ใช้ paired seeds ใหม่ 12 ค่าและ attempted evaluations 80 ครั้งต่อ treatment/seed: `960` attempts ต่อ treatmentและ `2,880` รวม invalid geometry, numerical failure, structural failure, exploit rejection หรือ DNF ทุกกรณีใช้หนึ่ง attempt
- GRID มีสี่ระดับในห้าตัวแปรจึงมี `4^5=1,024` combinations; GRID opportunities `12 x 80=960` ต้องไม่ซ้ำและห้ามวนกลับ
- promote training-feasible candidates สองแบบต่อ treatment/seed หรือบันทึก shortfall ชัดเจน สูงสุด 72 promotions เข้า frozen holdout และ Work 053 refined evaluation
- seed คือ inferential unit Candidate attempts ภายใน seed ไม่ใช่ independent replicates
- primary outcomes คือการมี refined-supported finisher ต่อ seed และ best frozen-holdout time ต่อ seed Failure ต้องยังมองเห็นและห้ามตัดออกหรือใส่ hidden neutral score
- candidate มีสิทธิ์เป็น winner หลังผ่าน frozen holdout, Work 053 refined stress/deformation, provenance, exploit และ final `3D -> STEP -> FreeCAD` witness gates เท่านั้น

## การตรวจสอบ

1. ตรวจ identity, SI bound, seed uniqueness/exclusion, budget arithmetic, GRID capacity, treatment symmetry, stage order, promotion cap, hypothesis/outcome definition, analysis plan, failure policy และ claim boundary
2. จงใจ reject duplicate/pilot/burn-in seed, GRID overflow, treatment budget ไม่เท่ากัน, failure ไม่ใช้ budget, attempt-level pseudo-replication, threshold ที่เปลี่ยนได้, refined evaluator unavailable และ physical-validation claim
3. รัน focused/full unit tests, Python compilation, repository-contract checks, staged `git diff --cached --check`, explicit scoped commit และ clean-tree protocol replay

## เกณฑ์สำเร็จ

- มี protocol สองภาษาแบบ versioned และสอดคล้องภายในหนึ่งชุดที่ validate แบบ deterministic โดยไม่ประเมิน candidate
- field ที่เปลี่ยน campaign ทุกตัวถูกตรึงและต้องใช้ protocol ID ใหม่หากเปลี่ยนหลังงานนี้
- protocol pin readiness/evaluator evidence identity ปัจจุบันและรับเฉพาะ bounded grammar/load/material domain เดิม
- negative fixtures fail closed สำหรับ exploit หรือ fairness violation ที่ระบุทั้งหมด

## เกณฑ์ล้มเหลว

หยุด Work 055 หากไม่สามารถใช้งบ GRID ที่ไม่ซ้ำพร้อมกับ paired treatment budget อย่างยุติธรรม, pin upstream identity ไม่ได้, outcome hierarchy ทิ้ง DNF/failure เงียบ หรือ validator แยก campaign readiness ออกจาก physical validation ไม่ได้

## ความเสี่ยงและสิ่งที่ไม่ทำ

จำนวน seed และ opportunity budget จำกัด campaign แรกนี้และไม่รับประกัน statistical power สำหรับ effect เล็ก GRID discretization ต่างจาก proposal distribution แบบต่อเนื่องของ RANDOM/EVOLUTION และต้องรายงานเป็นสมบัติของ treatment งานนี้ไม่ implement campaign runner, ไม่ทำ burn-in, ไม่ประเมิน candidate, ไม่เปลี่ยน physics, ไม่ขยาย topology/material/load domain, ไม่อ้าง algorithm superiority, ไม่ push หรือ publish
