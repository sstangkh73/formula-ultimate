# การป้อนกลับระหว่างสถาปัตยกรรมกับชิ้นส่วน V1

แหล่งภาษาอังกฤษ: `ARCHITECTURE_PART_FEEDBACK_V1.md`

สถานะ: Work 117 นำไปใช้เป็นหลักฐานการสร้างใหม่แบบมีขอบเขตที่ Level-0

## ขอบเขตหลักฐานและอัตลักษณ์

งานการเชื่อมต่อภายนอก อัตลักษณ์กติกาการแข่งขัน หน่วย SI, commit/contract ของ dependency และอัตลักษณ์ผลลัพธ์ Work 112, Work 114 และ Work 115 ที่ระบุแน่นอนเป็น input ที่แก้ไขไม่ได้ หลักฐานระดับ assembly ส่งค่า contact load สูงสุด displacement สูงสุด และ heat input ที่ลงทะเบียนแล้วไปยังงานภายในที่มี version โดยไม่เขียนทับงานภายนอก

การแก้ไขงานภายในแต่ละครั้งเก็บ SHA-256 ของ parent เมื่อเปลี่ยนงานภายใน ต้องทำให้หลักฐานของงานเดิมใช้ไม่ได้ก่อนสร้าง candidate ใหม่ หลักฐาน candidate เก็บอัตลักษณ์ของงาน geometry, seed, mass และ margin จากโมเดล structural/thermal แบบลดรูป `measured_material` และ `ground_interaction` ยังไม่ถูกแก้ ดังนั้น candidate ทุกตัวต้องรายงาน `complete_feasibility: false`

## control ที่เป็นธรรมและเกณฑ์รับ

โหมด feedback และ frozen-task ใช้งานเริ่มต้น coefficient, seed, จำนวน iteration และหนึ่ง evaluation ต่อ iteration เหมือนกัน การผ่านต้องมีอัตลักษณ์งานและ geometry เปลี่ยนหลัง feedback เชิงเหตุ มีการ invalidate งานเก่าทุกครั้ง จำนวน evaluation เท่ากัน อัตลักษณ์งานภายนอกไม่เปลี่ยน มวลของ multifunctional region ที่ซ้อนกันไม่ถูกนับซ้ำ และ coefficient ที่ขาดถูกปฏิเสธ

มีการวัดการเปลี่ยนแปลง mass หรือ margin แต่ไม่บังคับว่าต้องดีขึ้น เพราะการทดลองนี้ทดสอบว่า feedback ติดตามย้อนกลับและเป็นเชิงเหตุ ไม่ได้พิสูจน์ว่า generator แบบมีขอบเขตเป็น optimizer ตัวประเมิน structural และ thermal เป็นโมเดลลดรูป Contract นี้ไม่ยืนยัน unrestricted topology search, complete feasibility, material ที่วัดจริง, ground interaction, ความพร้อมระดับยานพาหนะ หรือ physical validation
