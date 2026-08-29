# รายงานปัญหา: baseline contact state ใช้ positional field ผิดช่อง

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_029_contact-runtime-positional-order.md`

## ปัญหา

campaign Work 029 รอบแรกสร้าง `ContactRuntimeState` แบบ positional และใส่อุณหภูมิ brake ที่ตั้งใจเป็น `300 K` ลงใน `suspension_travel_m` ทำให้ initial travel เป็น `300 m`

## ผลกระทบ

run ทุก circuit/seed fail-closed ที่ `contact_limit_solver` ก่อน commit แรก พร้อมเหตุผล `suspension_travel_m is outside declared travel limits`

## การแก้ไข

สร้าง baseline contact state ด้วย keyword argument ชัดเจนสำหรับ travel, angular speed, suspension velocity และ brake temperature โดยไม่ผ่อน tolerance หรือ travel limit
