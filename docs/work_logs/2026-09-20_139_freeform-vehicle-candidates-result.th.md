# ผลลัพธ์ Work 139: Vehicle Candidate ที่ใช้รูปทรงอิสระ

แหล่งภาษาอังกฤษ: `2026-09-20_139_freeform-vehicle-candidates-result.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์

vehicle candidate บรรจุ free-form solid ในตำแหน่งหน้าที่ได้แล้ว งานนี้ประกาศ candidate สองตัว สร้างด้วย CadQuery ตรวจ gate จาก solid ที่สร้างจริง และประเมินทีละ component ด้วย evaluator ของ Work 138 control ทั้งแปดข้อถูกปฏิเสธ และการ replay บน tree ที่สะอาดให้ result SHA-256 ตรงกันทุกประการ

สถานะที่ยอมรับคือ `passed_freeform_vehicle_composition` หมายถึง candidate สร้างได้ จัดวางได้ และประเมินได้ สรุปผลระบุ `discovery_claim`, `promotion_allowed`, `race_time_claim` และ `physical_validation` เป็นเท็จ และมี control หนึ่งข้อตรวจข้อนี้โดยตรง

## ผลที่วัดได้

Result SHA-256 `5f4a0e831d91dd7dc27496f6c4e8e0280aaca94a1e5ca6c9ce4c254c2bef2874` และ `run_b` ตรงกันทุกประการ

| Candidate | Packaging | มวล | จำนวน component | สถานะ |
| --- | --- | ---: | ---: | --- |
| `primitive_baseline_139` | `passed` | 30.6572 kg | 4 | `passed` 4 ชิ้น |
| `freeform_variant_139` | `passed` | 28.0482 kg | 4 | `passed` 3 ชิ้น, `unresolved_convergence` 1 ชิ้น |

ทั้งคู่ต่างกันที่ component เดียวคือ `propulsor`

| | Baseline | ตัวแปรรูปทรงอิสระ |
| --- | --- | --- |
| geometry | `box` 0.1 × 0.1 × 0.1 m | `curved_branch_001` จาก corpus ของ Work 092 |
| จำนวนผิวโค้ง | 0 | 3 |
| มวลของ component | 2.7000 kg | 0.0911 kg |
| สถานะของ component | `passed` | `unresolved_convergence` |
| utilization | 0.000868 | 0.304135 |
| มวลของ candidate | 30.6572 kg | 28.0482 kg (`-2.6089 kg`) |

candidate ทั้งสองวัดได้ว่าไม่มีการตัดกันเป็นคู่และไม่มีการรุกล้ำ keep-out จาก solid ที่สร้างจริง ส่วน core, source และ contact เหมือนกันทั้งคู่และให้ตัวเลขตรงกัน ซึ่งเป็นพฤติกรรมที่คาดหวังของการจับคู่

**สิ่งที่ยืนยันได้และไม่ได้** ยืนยันได้ว่า free-form solid ที่ยอมรับแล้วเข้าไปอยู่ในตำแหน่งหน้าที่ได้ ผ่าน gate การจัดวางที่วัดจาก geometry จริง และถูกให้คะแนนด้วย evaluator เดียวกับ primitive แต่ **ไม่ได้** ยืนยันว่าชิ้นโค้งดีกว่า เพราะมวลที่น้อยกว่ามาพร้อม utilization `0.304` เทียบกับ `0.000868` คือใช้กำลังที่ยอมให้ไปมากกว่าราว 350 เท่า และการลู่เข้ายังไม่ผ่านบน ladder ที่ลงทะเบียน การแทนหนึ่งชิ้นภายใต้ load case เดียวจึงรองรับข้ออ้างเรื่องความเหนือกว่า การค้นพบ หรือ promotion ไม่ได้ และไฟล์ผลลัพธ์ระบุข้อนี้ไว้ใน `matched_report.interpretation`

## ส่วนที่ต่างจากแผน

ไม่มี ขอบเขต การตรวจสอบ และสิ่งที่ไม่ทำ เป็นไปตามแผนที่เขียนไว้

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/search/freeform_vehicle_candidate.py`
- `scripts/cad/build_freeform_vehicle_candidate.py`
- `scripts/development/run_freeform_vehicle_candidate.py`
- `config/development/freeform_vehicle_candidate_v1.json`
- `tests/test_freeform_vehicle_candidate.py`
- `docs/contracts/FREEFORM_VEHICLE_CANDIDATE_V1.md` และคู่ภาษาไทย
- `docs/plans/detailed_part_to_vehicle_v1/work139-freeform_vehicle_candidates.md` คู่ภาษาไทย และดัชนีสองภาษา
- แผนและผลลัพธ์สองภาษานี้

หลักฐานที่สร้างขึ้นยังถูก ignore ไว้ใต้ `artifacts/work139/{pilot,run_a,run_b}`

## รายงานบั๊ก

1. **path แบบ relative ทำให้ตัว build พัง** อาการ: การ build หยุดด้วย `'artifacts\work139\pilot\cad\primitive_baseline_139\core.step' is not in the subpath of 'C:\Formula Ultimate'` สาเหตุ: ตัว build เรียก `Path.relative_to(ROOT)` บน path ที่ runner ส่งมาแบบ relative การแก้: `_repository_path` resolve เทียบ working directory ก่อน แล้วค่อยแปลงเป็นรูป POSIX ที่อ้างอิงรากของ repository
2. **control เรื่องความ deterministic hash ข้อมูลผิดชุด** อาการ: `AttributeError: 'list' object has no attribute 'get'` ระหว่างรัน control สาเหตุ: control เรียก `strip_process_evidence` ซ้ำกับ list ของรายการที่ถูก strip ไปแล้ว การแก้: control hash บันทึกที่รายงานโดยตรง แล้วเทียบกับการ round trip ผ่าน JSON
3. **hash ของ manifest ขึ้นกับไดเรกทอรีผลลัพธ์** อาการ: `run_b` ต่างจาก `run_a` ที่ `manifest_sha256` ทั้งสองค่าและที่ result hash ทั้งที่ hash ของ STEP ทุกไฟล์ตรงกัน สาเหตุ: body ที่ถูก hash มี `step_path` และ `assembly_step_path` ซึ่งมีชื่อไดเรกทอรีของการรัน การแก้: hash ของ manifest ครอบคลุมเฉพาะตัวตนของ geometry โดยยังเก็บ path ไว้ใน manifest เพื่อใช้งานแต่ไม่นำไป hash การทดสอบกำกับ: `run_a` กับ `run_b` ให้ result SHA-256 เดียวกัน

## การตรวจสอบ

สภาพแวดล้อม: Windows 11, Python 3.14.3, CadQuery 2.8.0 ใน `.tools/cadquery-mcp`, Gmsh 4.15.0 และ CalculiX 2.22 จาก `C:/Program Files/FreeCAD 1.1/bin`

```text
Command: python -m unittest tests.test_freeform_vehicle_candidate -v
Exit code: 0
Result: Ran 13 tests — OK (การทดสอบที่ build ด้วย CadQuery รันจริง และจะข้ามเมื่อไม่มี runtime)

Command: python scripts/development/run_freeform_vehicle_candidate.py --config config/development/freeform_vehicle_candidate_v1.json --output-root artifacts/work139/run_a
Exit code: 0
Result: passed_freeform_vehicle_composition; control 8/8 ถูกปฏิเสธ; unresolved 1 component;
        result SHA-256 5f4a0e831d91dd7dc27496f6c4e8e0280aaca94a1e5ca6c9ce4c254c2bef2874

Command: python scripts/development/run_freeform_vehicle_candidate.py --config ... --output-root artifacts/work139/run_b --replay-reference artifacts/work139/run_a/result.json
Exit code: 0
Result: replay exact: true

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 1001 tests — OK (skipped=11)

Command: python -m compileall -q src scripts tests
Exit code: 0

Command: python -m unittest tests.test_repository_contract
Exit code: 0
Result: Ran 6 tests — OK

Command: git diff --check ; git diff --cached --check
Exit code: 0
```

## ข้ออ้าง

- รองรับ: free-form solid ที่ยอมรับแล้วประกอบเข้าเป็น vehicle candidate ได้ ผ่าน gate เรื่อง envelope, การตัดกัน, keep-out และการครอบคลุมหน้าที่ ซึ่งวัดจาก solid ที่สร้างจริง และถูกให้คะแนนด้วย evaluator ของ Work 138 พร้อม replay ได้ตรงทุกประการ
- ไม่รองรับ: ตัวแปรรูปทรงอิสระดีกว่า เบากว่าในเชิงที่มีความหมาย หรือเป็นการค้นพบ, สมาชิก corpus เหมาะกับงานขับเคลื่อนเกินกว่าการอยู่ในตำแหน่งเชิงเรขาคณิต, หรือ candidate ใด promote ได้ ผลิตได้ หรือผ่าน physical validation

## ข้อจำกัดและงานถัดไป

- สมาชิก corpus วางตำแหน่งได้แต่ย่อขยายไม่ได้ ความพอดีกับตำแหน่งจึงเป็นเรื่องบังเอิญมากกว่าการออกแบบ การทำตระกูลรูปทรงอิสระแบบพารามิเตอร์เป็นงานถัดไป
- component รูปทรงอิสระยังเป็น `unresolved_convergence` บน ladder ที่ลงทะเบียน ซึ่งสืบทอดข้อจำกัดจาก Work 138 การมี ladder ที่คำนึงถึงความโค้งจะแก้เรื่องนี้
- มี load case เดียวต่อ component และยังไม่มีเส้นทางโหลดระดับ assembly component จึงถูกประเมินแยกชิ้น ไม่ใช่ในฐานะโครงสร้างที่เชื่อมกัน
- มวลระดับรถเป็นผลรวมของมวล component ยังไม่มีมวลของข้อต่อ ตัวยึด หรือ interface
- ถัดไป: Work 140 ที่ป้อนผล evaluator เข้าสู่เวลาแข่ง จากนั้นคือการค้นหาบนองค์ประกอบรูปทรงอิสระ แทนการประกาศคู่เดียว
