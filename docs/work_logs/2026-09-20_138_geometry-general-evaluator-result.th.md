# ผลลัพธ์ Work 138: Structural Evaluator ที่รับ Geometry ใดก็ได้

แหล่งภาษาอังกฤษ: `2026-09-20_138_geometry-general-evaluator-result.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์

evaluator ที่ Work 137 กำหนดไว้มีอยู่จริงและรันได้แล้ว solid เดียวที่ถูกต้องถูกให้คะแนนจาก geometry ของตัวเอง ตามเส้นทาง `STEP -> Gmsh tetrahedra อันดับสอง -> CalculiX C3D10 -> mass properties, displacement, von Mises, สมดุลแรงปฏิกิริยา -> สถานะที่ลงทะเบียนหนึ่งค่า` ประเมิน candidate สี่ตัว ตัวละสามระดับความละเอียด control ทั้งแปดข้อถูกปฏิเสธ และการ replay บน tree ที่สะอาดให้ result SHA-256 ตรงกันทุกประการ

สถานะที่ยอมรับคือ `passed_geometry_general_structural_evaluation` ซึ่งหมายถึงการประเมินเชิงโครงสร้างของ solid ที่ประกาศภายใต้ load case ที่ประกาศ ไม่ใช่ promotion ไม่ใช่ความเป็นไปได้ในการผลิต ไม่ใช่เวลาแข่ง และไม่ใช่ physical validation

## ผลที่วัดได้

Result SHA-256 `50e50ed6fa8aa3dfe93804f3a3e67a1471331b203c0da4c1d1c6001d0054d6ec` และ `run_b` ตรงกันทุกประการ

| Candidate | สถานะ | mesh ละเอียดสุด | มวลจาก mesh | displacement สูงสุด | von Mises สูงสุด | utilization |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `cantilever_benchmark` | `passed` | 34,122 node | 3.9000 kg | 0.591937 mm | 14.51 MPa | 0.0415 |
| `work135_frame_spine` | `passed` | 8,829 node | 153.1728 kg | 32.11 mm | 86.44 MPa | 0.3602 |
| `work092_curved_branch` | `unresolved_convergence` | 1,406 node | 0.0831 kg | 0.491 mm | 78.61 MPa | 0.3275 |
| `work062_cut_candidate_core` | `passed` | 6,877 node | 17.7555 kg | 0.0314 mm | 2.50 MPa | 0.0104 |

- **benchmark เชิงวิเคราะห์ผ่าน** ระดับละเอียดสุดของคานให้ `0.5919367 mm` เทียบกับ Euler-Bernoulli `0.5952381 mm` คลาดเคลื่อน `0.55%` ภายในเกณฑ์ `10%` ที่ลงทะเบียนไว้ ทั้งสายตั้งแต่ mesh, deck, การแก้สมการ จนถึงการอ่านผล จึงยึดกับคำตอบรูปปิด
- **มวลมาจากการคำนวณ ไม่ใช่การประกาศ** สำหรับ `frame_spine` mesh ให้ `153.1728 kg` เทียบกับมวล CadQuery ของ Work 135 ที่ `153.1054 kg` residual `0.00044` ซึ่งอยู่ในเกณฑ์ `0.05` ที่ลงทะเบียนไว้ evaluator จึงคำนวณ mass property ของ CAD ซ้ำได้เองจาก tetrahedra
- **ชิ้นที่หนักที่สุดของ Work 135 มีหลักฐานการรับโหลดแล้ว** ภายใต้แรงลัพธ์แนวดิ่ง `10 kN` ที่ประกาศบนผิวด้านท้าย spine frame โก่ง `32 mm` และมีค่าสูงสุด `86.4 MPa` คิดเป็น utilization `0.36` เทียบค่าที่ยอมให้ `240 MPa` นี่เป็นครั้งแรกที่ชิ้นส่วนใดของ Work 135 ถูกประเมินด้วยฟิสิกส์ แทนที่จะด้วยความหนาที่ประกาศไว้
- **รูปทรงที่ evaluator ของ campaign ให้คะแนนไม่ได้ ถูกให้คะแนนแล้ว** `curved_branch_001` จาก free-form corpus ของ Work 092 ทำ mesh และแก้สมการได้ ซึ่ง evaluator แบบกฎสเกลห้าตัวแปรทำไม่ได้เลย ผลที่ลงทะเบียนคือ `unresolved_convergence` เพราะสองระดับสุดท้ายเปลี่ยน `15.7%` ใน displacement และ `42.7%` ใน p90 stress เทียบขีดจำกัด `5%` และ `20%` ladder ที่ลงทะเบียนยังไม่ละเอียดพอสำหรับรูปทรงนี้ และระดับกลางยังให้ node น้อยกว่าระดับหยาบ (804 เทียบ 844) แสดงว่า `Mesh.MeshSizeFactor` ไม่ monotone กับชิ้นนี้ ผลนี้บันทึกเป็นหลักฐานด้านเครื่องมือ ไม่ใช่คำตัดสินต่อชิ้นงาน และไม่ได้ปรับเกณฑ์ย้อนหลังให้ผ่าน
- **candidate ที่ถูกตัดใน Work 062 ถูกประเมินใหม่** `candidate-000847d87c0270ab` เป็นหนึ่งใน 21 ผู้เข้ารอบที่ถูกตัดด้วย `refined_disagreement` และขั้น CAD ไม่เคยรัน งานนี้สร้าง assembly ของมันขึ้นใหม่จากตัวแปรที่ผนึกไว้ใน `artifacts/work062/result_ledger.jsonl` ผ่าน `mutate_candidate_assembly` แล้วส่งออกชิ้น core เป็น STEP ด้วย CadQuery และ evaluator นี้ให้ผล `passed` ที่ utilization `0.0104`

**ผลนี้ไม่ได้กลับคำตัดสินของ Work 062 และขอแก้ถ้อยคำของการ์ดตรงนี้** เพราะ gate ของ Work 062 เทียบโมเดลคานของโปรเจกต์กับ section force แบบ B31 ของ CalculiX บน load case ของ Work 048 ขณะที่การรันนี้ใส่ load case แบบ solid ที่ประกาศใหม่กับชิ้นส่วนเดียว ทั้งสองจึงเทียบกันไม่ได้ สิ่งที่ยืนยันได้จึงแคบกว่าแต่ยังมีประโยชน์ คือ geometry ของ candidate ที่ campaign ทิ้งไปนั้นประเมินได้ และการทิ้งเกิดจากโมเดลไม่ตรงกัน ไม่ใช่ solver ล้มเหลว การประเมินที่เทียบกันได้จริงต้องใช้ load case ของ Work 048 กับ assembly ทั้งชุด ซึ่งเป็นงานถัดไป

## ส่วนที่ต่างจากแผน

แผนระบุ `carrier_plate` เป็น candidate คู่กับ `spine_frame` แต่ถูกแทนด้วย `work062_cut_candidate_core` เพราะ control ข้อ 8 ต้องใช้ candidate ที่ถูกตัดใน Work 062 พร้อม geometry จริง และคงจำนวน candidate ไว้ที่สี่ตัว ส่วน `carrier_plate` ยังมีอยู่และยังไม่ได้ประเมิน

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/structural/geometry_general_evaluator.py`
- `scripts/structural/mesh_step_solid.py`
- `scripts/structural/run_geometry_general_evaluator.py`
- `config/development/geometry_general_evaluator_v1.json`
- `tests/test_geometry_general_evaluator.py`
- `docs/contracts/GEOMETRY_GENERAL_EVALUATOR_V1.md` และคู่ภาษาไทย
- แผนและผลลัพธ์สองภาษานี้

หลักฐานที่สร้างขึ้นยังถูก ignore ไว้ใต้ `artifacts/work138/{inputs,pilot,run_a,run_b}`

## รายงานบั๊ก

1. **CalculiX ตัด field ตัวเลขที่ยาวอย่างเงียบ ๆ** อาการ: deck ที่เขียนพิกัดด้วย `:.17g` ถูกปฏิเสธด้วย exit 201 และข้อความ `node 12 is not defined` สาเหตุที่หาได้จากการทดสอบแบบควบคุม ไม่ใช่การเดา: CalculiX อ่าน free field ลงบัฟเฟอร์ 20 ตัวอักษร ที่ 21 ตัวอักษร `-1.00000000000000e+03` ถูกอ่านเป็น `-1.0` และคืน **exit code 0** พร้อม displacement ที่เล็กกว่าจริง `1000 เท่า` ส่วนที่ 22 ตัวอักษรขึ้นไปการรันจะหยุด Work 085 เคยเจอโหมดที่หยุดและแก้ไว้ในรันเนอร์ของตัวเอง ส่วนโหมดที่เงียบถูกบันทึกที่นี่เป็นครั้งแรก การแก้: ทุก field ตัวเลขเขียนผ่าน `calculix_number` ซึ่งลดความละเอียดจนกว่าจะพอดี และ `build_deck` ตรวจซ้ำทุก field ตัวเลขก่อนส่ง deck ให้ solver การทดสอบกำกับ: `CalculiXFieldTests` ตรวจขีดจำกัด ความแม่นของการแปลงกลับ และการปฏิเสธค่าที่ไม่จำกัด
2. **element อันดับสองแบบโค้งกลับด้าน** อาการ: `frame_spine` ล้มเหลวทั้งสามระดับด้วย `*ERROR in e_c3d: nonpositive jacobian determinant` โดยระดับหยาบสุดมี 85 element การตั้ง `Mesh.HighOrderOptimize = 2` ลดเหลือ 5 และ `= 4` ยังเหลือ 83 จึงแก้ไม่จบด้วยการ optimize อย่างเดียว สาเหตุ: node กึ่งกลางที่ถูกดัดไปตามผิวโค้งของชิ้นงานทำให้ element C3D10 กลับด้าน การแก้: `Mesh.SecondOrderLinear = 1` ใช้ tetrahedra อันดับสองแบบขอบตรง หลังจากนั้นไม่มี jacobian error เลย ต้นทุนคือผิวโค้งกลายเป็นเหลี่ยม ซึ่งระบุไว้ในสัญญาแล้ว
3. **path แบบ relative ทำให้ mesher พัง** อาการ: ทุก candidate ได้ `unresolved_mesh` พร้อมข้อความ `Unable to open file ... part.geo` สาเหตุ: Gmsh ถูกรันด้วย `cwd` เป็นไดเรกทอรีงาน แต่รับ path ที่อ้างอิงจากรากของ repository การแก้: resolve ทั้งสอง path ก่อนเรียก
4. **ตัวตรวจความกว้างของ field ปฏิเสธบรรทัดหัวเรื่อง** อาการ: ทุก candidate ได้ `unsupported_representation` พร้อมข้อความ "deck contains a field CalculiX would truncate" สาเหตุ: ตัวตรวจวัดบรรทัดข้อความอิสระที่ต่อจาก `*HEADING` การแก้: ข้ามบรรทัดหัวเรื่อง และวัดเฉพาะ field ที่แปลงเป็นตัวเลขได้
5. **control เรื่องความ deterministic เองกลับไม่ deterministic** อาการ: `run_b` ต่างจาก `run_a` ที่ค่าเดียวคือ hash ของ `deterministic_restatement` สาเหตุ: control นั้น hash บันทึก candidate ที่รวมหลักฐาน process ซึ่งมีเวลานาฬิกา การแก้: ทั้ง control และผลที่เผยแพร่ hash บันทึกชุดเดียวกันที่ตัดหลักฐาน process ออกแล้ว การทดสอบกำกับ: `run_a` กับ `run_b` ตรงกันทุกประการ

## การตรวจสอบ

สภาพแวดล้อม: Windows 11, Python 3.14.3, Gmsh 4.15.0 และ CalculiX 2.22 จาก `C:/Program Files/FreeCAD 1.1/bin`, CadQuery 2.8.0 ใน `.tools/cadquery-mcp`

```text
Command: python -m unittest tests.test_geometry_general_evaluator -v
Exit code: 0
Result: Ran 24 tests — OK (การทดสอบ kernel ที่ใช้ Gmsh/CalculiX รันจริง และจะข้ามเมื่อไม่มี runtime)

Command: python scripts/structural/run_geometry_general_evaluator.py --config config/development/geometry_general_evaluator_v1.json --output-root artifacts/work138/run_a
Exit code: 0
Result: passed_geometry_general_structural_evaluation; ผ่าน 3, unresolved_convergence 1; control 8/8 ถูกปฏิเสธ;
        result SHA-256 50e50ed6fa8aa3dfe93804f3a3e67a1471331b203c0da4c1d1c6001d0054d6ec

Command: python scripts/structural/run_geometry_general_evaluator.py --config ... --output-root artifacts/work138/run_b --replay-reference artifacts/work138/run_a/result.json
Exit code: 0
Result: replay exact: true

Command: .tools/cadquery-mcp/Scripts/python.exe scripts/cad/generate_vehicle_assembly.py --config artifacts/work138/inputs/work062_cut_candidate.json --output-root artifacts/work138/inputs/work062_step --manifest artifacts/work138/inputs/work062_manifest.json
Exit code: 0
Result: solid ที่ถูกต้อง 4 ชิ้น; assembly SHA-256 8ccc596889bd599f0a5cfbbdada58513bd5de2d6b049b9dd87c7615e3c970253

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 988 tests — OK (skipped=11)

Command: python -m compileall -q src scripts tests
Exit code: 0

Command: git diff --check ; git diff --cached --check
Exit code: 0
```

## ข้ออ้าง

- รองรับ: solid เดียวที่ถูกต้องแบบใดก็ได้ รวมถึงรูปทรงอิสระ สามารถ mesh แก้สมการ และจำแนกสถานะได้แล้ว, ทั้งสายตรงกับคำตอบรูปปิดที่ `0.55%`, มวลจาก mesh ตรงกับมวล CadQuery ของ Work 135 ที่ `0.04%` และการรัน replay ได้ตรงทุกประการ
- ไม่รองรับ: การตัดใน Work 062 ผิด, spine frame ของ Work 135 เพียงพอหรือเหมาะสมที่สุด เพราะใส่ load case เดียว, หรือ candidate ใดผลิตได้ promote ได้ หรือผ่าน physical validation วัสดุเป็นค่าสังเคราะห์สำหรับ geometry เท่านั้น

## ข้อจำกัดและงานถัดไป

- ประเมิน load case เดียวต่อ candidate แม้ schema จะรองรับหลาย case แต่ยังไม่ได้ไล่ครบ
- element ขอบตรงประมาณผิวโค้ง จึงต้องมี ladder ที่คำนึงถึงความโค้งสำหรับชิ้นอย่าง `curved_branch_001` ซึ่ง ladder ปัจจุบันไม่ monotone
- `artifacts/` ถูก ignore ไว้ ดังนั้นต้องสร้าง STEP ของ candidate จาก Work 062 ใหม่ด้วยคำสั่งข้างต้นก่อน จึงจะรัน candidate นั้นซ้ำได้ใน checkout ที่สะอาด
- `acceptance.py` และ `element_verification.py` ยังเขียน field ของโหลดด้วย `:.17g` ค่าทศนิยมธรรมดาถูกตัดโดยไม่เสียหาย แต่ค่าวิทยาศาสตร์ขนาดเล็กจะเจอบั๊กข้อ 1 ควรมีงานแยกที่เปลี่ยนให้เขียนผ่าน `calculix_number`
- ถัดไป: ใส่ load case ของ Work 048 กับ assembly ของ Work 062 ที่สร้างใหม่ทั้งชุด เพื่อการประเมินที่เทียบกันได้ จากนั้นคือ Work 139 ที่เปิด grammar รูปทรงอิสระให้ candidate ของรถ และ Work 140 ที่ป้อนผล evaluator เข้าสู่เวลาแข่ง
