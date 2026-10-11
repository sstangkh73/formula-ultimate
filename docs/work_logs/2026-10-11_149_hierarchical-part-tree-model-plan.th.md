# แผน Work 149: โมเดลข้อมูล part tree แบบลำดับชั้น

ฉบับภาษาอังกฤษ: `2026-10-11_149_hierarchical-part-tree-model-plan.md`

วันที่: 2026-10-11

Status: Completed

## วัตถุประสงค์

Milestone 1 ของ `auto-loop/GOAL.md`: โมเดลข้อมูล part tree แบบ recursive ที่เป็น Python ล้วน
พร้อมการตรวจความถูกต้อง การรวมมวลและจุดศูนย์กลางมวลจากล่างขึ้นบน และการแปลงเป็น manifest
งานถัดไป (การแตกโครงสร้าง, เรขาคณิตชิ้นส่วนด้วย CadQuery, interface, generator CLI) จะต่อยอดจากโมเดลนี้

## ขอบเขต

- package ใหม่ `src/formula_ultimate/hierarchy/` ที่มี `part_tree.py`:
  - frozen dataclass สำหรับ part node (ใบ), assembly node, interface และทั้งต้นไม้
  - `canonical_sha256` ที่ใช้ canonical JSON แบบเดียวกับชุด acceptance
  - `validate_part_tree` ที่ raise `PartTreeViolation` เมื่อ: id ซ้ำ, child ที่ไม่รู้จัก,
    มี parent มากกว่าหนึ่ง, มีวงวน, node ที่เข้าถึงไม่ได้, root ไม่ใช่ assembly หรือไม่มี,
    assembly ว่าง, มวล/ความหนาแน่นไม่จำกัดหรือไม่เป็นบวก, ปลาย interface ที่ไม่ใช่ใบ,
    interface ที่ต่อกับตัวเอง, ชนิด joint ที่ไม่รู้จัก, `interference_m` บน joint ที่ไม่ใช่ interference
    หรืออยู่นอกช่วง `(0, 1e-4]` m, contact tolerance นอกช่วง `(0, 5e-4]` m และ program hash ไม่ตรง
  - `roll_up` คำนวณมวลของ assembly (ผลรวม) และจุดศูนย์กลางมวล (ถ่วงด้วยมวล) จากใบขึ้นไป
  - ตัววัดโครงสร้าง: จำนวนระดับ, จำนวนใบ, ความสูงของ subtree, เซตใบ และ topology signature
    ตามนิยามของชุด acceptance
  - `to_manifest` สร้างรายการ node และ interface ที่มีชุด field ตรงตามสัญญาใน goal
- ไฟล์เทสต์ใหม่ `tests/test_hierarchy_part_tree.py`

## ไฟล์ที่วางแผนไว้

- `src/formula_ultimate/hierarchy/__init__.py` (ใหม่)
- `src/formula_ultimate/hierarchy/part_tree.py` (ใหม่)
- `tests/test_hierarchy_part_tree.py` (ใหม่)
- แผนและผลลัพธ์คู่นี้ (อังกฤษและไทย)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## การตรวจสอบ

1. `python -m unittest tests.test_hierarchy_part_tree -v`
2. `pwsh -NoProfile -File auto-loop/verify.ps1` (Gate 1 และ 2 ต้องผ่าน
   Gate 3 คาดว่ายังตกเพราะยังไม่มี generator)

## เกณฑ์ความสำเร็จ

- เทสต์เฉพาะงานผ่าน รวมถึงเทสต์เชิงลบของทุกกรณีที่ระบุไว้
- Gate 1 และ 2 ผ่าน

## ความเสี่ยง

- โมเดลอาจเบี่ยงจากสัญญา acceptance แก้โดยนำชุด field และค่าคงที่จาก `auto-loop/GOAL.md` โดยตรง
- การรวมค่าทศนิยมต้องอยู่ในค่าคลาดเคลื่อนของ acceptance (มวล 1e-9 สัมพัทธ์, จุดศูนย์กลางมวล 1e-5 m)
  ใช้ผลรวม float ธรรมดาตามลำดับ child

## สิ่งที่ไม่ทำ

- ไม่มีเรขาคณิต ไม่มี CadQuery ไม่มี STL ไม่มีกระบวนการแตกโครงสร้าง ไม่มี generator CLI
  ไม่อ้างว่าผ่านการตรวจสอบทางฟิสิกส์ใดๆ
- ไม่มีค่าวัสดุ โมเดลเก็บค่าความหนาแน่นตามที่ได้รับเท่านั้น
