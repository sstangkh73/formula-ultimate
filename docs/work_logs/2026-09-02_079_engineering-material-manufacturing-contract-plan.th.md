# แผน Work 079: Engineering Material and Manufacturing Contract

สถานะ: Completed

ต้นฉบับภาษาอังกฤษ: `2026-09-02_079_engineering-material-manufacturing-contract-plan.md`

## วัตถุประสงค์และขอบเขต

Implement engineering material/manufacturing-process contract แบบ fail-closed และ hash-addressed แล้วผูกกับ geometry witness ความสามารถของ material ต้องมาจาก density, elastic, strength, fracture, fatigue-evidence status และ thermal property ที่ประกาศพร้อม source/domain/confidence Manufacturing admission ต้องมาจากการวัด wall, hole, ligament/web, radius, tool access และ requested tolerance เทียบกับ process envelope ที่มีหลักฐาน

Canonical record เป็น synthetic aluminium-like verification fixture ใช้ validate equation และ rejection behavior เท่านั้น และถูกห้ามใช้เพื่อ design โดยชัดแจ้ง งานนี้ไม่มี real coupon dataset ที่ผู้ใช้ส่งมา ดังนั้น implementation ต้องรักษาขอบเขต missing evidence แทนการสร้าง vehicle material ที่อ้างว่า sourced ขึ้นเอง

## แบบการทดลอง

- ตัวแปรอิสระ: ค่า material property/evidence class/domain, fatigue evidence status/curve, process limit, geometry witness measurement, tool direction/clearance/depth ratio, requested tolerance และ record hash
- ตัวแปรตาม: material/process/assignment admission, elastic-consistency residual, property coverage, manufacturing margin/violation code, design-use eligibility และ deterministic record/report identity
- ตัวแปรควบคุม: canonical synthetic record และ bracket-like witness ที่ผ่าน; control สำหรับ wrong unit/unknown field, `NaN`, negative property, invalid Poisson ratio, `E/G/nu` ไม่สอดคล้อง, ultimate ต่ำกว่า yield, property source หาย, unsupported fatigue claim, wall บาง, hole/ligament/web/radius เล็ก, tool access blocked, depth ratio มากเกิน, tolerance ผิด, unsupported feature และ assignment-hash mismatch
- สมมติฐานที่ต้องการ: record ที่ครบ/สอดคล้องและ witness ที่อยู่ใน process limit ทุกตัว replay exact; state ที่หาย ไม่สอดคล้อง ไม่รองรับ หรือเกิน envelope ทุกตัวต้อง fail ก่อนใช้กับ physics/fitness
- การหักล้าง: ยอมรับ `maximum_force` ลอย ๆ, infer fatigue evidence, เติม source ที่หายเงียบ ๆ, clip มิติ geometry ที่ fail, ใช้ synthetic fixture เป็น design material หรือรับ record hash ที่ stale

## ไฟล์ที่วางแผน

- `config/materials/engineering_material_manufacturing_v1.json`
- `src/formula_ultimate/components/engineering_contracts.py` และ component exports
- `scripts/components/validate_engineering_contracts.py`
- `tests/test_engineering_contracts.py`
- `docs/contracts/ENGINEERING_MATERIAL_MANUFACTURING_CONTRACT_V1.md` และคู่ภาษาไทย
- plan นี้และ result record คู่สองภาษา
- หลักฐานที่ ignore ใต้ `artifacts/work079/`

## การตรวจและเกณฑ์สำเร็จ

Canonical serialization/hash replay ต้อง exact Elastic constant ต้องตรง `G = E / (2*(1+nu))` ภายใน numerical tolerance ที่ประกาศ; strength ordering, thermal range, fracture/thermal property, source mapping ครบ, fatigue status และ claim boundary ต้องผ่าน Manufacturing witness ต้องแสดง margin ไม่ติดลบสำหรับ declared limit ทุกตัว และ negative control ทุกตัวต้อง fail ด้วย causal code ที่คงที่ Material/process hash แบบ exact ต้อง bind กับ assignment และ geometry witness Focused tests, full regression, compilation, bilingual contract, runner replay, scoped staging, `git diff --cached --check`, commit เดียว และ post-commit replay ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำโดยชัดแจ้ง

Internal consistency พิสูจน์ real material behavior ไม่ได้ Synthetic fixture ไม่มี design allowable, coupon scatter, anisotropy, strain-rate/environment dependence, weld/heat-treatment state, multiaxial fatigue, crack growth หรือ production capability evidence Process dimension ที่ผ่านเป็น screening rule ไม่ใช่หลักฐาน manufacturability, cost, quality, inspection, supplier capability หรือ structural safety
