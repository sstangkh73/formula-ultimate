# ผลลัพธ์ Work 150: การแตกโครงสร้างแบบนามธรรมที่ขับด้วย seed

ฉบับภาษาอังกฤษ: `2026-10-11_150_seeded-decomposition-result.md`

วันที่: 2026-10-11

แผน: `2026-10-11_150_seeded-decomposition-plan.md`

Status: Completed

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/hierarchy/decomposition.py` (ใหม่)
- `tests/test_hierarchy_decomposition.py` (ใหม่, 12 เทสต์)
- `docs/work_logs/2026-10-11_150_seeded-decomposition-{plan,result}{,.th}.md`
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## สิ่งที่สร้าง

- `DecompositionConfig` ประกาศข้อจำกัดทั้งหมด (งบใบ 170 ถึง 230, ใบขั้นต่ำ 150, 4 ชั้น,
  ความสูงความสามารถ 2 และ 5 ใบ, กิ่ง 2 ถึง 5, ความลึกสูงสุด 7, ความน่าจะเป็นรวม 0.3, ความยาว root 4.0 m,
  สัดส่วน anchor 0.55 ถึง 0.85, สัดส่วน satellite 0.12 ถึง 0.45, ความยาวใบขั้นต่ำ 0.004 m,
  อัตราส่วนขนาดใบ 100, ไม่เกิน 64 attempt)
- `decompose(seed, config)`: ใช้เฉพาะ `random.Random(seed * 1000003 + attempt)`
  สับความสามารถและจัดกลุ่มเดี่ยวหรือคู่; แต่ละกลุ่มได้งบใบแบบถ่วงน้ำหนัก; งบถูกแบ่งแบบ recursive
  ด้วย uniform random composition (กลุ่มความสามารถไม่แตกเป็นใบล้วน จึงสูงอย่างน้อย 2)
  anchor ของแต่ละ assembly คือลูกที่งบมากที่สุด ลูกที่ไม่ใช่ anchor ได้ attachment นามธรรม
  จาก anchor leaf ของตนไปยังใบที่ seed เลือกใน subtree ของ anchor พร้อมชนิดรอยต่อที่ seed เลือก
  attempt ที่ไม่ผ่านข้อจำกัดถูกปฏิเสธ และเก็บหมายเลข attempt ที่ยอมรับ root ไม่มีความสามารถ
- `constraint_violations`, `levels`, `leaves`, `subtree_height`,
  `subtree_leaf_count`, `topology_signature` (นิยามของ acceptance), `config_sha256`

## การตัดสินใจ

- Claude เขียนเอง ไม่ใช่ Codex: การออกแบบ (กฎ anchor, การแบ่งงบ, การค้นหาแบบปฏิเสธ)
  ต้องใช้บริบทของเป้าหมายทั้งหมด และโมดูลสั้น
- ความยาวลักษณะเป็นเป้าหมายการวางแผนสำหรับเรขาคณิตภายหลัง อัตราส่วนขนาดของ acceptance
  วัดจาก mesh และยังไม่ได้พิสูจน์ในงานนี้
- ใบไม่มี functions; sub-assembly สืบทอด functions ของกลุ่ม

## การตรวจสอบ

1. `python -m unittest tests.test_hierarchy_decomposition -v`: exit 0,
   `Ran 12 tests`, `OK`
2. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 PASS; Gate 2
   `Ran 1065 tests`, `OK (skipped=11)`; Gate 3 FAILED 13/13 เพราะยังไม่มี
   `scripts/hierarchy/generate_hierarchical_vehicle.py` (ตามคาด)

หลักฐานจากการกวาด seed (0 ถึง 39 และ 11, 23, 37): 175 ถึง 229 ใบ, 7 ถึง 8 ชั้น,
อัตราส่วนความยาวใบตามแผน 103 ถึง 277, ยอมรับที่ attempt 0 ถึง 2, fan-out สูงสุด 12 (ที่ขีดจำกัดความลึก)

## ข้อจำกัด

- ยังไม่มีเรขาคณิต มวล หรือ interface ที่วัดการสัมผัสได้
- fan-out ที่ขีดจำกัดความลึกอาจถึงประมาณ 12 ลูก ซึ่งการวางเรขาคณิตต้องรองรับ
- ความหลากหลายข้าม seed เป็นเชิงโทโพโลยีเท่านั้น ไม่ได้วัดประโยชน์

## งานถัดไป

- Milestone 3: สร้างเรขาคณิตใบจากต้นไม้นามธรรมด้วย free-form grammar เดิมและ CadQuery,
  export STL หน่วยเมตร และวัดมวลจาก mesh
