# แผน Work 156: ชนิดรอยต่อแบบผิวสัมผัสเรียบของ v2 โดยไม่มี `threaded` ที่ไม่มีแกน

ฉบับภาษาอังกฤษ: `2026-10-12_156_v2-flush-joint-kinds-plan.md`

วันที่: 2026-10-12

Status: Completed

## วัตถุประสงค์

เป้าหมาย v2 กำหนดให้ interface ชนิด `threaded` ทุกตัวต้องมี `axis_point_m` และ `axis_dir`
ที่เป็นเวกเตอร์หนึ่งหน่วย โดยแกนต้องผ่านรูของชิ้นหนึ่งและผ่านเนื้อวัสดุของอีกชิ้น
layout ของ v1 ต่อ leaf ด้วยการสัมผัสผิวเรียบที่ฝาปลายหรือผิวด้านข้าง ซึ่งไม่มีรูและไม่มีแกน
แต่ decomposition ของ v1 สุ่มได้ `threaded` ประมาณหนึ่งในห้าของรอยต่อ (49 รอยต่อใน seed 11)
ทำให้ `TierA0Interfaces` ของแพ็กเกจ v2 ไม่ผ่าน งานนี้ทำให้ตัวสร้าง v2 สุ่มชนิดรอยต่อแบบผิวสัมผัสเรียบ
จากชนิดของ v1 ที่ตัด `threaded` ออก เพื่อสงวน `threaded` ไว้สำหรับรอยต่อสลักผ่านรูจริง
ซึ่งงานถัดไปจะสร้างเป็นรูปทรง

## ขอบเขต

- `src/formula_ultimate/hierarchy/functional.py`: เพิ่ม `FLUSH_JOINT_KINDS`
  (`JOINT_KINDS` ของ v1 ที่ไม่มี `threaded`) และ
  `V2_DECOMPOSITION_CONFIG = replace(DEFAULT_CONFIG, joint_kinds=FLUSH_JOINT_KINDS)`
- `scripts/hierarchy/generate_functional_vehicle.py`: วางแผนด้วย `V2_DECOMPOSITION_CONFIG`
  และนำไปคำนวณใน `config_sha256`
- เทสต์ใหม่ในไฟล์ใหม่ `tests/test_hierarchy_functional_joints.py`: config v2 ไม่มี `threaded`
  ยังคงชนิดอื่นของ v1 ไว้, แผน v2 ของหลาย seed จัดวางได้โดยไม่มี interface `threaded`
  และค่าเริ่มต้นของ v1 ไม่เปลี่ยน

## ไฟล์ที่วางแผนไว้

- `src/formula_ultimate/hierarchy/functional.py`
- `scripts/hierarchy/generate_functional_vehicle.py`
- `tests/test_hierarchy_functional_joints.py` (ใหม่)
- แผนและผลลัพธ์คู่นี้ (อังกฤษและไทย)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## การตรวจสอบ

1. `python -m unittest tests.test_hierarchy_functional_joints tests.test_hierarchy_functional -v`
2. รันตัวสร้างสำหรับ seed 11 ใต้ CAD runtime ลงใน `artifacts/work156/`
3. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 และ 2 ต้องผ่าน; บันทึก Gate 3 แยกตาม tier

## เกณฑ์ความสำเร็จ

- `TierA0Interfaces` ผ่านสำหรับแพ็กเกจ v2; เทสต์ Tier A0 อื่นทั้งหมดและ Tier A3 ยังผ่าน;
  ชุดเทสต์ v1 ยังผ่าน
- ไม่มีการแก้โมดูล v1 หรือเทสต์ที่มีอยู่

## ความเสี่ยง

- การเปลี่ยนรายการชนิดรอยต่อทำให้ลำดับการสุ่มเปลี่ยน ต้นไม้ v2 จึงต่างจาก v1 ที่ seed เดียวกัน
  ซึ่งยอมรับได้ (v2 เป็นตัวสร้างแยก) แต่ layout อาจล้มเหลวบ่อยขึ้น; fallback ที่ประกาศไว้ของ v1
  (ลอง decomposition ครั้งถัดไป) ยังใช้ได้
- `TierB10ThreadedJoints` ยังไม่ผ่าน (ตอนนี้ล้มเพราะจำนวน 0 < 8 แทน `KeyError`)
  จนกว่าจะมีรอยต่อสลัก

## สิ่งที่ไม่ทำ

- ยังไม่มีรูปทรงรูหรือสลัก, ไม่มี motion, ไม่มี function evidence ในงานนี้
- ไม่มีการทำกรณีพิเศษให้ seed 11, 23 หรือ 37
