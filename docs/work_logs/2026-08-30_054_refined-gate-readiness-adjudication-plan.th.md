# แผนงาน 054: คำตัดสิน readiness ของรถทั้งคันหลัง refined gate

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_054_refined-gate-readiness-adjudication-plan.md`

## วัตถุประสงค์

แก้ blocker เดียวที่เหลือจาก Work 050 โดยใช้หลักฐาน independent evaluator ที่เสร็จใน Work 053, reject promotion ที่ไม่รองรับโดยไม่ rewrite ผลเดิม และออกคำตัดสิน readiness แบบ deterministic สำหรับ bounded whole-vehicle research campaign

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม adjudication configuration แบบ versioned ที่ตรึง Work 050 ledger/protocol และ Work 053 evaluator implementation/config/replay identity
- เพิ่ม pure adjudicator, fail-closed runner และ `scripts/run_work054.ps1`
- เพิ่ม focused tests, รายงาน readiness สองภาษา และ result records สองภาษา
- เขียน ignored evidence ใต้ `artifacts/work054/`

## นิยามการทดลองและคำตัดสิน

- ตัวแปรอิสระ: refined gate status ของ frozen Work 050 promotions ทั้ง 9 แบบ และ treatment/objective record เดิม
- ตัวแปรตาม: จำนวนที่รองรับแยก treatment, treatment winner, global winner, readiness checks, blockers, decision และ deterministic record hash
- ตัวแปรควบคุม: attempt budget GRID/RANDOM/EVOLUTION เดิม `96/96/96`, Work 050 provenance/exploit/holdout checks ทั้งหมด, Work 053 evaluator identity เดิม, Work 053 pass/fail outcome ที่ไม่เปลี่ยน และ objective value เดิม
- สมมติฐานที่ต้องพยายามหักล้าง: เมื่อตัดเฉพาะสอง candidate ที่ Work 053 reject แล้ว ทุก treatment ยังมี refined-supported promotions อย่างน้อยสองแบบ มี global winner ที่ refined-supported และ readiness checks อื่นยังเป็น true
- falsification: fail closed เมื่อ identity drift, มี Work 050 blocker เพิ่ม, winner ไม่ผ่าน, treatment หาย, treatment ใดมี supported candidate น้อยกว่าสอง, objective เปลี่ยน, refined status เปลี่ยน หรือ replay ไม่ exact

## การตรวจสอบและเกณฑ์สำเร็จ

1. รัน Work 053 ใหม่ ซึ่งรันและ verify Work 050 ภายใน ก่อน adjudication
2. ต้องมี frozen promotions 9 แบบและ original promotions สามแบบต่อ treatment พร้อม candidate identity ตรงกัน
3. join Work 053 ด้วย candidate ID; รับเฉพาะ candidate ที่ผ่านทั้งสอง holdout และคง candidate ที่ reject เป็น contradictory evidence ชัดเจน
4. ทุก treatment ต้องมี supported candidates อย่างน้อยสองแบบ เลือก treatment winner และ global winnerจาก original holdout objective โดยใช้ candidate ID เป็น deterministic tie-break
5. เปลี่ยนเฉพาะ `independent_refined_evaluation` จาก false เป็น true; Work 050 readiness checks อื่นต้องเป็น true อยู่แล้ว
6. คำตัดสินเป็นได้เพียง `ready_for_bounded_whole_vehicle_campaign` ห้ามอ้าง `physically_validated` หรือ engineering discovery
7. รัน focused/full tests, compilation, repository contract, staged checks แบบ fail-fast, explicit scoped commit และ clean-tree replay

## ความเสี่ยงและสิ่งที่ไม่ทำ

adjudication นี้ปิดได้เฉพาะ readiness ของกระบวนการวิจัย ไม่สามารถ validate รถทางกายภาพ, ซ่อม candidate ที่ reject, พิสูจน์ว่า search treatment ใดเหนือกว่า, ขยาย topology, เพิ่ม solid/contact/nonlinear/crash/fatigue evidence, รัน main campaign, push หรือ publish
