# แผนงาน 041: การตรวจ Near-Critical Mesh และ Element

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_041_near-critical-mesh-element-verification-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

แก้หรือยืนยัน numerical-convergence rejection จาก Work 039 โดยขยาย C3D4 refinement ให้ต่ำกว่า `1.0 mm` และเทียบ independently declared C3D10 route ภายใต้ comparable degree-of-freedom budget

## ขอบเขตและข้ออ้าง

- ใช้ cantilever geometry, synthetic elastic material, fixed support, `e0=0.1 mm` eigenmode imperfection และ fixed absolute compression schedule จาก Work 037-039
- ประเมิน C3D4 mesh size `1.0`, `0.8`, `0.65 mm` และ C3D10 mesh หนึ่งระดับที่เลือกด้วย mesh-only resource pilot ก่อน freeze admitted solver config
- รัน ideal eigenvalue และ precritical `NLGEOM` evidence พร้อมเก็บ exact mesh/deck/result hash และ solver confirmation
- แยก experiment execution จาก convergence hypothesis Hypothesis ที่ถูก reject เป็น measured result ที่ complete และ block promotion ไม่ใช่สิทธิ์ให้ผ่อน gate

งานนี้ตรวจ numerical adequacy เฉพาะ declared precritical column fixture ไม่ validate post-buckling capacity, plasticity, fracture, fatigue, safety หรือ vehicle component ใด

## การออกแบบการทดลอง

- ตัวแปรอิสระ: element family/order, characteristic mesh size และ absolute compressive load
- ตัวแปรตาม: eigenvalue `Pcr`, nonlinear amplification, stress, strain energy เมื่อมี, reaction, solver iteration/status, nodes/DOFs, tetrahedra, wall time, memory proxy และ artifact hash
- ตัวแปรควบคุม: `L=0.2 m`, `b=h=0.01 m`, `E=70 GPa`, `nu=0.3`, fixed-free support, `e0=0.1 mm`, cantilever eigenmode shape, CalculiX/Gmsh version, load distribution, parsing rule และ absolute load `1857.580`, `2600.612`, `3157.886 N`
- falsification: เก็บ load สูงสุด, ใช้ absolute load เดียวกันทุก mesh, reject missing/malformed/non-finite evidence และบันทึก changed mode family/non-convergence

## Gate ที่เสนอ

- static case ที่ admitted ทุกตัวมี complete finite evidence และ reaction residual `<=1e-5`
- last-two C3D4 amplification change `<=5%` ทุก absolute load
- refined C3D4 กับ admitted C3D10 amplification difference `<=5%`
- eigenmode secant error `<=15%` และ lowest physical eigenmode ยังคงเป็น global transverse bending
- C3D10 mesh node count ต้องประกาศหลัง mesh-only pilot และอยู่ภายใน `25%` ของ finest admitted C3D4 node count มิฉะนั้นต้องจัดผลเป็น not compute-comparable อย่างชัดเจน

## Implementation และ validation ที่วางแผน

เพิ่ม element-aware mesh/deck/parser contract, versioned frozen config, Work 041 runner/launcher, focused test, bilingual physics report, ignored solver evidence และ matching bilingual result log ตรวจ element connectivity/order, consistent quadratic-face loading, negative malformed-element fixture, focused/full test, Work 039 regression, compile check, staged diff check, explicit commit และ clean-tree replay

## ความเสี่ยงและสิ่งที่ไม่ทำ

Fine C3D4 eigenvalue extraction อาจใช้ compute/memory สูง Runner ต้อง fail แบบ observable ห้าม coarsen เงียบ ๆ ต้องตรวจ Gmsh/CalculiX quadratic tetrahedral node ordering ก่อน admission Comparable node/DOF count ไม่ได้หมายถึง truncation error เท่ากัน ไม่มี mass optimization, material nonlinearity, interface contact, arc-length continuation, whole vehicle, push หรือ publication
