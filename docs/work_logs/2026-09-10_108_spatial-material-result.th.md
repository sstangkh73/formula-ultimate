# ผล Work 108: ข้อมูลต้นทางร่วมของเนื้อวัสดุและช่องว่าง

ต้นฉบับภาษาอังกฤษ: `2026-09-10_108_spatial-material-result.md`

วันที่: 2026-09-10 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์

Work 108 พัฒนาแพ็กเกจแรกใน `docs/plans/detailed_part_to_vehicle_v1` แล้ว สามกรณี admitted จาก Work 092 ผูก source B-rep ที่ตรงกันกับการเป็นเจ้าของวัสดุ หลักฐาน void จาก subtraction และ rigid placement อย่างชัดเจน CadQuery และ FreeCAD วัด region STEP ชุดเดียวกันหลัง placement อย่างอิสระ ผล volume, mass, centre-of-mass และ inertia ผ่านขอบเขตที่ลงทะเบียน การรันสะอาดรอบสอง replay ได้ exact

นี่คือ spatial/CAD verification แบบมีขอบเขต ไม่ใช่คำกล่าวอ้างด้านโครงสร้าง thermal, flow, manufacturing, รถทั้งคัน, scientific benefit หรือ physical validation

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/components/spatial_material.py`
- `config/development/spatial_material_v1.json`
- `scripts/development/run_spatial_material.py`
- `scripts/cad/inspect_spatial_material_freecad.py`
- `tests/test_spatial_material.py`
- `docs/contracts/SPATIAL_MATERIAL_VOID_V1.md` และคู่ภาษาไทย
- `docs/work_logs/2026-09-10_108_spatial-material-plan.md` และคู่ภาษาไทย
- ผลนี้และคู่ภาษาไทย
- หลักฐานที่เก็บและ ignore ใต้ `artifacts/work108/run_a` และ `artifacts/work108/run_b`

ไม่ได้แก้ source API เดิมหรือไฟล์หลักฐานประวัติศาสตร์

## การตัดสินใจและ implementation

- การตรวจ exact schema บังคับค่า SI finite, density เป็นบวก, แกนหมุนเป็น unit, source body ที่มีเนื้อทุกก้อนมีเจ้าของเพียงหนึ่งเดียว, region identity ไม่ซ้ำ และ hash declaration/STEP ต้นทางเปลี่ยนย้อนหลังไม่ได้
- source corpus ถูกสร้างใหม่ตามลำดับ Work 092 เดิมก่อน export placed region ใด ๆ วิธีนี้รักษา canonical upstream STEP identity แทนการยอมรับ exporter counter ใหม่
- admitted กรณีโค้ง กรณีกลวงจาก subtraction และกรณีสี่ body กรณี multi-body กำหนดหนึ่ง solid ที่ตรงกันต่อ material region หลังเรียง centre/volume แบบ deterministic
- การตัดกันของ occupied body รายคู่เกิน `1e-12 m3` ล้มเหลวแบบปิด ค่าสูงสุดที่วัดได้คือ `0 m3`
- หลักฐาน cavity ต้องตรงกับ ancestry `boolean_subtract` จริง `outer`, `inner`, `duct` residual ของสมการปิดคือ `0`
- ค่า CAD หน่วย `mm3`, `mm` และ `mm5` ถูกแปลงเป็น `m3`, `m` และ `m5` การถ่วง density และ parallel-axis theorem สร้าง mass properties ทั้งระบบ
- วัสดุ Work 108 เป็น fixture ความหนาแน่นคงที่แบบ synthetic อย่างชัดเจน ชื่อวัสดุไม่อ้าง strength, thermal หรือ manufacturing property ที่วัดจริง
- Material mutation และ placement mutation เปลี่ยน dependent evidence identity การเติม geometry กลวงจริงเปลี่ยนทั้ง STEP SHA-256 และมวลจาก `0.115652168747105 kg` เป็น `0.224098880843536 kg`

## การหักล้างและการแก้ระหว่างพัฒนา

การรัน fail-fast สามครั้งเปิดเผยและแก้สมมติฐาน:

1. import แรกของ runner ใช้ชื่อ API เดิมผิดเป็น `validate_wire_grammar`; validator จริงของ Work 091 คือ `validate_grammar`
2. การ export placed region แทรกกลางเปลี่ยนตัวนับ `PRODUCT` ของ OCCT STEP จึงทำให้ SHA-256 source ของ hollow เปลี่ยนแม้ geometry เหมือนเดิม runner จึงสร้างและ export source corpus Work 092 ทั้งชุดตามลำดับเดิมก่อน downstream exports โดยไม่ลด identity gate
3. `Part.read` คืน compound wrapper ที่ไม่มี `MatrixOfInertia` FreeCAD inspector จึงบังคับหนึ่ง solid ต่อ region แล้ววัด solid นั้นโดยตรง

Duplicate ownership, incomplete ownership, วัสดุที่ไม่รู้จัก, placement non-finite, void semantics ที่ไม่รองรับ และ source identity เก่าถูกปฏิเสธ สมมติฐานที่ต้องการรอดจาก controls ที่ admitted: การเปลี่ยน geometry, material และ placement จริงทำให้หลักฐานที่พึ่งพาหมดอายุตามที่ตั้งใจ

## หลักฐานเชิงตัวเลข

หลักฐาน canonical: `artifacts/work108/run_a` Replay: `artifacts/work108/run_b/replay.json` ซึ่งมี `exact: true`

| หลักฐาน | ผล |
|---|---:|
| Cases / occupied material regions | `3 / 6` |
| CadQuery / FreeCAD | `2.8.0 / 1.1.3` |
| Maximum undeclared overlap | `0 m3` |
| Hollow cavity closure residual | `0` |
| Maximum system volume relative error | `4.01876492153646e-10` |
| Maximum system mass relative error | `1.79738452857777e-9` |
| Maximum system centre absolute error | `1.42850696549512e-11 m` |
| Maximum system inertia relative error | `4.85111865432947e-9` |
| Artifact manifest SHA-256 | `e29833cd993df2e2ffbebca2f60c1c9009cf5ac2f44d7aebc4a487be587276d8` |
| FreeCAD report SHA-256 | `edd1d7abdaef5f8927cad8f7674fea89944ada7faf03fdb1a4b1a2002aec17cb` |
| Result SHA-256 | `662f33cf876f6b6a444b46c346adcd7434e7baf60a95fb3366df3beffaf8470a` |

ค่ารวมรายกรณี:

| Case | Volume (`m3`) | Mass (`kg`) | Centre of mass (`m`) |
|---|---:|---:|---|
| `curved_branch_placed` | `3.37238125113722e-5` | `0.091054293780705` | `[0.11889545450136, -0.0406540121332367, 0.129199002436967]` |
| `tapered_hollow_placed` | `9.63768072892543e-5` | `0.115652168747105` | `[-0.0733739692121858, 0.0776078853869922, 0.0605122443349965]` |
| `multi_body_mixed_material_placed` | `2.93976512599125e-6` | `0.0143313549898507` | `[0.023682615749267, 0.00821489285403821, -0.0125828706419786]` |

## คำสั่งตรวจและ exit ที่ตรงกัน

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_spatial_material tests.test_repository_contract -v
# exit 0; ผ่าน 13 tests

python -m compileall -q src scripts tests
# exit 0

& .\.tools\cadquery-mcp\Scripts\python.exe -m unittest tests.test_spatial_material tests.test_repository_contract -v
# exit 0; ผ่าน 13 tests

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_spatial_material.py --config config\development\spatial_material_v1.json --output-root artifacts\work108\run_a --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe'
# exit 0; status passed; result_sha256 662f33cf876f6b6a444b46c346adcd7434e7baf60a95fb3366df3beffaf8470a

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_spatial_material.py --config config\development\spatial_material_v1.json --output-root artifacts\work108\run_b --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe' --replay-reference artifacts\work108\run_a\result.json
# exit 0; status passed; exact replay; result_sha256 เดียวกัน

& .\.tools\cadquery-mcp\Scripts\python.exe -m unittest tests.test_freeform_solid_grammar tests.test_spatial_material tests.test_repository_contract -v
# exit 0; ผ่าน affected tests 20 รายการ

git diff --check
# exit 0
```

ก่อน commit ยังต้อง stage แบบระบุไฟล์ ตรวจ staged names และรัน `git diff --cached --check` จะรายงาน short commit hash ที่ตรวจแล้วใน final handoff เพราะ commit ไม่สามารถบรรจุอัตลักษณ์ของตัวเองอย่างซื่อตรงได้

## ข้อจำกัด คำอธิบายทางเลือก และงานต่อ

CadQuery และ FreeCAD ใช้เทคโนโลยี geometry ตระกูล OCCT ร่วมกัน การเห็นตรงกันตรวจ exact artifact transfer และการวัดในแอปที่แยกกัน ไม่ใช่ physics อิสระ ความหนาแน่น synthetic คงที่ไม่จำลอง anisotropy, gradient, porosity, temperature dependence, failure หรือ manufacturing variation Work 108 admitted หนึ่งวัสดุต่อ source solid ที่เชื่อมต่อหนึ่งก้อน วัสดุที่แปรเชิงพื้นที่ภายใน body เชื่อมต่อเดียวยังขาดอยู่ กรณี Work 092 ที่เลือกไม่ได้ยืนยันความทนทานของ B-rep ตามอำเภอใจ

Work 109 สามารถสร้าง candidate เนื้อวัสดุ/ช่องว่าง free-form ใหม่เทียบกับ spatial contract ที่เปลี่ยนย้อนหลังไม่ได้นี้ Work 110 สามารถ mesh เฉพาะ geometry ที่ผ่าน ownership และ source identity gate นี้ ห้าม promote รถหรือชิ้นส่วนจาก mass-property checks เหล่านี้เพียงอย่างเดียว
