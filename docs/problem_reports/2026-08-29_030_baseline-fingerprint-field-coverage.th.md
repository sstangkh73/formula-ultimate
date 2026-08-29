# รายงานปัญหา: baseline fingerprint ครอบ field ที่ใช้ promotion ไม่ครบ

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_030_baseline-fingerprint-field-coverage.md`

## ปัญหา

payload ของ run fingerprint ใน Work 029 ไม่รวม field ที่สำคัญต่อ promotion เช่น `real_circuit_admitted` และ static-width status ส่วน campaign fingerprint ก็ยังไม่ verify aggregate consistency แยก

## ผลกระทบ

record ใน memory อาจถูกแก้หลังสร้างแต่ยังถือ fingerprint เก่า ทำให้ promotion gate เชื่อ evidence ที่ admission field ซึ่งมองเห็นไม่ตรงกับ identity

## การแก้ไข

bump baseline campaign evidence เป็น `work029-baseline-campaign-v2`, fingerprint field ของ run/result ทุกตัวนอกจากช่อง fingerprint เอง และเพิ่ม `verify_baseline_campaign_result` เพื่อคำนวณ identity กับ aggregate invariant ซ้ำ Work 030 จะปฏิเสธ campaign evidence เมื่อ verification fail
