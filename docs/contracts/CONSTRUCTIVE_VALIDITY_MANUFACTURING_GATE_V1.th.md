# Constructive Validity and Manufacturing Gate V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `CONSTRUCTIVE_VALIDITY_MANUFACTURING_GATE_V1.md`

## ขอบเขตหลักฐาน

Gate นี้ตรวจ synthetic witness fixture แบบ deterministic เทียบกับ constructive rule และ process envelope ที่ประกาศไว้ Source candidate ID และ STEP SHA-256 เป็นหลักฐานเดิมจริง แต่ค่า wall, ligament, radius, feature, access, overhang, void, tolerance และ joining ใน pilot นี้เป็น matched synthetic controls การผ่านพิสูจน์เพียงพฤติกรรม gate ไม่ใช่ข้อสรุป manufacturability ที่วัดจริงของ source STEP, supplier, toolchain หรือ material ใด

## ลำดับการทำงาน

Gate ตรวจ exact schema, ค่า SI ที่ finite, source identity, process profile, material compatibility และโอกาสที่เท่ากัน แล้วจึงทำเฉพาะ preregistered repair ก่อนมี performance observation Repair ทุกครั้งบันทึก evidence hash ก่อน/หลังและเปลี่ยน evaluated genotype/provenance identity ส่วน hidden, unregistered, over-budget หรือ post-observation repair ต้อง reject

Constructive check ครอบคลุม B-rep validity, exact single-solid declaration, self-intersection, zero thickness และ sliver/minimum feature ส่วน process check ครอบคลุม wall, ligament, radius, tool access, overhang/support, enclosed void/escape, tolerance, joining access และ material/process compatibility ระบบคืน violation code ทุกข้อที่เกี่ยวข้อง และไม่ repair failure ใดแบบเงียบ

## ความยุติธรรมและ replay

primitive control และ curved/free-form family อีก 5 แบบได้รับ scenario 8 แบบเดียวกัน opportunity ที่ reject ยังคงอยู่ในตัวหาร Yield และ rejection cause ทุกข้อรายงานแยกตาม family Exact clean replay ต้องสร้าง ordered ledger ทั้งชุดและ `result_sha256` เดิม

## ข้อจำกัด

coarse scalar fixture ไม่ได้ resolve local field, face semantic, collision, swept motion, tool trajectory, inspection, cost, production quality, structural adequacy หรือ safety Work 096 ต้อง derive semantic ที่ละเอียดขึ้นอย่างอิสระจาก geometry ก่อนนำกฎเหล่านี้ไป screen ค่าที่วัดจริงของ candidate
