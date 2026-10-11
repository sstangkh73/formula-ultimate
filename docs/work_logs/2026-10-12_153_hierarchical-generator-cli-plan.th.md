# แผน Work 153: CLI ตัวสร้างยานยนต์แบบลำดับชั้น

ฉบับภาษาอังกฤษ: `2026-10-12_153_hierarchical-generator-cli-plan.md`

วันที่: 2026-10-12

Status: Completed

## วัตถุประสงค์

Milestone 5 ของ `auto-loop/GOAL.md`: จุดเข้าใช้งาน
`scripts/hierarchy/generate_hierarchical_vehicle.py --seed S --out DIR`
(รันใต้ CadQuery runtime) ที่ต่อ `decompose` ของ Work 150, `layout` ของ Work 152 และ `realize_leaf`
ของ Work 151 เข้าด้วยกัน แล้วเขียน `DIR/manifest.json` และ STL หน่วยเมตรหนึ่งไฟล์ต่อใบ พร้อมฟิลด์ตามสัญญา
มวลที่วัดได้ และการรวมมวล (roll-up) ที่ตรงพอดี

## ขอบเขต

- `src/formula_ultimate/hierarchy/decomposition.py`: เพิ่มอาร์กิวเมนต์ทางเลือก `start_attempt` ให้
  `decompose` (ค่าเริ่มต้น 0 พฤติกรรมเดิมไม่เปลี่ยน) เพื่อให้ fallback ที่ประกาศไว้ขยับไปยัง attempt ถัดไปได้
- โมดูล Python ล้วนใหม่ `src/formula_ultimate/hierarchy/composition.py`:
  - `plan_vehicle(seed)`: decompose แล้ว layout เมื่อเกิด `LayoutFailure` ให้ขยับไป attempt ถัดไป
    (`start_attempt = tree.attempt + 1`) จำกัดด้วย `max_plan_attempts` ทุกความล้มเหลวถูกบันทึกในแผน
    รัน `layout_problems` และ raise ถ้ายังมีปัญหา
  - `composition_config_sha256(...)`: แฮชของ config และเวอร์ชันของ decomposition, config และเวอร์ชันของ
    layout, เวอร์ชันไวยากรณ์ใบ, ระเบียนวัสดุ, contact tolerance และ design language version
  - `build_manifest(plan, measurements, materials, git_commit)`: สร้าง `PartTree` ของ Work 149
    (functions ของ assembly จากต้นไม้นามธรรม, part จากมวลและจุดศูนย์กลางมวลที่วัดได้, interface
    `id, a, b, kind` จาก layout) และแปลงเป็นฟิลด์ตามสัญญาด้วย `to_manifest_nodes` / `to_manifest_interfaces`
  - การเลือกวัสดุ: สุ่มตาม seed ต่อใบจากไฟล์แคตตาล็อกที่ประกาศไว้ v1 ใช้ระเบียนสังเคราะห์ที่มีอยู่แล้ว
    `synthetic_aluminium_like_verification_v1` ใน
    `config/materials/engineering_material_manufacturing_v1.json`
    (`evidence_status=synthetic`, `design_use_allowed=false`) อ่านตอนรัน ไม่มีการเขียนค่าวัสดุใหม่ลงไฟล์ที่ติดตามใน git
- CLI ใหม่ `scripts/hierarchy/generate_hierarchical_vehicle.py`: อ่านอาร์กิวเมนต์, `git rev-parse HEAD`,
  วางแผน, สร้างทุกใบเป็น `DIR/meshes/<leaf id>.stl`, เขียน `manifest.json` แบบกำหนดแน่นอน
  (`sort_keys`, `allow_nan=False`)
- เทสต์ใหม่ `tests/test_hierarchy_composition.py` (ส่วน Python ล้วน และการรัน CLI หนึ่งครั้งผ่าน subprocess ของ CAD)

## ไฟล์ที่วางแผน

- `src/formula_ultimate/hierarchy/decomposition.py` (แก้ไข)
- `src/formula_ultimate/hierarchy/composition.py` (ใหม่)
- `scripts/hierarchy/generate_hierarchical_vehicle.py` (ใหม่)
- `tests/test_hierarchy_composition.py` (ใหม่)
- แผนและผลลัพธ์คู่นี้ (อังกฤษและไทย)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## การตรวจสอบ

1. `python -m unittest tests.test_hierarchy_composition tests.test_hierarchy_decomposition -v`
2. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 และ 2 ต้องผ่าน Gate 3 รันเต็มและบันทึกผล อาจยังล้มเหลวได้

## เกณฑ์ความสำเร็จ

- CLI ออกด้วยรหัส 0 สำหรับ seed 11, 23 และ 37 เขียนฟิลด์ตามสัญญา และการรันซ้ำได้ไฟล์เหมือนกันทุกไบต์
- มวลของใบมาจาก mesh ที่ส่งออกแล้วอ่านกลับมา คูณความหนาแน่นเท่านั้น
- บันทึกผล Gate 3 รายเทสต์

## ความเสี่ยง

- layout ล้มเหลวสำหรับบาง seed (seed 4 ใน Work 152) จัดการด้วย fallback ที่ประกาศไว้ ถ้าทุก attempt ล้มเหลว
  CLI จะออกด้วยรหัสไม่เป็นศูนย์
- ข้อต่อชนิด `interference` ไม่มี `interference_m` เพราะ layout ทำให้สัมผัสแบบเสมอระนาบ ชื่อชนิดเป็นเพียงป้ายกำกับเชิงการแทนข้อมูล
- วัสดุสังเคราะห์เพียงชนิดเดียวหมายความว่ามวลไม่ใช่มวลสำหรับการออกแบบ

## สิ่งที่ไม่ทำ

- ไม่มีการตรวจสอบทางฟิสิกส์ ไม่มีวัสดุที่มีแหล่งอ้างอิง ไม่แก้ชุด acceptance ไม่ทำกรณีพิเศษให้ seed 11, 23 หรือ 37
