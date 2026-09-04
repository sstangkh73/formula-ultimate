# แผน Work 096: Semantic Geometry Witness V3

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-05_096_semantic-geometry-witness-v3-plan.md`

## สถานะ

สถานะ: Completed

## วัตถุประสงค์

ตรวจ STEP candidate ทุกตัวของ Work 092 อย่างอิสระด้วย FreeCAD/OCCT และ recover physics-relevant semantic evidence ที่ไม่ขึ้นกับลำดับ face ผูก datum และ region intent ที่ประกาศกับ geometric signature แทน face index ที่ไม่เสถียร พร้อมระบุ bounded sampling และสิ่งที่ยังตีความไม่ได้อย่างชัดเจน

## ขอบเขตและไฟล์ที่วางแผนเปลี่ยน

- `config/cad/semantic_geometry_witness_v3.json`
- `src/formula_ultimate/components/semantic_geometry_witness.py`
- `src/formula_ultimate/components/__init__.py`
- `scripts/cad/inspect_semantic_geometry_witness_v3_freecad.py`
- `scripts/cad/compare_semantic_geometry_witness_v3.py`
- `tests/test_semantic_geometry_witness_v3.py`
- `docs/contracts/SEMANTIC_GEOMETRY_WITNESS_V3.md` และไฟล์ภาษาไทย
- plan/result ชุดนี้และไฟล์ภาษาไทย
- หลักฐาน FreeCAD/replay/negative-control ที่ ignore ใต้ `artifacts/work096/`

## ตัวแปรและ controls

- ตัวแปรอิสระ: exact Work 092 manifest/STEP identity, density ที่ประกาศ, datum declaration, semantic region declaration, กฎ axis/path, section/thickness sample fraction, curvature sampling rule, sweep rule และ comparison tolerance
- ตัวแปรตาม: imported solid/shell/body count; validity; volume; mass; centre of mass; full geometric/mass inertia กับ principal axes; axis-aligned และ principal-oriented bounds; curvature class/area spectrum กับ sampled curvature radius; sampled material-span thickness field; วิวัฒนาการของ section area/equivalent radius/second-moment proxy; datum; signature-selected support/load/contact/thermal/fluid region; path length/bend evidence; static clearance/interference กับ swept envelope; declaration/report identity และ residual
- controls: mapping-key และ face-record permutation; การสลับ report record ที่ไม่เปลี่ยนสาระ; STEP/interface/region signature ที่ถูกแก้; datum หรือ region หาย; ambiguous signature; report hash ถูกแก้; non-finite measurement; hidden repair; sampling protocol เปลี่ยน และ replay mutation

## นิยามการวัดแบบมีขอบเขต

- FreeCAD import exact STEP bytes ด้วย `Part.Shape.read` โดยไม่ heal หรือ mutate
- mass เท่ากับ imported volume คูณ synthetic density ที่ประกาศ และเก็บ OCCT inertia tensor ทั้งชุดพร้อม deterministic principal decomposition
- principal-oriented bounds project vertex ที่ import ทุกตัวลงบน inertia axes ที่วัด โดย canonicalize เครื่องหมายแกน และรายงานแกน near-degenerate แทนการอ้างว่า unique
- curvature spectrum ใช้ surface class, face area และ finite `Face.curvatureAt` sample ที่ fixed interior parameter fraction Radius คือ `1/|curvature|` เฉพาะค่าที่มากกว่า zero-curvature tolerance
- thickness เป็น deterministic sampled material-span witness จาก exact B-rep intersection ของ axis-aligned probe line ที่ frozen grid fraction ไม่ใช่ guaranteed global minimum wall thickness
- section evolution ใช้ thin exact B-rep slab ตั้งฉากกับ declared longest-bounds path Area คือ volume ของ slab intersection หาร slab thickness แล้ว derive equivalent radius และ centroidal second-moment proxy จาก sampled area/bounds
- region signature ใช้ datum-relative extreme plane, surface class, normal alignment, centroid, area และ bounding signature โดยไม่ใช้ face ordinalใน identity
- clearance/interference และ swept envelope เป็น self/static bounded witness ของ candidate เดี่ยว Assembly-pair clearance และ arbitrary motion ยัง unsupported จนกว่าจะมี typed mate

## เกณฑ์สำเร็จ

- STEP candidate Work 092 ทั้ง 10 ตัว รวม member ที่ประกาศ 4 solids ต้อง import valid และมี mandatory V3 evidence section ทุกส่วน
- datum และ support/load/contact/thermal/fluid region ที่ประกาศทุกตัวต้อง match exactly หนึ่ง independently inspected signature; semantic ที่ถูกแก้ หาย หรือ ambiguous ต้อง fail closed
- curved, hollow/shell, branching/ribbed, rotary/hub และ multi-body family ต้องได้ finite bounded measurement พร้อมบันทึก limitation
- การสลับ face/record ต้องรักษา semantic comparison identity และ clean FreeCAD rerun เดิมต้องสร้าง report/comparison SHA-256 เหมือนกันทั้งชุด
- focused tests, compilation, repository contracts, FreeCAD run/replay, negative controls และ full regression ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

sampled thickness และ section field อาจพลาด local extrema; B-spline curvature ขึ้นกับ fixed sampling; inertia axis อาจไม่ unique สำหรับชิ้นสมมาตร; region intent จำกัดใน datum-relative signature ที่ประกาศ และ static self-clearance ไม่ใช่ assembly clearance การผ่านพิสูจน์ exact inspection ของ corpus นี้ ไม่ใช่ structural validity, การรองรับ arbitrary future geometry, manufacturability, contact behavior, motion safety หรือ physical validation ส่วน Work 097 รับผิดชอบ generalized evaluation และ convergence benchmark
