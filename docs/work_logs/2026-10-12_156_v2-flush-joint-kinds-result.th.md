# ผลลัพธ์ Work 156: ชนิดรอยต่อแบบผิวสัมผัสเรียบของ v2 โดยไม่มี `threaded` ที่ไม่มีแกน

ฉบับภาษาอังกฤษ: `2026-10-12_156_v2-flush-joint-kinds-result.md`

แผน: `2026-10-12_156_v2-flush-joint-kinds-plan.md`

วันที่: 2026-10-12

Status: Completed

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/hierarchy/functional.py`: `FLUSH_JOINT_KINDS` (`JOINT_KINDS` ของ v1
  ที่ไม่มี `threaded`) และ `V2_DECOMPOSITION_CONFIG` (`DEFAULT_CONFIG` ที่เปลี่ยนเฉพาะ `joint_kinds`)
- `scripts/hierarchy/generate_functional_vehicle.py`: วางแผนด้วย `V2_DECOMPOSITION_CONFIG`
  และนำไปคำนวณใน `config_sha256`
- `tests/test_hierarchy_functional_joints.py` (ใหม่, 4 เทสต์)
- ผลลัพธ์คู่นี้, แผนคู่, `auto-loop/progress.md` และ `auto-loop/progress.th.md`

## การตัดสินใจ

- การสัมผัสที่ฝาปลายหรือผิวด้านข้างแบบเรียบไม่มีรูและไม่มีแกน การติดป้าย `threaded`
  จึงไม่อาจผ่านสัญญา v2 แทนที่จะเปลี่ยนป้ายหลังสุ่ม ตัวสร้าง v2 สุ่มชนิดรอยต่อผิวเรียบจากชนิดของ v1
  ที่ไม่ต้องมีแกน (`welded`, `bonded`, `interference`, `integral`) และสงวน `threaded`
  ไว้สำหรับรอยต่อสลักผ่านรูที่งานถัดไปจะสร้างเป็นรูปทรงพร้อมแกน
- ตัวสร้าง v1, config เริ่มต้นของ v1 และเทสต์ v1 ทั้งหมดไม่เปลี่ยน
- รายการตัวเลือกที่เปลี่ยนทำให้ลำดับการสุ่มเปลี่ยน ต้นไม้ v2 จึงต่างจาก v1 ที่ seed เดียวกัน
  ซึ่งยอมรับได้ เพราะ v2 เป็นตัวสร้างแยกที่มี `config_sha256` ของตัวเอง

## การตรวจสอบ

1. `python -m unittest tests.test_hierarchy_functional_joints tests.test_hierarchy_functional -v`
   -> `Ran 10 tests in 24.035s`, `OK` (exit 0)
2. `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed 11 --out artifacts/work156/seed11`
   -> `seed 11: 226 leaves, 225 interfaces, 0 motions` (exit 0)
3. `pwsh -NoProfile -File auto-loop/verify.ps1`:
   - Gate 1: `material publication boundary: PASS`
   - Gate 2: `Ran 1104 tests in 503.882s`, `OK (skipped=11)`
   - Gate 3: `Ran 41 tests`, `FAILED (failures=12)` ชุด v1 ผ่าน 13/13 ใน v2 Tier A0
     ผ่านทั้งหมดแล้ว (รวมเทสต์ `TierA0Interfaces` ทั้งสองที่เคยล้ม) รวมถึง Tier A2
     (ยังผ่านแบบว่างเปล่าเพราะไม่มี motion) และ Tier A3 ที่ยังล้ม: Tier A1 (leaf มีรู 0 ชิ้น),
     Tier B1–B10 (ไม่มี evidence; B10 ตอนนี้ล้มเพราะจำนวน 0 < 8 แทน `KeyError`) และ Tier C1
     (ยังไม่มี evaluator)

## ข้อจำกัด

- ตอนนี้แพ็กเกจ v2 ไม่มีรอยต่อ threaded เลย `TierB10ThreadedJoints` ต้องการสลักผ่านรูจริง
  (อย่างน้อย 8 ต่อ seed)
- Tier A2 ที่ผ่านยังเป็นแบบว่างเปล่าจนกว่าจะมี motion

## งานต่อไป

- ภาษารูปทรง Tier A1: leaf ที่ไม่ใช่ prismatic (>= 25 %) และ leaf ที่มีรูทะลุ (>= 5 %)
  แล้วจึงทำสลักเกลียวผ่านรูเหล่านั้น
