# ผล Work 116: Material Provenance และ Scoped Failure

ต้นฉบับภาษาอังกฤษ: `2026-09-12_116_material-failure-scope-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 116 พัฒนา provenance/range/process eligibility gates พร้อม bounded first-yield และ Euler-column references ใช้ Work 111 p90 stress `8631.834378747026 Pa`, Work 114 maximum dynamic contact force `19196.837823792008 N` และ Work 115 male temperature `299.6262800251348 K` หลังตรวจ result identities

Result SHA-256 คือ `ea418059c16fdddc6f7205b0d13b35b2d0623a17e9a930d474c9133137e708aa`; replay ตรงทุกบิต Safe/failed yield และ buckling fixtures ผ่าน ส่วน imperfection ที่เพิ่มลด capacity Temperature/rate/process/relabel/mixture controls ถูกปฏิเสธ Candidate numerical margin ยังเป็น diagnostic และ claim คือ `blocked_no_measured_process-qualified_material` Fatigue, fracture และ wear ยังเป็น unresolved blockers

ไฟล์ที่เปลี่ยน: implementation/config/runner/test ตามข้อเสนอ, contract `MATERIAL_FAILURE_SCOPE_V1` สองภาษา และ plan/result นี้สองภาษา หลักฐาน ignored อยู่ที่ `artifacts/work116/run_a|run_b` ไม่พบ implementation bug ระหว่าง admitted runs

## Validation และข้อจำกัด

```powershell
python -m unittest tests.test_material_failure_scope -v
# exit 0; ผ่าน 5 tests
python -m py_compile src/formula_ultimate/structural/material_failure_scope.py scripts/development/run_material_failure_scope.py
# exit 0
python scripts/development/run_material_failure_scope.py --config config/development/material_failure_scope_v1.json --output-root artifacts/work116/run_a
# exit 0; result SHA-256 ตามข้างต้น
python scripts/development/run_material_failure_scope.py --config config/development/material_failure_scope_v1.json --output-root artifacts/work116/run_b --replay-reference artifacts/work116/run_a/result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_vector_solid_fields tests.test_moving_contact_assembly tests.test_coupled_thermal_solid tests.test_material_failure_scope tests.test_repository_contract -v
# exit 0; ผ่าน 28 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; ตรงกับไฟล์ Work 116 ที่ประกาศไว้ 10 ไฟล์
git diff --cached --check
# exit 0
```

Analytic references และ synthetic margins ไม่ยืนยัน physical survival รายงาน verified commit hash ใน final handoff
