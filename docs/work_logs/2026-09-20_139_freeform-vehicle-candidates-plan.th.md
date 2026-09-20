# แผน Work 139: Vehicle Candidate ที่ใช้รูปทรงอิสระ

แหล่งภาษาอังกฤษ: `2026-09-20_139_freeform-vehicle-candidates-plan.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

การ์ดแผนดำเนินการ: `docs/plans/detailed_part_to_vehicle_v1/work139-freeform_vehicle_candidates.th.md`

## วัตถุประสงค์

ให้ vehicle candidate ประกาศ component เป็น free-form solid ของ Work 092 ที่ได้รับการยอมรับแล้ว แทนกล่องหรือทรงกระบอก สร้างขึ้นจริง ตรวจ gate การจัดวางจาก solid ที่สร้าง และประเมินทุก component ด้วย evaluator ของ Work 138

## หลักฐานตั้งต้น

- `scripts/cad/generate_vehicle_assembly.py` สร้างได้แค่กล่องหรือทรงกระบอก ส่วน `config/vehicle/topology_neutral_vehicle_v1.json` คือ assembly ฐานสี่ component ที่ campaign นำไป mutate
- `artifacts/work092/run_e/` มี free-form solid ที่ยอมรับแล้วสิบชิ้น แต่ละชิ้นเป็น solid เดียวที่ถูกต้อง พร้อม `manifest.json` และ `result.json` ที่เก็บ hash ของ declaration และ STEP
- `scripts/cad/generate_freeform_solid_corpus.py` มี `execute_candidate(candidate, profiles)` ที่สร้างสมาชิก corpus ขึ้นใหม่ใน CadQuery จาก declaration โดย profile มาจาก wire config ของ Work 091
- Work 138 ให้ `validate_protocol`, `evaluate_candidate` และชุดสถานะหกค่า พร้อมการรัน admitted ที่ result SHA-256 `50e50ed6fa8aa3dfe93804f3a3e67a1471331b203c0da4c1d1c6001d0054d6ec`

## ขอบเขต

- `src/formula_ultimate/search/freeform_vehicle_candidate.py`: schema และการตรวจ declaration, การครอบคลุม function tag ที่จำเป็น, gate การจัดวางเทียบ manifest ที่สร้างจริง, การสร้าง protocol การประเมินของ Work 138 และสรุปผลการรัน
- `scripts/cad/build_freeform_vehicle_candidate.py`: รันด้วย CadQuery runtime ที่ pin ไว้ สร้างแต่ละ component จาก primitive หรือจากสมาชิก corpus ที่ยอมรับแล้ว วางตำแหน่ง ส่งออก STEP ทั้งรายชิ้นและ assembly และวัด volume, mass, center, bounding box, การตัดกันเป็นคู่ และระยะปลอดของ keep-out
- `scripts/development/run_freeform_vehicle_candidate.py`: สร้าง candidate ทั้งสอง ตรวจ gate การจัดวาง ประเมินทุก component ผ่าน Work 138 รัน control แปดข้อ เขียน `result.json` พร้อม SHA-256 แบบ canonical และรองรับ `--replay-reference`
- `config/development/freeform_vehicle_candidate_v1.json`: baseline ที่เป็น primitive และตัวแปรที่ใช้รูปทรงอิสระ ต่างกันหนึ่ง component
- `tests/test_freeform_vehicle_candidate.py`: การทดสอบ logic ที่รันเสมอ และการทดสอบ kernel ที่ข้ามเมื่อไม่มี CadQuery
- `docs/contracts/FREEFORM_VEHICLE_CANDIDATE_V1.md` และคู่ภาษาไทย, การ์ดแผนคู่ภาษา, แถวในดัชนี, แผนสองภาษานี้และผลลัพธ์

## การตรวจสอบ

1. `python -m unittest tests.test_freeform_vehicle_candidate -v`: exit 0
2. `.tools/cadquery-mcp/Scripts/python.exe scripts/cad/build_freeform_vehicle_candidate.py ...`: exit 0 ทั้งสอง candidate
3. `python scripts/development/run_freeform_vehicle_candidate.py --config ... --output-root artifacts/work139/run_a`: exit 0, control แปดข้อถูกปฏิเสธ, ทุก component มีสถานะที่ลงทะเบียนหนึ่งค่า
4. runner ตัวเดิมไปที่ `run_b` พร้อม `--replay-reference`: exit 0 และ result SHA-256 ตรงกัน
5. `python -m unittest tests.test_repository_contract -v`, `python -m unittest discover -s tests`, `python -m compileall -q src scripts tests`, `git diff --check`, `git diff --cached --check`: exit 0

## เกณฑ์สำเร็จและล้มเหลว

สำเร็จ: candidate ทั้งสองสร้างได้ gate การจัดวางวัดจาก solid ที่สร้างจริง ทุก component มีสถานะที่ลงทะเบียนหนึ่งค่า control ทั้งแปดถูกปฏิเสธ และ replay ตรงทุกประการ

ล้มเหลว: component รูปทรงอิสระถูกแทนด้วย primitive อย่างเงียบ ๆ, มีการยกเว้น gate การจัดวาง, component หายไปจากการนับ หรือการรันอ้างว่าเป็นการค้นพบ

## ความเสี่ยงและสิ่งที่ไม่ทำ

- ความเสี่ยง: สมาชิก corpus ไม่พอดีกับตำแหน่งของมัน กรณีนั้น candidate ต้องหยุดเป็น `incomplete_composition` ห้ามเอากล่องมาแทน
- ความเสี่ยง: การจับคู่เปรียบเทียบอาจถูกอ่านว่าเป็นข้ออ้างความเหนือกว่า ผลลัพธ์ต้องระบุว่าคู่เดียวภายใต้ load case เดียวยืนยันได้แค่ว่าประเมินได้เท่านั้น
- สิ่งที่ไม่ทำ: ไม่สร้าง declaration รูปทรงอิสระนอก corpus ที่ยอมรับ ไม่ย่อขยายสมาชิก corpus ไม่เชื่อมกับเวลาแข่ง ไม่ทำการค้นหา ไม่ push และไม่เขียนประวัติใหม่
