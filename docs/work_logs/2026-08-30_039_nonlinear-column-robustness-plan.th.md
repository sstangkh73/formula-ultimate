# แผนงาน 039: ความทนทานของผลเสาเชิงไม่เชิงเส้น

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_039_nonlinear-column-robustness-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

ตรวจว่าผล precritical nonlinear amplification จาก Work 038 converge ทางตัวเลขเมื่อ refine mesh หรือไม่ และวัดว่าผลไวต่อรูป initial imperfection ที่ประกาศมากเพียงใด

## ขอบเขตและข้ออ้าง

- ใช้ cantilever column จาก Work 037 และ CalculiX `NLGEOM` evidence route จาก Work 038
- ใช้ absolute compressive load เดียวกันบน coarse, medium และ fine mesh จาก Work 037
- เทียบ cantilever eigenmode-shaped imperfection ที่ยอมรับกับ independent smooth cubic crookedness ซึ่งมี fixed-face offset, fixed-face slope และ free-end amplitude เท่ากัน
- แยก execution/evidence acceptance ออกจาก shape-robustness hypothesis outcome; สมมติฐานที่ถูกหักล้างยังเป็นผลทดลองที่บันทึกได้ ไม่ใช่ solver failure

งานนี้ยังเป็น precritical และ linear elastic ไม่ได้ยืนยัน limit point, post-buckling capacity, yield, fracture, fatigue, safety factor หรือ DNF coupling

## การออกแบบการทดลอง

- ตัวแปรอิสระ: mesh size, imperfection shape และ absolute compressive load
- ตัวแปรตาม: total tip offset, amplification, reaction closure, stress, axial shortening, secant-reference error, mesh-change metric และ shape-sensitivity metric
- ตัวแปรควบคุม: `L,b,h,E,nu`, tip imperfection amplitude, fixed-free support, C3D4 formulation, load distribution, solver version, parsing rule และ absolute load schedule
- execution ผ่านเมื่อ: declared subcritical case ทุกตัว converge พร้อม fresh complete evidence, reaction closure ผ่าน และ response แต่ละชุดเพิ่มตาม load
- numerical hypothesis: eigenmode-shaped response มี last-two-mesh change `<=5%` ที่ admitted load ทุกค่า และตรงกับ Work 037 secant reference ของแต่ละ meshภายใน `15%`
- robustness hypothesis: ที่ fine mesh imperfection shape สองแบบมี amplification ต่างกัน `<=10%`; ถ้าต่างมากกว่านี้ให้ reject robustness แต่เก็บ measured evidence

## Falsification และ control

Absolute load schedule อิง fraction ของ fine-mesh Work 037 eigenvalue เพื่อไม่ซ่อนผล mesh refinement ด้วยการ renormalize load ของแต่ละ mesh Unit test เปลี่ยน shape identity และ reject unknown shape, invalid coordinate และ supercritical secant request ต้องตรวจ Work 037 critical-load table และ source commit ให้ตรงก่อนรัน

## ไฟล์และ validation

เพิ่ม versioned config, shape-aware mesh contract, Work 039 runner/launcher, focused test, bilingual physics report, ignored experiment artifact และ matching bilingual result log รัน focused test, live Work 039, Work 038 regression, full test, compile check, explicit staged check, commit และ clean-tree replay

## ความเสี่ยงและสิ่งที่ไม่ทำ

Cubic imperfection ไม่ใช่ eigenfunction จึงใช้ single-mode secant equation เป็น exact reference ไม่ได้ C3D4 bending stiffness และ mesh asymmetry ยังเป็นคำอธิบายทางเลือก ไม่มี shell/local buckling, residual stress, manufacturing tolerance distribution, nonlinear material, contact, arc-length continuation, whole vehicle, push หรือ publication
