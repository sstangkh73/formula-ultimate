# กลยุทธ์ Validation

> ฉบับภาษาไทยของ `VALIDATION_STRATEGY.md`

## ลำดับชั้นของหลักฐาน

ข้ออ้างด้าน validation ถูกจำกัดด้วยชั้นที่แข็งแรงที่สุดซึ่งทำสำเร็จแล้ว:

1. **Structural:** มีไฟล์ schema และ package boundary ครบ
2. **Unit:** สมการ/component แต่ละตัวตรงกับ analytical reference
3. **Invariant:** conservation, bound และ dimensional contract ถูกต้อง
4. **Integration:** component ที่เชื่อมกันและ race loop ทำงานสอดคล้องกัน
5. **Regression:** named reference case ยังเสถียรข้ามการเปลี่ยนแปลง
6. **Numerical:** ผล converge เมื่อปรับ timestep/solver ให้ละเอียดขึ้น
7. **Cross-model:** candidate ที่ promote สอดคล้องกับ independent model
8. **Empirical:** simulation สอดคล้องกับข้อมูลวัดและ uncertainty bound

Initial commit มุ่งเฉพาะ structural validation

## Physics Test ที่จำเป็น

ก่อนใช้ Level 0 สรุปผลวิจัย ต้องมี:

- zero-input rest state
- constant-force analytical acceleration
- drag-only coast-down
- grade equilibrium case
- tyre-force saturation
- source depletion ที่ energy draw ทราบค่า
- ideal lossless energy-chain balance
- lossy chain พร้อมการคิด heat
- reference การเพิ่มอุณหภูมิและ passive cooldown
- การ reject component envelope
- กรณี graph invalidity
- deterministic replay
- timestep refinement/convergence
- การ reject NaN/infinity/negative-state

## Control ของ Experiment

- ใช้ component catalog และ constraint เดียวกันระหว่าง topology treatment
- ใช้จำนวน candidate evaluation หรือ measured compute budget เท่ากัน
- ประกาศ random seed ล่วงหน้าและทำ independent repeat เพียงพอ
- tune fixed-topology baseline ด้วย optimization effort ที่แข่งขันได้
- มี holdout track/configuration ที่ไม่ได้ใช้ระหว่าง search
- รายงาน surrogate prediction พร้อม uncertainty และ audit เป็นระยะด้วย
  authoritative simulator

## การเก็บรักษาหลักฐาน

ทุก result report บันทึก:

- คำสั่ง exact
- เวลาเริ่ม/จบหรือ duration เมื่อเกี่ยวข้อง
- exit code
- output แบบย่อ
- path และ hash ของ generated artifact เมื่อสำคัญ
- Git commit/configuration/seed สำหรับ experiment
- test ที่ fail และข้อจำกัดที่ยังไม่แก้

Artifact ขนาดใหญ่ที่ generate ต้องอยู่นอก Git ภายใต้ `artifacts/` หรือ `runs/`
และเก็บ manifest กับ hash ไว้ใน result log ที่เกี่ยวข้อง

## ภาษาที่ใช้ในการอ้างผล

- “Structurally validated” ไม่ได้หมายความว่าฟิสิกส์ทำงานถูกต้อง
- “Simulation-valid” ไม่ได้หมายความว่าสร้างได้จริงหรือปลอดภัย
- “Promoted” หมายถึงควรทดสอบด้วย model ที่แข็งแรงขึ้น ไม่ใช่พิสูจน์ว่า optimal
- “Discovered” ต้องระบุ design-language version และ comparison baseline
- “Novel” ต้องเปรียบเทียบกับ architecture ที่รู้จักและห้ามตัดสินจากรูปลักษณ์เพียงอย่างเดียว
