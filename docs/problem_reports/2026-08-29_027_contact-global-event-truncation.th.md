# รายงานปัญหา: contact event ไม่ตัด peer contact พร้อมกัน

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_027_contact-global-event-truncation.md`

## ปัญหา

Work 025 ประเมินแต่ละ contact แยกตลอด requested duration หาก suspension หรือ brake หนึ่งตัว fail ก่อน contact อื่นยังสะสมแรง ความร้อน และ recovered energy ต่อถึงปลาย step เดิม

## ผลกระทบ

aggregate contact signal หนึ่งชุดอาจรวมปริมาณที่อินทิเกรตด้วยระยะเวลาทางฟิสิกส์ต่างกัน

## การแก้ไข

ประเมินครั้งแรกเพื่อหา positive contact failure ที่เร็วสุด แล้ว rerun contact ทุกตัวแบบ deterministic ด้วยระยะเวลาสั้นร่วมกัน `ContactEnergyTransfers` แสดง requested/executed duration และ regression fixture ตรวจว่า end time กับ energy ของทุก contact ใช้ event time เดียวกัน

## ข้อจำกัด

เหตุการณ์ที่เกิดตรงเวลาเริ่มต้นถูกแสดงเป็น state invalid/failed ที่มีอยู่ก่อนและไม่ถูก advance
