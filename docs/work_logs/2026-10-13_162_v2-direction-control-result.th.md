# ผลงาน Work 162: การควบคุมทิศทาง v2 (เสาบังคับเลี้ยวและแขน)

ต้นฉบับภาษาอังกฤษ: `2026-10-13_162_v2-direction-control-result.md`

แผน: `2026-10-13_162_v2-direction-control-plan.md`

Status: Completed

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/hierarchy/direction_control.py` (ใหม่):
  `add_direction_control`, `direction_control_problems`, `steering_bore`,
  `convex_hull`, `steer_ids`, `DirectionControlConfig`
  (เวอร์ชัน `func-direction-control-v1`)
- `scripts/hierarchy/generate_functional_vehicle.py`: เรียก
  `add_direction_control` หลัง `add_ground_contacts` เพิ่ม
  `direction_control_problems` ในการตรวจซ้ำชั้นกลไก และนำ config ไป hash
  ภายใต้ `direction_control` ใน `config_sha256`
- `tests/test_hierarchy_direction_control.py` (ใหม่ 8 เทสต์ รวมเทสต์ realization
  ด้วย CAD หนึ่งเทสต์)
- บันทึกแผน/ผล (EN + TH), `auto-loop/progress.md` (+ `.th.md`)

## การตัดสินใจ

- การบังคับเลี้ยวเป็น assembly ระดับราก `m<k>-direction_control` (k = 5 เมื่อมี
  มุมล้อสี่มุม) ประกอบด้วย boss (`bonded` กับ deck), post (`bonded` กับ boss)
  และ arm (`bearing` กับ post) ทั้งหมดเป็น prism `func-leaf-mechanism-v2` ตาม +z
  motion คือ `{arm}` แบบ revolute รอบ +z ผ่านแกน post ช่วงสุ่มใน [0.3, 0.8] rad
  แกนตั้งฉากกับแกนล้อทุกแกน (y)
- รูเจาะ: 96 เหลี่ยม apothem `r_p + c` (c = 2.5e-5 m) มีจุดยอดในทิศจุดยอดของ post
  ทุกจุด (96 หารด้วย 6 และ 8 ลงตัว) ช่องว่างสถิตจึงเป็น c จุดสุ่มตัวอย่างจุดยอดเห็น
  การสัมผัสของ bearing และไม่มีการหมุนใดทะลุได้
- arm ลอยเหนือผิวบนของ boss เป็นระยะ c (ระยะเผื่อแรงตามแกน ไม่ถือเป็นการสัมผัส)
  post อยู่ปลาย +x ของ bay กึ่งกลางในแนว y วงกลมกวาดเต็มรอบอยู่ภายใน bay และขอบ
  deck 0.02 m ถ้า bay หรือ deck แคบ จะลดความยาวแขน (ยก error ถ้าแขนยาวไม่เกินรัศมี
  hub) ส่วน -x ของ bay ยังว่าง

## การตรวจสอบ

| คำสั่ง | Exit | ผลลัพธ์ |
|---|---|---|
| `python -m unittest tests.test_hierarchy_direction_control tests.test_hierarchy_ground_contacts tests.test_hierarchy_mechanisms` | 0 | `Ran 26 tests`, `OK` |
| `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed S --out artifacts/work162/seedS` (S = 11, 23, 37) | 0 | 268 / 267 / 270 leaves, 5 motions ต่อ seed |
| `python artifacts/work162/check.py artifacts/work162 TierA0Interfaces TierA0Hierarchy TierA0Capabilities TierA0NoFixedTemplate TierA1GeometryLanguage TierA2Motions TierA3Inertia TierB4GroundPropulsion TierB5DirectionControl TierB6Braking` (คลาส acceptance ผ่อนการตรวจเก้าคีย์ในเครื่อง) | 0 | `Ran 14 tests`, `OK` |
| `python scripts/hierarchy/evaluate_level0.py --manifest artifacts/work162/seed11/manifest.json --out artifacts/work162/l0_seed11.json` | 0 | `finished`, 10756.945 s, 1988.451 kg, residual 0.0 J |
| `pwsh -NoProfile -File auto-loop/verify.ps1` | 1 | Gate 1 PASS; Gate 2 `Ran 1156 tests`, `OK (skipped=11)`; Gate 3 `FAILED (failures=9)` เฉพาะ B1-B9 (การตรวจเก้าคีย์) |

หลักฐานการบังคับเลี้ยว: seed 11/23/37 ช่วง 0.743/0.792/0.393 rad; มวลราก
1988.5/2096.5/1484.0 kg

## ข้อจำกัด

- แขนไม่ได้เชื่อมกับล้อ ไม่มีเรขาคณิตการเลี้ยวหรือพลศาสตร์ยานยนต์ ไม่มีการจำลอง
  การยึดแขนตามแกน
- B5 จะผ่านในชุดทดสอบจริงได้หลังจากมีคีย์หลักฐานครบเก้าตัวเท่านั้น
- เป็นเพียง gate ด้านการแทนรูปแบบ ไม่ใช่การยืนยันทางฟิสิกส์

## งานต่อไป

การส่งกำลัง (ลูกกลิ้งหมุนเต็มรอบสองตัวบนเสา มีการสัมผัส `rolling`), ตัวแปลงพลังงาน
(ห้อง + ลูกสูบที่มี guide), ภาชนะและกล่องตัวควบคุมที่มีช่องว่าง, ครีบระบายความร้อน
แล้วจึงการตรวจ B7 ว่าโครงสร้างหลักเข้าถึงทุกฟังก์ชัน
