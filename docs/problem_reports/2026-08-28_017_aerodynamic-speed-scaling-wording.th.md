# รายงานปัญหา Work 017: ถ้อยคำ Aerodynamic Speed Scaling

ต้นฉบับภาษาอังกฤษ: `2026-08-28_017_aerodynamic-speed-scaling-wording.md`

สถานะ: Resolved

## ปัญหา

แผน Work 017 รุ่นแรกเรียกการตรวจแรง aerodynamic ว่า "inverse-square force
scaling" ซึ่งผิดทางฟิสิกส์สำหรับ quasi-steady coefficient model ที่ประกาศ
เมื่อ density, reference geometry และ coefficient คงที่ แรง aerodynamic แปรผัน
ตามกำลังสองของ airspeed ไม่ใช่ส่วนกลับกำลังสองของ airspeed

## สาเหตุราก

ถ้อยคำที่ตั้งใจคือ "speed-squared scaling" แต่คำว่า "inverse" ถูกใส่ระหว่าง
ร่างขอบเขต test สมการในแผนเดียวกันใช้ dynamic pressure
`q = 0.5*rho*V^2` ที่ถูกต้องอยู่แล้ว

## การแก้ไข

แผนทั้งสองภาษาเปลี่ยนเป็น "speed-squared force scaling" Implementation และ
test ใช้ความสัมพันธ์ `V^2` ที่ประกาศ โดยไม่มีกฎ inverse-speed

## การยืนยันที่กำหนด

Analytical test และ validator ของ Work 017 ต้องเปรียบเทียบจุดที่เหมือนกันนอกจาก
speed ที่ `20 m/s` กับ `40 m/s`: ขนาด force/moment ต้องมี ratio `4` ขณะที่
ram-air mass flow ต้องมี ratio `2`

ปัญหาถ้อยคำนี้พบก่อนเขียน aerodynamic implementation จึงไม่มี physics code หรือ
evidence ที่สร้างด้วยกฎผิด
