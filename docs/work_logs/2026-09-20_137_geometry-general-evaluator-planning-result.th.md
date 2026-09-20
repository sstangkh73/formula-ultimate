# ผลลัพธ์ Work 137: การวางแผน Geometry-General Evaluator

แหล่งภาษาอังกฤษ: `2026-09-20_137_geometry-general-evaluator-planning-result.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์

เขียนการ์ด Work 138 สองภาษาที่พร้อมดำเนินการ สำหรับ structural evaluator ที่รับ geometry ใดก็ได้ และบันทึกการ map เลขงานไว้ในดัชนีแผนละเอียดสองภาษา การ์ดกำหนดให้มีเส้นทาง `STEP -> Gmsh -> CalculiX C3D10 -> properties` ที่รับ solid ที่ถูกต้องแบบใดก็ได้ มีชุดสถานะหกค่าที่แยก `failed_physics` ออกจาก `unresolved_mesh`, `unresolved_solver` และ `unresolved_convergence` มี falsification control แปดข้อ มี refinement อย่างน้อยสามระดับ มีงบคำนวณ และต้อง replay ได้ตรงทุกประการ

งานนี้เปลี่ยนเฉพาะหลักฐานเชิงการวางแผน ไม่ได้ implement evaluator ไม่ได้รัน mesher หรือ solver และไม่ได้อ้างสมรรถนะ ความเป็นไปได้ หรือ promotion ใด

## หลักฐานตั้งต้นที่วัดได้เบื้องหลังการ์ด

ทุกตัวเลขในการ์ดอ้างกลับไปยัง path ที่ระบุชื่อได้ และวัดในเซสชันนี้

- `artifacts/work062/stage_ledger.jsonl`: refinement 72 รายการ ผ่าน 51 และ `failed` 21 ด้วย `refined_disagreement` ส่วน CAD witness 72 รายการ ผ่าน 51 และ `not_run` 21 ใน 21 แบบที่ถูกตัด ทุก holdout case มี `converged: true` คู่กับ `fine_cross_model_passed: false` การตัดจึงเกิดจากโมเดลไม่ตรงกัน ไม่ใช่ solver ล้มเหลว
- `artifacts/work062/result_ledger.jsonl`: ประเมิน 2,880 ครั้ง เป็น `feasible` 2,107 ครั้ง `structural_failure` 773 ครั้ง ไม่มี failure code อื่น
- `artifacts/work092/run_e/`: free-form solid 10 ชิ้น แต่ละชิ้นเป็น solid เดียวที่ valid และครอบคลุม operator ทั้ง 18 ตัว
- path ต้นทางของการล็อก template: `main_campaign_protocol.py` (ตัวแปรสเกล 5 ตัว ช่วง `0.8`–`1.2`), `whole_vehicle_search.py` (กฎสเกล `capacity_factor`), `generate_vehicle_assembly.py` (มีแค่ box หรือ cylinder) และ `config/development/native_detailed_vehicle_v1.json` (ชนิดชิ้นส่วนที่เขียนมือ 48 แบบ)

ตัวเลขอื่นที่พบใน `artifacts/` เช่น `unsupported_overhang` 24 และ `unsupported_wall` 12 **ไม่ถูกใช้** เป็นหลักฐาน เพราะ `artifacts/work095/run_a/result.json` กระจายสาเหตุการปฏิเสธอย่างละหนึ่งพอดีใน 6 family และระบุไว้เองว่า `"matched synthetic gate behavior only; no source STEP"` จึงเป็นเมทริกซ์ fixture ที่ออกแบบไว้ ไม่ใช่ yield ที่วัดได้

## ไฟล์ที่เปลี่ยน

- `docs/plans/detailed_part_to_vehicle_v1/work138-geometry_general_evaluator.md` และคู่ภาษาไทย
- `docs/plans/detailed_part_to_vehicle_v1/README.md` และคู่ภาษาไทย
- แผนและผลลัพธ์ Work 137 สองภาษานี้

## การตัดสินใจ

- **แก้ evaluator ก่อน grammar:** ถ้าเปิด grammar รูปทรงอิสระก่อน candidate ที่ได้จะเป็นแบบที่ evaluator ให้คะแนนไม่ได้ และจะถูกตัดเพราะไม่มีตัวประเมิน การ์ดจึงแก้การประเมินก่อน แล้วเลื่อน grammar ไป Work 139 และการเชื่อมกับเวลาแข่งไป Work 140
- **ชุดสถานะ:** แยก `unresolved_*` ออกจาก `failed_physics` เพื่อไม่ให้ข้อจำกัดของ solver ถูกบันทึกเป็นคำตัดสินทางฟิสิกส์ และเพื่อให้การกระจายสาเหตุ unresolved กลายเป็นหลักฐานว่าควรเพิ่ม capability ใดต่อ
- **Control ข้อ 8:** บังคับให้นำ candidate 21 แบบที่ถูกตัดด้วย `refined_disagreement` มาประเมินใหม่ และการ์ดกำหนดให้รายงานกรณีที่ยืนยันการตัดเดิมอย่างตรงไปตรงมาเท่ากับกรณีที่กลับคำตัดสิน
- **ความยุติธรรมในการเปรียบเทียบ:** การ์ดห้ามนำผลจากกฎสเกลไปเทียบกับผลจาก evaluator และบังคับให้ประเมิน baseline ใหม่ด้วยการลงทะเบียนเดียวกัน
- **การเข้าถึง runtime:** `gmsh` import ใน environment CadQuery ที่ pin ไว้ไม่ได้ การ์ดจึงกำหนดให้เรียก `gmsh.exe` ใน `C:/Program Files/FreeCAD 1.1/bin` เหมือนที่ `scripts/structural/run_beam_bending_acceptance.py` ทำอยู่ ส่วน `ccx.exe` อยู่ในไดเรกทอรีเดียวกัน
- **เลขงาน:** 136 และ 137 ถูกใช้ไปแล้ว งานรันฟิสิกส์บน native solid ที่ Work 135 เรียกว่า "Work 136" จะใช้เลขถัดไปที่ยังว่างตอนลงมือ ดัชนีบันทึกเรื่องนี้ไว้โดยไม่เขียนบันทึกของ Work 135 ใหม่

## การตรวจสอบ

สภาพแวดล้อม: Windows 11, Python 3.14.3

```text
Command: ตรวจ static contract ของแผน Work 138 สองภาษาและดัชนี (token ที่ต้องมี 14 รายการต่อภาษา, การอ้างแหล่งภาษาอังกฤษในไฟล์ไทย, ลิงก์ในดัชนีทั้งสองภาษา)
Exit code: 0
Result: work138_plan_contract: PASS

Command: python -m unittest tests.test_repository_contract
Exit code: 0
Result: Ran 6 tests — OK

Command: git diff --check
Exit code: 0

Command: git diff --cached --check
Exit code: 0
```

## ข้ออ้าง

- รองรับ: ตัวเลขตั้งต้นข้างต้นทำซ้ำได้จากไฟล์ artifact ที่ระบุชื่อ ณ commit นี้
- ไม่รองรับ: การมีอยู่ของ geometry-general evaluator, การที่ชิ้นส่วนของ Work 135 จะ mesh ได้สำเร็จ หรือการที่ candidate 21 แบบที่ถูกตัดจะผ่านภายใต้ evaluator นี้ ทั้งหมดเป็นคำถามเปิดที่การ์ดออกแบบไว้เพื่อตอบ

## ข้อจำกัดและงานถัดไป

คำสั่งของ Work 138 เป็นเอกสาร ยังไม่ถูกรัน งานนี้จึงไม่ได้สร้าง mesh, การแก้สมการ, โมดูล evaluator, configuration หรือการทดสอบใด งานที่ต้องลงมือถัดไปคือ Work 138 ส่วน Work 139 และ Work 140 ยังต้องเขียนการ์ดของตัวเอง
