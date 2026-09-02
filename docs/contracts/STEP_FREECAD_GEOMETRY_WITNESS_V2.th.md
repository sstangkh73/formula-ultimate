# STEP to FreeCAD Geometry Witness V2

ไฟล์ต้นฉบับภาษาอังกฤษ: `STEP_FREECAD_GEOMETRY_WITNESS_V2.md`

## วัตถุประสงค์และสิทธิ์ของหลักฐาน

Work 081 นำ canonical STEP ที่แน่นอนทั้งห้าไฟล์จาก Work 078 เข้าใหม่ผ่าน FreeCAD `Part.Shape.read` โดยไม่ heal หรือแทน geometry แล้ววัดเรขาคณิตในหน่วย SI declaration ที่ freeze คือ `config/cad/step_freecad_geometry_witness_v2.json`; extractor คือ `scripts/cad/inspect_geometry_witness_v2_freecad.py`; และ comparator แบบ fail-closed คือ `scripts/cad/compare_geometry_witness_v2.py` ซึ่งใช้ `src/formula_ultimate/components/geometry_witness.py`

รอบที่ยอมรับใช้ CadQuery `2.8.0` สร้างไบต์ STEP ที่ freeze ซ้ำ และใช้ FreeCAD `1.1.3` / OCCT `7.8.1` import เนื่องจากทั้งสองเส้นทางอาจใช้เทคโนโลยี OCCT ร่วมกัน ชั้นหลักฐานจึงเป็น `toolchain_cross_check` ไม่ใช่ physical validation

## ตัวตนที่แน่นอนและสมบัติที่วัด

ตัวตน source manifest คือ `fff5c0c74513fae1a2bc7cd55020affbbaf67bdd6e9c0908f5aa2ea4131b2448` artifact ทุกไฟล์ที่ import ต้องคง SHA-256 ที่แน่นอน มี valid solid หนึ่งก้อนพอดี และรายงาน `hidden_geometry_repair=false`

| ชิ้นส่วน | STEP SHA-256 prefix | FreeCAD volume (m3) | มวลจาก synthetic density (kg) | Centre of mass (m) |
|---|---|---:|---:|---|
| `shaft_001` | `34e81618e3cd` | `7.936733407181677e-05` | `0.2142918019939053` | `[-8.5441e-17, -6.9764e-19, 0.06595183958570189]` |
| `bracket_001` | `b06e3141f7a1` | `8.144352220392336e-05` | `0.21989750995059307` | `[0.0004628865601941557, 1.2298e-20, 0.005828531482650844]` |
| `hollow_housing_001` | `ef92f5215e56` | `0.0001304688570501225` | `0.35226591403533075` | `[-0.00046848910750642053, -8.5948e-19, 0.03272660375475765]` |
| `ribbed_plate_001` | `af73c6492c9c` | `9.9164928734969e-05` | `0.26774530758441634` | `[-3.5072e-17, -0.0009113784760267323, 0.006314811066097798]` |
| `hub_like_001` | `8b3ff2186103` | `0.0001451118244934476` | `0.3918019261323085` | `[1.5696e-15, 8.2571e-16, 0.014999999999999993]` |

มวลเป็นการแปลง volume ที่วัดด้วย synthetic density ของ Work 079 ซึ่งระบุชัดเป็น `2700 kg/m3` ไม่ใช่มวลจากวัสดุที่วัดหรือมีแหล่งอ้างอิง และห้ามใช้สนับสนุน design use รายงานยังบันทึก full geometric inertia tensor, mass inertia tensor ที่แปลง และ principal moments/axes Comparator ตรวจค่า finite, symmetry, การสเกลด้วย density, การรักษา trace และ principal axes ที่ orthonormal

## การค้น interface โดยไม่ใช้เลข face

ไม่ถือว่าลำดับ face ใน STEP เป็นตัวตนถาวร semantic interface แต่ละตัวใช้ cylindrical-surface signature ซึ่งมี radius, แกน unsigned ที่ canonical, จุดบนแกนที่ใกล้ world origin ที่สุด และ axial bounds Extractor hash เนื้อหา surface ที่วัด และ comparator บังคับให้ตรงเพียงหนึ่งรายการภายใน tolerance ของ radius, position, axial และ angle ที่ freeze

witness ที่ยอมรับคือ shaft bearing surface, bracket through hole, housing through bore, ribbed-plate relief hole และ hub central bore ทั้งห้าถูกค้นแบบ unique การไม่พบกับการพบสอง surface ล้มด้วย causal code คนละรหัส

bounding box ปกติของ FreeCAD ให้ขอบเขตกว้างเกินจริงกับ fillet ของ shaft หลัง STEP import ดังนั้น V2 preregister และใช้ `optimalBoundingBox(True, False)` ของ FreeCAD ในการเปรียบเทียบ การเปลี่ยนนี้เปลี่ยนเฉพาะวิธีวัด ไม่ได้แก้ shape ที่ import ขอบเขต optimal ทั้งห้าตรงกับ exporter ภายใน gate `1e-9 m + 1e-6 relative` และ volume residual ทุกชิ้นต่ำกว่า `1.31e-13` relative

## การทำซ้ำ

สร้าง exact STEP corpus ซ้ำด้วย pinned CadQuery environment ก่อน:

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\cad\generate_brep_feature_corpus.py `
  --config config\cad\brep_feature_grammar_v1.json `
  --output-root artifacts\work081\source_step `
  --manifest artifacts\work081\source_manifest.json
```

ตั้ง `FORMULA_ULTIMATE_W081_CONFIG`, `FORMULA_ULTIMATE_W081_SOURCE_MANIFEST`, `FORMULA_ULTIMATE_W081_SOURCE_ROOT` และ `FORMULA_ULTIMATE_W081_OUTPUT` แล้วเรียก extractor ด้วย `C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe` path ที่มีช่องว่างอาจต้องใช้ Windows short-path สำหรับ argument ของ script จากนั้นเปรียบเทียบด้วย:

```powershell
python scripts\cad\compare_geometry_witness_v2.py `
  --config config\cad\step_freecad_geometry_witness_v2.json `
  --report artifacts\work081\run_a\freecad_report.json `
  --output artifacts\work081\run_a\comparison.json
python -m unittest tests.test_geometry_witness_v2 -v
```

## ตัวควบคุม ข้อจำกัด และ gate ถัดไป

ตัวควบคุมปฏิเสธ STEP/source-manifest identity ที่เปลี่ยน, solid ผิดหรือหลายก้อน, hidden repair, volume/bounds/mass/inertia drift, ข้อมูล non-finite, surface signature หาย/กำกวม/ถูกแก้ และรายการข้อจำกัดที่เปลี่ยน การสลับ key order คง canonical identity ส่วน FreeCAD/comparison สองรอบให้รายงานที่ byte-identical

V2 ไม่แก้ arbitrary global minimum wall thickness, exact section torsion constant, collision/interference ระหว่างชิ้นส่วน, clearance ของ assembly ที่เคลื่อนที่, การระบุวัสดุ, process capability, strength, fatigue, safety หรือ manufacturability ค่าที่ไม่รองรับเหล่านี้ยังระบุชัดต่อชิ้นส่วน material/process record ของ Work 079 ยังเป็น synthetic จึงมี `design_use_allowed=false` Work 082 ใช้ผลนี้ได้เฉพาะ software-coupling verification จนกว่างาน remediation แยกจะมี sourced material/process evidence และ independent manufacturing measurement ที่ครบ
