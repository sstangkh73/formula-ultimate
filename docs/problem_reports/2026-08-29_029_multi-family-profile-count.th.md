# รายงานปัญหา: completed profile count นับ family-profile แทน profile

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_029_multi-family-profile-count.md`

## ปัญหา

campaign aggregate รุ่นแรกนับคู่ `(family_id, circuit_id)` ที่จบ แต่เผยค่าเป็น `completed_profile_count` ซึ่งบังเอิญเท่ากับสิบสำหรับ Work 029 ที่มี family เดียว แต่จะนับเกินเมื่อเพิ่ม reference family

## ผลกระทบ

campaign หลาย family ในอนาคตอาจรายงาน profile ที่จบมากกว่าจำนวนจริงใน catalog

## การแก้ไข

นับ circuit profile ว่าจบเมื่อ run ของ family/seed ที่ประกาศทั้งหมดสำหรับ circuit นั้น finish และกำหนด `total_profile_count` เป็นจำนวน profile ใน catalog โดยหลักฐานราย family/run ไม่เปลี่ยน
