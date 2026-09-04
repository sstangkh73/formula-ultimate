# แผน Work 091: Constrained Free-Form Sketch and Wire Grammar V2

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_091_constrained-freeform-wire-grammar-v2-plan.md`

## สถานะ

สถานะ: Completed

## วัตถุประสงค์

Implement grammar ของ 2D wire สำหรับ agent แบบ bounded เพื่อเอาคอขวด profile สี่แบบที่ Work 090 วัดได้ออก Grammar ต้อง execute geometry จริงแบบ line, polyline, tangent arc, three-point arc, circle, ellipse, quadratic/cubic Bezier และ B-spline ที่จำกัด degree รองรับหลาย loop/hole, deterministic trim/offset และ local transform พร้อมปฏิเสธ profile ที่กำกวมหรือ invalid ก่อน Work 092 นำไปสร้าง solid

รุ่นแรกยอมรับเฉพาะ geometry ที่กำหนดครบและ validate geometric constraint ที่ประกาศ โดยตั้งใจปฏิเสธ sketch ที่ underconstrained แทนการใช้ iterative sketch solver ที่ไม่ deterministic

## ขอบเขตและไฟล์ที่วางแผน

- `config/cad/freeform_wire_grammar_v2.json`
- `src/formula_ultimate/components/freeform_wire_grammar.py`
- `scripts/cad/generate_freeform_wire_corpus.py`
- `scripts/cad/inspect_freeform_wire_corpus_freecad.py`
- `tests/test_freeform_wire_grammar.py`
- `docs/contracts/FREEFORM_WIRE_GRAMMAR_V2.md` และไฟล์ภาษาไทยคู่กัน
- แผน/ผลนี้และไฟล์ภาษาไทยคู่กัน
- หลักฐาน STEP/manifest/FreeCAD witness ที่ ignore ใต้ `artifacts/work091/`

## ตัวแปรต้น/ตามและตัวควบคุม

- Input อิสระ: profile family, segment operator/control point ตามลำดับ, loop/role, transform list, trim fraction, offset distance/kind, constraint, ขอบเขต SI และนโยบาย tolerance
- Output ตาม: closed-wire validity, จำนวน edge/wire, planar area, perimeter, bounds, operator coverage, จำนวน curved edge, STEP identity, FreeCAD witness และ replay equality
- Negative control: open loop, self-intersection, segment/loop identity ซ้ำ, zero-length segment, arc/tangent ผิด, degree/control-point mismatch, hole nesting ผิด, offset มากเกิน/ต่ำกว่า tolerance, ค่าที่ไม่ finite, operator ไม่รองรับ, constraint fail และ unknown field
- Metamorphic control: การสลับลำดับ declaration key ต้องคง identity; control-point mutation ต้องเปลี่ยน declaration และ STEP identity

## การตรวจสอบและเกณฑ์สำเร็จ

- มี profile อย่างน้อยสิบสองแบบจากอย่างน้อยหก family
- Operator family ที่ประกาศทั้งหมดต้อง execute เชิงสาเหตุใน corpus รวมตัวอย่าง trim/offset ที่ไม่เป็นศูนย์
- ทุก profile ต้องเป็น planar face พื้นที่บวกหนึ่งหน้า มี outer loop ปิดและ hole loop ศูนย์หรือมากกว่าที่ซ้อนถูกต้อง
- CadQuery และ FreeCAD inspection อิสระต้องตรงกันด้านจำนวน wire/edge, bounds, area และ perimeter ภายใน tolerance ที่ประกาศ
- Output root สะอาดสองชุดต้องสร้าง canonical STEP, manifest และ result identity เหมือนกัน
- Focused test, repository-contract test, compilation และ full regression ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

Endpoint continuity ของ B-spline/Bezier, topology หลัง offset, ลำดับ edge ใน STEP และความไวต่อ tolerance อาจทำให้ profile ที่ดูง่าย invalid ผลเหล่านี้ต้องปรากฏชัดและห้าม hidden healing งานนี้สร้างความสามารถ planar profile/wire เท่านั้น ไม่สร้าง 3D solid, loft/sweep part, topology mutation, physical evaluation, manufacturing admission หรือ discovery
