# ผล Work 006: Constrained 3D Component Grammar และวงจรหลักฐาน

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-25_006_constrained-component-grammar-result.md`

## ผลลัพธ์

Work 006 implement `mounting_plate_v1` และทำวงจร local แบบควบคุมสำเร็จ:

```text
constrained SI-unit JSON
  -> pre-CAD grammar gate
  -> CadQuery 2.8.0 B-rep
  -> STEP ที่มี hash
  -> FreeCAD 1.1.3 import และวัดอย่างอิสระ
  -> analytical/CadQuery/FreeCAD evidence gate
  -> มวล constant-density จาก FreeCAD
  -> longitudinal point-mass kernel ระดับ Level 0 ที่มีอยู่
```

Candidate valid ที่ประกาศล่วงหน้าทั้งสามตัวผ่าน Candidate invalid ตัวที่สี่
ถูกปฏิเสธก่อน CadQuery execute และ monotonic check ที่ประกาศล่วงหน้าทั้งสี่ผ่าน
ผลนี้รองรับเพียงความสอดคล้องของ local pipeline ไม่ใช่ physical validation
ของ component

## ไฟล์ที่เปลี่ยน

### Grammar และสัญญา Level 0

- `src/formula_ultimate/components/grammar.py`
  - กำหนด `mounting_plate_v1`, `Material`, `MountingPlateSpec`, analytical
    volume, symmetric mounting port และ error `GrammarViolation` ที่สังเกตได้;
  - บังคับ dimension bound, finite value, schema/version identity, minimum edge
    ligament, minimum hole-to-hole web และ minimum central-cut web ก่อนเรียก CAD
- `src/formula_ultimate/components/__init__.py`
  - export public grammar type
- `src/formula_ultimate/experiments/cad_level0.py`
  - กำหนดสัญญา independent-CAD measurement และ Level 0 control แบบเข้มงวด;
  - ปฏิเสธ topology ผิด, non-finite value, type/vector ผิด, bounding-box
    ไม่ตรง และ volume residual เกินกำหนด;
  - สร้าง component mass จาก measurement volume ที่ผ่าน gate เท่านั้น
- `src/formula_ultimate/experiments/__init__.py`
  - export CAD-to-Level-0 evidence API

### Configuration และวงจรที่ execute ได้

- `config/work006_mounting_plate.json`
  - บันทึก experiment ID, grammar version, seed `6001`, สมมติฐาน aluminium
    constant density `2700 kg/m^3`, geometry ร่วม, candidate, Level 0 control
    และ tolerance
- `scripts/cad/generate_mounting_plate.py`
  - validate candidate ที่ประกาศหนึ่งตัว สร้าง CadQuery solid หนึ่งชิ้น export
    STEP และบันทึก CadQuery measurement, tool version, size, header และ SHA-256;
  - เขียน pre-CAD failure evidence และคืน exit code `2` เมื่อ grammar ปฏิเสธ
- `scripts/cad/inspect_step_freecad.py`
  - รันด้วย bundled Python ของ FreeCAD, import STEP exact และรายงาน FreeCAD
    version, hash, validity, solid count, volume, bound และ centre of mass
- `scripts/cad/aggregate_work006.py`
  - ตรวจ identity/hash, gate หลักฐาน analytical/CadQuery/FreeCAD, ป้อน volume
    จาก FreeCAD เข้า Level 0, ตรวจสมมติฐานควบคุม และเขียน replay summary
- `scripts/run_work006.ps1`
  - ทำลำดับ local ทั้งหมดและปฏิเสธ evidence ที่หาย แม้ external process
    จะคืน success

### Test และเอกสาร

- `tests/test_component_grammar.py`
  - ทดสอบ valid production, mapping round-trip, version/schema rejection,
    finite/range gate, material constraint, ligament/web rule ที่ implement
    ทั้งหมด และ monotonic analytical volume
- `tests/test_cad_level0.py`
  - ทดสอบ measurement admission, มวลจาก FreeCAD, analytical Level 0 outcome,
    malformed evidence, topology/validity failure, volume disagreement, bounds
    disagreement และ invalid control
- `docs/3d/CONSTRAINED_COMPONENT_GRAMMAR.md`
- `docs/3d/CONSTRAINED_COMPONENT_GRAMMAR.th.md`
  - นิยาม production, หน่วย SI, พิกัด, constraint, equation, evidence loop,
    experiment, คำสั่งรัน และขอบเขตข้ออ้าง
- plan/result record Work 006 ที่ตรงกัน แยกภาษาอังกฤษและไทย

หลักฐาน generated ถูก Git ignore โดยเจตนาใต้ `artifacts/work006/`

## การตัดสินใจสำคัญ

1. **จำกัด version 1 ให้แคบ** Production มีเพียง rounded prismatic plate,
   fixed-interface hole สี่รู, optional circular centre cut และ density
   ที่ประกาศหนึ่งค่า ไม่มี arbitrary generated Python หรือ free topology
   เข้าสู่ grammar
2. **ใช้ SI ที่ domain boundary** แปลงเป็น millimetre เฉพาะใน CadQuery adapter
   และแปลง CAD output กลับ SI ก่อน admission
3. **ใช้ imported volume อิสระสำหรับ Level 0** Analytical volume และ CadQuery
   volume เป็น gate ส่วน component mass ที่ Level 0 ใช้คือ
   `FreeCAD STEP volume * declared density` เท่านั้น
4. **ทำให้ failure สังเกตได้** ไม่มี parameter clipping, silent topology repair
   หรือ analytical substitution เมื่อ CAD evidence หาย
5. **ถือ mounting pattern เป็น interface geometry** Port สี่จุดคงความสมมาตร
   และถูกควบคุม ขณะที่เปลี่ยนเฉพาะ centre-cut radius
6. **ใช้ bundled Python runtime ของ FreeCAD** ใน build 1.1.3 ที่ติดตั้ง
   `FreeCADCmd` คืน exit code `0` ทั้งที่ไม่ execute input `.py` หรือ `.FCMacro`
   ที่ stage ไว้ ส่วน `bin/python.exe` import FreeCAD/Part เดียวกัน, execute
   ได้แน่นอน, รองรับ path ที่มีช่องว่าง และให้ process exit code ที่เชื่อถือได้
7. **ต้องมี output evidence file นอกจาก exit code `0`** กฎนี้กัน false-success
   ของ `FreeCADCmd` ที่พบไม่ให้ผ่านวงจรโดยตรง

## การทดลองแบบควบคุม

### ตัวแปรและตัวควบคุม

- ตัวแปรอิสระ: `lightening_radius_m = 0, 0.025, 0.040`
- ตัวแปรตาม: CAD volume/residual, มวลจาก density, final speed ระดับ Level 0
  และ final distance ระดับ Level 0
- ตัวควบคุม: dimension อื่นทุกค่า, mounting port สี่จุด, material density,
  seed, software route, base vehicle mass `300 kg`, traction `1200 N`, duration
  `5 s` และ timestep `0.05 s`
- Negative case: radius `0.055 m` ซึ่งต้องละเมิด minimum outer-edge ligament
  `0.006 m` ก่อน CAD

### หลักฐานสุดท้าย

| Candidate | FreeCAD volume (`m^3`) | CQ-to-FreeCAD residual (`m^3`) | Analytical relative residual | Mass (`kg`) | Final speed (`m/s`) | Final distance (`m`) |
|---|---:|---:|---:|---:|---:|---:|
| `solid_reference` | `0.00018970477868423448` | `5.9631119486702744e-19` | `3.2862443081460257e-15` | `0.51220290244743305` | `19.965911340870651` | `49.914778352176597` |
| `relief_25mm` | `0.00017399681541628494` | `5.4210108624275222e-20` | `3.1155805061476737e-16` | `0.46979140162396932` | `19.968729541866246` | `49.921823854665597` |
| `relief_40mm` | `0.00014949239271828358` | `-9.2157184661267877e-19` | `6.3459878036240901e-15` | `0.40362946033936564` | `19.973127524386776` | `49.932818810966978` |

Imported bounding box ทุกตัวเท่ากับ `0.2 x 0.12 x 0.008 m` ที่ precision
ที่บันทึก และ FreeCAD รายงาน valid solid หนึ่งชิ้นสำหรับ STEP ทุกไฟล์

หลักฐาน STEP สุดท้ายจากรอบที่บันทึกคือ:

| Candidate | Bytes | SHA-256 |
|---|---:|---|
| `solid_reference` | `50828` | `0BDDBDC39F0FEF749B158B7033EF7DA684BEAB5E623492442BCACB1101162936` |
| `relief_25mm` | `55774` | `EB635ECDA1F22CABDC8F906853C1AE3862F025E8BB8503CF2090EC69EB28B909` |
| `relief_40mm` | `55770` | `341A69FBD8DA42C3352AF53DAF7F78C7CC59C0E92F8120FDA01614301FFD0A4D` |

หลักฐาน invalid คือ:

```text
candidate_id: invalid_relief_55mm
stage: grammar_validation_before_cad
cadquery_executed: false
error_type: GrammarViolation
message: lightening cut violates the minimum outer-edge ligament
generator exit code: 2 (expected)
```

Monotonic check ทั้งหมดเป็น `true`:

- FreeCAD volume ลดลงอย่าง strict;
- component mass ลดลงอย่าง strict;
- final speed ระดับ Level 0 เพิ่มขึ้นอย่าง strict;
- final distance ระดับ Level 0 เพิ่มขึ้นอย่าง strict

### การทบทวนเพื่อพยายามหักล้าง

- หลักฐานสนับสนุน: candidate valid สามตัวผ่าน analytical, CadQuery และ FreeCAD
  gate; FreeCAD วัด exact STEP hash; controlled trend ผ่าน; deliberate invalid
  candidate ถูกปฏิเสธที่ boundary ที่ตั้งใจ
- หลักฐานขัดแย้ง: ไม่มีภายใน metric ที่ประกาศล่วงหน้าของ Work 006
- คำอธิบายทางเลือก: Level 0 trend เป็นผลจาก point-mass equation ที่ประกาศไว้
  แล้วและไม่ได้บอกว่าการเอาเนื้อออกมีประโยชน์เชิงโครงสร้างหรือไม่; CadQuery
  และ FreeCAD ต่างพึ่งพา geometry ตระกูล OCCT
- หลักฐานที่ขาด: load, boundary condition, material allowable, FEA,
  convergence, fatigue, joint, manufacturing, assembly, collision, uncertainty
  และ empirical measurement
- Confidence: สูงสำหรับ local pipeline run นี้; ไม่มีสำหรับ physical suitability

## Replay Metadata และ Artifact

- Repository commit ที่มีอยู่ระหว่างรัน:
  `f59879976f5cd56b57de7532ec6748c2da71d0ee`
- Worktree dirty ระหว่างรัน: `true` เพราะ Work 006 เองยังไม่ commit
- Seed: `6001`
- CadQuery: `2.8.0`
- FreeCAD: `1.1.3`
- Config SHA-256:
  `0EBE4E9CBBC99AFCFFD3237817CAB2B9C50ABE73139EA6438C40B89A2D86A6F4`
- Final summary:
  `artifacts/work006/experiment_summary.json`
- Final summary SHA-256:
  `23563ABBCC232E5A08C47798A514FDE27833EDFFF5D0030D5FC484AF69AA769F`

เนื่องจากรันใน dirty worktree ตัว summary จึงบันทึก SHA-256 exact ของ source
surface ที่ execute ด้วย:

| Source | SHA-256 |
|---|---|
| `src/formula_ultimate/components/grammar.py` | `8DDDFECDB6F4934BBFBA1A8E618F8D65242AF49BD62005280DA8EDBD94B7482E` |
| `src/formula_ultimate/experiments/cad_level0.py` | `D65CD624D9CA4BDB5962529CA55A96355AF859E6B4ED943D451481301D35FACD` |
| `scripts/cad/generate_mounting_plate.py` | `1302445A9B6F1E0568795105188D01D93E586289EFC5CF2072A93831B8AE79B4` |
| `scripts/cad/inspect_step_freecad.py` | `8B036B0512E233C770A3C33373E2AD28851E9B610B50BB6A78609189CAE62DED` |
| `scripts/cad/aggregate_work006.py` | `D98C1DD9883C857265F57AB8BDF9F9DDEE0EA42383B729FA0E1C6158B4F7A100` |
| `scripts/run_work006.ps1` | `C214EE1A544AF737636F9CA3046B7B57DAB9EDCDEFC9531A999835144B0C4F5F` |

STEP hash ยืนยัน exchange artifact หนึ่งรอบที่บันทึก แต่ไม่คาดว่าจะเหมือนกันทุก
byte ข้ามการรัน เพราะ STEP exporter เขียน run metadata เช่น timestamp ดังนั้น
deterministic replay ตัดสินจาก input ที่ประกาศ, valid topology, dimension
และ physical property ที่วัดได้ภายใน tolerance ไม่ใช่ STEP serialization
ที่ byte-identical

## คำสั่งตรวจสอบและผลแบบ Exact

### Final combined validation

คำสั่ง:

```powershell
py -3.14 -m unittest discover -s tests -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work006.ps1
py -3.14 -m compileall -q src scripts tests
git diff --check
```

Exit status: `0` ทุกคำสั่ง

Output ที่เกี่ยวข้อง:

```text
Ran 32 tests in 0.159s
OK
candidate_count: 3
status: passed
component_mass_strictly_decreases: true
freecad_volume_strictly_decreases: true
level0_final_distance_strictly_increases: true
level0_final_speed_strictly_increases: true
```

`compileall` และ `git diff --check` ไม่มี error Git แสดงเพียง Windows line-ending
warning ที่มีอยู่สำหรับไฟล์ `__init__.py` ที่แก้สองไฟล์

### Failed attempt ที่เกี่ยวข้องและเก็บเป็นหลักฐาน

1. Focused unit run แรกคืน exit code `1` เพราะ test ใช้ pitch `0.020 m` ขณะที่
   required pitch ที่คำนวณคือเพียง `0.018 m` จึงแก้ test เป็น `0.015 m`
   โดย rule implementation ไม่เปลี่ยน
2. Full-loop attempt แรกที่ใช้ `FreeCADCmd` คืน overall exit code `1` FreeCAD
   พิมพ์ `Unknown extension` สำหรับ path แบบ 8.3 ที่ลงท้าย `.PY` แต่ process
   FreeCAD เองคืน `0` และไม่มี measurement file
3. การ stage path `.py` ตัวเล็กหรือ `.FCMacro` ยังไม่เกิด evidence ที่ execute
   บน build นี้ launcher จึงใช้ bundled Python ของ FreeCAD และตรวจ output file
   เพิ่มด้วย
4. Bundled-Python import ครั้งแรกคืน exit code `1` เพราะ top-level STEP compound
   ที่ import ไม่มี `CenterOfMass` adapter จึงบังคับว่าต้องมี solid เดียวก่อน
   และอ่าน `shape.Solids[0].CenterOfMass` โดยไม่มีการแทนหรือ repair ค่า CAD

## สิ่งที่ต่างจากแผน

- เพิ่ม `config/work006_mounting_plate.json` และ
  `scripts/cad/aggregate_work006.py` เพื่อให้ variable/control เป็น declarative
  และทดสอบ evidence admission แยกได้
- เปลี่ยนจากการเรียก `FreeCADCmd` ที่วางแผนไว้เป็น bundled Python ของ FreeCAD
  ที่ติดตั้ง หลังบันทึก false-success behavior ข้างต้น
- ไม่เพิ่มงาน Fusion หรือ community FreeCAD MCP

## ข้อจำกัด

- Level 0 ใช้เพียง added point mass ภายใต้ traction คงที่ ความต่าง speed/distance
  สอดคล้องทางคณิตศาสตร์แต่ไม่ใช่หลักฐาน lap time หรือ component performance
- Constant density `2700 kg/m^3` เป็นสมมติฐาน ไม่ใช่ material certificate
- กฎ ligament/web `0.006 m` ของ grammar เป็น syntax constraint ที่เลือกสำหรับ
  การทดลองนี้ ไม่ใช่ design allowable จาก stress
- CadQuery และ FreeCAD เป็นคนละโปรแกรม แต่ไม่ใช่ geometric kernel ที่อิสระ
  ในความหมายที่แข็งแรงที่สุด เพราะทั้งคู่ใช้เทคโนโลยีตระกูล OCCT
- ไม่รับประกัน STEP replay แบบ byte-identical
- ไม่ทำ simulation ระดับ Level 1/2/3 หรือ scientific validation

## งานต่อไป

1. เพิ่ม named load, attachment semantic, manufacturing process และ material
   allowable ก่อนถามคำถามเชิงโครงสร้าง
2. สร้าง work item แยกสำหรับ mesh generation, boundary-condition audit,
   solver convergence และ FEA baseline ที่พยายามหักล้าง preference เรื่อง
   lightening
3. เปรียบเทียบ fixed กับ free topology หลังทำ component library, constraint,
   seed, candidate evaluation และ measured compute budget ให้เท่ากันเท่านั้น
4. เก็บ solid plate ของ Work 006 เป็น fixed-topology geometry baseline;
   ห้ามถือว่า plate ที่เบาที่สุดถูก promote จนกว่าจะมีหลักฐานที่แข็งแรงขึ้น
