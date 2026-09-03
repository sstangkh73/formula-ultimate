# Contract การตรวจ Admission ของ Whole Mechanical Vehicle Candidate 001

ไฟล์ต้นฉบับภาษาอังกฤษ: `WHOLE_MECHANICAL_VEHICLE_CANDIDATE_001.md`

Contract นี้แยก audit ที่สำเร็จออกจาก candidate ที่ได้รับ admission ชุดหลักฐานที่สมบูรณ์อาจให้ `audit_status=passed` และ `candidate_verdict=not_ready` ผลนี้คือ audit ที่ถูกต้องและเสร็จสมบูรณ์ ไม่ใช่คำอ้างว่ารถพร้อม

Audit จะล็อก identity ของหลักฐาน Work 083, 084, 086 และ 087 ตรวจ STEP แยกชิ้นสิบเจ็ดไฟล์, assembly STEP และ FCStd สร้าง record ด้าน assembly, interface, material, mass property, interference, structural, energy, failure, replay และการตัดสิน Level 0 ที่บังคับ พร้อมประเมิน preregistered case ทั้งสิบเอ็ดกรณี

การเปลี่ยน source, artifact หาย, ซ่อน blocker, เปลี่ยนชื่อ synthetic evidence, ตัด case หรือพยายามรัน Level 0 ขณะมี blocker ถือเป็น audit error ส่วนหลักฐานที่ครบแต่ให้ผลไม่ผ่านจะคืน `not_ready` และ `level0_simulation.status=not_run_pre_admission_blocked` ด้วย exit code `0` เพราะกระบวนการตัดสินสำเร็จ แม้ candidate จะไม่ผ่านคุณสมบัติ

Audit ไม่ซ่อม geometry ไม่เติมหลักฐานฟิสิกส์ที่ขาด และไม่เปลี่ยน Level-0/component evidence ให้เป็น physical validation
