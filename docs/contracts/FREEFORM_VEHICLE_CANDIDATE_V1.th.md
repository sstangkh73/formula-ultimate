# Vehicle Candidate ที่ใช้รูปทรงอิสระ v1

แหล่งภาษาอังกฤษ: `FREEFORM_VEHICLE_CANDIDATE_V1.md`

Protocol version: `freeform_vehicle_candidate_v1` implement โดย Work 139

## 1. ขอบเขตของสัญญานี้

vehicle candidate ประกาศ component โดย component เป็นได้ทั้ง primitive (`box`, `cylinder_z`) หรือ free-form solid ของ Work 092 ที่ยอมรับแล้ว อ้างผ่าน `corpus_candidate_id` องค์ประกอบนี้ถูกสร้างใน CadQuery ตรวจ gate จาก solid ที่สร้างจริง และทุก component ถูกให้คะแนนด้วย evaluator ของ Work 138

```text
declaration -> CadQuery สร้าง (primitive หรือสมาชิก corpus ที่ยอมรับ พร้อมการวางตำแหน่ง)
  -> STEP รายชิ้นและ STEP ของ assembly
  -> วัด packaging จาก solid ที่สร้างจริง
  -> ประเมินด้วย Work 138 ต่อ component
  -> สถานะที่ลงทะเบียนหนึ่งค่าต่อ component และรายงานแบบจับคู่
```

## 2. กฎการแทนรูปทรง

- อ้างได้เฉพาะสมาชิกที่อยู่ใน `corpus.admitted_candidate_ids` และ SHA-256 ของ declaration ของ corpus ถูกคำนวณซ้ำตอน build
- สมาชิก corpus ทำได้แค่วางตำแหน่ง ห้ามย่อขยายหรือแก้ไข การเปลี่ยน geometry หมายถึงต้องประกาศสมาชิก corpus ใหม่และผ่าน gate ของ Work 092 ก่อน
- รูปทรงอิสระใหม่เข้ามาทาง protocol นี้ไม่ได้

## 3. Gate การจัดวาง วัดจาก solid ที่สร้างจริง

1. ทุก component เป็น solid เดียวที่ถูกต้อง
2. ทุก component อยู่ในกรอบ envelope ที่ประกาศ
3. ไม่มีคู่ใดตัดกันเกิน `packaging.maximum_pairwise_intersection_m3`
4. ไม่มี keep-out ใดถูกรุกล้ำ
5. ทุก tag ใน `required_function_tags` มี component รองรับอย่างน้อยหนึ่งชิ้น
6. มวลที่ประกาศซึ่งขัดกับมวลที่สร้างจริงเกิน `packaging.declared_mass_relative` ต้องถูกปฏิเสธ

candidate ที่ตก gate ใดจะเป็น `incomplete_composition` ห้ามเอา primitive มาแทน component รูปทรงอิสระเพื่อให้ผ่าน gate

## 4. การประเมินและสถานะ

แต่ละ component กลายเป็น candidate ชนิด `step_file` ของ Work 138 พร้อมวัสดุ ขอบเขต และ load case ที่ประกาศ โดยใช้มวลที่สร้างจริงเป็นมวลที่ประกาศ แล้วได้สถานะของ Work 138 กลับมาหนึ่งค่าพอดี component ที่เป็น `unresolved_*` ต้องรายงานพร้อมสาเหตุและถูกนับ ห้ามหายไป ถ้ามี component ใดเป็น `unsupported_representation` candidate นั้นจะเป็น `incomplete_composition`

## 5. การเปรียบเทียบแบบจับคู่

declaration ต้องมี `primitive_baseline` หนึ่งตัวและ `freeform_variant` หนึ่งตัวที่ต่างกันเพียง component เดียว และ component ที่เปลี่ยนในตัวแปรต้องเป็นชิ้นรูปทรงอิสระ ทั้งสอง candidate ถูกสร้าง ตรวจ gate และประเมินภายใต้วัสดุ, ladder ของ mesh, ขีดจำกัดการลู่เข้า, งบ และ load case เดียวกัน

รายงานแบบจับคู่ระบุมวลของแต่ละ candidate ผลต่างของมวล และสถานะกับ utilization ของ component ที่ถูกแทนทั้งสองฝั่ง พร้อมระบุสิ่งที่คู่นี้ยืนยันไม่ได้ คือการแทนหนึ่งชิ้นภายใต้ load case เดียวเป็นหลักฐานว่าประกอบได้และประเมินได้ ไม่ใช่ว่าดีกว่า

## 6. ขอบเขตข้ออ้าง

`passed_freeform_vehicle_composition` หมายถึง candidate ที่ประกาศถูกสร้าง จัดวาง และประเมินแล้ว สรุปผลระบุ `discovery_claim`, `promotion_allowed`, `race_time_claim` และ `physical_validation` เป็นเท็จ และมี control ตรวจข้อนี้ วัสดุยังเป็นค่าสังเคราะห์สำหรับ geometry เท่านั้น

## 7. Control ที่บังคับ

`component_outside_envelope`, `components_intersect`, `missing_required_function_tag`, `corpus_hash_mismatch`, `unadmitted_corpus_member`, `declared_mass_contradiction`, `no_discovery_claim` และ `exact_replay` ทั้งแปดข้อต้องถูกปฏิเสธ และการ replay บน tree ที่สะอาดต้องให้ result SHA-256 ตรงกันทุกประการ โดย hash ของ manifest ครอบคลุมเฉพาะตัวตนของ geometry ดังนั้น candidate เดียวกันที่ build ลงคนละ output root จะได้ hash เท่ากัน
