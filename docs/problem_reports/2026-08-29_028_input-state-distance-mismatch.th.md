# รายงานปัญหา: race distance ของ input scenario อาจไม่ตรง shared state

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_028_input-state-distance-mismatch.md`

## ปัญหา

input adapter จาก Work 023 ตรวจ race distance ของ scenario เทียบ circuit แต่ไม่บังคับให้เท่ากับ `state.current.race_distance_m`

## ผลกระทบ

whole-race step อาจเลือก spatial/weather evidence ของ station หนึ่งแต่ integrate รถที่อีก station

## การแก้ไข

input bridge บังคับความเท่ากันภายใน `1e-9 m` และคืน invalid พร้อม write ศูนย์เมื่อไม่ตรง พร้อมแก้ analytical fixture เดิมให้ประกาศ state distance ที่ใช้จริง
