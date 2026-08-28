# รายงานปัญหา Work 024: Wind Coordinate Frame หาย

ต้นฉบับภาษาอังกฤษ: `2026-08-28_024_wind-coordinate-frame.md`

สถานะ: Resolved

## ปัญหา

การ review integration Work 024 พบว่า `WeatherStepEvidence.wind_velocity_mps`
ไม่ประกาศ coordinate frame tuple เดียวกันจึงอาจถูกตีความเป็น local ENU หรือ
vehicle-body velocity ทำให้ relative airspeed/yaw ต่างกัน

## ผลกระทบ

Typing และ missing-evidence gate จาก Work 023 ยังถูกต้อง แต่ observed wind มี
semantic กำกวมและไม่ปลอดภัยสำหรับ aerodynamic physics

## การแก้

เพิ่ม `wind_coordinate_frame`; observed evidence ต้องเป็น `local_enu` และ missing
weather ต้องไม่มี field นี้ Work 024 จะ rotate relative ENU air velocity เข้า body
axis ด้วย yaw ใน shared state พร้อม rejection/rotation regression test และอัปเดต
เอกสาร Work 023 สองภาษา

## Validation

Observed wind ที่ไม่มี `local_enu` ถูก reject Regression yaw `pi/2` rotate global
velocity `(0,30,0) m/s` เป็น body-forward `30 m/s` และ evaluate exact map node
Focused Work 023/024 และ repository test 196 รายการผ่านทั้งหมด
