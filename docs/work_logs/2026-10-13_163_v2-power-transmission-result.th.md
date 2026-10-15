# ผลงาน Work 163: การส่งกำลัง v2 (โซ่ลูกกลิ้งแบบ rolling)

ต้นฉบับภาษาอังกฤษ: `2026-10-13_163_v2-power-transmission-result.md`

แผน: `2026-10-13_163_v2-power-transmission-plan.md`

Status: Completed

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/hierarchy/power_transmission.py` (ใหม่):
  `add_power_transmission`, `power_transmission_problems`, `free_strip`,
  `bay_occupants`, `transmission_ids`, `PowerTransmissionConfig`
  (เวอร์ชัน `func-power-transmission-v1`)
- `scripts/hierarchy/generate_functional_vehicle.py`: เรียก
  `add_power_transmission` หลัง `add_direction_control` เพิ่ม
  `power_transmission_problems` ในการตรวจซ้ำชั้นกลไก และนำ config ไป hash
  ภายใต้ `power_transmission` ใน `config_sha256`
- `tests/test_hierarchy_power_transmission.py` (ใหม่ 7 เทสต์)
- บันทึกแผน/ผล (EN + TH), `auto-loop/progress.md` (+ `.th.md`)

## การตัดสินใจ

- assembly ระดับรากหนึ่งตัว `m<k>-power_transmission` (k = 6) ติดแท็ก
  `[power_transmission]` มี 2 หรือ 3 สถานีเรียงตามแนว y ในแถบว่างด้าน -x ของ
  deck bay (จาก `bay_x0 + 0.02 m` ถึงวงกลมกวาดของสิ่งที่อยู่ใน bay ที่ใกล้ที่สุด
  ลบ 0.02 m) แต่ละสถานี: boss (`bonded` กับ deck), post (`bonded` กับ boss),
  roller (จาน N_r เหลี่ยม N_r ใน {48, 64, 96} มีรูเจาะ 96 เหลี่ยมแบบ Work 162
  apothem `r_p + c`, c = 2.5e-5 m ลอยเหนือ boss เป็นระยะ c, `bearing` กับ post)
- ระยะระหว่างศูนย์กลาง roller ข้างเคียงคือ `R_i + R_j + c` (รัศมีวงล้อม) และมี
  จุดยอดชี้ไปยังเพื่อนบ้านแต่ละตัว ช่องว่างจุดยอดที่สุ่มตัวอย่างของ interface
  `rolling` แต่ละอันจึงเป็น c และการกวาดเต็มรอบไม่สามารถถึงเพื่อนบ้านได้
- motion `<assembly>.r<i>` = {roller i} แบบ revolute รอบ +z ช่วง 2 pi
  หลักฐาน `power_transmission: {chain: [r0, r1, ...]}`
- ถ้าแถบแคบ จะจำกัดรัศมี roller และตัดสถานีสุดท้ายออก หากแม้ roller ขนาดเล็กสุด
  สองตัวยังไม่พอดี การวางแผนจะยก error

## การตรวจสอบ

| คำสั่ง | Exit | ผลลัพธ์ |
|---|---|---|
| `python -m unittest tests.test_hierarchy_power_transmission tests.test_hierarchy_direction_control` | 0 | `Ran 15 tests`, `OK` |
| `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed S --out artifacts/work163/seedS` (S = 11, 23, 37) | 0 | เขียน package แล้ว |
| `python artifacts/work163/check.py artifacts/work163 TierA0Interfaces TierA2Motions TierB3PowerTransmission TierB4GroundPropulsion TierB5DirectionControl TierB6Braking TierA1GeometryLanguage TierA3Inertia` (คลาส acceptance ผ่อนการตรวจเก้าคีย์ในเครื่อง) | 0 | `Ran 10 tests`, `OK` |
| `python scripts/hierarchy/evaluate_level0.py --manifest artifacts/work163/seed11/manifest.json --out artifacts/work163/l0_seed11.json` | 0 | `finished`, 10757.947 s, 1993.034 kg, residual 0.0 J |
| `pwsh -NoProfile -File auto-loop/verify.ps1` | 3 | Gate 1 PASS; Gate 2 `Ran 1163 tests`, `OK (skipped=11)`; Gate 3 `Ran 41 tests`, `FAILED (failures=9)` เฉพาะ B1-B9 (การตรวจเก้าคีย์) |

หลักฐานการส่งกำลัง: seed 11/23/37 โซ่ยาว 3/2/3 roller แต่ละตัวช่วง 2 pi rad
มี interface `rolling` 2/1/2 อัน

## ข้อจำกัด

- roller ไม่ได้เชื่อมกับล้อหรือตัวแปลงพลังงาน ไม่มีแบบจำลองแรงบิด ประสิทธิภาพ
  การลื่นไถล หรือฟันเฟือง การสัมผัสเป็นจุดยอดหนึ่งคู่ต่อ roller หนึ่งคู่ (proxy
  จากการสุ่มตัวอย่าง)
- B3 จะผ่านในชุดทดสอบจริงได้หลังจากมีคีย์หลักฐานครบเก้าตัวเท่านั้น
- เป็นเพียง gate ด้านการแทนรูปแบบ ไม่ใช่การยืนยันทางฟิสิกส์

## งานต่อไป

ตัวแปลงพลังงาน (ห้องที่มีรูเจาะ + ลูกสูบ prismatic ที่มี guide), ภาชนะเก็บพลังงาน
และกล่องตัวควบคุมที่มีช่องว่างภายใน, ครีบระบายความร้อน แล้วจึงการตรวจ B7 ว่า
โครงสร้างรับภาระเข้าถึงทุกฟังก์ชัน
