# ชุดประกอบ Moving Contact V1

ต้นฉบับภาษาอังกฤษ: `MOVING_CONTACT_ASSEMBLY_V1.md`

Status: พัฒนาโดย Work 114 สำหรับชุดประกอบสองพิกัดแบบมีขอบเขต

## ขอบเขตและ dependency

Contract นี้ตรึง Work 113 commit `2c6434bfbc2b1776b2ed922fc9b4084c69c03ff5` และ detailed-connection contract ที่เกี่ยวข้อง ใช้ threaded-reference reduced normal/tangent stiffness, preload `4000 N` และ friction `0.25` โดยไม่แทนค่าเงียบ สมาชิกมวล `0.2 kg` เคลื่อนเฉพาะแกน prismatic ที่ประกาศ; tangential motion เป็น prescribed contact probe

Base ป้อน sinusoidal reversal amplitude `2e-6 m` ที่ `20000 Hz` นาน `0.0005 s` Tangential probe amplitude คือ `1e-7 m` Explicit time steps คือ `5e-7`, `2.5e-7` และ `1.25e-7 s` Unilateral normal penalty contact ใช้ preload compression; reaction คำนวณจาก penetration Coulomb capacity ตัดสิน stick/slip เก็บ opening, closing, slip start/recovery, normal impulse และ deterministic histories เต็ม

## Gates และพฤติกรรมเมื่อไม่ผ่าน

Axial energy ledger มี kinetic/contact/preload energy, base-boundary work และ damping loss Relative energy residual ต้องไม่เกิน `0.12`; constraint drift ไม่เกิน `1e-12 m`; swept clearance ต้องเหลืออย่างน้อย `1e-6 m` Last-two relative changes ของ maximum displacement, maximum contact force และ transmitted normal impulse ต้องไม่เกิน `0.12`

ตรวจ swept clearance ตลอด motion Collision บล็อกเฉพาะ assembly นั้น Rigid/moving conflict และ severed coupling ล้มเหลวแบบปิด Free rigid motion ต้องตรง analytic trajectory การเปิดหรือ slip ทำให้ใช้ Work 113 reduced stick model นอก registered range ไม่ได้ แต่ไม่ลบ detailed event history

งานนี้เป็น bounded axial dynamic model พร้อม prescribed tangential history ไม่ใช่ general 3D collision/contact, flexible-body หรือ full multibody dynamics, complete suspension, crash evidence, vehicle readiness หรือ physical validation
