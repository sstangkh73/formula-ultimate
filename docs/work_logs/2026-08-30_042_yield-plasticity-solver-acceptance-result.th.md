# ผลงาน 042: การยอมรับ Yield และ Plasticity Solver

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_042_yield-plasticity-solver-acceptance-result.md`

สถานะ: เสร็จสมบูรณ์

## ผลลัพธ์

Synthetic bilinear CalculiX acceptance ผ่าน Solver evidence มี yield transition, `PEEQ` ที่ไม่เป็นศูนย์, residual strain, unloading/reversal, reaction closure, `ELSE` internal energy, two-mesh agreement, hash และ replay metadata นี่เป็น implementation evidence เท่านั้นและห้ามใช้เป็น real design material record

## ไฟล์ที่เปลี่ยน

- `config/structural/yield_plasticity_acceptance_v1.json`
- `src/formula_ultimate/structural/plasticity.py` และ structural exports
- `scripts/structural/run_yield_plasticity_acceptance.py`
- `scripts/run_work042.ps1`
- `tests/test_plasticity_acceptance.py`
- `docs/physics/YIELD_PLASTICITY_ACCEPTANCE.md` และ `.th.md`
- matching Work 042 plan/result pair

Ignored solver evidence อยู่ใต้ `artifacts/work042/`

## การตัดสินใจและ deviation

- ใช้ deterministic structured C3D8 mesh เพื่อให้ fixture แยก constitutive behavior ออกจาก tetrahedral geometry error
- แปลง total tangent `Et` เป็น `*PLASTIC` hardening slope `H=E Et/(E-Et)`
- Integrate actual solver force-displacement endpoint แล้วเทียบกับ solver `ELSE`; ไม่ใช้ analytical energy แทน solver evidence
- Exploratory solve แรกไม่ถูก admit รอบนั้นเผย default every-increment output และ exact heading `internal energy (element, energy)` จากนั้นจึง freeze `FREQUENCY=999` และ observed parser contract ก่อน admitted rerun

## การตรวจสอบ

```powershell
py -3.14 -m unittest tests.test_plasticity_acceptance -v
# exit 0; Ran 4 tests; OK

.\scripts\run_work042.ps1
# exit 0; status=passed

py -3.14 -m unittest discover -s tests -v
# exit 0; Ran 299 tests in 19.432s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

Fine-mesh yield/tangent/plastic/residual relative error คือ `1.0145e-9`, `5.0000e-8`, `2.1739e-7` และ `2.1739e-7` Maximum reaction/energy residual คือ `1.0840e-16` และ `2.7508e-7` Response convergence metric ทั้งสามเป็นศูนย์

## ข้อจำกัดและงานต่อ

Fixture ไม่มี sourced real material, geometric concentration, temperature/rate dependence, cyclic hardening, fracture หรือ fatigue Work 043 ใช้ typed provenance requirement และ analytical material-state boundary ต่อได้ แต่ห้ามตีความ synthetic law นี้เป็น toughness evidence
