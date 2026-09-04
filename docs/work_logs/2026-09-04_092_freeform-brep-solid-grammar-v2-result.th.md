# ผล Work 092: Free-Form B-rep Solid Grammar V2

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_092_freeform-brep-solid-grammar-v2-result.md`

## สถานะและผลลัพธ์

สถานะ: Completed

Work 092 implement solid grammar แบบ strict feature DAG และ execute non-primitive candidate 10 แบบจาก Work 091 profile Operator ที่รับทั้ง 18 ตัวทำงานเชิงสาเหตุ CadQuery กับ FreeCAD inspection อิสระตรงกันด้าน exact topology และ measurement/datum ภายในขอบเขต พร้อม replay ผลทั้งชุดได้ exact

นี่คือ milestone แรกที่โครงการสร้าง B-rep geometry แบบ curved, lofted, swept, hollow, treated และ multi-body หลากหลายได้จริง แต่เป็นหลักฐาน geometry เท่านั้น ไม่ใช่ functional discovery หรือ physical validation

## ไฟล์ที่เปลี่ยน

- `config/cad/freeform_brep_solid_grammar_v2.json`
- `src/formula_ultimate/components/freeform_solid_grammar.py`
- `src/formula_ultimate/components/__init__.py`
- `scripts/cad/generate_freeform_solid_corpus.py`
- `scripts/cad/inspect_freeform_solid_corpus_freecad.py`
- `tests/test_freeform_solid_grammar.py`
- `docs/contracts/FREEFORM_BREP_SOLID_GRAMMAR_V2.md` และไฟล์ภาษาไทยคู่กัน
- แผน/ผลนี้และไฟล์ภาษาไทยคู่กัน
- หลักฐานที่ ignore และเก็บไว้ใต้ `artifacts/work092/run_a` ถึง `run_h`

## การตัดสินใจและ falsification

- Feature input อ้างได้เฉพาะ typed state ที่มาก่อน; final body count เป็น declaration แบบ exact
- Intermediate ที่ empty/invalid, disconnected body ที่ไม่ได้ประกาศ, selector ที่หาไม่พบ และ shell self-erasure ต้อง fail ให้เห็น
- Fillet/chamfer ใช้ axis-parallel geometric signature; shell opening ใช้ extreme-face signature ห้าม raw edge/face index
- Datum เป็น declaration ร่วมกับค่าที่ derive จาก geometry และคำนวณใหม่อย่างอิสระหลัง STEP ไม่ได้ copy measurement จาก CadQuery
- `run_b` หักล้างสมมติฐานว่า revolved intersection สุดท้ายเป็น body เดียว: มันสร้าง disconnected body สี่ชิ้น Grammar จึงประกาศ `expected_body_count: 4` และตรวจ exact โดยไม่ auto-fuse
- `run_d` แสดงว่า floating-point datum JSON equality แบบ exact เข้มผิดประเภท แม้ position residual ใกล้ `1e-15 m` การเทียบจึงคง datum identity/kind แบบ exact และใช้ coordinate tolerance `1e-7 m` ที่ประกาศ

## หลักฐานที่สำเร็จ

หลักฐาน canonical คือ `artifacts/work092/run_g`; `run_h/replay.json` รายงาน `exact: true`

| หลักฐาน | ผล |
|---|---:|
| Candidates / families | 10 / 10 |
| Operator coverage | 18 / 18 |
| Maximum volume relative difference | `2.9726979210197703e-09` |
| Maximum area relative difference | `3.935383817517682e-10` |
| Maximum position/datum difference | `1.413570801210573e-11 m` |
| Declaration SHA-256 | `a0e1c47ee15dbebac9dce2183a502c26199197b751fe427c74c2824dd1b4ad8a` |
| Manifest SHA-256 | `369750f5ebef5a72dcd63147cec251a9a88d3d05a289d68289d6a9cd501a90ea` |
| FreeCAD report SHA-256 | `bf211fd926730d5fcb9db9be9bd2db0a50b7834364677fb64091e3bb9125aff7` |
| Result SHA-256 | `2f3fd3fceb5be7df82eecf73f15802fe5a219fc251ed62c466a77ca5dcde4ac9` |
| Hidden geometry repair | `false` |

## คำสั่ง validation แบบ exact

```powershell
$env:PYTHONPATH='src'
& .\.tools\cadquery-mcp\Scripts\python.exe -m unittest tests.test_freeform_solid_grammar -v
# exit 0; ผ่าน 7 tests

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_freeform_solid_corpus.py --config config\cad\freeform_brep_solid_grammar_v2.json --wire-config config\cad\freeform_wire_grammar_v2.json --output-root artifacts\work092\run_g --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe'
# exit 0

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_freeform_solid_corpus.py --config config\cad\freeform_brep_solid_grammar_v2.json --wire-config config\cad\freeform_wire_grammar_v2.json --output-root artifacts\work092\run_h --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe' --replay-reference artifacts\work092\run_g\result.json
# exit 0; exact true

python -m compileall -q src scripts tests
python -m unittest tests.test_freeform_solid_grammar tests.test_repository_contract -v
python -m unittest discover -s tests -q
# exit 0; focused/repository ผ่าน 13 และ skip 2 ตามคาด; full ผ่าน 647 ใน 396.855 s และ skip 7 ตามคาด
```

## ข้อจำกัดและงานต่อ

Corpus เป็นหลักฐานแข็งแรงสำหรับ bounded CAD language นี้ภายใต้ CadQuery `2.8.0` กับ FreeCAD `1.1.3`/OCCT `7.8.1` แต่ไม่พิสูจน์ arbitrary loft/sweep robustness, manufacturing access, wall quality, structural strength, interface หรือ function ชิ้นสี่ body เป็น multi-body ชัดเจนและไม่ใช่ connected part Work 093 ต้องแทน mutable typed part/interface/feature/path topology; Work 094 ต้อง mutate มันแบบ reproducible ก่อนอ้าง discovery ใด ๆ
