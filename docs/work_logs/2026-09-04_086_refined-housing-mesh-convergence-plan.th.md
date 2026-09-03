# แผน Work 086: Refined Housing Mesh Convergence

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_086_refined-housing-mesh-convergence-plan.md`

## สถานะ

สถานะ: Completed

## วัตถุประสงค์

แก้หรือยืนยัน convergence failure เพียงรายการเดียวจาก Work 085 ด้วยการทดลองใหม่ที่ตรึงไว้ คง gate `12%` และโหลด รูปทรง วัสดุ solver กับ evidence identity ทั้งหมดจาก Work 084 เปลี่ยนเฉพาะลำดับ mesh ของ `converter_housing_mount` ให้ละเอียดขึ้น

เนื่องจากนี่เป็น remedial item อีกงาน ขอบเขต integration และ whole-candidate เดิมจึงเลื่อนไป Works 087 และ 088 ตามลำดับ แผน/ผลในอดีตยังคงเดิม

## ขอบเขต

- ตรวจ SHA-256 ของหลักฐาน Work 085 ที่ล้มเหลว `71244cf626bc593f953dc5c37329541eb55462340a6c28885601b4d733f2c247` และสร้างค่าการเปลี่ยน housing displacement `13.187908211258156%` ซ้ำ
- สร้าง solver config ใหม่จากตัวตน config Work 085 `f23b487f5f053325a4e349f686f4a2e24af3281fe8de3e1caf8e83fb7a5aec11`
- คง mesh ของ shaft/support และ physical declaration ทุกค่า
- เปลี่ยนเฉพาะ mesh length ของ housing จาก `8/6/4.5 mm` เป็น `4.5/3.5/2.75 mm`
- รันทุกกรณีใหม่เพื่อให้ result ใหม่ครบในตัว แล้ว replay ภายใต้ root ใหม่รอบสอง
- คง `design_use_allowed=false` และ verdict `synthetic_meshed_verification_only`

## ไฟล์ที่วางแผนแก้ไข

- `config/structural/refined_housing_mesh_convergence_v1.json`
- `src/formula_ultimate/structural/refined_mesh.py`
- `scripts/structural/run_refined_housing_mesh.py`
- `tests/test_refined_housing_mesh.py`
- แผนนี้และไฟล์คู่ภาษาไทย
- result และไฟล์คู่ภาษาไทย
- หลักฐานที่ ignore ภายใต้ `artifacts/work086/`

## Validation และเกณฑ์สำเร็จ

- ตัวตน prior failure และ base config ตรงแบบ exact
- Derived config ต่างเฉพาะ housing mesh path ที่ประกาศ
- Solve ทั้งเก้ารอบ converge และคง force/moment `<=1e-5`, energy `<=1e-4` รวมถึง last-two metric ทุกค่า `<=12%`
- Fine p90 stress ต่ำกว่า synthetic yield หรือ fail อย่างสังเกตได้
- รันใหม่สองรอบสร้าง derived-config, solver-result และ refinement-result identity ซ้ำได้
- Focused, repository-contract, compilation และ full regression test ผ่านก่อน commit

## ความเสี่ยงและสิ่งที่ไม่ทำ

Mesh ที่ละเอียดขึ้นอาจยังอยู่นอกช่วง asymptotic หรือเพิ่มเวลา compute การผ่านไม่ใช่ physical validation และไม่สร้างหลักฐานวัสดุ/กระบวนการ, contact, fatigue, fastener, bearing life, manufacturing หรือ safety งานนี้ไม่มี integration หรือ whole-vehicle
