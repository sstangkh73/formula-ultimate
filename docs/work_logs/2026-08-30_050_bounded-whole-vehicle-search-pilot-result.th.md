# ผลงาน 050: Bounded Whole-Vehicle Search Pilot และ Readiness Review

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_050_bounded-whole-vehicle-search-pilot-result.md`

## ผลลัพธ์

รัน preregistered equal-budget pilot `288` attempts ครบ Search mechanics, exact replay, frozen holdout, ancestry, budget accounting, provenance และ exploit rejection ผ่าน Readiness decision คือ `not_ready` เพราะไม่มี `independent_refined_evaluation` ไม่มี candidate ใดเป็นผู้ชนะและไม่ authorize main campaign

## ไฟล์ที่เปลี่ยน

- `config/experiments/bounded_whole_vehicle_search_pilot_v1.json`
- `src/formula_ultimate/experiments/whole_vehicle_search.py` และ experiment exports
- `scripts/experiments/run_whole_vehicle_search_pilot.py`
- `scripts/run_work050.ps1`
- `tests/test_whole_vehicle_search.py`
- `docs/reports/BOUNDED_WHOLE_VEHICLE_SEARCH_PILOT_READINESS.md` และ `.th.md`
- plan/result record สองภาษาของ Work 050

Ignored ledger/evidence อยู่ใต้ `artifacts/work050/`

## การตัดสินใจและหลักฐาน

- `GRID`, `RANDOM`, `EVOLUTION` ใช้ `96` attempts เท่ากัน; รวม `288`
- Feasible count คือ `50`, `71`, `86`; structural failure คือ `46`, `25`, `10`
- Best provisional training time คือ `34.1204253544251/35.42349737959053/34.16703235066346 s`
- Selected candidate เก้าตัวผ่าน frozen holdout; ศูนย์ตัวมี refined-evaluator evidence
- Complete same-seed replay exact: result/replay ledger SHA-256 `15d20e607ddc0e60d6f70e5dc027be680f392a1c55c1a744edf0f1fdd0cbb7bb`
- Budget ledger SHA-256 `1c27bbe2a5917dd1334a140be3e1550d6028b3391af438bbdd6aa87bceb79224`; failure ถูกนับ
- Exploit control ห้ากรณี fail closed
- ตัด mutable density variable ก่อน admitted run เพราะ density ที่ไม่มี coupled strength evidence เป็น exploit แล้วใช้ fixed material กับ geometry scale แทน

## การตรวจสอบแบบ exact

```powershell
py -3.14 -m unittest tests.test_whole_vehicle_search -v
# exit 0; Ran 4 tests; OK

.\scripts\run_work050.ps1
# exit 0; status=passed; attempts=288
# budgets GRID=96 RANDOM=96 EVOLUTION=96
# promotions=9; holdout_passed=9; refined_passed=0
# replay=exact; decision=not_ready
# blockers=[independent_refined_evaluation]; exploit_controls=5

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 334 tests in 35.459s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

Staged check, explicit commit และ clean-tree replay จะทำหลัง record นี้มีอยู่จริงและรายงานใน final handoff

## ข้อจำกัดและงานต่อไป

นี่คือ bounded search-mechanics pilot ด้วย five-variable primitive grammar และ analytical structural proxy ไม่ authorize main campaign และไม่รองรับ claim ด้าน superiority, discovery, physical validity, safety, real-circuit, aero, thermal หรือ manufacturing งาน remediation ถัดไปที่จำเป็นคือ independent refined whole-vehicle stress/deformation evaluator ตามด้วย pilot rerun ที่รักษา gate เดิม
