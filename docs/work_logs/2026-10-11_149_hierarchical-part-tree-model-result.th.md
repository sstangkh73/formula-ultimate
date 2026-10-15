# ผลลัพธ์ Work 149: โมเดลข้อมูล part tree แบบลำดับชั้น

ฉบับภาษาอังกฤษ: `2026-10-11_149_hierarchical-part-tree-model-result.md`

แผน: `2026-10-11_149_hierarchical-part-tree-model-plan.md`

วันที่: 2026-10-11

Status: Completed

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/hierarchy/__init__.py` (ใหม่)
- `src/formula_ultimate/hierarchy/part_tree.py` (ใหม่)
- `tests/test_hierarchy_part_tree.py` (ใหม่ 11 เทสต์)
- `docs/work_logs/2026-10-11_149_hierarchical-part-tree-model-{plan,result}{,.th}.md`
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## สิ่งที่สร้าง

- frozen dataclass `PartNode`, `AssemblyNode`, `Interface`, `PartTree`
- `validate_part_tree` raise `PartTreeViolation` ในทุกกรณีที่ระบุในแผน (id, parent, วงวน,
  การเข้าถึงได้, ค่าตัวเลข, path ของ mesh, program, functions, contact tolerance ในช่วง `(0, 5e-4]` m,
  ชนิด joint, `interference_m` ในช่วง `(0, 1e-4]` m และใช้ได้เฉพาะ joint ชนิด interference)
- `roll_up`: มวลของ assembly เท่ากับผลรวมมวลของ child และจุดศูนย์กลางมวลถ่วงด้วยมวล
  ทั้งสองค่าคำนวณตามลำดับ child การไล่ต้นไม้ทุกแบบเป็นแบบ iterative และมีเทสต์สายโซ่ลึก 3000 ระดับ
- ตัววัด `levels`, `leaf_ids`, `subtree_height`, `subtree_leaves` และ `topology_signature`
  ซึ่งใช้นิยามเดียวกับชุด acceptance
- `to_manifest_nodes` และ `to_manifest_interfaces` ให้ชุด field ตรงตาม `auto-loop/GOAL.md`

## ผู้ทำงาน

Codex เขียนโมดูลและเทสต์ตามสเปกที่ละเอียด Claude ตรวจ diff ทั้งหมด
Codex ยังสร้างไฟล์ work log ที่ใช้เลขผิด 4 ไฟล์ (`2026-10-11_148_hierarchy-part-tree-*`)
Claude ลบไฟล์เหล่านั้นเพราะซ้ำกับบันทึกนี้ และไฟล์เหล่านั้นไม่เคยถูก commit

## การตรวจสอบ

| คำสั่ง | Exit | ผลลัพธ์ |
|---|---|---|
| `python -m unittest tests.test_hierarchy_part_tree -v` | 0 | `Ran 11 tests in 0.036s`, `OK` |
| `pwsh -NoProfile -File auto-loop/verify.ps1` | 3 (Gate 3) | Gate 1 `PASS`; Gate 2 `Ran 1053 tests in 337.261s`, `OK (skipped=11)`; Gate 3 ตก 13 รายการ ทั้งหมดเป็น `missing: scripts/hierarchy/generate_hierarchical_vehicle.py` (ตามที่คาด) |

## ข้อจำกัด

- เป็นโมเดลการแทนข้อมูลเท่านั้น ไม่มีเรขาคณิต ไม่มี mesh และไม่ผ่านการตรวจสอบทางฟิสิกส์
- ฟังก์ชันตัววัดตรวจต้นไม้ซ้ำทุกครั้งที่เรียก ซึ่งใช้ O(n) ต่อครั้ง
  ยังใช้ได้ดีที่ประมาณ 10^3 node แต่ภายหลังอาจต้องมีฟังก์ชันแบบ batch
- `PartNode.program` เก็บแบบอ้างอิง ผู้เรียกต้องไม่แก้ค่าหลังสร้าง node แล้ว

## งานต่อไป

ถัดไป: Milestone 2 กระบวนการแตกโครงสร้างที่ขับด้วย seed ครอบคลุม 9 capability
ซึ่งสร้างโครง `PartTree` แบบนามธรรม (ไม่มีเรขาคณิต) โดยไม่ใช้แคตตาล็อกชิ้นส่วนแบบดั้งเดิม
