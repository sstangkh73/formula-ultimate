# ผล Work 091: Constrained Free-Form Sketch and Wire Grammar V2

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_091_constrained-freeform-wire-grammar-v2-result.md`

## สถานะและผลลัพธ์

สถานะ: Completed

Work 091 implement และทดสอบ grammar ของ planar wire แบบ bounded อย่างอิสระ ไม่ได้เขียนเพียง syntax สำหรับอนาคต Corpus ที่รับสร้าง STEP profile valid 12 แบบจาก 9 family labels, ครอบคลุม curve/transform/constraint operator ทุกตัว, ผ่านพยาน import จาก FreeCAD อิสระ และสร้าง result identity ทั้งชุดซ้ำได้ตรงกันใน clean run รอบสอง

งานนี้เอาคอขวดเดิมที่รองรับเพียง rectangle/circle/annulus/shaft-section ออกจากชั้น geometry 2D แต่ยังไม่สร้าง 3D part และยังไม่ยืนยันประโยชน์ทางกายภาพ

## ไฟล์ที่เปลี่ยน

- `config/cad/freeform_wire_grammar_v2.json`: corpus SI 12 profile ที่รับและขอบเขตชัดเจน
- `src/formula_ultimate/components/freeform_wire_grammar.py`: strict declaration validator, canonical identity และการเทียบพยานข้าม kernel
- `src/formula_ultimate/components/__init__.py`: public grammar exports
- `scripts/cad/generate_freeform_wire_corpus.py`: CadQuery execution, constraints, nesting checks, canonical STEP export, FreeCAD orchestration และ replay
- `scripts/cad/inspect_freeform_wire_corpus_freecad.py`: import exact STEP อิสระและพยาน `.FCStd`
- `tests/test_freeform_wire_grammar.py`: parser, metamorphic, negative, measurement และ pinned-kernel tests
- `docs/contracts/FREEFORM_WIRE_GRAMMAR_V2.md` และไฟล์ภาษาไทยคู่กัน
- แผน/ผลนี้และไฟล์ภาษาไทยคู่กัน
- หลักฐานที่ ignore ใต้ `artifacts/work091/run_a` ถึง `run_e`; เก็บ failed run ไว้โดยไม่เขียนทับ

## การตัดสินใจและผล falsification

- V2 รับ curve ที่กำหนดครบและปฏิเสธ sketch ที่ underconstrained แทนการเรียก hidden iterative solver
- Operator ทั้งแปด execute จริง: `line`, `polyline`, `tangent_arc`, `three_point_arc`, `circle`, `ellipse`, quadratic/cubic `bezier` และ periodic `bspline` ที่จำกัด degree
- รองรับหลาย loop/hole, translate/rotate/mirror ตามลำดับ, line trim ที่ไม่ trivial หนึ่งตัว และ polygon offset ที่ไม่เป็นศูนย์หนึ่งตัว โดยไม่มี hidden healing
- พิสูจน์ว่า hole อยู่ภายใน outer loop และ hole ไม่ทับกันก่อนสร้าง final face Invalid nesting และ constraint ที่ไม่ผ่านยังเป็น failure ที่มองเห็นได้
- CadQuery กับ FreeCAD ต้องตรงกันแบบ exact ด้านจำนวน face/wire/edge Bounds คง absolute tolerance `1e-7 m` ส่วน area/perimeter ใช้ relative interoperability tolerance `0.002` ที่แยกชื่อชัดเจน ซึ่งไม่ผ่อน closure, validity, nesting หรือ topology
- FreeCAD ใช้ `optimalBoundingBox(False, False)` เพราะ default triangulation/display box ต่างจาก geometry-derived box ของ CadQuery บน free-form curve จึงปฏิเสธ default box แทนการเพิ่ม tolerance เพื่อซ่อนผล

Initial run สามรอบหักล้างสมมติฐานที่เร็วเกินไปและถูกเก็บเป็นหลักฐาน:

1. `run_a`: ellipse offset valid ก่อน export แต่ invalid หลัง STEP import ใน FreeCAD จึงเปลี่ยน offset control ที่รับเป็น closed polygon
2. `run_b`: strict absolute perimeter equality ปฏิเสธ ellipse โดยมี relative difference `0.0018832339106344149`; contract จึงประกาศ cross-kernel measurement tolerance แบบ capped ที่ `0.002`
3. `run_c`: default FreeCAD bounding box ต่างสูงสุดประมาณ `0.006019526 m` สำหรับ cubic Bezier แม้ area/topology ตรงกัน เมื่อใช้ geometry-derived optimal box ค่า maximum bound difference ของ successful run ลดเหลือ `6.6405214660392176e-15 m`

## หลักฐานที่สำเร็จ

ผล canonical ที่สำเร็จคือ `artifacts/work091/run_d/result.json`; `run_e/replay.json` รายงาน `exact: true`

| หลักฐาน | ผล |
|---|---:|
| Profiles | 12 |
| Family labels | 9 |
| Operator coverage | 8 จาก 8 |
| Transform coverage | 3 จาก 3 |
| Constraint coverage | 4 จาก 4 |
| Nontrivial trim segments | 1 |
| Nonzero offset profiles | 1 |
| Maximum area relative difference | `4.285843071817371e-13` |
| Maximum perimeter relative difference | `0.0018832339106344149` |
| Maximum bounds absolute difference | `6.6405214660392176e-15 m` |
| Declaration SHA-256 | `4a88ef8001377472c35eb18fe0eac23f4afd92b83c86edf86233af458a223820` |
| Manifest SHA-256 | `ae25ede8ccc54b768fada6253a039e2e8e440205d2b5a56109e348898eca9862` |
| FreeCAD report SHA-256 | `a07d72aae38adb51130436565d7b36db702ceb415011d2ef1ca2cbffd6077812` |
| Result SHA-256 | `94798aeb093d6bbcf7f3440faef96aed3f928180223f3679807a358dd3d3cae0` |
| Hidden geometry repair | `false` |

## คำสั่ง validation แบบ exact และ exit status

CadQuery kernel tests ที่สำเร็จ:

```powershell
$env:PYTHONPATH='src'
& .\.tools\cadquery-mcp\Scripts\python.exe -m unittest tests.test_freeform_wire_grammar -v
```

Exit status: `0`; ผ่าน 10 tests

Primary/replay witness ที่สำเร็จ:

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_freeform_wire_corpus.py --config config\cad\freeform_wire_grammar_v2.json --output-root artifacts\work091\run_d --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe'

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_freeform_wire_corpus.py --config config\cad\freeform_wire_grammar_v2.json --output-root artifacts\work091\run_e --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe' --replay-reference artifacts\work091\run_d\result.json
```

Exit status: `0` ทั้งสองคำสั่ง ทั้งคู่ให้ manifest `ae25ede8ccc54b768fada6253a039e2e8e440205d2b5a56109e348898eca9862` และ result `94798aeb093d6bbcf7f3440faef96aed3f928180223f3679807a358dd3d3cae0`

Compilation, focused/repository contracts และ regression ที่สำเร็จ:

```powershell
python -m compileall -q src scripts tests
python -m unittest tests.test_freeform_wire_grammar tests.test_repository_contract -v
python -m unittest discover -s tests -v
```

Exit status: `0` ทุกคำสั่ง Focused/repository ผ่าน 16 tests โดย skip 2 ตามคาดเพราะ Python ปกติไม่มี CadQuery Full regression ผ่าน 640 tests ใน `392.443 s` และ skip 5 รายการที่ขึ้นกับ environment ตามคาด

## ข้อจำกัด หลักฐานที่ขัด และความมั่นใจ

หลักฐานรองรับ bounded 2D profile execution และ deterministic STEP transfer ภายใต้ CadQuery `2.8.0` กับ FreeCAD `1.1.3`/OCCT `7.8.1` อย่างแข็งแรง Failed run ที่เก็บไว้ขัดกับคำอ้างว่า curve offset ทั่วไปหรือ default kernel measurement จะ portable โดยอัตโนมัติ Residual ของ ellipse perimeter แสดงว่าแม้เครื่องมือมาจากสาย OCCT ร่วมกันก็ยังวัดความยาว curve ต่างกันได้

คำอธิบายทางเลือกคือ exporter/importer และ approximation policy ที่ขึ้นกับ OCCT version; ยังไม่ได้ทดสอบ CAD kernel ตัวที่สาม หลักฐานที่ขาดคือ arbitrary NURBS weight/knot, multiple-hole ที่ซับซ้อนกว่า, 3D loft/sweep validity, minimum-wall behavior, material/manufacturing assignment, load, assembly, aero, thermal, race performance และ physical test ความมั่นใจสูงภายใน corpus/toolchain นี้ และต่ำเมื่ออยู่นอกขอบเขตที่ประกาศ

## งานต่อ

Work 092 ควรใช้ profile ที่รับเหล่านี้กับ grammar ของ constrained loft/sweep/guide-curve surface-and-solid และเพิ่ม gate สำหรับ section compatibility, self-intersection, thickness, topology, independent solid import และ replay โดยห้ามอนุมานว่า 2D profile ที่ผ่าน Work 091 เป็น viable component แล้ว
