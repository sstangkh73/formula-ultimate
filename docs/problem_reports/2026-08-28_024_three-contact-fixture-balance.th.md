# รายงานปัญหา Work 024: Baseline Fixture สาม Contact ไม่สมดุล

ต้นฉบับภาษาอังกฤษ: `2026-08-28_024_three-contact-fixture-balance.md`

สถานะ: Resolved

## ปัญหาและผลกระทบ

Test สาม contact รุ่นแรกใช้ตำแหน่ง longitudinal หลัง `-0.667 m` การปัด decimal
ทำให้ baseline load ที่ประกาศมี pitch residual จริง `-1.7658 N*m` จึงถูก
`PlanarVehicle` contract เดิม reject ก่อน coupling ไม่ใช่ fault ของ production
coupling code

## การแก้และ Validation

ใช้ analytical coordinate ตรง `-2/3 m` ซึ่งปิด baseline pitch moment สำหรับ load
split `40%/30%/30%` จากนั้น three-contact aero/load coupling ผ่านพร้อม output สาม
จุด และ focused Work 024 ผ่าน 10/10
