# ผลงาน 048: Whole-Vehicle Load Cases และ Structural Coupling

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_048_whole-vehicle-load-cases-result.md`

## ผลลัพธ์

Implement และ validate bounded quasi-static tree-wrench adapter สำหรับ exact Work 047 assembly แล้ว Frozen training/holdout เจ็ดกรณีสมดุลและยัง running; deliberate overload หนึ่งกรณีข้าม critical support capacity และ couple เข้า Work 046 เป็น `DNF` งานนี้ปิด Work 048 algebraic load-traceability gate แต่ไม่ปิดหลักฐาน whole-vehicle stress FEA ที่ยังขาด

## ไฟล์ที่เปลี่ยน

- `config/vehicle/whole_vehicle_load_cases_v1.json`
- `src/formula_ultimate/simulation/vehicle_load_cases.py` และ simulation exports
- `scripts/simulation/run_vehicle_load_cases.py`
- `scripts/run_work048.ps1`
- `tests/test_vehicle_load_cases.py`
- `docs/physics/WHOLE_VEHICLE_LOAD_CASES.md` และ `.th.md`
- plan/result record สองภาษาของ Work 048

Ignored evidence อยู่ใต้ `artifacts/work048/`

## การตัดสินใจและหลักฐาน

- Freeze training ห้ากรณีและ holdout สองกรณีก่อน Work 050; partition SHA-256 คือ `d19f8e33c1259e64632e6e89f9768fddeb8c6e54f4a204994e200037c6beba38` และ `5045fd461c740e4edc461a702dc96bf3e93fba0b4dbb0bbeeca8adcaf4d5cf41`
- Regenerated assembly STEP SHA-256 คือ `f60bb686dfaca51c06bed8b1b086418c5f9ce2208d861b5b2ff18d8f845f18b9`
- Maximum FreeCAD mass-property error `1.7042240975184457e-15`
- Maximum global/component/interface residual คือ `1.5631940186722204e-13`, `2.2737367544323206e-13` และ `0`
- Nominal เจ็ดกรณียัง `running`; deliberate overload คืน `DNF`; same-input replay hash คือ `da4848de71c19f9d76cad00cdf5013791e5b0d6f5b544293dcf9e094d782bb03`
- Malformed/unsupported control เจ็ดกรณี fail closed
- Focused test พบ early typed-result serialization ก่อน แล้ว disproved สมมติฐานว่า overload จะทำให้เสียเพียง connection เดียว Implementation เก็บ physical multi-capacity exceedance และแก้เฉพาะ test expectation ที่เจาะจงเกินจริง

## การตรวจสอบแบบ exact

```powershell
py -3.14 -m unittest tests.test_vehicle_load_cases -v
# exit 0; Ran 4 tests; OK

.\scripts\run_work048.ps1
# exit 0; status=passed; cases=8; nominal=7; overload=DNF
# max_global_residual=1.5631940186722204e-13
# max_component_residual=2.2737367544323206e-13
# mass_property_error=1.7042240975184457e-15; replay=exact; negative_controls=7

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 326 tests in 35.360s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

Staged check, explicit commit และ clean-tree replay จะทำหลัง record นี้มีอยู่จริงและรายงานใน final handoff

## ข้อจำกัดและงานต่อไป

Structural response เป็น rigid-component cut-load algebra พร้อม synthetic declared capacity ไม่ใช่ stress FEA ยังไม่มี arbitrary-geometry meshing, local stress/strain, contact, preload, friction, transient load, vibration, crash หรือ physical calibration Work 049 ทดสอบ end-to-end fixed baseline ด้วย exact evidence class นี้ได้ แต่รายงานต้องเก็บ blocker นี้ไว้สำหรับ Work 050 readiness
