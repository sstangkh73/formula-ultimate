# ผลงาน 047: Topology-Neutral Whole-Vehicle CAD และ Assembly Grammar

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_047_topology-neutral-vehicle-assembly-result.md`

## ผลลัพธ์

Implement และ validate v1 topology-neutral multi-solid assembly grammar แล้ว Fixture สี่ solid หนึ่ง contact ผ่าน explicit interface, connection, energy/load path, envelope, keep-out, ground, deterministic STEP, FreeCAD validity และ mass-property gate

## ไฟล์ที่เปลี่ยน

- `config/vehicle/topology_neutral_vehicle_v1.json`
- `src/formula_ultimate/topology/vehicle_assembly.py` และ exports
- `scripts/cad/generate_vehicle_assembly.py`
- `scripts/cad/inspect_vehicle_assembly_freecad.py`
- `scripts/topology/run_vehicle_assembly_acceptance.py`
- `scripts/run_work047.ps1`
- `tests/test_vehicle_assembly.py`
- `docs/physics/TOPOLOGY_NEUTRAL_VEHICLE_ASSEMBLY.md` และ `.th.md`
- plan/result record สองภาษาของ Work 047

Ignored CAD/STEP evidence อยู่ใต้ `artifacts/work047/`

## การตัดสินใจและหลักฐาน

- ใช้ primitive function tag และ variable declaration แทน conventional-car schema
- ใช้ per-component STEP hash/signature เพราะไม่เชื่อ STEP label เป็น identity
- Valid solid สี่ชิ้นและ explicit contact หนึ่งจุดให้ mass `30.657168026350796 kg`
- Maximum mass/centre/inertia relative error `1.7042240975184457e-15`; interface residual `1.3877787807814457e-17 m`
- Export อิสระสองรอบให้ assembly SHA-256 ตรงกัน `f60bb686dfaca51c06bed8b1b086418c5f9ce2208d861b5b2ff18d8f845f18b9`
- Negative control แปดกรณี fail closed
- Exploratory cylinder รอบแรกใช้ `both=True`, ทำให้ความสูงเป็นสองเท่าและ mass ต่าง `4.43%` FreeCAD เปิดเผย defect รอบนั้นไม่ admit และแก้ generator โดยไม่เปลี่ยน declaration/threshold
- Combined temp-probe command ที่มี recursive deletion ถูก host safety policy ปฏิเสธ จึง rerun ใน explicit artifact directory โดยไม่มี deletion นั้น

## การตรวจสอบแบบ exact

```powershell
py -3.14 -m unittest tests.test_vehicle_assembly tests.test_repository_contract -v
# exit 0; Ran 9 tests; OK

.\scripts\run_work047.ps1
# exit 0; status=passed; solid_count=4; mass_kg=30.657168026350796
# max_mass_property_error=1.7042240975184457e-15
# replay=exact; negative_controls=8

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 322 tests in 35.715s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

Repository-contract check, staged `git diff --cached --check`, explicit commit และ clean-tree Work 047 replay จะตรวจหลัง record นี้มีอยู่จริงและรายงานใน final handoff

## ข้อจำกัดและงานต่อไป

Grammar v1 เป็น primitive และ translation-only ยังไม่มี arbitrary orientation, free-form solid, physical joint, contact mechanics, FEA load case, aero/thermal evidence, manufacturing constraint หรือ physical validation Work 048 ใช้ exact mass/inertia/interface identity ต่อได้ แต่ห้ามสรุป strength หรือ race fitness จาก geometric admission
