# การยอมรับ Eigenvalue Buckling

ไฟล์ต้นฉบับภาษาอังกฤษ: `EIGENVALUE_BUCKLING_ACCEPTANCE.md`

สถานะ: ผ่านสำหรับ Work 037

Work 037 verify ideal linear eigenvalue buckling ของ solid rectangular cantilever column (`L=0.2 m`, `b=h=0.01 m`, `E=70 GPa`, `K=2`) ภายใต้ distributed compression reference `100 N` โดย Euler ให้ `Pcr=3598.2932712304946 N`

| Mesh | Nodes | C3D4 | Pcr (N) | Error | Pair split | Transverse/axial |
|---|---:|---:|---:|---:|---:|---:|
| 1.5 mm | 7,052 | 29,098 | 3852.795 | 7.073% | 0.380% | 24.64 |
| 1.25 mm | 11,702 | 51,221 | 3776.375 | 4.949% | 0.0458% | 24.95 |
| 1.0 mm | 20,514 | 95,711 | 3715.160 | 3.248% | 0.0128% | 25.66 |

Last-two critical-load change เท่ากับ `1.6477%`; static reaction closure ตรงใน printed precision Parse eigenfactor สี่ค่าและ FRD displacement mode Near-degenerate pair แรกกับ transverse-dominant displacement ระบุ bending สองทิศที่คาด Euclidean tip-vector orthogonality ถูกรายงานแต่ไม่ gate เพราะ nearly degenerate eigenspace อาจคืน arbitrary mixed basis; mass/stiffness-weighted MAC เป็นหลักฐานอนาคต

Mesh 3 mm และ 2 mm แรก fail analytical gate 10% เดิม Tension load ให้เฉพาะ negative factor จึง reject ส่วน unclamped model คืน factor ใกล้หนึ่งพร้อม exit `0` อย่างทำให้เข้าใจผิด แต่ admission layer reject เพราะไม่มี required support contract

รัน `scripts\run_work037.ps1` และเปิด `artifacts/work037/fine_1mm/column.frd` ผลนี้เป็นเพียง ideal elastic instability estimate ไม่ใช่ physical capacity ต้องมี geometric imperfection, nonlinear geometry/material response, limit point และ post-buckling ก่อนใช้ใน fitness
