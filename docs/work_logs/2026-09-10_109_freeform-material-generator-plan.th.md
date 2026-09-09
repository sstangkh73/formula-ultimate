# แผน Work 109: ตัวสร้างเนื้อวัสดุรูปทรงอิสระ

ต้นฉบับภาษาอังกฤษ: `2026-09-10_109_freeform-material-generator-plan.md`

วันที่: 2026-09-10 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์

พัฒนา implicit material/void generator แบบมีขอบเขตที่เปลี่ยนขอบเขตต่อเนื่องและ topology ได้โดยไม่ใช้ template ชื่อชิ้นส่วน พร้อมเก็บ resolution, labels, mutation ancestry, conversion error, resource accounting และ deterministic replay อย่างชัดเจน

## ขอบเขตและการทดลอง

representation ต้นทางคือ Cartesian occupancy/material field แบบ uniform และ finite ในหน่วย SI นี่คือ implementation implicit-volume รุ่นแรกที่ admitted ไม่ใช่ระบบ adaptive geometry สากล Operators ที่ลงทะเบียนคือ boundary displacement, cavity routing, branching, split, merge และ material redistribution

- ตัวแปรอิสระ: edit operator, cell resolution, mutation seed และ complexity cap
- ตัวแปรตาม: occupied volume, จำนวน connected components และ enclosed voids, label volumes, การอยู่รอดของ thin feature, surface conversion error, execution operations และ geometry identity
- ตัวควบคุม: spatial domain, material labels, seed schedule, operator slots และงบ cell/operation ต่อ attempt เท่ากัน; Work 108 ยังเป็นเส้นทางเทียบ B-rep คงที่
- การหักล้าง: สร้าง/ปิด through-hole, แยก/ต่อ occupied regions, รักษา asymmetric thin feature และปฏิเสธ required cavity ที่หาย, label mixing, bounds ไม่ถูกต้อง, edit เกินงบ และความใหม่ปลอมจากเปลี่ยนชื่อเท่านั้น

## ไฟล์ที่วางแผนเปลี่ยน

- `src/formula_ultimate/search/freeform_material_generator.py`
- `config/development/freeform_material_generator_v1.json`
- `scripts/development/run_freeform_material_generator.py`
- `tests/test_freeform_material_generator.py`
- `docs/contracts/FREEFORM_MATERIAL_GENERATOR_V1.md` และคู่ภาษาไทย
- plan/result นี้และคู่ภาษาไทย
- generated corpus, OBJ surfaces, ancestry และ reports ที่ ignore ใต้ `artifacts/work109/`

## การพัฒนาและการตรวจสอบ

1. ตรวจ exact-schema SI domain, resolution, feature/budget limits, labels, source field และ seeded operator schedule
2. สร้าง occupancy โดยตรงจาก implicit primitives ใช้ edit แต่ละรายการแบบ causal และเก็บ before/after identities กับ topology descriptors
3. แปลง watertight oriented voxel boundary เป็น OBJ วัด enclosed volume เทียบ field volume และปฏิเสธ non-manifold/duplicate faces
4. รัน mutation chains ที่ลงทะเบียน พร้อม resolution-enlargement trials และ unsupported-conversion controls
5. สร้าง `result.json` แบบ deterministic และ exact replay

ประตูตรวจที่วางแผน:

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_freeform_material_generator tests.test_repository_contract -v
python scripts/development/run_freeform_material_generator.py --config config/development/freeform_material_generator_v1.json --output-root artifacts/work109/run_a
python scripts/development/run_freeform_material_generator.py --config config/development/freeform_material_generator_v1.json --output-root artifacts/work109/run_b --replay-reference artifacts/work109/run_a/result.json
python -m compileall -q src scripts tests
```

รัน affected regressions, `git diff --check`, stage แบบระบุไฟล์, ตรวจ staged names และ `git diff --cached --check` ก่อน commit จำกัด scope หนึ่งก้อนทันที

## เกณฑ์สำเร็จ

operator ที่ลงทะเบียนทั้งหมดทำงานภายในงบคงที่; controls hole/split/reconnect/thin-feature และ controls เชิงลบทำงานตามที่ประกาศ; surface volume ตรงกับ field volumeภายใน tolerance ที่ล็อก; รายงาน representation refinement โดยไม่ relabel เป็น physical truth; inputs เดียวกัน replay exact; commit หลักฐาน implementation สองภาษา

## ความเสี่ยงและสิ่งที่ไม่ทำ

Grid anisotropy, voxel aliasing และ resolution จำกัดอาจดูเหมือนข้อจำกัดการออกแบบ ต้องคงให้สังเกตได้และส่งต่อให้ meshing/refinement ใน Work 110 สิ่งที่ไม่ทำ: functional superiority, target silhouette, mixed-property homogenization, physics โครงสร้าง/flow/thermal, manufacturing, รถทั้งคันหรือ physical validation, ติดตั้ง dependency, push หรือเขียนประวัติใหม่
