# แผนงาน 040: Roadmap สิบงานสู่การวิจัยรถทั้งคัน

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_040_whole-vehicle-10-work-roadmap-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

สร้าง roadmap สิบงานแบบละเอียด เรียง dependency และมีสองภาษา เพื่อนำ Formula Ultimate จาก component fixture และ coupled Level 0 reference ที่ตรวจแล้ว ไปสู่ bounded whole-vehicle research pilot

## ขอบเขต

- กำหนด execution Work 041-050 พร้อมวัตถุประสงค์, prerequisite, experiment variable, control, metric, gate, deliverable, failure criterion, risk, non-goal และ claim boundary
- รักษาขอบเขตหลักฐานปัจจุบัน: Work 039 reject near-critical mesh convergence และ imperfection-shape robustness ดังนั้น roadmap ต้องแก้ผลนี้ก่อน post-buckling
- รักษา vehicle representation ให้ topology-neutral และไม่บังคับ conventional vehicle layout
- แยกความพร้อมเริ่ม bounded whole-vehicle search ออกจาก physical validation หรือ discovery

## ไฟล์ที่วางแผน

- `docs/reports/WHOLE_VEHICLE_RESEARCH_10_WORK_ROADMAP.md`
- `docs/reports/WHOLE_VEHICLE_RESEARCH_10_WORK_ROADMAP.th.md`
- matching Work 040 bilingual plan/result log

## Validation และเกณฑ์สำเร็จ

- เอกสารสองภาษาต้องอ้างถึงกันและคง identifier, equation, unit, numeric gate, dependency และ limitation ให้ตรงกัน
- Roadmap ต้องมี execution work item exactly สิบรายการ หมายเลข 041-050
- ทุก work item ต้องมี falsifiable completion gate และ explicit non-claim
- Repository Markdown-pairing/plan-result contract test, diff check และ validated commit ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

สิบงานนี้เป็น minimum logical route ไม่ใช่คำสัญญาด้านปฏิทิน หาก hypothesis ถูก reject, material data ขาด, solver มีข้อจำกัด หรือ validation ไม่ผ่าน อาจต้องเพิ่ม remedial work งานนี้ไม่ implement physics, ไม่สร้างรถ, ไม่รัน search campaign, ไม่อ้าง safety และไม่ authorize publication/push
