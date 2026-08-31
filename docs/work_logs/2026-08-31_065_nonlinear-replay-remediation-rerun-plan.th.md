# แผนงาน 065: Nonlinear Replay Remediation และ Fresh Rerun

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_065_nonlinear-replay-remediation-rerun-plan.md`

## วัตถุประสงค์

แก้ Work 064 strict-JSON representation defect ภายใต้ execution protocol ใหม่ `work062_finalist_nonlinear_execution_v2` และ campaign `FU-NLG-002` แล้วรัน candidate/holdout cases ใหม่ครบ 102 กรณีจาก clean committed tree โดยไม่ reuse Work 064 observations

## การเปลี่ยนที่ควบคุมไว้

Behavioral remediation เพียงอย่างเดียวคือ canonical strict-JSON round-trip normalization ก่อน summary storage และ comparison เพิ่ม regression test ที่ write/reload tuple-bearing aggregate evidence ข้าม actual JSON boundary ส่วน Work 063 gate configuration, source inclusion, candidate geometries, loads, mesh, material, thresholds, solver, failure policy และ analysis ไม่เปลี่ยนทางวิทยาศาสตร์

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม `config/experiments/work062_finalist_nonlinear_execution_v2.json` พร้อม supersession และ unchanged-science declarations
- อัปเดต `scripts/structural/run_whole_vehicle_nonlinear_gate.py` ให้แยก execution-protocol identity และทำ strict-JSON summary normalization
- อัปเดต focused runner tests ด้วย disk round-trip replay regression และ v2 identity checks
- สร้าง fresh ignored evidence ใต้ `artifacts/work065/`
- เพิ่ม bilingual research/result records และอัปเดต plan หลัง terminal replay

## Validation และเกณฑ์สำเร็จ

ก่อน execution ต้องแสดง v1/v2 scientific-rule equivalence, focused regression tests, full tests และ compilation แล้ว commit plan/code/config/tests จากนั้น execute candidates 51 ตัวและ cases 102 กรณีภายใต้ `FU-NLG-002` Success ต้องมี terminal ledgers, explicit distributions/ranges, exact immediate verify-only replay, bilingual evidence, result commit ที่สอง และ exact post-commit clean-tree replay Physical outcome ที่ pass ศูนย์ตัวยังถือว่าถูกต้องได้

## โครงสร้าง commit ความเสี่ยง และสิ่งที่ไม่ทำ

ต้องใช้สอง commits: commit แรก freeze remediation ก่อน fresh execution และ commit ที่สองบันทึกผล การเปลี่ยน code/config หลังเริ่มจะหยุด `FU-NLG-002` ความเสี่ยงยังเป็น solver/parser failure และ beam-model insensitivity ไม่อ้าง physical validation, buckling certification, material nonlinearity, contact, fracture, fatigue, safety, manufacturability, algorithm superiority หรือ independent search replication
