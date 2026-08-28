# รายงานปัญหา Work 025: นับ Brake Energy เกินหลัง Combined Tyre

ต้นฉบับภาษาอังกฤษ: `2026-08-28_025_combined-tyre-brake-energy.md`

สถานะ: Resolved

## ปัญหา

Implementation Work 025 รุ่นแรกที่ผ่าน test evaluate brake/regen energy ก่อน
combined tyre ellipse เมื่อ lateral demand พร้อมกันลด longitudinal brake force แต่
recovered energy และ mechanical heat ยังอิง torque ก่อน ellipse ที่มากกว่า

## ผลกระทบ

Force saturation แสดงชัด แต่ wheel energy removal, storage recovery, loss, heat
และ brake temperature อาจมากกว่า torque ที่ถ่ายทอดลงถนนจริง

## การแก้

ใช้ brake evaluation สอง pass deterministic: หา subsystem torque capacity ก่อน,
project force พร้อม lateral demand ผ่าน tyre ellipse แล้ว rerun suspension/brake/
regen และ thermal integration ด้วย projected brake torque เก็บ requested torque
เดิมลบ final applied เป็น unserved และไม่ redistribute พร้อมเพิ่ม energy/force
consistency regression

## Validation

Regression combined braking/steering พิสูจน์ทุก contact ว่า
`wheel_energy_removed = abs(applied_Fx) * effective_radius * omega * duration`
Brake demand เดิมที่ tyre ส่งไม่ได้ยังอยู่ใน unserved torque Focused 11/11,
repository 207/207 และ validator ผ่าน
