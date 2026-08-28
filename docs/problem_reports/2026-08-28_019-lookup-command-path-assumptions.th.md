# รายงานปัญหา Work 019: สมมติฐาน Path ของ Lookup Command

ต้นฉบับภาษาอังกฤษ: `2026-08-28_019-lookup-command-path-assumptions.md`

สถานะ: Resolved

## ปัญหา

Repository probe แบบ read-only ครั้งแรกสมมติชื่อไฟล์ Work 015 ว่า
`tests/test_race_loop.py` และ `scripts/validate_race_loop.py` พร้อมส่ง PowerShell
wildcard เป็น path ให้ `rg` โดยตรง คำสั่งจบ non-zero พร้อม path error สามรายการ

## ผลกระทบ

ไม่มีไฟล์ถูกเปลี่ยนและไม่มี validation result ถูกกลบ ปัญหากระทบเฉพาะการค้น
reference implementation และข้อความ queue

## การแก้ไข

ค้น repository แล้วพบ path จริงคือ `tests/test_race.py` และ
`scripts/validate_race.py` ส่วน queue lookup เปลี่ยนเป็นส่งชื่อไฟล์สองภาษาแบบ
explicit คำสั่งอ่านหลังจากนั้น exit status `0`

## Validation

Probe ที่แก้แล้วแสดง test, validator, race model ของ Work 015 และ queue row Work
019 ทั้งสองภาษา ปัญหาจบแล้วโดยไม่เปลี่ยน product code
