# ผล Work 096: Semantic Geometry Witness V3

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-05_096_semantic-geometry-witness-v3-result.md`

## สถานะและผลลัพธ์

สถานะ: Completed

Work 096 import และ inspect STEP candidate exact ทั้ง 10 ตัวของ Work 092 อย่างอิสระด้วย FreeCAD `1.1.3` / OCCT `7.8.1` และ recover mandatory bounded semantic section โดยไม่ใช้ face ordinal รวมถึง candidate 4 solids Clean run สองครั้งสร้าง report ที่ตรงกันทุก byte และ normalized semantic comparison SHA-256 เดิม

ผลนี้พิสูจน์ deterministic semantic inspection ของ frozen corpus ไม่ได้พิสูจน์ structural validity, global minimum thickness, assembly clearance, manufacturability, safety หรือ physical validity

## ไฟล์ที่เปลี่ยน

- `config/cad/semantic_geometry_witness_v3.json`
- `src/formula_ultimate/components/semantic_geometry_witness.py`
- `src/formula_ultimate/components/__init__.py`
- `scripts/cad/inspect_semantic_geometry_witness_v3_freecad.py`
- `scripts/cad/compare_semantic_geometry_witness_v3.py`
- `tests/test_semantic_geometry_witness_v3.py`
- `docs/contracts/SEMANTIC_GEOMETRY_WITNESS_V3.md` และไฟล์ภาษาไทย
- plan/result ชุดนี้และไฟล์ภาษาไทย
- หลักฐานที่ ignore และเก็บไว้ใต้ `artifacts/work096/run_a` กับ `run_b`

## การตัดสินใจและหลักฐาน

- ตรวจ exact source manifest และ STEP SHA-256 ก่อน import ใช้ `Part.Shape.read_step_no_repair` และ `hidden_geometry_repair` คงเป็น false
- compound ไม่มี shape-level inertia property ใน FreeCAD API นี้ V3 จึงรวม geometric inertia ของแต่ละ solid รอบ aggregate centre ด้วย parallel-axis theorem ทำให้ยังเก็บ member 4 solids ไว้ ไม่ตัดออก
- เก็บ body/solid/shell count, volume, area, mass จาก density ที่ประกาศ, centre of mass, full inertia, principal moment/axis, axis degeneracy, axis-aligned bounds และ tessellated principal-oriented bounds
- report มี order-independent face signature 139 รายการและ fixed-parameter curvature sample 417 จุด Comparator คำนวณ curvature class/area/radius spectrum ซ้ำอย่างอิสระ
- thickness probe ใช้ exact B-rep line/face intersection ที่ global grid line 27 เส้น บวก centre line 3 แกนต่อ solid แล้วเลือก material interval ด้วย midpoint containment ช่วง minimum sampled span ที่พบคือ `0.00030120991794767293–0.015805462099021627 m`; ไม่ใช่ guaranteed global wall minimum
- section evolution ใช้ exact thin-slab intersection volume ค่า section area เป็นศูนย์เมื่อ path ผ่านพื้นที่ว่างยังคงเป็น output ไม่เติมหรือ repair
- support/load/contact/thermal/fluid region identity hash ชุด face signature ที่ sort แล้วตาม geometric rule ที่ประกาศ การสลับ candidate, face, datum และ region record รักษา normalized semantic comparison identity
- member 4 solids รายงาน internal solid pair 6 คู่, minimum clearance `0.035443617196894 m` และ pairwise interference volume ที่วัดได้เป็นศูนย์
- comparator ที่เข้มขึ้นคำนวณซ้ำ mass/inertia consistency, curvature spectrum, datum/region correspondence, thickness minima, section/path correspondence, clearance pair count และ static swept-envelope volume

## หลักฐาน identity

- Config SHA-256: `b6233a5a8e07a74b77c4e59bf6e5164b01d7f4d954bfb3fa230724f51b31c41a`
- FreeCAD report SHA-256: `96cf848f1dc1482be4b408eb146c36cca324f71b21c74a4b5b5de243412c6c08`
- Report-file SHA-256 ทั้งสองรอบ: `97e2259c1cf230c8be8e0f37c244c419c34db86afba41505ef5da87bd6e2ba2a`
- Normalized comparison SHA-256: `731ba8b6c167f36703a278da959cf8f586714262995c811ede38b2892599cf7d`
- Candidate count: `10`; `hidden_geometry_repair: false`; `structural_validity: false`

## คำสั่งตรวจสอบที่ใช้จริง

```powershell
$env:PYTHONPATH='C:\Program Files\FreeCAD 1.1\bin'
$env:FORMULA_ULTIMATE_W096_CONFIG=(Resolve-Path 'config/cad/semantic_geometry_witness_v3.json').Path
$env:FORMULA_ULTIMATE_W096_MANIFEST=(Resolve-Path 'artifacts/work092/run_g/manifest.json').Path
$env:FORMULA_ULTIMATE_W096_SOURCE_ROOT=(Resolve-Path 'artifacts/work092/run_g').Path
$env:FORMULA_ULTIMATE_W096_OUTPUT=(Join-Path (Resolve-Path 'artifacts/work096/run_a').Path 'report.json')
& 'C:\Program Files\FreeCAD 1.1\bin\python.exe' 'scripts/cad/inspect_semantic_geometry_witness_v3_freecad.py'
# exit 0; วัด 10 candidates

python scripts/cad/compare_semantic_geometry_witness_v3.py --config config/cad/semantic_geometry_witness_v3.json --report artifacts/work096/run_a/report.json --output artifacts/work096/run_a/comparison_strict.json
# exit 0; comparison ผ่าน

# ใช้ FreeCAD command เดิมโดยเปลี่ยน W096_OUTPUT ไปใต้ run_b แล้วรัน:
python scripts/cad/compare_semantic_geometry_witness_v3.py --config config/cad/semantic_geometry_witness_v3.json --report artifacts/work096/run_b/report.json --output artifacts/work096/run_b/comparison.json --replay-reference artifacts/work096/run_a/comparison.json
# exit 0; report JSON exact=true และ file SHA-256 เหมือนกัน

python -m unittest tests.test_semantic_geometry_witness_v3 tests.test_repository_contract -q
# exit 0; ผ่าน 14 tests

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; ผ่าน 680 tests ใน 341.326 s; skip ตามสภาพแวดล้อมที่คาดไว้ 7 tests
```

## ข้อจำกัดและงานถัดไป

thickness field เป็น sampled, B-spline curvature sample ที่ fixed parameter และ section second moment เป็น bounding proxy Principal axis อาจไม่ unique สำหรับ geometry สมมาตร Region semantic เป็น geometric selection rule ไม่ใช่ physical boundary-condition evidence Clearance อยู่ระหว่าง solid ภายใน imported candidate เดียว และ swept envelope เป็น static identity motion Work 097 ต้องนำ unfamiliar geometry family เข้า declared model selection, meshing, contact/failure controls, convergence และ independent residual gates ต่อไป
