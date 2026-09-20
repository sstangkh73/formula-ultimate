# Work 139: Vehicle candidate ที่ใช้รูปทรงอิสระ

แหล่งภาษาอังกฤษ: `work139-freeform_vehicle_candidates.md`

Status: Planned

แพ็กเกจเดิมของ Work 106: ไม่มี เป็นส่วนขยายเชิงแก้ไข เขียนพร้อมกับ Work 139 เอง

Dependencies: Work 047 (vehicle assembly primitives), Work 091/092 (grammar ของ wire และ solid แบบอิสระ), Work 138 (geometry-general evaluator)

ข้อกำหนดร่วมที่บังคับใช้: [ดัชนีและกฎการดำเนินการ](README.th.md)

## 1. ผลลัพธ์และขอบเขต

vehicle candidate สามารถประกาศ component เป็น free-form solid ที่ผ่านการยอมรับแล้ว แทนกล่องหรือทรงกระบอก และทุก component ถูกประเมินด้วย evaluator ของ Work 138 การผ่านหมายถึงเพียง `passed_freeform_vehicle_composition` คือ candidate สร้างได้ จัดวางได้ และประเมินได้ ไม่ใช่การค้นพบ ไม่ใช่ promotion ไม่ใช่เวลาแข่ง และไม่ใช่ physical validation

รูปร่างแปลกใหม่ไม่ใช่หลักฐาน component แบบอิสระไม่ได้แต้มจากการโค้ง แต่ถูกประเมินภายใต้โหลดเดียวกัน evaluator เดียวกัน และการลงทะเบียนเดียวกันกับ baseline ที่เป็น primitive

## 2. ทำไมต้องมีงานนี้

`scripts/cad/generate_vehicle_assembly.py` สร้างได้แค่กล่องกับทรงกระบอก และ evaluator ของ campaign ให้คะแนนตัวแปรสเกลห้าตัวแทนที่จะอ่าน geometry Work 138 ปลดข้อจำกัดด้านการประเมินไปแล้ว งานนี้ปลดข้อจำกัดด้านการประกอบ เพื่อให้รูปทรงจาก corpus ของ Work 092 เข้าไปอยู่ในตำแหน่งหน้าที่ของรถได้

## 3. การแทนรูปทรง

component ประกาศได้สองแบบ

- `primitive`: `box` หรือ `cylinder_z` เหมือนเดิม หรือ
- `freeform_reference`: path ของ corpus Work 092 พร้อม SHA-256 ของ declaration และ `candidate_id` ที่ได้รับการยอมรับ พร้อมการวางตำแหน่ง (`translation_m`, `rotation_deg_xyz`)

v1 อนุญาตเฉพาะสมาชิกของ corpus ที่ยอมรับแล้ว declaration ใหม่ต้องผ่าน gate ของ corpus Work 092 ก่อน และห้ามย่อขยายสมาชิก corpus เพราะจะทำให้ geometry ออกนอก declaration ที่ยอมรับไว้

## 4. Gate การจัดวาง วัดจาก solid ที่สร้างจริง

1. ทุก component เป็น solid เดียวที่ถูกต้อง
2. ทุก component อยู่ในกรอบ envelope ที่ประกาศ
3. ไม่มีคู่ใดตัดกันเกินค่าคลาดเคลื่อนที่ประกาศ
4. ทุก keep-out ที่ประกาศยังว่าง
5. ทุก function tag ที่จำเป็นมี component รองรับอย่างน้อยหนึ่งชิ้น
6. mass properties มาจาก geometry ไม่ใช่จากการประกาศ

## 5. การประเมิน

แต่ละ component ถูกส่งเข้า evaluator ของ Work 138 ในฐานะ candidate ชนิด `step_file` พร้อมวัสดุและ load case ที่ประกาศ และได้สถานะที่ลงทะเบียนกลับมาหนึ่งค่า candidate จะเป็น `evaluable` ก็ต่อเมื่อไม่มี component ใดเป็น `unsupported_representation` ส่วน component ที่เป็น `unresolved_*` ต้องรายงานพร้อมสาเหตุ ห้ามตัดทิ้ง

## 6. กฎการเปรียบเทียบแบบจับคู่

การรัน admitted ประเมิน baseline ที่เป็น primitive กับตัวแปรที่ใช้รูปทรงอิสระ ซึ่งต่างกันเพียง component เดียว ทั้งคู่ใช้ evaluator, ladder ของ mesh, วัสดุ, โหลด และงบเดียวกัน รายงานมวลและ utilization คู่กัน และระบุตรง ๆ ว่านี่คือการประเมินแบบจับคู่ ไม่ใช่ข้ออ้างการค้นพบ เพราะคู่เดียวภายใต้ load case เดียวพิสูจน์ความเหนือกว่าไม่ได้

## 7. Control ที่บังคับ

1. component ที่อยู่นอก envelope ต้องถูกปฏิเสธ
2. component ที่ซ้อนทับกันต้องถูกปฏิเสธ
3. function tag ที่จำเป็นแล้วขาดหายต้องถูกปฏิเสธ
4. hash ของ corpus ที่ไม่ตรงกับ declaration ต้องถูกปฏิเสธ
5. `candidate_id` ที่ไม่มีใน corpus ที่ยอมรับต้องถูกปฏิเสธ
6. มวลที่ประกาศซึ่งขัดกับ geometry ที่สร้างจริงต้องถูกปฏิเสธ
7. ผลลัพธ์ต้องไม่มีข้ออ้างเรื่องการค้นพบ promotion หรือเวลาแข่ง
8. การ replay บน tree ที่สะอาดต้องให้ result SHA-256 ตรงกันทุกประการ

## 8. ไฟล์ที่เสนอ

- `src/formula_ultimate/search/freeform_vehicle_candidate.py`
- `scripts/cad/build_freeform_vehicle_candidate.py` (รันด้วย CadQuery runtime ที่ pin ไว้)
- `scripts/development/run_freeform_vehicle_candidate.py`
- `config/development/freeform_vehicle_candidate_v1.json`
- `tests/test_freeform_vehicle_candidate.py`
- `docs/contracts/FREEFORM_VEHICLE_CANDIDATE_V1.md` และคู่ภาษาไทย

## 9. เกณฑ์การยอมรับ

control ทั้งแปดถูกปฏิเสธ ทุก component มีสถานะที่ลงทะเบียนหนึ่งค่า gate การจัดวางวัดจาก solid ที่สร้างจริง และ replay ตรงทุกประการ

## 10. ความเสี่ยงและการส่งต่อ

- สมาชิก corpus อาจไม่พอดีกับตำแหน่งหน้าที่ใด กรณีนั้น candidate ต้องหยุดเป็น `incomplete_composition` ไม่ใช่เอากล่องมาแทน
- ชิ้นส่วนอิสระอาจ mesh ได้ไม่ดี นั่นคือหลักฐาน `unresolved_*` จาก Work 138 ไม่ใช่คำตัดสินต่อรูปทรง
- การป้อนผล evaluator เข้าสู่เวลาแข่งยังเป็น Work 140 และการค้นหาบนองค์ประกอบรูปทรงอิสระเป็นงานถัดไปอีกขั้น
