# รายงานปัญหา: weather contract แทน synthetic control ไม่ได้

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_029_synthetic-weather-evidence-vocabulary.md`

## ปัญหา

`WeatherStepEvidence.status` ยอมรับเพียง `observed` หรือ `missing` ทำให้ controlled analytical baseline ต้องติดป้าย synthetic weather ผิดเป็น observed หรือหยุดก่อน simulation

## ผลกระทบ

การติดป้ายผิดจะทำให้ proxy campaign ของ Work 029 ดูเหมือนมี measured local weather evidence และอาจถูกใช้สนับสนุน real-circuit admission อย่างไม่ถูกต้อง

## การแก้ไข

เพิ่มสถานะ `synthetic_control` และให้ aerodynamic adapter รับสถานะนี้ โดยต้องมี field SI ครบและ finite เช่นเดียวกับ observed record แต่รักษา identity และ fingerprint แยก เอกสารกับ test ห้ามตีความสถานะนี้เป็น observation หรือหลักฐานสนามจริง
