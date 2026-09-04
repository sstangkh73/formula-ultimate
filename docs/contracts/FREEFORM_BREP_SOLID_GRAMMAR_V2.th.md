# Free-Form B-rep Solid Grammar V2

ไฟล์ต้นฉบับภาษาอังกฤษ: `FREEFORM_BREP_SOLID_GRAMMAR_V2.md`

## จุดประสงค์และ authority

`freeform_brep_solid_grammar_v2` คือภาษา Work 092 แบบ bounded สำหรับเปลี่ยน exact Work 091 profile ร่วมกับ path และ feature ancestry ที่ประกาศให้เป็น OCCT B-rep solid Validator คือ `src/formula_ultimate/components/freeform_solid_grammar.py`; CadQuery executor คือ `scripts/cad/generate_freeform_solid_corpus.py`; พยาน STEP อิสระคือ `scripts/cad/inspect_freeform_solid_corpus_freecad.py`; และ corpus ที่รับคือ `config/cad/freeform_brep_solid_grammar_v2.json`

การผ่านหมายถึง geometry execute ได้, body count ตรงกับที่ประกาศ exact, คงอยู่ผ่าน STEP, การวัดอิสระอยู่ในขอบเขต, recover datum ได้ และ replay deterministic สำหรับ corpus นี้ ไม่ใช่ manufacturing, load, fatigue, flow, thermal, race หรือ physical validation และไม่ใช่ topology discovery

## Typed feature DAG

ทุก candidate ประกาศ `candidate_id`, coverage `family` ที่ไม่บังคับรูปทรง, `expected_body_count` แบบ exact, `features` ตามลำดับ, `final_feature_id` และ derived datums Feature มี stable ID, operator, input ที่มาก่อน และ exact parameters Unknown field/operator, forward reference, input kind ไม่เข้ากัน, Work 091 profile หาย, ค่า non-finite, dimension เกินขอบเขต, path ยาวศูนย์, body count ผิด หรือ datum kind บังคับไม่ครบ ต้อง fail ก่อนเข้า CAD

Source declaration ของ Work 091 ถูก pin ด้วย SHA-256 Section อ้างถึง profile เหล่านั้นและใช้ bounded scale, local `z` rotation และ 3D translation ได้ Path เป็น polyline หรือ spline ที่ประกาศ Length ใช้ metre และ angle ใช้ radian ที่ contract boundary แล้ว executor แปลงครั้งเดียวเป็น millimetre/degree ของ kernel

## Operator ที่รับ

- Construction: `section`, `path`, `extrude` พร้อม taper, `revolve` รอบ arbitrary axis, curved/straight `sweep` และ multi-section `loft`
- Modification: `shell` ที่ใช้ geometry signature, `rib_web`, `gusset`, `pocket`, `bore`, `linear_pattern` แบบ fused หรือ explicit body, `fillet` และ `chamfer` ที่เลือกด้วย signature
- Composition: `boolean_union`, `boolean_subtract`, `boolean_intersect` และ deterministic `transform`

ห้าม raw edge number Fillet/chamfer เลือก line edge ที่ขนาน local axis ที่ประกาศและ fail เมื่อ signature ไม่พบสิ่งใด Shell เลือก geometry-extreme face และปฏิเสธ thickness ที่เท่ากับหรือเกินครึ่ง minimum body span ก่อน kernel สร้างผลที่ไม่ตั้งใจ Geometry ระหว่างทางที่ empty/invalid/non-finite ต้อง fail Solid count สุดท้ายต้องเท่ากับ `expected_body_count`; ไม่มีการ fuse disconnected body แบบเงียบ

## Datum และพยานอิสระ

ทุก candidate ประกาศ geometry-derived datum ที่ recover ได้สาม kind: bounding-box centre, longest bounding-box axis และ plane min/max ที่ประกาศบน `x`, `y` หรือ `z` CadQuery วัดจาก geometry-derived optimal box FreeCAD import exact canonical STEP อย่างอิสระและคำนวณ datum เดิมใหม่ด้วย `optimalBoundingBox(False, False)` Datum identity/kind/direction และ coordinate ทั้งหมดถูกเทียบภายใน `1e-7 m`; จำนวน face/edge/solid ต้อง exact

การเทียบ volume/surface area ใช้ relative tolerance แบบ capped `0.002` ซึ่งเป็น allowance สำหรับการวัดข้าม kernel เท่านั้น ไม่ repair shape, เปลี่ยน topology หรือผ่อน body validity ค่า `hidden_geometry_repair` เป็น `false` เสมอ

## Corpus ที่รับและ replay

Corpus 10 candidates ครอบคลุม operator ที่รับทั้ง 18 ตัว ผ่าน curved branch, tapered hollow duct, lofted rotary member, organic-like swept bridge, variable-section shell, tapered open shell, rib/gusset hybrid, bored/chamfered hub, fused/filleted pattern และ revolved intersection แบบสี่ body ที่ประกาศ Family label เป็น coverage label ไม่ใช่รูปทรงชิ้นส่วนรถที่บังคับ

รัน clean witness สองรอบด้วย:

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_freeform_solid_corpus.py `
  --config config\cad\freeform_brep_solid_grammar_v2.json `
  --wire-config config\cad\freeform_wire_grammar_v2.json `
  --output-root artifacts\work092\run_g `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe"

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_freeform_solid_corpus.py `
  --config config\cad\freeform_brep_solid_grammar_v2.json `
  --wire-config config\cad\freeform_wire_grammar_v2.json `
  --output-root artifacts\work092\run_h `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe" `
  --replay-reference artifacts\work092\run_g\result.json
```

Normalize เฉพาะ STEP `FILE_NAME` timestamp Replay บังคับ result equality ทั้งชุด รวม STEP SHA-256 ทุกไฟล์, manifest และ independent FreeCAD report identity

## ข้อจำกัด

V2 ยังไม่มี general NURBS knot/weight, guide surface, persistent STEP product metadata, arbitrary topology-aware selector, local thickness field, lattice/mesh substitution, manufacturing construction, load, meshing หรือ simulation Datum recovery ตั้งใจจำกัดที่ bounding geometry และยังไม่ระบุ arbitrary interface surface; Work 096 รับผิดชอบ semantic witness ที่เข้มกว่า Work 093 จะเพิ่ม topology genome แต่ Work 092 เพียงลำพังพิสูจน์เฉพาะภาษา shape ที่ execute ได้หลากหลายขึ้น
