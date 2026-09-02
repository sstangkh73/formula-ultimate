# เคอร์เนลชุดประกอบเชิงกลและข้อต่อ V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `MECHANICAL_ASSEMBLY_JOINT_KERNEL_V1.md`

## วัตถุประสงค์และขอบเขตหลักฐาน

Work 080 แปลงชิ้นส่วนที่ระบุตำแหน่งและตัวตนเรขาคณิตไว้อย่างชัดเจนให้เป็นระบบ constraint ของชุดประกอบเชิงกลแบบ deterministic ระบบตรวจ frame ของ datum/interface คำนวณ constraint rank และ rigid-body degrees of freedom (DOFs) ที่เกิดขึ้นจริง ตรวจพิกัดจำกัดของข้อต่อและ clearance ที่ประกาศ และปฏิเสธการชนของ motion envelope แบบต่อเนื่องเชิงอนุรักษนิยม ชุดทดสอบที่รับอ้างอิง SHA-256 ของ canonical STEP ที่ Work 078 สร้างจริง

การผ่าน V1 เป็นหลักฐานเฉพาะว่า declaration สอดคล้องกัน, DOF ถูกคำนวณ และ proxy envelope เชิงอนุรักษนิยมที่ประกาศไม่ชนกัน ไม่ใช่ physical validation, ใบรับรองการชนของ B-rep แบบ exact, multibody dynamics, อายุ bearing, ความแข็งแรงข้อต่อ, การสึกหรอ, friction, fatigue หรือการอนุมัติความปลอดภัย

## คณิตศาสตร์ของข้อต่อ

ชิ้นส่วนที่ไม่ใช่ ground แต่ละชิ้นมี generalized coordinate 6 ค่า ข้อต่อเพิ่มแถว constraint อิสระในแกน world-frame ที่ประกาศดังนี้:

| ข้อต่อ | แถว constraint | DOF สัมพัทธ์ที่เกิดจริง |
|---|---:|---:|
| fixed | 6 | 0 |
| revolute | 5 | หมุน 1 DOF รอบแกนข้อต่อ |
| prismatic | 5 | เลื่อน 1 DOF ตามแกนข้อต่อ |
| spherical | 3 | หมุน 3 DOFs รอบศูนย์กลางข้อต่อ |

เคอร์เนลทำ Gaussian elimination แบบ deterministic ด้วย absolute rank tolerance ที่ประกาศ โดย `realized_dof_count = 6 * component_count - calculated_rank`; ค่า rank และ DOF ที่คาดหมายเป็น assertion ที่ตรวจหลังการคำนวณ ไม่เคยถูกนำมาแทนผลคำนวณ แถว constraint ที่ซ้ำจะถูกปฏิเสธว่า overconstrained และชิ้นส่วนที่ไม่มีข้อต่อจะถูกปฏิเสธว่า underconstrained

## Frame, mate และ interface

frame ของชิ้นส่วนและ interface ทุกตัวมีจุดกำเนิดหน่วย SI พร้อมแกนตั้งฉากหนึ่งหน่วยแบบมือขวา ค่าไม่รู้จัก, non-finite, แกนไม่เป็นหนึ่งหน่วย, ไม่ตั้งฉาก หรือแบบมือซ้ายจะ fail closed จุดกำเนิด interface และแกนข้อต่อต้องตรงกันอยู่แล้วภายในค่าคลาดเคลื่อนที่เข้มที่สุดจาก mate/interface เคอร์เนลไม่ snap, align, heal หรือซ่อม declaration

ชุด compatibility ของ interface ใน V1 มีขอบเขต: fixed รับ fixed mount, bolted/welded interface และ shaft coupling; revolute รับ revolute, bearing-seat และ shaft-coupling interface; prismatic และ spherical ต้องใช้อินเทอร์เฟซชนิดตรงกัน การอ้างอิงที่หาย, ซ้ำ, ใช้ชื่อสงวน, ต่อเข้าตัวเอง หรือไม่เข้ากันจะ fail closed

## Clearance และตัวควบคุมการชนแบบต่อเนื่อง

ค่า minimum, home และ maximum ของข้อต่อต้องเรียงลำดับและ finite; fixed joint ต้องเป็นศูนย์ทั้งหมด axial/radial clearance ต้องไม่เกินค่าสูงสุดที่ประกาศ preload และ translational/rotational stiffness เป็นค่าที่บันทึกตรวจสอบได้ แต่ V1 ไม่ได้แก้ contact stress หรือ deformation จากค่าเหล่านี้

collision proxy เป็นทรงกลมในกรอบเฉพาะชิ้นส่วน ทรงกลมของ prismatic กลายเป็น line-segment sweep ที่ exact สำหรับทรงกลมนั้นตลอดระยะเคลื่อนที่ ทรงกลมของ revolute หรือ spherical กลายเป็นทรงกลมเชิงอนุรักษนิยมรอบศูนย์กลางข้อต่อซึ่งครอบคลุมทุกมุมหมุน ส่วน fixed อยู่กับที่ ระยะระหว่าง finite segments แบบจับคู่ให้ minimum gap และตรวจการชนตลอด proxy envelope แบบต่อเนื่อง ไม่ใช่เฉพาะจุด sample วิธีนี้อาจให้ผลบวกเกินจริงเชิงอนุรักษนิยมและไม่รับรอง clearance ของ B-rep แบบ exact

## ชุดอ้างอิงและตัวควบคุม

`config/assembly/mechanical_assembly_joint_kernel_v1.json` มีชิ้นส่วนต่อกับ ground สี่ชิ้น ครอบคลุม fixed, revolute, prismatic และ spherical ระบบที่คำนวณได้มีแถวอิสระ 19 แถวและ DOF จริง 5 ค่า ตัวควบคุมล้มการยอมรับด้วยแกน/จุดกำเนิดเหลื่อม, constraint ซ้ำ, DOF ที่ประกาศหรือคาดหมายผิด, clearance เกิน, limit ไม่ถูกต้อง, ชนระหว่างช่วงเคลื่อนที่ต่อเนื่อง, interface หาย/ซ้ำ/ไม่เข้ากัน, frame non-finite และ frame มือซ้าย การสลับลำดับ key ใน mapping ต้องไม่เปลี่ยน declaration/result identity แต่การเปลี่ยน geometry hash ต้องเปลี่ยนทั้งคู่

รันหลักฐานที่ยอมรับด้วย:

```powershell
python scripts\assembly\run_joint_kernel_acceptance.py `
  --output artifacts\work080\acceptance.json
python -m unittest tests.test_joint_kernel -v
```

## ข้อจำกัด V1 และ dependency ถัดไป

ชุดอ้างอิงใช้การต่อกับ ground หนึ่งจุดต่อหนึ่งชิ้นส่วน สูตร rank รองรับ constraint ระหว่างชิ้นส่วน แต่การวาง swept envelope ของ V1 ยังไม่ได้ตรวจสอบโซ่ kinematic ที่ parent เคลื่อนที่ได้ จึงห้ามส่งต่อ claim เรื่องการชนจากชุดอ้างอิงไปยังชุดประกอบแบบนั้น collision sphere เป็น proxy ที่ประกาศ ไม่ใช่ขอบเขต B-rep ที่วัดอย่างอิสระ Work 081 ต้อง re-import ไบต์ STEP ชุดเดียวกันด้วยเครื่องมืออิสระ วัดเรขาคณิตและ mass properties และค้น interface จาก geometric signature แทนเลข face แบบถาวร
