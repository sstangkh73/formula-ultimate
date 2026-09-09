# Contract เนื้อวัสดุและช่องว่างเชิงพื้นที่ V1

ต้นฉบับภาษาอังกฤษ: `SPATIAL_MATERIAL_VOID_V1.md`

Status: พัฒนาโดย Work 108 สำหรับขอบเขตหลักฐาน CAD แบบจำกัด

## จุดประสงค์และขอบเขตคำกล่าวอ้าง

Contract นี้ทำให้ geometry ที่มีเนื้อเป็นข้อมูลต้นทางของปริมาตร และทำให้การเป็นเจ้าของวัสดุเป็นข้อมูลต้นทางของมวล จุดศูนย์กลางมวล และความเฉื่อย เพื่อไม่ให้ revision geometry, cavity, การกำหนดวัสดุ หรือ placement เปลี่ยน แต่หลักฐานปลายน้ำยังเก็บ mass properties เก่าแบบเงียบ

การผ่าน contract นี้คือ software execution และ numerical/CAD verification สำหรับกรณี Work 092 ที่ admitted ไม่ใช่การตรวจโครงสร้าง thermal, flow, manufacturing, durability, รถทั้งคัน, scientific benefit หรือ physical validation

## Spatial representation

พิกัดทั้งหมดเป็นเมตร ความหนาแน่นเป็น `kg/m3` มวลเป็น `kg` และความเฉื่อยเป็น `kg m2` แต่ละกรณีระบุ candidate Work 092 หนึ่งรายการและ SHA-256 ของ canonical STEP ที่ตรงกัน ชุด admitted มี single body แบบโค้ง, body กลวงจาก subtraction และรูปทรงสี่ body

source solid ที่มีเนื้อทุกก้อนมีเจ้าของ material region เพียงหนึ่งเดียว ห้าม source body ไม่มีเจ้าของหรือมีหลายเจ้าของ source solid แบบหลาย body ถูกเรียง canonical ตามพิกัดจุดศูนย์กลางและปริมาตรก่อนใช้ body index ที่ลงทะเบียนไว้ การตัดกันรายคู่เกิน `1e-12 m3` ถูกปฏิเสธ ไม่อนุญาต fusion หรือกลบ overlap

void จะ admitted เฉพาะเมื่อ `outer_feature_id`, `cavity_feature_id` และ `occupied_feature_id` ที่ลงทะเบียนตรงกับ ancestry `boolean_subtract` จริงของ Work 092 ปริมาตรเนื้อต้องปิดสมการ `outer - cavity` ภายใน relative error `1e-8` ป้าย void ที่ไม่มี geometry นี้ไม่ใช่หลักฐาน

## วัสดุและ placement

Work 108 ใช้ความหนาแน่น synthetic คงที่เพื่อทดสอบการทำบัญชีเท่านั้น ชื่อวัสดุไม่ได้ยืนยันคุณสมบัติวิศวกรรมที่วัดจริง ทุก density เปิดเผย provenance และ validity statement

Rigid placement คือแกนหมุนหน่วย มุมหน่วยเรเดียน และการเลื่อนหน่วยเมตร runner ใช้ transform กับ B-rep ของ region จริงก่อนวัด ปริมาตรและ centroidal shape invariants ต้องสอดคล้อง ส่วน centre ในกรอบโลกและทิศของ inertia เปลี่ยนได้ อัตลักษณ์ source STEP, การเป็นเจ้าของวัสดุที่เรียงแล้ว, void declaration และ placement ถูก hash รวมเป็น dependent-evidence identity

## การคำนวณ mass properties

CadQuery และ FreeCAD วัด region STEP ที่ placement แล้วจริงอย่างละชุด volume moments จาก CAD ถูกแปลงจาก `mm3`, `mm` และ `mm5` เป็น `m3`, `m` และ `m5` มวล region คือ `density * volume`; centroidal inertia ของ region คือ `density * geometric volume moment` จุดศูนย์กลางและ inertia รวมใช้การถ่วงด้วยมวลและ parallel-axis theorem ต้องเป็นค่า finite, symmetric และมีเส้นทแยงมุมเป็นบวก

ขอบเขต cross-tool ที่ลงทะเบียนคือ:

- volume relative error: `5e-7`
- mass relative error: `5e-7`
- centre absolute error: `1e-7 m`
- inertia relative error: `2e-6`

CadQuery และ FreeCAD ใช้เทคโนโลยี geometry ตระกูล OCCT ร่วมกัน ดังนั้นการเห็นตรงกันเป็นหลักฐานความสอดคล้องของ exact artifact ที่แข็งแรง แต่ไม่ใช่ physical validation อิสระ

## Mutation, replay และสถานะล้มเหลว

admitted run เติม cavity ที่ลงทะเบียนด้วย outer B-rep จริง และบังคับให้ทั้ง STEP identity และมวลเปลี่ยน Material mutation และ placement mutation ต้องเปลี่ยน dependent-evidence identity ด้วย Duplicate/incomplete ownership, วัสดุที่ไม่รู้จัก, พิกัด non-finite, แกนไม่เป็นหน่วย, hash ของ declaration/STEP ต้นทางเก่า, CAD ไม่ถูกต้อง, overlap ที่ไม่ประกาศ, cavity ปิดสมการไม่ได้, เกิน tolerance และ replay ไม่ exact ล้มเหลวแบบปิดทั้งหมด

`result.json` เก็บ input identities, สมบัติราย region และทั้งระบบ, comparison residuals, controls, execution identities, supporting/contradicting evidence, alternative explanations, missing evidence และ confidence การรันสะอาดครั้งที่สองต้องตรงกับ canonical result identity แบบ exact

## การส่งต่อ

Works 109 และ 110 ใช้ contract นี้เพื่อรับรองว่า geometry ที่สร้างหรือ mesh มีการเป็นเจ้าของวัสดุและ void แบบ causal ได้ Work 112 ผูก physical interfaces ได้เฉพาะกับ spatial revision ที่เปลี่ยนย้อนหลังไม่ได้ การขยายไปยังวัสดุที่แปรเชิงพื้นที่ภายใน body เชื่อมต่อเดียว ต้องมี declaration, tests และวิธีวัดอิสระใหม่แบบมีขอบเขต
