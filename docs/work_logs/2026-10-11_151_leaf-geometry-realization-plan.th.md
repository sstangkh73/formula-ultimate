# แผน Work 151: การสร้างเรขาคณิตของชิ้นส่วนใบ

ฉบับภาษาอังกฤษ: `2026-10-11_151_leaf-geometry-realization-plan.md`

วันที่: 2026-10-11

Status: Completed

## วัตถุประสงค์

Milestone 3(a) ของ `auto-loop/GOAL.md`: แปลงชิ้นส่วนใบนามธรรมหนึ่งชิ้นเป็นโปรแกรม free-form ที่บันทึกไว้
รันผ่านตัวประมวลผล grammar ของ Work 091/092 ที่มีอยู่ภายใต้ CadQuery ส่งออก STL แบบ binary ที่ปิดสนิทในหน่วยเมตร
และวัดมวลกับจุดศูนย์กลางมวลจาก mesh ที่ส่งออก (ไม่ใช่จาก CAD kernel)

## ขอบเขต

- โมดูล Python ล้วนใหม่ `src/formula_ultimate/hierarchy/leaf_geometry.py`:
  - `leaf_program(rng, characteristic_length_m, placement)` คืน program dict ที่ประกอบด้วย profile แบบ Work 091
    (outer loop หนึ่งวง: polyline ปิดหรือ B-spline แบบ periodic ที่เป็นรูปดาวรอบจุดกำเนิดพร้อมรัศมีวงในที่ประกาศ)
    และ candidate แบบ Work 092 (`section -> extrude` ตาม +z แล้วตามด้วย feature `transform` สำหรับการวางตำแหน่ง)
    รวมถึงค่าความคลาดเคลื่อนของการแบ่ง mesh การ extrude มีหน้าปลายเรียบที่ `z = 0` และ `z = h` ในพิกัดท้องถิ่น
    เพื่อใช้สัมผัสแบบระนาบในภายหลัง
  - `validate_leaf_program(program)` ตรวจชุดฟิลด์ที่ตรงตัวและขอบเขต
  - ตัวเขียน/อ่าน STL แบบ binary, การตรวจความปิด, ปริมาตรแบบมีเครื่องหมายและ centroid,
    และ `measure_mesh(triangles, density)` ที่คืนมวลและจุดศูนย์กลางมวล
- โมดูลสคริปต์ CadQuery ใหม่ `scripts/hierarchy/leaf_realization.py`:
  `realize_leaf(program, stl_path)` ที่ใช้ `execute_loop`
  (`scripts/cad/generate_freeform_wire_corpus.py`) และ `execute_candidate`
  (`scripts/cad/generate_freeform_solid_corpus.py`) ซ้ำ แปลง mm เป็น m แบ่ง mesh ตามค่าความคลาดเคลื่อนที่ประกาศ
  เขียน STL แบบ binary ที่ determinate และปฏิเสธ mesh ที่ไม่ปิดหรือทิศทางไม่สอดคล้อง
- เทสต์ใหม่ `tests/test_hierarchy_leaf_geometry.py`: เทสต์ Python ล้วนภายใต้ `python`
  และเทสต์ไปกลับผ่าน CadQuery ที่รันด้วย CAD interpreter ที่ตรึงไว้ใน subprocess (ข้ามเมื่อไม่มี interpreter)

## ไฟล์ที่วางแผน

- `src/formula_ultimate/hierarchy/leaf_geometry.py` (ใหม่)
- `scripts/hierarchy/__init__.py`, `scripts/hierarchy/leaf_realization.py` (ใหม่)
- `tests/test_hierarchy_leaf_geometry.py` (ใหม่)
- คู่แผนและผลลัพธ์นี้ (อังกฤษและไทย)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## การตรวจสอบ

1. `python -m unittest tests.test_hierarchy_leaf_geometry -v`
2. `pwsh -NoProfile -File auto-loop/verify.ps1` (Gate 1 และ 2 ต้องผ่าน;
   Gate 3 ยังล้มเพราะยังไม่มี generator)

## เกณฑ์ความสำเร็จ

- โปรแกรมสำหรับความยาว 0.004 m ถึง 4 m สร้าง ส่งออก และอ่านกลับได้เป็น mesh ที่ปิดและทิศทางสอดคล้องพร้อมปริมาตรบวก
- เส้นทแยงของกล่องล้อมรอบที่ส่งออกอยู่ภายในตัวคูณที่ประกาศของความยาวลักษณะ; สัดส่วนการเติมกล่องต่ำกว่า 0.999
- มวลเท่ากับปริมาตร mesh คูณความหนาแน่นตามที่คำนวณจาก STL แบบ float32 พอดี;
  โปรแกรมเดิมให้ไบต์ STL เหมือนกันสองครั้ง
- `program_sha256` คือ SHA-256 ของ canonical JSON ของโปรแกรม

## ความเสี่ยง

- การแบ่ง mesh ของ OpenCascade อาจไม่ใช้ node ขอบร่วมกันระหว่างหน้าอย่างตรงตัวหลังปัดเป็น float32;
  สิ่งนี้ถูกตรวจและล้มอย่างชัดเจน ไม่ซ่อมแบบเงียบ
- ชิ้นส่วนที่เล็กมากอาจให้สามเหลี่ยม float32 ที่เสื่อม

## สิ่งที่ไม่ทำ

- ไม่มีการค้นหาตำแหน่งวาง, interface, วัสดุ, manifest หรือ generator CLI
- ไม่มีการยืนยันทางกายภาพของชิ้นส่วนใด
