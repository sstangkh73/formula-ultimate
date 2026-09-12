# แผน Work 116: Material Provenance และ Scoped Failure

ต้นฉบับภาษาอังกฤษ: `2026-09-12_116_material-failure-scope-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

พัฒนา material/process applicability registry ที่ trace ได้บนหลักฐาน Work 111 field, Work 114 history และ Work 115 temperature ที่ตรงกัน รักษา units, provenance, temperature/rate/history ranges, uncertainty และ process dependence ก่อนประเมิน failure law

ตรวจ bounded first-yield และ Euler-column reference laws ด้วย safe/failed และ imperfection-sensitivity fixtures Properties ของ candidate ยังเป็น synthetic ดังนั้น numerical margins เป็น diagnostic เท่านั้นและห้ามกลายเป็น measured survival evidence Fatigue, fracture และ wear ยังคงเป็น unresolved extension slots ชัดเจน

## ตัวแปร controls และไฟล์

- IV: material/process record, temperature, strain rate, load history และ column imperfection
- DV: eligibility, yield/buckling margin, uncertainty interval, sensitivity และ missing-domain coverage
- Controls: analytic yield/Euler references, known safe/failed cases, zero/increased imperfection; ปฏิเสธ out-of-range properties, missing units, unjustified mixtures และ synthetic-to-measured relabeling
- Success: ตรึง dependency evidence, law references ผ่าน, imperfection ลด buckling capacity, candidate coverage ไม่เกิน provenance, missing domains บล็อก dependent claims และ replay ตรงทุกบิต

ไฟล์ที่วางแผน: `src/formula_ultimate/structural/material_failure_scope.py`, `config/development/material_failure_scope_v1.json`, `scripts/development/run_material_failure_scope.py`, `tests/test_material_failure_scope.py`, `docs/contracts/MATERIAL_FAILURE_SCOPE_V1*` สองภาษา, plan/result นี้สองภาษา และ `artifacts/work116/run_a|run_b` แบบ ignored

## Validation

```powershell
python -m unittest tests.test_material_failure_scope tests.test_repository_contract -v
python scripts/development/run_material_failure_scope.py --config config/development/material_failure_scope_v1.json --output-root artifacts/work116/run_a
python scripts/development/run_material_failure_scope.py --config config/development/material_failure_scope_v1.json --output-root artifacts/work116/run_b --replay-reference artifacts/work116/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน affected regressions และ explicit staged/cached diff checks; commit ทันทีหลังทุก gate ผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

Reference-law verification ไม่ได้ calibrate synthetic candidate material สิ่งที่ไม่ทำ: universal constitutive behavior, fatigue life, fracture, wear, manufacturing qualification, safety certification, complete physical survival, push หรือ rewrite history
