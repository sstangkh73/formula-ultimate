# ผลลัพธ์ Work 157: รูเจาะทะลุของ leaf ใน v2 ที่รักษาพื้นที่สัมผัส

ฉบับภาษาอังกฤษ: `2026-10-12_157_v2-leaf-through-bores-result.md`

วันที่: 2026-10-12

Status: Completed

แผน: `2026-10-12_157_v2-leaf-through-bores-plan.md`

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/hierarchy/leaf_refinement.py` (ใหม่ Python ล้วน):
  `RefinementConfig` (ความน่าจะเป็นเจาะ 0.8, มุมเอียง 5–40 องศา, สัดส่วนรัศมี
  0.12–0.30 ของ `rho`, สัดส่วนผนัง 0.12, สุ่ม 12 ครั้ง), `REFINED_LEAF_GRAMMAR_VERSION =
  "func-leaf-bored-v2"`, `contact_patches`, `bore_parameters`, `bore_program`,
  `base_program`, `bore_exits`, `validate_refined_program`, `refine_layout`,
  `refinement_problems`, `refinement_config_record`
- `scripts/hierarchy/functional_realization.py` (ใหม่ CAD runtime):
  `realize_program` ตรวจโปรแกรม v1 หรือโปรแกรมที่ปรับแต่ง แล้วใช้ executor และ `tessellate_m` เดิมโดยไม่แก้
- `src/formula_ultimate/hierarchy/functional.py`: `config_sha256_v2` รับ record การปรับแต่งแบบไม่บังคับ
  (ผลลัพธ์เดิมเมื่อไม่ส่ง); `with_leaf_grammar_versions` บันทึก grammar ของแต่ละโปรแกรมใน manifest
- `scripts/hierarchy/generate_functional_vehicle.py`: ปรับแต่งหลังวางแผน ตรวจซ้ำด้วย
  `refinement_problems` (แจ้งข้อผิดพลาดเมื่อพบปัญหา) สร้างด้วย `realize_program` และรวม config การปรับแต่งใน hash
- `tests/test_hierarchy_leaf_refinement.py` (ใหม่ 9 เทสต์ หนึ่งเทสต์ผ่าน CAD runtime)

## การตัดสินใจ

- เบี่ยงจากแผน: จุดบนแกนรูเป็น `(ox, oy, h/2)` ที่สุ่มระยะเลื่อนด้านข้าง แทน `(0, 0, h/2)` คงที่
  เหตุผล: เมื่อแกนอยู่ตรงกลาง leaf ที่รับพื้นที่สัมผัส 104 จาก 110 ชิ้น (seed 11) เจาะไม่ได้
  เพราะทางออกตกบนพื้นที่สัมผัสที่อยู่ตรงกลาง กฎระยะเผื่อจึงเป็น
  `|(ox, oy)| + (h/2) tan b + r / cos b <= (1 - wall) rho` และเพิ่มความน่าจะเป็นเจาะจาก 0.5 เป็น 0.8
  (สัดส่วนที่ 0.5 คือ 25–33 % ใกล้เกณฑ์ 25 % เกินไป)
- การปรับแต่งเอาเนื้อวัสดุออกเฉพาะในทรงกระบอกวงใน จึงไม่สร้างการทะลุกัน และกล่องกับ interface ของ layout
  ไม่เปลี่ยน (ตรวจด้วย `refinement_problems`)
- กฎพื้นที่สัมผัส: ฝาเป้าหมายใต้ฝาต้นทางที่เล็กกว่า (mode `inside`) รับดิสก์ของต้นทาง;
  ฝาต้นทางที่ครอบพื้นที่เป้าหมาย (mode `around`) รับพื้นที่นั้น กรณีอื่นขอบผิวทั้งหมดของ leaf ยังสัมผัสอยู่

## คำสั่งและผลลัพธ์

1. `python -m unittest tests.test_hierarchy_leaf_refinement tests.test_hierarchy_functional tests.test_hierarchy_functional_joints`
   -> exit 0, `Ran 19 tests in 43.411s`, `OK` (หลังแก้เทสต์หนึ่งครั้ง: รูรัศมี
   `0.99 * inscribed` ไม่ถูกปฏิเสธเพราะขีดจำกัดคือ `inscribed - tolerance` ซึ่งเกือบเท่ากัน
   เทสต์จึงใช้รัศมี `inscribed`)
2. สัดส่วนจากการวางแผนล้วน (leaf ที่เจาะ / leaf ทั้งหมด): seed 11 92/226, 23 110/229,
   37 101/229, 0 72/177, 1 81/201, 2 99/228; `refinement_problems` ว่างทุก seed
3. `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed 11 --out artifacts/work157/s11`
   -> exit 0, 22 s, 226 leaf
   `python artifacts/work157/spot_check.py artifacts/work157/s11` (ฟังก์ชันช่วยของ acceptance):
   เจาะ 92, ไม่เป็นปริซึม 160, มีรู (genus >= 1) 92, ช่องว่าง interface สูงสุด 2.1e-18 m
4. `pwsh -NoProfile -File auto-loop/verify.ps1` -> Gate 1 PASS; Gate 2
   `Ran 1113 tests in 648.508s`, `OK (skipped=11)`; Gate 3
   `Ran 41 tests`, `FAILED (failures=11)`: ชุด v1 ผ่าน 13/13, v2 Tier A0,
   A1, A2 (ผ่านแบบว่างเปล่า ยังไม่มีการเคลื่อนที่) และ A3 ผ่าน; B1–B10 และ C1 ยังล้มเหมือนเดิม

## ข้อจำกัด

- ก่อนงานนี้ mesh ของ v2 ผ่านสัดส่วนไม่เป็นปริซึมอยู่แล้ว (Gate 3 ล้ม A1 เพราะรูเท่านั้น)
  ตัวแทนนี้สุ่มตรวจสามเหลี่ยมใหญ่สุด 20 ชิ้น การอัดรีดตรงบางชิ้นจึงนับเป็นไม่เป็นปริซึม
  รูเจาะเพิ่มผิวเอียงจริง แต่ตัวแทนนี้ไม่ใช่การวัดคุณภาพรูปทรง
- รูเจาะเป็นรายละเอียดเชิงการแทนที่ไม่มีหน้าที่ที่ประกาศ (ลดน้ำหนัก ทางผ่าน) ไม่แสดงความสามารถรับแรง
- การตรวจการสัมผัสใช้รูปทรงผิวที่ประกาศ การวัดของ acceptance ยืนยันเฉพาะ seed 11 ในงานนี้
  (seed 23 และ 37 ผ่าน Gate 3)

## งานต่อไป

- Tier B10: รอยต่อตัวยึด `threaded` จริง (>= 8 ต่อ seed) แนวทางที่แนะนำ: รูเจาะตามแกน
  (มุมเอียง 0) ใน leaf ที่มีรู และ leaf สลักใหม่ที่ก้านอยู่ตามแกนรูภายในรูและหัวเรียบวางบนฝา
  ทำให้แกนผ่านรูของชิ้นหนึ่งและผ่านเนื้อของสลัก
- จากนั้นโมดูลเชิงฟังก์ชันต่อความสามารถ (Tier B) และตัวประเมิน Level-0 (Tier C)
