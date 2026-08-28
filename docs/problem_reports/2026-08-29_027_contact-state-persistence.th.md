# รายงานปัญหา: contact subsystem state ไม่คงอยู่ข้าม step

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_027_contact-state-persistence.md`

## ปัญหา

`ContactRuntimeState` ไม่มี suspension velocity, brake temperature, recovered contact-store energy และ latched suspension/brake failure ส่วน adapter ของ Work 025 รับ subsystem snapshot ภายนอก จึงอาจนำ state เก่ากลับมาใช้ใน orchestrator หลาย step

## ผลกระทบ

thermal accumulation, regeneration capacity, suspension dynamics และ failure อาจ reset ระหว่าง coupled step แม้ replay metadata ดูถูกต้อง

## การแก้ไข

ขยาย `ContactRuntimeState` แบบ backward-compatible ให้เก็บ persistent state ของ Work 018 ครบ Work 025 ตรวจ external snapshot เทียบ shared stateและสามารถสร้าง snapshot จาก shared state ส่วน Work 027 merge contact end state กลับเข้า shared candidate ถัดไป

## ข้อจำกัด

field เหล่านี้ยังเป็น reduced-order Level-0 state ไม่ใช่สถานะ hardware ที่วัดจริง
