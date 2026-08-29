# แผนงาน 033: รายงานตรวจสอบ Material Load Path และ Failure

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_033_material-load-path-failure-validation-report-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

จัดทำแผนการทดลองที่พร้อมนำไป implement เพื่อยืนยันการส่งแรงและ torque ผ่าน
geometry/material model จริง ก่อน Formula Ultimate ใช้ structural fitness หรือ
เริ่มค้นหา geometry ของรถทั้งคัน

## ขอบเขต

- กำหนด material-law และ solver evidence boundary โดยไม่บังคับ thickness หรือ
  shape ตามความนิยมของมนุษย์
- วางแผน analytical/finite-element validation สำหรับ tension, beam bending,
  shaft torsion, buckling, loaded-interface load transfer และ vehicle failure
  coupling
- ระบุ geometry, boundary condition, ตัวแปรอิสระ/ตาม, control, mesh study,
  analytical reference, success/failure criteria และ falsification case ของ
  specimen ทุกชุด
- แยก physical failure, numerical invalidity/non-convergence และ optional
  manufacturing constraint
- กำหนดวิธีให้หลักฐาน yield, deformation, buckling, fracture และ fatigue
  ตัด/ลดความสามารถของ physical connection แล้วส่งต่อเป็น subsystem failure
  หรือ `DNF`
- บันทึก solver inventory local ที่ตรวจแล้วและความเสี่ยงสำหรับ implementation
  ในอนาคต
- ดูแลรายงานอังกฤษและไทยแยกไฟล์

## ไฟล์ที่วางแผน

- `docs/reports/MATERIAL_LOAD_PATH_FAILURE_VALIDATION_PLAN.md`
- `docs/reports/MATERIAL_LOAD_PATH_FAILURE_VALIDATION_PLAN.th.md`
- แผน/ผล Work 033 ภาษาอังกฤษและไทยที่ตรงกัน

Work item นี้เป็นงานเอกสารเท่านั้น จะไม่ implement material law, สร้าง mesh,
รัน FEA specimen, mutate candidate geometry หรือเปลี่ยน vehicle simulator

## หลักฐานเครื่องมือปัจจุบันที่ต้องเก็บ

- Bundled Python ของ FreeCAD `1.1.3` import `FreeCAD`, `Part`, `Fem` ได้
- `C:\Program Files\FreeCAD 1.1\bin\ccx.exe` ระบุตัวเองเป็น CalculiX `2.22`
  แต่คืน exit code `201` เมื่อเรียก `-v`
- `C:\Program Files\FreeCAD 1.1\bin\gmsh.exe` รายงาน `4.15.0` ใน version probe
  แต่ invocation ที่สังเกตคืน exit code `201` เช่นกัน
- Launcher ในอนาคตต้องบังคับ expected solver artifact และ parsed evidence;
  exit code หรือ console text เพียงอย่างเดียวไม่เพียงพอ

## คำถามการทดลอง

1. ผล displacement, strain, stress, reaction และ strain energy ตรง analytical
   reference ใน linear regime หรือไม่?
2. Torque ทำให้ shear-stress distribution และ twist angle ถูกต้องหรือไม่?
3. Solver ตรวจ elastic instability และเก็บ buckling mode/eigenvalue evidence
   ได้หรือไม่?
4. Load ที่ใส่บน interface ที่ประกาศไหลผ่าน candidate geometry และปิดสมดุล
   force/moment หรือไม่?
5. Mesh sensitivity, boundary-condition sensitivity, singularity และ
   non-convergence ถูกแสดงแทนการรับแบบเงียบหรือไม่?
6. Structural failure ตัด/ลด connection แบบ deterministic แล้วเปลี่ยน coupled
   vehicle outcome หรือทำให้ `DNF` ได้หรือไม่?

## การตรวจสอบ

คำสั่งที่วางแผน:

```powershell
py -3.14 -m unittest tests.test_repository_contract -v
py -3.14 -m unittest discover -s tests -q
git diff --check
git diff --cached --check
```

Result record จะเก็บ exact exit code และ output สำคัญแบบกระชับ

## เกณฑ์สำเร็จ

- Experiment family ทั้งหกมี hypothesis, variables, controls,
  equation/reference solution, pass/fail rule และ falsification attempt
- ไม่ปฏิเสธ geometry บางจาก engineering preference แต่ให้ fail จาก task
  boundary, material/instability/fatigue law หรือ numerical-resolution limit
  ที่สังเกตได้เท่านั้น
- แยก physical failure จาก solver invalidity และ unsupported physics
- แผนกำหนด reaction-force/moment closure, energy consistency, mesh convergence
  และ boundary-condition audit
- Failure coupling เก็บ event time, broken connection identity, policy ของ
  released/dissipated energy, downstream state change และ replay metadata
- ไม่เรียก analytical agreement หรือ FEA หนึ่งครั้งว่า physical validation
- bilingual, repository, whitespace, staged-scope check ผ่านและ commit สำเร็จ

## ความเสี่ยง

- Fixed minimum thickness จะฝัง human design preference แทนการทดสอบ physics
- Mesh ที่ resolve thin geometry ไม่ได้อาจถูกเข้าใจผิดเป็น physical failure
- Linear elasticity ทำนาย plastic collapse, fracture หรือ fatigue ไม่ได้
- Idealized clamp และ point load สร้าง artificial stiffness/stress singularity
- Eigenvalue buckling อย่างเดียวไม่พิสูจน์ post-buckling capacity
- ต้อง acceptance-test process/artifact behavior ของ CalculiX/FreeCAD/Gmsh
  บน version ที่ติดตั้งก่อน campaign
- Structural failure event อาจละเมิด force/energy conservation หากลบ connection
  โดยไม่มี release/dissipation model ชัดเจน

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่มี FEA ที่เสร็จ, structural implementation, material calibration,
  physical test, safety certification หรือ autonomous design search
- ไม่ใช้กฎ conventional layout, thickness, web หรือ feature size แบบตามอำเภอใจ
  แทน physics
- ไม่อ้างว่า isotropic material law หนึ่งชุดครอบคลุม composite, anisotropy,
  joint, adhesive, weld, temperature dependence หรือ rate effect
- ไม่มี full crash, fracture mechanics, composite failure หรือ manufacturing
  model ใน implementation phase แรก
- ไม่ push, publish, upload ภายนอก หรือ rewrite history
