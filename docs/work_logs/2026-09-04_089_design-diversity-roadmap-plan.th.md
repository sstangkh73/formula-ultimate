# แผน Work 089: Roadmap ความหลากหลายในการออกแบบ

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_089_design-diversity-roadmap-plan.md`

## สถานะ

สถานะ: Completed

## วัตถุประสงค์

กำหนด roadmap ที่พร้อมนำไป implement เพื่อขยาย Formula Ultimate จากการปรับ scale ของ primitive ที่ topology ตายตัวและ candidate builder ที่เขียนด้วยมือ ไปเป็นการค้นหาการออกแบบแบบ topology-mutating และ free-form ที่ geometry เป็นสาเหตุของผลฟิสิกส์ และสามารถเสนอชิ้นส่วนทำงานที่ไม่คุ้นเคยจริงได้

Roadmap ต้องแยกผิวโค้งที่ดูแปลกออกจากอิสระในการออกแบบจริง และต้องขยาย representation, mutation, semantic interface, geometry inspection, meshing, physical evaluation และ quality-diversity search ไปพร้อมกัน โดยยังรักษา deterministic replay, หน่วย SI, evidence gate, baseline ที่ยุติธรรม และข้อห้ามเรื่อง hidden result-conditioned geometry repair

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม `docs/reports/GEOMETRIC_DESIGN_DIVERSITY_ROADMAP_V1.md` และไฟล์ภาษาไทยคู่กัน
- บันทึกคอขวดด้าน expressivity ปัจจุบันพร้อมหลักฐาน exact จาก repository
- กำหนด future work ที่เรียงลำดับแล้ว พร้อม dependency, deliverable, test, metric, gate, risk, stop condition และสิ่งที่ไม่ทำ
- เพิ่มแผน/ผลนี้และไฟล์ภาษาไทยคู่กัน

## การตรวจสอบและเกณฑ์สำเร็จ

- Roadmap ต้องครอบคลุมการวัด search space, free-form profile และ solid, topology genome, typed mutation, deterministic constructive repair, semantic geometry witness, generalized meshing/physics, quality-diversity search, การทดลอง subsystem แยก, integrated candidate และ higher-fidelity promotion
- Future work ทุกงานต้องมีเกณฑ์สำเร็จที่หักล้างได้และบอกว่างานนั้นไม่พิสูจน์อะไร
- แผนต้องไม่บังคับรูปแบบรถตามประเพณีและไม่ถือความแปลกทางสายตาเป็น functional discovery
- โครงสร้าง EN/TH, identifier, หมายเลข work, สมการ, หน่วย, gate และข้อจำกัดต้องตรงกัน
- Repository-contract test และการตรวจ Markdown companion ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

ความเสี่ยงได้แก่การเพิ่ม curved operator โดยไม่เชื่อมกับ search, การให้รางวัลกับความแปลกทางสายตา, การปล่อยให้ candidate ซับซ้อนใช้ compute อย่างไม่ยุติธรรม, การซ่อน invalid geometry ด้วย repair และการสร้าง grammar ที่ physics ประเมินไม่ได้ งานวางแผนนี้ไม่ implement CAD operator, ไม่รัน evolution campaign, ไม่สร้าง candidate ใหม่ และไม่อ้างว่าบรรลุ open-ended discovery แล้ว
