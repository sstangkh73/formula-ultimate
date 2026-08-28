# รายงานปัญหา: energy depletion ตรงปลาย step ไม่ถูกสร้างเป็น event

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_028_exact-end-depletion-event.md`

## ปัญหา

Work 027 emit depletion เฉพาะ analytical crossing ที่เกิดก่อนปลาย contact interval แบบ strict การใช้พลังงานหมดตรงปลายจึงได้ energy ศูนย์แต่ไม่มี event candidate

## ผลกระทบ

Work 028 เก็บ exact finish/depletion tie หรือใช้ event priority ที่ประกาศไม่ได้

## การแก้ไข

ถือว่า depletion crossing ที่ปลาย interval หรืออยู่ภายใน `1e-15 s` เป็น candidate `energy_depletion` และ regression ของ race progress พิสูจน์ว่า `finished` ชนะ exact tie โดย tied ID ยังสังเกตได้
