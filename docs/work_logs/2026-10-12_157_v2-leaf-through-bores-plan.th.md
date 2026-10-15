# แผน Work 157: รูเจาะทะลุของ leaf ใน v2 ที่รักษาพื้นที่สัมผัส

ฉบับภาษาอังกฤษ: `2026-10-12_157_v2-leaf-through-bores-plan.md`

วันที่: 2026-10-12

Status: Completed

## วัตถุประสงค์

Tier A1 ของเป้าหมาย v2 กำหนดให้ leaf อย่างน้อย 25 % ไม่เป็นทรงปริซึม (ไม่มีทิศใดทิศเดียวที่ทำให้
พื้นที่ผิว mesh 99 % ขนานหรือตั้งฉากกับทิศนั้น) และอย่างน้อย 5 % มีรูทะลุ (genus >= 1)
leaf ของ v1 ทุกชิ้นเป็นการอัดรีดตรง จึงเป็นทรงปริซึมและมี genus 0 (seed 11: มีรู 0/226)

เพิ่มขั้นตอนปรับแต่ง leaf ของ v2 ที่ทำงานหลัง layout ของ v1 สำหรับ leaf บางส่วนที่ seed เลือก
จะเพิ่มรูเจาะทรงกระบอกทะลุหนึ่งรูให้ของแข็งที่อัดรีดในกรอบพิกัดท้องถิ่น ก่อนการแปลงตำแหน่ง
แกนรูผ่านจุดบนแกนท้องถิ่น `(0, 0, h/2)` เอียงจากแกนอัดรีดเป็นมุม `beta` ที่สุ่ม
(รูเอียงให้เวกเตอร์ตั้งฉากของผนังรูที่ไม่ขนานและไม่ตั้งฉากกับแกนอัดรีด) เข้าทางฝาปลายด้านหนึ่ง
ออกทางฝาปลายอีกด้าน และไม่ถึงผนังด้านข้าง

การปรับแต่งเพียงเอาเนื้อวัสดุภายใน leaf ออก จึงไม่สร้างการทะลุกันใหม่และกล่องของ leaf ไม่โตขึ้น
การสัมผัสรักษาไว้ด้วยกฎ: วงรีทางออกของรูบนฝาปลายต้องห่างจากพื้นที่สัมผัสทุกส่วนที่ฝานั้นรับจากชิ้นข้างเคียง

## กฎเรขาคณิต (หน่วย SI, กรอบพิกัดท้องถิ่นของ leaf)

- อัดรีดตามแกน +z ท้องถิ่นจาก `z = 0` ถึง `z = h`; รัศมีวงในที่ประกาศ
  `rho = inscribed_radius_m - linear_tolerance_m`
- รัศมีรู `r = f * rho` โดยสุ่ม `f` ในช่วงที่ประกาศ; มุมเอียง `beta` สุ่มในช่วงที่ประกาศ
  (5 ถึง 40 องศา) มุมทิศ `phi` สุ่มแบบสม่ำเสมอ
- ระยะเผื่อด้านข้าง: `(h/2) tan(beta) + r / cos(beta) <= (1 - wall) rho`
  ทำให้รูอยู่ในทรงกระบอกวงในตลอด `0 <= z <= h` ถ้าไม่มีมุมเอียงในช่วงที่ใส่ได้
  leaf นั้นไม่ถูกปรับแต่ง (ไม่ตัดทิ้งแบบเงียบ)
- จุดศูนย์กลางทางออก: `-/+ (h/2) tan(beta) (cos phi, sin phi)` บนฝา 0 และ 1;
  ขอบเขตรัศมีทางออก `r / cos(beta)`
- กฎพื้นที่สัมผัสจาก interface ที่วางแผนไว้: ฝาที่เป็นผิวเป้าหมายของฝาต้นทางที่เล็กกว่า (mode `inside`)
  รับดิสก์ของต้นทาง; ฝาต้นทางที่ครอบพื้นที่เป้าหมาย (mode `around`) รับพื้นที่เป้าหมายนั้น
  (รัศมีนอกของดิสก์หรือครึ่งเส้นทแยงของสี่เหลี่ยม) กรณีอื่นขอบผิวทั้งหมดของ leaf ยังสัมผัสอยู่
  จึงไม่ต้องเผื่อระยะ ทางออกแต่ละด้านต้องห่างจากศูนย์กลางพื้นที่สัมผัสทุกจุดบนฝาเดียวกันอย่างน้อย
  `patch radius + r / cos(beta) + linear tolerance`

## ขอบเขต

- ไฟล์ใหม่ `src/formula_ultimate/hierarchy/leaf_refinement.py` (Python ล้วน):
  config, เวอร์ชัน grammar ที่ปรับแต่ง, `contact_patches`, `bore_program`,
  `validate_refined_program`, `base_program`, `refine_layout`
- ไฟล์ใหม่ `scripts/hierarchy/functional_realization.py` (CAD runtime): สร้างโปรแกรม v1
  หรือโปรแกรมที่ปรับแต่งด้วย executor และ tessellation เดิม
- `functional.py`: บันทึกเวอร์ชัน grammar ของแต่ละ leaf ใน manifest
- `scripts/hierarchy/generate_functional_vehicle.py`: ปรับแต่งหลังวางแผน สร้างด้วย realizer ใหม่
  และรวม config การปรับแต่งใน hash
- ทดสอบใหม่ `tests/test_hierarchy_leaf_refinement.py`

## ไฟล์ที่วางแผน

- `src/formula_ultimate/hierarchy/leaf_refinement.py` (ใหม่)
- `scripts/hierarchy/functional_realization.py` (ใหม่)
- `src/formula_ultimate/hierarchy/functional.py`
- `scripts/hierarchy/generate_functional_vehicle.py`
- `tests/test_hierarchy_leaf_refinement.py` (ใหม่)
- แผนและผลลัพธ์คู่นี้ (อังกฤษและไทย)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## การตรวจสอบ

1. `python -m unittest tests.test_hierarchy_leaf_refinement tests.test_hierarchy_functional tests.test_hierarchy_functional_joints -v`
2. รันตัวสร้างสำหรับ seed 11 ด้วย CAD runtime ลงใน `artifacts/work157/` และตรวจสัดส่วน A1
   กับการสัมผัสของ interface ด้วยฟังก์ชันช่วยของชุด acceptance
3. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 และ 2 ต้องผ่าน;
   บันทึก Gate 3 ตาม tier

## เกณฑ์ความสำเร็จ

- `TierA1GeometryLanguage` ผ่าน; การทดสอบ Tier A0 ทั้งหมด A2 และ A3 ยังผ่าน;
  ชุด v1 ยังผ่าน
- ไม่มีการแก้โมดูล v1 หรือการทดสอบเดิม

## ความเสี่ยง

- mesh ที่เจาะรูอาจไม่ปิดหรือนับ genus ผิดถ้า tessellation ไม่ดี; realizer วัดทุก mesh
  และแจ้งข้อผิดพลาดเมื่อ mesh ไม่ปิด
- leaf เล็กอาจได้รูใกล้ค่าความคลาดเคลื่อนของ tessellation; สัดส่วนรัศมีและระยะผนังเผื่อ
  ทำให้รายละเอียดใหญ่กว่า `2e-3 L` มาก
- การไม่เป็นปริซึมด้วยรูเอียงเป็นตัวแทนตามชุด acceptance ไม่ใช่ข้ออ้างเรื่องหน้าที่ทางโครงสร้าง

## สิ่งที่ไม่ทำ

- ไม่มีตัวยึด รอยต่อ `threaded` การเคลื่อนที่ หรือหลักฐานหน้าที่
- ไม่มี leaf แบบเรียวหรือ loft ในงานนี้
- ไม่กำหนดกรณีพิเศษสำหรับ seed 11, 23 หรือ 37
