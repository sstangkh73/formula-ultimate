# แผน Work 092: Free-Form B-rep Solid Grammar V2

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_092_freeform-brep-solid-grammar-v2-plan.md`

## สถานะ

สถานะ: Completed

## วัตถุประสงค์

Implement solid grammar แบบ bounded และ deterministic ที่ใช้ planar profile ซึ่ง Work 091 รับแล้วร่วมกับ path/section 3D ที่ประกาศ เพื่อสร้าง OCCT B-rep solid จริงแทน mesh ที่ opaque หรือใช้ตกแต่ง Corpus ต้องแสดง non-primitive solid อย่างน้อยสิบแบบ รวม curved branch, tapered hollow duct, lofted rotary member, organic-like load bridge และ variable-section shell

การผ่าน Work 092 ยืนยันเฉพาะการ execute geometry และการคงอยู่หลัง STEP inspection อิสระ ไม่ยืนยัน topology search, manufacturing feasibility, structural adequacy, functional usefulness หรือ physical validation

## ขอบเขตและไฟล์ที่วางแผน

- `config/cad/freeform_brep_solid_grammar_v2.json`
- `src/formula_ultimate/components/freeform_solid_grammar.py`
- `src/formula_ultimate/components/__init__.py`
- `scripts/cad/generate_freeform_solid_corpus.py`
- `scripts/cad/inspect_freeform_solid_corpus_freecad.py`
- `tests/test_freeform_solid_grammar.py`
- `docs/contracts/FREEFORM_BREP_SOLID_GRAMMAR_V2.md` และไฟล์ภาษาไทยคู่กัน
- แผน/ผลนี้และไฟล์ภาษาไทยคู่กัน
- หลักฐาน STEP/manifest/FreeCAD/replay ที่ ignore ใต้ `artifacts/work092/`

## ตัวแปรต้นและตัวแปรตาม

- Input อิสระ: Work 091 profile identity, operator DAG, local axis/datum, section scale/rotation/translation, 3D path control point, มิติ wall/pocket/bore/rib, transform parameters, boolean ancestry และขอบเขต SI ที่ประกาศ
- Output ตาม: จำนวน solid/body/face/edge, validity, volume, area, centre of mass, bounds, หลักฐาน curved face, datum signature ที่ recover ได้, STEP identity, FreeCAD residual และ replay equality
- Control: simple extrude เป็น reference; invalid ancestry, profile หาย, ค่า non-finite/เกินขอบเขต, path ยาวศูนย์, loft section เข้ากันไม่ได้, shell ลบตัวเอง, union ไม่ต่อกัน, intersection/subtraction ว่าง, selector ไม่คงที่, multi-body declaration ผิด, datum ถูกเปลี่ยน และ unknown field ต้องเป็น failure
- Metamorphic control: ลำดับ declaration key ไม่เปลี่ยน identity; การเปลี่ยน section/path/control point ต้องเปลี่ยน genotype และ exported geometry identity

## ขอบเขต grammar และ execution

- รองรับ bounded extrude/revolve, straight/curved sweep, multi-section loft, taper/variable section, shell-by-boolean, rib/web, gusset, pocket, bore, local pattern, fillet/chamfer ที่เลือกด้วย signature, union/subtract/intersect, local transform และ derived datum point/axis/plane declaration
- Feature input อ้างได้เฉพาะ feature ที่มาก่อน ทุก operation ต้องเปิดเผยผล invalid, empty, disconnected, non-finite หรือ multi-solid เว้นแต่ declaration อนุญาต multi-body ชัดเจน
- Edge-treatment selector ต้องใช้ geometric signature และ deterministic tie-breaking; ห้าม raw edge index
- ตรวจ datum หลัง STEP จาก geometry/bounds ที่วัดได้ แทนการเชื่อ face number หรือ display metadata ที่เปลี่ยนง่าย
- ห้าม voxel, STL, triangle mesh, silent healing, fallback primitive หรือ result-conditioned repair

## การตรวจสอบและเกณฑ์สำเร็จ

- Corpus อย่างน้อยสิบรายการ ทุกตัว valid ใน CadQuery และหลัง FreeCAD import STEP อิสระ
- ต้องมี family ตามชื่อ: curved branch, tapered hollow duct, lofted rotary member, organic-like load bridge และ variable-section shell
- Corpus execute operator family V2 ที่รับทั้งหมดเชิงสาเหตุ และมีทั้ง ancestry แบบ single-feature กับ multi-feature boolean
- Corpus ที่ไม่ใช่ multi-body ทุกตัวมี positive-volume solid หนึ่งตัวพอดี; ถ้ารับ multi-body ต้องประกาศและสร้าง body count exact ซ้ำได้
- FreeCAD ต้องตรงกันด้าน body/solid topology, volume, centre of mass, geometry-derived bounds และ datum signature ภายใน tolerance ที่ประกาศ
- Clean run สองรอบต้องสร้าง canonical STEP hash, manifest identity และ result identity exact เหมือนกัน
- Pinned CadQuery kernel tests, default-Python parser tests, repository contracts, compilation และ full regression ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

Loft อาจ twist จาก section correspondence, sweep อาจ self-intersect เมื่อโค้งแคบ, boolean อาจสร้าง sliver/หลาย solid, shell subtraction อาจลบ body และ fillet selector อาจกำกวม Failure เหล่านี้ต้องมองเห็นได้ Work 092 ไม่ทำ search-space mutation, manufacturing admission, automatic meshing, FEA/contact, flow/thermal evaluation, subsystem discovery, whole-vehicle integration หรืออ้างว่ารูปร่างโค้งคือ functional novelty
