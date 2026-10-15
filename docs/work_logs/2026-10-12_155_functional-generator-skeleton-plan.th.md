# แผน Work 155: โครงตัวสร้างยานยนต์เชิงฟังก์ชัน (v2) พร้อมโมเมนต์ความเฉื่อยที่วัดได้

ฉบับภาษาอังกฤษ: `2026-10-12_155_functional-generator-skeleton-plan.md`

วันที่: 2026-10-12

Status: Completed

## วัตถุประสงค์

ขั้นแรกของเป้าหมาย v2 (`auto-loop/GOAL.md`, Tier A): เพิ่มจุดเข้าใช้งาน v2
`scripts/hierarchy/generate_functional_vehicle.py --seed S --out DIR`
(รันใต้ CadQuery runtime) ที่ใช้แผนและการสร้างรูปทรงของ v1 โดยไม่แก้ไข และเขียนฟิลด์ระดับบนของ v2:
`up_axis = "z"`, `motions`, `function_evidence` และ `vehicle_inertia_kg_m2` (เมทริกซ์ 3x3
รอบจุดศูนย์กลางมวลของยานยนต์ คำนวณจาก mesh ที่ส่งออกแล้วอ่านกลับมา)

## ขอบเขต

- โมดูล Python ล้วนใหม่ `src/formula_ultimate/hierarchy/functional.py`:
  - `DESIGN_LANGUAGE_VERSION_V2 = "func-composition-v2"`
  - `mesh_inertia(meshes_and_density)`: มวล จุดศูนย์กลางมวล และเทนเซอร์ความเฉื่อยรอบจุดศูนย์กลางมวล
    ของชุด mesh สามเหลี่ยมปิดที่มีความหนาแน่นสม่ำเสมอแต่ละชิ้น (อินทิกรัลทรงสี่หน้าตามทฤษฎีไดเวอร์เจนซ์ หน่วย SI)
  - `build_functional_manifest(v1_manifest, motions, function_evidence, inertia)`: manifest ของ v1
    บวกฟิลด์ v2 ทั้งสี่และ design language version ของ v2
- CLI ใหม่ `scripts/hierarchy/generate_functional_vehicle.py`: วางแผนด้วย `plan_vehicle` ของ v1,
  สร้างใบ, อ่าน STL ทุกไฟล์กลับมา, คำนวณความเฉื่อย, เขียน manifest ในโครงนี้ `motions` เป็น `[]` และ
  `function_evidence` เป็น `{}`: ยังไม่อ้างการเคลื่อนที่หรือหลักฐานความสามารถใด ๆ งานถัดไปจะเพิ่มเข้ามา
- `config_sha256` ครอบคลุม config การประกอบของ v1 บวก design language version ของ v2
- เทสต์ใหม่ `tests/test_hierarchy_functional.py`: ความเฉื่อยของกล่องเชิงวิเคราะห์ (มีการเลื่อนและหมุน)
  เทียบกับสูตรปิด ทฤษฎีแกนขนานสำหรับสองวัตถุที่แยกกัน และชุดฟิลด์ของ manifest

## ไฟล์ที่วางแผน

- `src/formula_ultimate/hierarchy/functional.py` (ใหม่)
- `scripts/hierarchy/generate_functional_vehicle.py` (ใหม่)
- `tests/test_hierarchy_functional.py` (ใหม่)
- แผนและผลลัพธ์คู่นี้ (อังกฤษและไทย)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## การตรวจสอบ

1. `python -m unittest tests.test_hierarchy_functional -v`
2. รันตัวสร้างหนึ่งครั้งสำหรับ seed 11 ใต้ CAD runtime ไปที่ `artifacts/work155/`
3. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 และ 2 ต้องผ่าน บันทึก Gate 3 ราย tier
   คาดว่ายังล้มเหลวใน Tier A1 และ Tier B/C

## เกณฑ์ความสำเร็จ

- Tier A0 (สัญญา v1 บนแพ็กเกจ v2) และ Tier A3 (ความเฉื่อย) ผ่าน
- Tier A2 ผ่านเพียงแบบว่างเปล่า (ยังไม่มีการเคลื่อนที่) บันทึกไว้ว่ายังไม่มีความหมาย
- ชุด v1 และเทสต์เดิมทั้งหมดยังผ่าน

## ความเสี่ยง

- ค่าคลาดเคลื่อนความเฉื่อยคือ 1e-5 สัมพัทธ์กับค่าที่ใหญ่ที่สุด การคำนวณจาก mesh float32 ที่อ่านกลับมาด้วย
  float64 ควรตรงกับสูตรของ acceptance
- `motions` / `function_evidence` ที่ว่างต้องไม่ถูกนำเสนอว่าเป็นหลักฐานเชิงฟังก์ชัน เป็นเพียงตัวยึดตำแหน่งที่จงใจให้ Tier B ล้มเหลว

## สิ่งที่ไม่ทำ

- ไม่มีรูปทรงเชิงฟังก์ชัน ไม่มีการเคลื่อนที่ ไม่มีตัวประเมิน Level-0 ในงานนี้
- ไม่แก้โมดูล v1 ไม่ทำกรณีพิเศษให้ seed 11, 23 หรือ 37
