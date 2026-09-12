# Manufacturing Tolerance Handoff V1

แหล่งภาษาอังกฤษ: `MANUFACTURING_TOLERANCE_HANDOFF_V1.md`

สถานะ: Work 130 นำไปใช้เป็นด่าน route, access และ worst-case tolerance

## ขอบเขตหลักฐาน

ทุก region จาก Work 126 ต้องจับคู่ครั้งเดียวกับ candidate process route, stock/source assumption, tool access และ inspection access ลำดับ dependency ของ assembly ต้องเป็น acyclic order ที่ทำได้ trapped internal core, required feature ที่เข้าถึงไม่ได้ และ assembly reference ที่ไม่รู้จักต้อง fail closed

Clearance ประเมินจาก nominal clearance ลบ feature tolerance ที่ลงทะเบียนทั้งสองฝั่ง Preload ประเมินจาก nominal preload ลบ preload tolerance ที่ลงทะเบียน Nominal-only fit ยืนยัน readiness ไม่ได้ route รองรับเมื่อมี measured process-capability หรือ qualified-supplier evidence เท่านั้น heuristic minimum-feature check และ supplier identity placeholder ยังคง `unknown_missing_capability_evidence` ไม่ใช่ globally impossible

Manufacturing readiness ยังต้องมี native manufacturing CAD, access ครบ และ worst-case tolerance ผ่าน Exact replay ต้องได้ result SHA-256 เดิม สัญญานี้ไม่อนุญาต purchasing, fabrication, supplier qualification, safety certification หรือ physical validation
