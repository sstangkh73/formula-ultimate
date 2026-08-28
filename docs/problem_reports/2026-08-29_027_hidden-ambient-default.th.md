# รายงานปัญหา: ค่า thermal ambient เริ่มต้นแบบซ่อน

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_027_hidden-ambient-default.md`

## ปัญหา

ร่าง central-health แรกส่ง ambient temperature แบบ hard-code `300 K` เข้า thermal component ทุกตัว เพราะ architecture ของ health stage ไม่รับ environment input

## ผลกระทบ

ผล thermal อาจดูเหมือนมี evidence รองรับแต่จริง ๆ ขึ้นกับ neutral condition ที่ไม่ได้ประกาศ

## การแก้ไข

กำหนด `ambient_temperature_k` เป็น field บังคับที่เป็นบวกและ finite ใน `CentralHealthConfiguration` และบันทึกใน validation fixture โดย solver จะไม่ใส่ thermal ambient กลางแบบซ่อน

## ข้อจำกัด

Work 028 ต้องสร้าง configuration นี้จาก step environment ที่ประกาศอย่างชัดเจน ส่วน calibration กับสภาพอากาศจริงยังไม่มี
