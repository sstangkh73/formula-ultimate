# เป้าหมายของลูป: การประกอบชิ้นส่วน free-form แบบลำดับชั้น v1

ฉบับภาษาอังกฤษ: `GOAL.md`

ไฟล์นี้ห้ามแก้ ถ้าถูกแก้ลูปจะหยุด กำหนดโดย Work 148

## สิ่งที่เจ้าของโครงการต้องการ

ระบบออกแบบชิ้นส่วนได้อิสระโดยไม่กำหนดรูปร่างไว้ก่อน ออกแบบตั้งแต่ชิ้นที่เล็กที่สุดขึ้นไปแล้วประกอบเข้าด้วยกัน
ชิ้นเล็กประกอบเป็นชุดย่อย ชุดย่อยประกอบเป็นระบบ ระบบประกอบเป็นรถ
เช่น ตัวแปลงพลังงานคล้ายเครื่องยนต์ก็จะมีห้อง ชิ้นที่เคลื่อนที่ ชิ้นจ่ายเชื้อเพลิง และตัวยึด
ต้องเป็นแบบนี้กับชิ้นส่วน**ทุกชิ้น**ของรถ ไม่ใช่เฉพาะตัวแปลงพลังงาน
ระบบ**ไม่จำเป็น**ต้องสร้างเครื่องยนต์แบบดั้งเดิมหรือรายการชิ้นส่วนแบบเดิมขึ้นมาใหม่
ไม่ว่าจะแยกส่วนแบบไหน ต้องเป็นการเลือกของระบบเอง และต้องวัดผลได้

## "เสร็จ" หมายถึง

`pwsh -NoProfile -File auto-loop/verify.ps1` exit 0 บน tree ที่สะอาดและ commit แล้ว

1. Gate 1: `scripts/validation/check_material_publication_boundary.py` ผ่าน
2. Gate 2: เทสต์ทั้ง repository `python -m unittest discover -s tests` ผ่าน
3. Gate 3: `python -m unittest discover -s auto-loop/acceptance` ผ่าน

## สัญญาที่ Gate 3 ตรวจ

entry point ที่รันด้วย CadQuery runtime ที่ pin ไว้

```text
.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_hierarchical_vehicle.py --seed S --out DIR
```

`DIR` อาจยังไม่มี generator สร้างเอง ต้อง exit 0 ภายใน 20 นาที และเขียน

- `DIR/manifest.json`
- STL mesh (binary หรือ ASCII) หนึ่งไฟล์ต่อชิ้นส่วน leaf หน่วยเป็น**เมตร**
  วางในพิกัดของรถ และอ้างถึงด้วย path แบบสัมพัทธ์ภายใน `DIR`

`manifest.json` มี top-level field ตามนี้เท่านั้น

| Field | ความหมาย |
|---|---|
| `design_language_version` | string ที่ไม่ว่าง |
| `seed` | จำนวนเต็มที่ส่งเข้ามา |
| `config_sha256` | hash แบบ hex 64 ตัวของ configuration ที่ใช้ |
| `git_commit` | `git rev-parse HEAD` ตอนรัน |
| `length_unit`, `mass_unit` | `"m"`, `"kg"` |
| `contact_tolerance_m` | `0 < tol <= 5e-4` |
| `root` | id ของ node assembly ที่เป็นตัวรถ |
| `nodes` | รายการ node ของ assembly และ part |
| `interfaces` | รายการรอยต่อระหว่างชิ้น leaf |

node แบบ assembly มี field `id, kind="assembly", children, functions, mass_kg,
center_of_mass_m` เท่านั้น node แบบ part มี `id, kind="part", mesh,
material_id, density_kg_m3, mass_kg, center_of_mass_m, generator` เท่านั้น โดย
`generator = {grammar_version, program, program_sha256}` และ `program_sha256`
คือ SHA-256 ของ JSON แบบ canonical (`sort_keys`, separators `(",", ":")`,
`ensure_ascii`, ไม่มี NaN) ของ `program`
interface มี `id, a, b, kind` และมี `interference_m` ได้ถ้าต้องการ
`a` และ `b` ต้องเป็นชิ้น leaf ส่วน `kind` เป็นหนึ่งใน `threaded, welded, bonded, interference, integral` (Work 140)
`interference_m` ใช้ได้กับ `interference` เท่านั้น และต้อง `0 < x <= 1e-4`

เกณฑ์การยอมรับ ตรวจจาก mesh อย่างอิสระ

1. **Replay** seed เดียวกันต้องได้ชุดไฟล์เหมือนกันทุก byte field metadata ถูกต้อง
   และ `git_commit` ตรงกับ HEAD
2. **ลำดับชั้น** มี root เดียว ทุก node มี parent ตัวเดียว ไม่มีวงวน และเข้าถึงได้ทุก node
   มีอย่างน้อย **4 ระดับ** และชิ้น leaf อย่างน้อย **150 ชิ้น** เส้นทแยงของ bounding box
   ของ leaf ที่ใหญ่ที่สุดต้องยาวอย่างน้อย **100 เท่า** ของชิ้นที่เล็กที่สุด
3. **ทุกหน้าที่** ความสามารถทั้งเก้าใน
   `formula_ultimate.topology.functional_vehicle.REQUIRED_CAPABILITIES`
   ต้องถูกระบุใน `functions` ของ assembly ที่ subtree สูงอย่างน้อย 2 และมี leaf อย่างน้อย 5 ชิ้น
4. **เรขาคณิตและมวล** mesh ของ leaf ทุกชิ้นปิดและหันทิศทางสม่ำเสมอ ปริมาตรเป็นบวก
   `mass_kg` ของ leaf เท่ากับปริมาตร mesh คูณ `density_kg_m3` ภายใน relative 1e-5
   จุดศูนย์กลางมวลคลาดไม่เกิน 1e-5 m มวลและจุดศูนย์กลางมวลของ assembly ต้องรวมขึ้นมาจากลูกได้ตรง
5. **Free form** leaf ที่กิน bounding box แนวแกนของตัวเองตั้งแต่ 99.9 % ขึ้นไป มีได้ไม่เกิน 25 %
   hash ของโปรแกรมของ leaf ทุกชิ้นต้องตรง
6. **Interface** ภายใน assembly ทุกตัว ลูกต้องเชื่อมกันผ่าน interface
   interface ทุกตัวต้องมีการสัมผัสของพื้นผิวที่วัดได้ภายใน `contact_tolerance_m`
   จุดที่สุ่มของ leaf หนึ่งต้องไม่อยู่ในอีกชิ้นลึกเกิน tolerance หรือเกิน `interference_m` ที่ประกาศ
7. **ไม่มี template ตายตัว** seed 11, 23 และ 37 ต้องได้โครงสร้างต้นไม้ต่างกันทุกคู่
   และทุกความสามารถต้องมีโครงสร้าง subtree อย่างน้อย 2 แบบในสาม seed นั้น

## ขอบเขตที่ลูปต้องเคารพ

- ใช้ `AGENTS.md` ทั้งหมด: หนึ่ง work item ที่มีเลขกำกับต่อรอบ, บันทึก plan/result สองภาษา,
  stage แบบระบุไฟล์, commit หลัง validation ผ่านเท่านั้น, หน่วย SI และมีเทสต์กับ model ใหม่ทุกตัว
- วัสดุมาจาก catalog เท่านั้น ไม่ออกแบบส่วนผสมใหม่ ค่าวัสดุจริงอยู่ใน `/private/` ที่อยู่ใน gitignore
  ห้าม commit และห้ามพิมพ์ลงในไฟล์ที่ track ค่าความหนาแน่นใน artifact ที่ generator สร้างใช้ได้
  เพราะ `artifacts/` อยู่ใน gitignore วัสดุ placeholder สังเคราะห์ต้องติดป้ายว่าสังเคราะห์
  และ `design_use_allowed=false`
- ใช้ของที่มีอยู่ซ้ำ ได้แก่ free-form grammar (`components/freeform_solid_grammar.py`,
  `scripts/cad/*`), ด่าน part-resolution และ joint (`assembly/part_resolution.py`)
  และคำศัพท์หน้าที่ (`topology/functional_vehicle.py`) ห้ามแทนด้วยของที่ไม่เกี่ยวกัน
- ห้าม hard-code ชื่อชิ้นส่วนแบบดั้งเดิมเป็นชิ้นส่วนบังคับ การแยกส่วนต้องมาจากขั้นตอน generative
  หรือ search ที่ประกาศไว้ ซึ่งขับเคลื่อนด้วย seed และข้อจำกัดที่ประกาศ

## การผ่าน "ไม่ได้" หมายความว่า

การผ่านคือ**ด่าน representation ของเรขาคณิตและการประกอบ** ไม่ใช่การยืนยันทางฟิสิกส์
ไม่ได้แสดงว่าชิ้นส่วนทำงานได้ รับแรงได้ ทนความร้อนได้ หรือทำให้รถเร็วขึ้น
และไม่ได้แสดงว่าการแยกส่วนนั้นมีประโยชน์ การเชื่อมลำดับชั้นเข้ากับ physics Level-0
และ race kernel เป็นเป้าหมายรอบหลัง

ข้อจำกัดของการตรวจที่รู้อยู่แล้ว

- การตรวจชิ้นทะลุกันสุ่มดูเฉพาะ vertex และจุดศูนย์กลางของสามเหลี่ยม การซ้อนทับแบบตัดผ่านบางกรณีจึงอาจหลุด
- สัดส่วนกล่องเป็นแค่ตัวแทนของ free form
- ความหลากหลายของโครงสร้างจากสาม seed ตัดกรณี template ตายตัวแบบเดียวได้
  แต่ไม่ได้วัดว่ามีประโยชน์หรือไม่

## Milestone ที่แนะนำ (ลูปเรียงใหม่ได้)

1. data model ของต้นไม้ชิ้นส่วนแบบ recursive พร้อม validation และเทสต์ (Python ล้วน ไม่ใช้ CAD)
2. ขั้นตอนแยกส่วนที่ขับเคลื่อนด้วย seed ครอบคลุมทั้งเก้าความสามารถ โดยไม่พึ่ง catalog ชิ้นส่วน
3. สร้างเรขาคณิตของ leaf ผ่าน free-form grammar ที่มีอยู่และ CadQuery
   export STL หน่วยเมตร และคำนวณมวลจาก mesh ที่ export ออกมา
4. วาง interface ให้เกิดการสัมผัสที่วัดได้โดยไม่ทะลุกัน
5. generator CLI, manifest และความ deterministic ของ replay (ปิด parallel boolean ของ CadQuery)
6. ขยายให้ได้อย่างน้อย 150 leaf และช่วงขนาดอย่างน้อย 100 เท่า แล้วผ่าน Gate 3 ครบทั้งสาม seed
