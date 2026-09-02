# Parametric B-rep Feature Grammar V1

ต้นฉบับภาษาอังกฤษ: `PARAMETRIC_BREP_FEATURE_GRAMMAR_V1.md`

## จุดประสงค์และ authority

`parametric_brep_feature_grammar_v1` คือภาษาสำหรับ agent แบบ bounded เพื่อสร้าง B-rep solid ของ single part จริงในหน่วย SI Declaration validator คือ `src/formula_ultimate/components/brep_grammar.py`; executor CadQuery/OCCT ที่ pin คือ `scripts/cad/generate_brep_feature_corpus.py`; และ corpus ที่รับคือ `config/cad/brep_feature_grammar_v1.json`

การผ่าน contract นี้หมายถึงเฉพาะ declaration ที่ระบุมี bound, operator V1 ทุกตัว execute ใน corpus ที่ทดสอบ, final part ที่บังคับทุกตัวเป็น solid เดียว valid มี volume เป็นบวก และ canonical STEP replay คงที่ภายใต้ toolchain ที่ pin ไม่ใช่ material, manufacturing, structural, assembly, thermal หรือ physical validation

## Topology ของ declaration

Root บังคับเฉพาะ `grammar_version` และ `candidates` Candidate แต่ละตัวบังคับ `candidate_id`, `family` ที่รับได้หนึ่งค่า, `features` ตามลำดับ และ `final_feature_id` Feature แต่ละตัวบังคับเฉพาะ `feature_id`, `operator`, `inputs` และ `parameters` Input อ้างได้เฉพาะ feature ที่มาก่อน; sketch profile ใช้ input ศูนย์, boolean ใช้สอง และ operator อื่นใช้หนึ่ง

Family บังคับ 5 แบบคือ `shaft`, `bracket`, `hollow_housing`, `ribbed_plate` และ `hub_like_rotating_part` Operator identity ด้านล่างทุกตัวต้องปรากฏใน admitted corpus

## Operator V1

| Operator | Behavior แบบ bounded |
|---|---|
| `sketch_profile` | Rectangle, circle, annulus หรือ axial shaft-section profile บน convention local plane ที่ประกาศ |
| `extrude` | สร้าง solid ระยะบวกจาก rectangle/circle/annulus |
| `revolve` | หมุนมุมบวกไม่เกิน `2*pi`; V1 execute axial shaft section |
| `pocket_cut` | ตัดสี่เหลี่ยมบางส่วนแบบ bounded โดยห้ามลบหรือแยก blank |
| `through_hole` | ลบทรงกระบอกเต็มความสูงที่ derive จาก geometry |
| `stepped_bore` | Through bore และ counterbore ใหญ่กว่าแต่ตื้นกว่า |
| `shaft_shoulder` | Fuse ทรงกระบอก coaxial แบบ bounded เข้ากับ shaft |
| `rib_web` | Rib tool ทรงปริซึมแบบ bounded ใน part frame |
| `shell_wall` | ความหนาผนังคงที่เข้าด้านใน พร้อม top opening ที่ประกาศ |
| `linear_pattern` | Copy `2..64` รายการตามแกน `x`, `y` หรือ `z` |
| `circular_pattern` | Copy หมุน `2..64` รายการรอบ local `z` ภายในมุมบวกที่ประกาศ |
| `fillet_chamfer` | Fillet หรือ chamfer แบบ bounded บน edge selection ชนิด vertical/circular |
| `boolean_union` | OCCT union แบบ exact; ไม่ปิด gap โดยปริยาย |
| `boolean_subtract` | OCCT subtraction แบบ exact; ผล empty ต้อง fail |
| `boolean_intersect` | OCCT intersection แบบ exact; ผล empty ต้อง fail |

Length parameter ใช้ metre และแปลงหนึ่งครั้งเป็น convention kernel millimetre ของ CadQuery Angle ใช้ radian และ count เป็น integer ใน `[2, 64]` มิติที่เป็นบวกถูก bound ที่ `5 m`; coordinate ต้อง finite และ magnitude ไม่เกิน `5 m` Unknown field, parameter name, unit, profile, selector, direction, mode, operator, family หรือ ancestry ต้อง fail closed

## กติกา kernel state

Non-profile feature ที่ execute ทุกตัวต้องคืน OCCT shape ที่ valid, non-empty, finite และ volume เป็นบวก `Compound` ที่มี solid เดียวจะถูก unwrap เฉพาะ representation โดยไม่เปลี่ยน topology; หลาย solid จะไม่ถูก auto-fuse หรือ repair Final feature ของ candidate ต้องมี solid เดียว Boolean self-erasure และ disconnected pattern ที่ใช้เป็น final part เป็น negative control โดยตรง

Executor บันทึก feature ID/operator/status/solid count ทุกตัว แล้ว export exact final shape เป็น STEP จากนั้นแทนเฉพาะ timestamp ที่เปลี่ยนได้ใน `FILE_NAME` ด้วย `1970-01-01T00:00:00` และ hash exact bytes ระบบไม่ rename face, heal invalid solid, close gap, เปลี่ยน parameter หรือเลือก fallback feature

## Admitted corpus และ replay

Corpus exercise operator set แบบ causal ผ่าน:

- shaft จาก revolve พร้อม shoulder และ bounded edge treatment
- bracket จาก extrude พร้อม partial pocket, through hole และ chamfer
- cylindrical housing จาก extrude พร้อม inward shell และ stepped bore ที่เยื้องแกน
- plate จาก extrude พร้อม rib seed, linear pattern, union, subtract และ intersect
- annular hub พร้อม lug seed, circular pattern และ union

รัน witness สองชุดอิสระด้วย:

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\cad\generate_brep_feature_corpus.py `
  --config config\cad\brep_feature_grammar_v1.json `
  --output-root artifacts\work078\run_a\step `
  --manifest artifacts\work078\run_a\manifest.json
```

ทำซ้ำด้วย `run_b` แล้วเทียบ `manifest_sha256` และ `step_sha256` ทุกตัว Output path ไม่รวมใน canonical manifest payload และ STEP base filename เหมือนกัน

## ขอบเขตคำอ้างและข้อจำกัด

ชื่อ family V1 เป็น test fixture ไม่ใช่ architecture บังคับของรถในอนาคต Grammar ไม่บังคับ wheel count, suspension form, powertrain technology, body form หรือ known component shape และตั้งใจ bounded จึงยังไม่รองรับ freeform spline, loft/sweep, complex datum transform, arbitrary edge query, thread/gear, sheet-metal process history, composite, topology-optimization field หรือ persistent STEP semantic signature

CadQuery และ STEP export ใช้เทคโนโลยี OCCT ร่วมกัน ดังนั้น replay ที่สำเร็จเป็น toolchain evidence ไม่ใช่ geometric truth source อิสระ Work 079 จะเพิ่ม material/manufacturing contract และ Work 081 ต้องตรวจ exact STEP อย่างอิสระ พร้อม recover interface ด้วย geometry signature/datum แทน face number
