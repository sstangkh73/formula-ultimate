# แผนงาน Work 158: ตัวยึดแบบรูหกเหลี่ยมใน v2 เป็นรอยต่อ threaded

ต้นฉบับภาษาอังกฤษ: `2026-10-12_158_v2-hex-socket-fasteners-plan.md`

วันที่: 2026-10-12

สถานะ: Completed

## วัตถุประสงค์

Goal v2 Tier B10 กำหนดให้มี interface ชนิด `threaded` อย่างน้อย 8 รายการต่อ seed
แต่ละรายการมี `axis_point_m` และ `axis_dir` ที่เป็นเวกเตอร์หนึ่งหน่วย เส้นแกนต้อง
ไม่ผ่านเนื้อวัสดุของชิ้นหนึ่ง (รูทะลุ, genus >= 1, มีเนื้อวัสดุครบทั้ง 8 ทิศรัศมีรอบจุดแกน)
และต้องผ่านเนื้อวัสดุของอีกชิ้น (ตัดสามเหลี่ยมอย่างน้อย 2 ครั้ง) ตั้งแต่ Work 156
generator v2 ไม่สร้าง interface `threaded` เลย (seed 11: 0 < 8)

เพิ่มขั้นตอนตัวยึดหลัง refinement: สำหรับ leaf ที่ seed เลือกจากกลุ่มที่ Work 157
ไม่ได้เจาะรู ให้ตัดรูหกเหลี่ยมด้านเท่าตามแนวแกนทะลุ leaf (เป็น loop ชนิด `hole`
ใน profile ที่ extrude) และเพิ่ม leaf หมุดใหม่: แท่งปริซึมหกเหลี่ยมที่สวมอยู่ในรูโดยมี
ระยะเผื่อที่ประกาศไว้ หมุดกับ leaf ที่มีรูเชื่อมกันด้วย interface `threaded` ที่มีแกน
เป็นแกนของรู

## กฎเรขาคณิต (หน่วย SI, กรอบพิกัดเฉพาะที่ของ leaf ที่มีรู)

- leaf ที่มีรู extrude ตามแกน +z เฉพาะที่ จาก `z = 0` ถึง `z = h`;
  `rho = inscribed_radius_m - linear_tolerance_m`
- รู: หกเหลี่ยมด้านเท่า apothem `a`, เฟส `phi`, จุดศูนย์กลาง `(ox, oy)`,
  รัศมีวงล้อม `R = a / cos(pi/6)` กฎ `|(ox, oy)| + R <= (1 - wall) rho`
  ทำให้รูอยู่ในวงกลมแนบใน (จึงอยู่ใน outer loop) และ `a >= min_apothem_m`
- ทางออกที่ฝาปลาย: จุดศูนย์กลาง `(ox, oy, 0)` และ `(ox, oy, h)` ในพิกัดโลกต้องห่าง
  จาก contact patch ทุกอันที่ฝานั้นรับอย่างน้อย `รัศมี patch + R + linear tolerance`
  (ใช้ `contact_patches` ของ Work 157)
- หมุด: ปริซึมหกเหลี่ยมเฟสเดียวกัน apothem `a - c` สูง `h - 2c` เลื่อนเฉพาะที่
  `(ox, oy, c)` แล้วตามด้วย placement ของ leaf ที่มีรู ระยะเผื่อ `c = 2.5e-5 m`
  (หนึ่งในสี่ของ contact tolerance 1e-4 m) ผิวเรียบของหมุดจึงขนานกับผิวรูที่ระยะ `c`:
  ช่องว่างสัมผัสที่วัดได้ `c <= tolerance` และไม่ทะลุกัน ผิวเรียบ tessellate ได้แม่นยำ
  จึงเป็นจริงบน mesh ด้วย (ยกเว้นการปัดเศษ float32 ราว 1e-7 m)
- แกนเกลียว: `axis_point_m` = ภาพในพิกัดโลกของ `(ox, oy, h/2)` (อยู่ภายในความหนา
  ของชิ้นที่มีรู), `axis_dir` = ภาพในพิกัดโลกของ +z เฉพาะที่
- leaf หมุดเป็นลูกใหม่ของ assembly แม่ของ leaf ที่มีรู (จึงอยู่ใน subtree ของ
  capability เดียวกัน) วัสดุสุ่มต่อหมุดจาก catalogue ที่ประกาศไว้ มวลของ assembly
  รวมขึ้นจาก mesh ที่วัดได้เหมือนเดิม

## ขอบเขต

- ไฟล์ใหม่ `src/formula_ultimate/hierarchy/fasteners.py` (Python ล้วน): config,
  grammar version ของ leaf ที่มีรู, `socket_program`, `pin_program`,
  `validate_v2_program`, `add_fasteners`, `fastener_problems`
- `scripts/hierarchy/functional_realization.py`: ตรวจด้วย `validate_v2_program`
  เพื่อให้ program ที่มีรูหกเหลี่ยมสร้างได้
- `src/formula_ultimate/hierarchy/functional.py`: `with_threaded_axes`
- `scripts/hierarchy/generate_functional_vehicle.py`: เรียกขั้นตอนตัวยึดหลัง
  refinement เพิ่มแกน และ hash config ของตัวยึด
- เทสต์ใหม่ `tests/test_hierarchy_fasteners.py`

## ไฟล์ที่วางแผน

- `src/formula_ultimate/hierarchy/fasteners.py` (ใหม่)
- `scripts/hierarchy/functional_realization.py`
- `src/formula_ultimate/hierarchy/functional.py`
- `scripts/hierarchy/generate_functional_vehicle.py`
- `tests/test_hierarchy_fasteners.py` (ใหม่)
- แผนและผลลัพธ์คู่นี้ (อังกฤษและไทย)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## การตรวจสอบ

1. `python -m unittest tests.test_hierarchy_fasteners tests.test_hierarchy_leaf_refinement tests.test_hierarchy_functional -v`
2. รัน generator สำหรับ seed 11 ใน CAD runtime ไปที่ `artifacts/work158/` และตรวจ
   แบบสุ่มด้วย helper ของ acceptance (เงื่อนไข B10, ช่องว่าง interface, การทะลุของหมุด)
3. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 และ 2 ต้องผ่าน; บันทึก
   Gate 3 แยกตาม tier

## เกณฑ์ความสำเร็จ

- Gate 1 และ 2 ผ่าน เทสต์ Tier A ทุกตัวยังผ่าน TierB10 ผ่านสำหรับ seed 11, 23 และ 37

## เกณฑ์ความล้มเหลว

- บาง seed ใส่รูได้น้อยกว่า 8 รู หมุดทะลุหรือเสียการสัมผัส หรือเทสต์ Tier A ใดถดถอย

## ความเสี่ยง

- leaf ที่ไม่ได้เจาะและมีที่ว่างพ้น contact patch มีน้อยเกินไป ทางลด: ประกาศ
  ความน่าจะเป็นและจำนวนครั้งที่สุ่ม และบันทึกจำนวนต่อ seed
- ทิศทางหรือการซ้อนของ hole loop ใน CAD ล้มเหลว ทางลด: เทสต์ CAD

## สิ่งที่ไม่ทำ

- ไม่มีเรขาคณิตเกลียวจริง (สัญญาตรวจเพียงรูทะลุ) ไม่อ้างเรื่องแรงขันหรือเส้นทางรับแรง
  ไม่แก้โมดูล v1 หรือเทสต์ที่มีอยู่
