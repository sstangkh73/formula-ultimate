# ผลงาน Work 160: โครงชั้นกลไกของ v2 และแผ่นพื้นโครงสร้าง

ต้นฉบับภาษาอังกฤษ: `2026-10-12_160_v2-mechanism-backbone-result.md`

สถานะ: Completed

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/hierarchy/mechanisms.py` (ใหม่): `measure_cluster`,
  ไวยากรณ์ปริซึมกลไก `func-leaf-mechanism-v2` (`prism_program`,
  `validate_mechanism_program`, `prism_vertices`), `plan_backbone`,
  `plan_mechanisms`, `mechanism_problems`, `roll_up_manifest_nodes`,
  `merge_mechanism_layer`, `mechanism_config_record`
- `scripts/hierarchy/functional_realization.py`: ตรวจโปรแกรมกลไกด้วย
  `validate_mechanism_program` โปรแกรมอื่นตรวจเหมือนเดิม
- `scripts/hierarchy/generate_functional_vehicle.py`: สร้างกลุ่มชิ้นส่วน อ่านเมชกลับ
  วัดกล่อง วางแผน/สร้าง/รวมชั้นกลไก อินทิเกรตความเฉื่อยจากเมชกลุ่มชิ้นส่วนรวมกลไก
  และแฮช config ของกลไก
- `src/formula_ultimate/hierarchy/functional.py`: `config_sha256_v2(...,
  mechanisms=None)`
- `tests/test_hierarchy_mechanisms.py` (ใหม่, 10 การทดสอบ รวมหนึ่งการทดสอบ CAD)

## การตัดสินใจ

- leaf ของกลไกอยู่ใน assembly ระดับราก `m<k>-<capability>` และพบกลุ่มชิ้นส่วน v1
  ผ่านแผ่นพื้นเท่านั้น (interface ที่นั่ง `bonded` กับ leaf ต่ำสุดของกลุ่ม ซึ่งมีจุดยอด
  อยู่บนผิวบนแผ่นพื้นที่ `Z0`)
- แผ่นพื้น: แปดเหลี่ยมตัดมุม หนา 0.04-0.06 m ระยะขอบ 0.08-0.2 m ตัดมุม 0.01-0.03 m
  ช่องสำรองด้าน +x 0.8-1.2 m ขอบยื่นแกน x 0.14 m ทั้งสองปลาย (สำรองไว้สำหรับแนว
  สัมผัสพื้นและที่นั่งเพลา) ทั้งหมดสุ่มจาก seed
- interface ชนิด v2 ต่อที่ระดับ manifest มวลและจุดศูนย์กลางของ assembly คำนวณใหม่
  ด้วยเลขคณิตของ `part_tree.roll_up` (ทดสอบแล้วว่าเท่ากัน)
- หลักฐานที่ออกแล้ว: `load_structure: {members: [m0-load_structure.deck]}`

## การตรวจสอบ

| คำสั่ง | Exit | ผลลัพธ์ |
|---|---|---|
| `python -m unittest tests.test_hierarchy_mechanisms -v` | 0 | `Ran 10 tests`, `OK` |
| `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed 11 --out artifacts/work160/seed11` | 0 | 249 leaf, 248 interface, 25 s |
| `python scripts/hierarchy/evaluate_level0.py --manifest artifacts/work160/seed11/manifest.json --out artifacts/work160/l0.json` | 0 | `finished`, 9682.3 s, มวล 1766.2 kg |
| `python -m unittest test_functional_composition` (ใน `auto-loop/acceptance`) | 1 | 28 การทดสอบ ล้มเหลวเฉพาะ B1-B9 (ชุดคีย์) |
| `pwsh -NoProfile -File auto-loop/verify.ps1` | 3 | Gate 1 PASS; Gate 2 `Ran 1140 tests`, `OK (skipped=11)`; Gate 3 `Ran 41`, `FAILED (failures=9)`: เฉพาะ B1-B9 |

## ข้อจำกัด

- แผ่นพื้นหนัก: มวลรากของ seed 11 เพิ่มจาก 528 kg เป็น 1766 kg (แผ่นพื้นราว 1240 kg
  ด้วยความหนาแน่นของแคตตาล็อกสังเคราะห์) Level-0 ยังจบการแข่ง การเจาะรูลดน้ำหนักหรือ
  แผ่นพื้นที่บางลงเป็นงานต่อได้
- ไม่ได้แสดงว่าแผ่นพื้นรับภาระได้ ที่นั่งเป็นเพียงการสัมผัสเชิงตัวแทน
- B1-B9 ยังล้มเหลวเพราะชุดคีย์หลักฐานยังไม่ครบ

## งานต่อ

การสัมผัสพื้นและเบรกบนแนวขอบยื่นของแผ่นพื้น (ล้อที่มีรูเจาะหลายเหลี่ยมบนเพลานิ่ง
ที่นั่งบนหน้าข้างของแผ่นพื้น จานโรเตอร์หมุนร่วมกับล้อ สเตเตอร์บนด้านบนของเพลา)
แล้วจึงการบังคับเลี้ยว การส่งกำลัง ตัวแปลงพลังงาน ภาชนะ ตัวควบคุม และโมดูลระบาย
ความร้อนในช่องสำรอง
