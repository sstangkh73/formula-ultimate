# รายงานปัญหา: ขาด drive-energy transfer

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_027_missing-drive-energy-transfer.md`

## ปัญหา

Work 025 ส่ง braking/recovery energy แต่ไม่มี mechanical wheel energy สำหรับ drive force บวก ทำให้ Work 027 หาความต้องการพลังงานต้นทางไม่ได้โดยไม่สร้างพลังงานจากแรงเอง

## ผลกระทบ

รถสามารถเร่งได้แต่พลังงาน onboard ส่วนกลางไม่ลดลง

## การแก้ไข

เพิ่ม `drive_wheel_energy_j` ราย contact และค่ารวมใน `ContactEnergyTransfers` คำนวณจาก applied positive local longitudinal force, effective radius, wheel angular speed และ executed duration ของ contact พร้อม test สำหรับ zero-drive, positive-drive, saturation และ replay

## ข้อจำกัด

เป็นการประมาณ wheel work แบบ no-slip ส่วน powertrain efficiency และ auxiliary demandอยู่ใน configuration ของ Work 027
