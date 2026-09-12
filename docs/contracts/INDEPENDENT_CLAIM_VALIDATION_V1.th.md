# การตรวจสอบ Claim แบบอิสระ V1

แหล่งภาษาอังกฤษ: `INDEPENDENT_CLAIM_VALIDATION_V1.md`

สถานะ: Work 129 นำไปใช้เป็นด่าน claim เชิงตัวเลขแบบ independent code path

## ขอบเขตหลักฐาน

claim สำคัญด้าน paired time, source energy, thermal margin และ structural margin ถูกคำนวณใหม่จาก raw telemetry ที่ล็อกไว้ด้วย backend และ source module ที่ประกาศว่าแตกต่างจาก upstream summary implementation shared-function wrapper ถือเป็น independent ไม่ได้ identity ของ candidate, telemetry และ dependency ถูกตรึงก่อนคำนวณ และเปรียบเทียบ upstream conclusion หลังผลอิสระมีอยู่แล้วเท่านั้น

interpretation ที่แรงกว่าใช้ conservative boundary penalty ที่ลงทะเบียนล่วงหน้าและจำแนก disagreement เทียบ trigger ที่ตรึง known omitted-boundary injection ต้องถูกตรวจพบ shared assumptions และ common-mode uncertainty ยังคงแสดงชัด; code path แยกไม่ใช่ institutional independence

selected claims รอดเมื่อผลที่คำนวณอย่างอิสระถึง threshold ที่ลงทะเบียนโดยไม่มี unresolved discrepancy เท่านั้น Exact replay ต้องได้ result SHA-256 เดิม สัญญานี้แทน measured boundary histories, manufacturing evidence, physical tests, external novelty review หรือ promotion evidence ไม่ได้
