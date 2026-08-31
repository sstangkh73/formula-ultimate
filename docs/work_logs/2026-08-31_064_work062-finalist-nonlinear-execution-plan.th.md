# แผนงาน 064: Work 062 Finalist Nonlinear Execution

สถานะ: หยุด (Stopped) — deterministic verify-only replay เปรียบเทียบ in-memory evidence แบบ tuple กับ strict-JSON evidence แบบ list

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_064_work062-finalist-nonlinear-execution-plan.md`

## วัตถุประสงค์

นำ committed gate `whole_vehicle_geometric_nonlinearity_gate_v1` ไปใช้กับ all and only Work 062 candidates 51 ตัวที่ผ่าน frozen holdout, Work 053 refinement และ STEP/FreeCAD witness เก็บ nonlinear case ทุกกรณีเป็น append-only hash-chained evidence และ adjudicate โดยไม่ retry หรือ silent repair

## แบบการทดลอง

- Independent variable: exact Work 062 finalist geometry; ไม่มี search ใหม่หรือการเปลี่ยน geometry
- Dependent variables: CalculiX nonlinear convergence/confirmation, maximum displacement, maximum surface von Mises stress, linear-reference amplification ratios, yield margin, case status และ candidate status
- Controls: Work 062 stage fingerprint, exact holdout cases สองกรณี, B31 subdivisions ต่อ branch เท่ากับ 16, Work 053 synthetic material, fixed boundary/load mapping, CalculiX identity และ frozen Work 063 thresholds
- Inclusion: candidate IDs ต้องตรงกับ exact intersection ที่แทนด้วย Work 062 refinement-passed และ CAD-witness-passed evidence โดยมี cardinality ที่คาดไว้ 51 Outcomes ห้ามเปลี่ยน set
- Failure: missing/tampered source evidence, identity mismatch, nonzero process exit, ไม่มี `nonlinear geometric` confirmation, non-finite output, threshold violation, incomplete terminal ledger หรือ replay mismatch ต้องมองเห็นและ fail closed

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม `scripts/structural/run_whole_vehicle_nonlinear_gate.py` ที่รองรับ execution, resume, chained ledger, deterministic summary และ verify-only replay
- เพิ่ม focused runner tests
- สร้าง ignored evidence ใต้ `artifacts/work064/`
- หลัง execution เพิ่ม bilingual research result และ Work 064 result documents พร้อมอัปเดต plan status

## Validation และเกณฑ์สำเร็จ

ต้องมี exact source fingerprints, included candidates ไม่ซ้ำ 51 ตัว, unique terminal case results 102, terminal candidate adjudications 51, exact replay fingerprint, explicit pass/failure distributions, focused/full tests, compilation, bilingual records และ post-result-commit clean-tree verify-only replay Candidates ผ่านศูนย์ตัวถือเป็นผลที่ถูกต้องหาก evidence ครบ

## โครงสร้าง commit

งานนี้ตั้งใจใช้สอง commits Commit แรก freeze แผน, runner และ tests ก่อน candidate execution เพื่อให้ run เริ่มจาก clean committed tree Commit ที่สองบันทึก terminal bilingual result หลัง validation ห้ามเปลี่ยน threshold, inclusion rule, code หรือ config ระหว่างสอง commits; หากเปลี่ยนต้องหยุด execution นี้และใช้ work item/protocol identity ใหม่

## ความเสี่ยงและสิ่งที่ไม่ทำ

ความเสี่ยงคือ nonlinear solver nonconvergence, output/parser ambiguity, partial interruption และ low-load insensitivity Resume ทำต่อเฉพาะ missing cases ได้แต่ห้าม retry consumed terminal case Execution นี้ไม่อ้าง buckling certification, solid/contact/material-nonlinear behavior, fracture, fatigue, physical validation, safety, manufacturability หรือ algorithm superiority Independent search replication ยังเป็น work item ภายหลัง
