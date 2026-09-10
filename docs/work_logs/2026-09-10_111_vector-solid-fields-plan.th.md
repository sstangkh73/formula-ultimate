# แผน Work 111: สนามของแข็งแบบ vector จาก geometry ที่สร้าง

ต้นฉบับภาษาอังกฤษ: `2026-09-10_111_vector-solid-fields-plan.md`

วันที่: 2026-09-10 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

พัฒนา tetrahedral FEM แบบ small-strain isotropic linear-elastic บน mesh จริงของ Work 110 โดยมี displacement DOFs สามค่าต่อ node, traction/body-force conventions, supports ชัดเจน, recovered reactions, vector displacement และ tensor stress fields ใช้เฉพาะวัสดุ fixture แบบ synthetic

การทดลอง admitted มี structured cuboid reference สำหรับ affine patch และเทียบ axial displacement เชิงวิเคราะห์ พร้อม geometry ไม่คุ้นเคยจาก Work 109 ผ่าน Work 110 ที่ `0.02`, `0.01` และ `0.008 m` ไม่ใช้ point maximum ที่มุมคม; stress quantity ที่ลงทะเบียนคือ element-volume-weighted p90 von Mises stress

## ตัวแปร Controls และไฟล์

- ตัวแปรอิสระ: geometry, ทิศแรง, Young's modulus และ resolution
- ตัวแปรตาม: vector displacement, compliance, p90 von Mises stress, reactions, strain energy, force/moment/energy residual และ diagonal conditioning proxy
- Controls: SI material/load/support semantics เดียวกัน; analytic cuboid; affine patch; stiffness scaling; rigid-mode, severed-path และ corrupt-stiffness failures
- สำเร็จ: solve ไม่ singular, residual gates, analytic/patch gates, last-two changes มีขอบเขต, field identities deterministic และ load/material mutations causal

ไฟล์ที่วางแผน: `src/formula_ultimate/structural/vector_solid_fields.py`, `config/development/vector_solid_fields_v1.json`, `scripts/development/run_vector_solid_fields.py`, `tests/test_vector_solid_fields.py`, `docs/contracts/VECTOR_SOLID_FIELDS_V1*` สองภาษา, plan/result นี้สองภาษา และ `artifacts/work111/run_a|run_b` ที่ ignore

## การตรวจ

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_vector_solid_fields tests.test_repository_contract -v
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_vector_solid_fields.py --config config\development\vector_solid_fields_v1.json --output-root artifacts\work111\run_a
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_vector_solid_fields.py --config config\development\vector_solid_fields_v1.json --output-root artifacts\work111\run_b --replay-reference artifacts\work111\run_a\result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน affected regressions, `git diff --check`, stage แบบระบุไฟล์, ตรวจ cached scope และ `git diff --cached --check`; commit ทันทีเมื่อทุก gate ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

Voxel geometry เปลี่ยนตาม resolution, stress ใกล้มุมขั้นบันไดอาจ singular และ diagonal proxy ไม่ใช่ spectral condition number ต้องเก็บข้อจำกัดเหล่านี้ สิ่งที่ไม่ทำ: nonlinear/contact/plastic/fatigue mechanics, certified material data, stress-convergence proof, vehicle feasibility, physical validation, ติดตั้ง dependency, push หรือเขียนประวัติใหม่
