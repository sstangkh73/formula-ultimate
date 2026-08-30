# ผลงาน 049: Fixed-Topology End-to-End Whole-Vehicle Baseline

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_049_fixed-topology-end-to-end-baseline-result.md`

## ผลลัพธ์

Reviewed fixed baseline ผ่าน bounded CAD-to-Level-0 chain ปัจจุบันครบ Reference และ heavy control finish; weak/disconnected control ให้ explicit `DNF` Timestep และ declared-capacity sensitivity ผ่าน frozen gate และ same-input replay exact ผลนี้ validate orchestration ไม่ใช่ whole-vehicle stress หรือ physical feasibility

## ไฟล์ที่เปลี่ยน

- `config/vehicle/fixed_topology_end_to_end_baseline_v1.json`
- `src/formula_ultimate/experiments/whole_vehicle_baseline.py` และ experiment exports
- `scripts/experiments/run_whole_vehicle_baseline.py`
- `scripts/run_work049.ps1`
- `tests/test_whole_vehicle_baseline.py`
- `docs/reports/FIXED_TOPOLOGY_END_TO_END_BASELINE.md` และ `.th.md`
- plan/result record สองภาษาของ Work 049

Ignored evidence อยู่ใต้ `artifacts/work049/`

## การตัดสินใจและหลักฐาน

- Reference: `finished`, `40.0 s`, `108000 J`, maximum utilization `0.715678478993928`
- Heavy control: `finished`, `43.81780460041329 s`, `128763.56092008266 J`, maximum utilization `0.8588141747927136`
- Weak control: `DNF` จาก structural failure; disconnected control: `DNF` จาก explicit load-path loss
- Finish-time relative change `0`; declared-capacity sensitivity `0.007035175879396918` ต่ำกว่า `0.01`
- Reference/matrix replay SHA-256 คือ `12774be503f21212cd35cc10b48f1eb60ab5740005ab264dfa17b35f87eb1097` และ `237b2454eb0d4d83c750177ce96964d3fdadbcf52e456687f47e2c43f28fb71c`
- Malformed/unregistered control สี่กรณี fail closed
- Incomplete-case control รอบแรกลบ overload control แทน nominal case Runner reject premise ของ test อย่างถูกต้อง Fixture ถูกแก้ให้ลบ named training case โดยไม่เปลี่ยน evaluator logic/threshold

## การตรวจสอบแบบ exact

```powershell
py -3.14 -m unittest tests.test_whole_vehicle_baseline -v
# exit 0; Ran 4 tests; OK

.\scripts\run_work049.ps1
# exit 0; reference=finished; weak=DNF; disconnected=DNF; heavy=finished
# reference_time_s=40.0; heavy_time_s=43.81780460041329
# timestep_relative=0; structural_relative=0.007035175879396918
# replay=exact; negative_controls=4

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 330 tests in 33.589s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

Staged check, explicit commit และ clean-tree replay จะทำหลัง record นี้มีอยู่จริงและรายงานใน final handoff

## ข้อจำกัดและงานต่อไป

Baseline นี้ใช้ synthetic `1000 m` Level 0 fixture และ analytical capacity sensitivity ไม่มี whole-vehicle stress FEA, independent refined evaluator, transient/contact/aero fidelity, physical calibration, real circuit, safety หรือ manufacturing evidence Work 050 ทดสอบ proposal/evaluation fairness ได้ แต่ต้องคืน `not_ready` หาก blocker เหล่านี้ยังอยู่
