# รายงานปัญหา: โมดูล motion ขาดสัญญาณ corridor

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-28_026_motion-missing-corridor-signal.md`

## บริบท

Work 026 ต้องอินทิเกรตระยะทางแข่งตามแนวสัมผัสสนาม และมี gate ที่แสดง corridor departure ได้

## วิธีทำให้เกิดปัญหา

ตรวจ `config/simulation/coupled_level0_architecture_v1.json` จะพบว่า `input_bridge` สร้าง `circuit.segment_inputs` แต่ `vehicle_motion_solver` รับเพียง:

- `aero.force_moment`
- `contact.force_moment`
- `state.current`

สัญญาณดังกล่าวไปถึง `race_progress_solver` ในภายหลัง หลังจากคำนวณ motion candidate แล้ว

## ผลกระทบ

โมดูล motion ไม่สามารถหาความคืบหน้าตามแนวสัมผัส corridor หรือปฏิเสธ candidate ที่ออกนอก corridor จาก declared reads ได้ การทำเช่นนั้นจะกลายเป็น undeclared read หรือใช้ adapter configuration ที่ซ่อน spatial evidence ของ step

## สาเหตุราก

architecture จาก Work 021 จอง motion output ไว้ก่อนสร้างสัญญา integration ที่พึ่ง corridor ใน Work 026 จึงตกหล่น spatial input ที่สัญญารุ่นหลังต้องใช้

## การแก้ไข

- เก็บ `coupled_level0_architecture_v1.json` เป็นหลักฐานประวัติเดิม
- เพิ่ม `coupled_level0_architecture_v2.json`
- route `circuit.segment_inputs` ไปยัง `vehicle_motion_solver` ใน v2
- pin โมดูล motion เป็น `work026-coupled-motion-v1` ใน v2
- เพิ่ม test ที่ compile v2 แบบ deterministic และตรวจ exact motion input contract

## Regression gate

ชุดทดสอบ Work 026 ต้องล้มเหลวหากเอา `circuit.segment_inputs` ออกจาก motion module ใน v2 และ motion adapter ต้องปฏิเสธ spatial evidence ที่หาย/ไม่รองรับโดยมี output signal เป็นศูนย์

## ข้อจำกัด

การแก้นี้แก้เฉพาะ signal routing ตัวอย่าง corridor เชิงวิเคราะห์เฉพาะตำแหน่งยังเป็นหลักฐาน Level 0 และไม่ทดแทน corridor สามมิติที่สำรวจจริง
