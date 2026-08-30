# ผลงาน 045: Loaded Interface และ Joint Load Path

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_045_loaded-interface-joint-load-path-result.md`

สถานะ: เสร็จสมบูรณ์

## ผลลัพธ์

Execution และ mesh/equilibrium/energy/identity hypothesis ผ่าน แต่ preferred hypothesis รวมถูกปฏิเสธเพราะ one-support compliance เปลี่ยน `299.021%`; transferability นอก exact two-support fixture ถูก block

## ไฟล์ที่เปลี่ยน

- `config/structural/loaded_interface_plate_v1.json`
- `src/formula_ultimate/structural/loaded_interface.py` และ structural exports
- `scripts/cad/generate_loaded_interface_plate.py`
- `scripts/cad/inspect_loaded_interface_freecad.py`
- `scripts/structural/run_loaded_interface_acceptance.py`
- `scripts/run_work045.ps1`
- `tests/test_loaded_interface.py`
- `docs/physics/LOADED_INTERFACE_JOINT_LOAD_PATH.md` และ `.th.md`
- matching Work 045 plan/result pair

Ignored CAD/STEP/mesh/solver evidence อยู่ใต้ `artifacts/work045/`

## การตัดสินใจและ deviation

- ใช้ geometric center/radius/axis/area signature เพราะ STEP ไม่ preserve application face label อย่างน่าเชื่อถือ
- Freeze mesh level `6/4/3 mm` ก่อนเห็น structural result
- Solver attempt แรกไม่ถูก admit เพราะ `.17g` coordinate เกิน CalculiX free-field parser limit การใช้ `.12g` แก้เฉพาะ deck interface และรักษา frozen geometry/mesh
- Replay probe พบว่า OCCT wall-clock time เป็นความต่างเดียวระหว่าง STEP ที่ geometry เหมือนกัน การ canonicalize header นั้นให้ repeat hash ตรงโดยไม่เปลี่ยน geometry
- Mesh convergence ผ่าน ส่วน one-support solve ที่เก็บไว้ reject transferability ตามกติกา

## การตรวจสอบ

```powershell
py -3.14 -m unittest tests.test_loaded_interface -v
# exit 0; Ran 3 tests; OK

.\scripts\run_work045.ps1
# exit 0; status=passed; mesh_convergence=supported; transferability=rejected

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 310 tests in 24.032s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0

# independent CAD export สองรอบหลัง canonicalization
# identical SHA-256: 6F20D310970723738ABAFB19FA212264F14A5147880144280C2DBE92502C4AEE
```

Fine baseline force/moment/energy residual คือ `4.14e-9`, `1.08e-9`, `2.28e-8` Last-two compliance change คือ `0.6959%` One-support sensitivity เปลี่ยน compliance `299.021%` และ peak von Mises จาก `5.60` เป็น `27.61 MPa`

## ข้อจำกัดและงานต่อ

Interface เป็น rigid bonded cylindrical surface ไม่ใช่ contact joint มีการรายงาน raw maximum stress แต่ไม่ promote เป็น bearing strength Gate A ยังเปิดเพราะ Work 041 cross-element convergence และ Work 045 transferability ถูก reject Work 046 ห้ามเริ่มในฐานะ promotable structural-fitness coupling จนกว่า separately numbered remediation จะแก้หรือกำหนดขอบเขต blocker ทั้งสอง
