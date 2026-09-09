# ผล Work 109: ตัวสร้างเนื้อวัสดุรูปทรงอิสระ

ต้นฉบับภาษาอังกฤษ: `2026-09-10_109_freeform-material-generator-result.md`

วันที่: 2026-09-10 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และไฟล์ที่เปลี่ยน

Work 109 พัฒนา implicit Cartesian material/void field แบบมีขอบเขต, edit ครบหกตระกูล, deterministic OBJ boundary extraction, topology/feature controls, representation สามระดับ, resource caps และ exact replay สิ่งนี้พิสูจน์ execution และ geometry coverage ภายใน grid ที่ลงทะเบียน ไม่ใช่ functional หรือ physical superiority

ไฟล์ที่เปลี่ยน:

- `src/formula_ultimate/search/freeform_material_generator.py`
- `config/development/freeform_material_generator_v1.json`
- `scripts/development/run_freeform_material_generator.py`
- `tests/test_freeform_material_generator.py`
- `docs/contracts/FREEFORM_MATERIAL_GENERATOR_V1.md` และคู่ภาษาไทย
- plan/result นี้และคู่ภาษาไทย
- หลักฐานที่ ignore ใต้ `artifacts/work109/run_a` และ `run_b`

## การตัดสินใจและการหักล้าง

- scalar label หนึ่งค่าเป็นเจ้าของ occupied cell แต่ละช่อง cell ที่ไม่มีคือ void; mixed labels ไม่รองรับและถูกปฏิเสธ
- Geometry identity รวม occupancy และ labels ที่เรียงแล้วแต่ไม่รวมชื่อ case ดังนั้นความใหม่ปลอมจากเปลี่ยนชื่อมี identity เดิมและถูกปฏิเสธ
- slots คงที่เจ็ดรายการใช้ operators หกตระกูล; `boundary_displacement` ใช้หนึ่งครั้งขยาย boundary และอีกครั้งเติม through-hole จริง
- emit surface triangles เฉพาะเมื่อทุก edge มี incident faces สองหน้าพอดี ไม่อนุญาต healing
- Through-hole เปลี่ยน genus `0 -> 1` และการเติมกลับเป็น `1 -> 0` Split/merge เปลี่ยน occupied components `1 -> 2 -> 1` asymmetric thin feature มี retained fraction `1.0`
- coarse level แรกที่เสนอ `0.012 m` เปิดเผย edge-only contact และ OBJ boundary แบบ non-manifold การรันนั้นล้มเหลว จึงลงทะเบียน coarse level เป็น `0.02 m` และยังเปิดเผยผล `0.012 m` ที่ไม่รองรับไว้ที่นี่ ไม่มีการ repair mesh หรือยอมรับแบบเงียบ
- refinement volumes ต่างกัน (`0.001312`, `0.0013500000000000003`, `0.00126976 m3`) ซึ่งขัดแย้งกับคำกล่าวอ้างว่าไม่ขึ้นกับ resolution จึงบันทึกเป็น grid bias ไม่ใช่ข้อจำกัดทางกายภาพ

## หลักฐานเชิงตัวเลข

Canonical `run_a` และ replay `run_b` ใช้ result SHA-256 เดียวกัน `0866184b76def5f40cbde496f067f16db31ddf7bb4bbda41d8054467856a6a67`; replay รายงาน `exact: true` Artifact manifest SHA-256 คือ `1874ed3c88aa32d69a338d9bc3c8717dbaf38ad3cc0346ea6e59fb1374d034a2`

| Stage | Cells | Components | Genus | Triangles | Volume error |
|---|---:|---:|---:|---:|---:|
| source | `1350` | `1` | `0` | `1868` | `9.637352644315593e-16` |
| cavity route | `1194` | `1` | `1` | `2164` | `1.4347063924012536e-14` |
| cavity fill | `1442` | `1` | `0` | `2116` | `8.571362528664874e-15` |
| split | `1118` | `2` | `0` | `2464` | `1.881352606996313e-14` |
| merge | `1126` | `1` | `0` | `2480` | `1.6946676941158857e-14` |
| final redistribution | `1126` | `1` | `0` | `2480` | `1.6946676941158857e-14` |

errors ทั้งหมดต่ำกว่าขอบเขต surface-volume `1e-10` ที่ลงทะเบียน Refinement grid visits คือ `1728`, `13824` และ `27000`; ไม่ใช้เวลาประมาณแทน deterministic cost counts นี้

## คำสั่งตรวจและ exits ที่ตรงกัน

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_freeform_material_generator tests.test_repository_contract -v
# exit 0; ผ่าน 12 tests

python scripts/development/run_freeform_material_generator.py --config config/development/freeform_material_generator_v1.json --output-root artifacts/work109/run_a
# exit 0; 7 operator slots; status passed

python scripts/development/run_freeform_material_generator.py --config config/development/freeform_material_generator_v1.json --output-root artifacts/work109/run_b --replay-reference artifacts/work109/run_a/result.json
# exit 0; exact replay; result_sha256 เดียวกัน

python -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

runner attempt ก่อนหน้าที่ `0.012 m` exit `1` พร้อม `surface is not closed two-manifold` ต้องรัน affected regression สุดท้าย ตรวจ staged scope แบบระบุไฟล์ และ `git diff --cached --check` ก่อน commit จะรายงาน commit hash ที่ตรวจแล้วใน final handoff

## ข้อจำกัดและการส่งต่อ

นี่คือ voxel boundary ไม่ใช่ smooth B-rep หรือ volume mesh พร้อม solver Cartesian resolution และ orientation ทำให้ reachability, topology และ feature survival มีอคติ Material labels ไม่มีความหมาย mixed-cell, constitutive หรือ manufacturing Work 110 ต้องพัฒนา geometry-to-mesh bridge จริง รักษา field/material identity วัด approximation และเปิดเผย conversions ที่ไม่รองรับ ไม่มี scientific benefit หรือคำกล่าวอ้างรถเกิดจาก Work 109
