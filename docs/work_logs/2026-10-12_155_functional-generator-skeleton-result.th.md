# ผลลัพธ์ Work 155: โครงตัวสร้างยานยนต์เชิงฟังก์ชัน (v2) พร้อมโมเมนต์ความเฉื่อยที่วัดได้

ฉบับภาษาอังกฤษ: `2026-10-12_155_functional-generator-skeleton-result.md`

วันที่: 2026-10-12

แผน: `2026-10-12_155_functional-generator-skeleton-plan.md`

Status: Completed

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/hierarchy/functional.py` (ใหม่): `mesh_inertia` (มวล จุดศูนย์กลางมวล และเทนเซอร์ความเฉื่อย
  รอบจุดศูนย์กลางมวลจาก mesh สามเหลี่ยมปิด ด้วยอินทิกรัลทรงสี่หน้ามีเครื่องหมาย), `config_sha256_v2`,
  `build_functional_manifest`, `DESIGN_LANGUAGE_VERSION_V2 = "func-composition-v2"`
- `scripts/hierarchy/generate_functional_vehicle.py` (ใหม่): จุดเข้าใช้งาน v2 ใช้ `plan_vehicle` และ
  `realize_leaf` ของ v1 โดยไม่แก้ไข อ่าน STL ที่ส่งออกทุกไฟล์กลับมา และเขียนฟิลด์ v2
- `tests/test_hierarchy_functional.py` (ใหม่ 6 เทสต์)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## การตัดสินใจ

- เป็นเพียงโครง: `motions = []` และ `function_evidence = {}` ไม่อ้างการเคลื่อนที่หรือหลักฐานความสามารถใด ๆ
  Tier B จงใจให้ล้มเหลวจนกว่างานถัดไป
- ความเฉื่อยคำนวณด้วย float64 จากสามเหลี่ยม STL float32 ที่อ่านกลับมา ซึ่งเป็นข้อมูลเดียวกับที่ชุด acceptance อ่าน
- ไม่แก้โมดูล v1 ตัวสร้าง v2 ห่อ manifest ของ v1

## การตรวจสอบ

1. `python -m unittest tests.test_hierarchy_functional -v`: exit 0, `Ran 6 tests`, `OK`
2. `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed 11 --out artifacts/work155/seed11`:
   exit 0, `seed 11: 226 leaves, 225 interfaces, 0 motions`
3. `pwsh -NoProfile -File auto-loop/verify.ps1`:
   - Gate 1 PASS
   - Gate 2 `Ran 1100 tests in 452.108s`, `OK (skipped=11)`
   - Gate 3 `Ran 41 tests`, `FAILED (failures=13, errors=1)` เทสต์ v1 ทั้ง 13 ผ่าน v2 ที่ผ่าน: TierA0 Replay (2),
     Hierarchy (2), Capabilities, GeometryAndMass (2), FreeForm (2), NoFixedTemplate (2), TierA2 (2, ผ่านแบบว่างเปล่าเท่านั้น:
     ไม่มีการเคลื่อนที่), TierA3 ความเฉื่อย
   - v2 ที่ล้มเหลว: TierA0Interfaces (2): layout ของ v1 สร้าง interface ชนิด `threaded` (49 ตัวใน seed 11) โดยไม่มี
     `axis_point_m`/`axis_dir`; TierA1 (สัดส่วนชิ้นไม่ใช่ปริซึมและชิ้นมีรูทะลุ); TierB1..B9 (ไม่มีหลักฐาน);
     TierB10 error (ข้อต่อเกลียวไม่มีแกน); TierC1 (ยังไม่มีตัวประเมิน)

## ข้อจำกัด

- การผ่าน Tier A2 ยังไม่มีความหมายขณะที่ `motions` ว่าง
- รูปทรงยังเป็นภาษาการอัดรีดตรงของ v1

## งานต่อไป

- ถัดไป: ข้อต่อเกลียวที่มีรูและสลักจริง (แก้ TierA0Interfaces และ TierB10) หรือเปลี่ยนป้ายกำกับการสัมผัสแบบ threaded
  ของ v1 ที่ไม่สามารถมีแกนได้ และเพิ่มใบที่ไม่ใช่ปริซึมและมีรู (TierA1)
