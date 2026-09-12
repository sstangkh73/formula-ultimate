# แผน Work 134: การวางแผน Native Detailed Vehicle Realization

แหล่งภาษาอังกฤษ: `2026-09-13_134_native-detailed-vehicle-realization-planning-plan.md`

วันที่: 2026-09-13 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

เขียนแผน Work 135 สองภาษาที่พร้อมดำเนินการ เพื่อแก้ scope regression ของ Work 126 โดยบังคับให้มี contiguous native detailed vehicle assembly, per-part solids จริง และ face-level interfaces พร้อมอัปเดตดัชนีแผนละเอียดสองภาษาโดยไม่เขียนประวัติ Work 126 ใหม่

งานนี้เป็นการวางแผนเท่านั้น ไม่ได้สร้าง CAD, ผ่าน geometry gate, อนุญาต fabrication หรืออ้างสมรรถนะรถ

## ไฟล์ที่วางแผน

- `docs/plans/detailed_part_to_vehicle_v1/work135-native_detailed_vehicle_realization.md` และคู่ภาษาไทย
- `docs/plans/detailed_part_to_vehicle_v1/README.md` และคู่ภาษาไทย
- แผน Work 134 สองภาษานี้และผลลัพธ์สองภาษาที่ตรงกัน

## การตรวจสอบและเกณฑ์สำเร็จ

ตรวจ CAD/mesh/geometry APIs ปัจจุบันและ evidence contracts ก่อนหน้า แผน Work 135 ต้องกำหนด inputs, native representations, exact decomposition, interface/assembly requirements, physics-boundary mapping, negative controls, staged acceptance, artifacts, replay, tests, risks และ non-goals ชัดเจน Repository bilingual/document contracts ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

ไม่บังคับ conventional vehicle layout, สร้าง supplier evidence สมมติ, ถือ visual mesh เท่ากับ native CAD หรือเรียก capability ที่วางแผนว่า implemented ไม่ทำ code/CAD implementation, push หรือ history rewrite
