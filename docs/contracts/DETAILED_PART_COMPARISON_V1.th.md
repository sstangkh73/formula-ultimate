# การเปรียบเทียบชิ้นส่วนละเอียด V1

แหล่งภาษาอังกฤษ: `DETAILED_PART_COMPARISON_V1.md`

สถานะ: Work 125 นำไปใช้เป็นด่านเปรียบเทียบแบบจำกัดที่ลงทะเบียนล่วงหน้า

## ขอบเขตหลักฐาน

แขน fixed-family, existing-grammar, open-material และ random-control ได้รับโจทย์ ขอบเขตวัสดุ/กระบวนการสังเคราะห์ จำนวนพารามิเตอร์ จำนวนการประเมินเพื่อ optimization และเงื่อนไข holdout แบบจับคู่เหมือนกัน ตัวระบุ training กับ holdout ต้องไม่ทับกัน ทุกแขนต้องถูก optimize ก่อนเปรียบเทียบ baseline ที่ไม่ tune ไม่ถือว่ายอมรับได้

estimand ที่ลงทะเบียนคือ open-material ลบด้วย control แบบไม่เปิดที่ optimize แล้วและดีที่สุด ณ fine fidelity การอ้างประโยชน์ต้องผ่าน constraint ครบและขอบล่างของ paired interval ไม่น้อยกว่า meaningful effect ที่ลงทะเบียน การละเว้น hardware ทำให้การประเมิน invalid geometry ที่ถูกปฏิเสธหรือยังไม่สรุปยังต้องผ่าน audit ที่ไม่ขึ้นกับ proxy score และ coupling ที่อ้างว่า active ต้องสูญเสียผลเมื่อทำ targeted ablation ขณะที่ inactive appendage ต้องไม่เปลี่ยนผล

fixture เชิงกำหนดเป็นข้อมูลสังเคราะห์ อันดับบวกใน coarse ที่กลับเป็นลบใน fine เป็นหลักฐานโต้แย้งและปิดกั้นการอ้างประโยชน์ exact replay ต้องได้ result SHA-256 เดิม สัญญานี้ไม่ยืนยัน external novelty, measured material survival, whole-vehicle benefit, manufacturing feasibility หรือ physical validation
