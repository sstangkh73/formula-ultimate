# ผล Work 082: Geometry-to-Structural Physics Coupling V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-03_082_geometry-structural-coupling-v1-result.md`

## สถานะและคำตัดสิน

สถานะ: Completed

คำตัดสิน: exact STEP/interface identity ของ bracket จาก Work 081 ขับการทดลอง software-coupling ด้วย Gmsh/CalculiX สามระดับจริงแล้ว residual/refinement gate ผ่านทั้งหมด reference ยังอยู่ในโดเมน elastic แบบ synthetic และ connection critical ที่ถูกตัดลบ transmitted wrench พร้อมให้ `dnf` เชิงสาเหตุ เนื่องจากวัสดุที่ผูกเป็น synthetic จึงมี `design_use_allowed=false`; ไม่ใช่ real-part capacity

## ไฟล์ที่เปลี่ยน

- `config/structural/geometry_structural_coupling_v1.json`
- `src/formula_ultimate/structural/geometry_coupling.py`
- `scripts/structural/run_geometry_structural_coupling.py`
- `tests/test_geometry_structural_coupling.py`
- `docs/contracts/GEOMETRY_STRUCTURAL_COUPLING_V1.md` และไฟล์ภาษาไทย
- ผลฉบับนี้และไฟล์ภาษาไทย
- แผน Work 082 และไฟล์ภาษาไทย ซึ่งเป็น `Completed`

mesh, deck, DAT, FRD และ result evidence ที่สร้างยังถูก ignore ใต้ `artifacts/work082/`

## หลักฐานและการตัดสินใจ

- ตรวจ exact hash ของ STEP, FreeCAD report, surface signature และ synthetic material record ก่อน meshing
- Gmsh import STEP และสร้าง C3D4 `2,924`, `8,542` และ `17,463` elements
- การเปลี่ยน medium-to-fine ประมาณ `1.27%` displacement, `1.11%` compliance และ `1.65%` p90 stress ต่ำกว่า `5%`
- fine residual คือแรง `4.4238208804794904e-8`, moment `2.249840148494702e-8` และ energy `3.1124177238745204e-8`
- fine displacement คือ `1.5955631992710995e-5 m`; p90 von Mises stress คือ `3.926391799777586e6 Pa`
- raw CalculiX FRD มี runtime `1UTIME` canonicalize เฉพาะ field เดียวนี้เพื่อ hash; metadata เวลาไม่มี/กำกวมจะ reject และยังเก็บ raw FRD
- รอบซ้ำได้ result identity `3b5d82a7a60f68a8420f1fe5bea9915e494cc29f98bf568e1862903e929b805a` และ result-file SHA-256 ที่ตรงกัน `48636e7c20f520d9c6800ab8a893fe4f0e9bb8d2c55acb9a22b94d056b0be44b`

หลักฐานสนับสนุน: mesh converge สามระดับ, ledger แรง/moment/energy ปิด, refinement คงที่, exact replay และ causal failure propagation หลักฐานขัดแย้ง: raw FRD byte identity เปลี่ยนเฉพาะ clock field; canonical evidence บันทึกเรื่องนี้แทนการอ้าง raw equality คำอธิบายทางเลือก: bonded constraint และ linear elasticity อาจทำให้ bounded response ดูสะอาดกว่าข้อต่อจริง หลักฐานที่ขาด: sourced material/process, contact/preload/friction, plastic redistribution, fracture, fatigue และ experiment ความเชื่อมั่นสูงสำหรับ software path นี้และต่ำสำหรับ capacity จริง

## การตรวจสอบจริง

```powershell
python scripts/structural/run_geometry_structural_coupling.py `
  --config config/structural/geometry_structural_coupling_v1.json `
  --geometry-root artifacts/work081 `
  --output-root artifacts/work082/run_d `
  --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" `
  --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
# run_d exit 0; run_e exit 0; result identity/file hash ตรงกัน

python -m unittest tests.test_geometry_structural_coupling -v
# exit 0; Ran 10 tests; OK

python -m unittest tests.test_geometry_structural_coupling tests.test_repository_contract -v
# exit 0; Ran 16 tests; OK

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; Ran 534 tests in 410.066s; OK (skipped=3)
```

## ข้อจำกัดและงานถัดไป

Work 083 ใช้ exact geometry/solver interface และ failure protocol ได้ แต่ห้ามอ้าง ground-interaction design ที่ validated ขณะที่ material/process evidence ยังเป็น synthetic candidate ดังกล่าวต้องให้คำตัดสิน non-admission หรือจัดหาหลักฐานที่มีแหล่งอ้างอิงแยก
