# ผลงาน 036: Solid-Shaft Torsion

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_036_solid-shaft-torsion-result.md`

สถานะ: เสร็จสมบูรณ์

Implement versioned torsion fixture, consistent pure-torque surface load, least-squares twist gauge, reaction torque, signed shear-vector field gate, three-mesh convergence, `-T`, `2T`, doubled-modulus และ unrestrained negative-control case พร้อม configuration, structural contract, runner, launcher, test และ bilingual physics evidence

Accepted fine result: 8,967 nodes, 44,200 C3D4, twist `0.002293104622232224 rad` (error 3.023%), shear RMS error 8.932%, correlation 0.996165, force closure `1.52e-13`, moment closure `7.02e-9` Metamorphic residual ทุกค่าต่ำกว่า `1.1e-8`; unrestrained run ถูก reject เพราะ unbounded rigid-body displacement

รายงานเก็บ failed attempt: coordinate serialization ยาวเกินทำให้ CalculiX reject input, coarse mesh sequence fail twist/stress gate เดิม และ CalculiX exit `0` บน singular negative control ทำให้ต้อง reject จาก displacement evidence

Validation คืน exit `0`: focused `16 tests`, live Work 036, Work 035/034 regression, full `284 tests in 46.474s`, compileall, `git diff --check`, explicit staging และ `git diff --cached --check` โดยรายงาน commit hash ใน final handoff

ข้อจำกัดอยู่ใน `SHAFT_TORSION_ACCEPTANCE.md`; ไม่อ้าง nonlinear failure capability
