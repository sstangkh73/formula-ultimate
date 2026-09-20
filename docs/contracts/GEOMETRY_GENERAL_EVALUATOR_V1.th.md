# Structural Evaluator ที่รับ Geometry ใดก็ได้ v1

แหล่งภาษาอังกฤษ: `GEOMETRY_GENERAL_EVALUATOR_V1.md`

Protocol version: `geometry_general_evaluator_v1` implement โดย Work 138

## 1. ขอบเขตของสัญญานี้

solid เดียวที่ถูกต้องแบบใดก็ได้ให้คะแนนได้ evaluator อ่าน geometry ไม่ใช่ตัวแปรออกแบบ

```text
STEP solid (หรือกล่อง benchmark ที่ลงทะเบียนไว้)
  -> Gmsh สร้าง tetrahedral mesh อันดับสองอย่างน้อยสามระดับความละเอียด
  -> คำนวณ volume, mass, center of mass และ point-mass inertia จาก geometry
  -> CalculiX C3D10 แก้สมการ linear static ต่อ load case ที่ลงทะเบียน
  -> displacement, von Mises, สมดุลแรงปฏิกิริยา, utilization
  -> สถานะที่ลงทะเบียนหนึ่งค่าเท่านั้น พร้อม hash ของหลักฐาน
```

ห้าม candidate ประกาศความแข็ง ความแข็งแรง หรือ margin ของตัวเอง มวลที่ประกาศจะถูกตรวจกับ mesh ไม่ใช่เชื่อตามที่แจ้ง

## 2. ชุดสถานะ

| สถานะ | ความหมาย |
| --- | --- |
| `passed` | ลู่เข้า สมดุล และอยู่ในค่าที่ยอมให้ |
| `failed_physics` | แก้สมการได้ แต่เกินค่าที่ยอมให้ หรือมวลที่ประกาศขัดกับ mesh |
| `unresolved_mesh` | สร้าง mesh ไม่ได้แม้ที่ระดับหยาบสุด หรือ mesh เกินงบจำนวน node |
| `unresolved_solver` | solver ทำงานไม่จบ หรือแรงปฏิกิริยาไม่สมดุลกับแรงลัพธ์ที่ใส่ |
| `unresolved_convergence` | มีระดับที่แก้สำเร็จน้อยกว่าสามระดับ หรือสองระดับสุดท้ายเกินขีดจำกัดการเปลี่ยนแปลง |
| `unsupported_representation` | ไม่ใช่ tetrahedral solid เดียวที่ถูกต้อง หรือการเลือกขอบเขตที่ประกาศใช้ไม่ได้ |

`unresolved_*` เป็นข้อความเกี่ยวกับเครื่องมือ ไม่ใช่เกี่ยวกับตัวออกแบบ การรันต้องรายงานจำนวนและสาเหตุของทุก candidate ที่ unresolved เพราะการกระจายนั้นคือหลักฐานว่าควรเพิ่ม capability ใดต่อ

## 3. การลงทะเบียนเชิงตัวเลข

freeze ไว้ใน `config/development/geometry_general_evaluator_v1.json` ก่อนรัน admitted: ชนิด element `C3D10`, ระดับ mesh อย่างน้อยสามระดับที่ละเอียดขึ้นอย่างเคร่งครัด แสดงเป็น `Mesh.MeshSizeFactor` ของ Gmsh, ขีดจำกัดการลู่เข้าของ displacement สูงสุดและ p90 von Mises ระหว่างสองระดับสุดท้ายที่แก้สำเร็จ, ค่าที่ยอมให้และแหล่งข้อมูลของแต่ละวัสดุ, load case พร้อมการเลือกผิวและแรงลัพธ์, residual ของสมดุลแรงปฏิกิริยาและมวลที่ประกาศ รวมถึงงบจำนวน node เวลา และการลองซ้ำ

## 4. ข้อจำกัดของ mesh และ solver

- **element อันดับสองแบบขอบตรง:** `Mesh.SecondOrderLinear = 1` การดัด node กึ่งกลางให้ไปอยู่บนผิวโค้งทำให้เกิด element กลับด้านที่ CalculiX ปฏิเสธด้วย nonpositive jacobian ต้นทุนคือผิวโค้งกลายเป็นเหลี่ยม ซึ่งเป็นการประมาณทางเรขาคณิตที่ลงทะเบียนไว้
- **ความกว้างของ field:** CalculiX อ่าน free field ลงบัฟเฟอร์ 20 ตัวอักษร ค่าวิทยาศาสตร์ยาว 21 ตัวอักษรจะถูกตัดอย่างเงียบ ๆ วัดไว้ใน Work 138 ว่า `-1.00000000000000e+03` ถูกอ่านเป็น `-1.0` และคืน exit code 0 พร้อม displacement ที่เล็กกว่าจริง 1000 เท่า ส่วน 22 ตัวอักษรขึ้นไปทำให้การรันหยุด ทุก field ตัวเลขจึงเขียนผ่าน `calculix_number` และ deck ถูกตรวจซ้ำทีละ field ก่อนส่งให้ solver
- **โหลดผิวแบบ consistent:** แรงลัพธ์กระจายบนผิว TRI6 ด้วยน้ำหนัก consistent ที่ถูกต้อง คือ shape function ที่มุมอินทิเกรตเป็นศูนย์ และแต่ละ node กึ่งกลางได้ `A/3` โหลดที่กระจายแล้วต้องรวมกลับเป็นแรงลัพธ์ที่ประกาศภายใน `1e-12`

## 5. Control ที่บังคับ

ทุกการรัน admitted ต้องทดสอบ control แปดข้อและต้องปฏิเสธทั้งหมด ได้แก่ `analytical_benchmark`, `under_refined_mesh`, `unsupported_representation`, `declared_mass_contradiction`, `removed_load_case`, `post_observation_allowable`, `deterministic_restatement` และ `work062_refined_disagreement_reevaluated` ถ้ามี control ใดรอด สถานะของการรันจะเป็น `failed_controls`

## 6. การยอมรับและขอบเขตข้ออ้าง

การรันจะถูกยอมรับเป็น `passed_geometry_general_structural_evaluation` ก็ต่อเมื่อ control ทั้งแปดถูกปฏิเสธ ทุก candidate มีสถานะที่ลงทะเบียนหนึ่งค่าพอดี และการ replay บน tree ที่สะอาดให้ result SHA-256 ตรงกันทุกประการ

สถานะนั้นหมายถึงการประเมินเชิงโครงสร้างของ solid ที่ประกาศภายใต้ load case ที่ประกาศเท่านั้น ไม่ใช่ promotion ไม่ใช่ความเป็นไปได้ในการผลิต ไม่ใช่เวลาแข่ง และไม่ใช่ physical validation วัสดุเป็นค่าสังเคราะห์สำหรับ geometry เท่านั้น เว้นแต่ evidence class จะระบุเป็นอย่างอื่น

## 7. กฎการเปรียบเทียบ

ห้ามนำผลจาก evaluator นี้ไปเทียบกับผลจาก evaluator แบบกฎสเกลของ campaign ใน `whole_vehicle_search` การเปรียบเทียบใด ๆ ต้องประเมินทุกกลุ่มใหม่ที่นี่ รวมถึง baseline แบบ fixed topology ภายใต้การลงทะเบียน mesh, solver, การลองซ้ำ และงบคำนวณเดียวกัน
