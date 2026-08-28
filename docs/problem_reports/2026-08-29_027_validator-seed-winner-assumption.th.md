# รายงานปัญหา: validator สมมติว่าทุก seed ต้องเปลี่ยนเวลาเหตุการณ์ที่ชนะ

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_027_validator-seed-winner-assumption.md`

## ปัญหา

validator Work 027 รุ่นแรกบังคับว่า seed ต่างต้องทำให้ final execution time ต่าง แม้ deterministic thermal failure ที่เร็วกว่าเป็นผู้ชนะทั้งสองรอบ

## ผลกระทบ

ผล event arbitration ที่ถูกต้องถูกแจ้งว่า validation ล้มเหลว

## การแก้ไข

คง assertion ว่า same-seed replay ต้องตรง exact แต่ตรวจ seed ต่างจาก component reliability draw โดยยอมให้ winning time เท่ากันเมื่อมีเหตุการณ์อื่นที่เร็วกว่าเป็นตัวครอบงำ
