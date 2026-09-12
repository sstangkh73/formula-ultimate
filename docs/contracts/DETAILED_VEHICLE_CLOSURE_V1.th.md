# การปิดรายละเอียดยานพาหนะ V1

แหล่งภาษาอังกฤษ: `DETAILED_VEHICLE_CLOSURE_V1.md`

สถานะ: Work 126 นำไปใช้เป็นด่าน closure ของ G3 registry เชิงกำหนด

## ขอบเขตหลักฐาน

ทุก external function ที่ลงทะเบียนมี component owner ชัดเจนอย่างน้อยหนึ่งรายการ และต้องติดตั้งทุก role ที่จำเป็น ได้แก่ structure, ground-port, actuator, energy-store, controller, cooler, fastener, support, seal, signal, thermal-link และ load-link ตัวระบุ material region ต้องไม่ซ้ำ mass, center, diagonal inertia และ occupied volume ถูกคำนวณใหม่จาก component record หน่วย SI; ledger ที่ประกาศต้องตรงภายใน tolerance ที่ตรึงไว้

เส้นทาง energy, signal, heat และ load ต้องเชื่อม source กับ sink ที่ลงทะเบียน component bounds ต้องอยู่ใน subsystem envelope รุ่นสุดท้ายโดยไม่มี interference แบบ static หรือ sampled swept-motion การเอา hardware ที่จำเป็นออก, ทำ region ownership ซ้ำ, สร้าง void นอก envelope, interference, open path หรือ stale envelope ต้อง fail closed

G3 registry หมายถึง component bounds, placement, ownership และ interface graph เชิงกำหนดที่ชัดเจน ไม่ใช่ native CAD ชิ้นส่วนที่ซื้อถูกระบุที่มา ไม่อ้างเป็น generated discovery exact replay ต้องได้ result SHA-256 เดิม ช่องว่างด้าน material, surface, tolerance, manufacturing และ physical test ที่จำเป็นยังต้องสังเกตได้และบังคับสถานะ `detailed_exploratory`; สัญญานี้อนุญาต vehicle promotion หรือ physical validation ไม่ได้
