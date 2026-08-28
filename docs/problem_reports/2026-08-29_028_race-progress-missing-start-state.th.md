# รายงานปัญหา: race-progress stage ขาด start state

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_028_race-progress-missing-start-state.md`

## ปัญหา

architecture v3 ไม่ route `state.current` ไป `race_progress_solver`

## ผลกระทบ

adapter คำนวณ fraction ของ finish/timeout crossing หรือยืนยันว่า motion, energy และ health candidate มาจาก start state เดียวกันไม่ได้

## การแก้ไข

เก็บ v3 เดิมและเพิ่ม architecture v4 โดย route `state.current` เข้า race progress และ pin `work028-race-progress-v1`
