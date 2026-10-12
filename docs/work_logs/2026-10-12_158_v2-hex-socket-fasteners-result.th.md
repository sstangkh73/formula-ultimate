# ผลงาน Work 158: ตัวยึดแบบรูหกเหลี่ยมใน v2 เป็นรอยต่อ threaded

ต้นฉบับภาษาอังกฤษ: `2026-10-12_158_v2-hex-socket-fasteners-result.md`

วันที่: 2026-10-12

แผน: `2026-10-12_158_v2-hex-socket-fasteners-plan.md`

สถานะ: Completed

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/hierarchy/fasteners.py` (ใหม่): `FastenerConfig`,
  `SOCKETED_LEAF_GRAMMAR_VERSION = "func-leaf-socketed-v2"`, `hexagon`,
  `socket_program`, `socket_base_program`, `validate_v2_program`,
  `pin_program`, `socket_axis`, `socket_exits`, `add_fasteners`,
  `fastener_problems`, `fastener_config_record`
- `src/formula_ultimate/hierarchy/functional.py`: `with_threaded_axes`;
  `config_sha256_v2` รับ record ของตัวยึดแบบไม่บังคับ (hash เดิมไม่เปลี่ยนเมื่อไม่ส่ง)
- `scripts/hierarchy/functional_realization.py`: ตรวจด้วย `validate_v2_program`
- `scripts/hierarchy/generate_functional_vehicle.py`: เรียก `add_fasteners` และ
  `fastener_problems` หลัง refinement ของ Work 157 เขียนแกนของรอยต่อ threaded และ
  hash config ของตัวยึด
- `tests/test_hierarchy_fasteners.py` (ใหม่, 10 เทสต์, มี CAD subprocess หนึ่งตัว)

## การตัดสินใจ

- ใส่รูเฉพาะ leaf ที่ Work 157 ไม่ได้เจาะ (ไม่ต้องพิจารณาการตัดกันของรูเจาะกับรูหกเหลี่ยม)
  leaf ทุกตัวในกลุ่มนี้ได้ลอง (`socket_probability = 1.0`, สุ่ม 24 ครั้ง) config แรก
  (p = 0.6, 12 ครั้ง, `min_apothem_m = 1e-3`) ได้เพียง 7 รอยต่อใน seed 23 และ 3 ใน seed 10
  จึงขยาย config เป็น `min_apothem_m = 5e-4 m` และ 24 ครั้งก่อนรัน acceptance ใดๆ
  จำนวน (จากการวางแผนด้วย Python ล้วน): seed 11/23/37/0/10 ได้ 22/18/21/14/10
- ใช้หกเหลี่ยมแทนทรงกระบอก: ผิวเรียบ tessellate ได้แม่นยำ ผิวหมุดจึงขนานกับผิวรูที่ระยะ
  เผื่อพอดี `c = 2.5e-5 m` (หนึ่งในสี่ของ contact tolerance 1e-4 m) ถ้าเป็นทรงกระบอก
  ช่องว่างและการทะลุจะขึ้นกับ tessellation ของ CAD
- id ของหมุดคือ `<id ของ leaf ที่มีรู>.pin` id ของ interface คือ `<id หมุด>.thread`
  หมุดเป็นลูกใหม่ของ assembly แม่ของ leaf ที่มีรู วัสดุของหมุดสุ่มต่อหมุดจาก catalogue
  ที่ประกาศไว้ด้วย seed ที่ derive แยก จึงไม่เปลี่ยนการสุ่มวัสดุของ leaf เดิม

## คำสั่งและสถานะการออก

1. `python -m unittest tests.test_hierarchy_fasteners tests.test_hierarchy_leaf_refinement tests.test_hierarchy_functional -v`
   exit 0: `Ran 25 tests`, `OK`
2. `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed 11 --out artifacts/work158/seed11`
   exit 0: `seed 11: 248 leaves, 247 interfaces, 0 motions`
3. `python artifacts/work158/check.py artifacts/work158/seed11` (สคริปต์ตรวจที่ถูก
   gitignore ใช้ helper ของ acceptance) exit 0: `threaded 22`, `b10 failures 0`,
   ช่องว่าง interface มากสุด `2.4999994e-05 m`, การทะลุของหมุดมากสุด `0.0`;
   leaf มีรู 114/248, ไม่เป็นปริซึม 162/248
4. `pwsh -NoProfile -File auto-loop/verify.ps1` exit 1 (เฉพาะ Gate 3):
   - Gate 1: `material publication boundary: PASS`
   - Gate 2: `Ran 1123 tests in 729.577s`, `OK (skipped=11)`
   - Gate 3: `Ran 41 tests`, `FAILED (failures=10)` ชุด v1 ผ่าน 13/13 และเทสต์ v2
     Tier A ผ่านทั้งหมด TierB10 ผ่านแล้ว B1-B9 (ไม่มี `function_evidence`) และ C1
     (ไม่มี evaluator) ล้มเหลวตามคาด

## ข้อจำกัด

- หมุดหกเหลี่ยมในรูเป็นเพียงตัวแทนของตัวยึดเกลียว: ไม่มีเกลียว แรงขัน แรงเสียดทาน หรือ
  เส้นทางรับแรง สัญญาตรวจเพียงรูทะลุ
- หมุดไม่ได้หนีบชิ้นอื่นนอกจาก leaf ที่มีรูของตัวเอง รอยต่อแสดงเพียงว่ามีตัวยึดอยู่ในรู
- จำนวนรอยต่อขึ้นกับจำนวน leaf ที่ไม่ได้เจาะและมีที่ว่างพ้น contact patch บนฝา seed 10
  มีเพียง 10 รอยต่อ ถ้าภายหลังเจาะ leaf มากขึ้นบาง seed อาจต่ำกว่า 8

## งานต่อไป

- หลักฐานหน้าที่ของ Tier B: เทสต์ B1-B9 ทุกตัวตรวจก่อนว่า `function_evidence` มีครบ
  เก้า key ดังนั้นจะไม่มี B1-B9 ตัวใดผ่านจนกว่าทั้งเก้า capability มีหลักฐาน ควรวางแผน
  โมดูลหน้าที่ตามนี้
- evaluator ของ Tier C1 (ไม่ขึ้นกับเรขาคณิต เหมาะเป็นงานของ Codex)
