# Constrained Free-Form Wire Grammar V2

ไฟล์ต้นฉบับภาษาอังกฤษ: `FREEFORM_WIRE_GRAMMAR_V2.md`

## จุดประสงค์และขอบเขตคำอ้าง

`constrained_freeform_wire_grammar_v2` คือภาษาที่ bounded และ deterministic สำหรับ profile ระนาบที่ agent สร้างในหน่วย SI metre และ radian ตัวตรวจ declaration คือ `src/formula_ultimate/components/freeform_wire_grammar.py`, executor CadQuery คือ `scripts/cad/generate_freeform_wire_corpus.py`, พยาน STEP อิสระคือ `scripts/cad/inspect_freeform_wire_corpus_freecad.py` และ corpus ที่รับคือ `config/cad/freeform_wire_grammar_v2.json`

การผ่าน contract นี้ยืนยันเพียงว่า declaration ที่ระบุสร้าง face ระนาบปิดและ valid ใน CAD kernel ที่ pin, ผ่าน constraint ทาง geometry ที่ประกาศ, ผ่านการถ่ายโอน STEP และ replay ได้แบบ deterministic เท่านั้น ไม่ใช่หลักฐานว่าเป็นชิ้นส่วนรถที่มีประโยชน์, เป็น 3D solid, ผลิตได้ด้วยวัสดุ/กระบวนการจริง, รับแรงได้, ประกอบเข้ากันได้, มีประโยชน์ทาง aero, ปลอดภัยทาง thermal หรือผ่าน physical validation

## Declaration แบบ exact และขอบเขต

Root มีเฉพาะ `grammar_version`, `units`, `limits` และ `profiles` Profile แต่ละตัวประกาศ identity, family label ที่ไม่บังคับรูปทรง, loop ตามลำดับ, transform ตามลำดับ, นโยบาย offset หนึ่งชุด และ constraint ทาง geometry ต้องมี `outer` loop ตัวแรกหนึ่งตัวพอดี และอาจมี `hole` loop แบบ bounded ทุก loop/segment มี identity คงที่ Unknown field, unit, operator, identity ผิดรูปแบบ, ตัวเลข non-finite, coordinate เกินขอบเขต, จำนวน segment/point/loop เกินขอบเขต หรือ endpoint ไม่ปิด ต้อง fail closed

V2 รับเฉพาะ geometry ที่กำหนดครบ ไม่มี iterative constraint solver และไม่อนุมาน dimension, tangency, closure หรือ topology ที่หายไป Length ใช้ metre ที่ contract boundary และแปลงหนึ่งครั้งเป็น convention millimetre ของ CAD kernel ส่วน angle ใช้ radian

ขอบเขตที่ประกาศคือ:

- tolerance แบบ absolute สำหรับ closure และ bounding box: `1e-7 m`
- tolerance แบบ relative สำหรับการวัด area/perimeter อิสระ: `0.002` (`0.2%`)
- minimum feature: `1e-5 m`
- absolute coordinate สูงสุด: `1.0 m`
- absolute offset สูงสุด: `0.02 m`
- ไม่เกิน 32 points ต่อ segment, 16 segments ต่อ loop และ 4 loops ต่อ profile

Tolerance `0.2%` ใช้เฉพาะเป็นขอบเขต interoperability ของ algorithm วัด length/area ระหว่าง CadQuery กับ FreeCAD ไม่ลดความเข้มของ wire closure, hole nesting, bounding box, validity หรือ topology และไม่ทำ repair Corpus ที่ผ่านจะบันทึก residual สูงสุดจริง

## Segment operator

| Operator | Behavior ของ V2 |
|---|---|
| `line` | Edge เดียวจาก start ถึง end ที่ finite; trim parameter ที่ไม่ trivial รับเฉพาะ operator นี้ |
| `polyline` | จุดตามลำดับที่ปิดอย่างชัดเจน ไม่มี edge ศูนย์/ต่ำกว่า tolerance หรือ proper self-intersection |
| `tangent_arc` | Arc จาก start, tangent vector ที่ไม่เป็นศูนย์ และ end ที่ประกาศ |
| `three_point_arc` | Arc ผ่าน start, จุดกลาง และ end ที่ไม่ collinear |
| `circle` | Circle ปิดจาก centre และ radius บวก |
| `ellipse` | Ellipse ปิดจาก centre, radius บวกสองค่า และ rotation |
| `bezier` | Quadratic/cubic Bezier จาก control point สามหรือสี่จุดพอดี |
| `bspline` | Degree `2..5`, รายการ control point แบบ bounded และ periodic flag ชัดเจน |

Closed primitive และ periodic spline ต้องเป็น segment เดียวของ loop Segment อื่นต้องชนกันตามลำดับ declaration ภายใน `1e-7 m` รวมรอยต่อสุดท้ายกลับจุดแรก

## Transform, offset และ constraint

Transform execute ตามลำดับที่ประกาศ: translate ด้วยเวกเตอร์ SI 2D, rotate รอบ local origin และ mirror รอบ local `x` หรือ `y` ระยะ offset ถูก bounded และใช้ behavior ของจุดต่อแบบ `arc`, `intersection` หรือ `tangent` อย่างชัดเจน V2 ปฏิเสธ offset ที่เปลี่ยน topology จาก wire เดียวที่คาดไว้

ทุก profile ต้องประกาศอย่างน้อยหนึ่งชนิดจาก `positive_area`, `minimum_perimeter`, `hole_count` หรือ `symmetric_axis` Executor สร้าง hole แต่ละวงเป็น face อิสระ, พิสูจน์ว่าอยู่ภายใน outer face ทั้งหมด, ปฏิเสธ hole ที่ทับกัน แล้วจึงสร้าง face พื้นที่บวกหนึ่งหน้า ระบบไม่ย้าย, หด, heal หรือตัด hole ทิ้งเพื่อให้ geometry valid

## Corpus และหลักฐาน

Corpus ที่รับมี 12 profiles จาก 9 family labels และครอบคลุม segment operator ทั้งแปด, transform ทั้งสาม, constraint ทั้งสี่, trim ที่ไม่ trivial หนึ่งตัว, polygon offset ที่ไม่เป็นศูนย์หนึ่งตัว, profile โค้ง และ annulus อย่างเป็นเหตุเป็นผล Output แต่ละตัวบันทึกจำนวน face/wire/edge, จำนวน curved edge, area, perimeter, geometry-derived optimal bounds และ SHA-256 ของ canonical STEP แบบ exact

FreeCAD import STEP แบบ exact ทุกไฟล์ ตรวจ file identity/validity และเขียนพยาน `.FCStd` ความสอดคล้องของ topology face/wire/edge ต้อง exact; bounds ใช้ strict absolute tolerance; area/perimeter ใช้ relative interoperability tolerance ที่ประกาศ ห้ามใช้ bounds จาก display triangulation: FreeCAD ใช้ `optimalBoundingBox(False, False)` เพื่อให้ตรงกับการคำนวณจาก geometry ของ CadQuery

รันและ replay ด้วย:

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\cad\generate_freeform_wire_corpus.py `
  --config config\cad\freeform_wire_grammar_v2.json `
  --output-root artifacts\work091\run_d `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe"

& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\cad\generate_freeform_wire_corpus.py `
  --config config\cad\freeform_wire_grammar_v2.json `
  --output-root artifacts\work091\run_e `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe" `
  --replay-reference artifacts\work091\run_d\result.json
```

Output root ต้องยังไม่มีหรือว่าง ระบบ normalize เฉพาะ timestamp ของ STEP เป็น `1970-01-01T00:00:00`; geometry และเนื้อหา STEP อื่นไม่เปลี่ยน Replay บังคับ result equality ทั้งชุด จึงรวม declaration, manifest, independent witness และ STEP identity ทุกไฟล์ที่เหมือนกัน

## ข้อจำกัดและงานถัดไป

Grammar นี้ตั้งใจให้เป็น 2D และ bounded ยังไม่รองรับ NURBS knot/weight vector ทั่วไป, dimensional constraint จาก solver, surface patch, loft, sweep, guide rail, variable section, shell/thickness field, topology mutation หรือ semantic interface Family label เป็น label สำหรับ coverage ไม่ใช่ข้อบังคับชิ้นส่วน conventional Work 092 อาจนำ profile เหล่านี้ไปสร้าง 3D loft/sweep แบบ constrained แต่ต้องเพิ่ม validity, self-intersection, thickness และ independent solid-witness gate ของตัวเอง
