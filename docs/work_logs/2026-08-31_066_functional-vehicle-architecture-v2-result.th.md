# ผลงาน 066: Functional Vehicle Architecture v2

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_066_functional-vehicle-architecture-v2-result.md`

สถานะ: เสร็จสมบูรณ์ (Completed)

## ผลลัพธ์

สร้าง technology-neutral functional-vehicle grammar และ reference candidate 10 components แล้ว Admission ต้องมี compatible typed ports และ explicit structural, power, thermal, control และ ground paths Component ที่ประกาศ propulsion แต่ไม่มี storage-to-ground power path จะ fail เป็น `force-from-nowhere`

Reference สร้าง STEP ต่อ component 10 ไฟล์และ assembly 10 solids หนึ่งไฟล์ CadQuery generation, independent FreeCAD import, mass-property comparison และ separate-directory deterministic replay ผ่านโดยไม่มี hidden repair

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/topology/functional_vehicle.py`
- `src/formula_ultimate/topology/__init__.py`
- `config/vehicle/functional_vehicle_architecture_v2.json`
- `scripts/cad/generate_functional_vehicle_v2.py`
- `scripts/cad/inspect_functional_vehicle_v2_freecad.py`
- `tests/test_functional_vehicle_architecture.py`
- `docs/research/FUNCTIONAL_VEHICLE_ARCHITECTURE_V2.md`
- `docs/research/FUNCTIONAL_VEHICLE_ARCHITECTURE_V2.th.md`
- bilingual plan/result ชุดนี้

Generated evidence ที่ถูก ignore อยู่ใต้ `artifacts/work066/` ไฟล์โมเดลหลักที่เปิดดูได้คือ `artifacts/work066/step/assembly.step`

## การตัดสินใจ

- Infer capabilities จาก function tags และ connected physical domains ไม่ใช่ชื่อ component หรือ vehicle layout ที่บังคับไว้
- Fixed reference เป็น evidence baseline ไม่ใช่ preferred discovered solution และไม่แทน frozen Work 062 campaign
- Functional component แต่ละชิ้นยังเป็น separate solid Primitive geometry ตั้งใจให้เพียงพอเฉพาะ architecture, packaging และ deterministic mass-property checks
- Energy และ torque conservation เป็น local fail-closed admission checks; control connections ไม่ขน power
- Geometry mismatch, invalid state, broken path หรือ replay mismatch จะถูกรายงาน ไม่ถูก repair

## หลักฐาน validation

Reference grammar validation คืน `status=passed`, `component_count=10`, `port_count=48`, `connection_count=23`, `ground_contact_count=2` และมวล `272.55249331647553 kg` Validation identity คือ `d29f5d51a9b23db2dce9c33f93539cb71afaa020709fc5bcb69b2b6ebaa27677`

คำสั่ง:

```powershell
py -3.14 -m unittest tests.test_functional_vehicle_architecture -q
```

Exit status `0`; output: `Ran 7 tests ... OK` Negative controls ครอบคลุม power/structural/thermal/control paths ที่หายไป, port incompatibility, invalid limits, การสร้าง power/torque ที่ไม่ได้ประกาศ, overlap, ports อยู่นอก solids, invalid ground elevation, connection length เกินค่า และ cylinder-axis inertia

คำสั่ง:

```powershell
.\.tools\cadquery-mcp\Scripts\python.exe scripts/cad/generate_functional_vehicle_v2.py --config config/vehicle/functional_vehicle_architecture_v2.json --output-root artifacts/work066/step --manifest artifacts/work066/cadquery_manifest.json
```

Exit status `0`; สร้าง valid components 10 ชิ้นและ valid assembly 10 solids Assembly SHA-256: `983902b813ab6ee3fd69c703521ee32206e224b98013f430d1aeee7249ac75da`

คำสั่ง:

```powershell
& 'C:\Program Files\FreeCAD 1.1\bin\python.exe' scripts/cad/inspect_functional_vehicle_v2_freecad.py artifacts/work066/cadquery_manifest.json config/vehicle/functional_vehicle_architecture_v2.json artifacts/work066/freecad_report.json
```

Exit status `0`; FreeCAD 1.1.3 ยืนยัน valid solids 10 ชิ้นอย่างอิสระ Relative residuals คือ mass `2.0855952616365914e-16`, centre `1.2421529906547113e-17` และ inertia `7.979411838121619e-18` ทุกค่าต่ำกว่า `1e-6`

Generation และ inspection เดิมถูกรันซ้ำใต้ `artifacts/work066/replay/` Exit status เป็น `0`; assembly hash และ component hashes ทั้ง 10 รายการตรงกันทั้งหมด

คำสั่ง:

```powershell
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
```

Exit statuses เป็น `0`; full output: `Ran 388 tests ... OK`; compilation และ diff checks ไม่มี error

## ข้อจำกัดและหลักฐานที่ขัดแย้ง

ไม่พบผลที่ขัดแย้งภายใน architecture/CAD checks ที่ประกาศไว้ แต่การผ่าน checks เหล่านี้ไม่ได้แสดงว่า reference เร่งความเร็ว เลี้ยว เบรก ระบายความร้อน ทนแรง หรือจบการแข่งขันได้ Component limits เป็น synthetic declarations ไม่ใช่ measured maps หรือ certified allowables Model ยังไม่มี transient dynamics, electrical state, torque-speed behavior, shaft compliance, tyre slip, suspension, detailed joints, thermal state, nonlinear material response, fatigue, fracture, buckling, crashworthiness, manufacturability และ safety validation Level 0 กับ primitive CAD ปิด claims เหล่านี้ไม่ได้

## งานถัดไป

Work 067 ควรสร้างและ analytically validate coupled storage-converter-transmission dynamic path รวม state, efficiency/loss heat, torque-speed limits, inertia, compliance, failure states และ deterministic replay จากนั้นจึงเชื่อม path นี้กับ ground-force/slip, steering/braking, thermal และ structural solvers ก่อนอ้าง whole-car optimization
