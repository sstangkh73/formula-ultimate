# Contact ของจุดเชื่อมแบบละเอียด V1

ต้นฉบับภาษาอังกฤษ: `DETAILED_CONNECTION_CONTACT_V1.md`

Status: พัฒนาโดย Work 113 สำหรับหลักฐาน joint ระดับ Level-0 แบบมีขอบเขต

## ขอบเขตและ task ที่ตรึง

Contract นี้ตรึง commits/contracts ของ Work 111 vector field และ Work 112 physical interface Threaded helix reference และทางเลือก six-ramp ที่ topology ต่างกันใช้ envelope `0.03 m` diameter คูณ `0.04 m`, อุณหภูมิ `293.15 K`, synthetic isotropic material, axial tension `800 N`, shear `500 N`, off-axis moment `1 N m`, preload `2000-6000 N`, friction `0.2-0.35` และ clearance `0-5e-5 m` เดียวกัน Engaged state ไม่ยอมให้เกิด relative motion

ทั้งสอง strategies สร้าง male/female STEP solids แยกกันและ valid Reference มี rounded swept helix รอบ root cylinder ที่ประกาศชัด ไม่ใช่ standardized V-thread ทางเลือกมี segmented radial engagement ramps หกจุด Root, contact, engagement และ sleeve radii รวมถึงความยาวต้องเรียงถูกและอยู่ใน common envelope Male/female interference ต้องไม่เกิน `1e-12 m3`

## Contact formulation และ gates

Detailed model แบ่ง engagement surface ที่ประกาศเป็น `12`, `24` และ `48` patches แก้ nonnegative normal reactions ให้สมดุล compression ที่เหลือและ off-axis moment Patch contact เป็น unilateral การส่งแรง tangential จำกัดด้วย Coulomb capacity `mu * sum(normal reaction)`; เมื่อเกินให้รายงาน slip พร้อม post-slip compliance ชัดเจน Joint ที่ถอด/ตัด, contact เปิดหมด, engagement ผิด และ input นอกช่วงล้มเหลวแบบปิด ไม่มี hidden stabilizing support

Acceptance ใช้ patch-average maximum pressure แทน singular point stress Last-two relative changes ของ normal stiffness, shear displacement และ maximum patch pressure ต้องไม่เกิน `0.15`; force และ moment residuals ต้องไม่เกิน `1e-9` Reduced stiffness ใช้ได้เฉพาะ full-engagement stick cases ที่ลงทะเบียนและ displacement error ต้องไม่เกิน `0.05`

Clearance, engagement, preload/friction และ load reversal ต้องเปลี่ยน response อย่างเป็นเหตุเป็นผล ทางเลือกที่ล้มเหลวยังคงเป็น negative evidence Exact replay ต้องได้ result SHA-256 เดิม งานนี้เป็น deterministic initialization และ reduced-model evidence ไม่ใช่ general nonlinear contact solve, thread strength, loosening/fatigue prediction, manufacturing release, safety certification หรือ physical validation
