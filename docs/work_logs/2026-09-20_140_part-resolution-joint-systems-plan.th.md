# แผน Work 140: ความละเอียดของชิ้นส่วนและระบบข้อต่อ

แหล่งภาษาอังกฤษ: `2026-09-20_140_part-resolution-joint-systems-plan.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

การ์ดแผนดำเนินการ: `docs/plans/detailed_part_to_vehicle_v1/work140-part_resolution_joint_systems.th.md`

## วัตถุประสงค์

ทำให้โปรเจกต์มีนิยามที่วัดได้ของคำว่า "ละเอียดพอ" และนิยามที่เป็นกลางทางเทคโนโลยีของคำว่า "ข้อต่อจริง" แล้วนำทั้งสองมาใช้กับรถที่มีอยู่ และรายงานผลตามความจริง

## หลักฐานตั้งต้นที่วัดเมื่อ 2026-09-20

- ทั้ง 48 definition ของ Work 135 ประกาศ feature ชิ้นละสามอย่างพอดี ขนาดเล็กสุดที่ประกาศในรถคือ `1.5 mm` (ความหนาแหวนรอง) และค่ากลางของ feature เล็กสุดต่อชิ้นคือ `6.0 mm`
- ตัวยึดของ Work 135 คือ `{"kind": "bolt_z", "shaft_radius_m": 0.004, "shaft_length_m": 0.28, "head_radius_m": 0.008, "head_height_m": 0.006}` เป็นทรงกระบอกสองชิ้น ไม่มีเกลียว ไม่มีมุมลบ ไม่มีผิวรับแรงกด
- `config/cad/freeform_brep_solid_grammar_v2.json` อนุญาต `minimum_feature_m = 1e-05` และ 32 feature ต่อ candidate อยู่แล้ว kernel จึงไม่ใช่ข้อจำกัด
- การสำรวจความสามารถ: เกลียว M8 ที่กวาดจริงเชื่อมเป็น solid เดียวที่ถูกต้องใน `0.4 วินาที` (21 หน้า โค้ง 17 หน้า) ส่วนตัวยึดอ้างอิงเต็มรูปแบบที่มีหัวหกเหลี่ยม เบ้าหกเหลี่ยม และมุมลบ สร้างได้ใน `0.5 วินาที` เป็น solid เดียวที่ถูกต้อง มี 34 หน้า โค้ง 17 หน้า 85 ขอบ พื้นที่หน้าเล็กสุด `0.1544 mm^2` และขอบสั้นสุด `0.0843 mm` ส่วนรัศมีโคนใต้หัวเกิด `StdFail_NotDone` จึงยังไม่ใส่
- การสำรวจความสามารถ: การตัดเกลียวในออกจากน็อตหกเหลี่ยมไม่ได้เอาเนื้อออกจริง boolean คืนรูที่ไม่มีเกลียวอย่างเงียบ ๆ เรื่องนี้บันทึกเป็นข้อจำกัดของ kernel และจะรายงานเป็น `unresolved_measurement` ไม่ใช่เลี่ยงด้วยการประกาศว่าน็อตมีเกลียว

## ขอบเขต

- `src/formula_ultimate/assembly/part_resolution.py`: schema ของ declaration, ทะเบียนเทคโนโลยีข้อต่อและหลักฐานที่ต้องมี, gate ความละเอียด, ชุดสถานะ และการสรุปผลการรัน
- `scripts/cad/measure_part_resolution.py`: รันด้วย CadQuery runtime ที่ pin ไว้ สร้างชิ้นส่วนอ้างอิง นำเข้าชิ้นส่วน STEP ที่ประกาศ และวัดจำนวนหน้า ขอบ หน้าโค้ง ชนิดผิว พื้นที่หน้าเล็กสุด ขอบสั้นสุด ปริมาตร และกรอบขอบเขต ส่วนข้อต่อวัดระยะใกล้สุด ปริมาตรการแทรกสอด และคู่ผิวสัมผัส
- `scripts/development/run_part_resolution_gate.py`: เรียกการวัด ใช้ gate ตรวจความละเอียดของ mesh ด้วยตัว mesh ของ Work 138 รัน control แปดข้อ เขียน `result.json` พร้อม SHA-256 แบบ canonical และรองรับ `--replay-reference`
- `config/development/part_resolution_gate_v1.json`, `tests/test_part_resolution.py`, สัญญาสองภาษา, การ์ดแผนสองภาษา, แถวในดัชนี รวมถึงแผนสองภาษานี้และผลลัพธ์

## การตรวจสอบ

1. `python -m unittest tests.test_part_resolution -v`: exit 0
2. `python scripts/development/run_part_resolution_gate.py --config ... --output-root artifacts/work140/run_a`: exit 0, control แปดข้อถูกปฏิเสธ, ทุกหัวข้อมีสถานะที่ลงทะเบียนหนึ่งค่า
3. runner ตัวเดิมไปที่ `run_b` พร้อม `--replay-reference`: exit 0 และ result SHA-256 ตรงกัน
4. `python -m unittest discover -s tests`, `python -m unittest tests.test_repository_contract -v`, `python -m compileall -q src scripts tests`, `git diff --check`, `git diff --cached --check`: exit 0

## เกณฑ์สำเร็จและล้มเหลว

สำเร็จ: ทุกตัวเลขของ gate วัดจาก geometry ที่สร้างจริง ทุกหัวข้อมีสถานะที่ลงทะเบียนหนึ่งค่า control ทั้งหมดถูกปฏิเสธ และ replay ตรงทุกประการ

ล้มเหลว: มีการผ่อน gate หลังเห็นผล, ซ่อนการปฏิเสธของ kernel ไว้หลังชิ้นส่วนที่ลดรูป, หัวข้อหายไปจากการนับ หรือการรันอ้างเกินกว่าคำตัดสินเชิง geometry

## ความเสี่ยงและสิ่งที่ไม่ทำ

- คาดว่าตัวยึดของ Work 135 จะไม่ผ่าน การรายงานเรื่องนี้คือจุดประสงค์ของงาน
- สิ่งที่ไม่ทำ: ไม่แก้สมการแบบ contact หรือ tied surface ข้ามข้อต่อ, ไม่ออกแบบรถ Work 135 ใหม่, ไม่เชื่อมกับเวลาแข่ง, ไม่ push และไม่เขียนประวัติใหม่
