# แผน Work 088: การตรวจ Admission ของ Whole Mechanical Vehicle Candidate 001

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_088_whole-mechanical-vehicle-candidate-001-plan.md`

## สถานะ

สถานะ: Completed

## วัตถุประสงค์

ทำขอบเขตที่เดิมเป็น Work 086 หลังงานแก้ structural ที่แทรกเพิ่มสองงาน โดยประกอบดัชนีหลักฐานทั้ง candidate แบบ immutable และ deterministic จากผล exact ของ Work 083, 084, 086 และ 087 ตรวจ CAD และ report artifact ที่บังคับทั้งหมด ประเมิน whole-vehicle admission case ที่ preregister ไว้ทุกกรณี และตัดสินว่าจะ admit candidate เข้า Level 0 หรือหยุดก่อน simulation ด้วย verdict `not_ready` ที่เครื่องอ่านได้

คาดว่า verdict จะเป็น `not_ready` เพราะ Work 087 บันทึก forbidden geometry interference, motion-interface mismatch, การขาด mesh convergence ของ load frame ใหม่ และ material/process evidence ที่ยังเป็น synthetic การสร้าง verdict แบบ fail-closed ที่ถูกต้องคือเกณฑ์สำเร็จของ audit นี้ ไม่ใช่สิทธิ์ให้เปลี่ยนชื่อ candidate ว่าเป็นรถที่สมบูรณ์

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม `config/candidates/whole_mechanical_vehicle_candidate_001.json` พร้อม source identity, seed, required artifact class, admission case และ evidence policy ที่ตรึงไว้
- เพิ่ม `src/formula_ultimate/experiments/whole_mechanical_vehicle_candidate.py` สำหรับตรวจ schema, identity, artifact, case, blocker และ replay
- เพิ่ม `scripts/candidates/run_whole_mechanical_vehicle_candidate_001.py` เพื่อสร้าง immutable evidence bundle โดยไม่แก้ upstream geometry
- เพิ่ม `tests/test_whole_mechanical_vehicle_candidate_001.py` สำหรับ positive audit, source tamper, missing artifact, blocker suppression, premature simulation, synthetic evidence, case omission และ replay
- เพิ่ม `docs/contracts/WHOLE_MECHANICAL_VEHICLE_CANDIDATE_001.md` และไฟล์ภาษาไทยคู่กัน
- เพิ่มแผน/ผลนี้และไฟล์ภาษาไทยคู่กัน
- สร้างหลักฐานที่ ignore ใต้ `artifacts/work088/`

## ตัวแปรต้น/ตาม ตัวควบคุม และเมตริก

- ตัวแปรต้นจำกัดเฉพาะ frozen evidence bundle และ falsification control ที่ฉีดเข้าไป ห้ามเปลี่ยน geometry parameter ในงานนี้
- ผลลัพธ์ตามคือสถานะ source/artifact identity, readiness ราย case, blocker set, สถานะการรัน Level 0, candidate verdict, bundle identity และ replay equality
- ตัวควบคุม: source identity ที่เปลี่ยนหนึ่งรายการ, artifact ที่หายหนึ่งรายการ, blocker ที่ถูกซ่อนหนึ่งรายการ, forced simulation request หนึ่งครั้ง, evidence class ที่ถูกเปลี่ยนชื่อหนึ่งรายการ, admission case ที่ถูกตัดหนึ่งกรณี และ replay หนึ่งครั้ง
- เมตริก: SHA-256 identity equality แบบ exact, required-artifact coverage, required-case coverage, การคง blocker, `level0_simulation.status`, deterministic result equality และ test exit status

## การตรวจสอบและเกณฑ์สำเร็จ

- ตรวจ STEP แยกชิ้นสิบเจ็ดไฟล์, complete assembly STEP, FCStd, assembly tree, joint/DOF manifest, material manifest, mass/COM/inertia report, interference report, structural report, energy ledger, failure report, replay manifest และ Level-0 decision record
- ประเมิน static support, acceleration, braking, steady cornering, combined braking/cornering, bump/vertical event, torque reaction, thermal-duration, single-connection failure, refinement/replay และ mirrored/control case
- รักษา upstream blocker ทุกตัวและพิสูจน์ว่า admission ที่ถูก block ป้องกันการรัน Level 0
- สร้าง result สองไฟล์ที่เหมือนกันทุก byteจาก config และ source evidence เดิม
- ผ่าน focused test, repository-contract test, compilation และ full regression

## ความเสี่ยง สิ่งที่ไม่ทำ และเงื่อนไขหยุด

ความเสี่ยงได้แก่การนับ report ที่ทำดัชนีแล้วเป็นหลักฐานฟิสิกส์ใหม่ การสับสน audit ที่ถูกต้องกับการ admit รถ การยอมรับ ignored artifact ที่ stale และการปล่อยให้ check ที่ผ่านภายหลังกลบ blocker ตัว runner ต้อง fail closed เมื่อ identity หรือ schema เสีย และคืนผล `not_ready` ที่ถูกต้องเมื่อหลักฐานครบแต่มี blocker

งานนี้ไม่ซ่อม geometry, ไม่สร้าง structural evidence ที่ขาด, ไม่รัน Level-0 simulation ที่ยังไม่ admissible, ไม่ validate วัสดุ, ไม่ยืนยัน crashworthiness หรือ safety, ไม่อ้าง race completion, ไม่ optimize topology และไม่อ้าง physical validation หากตรวจ source identity หรือ required artifact ไม่ได้ ให้หยุด audit เป็น invalid แทนการอนุมานหลักฐานที่หาย
