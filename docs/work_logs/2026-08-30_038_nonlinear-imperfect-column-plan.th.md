# แผนงาน 038: เสาไม่สมบูรณ์แบบเชิงไม่เชิงเส้น

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_038_nonlinear-imperfect-column-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

ตรวจว่าความคดเริ่มต้นที่ประกาศไว้ทำให้แรงอัดตามแกนส่งผลเป็นการเคลื่อนด้านข้างผ่าน geometric nonlinearity ของ CalculiX จริง ก่อนให้ผลที่ไวต่อ instability มีผลต่อ candidate fitness

## ขอบเขตและข้ออ้าง

- ใช้ physics ของ cantilever solid column และ C3D4 route จาก Work 037
- ใส่ imperfection รูป first mode ของ cantilever แบบ deterministic หลาย amplitude
- แก้หลาย subcritical load fraction ด้วย `NLGEOM` แล้วเทียบ total tip offset และ amplification กับ elastic secant-column relation โดยใช้ eigenvalue ของ mesh เดียวกันจาก Work 037 เป็น numerical reference
- Gate force/reaction closure, solver completion, monotonic response, cross-amplitude consistency, analytical agreement และ artifact freshness

งานนี้ตรวจเฉพาะ precritical geometric-nonlinearity และ imperfection sensitivity ไม่ได้ยืนยัน post-buckling capacity, collapse load, allowable load, yield, fracture หรือ fatigue

## การออกแบบการทดลอง

- ตัวแปรอิสระ: initial tip imperfection amplitude และ compressive load fraction
- ตัวแปรตาม: incremental/total lateral tip offset, amplification factor, secant-reference error, axial shortening, stress, reaction closure, convergence status และ artifact hash
- ตัวแปรควบคุม: `L,b,h,E,nu`, cantilever support, C3D4 mesh, load distribution, solver version, imperfection shape และ parsing rule
- falsification: perfect symmetric control ต้องไม่สร้าง material lateral motion เองก่อน critical load; geometrically linear control ต้องไม่ผ่าน nonlinear amplification response ที่กำหนด; malformed หรือ stale solver evidence ต้องถูก reject

## Analytical reference และ gate ที่เสนอ

สำหรับ mode-shaped imperfect elastic column ใช้ `A(P)=1/(1-P/Pcr)` เป็น precritical secant amplification reference โดย total free-end offset `e(P)=e0*A(P)` ค่า numerical `Pcr` ผูกกับ mesh เดียวกันจาก Work 037 และเก็บค่า Euler เป็น comparison แยก Proposed gates ได้แก่ reaction residual `<=1e-5`, amplification เพิ่มตาม load, normalized response spread ระหว่าง admitted imperfection amplitudes `<=10%` และ secant-reference relative error `<=15%` ใน subcritical range ที่ประกาศ

## ไฟล์และ validation

เพิ่ม versioned config, nonlinear-imperfection contract/runner, launcher, focused tests, bilingual physics report, experiment artifact และ matching bilingual result log รัน focused test, live Work 038, Work 037 regression, full tests, compile check, staged diff check, explicit commit และ clean-tree replay

## ความเสี่ยงและสิ่งที่ไม่ทำ

Load-controlled static analysis อาจผ่าน limit point ไม่ได้, tetrahedral bending stiffness อาจทำให้ amplification bias และ imperfection ใหญ่อาจออกจาก small-deflection secant regime ข้อจำกัดเหล่านี้ต้องเป็น observable output ไม่ใช่ค่าที่แก้เงียบ ๆ ไม่มี arc-length continuation, plasticity, contact, local shell buckling, fracture, fatigue, whole vehicle, push หรือ publication
