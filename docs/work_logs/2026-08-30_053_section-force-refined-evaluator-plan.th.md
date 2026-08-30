# แผนงาน 053: ตัวประเมินทั้งคันแบบละเอียดด้วย section force

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_053_section-force-refined-evaluator-plan.md`

## วัตถุประสงค์

แทน observable ของ stress ที่ถูกหักล้างใน Work 052 ด้วย external check ที่ preregister และมีมิติทางฟิสิกส์ตรงกัน: นำ section force/moment resultants จาก CalculiX B31 มาคำนวณ extreme-fiber equivalent stress ด้วยสมบัติหน้าตัดที่ประกาศไว้ จะยอมรับตัวประเมิน stress/deformation แบบอิสระในขอบเขตจำกัดเฉพาะเมื่อ analytical, equilibrium, refinement, cross-model, identity และ negative-control gate ผ่าน

## ขอบเขตและไฟล์ที่วางแผน

- แก้ trailing blank line ที่ `git diff --cached --check` รายงานในผล Work 052 ที่หยุดแล้ว โดยคง commit `37359db` และไม่ amend หรือ rewrite
- เพิ่ม configuration งาน 053 แบบ versioned ที่มีความหมาย output ถูกต้องและตรึง upstream identities
- ทำ project 6-DOF frame model, CalculiX deck/FRD section-resultant parser, candidate-geometry adapter, runner, PowerShell entry point, tests, รายงานฟิสิกส์สองภาษา และ result record สองภาษาให้เสร็จ
- เก็บ raw evidence ที่ถูก ignore ใต้ `artifacts/work053/`

## นิยามการทดลอง

- ตัวแปรอิสระ: geometry ที่ promote จาก Work 050 จำนวน 9 แบบ, frozen Work 048 holdout load case จำนวน 2 กรณี และ B31 subdivisions ต่อ branch เท่ากับ `4/8/16`
- ตัวแปรตาม: maximum displacement จาก project-frame และ CalculiX, section force/moment, extreme-fiber equivalent stress ที่คำนวณ, reaction residual, last-two refinement change, yield margin, solver status และ evidence hashes
- ตัวแปรควบคุม: Work 050 candidate identity และ ancestry เดิม; Work 048 wrench เดิม; SI units; CalculiX 2.22; วัสดุ isotropic สังเคราะห์ `E=70 GPa`, `nu=0.3`, yield stress `250 MPa`; fixed support; square equivalent sections; และไม่อ่าน Work 050 capacity factor
- การแยก external solver: shared node อาจเฉลี่ย section output ของหน้าตัดต่างกัน จึงรัน coupled state เต็มซ้ำหนึ่งครั้งต่อ section output set ทั้งสาม deck คงโครงสร้างและ load ครบ ต่างกันเฉพาะ result set ที่ร้องขอ และ displacement ต้อง replay สอดคล้องกัน
- falsification controls: analytical cantilever, reversed load, zero stiffness, missing restraint, altered identity, DAT/FRD ไม่ครบ, section-output mismatch และหน้าตัดที่จงใจเล็กเกิน

## การตรวจสอบและ gate

1. คำนวณ surface stress จาก CalculiX resultants `N`, `V1`, `V2`, `T`, `M1`, `M2`; ห้ามเทียบ integration-point material stress กับ root surface stress
2. ที่ cantilever mesh ละเอียดสุด displacement/stress จาก project และ CalculiX ต้องต่างจาก `F L^3/(3 E I)` และ `6 F L/b^3` ไม่เกิน `5%`; error ของ CalculiX ต้องลดลงต่อเนื่อง
3. ประเมิน structural state `9 x 2 x 3 = 54` ชุด และรัน section-output deck สามชุดต่อ state รวม candidate CalculiX `162` processes บวก benchmark สาม processes
4. reaction residual ต้อง `<=1e-5`, last-two displacement/stress change `<=5%`, ผล project/CalculiX ที่ mesh ละเอียดต้องต่างกัน `<=8%`, yield margin `>=1.1` และ displacement `<=0.02 m`
5. ต้องมี hash ของ `.inp/.dat/.frd` ที่สร้างใหม่, exact replay identity, focused/full tests, compilation, repository-contract checks, staged-diff แบบ fail-fast, explicit scoped commit และ clean-tree replay

## เกณฑ์สำเร็จ

- observable ที่แก้ไขแล้วผ่านโดยไม่ผ่อน threshold `5%`/`8%` หลังเห็นผล
- candidate/holdout ที่ promote ทุกชุดมีหลักฐานครบและ converge หรือ fail อย่างชัดเจน
- คำตัดสินสุดท้ายกล่าวได้เพียงหลักฐาน linear-elastic beam-network ในขอบเขตจำกัด และไม่อ้างว่า validate solid/contact, nonlinear, crash หรือ hardware แล้ว

## ความเสี่ยงและสิ่งที่ไม่ทำ

B31, rigid joint, square equivalent section, fixed ground, วัสดุสังเคราะห์ และ quasi-static wrench ไม่ครอบคลุม local solid stress concentration, fastener จริง, contact, preload, plasticity, fracture propagation, buckling, vibration, crash, fatigue life, manufacturing variation และ physical calibration งานนี้ไม่รวม arbitrary topology, main research campaign, push หรือ publication
