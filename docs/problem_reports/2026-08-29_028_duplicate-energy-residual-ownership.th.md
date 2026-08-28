# รายงานปัญหา: health adapter ส่ง energy residual ID ซ้ำ

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_028_duplicate-energy-residual-ownership.md`

## ปัญหา

การคำนวณ health จาก Work 027 เก็บ truncated energy residual แล้ว adapter ส่ง residual `energy.*` ซ้ำหลัง energy adapter เผยแพร่ ID เดียวกันแล้ว

## ผลกระทบ

transaction ครบแปด stage ครั้งแรกล้มด้วย `evidence_identity_duplicate` แม้ numerical residual ทุกตัวผ่าน

## การแก้ไข

เก็บ truncated-energy residual ภายใน `CentralHealthEvidence` เพื่อการตรวจสอบ แต่ให้ `health_event_solver` publish เฉพาะ residual `health.*` ที่ adapter เป็นเจ้าของ ส่วน invalidity ยัง fail closed ผ่านสถานะ health result
