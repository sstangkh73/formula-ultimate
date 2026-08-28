# รายงานปัญหา Work 024: Aerodynamic Query Roundoff ที่ Exact Node

ต้นฉบับภาษาอังกฤษ: `2026-08-28_024_aero-query-roundoff.md`

สถานะ: Resolved

## ปัญหา

Regression ENU-to-body ที่ vehicle yaw `pi/2` ควรได้ aerodynamic yaw ศูนย์ตรง แต่
floating-point rotation ให้ประมาณ `1e-16 rad` ทำให้ yaw map node เดียวที่ `0.0
rad` reject raw value ว่าอยู่นอก envelope อย่างถูกต้องตาม contract เดิม

## ผลกระทบ

Map ไม่ได้ clamp ผิด แต่ coupling layer แยก coordinate-transform roundoff ออกจาก
query นอก envelope ที่มีความหมายไม่ได้ Exact physical node จึงอาจ fail ตาม
trigonometric roundoff

## การแก้

Snap derived query เข้า declared map node เฉพาะใน relative/absolute tolerance
`1e-12` พร้อมเก็บ raw/query airspeed/yaw และชื่อแกนที่ snap ใน
`AerodynamicQueryEvidence` ค่าเกิน tolerance ยัง invalid และไม่ clamp

## Validation

Regression เก็บ raw yaw ที่ไม่เป็นศูนย์, บันทึก `yaw_angle` ใน snapped-axis tuple,
query `0.0 rad` ตรงและผ่าน ขณะที่ query `40 m/s` ซึ่งอยู่นอก tolerance ของ node
`30 m/s` ยัง invalid พร้อม write ศูนย์ Focused 10/10 และ repository 196 รายการผ่าน
