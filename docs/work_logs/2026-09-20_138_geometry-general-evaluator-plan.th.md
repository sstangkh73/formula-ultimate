# แผน Work 138: Structural Evaluator ที่รับ Geometry ใดก็ได้

แหล่งภาษาอังกฤษ: `2026-09-20_138_geometry-general-evaluator-plan.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

การ์ดแผนดำเนินการ: `docs/plans/detailed_part_to_vehicle_v1/work138-geometry_general_evaluator.th.md`

## วัตถุประสงค์

implement evaluator ตามการ์ด Work 138 คือเส้นทาง `STEP -> Gmsh -> CalculiX C3D10 -> properties` ที่รับ solid เดียวที่ถูกต้องแบบใดก็ได้ คำนวณ mass properties และการตอบสนองต่อโหลดด้วยตัวเอง คืนสถานะที่ลงทะเบียนหนึ่งค่าต่อ candidate และ replay ได้ตรงทุกประการ

## การสำรวจความสามารถเมื่อ 2026-09-20 (ก่อน implement)

- `gmsh.exe` ทำ mesh `artifacts/work135/run_a/cad/parts/carrier_plate.step` ที่ order สองได้ใน `1.3 วินาที` ได้ 13,334 node และ 7,586 C3D10 tetrahedra
- `ccx.exe` (CalculiX 2.22) แก้ deck C3D10 ที่สร้างจาก mesh นั้นได้ในราว `1 วินาที`
- deck ที่เขียนพิกัดด้วย `:.17g` ถูกปฏิเสธ การทดสอบแบบควบคุมพบว่า CalculiX ตัด field ตัวเลขที่ 20 ตัวอักษร ค่าวิทยาศาสตร์ยาว 21 ตัวอักษร `-1.00000000000000e+03` ถูกอ่านเป็น `-1.0` และให้ displacement เล็กกว่าความจริง `1000 เท่า` โดย **exit code เป็น 0** ส่วน 22 ตัวอักษรขึ้นไปจะหยุดด้วย exit 201 Work 085 เคยเจอโหมดที่ถูกปฏิเสธและแก้ไว้เฉพาะใน runner ของตัวเอง evaluator นี้จึงต้องจัดรูปแบบตัวเลขทุก field อย่างระมัดระวัง

## ขอบเขต

- `src/formula_ultimate/structural/geometry_general_evaluator.py`: ตรวจ protocol, จัดรูปแบบตัวเลขให้ปลอดภัยกับ CalculiX, เลือกขอบเขต, โหลดผิวแบบ TRI6 consistent, สร้าง deck C3D10, อ่าน `.dat` โดยเก็บทุก integration point, คำนวณ mass properties จาก mesh, ตรวจการลู่เข้า และชุดสถานะ
- `scripts/structural/mesh_step_solid.py`: แปลง STEP เป็น Gmsh `msh2` ที่ characteristic length ที่ประกาศไว้ พร้อมหลักฐาน process และ hash
- `scripts/structural/run_geometry_general_evaluator.py`: runner สำหรับรัน admitted รวม analytical benchmark, control แปดข้อ, `result.json` พร้อม SHA-256 แบบ canonical และ `--replay-reference`
- `config/development/geometry_general_evaluator_v1.json`
- `tests/test_geometry_general_evaluator.py`: การทดสอบ logic ที่รันเสมอ และการทดสอบ kernel ที่ข้ามเมื่อไม่มี `gmsh.exe` หรือ `ccx.exe`
- `docs/contracts/GEOMETRY_GENERAL_EVALUATOR_V1.md` และคู่ภาษาไทย
- แผนสองภาษานี้และผลลัพธ์สองภาษาที่ตรงกัน

## Candidate สำหรับรัน admitted

1. `cantilever_benchmark`: คานกล่องที่ทำ mesh โดยตรง เทียบกับการโก่งปลายตามทฤษฎี Euler-Bernoulli นี่คือ control ข้อ 1
2. `spine_frame` และ `carrier_plate` จาก Work 135 คือชิ้นโครงสร้างที่หนักที่สุดกับ carrier โดยใช้ไฟล์ STEP ของ occurrence นั้นจริง
3. `curved_branch_001` จาก `artifacts/work092/run_e` ซึ่งเป็น free-form solid ที่ evaluator ของ campaign ปัจจุบันให้คะแนนไม่ได้เลย

## การตรวจสอบ

1. `python -m unittest tests.test_geometry_general_evaluator -v`: exit 0
2. `python scripts/structural/run_geometry_general_evaluator.py --config ... --output-root artifacts/work138/run_a`: exit 0 ทุก candidate มีสถานะที่ลงทะเบียนหนึ่งค่า และ benchmark ผ่าน
3. runner ตัวเดิมไปที่ `run_b` พร้อม `--replay-reference artifacts/work138/run_a/result.json`: exit 0 และ result SHA-256 ตรงกัน
4. `python -m unittest tests.test_repository_contract -v`, `python -m compileall -q src scripts tests`, `git diff --check`, `git diff --cached --check`: exit 0

## เกณฑ์สำเร็จและล้มเหลว

สำเร็จ: benchmark อยู่ในค่าคลาดเคลื่อนที่ลงทะเบียน control ทั้งแปดข้อทำงานตามที่ลงทะเบียน ทุก candidate รายงานสถานะที่ลงทะเบียน มวลที่ได้จาก mesh ตรงกับมวลจาก CadQuery ของ Work 135 ภายใน residual ที่ลงทะเบียน และ replay ตรงทุกประการ

ล้มเหลว: มี candidate หายไปเงียบ ๆ, ความล้มเหลวของ solver ถูกบันทึกเป็นคำตัดสินทางฟิสิกส์, benchmark ไม่เข้าเกณฑ์ หรือ replay ไม่ตรง

## ความเสี่ยงและสิ่งที่ไม่ทำ

- ชิ้นส่วนอาจ mesh ไม่ได้หรือไม่ลู่เข้า กรณีนั้นบันทึกเป็นหลักฐาน `unresolved_*` ไม่ใช่ความล้มเหลวของงาน และไม่ใช่เหตุผลให้ลดรูปชิ้นส่วน
- ผลลัพธ์เป็นการประเมินเชิงโครงสร้างเท่านั้น ไม่ใช่ promotion ไม่ใช่ความเป็นไปได้ในการผลิต ไม่ใช่เวลาแข่ง และไม่ใช่ physical validation
- สิ่งที่ไม่ทำ: ไม่แก้ grammar, การค้นหา, race simulator หรือบันทึกของ Work 062, 092 และ 135 ไม่ push และไม่เขียนประวัติใหม่
