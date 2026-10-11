# ผลลัพธ์ Work 153: CLI ตัวสร้างยานยนต์แบบลำดับชั้น

ฉบับภาษาอังกฤษ: `2026-10-12_153_hierarchical-generator-cli-result.md`

วันที่: 2026-10-12

Status: Completed

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/hierarchy/decomposition.py`: `decompose(seed, config,
  start_attempt=0)` พฤติกรรมค่าเริ่มต้นไม่เปลี่ยน
- `src/formula_ultimate/hierarchy/composition.py` (ใหม่): `plan_vehicle`
  (decompose -> layout -> `layout_problems` เมื่อเกิด `LayoutFailure` ให้ค้นต่อจาก decomposition attempt ถัดไป
  สูงสุด `max_plan_attempts=8` และบันทึกการปฏิเสธไว้), `load_leaf_materials`, `assign_materials`,
  `composition_config_sha256`, `build_part_tree`, `build_manifest`, `manifest_bytes`
  `DESIGN_LANGUAGE_VERSION = "hier-composition-v1"`, `contact_tolerance_m = 1e-4`
- `scripts/hierarchy/generate_hierarchical_vehicle.py` (ใหม่): จุดเข้าใช้งานตามสัญญา สร้างแต่ละใบด้วย
  `realize_leaf` ของ Work 151 ไปยัง `DIR/meshes/<leaf id>.stl` ใช้มวลและจุดศูนย์กลางมวลจาก STL ที่อ่านกลับมา
  และเขียน `manifest.json` (เรียงคีย์ ไม่มี NaN)
- `tests/test_hierarchy_composition.py` (ใหม่ 12 เทสต์ หนึ่งเทสต์รัน CLI ใต้ CAD runtime สำหรับ seed 37)
- ผลลัพธ์คู่นี้ แผนคู่ `auto-loop/progress.md` และ `auto-loop/progress.th.md`

## การตัดสินใจ

- วัสดุ: v1 อ่านระเบียนสังเคราะห์ที่มีอยู่แล้ว `synthetic_aluminium_like_verification_v1` จาก
  `config/materials/engineering_material_manufacturing_v1.json` ตอนรัน
  (`evidence_status=synthetic`, `design_use_allowed=false`) ไม่มีค่าวัสดุใดถูกเขียนลงไฟล์ที่ติดตามใน git
  ค่าความหนาแน่นปรากฏเฉพาะในแพ็กเกจที่สร้างขึ้นใต้ `artifacts/` หรือไดเรกทอรีชั่วคราว
  การสุ่มต่อใบขับด้วย seed จึงเพิ่มแคตตาล็อกที่ใหญ่ขึ้นได้โดยไม่ต้องแก้โค้ด
- ชนิดข้อต่อเป็นป้ายของ Work 150 ข้อต่อ `interference` ไม่มี `interference_m` เพราะ layout ทำให้สัมผัส
  เสมอระนาบ (ฟิลด์นี้เป็นทางเลือกในสัญญา)
- fallback ของ layout เป็นส่วนหนึ่งของการค้นหาที่ประกาศไว้ ไม่ใช่กรณีพิเศษราย seed

## คำสั่งและสถานะการออก

1. `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_hierarchical_vehicle.py --seed 11 --out artifacts/work153/seed11`
   exit 0, `226 leaves, 225 interfaces`, 13.8 s
2. คำสั่งเดียวกันกับ `--seed 4`: exit 0 decomposition attempt สองครั้งถูก layout ปฏิเสธและบันทึกใน stderr
   `180 leaves, 179 interfaces`
3. `python -m unittest discover -s auto-loop/acceptance`: `Ran 13 tests in 66.881s`, `OK`
4. `python -m unittest tests.test_hierarchy_composition tests.test_hierarchy_decomposition`:
   `Ran 24 tests in 86.384s`, `OK`
5. ไล่วางแผน seed 0..39 (Python ล้วน): ล้มเหลว 0 มี 1 seed (4) ที่ต้องใช้ fallback
6. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 `PASS`; Gate 2
   `Ran 1094 tests in 502.849s`, `OK (skipped=11)`; Gate 3 `Ran 13 tests in
   71.967s`, `OK`; `ALL GATES PASSED`

## ข้อจำกัด

- การผ่าน Gate 3 เป็นเพียงเกตด้านการแทนรูปทรงและการประกอบ ไม่มีสิ่งใดแสดงว่าชิ้นส่วนใดทำงาน รับภาระ หรือทนความร้อนได้
- มีวัสดุสังเคราะห์ชนิดเดียว มวลทุกค่าจึงเป็นค่าเชิงการแทนข้อมูล ไม่ใช่มวลสำหรับการออกแบบ
- ป้ายชนิดข้อต่อไม่มีแบบจำลองทางฟิสิกส์รองรับ
- การที่กล่องไม่ทับกันทำให้ยานยนต์โปร่ง ยังไม่ได้จัดวางให้กระชับ
- การตรวจการทะลุกันของ acceptance สุ่มเฉพาะจุดยอดและจุดศูนย์กลางสามเหลี่ยม

## งานต่อเนื่อง

- แทนวัสดุสังเคราะห์ด้วยวัสดุจากแคตตาล็อกเท่านั้น (ค่าอยู่ใน `/private/` หรืออ่านตอนรัน) และบันทึกขั้นตอนการเลือกวัสดุ
- เชื่อมลำดับชั้นเข้ากับฟิสิกส์ Level-0 และ race kernel (เป้าหมายภายหลัง)
