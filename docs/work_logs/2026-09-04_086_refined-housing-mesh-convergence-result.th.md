# ผล Work 086: Refined Housing Mesh Convergence

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_086_refined-housing-mesh-convergence-result.md`

## สถานะและผลลัพธ์

สถานะ: Completed

การทดลอง mesh ใหม่ที่ตรึงไว้แก้ convergence failure เพียงรายการเดียวของ Work 085 โดยไม่ผ่อน gate `12%` Runner ตรวจไฟล์หลักฐาน failure exact สร้างค่าการเปลี่ยน housing displacement `13.187908211258156%` ซ้ำ สร้าง config ที่เปลี่ยนเฉพาะ `cases[2].mesh_levels_m` และรัน Gmsh/CalculiX ใหม่ทั้งเก้ากรณี

เมื่อใช้ housing mesh `4.5/3.5/2.75 mm` การเปลี่ยนสองระดับสุดท้ายคือ displacement `6.528877212806262%`, compliance `5.626733597565592%` และ p90 stress `0.5739008104203665%` ทุก metric ต่ำกว่า `12%` ทั้งสามกรณีเป็น elastic เทียบกับค่า yield synthetic `250 MPa` และ equilibrium/energy gate ทุกค่าผ่าน Root ใหม่สองชุดสร้างผลครบตรงกันแบบ exact

งานนี้ปิด blocker ซอฟต์แวร์ meshed torsion/bearing/housing ที่ Work 084/085 บันทึกไว้ ไม่เปลี่ยนสถานะในอดีต ไม่ปิด blocker ด้าน design evidence และไม่สร้าง physical validation

## ไฟล์ที่เปลี่ยน

- `config/structural/refined_housing_mesh_convergence_v1.json`
- `src/formula_ultimate/structural/refined_mesh.py`
- `scripts/structural/run_refined_housing_mesh.py`
- `tests/test_refined_housing_mesh.py`
- result นี้และไฟล์คู่ภาษาไทย
- แผน Work 086 และไฟล์คู่ภาษาไทย ซึ่งเปลี่ยนเป็น `Completed`

Derived config และ solver/replay evidence ที่สร้างใต้ `artifacts/work086/` ถูก ignore และไม่ได้ commit

## หลักฐาน exact

- SHA-256 ของ prior failed evidence: `71244cf626bc593f953dc5c37329541eb55462340a6c28885601b4d733f2c247`
- ตัวตน derived generalized solver config: `0d3d6b707b2d738d70d05d85a14628737f0d546097a4cb0776ebb1cb054866de`
- ตัวตน refinement result: `ec818c21ea45f4a129f762bac3130e06628c7b560bb1d74dff8a8c9555cdf827`
- SHA-256 ของ result JSON ที่เหมือนกันทุกไบต์: `0c4930b49e6d77189f24e6a752ae8b14664c1bc9c6c054349d01a74be1636e64`
- Replay identity: `b00c72af7f899918641a27ade27ac23780b1f630fc0851c2c596343a72558fdf`, `exact=true`
- Fine housing mesh: `11789` nodes, `49282` tetrahedra, displacement `8.697399879757787e-7 m`, compliance `8.061086986709912e-9 m/N`, p90 stress `313161.0272046963 Pa`
- Fine shaft mesh: p90 stress `144476407.7862506 Pa` ต่ำกว่า synthetic yield แต่ไม่ใช่ design claim
- force/moment/energy residual สูงสุดยังต่ำกว่า `1e-5/1e-5/1e-4`

## คำสั่ง validation และผล exact

```powershell
python scripts\structural\run_refined_housing_mesh.py `
  --config config\structural\refined_housing_mesh_convergence_v1.json `
  --output-root artifacts\work086\run_a `
  --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" `
  --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
# exit 0; result_sha256=ec818c21ea45f4a129f762bac3130e06628c7b560bb1d74dff8a8c9555cdf827

python scripts\structural\run_refined_housing_mesh.py `
  --config config\structural\refined_housing_mesh_convergence_v1.json `
  --output-root artifacts\work086\run_b `
  --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" `
  --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe" `
  --replay-reference artifacts\work086\run_a\result.json
# exit 0; replay_exact=true

python -m unittest tests.test_refined_housing_mesh tests.test_generalized_structural_coupling tests.test_repository_contract -v
# exit 0; Ran 27 tests; OK

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; Ran 598 tests in 343.349s; OK (skipped=3)
```

## การทบทวนหลักฐานและข้อจำกัด

หลักฐานสนับสนุน: ตัวตน input ที่ล้มเหลวแบบ exact, gate ที่ไม่เปลี่ยน, การแปลง config เพียง path เดียว, solve converge เก้ารอบ, last-two metrics ผ่านสามค่าต่อกรณี และ exact replay หลักฐานที่ขัดแย้ง: fine shaft p90 stress อยู่ประมาณ `57.8%` ของค่า yield synthetic และควรศึกษา element/contact/fatigue เพิ่ม ไม่ใช่ physical margin ที่สบาย คำอธิบายทางเลือก: convergence ที่เห็นอาจยังขึ้นกับ element family เพราะทุก solve ใช้ first-order C3D4 tetrahedra หลักฐานที่ยังขาดคือข้อมูลวัสดุ/กระบวนการที่ใช้ design ได้, การเทียบ solver/element อิสระ, nonlinear contact, fatigue/fracture, fastener, bearing life, manufacturing tolerance และ physical test

งานถัดไปอาจ integrate Works 083/084 ได้เฉพาะเป็น synthetic fixture ที่ล็อกตัวตน Verdict ต้องยัง non-admitted จนกว่า blocker ด้าน material/process evidence จะได้รับการแก้แยกต่างหาก
