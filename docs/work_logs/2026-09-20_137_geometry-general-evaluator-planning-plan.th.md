# แผน Work 137: การวางแผน Geometry-General Evaluator

แหล่งภาษาอังกฤษ: `2026-09-20_137_geometry-general-evaluator-planning-plan.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์

เขียนแผนสองภาษาที่พร้อมดำเนินการสำหรับ Work 138 ซึ่งเป็น structural evaluator ที่รับ geometry ใดก็ได้ ปัจจุบัน evaluator ของ campaign อ่านตัวแปรสเกล 5 ตัว ไม่ได้อ่าน geometry รูปทรงอิสระจึงให้คะแนนไม่ได้เลย Work 138 ต้องแทนที่ด้วยเส้นทาง `STEP -> mesh -> solver -> properties` ที่รับ solid ที่ถูกต้องแบบใดก็ได้

งานนี้เป็นการวางแผนเท่านั้น ไม่เขียน evaluator ไม่รัน solver และไม่อ้างสมรรถนะใด

## หลักฐานตั้งต้นที่วัดเมื่อ 2026-09-20

- `artifacts/work062/stage_ledger.jsonl`: ผู้เข้ารอบ 72 แบบเข้าสู่ refinement ผ่าน 51 แบบ และถูกตัด 21 แบบด้วย `refined_disagreement` ทั้ง 21 แบบทุก holdout case บันทึก `converged: true` คู่กับ `fine_cross_model_passed: false` และขั้น CAD ของทั้งหมดบันทึก `not_run` การตัดจึงเกิดจากโมเดลไม่ตรงกัน ไม่ใช่ solver ล้มเหลว
- `artifacts/work062/result_ledger.jsonl`: ประเมิน 2,880 ครั้ง เป็น `feasible` 2,107 ครั้ง `structural_failure` 773 ครั้ง และไม่มี failure code อื่น
- `src/formula_ultimate/experiments/main_campaign_protocol.py`: พื้นที่ candidate คือตัวแปรสเกล 5 ตัว ขอบเขต `0.8`–`1.2`
- `src/formula_ultimate/experiments/whole_vehicle_search.py`: `capacity_factor` คือ `min(core_width_scale, contact_radius_scale**2, source_size_scale**2, propulsor_size_scale**2)` และ utilization คือโหลดที่ freeze ไว้จาก Work 048 คูณ `mass_ratio / capacity_factor` นี่คือกฎสเกลที่ผูกกับ template เดียว ไม่ใช่การประเมิน geometry
- `scripts/cad/generate_vehicle_assembly.py`: `shape_for()` สร้างได้เฉพาะ box หรือ cylinder เท่านั้น
- `artifacts/work092/run_e/`: free-form solid สิบชิ้น รวม `curved_branch` และ `organic_load_bridge` แต่ละชิ้นเป็น solid เดียวที่ valid และใช้ operator ครบทั้ง 18 ตัว grammar รูปทรงอิสระใช้งานได้จริงแต่ไม่เคยไปถึง candidate ของรถหรือ race simulator
- runtime ที่มีอยู่: CadQuery `2.8.0` ใน `.tools/cadquery-mcp` กับ `gmsh.exe` และ `ccx.exe` ใน `C:/Program Files/FreeCAD 1.1/bin` โดย `gmsh` import เป็นโมดูล Python ไม่ได้ Work 138 จึงต้องเรียกไฟล์ executable เหมือนที่ `scripts/structural/run_beam_bending_acceptance.py` ทำอยู่แล้ว
- ส่วนที่นำกลับมาใช้ได้: `structural/element_verification.py` อ่าน Gmsh `msh2` และสร้าง deck C3D4/C3D10 ของ CalculiX ได้ ส่วน `structural/refined_mesh.py` และ `structural/acceptance.py` มี logic ของ refinement และ acceptance อยู่แล้ว ขณะที่ `structural/geometry_mesh_bridge.py` เป็น bridge จาก labelled cell ไม่ใช่ตัวอ่าน STEP Work 138 จึงต้องมีเส้นทาง STEP ใหม่

## ไฟล์ที่วางแผน

- `docs/plans/detailed_part_to_vehicle_v1/work138-geometry_general_evaluator.md` และคู่ภาษาไทย
- `docs/plans/detailed_part_to_vehicle_v1/README.md` และคู่ภาษาไทย: เพิ่มแถว Work 137 และ Work 138 พร้อมการ map เลขงาน
- แผน Work 137 สองภาษานี้และผลลัพธ์สองภาษาที่ตรงกัน

## การตรวจสอบ

1. ตรวจ static contract ว่าการ์ดแผนทั้งสองภาษามี token ที่กำหนด และดัชนีทั้งสองภาษาลิงก์ไปยังการ์ดใหม่
2. `python -m unittest tests.test_repository_contract -v`: exit 0
3. `git diff --check` และ `git diff --cached --check`: exit 0

## เกณฑ์สำเร็จและล้มเหลว

สำเร็จ: การ์ด Work 138 กำหนด inputs, representation, สัญญาของ mesh และ solver, การลงทะเบียน refinement, negative controls, acceptance, artifacts, replay, tests, ความเสี่ยงและ non-goals ครบ และทุกตัวเลขตั้งต้นข้างต้นอ้างกลับไปยัง artifact หรือ path ที่ระบุชื่อได้ ล้มเหลว: การ์ดอ้างว่า capability ถูก implement แล้ว อ้างตัวเลขที่ไม่มีที่มา หรือกำหนด conventional vehicle layout

## ความเสี่ยงและสิ่งที่ไม่ทำ

- ความเสี่ยง: evaluator ที่รับ geometry ใดก็ได้ช้ากว่ากฎสเกล campaign อาจแพงเกินรับไหว การ์ดจึงต้องลงทะเบียนงบคำนวณและ fidelity ladder แทนการสมมติว่าทุก candidate จะ mesh และแก้สมการได้
- ความเสี่ยง: การเปลี่ยน evaluator ทำให้เทียบกับผลรันเก่าไม่ได้ การ์ดต้องบังคับให้ประเมิน baseline ใหม่ด้วย evaluator เดียวกันก่อนเปรียบเทียบ
- สิ่งที่ไม่ทำ: ไม่ implement ไม่รัน solver ไม่แก้บันทึกของ Work 062 หรือ Work 135 ไม่ push และไม่เขียนประวัติใหม่
