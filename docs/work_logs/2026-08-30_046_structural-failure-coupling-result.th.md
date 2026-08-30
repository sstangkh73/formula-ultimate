# ผลงาน 046: Structural Failure Coupling และ DNF

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_046_structural-failure-coupling-result.md`

## ผลลัพธ์

Implement และ validate bounded deterministic structural failure-coupling policy แล้ว Fixture รองรับ `intact -> degraded -> failed`, post-failure zero wrench exact, redundant redistribution, critical `DNF`, event-time refinement, retained energy residual, race arbitration, exact replay และ fail-closed invalid evidence

## ไฟล์ที่เปลี่ยน

- `config/simulation/structural_failure_coupling_v1.json`
- `src/formula_ultimate/simulation/structural_failure_coupling.py`
- simulation exports, central event typing และ whole-race structural-failure mapping
- `scripts/simulation/run_structural_failure_coupling.py`
- `scripts/run_work046.ps1`
- `tests/test_structural_failure_coupling.py`
- `docs/physics/STRUCTURAL_FAILURE_COUPLING_DNF.md` และ `.th.md`
- `docs/simulation/COUPLING_CONTRACT_AND_ARCHITECTURE.md` และ `.th.md`
- plan/result record สองภาษาของ Work 046

Ignored evidence อยู่ใต้ `artifacts/work046/`

## การตัดสินใจและหลักฐาน

- Yield ทำให้ degrade; fracture/fatigue ทำให้ fail และบังคับ six-axis wrench เป็นศูนย์ exact
- Event time เป็น `0.375 s` สำหรับ timestep `0.5/0.25/0.125 s`; relative change เป็น `0`
- Redundant topology ยัง `running`; survivor รับ `(1000,50,-20,10,5,-3)` ใน component หน่วย `N` และ `N*m`
- Critical topology ให้ `DNF` ทุก timestep
- Failure ledger `12 J` ให้ dissipated `8.399999999999999 J`, released `3.6000000000000005 J` และ residual `8.881784197001252e-16 J`
- Same-input replay ตรง exact; malformed/out-of-domain control ห้ากรณี fail closed โดยไม่มี candidate state
- Focused run ครั้งแรก reject เฉพาะ exact-decimal test expectation ของ `12*0.7`; implementation เก็บ nonzero floating residual และผ่านอยู่แล้ว จึงแก้ test/runner ให้ใช้ declared residual tolerance พร้อมคง failed wrench เป็น bitwise zero

## การตรวจสอบแบบ exact

```powershell
py -3.14 -m unittest tests.test_structural_failure_coupling tests.test_coupling_contracts tests.test_whole_race -q
# exit 0; Ran 24 tests; OK

.\scripts\run_work046.ps1
# exit 0; status=passed; event_time_s=0.375
# redundant_outcome=running; critical_outcome=DNF
# event_time_refinement_relative=0; replay=exact; negative_controls=5
# wrench_residual=8.881784197001252e-16
# energy_residual_j=8.881784197001252e-16

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 319 tests in 28.572s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0
```

Repository-contract check, staged `git diff --cached --check`, explicit scoped commit และ clean-tree Work 046 replay จะตรวจหลัง result นี้มีอยู่จริงและรายงานใน final handoff

## ข้อจำกัดและงานต่อไป

นี่คือการ validate coupling policy เท่านั้น Redistribution เป็น instantaneous; ไม่ model ปลายทาง released energy; fixture มี bounded load-path group หนึ่งกลุ่มและ exact Work 051 identity ไม่มี transient fracture, stress wave, contact/preload/friction, physical joint calibration, post-critical response, impact หรือ crash evidence Work 047 ใช้ typed contract ต่อได้แต่ห้ามขยาย claim เหล่านี้
