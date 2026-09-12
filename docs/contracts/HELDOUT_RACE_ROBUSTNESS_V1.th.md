# ความทนทานในการแข่งแบบ Held-Out V1

แหล่งภาษาอังกฤษ: `HELDOUT_RACE_ROBUSTNESS_V1.md`

สถานะ: Work 128 นำไปใช้เป็นด่าน synthetic holdout ที่ seal

## ขอบเขตหลักฐาน

identity ของ finalist, controller, evaluator, rules และ holdout ถูก seal ก่อนเปิดเผย ตัวระบุ training กับ holdout ต้องไม่ทับกัน finalist ทุกตัวรันทุก condition ที่ลงทะเบียน และ trajectory ที่ไม่จบหรือหยุดยังต้องอยู่ใน telemetry การ tune/repair หลัง exposure, เปลี่ยน source หรือ threshold ทำให้ admitted comparison เป็น invalid

estimand ที่ลงทะเบียนคือเวลาของ fixed-finalist ลบเวลาของ open-finalist สำหรับคู่ที่เข้าเส้นชัย Robust superiority ยังต้องให้ขอบล่างของ uncertainty interval ถึง time improvement ที่ลงทะเบียน, finalist ทุกตัวผ่าน completion rate และผ่าน source-energy, thermal และ structural gates ทั้งหมด Numerical uncertainty ถูกบวกเข้า paired statistical interval ไม่ใช่แก้เงียบ

Exact replay ต้องได้ result SHA-256 เดิม trajectory เหล่านี้เป็น deterministic synthetic evidence; numerical race completion ไม่ยืนยัน manufactured behavior, external novelty, vehicle promotion หรือ physical validation
