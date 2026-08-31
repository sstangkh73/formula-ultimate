# ผล Work 069: โทโพโลยีฐานรองรับที่เสถียรและด่านพลวัตระนาบ

เอกสารผลภาษาไทยของแผนต้นฉบับ `2026-08-31_069_stable-support-topology-planar-gate-plan.md`

สถานะ: เสร็จสมบูรณ์

เอกสารต้นฉบับภาษาอังกฤษ: `2026-08-31_069_stable-support-topology-planar-gate-result.md`

## ผลลัพธ์

สถาปัตยกรรมสองจุดสัมผัส v2 ที่ตรึงไว้ถูกปฏิเสธอย่างถูกต้องว่าไม่เสถียรทางสถิต สถาปัตยกรรม v3 แยกต่างหากเพิ่มฐานรองรับหลังแบบ passive หนึ่งจุด ผ่าน functional architecture contract สร้าง support polygon พื้นที่บวกที่ครอบภาพฉายจุดศูนย์กลางมวลจาก geometry ผ่านกรณีโหลดสถิต/กึ่งสถิตที่ประกาศ แสดงกรณี contact lift โดยไม่ clip และให้การตอบสนองการเลี้ยวระนาบที่ bounded และมีเครื่องหมายถูกต้อง

geometry ที่ materialize ชุดเดียวกันสร้าง STEP solids deterministic `11` ชิ้น FreeCAD import แยกอิสระแล้วได้มวล จุดศูนย์กลาง และ inertia รวมตรงกัน โดย residual สัมพัทธ์สูงสุด `5.000115436834047e-16` เทียบ tolerance `1e-6`

## ไฟล์ที่เปลี่ยน

- `config/vehicle/functional_vehicle_architecture_v3_planar.json`
- `config/vehicle/planar_support_gate_v1.json`
- `src/formula_ultimate/simulation/planar_support_gate.py`
- `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_planar_support_gate.py`
- `tests/test_planar_support_gate.py`
- `docs/research/STABLE_SUPPORT_TOPOLOGY_PLANAR_GATE_V1.md`
- `docs/research/STABLE_SUPPORT_TOPOLOGY_PLANAR_GATE_V1.th.md`
- บันทึกแผน/ผล Work 069 สองภาษาที่ตรงกัน

หลักฐานที่ generate อยู่ใต้ `artifacts/work069/` ซึ่ง git ignore ได้แก่ materialized architecture, experiment JSON, component/assembly STEP, CadQuery manifest, FreeCAD report และ replay tree อิสระ

## การตัดสินใจและหลักฐาน

- v2 support margin: `-0.4749520887695175 m`; สถานะ `unstable`
- v3 support area: `0.32000000000000006 m^2`; margin `0.15751201265152398 m`; สถานะ `stable`
- มวล v3: `276.89543100079806 kg`; contacts: `3`; components: `11`
- แรงต่ำสุดในกรณีกึ่งสถิตที่อนุมัติ: `343.2099673452492 N`
- excessive lateral control: แรงต่ำสุด `-254.24190827234736 N`; สถานะ `contact_lift`
- การเลี้ยว `0.02 rad` ด้านบวก: heading สุดท้าย `0.1731027912670698 rad`; yaw rate `0.5736686138311934 rad/s`
- zero steer คง lateral position, heading, lateral velocity และ yaw rate เป็นศูนย์ตรง ๆ; การเลี้ยวลบขนาดเท่ากันให้สถานะแนวข้างที่เลือกตรงข้ามกันพอดี
- planar contact utilization สูงสุด: `1.0000000000000002` อนุมัติภายใน roundoff `1e-12`
- ความต่างสัมพัทธ์สูงสุดเมื่อแบ่ง step ครึ่ง: `0.001216322032258299` ต่ำกว่า `0.02`
- Experiment evidence SHA-256: `d3a480c4637f5955668259d7e3b52b8bc474ce084a32359964558d4c624a81b5`
- Materialized architecture SHA-256: `cf78a1c499790aed6c8b117c8f583a427a9d91a9fb36605e2b7038b2907b1418`
- Assembly STEP SHA-256: `a260b74185fbd473ef33fb0e71387121af25c045609a4007347e3256b3affaf4`
- replay ให้ architecture bytes, evidence hash, assembly hash, STEP hash ทุก component และมวล FreeCAD ตรงกันทั้งหมด

## คำสั่ง validation ที่ใช้จริงและสถานะ

```powershell
python -m unittest tests.test_planar_support_gate -v
# exit 0; Ran 8 tests; OK

python scripts/experiments/run_planar_support_gate.py --config config/vehicle/planar_support_gate_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work069/materialized_architecture_v3.json --output artifacts/work069/experiment_evidence.json
# exit 0; status passed

.\.tools\cadquery-mcp\Scripts\python.exe scripts/cad/generate_functional_vehicle_v2.py --config artifacts/work069/materialized_architecture_v3.json --output-root artifacts/work069/step --manifest artifacts/work069/cadquery_manifest.json
# exit 0; component_count 11; status passed

& 'C:\Program Files\FreeCAD 1.1\bin\python.exe' scripts/cad/inspect_functional_vehicle_v2_freecad.py artifacts/work069/cadquery_manifest.json artifacts/work069/materialized_architecture_v3.json artifacts/work069/freecad_report.json
# exit 0; component_count 11; maximum_residual 5.000115436834047e-16; status passed

# ทำคำสั่ง experiment, CadQuery และ FreeCAD ซ้ำใต้ artifacts/work069/replay
# ผลเปรียบเทียบ: evidence_exact=true, architecture_bytes_exact=true,
# assembly_exact=true, component_hashes_exact=true, freecad_mass_exact=true

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests
# exit 0; Ran 412 tests in 36.327s; OK
```

## ข้อจำกัดและงานถัดไป

งานนี้ยังเป็นหลักฐานสังเคราะห์ Level 0 ใช้ฐานรองรับ rigid quasi-static, cornering stiffness/friction คงที่ ไม่มี suspension transient ไม่มีการวัดยาง ไม่มี aerodynamic transient และไม่มีการ validate โลกจริง specimen ที่อนุมัติ `0.02 rad` ไม่ได้พิสูจน์ว่าคำสั่งเลี้ยวทุกขนาดปลอดภัย; การสำรวจ `0.04 rad` ทำให้ contact lift

ความเร็วขับเคลื่อนซ้าย/ขวาอิสระยังถูกเลื่อนอย่างตั้งใจ Work 070 ต้องนิยาม differential/carrier energy และ inertia contract ก่อนแยกเพลา output ร่วมจาก Work 067 คำกล่าวอ้าง whole-race ยังถูก block จนกว่าจะมี branch drivetrain model, หลักฐาน chassis/contact fidelity สูงขึ้น, circuit trajectory coupling และ physical validation
