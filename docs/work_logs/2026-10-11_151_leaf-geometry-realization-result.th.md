# ผลลัพธ์ Work 151: การสร้างเรขาคณิตของชิ้นส่วนใบ

ฉบับภาษาอังกฤษ: `2026-10-11_151_leaf-geometry-realization-result.md`

วันที่: 2026-10-11

Status: Completed

แผน: `2026-10-11_151_leaf-geometry-realization-plan.md`

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/hierarchy/leaf_geometry.py` (ใหม่): `leaf_program`,
  `placement_transforms`, `with_placement`, `transform_points`,
  `validate_leaf_program`, `program_sha256`, `stl_bytes`, `read_binary_stl`,
  `closure_problems`, `volume_and_centroid`, `box_fill_fraction`,
  `measure_mesh`
- `scripts/hierarchy/leaf_realization.py` (ใหม่): `build_shape`,
  `tessellate_m`, `realize_leaf` และ CLI ขนาดเล็ก
- `tests/test_hierarchy_leaf_geometry.py` (ใหม่, 9 เทสต์)
- คู่แผน/ผลลัพธ์นี้, `auto-loop/progress.md`, `auto-loop/progress.th.md`

## การตัดสินใจ

- ชิ้นส่วนใบคือ profile รูปดาวแบบ Work 091 (polyline ปิด 5..11 จุดยอด หรือ B-spline แบบ periodic ผ่าน 6..12 จุด
  มุมแบบสุ่มเหลื่อม รัศมี 0.62..1.0 ของรัศมี 0.22..0.5 L) ที่ extrude ตรงตาม +z ท้องถิ่นเป็นระยะ 0.12..0.9 L
  ฝาปลายที่เรียบเป็นหน้าสัมผัสแบบระนาบสำหรับการวางตำแหน่งภายหลัง โปรแกรมบันทึก `contact.height_m`,
  `contact.inscribed_radius_m` (รัศมีวงในของรูปหลายเหลี่ยมแบบตรงตัว; สำหรับ B-spline ใช้
  `0.8 * min radius * cos(pi/n)`) และ `contact.outer_radius_m`
- การรันใช้ `execute_candidate` (Work 092) และจึงใช้ `execute_loop` (Work 091) โดยไม่แก้ไข
  ไม่เรียกตัวตรวจระดับ corpus เพราะตรวจทั้ง corpus (>= 10 candidate, >= 12 profile);
  `validate_leaf_program` ตรวจเฉพาะส่วนย่อยที่โปรแกรมใบใช้แบบตรงตัว
- การวางตำแหน่งเป็นส่วนหนึ่งของโปรแกรม (feature `transform` ของ Work 092) โปรแกรมจึงกำหนด mesh ที่วางแล้วและ hash
  ได้ครบถ้วน `transform_points` ทำซ้ำได้ใน Python ล้วนสำหรับการวางแผนเลย์เอาต์
- STL เขียนด้วยตัวเขียน binary ของเราเองที่ determinate (header คงที่, จุดยอด float32, normal ที่คำนวณ)
  มวลและจุดศูนย์กลางมวลวัดจากสามเหลี่ยม float32 ที่อ่านกลับด้วยสูตรเดียวกับชุด acceptance; ไม่มีการซ่อมใด ๆ

## การตรวจสอบ

| คำสั่ง | Exit | ผลลัพธ์ |
|---|---|---|
| `.tools/cadquery-mcp/Scripts/python.exe artifacts/work151/probe.py 600` (สำรวจ, gitignored) | 0 | `fails 0 time 18.9 fill max 0.8575 diag/L 0.442 .. 1.502` |
| `python -m unittest tests.test_hierarchy_leaf_geometry -v` | 0 | `Ran 9 tests ... OK` |
| `pwsh -NoProfile -File auto-loop/verify.ps1` | 3 | Gate 1 PASS; Gate 2 `Ran 1074 tests`, `OK (skipped=11)`; Gate 3 ล้ม 13/13 (ยังไม่มี generator ตามคาด) |

การรันเทสต์ครั้งแรกล้มหนึ่งข้อ: การเทียบกล่องล้อมรอบหลังวางตำแหน่งใช้ขอบเขตแค่การปัด float32
แต่รูปทรงที่วางแล้วถูกแบ่ง mesh ใหม่ ความต่างจึงถูกจำกัดด้วยค่าความคลาดเคลื่อนเชิงเส้นที่ประกาศ (2e-3 L)
จึงแก้ขอบเขตเป็น `2e-3 * L + 1e-6` m (สังเกตได้ 1.9e-6 m ที่ L = 0.03 m)

## หลักฐาน

- ชิ้นส่วนใบสุ่ม 600 ชิ้น (L ตั้งแต่ 0.004 ถึง 4 m, แกน การพลิก การหมุน และการเลื่อนแบบสุ่ม)
  ส่งออกเป็น mesh ที่ปิดและทิศทางสอดคล้องทั้งหมดในเวลารวม 18.9 s; box-fill สูงสุด 0.858 (< 0.999);
  เส้นทแยงกล่องล้อมรอบ 0.44..1.50 L
- จุดยอดบนฝาอยู่ในช่วงรัศมี `[inscribed, outer]` สำหรับใบที่ทดสอบ; โปรแกรมเดิมให้ไบต์ STL เหมือนกัน

## ข้อจำกัด

- หน้าข้างเบี่ยงจากพื้นผิวจริงได้ถึงค่าความคลาดเคลื่อนเชิงเส้น การสัมผัสจึงต้องใช้ฝาเรียบ ไม่ใช่หน้าข้าง
- รัศมีวงในของ B-spline เป็นค่าเผื่อที่ประกาศ ตรวจเฉพาะกรณีที่ทดสอบ ไม่ได้พิสูจน์
- ยังมีตระกูลรูปทรงเดียว (extrude ตรง); operator อื่นของ Work 092 (loft, revolve, sweep, bore) ยังไม่ได้ใช้
- วัสดุและความหนาแน่นเป็น input; การเลือกจากแคตตาล็อกเป็นงานภายหลัง
- ไม่มีการยืนยันทางกายภาพ

## งานต่อไป

- Milestone 4: การวาง subtree พร้อมการสัมผัสผ่านฝาเรียบและไม่มีการทะลุกัน (เลย์เอาต์ที่ AABB ไม่ซ้อนกัน;
  การตรวจของ acceptance ทดสอบเฉพาะคู่ที่กล่องซ้อนกันมากกว่าค่าความคลาดเคลื่อน)
