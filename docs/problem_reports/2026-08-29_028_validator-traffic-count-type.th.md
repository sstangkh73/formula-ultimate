# รายงานปัญหา: validator ใช้จำนวนรถรอบข้างเป็น floating point

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_028_validator-traffic-count-type.md`

## ปัญหา

validator แยกของ Work 028 สร้าง isolated-traffic evidence ด้วย `nearby_vehicle_count = 0.0` ขณะที่ typed input contract กำหนดให้เป็นจำนวนเต็มที่ไม่ติดลบ

## ผลกระทบ

validator หยุดก่อน execute coupled race จึงยังสร้างหลักฐานอิสระไม่ได้ แม้ focused test จะผ่านแล้ว

## การแก้ไข

เปลี่ยน fixture ของ validator ให้ใช้จำนวนเต็ม `0` โดย production type contract ยังคงเข้มงวดและไม่ได้เพิ่ม implicit coercion
