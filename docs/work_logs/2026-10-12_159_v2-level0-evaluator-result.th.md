# ผลงาน Work 159: ตัวประเมิน Level-0 ของ v2 บนเคอร์เนลการแข่งที่มีอยู่

ต้นฉบับภาษาอังกฤษ: `2026-10-12_159_v2-level0-evaluator-result.md`

สถานะ: Completed

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/hierarchy/level0.py` (ใหม่): มวลรากจาก manifest กล่อง
  หน้าตัด (y-z) จากเมช leaf พื้นที่ลาก `C_box * extent_y * extent_z`
  `RaceVehicle`/`RaceControl` จาก config `run_full_race` ฟิลด์ผลลัพธ์เก้าฟิลด์ และ
  `result_bytes` แบบกำหนดแน่นอน (เรียงคีย์ เยื้อง 2)
- `config/hierarchy/level0_race_v1.json` (ใหม่): `monza_2026`, `C_box = 1.0`,
  `C_rr = 0.015`, 4000 N, 4.0e9 J ไม่มีความร้อนทิ้งหรือกำลังเสริม ก้าวเวลา 1 s,
  timeout 36000 s, bisection 64 รอบ, seed 0
- `scripts/hierarchy/evaluate_level0.py` (ใหม่): CLI `--manifest`, `--out`,
  `--config` (ไม่บังคับ)
- `tests/test_hierarchy_level0.py` (ใหม่ 7 เทสต์)
- `auto-loop/progress.md` และบันทึกแผน/ผลชุดนี้

## การตัดสินใจ

- มวลคือ `mass_kg` ของรากตามที่เขียนใน manifest (ไม่คำนวณใหม่) การแข่งจึงตอบสนอง
  ต่อมวลรถที่ประกาศ
- พื้นที่ลากเป็นขอบเขตบนกล่องหน้าตัด ไม่ใช่ค่าลากที่คำนวณได้ สัญญากำหนดแค่ขอบเขต
  (`<= 1.5 * extent_y * extent_z`)
- แรงคงที่และไม่มีภาระความร้อน ทำให้ใช้เพียงเส้นทางตามยาวและพลังงานของเคอร์เนล
  ไม่ได้เขียนแบบจำลองการแข่งใหม่

## การตรวจสอบ

- `python -m unittest tests.test_hierarchy_level0 -v`: exit 0, `Ran 7 tests`, `OK`
- `python scripts/hierarchy/evaluate_level0.py --manifest artifacts/work158/seed11/manifest.json --out artifacts/work159/a.json`
  (และอีกครั้งไปที่ `b.json`) แล้ว `cmp`: เหมือนกัน ผลลัพธ์: `finished`,
  `race_time_s = 8563.913278125894`, `mass_kg = 351.9110894669954`,
  `drag_area_m2 = 5.022968018346177`, `consumed_energy_j = 1226880000.0`,
  residual `0.0` ใช้เวลาประมาณ 3 s
- การตรวจเชิงพิสูจน์เท็จ (มวลราก x1.5, `artifacts/work159/heavy`): `finished`,
  `race_time_s = 8593.223`, `mass_kg = 527.867` ช้าลงประมาณ 29.3 s
- `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 PASS; Gate 2
  `Ran 1130 tests`, `OK (skipped=11)`; Gate 3 `FAILED (failures=9)`: v1 13/13,
  v2 ผ่าน Tier A ทั้งหมด B10 และ **C1** ส่วน B1-B9 ไม่ผ่าน (ไม่มี `function_evidence`)

## การทบทวน

- หลักฐานสนับสนุน: เวลาแข่งเพิ่มขึ้นตามมวล ผลลัพธ์เหมือนกันทุกไบต์ รหัสเคอร์เนลมาจาก
  replay metadata ของเคอร์เนลเอง
- หลักฐานแย้ง / ข้อจำกัด: ผลของมวลมีขนาดเล็ก (+0.34 % ต่อมวล +50 %) เพราะกล่อง
  หน้าตัดใหญ่ (5.0 m^2) ทำให้แรงลากเด่น และแรงคงที่ไม่สนใจขีดจำกัดกำลัง เวลานี้
  ไม่ใช่การทำนายเวลาต่อรอบ
- คำอธิบายทางเลือก: ไม่มีสำหรับทิศทางของผล ความเร่งและความต้านทานการหมุนขึ้นกับมวล
  ทั้งคู่
- ความมั่นใจ: สูงสำหรับเกตการเชื่อมโยง ไม่มีสำหรับข้ออ้างด้านสมรรถนะ

## ข้อจำกัด

มวลรวมและแรงลากแบบขอบเขตเท่านั้น ไม่มีการเข้าโค้ง ขีดจำกัดกำลัง หรือภาระความร้อน
ไม่ใช่การยืนยันทางกายภาพ

## งานต่อไป

โมดูลความสามารถ B1-B9 และ `function_evidence` (ต้องครบทั้งเก้าก่อนที่เทสต์ B1-B9
ใดจะผ่านได้)
