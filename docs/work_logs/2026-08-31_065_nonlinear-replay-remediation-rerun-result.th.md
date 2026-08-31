# ผลงาน 065: Nonlinear Replay Remediation และ Fresh Rerun

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_065_nonlinear-replay-remediation-rerun-result.md`

## ผลลัพธ์

แก้ Work 064 tuple/list replay defect โดย normalize complete summary ผ่าน strict JSON ก่อนทั้ง storage และ comparison Freeze การเปลี่ยนที่ commit `729edcbfa7574a5bfa2d3aa972fb15acec7e4295`, สร้าง fresh campaign `FU-NLG-002`, รันใหม่ครบ 102 cases โดยไม่ใช้ Work 064 observations และได้ exact immediate replay Candidates 51 ตัวและ cases 102 กรณีผ่าน Work 063 geometric-nonlinearity sensitivity thresholds ทั้งหมด

## ไฟล์ที่เปลี่ยน

- `config/experiments/work062_finalist_nonlinear_execution_v2.json`
- `scripts/structural/run_whole_vehicle_nonlinear_gate.py`
- `tests/test_work062_nonlinear_execution.py`
- เอกสาร Work 065 plan, result และ research result ภาษาอังกฤษ/ไทย
- Fresh ignored evidence ใต้ `artifacts/work065/`

## คำสั่ง validation จริง

- `py -3.14 -m unittest tests.test_work062_nonlinear_execution tests.test_vehicle_nonlinear_gate -q` → exit `0`; `Ran 9 tests`, `OK`
- `py -3.14 -m unittest discover -s tests -q` ก่อน execution → exit `0`; `Ran 381 tests in 28.728s`, `OK`
- `py -3.14 -m compileall -q src scripts tests` ก่อน execution → exit `0`
- `py -3.14 scripts/structural/run_whole_vehicle_nonlinear_gate.py --artifact-root artifacts/work065` → exit `0`; 51 candidates, 102 cases, 51 candidate passes
- `py -3.14 scripts/structural/run_whole_vehicle_nonlinear_gate.py --artifact-root artifacts/work065 --verify-only` → exit `0`; replay `exact`
- `py -3.14 -m unittest discover -s tests -q` หลัง execution → exit `0`; `Ran 381 tests in 28.740s`, `OK`
- `py -3.14 -m compileall -q src scripts tests` หลัง execution → exit `0`

## หลักฐานและ review

Ledger fingerprint คือ `ffbc7eef129b5c51cb114bfa6ec849fae15617f32bbc0c022aa05e1f50825e27`; summary identity คือ `4d28434bd2a050045fdd8579bd4ce5e75ab11c827af3e0744da2d321dfd6227f` มี solver processes 306 รายการ, nonzero exits ศูนย์, missing confirmations ศูนย์ และไม่มี failure codes Maximum displacement/stress amplification เท่ากับ `1.0000299794481688` / `1.0000338606574917`; minimum yield margin เท่ากับ `358.6735825412834`

หลักฐานสนับสนุน negligible geometric-nonlinearity sensitivity เฉพาะภายใน frozen beam/load/synthetic-material domain เท่านั้น ไม่มีผลขัดกับ gate threshold แต่ margin ที่สูงมากอาจบ่งชี้ loads ไม่รุนแรงพอหรือ abstraction มีข้อจำกัด ไม่อ้าง buckling, physical validation, safety, fracture, fatigue, contact, material nonlinearity หรือ algorithm superiority Result commit และ post-commit clean-tree replay จะรายงานใน final handoff
