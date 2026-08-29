# แผนงาน 037: การตรวจ Eigenvalue Buckling

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_037_eigenvalue-buckling-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

ตรวจ installed CalculiX linear-buckling route เทียบ Euler column ก่อนให้ผล buckling มีผลต่อ candidate fitness

## ขอบเขตและข้ออ้าง

- ใช้ slender solid rectangular cantilever column พร้อม declared effective-length factor `K=2` เพื่อไม่แกล้งเรียก solid-face constraint ว่า ideal pin
- สร้าง C3D4 mesh สามระดับ ใส่ finite distributed compressive reference load ขอ lowest four buckling factors parse fresh eigenvalue/mode evidence และเทียบ `Pcr = pi^2*E*I/(K*L)^2`
- Gate load/reaction identity, lowest positive global bending mode, orthogonal near-degenerate mode pair, analytical error และ mesh convergence
- เก็บ exact tool, deck, output, hash, failure และ deterministic replay

ผลนี้ verify เฉพาะ ideal linear elastic eigenvalue buckling ไม่ใช่ allowable load หรือ physical capacity ต้องมี work item แยกสำหรับ nonlinear geometry พร้อม seeded imperfection และ post-buckling response

## การออกแบบการทดลอง

- ตัวแปรอิสระ: mesh size สามระดับ
- ตัวแปรตาม: buckling factor/load, mode order และ transverse/axial mode content, reaction closure, volume, convergence, solver status, artifact และเวลา
- ตัวแปรควบคุม: `L,b,h,E,nu`, fixed-free support, `K=2`, reference compression, element type/order, solver/parsing rule
- falsification: กลับ load เป็น tension แล้วต้องไม่มี admitted positive compression mode; เอา clamp ออกแล้วต้อง reject; เปลี่ยน `L,E,I` ใน analytical unit test

## Analytical reference และ gate

สำหรับหน้าตัดสองแกนเท่ากัน `I=b*h^3/12` และ `Pcr=pi^2*E*I/(2L)^2` Physical mode สองตัวแรกควรเป็น near-degenerate orthogonal bending pair Gate ที่เสนอ: first-mode load error `<=10%`, last-two change `<=5%`, pair split `<=5%`, reaction residual `<=1e-6` และ mode transverse-to-axial amplitude ratio `>=10`

## ไฟล์และ validation

เพิ่ม versioned config, buckling contract/parser/runner, launcher, tests, bilingual physics report และ matching result log รัน focused test, live Work 037, Work 034-036 regression, full tests, compileall, diff check, explicit commit และ clean-tree replay

## ความเสี่ยงและสิ่งที่ไม่ทำ

C3D4 bending stiffness/faceted geometry อาจต้อง refine Eigenvalue sign/order และ `.dat/.frd` format ขึ้นกับ solver versionจึงต้อง fail closed ไม่มี imperfection, nonlinear collapse, local shell buckling, yield, fracture, fatigue, safety factor, whole vehicle, push หรือ publication
