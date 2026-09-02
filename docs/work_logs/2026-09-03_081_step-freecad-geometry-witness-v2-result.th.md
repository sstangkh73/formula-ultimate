# ผล Work 081: STEP to FreeCAD Geometry Witness V2

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-03_081_step-freecad-geometry-witness-v2-result.md`

## สถานะและผลลัพธ์

สถานะ: Completed

FreeCAD `1.1.3` / OCCT `7.8.1` นำไบต์ canonical STEP ที่แน่นอนทั้งห้าไฟล์จาก Work 078 เข้าใหม่อย่างอิสระ ทุก artifact คง SHA-256 ที่ freeze, import เป็น valid solid หนึ่งก้อนพอดีโดยไม่รายงานการ repair และให้ค่า SI ที่ finite ได้แก่ volume, optimal bounding box, centre of mass, full inertia tensor, principal moments และ principal axes semantic cylindrical interface ห้าตัวถูกค้นแบบ unique จาก geometry signature โดยไม่ใช้ face index

FreeCAD-to-CadQuery volume relative residual สูงสุดคือ `1.3037757588616636e-13`; optimal-bound absolute error สูงสุดคือ `4.28129753871076e-15 m` ทั้งคู่อยู่ใน gate `1e-6` relative และ `1e-9 m` absolute ที่ freeze การรัน FreeCAD สองรอบและ comparator สองรอบตรงกันแบบ byte-identical

ผลเป็น `toolchain_cross_check` ไม่ใช่ physical validation เพราะสองเส้นทางอาจใช้ OCCT ร่วมกัน มวลที่รายงานใช้ density synthetic ที่ระบุชัด `2700 kg/m3`; หลักฐานวัสดุและ process ยังเป็น synthetic จึงมี `design_use_allowed=false`

## ไฟล์ที่เปลี่ยน

- `config/cad/step_freecad_geometry_witness_v2.json`
- `src/formula_ultimate/components/geometry_witness.py`
- `scripts/cad/inspect_geometry_witness_v2_freecad.py`
- `scripts/cad/compare_geometry_witness_v2.py`
- `tests/test_geometry_witness_v2.py`
- `docs/contracts/STEP_FREECAD_GEOMETRY_WITNESS_V2.md` และไฟล์ภาษาไทย
- ผลฉบับนี้และไฟล์ภาษาไทย
- แผน Work 081 และไฟล์ภาษาไทย ซึ่งเปลี่ยนสถานะเป็น `Completed`

STEP, manifest, FreeCAD JSON และ comparison evidence ที่สร้างใต้ `artifacts/work081/` ถูก ignore และไม่รวมใน commit

## การตัดสินใจและการทบทวนหลักฐาน

- ตรวจ exact source-manifest และ per-STEP hash ก่อน import; ตัวตนที่เปลี่ยน fail ก่อนยอมรับการวัด
- ใช้ `Part.Shape.read` โดยไม่เรียก heal วัด shape validity และ topology หนึ่ง solid หลัง import
- bounding box ปกติของ FreeCAD ขยายขอบเขต fillet ของ shaft เกินจริง (`ประมาณ +/-0.021647844 m` เทียบ exporter `ประมาณ +/-0.0200000001 m`) หลักฐานวิธีวัดที่ขัดกันนี้ถูกเก็บไว้และแก้โดย preregister `optimalBoundingBox(True, False)` ของ FreeCAD ซึ่งไม่แก้ shape สำหรับ comparison ที่ยอมรับ ไม่มีการแก้ geometry
- full inertia evidence มาจาก matrix ของ solid ใน FreeCAD tensor เชิงเรขาคณิตหน่วย `m5` คูณ density ที่ประกาศเป็น `kg m2`; comparator ตรวจ symmetry, diagonal ที่ finite/positive, density scaling, trace ของ principal value และแกน orthonormal
- interface ใช้ radius, canonical unsigned axis, จุดบนแกนที่ใกล้ world origin ที่สุด และ axial bounds hash เนื้อหา surface ไม่ขึ้นกับเลข face ชั่วคราว
- arbitrary wall minima, section/torsion constants, moving-assembly collision และสมบัติการผลิตที่ไม่รองรับยังระบุชัดแทนการอนุมาน

หลักฐานสนับสนุน: exact one-solid import ห้าชิ้น, unique interface ห้าตัว, volume residual สูงสุด `1.3037757588616636e-13`, bound error สูงสุด `4.28129753871076e-15 m` และ exact replay หลักฐานขัดแย้ง: bounding box ปกติของ FreeCAD ไม่เหมาะกับ shaft fillet และไม่ได้ใช้รับผล คำอธิบายทางเลือก: ความตรงกันอาจเกิดจาก OCCT ที่ใช้ร่วมกัน จึงไม่เรียกเป็นความจริงทางกายภาพแบบอิสระ หลักฐานที่ขาด: material/process ที่มีแหล่งอ้างอิง, density/mass จริง, arbitrary wall/section convergence, exact part-to-part interference, การเทียบการทดลอง และหลักฐานความปลอดภัย ความเชื่อมั่นสูงสำหรับ exact byte identity และ deterministic software measurement ภายใต้ pinned local toolchain แต่ต่ำสำหรับ claim การออกแบบโลกจริง

## คำสั่งตรวจสอบจริงและผล

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\cad\generate_brep_feature_corpus.py `
  --config config\cad\brep_feature_grammar_v1.json `
  --output-root artifacts\work081\source_step `
  --manifest artifacts\work081\source_manifest.json
# exit 0; 5 candidates; manifest_sha256=
# fff5c0c74513fae1a2bc7cd55020affbbaf67bdd6e9c0908f5aa2ea4131b2448

# ตั้ง FORMULA_ULTIMATE_W081_CONFIG, _SOURCE_MANIFEST, _SOURCE_ROOT,
# และ _OUTPUT ไปยัง path ที่บันทึก; ส่ง script path แบบ 8.3:
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" `
  scripts\cad\inspect_geometry_witness_v2_freecad.py
# run_a exit 0; run_b exit 0; แต่ละรอบวัด 5 parts
# report_sha256=34ad809df13ba746352107e952e67a6d187795c96e1cb1096a6efc9a7ba28132

python scripts\cad\compare_geometry_witness_v2.py `
  --config config\cad\step_freecad_geometry_witness_v2.json `
  --report artifacts\work081\run_a\freecad_report.json `
  --output artifacts\work081\run_a\comparison.json
# run_a exit 0; run_b exit 0; comparison_sha256=
# 7ea916aff72334bd47ccf7b4af36f8c3c64674037e5532ce2e5a961d53cc13b7

Get-FileHash artifacts\work081\run_a\freecad_report.json -Algorithm SHA256
Get-FileHash artifacts\work081\run_b\freecad_report.json -Algorithm SHA256
# ทั้งคู่ 01bfecefb35931da8d92b53a048186550686e0bd82d5c71b4346f1b1edaad15c

Get-FileHash artifacts\work081\run_a\comparison.json -Algorithm SHA256
Get-FileHash artifacts\work081\run_b\comparison.json -Algorithm SHA256
# ทั้งคู่ 0e0238afcc24bbf72ca8d552b291fafc5071f6ef1d734b50983dad7544540ec0

python -m unittest tests.test_geometry_witness_v2 tests.test_repository_contract -v
# exit 0; Ran 16 tests; OK

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -v
# exit 0; Ran 524 tests in 300.239s; OK (skipped=3 tests ของ pinned CadQuery environment)
```

## ข้อจำกัดและงานถัดไป

Work 081 ทำ geometry import และ tooling สำหรับ global-property/interface witness ของ canonical fixture ห้าชิ้นเสร็จเท่านั้น ยังไม่ผ่าน evidence-remediation gate ของ Work 081 สำหรับ design use เพราะแหล่ง material/process ของ Work 079 เป็น synthetic และ fixture ไม่รองรับ arbitrary manufacturing measurement ทุกชนิด ต้องมีงาน remediation ที่วางแผนแยกก่อน Work 082 จะอ้าง capacity ของชิ้นส่วนจริงได้ หากยังไม่มี Work 082 จำกัดเฉพาะ software-coupling verification
