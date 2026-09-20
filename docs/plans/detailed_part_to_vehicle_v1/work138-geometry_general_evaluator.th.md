# Work 138: Structural evaluator ที่รับ geometry ใดก็ได้

แหล่งภาษาอังกฤษ: `work138-geometry_general_evaluator.md`

Status: Planned

แพ็กเกจเดิมของ Work 106: ไม่มี งานนี้เป็นส่วนขยายเชิงแก้ไขที่เขียนขึ้นโดย Work 137

Dependencies: Work 062 (หลักฐาน campaign), Work 078 และ Work 092 (grammar), Work 110 (mesh bridge), Work 111 (solid fields), Work 135 (native geometry) ส่วนที่นำกลับมาใช้: `element_verification`, `refined_mesh`, `acceptance`

ข้อกำหนดร่วมที่บังคับใช้: [ดัชนีและกฎการดำเนินการ](README.th.md) ตัวเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ได้ implement

## 1. ปัญหาที่งานนี้แก้

evaluator ที่ bounded campaign ใช้อยู่ไม่ได้อ่าน geometry `src/formula_ultimate/experiments/whole_vehicle_search.py` คำนวณ `capacity_factor` จาก `min(core_width_scale, contact_radius_scale**2, source_size_scale**2, propulsor_size_scale**2)` แล้วนำโหลดที่ freeze ไว้จาก Work 048 มาคูณ `mass_ratio / capacity_factor` พื้นที่ candidate ใน `main_campaign_protocol.py` จึงเป็นตัวแปรสเกล 5 ตัวขอบเขต `0.8`–`1.2` และ `scripts/cad/generate_vehicle_assembly.py` สร้างได้เฉพาะ box กับ cylinder

ผลที่วัดได้สองข้อ ทั้งคู่มาจาก `artifacts/work062/` เมื่อ 2026-09-20

1. รูปทรงนอก template ให้คะแนนไม่ได้เลย การค้นหาจึงออกจาก template ไม่ได้ ทั้งที่ grammar รูปทรงอิสระมีอยู่และใช้ได้จริง `artifacts/work092/run_e/` มี free-form candidate สิบชิ้นที่ valid เป็น solid เดียวและครอบคลุม operator ทั้ง 18 ตัว รวม `curved_branch` และ `organic_load_bridge` แต่วันนี้ยังเข้าเป็น candidate ของรถไม่ได้
2. จากผู้เข้ารอบ 72 แบบ มี 21 แบบถูกตัดด้วย `refined_disagreement` ทั้ง 21 แบบทุก holdout case บันทึก `converged: true` คู่กับ `fine_cross_model_passed: false` และขั้น CAD บันทึก `not_run` นั่นคือ solver ทำงานสำเร็จ แต่โมเดลราคาถูกกับ CalculiX ไม่ตรงกัน แล้วระบบทิ้ง candidate แทนที่จะตัดสินด้วยโมเดลที่ดีกว่า

Work 138 ทำให้ geometry เป็นอินพุตของการประเมิน แต่ตัวมันเองยังไม่เปิด grammar การออกแบบ ซึ่งเป็นงานของ Work 139

## 2. ผลลัพธ์และขอบเขตข้ออ้าง

การผ่าน Work 138 หมายถึงเพียง `passed_geometry_general_structural_evaluation` คือมี evaluator ที่รับ solid assembly ที่ถูกต้องแบบใดก็ได้ คำนวณ mass properties และการตอบสนองต่อโหลดด้วยตัวเอง และรายงานสถานะที่ลงทะเบียนไว้ต่อ candidate ไม่ใช่ผลสมรรถนะ ไม่ใช่ promotion ไม่ใช่ความเป็นไปได้ในการผลิต และไม่ใช่ physical validation

## 3. หลักฐานตั้งต้นและตัวตนที่ freeze

ก่อนรัน admitted ใด ๆ ต้องตรึงและบันทึก: commit ของ repository และสถานะ clean tree, เวอร์ชันของ CadQuery, OCCT, FreeCAD, Gmsh และ CalculiX พร้อม SHA-256 ของไฟล์ executable, declaration ของ Work 135 และ hash ของ STEP, รวมถึง hash ของ protocol, result ledger และ stage ledger ของ Work 062 โดย `gmsh` import เป็นโมดูล Python ไม่ได้ใน environment ที่ pin ไว้ จึงต้องเรียก `gmsh.exe` ตามแบบ `scripts/structural/run_beam_bending_acceptance.py`

## 4. ไฟล์ที่เสนอให้ดูแล

- `src/formula_ultimate/structural/geometry_general_evaluator.py`
- `scripts/structural/mesh_step_solid.py` — แปลง STEP เป็น Gmsh `msh2` พร้อมบันทึก option แบบ deterministic
- `scripts/structural/run_geometry_general_evaluator.py`
- `config/development/geometry_general_evaluator_v1.json`
- `tests/test_geometry_general_evaluator.py`
- `docs/contracts/GEOMETRY_GENERAL_EVALUATOR_V1.md` และคู่ภาษาไทย

## 5. สัญญาของการประเมิน

อินพุตคือ solid assembly ในรูป STEP พร้อมวัสดุที่ประกาศต่อ solid และชุด load case ที่ประกาศไว้ ห้าม candidate ประกาศความแข็ง ความแข็งแรง มวล หรือ margin ของตัวเอง

ลำดับการทำงาน

```text
ชุด STEP solid
  -> ตรวจความถูกต้องและความเป็น solid เดียวต่อชิ้น
  -> คำนวณ volume, mass, center of mass และ inertia จาก geometry
  -> สร้าง tetrahedral mesh ด้วย Gmsh อย่างน้อยสามระดับความละเอียด
  -> แก้สมการด้วย CalculiX C3D10 ต่อ load case ที่ลงทะเบียน
  -> displacement, von Mises, สมดุลแรงปฏิกิริยา, utilization เทียบค่าที่ยอมให้
  -> สถานะที่ลงทะเบียนและ hash ของหลักฐาน
```

เอาต์พุตที่ต้องมีต่อ candidate: `mass_kg`, `center_m`, `inertia_kg_m2`, ต่อ case มี `maximum_displacement_m`, `maximum_von_mises_pa`, `utilization`, `reaction_residual_n`, ตัวตนของ mesh ในแต่ละระดับ และบันทึก process ของ solver

## 6. ชุดสถานะ: การตัดต้องถูกจำแนก

evaluator คืนสถานะเดียวต่อ candidate ห้ามปฏิเสธแบบเงียบ

| สถานะ | ความหมาย | ผลต่อการค้นหา |
|---|---|---|
| `passed` | แก้สมการได้และอยู่ในค่าที่ยอมให้ | ไปต่อได้ |
| `failed_physics` | แก้สมการได้และเกินค่าที่ยอมให้ | ปฏิเสธพร้อมสาเหตุ |
| `unresolved_mesh` | สร้าง mesh ไม่ได้แม้ที่ระดับหยาบสุดที่ลงทะเบียน | ลองซ้ำตามงบ แล้วบันทึกเป็น unresolved |
| `unresolved_solver` | solver ลู่ออกหรือทำงานไม่จบ | ลองซ้ำตามงบ แล้วบันทึกเป็น unresolved |
| `unresolved_convergence` | ระดับ refinement ไม่ผ่านเกณฑ์การลู่เข้าที่ลงทะเบียน | บันทึกเป็น unresolved |
| `unsupported_representation` | อินพุตไม่ใช่ solid เดียวที่ถูกต้องต่อชิ้น | ปฏิเสธก่อนทำ mesh |

`unresolved_*` ไม่เท่ากับ `failed_physics` การรันต้องรายงานจำนวนและการกระจายสาเหตุของ candidate ที่ unresolved เพราะการกระจายนี้คือหลักฐานว่าควรเพิ่ม capability ตัวใดต่อ นโยบายการลองซ้ำต้องประกาศก่อนรันและใช้เหมือนกันทุกกลุ่ม

## 7. การลงทะเบียนเชิงตัวเลข

ต้อง freeze ก่อนรัน admitted: ชนิดและลำดับของ element (`C3D10` เว้นแต่มีเหตุผลอื่น), ระดับความละเอียด mesh อย่างน้อยสามระดับจากหยาบไปละเอียด, เกณฑ์การลู่เข้าของ displacement และ stress ระหว่างสองระดับสุดท้าย, ชุดค่าที่ยอมให้ต่อวัสดุพร้อมแหล่งที่มา, load case พร้อมที่มา, ค่าคลาดเคลื่อนของสมดุลแรงปฏิกิริยา, งบเวลาและหน่วยความจำต่อ candidate และนโยบายการลองซ้ำของแต่ละสาเหตุ `unresolved_*`

วัสดุมาจากแคตตาล็อกที่ประกาศไว้พร้อมบันทึกแหล่งข้อมูล ถ้าเป็นความหนาแน่นสังเคราะห์เพื่อ geometry ต้องกำกับไว้ในหลักฐานว่าเป็นค่าสังเคราะห์

## 8. Falsification control ที่บังคับ

แต่ละ control ต้องถูกปฏิเสธโดย evaluator และต้องบันทึกการปฏิเสธไว้

1. benchmark เชิงวิเคราะห์ที่มีคำตอบรูปปิด ต้องแก้ได้ภายในค่าคลาดเคลื่อนที่ลงทะเบียน ใช้ beam benchmark ที่มีอยู่แล้วใน `artifacts/work062` เป็นหลักยึด
2. mesh ที่ตั้งใจให้หยาบเกินไป ต้องได้ `unresolved_convergence` ไม่ใช่ผ่าน
3. อินพุตที่ตัดกันเองหรือมีหลาย solid ต้องได้ `unsupported_representation`
4. candidate ที่มวลที่ประกาศขัดกับมวลที่คำนวณจาก geometry ต้องถูกปฏิเสธ
5. การถอด load case ออกจากชุด ต้องทำให้ผลเปลี่ยน และห้ามผ่านแบบเงียบ
6. การลดค่าที่ยอมให้หลังเห็นผลแล้ว ต้องถูกปฏิเสธในฐานะการซ่อมหลังสังเกต
7. candidate เดียวกันประเมินสองครั้ง ต้องได้ hash เท่ากัน
8. นำ candidate ที่ถูกตัดด้วย `refined_disagreement` ใน Work 062 หนึ่งในยี่สิบเอ็ดแบบมาประเมินตรง ๆ ผลต้องเป็นสถานะที่ลงทะเบียนของ evaluator นี้ และบันทึกต้องระบุตรง ๆ ว่ายืนยันหรือกลับคำตัดสินเดิม

## 9. เกณฑ์การยอมรับ

ยอมรับได้ก็ต่อเมื่อ benchmark เชิงวิเคราะห์ผ่าน, control ทั้งแปดข้อทำงานตามที่ลงทะเบียน, ทุก candidate ที่ยอมรับแสดงการลู่เข้าอย่างน้อยสามระดับ, mass properties ระหว่าง CadQuery กับ FreeCAD ตรงกันภายใน residual ที่ลงทะเบียน, ทุก candidate มีสถานะหนึ่งเดียวจากหัวข้อ 6 และการรันซ้ำบน tree ที่สะอาดให้ result SHA-256 เดิมทุกประการ

## 10. ความยุติธรรมในการเปรียบเทียบ

ถ้าภายหลังนำ evaluator นี้ไปใช้เปรียบเทียบ ทุกกลุ่มรวมถึง baseline แบบ fixed topology ต้องถูกประเมินใหม่ด้วย evaluator นี้ภายใต้การลงทะเบียน mesh, solver, การลองซ้ำ และงบคำนวณเดียวกัน ห้ามนำผลจาก evaluator แบบกฎสเกลไปเทียบกับผลจาก evaluator นี้

## 11. ลำดับการ implement

1. ทำ mesh ชิ้นส่วนหนึ่งชิ้นของ Work 135 จากไฟล์ STEP และบันทึกคำสั่ง Gmsh กับตัวตนของ mesh
2. แก้สมการชิ้นนั้นด้วย CalculiX C3D10 และทำ benchmark เชิงวิเคราะห์ให้ได้ผลตรง
3. เพิ่ม refinement สามระดับและเกณฑ์การลู่เข้า
4. เพิ่ม mass properties จาก geometry และตรวจซ้ำใน FreeCAD
5. เพิ่มชุดสถานะ นโยบายการลองซ้ำ และบันทึกหลักฐาน
6. เพิ่ม control ทั้งแปดข้อพร้อมการทดสอบ
7. ประเมิน candidate ทั้ง 21 แบบที่ถูกตัดด้วย `refined_disagreement` ใน Work 062 และบันทึกผล
8. ประเมิน free-form solid ของ Work 092 หนึ่งชิ้น เพื่อแสดงว่ารูปทรงนอก template ให้คะแนนได้แล้ว

## 12. คำสั่งตรวจสอบที่เสนอ

แทน `python` ด้วย executable ที่มี dependency นั้นจริง และบันทึก exit code

```powershell
python -m unittest tests.test_geometry_general_evaluator -v
python scripts/structural/mesh_step_solid.py --step <part.step> --levels 3 --output artifacts/work138/mesh
python scripts/structural/run_geometry_general_evaluator.py --config config/development/geometry_general_evaluator_v1.json --output-root artifacts/work138/run_a
python scripts/structural/run_geometry_general_evaluator.py --config config/development/geometry_general_evaluator_v1.json --output-root artifacts/work138/run_b --replay-reference artifacts/work138/run_a/result.json
python -m unittest tests.test_repository_contract -v
python -m compileall -q src scripts tests
git diff --check
```

## 13. ความเสี่ยงและการส่งต่อ

- ต้นทุน: การแก้สมการ solid ต่อ candidate แพงกว่ากฎสเกลมาก ต้องลงทะเบียนงบคำนวณ คงตัวกรองราคาถูกไว้ก่อน และส่งเฉพาะผู้รอดเข้ามาที่ evaluator นี้ ถ้างบไม่พอกับจำนวน candidate ที่ลงทะเบียน ให้ลดจำนวน candidate ไม่ใช่ลดความละเอียด
- ความเปราะของ mesh: ผนังบาง เศษผิวแคบ และ fillet เล็กในชิ้นส่วนของ Work 135 อาจ mesh ไม่ได้ ผลนั้นคือหลักฐาน `unresolved_mesh` และเป็นข้อค้นพบด้านคุณภาพ geometry ไม่ใช่ใบอนุญาตให้ลดรูปชิ้นส่วนกลับไปเป็นกล่อง
- การขยายขอบเขต: งานนี้ประเมิน geometry เท่านั้น ไม่เปลี่ยน grammar, ไม่เปลี่ยนการค้นหา และไม่เปลี่ยน race simulator การเปิด grammar รูปทรงอิสระให้ candidate ของรถเป็น Work 139 และการป้อนผล evaluator เข้าสู่เวลาแข่งเป็น Work 140
- ความซื่อตรง: ถ้าผลการประเมินใหม่ของ 21 candidate ชี้ว่าการตัดเดิมถูกต้องแล้ว ต้องบันทึกตามนั้น ผลนั้นขัดกับสมมติฐานตั้งต้นและต้องรายงานตามที่พบ
